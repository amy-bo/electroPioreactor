# pioreactor-aep-plugin

A [Pioreactor](https://pioreactor.com) community plugin for the **Aseptic ElectroPioreactor (AEP)**.

Provides a single background job, **AEP Sparging**, that:

- Drives electrolysis via **LED channel D** at a configurable power level.
- Periodically opens a CO₂ solenoid (PWM channel 4, `relay`) for a configurable duration.
- Automatically turns LED D **off** during each sparging cycle and restores it immediately after.

All three parameters are editable live from the Pioreactor web interface.

## Hardware requirements

- Pioreactor with an electrode pair wired to **LED channel D**.
- CO₂ solenoid valve wired to **PWM channel 4**.
- SodaStream + needle valve + 0.2 µm vent filters as described in the [AEP0.1.1 assembly guide](https://github.com/amybo-org/AsepticElectroPioreactor).

## Installation

```
pio plugin install pioreactor-aep-plugin
```

Or on the whole cluster:

```
pios plugin install pioreactor-aep-plugin
```

## Configuration

After installation the following defaults are merged into your `unit_config.ini`:

```ini
[PWM]
4=relay

[aep_sparging.config]
electrolysis_power=3.0       ; LED D intensity (%)
sparge_duration_seconds=10.0 ; solenoid open time per cycle (s)
sparge_interval_hours=1.0    ; cycle frequency (h)
```

Adjust values in the Pioreactor **Configuration** page, or change them live via the **Settings** panel in the web interface.

## Starting the job

Via the web interface: open the **Activities** tab on the *Manage* screen and start **AEP Sparging**.
All three parameters can then be adjusted live from the **Settings** panel without restarting the job.

Via CLI:

```
pio run aep_sparging --electrolysis-power 2.5 --sparge-duration-seconds 10 --sparge-interval-hours 1
```

## Contributing

Issues and pull requests welcome at <https://github.com/amybo-org/pioreactor-aep-plugin>.
