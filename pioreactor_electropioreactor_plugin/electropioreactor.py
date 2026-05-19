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


class ElectroPioreactor(BackgroundJob):
    """
    Single background job for electroPioreactors.

    Drives electrolysis via LED channel D at a user-defined power level, and
    periodically opens a CO₂ solenoid (PWM channel 4) for a user-defined
    duration every user-defined interval. Electrolysis is paused for the
    duration of each sparge and resumed immediately after.
    """

    job_name = "electropioreactor"

    # `persist: True` keeps MQTT-retained values and the SQLite metadata-DB row
    # alive across job stops. Without it, BackgroundJob._clear_caches publishes
    # None to every retained topic on shutdown, leaving the Advanced modal with
    # nothing to read on remount and no fallback (precedent: dosing_automation's
    # alt_media_throughput / media_throughput).
    published_settings = {
        "electrolysis_power": {"datatype": "float", "settable": True, "persist": True},
        "sparge_duration_seconds": {"datatype": "float", "settable": True, "persist": True},
        "sparge_interval_minutes": {"datatype": "float", "settable": True, "persist": True},
        "od_pause_after_sparge_seconds": {"datatype": "float", "settable": True, "persist": True},
        # reset_to_defaults is intentionally NOT in published_settings — Pioreactor
        # would otherwise store and replay the last True value on every restart,
        # firing a reset 2 seconds after each start. It is in the YAML for UI display
        # and handled via MQTT set/<unit>/<exp>/electropioreactor/reset_to_defaults.
    }

    def __init__(
        self,
        unit: str,
        experiment: str,
        electrolysis_power: float = 2.5,
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
        self._od_paused = False
        self._sparge_timer: threading.Timer | None = None
        self._stop_timer: threading.Timer | None = None
        self._od_resume_timer: threading.Timer | None = None
        self.reset_to_defaults = False

        self.electrolysis_power = self._clamp_power(electrolysis_power)
        if self.electrolysis_power != float(electrolysis_power):
            self.logger.info(
                f"electrolysis_power was clamped from {electrolysis_power} to "
                f"{self.electrolysis_power} (allowed range 0–{self.MAX_ELECTROLYSIS_POWER})."
            )
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
        self._set_led_d(self.electrolysis_power)
        self._schedule_next_sparge()

    # ── settings setters ────────────────────────────────────────────────────

    def set_electrolysis_power(self, value: float) -> None:
        self.electrolysis_power = self._clamp_power(value)
        self._save_config("electrolysis_power", self.electrolysis_power)
        if not self._is_sparging:
            self._set_led_d(self.electrolysis_power)

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
        self._set_led_d(0.0)
        self._pwm.change_duty_cycle(100.0)

        self._stop_timer = threading.Timer(self.sparge_duration_seconds, self._end_sparge)
        self._stop_timer.daemon = True
        self._stop_timer.start()

        # OD pause window: duration + user-defined offset, measured from sparge start.
        # A sufficiently negative offset (<= -sparge_duration) means "never pause OD".
        total_od_pause = self.sparge_duration_seconds + self.od_pause_after_sparge_seconds
        if total_od_pause > 0:
            self._pause_od_reading()
            self._od_resume_timer = threading.Timer(total_od_pause, self._resume_od_reading)
            self._od_resume_timer.daemon = True
            self._od_resume_timer.start()

    def _end_sparge(self) -> None:
        self._pwm.change_duty_cycle(0.0)
        self._is_sparging = False
        if self.state == self.READY:
            self._set_led_d(self.electrolysis_power)
            self.logger.debug("CO₂ sparging complete; electrolysis resumed")
            self._schedule_next_sparge()

    def _pause_od_reading(self) -> None:
        # JobState is a StrEnum on-device — its members ARE strings; .encode()
        # turns them into the bytes paho-mqtt expects. (Earlier code used
        # .to_bytes(), which doesn't exist on str subclasses and threw on every
        # sparge cycle. Off-device tests passed because conftest stubbed JobState
        # with its own .to_bytes(); see conftest fix in same commit.)
        topic = f"pioreactor/{self.unit}/{self.experiment}/od_reading/$state/set"
        try:
            publish(topic, JobState.SLEEPING.encode(), qos=QOS.AT_LEAST_ONCE)
            self._od_paused = True
        except Exception as e:
            self.logger.warning(f"Could not pause od_reading: {e}")

    def _resume_od_reading(self) -> None:
        if not self._od_paused:
            return
        topic = f"pioreactor/{self.unit}/{self.experiment}/od_reading/$state/set"
        try:
            publish(topic, JobState.READY.encode(), qos=QOS.AT_LEAST_ONCE)
        except Exception as e:
            self.logger.warning(f"Could not resume od_reading: {e}")
        finally:
            self._od_paused = False

    # ── lifecycle hooks ──────────────────────────────────────────────────────

    def on_ready_to_sleeping(self) -> None:
        super().on_ready_to_sleeping()
        self._is_sparging = False
        # Each step is independently safed: a failure in one (e.g. PWM throws)
        # must not skip the others, otherwise the LED can stay on or od_reading
        # can stay paused.
        self._safe("cancel timers", self._cancel_timers)
        self._safe("close solenoid", self._pwm.change_duty_cycle, 0.0)
        self._safe("turn off LED D", self._set_led_d, 0.0)
        self._safe("resume od_reading", self._resume_od_reading)

    def on_sleeping_to_ready(self) -> None:
        super().on_sleeping_to_ready()
        self._is_sparging = False
        self._set_led_d(self.electrolysis_power)
        self._schedule_next_sparge()

    def on_disconnected(self) -> None:
        super().on_disconnected()
        self._is_sparging = False
        self._safe("cancel timers", self._cancel_timers)
        self._safe("close solenoid", self._pwm.change_duty_cycle, 0.0)
        self._safe("clean up PWM", self._pwm.clean_up)
        self._safe("turn off LED D", self._set_led_d, 0.0)
        self._safe("resume od_reading", self._resume_od_reading)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _safe(self, what: str, fn, *args, **kwargs) -> None:
        """Call `fn(*args, **kwargs)` and log-and-swallow any exception so
        subsequent shutdown steps still run (LED off, OD resume, etc.)."""
        try:
            fn(*args, **kwargs)
        except Exception as e:
            self.logger.warning(f"Failed to {what} during cleanup: {e}")

    def _set_led_d(self, intensity: float) -> None:
        led_intensity({"D": intensity}, unit=self.unit, experiment=self.experiment)

    def _cancel_timers(self) -> None:
        if self._sparge_timer is not None:
            self._sparge_timer.cancel()
            self._sparge_timer = None
        if self._stop_timer is not None:
            self._stop_timer.cancel()
            self._stop_timer = None
        if self._od_resume_timer is not None:
            self._od_resume_timer.cancel()
            self._od_resume_timer = None

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
        """Write all three current values to both config files in one pass."""
        for path in self._config_paths():
            try:
                parser = ConfigParserMod()
                parser.read(path)
                if not parser.has_section(_CONFIG_SECTION):
                    parser.add_section(_CONFIG_SECTION)
                parser.set(_CONFIG_SECTION, "electrolysis_power", str(self.electrolysis_power))
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


# ── CLI entry point ──────────────────────────────────────────────────────────
# Defaults are lambdas so they are evaluated at invocation time, after
# Pioreactor has applied any --config-override values from the Advanced panel.

@run.command(name="electropioreactor", help=__plugin_summary__)
@click.option(
    "--electrolysis-power",
    default=lambda: config.getfloat(_CONFIG_SECTION, "electrolysis_power", fallback=2.5),
    type=float,
    show_default=True,
    help="LED D intensity for electrolysis (0–10 %).",
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
        sparge_duration_seconds=sparge_duration_seconds,
        sparge_interval_minutes=sparge_interval_minutes,
        od_pause_after_sparge_seconds=od_pause_after_sparge_seconds,
    )
    job.block_until_disconnected()
