# MEP Operation (Edinburgh MSc)

You can run the pioreactor in three main operating modes: **fed-batch**, **chemostat**, and **turbidostat**. The first is strictly *fed-batch* — though no liquid medium is added or removed, the macronutrients (CO₂ from the sparge, H₂ and O₂ from in-culture electrolysis) are continuously fed. For brevity we'll call it **batch** in the rest of this doc. All three modes use the same hardware: stirring on PWM 1, product/waste on PWM 2, media on PWM 3, CO₂ relay on PWM 4, electrolysis on LED D at 2.5 %.

This doc is read as a walkthrough first (the theory of what you're about to do), then executed as a procedure later in the day if time allows. Actual execution requires both units fully set up per [Calibration.md](Calibration.md): stirring, peristaltic pumps, **OD600** (per-unit standard curve, [Calibration § 3](Calibration.md#3-od-calibration)), vial level, CO₂ flow rate, and electrolysis V and I. The per-experiment **OD blank** is a separate step (see § 1 Batch step 4 below) and is not a substitute for the standard curve.

## Modes at a glance

| Mode | Media in? | Product/Waste out? | When you would use it |
|------|-----------|------------|------------------------|
| Batch | No | No | Watch a culture grow on a fixed media charge until something runs out |
| Chemostat | fixed rate | fixed rate | Hold steady-state with a constant dilution; cells reach a balance between growth and washout |
| Turbidostat | OD-triggered | OD-triggered | Hold steady-state at a target Optical Density (OD) by running media + product/waste when OD exceeds threshold |

## 1. Batch experiment

This is the simplest experiment and the best for initial culture growth. The vial is filled once, the experiment runs, you watch.

1. **Prepare the vial.**
   1. Confirm electrodes at standard depth and connected with correct polarity (red→Pt anode, black→SS cathode).
   2. Fill the vial with 14 ml of MC02 medium (the 1 ml of headroom accommodates the electrodes and sparging tube).
   3. Screw the vial cap down. Attach the vent filters: one on the CO₂ entry luer, two on the exhaust luers.
2. **Seat the vial** in the Pioreactor (pre-inoculation, for OD blanking).
3. **Set up the experiment** in the web UI.
   1. Create a new experiment, name it e.g. `ed04_batch_<date>` (or ed05).
   2. Assign ed04 (or ed05) to the experiment.
4. **Read the OD blank.** Run `od_reading` until the trace is stable; save the blank for this experiment. 26.4.x's `od_reading` will refuse to start with OD calibrations or fused estimators enabled if no blank exists for the experiment.
5. **Inoculate.** Add inoculum through one of the exhaust luers using a syringe. (No need to unseat the vial.)
6. **Start jobs**, in this order:
   1. **Stirring.** Confirm the fan engages and the stir bar is moving in the vial.
   2. **OD reading.** Resume/restart; the saved blank is now applied to the trace.
   3. **Electrolysis.** In electroPioreactor Advanced set LED D to 2.5 %. Watch for bubbles within 30 s.
   4. **CO₂ sparging.** Set up electroPioreactor Advanced to open the relay every hour for 3 s. The electroPioreactor plugin handles pausing electrolysis during each sparge.
7. **Watch.** OD should rise; voltage and current should drift slightly as ionic strength changes; cathode bubbles should remain visibly more numerous than anode bubbles. Record voltage regularly.
8. **End.** When OD plateaus or you reach your endpoint, stop electrolysis and the sparge profile (by stopping electroPioreactor), stop stirring. Sample the vial through an exhaust luer.
9. **Strip down.** Drain the vial, rinse with distilled water then sterilise.

## 2. Chemostat

A chemostat continuously dilutes the culture at a fixed rate. Cells either grow fast enough to keep up (steady state) or wash out (rate too high). Start here only after you have a successful batch run.

1. Set up exactly as in batch, through inoculation and seating the vial.
2. Configure the **dosing automation** in the Pioreactor UI:
   1. Mode: chemostat
   2. `exchange volume` (mL): e.g. 0.5
   3. `duration` (minutes): the interval between doses. Combined with `exchange volume`, this sets the dilution rate D (h⁻¹) = (`exchange volume` × 60 / `duration`) / 14, where 14 is the working volume in mL (see `efflux_tube_volume_ml`).
3. Start stirring, OD, electrolysis at 2.5 %, sparge profile, and chemostat dosing.
4. Watch OD over many hours: it will move toward a steady state if D is below the maximum specific growth rate, otherwise wash out.
5. End and strip down as for batch.

**Vial level:** Position the waste tube at your desired vial level before starting. The waste pump over-runs each dilution cycle by design; tube height is the level setpoint, not the media/waste volume ratio. See [forum #801](https://forum.pioreactor.com/t/dosing-volumes-how-to-keep-the-volume-added-and-the-volume-removed-to-be-equal/801) for an explanation.

## 3. Turbidostat

A turbidostat holds OD at a target by triggering media and product/waste pulses whenever OD exceeds threshold.

1. Set up as for chemostat, through inoculation and seating.
2. Configure the **dosing automation**:
   1. Mode: turbidostat
   2. `target biomass`: e.g. 0.5 (set as anticipated for the electrolysis/medium/strain combination)
   3. `biomass signal`: leave at `auto` unless you have reason to pick `normalized_od`, `od_fused`, or `od` explicitly.
   4. `exchange volume` (mL): 1.0–2.0 (Pioreactor's recommendation for fast-growing cultures); waste side is matched by the same dosing event.
3. Start the standard job set (stirring, OD, electrolysis, sparge profile) and the turbidostat dosing automation.
4. The unit pulses media + product/waste whenever OD crosses the target. OD trace becomes a sawtooth around the target.
5. End and strip down as for batch.

## Records

For each run, record in the Pioreactor software:

In the experimental setup dialogue:
- Experiment name, mode, unit, dates
- Media batch, inoculum source, inoculum volume
As you proceed:
- Voltage and current at start, voltage at least daily, ideally hourly, and at end
- Any anomalies: loose electrode connection at the Top Stop captive nut, bubble rate change, anode discolouration, vial level drift, Pioreactor knocked, etc.

