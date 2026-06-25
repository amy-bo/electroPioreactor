# -*- coding: utf-8 -*-
from __future__ import annotations

import configparser
import os
import threading
from pathlib import Path

import click
from pioreactor.actions.led_intensity import led_intensity
from pioreactor.background_jobs.base import BackgroundJob
from pioreactor.cli.run import run
from pioreactor.config import config, ConfigParserMod
from pioreactor.pubsub import QOS
from pioreactor.pubsub import publish
from pioreactor.states import JobState
from pioreactor.utils.pwm import PWM
from pioreactor.whoami import get_assigned_experiment_name
from pioreactor.whoami import get_unit_name

__plugin_summary__ = "Electrolysis and CO₂ sparging control for electroPioreactors"
__plugin_version__ = "0.6.7"
__plugin_name__ = "electroPioreactor"
__plugin_author__ = "Martin Currie"
__plugin_homepage__ = "https://github.com/amy-bo/electroPioreactor"

_CONFIG_SECTION = "electropioreactor.config"

# Valid LED channels on a Pioreactor HAT. The electrolysis electrode pair is
# wired to one of these; which one is user-configurable (see _get_led_channel).
_VALID_LED_CHANNELS = ("A", "B", "C", "D")

# OD-pause owners (reasons). OD reading is paused while ANY of these is active
# and only resumed once all have released. See ElectroPioreactor._od_pausers.
_OD_PAUSE_SPARGE = "sparge"
_OD_PAUSE_ELECTROLYSIS = "electrolysis"


def od_pause_window_seconds(on_seconds: float, pause_after_seconds: float) -> float:
    """Effective OD-suppression window (seconds) measured from electrolysis-ON start.

    OD reading is paused for the whole electrolysis ON phase plus a user-defined
    settle period *after* electrolysis ends. That settle period
    (``pause_after_seconds``) is allowed to be **negative**: a negative value
    eats into the ON-phase pause so OD resumes *before* electrolysis finishes,
    letting OD be measured during (the tail of, or all of) the ON phase.

    The window is the time from ON start at which OD reading resumes::

        window = on_seconds + pause_after_seconds          (floored at 0)

    Floored at 0 because a negative window is meaningless — at and below
    ``-on_seconds`` the pause is fully cancelled and OD is never suppressed.

    Worked example, with ``on_seconds = 10``:

        pause_after = +5  -> window = 15  : OD off for the 10 s ON phase + 5 s settle
        pause_after =  0  -> window = 10  : OD off for exactly the ON phase
        pause_after = -3  -> window =  7  : OD resumes at t=7 s, 3 s BEFORE electrolysis
                                            ends -> OD measured during the tail of the ON phase
        pause_after = -10 -> window =  0  : window == 0 -> OD never paused, measured
                                            throughout electrolysis  (-10 == -on_seconds)
        pause_after = -50 -> window =  0  : clamp floor; any value <= -on_seconds gives 0

    :param on_seconds: electrolysis ON-phase duration (> 0).
    :param pause_after_seconds: settle period after electrolysis ends; may be
        negative down to ``-on_seconds`` (and beyond, which also gives 0).
    :returns: seconds from ON start until OD reading should resume; ``0.0``
        means "do not pause OD at all this cycle".
    """
    return max(0.0, float(on_seconds) + float(pause_after_seconds))


