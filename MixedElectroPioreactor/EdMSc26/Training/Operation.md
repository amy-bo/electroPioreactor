# MEP Operation (Edinburgh MSc)

Three operating modes. Start with **batch**, then move to **chemostat**, then **turbidostat**. All three use the same hardware: stirring on PWM 1, waste on PWM 2, media on PWM 3, CO₂ relay on PWM 4, electrolysis on LED D at 2.5 %.

This doc is read as a **walkthrough** first (the theory of what you're about to do), then executed as a procedure later in the day if time allows. Actual execution requires both units calibrated per [Calibration.md](Calibration.md): pumps calibrated, CO₂ flow at the target Martin recorded during PreTransport, electrolysis V and I matching the PreTransport reference.

## Modes at a glance

| Mode | Media in? | Waste out? | When you would use it |
|------|-----------|------------|------------------------|
| Batch | No | No | Watch a culture grow on a fixed media charge until something runs out (substrate, headspace) |
| Chemostat | Yes, fixed rate | Yes, fixed rate | Hold steady-state with a constant dilution; cells reach a balance between growth and washout |
| Turbidostat | OD-triggered | OD-triggered | Hold steady-state at a target OD by pulsing media + waste when OD exceeds threshold |

## 1. Batch experiment

This is the simplest experiment and the right one to start with. The vial is filled once, the experiment runs, you watch.

1. **Prepare the vial.**
   1. Confirm electrodes at standard depth and connected with correct polarity (red→Pt anode, black→SS cathode).
   2. Fill the vial with 15 ml of MC02 medium.
   3. Screw the vial cap down. Attach the vent filters: one on the CO₂ entry luer, two on the exhaust luers.
2. **Inoculate.** Add inoculum through one of the exhaust luers using a syringe. Re-attach the vent filter.
3. **Seat the vial** in the Pioreactor.
4. **Set up the experiment** in the web UI.
   1. Create a new experiment, name it `ed04_batch_<date>` (or ed05).
   2. Assign ed04 (or ed05) to the experiment.
5. **Start jobs**, in this order:
   1. **Stirring.** Confirm the fan engages and the stir bar is moving in the vial.
   2. **OD reading.** Start; check the OD trace updates.
   3. **Electrolysis.** Set LED D to 2.5 %. Watch for bubbles within 30 s.
   4. **CO₂ sparging.** Apply the experiment profile that opens the relay every hour for 10 s (the [pioreactor-relay-plugin](https://docs.pioreactor.com/user-guide/using-community-plugins#installing-plugins) profile). The electroPioreactor plugin handles pausing electrolysis during each sparge.
6. **Watch.** OD should rise; voltage and current should drift slightly as ionic strength changes; cathode bubbles should remain visibly more numerous than anode bubbles. Record V and I at every sparge cycle.
7. **End.** When OD plateaus or you reach your endpoint, stop electrolysis, stop the sparge profile, stop stirring. Sample the vial through an exhaust luer.
8. **Strip down.** Drain the vial, rinse with distilled water, dry. Disconnect electrodes, coil leads, store.

## 2. Chemostat

A chemostat continuously dilutes the culture at a fixed rate. Cells either grow fast enough to keep up (steady state) or wash out (rate too high). Start here only after you have a successful batch run.

1. Set up exactly as in batch, through inoculation and seating the vial.
2. Configure the **dosing automation** in the Pioreactor UI:
   1. Mode: chemostat
   2. Volume per dose: e.g. 0.5 ml
   3. Interval: chosen to give the dilution rate D (h⁻¹) you want. Working volume is 15 ml, so D = (volume per dose × doses per hour) / 15.
3. Start stirring, OD, electrolysis at 2.5 %, sparge profile, and chemostat dosing.
4. Watch OD over many hours: it will move toward a steady state if D is below the maximum specific growth rate, otherwise wash out.
5. End and strip down as for batch.

## 3. Turbidostat

A turbidostat holds OD at a target by triggering media and waste pulses whenever OD exceeds threshold.

1. Set up as for chemostat, through inoculation and seating.
2. Configure the **dosing automation**:
   1. Mode: turbidostat
   2. OD target: e.g. 0.5 (set in agreement with Martin for the anode/medium/strain combination)
   3. Volume per dose: e.g. 0.5 ml (will be matched on the waste side)
3. Start the standard job set (stirring, OD, electrolysis, sparge profile) and the turbidostat dosing automation.
4. The unit pulses media + waste whenever OD crosses the target. OD trace becomes a sawtooth around the target.
5. End and strip down as for batch.

## Records to hand back to Martin

For each run, give Martin:

- Experiment name, mode, unit, dates
- Media batch, inoculum source, inoculum volume
- Voltage and current at start, every sparge cycle through the run, and at end
- OD trace export (CSV from the UI)
- Any anomalies: loose electrode connection at the Top Stop captive nut, bubble rate change, anode discolouration, vial level drift
- Disposed-of cleanly? Cell biomass to where?
