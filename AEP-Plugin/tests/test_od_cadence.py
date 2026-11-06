# -*- coding: utf-8 -*-
"""
Simulated-time regression tests for the OD-reading cadence around electrolysis.

Bug fixed in v0.7.3: with the default settings (electrolysis_on_seconds=60,
electrolysis_off_seconds=0 i.e. continuous, od_pause_after_electrolysis_seconds=5)
v0.7.0-v0.7.2 paused od_reading at job start and never resumed it. Continuous
mode re-entered the ON phase every 60 s, and each re-entry cancelled the
pending 65 s OD-resume timer (the v0.7.1 orphan fix) and armed a fresh one, so
the resume was pushed 60 s further out for as long as the job ran.

These tests replace threading.Timer with a deterministic fake clock, drive the
job for simulated minutes or hours, and model od_reading as Pioreactor's default
(one reading every 5 s, samples_per_second = 0.2) that only takes a reading
while its state is READY. They assert where readings land, not how the timers
are wired, so they do not depend on the implementation's internal shape.
"""
import heapq
import itertools

import pytest
from unittest.mock import patch

from pioreactor_electropioreactor_plugin.electropioreactor import ElectroPioreactor
from pioreactor.actions.led_intensity import led_intensity
from pioreactor.pubsub import publish as mqtt_publish

OD_TOPIC = "pioreactor/unit/exp/od_reading/$state/set"
OD_PERIOD = 5.0  # Pioreactor default: samples_per_second = 0.2


# ── fake clock ────────────────────────────────────────────────────────────────

class FakeClock:
    """Deterministic stand-in for threading.Timer. Timers fire in due-time
    order (ties in start order) when advance() moves the clock past them."""

    def __init__(self):
        self.now = 0.0
        self._heap = []
        self._seq = itertools.count()
        self.all_timers = []

    def Timer(self, interval, function, args=None, kwargs=None):
        t = _FakeTimer(self, interval, function, args or (), kwargs or {})
        self.all_timers.append(t)
        return t

    def _schedule(self, timer):
        timer.due = self.now + float(timer.interval)
        heapq.heappush(self._heap, (timer.due, next(self._seq), timer))

    def advance_to(self, t_end):
        while self._heap and self._heap[0][0] <= t_end:
            due, _, timer = heapq.heappop(self._heap)
            if timer.cancelled:
                continue
            self.now = due
            timer.fired = True
            timer.function(*timer.args, **timer.kwargs)
        self.now = t_end

    def live_timers(self):
        return [t for t in self.all_timers if t.started and not t.cancelled and not t.fired]


class _FakeTimer:
    def __init__(self, clock, interval, function, args, kwargs):
        self.clock, self.interval, self.function = clock, interval, function
        self.args, self.kwargs = args, kwargs
        self.daemon = False
        self.started = self.cancelled = self.fired = False
        self.due = None

    def start(self):
        self.started = True
        self.clock._schedule(self)

    def cancel(self):
        self.cancelled = True


# ── recorders: OD state and LED intensity as functions of simulated time ─────

class Recorder:
    def __init__(self, clock):
        self.clock = clock
        self.od_events = []   # (t, "sleeping" | "ready")
        self.led_events = []  # (t, intensity)

    def on_publish(self, topic, payload, *a, **kw):
        if topic == OD_TOPIC:
            if isinstance(payload, bytes):
                payload = payload.decode()
            self.od_events.append((self.clock.now, str(payload)))

    def on_led(self, intensities, *a, **kw):
        (value,) = intensities.values()
        self.led_events.append((self.clock.now, float(value)))

    def _state_at(self, events, t, initial):
        state = initial
        for te, v in events:
            if te <= t:
                state = v
            else:
                break
        return state

    def od_ready_at(self, t):
        return self._state_at(self.od_events, t, "ready") == "ready"

    def led_at(self, t):
        return self._state_at(self.led_events, t, 0.0)

    def od_samples(self, t_start, t_end):
        """Times od_reading (5 s cadence, phase-offset so ticks never coincide
        exactly with a timer edge) would take a reading in [t_start, t_end)."""
        out, k = [], 0
        while True:
            t = 2.5 + k * OD_PERIOD
            if t >= t_end:
                return out
            if t >= t_start and self.od_ready_at(t):
                out.append(t)
            k += 1


