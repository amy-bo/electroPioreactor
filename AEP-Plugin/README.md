# electroPioreactor-plugin

A [Pioreactor](https://pioreactor.com) community plugin for the **[electroPioreactor](https://electroPioreactor.org)** – any Pioreactor fitted with an electrode pair driven by an LED channel and a CO₂ solenoid driven by a PWM channel.

Provides a single background job, **electroPioreactor**, that:

- Drives electrolysis (via the configured LED channel, default **D**) at a user-defined power level (0–10 %, clamped at runtime to protect the electrodes).
- **Cycles electrolysis ON/OFF** on a user-defined schedule (`electrolysis_on_seconds` ON, then `electrolysis_off_seconds` OFF, repeating). Set the OFF time to `0` for continuous electrolysis.
- Sparges CO₂ by periodically opening a CO₂ solenoid (the configured PWM channel, default **4**) for a user-defined duration, at a user-defined interval in minutes.
- Pauses electrolysis (LED → 0 %) for the duration of each sparge and resumes it immediately after.
- Pauses the `od_reading` job around each electrolysis ON phase (plus a user-defined window) and, independently, around each CO₂ sparge, so OD samples aren't contaminated by electrolysis or bubbles.

All electrolysis and sparging parameters are editable live from the Pioreactor web interface. The LED and PWM channels are set in `config.ini` (they're hardware bindings, not runtime settings — see **Hardware connections**).

### Electrolysis ON/OFF cycling

- `electrolysis_on_seconds` (default `60.0`) – how long electrolysis is ON each cycle. Must be > 0.
- `electrolysis_off_seconds` (default `0.0`) – how long electrolysis is OFF between ON phases. Must be ≥ 0; `0` = continuous electrolysis (no OFF phase, identical to the pre-v0.7 behaviour).

A mid-cycle change applies to the **next** phase, not the in-flight one.

### OD pausing around electrolysis

`od_pause_after_electrolysis_seconds` (default `5.0`) is the settle window **after each electrolysis ON phase ends** before OD reading resumes. The effective OD-suppression window, measured from the start of the ON phase, is:

```
od_pause_window = electrolysis_on_seconds + od_pause_after_electrolysis_seconds   (floored at 0)
```

This value is **allowed to go negative**, down to (and below) −`electrolysis_on_seconds`. A negative value eats into the ON-phase pause, so OD resumes *before* electrolysis ends and OD is measured **during** electrolysis. Worked example with `electrolysis_on_seconds = 10`:

| `od_pause_after_electrolysis_seconds` | window | behaviour |
|---|---|---|
| `+5` | `15` | OD off for the 10 s ON phase + 5 s settle after. Typical. |
| `0`  | `10` | OD off for exactly the ON phase. |
| `−3` | `7`  | OD resumes at t = 7 s, **3 s before electrolysis ends** → OD measured during the tail of electrolysis. |
| `−10` (= −on) | `0` | OD never paused → OD measured throughout electrolysis. |
| `−99999` | `0` | clamped to 0; disables this OD pause entirely. |

### OD pausing around sparging

`od_pause_after_sparge_seconds` (default `5.0`) is the bubble-clearance window **after the CO₂ solenoid closes** before OD reading resumes. The total OD pause window is `sparge_duration_seconds + od_pause_after_sparge_seconds`, measured from sparge start, and follows the same positive/zero/negative rules as the electrolysis OD pause (negatives down to −`sparge_duration_seconds` shorten or cancel the pause).

Pause/resume is done by publishing `JobState.SLEEPING`/`READY` to `od_reading`'s `$state/set` topic. If `od_reading` isn't running, the publish is a no-op.

## Hardware connections

The electrode pair drives an LED channel and the CO₂ solenoid drives a PWM channel; **both are configurable** in `~/.pioreactor/config.ini` so the plugin doesn't assume a fixed channel is free (e.g. if other jobs occupy LED slots).

- **LED channel** for the electrode pair: `[electropioreactor.config] led_channel = D` (one of `A`, `B`, `C`, `D`; default `D`). An invalid label makes the job refuse to start with a clear error.
- **PWM channel** for the CO₂ solenoid: Pioreactor's own `[PWM] N = relay` label indirection. The plugin opens whichever PWM channel is labelled `relay`. The install flow sets `[PWM] 4 = relay`; to use a different channel, wire the solenoid there and set e.g. `[PWM] 2 = relay` instead.

## Hardware requirements

- Pioreactor with an electrode pair wired to the configured **LED channel** (default D).
- CO₂ solenoid valve wired to the configured **PWM channel** (default 4).
- CO₂ supply (e.g. SodaStream) ideally with a needle valve for flow control.

## Installation

Skip step 1 if your Pioreactor is already imaged and reachable on its network.

### 1. (Optional) Flash a fresh Pioreactor image

> ⚠️ **Warning**
> Flashing wipes the SD card. Only do this if you are starting from scratch and have **no data on the unit you want to keep** – any experiments, calibrations, or local config on the SD card will be lost.

Follow [Pioreactor's official software-installation guide](https://docs.pioreactor.com/user-guide/software-set-up). The steps below mirror that doc verbatim; if Pi Imager's UI changes, that page is the source of truth.

On your Mac/Windows/Linux machine, install [Raspberry Pi Imager](https://www.raspberrypi.com/software/), then:

1. Open Raspberry Pi Imager.
2. Immediately click **App Options**.
3. Click **Edit** next to **Content Repository**.
4. Choose **Use Custom URL** and paste:

   ```
   https://pioreactor.com/imager/os-list.json
   ```
5. Click **Apply & restart**.
6. Choose your RPi model and click **Next** (Raspberry Pi Zero 2 W for current ed04 hardware).
7. Choose the operating system **Pioreactor**
8. Choose the **latest** OS on the list (at the top)
9. Choose **Leader + Worker** and click **Next**. (Use **Worker** instead if this unit will join an existing cluster as a worker only; **Leader** if you want a leader that doesn't itself run experiments. For a stand-alone unit like ed04, pick Leader + Worker.)
10. Insert your microSD card and select it as your **Storage** device.
11. Input a unique hostname for this unit (e.g. `ed04`). **Do not use `pioreactor` or `raspberrypi`** – those names are reserved and will break mDNS resolution. Click **Next**.
12. Change localization preferences (time zone, keyboard layout) and click **Next**.
13. enter **Username**: `pioreactor` (do not change – the Pioreactor image hardcodes this username and several plugin install paths assume it).
14. enter **Password**: Pioreactor's docs use `raspberry`; pick something stronger for any unit that will run real experiments. Enter password again and click **Next**.
15. Enter your **SSID** and **WiFi password** (optional if using Ethernet - note Raspberry Pi Zero's do not have Ethernet so WiFi is required). Click **Next**.
16. Confirm **Enable SSH** is active and **Use password authentication** is selected. Click **Next**.
17. Click **Write** to begin imaging. Accept any permission prompts. Writing takes up to 5 minutes.

When the write finishes, eject the card and insert it into the Raspberry Pi (HAT attached, power unplugged). The microSD slot is on the PWM side. Plug power in; after a few minutes the Pioreactor HAT will briefly blink a blue LED to indicate first-boot is complete.

In a browser, navigate to `http://<hostname>.local` (e.g. `http://ed04.local`) – the Pioreactor lighttpd web UI loads unauthenticated when ready. When the UI loads you'll be prompted by an **Update Pioreactor model** dialog: select the correct model and hardware version, then click **Save**.

> ℹ️ **The Pioreactor image is headless by design.** A connected monitor will stay blank even on a fully working unit (HDMI output, ACT LED, and boot splash are all disabled in `/boot/firmware/config.txt`). Don't troubleshoot from screen output – verify boot via the brief blue LED flash, by `ping <hostname>.local` from another device on the same network, or by the web UI loading.

### 2. SSH in and install the plugin

**On your Mac/Windows/Linux shell**, open the SSH session:

```bash
ssh pioreactor@<hostname>.local
```

Type `yes` to accept the host fingerprint on first connect, then enter the password you set in step 1.

**Inside the SSH session on the Pi**:

```bash
cd ~
```

```bash
sudo apt update && sudo apt install -y git
```

```bash
git clone https://github.com/amy-bo/electroPioreactor.git
```

```bash
git -C electroPioreactor checkout AEP-Plugin
```

```bash
/opt/pioreactor/venv/bin/pip install ./electroPioreactor/AEP-Plugin
```

```bash
/opt/pioreactor/venv/bin/pip show pioreactor-electropioreactor-plugin | grep Version
```

The last line should print `Version: 0.7.0` (or later).

### 3. Deploy the UI job descriptor

```bash
bash /home/pioreactor/electroPioreactor/AEP-Plugin/scripts/deploy-ui-yaml.sh
```

### 4. Patch `config.ini` (idempotent)

Adds `[PWM] 4=relay` and the four `[electropioreactor.config]` defaults. Re-runs are safe; existing keys are preserved.

```bash
/opt/pioreactor/venv/bin/python /home/pioreactor/electroPioreactor/AEP-Plugin/scripts/patch-config-ini.py
```

See **Configuration** below for what these values mean.

### 5. Restart `lighttpd`

```bash
sudo systemctl restart lighttpd
```

### 6. Verify

```bash
export DOT_PIOREACTOR=/home/pioreactor/.pioreactor
```

```bash
/opt/pioreactor/venv/bin/pio plugins list 2>&1 | grep electro
```

Expected: `pioreactor-electropioreactor-plugin==0.7.0` (or later).

```bash
ls -la /home/pioreactor/.pioreactor/plugins/ui/jobs/20_electropioreactor.yaml
```

Expected: file present, owned by `pioreactor:www-data`.

```bash
curl -s http://localhost/unit_api/jobs/descriptors | grep -c electropioreactor
```

Expected: `1`.

Then in your browser, hard-refresh `http://<hostname>.local/` (Ctrl/Cmd+Shift+R), navigate to **Pioreactors → `<hostname>` → Manage**, and **electroPioreactor** should appear under **Activities**.

## Other installation methods

### From PyPI (future)

Once the plugin is published to PyPI, installation will be a one-liner:

```bash
pio plugin install pioreactor-electropioreactor-plugin
```

Or on the whole cluster:

```bash
pios plugin install pioreactor-electropioreactor-plugin
```

### Pre-built OS image (future)

A Raspberry Pi OS image with the plugin pre-installed and pre-configured is published from the `electroPioreactorOS` branch of this repo. See `electropioreactor-image/README.md` on that branch, or flash via Raspberry Pi Imager using the custom URL `https://amy-bo.github.io/electroPioreactor/os-list.json` (available after the OS branch is merged and the first release is cut).

### Local development (off-device)

```bash
git clone https://github.com/amy-bo/electroPioreactor.git
cd electroPioreactor/AEP-Plugin
pip install -e ".[dev]"
pytest tests/                   # off-device, no Pi needed
```

## Configuration

The install flow above writes the following to `~/.pioreactor/config.ini`:

```ini
[PWM]
4=relay

[electropioreactor.config]
led_channel=D                            ; LED channel for the electrode pair (A/B/C/D)
electrolysis_power=2.5                    ; LED intensity (0–10 %, clamped at runtime)
electrolysis_on_seconds=60.0             ; electrolysis ON time per cycle (s, > 0)
electrolysis_off_seconds=0.0             ; electrolysis OFF time per cycle (s, >= 0; 0 = continuous)
od_pause_after_electrolysis_seconds=5.0  ; OD settle window after electrolysis ON ends (s); negative allowed
sparge_duration_seconds=10.0             ; solenoid open time per cycle (s)
sparge_interval_minutes=60.0             ; cycle frequency (min)
od_pause_after_sparge_seconds=5.0        ; OD settle window after sparge ends (s); negative allowed
```

Adjust the numeric values in the Pioreactor **Configuration** page, or change them live via the **Settings** panel on the *Manage* screen while the job is running. `led_channel` is a hardware binding and is read once at job start (see **Hardware connections**); change it in `config.ini` and restart the job to switch channels.

The OD-pause and cycle-duration settings can be edited live, but a new value only takes effect on the **next** phase/cycle – an in-flight pause uses the value that was set when that phase began.

## Starting the job

Via the web interface: open the **Activities** tab on the *Manage* screen and start **electroPioreactor**. All numeric parameters can then be adjusted live from the **Settings** panel without restarting the job.

Via CLI:

```bash
pio run electropioreactor \
    --electrolysis-power 2.5 \
    --electrolysis-on-seconds 60 \
    --electrolysis-off-seconds 0 \
    --od-pause-after-electrolysis-seconds 5 \
    --sparge-duration-seconds 10 \
    --sparge-interval-minutes 60 \
    --od-pause-after-sparge-seconds 5
```

## Pioreactor version compatibility

Requires **Pioreactor ≥ 26.5.0** (released 2026-05-07). Earlier releases lack [PR #615](https://github.com/Pioreactor/pioreactor/pull/615) (merged 2026-04-30), without which the plugin's Advanced modal would need a hard-refresh after each Stop to display fresh values. The plugin's own data-layer persistence bug (which actually *wiped* values from MQTT/SQLite) was fixed in v0.6.1.

If your unit is on an older Pioreactor, run `pio update` before installing this plugin.

## Contributing

Issues and pull requests welcome at <https://github.com/amy-bo/electroPioreactor>.

### Release checklist (maintainers)

When bumping the plugin version, update the version string in **all** of these in the same commit, or the install/verify instructions go stale:

- `setup.py` (`version=`)
- `pioreactor_electropioreactor_plugin/electropioreactor.py` (`__plugin_version__`)
- `README.md` — the two expected-version strings in the install/verify steps (`Version: X.Y.Z` and `pioreactor-electropioreactor-plugin==X.Y.Z`); both are written as "(or later)" so a reader on a newer build isn't tripped up, but keep the literal in step with the release.
- `CHANGELOG.md` — add the new version's entry.
