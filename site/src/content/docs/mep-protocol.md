---
slug: MEP/protocol
title: MEP protocol
description: Calibrating and running an experiment on an assembled Mixed-culture electroPioreactor.
---

Running an assembled MEP. To build one, follow the [MEP guide](/MEP/). Source documents: [Calibration](https://github.com/amy-bo/electroPioreactor/blob/main/MixedElectroPioreactor/Calibration.md) and [Operation](https://github.com/amy-bo/electroPioreactor/blob/main/MixedElectroPioreactor/Operation.md).

Every mode uses the same hardware: stirring on PWM 1, waste (product) on PWM 2, media on PWM 3, the CO₂ relay on PWM 4, and electrolysis on LED D at 2.5% from the electroPioreactor job.

## Calibrate each unit

Do these once per unit before the first experiment, and check the electrolysis values again before and after each experiment. A significant change means recalibrating.

1. Run Pioreactor's [self test](https://docs.pioreactor.com/user-guide/pre-flight-hardware-check#step-1-run-a-self-test).
2. [Calibrate stirring](https://docs.pioreactor.com/user-guide/hardware-calibrations#stirring-calibrations).
3. Calibrate the pumps and set the level: done in the guide's **Calibrate the pumps and set the level** step.
4. Make an [OD600 standard curve](https://docs.pioreactor.com/user-guide/calibrate-od600) on the **Protocols** page (device `od90`), from vials of known OD600 measured on a benchtop spectrophotometer plus a media-only blank. Redo it every 6 months, or whenever the optics change.
5. Calibrate the CO₂ flow: done in the guide's **Calibrate CO₂ flow** step.
6. Record the electrolysis voltage and current at 2.5%: done in the guide's **Test electrolysis** step.

## Modes

| Mode | Media in | Waste out | Use it to |
| --- | --- | --- | --- |
| Batch | No | No | Grow a culture on one fill until something runs out. CO₂, H₂ and O₂ are still fed, so strictly it is fed-batch. |
| Chemostat | Fixed rate | Fixed rate | Hold a steady state at a constant dilution rate. |
| Turbidostat | When OD is above target | When OD is above target | Hold a steady state at a target OD. |

## Batch

1. Check the electrodes are at the standard depth, red on the anode and black on the cathode.
2. Fill the vial with 14 ml of nutrient solution ([MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media)) and screw the cap down.
3. Seat the vial in the Pioreactor.
4. In the web interface, create an experiment (for example `ed04_batch_<date>`) and assign the unit to it.
5. Run OD reading until the trace is stable, and save the OD blank for this experiment. OD reading will not start with OD calibrations enabled until a blank exists.
6. Inoculate through one of the gas outlet luers with a syringe. The vial stays seated.
7. Start, in this order: stirring (check the stir bar turns), OD reading, then **electroPioreactor** (electrolysis at 2.5%, sparging 3 seconds every hour). Bubbles should appear within 30 seconds.
8. Watch OD rise. Record the electrolysis voltage at least daily, ideally hourly; the cathode should keep bubbling faster than the anode.
9. At the endpoint, stop **electroPioreactor** and stirring, and sample through a gas outlet luer.
10. Drain the vial, rinse it with distilled water, and clean it.

## Chemostat

Start here only after a successful batch run.

1. Set up as for batch, up to inoculation.
2. Set the waste line to your level (see the guide's **Calibrate the pumps and set the level** step). The waste pump over-runs each dilution by design, so the line's height is the level.
3. In the **dosing automation**, choose chemostat, with an `exchange volume` (for example 0.5 ml) and a `duration` between doses. The dilution rate D (h⁻¹) = (`exchange volume` × 60 / `duration`) / 14.
4. Start stirring, OD reading, **electroPioreactor** and the dosing automation.
5. Over many hours OD settles to a steady state if D is below the culture's maximum growth rate; otherwise the culture washes out.
6. End and strip down as for batch.

## Turbidostat

1. Set up as for chemostat.
2. In the **dosing automation**, choose turbidostat: `target biomass` as expected for your culture (for example 0.5), `biomass signal` left at `auto`, and `exchange volume` 1 to 2 ml.
3. Start stirring, OD reading, **electroPioreactor** and the dosing automation.
4. OD becomes a sawtooth around the target as the unit doses whenever OD crosses it.
5. End and strip down as for batch.

## Records

In the experiment setup: name, mode, unit, dates, media batch, inoculum source and volume. As you go: electrolysis voltage and current at the start, at least daily and at the end, and anything unusual (a loose electrode bolt, a change in bubble rate, anode discolouration, level drift, a knocked unit).