@pytest.fixture
def sim():
    clock = FakeClock()
    rec = Recorder(clock)
    led_intensity.reset_mock()
    mqtt_publish.reset_mock()
    old_led_se, old_pub_se = led_intensity.side_effect, mqtt_publish.side_effect
    led_intensity.side_effect = rec.on_led
    mqtt_publish.side_effect = rec.on_publish
    try:
        with patch("threading.Timer", clock.Timer):
            yield clock, rec
    finally:
        led_intensity.side_effect = old_led_se
        mqtt_publish.side_effect = old_pub_se
        led_intensity.reset_mock()
        mqtt_publish.reset_mock()


def _start(**kwargs):
    job = ElectroPioreactor(unit="unit", experiment="exp", **kwargs)
    job.on_init_to_ready()
    return job


def _expected_ticks(t_start, t_end):
    return int((t_end - t_start) / OD_PERIOD)


# ── continuous electrolysis (the defaults) ────────────────────────────────────

class TestDefaultsContinuous:
    def test_defaults_are_continuous(self):
        defaults = ElectroPioreactor.__init__.__defaults__
        # (power, on, off, pause_after_electrolysis, sparge_dur, sparge_int, pause_after_sparge)
        assert defaults[1:4] == (60.0, 0.0, 5.0)

    def test_od_reads_at_full_cadence_with_defaults(self, sim):
        # The reported bug: v0.7.2 paused OD at t=0 and never resumed it.
        clock, rec = sim
        _start()
        clock.advance_to(30 * 60)  # 30 min, before the first sparge at 60 min
        samples = rec.od_samples(0, 30 * 60)
        assert len(samples) == _expected_ticks(0, 30 * 60), (
            f"only {len(samples)} OD readings in 30 min; od events: {rec.od_events[:6]}"
        )

    def test_defaults_never_pause_od_for_electrolysis(self, sim):
        # v0.6.x parity: continuous electrolysis has no OFF phase, so there is
        # no bubble-free window to dodge into; OD is not paused for it.
        clock, rec = sim
        _start()
        clock.advance_to(59 * 60)
        assert rec.od_events == []

    def test_defaults_od_paused_only_around_sparges(self, sim):
        clock, rec = sim
        _start()
        clock.advance_to(3 * 3600 + 120)
        # Sparges start at 60 min, then every 60 min after each sparge ends
        # (10 s), so at 3600, 7210, 10820. Each pauses OD for 10 + 5 = 15 s.
        sparge_starts = [3600.0, 7210.0, 10820.0]
        assert rec.od_events == [
            ev for s in sparge_starts for ev in ((s, "sleeping"), (s + 15.0, "ready"))
        ]
        samples = rec.od_samples(0, 3 * 3600 + 120)
        for t in samples:
            assert not any(s <= t < s + 15.0 for s in sparge_starts)
        assert len(samples) == _expected_ticks(0, 3 * 3600 + 120) - 3 * 3

    def test_defaults_light_led_once_like_v06(self, sim):
        # v0.6.x lit the LED once and left it. The continuous-mode internal
        # 60 s tick must not re-drive the LED (each led_intensity call is a
        # logged LED-change event on the unit).
        clock, rec = sim
        job = _start()
        clock.advance_to(30 * 60)
        assert rec.led_events == [(0.0, job.electrolysis_power)]

    def test_defaults_led_on_throughout(self, sim):
        clock, rec = sim
        job = _start()
        clock.advance_to(59 * 60)
        for t in range(0, 59 * 60, 7):
            assert rec.led_at(t) == job.electrolysis_power

    def test_sparge_still_interrupts_and_restores_led(self, sim):
        clock, rec = sim
        job = _start()
        clock.advance_to(3600 + 30)
        assert rec.led_at(3605) == 0.0
        assert rec.led_at(3611) == job.electrolysis_power


