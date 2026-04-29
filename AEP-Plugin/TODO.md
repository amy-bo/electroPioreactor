# electroPioreactor Plugin — Status

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

## Known issue: hard-refresh after Stop

The Pioreactor frontend (React) does **not** re-fetch settings when the job
transitions to disconnected. With the data layer correctly populated by v0.6.1,
hard-refreshing the browser tab (Cmd+Shift+R) after Stop shows the right values.
Without hard-refresh, the modal continues to show whatever it had cached in
local React state at the moment of Stop.

This is upstream Pioreactor frontend behaviour. Investigation underway to
identify whether the plugin can publish a signal that triggers re-render
without a frontend patch.

**Workaround for users:** hard-refresh (Cmd+Shift+R) after Stop if you want to
re-open the Advanced modal and see current values.

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
/home/pioreactor/.pioreactor/config_pio01.ini                  — plugin-written, read by web API
/home/pioreactor/.pioreactor/unit_config.ini                   — plugin-written, read by job process
/home/pioreactor/.pioreactor/ui/contrib/jobs/20_electropioreactor.yaml
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor_electropioreactor_plugin/
```