class ElectroPioreactor(BackgroundJob):
    """
    Single background job for electroPioreactors.

    Drives electrolysis on a user-configured LED channel (default D) at a
    user-defined power level, cycling it ON for ``electrolysis_on_seconds`` and
    OFF for ``electrolysis_off_seconds`` (0 = continuous), and periodically
    opens a CO₂ solenoid (PWM channel configured via ``[PWM] N = relay``) for a
    user-defined duration every user-defined interval. Electrolysis is paused
    for the duration of each sparge and resumed immediately after.

    OD reading is paused during each electrolysis ON phase plus a settle window
    (``od_pause_after_electrolysis_seconds``, which may be negative — see
    :func:`od_pause_window_seconds`) and, independently, during each CO₂ sparge.
    """

    job_name = "electropioreactor"

    # `persist: True` keeps MQTT-retained values and the SQLite metadata-DB row
    # alive across job stops. Without it, BackgroundJob._clear_caches publishes
    # None to every retained topic on shutdown, leaving the Advanced modal with
    # nothing to read on remount and no fallback (precedent: dosing_automation's
    # alt_media_throughput / media_throughput).
    published_settings = {
        "electrolysis_power": {"datatype": "float", "settable": True, "persist": True},
        "electrolysis_on_seconds": {"datatype": "float", "settable": True, "persist": True},
        "electrolysis_off_seconds": {"datatype": "float", "settable": True, "persist": True},
        "od_pause_after_electrolysis_seconds": {"datatype": "float", "settable": True, "persist": True},
        "sparge_duration_seconds": {"datatype": "float", "settable": True, "persist": True},
        "sparge_interval_minutes": {"datatype": "float", "settable": True, "persist": True},
        "od_pause_after_sparge_seconds": {"datatype": "float", "settable": True, "persist": True},
        # reset_to_defaults is intentionally NOT in published_settings — Pioreactor
        # would otherwise store and replay the last True value on every restart,
        # firing a reset 2 seconds after each start. It is in the YAML for UI display
        # and handled via MQTT set/<unit>/<exp>/electropioreactor/reset_to_defaults.
        #
        # led_channel is also NOT in published_settings: it's a hardware binding
        # (which physical LED slot the electrode pair occupies), set once in
        # config.ini and read at job init. Switching it at runtime would need a
        # teardown/reinit of the LED, so it is config-only, not a live setting.
    }

    def __init__(
        self,
        unit: str,
        experiment: str,
        electrolysis_power: float = 2.5,
        electrolysis_on_seconds: float = 60.0,
        electrolysis_off_seconds: float = 0.0,
        od_pause_after_electrolysis_seconds: float = 5.0,
        sparge_duration_seconds: float = 10.0,
        sparge_interval_minutes: float = 60.0,
        od_pause_after_sparge_seconds: float = 5.0,
    ) -> None:
        super().__init__(unit=unit, experiment=experiment)
        # Timer/state attrs go BEFORE any validator that can raise.
        # BackgroundJob's exception-cleanup path calls _cancel_timers, which
        # reads these attrs; if a validator below raises before they exist,
        # cleanup masks the real ValueError with an AttributeError.
        self._is_sparging = False
        # OD reading has TWO independent pausers — the sparge cycle and the
        # electrolysis ON phase — that can overlap. A single boolean let a
        # sparge resume re-enable OD mid-electrolysis (and vice-versa). Track
        # the set of active pause owners instead; OD is only actually resumed
        # when the LAST owner releases (the set becomes empty). See
        # _pause_od_reading / _resume_od_reading.
        self._od_pausers: set[str] = set()
        self._sparge_timer: threading.Timer | None = None
        self._stop_timer: threading.Timer | None = None
        self._od_resume_timer: threading.Timer | None = None
        # Electrolysis-cycling timers/state (mirror the sparge attrs above).
        self._electrolysis_on = False
        self._electrolysis_on_timer: threading.Timer | None = None
        self._electrolysis_off_timer: threading.Timer | None = None
        self._electrolysis_od_resume_timer: threading.Timer | None = None
        self.reset_to_defaults = False

        # Hardware binding: which LED channel the electrode pair is wired to.
        # Read + validated once at init (raises ValueError on an invalid label,
        # surfacing through Pioreactor's job-start error path).
        self.led_channel = self._get_led_channel()

        self.electrolysis_power = self._clamp_power(electrolysis_power)
        if self.electrolysis_power != float(electrolysis_power):
            self.logger.info(
                f"electrolysis_power was clamped from {electrolysis_power} to "
                f"{self.electrolysis_power} (allowed range 0–{self.MAX_ELECTROLYSIS_POWER})."
            )
        self.electrolysis_on_seconds = self._positive(electrolysis_on_seconds, "electrolysis_on_seconds")
        self.electrolysis_off_seconds = self._non_negative(electrolysis_off_seconds, "electrolysis_off_seconds")
        self.od_pause_after_electrolysis_seconds = float(od_pause_after_electrolysis_seconds)
        self.sparge_duration_seconds = self._positive(sparge_duration_seconds, "sparge_duration_seconds")
        self.sparge_interval_minutes = self._positive(sparge_interval_minutes, "sparge_interval_minutes")
        self.od_pause_after_sparge_seconds = float(od_pause_after_sparge_seconds)

        pwm_channel = config.get("PWM_reverse", "relay")
        # Deferred: PWM_TO_PIN is a lazy resolver that touches DOT_PIOREACTOR env var.
        from pioreactor.hardware import PWM_TO_PIN
        self._pwm = PWM(
            PWM_TO_PIN[pwm_channel],
            hz=16,
            unit=unit,
            experiment=experiment,
            pub_client=self.pub_client,
        )
        self._pwm.lock()

    def on_init_to_ready(self) -> None:
        super().on_init_to_ready()
        # Persist startup values (which may have come from Pioreactor's config-override
        # replay) so the Advanced tab always shows what the job actually started with.
        self._save_all_config()
        self._pwm.start(0.0)
        # Electrolysis now CYCLES (ON for electrolysis_on_seconds, OFF for
        # electrolysis_off_seconds) rather than running continuously. Kick off
        # the first ON phase immediately.
        self._begin_electrolysis_on()
        self._schedule_next_sparge()

    # ── settings setters ────────────────────────────────────────────────────

    def set_electrolysis_power(self, value: float) -> None:
        self.electrolysis_power = self._clamp_power(value)
        self._save_config("electrolysis_power", self.electrolysis_power)
        # Only push the new power to the LED if electrolysis is currently driving
        # it: not while sparging (LED is forced to 0), and not during an OFF
        # phase of the electrolysis cycle (LED is intentionally 0).
        if not self._is_sparging and self._electrolysis_on:
            self._set_led(self.electrolysis_power)

    def set_electrolysis_on_seconds(self, value: float) -> None:
        self.electrolysis_on_seconds = self._positive(value, "electrolysis_on_seconds")
        self._save_config("electrolysis_on_seconds", self.electrolysis_on_seconds)
        # Like sparge duration, a mid-phase change applies to the NEXT phase,
        # not the in-flight one — we don't cancel the running ON/OFF timer.

    def set_electrolysis_off_seconds(self, value: float) -> None:
        self.electrolysis_off_seconds = self._non_negative(value, "electrolysis_off_seconds")
        self._save_config("electrolysis_off_seconds", self.electrolysis_off_seconds)

    def set_od_pause_after_electrolysis_seconds(self, value: float) -> None:
        self.od_pause_after_electrolysis_seconds = float(value)
        self._save_config(
            "od_pause_after_electrolysis_seconds", self.od_pause_after_electrolysis_seconds
        )

    def set_sparge_duration_seconds(self, value: float) -> None:
        self.sparge_duration_seconds = self._positive(value, "sparge_duration_seconds")
        self._save_config("sparge_duration_seconds", self.sparge_duration_seconds)

    def set_sparge_interval_minutes(self, value: float) -> None:
        self.sparge_interval_minutes = self._positive(value, "sparge_interval_minutes")
        self._save_config("sparge_interval_minutes", self.sparge_interval_minutes)
        if not self._is_sparging:
            self._schedule_next_sparge()

    def set_od_pause_after_sparge_seconds(self, value: float) -> None:
        self.od_pause_after_sparge_seconds = float(value)
        self._save_config("od_pause_after_sparge_seconds", self.od_pause_after_sparge_seconds)

    def set_reset_to_defaults(self, value: bool) -> None:
        if not value:
            return
        self.logger.info("Resetting all settings to config.ini defaults.")
        self._clear_unit_config()
        self.set_electrolysis_power(
            config.getfloat(_CONFIG_SECTION, "electrolysis_power", fallback=2.5)
        )
        self.set_electrolysis_on_seconds(
            config.getfloat(_CONFIG_SECTION, "electrolysis_on_seconds", fallback=60.0)
        )
        self.set_electrolysis_off_seconds(
            config.getfloat(_CONFIG_SECTION, "electrolysis_off_seconds", fallback=0.0)
        )
        self.set_od_pause_after_electrolysis_seconds(
            config.getfloat(_CONFIG_SECTION, "od_pause_after_electrolysis_seconds", fallback=5.0)
        )
        self.set_sparge_duration_seconds(
            config.getfloat(_CONFIG_SECTION, "sparge_duration_seconds", fallback=10.0)
        )
        self.set_sparge_interval_minutes(
            config.getfloat(_CONFIG_SECTION, "sparge_interval_minutes", fallback=60.0)
        )
        self.set_od_pause_after_sparge_seconds(
            config.getfloat(_CONFIG_SECTION, "od_pause_after_sparge_seconds", fallback=5.0)
        )
        # Snap the toggle back so the YAML claim ("resets itself automatically
        # after applying") matches the in-memory state.
        self.reset_to_defaults = False

    # ── sparging cycle ───────────────────────────────────────────────────────

    def _schedule_next_sparge(self) -> None:
        if self._sparge_timer is not None:
            self._sparge_timer.cancel()
        self._sparge_timer = threading.Timer(
            self.sparge_interval_minutes * 60.0, self._begin_sparge
        )
        self._sparge_timer.daemon = True
        self._sparge_timer.start()

    def _begin_sparge(self) -> None:
        if self.state != self.READY:
            return

        self._is_sparging = True
        self.logger.info(
            f"Sparging CO₂ for {self.sparge_duration_seconds:.0f}s (electrolysis paused)"
        )
        self._set_led(0.0)
        self._pwm.change_duty_cycle(100.0)

        self._stop_timer = threading.Timer(self.sparge_duration_seconds, self._end_sparge)
        self._stop_timer.daemon = True
        self._stop_timer.start()

        # OD pause window: duration + user-defined offset, measured from sparge start.
        # A sufficiently negative offset (<= -sparge_duration) means "never pause OD".
        total_od_pause = self.sparge_duration_seconds + self.od_pause_after_sparge_seconds
        if total_od_pause > 0:
            self._pause_od_reading(_OD_PAUSE_SPARGE)
            self._od_resume_timer = threading.Timer(
                total_od_pause, self._resume_od_reading, args=(_OD_PAUSE_SPARGE,)
            )
            self._od_resume_timer.daemon = True
            self._od_resume_timer.start()

    def _end_sparge(self) -> None:
        self._pwm.change_duty_cycle(0.0)
        self._is_sparging = False
        if self.state == self.READY:
            # Only re-light the LED if electrolysis is in an ON phase right now.
            # If the sparge straddled an OFF phase, the LED must stay dark.
            if self._electrolysis_on:
                self._set_led(self.electrolysis_power)
            self.logger.debug("CO₂ sparging complete; electrolysis resumed")
            self._schedule_next_sparge()

    # ── electrolysis ON/OFF cycle ────────────────────────────────────────────
    # Electrolysis cycles ON for electrolysis_on_seconds then OFF for
    # electrolysis_off_seconds, repeating. electrolysis_off_seconds == 0 means
    # "continuous" — we keep the LED on and never schedule an OFF phase (the
    # v0.6.x behaviour, so default-config users see no change). The chain mirrors
    # the sparge timer chain above. OD reading is paused for the ON phase plus an
    # offset (od_pause_after_electrolysis_seconds, may be negative — see
    # od_pause_window_seconds), independently of the sparge OD pause.

    def _begin_electrolysis_on(self) -> None:
        if self.state != self.READY:
            return

        self._electrolysis_on = True
        if not self._is_sparging:
            # A sparge in progress owns the LED (forced to 0); don't fight it.
            # When the sparge ends, _end_sparge re-lights us because
            # _electrolysis_on is True.
            self._set_led(self.electrolysis_power)
        self.logger.debug(
            f"Electrolysis ON for {self.electrolysis_on_seconds:.0f}s "
            f"(power {self.electrolysis_power:.2f}%)"
        )

        # Pause OD for the ON phase + the (possibly negative) settle offset.
        window = od_pause_window_seconds(
            self.electrolysis_on_seconds, self.od_pause_after_electrolysis_seconds
        )
        if window > 0:
            self._pause_od_reading(_OD_PAUSE_ELECTROLYSIS)
            self._electrolysis_od_resume_timer = threading.Timer(
                window, self._resume_od_reading, args=(_OD_PAUSE_ELECTROLYSIS,)
            )
            self._electrolysis_od_resume_timer.daemon = True
            self._electrolysis_od_resume_timer.start()

        # Schedule the end of this ON phase.
        self._electrolysis_off_timer = threading.Timer(
            self.electrolysis_on_seconds, self._begin_electrolysis_off
        )
        self._electrolysis_off_timer.daemon = True
        self._electrolysis_off_timer.start()

    def _begin_electrolysis_off(self) -> None:
        if self.state != self.READY:
            return

        self._electrolysis_on = False
        if self.electrolysis_off_seconds <= 0.0:
            # Continuous mode: no OFF phase. Immediately re-enter the ON phase so
            # the LED stays lit and the cycle keeps a single ON segment going.
            self._begin_electrolysis_on()
            return

        if not self._is_sparging:
            self._set_led(0.0)
        self.logger.debug(f"Electrolysis OFF for {self.electrolysis_off_seconds:.0f}s")

        self._electrolysis_on_timer = threading.Timer(
            self.electrolysis_off_seconds, self._begin_electrolysis_on
        )
        self._electrolysis_on_timer.daemon = True
        self._electrolysis_on_timer.start()

    @property
    def _od_paused(self) -> bool:
        """Aggregate 'is OD currently paused by us' — True iff any owner holds a
        pause. Kept as a convenience/back-compat accessor over the _od_pausers
        set. Writing True registers a generic pause owner; writing False clears
        all owners (does NOT publish — use _resume_od_reading for that)."""
        return bool(self._od_pausers)

    @_od_paused.setter
    def _od_paused(self, value: bool) -> None:
        if value:
            self._od_pausers.add("_generic")
        else:
            self._od_pausers.clear()

    def _pause_od_reading(self, reason: str) -> None:
        # JobState is a StrEnum on-device — its members ARE strings; .encode()
        # turns them into the bytes paho-mqtt expects. (Earlier code used
        # .to_bytes(), which doesn't exist on str subclasses and threw on every
        # sparge cycle. Off-device tests passed because conftest stubbed JobState
        # with its own .to_bytes(); see conftest fix in same commit.)
        #
        # `reason` registers an OD-pause owner ('sparge' or 'electrolysis'). Only
        # the FIRST owner publishes SLEEPING; a second overlapping owner just
        # joins the set so it won't be resumed early by the other's resume timer.
        already_paused = bool(self._od_pausers)
        self._od_pausers.add(reason)
        if already_paused:
            return
        topic = f"pioreactor/{self.unit}/{self.experiment}/od_reading/$state/set"
        try:
            publish(topic, JobState.SLEEPING.encode(), qos=QOS.AT_LEAST_ONCE)
        except Exception as e:
            # Pausing failed: drop this owner again so we don't later think OD is
            # paused-by-us and publish a spurious READY.
            self._od_pausers.discard(reason)
            self.logger.warning(f"Could not pause od_reading: {e}")

    def _resume_od_reading(self, reason: str | None = None) -> None:
        # reason=None is an unconditional release (cleanup paths: sleep,
        # disconnect) — clear ALL owners. A specific reason releases only that
        # owner. Either way, OD is only actually resumed once NO owner remains,
        # so e.g. a sparge resume can't re-enable OD while electrolysis still
        # holds its pause.
        if not self._od_pausers:
            return
        if reason is None:
            self._od_pausers.clear()
        else:
            self._od_pausers.discard(reason)
            if self._od_pausers:
                return
        topic = f"pioreactor/{self.unit}/{self.experiment}/od_reading/$state/set"
        try:
            publish(topic, JobState.READY.encode(), qos=QOS.AT_LEAST_ONCE)
        except Exception as e:
            self.logger.warning(f"Could not resume od_reading: {e}")

    # ── lifecycle hooks ──────────────────────────────────────────────────────

    def on_ready_to_sleeping(self) -> None:
        super().on_ready_to_sleeping()
        self._is_sparging = False
        self._electrolysis_on = False
        # Each step is independently safed: a failure in one (e.g. PWM throws)
        # must not skip the others, otherwise the LED can stay on or od_reading
        # can stay paused.
        self._safe("cancel timers", self._cancel_timers)
        self._safe("close solenoid", self._pwm.change_duty_cycle, 0.0)
        self._safe("turn off LED", self._set_led, 0.0)
        self._safe("resume od_reading", self._resume_od_reading)

    def on_sleeping_to_ready(self) -> None:
        super().on_sleeping_to_ready()
        self._is_sparging = False
        # Restart the electrolysis cycle from a fresh ON phase, and the sparge.
        self._begin_electrolysis_on()
        self._schedule_next_sparge()

    def on_disconnected(self) -> None:
        super().on_disconnected()
        self._is_sparging = False
        self._electrolysis_on = False
        self._safe("cancel timers", self._cancel_timers)
        self._safe("close solenoid", self._pwm.change_duty_cycle, 0.0)
        self._safe("clean up PWM", self._pwm.clean_up)
        self._safe("turn off LED", self._set_led, 0.0)
        self._safe("resume od_reading", self._resume_od_reading)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _safe(self, what: str, fn, *args, **kwargs) -> None:
        """Call `fn(*args, **kwargs)` and log-and-swallow any exception so
        subsequent shutdown steps still run (LED off, OD resume, etc.)."""
        try:
            fn(*args, **kwargs)
        except Exception as e:
            self.logger.warning(f"Failed to {what} during cleanup: {e}")

    def _get_led_channel(self) -> str:
        """Read + validate the configured electrolysis LED channel.

        Defaults to ``D`` (the v0.6.x hardcoded channel) for backwards
        compatibility. Raises ``ValueError`` for any label that isn't one of
        A/B/C/D so a typo surfaces at job start rather than silently driving
        nothing.
        """
        raw = config.get(_CONFIG_SECTION, "led_channel", fallback="D")
        channel = str(raw).strip().upper()
        if channel not in _VALID_LED_CHANNELS:
            raise ValueError(
                f"led_channel must be one of {', '.join(_VALID_LED_CHANNELS)} "
                f"(got {raw!r})"
            )
        return channel

    def _set_led(self, intensity: float) -> None:
        led_intensity({self.led_channel: intensity}, unit=self.unit, experiment=self.experiment)

    def _cancel_timers(self) -> None:
        for attr in (
            "_sparge_timer",
            "_stop_timer",
            "_od_resume_timer",
            "_electrolysis_on_timer",
            "_electrolysis_off_timer",
            "_electrolysis_od_resume_timer",
        ):
            timer = getattr(self, attr, None)
            if timer is not None:
                timer.cancel()
                setattr(self, attr, None)

    def _config_paths(self) -> list[Path]:
        # The web UI reads config.ini + config_<unit>.ini (e.g. config_pio01.ini).
        # The job process reads config.ini + unit_config.ini.
        # We must write to both so the Advanced form and the next job start stay in sync.
        dot = Path(os.environ["DOT_PIOREACTOR"])
        return [dot / f"config_{self.unit}.ini", dot / "unit_config.ini"]

    def _atomic_write(self, path: Path, parser: configparser.ConfigParser) -> None:
        # Write to a tempfile in the same directory, then os.replace so an
        # interrupted write (power loss, kernel panic) can't truncate the file.
        tmp = path.with_suffix(path.suffix + ".tmp")
        with open(tmp, "w") as fh:
            parser.write(fh)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)

    def _save_all_config(self) -> None:
        """Write all current settable values to both config files in one pass."""
        for path in self._config_paths():
            try:
                # ConfigParserMod is Pioreactor's case-preserving subclass
                # (optionxform = str). Default ConfigParser would silently
                # lower-case existing keys (A→a, Kp→kp) on round-trip and
                # break Pioreactor's case-sensitive lookups.
                parser = ConfigParserMod()
                parser.read(path)
                if not parser.has_section(_CONFIG_SECTION):
                    parser.add_section(_CONFIG_SECTION)
                parser.set(_CONFIG_SECTION, "electrolysis_power", str(self.electrolysis_power))
                parser.set(_CONFIG_SECTION, "electrolysis_on_seconds", str(self.electrolysis_on_seconds))
                parser.set(_CONFIG_SECTION, "electrolysis_off_seconds", str(self.electrolysis_off_seconds))
                parser.set(_CONFIG_SECTION, "od_pause_after_electrolysis_seconds", str(self.od_pause_after_electrolysis_seconds))
                parser.set(_CONFIG_SECTION, "sparge_duration_seconds", str(self.sparge_duration_seconds))
                parser.set(_CONFIG_SECTION, "sparge_interval_minutes", str(self.sparge_interval_minutes))
                parser.set(_CONFIG_SECTION, "od_pause_after_sparge_seconds", str(self.od_pause_after_sparge_seconds))
                self._atomic_write(path, parser)
            except Exception as e:
                self.logger.warning(f"Could not persist settings to {path.name}: {e}")

    def _save_config(self, key: str, value: float) -> None:
        """Persist a single setting to both config files (used by runtime setters)."""
        for path in self._config_paths():
            try:
                # ConfigParserMod is Pioreactor's case-preserving subclass
                # (optionxform = str). Default ConfigParser would silently
                # lower-case existing keys (A→a, Kp→kp) on round-trip and
                # break Pioreactor's case-sensitive lookups.
                parser = ConfigParserMod()
                parser.read(path)
                if not parser.has_section(_CONFIG_SECTION):
                    parser.add_section(_CONFIG_SECTION)
                parser.set(_CONFIG_SECTION, key, str(value))
                self._atomic_write(path, parser)
            except Exception as e:
                self.logger.warning(f"Could not persist {key} to {path.name}: {e}")

    def _clear_unit_config(self) -> None:
        """Remove our section from both config files so config.ini defaults take effect."""
        for path in self._config_paths():
            try:
                # ConfigParserMod is Pioreactor's case-preserving subclass
                # (optionxform = str). Default ConfigParser would silently
                # lower-case existing keys (A→a, Kp→kp) on round-trip and
                # break Pioreactor's case-sensitive lookups.
                parser = ConfigParserMod()
                parser.read(path)
                parser.remove_section(_CONFIG_SECTION)
                self._atomic_write(path, parser)
            except Exception as e:
                self.logger.warning(f"Could not clear {path.name}: {e}")

    MAX_ELECTROLYSIS_POWER = 10.0

    @staticmethod
    def _clamp_power(value: float) -> float:
        v = float(value)
        if v < 0.0:
            return 0.0
        if v > ElectroPioreactor.MAX_ELECTROLYSIS_POWER:
            return ElectroPioreactor.MAX_ELECTROLYSIS_POWER
        return v

    @staticmethod
    def _positive(value: float, name: str) -> float:
        v = float(value)
        if v <= 0.0:
            raise ValueError(f"{name} must be > 0 (got {v})")
        return v

    @staticmethod
    def _non_negative(value: float, name: str) -> float:
        """Used for electrolysis_off_seconds: 0 is valid (= continuous, no OFF
        phase), negatives are not."""
        v = float(value)
        if v < 0.0:
            raise ValueError(f"{name} must be >= 0 (got {v})")
        return v


