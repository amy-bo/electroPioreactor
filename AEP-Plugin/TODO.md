# electroPioreactor Plugin — Status

## Persistence — verified working (v0.5.2)

Tested end-to-end on `pio01` on 2026-04-21:

1. Triggered a run via the same PATCH `/api/workers/pio01/jobs/run/...` that the
   Advanced modal uses, with `config_overrides` for all three keys (7.5, 15.0, 30.0).
2. Job started, `on_init_to_ready → _save_all_config` wrote both
   `~/.pioreactor/config_pio01.ini` and `~/.pioreactor/unit_config.ini`.
3. Stopped job via PATCH `/api/workers/pio01/jobs/stop/...`.
4. Queried `/api/config/units/pio01` → returned `{electrolysis_power: "7.5",
   sparge_duration_seconds: "15.0", sparge_interval_minutes: "30.0"}`.

The Advanced modal reads from exactly that endpoint (confirmed by inspecting the
minified React bundle at `/usr/share/pioreactorui/static/static/js/main.b95f4ece.js`,
module `49231`, which initialises both `S` and `O` to the `config` prop passed in
by the parent page, which in turn fetches `/api/config/units/${unit}`). So the
modal will display the persisted values once the page re-mounts.

## Known UX pitfall — not a plugin bug

The parent-page `useEffect(..., [])` fetches `/api/config/units/<unit>` **only on
mount**. If the user stops the job and reopens the Advanced modal without
reloading the page, the React state still holds the values from the last page
load — so the modal looks unchanged even though the API now returns the
persisted values. A hard browser refresh (or navigating away and back) remounts
the component and picks up the correct values.

## Reset toggle

`set_reset_to_defaults(True)` clears `[electropioreactor.config]` from both unit
config files (so `config.ini` defaults apply) and then re-saves those defaults
so the persisted state stays consistent. The toggle is intentionally *not* in
`published_settings` — having it there caused Pioreactor to replay the last
`True` value on every restart.

## Atomic writes

`_save_all_config`, `_save_config`, and `_clear_unit_config` now write via a
tempfile + `os.replace` to survive a power loss mid-write.

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
/home/pioreactor/electropioreactor-plugin/                         — git checkout, editable-installed
/home/pioreactor/.pioreactor/config.ini                            — global baseline
/home/pioreactor/.pioreactor/config_pio01.ini                      — plugin-written, read by web API
/home/pioreactor/.pioreactor/unit_config.ini                       — plugin-written, read by job process
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/api.py     line 2751
/usr/share/pioreactorui/static/static/js/main.b95f4ece.js          — compiled React UI
```
