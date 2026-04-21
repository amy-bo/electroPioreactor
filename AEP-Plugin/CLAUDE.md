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

Persistence is **still broken** on-device as of 2026-04-21 despite the v0.5.2/0.5.3 fixes.
The earlier "verified working" note was wrong — the device was running v0.5.0 during that
"verification." See **[TODO.md](TODO.md)** for the honest status and the next
on-device debugging step (which layer — file / API / MQTT / React — actually disagrees).
