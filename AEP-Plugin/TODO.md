# electroPioreactor Plugin — Outstanding Issues

## Critical: Settings do not persist across stop/start

### What the user wants

Set values in the Advanced modal (Electrolysis Power, Sparging Duration, Sparging Interval),
stop the job, reopen Advanced, and see those same values.

### What actually happens

The Advanced modal always shows whatever values were in the config files when the job last
started — which tends to be the global `config.ini` defaults (2.5%, 10s, 60min), or
previously-stale values, rather than what the user last entered.

---

## What has been investigated and confirmed

### Pioreactor config architecture (confirmed by reading source on device)

There are **three separate config stores** on a single-unit leader/worker setup:

| File | Who writes it | Who reads it |
|------|--------------|--------------|
| `~/.pioreactor/config.ini` | Web UI Config Editor / manual | Everything — global baseline |
| `~/.pioreactor/config_pio01.ini` | Web UI Config Editor / manual | Leader web API (`GET /api/config/units/pio01`) → populates Advanced modal form |
| `~/.pioreactor/unit_config.ini` | `pios sync-config` / manual | Job process (`pioreactor.config.get_config()`) → determines startup values |

Key source references on the device:
- `get_config()` in `/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/config.py` line 127: reads `config.ini` + `unit_config.ini`
- `/api/config/units/<unit>` in `/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/api.py` line 2750: reads `config.ini` + `config_<unit>.ini`

These are **different files**. A write to `unit_config.ini` is invisible to the Advanced form. A write to `config_pio01.ini` is invisible to the job process at startup.

### How the Advanced modal starts a job (confirmed from logs)

When the user clicks Start, the web UI sends:

```
PATCH /api/workers/pio01/jobs/run/job_name/electropioreactor/experiments/<exp>
Body: {"config_overrides": [["electropioreactor.config", "electrolysis_power", "<val>"], ...]}
```

These config_overrides become CLI flags:

```
pio run --config-override electropioreactor.config electrolysis_power <val> ... electropioreactor
```

Pioreactor applies them via `temporary_config_changes` (a context manager in `cli/run.py`).
The changes apply to the in-memory `config` object for the duration of the job run, then are
**reverted when the job exits**. They are NOT written to any file by Pioreactor itself.

The form values the UI sends as config_overrides come from whatever `GET /api/config/units/pio01`
returned when the Advanced modal was last opened — i.e., from `config_pio01.ini`.

### Our persistence approach (v0.5.1)

`on_init_to_ready` calls `_save_all_config()`, which writes `self.electrolysis_power`,
`self.sparge_duration_seconds`, `self.sparge_interval_minutes` to both `config_pio01.ini`
AND `unit_config.ini`.

Individual setters (`set_electrolysis_power` etc.) call `_save_config(key, value)` which
also writes to both files.

This was confirmed to work in isolation via command-line test:

```
pio run --config-override electropioreactor.config electrolysis_power 7.5 ... electropioreactor
→ both config files correctly showed 7.5 after run
```

### Why it still fails end-to-end

The **UI sends the wrong config_overrides on start**. Observed in `/var/log/pioreactor.log`:

```
Executing `pio run --config-override electropioreactor.config electrolysis_power 0
  --config-override electropioreactor.config sparge_duration_seconds 0.1
  --config-override electropioreactor.config sparge_interval_minutes 0.1 electropioreactor`
```

Even after manually clearing both config files (so the API returns the `config.ini` defaults
of 2.5, 10, 60), the UI continues to send the old stale values on the next Start click.

The user confirmed they hard-refresh the browser each time, so this is not browser cache.

**Root cause is not yet identified.** The stale config_override values (0, 0.1, 0.1) must be
stored somewhere that survives a config file clear and a browser hard-refresh. Candidates not
yet ruled out:

1. **Pioreactor web server in-memory state** — the Flask/lighttpd process may cache the last
   config_overrides for the job and replay them without re-reading the config file. The web
   server process was NOT restarted during testing.

