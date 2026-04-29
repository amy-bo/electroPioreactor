# electroPioreactor Plugin — Developer Context

## What this plugin does

Drives electrolysis via LED channel D and periodically opens a CO₂ solenoid on PWM channel 4.
Electrolysis is paused during each sparge. All three settings are user-configurable at runtime
via the Pioreactor Advanced modal.

## Hardware connections

- Electrode pair → LED channel D
- CO₂ solenoid → PWM channel 4

## Development setup

```bash
cd AEP-Plugin
python3 -m pytest tests/        # all tests run off-device; no Pi needed
```

Tests use a conftest that stubs the entire `pioreactor` package.
`DOT_PIOREACTOR` is set to `/tmp` in conftest so file-write code doesn't error.

## Device install

End-user install steps are in `README.md`. For development, an editable
install off a local checkout is convenient:

```bash
/opt/pioreactor/venv/bin/pip install -e /path/to/electroPioreactor/AEP-Plugin
```

## Status

Data-layer persistence is **fixed in v0.6.1** (2026-04-29). Root cause was missing
`persist: True` on `published_settings`, which made Pioreactor's `BackgroundJob._clear_caches`
wipe MQTT retained + SQLite rows on every Stop. Verified end-to-end on-device.

The Advanced modal still requires a hard-refresh (Cmd+Shift+R) after Stop because
Pioreactor's React frontend doesn't re-fetch settings on the disconnected
transition. Hardening that is the current open task — see **[TODO.md](TODO.md)**.
