#!/usr/bin/env python3
"""Idempotently add [PWM] 4=relay and the four [electropioreactor.config]
defaults to ~/.pioreactor/config.ini. Re-runs preserve any existing values."""
from __future__ import annotations

import configparser
import os
import sys
from pathlib import Path

DOT = os.environ.get("DOT_PIOREACTOR", str(Path.home() / ".pioreactor"))
PATH = Path(DOT) / "config.ini"

DEFAULTS = {
    "electrolysis_power": "2.5",
    "sparge_duration_seconds": "10.0",
    "sparge_interval_minutes": "60.0",
    "od_pause_after_sparge_seconds": "5.0",
}


def main() -> int:
    p = configparser.ConfigParser()
    p.read([PATH])

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