# ── CLI entry point ──────────────────────────────────────────────────────────
# Defaults are lambdas so they are evaluated at invocation time, after
# Pioreactor has applied any --config-override values from the Advanced panel.

@run.command(name="electropioreactor", help=__plugin_summary__)
@click.option(
    "--electrolysis-power",
    default=lambda: config.getfloat(_CONFIG_SECTION, "electrolysis_power", fallback=2.5),
    type=float,
    show_default=True,
    help="LED intensity for electrolysis on the configured channel (0–10 %).",
)
@click.option(
    "--electrolysis-on-seconds",
    default=lambda: config.getfloat(_CONFIG_SECTION, "electrolysis_on_seconds", fallback=60.0),
    type=float,
    show_default=True,
    help="Electrolysis ON-phase duration each cycle (seconds).",
)
@click.option(
    "--electrolysis-off-seconds",
    default=lambda: config.getfloat(_CONFIG_SECTION, "electrolysis_off_seconds", fallback=0.0),
    type=float,
    show_default=True,
    help="Electrolysis OFF-phase duration each cycle (seconds). 0 = continuous "
         "electrolysis (no OFF phase).",
)
@click.option(
    "--od-pause-after-electrolysis-seconds",
    default=lambda: config.getfloat(_CONFIG_SECTION, "od_pause_after_electrolysis_seconds", fallback=5.0),
    type=float,
    show_default=True,
    help="Seconds after each electrolysis ON phase ends before OD reading "
         "resumes. Negative values resume OD during electrolysis; values "
         "≤ −electrolysis_on_seconds disable this OD pause entirely.",
)
@click.option(
    "--sparge-duration-seconds",
    default=lambda: config.getfloat(_CONFIG_SECTION, "sparge_duration_seconds", fallback=10.0),
    type=float,
    show_default=True,
    help="How long to open the CO₂ solenoid each cycle (seconds).",
)
@click.option(
    "--sparge-interval-minutes",
    default=lambda: config.getfloat(_CONFIG_SECTION, "sparge_interval_minutes", fallback=60.0),
    type=float,
    show_default=True,
    help="How often to sparge (minutes).",
)
@click.option(
    "--od-pause-after-sparge-seconds",
    default=lambda: config.getfloat(_CONFIG_SECTION, "od_pause_after_sparge_seconds", fallback=5.0),
    type=float,
    show_default=True,
    help="Seconds after sparge ends before OD reading resumes. Negative values "
         "resume OD during the sparge; values ≤ −sparge_duration disable OD pausing.",
)
def click_electropioreactor(
    electrolysis_power: float,
    electrolysis_on_seconds: float,
    electrolysis_off_seconds: float,
    od_pause_after_electrolysis_seconds: float,
    sparge_duration_seconds: float,
    sparge_interval_minutes: float,
    od_pause_after_sparge_seconds: float,
) -> None:
    unit = get_unit_name()
    experiment = get_assigned_experiment_name(unit)
    job = ElectroPioreactor(
        unit=unit,
        experiment=experiment,
        electrolysis_power=electrolysis_power,
        electrolysis_on_seconds=electrolysis_on_seconds,
        electrolysis_off_seconds=electrolysis_off_seconds,
        od_pause_after_electrolysis_seconds=od_pause_after_electrolysis_seconds,
        sparge_duration_seconds=sparge_duration_seconds,
        sparge_interval_minutes=sparge_interval_minutes,
        od_pause_after_sparge_seconds=od_pause_after_sparge_seconds,
    )
    job.block_until_disconnected()
