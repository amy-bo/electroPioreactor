# -*- coding: utf-8 -*-
"""
Inject stub modules for the pioreactor package so tests can run off-device.

All pioreactor imports are satisfied by lightweight fakes; only the logic
inside ElectroPioreactor itself is exercised.
"""
import configparser
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

# Point DOT_PIOREACTOR at /tmp so _config_paths() has a writable directory.
os.environ.setdefault("DOT_PIOREACTOR", "/tmp")


def _mod(name: str) -> types.ModuleType:
    m = types.ModuleType(name)
    sys.modules[name] = m
    return m


# ── package skeleton ──────────────────────────────────────────────────────────
_mod("pioreactor")
_mod("pioreactor.background_jobs")
_mod("pioreactor.actions")
_mod("pioreactor.cli")
_mod("pioreactor.utils")


# ── BackgroundJob ─────────────────────────────────────────────────────────────
class _BackgroundJob:
    READY = "ready"
    SLEEPING = "sleeping"
    DISCONNECTED = "disconnected"

    def __init__(self, unit, experiment):
        self.unit = unit
        self.experiment = experiment
        self.state = self.READY
        self.logger = MagicMock()
        self.pub_client = MagicMock()

    def on_init_to_ready(self): pass
    def on_ready_to_sleeping(self): pass
    def on_sleeping_to_ready(self): pass
    def on_disconnected(self): pass


_bgj = _mod("pioreactor.background_jobs.base")
_bgj.BackgroundJob = _BackgroundJob


# ── led_intensity ─────────────────────────────────────────────────────────────
_ali = _mod("pioreactor.actions.led_intensity")
_ali.led_intensity = MagicMock()


# ── CLI run group (click group is replaced by a no-op decorator factory) ──────
_cli = _mod("pioreactor.cli.run")
_mock_run = MagicMock()
_mock_run.command = lambda *a, **kw: (lambda f: f)
_cli.run = _mock_run


# ── config ────────────────────────────────────────────────────────────────────
_cfg = _mod("pioreactor.config")
_mock_config = MagicMock()
_mock_config.get.return_value = "4"                          # PWM_reverse → channel "4"
_mock_config.getfloat.side_effect = lambda s, k, **kw: kw.get("fallback", 0.0)
_cfg.config = _mock_config


# Mirror of the upstream pioreactor.config.ConfigParserMod — keeps key case
# on read/write (optionxform = str). Provided here so the plugin's
# `from pioreactor.config import ConfigParserMod` resolves under the stub.
class _StubConfigParserMod(configparser.ConfigParser):
    optionxform = staticmethod(str)


_cfg.ConfigParserMod = _StubConfigParserMod


# ── hardware ──────────────────────────────────────────────────────────────────
_hw = _mod("pioreactor.hardware")
_hw.PWM_TO_PIN = {"4": 12}


# ── PWM ───────────────────────────────────────────────────────────────────────
_upwm = _mod("pioreactor.utils.pwm")
_upwm.PWM = MagicMock(side_effect=lambda *a, **kw: MagicMock())  # fresh unspec'd mock per call


# ── whoami ────────────────────────────────────────────────────────────────────
_wai = _mod("pioreactor.whoami")
_wai.get_unit_name = MagicMock(return_value="unit")
_wai.get_assigned_experiment_name = MagicMock(return_value="exp")


# ── pubsub ────────────────────────────────────────────────────────────────────
_ps = _mod("pioreactor.pubsub")
_ps.publish = MagicMock()
_ps.QOS = types.SimpleNamespace(AT_LEAST_ONCE=1, AT_MOST_ONCE=0, EXACTLY_ONCE=2)


# ── states ────────────────────────────────────────────────────────────────────
# Real Pioreactor JobState is a str-subclass enum (StrEnum). The plugin relies
# on str.encode() to produce the bytes paho-mqtt wants; an earlier stub here
# defined a custom .to_bytes() method that masked a real on-device bug. Stub
# now mirrors the upstream str-subclass shape so off-device tests fail the
# same way on-device would.
class _JobState(str):
    pass


_states = _mod("pioreactor.states")
_states.JobState = types.SimpleNamespace(
    SLEEPING=_JobState("sleeping"),
    READY=_JobState("ready"),
    DISCONNECTED=_JobState("disconnected"),
)
