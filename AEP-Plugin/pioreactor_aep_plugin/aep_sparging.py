# -*- coding: utf-8 -*-
from __future__ import annotations

import threading

import click
from pioreactor.actions.led_intensity import led_intensity
from pioreactor.background_jobs.base import BackgroundJob
from pioreactor.cli.run import run
from pioreactor.config import config
from pioreactor.hardware import PWM_TO_PIN
from pioreactor.utils.pwm import PWM
from pioreactor.whoami import get_assigned_experiment_name
from pioreactor.whoami import get_unit_name

__plugin_summary__ = "AEP CO₂ sparging with electrolysis power control"
__plugin_version__ = "0.1.0"
__plugin_name__ = "AEP Sparging"
__plugin_author__ = "Martin Currie"
__plugin_homepage__ = "https://github.com/amybo-org/pioreactor-aep-plugin"


class AEPSparging(BackgroundJob):
    """
    Controls CO₂ sparging and electrolysis (LED D) for the Aseptic ElectroPioreactor.

    Periodically opens the CO₂ solenoid for `sparge_duration_seconds` every
    `sparge_interval_hours`. LED D (electrolysis) is turned off during sparging
    and restored immediately after.
    """

    job_name = "aep_sparging"

    published_settings = {
        "electrolysis_power": {"datatype": "float", "settable": True, "unit": "%"},
        "sparge_duration_seconds": {"datatype": "float", "settable": True, "unit": "s"},
        "sparge_interval_hours": {"datatype": "float", "settable": True, "unit": "h"},
    }

    def __init__(
        self,
        unit: str,
        experiment: str,
        electrolysis_power: float = 2.5,
        sparge_duration_seconds: float = 10.0,
        sparge_interval_hours: float = 1.0,
    ) -> None:
        super().__init__(unit=unit, experiment=experiment)
        self.electrolysis_power = float(electrolysis_power)
        self.sparge_duration_seconds = float(sparge_duration_seconds)
        self.sparge_interval_hours = float(sparge_interval_hours)
        self._is_sparging = False
        self._sparge_timer: threading.Timer | None = None
        self._stop_timer: threading.Timer | None = None

        pwm_channel = config.get("PWM_reverse", "relay")
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
        self._pwm.start(0.0)
        self._set_led_d(self.electrolysis_power)
        self._schedule_next_sparge()

    # ── settings setters ────────────────────────────────────────────────────

    def set_electrolysis_power(self, value: float) -> None:
        self.electrolysis_power = float(value)
        if not self._is_sparging:
            self._set_led_d(self.electrolysis_power)

    def set_sparge_duration_seconds(self, value: float) -> None:
        self.sparge_duration_seconds = float(value)

    def set_sparge_interval_hours(self, value: float) -> None:
        self.sparge_interval_hours = float(value)
        if not self._is_sparging:
            self._schedule_next_sparge()

    # ── sparging cycle ───────────────────────────────────────────────────────

    def _schedule_next_sparge(self) -> None:
        if self._sparge_timer is not None:
            self._sparge_timer.cancel()
        self._sparge_timer = threading.Timer(
            self.sparge_interval_hours * 3600, self._begin_sparge
        )
        self._sparge_timer.daemon = True
        self._sparge_timer.start()

    def _begin_sparge(self) -> None:
        if self.state != self.READY:
            self._schedule_next_sparge()
            return

        self._is_sparging = True
        self.logger.info(
            f"Sparging CO₂ for {self.sparge_duration_seconds:.0f}s (LED D off during sparging)"
        )
        self._set_led_d(0.0)
        self._pwm.change_duty_cycle(100.0)

        self._stop_timer = threading.Timer(self.sparge_duration_seconds, self._end_sparge)
        self._stop_timer.daemon = True
        self._stop_timer.start()

    def _end_sparge(self) -> None:
        self._pwm.change_duty_cycle(0.0)
        self._set_led_d(self.electrolysis_power)
        self._is_sparging = False
        self.logger.debug("CO₂ sparging complete; LED D restored")
        self._schedule_next_sparge()

    # ── lifecycle hooks ──────────────────────────────────────────────────────

    def on_ready_to_sleeping(self) -> None:
        super().on_ready_to_sleeping()
        self._cancel_timers()
        self._pwm.change_duty_cycle(0.0)
        self._set_led_d(0.0)

    def on_sleeping_to_ready(self) -> None:
        super().on_sleeping_to_ready()
        self._is_sparging = False
        self._set_led_d(self.electrolysis_power)
        self._schedule_next_sparge()

    def on_disconnected(self) -> None:
        super().on_disconnected()
        self._cancel_timers()
        self._pwm.change_duty_cycle(0.0)
        self._pwm.clean_up()
        self._set_led_d(0.0)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _set_led_d(self, intensity: float) -> None:
        led_intensity({"D": intensity}, unit=self.unit, experiment=self.experiment)

    def _cancel_timers(self) -> None:
        if self._sparge_timer is not None:
            self._sparge_timer.cancel()
            self._sparge_timer = None
        if self._stop_timer is not None:
            self._stop_timer.cancel()
            self._stop_timer = None


@run.command(name="aep_sparging", help=__plugin_summary__)
@click.option(
    "--electrolysis-power",
    default=config.getfloat("aep_sparging.config", "electrolysis_power", fallback=2.5),
    type=float,
    show_default=True,
    help="Initial LED D intensity for electrolysis (0–100 %).",
)
@click.option(
    "--sparge-duration-seconds",
    default=config.getfloat("aep_sparging.config", "sparge_duration_seconds", fallback=10.0),
    type=float,
    show_default=True,
    help="How long to open the CO₂ solenoid each cycle (seconds).",
)
@click.option(
    "--sparge-interval-hours",
    default=config.getfloat("aep_sparging.config", "sparge_interval_hours", fallback=1.0),
    type=float,
    show_default=True,
    help="How often to sparge (hours).",
)
def click_aep_sparging(
    electrolysis_power: float,
    sparge_duration_seconds: float,
    sparge_interval_hours: float,
) -> None:
    unit = get_unit_name()
    experiment = get_assigned_experiment_name(unit)
    job = AEPSparging(
        unit=unit,
        experiment=experiment,
        electrolysis_power=electrolysis_power,
        sparge_duration_seconds=sparge_duration_seconds,
        sparge_interval_hours=sparge_interval_hours,
    )
    job.block_until_disconnected()
