# MEP Calibration (Edinburgh MSc)

Three things to calibrate per unit before any experiment: peristaltic pumps, CO₂ flow rate, and electrolysis (Voltage across electrodes and Pioreactor Controlled Current through electrodes at 2.5 % LED D). Run on ed04 and ed05 in turn.

Pre-requisite: both units assembled per [Assembly](Assembly-EdMSc26.md), and reachable on the network.

## 0. Self test

Follow [Pioreactor’s self test guide](https://docs.pioreactor.com/user-guide/pre-flight-hardware-check#step-1-run-a-self-test) to ensure everything is working as anticipated.

## 1. Stirring

Follow [Pioreactor’s really simple stirring calibration procedure](https://docs.pioreactor.com/user-guide/pre-flight-hardware-check#step-1-run-a-self-test).

## 2. Peristaltic pumps

Follow [Pioreactor's pump calibration guide](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration). For each pump (media on PWM 3, waste on PWM 2):

1. Place a weighing boat on the analytical balance, tare to zero.
2. Run the pump for the calibration duration the UI requests.
3. Weigh the delivered fluid. Repeat across the requested set of duty cycles.
4. Save the calibration. The UI will refuse to dose until both pumps are calibrated.

Record on the unit's calibration sheet: date, balance ID, who ran the calibration, ml/s at 100 % duty for each pump.

## 3. Level

1. Dry and weigh your vial
2. Add water to your media vessel
3. Add water to your vial to the level that you want to operate at (say 14ml)
5. Weigh your vial to confirm the volume of water in it
6. Adjust your product/waste line so that it is only just submerged at the desired water level
7. Run the media and product/waste pumps
8. Go to step 5 and repeat until you have the desired volume of water after running the pumps

## 4. CO₂ flow rate

The FZone regulator has a fixed, non-adjustable outlet pressure. The only variable you control on the gas side is the needle-valve opening.

1. Confirm the SodaStream is open (the valve directly on top of it is fully down)
2. Run a 1/16" tubing line from one of the vial's exhaust luer locks to a measuring cylinder inverted in a water bath. Plug the other exhaust luer with a luer plug or tie a knot in its line.
3. From the web UI's relay activity tab, open the solenoid (relay on) for a fixed observation window.
4. Record the volume of CO₂ collected.
5. Compute flow rate (ml CO₂ per second of solenoid-open).
6. Adjust the needle valve and repeat until you hit your target.
7. Record needle-valve setting (turns from fully closed) on the unit's calibration sheet.

If you cannot get to the target flow within sensible needle-valve travel, the problem is one of: (a) needle-valve creep, (b) a kinked line, (c) a leak at one of the Loctite-577 joints. If you suspect (c) try pipetting washing-up liquid in water at the joints and watching for bubbles.

## 5. Electrolysis (V and I at 2.5 % LED D)

1. With the bicarbonate-filled vial seated in the Pioreactor, set LED channel D to **2.5 %** in the web UI.
2. Within 30 s you should see bubbles on both electrodes. The cathode (stainless steel, black lead) should bubble at roughly twice the rate of the anode (Pt-plated Ti, red lead). This is the H₂:O₂ molar 2:1 ratio you would expect.
3. Measure **voltage across the electrodes** with a multimeter on the DC volts range, probes on the two ring-crimp terminals. Record V on the calibration sheet.
4. Measure **current through the electrodes** by breaking one electrode lead, putting the multimeter inline on the DC current range (mA), and reconnecting. Record I on the calibration sheet.
6. Set LED D back to 0 % at the end of the check.

Once steps 1–5 are signed off for both ed04 and ed05, the units are ready to run [Operation.md](Operation.md) for real.  However it is recommended that you return and validate that values haven’t changed before and after each experiment.  If you notice significant change you will need to recalibrate.
