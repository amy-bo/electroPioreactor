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

### From the card

Needs a Pioreactor OS release with boot-partition plugin support (proposed at https://github.com/amy-bo/CustoPiZer/tree/bootfs-plugins and accepted by Pioreactor; until it ships, use the SSH route below).

1. Flash a Pioreactor image following [Pioreactor's software set-up guide](https://docs.pioreactor.com/user-guide/software-set-up). Before you click **Write**, untick **Eject media when finished** in Imager's options.
2. While the card writes, download and unzip the [card bundle](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-card-bundle.zip).
3. When the write finishes, drag the `pioreactor` folder from the bundle onto the `bootfs` drive. If the card was ejected anyway, remove and reinsert it.
4. Eject the card and continue Pioreactor's guide from its step 18. When the web interface loads, **electroPioreactor** is under **Activities** on the unit's *Manage* page.

If it is missing, put the card back in your computer: `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong.

Worker-only units: the same steps with a **Worker** image. The plugin installs when you add the unit from the leader's **Inventory** page.

### Over SSH

For a unit that is already running, or an OS release without boot-partition plugin support.

1. Download and unzip the [card bundle](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-card-bundle.zip) on your computer.
2. In a terminal, from the unzipped `pioreactor/plugins` folder, with `<hostname>` replaced by the unit's name. Each command asks for the unit's password; answer `yes` if asked about a fingerprint.

   ```bash
   scp pioreactor_electropioreactor_plugin-*.whl pioreactor@<hostname>.local:
   ssh pioreactor@<hostname>.local '/opt/pioreactor/venv/bin/pio plugins install pioreactor-electropioreactor-plugin --source pioreactor_electropioreactor_plugin-*.whl'
   ```

3. Refresh the unit's web interface: **electroPioreactor** is under **Activities** on the *Manage* page.

## Configuration

Installation sets these defaults:

```ini
[PWM]
4=relay

[electropioreactor.config]
electrolysis_power=2.5              ; LED D intensity (0–10 %, clamped at runtime)
sparge_duration_seconds=10.0        ; solenoid open time per cycle (s)
sparge_interval_minutes=60.0        ; cycle frequency (min)
od_pause_after_sparge_seconds=5.0   ; OD settle window after sparge ends (s); negative allowed
```

Change them on the Pioreactor **Configuration** page, or live in the job's **Settings** panel while it runs. A new `od_pause_after_sparge_seconds` applies from the next sparge.

## Starting the job

In the web interface: open **Activities** on the *Manage* page and start **electroPioreactor**. All four parameters can be changed live from **Settings** without restarting.

From the command line:

```bash
pio run electropioreactor \
    --electrolysis-power 2.5 \
    --sparge-duration-seconds 10 \
    --sparge-interval-minutes 60 \
    --od-pause-after-sparge-seconds 5
```

## Pioreactor version

Requires Pioreactor 26.5.0 or later. On an older unit, run `pio update` first.

## Development

```bash
git clone https://github.com/amy-bo/electroPioreactor.git
cd electroPioreactor/AEP-Plugin
pip install -e ".[dev]"
pytest tests/                   # off-device, no Pi needed
```

## Contributing

Issues and pull requests welcome at <https://github.com/amy-bo/electroPioreactor>.
