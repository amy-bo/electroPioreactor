# electroPioreactor Plugin — Changelog

## v0.7.1 (2026-06-26) — fix orphaned electrolysis OD-resume timer

Bugfix on the v0.7.0 OD-pause-around-electrolysis path. `_begin_electrolysis_on`
reassigned `self._electrolysis_od_resume_timer` **without first cancelling the
prior one**. With a continuous-ish window where the OD-pause window (`on_seconds`
+ `od_pause_after_electrolysis_seconds`) exceeds the electrolysis period
(e.g. `on=60, off=0, pause_after=5` → window `65` > period `60`), a second
`_begin_electrolysis_on` fires while the previous window's resume timer is still
pending. The orphaned timer later fired `_resume_od_reading("electrolysis")`,
dropped the sole `electrolysis` pause owner, and republished the OD job **READY
while electrolysis was still ON** — exactly the failure the sparge path already
guards against. The orphan also escaped `_cancel_timers`, which only ever holds
the latest timer reference.

Fix: mirror the sparge path — cancel any pending
`_electrolysis_od_resume_timer` before reassigning it (under the existing
`window > 0` guard, keeping the daemon/start pattern). Added a symmetric
unit regression (`test_begin_electrolysis_on_cancels_prior_od_resume_timer`)
and a cycle-level regression (`test_second_electrolysis_on_does_not_resume_od_early`)
asserting a second ON phase does not republish OD READY while the electrolysis
owner is still held.

## v0.7.0 (2026-06-25) — electrolysis ON/OFF cycling, OD pause around electrolysis, configurable LED channel

