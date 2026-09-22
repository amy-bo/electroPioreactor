#!/usr/bin/env python3
"""Idempotently add [PWM] 4=relay and the four [electropioreactor.config]
defaults to ~/.pioreactor/config.ini. Re-runs preserve any existing values.

Uses pioreactor.config.ConfigParserMod (the case-preserving subclass
Pioreactor itself uses) rather than configparser.ConfigParser(), so
existing keys in the file – including uppercase ones in [leds] and
the [*.pid] sections – survive the round-trip unchanged.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from pioreactor.config import ConfigParserMod

DOT = os.environ.get("DOT_PIOREACTOR", str(Path.home() / ".pioreactor"))
PATH = Path(DOT) / "config.ini"

DEFAULTS = {
    "electrolysis_power": "2.5",
    "sparge_duration_seconds": "10.0",
    "sparge_interval_minutes": "60.0",
    "od_pause_after_sparge_seconds": "5.0",
}


def main() -> int:
    force = "--force" in sys.argv[1:]

    p = ConfigParserMod()
    p.read([PATH])

    if "PWM" not in p:
        p.add_section("PWM")
    existing = p["PWM"].get("4")
    if existing not in (None, "relay") and not force:
        print(
            f"refusing to overwrite [PWM] 4 = {existing!r} in {PATH}; "
            f"electroPioreactor needs [PWM] 4 = relay.",
            file=sys.stderr,
        )
        if existing == "waste":
            print(
                "'waste' is the stock Pioreactor default for channel 4, not "
                "necessarily a pump you have wired. On an electroPioreactor the "
                "CO2 solenoid takes channel 4, so unless a waste pump really is "
                "on it, re-run with --force. If one is, move it to a free "
                "channel in the UI's Configuration page first.",
                file=sys.stderr,
            )
        else:
            print(
                "Free PWM 4 (or wire the solenoid to a different channel and "
                "adjust this script), or re-run with --force to take it anyway.",
                file=sys.stderr,
            )
        return 1
    if existing not in (None, "relay"):
        print(f"replacing [PWM] 4 = {existing!r} with 'relay'")
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
