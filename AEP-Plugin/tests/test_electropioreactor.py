# -*- coding: utf-8 -*-
"""
Tests for ElectroPioreactor logic.

Hardware calls (led_intensity, PWM) are mocked by conftest.py.
threading.Timer is patched per-test so no real timers fire.
"""
import pytest
from unittest.mock import MagicMock, patch

from pioreactor_electropioreactor_plugin.electropioreactor import (
    ElectroPioreactor,
    od_pause_window_seconds,
)
from pioreactor.actions.led_intensity import led_intensity
from pioreactor.pubsub import publish as mqtt_publish


@pytest.fixture
def job():
    """
    Fully initialised ElectroPioreactor with timers and LED calls suppressed.
    Call records from __init__ / on_init_to_ready are cleared before the test body runs.
    """
    with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
        inst = ElectroPioreactor(unit="unit", experiment="exp")
        inst.on_init_to_ready()
        # on_init_to_ready starts the electrolysis cycle, which lights the LED
        # and (with the default OD-pause window) pauses od_reading. Clear that
        # init noise AND the resulting state so each test body starts clean.
        led_intensity.reset_mock()
        inst._pwm.reset_mock()
        mqtt_publish.reset_mock()
        inst._od_paused = False
        yield inst


# ── validators ────────────────────────────────────────────────────────────────

