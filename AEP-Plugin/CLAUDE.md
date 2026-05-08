# electroPioreactor Plugin — Developer Context

## Safety: do NOT actuate live hardware without explicit per-action permission

This plugin runs a real electrochemical bioreactor. Starting `electropioreactor`
on a live unit drives current across the electrode pair (generating H2 and
O2) and opens the CO2 solenoid on a fixed cycle. Both have safety
implications for whoever is in the room. An over-spec electrolysis_power
also risks physical damage to the electrodes.

When working on this plugin in any agent or assistant:

- Do NOT POST to `/api/.../jobs/run/...`, `/unit_api/jobs/run/...`, or any
  equivalent endpoint that spawns `pio run electropioreactor` or any other
  hardware-actuating job (stirring, dosing_automation, temperature_automation,
  pumps, LED set, PWM toggle) without explicit per-action permission for
  THAT specific run.
- Do NOT invoke the equivalent CLI form (`/opt/pioreactor/venv/bin/pio run ...`)
  on a live unit without the same permission.
- Read access (inspecting state, files, logs, MQTT subscriptions, the running
  jobs list, settings dumps) is fine; "the API exists" or "I want to verify
  the override path works" is NOT permission to actuate.
- Off-device verification is the default: the `tests/` conftest stubs the
  entire `pioreactor` package and sets `DOT_PIOREACTOR=/tmp`, so behavioural
  tests run with zero hardware risk. Use that, not live runs, for anything
  the test harness can cover.
- If a live-hardware test is genuinely necessary, propose it as text first
  (the exact curl / command + power level + duration) and wait for an
  explicit yes for that specific test in this turn.

This is the strictest safety rule in the project. Implied permission from
earlier in the session does NOT carry. Each actuation needs its own yes.

## What this plugin does

Drives electrolysis via the configured LED channel and periodically opens a CO₂ solenoid on the configured PWM channel. Electrolysis is paused during each sparge. The four numeric runtime parameters are user-configurable via the Pioreactor Advanced modal; the LED and PWM channel bindings are set in `config.ini` and read once at job init (channels are hardware bindings, not runtime-switchable).

## Hardware connections

- Electrode pair → LED channel set by `[electropioreactor.config] led_channel` in `config.ini` (default `D`, must be `A`, `B`, `C`, or `D`).
- CO₂ solenoid → PWM channel set by the standard `[PWM] N = relay` label indirection in `config.ini` (default `4`).

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

- **v0.6.1** (2026-04-29) – data-layer persistence fix (`persist: True` on
  all four `published_settings`).
- **v0.6.2** (2026-04-30) – polish pass: hardened shutdown cleanup, YAML
  input validation, init-time clamp logging, in-flight sparge-duration test,
  packaging hygiene, CI workflow.
- **v0.6.3** (2026-05-04) – defer `from pioreactor.hardware import PWM_TO_PIN`
  to inside `__init__` so module import doesn't touch `DOT_PIOREACTOR` (the
  alias is now a deprecated lazy resolver in current Pioreactor; reading it
  at module level broke `pio plugins list` from interactive shells).
- **v0.6.4** (2026-05-04) – drop unsupported `min` / `max` / `step` from
  `published_settings` YAML descriptors (Pioreactor's `BackgroundJobDescriptor`
  schema uses `forbid_unknown_fields=True`); change README install target
  from `~/.pioreactor/ui/contrib/jobs/` (no longer scanned) to
  `~/.pioreactor/plugins/ui/jobs/` (current convention).
- **v0.6.5** (2026-05-04) – move timer/state attribute initialisation to
  the top of `__init__`, before any validator that can raise, so cleanup
  on a validator failure doesn't `AttributeError` on `_sparge_timer` and
  mask the real `ValueError`.
- **v0.6.6** (2026-05-08) – PR-16 review feedback: drop the PR #615
  tarball-patch flow (Pioreactor 26.5.0 ships PR #615 natively); harden
  `patch-config-ini.py` against PWM 4 collision; gitignore hygiene;
  rename `TODO.md` → `CHANGELOG.md`. No runtime behaviour change.
- **v0.7.0** (2026-05-08) – LED channel configurable via
  `[electropioreactor.config] led_channel` (default `D`, validated against
  `A`/`B`/`C`/`D` at init). PWM channel was already configurable via the
  standard `[PWM] N = relay` indirection. New `--led-channel` CLI option.

The Advanced modal hard-refresh symptom was fixed upstream in
[Pioreactor/pioreactor#615](https://github.com/Pioreactor/pioreactor/pull/615)
and ships in Pioreactor 26.5.0+ (released 2026-05-07). v0.6.6 dropped
the transitional tarball-patch flow that supported pre-26.5.0 versions;
the plugin now requires Pioreactor ≥ 26.5.0.
