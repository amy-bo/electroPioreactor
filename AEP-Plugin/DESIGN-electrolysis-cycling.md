# Design note — electrolysis ON/OFF cycling + OD-pause around electrolysis

Branch: `plugin/electrolysis-cycling-od-pause` (off `origin/AEP-Plugin`, v0.6.7)
Target version: **v0.7.0**

## 1. What exists today (v0.6.7)

`ElectroPioreactor(BackgroundJob)` in
`pioreactor_electropioreactor_plugin/electropioreactor.py`:

- **Electrolysis** is *continuous*: on `on_init_to_ready` it sets LED channel
  **D** (hardcoded in `_set_led_d`) to `electrolysis_power` and leaves it there.
- **CO₂ sparge** runs on a repeating `threading.Timer` chain
  (`_schedule_next_sparge → _begin_sparge → _end_sparge`). Channel is the PWM
  whose `[PWM] N = relay` label is read via `config.get("PWM_reverse", "relay")`
  — i.e. PWM is *already* configurable; only the LED channel is hardcoded.
- During each sparge, electrolysis is paused (LED → 0), the solenoid opens
  (`_pwm.change_duty_cycle(100)`), and `od_reading` is paused via an MQTT
  `$state/set → sleeping` publish, resuming after
  `sparge_duration_seconds + od_pause_after_sparge_seconds` (the offset may be
  negative, down to `−sparge_duration`, which disables the OD pause).
- Settings persist to both `config_<unit>.ini` and `unit_config.ini` via an
  atomic write; all four are live-editable from the Advanced modal and declared
  in `published_settings` (with `persist: True`) and in the UI YAML descriptor.
- Off-device tests stub the whole `pioreactor` package (`tests/conftest.py`);
  `threading.Timer` is patched so no real timers fire.

## 2. What the task asks for

1. **Electrolysis ON/OFF cycling.** Electrolysis should itself cycle: a
   configurable ON period and OFF period (seconds), repeating. The driven
   channel must be **configurable, not hardcoded** (prior reviewer flagged the
   hardcoded LED `D`).
2. **OD-read pause around electrolysis.** Pause OD during each electrolysis ON
   phase AND for a user-defined period *after* electrolysis ends. That
   post-electrolysis pause may go **negative**, down to `−(ON time)`; a negative
   value shortens/cancels the pause so OD is measured during electrolysis.
   Effective OD-suppression window = `[ON start, ON end + pause]`.

## 3. Chosen design

Keep the existing CO₂-sparge machinery untouched (it is orthogonal and already
shipped). **Add a parallel electrolysis-cycling layer** with the same
timer-chain + persisted-setting + YAML shape as sparging, so the code style is
consistent and the reviewer sees a familiar pattern.

### 3a. Configurable electrolysis channel (closes the v0.7 reviewer flag)

- New `[electropioreactor.config] led_channel` setting (default `D`).
- `_get_led_channel()` reads + validates it (must be one of `A B C D`); invalid
  raises `ValueError` at `__init__`, surfacing through the job-start error path.
- `_set_led(intensity)` replaces `_set_led_d`, driving the configured channel.
- PWM channel stays configurable via the existing `[PWM] N = relay` indirection;
  README now documents both.

### 3b. Electrolysis cycling

New settings (seconds, both `> 0`, validated by the existing `_positive`):

- `electrolysis_on_seconds`  (default `60.0`)
- `electrolysis_off_seconds` (default `0.0`* — see note)

\* `0.0` OFF means "continuous electrolysis" = the v0.6.x behaviour, so existing
users get no behaviour change. `_positive` rejects ≤ 0, so OFF uses a dedicated
`_non_negative` validator (≥ 0) and ON uses `_positive` (> 0). When
`electrolysis_off_seconds == 0`, we skip the OFF phase entirely and keep the LED
on continuously (no pointless 0-second timer churn).

Timer chain mirrors sparging:

```
on_init_to_ready
  └─ _start_electrolysis_cycle
       └─ _electrolysis_on        # LED → power; pause OD; schedule _electrolysis_off at ON_secs
            └─ _electrolysis_off  # LED → 0;     schedule _electrolysis_on  at OFF_secs (if OFF>0)
```

`_electrolysis_paused` flag and `_electrolysis_on_timer` / `_electrolysis_off_timer`
mirror the sparge attrs (initialised at top of `__init__` before any validator,
per the v0.6.5 lesson).

### 3c. OD pause tied to the electrolysis ON phase

New setting `od_pause_after_electrolysis_seconds` (default `5.0`, **may be
negative**, mirrors the existing `od_pause_after_sparge_seconds` exactly).

When an ON phase begins, the effective OD-suppression window is:

```
window = electrolysis_on_seconds + od_pause_after_electrolysis_seconds
```

measured from ON start. Clamped to `≥ 0`. Pure timing function extracted as
a **module-level, side-effect-free** helper so the negative-pause edge cases are
unit-testable without constructing a job:

```python
def od_pause_window_seconds(on_seconds: float, pause_after_seconds: float) -> float:
    """Effective OD-suppression window measured from electrolysis-ON start."""
    return max(0.0, on_seconds + pause_after_seconds)
```

Behaviour (worked example, `on = 10`):

| pause_after | window | meaning |
|-------------|--------|---------|
| `+5`  | `15` | OD off through the 10 s ON phase + 5 s settle after |
| `0`   | `10` | OD off for exactly the ON phase |
| `−3`  | `7`  | OD resumes at t=7 s, i.e. 3 s **before** electrolysis ends → OD measured during the tail of electrolysis |
| `−10` | `0`  | window == 0 → OD never paused; measured throughout electrolysis |
| `−10` (≤ −on) | `0` | clamp floor; further-negative values also give 0 |

This is the same contract the existing sparge OD-pause already honours; we reuse
the identical pattern so the two pauses compose predictably and the code is
uniform. If both a sparge-pause and an electrolysis-pause overlap, each just
publishes `sleeping`/`ready`; the resume is guarded by the `_od_paused` flag so a
double-resume is a no-op (existing behaviour).

### 3d. Why not merge the two OD pauses / fold sparge into cycling?

They are independent physical events (CO₂ bubbles vs electrolysis bubbles/IR
interference) on independent timers. Folding them would change shipped sparge
behaviour and break existing tests/YAML. Keeping them parallel is the minimal,
lowest-risk change and matches the existing code's structure.

## 4. Files touched

- `electropioreactor.py` — cycling layer, configurable LED channel, OD-pause
  helper, new setters/validators, new published_settings, CLI options.
- `additional_config.ini` — new defaults (`led_channel`,
  `electrolysis_on_seconds`, `electrolysis_off_seconds`,
  `od_pause_after_electrolysis_seconds`).
- `ui/contrib/jobs/electropioreactor.yaml` — new published-setting descriptors;
  reword D/4 references to "the configured channel".
- `scripts/patch-config-ini.py` — write the new defaults idempotently.
- `tests/test_electropioreactor.py` — cycling timer logic, configurable channel,
  and the negative-pause edge cases (incl. the pure `od_pause_window_seconds`).
- `README.md`, `CHANGELOG.md`, `setup.py`, `__plugin_version__` — docs + bump.

## 5. Constraints honoured

- No system patching without consent; we only add a config setting and require
  Pioreactor ≥ 26.5.0 (already the documented minimum). No frontend patch.
- No per-machine specifics; channels are configurable, defaults are generic.
- Tests are pure-logic/mocked; no hardware actuation.
- Existing-user backwards compatibility: default `led_channel=D`,
  `electrolysis_off_seconds=0` (continuous) → identical to v0.6.x.
