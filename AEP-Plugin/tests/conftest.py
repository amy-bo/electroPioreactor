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
def _cast_bytes_to_type(value, type_):
    # Faithful mirror of pioreactor.background_jobs.base.cast_bytes_to_type for
    # the datatypes the plugin uses (float, boolean), so _set_attr_from_message
    # below behaves like the real dispatcher.
    if type_ == "string":
        return value.decode()
    if type_ == "float":
        return float(value)
    if type_ == "integer":
        return int(value)
    if type_ == "boolean":
        return value.decode().lower() in ("true", "1", "y", "on", "yes", "t")
    raise TypeError(f"{type_} not found.")


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

    # Faithful mirror of the real BackgroundJob dispatcher
    # (pioreactor.background_jobs.base.BackgroundJob._set_attr_from_message):
    # a `set` is DROPPED unless the attr is in published_settings AND settable,
    # then routed to set_<attr> if that method exists. This is the exact path a
    # UI/MQTT `set` takes, so tests can drive it instead of calling setters
    # directly. (This is why reset_to_defaults MUST be in published_settings —
    # otherwise the toggle is inert.)
    def _set_attr_from_message(self, message) -> None:
        attr = message.topic.split("/")[4].lstrip("$")
        settings = type(self).published_settings
        if attr not in settings:
            return
        if not settings[attr]["settable"]:
            return
        if not hasattr(self, attr):
            return
        new_value = _cast_bytes_to_type(message.payload, settings[attr]["datatype"])
        if hasattr(self, f"set_{attr}"):
            getattr(self, f"set_{attr}")(new_value)
        else:
            setattr(self, attr, new_value)


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


# config.get is called with two distinct shapes by the plugin:
#   config.get("PWM_reverse", "relay")                         -> PWM channel label "4"
#   config.get(_CONFIG_SECTION, "led_channel", fallback="D")   -> LED channel label "D"
# A single return value can't serve both, so dispatch on the args. Any other
# .get falls back to the supplied fallback (or "" ) so tests stay robust.
def _config_get(*args, **kwargs):
    if args and args[0] == "PWM_reverse":
        return "4"                                            # PWM_reverse → channel "4"
    if len(args) >= 2 and args[1] == "led_channel":
        return kwargs.get("fallback", "D")                    # default LED channel "D"
    return kwargs.get("fallback", "")


_mock_config.get.side_effect = _config_get


# config.getfloat is what set_reset_to_defaults reads to restore "config.ini
# defaults". The old stub returned the caller's own `fallback`, which made every
# reset assertion vacuous (it compared a value to the same fallback it would
# itself produce — a literal compared to itself). Instead, return a DISTINCT,
# non-fallback value per (section, key) so a reset that genuinely reads config
# lands a value that differs from both the fallback AND any pre-reset value the
# test set. Tests assert the injected value (see CONFIG_RESET_VALUES), not a
# re-call with fallback.
CONFIG_RESET_VALUES = {
    ("electropioreactor.config", "electrolysis_power"): 3.3,
    ("electropioreactor.config", "electrolysis_on_seconds"): 33.0,
    ("electropioreactor.config", "electrolysis_off_seconds"): 7.0,
    ("electropioreactor.config", "od_pause_after_electrolysis_seconds"): 2.0,
    ("electropioreactor.config", "sparge_duration_seconds"): 8.0,
    ("electropioreactor.config", "sparge_interval_minutes"): 44.0,
    ("electropioreactor.config", "od_pause_after_sparge_seconds"): 6.0,
}


def _config_getfloat(section, key, **kwargs):
    if (section, key) in CONFIG_RESET_VALUES:
        return CONFIG_RESET_VALUES[(section, key)]
    return kwargs.get("fallback", 0.0)


_mock_config.getfloat.side_effect = _config_getfloat
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
