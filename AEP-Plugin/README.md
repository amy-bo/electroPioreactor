# electroPioreactor-plugin

A [Pioreactor](https://pioreactor.com) community plugin for the **[electroPioreactor](https://electroPioreactor.org)** - any Pioreactor fitted with an electrode pair driven by LED D and a CO₂ solenoid driven by PWM channel 4.

Provides a single background job, **electroPioreactor**, that:

- Drives electrolysis (via LED channel D) at a user-defined power level (0–10 %, clamped at runtime to protect the electrodes).
- Sparges CO₂ by periodically opening a CO₂ solenoid (PWM channel 4 relay) for a user-defined duration, at a user-defined interval in minutes.
- Automatically pauses electrolysis (LED D → 0 %) for the duration of each sparge and resumes it immediately after.
- Pauses the `od_reading` job for the duration of the sparge plus a user-defined settle window, so OD samples aren't contaminated by bubbles.

All four user-defined parameters are editable live from the Pioreactor web interface.

### OD pausing

`od_pause_after_sparge_seconds` (default `5.0`) is the number of seconds **after the CO₂ solenoid closes** before OD reading resumes — i.e. the bubble-clearance window. The total OD pause window is `sparge_duration_seconds + od_pause_after_sparge_seconds`, measured from sparge start.

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

### Option B — from GitHub (current)

The plugin is not on PyPI yet. Install from source into the Pioreactor venv:

```bash
ssh pioreactor@<your-pioreactor>.local
cd ~
sudo apt update && sudo apt install -y git
git clone https://github.com/amy-bo/electroPioreactor.git
git -C electroPioreactor checkout AEP-Plugin
/opt/pioreactor/venv/bin/pip install ./electroPioreactor/AEP-Plugin
```

Deploy the UI job descriptor so the job appears in the **Activities** panel:

```bash
PLUGIN=/opt/pioreactor/venv/lib/python3.*/site-packages/pioreactor_electropioreactor_plugin
mkdir -p ~/.pioreactor/plugins/ui/jobs
cp $PLUGIN/ui/contrib/jobs/electropioreactor.yaml \
   ~/.pioreactor/plugins/ui/jobs/20_electropioreactor.yaml
```

Add the PWM-4 relay mapping and default values to `~/.pioreactor/config.ini` (idempotent – re-runs are safe; existing keys are preserved):

```bash
/opt/pioreactor/venv/bin/python <<'PY'
import configparser
path = "/home/pioreactor/.pioreactor/config.ini"
p = configparser.ConfigParser()
p.read([path])
if "PWM" not in p: p.add_section("PWM")
p["PWM"]["4"] = "relay"
sec = "electropioreactor.config"
if sec not in p: p.add_section(sec)
for k, v in {
    "electrolysis_power": "2.5",
    "sparge_duration_seconds": "10.0",
    "sparge_interval_minutes": "60.0",
    "od_pause_after_sparge_seconds": "5.0",
}.items():
    p[sec].setdefault(k, v)
with open(path, "w") as f:
    p.write(f)
PY
```

See **Configuration** below for what these values mean. Restart `lighttpd` so the web UI picks up the new job descriptor:

```bash
sudo systemctl restart lighttpd
```

Hard-refresh the browser and the **electroPioreactor** job will appear under *Activities*.

### Option A — from PyPI (future)

Once the plugin is published to PyPI, installation will be a one-liner:

```bash
pio plugin install pioreactor-electropioreactor-plugin
```

Or on the whole cluster:

```bash
pios plugin install pioreactor-electropioreactor-plugin
```

### Option C — pre-built OS image (future)

A Raspberry Pi OS image with the plugin pre-installed and pre-configured is published from the `electroPioreactorOS` branch of this repo. See `electropioreactor-image/README.md` on that branch, or flash via Raspberry Pi Imager using the custom URL `https://amy-bo.github.io/electroPioreactor/os-list.json` (available after the OS branch is merged and the first release is cut).

### Option D — local development (off-device)

```bash
git clone https://github.com/amy-bo/electroPioreactor.git
cd electroPioreactor/AEP-Plugin
pip install -e ".[dev]"
pytest tests/                   # off-device, no Pi needed
```

## Configuration

Add the following to `~/.pioreactor/config.ini`:

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

`od_pause_after_sparge_seconds` can be edited live, but the new value only takes effect on the **next** sparge cycle — an in-flight OD pause uses the value that was set when that sparge began.

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

This plugin requires **Pioreactor 26.4.5 or later** for full-fidelity Advanced-modal behaviour.

On Pioreactor 26.4.4 and earlier, after you Start and then Stop the job, re-opening the Advanced modal in the same browser tab may show the values from before the run — the data underneath is correct, but Pioreactor's React frontend doesn't re-fetch when the job transitions to disconnected. Workaround on those versions: hard-refresh the tab (Ctrl/Cmd+Shift+R).

This is fixed upstream in Pioreactor 26.4.5+ via [Pioreactor/pioreactor#615](https://github.com/Pioreactor/pioreactor/pull/615). The plugin's own data-layer persistence bug (which made the same scenario actually *wipe* values from MQTT/SQLite, not just appear stale) was fixed in v0.6.1.

## Contributing

Issues and pull requests welcome at <https://github.com/amy-bo/electroPioreactor>.
