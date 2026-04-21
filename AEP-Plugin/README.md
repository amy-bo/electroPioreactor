# pioreactor-electropioreactor-plugin

A [Pioreactor](https://pioreactor.com) community plugin for **[electroPioreactors](https://electropioreactor.org)** — any Pioreactor fitted with an electrode pair driven by LED D and a CO₂ solenoid driven by PWM channel 4.

Provides a single background job, **electroPioreactor**, that:

- Drives electrolysis (via LED channel D) at a user-defined power level (0–100 %).
- Sparges CO2 by periodically opening a CO₂ solenoid (PWM channel 4 relay) for a user-defined duration, at a user-defined interval in minutes.
- Automatically pauses electrolysis (LED D → 0 %) for the duration of each sparge and resumes it immediately after.

All three user-defined parameters are editable live from the Pioreactor web interface.

## Hardware requirements

- Pioreactor with an electrode pair wired to **LED channel D**.
- CO₂ solenoid valve wired to **PWM channel 4**.
- CO₂ supply (e.g. SodaStream) ideally with needle valve for flow control.

## Installation

The plugin is not on PyPI. Install from GitHub into the Pioreactor venv:

```bash
ssh pioreactor@<your-pioreactor>.local
cd ~
git clone https://github.com/amy-bo/electroPioreactor.git
git -C electroPioreactor checkout AEP-Plugin
/opt/pioreactor/venv/bin/pip install ./electroPioreactor/AEP-Plugin
```

Then deploy the UI job descriptor so the job appears in the **Activities** panel:

```bash
PLUGIN=/opt/pioreactor/venv/lib/python3.*/site-packages/pioreactor_electropioreactor_plugin
mkdir -p ~/.pioreactor/ui/contrib/jobs
cp $PLUGIN/ui/contrib/jobs/electropioreactor.yaml ~/.pioreactor/ui/contrib/jobs/20_electropioreactor.yaml
```

Finally add the PWM-4 relay mapping and default config values to `~/.pioreactor/config.ini`:

```ini
[PWM]
4=relay

[electropioreactor.config]
electrolysis_power=2.5       ; LED D intensity (%)
sparge_duration_seconds=10.0 ; solenoid open time per cycle (s)
sparge_interval_minutes=60.0 ; cycle frequency (min)
```

Restart `lighttpd` (`sudo systemctl restart lighttpd`) so the web UI picks up the
new job descriptor, then hard-refresh the browser.

### Pre-built OS image (alternative)

A Raspberry Pi OS image with the plugin pre-installed and pre-configured is
published from the `electroPioreactorOS` branch of this repo. See
`electropioreactor-image/README.md` on that branch, or flash via Raspberry Pi
Imager using the custom URL `https://amy-bo.github.io/electroPioreactor/os-list.json`
(available after the OS branch is merged and the first release is cut).

### Local development (off-device)

```bash
git clone https://github.com/amy-bo/electroPioreactor.git
cd electroPioreactor/AEP-Plugin
python3 -m pytest tests/        # 25 tests, runs without a Pi
```

## Configuration

After installation the following defaults are merged into your `unit_config.ini`:

```ini
[PWM]
4=relay

[electropioreactor.config]
electrolysis_power=2.5       ; LED D intensity (%)
sparge_duration_seconds=10.0 ; solenoid open time per cycle (s)
sparge_interval_minutes=60.0 ; cycle frequency (min)
```

Adjust values in the Pioreactor **Configuration** page, or change them live via the **Settings** panel in the web interface.

## Starting the job

Via the web interface: open the **Activities** tab on the *Manage* screen and start **electroPioreactor**.
All three parameters can then be adjusted live from the **Settings** panel without restarting the job.

Via CLI:

```
pio run electropioreactor --electrolysis-power 2.5 --sparge-duration-seconds 10 --sparge-interval-minutes 60
```

## Contributing

Issues and pull requests welcome at <https://github.com/amy-bo/electroPioreactor>.