class TestValidators:
    def test_clamp_power_below_zero(self):
        assert ElectroPioreactor._clamp_power(-5) == 0.0

    def test_clamp_power_above_max(self):
        assert ElectroPioreactor._clamp_power(200) == 10.0

    def test_clamp_power_at_max(self):
        assert ElectroPioreactor._clamp_power(10.0) == 10.0

    def test_clamp_power_in_range(self):
        assert ElectroPioreactor._clamp_power(4.25) == 4.25

    def test_positive_rejects_zero(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._positive(0, "sparge_interval_minutes")

    def test_positive_rejects_negative(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._positive(-1, "sparge_duration_seconds")

    def test_positive_accepts_positive(self):
        assert ElectroPioreactor._positive(0.5, "x") == 0.5

    # ── non-finite guards (NaN/inf must never reach hardware or threading.Timer) ──
    def test_clamp_power_nan_returns_floor(self):
        # _clamp_power is a clamp, not a validator: callers don't expect a raise,
        # so non-finite maps to the safe floor 0.0 (never reaches led_intensity).
        assert ElectroPioreactor._clamp_power(float("nan")) == 0.0

    def test_clamp_power_inf_returns_floor(self):
        assert ElectroPioreactor._clamp_power(float("inf")) == 0.0
        assert ElectroPioreactor._clamp_power(float("-inf")) == 0.0

    def test_positive_rejects_nan(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._positive(float("nan"), "electrolysis_on_seconds")

    def test_positive_rejects_inf(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._positive(float("inf"), "electrolysis_on_seconds")

    def test_non_negative_rejects_nan(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._non_negative(float("nan"), "electrolysis_off_seconds")

    def test_non_negative_rejects_inf(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._non_negative(float("inf"), "electrolysis_off_seconds")

    def test_finite_offset_accepts_finite_including_negative(self):
        assert ElectroPioreactor._finite_offset(-3.0, "x") == -3.0
        assert ElectroPioreactor._finite_offset(0.0, "x") == 0.0
        assert ElectroPioreactor._finite_offset(5.0, "x") == 5.0

    def test_finite_offset_rejects_nan(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._finite_offset(float("nan"), "od_pause_after_sparge_seconds")

    def test_finite_offset_rejects_inf(self):
        with pytest.raises(ValueError):
            ElectroPioreactor._finite_offset(float("-inf"), "od_pause_after_electrolysis_seconds")


# ── settings setters ──────────────────────────────────────────────────────────

class TestSetters:
    def test_set_electrolysis_power_while_sparging_skips_led(self, job):
        job._is_sparging = True
        job.set_electrolysis_power(5.0)
        assert job.electrolysis_power == 5.0
        led_intensity.assert_not_called()

    def test_set_electrolysis_power_while_not_sparging_updates_led(self, job):
        job._is_sparging = False
        job.set_electrolysis_power(7.0)
        led_intensity.assert_called_once_with({"D": 7.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_set_electrolysis_power_clamped_to_max(self, job):
        job._is_sparging = False
        job.set_electrolysis_power(999.0)
        assert job.electrolysis_power == 10.0

    def test_set_electrolysis_power_clamped_to_0(self, job):
        job._is_sparging = False
        job.set_electrolysis_power(-5.0)
        assert job.electrolysis_power == 0.0

    def test_set_sparge_interval_reschedules_timer(self, job):
        old_timer = job._sparge_timer
        job.set_sparge_interval_minutes(30.0)
        assert job.sparge_interval_minutes == 30.0
        old_timer.cancel.assert_called_once()

    def test_set_sparge_interval_while_sparging_does_not_reschedule(self, job):
        job._is_sparging = True
        old_timer = job._sparge_timer
        job.set_sparge_interval_minutes(30.0)
        old_timer.cancel.assert_not_called()

    def test_set_sparge_duration_rejects_zero(self, job):
        with pytest.raises(ValueError):
            job.set_sparge_duration_seconds(0)


# ── sparging cycle ────────────────────────────────────────────────────────────

class TestSparging:
    def test_begin_sparge_bails_when_not_ready(self, job):
        job.state = job.SLEEPING
        job._begin_sparge()
        assert not job._is_sparging
        led_intensity.assert_not_called()
        job._pwm.change_duty_cycle.assert_not_called()

    def test_begin_sparge_opens_solenoid_and_kills_led(self, job):
        job.state = job.READY
        job._begin_sparge()
        assert job._is_sparging
        job._pwm.change_duty_cycle.assert_called_with(100.0)
        led_intensity.assert_called_with({"D": 0.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_end_sparge_closes_solenoid(self, job):
        job._is_sparging = True
        job.state = job.READY
        job._end_sparge()
        job._pwm.change_duty_cycle.assert_called_with(0.0)

    def test_end_sparge_restores_led_and_reschedules_when_ready(self, job):
        job._is_sparging = True
        job.electrolysis_power = 7.0
        job.state = job.READY
        old_timer = job._sparge_timer
        job._end_sparge()
        assert not job._is_sparging
        led_intensity.assert_called_with({"D": 7.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)
        old_timer.cancel.assert_called_once()   # _schedule_next_sparge cancels old timer

    def test_end_sparge_does_not_restore_led_when_not_ready(self, job):
        job._is_sparging = True
        job.state = job.SLEEPING
        job._end_sparge()
        assert not job._is_sparging
        led_intensity.assert_not_called()

    def test_set_sparge_duration_does_not_affect_in_flight_sparge(self, job):
        # Documented invariant (see electropioreactor.yaml description for
        # sparge_duration_seconds): mid-sparge changes apply to the next cycle,
        # not the in-flight one. A user who shortens the duration mid-sparge
        # does NOT see the current sparge end early. Pinning this here so a
        # future "fix" doesn't silently change the user-facing behaviour
        # without updating the YAML description too.
        job.state = job.READY
        job.sparge_duration_seconds = 60.0
        job._begin_sparge()
        in_flight_stop_timer = job._stop_timer

        job.set_sparge_duration_seconds(2.0)

        assert job._stop_timer is in_flight_stop_timer
        in_flight_stop_timer.cancel.assert_not_called()

    def test_begin_sparge_cancels_prior_od_resume_timer(self, job):
        # Regression: a new sparge must cancel any pending OD-resume timer from a
        # prior sparge before reassigning _od_resume_timer. Otherwise the orphan
        # fires _resume_od_reading() mid-new-sparge and escapes _cancel_timers
        # (which only ever sees the latest reference).
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = 5.0
        stale = MagicMock()
        job._od_resume_timer = stale
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_sparge()
        stale.cancel.assert_called_once()
        assert job._od_resume_timer is not stale


# ── lifecycle ─────────────────────────────────────────────────────────────────

class TestLifecycle:
    def test_sleeping_resets_is_sparging(self, job):
        job._is_sparging = True
        job.on_ready_to_sleeping()
        assert not job._is_sparging

    def test_sleeping_closes_solenoid_and_led(self, job):
        job.on_ready_to_sleeping()
        job._pwm.change_duty_cycle.assert_called_with(0.0)
        led_intensity.assert_called_with({"D": 0.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_sleeping_cancels_timers(self, job):
        sparge_timer = job._sparge_timer
        job.on_ready_to_sleeping()
        sparge_timer.cancel.assert_called_once()

    def test_resume_from_sleep_restores_led_and_reschedules(self, job):
        # By the time on_sleeping_to_ready runs, BackgroundJob has already
        # transitioned state to READY; mirror that so _begin_electrolysis_on
        # (which guards on state == READY) proceeds.
        job.state = job.READY
        job._is_sparging = True   # simulate interrupted mid-sparge
        job.electrolysis_power = 3.0
        job.on_sleeping_to_ready()
        assert not job._is_sparging
        # Resume starts a fresh electrolysis ON phase, which lights the LED.
        led_intensity.assert_called_with({"D": 3.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)


# ── reset_to_defaults ─────────────────────────────────────────────────────────

class TestResetToDefaults:
    def test_reset_applies_config_defaults(self, job):
        # The conftest getfloat stub injects DISTINCT, non-fallback values per
        # (section, key) (CONFIG_RESET_VALUES), so asserting against those proves
        # the reset actually READ config — unlike the old vacuous "fallback ==
        # fallback" compare. Pre-set values differ from the injected ones too,
        # so a no-op reset would fail.
        from conftest import CONFIG_RESET_VALUES
        job.set_electrolysis_power(99.0)
        job.set_sparge_interval_minutes(5.0)
        job.set_sparge_duration_seconds(30.0)
        job.set_reset_to_defaults(True)
        assert job.electrolysis_power == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "electrolysis_power")
        ]
        assert job.sparge_interval_minutes == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "sparge_interval_minutes")
        ]
        assert job.sparge_duration_seconds == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "sparge_duration_seconds")
        ]

    def test_reset_false_is_noop(self, job):
        job.set_electrolysis_power(5.0)
        job.set_reset_to_defaults(False)
        assert job.electrolysis_power == 5.0

    def test_reset_clears_the_toggle_after_applying(self, job):
        job.reset_to_defaults = True  # would normally arrive via __setattr__
        job.set_reset_to_defaults(True)
        assert job.reset_to_defaults is False

    def test_reset_to_defaults_is_published_and_settable(self):
        # reset_to_defaults MUST be in published_settings, otherwise the real
        # BackgroundJob._set_attr_from_message dispatcher drops the UI `set` and
        # the toggle is inert (the bug this fixes). It is published with
        # persist=False so Pioreactor doesn't retain/replay the last True value
        # on restart and fire a spurious reset.
        props = ElectroPioreactor.published_settings.get("reset_to_defaults")
        assert props is not None
        assert props["datatype"] == "boolean"
        assert props["settable"] is True
        assert props["persist"] is False

    def test_numeric_published_settings_have_persist_true(self):
        # The numeric/value settings need persist=True: without it,
        # BackgroundJob._clear_caches publishes None to each retained MQTT topic
        # on shutdown, leaving the Advanced modal showing stale values until
        # hard-refresh. reset_to_defaults is the deliberate exception (a
        # momentary action, not a stored value) and is persist=False.
        for setting, props in ElectroPioreactor.published_settings.items():
            if setting == "reset_to_defaults":
                assert props.get("persist") is False
                continue
            assert props.get("persist") is True, (
                f"{setting!r} must declare persist=True so its MQTT-retained "
                f"value survives job stop"
            )

    def test_set_via_dispatcher_drives_reset_to_defaults(self, job):
        # Drive the REAL BackgroundJob._set_attr_from_message path (the route a
        # UI/MQTT `set` actually takes) rather than calling the setter directly.
        # This is the regression guard for the "dead toggle" bug: if
        # reset_to_defaults were absent from published_settings, the dispatcher
        # would drop this message and the assert below would fail.
        from types import SimpleNamespace
        job.set_electrolysis_power(99.0)
        msg = SimpleNamespace(
            topic="pioreactor/unit/exp/electropioreactor/reset_to_defaults/set",
            payload=b"1",
        )
        job._set_attr_from_message(msg)
        from conftest import CONFIG_RESET_VALUES
        assert job.electrolysis_power == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "electrolysis_power")
        ]

    def test_set_via_dispatcher_drops_unpublished_attr(self, job):
        # The flip side: an attr NOT in published_settings is dropped by the
        # dispatcher. This is exactly why the toggle was dead before being
        # published — encoded here so the mechanism stays understood.
        from types import SimpleNamespace
        assert "led_channel" not in ElectroPioreactor.published_settings
        job.led_channel = "D"
        msg = SimpleNamespace(
            topic="pioreactor/unit/exp/electropioreactor/led_channel/set",
            payload=b"B",
        )
        job._set_attr_from_message(msg)
        assert job.led_channel == "D"  # unchanged: dispatcher dropped it


# ── OD pause during sparge ────────────────────────────────────────────────────

def _od_state_payloads(unit="unit", experiment="exp"):
    topic = f"pioreactor/{unit}/{experiment}/od_reading/$state/set"
    return [
        call.args[1].decode() if isinstance(call.args[1], (bytes, bytearray)) else str(call.args[1])
        for call in mqtt_publish.call_args_list
        if call.args and call.args[0] == topic
    ]


class TestODPause:
    def test_default_value_is_5s(self, job):
        assert job.od_pause_after_sparge_seconds == 5.0

    def test_od_pause_in_published_settings(self):
        assert "od_pause_after_sparge_seconds" in ElectroPioreactor.published_settings

    def test_setter_accepts_negative(self, job):
        job.set_od_pause_after_sparge_seconds(-30.0)
        assert job.od_pause_after_sparge_seconds == -30.0

    def test_setter_accepts_zero(self, job):
        job.set_od_pause_after_sparge_seconds(0.0)
        assert job.od_pause_after_sparge_seconds == 0.0

    def test_begin_sparge_publishes_sleeping(self, job):
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = 5.0
        job._begin_sparge()
        payloads = _od_state_payloads()
        assert "sleeping" in payloads
        assert job._od_paused is True

    def test_begin_sparge_skips_pause_when_total_is_zero(self, job):
        """delay == -sparge_duration → total pause == 0 → don't touch od_reading at all."""
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = -10.0
        job._begin_sparge()
        assert _od_state_payloads() == []
        assert job._od_paused is False

    def test_begin_sparge_skips_pause_when_total_is_negative(self, job):
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = -60.0
        job._begin_sparge()
        assert _od_state_payloads() == []

    def test_resume_timer_scheduled_at_total_pause(self, job):
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = 5.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_sparge()
            # two timers scheduled: stop at 10s, resume at 15s
            delays = [c.args[0] for c in timer_cls.call_args_list]
            assert 10.0 in delays
            assert 15.0 in delays

    def test_resume_timer_scheduled_during_sparge_for_negative_delay(self, job):
        """delay = -3 with duration 10 → resume at t=7 (while sparge still running)."""
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = -3.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_sparge()
            delays = [c.args[0] for c in timer_cls.call_args_list]
            assert 7.0 in delays

    def test_resume_od_reading_publishes_ready(self, job):
        job._od_paused = True
        job._resume_od_reading()
        assert "ready" in _od_state_payloads()
        assert job._od_paused is False

    def test_resume_od_reading_noop_when_not_paused(self, job):
        job._od_paused = False
        job._resume_od_reading()
        assert _od_state_payloads() == []

    def test_sleeping_resumes_od(self, job):
        job._od_paused = True
        job.on_ready_to_sleeping()
        assert "ready" in _od_state_payloads()
        assert job._od_paused is False

    def test_disconnect_resumes_od(self, job):
        job._od_paused = True
        job.on_disconnected()
        assert "ready" in _od_state_payloads()

    def test_cancel_timers_includes_od_resume(self, job):
        t = MagicMock()
        job._od_resume_timer = t
        job._cancel_timers()
        t.cancel.assert_called_once()
        assert job._od_resume_timer is None

    def test_reset_to_defaults_resets_od_pause(self, job):
        from conftest import CONFIG_RESET_VALUES
        job.set_od_pause_after_sparge_seconds(42.0)
        job.set_reset_to_defaults(True)
        assert job.od_pause_after_sparge_seconds == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "od_pause_after_sparge_seconds")
        ]


# ── OD-pause owner refcount (electrolysis + sparge interaction) ────────────────

class TestODPauseOwners:
    """The named feature's core defect: a single shared boolean let a sparge
    resume re-enable OD mid-electrolysis. OD pause is now reference-counted by
    owner ('sparge' / 'electrolysis'); OD only actually resumes once the LAST
    owner releases. These tests pin that model."""

    def test_second_owner_does_not_republish_sleeping(self, job):
        from pioreactor_electropioreactor_plugin.electropioreactor import (
            _OD_PAUSE_ELECTROLYSIS,
            _OD_PAUSE_SPARGE,
        )
        job._pause_od_reading(_OD_PAUSE_ELECTROLYSIS)
        first = list(_od_state_payloads())
        assert first == ["sleeping"]
        # A second, overlapping owner joins without re-publishing SLEEPING.
        job._pause_od_reading(_OD_PAUSE_SPARGE)
        assert _od_state_payloads() == ["sleeping"]
        assert job._od_pausers == {_OD_PAUSE_ELECTROLYSIS, _OD_PAUSE_SPARGE}

    def test_releasing_one_of_two_owners_does_not_resume(self, job):
        from pioreactor_electropioreactor_plugin.electropioreactor import (
            _OD_PAUSE_ELECTROLYSIS,
            _OD_PAUSE_SPARGE,
        )
        job._pause_od_reading(_OD_PAUSE_ELECTROLYSIS)
        job._pause_od_reading(_OD_PAUSE_SPARGE)
        mqtt_publish.reset_mock()
        # Sparge releases its owner; electrolysis still holds → OD must NOT resume.
        job._resume_od_reading(_OD_PAUSE_SPARGE)
        assert "ready" not in _od_state_payloads()
        assert job._od_pausers == {_OD_PAUSE_ELECTROLYSIS}

    def test_releasing_last_owner_resumes(self, job):
        from pioreactor_electropioreactor_plugin.electropioreactor import (
            _OD_PAUSE_ELECTROLYSIS,
            _OD_PAUSE_SPARGE,
        )
        job._pause_od_reading(_OD_PAUSE_ELECTROLYSIS)
        job._pause_od_reading(_OD_PAUSE_SPARGE)
        job._resume_od_reading(_OD_PAUSE_SPARGE)
        mqtt_publish.reset_mock()
        job._resume_od_reading(_OD_PAUSE_ELECTROLYSIS)
        assert "ready" in _od_state_payloads()
        assert job._od_pausers == set()

    def test_sparge_resume_does_not_resume_od_mid_electrolysis(self, job):
        """REGRESSION (the reviewer's top improvement): electrolysis OD-pause
        active → a sparge OD-pause begins → the SPARGE resume timer fires →
        OD must NOT be resumed while electrolysis still holds its pause."""
        from pioreactor_electropioreactor_plugin.electropioreactor import (
            _OD_PAUSE_ELECTROLYSIS,
            _OD_PAUSE_SPARGE,
        )
        job.state = job.READY
        job._is_sparging = False

        # 1. Electrolysis ON phase pauses OD.
        job.electrolysis_on_seconds = 60.0
        job.od_pause_after_electrolysis_seconds = 5.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_electrolysis_on()
        assert job._od_pausers == {_OD_PAUSE_ELECTROLYSIS}

        # 2. A sparge begins and also pauses OD.
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = 5.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_sparge()
        assert job._od_pausers == {_OD_PAUSE_ELECTROLYSIS, _OD_PAUSE_SPARGE}

        # 3. Fire the SPARGE resume (what the sparge resume timer would do).
        mqtt_publish.reset_mock()
        job._resume_od_reading(_OD_PAUSE_SPARGE)

        # OD must STILL be paused — electrolysis owner remains.
        assert "ready" not in _od_state_payloads()
        assert job._od_pausers == {_OD_PAUSE_ELECTROLYSIS}
        assert job._od_paused is True

    def test_begin_sparge_registers_sparge_owner(self, job):
        from pioreactor_electropioreactor_plugin.electropioreactor import _OD_PAUSE_SPARGE
        job.state = job.READY
        job.sparge_duration_seconds = 10.0
        job.od_pause_after_sparge_seconds = 5.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_sparge()
        assert _OD_PAUSE_SPARGE in job._od_pausers

    def test_begin_electrolysis_on_registers_electrolysis_owner(self, job):
        from pioreactor_electropioreactor_plugin.electropioreactor import _OD_PAUSE_ELECTROLYSIS
        job.state = job.READY
        job._is_sparging = False
        job.electrolysis_on_seconds = 10.0
        job.od_pause_after_electrolysis_seconds = 5.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_electrolysis_on()
        assert _OD_PAUSE_ELECTROLYSIS in job._od_pausers


# ── persistence smoke ─────────────────────────────────────────────────────────

class TestPersistence:
    """End-to-end check that setter -> _save_config -> file actually writes.

    The other tests heavily mock; this one exercises the real configparser +
    atomic-write path so a regression that breaks file persistence (e.g. an
    accidental no-op refactor of _save_config) is caught off-device.
    """

    def test_set_electrolysis_power_writes_to_both_config_files(self, job, tmp_path, monkeypatch):
        import configparser
        monkeypatch.setenv("DOT_PIOREACTOR", str(tmp_path))

        job.set_electrolysis_power(7.5)

        for fname in ("config_unit.ini", "unit_config.ini"):
            path = tmp_path / fname
            assert path.exists(), f"{fname} should have been created"
            parsed = configparser.ConfigParser()
            parsed.read(path)
            assert parsed.get("electropioreactor.config", "electrolysis_power") == "7.5"

    def test_save_all_config_writes_every_setting(self, job, tmp_path, monkeypatch):
        import configparser
        monkeypatch.setenv("DOT_PIOREACTOR", str(tmp_path))
        job.electrolysis_power = 3.25
        job.sparge_duration_seconds = 11.0
        job.sparge_interval_minutes = 12.5
        job.od_pause_after_sparge_seconds = -1.0

        job._save_all_config()

        path = tmp_path / "config_unit.ini"
        parsed = configparser.ConfigParser()
        parsed.read(path)
        section = parsed["electropioreactor.config"]
        assert section["electrolysis_power"] == "3.25"
        assert section["sparge_duration_seconds"] == "11.0"
        assert section["sparge_interval_minutes"] == "12.5"
        assert section["od_pause_after_sparge_seconds"] == "-1.0"


# ── pure OD-pause-window timing function (negative-pause edge cases) ───────────
# These exercise the contract WITHOUT constructing a job: od_pause_window_seconds
# is the side-effect-free core of the "OD pause around electrolysis" feature.

class TestODPauseWindowFunction:
    def test_positive_pause_extends_window_past_on_phase(self):
        # on=10, pause=+5 -> OD off for the 10s ON phase + 5s settle = 15s.
        assert od_pause_window_seconds(10.0, 5.0) == 15.0

    def test_zero_pause_equals_on_phase(self):
        # on=10, pause=0 -> OD off for exactly the ON phase.
        assert od_pause_window_seconds(10.0, 0.0) == 10.0

    def test_negative_pause_shortens_window_into_on_phase(self):
        # on=10, pause=-3 -> OD resumes at t=7s, i.e. 3s BEFORE electrolysis
        # ends, so OD is measured during the tail of the ON phase.
        assert od_pause_window_seconds(10.0, -3.0) == 7.0

    def test_negative_pause_equal_to_on_cancels_window(self):
        # on=10, pause=-10 (== -on) -> window 0 -> OD never paused; measured
        # throughout electrolysis. This is the floor boundary.
        assert od_pause_window_seconds(10.0, -10.0) == 0.0

    def test_negative_pause_beyond_on_clamps_to_zero(self):
        # on=10, pause=-50 (< -on) -> still clamped to 0, never negative.
        assert od_pause_window_seconds(10.0, -50.0) == 0.0

    def test_window_never_negative(self):
        # Property: for any inputs the window is >= 0.
        for on in (1.0, 10.0, 60.0):
            for pause in (-1000.0, -on, -1.0, 0.0, 1.0, 1000.0):
                assert od_pause_window_seconds(on, pause) >= 0.0

    def test_accepts_int_and_str_floats(self):
        assert od_pause_window_seconds(10, -3) == 7.0


# ── electrolysis ON/OFF cycling ───────────────────────────────────────────────

class TestElectrolysisCycling:
    def test_defaults(self, job):
        assert job.electrolysis_on_seconds == 60.0
        assert job.electrolysis_off_seconds == 0.0
        assert job.od_pause_after_electrolysis_seconds == 5.0

    def test_new_settings_in_published_settings(self):
        for key in (
            "electrolysis_on_seconds",
            "electrolysis_off_seconds",
            "od_pause_after_electrolysis_seconds",
        ):
            assert key in ElectroPioreactor.published_settings
            assert ElectroPioreactor.published_settings[key]["persist"] is True

    def test_begin_on_lights_led_and_schedules_off(self, job):
        job.state = job.READY
        job._is_sparging = False
        job.electrolysis_power = 6.0
        job.electrolysis_on_seconds = 30.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_electrolysis_on()
        assert job._electrolysis_on is True
        led_intensity.assert_called_with({"D": 6.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_begin_on_bails_when_not_ready(self, job):
        job.state = job.SLEEPING
        job._electrolysis_on = False
        job._begin_electrolysis_on()
        assert job._electrolysis_on is False
        led_intensity.assert_not_called()

    def test_begin_on_does_not_fight_in_flight_sparge(self, job):
        # While a sparge owns the LED (forced to 0), the ON phase must not
        # re-light it; _end_sparge re-lights when the sparge finishes.
        job.state = job.READY
        job._is_sparging = True
        job.electrolysis_power = 4.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_electrolysis_on()
        assert job._electrolysis_on is True
        led_intensity.assert_not_called()

    def test_off_phase_kills_led_and_schedules_next_on(self, job):
        job.state = job.READY
        job._is_sparging = False
        job.electrolysis_off_seconds = 20.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_electrolysis_off()
            delays = [c.args[0] for c in timer_cls.call_args_list]
        assert job._electrolysis_on is False
        led_intensity.assert_called_with({"D": 0.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)
        assert 20.0 in delays  # next ON scheduled at OFF duration

    def test_off_seconds_zero_means_continuous(self, job):
        # OFF == 0 -> no OFF phase; _begin_electrolysis_off immediately re-enters
        # the ON phase, keeping the LED lit (v0.6.x continuous behaviour).
        job.state = job.READY
        job._is_sparging = False
        job.electrolysis_off_seconds = 0.0
        job.electrolysis_power = 5.0
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            job._begin_electrolysis_off()
        assert job._electrolysis_on is True
        # last LED call is the re-light, not the 0.0 off
        led_intensity.assert_called_with({"D": 5.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_on_phase_pauses_od_for_window(self, job):
        job.state = job.READY
        job._is_sparging = False
        job._od_paused = False
        job.electrolysis_on_seconds = 10.0
        job.od_pause_after_electrolysis_seconds = 5.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_electrolysis_on()
            delays = [c.args[0] for c in timer_cls.call_args_list]
        assert "sleeping" in _od_state_payloads()
        assert job._od_paused is True
        assert 15.0 in delays   # OD resume at on+pause = 15s
        assert 10.0 in delays   # OFF transition at on = 10s

    def test_on_phase_resumes_od_during_electrolysis_for_negative_pause(self, job):
        # pause=-3, on=10 -> OD resume scheduled at t=7s, during electrolysis.
        job.state = job.READY
        job._is_sparging = False
        job._od_paused = False
        job.electrolysis_on_seconds = 10.0
        job.od_pause_after_electrolysis_seconds = -3.0
        with patch("threading.Timer") as timer_cls:
            timer_cls.side_effect = lambda *a, **kw: MagicMock()
            job._begin_electrolysis_on()
            delays = [c.args[0] for c in timer_cls.call_args_list]
        assert job._od_paused is True
        assert 7.0 in delays

    def test_on_phase_never_pauses_od_when_window_is_zero(self, job):
        # pause == -on -> window 0 -> OD not touched at all.
        job.state = job.READY
        job._is_sparging = False
        job._od_paused = False
        job.electrolysis_on_seconds = 10.0
        job.od_pause_after_electrolysis_seconds = -10.0
        job._begin_electrolysis_on()
        assert _od_state_payloads() == []
        assert job._od_paused is False

    def test_on_phase_never_pauses_od_when_window_negative(self, job):
        job.state = job.READY
        job._is_sparging = False
        job._od_paused = False
        job.electrolysis_on_seconds = 10.0
        job.od_pause_after_electrolysis_seconds = -60.0
        job._begin_electrolysis_on()
        assert _od_state_payloads() == []


# ── electrolysis-cycling setters & validators ─────────────────────────────────

class TestElectrolysisSetters:
    def test_set_on_seconds_rejects_zero(self, job):
        with pytest.raises(ValueError):
            job.set_electrolysis_on_seconds(0)

    def test_set_on_seconds_rejects_negative(self, job):
        with pytest.raises(ValueError):
            job.set_electrolysis_on_seconds(-5)

    def test_set_on_seconds_accepts_positive(self, job):
        job.set_electrolysis_on_seconds(45.0)
        assert job.electrolysis_on_seconds == 45.0

    def test_set_on_seconds_rejects_nan(self, job):
        with pytest.raises(ValueError):
            job.set_electrolysis_on_seconds(float("nan"))

    def test_set_off_seconds_rejects_inf(self, job):
        with pytest.raises(ValueError):
            job.set_electrolysis_off_seconds(float("inf"))

    def test_set_od_pause_after_electrolysis_rejects_nan(self, job):
        with pytest.raises(ValueError):
            job.set_od_pause_after_electrolysis_seconds(float("nan"))

    def test_set_od_pause_after_sparge_rejects_inf(self, job):
        with pytest.raises(ValueError):
            job.set_od_pause_after_sparge_seconds(float("inf"))

    def test_set_off_seconds_accepts_zero(self, job):
        job.set_electrolysis_off_seconds(0)
        assert job.electrolysis_off_seconds == 0.0

    def test_set_off_seconds_rejects_negative(self, job):
        with pytest.raises(ValueError):
            job.set_electrolysis_off_seconds(-1)

    def test_set_off_seconds_accepts_positive(self, job):
        job.set_electrolysis_off_seconds(15.0)
        assert job.electrolysis_off_seconds == 15.0

    def test_set_od_pause_after_electrolysis_accepts_negative(self, job):
        job.set_od_pause_after_electrolysis_seconds(-20.0)
        assert job.od_pause_after_electrolysis_seconds == -20.0

    def test_non_negative_validator(self):
        assert ElectroPioreactor._non_negative(0, "x") == 0.0
        assert ElectroPioreactor._non_negative(3.5, "x") == 3.5
        with pytest.raises(ValueError):
            ElectroPioreactor._non_negative(-0.01, "x")

    def test_set_power_during_off_phase_does_not_touch_led(self, job):
        # During an OFF phase the LED is intentionally 0; changing power must not
        # light it. (It applies on the next ON phase.)
        job._is_sparging = False
        job._electrolysis_on = False
        job.set_electrolysis_power(8.0)
        assert job.electrolysis_power == 8.0
        led_intensity.assert_not_called()

    def test_set_power_during_on_phase_updates_led(self, job):
        job._is_sparging = False
        job._electrolysis_on = True
        job.set_electrolysis_power(8.0)
        led_intensity.assert_called_once_with({"D": 8.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)


# ── configurable LED channel ──────────────────────────────────────────────────

class TestConfigurableLEDChannel:
    def test_default_channel_is_D(self, job):
        assert job.led_channel == "D"

    def test_set_led_uses_configured_channel(self, job):
        job.led_channel = "B"
        job._set_led(4.0)
        led_intensity.assert_called_with({"B": 4.0}, unit="unit", experiment="exp", pubsub_client=job.pub_client)

    def test_get_led_channel_normalises_case_and_whitespace(self, job):
        from pioreactor.config import config
        with patch.object(config, "get", side_effect=lambda *a, **kw: " c "):
            assert job._get_led_channel() == "C"

    def test_get_led_channel_rejects_invalid(self, job):
        from pioreactor.config import config
        with patch.object(config, "get", side_effect=lambda *a, **kw: "Z"):
            with pytest.raises(ValueError):
                job._get_led_channel()

    def test_invalid_channel_raises_at_init(self):
        from pioreactor.config import config
        with patch("threading.Timer", side_effect=lambda *a, **kw: MagicMock()):
            with patch.object(config, "get", side_effect=lambda *a, **kw: "Q"):
                with pytest.raises(ValueError):
                    ElectroPioreactor(unit="unit", experiment="exp")


# ── electrolysis-cycling persistence + reset ──────────────────────────────────

class TestElectrolysisPersistence:
    def test_save_all_config_includes_electrolysis_cycle_settings(self, job, tmp_path, monkeypatch):
        import configparser
        monkeypatch.setenv("DOT_PIOREACTOR", str(tmp_path))
        job.electrolysis_on_seconds = 25.0
        job.electrolysis_off_seconds = 5.0
        job.od_pause_after_electrolysis_seconds = -2.0

        job._save_all_config()

        parsed = configparser.ConfigParser()
        parsed.read(tmp_path / "config_unit.ini")
        section = parsed["electropioreactor.config"]
        assert section["electrolysis_on_seconds"] == "25.0"
        assert section["electrolysis_off_seconds"] == "5.0"
        assert section["od_pause_after_electrolysis_seconds"] == "-2.0"

    def test_reset_restores_electrolysis_cycle_defaults(self, job):
        from conftest import CONFIG_RESET_VALUES
        job.set_electrolysis_on_seconds(5.0)
        job.set_electrolysis_off_seconds(99.0)
        job.set_od_pause_after_electrolysis_seconds(42.0)
        job.set_reset_to_defaults(True)
        assert job.electrolysis_on_seconds == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "electrolysis_on_seconds")
        ]
        assert job.electrolysis_off_seconds == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "electrolysis_off_seconds")
        ]
        assert job.od_pause_after_electrolysis_seconds == CONFIG_RESET_VALUES[
            ("electropioreactor.config", "od_pause_after_electrolysis_seconds")
        ]

    def test_cancel_timers_includes_electrolysis_timers(self, job):
        t_on, t_off, t_od = MagicMock(), MagicMock(), MagicMock()
        job._electrolysis_on_timer = t_on
        job._electrolysis_off_timer = t_off
        job._electrolysis_od_resume_timer = t_od
        job._cancel_timers()
        t_on.cancel.assert_called_once()
        t_off.cancel.assert_called_once()
        t_od.cancel.assert_called_once()
        assert job._electrolysis_on_timer is None
        assert job._electrolysis_off_timer is None
        assert job._electrolysis_od_resume_timer is None
