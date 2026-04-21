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

## Device setup (pio01)

Plugin is installed as an editable install in the Pioreactor venv:

```bash
/opt/pioreactor/venv/bin/pip install -e /home/pioreactor/electropioreactor-plugin/AEP-Plugin
```

To update after a push:

```bash
cd /home/pioreactor/electropioreactor-plugin && git pull
```

SSH: `pioreactor@pio01.local`, password: `raspberry`

## Status

Persistence is working end-to-end as of v0.5.2 — verified on-device. See **[TODO.md](TODO.md)**
for the verification notes, the one remaining UX pitfall (stale React state if the parent
page doesn't remount), and the atomic-write detail.
