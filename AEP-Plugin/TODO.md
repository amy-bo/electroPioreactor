# electroPioreactor Plugin – Open backlog

## Open

- [ ] **v0.7 Path 2 – on-device install + sanity** (no actuation). SSH to a Pioreactor ≥ 26.5.0 unit, then paste each line individually:
    - `cd ~/electroPioreactor && git fetch && git checkout configurable-led-channel && git pull`
    - `/opt/pioreactor/venv/bin/pip install ./AEP-Plugin --upgrade`
    - `/opt/pioreactor/venv/bin/pip show pioreactor-electropioreactor-plugin | grep Version` – expect `Version: 0.7.0`
    - `/opt/pioreactor/venv/bin/pio run electropioreactor --help` – expect `--led-channel` option in the help
    - `/opt/pioreactor/venv/bin/python /home/pioreactor/electroPioreactor/AEP-Plugin/scripts/patch-config-ini.py` – idempotent re-run, adds `led_channel = D` if missing
    - `grep led_channel ~/.pioreactor/config.ini` – expect `led_channel = D`
    - Negative test: edit `~/.pioreactor/config.ini` to set `led_channel = Z`, hard-refresh the UI, click Start in Activities → electroPioreactor. Expect job-start failure; error log should contain `led_channel must be one of A, B, C, D`. Reset to `D` afterwards.
- [ ] **v0.7 Path 3 – live actuation test** (drives current; per `AEP-Plugin/CLAUDE.md` safety rule, request a specific plan from Claude before executing). Pre-reqs: Path 2 passed; one electrode pair wired to a non-`D` LED channel for round-trip verification (or a meter on the chosen channel's LED line). Plan should specify target channel, power level, duration, what to watch, abort path. No live test until Path 2 is green.

Once each item is done, move it to `CHANGELOG.md` under v0.7.0 with a one-line completion note (or just mark `[x]` here if the narrative is already in the changelog).
