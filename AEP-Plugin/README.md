# electroPioreactor-plugin

A [Pioreactor](https://pioreactor.com) community plugin for the **[electroPioreactor](https://electroPioreactor.org)** – any Pioreactor fitted with an electrode pair driven by LED D and a CO₂ solenoid driven by PWM channel 4.

Provides a single background job, **electroPioreactor**, that:

- Drives electrolysis (via LED channel D) at a user-defined power level (0–10 %, clamped at runtime to protect the electrodes).
- Sparges CO₂ by periodically opening a CO₂ solenoid (PWM channel 4 relay) for a user-defined duration, at a user-defined interval in minutes.
- Automatically pauses electrolysis (LED D → 0 %) for the duration of each sparge and resumes it immediately after.
- Pauses the `od_reading` job for the duration of the sparge plus a user-defined settle window, so OD samples aren't contaminated by bubbles.

All four user-defined parameters are editable live from the Pioreactor web interface.

### OD pausing

`od_pause_after_sparge_seconds` (default `5.0`) is the number of seconds **after the CO₂ solenoid closes** before OD reading resumes – the bubble-clearance window. The total OD pause window is `sparge_duration_seconds + od_pause_after_sparge_seconds`, measured from sparge start.

- **Positive** → pause OD for the full sparge plus N seconds of settle time. Typical.
- **Zero** → resume OD the instant the solenoid closes.
- **Negative** → resume OD part-way through the sparge (OD continues through the tail end of sparging).
- **≤ −`sparge_duration_seconds`** → total pause ≤ 0; OD is not paused at all. Use a large negative (e.g. `-99999`) to disable the feature entirely.

Pause/resume is done by publishing `JobState.SLEEPING`/`READY` to `od_reading`'s `$state/set` topic. If `od_reading` isn't running, the publish is a no-op.

## Hardware requirements

- Pioreactor with an electrode pair wired to **LED channel D**.
- CO₂ solenoid valve wired to **PWM channel 4**.
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

**Inside the SSH session on the Pi**, paste each block below one at a time. Wait for each command to finish (the prompt returns) before pasting the next:

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

The last line should print `Version: 0.6.5` (or later).

### 3. Apply the version-specific frontend patch

Check which Pioreactor version your unit is running:

```bash
/opt/pioreactor/venv/bin/pio version
```

#### If the output is `26.4.5` or later

The plugin's Advanced modal works out of the box on these versions. **Skip to step 4.**

#### If the output is `26.4.4` or earlier

The plugin's Advanced modal needs Pioreactor [PR #615](https://github.com/Pioreactor/pioreactor/pull/615) (merged to master 2026-04-30, will ship in 26.4.5). Hot-patch the running frontend with a pre-built bundle from this repo:

```bash
bash ~/electroPioreactor/AEP-Plugin/scripts/apply-pr615-patch.sh
```

The original bundle is preserved at `<pioreactor.web.static>.pre-pr615.bak`. To revert after you upgrade to 26.4.5+:

```bash
bash ~/electroPioreactor/AEP-Plugin/scripts/revert-pr615-patch.sh
```

### 4. Deploy the UI job descriptor

```bash
bash ~/electroPioreactor/AEP-Plugin/scripts/deploy-ui-yaml.sh
```

### 5. Patch `config.ini` (idempotent)

Adds `[PWM] 4=relay` and the four `[electropioreactor.config]` defaults. Re-runs are safe; existing keys are preserved.

```bash
/opt/pioreactor/venv/bin/python ~/electroPioreactor/AEP-Plugin/scripts/patch-config-ini.py
```

See **Configuration** below for what these values mean.

### 6. Restart `lighttpd`

```bash
sudo systemctl restart lighttpd
```

### 7. Verify

Paste each block one at a time:

```bash
DOT_PIOREACTOR=/home/pioreactor/.pioreactor /opt/pioreactor/venv/bin/pio plugins list 2>&1 | grep electro
```

```bash
ls -la ~/.pioreactor/plugins/ui/jobs/20_electropioreactor.yaml
```

```bash
curl -s http://localhost/unit_api/jobs/descriptors | python3 -c "import sys,json; print('electropioreactor' in [j['job_name'] for j in json.load(sys.stdin)])"
```

Expected:
- `pioreactor-electropioreactor-plugin==0.6.5` (or later) from `pio plugins list`
- The YAML file present, owned by `pioreactor:www-data`
- `True` from the descriptor check

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
electrolysis_power=2.5              ; LED D intensity (0–10 %, clamped at runtime)
sparge_duration_seconds=10.0        ; solenoid open time per cycle (s)
sparge_interval_minutes=60.0        ; cycle frequency (min)
od_pause_after_sparge_seconds=5.0   ; OD settle window after sparge ends (s); negative allowed
```

Adjust these values in the Pioreactor **Configuration** page, or change them live via the **Settings** panel on the *Manage* screen while the job is running.

`od_pause_after_sparge_seconds` can be edited live, but the new value only takes effect on the **next** sparge cycle – an in-flight OD pause uses the value that was set when that sparge began.

## Starting the job

Via the web interface: open the **Activities** tab on the *Manage* screen and start **electroPioreactor**. All four parameters can then be adjusted live from the **Settings** panel without restarting the job.

Via CLI:

```bash
pio run electropioreactor \
    --electrolysis-power 2.5 \
    --sparge-duration-seconds 10 \
    --sparge-interval-minutes 60 \
    --od-pause-after-sparge-seconds 5
```

## Pioreactor version compatibility

This plugin's Advanced modal depends on Pioreactor [PR #615](https://github.com/Pioreactor/pioreactor/pull/615) (merged to master 2026-04-30, will ship in **26.4.5**) for the modal to re-fetch from disk on open after a Stop. On 26.4.4 and earlier, the install flow above hot-patches the running frontend with a pre-built bundle (step 3) so the behaviour is consistent across versions. The plugin's own data-layer persistence bug (which made the same scenario actually *wipe* values from MQTT/SQLite, not just appear stale) was fixed in v0.6.1.

Once 26.4.5 ships and you upgrade, you can revert the hot-patch (revert command shown in step 3) – the upgraded Pioreactor frontend will include PR #615 natively.

## Contributing

Issues and pull requests welcome at <https://github.com/amy-bo/electroPioreactor>.