# ── intermittent (duty-cycled) electrolysis ──────────────────────────────────

class TestIntermittent:
    def test_od_reads_only_in_settled_off_phase(self, sim):
        # on=60, off=60, pause_after=5: each 120 s cycle has OD paused for
        # [0, 65) and reading during [65, 120).
        clock, rec = sim
        _start(electrolysis_off_seconds=60.0)
        clock.advance_to(30 * 60)
        samples = rec.od_samples(0, 30 * 60)
        for t in samples:
            phase = t % 120.0
            assert 65.0 <= phase < 120.0, f"OD reading at t={t} (cycle phase {phase})"
            assert rec.led_at(t) == 0.0
        # 15 cycles x 11 readings (phases 67.5, 72.5, ..., 117.5)
        assert len(samples) == 15 * 11

    def test_od_resumes_every_cycle(self, sim):
        clock, rec = sim
        _start(electrolysis_off_seconds=60.0)
        clock.advance_to(10 * 120)
        ready_times = [t for t, s in rec.od_events if s == "ready"]
        assert ready_times == [65.0 + 120.0 * k for k in range(10)]

    def test_negative_pause_reads_during_on_tail(self, sim):
        # on=60, off=30, pause=-10: OD resumes 50 s into each ON phase.
        clock, rec = sim
        _start(electrolysis_off_seconds=30.0, od_pause_after_electrolysis_seconds=-10.0)
        clock.advance_to(9 * 90)
        samples = rec.od_samples(0, 9 * 90)
        for t in samples:
            assert t % 90.0 >= 50.0
        assert len(samples) == 9 * 8

    def test_window_covering_whole_period_warns(self, sim):
        # on=60, off=3, pause=5: the 5 s settle never fits in the 3 s OFF
        # phase, so OD can never read. That is the literal meaning of the
        # settings, but it must not be silent.
        clock, rec = sim
        job = _start(electrolysis_off_seconds=3.0)
        clock.advance_to(10 * 60)
        assert rec.od_samples(0, 10 * 60) == []
        warnings = [c.args[0] for c in job.logger.warning.call_args_list]
        assert any("od_reading" in w and "never" in w for w in warnings), warnings
        # ...once, not every cycle.
        assert len([w for w in warnings if "never" in w]) == 1

    def test_window_shorter_than_period_does_not_warn(self, sim):
        clock, rec = sim
        job = _start(electrolysis_off_seconds=60.0)
        clock.advance_to(10 * 60)
        assert not [c for c in job.logger.warning.call_args_list if "never" in c.args[0]]


# ── settings changes mid-run ──────────────────────────────────────────────────

class TestModeSwitch:
    def test_switch_cycling_to_continuous_releases_od(self, sim):
        # Start in a configuration whose OD pause never expires, then switch to
        # continuous: OD must come back within one pause window.
        clock, rec = sim
        job = _start(electrolysis_off_seconds=3.0)
        clock.advance_to(200.0)
        assert not rec.od_ready_at(200.0)
        job.set_electrolysis_off_seconds(0.0)
        clock.advance_to(200.0 + 65.0)
        assert rec.od_ready_at(clock.now)
        clock.advance_to(3000.0)
        assert len(rec.od_samples(270.0, 3000.0)) == _expected_ticks(270.0, 3000.0)

    def test_switch_continuous_to_cycling_starts_dodging(self, sim):
        clock, rec = sim
        job = _start()
        clock.advance_to(90.0)
        job.set_electrolysis_off_seconds(60.0)
        # The in-flight ON phase (started t=60) ends at t=120, OFF until 180,
        # then cycling with 120 s period from t=180.
        clock.advance_to(180.0 + 10 * 120.0)
        for t in rec.od_samples(180.0, clock.now):
            assert (t - 180.0) % 120.0 >= 65.0
        assert len(rec.od_samples(180.0, clock.now)) == 10 * 11
        assert rec.led_at(150.0) == 0.0

    def test_reset_to_defaults_from_stuck_config_recovers(self, sim):
        # Reset to config.ini defaults (conftest injects on=33, off=7, pause=2:
        # window 35 < period 40) from the never-expiring on=60/off=3/pause=5.
        clock, rec = sim
        job = _start(electrolysis_off_seconds=3.0)
        clock.advance_to(300.0)
        job.set_reset_to_defaults(True)
        clock.advance_to(1200.0)
        assert len(rec.od_samples(600.0, 1200.0)) > 0
        ready = [t for t, s in rec.od_events if s == "ready" and t > 300.0]
        assert ready, rec.od_events[-6:]


