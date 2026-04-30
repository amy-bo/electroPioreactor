# -*- coding: utf-8 -*-
"""
Tests for ElectroPioreactor logic.

Hardware calls (led_intensity, PWM) are mocked by conftest.py.
threading.Timer is patched per-test so no real timers fire.
"""
import pytest
from unittest.mock import MagicMock, patch

from pioreactor_electropioreactor_plugin.electropioreactor import ElectroPioreactor
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
        # clear init noise so assertions in tests start clean
        led_intensity.reset_mock()
        inst._pwm.reset_mock()
        mqtt_publish.reset_mock()
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
        led_intensity.assert_called_once_with({"D": 7.0}, unit="unit", experiment="exp")

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
        led_intensity.assert_called_with({"D": 0.0}, unit="unit", experiment="exp")

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
        led_intensity.assert_called_with({"D": 7.0}, unit="unit", experiment="exp")
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


# ── lifecycle ─────────────────────────────────────────────────────────────────

class TestLifecycle:
    def test_sleeping_resets_is_sparging(self, job):
        job._is_sparging = True
        job.on_ready_to_sleeping()
        assert not job._is_sparging

    def test_sleeping_closes_solenoid_and_led(self, job):
        job.on_ready_to_sleeping()
        job._pwm.change_duty_cycle.assert_called_with(0.0)
        led_intensity.assert_called_with({"D": 0.0}, unit="unit", experiment="exp")

    def test_sleeping_cancels_timers(self, job):
        sparge_timer = job._sparge_timer
        job.on_ready_to_sleeping()
        sparge_timer.cancel.assert_called_once()

    def test_resume_from_sleep_restores_led_and_reschedules(self, job):
        job.state = job.SLEEPING
        job._is_sparging = True   # simulate interrupted mid-sparge
        job.electrolysis_power = 3.0
        job.on_sleeping_to_ready()
        assert not job._is_sparging
        led_intensity.assert_called_with({"D": 3.0}, unit="unit", experiment="exp")


# ── reset_to_defaults ─────────────────────────────────────────────────────────

class TestResetToDefaults:
    def test_reset_applies_config_defaults(self, job):
        from pioreactor.config import config
        job.set_electrolysis_power(99.0)
        job.set_sparge_interval_minutes(5.0)
        job.set_sparge_duration_seconds(30.0)
        job.set_reset_to_defaults(True)
        # config mock returns fallback values
        assert job.electrolysis_power == config.getfloat(
            "electropioreactor.config", "electrolysis_power", fallback=2.5
        )
        assert job.sparge_interval_minutes == config.getfloat(
            "electropioreactor.config", "sparge_interval_minutes", fallback=60.0
        )
        assert job.sparge_duration_seconds == config.getfloat(
            "electropioreactor.config", "sparge_duration_seconds", fallback=10.0
        )

    def test_reset_false_is_noop(self, job):
        job.set_electrolysis_power(5.0)
        job.set_reset_to_defaults(False)
        assert job.electrolysis_power == 5.0

    def test_reset_clears_the_toggle_after_applying(self, job):
        job.reset_to_defaults = True  # would normally arrive via __setattr__
        job.set_reset_to_defaults(True)
        assert job.reset_to_defaults is False

    def test_reset_to_defaults_not_in_published_settings(self):
        assert "reset_to_defaults" not in ElectroPioreactor.published_settings

    def test_all_published_settings_have_persist_true(self):
        # Without persist=True, BackgroundJob._clear_caches publishes None to
        # each retained MQTT topic on shutdown, which leaves the Advanced modal
        # showing stale values until hard-refresh. See electropioreactor.py
        # for the comment block above published_settings.
        for setting, props in ElectroPioreactor.published_settings.items():
            assert props.get("persist") is True, (
                f"{setting!r} must declare persist=True so its MQTT-retained "
                f"value survives job stop"
            )


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
        job.set_od_pause_after_sparge_seconds(42.0)
        job.set_reset_to_defaults(True)
        from pioreactor.config import config
        assert job.od_pause_after_sparge_seconds == config.getfloat(
            "electropioreactor.config", "od_pause_after_sparge_seconds", fallback=5.0
        )


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
