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

Data-layer persistence was fixed in **v0.6.1** (2026-04-29) by adding
`persist: True` to all four `published_settings`. **v0.6.2** (2026-04-30) is
a polish pass over the whole plugin: hardened shutdown cleanup, YAML input
validation, init-time clamp logging, in-flight sparge-duration test pinning
the documented behaviour, packaging hygiene, and a CI workflow.

The Advanced modal hard-refresh symptom is being fixed upstream in the
Pioreactor React frontend (separate PR, single-file change to
`AdvancedConfigDialog.jsx`). v0.6.2 of this plugin is independent of that PR.
