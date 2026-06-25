#!/usr/bin/env python3
"""Idempotently add [PWM] 4=relay and the four [electropioreactor.config]
defaults to ~/.pioreactor/config.ini. Re-runs preserve any existing values.

Self-healing (added v0.6.7): pre-v0.6.7 versions of this script used a
default `configparser.ConfigParser()`, which silently lower-cased every
key on round-trip — turning the upstream Pioreactor template's `[leds]`
entries (A/B/C/D) into a/b/c/d, and the PID gains (Kp/Ki/Kd) under
`[stirring.pid]`, `[dosing_automation.pid_morbidostat]`, and
`[temperature_automation.thermostat]` into kp/ki/kd. Pioreactor itself
uses `ConfigParserMod` (optionxform = str) and looks those keys up
case-sensitively, so the corruption silently broke OD reading
(channel-label resolution in `[leds]`) and every PID-controlled job on
each unit that ran the buggy script. This version uses
`ConfigParserMod` AND repairs already-corrupted files on the next run.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from pioreactor.config import ConfigParserMod

DOT = os.environ.get("DOT_PIOREACTOR", str(Path.home() / ".pioreactor"))
PATH = Path(DOT) / "config.ini"

DEFAULTS = {
    "led_channel": "D",
    "electrolysis_power": "2.5",
    "electrolysis_on_seconds": "60.0",
    "electrolysis_off_seconds": "0.0",
    "sparge_duration_seconds": "10.0",
    "sparge_interval_minutes": "60.0",
    "od_pause_after_sparge_seconds": "5.0",
}

# Sections + keys whose canonical case Pioreactor looks up case-sensitively.
# `[leds]` uses LETTER keys (A/B/C/D) — these are the LED-channel labels
# that appeared as `a = IR` etc. on units patched by pre-v0.6.7 versions.
# `[od_config.photodiode_channel]` upstream uses NUMERIC keys (1/2/3/4),
# which have no case — it's NOT a target for this repair.
# PID gains (Kp/Ki/Kd) live under varied section names — we don't filter
# by section name; iterating every section and repairing any kp/ki/kd we
# find is safe and covers them all.
_LEDS_SECTION = "leds"
_LEDS_KEYS = {"a": "A", "b": "B", "c": "C", "d": "D"}
_PID_KEYS = {"kp": "Kp", "ki": "Ki", "kd": "Kd"}


def _repair_lowercased_keys(p: ConfigParserMod) -> list[str]:
    """Restore canonical case for keys that a prior buggy run lower-cased.
    Returns a list of human-readable repair descriptions for logging."""
    repairs: list[str] = []

    def _repair(section: str, mapping: dict[str, str]) -> None:
        if not p.has_section(section):
            return
        for lower, canonical in mapping.items():
            if p.has_option(section, lower) and not p.has_option(section, canonical):
                p[section][canonical] = p[section][lower]
                p.remove_option(section, lower)
                repairs.append(f"[{section}] {lower} -> {canonical}")

    _repair(_LEDS_SECTION, _LEDS_KEYS)
    for sec in p.sections():
        _repair(sec, _PID_KEYS)

    return repairs


def main() -> int:
    p = ConfigParserMod()
    p.read([PATH])

    repairs = _repair_lowercased_keys(p)

    if "PWM" not in p:
        p.add_section("PWM")
    existing = p["PWM"].get("4")
    if existing not in (None, "relay"):
        print(
            f"refusing to overwrite [PWM] 4 = {existing!r} in {PATH}; "
            f"electroPioreactor needs [PWM] 4 = relay. "
            f"Free PWM 4 (or wire the solenoid to a different channel and "
            f"adjust this script) before re-running.",
            file=sys.stderr,
        )
        return 1
    p["PWM"]["4"] = "relay"

    sec = "electropioreactor.config"
    if sec not in p:
        p.add_section(sec)
    for k, v in DEFAULTS.items():
        p[sec].setdefault(k, v)

    with open(PATH, "w") as f:
        p.write(f)

    print(f"Patched: {PATH}")
    if repairs:
        print("Repaired lower-cased keys (left over from a pre-v0.6.7 run):")
        for line in repairs:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
