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
- CO₂ supply (e.g. SodaStream) ideally with needle valve for flow control. See the [AEP0.1.1 assembly guide](https://github.com/amybo-org/AsepticElectroPioreactor) for one reference build.

## Installation

```
pio plugin install pioreactor-electropioreactor-plugin
```

Or on the whole cluster:

```
pios plugin install pioreactor-electropioreactor-plugin
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

Issues and pull requests welcome at <https://github.com/amybo-org/pioreactor-electropioreactor-plugin>.
