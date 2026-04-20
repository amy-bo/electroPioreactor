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
        yield inst


# ── validators ────────────────────────────────────────────────────────────────

class TestValidators:
    def test_clamp_power_below_zero(self):
        assert ElectroPioreactor._clamp_power(-5) == 0.0

    def test_clamp_power_above_100(self):
        assert ElectroPioreactor._clamp_power(200) == 100.0

    def test_clamp_power_in_range(self):
        assert ElectroPioreactor._clamp_power(42.5) == 42.5

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
        job.set_electrolysis_power(50.0)
        assert job.electrolysis_power == 50.0
        led_intensity.assert_not_called()

    def test_set_electrolysis_power_while_not_sparging_updates_led(self, job):
        job._is_sparging = False
        job.set_electrolysis_power(10.0)
        led_intensity.assert_called_once_with({"D": 10.0}, unit="unit", experiment="exp")

    def test_set_electrolysis_power_clamped_to_100(self, job):
        job._is_sparging = False
        job.set_electrolysis_power(999.0)
        assert job.electrolysis_power == 100.0

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