Two new features plus the long-deferred configurable-LED-channel work
(Gerrit's PR #16 flag).

### Electrolysis ON/OFF cycling

Electrolysis previously ran continuously (LED held at power, only dropped
during a sparge). It now **cycles**: ON for `electrolysis_on_seconds`
(> 0, default `60`), then OFF for `electrolysis_off_seconds` (≥ 0, default
`0`), repeating. `electrolysis_off_seconds = 0` means continuous (no OFF
phase) — identical to the v0.6.x behaviour, so default-config users see no
change. The cycle is a `threading.Timer` chain
(`_begin_electrolysis_on` → `_begin_electrolysis_off` → …) mirroring the
existing sparge chain. A mid-phase setting change applies to the next
phase, not the in-flight one (same invariant as `sparge_duration_seconds`).

### OD-read pause around electrolysis

OD reading is now paused around each electrolysis ON phase, governed by a
new `od_pause_after_electrolysis_seconds` (default `5.0`). The effective
OD-suppression window, from ON start, is
`electrolysis_on_seconds + od_pause_after_electrolysis_seconds` (floored at
0). Crucially the offset **may be negative**, down to and below
`−electrolysis_on_seconds`: a negative value shortens or cancels the pause
so OD resumes *during* electrolysis (e.g. `on=10, pause=−3` → OD resumes at
t=7 s, 3 s before electrolysis ends; `pause=−10` → never paused, OD
measured throughout). The pure timing core is extracted as the
side-effect-free module function `od_pause_window_seconds(on, pause_after)`
with a worked-example docstring, unit-tested across the negative edge
cases. This OD pause is independent of, and composes with, the existing
sparge OD pause.

### Configurable LED channel (closes PR #16 / v0.7 reviewer flag)

The electrolysis LED channel was hardcoded to `D`. It is now read from
`[electropioreactor.config] led_channel` (default `D`, validated to one of
A/B/C/D — an invalid label raises `ValueError` at job start). `_set_led`
drives the configured channel; `_set_led_d` is gone. The PWM (CO₂) channel
was already configurable via `[PWM] N = relay`; the README now documents
both in a new **Hardware connections** section. `led_channel` is a hardware
binding read once at init (not a live setting), so switching it needs a
config edit + restart.

### Settings, config, UI

Three new live settings (`electrolysis_on_seconds`,
`electrolysis_off_seconds`, `od_pause_after_electrolysis_seconds`) added to
`published_settings` (all `persist: True`), the YAML descriptor, the CLI,
`additional_config.ini`, and `scripts/patch-config-ini.py` defaults.
`reset_to_defaults` now also resets the three new values. YAML/README
D/4 references reworded to "the configured channel".

### Tests

`tests/test_electropioreactor.py` gains 36 tests (now 82 total in that
file): the pure `od_pause_window_seconds` with all negative-pause edge
cases, the ON/OFF cycle timer logic, continuous-mode (`off=0`), the
OD-pause-during-electrolysis scheduling, the new setters/validators
(`_non_negative`), configurable-LED-channel resolution + invalid-channel
rejection at init, and electrolysis-cycle persistence/reset. The
`patch-config-ini` test asserts the new defaults. All pass off-device
(mocked, no hardware). Backwards-compat: with defaults (`led_channel=D`,
`electrolysis_off_seconds=0`) behaviour is identical to v0.6.x.

### Compatibility note

This branch is based on `AEP-Plugin` (v0.6.7), not the parallel
`configurable-led-channel` v0.7 spec branch; it folds that branch's
configurable-LED-channel goal into this release so the cycling/OD-pause
work ships channel-agnostic in one version.

### Review fixes (pre-merge)

A round of code review on the v0.7.0 work surfaced several correctness and
hygiene issues, all fixed in this release (each paired with tests):

- **OD-pause owner refcount (the named feature's core defect).** Sparge and
  electrolysis both paused OD via a single shared `_od_paused` boolean, and
  `_resume_od_reading` cleared it unconditionally — so a sparge resume could
  re-enable OD *mid-electrolysis* (and vice-versa). OD pausing is now
  reference-counted by owner (`_od_pausers`: `{'sparge', 'electrolysis'}`):
  the first owner publishes SLEEPING, each resume releases only its own owner,
  and OD is actually resumed only once the last owner releases. Regression
  test added: electrolysis pause → sparge pause → sparge resume → OD stays
  paused while electrolysis still holds.
- **Dead "Reset to Defaults" toggle.** `reset_to_defaults` was absent from
  `published_settings`, so the real `BackgroundJob._set_attr_from_message`
  dispatcher silently dropped every UI `set` and the toggle was inert. Added
  it as `{datatype: boolean, settable: True, persist: False}` (persist=False
  so Pioreactor doesn't retain/replay the last True and fire a spurious reset
  on restart); corrected the false "handled via MQTT" comment. Tests now
  drive the real dispatcher path.
- **Orphaned OD-resume timer mid-sparge.** A new sparge reassigned
  `_od_resume_timer` without cancelling a pending one; the orphan fired
  `_resume_od_reading` mid-new-sparge and escaped `_cancel_timers`. Now
  cancelled before reassignment.
- **LED MQTT connection churn.** `_set_led` called `led_intensity()` without
  a `pubsub_client`, opening a fresh MQTT connect/disconnect on every call.
  Now passes the job's `self.pub_client`.
- **Non-finite floats reaching hardware / `threading.Timer`.** NaN/inf could
  flow into `led_intensity` and into timer delays (a NaN delay silently kills
  the timer thread, stopping the schedule). `_positive` / `_non_negative` and
  the OD-pause offsets now reject non-finite via the existing `ValueError`
  contract; `_clamp_power` maps non-finite to the safe floor `0.0` (callers
  don't expect it to raise).
- **Docs.** Rewrote the `CLAUDE.md` status note to state the PR-#615
  transitional hot-patch flow was removed in v0.6.6 and the minimum Pioreactor
  is 26.5.0 (`pio update` is the remedy on older units) — the code already
  enforces the minimum, no system-patching. Added a maintainer release
  checklist to the README so the expected-version strings get bumped alongside
  `setup.py` / `__plugin_version__`.
- **Test-harness rigor.** The conftest `getfloat` stub returned the caller's
  own fallback, making config-reset assertions vacuous (a literal compared to
  itself). It now injects distinct non-fallback values per `(section, key)`,
  and the reset tests assert those injected values.

## v0.6.7 (2026-05-10) — preserve key case in config.ini writes

Pre-v0.6.7 the plugin used a default `configparser.ConfigParser()` in
three runtime writers (`_save_all_config`, `_save_config`,
`_clear_unit_config`) and in the install-time
`scripts/patch-config-ini.py`. Default `ConfigParser` calls
`optionxform = str.lower` on every key as it parses, so a write-after-read
silently lower-cased every existing key in `~/.pioreactor/config.ini` —
including the `[leds]` LED-channel labels (A/B/C/D), and PID gains
(Kp/Ki/Kd) in `[stirring.pid]`,
`[dosing_automation.pid_morbidostat]`, and
`[temperature_automation.thermostat]`. Pioreactor itself uses
`ConfigParserMod` (`optionxform = str`) and looks all of those keys up
case-sensitively, so the corruption hard-failed every PID-controlled job
and broke the LED-label resolution OD reading depends on.

(Note on scope: `[od_config.photodiode_channel]` upstream uses **numeric**
keys 1/2/3/4, not letter keys, so it has no case-sensitivity bug. Letter-
key corruption appears in `[leds]`, not in the photodiode-channel section.
A first attempt at this fix on a feature branch wrongly targeted
photodiode_channel; the parallel `vibe pioreactor` session caught the
mismatch by inspecting an actual ed05 config.ini against the upstream
template before deploying.)

### Fix

All four ConfigParser sites now use `pioreactor.config.ConfigParserMod`
(case-preserving — the same class Pioreactor uses for its own config
machinery). The conftest stub now provides `ConfigParserMod` so off-device
tests still load the plugin.

### Self-healing

`scripts/patch-config-ini.py` now repairs already-corrupted files on the
next run: lowercase a/b/c/d under `[leds]` get renamed to A/B/C/D, and
lowercase kp/ki/kd in **any** section get renamed to Kp/Ki/Kd (real
upstream PID section names vary — `[stirring.pid]`,
`[dosing_automation.pid_morbidostat]`,
`[temperature_automation.thermostat]` — so the matcher iterates every
section rather than filtering by name). Idempotent — repeat runs on a
clean file are no-ops. Logged on stdout when a repair fires.

The PWM-4 guard from v0.6.6 is preserved (test pinned).

### Tests

`tests/test_patch_config_ini.py` (new, 9 tests) pins both
case-preservation on round-trip and self-healing of a previously-corrupted
file, asserts the photodiode numeric-key section is left alone, and pins
the PWM-4 guard. Existing 46 tests still pass — total 55 pass off-device.

## v0.6.6 (2026-05-08) — PR-16 review feedback (Gerrit)

Cleanup pass addressing the inline comments on PR #16. No behaviour change
for the running plugin; minimum supported Pioreactor version bumped to
**26.5.0**.

- **Drop the PR #615 tarball-patch flow.** Pioreactor 26.5.0 (released
  2026-05-07) ships PR #615 natively, so the transitional hot-patch is
  obsolete. Removed `scripts/apply-pr615-patch.sh`,
  `scripts/revert-pr615-patch.sh`, `transitional/pioreactor-static-pr615.tar.gz`,
  and the README "step 3" section. README "Pioreactor version compatibility"
  now states the 26.5.0 minimum and points users at `pio update`.
- **`patch-config-ini.py` no longer silently overwrites `[PWM] 4`.** If the
  channel is already mapped to a non-`relay` label, the script refuses with
  a non-zero exit and a clear remediation message instead of clobbering the
  user's wiring.
- **Repository hygiene.** `.claude/` and `.vibe/` added to `.gitignore`;
  `.claude/settings.local.json` and `.vibe/copy-latest.txt` removed from
  version control. `pi02-setup-notes.md` (development notes specific to one
  unit) removed from the repo.
- **`TODO.md` → `CHANGELOG.md`.** Naming reflects what the file actually
  is.

### Deferred to v0.7

Gerrit also flagged that the LED channel is hardcoded to `D` and the YAML
descriptions point specifically at PWM `4`. PWM is in fact already
configurable via Pioreactor's `[PWM] N = relay` label indirection (see
`pioreactor_electropioreactor_plugin/electropioreactor.py:89`). Making the
LED side equivalently configurable, and updating the YAML descriptions to
match, is the v0.7 work. Branch:
[`configurable-led-channel`](https://github.com/amy-bo/electroPioreactor/tree/configurable-led-channel)
(spec at `AEP-Plugin/v0.7-SPEC.md`).

## v0.6.5 (2026-05-04) — init ordering, no more masked ValueErrors

Moved timer/state attribute initialisation (`_sparge_timer`, `_stop_timer`,
`_od_resume_timer`, `_is_sparging`, `_od_paused`, `reset_to_defaults`) to
the top of `__init__`, before any validator that can raise. Without this,
a non-positive `sparge_duration_seconds` from the Advanced modal triggered
`_positive` to raise `ValueError`, BackgroundJob's exception cleanup then
called `_cancel_timers`, and the user saw

```
Failed to cancel timers during cleanup: 'ElectroPioreactor' object has no
attribute '_sparge_timer'
```

instead of the actual validation error. The cleanup path is now safe
regardless of which subsequent line in `__init__` fails.

## v0.6.4 (2026-05-04) — YAML schema + plugin install path

Two fixes that together let the UI actually render the plugin in
**Activities** on current Pioreactor:

- **YAML schema**. Pioreactor's `BackgroundJobDescriptor` /
  `PublishedSettingsDescriptor` use `forbid_unknown_fields=True` and only
  allow `key, type, display, description, default, unit, label, editable`.
  v0.6.2 added `min` / `max` / `step` to `published_settings` for UI input
  validation; current Pioreactor rejects the file silently
  (validation error logged via `report_error`, descriptor dropped). Stripped
  those fields. Range enforcement still happens at runtime in the job
  (`_clamp_power`, `_positive`).
- **Install target path**. Pioreactor's
  `web/utils.py:load_background_job_descriptors` scans
  `~/.pioreactor/ui/jobs/` (built-ins) and
  `~/.pioreactor/plugins/ui/jobs/` (plugin descriptors). The legacy
  `~/.pioreactor/ui/contrib/jobs/` is no longer scanned. README install
  step updated to deploy to the correct path.

## v0.6.3 (2026-05-04) — defer hardware import

`from pioreactor.hardware import PWM_TO_PIN` at module level fired
Pioreactor's `__getattr__` deprecation lazy-resolver, which calls
`get_pwm_to_pin_map()` and `Path(environ["DOT_PIOREACTOR"])` on access.
That broke `pio plugins list` from interactive shells (Pioreactor sets
`DOT_PIOREACTOR` via systemd / `/etc/pioreactor.env`, not
`/etc/environment`). Moved the import inside
`ElectroPioreactor.__init__`. Module imports cleanly regardless of env
state; instantiation still requires `DOT_PIOREACTOR`, which is correct.

## v0.6.2 (2026-04-30) — polish pass

After the v0.6.1 root-cause fix, a Superpowers code review surfaced a list
of pre-existing rough edges. v0.6.2 addresses them in a single focused
release:

- **CI**: added `.github/workflows/aep-plugin-tests.yml` running `pytest tests/`
  on push and PR. Pre-v0.6.2 the suite had never been executed by a machine.
- **YAML input validation**: `sparge_duration_seconds` and
  `sparge_interval_minutes` now declare `min: 0.01` so the UI rejects values
  the runtime would silently swallow as `ValueError`. `step: 0.1` on the
  three `seconds` fields gives the spinner sensible increments.
- **Hardened shutdown**: `on_disconnected` and `on_ready_to_sleeping` now
  run each cleanup step (cancel timers, close solenoid, off LED, resume
  od_reading) under a `_safe()` wrapper so a failure in one step doesn't
  skip the others.
- **Init-time clamp logging**: when `__init__` clamps `electrolysis_power`
  to the `[0, 10]` range, it now logs the original-and-clamped values
  instead of silently overwriting the user's input.
- **Reset toggle self-clears**: `set_reset_to_defaults` now sets
  `self.reset_to_defaults = False` at the end so the YAML's "resets itself
  automatically after applying" claim matches in-memory state.
- **In-flight sparge invariant pinned**: a new test asserts that mid-sparge
  changes to `sparge_duration_seconds` apply to the next cycle, not the
  in-flight one (matching the YAML description). A future "fix" that
  silently changes this user-facing behaviour now fails CI.
- **Packaging**: `click` moved from `extras_require['dev']` (where it was
  miscategorised) to `install_requires`. `requirements-dev.txt` deleted —
  duplicated `extras_require['dev']`, single source of truth now.
  `__init__.py` exports `ElectroPioreactor` for clean downstream imports.
- **Docs**: README "41 tests" claim removed (was stale); install
  instructions use `pip install -e ".[dev]"` instead of pointing at the
  removed `requirements-dev.txt`.
- **Persistence smoke test**: new `TestPersistence` class exercises the
  real configparser + atomic-write path so a regression that breaks
  setter-to-disk persistence is caught off-device.

46 tests pass off-device (verified on Pi venv).

---

## v0.6.1 (2026-04-29) — data-layer persistence fixed

### What was actually wrong

`published_settings` declared each setting with only `{datatype, settable}`.
Pioreactor's `BackgroundJob._clear_caches` runs during clean-up and, for every
entry without `persist: True`, publishes a `None` payload to the retained MQTT
topic and zeros the corresponding row in the SQLite metadata DB
(`pio_job_published_settings`). Result: every Stop wiped our four settings from
both data sources. The Advanced modal subscribes to those retained MQTT topics;
with our values nulled, React was left holding whatever it last displayed.

The 0.5.2/0.5.3 atomic-write fixes attacked the wrong layer (config files were
fine), so they had no effect on the symptom.

### Fix

Added `"persist": True` to all four entries in `published_settings`. Same
pattern Pioreactor's own `dosing_automation` uses for `alt_media_throughput` and
`media_throughput`. Verified end-to-end on-device: after a CLI run with
electrolysis_power=7.5, sparge_duration=13, sparge_interval=60,
od_pause_after=4.2 and SIGTERM, both MQTT retained and `pio_job_published_settings`
still hold all four values. Pre-fix, only `$state` survived (4 prior runs of
electropioreactor showed only `$state` in SQLite).

### Also fixed in v0.6.1

`_pause_od_reading` and `_resume_od_reading` called `JobState.SLEEPING.to_bytes()`,
which doesn't exist on str-subclass enums. Threw on every sparge cycle (caught
silently by try/except, but spammed the log). Switched to `.encode()`. Off-device
tests previously passed because `conftest.py` stubbed `JobState` with its own
`.to_bytes()`; that stub was wrong and is now a `str` subclass to mirror upstream.

## Pioreactor version compatibility

The Pioreactor frontend (React) bug that caused the Advanced modal to require
a hard-refresh after Stop was fixed upstream in
[Pioreactor/pioreactor#615](https://github.com/Pioreactor/pioreactor/pull/615),
merged 2026-04-30. The fix lands in **Pioreactor 26.4.5+**; the latest tagged
release at the time of writing was 26.4.4 (2026-04-23).

**Users on 26.4.5 or later** see the modal display fresh values on every
re-open with no extra action.

**Users on 26.4.4 or earlier**: the README install flow (step 3) hot-patches
`pioreactor.web.static` with a pre-built bundle from
`AEP-Plugin/transitional/pioreactor-static-pr615.tar.gz` so the modal also
re-fetches on open. The hot-patch is reversible (the original bundle is
preserved at `pioreactor.web.static.pre-pr615.bak`). After upgrading to
26.4.5+, revert the hot-patch and the upstream-included PR #615 takes over.
The plugin's data layer (config files, MQTT retained, SQLite metadata DB)
is correct on both versions; the symptom was purely React component state.

## Reset toggle

`set_reset_to_defaults(True)` clears `[electropioreactor.config]` from both unit
config files (so `config.ini` defaults apply) then re-saves those defaults. The
toggle is intentionally *not* in `published_settings` — having it there caused
Pioreactor to replay the last `True` value on every restart.

## Atomic writes

`_save_all_config`, `_save_config`, and `_clear_unit_config` write via a
tempfile + `fsync` + `os.replace` to survive power loss mid-write.

## Relevant files

```
AEP-Plugin/pioreactor_electropioreactor_plugin/electropioreactor.py   — main plugin
AEP-Plugin/pioreactor_electropioreactor_plugin/ui/contrib/jobs/electropioreactor.yaml
AEP-Plugin/pioreactor_electropioreactor_plugin/additional_config.ini
AEP-Plugin/setup.py
AEP-Plugin/tests/
```

On device (`pio01`):

```
/home/pioreactor/.pioreactor/config.ini                        — global baseline
/home/pioreactor/.pioreactor/config_<unit>.ini                  — plugin-written, read by web API
/home/pioreactor/.pioreactor/unit_config.ini                   — plugin-written, read by job process
/home/pioreactor/.pioreactor/plugins/ui/jobs/20_electropioreactor.yaml   — UI descriptor (current path; was ui/contrib/jobs/ pre-v0.6.4)
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor_electropioreactor_plugin/
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/static/                — Pioreactor frontend; on 26.4.4 or earlier the README install step 3 hot-patches this with PR #615
```