2. **MQTT retained messages** — Pioreactor publishes setting values to MQTT topics. If the
   broker has retained messages for the published_settings topics, the UI might read these
   retained values rather than the config files when constructing the Advanced form.
   Topic pattern: `pioreactor/pio01/<experiment>/electropioreactor/<setting>`.

3. **The Advanced modal reads from a different API endpoint** — the access log shows
   `GET /api/config/units/pio01` is called, but the Advanced modal may also call
   `/unit_api/jobs/settings/job_name/electropioreactor` or a similar endpoint that returns
   the last-published MQTT values for a stopped job (from the intermittent SQLite cache
   at `/run/pioreactor/cache/local_intermittent_pioreactor_metadata.sqlite`).

4. **The PATCH body is constructed from UI component state that is not re-fetched** — the
   React component might store the form values in local state at mount time and not
   re-populate them from the API when the Advanced modal is reopened without a full component
   remount.

---

## What has NOT been tried yet

- **Restart the Pioreactor web server** (`sudo systemctl restart pioreactor_web` or equivalent)
  to flush any in-memory cached state, then test persistence.

- **Clear MQTT retained messages** for the electropioreactor topics:
  ```bash
  mosquitto_pub -h localhost -t "pioreactor/pio01/Plugin Test/electropioreactor/electrolysis_power" \
    -n --retain
  # repeat for sparge_duration_seconds and sparge_interval_minutes
  ```

- **Inspect the actual PATCH request body** the browser sends (use browser DevTools →
  Network tab → filter for `electropioreactor` → click Start → inspect the request payload).
  This would definitively show whether the UI is sending stale values or fresh ones from
  the config files.

- **Read the Pioreactor web UI source** to understand exactly how the Advanced modal
  constructs its config_override payload — specifically whether it reads from the config
  API, from MQTT retained messages, or from some other source.

---

## Current state of config files on pio01 (as of last reset)

Both `~/.pioreactor/unit_config.ini` and `~/.pioreactor/config_pio01.ini` have been manually
reset to safe defaults:

```ini
[electropioreactor.config]
electrolysis_power = 2.5
sparge_duration_seconds = 10.0
sparge_interval_minutes = 60.0
```

`~/.pioreactor/config.ini` also has the same values in `[electropioreactor.config]`.

---

## Plugin version history relevant to this issue

| Version | Change | Result |
|---------|--------|--------|
| v0.3.0 | Added `reset_to_defaults` to `published_settings`; lazy click defaults | Pioreactor replayed `True` for reset on every restart; settings reset on every start |
| v0.4.0 | `_save_config()` writes to `unit_config.ini` in each setter | UI still showed defaults (reads `config_pio01.ini`, not `unit_config.ini`) |
| v0.5.0 | Removed `reset_to_defaults` from `published_settings`; `_save_all_config()` in `on_init_to_ready` | Reset-on-restart bug fixed; persistence still not working |
| v0.5.1 | `_save_all_config()` and `_save_config()` write to BOTH `config_pio01.ini` AND `unit_config.ini` | File writes confirmed working; UI still sends stale config_overrides on start |

---

## Relevant files

```
AEP-Plugin/pioreactor_electropioreactor_plugin/electropioreactor.py   — main plugin
AEP-Plugin/pioreactor_electropioreactor_plugin/ui/contrib/jobs/electropioreactor.yaml
AEP-Plugin/pioreactor_electropioreactor_plugin/additional_config.ini
AEP-Plugin/setup.py
AEP-Plugin/tests/test_electropioreactor.py
AEP-Plugin/tests/conftest.py
```

On device (pio01):
```
/home/pioreactor/.pioreactor/config.ini
/home/pioreactor/.pioreactor/config_pio01.ini
/home/pioreactor/.pioreactor/unit_config.ini
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/api.py       line 2750
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/unit_api.py  line 528
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/web/tasks.py     line 243
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/config.py        line 127
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor/cli/run.py
/var/log/pioreactor.log
/var/log/lighttpd/access.log
```