# ── stop / sleep / timers ─────────────────────────────────────────────────────

class TestReleaseAndTimers:
    def _disconnect_mid_run(self, sim, off, at):
        clock, rec = sim
        job = _start(electrolysis_off_seconds=off)
        clock.advance_to(at)
        job.state = job.DISCONNECTED
        job.on_disconnected()
        return clock, rec, job

    def test_stop_mid_on_phase_releases_od_cycling(self, sim):
        clock, rec, job = self._disconnect_mid_run(sim, 60.0, 30.0)
        assert rec.od_events[-1][1] == "ready"
        assert clock.live_timers() == []
        assert rec.led_events[-1][1] == 0.0

    def test_stop_mid_sparge_releases_od_continuous(self, sim):
        clock, rec, job = self._disconnect_mid_run(sim, 0.0, 3605.0)
        assert rec.od_events[-1][1] == "ready"
        assert clock.live_timers() == []
        n = len(rec.od_events)
        clock.advance_to(5 * 3600)
        assert len(rec.od_events) == n  # nothing fires after stop

    def test_stop_with_defaults_leaves_no_timers(self, sim):
        clock, rec, job = self._disconnect_mid_run(sim, 0.0, 600.0)
        assert clock.live_timers() == []
        assert rec.od_ready_at(600.0)

    def test_sleep_releases_and_wake_restarts_cadence(self, sim):
        clock, rec = sim
        job = _start(electrolysis_off_seconds=60.0)
        clock.advance_to(30.0)
        job.state = job.SLEEPING
        job.on_ready_to_sleeping()
        assert rec.od_events[-1] == (30.0, "ready")
        assert clock.live_timers() == []
        clock.advance_to(100.0)
        job.state = job.READY
        job.on_sleeping_to_ready()
        clock.advance_to(100.0 + 5 * 120.0)
        assert [t for t, s in rec.od_events if s == "ready" and t > 100] == [
            100.0 + 65.0 + 120.0 * k for k in range(5)
        ]

    @staticmethod
    def _electrolysis_chain_timers(clock):
        return [
            t for t in clock.live_timers()
            if getattr(t.function, "__name__", "") in ("_begin_electrolysis_on", "_begin_electrolysis_off")
        ]

    def test_one_electrolysis_chain_at_a_time(self, sim):
        # A spurious extra ON entry (e.g. a wake racing a firing timer) must
        # not leave two parallel ON/OFF chains running.
        clock, rec = sim
        job = _start(electrolysis_off_seconds=60.0)
        clock.advance_to(10.0)
        job._begin_electrolysis_on()
        assert len(self._electrolysis_chain_timers(clock)) == 1
        clock.advance_to(10 * 120.0)
        assert len(self._electrolysis_chain_timers(clock)) == 1

    def test_continuous_keeps_exactly_one_pending_tick(self, sim):
        clock, rec = sim
        _start()
        for minute in range(1, 30):
            clock.advance_to(minute * 60.0 + 1)
            assert len(self._electrolysis_chain_timers(clock)) == 1
