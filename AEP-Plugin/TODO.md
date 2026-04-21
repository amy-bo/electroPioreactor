# electroPioreactor Plugin — Status

## Persistence — still broken, cause unknown (as of 2026-04-21 evening)

**Earlier "verified on v0.5.2" claim was wrong.** On 2026-04-21 a fresh install
from `AEP-Plugin` at `1308b11` uninstalled `pioreactor-electropioreactor-plugin-0.5.0`
— i.e. the device had been running 0.5.0 the whole time the "verification"
commits were made, so nothing about 0.5.2's persistence changes was ever
observed running on-device. Previous TODO notes asserting otherwise were
inferred from code and API responses, not from the modal behaviour itself.

After installing v0.5.3 cleanly today and deploying the UI job descriptor
(`~/.pioreactor/ui/contrib/jobs/20_electropioreactor.yaml`) with `lighttpd`
restarted, the user reports the Advanced modal **still** shows stale values
after Start/Stop. So the fix in 0.5.2 does not resolve the symptom and the
stale-React-state theory in the earlier "Known UX pitfall" section is unproven.

## Next debugging step (requires on-device access)

The goal is to narrow *which* source of truth is stale. Reproduce by setting
new values → Start → Stop, then — without hard-refreshing the browser —
check all three at once:

```bash
ssh pioreactor@pioreactor.local
# 1. Files the job writes
grep -A3 '\[electropioreactor.config\]' ~/.pioreactor/config_pio01.ini \
    ~/.pioreactor/unit_config.ini

# 2. What the web API returns (this is what the modal *should* display on remount)
curl -s http://pioreactor.local/api/config/units/pio01 | python3 -m json.tool \
    | grep -iE 'electro|sparge'

# 3. MQTT retained state (what published_settings writes back)
mosquitto_sub -h localhost -C 3 -t 'pioreactor/pio01/+/electropioreactor/#' -v
```

Then compare with what the Advanced modal displays and what was typed in.
Whichever of the three disagrees tells you the layer that's failing:
- Files wrong  → `_save_*` not being called, or being called with old values
- API wrong    → Pioreactor API caches files, needs rescan trigger
- MQTT wrong   → `published_settings` setter isn't being invoked
- All three right but modal wrong → React stale-state (then hard-refresh fixes it)

## What IS known to work

- 26/26 off-device tests pass (`python3 -m pytest tests/` from `AEP-Plugin/`)
- v0.5.3 installs cleanly on the device
- CLI `pio run electropioreactor` starts the job
- The YAML descriptor with `min: 0 / max: 10` on `electrolysis_power`
  is now deployed (just not exercised yet)
- Runtime clamp of `electrolysis_power` to `[0, 10]` (authoritative, applied
  in `__init__`, every `set_*` handler, and at CLI-option default)

## Device state as of 2026-04-21 evening

- `pioreactor.local` (pio01): v0.5.3 installed, UI YAML deployed, powered down
- `pi02.local`: SSH up but rejecting our key; requires physical reflash
  (see `pi02-setup-notes.md` at repo root) — user will do this 2026-04-22

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
/home/pioreactor/electropioreactor-plugin/                     — git checkout
/home/pioreactor/.pioreactor/config.ini                        — global baseline
/home/pioreactor/.pioreactor/config_pio01.ini                  — plugin-written, read by web API
/home/pioreactor/.pioreactor/unit_config.ini                   — plugin-written, read by job process
/home/pioreactor/.pioreactor/ui/contrib/jobs/20_electropioreactor.yaml  — UI descriptor (deployed 2026-04-21)
/opt/pioreactor/venv/lib/python3.13/site-packages/pioreactor_electropioreactor_plugin/
```

## Reset toggle

`set_reset_to_defaults(True)` clears `[electropioreactor.config]` from both unit
config files (so `config.ini` defaults apply) then re-saves those defaults. The
toggle is intentionally *not* in `published_settings` — having it there caused
Pioreactor to replay the last `True` value on every restart.

## Atomic writes

`_save_all_config`, `_save_config`, and `_clear_unit_config` write via a
tempfile + `fsync` + `os.replace` to survive power loss mid-write.
