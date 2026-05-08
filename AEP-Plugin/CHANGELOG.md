# electroPioreactor Plugin — Changelog

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
