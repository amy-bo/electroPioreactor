# MEP Calibration (Edinburgh MSc)

Six things to set up per unit before any experiment: stirring (PWM↔RPM), peristaltic pumps, OD600 (cell-density curve vs photodiode signal), vial level, CO₂ flow rate, and electrolysis (Voltage across electrodes and Pioreactor Controlled Current through electrodes at 2.5 % LED D). Run on ed04 and ed05 in turn.

Pre-requisite: both units assembled per [Assembly](Assembly-EdMSc26.md), and reachable on the network.

## 0. Self test

Follow [Pioreactor’s self test guide](https://docs.pioreactor.com/user-guide/pre-flight-hardware-check#step-1-run-a-self-test) to ensure everything is working as anticipated.

## 1. Stirring

Follow [Pioreactor’s really simple stirring calibration procedure](https://docs.pioreactor.com/user-guide/hardware-calibrations#stirring-calibrations).

## 2. Peristaltic pumps

Follow [Pioreactor's pump calibration guide](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration) on the Protocols page. For each pump (media on PWM 3, waste on PWM 2):

1. When prompted, enter the target volumes to calibrate around (comma-separated, in mL).
2. For each prompted dispense: catch the output in a tared weighing boat on the analytical balance, then enter the measured volume back into the UI (1 mL water ≈ 1 g at room temp).
3. Repeat across the prompted set.
4. Save the calibration. The UI will refuse to dose until both pumps are calibrated.

Record on the unit's calibration sheet: date, balance ID, who ran the calibration, ml/s at 100 % duty for each pump.

## 3. OD calibration

Follow [Pioreactor's "Standard curves for OD600 readings"](https://docs.pioreactor.com/user-guide/calibrate-od600). This sets the relationship between raw photodiode signal and cell density for *this unit*, so OD traces from ed04 and ed05 can be compared meaningfully. It lives on the **Protocols** page (Device = `od90` for the standard 90° channel).

You'll need a series of vials with **known OD600 values** (measured against a benchtop spectrophotometer) plus a media-only blank. The UI walks you through naming the calibration, recording each standard, and fits a curve from the live chart. See [§ Running the calibration](https://docs.pioreactor.com/user-guide/calibrate-od600#running-the-calibration) for the step-by-step.

**Per unit; redo every 6 months or whenever the optical setup changes.** The per-experiment **OD blank** done at experiment start (see [Operation § Batch step 4](Operation.md#1-batch-experiment)) is a separate, additional baseline correction.

Record on the calibration sheet: date, who ran it, spec model used for reference, OD600 of each standard.

## 4. Level

1. Dry and weigh your vial
2. Add water to your media vessel
3. Add water to your vial to the level that you want to operate at (say 14ml)
4. Weigh your vial to confirm the volume of water in it
5. Adjust your product/waste line so that it is only just submerged at the desired water level
6. Run the media and product/waste pumps
7. Go to step 4 and repeat until you have the desired volume of water after running the pumps

## 5. CO₂ flow rate

The FZone regulator has a fixed, non-adjustable outlet pressure. The only variable you control on the gas side is the needle-valve opening.

1. Confirm the SodaStream is open (the valve directly on top of it is fully down)
2. Run a 1/16" tubing line from one of the vial's exhaust luer locks to a measuring cylinder inverted in a water bath. Plug the other exhaust luer with a luer plug or tie a knot in its line.
3. Sparge CO2 into the water bath until it is saturated with CO2 (you could monitor for no further pH drop to determine saturation.)
4. From the web UI's relay activity tab, open the solenoid (relay on) for a fixed time.
5. Record the volume of CO₂ collected.
6. Compute flow rate (ml CO₂ per second of solenoid-open).
7. Adjust the needle valve and repeat until you hit your target.
8. Record needle-valve setting (turns from fully closed) on the unit's calibration sheet.

If you cannot get to the target flow within sensible needle-valve travel, the problem is one of: (a) needle-valve creep, (b) a kinked line, (c) a leak at one of the Loctite-577 joints. If you suspect (c) try pipetting washing-up liquid in water at the joints and watching for bubbles.

## 6. Electrolysis (V and I at 2.5 % LED D)

1. With the bicarbonate-filled vial seated in the Pioreactor, set LED channel D to **2.5 %** in the web UI.
2. Within 30 s you should see bubbles on both electrodes. The cathode (stainless steel, black lead) should bubble at roughly twice the rate of the anode (Pt-plated Ti, red lead). This is the H₂:O₂ molar 2:1 ratio you would expect.
3. Measure voltage across the electrodes with a multimeter on the DC volts range, probes on the two ring-crimp terminals. Record V on the calibration sheet.
4. Measure current through the electrodes by breaking one electrode lead, putting the multimeter inline on the DC current range (mA), and reconnecting. Record I on the calibration sheet.
5. Set LED D back to 0 % at the end of the check.

Once steps 1–6 are signed off for both ed04 and ed05, the units are ready to run [Operation.md](Operation.md) for real.  However it is recommended that you return and validate that values haven’t changed before and after each experiment.  If you notice significant change you will need to recalibrate.
