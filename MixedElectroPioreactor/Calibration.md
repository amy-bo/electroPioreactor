# MEP Calibration (Edinburgh MSc)

Three things to calibrate per unit before any experiment: peristaltic pumps, CO₂ flow rate, and electrolysis (V across electrodes and I through electrodes at 2.5 % LED D). Run on ed04 and ed05 in turn.

Pre-requisite: both units assembled per [Assembly](Assembly-EdMSc26.md), bicarbonate-filled, and reachable on the network.

## 1. Peristaltic pumps

Follow [Pioreactor's pump calibration guide](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration). For each pump (media on PWM 3, waste on PWM 2):

1. Place a centrifuge tube on the analytical balance, tare to zero.
2. Run the pump for the calibration duration the UI requests.
3. Weigh the delivered fluid. Repeat across the requested set of duty cycles.
4. Save the calibration. The UI will refuse to dose until both pumps are calibrated.

Record on the unit's calibration sheet: date, balance ID, who ran the calibration, ml/s at 100 % duty for each pump.

## 2. CO₂ flow rate (needle valve only)

The FZone regulator has a fixed, non-adjustable outlet pressure. The only variable you control on the gas side is the needle-valve opening. Your target flow rate is the value Martin recorded during [PreTransport](PreTransportCheck-EdMSc26.md#fzone-leak-check), which matches AEP0.1.1's ODL setup for comparability.

1. Confirm the SodaStream is open (Martin will have done this on arrival).
2. Run a 1/16" tubing line from one of the vial's exhaust luer locks to a measuring cylinder inverted in a water bath. Plug the other exhaust luer with a luer plug.
3. From the web UI's relay activity tab, open the solenoid (relay on) for a fixed observation window.
4. Time the volume of CO₂ collected.
5. Compute flow rate (ml CO₂ per second of solenoid-open).
6. Adjust the needle valve and repeat until you hit Martin's target.
7. Record needle-valve setting (turns from fully closed) on the unit's calibration sheet.

If you cannot get to the target flow within sensible needle-valve travel, the problem is one of: (a) needle-valve creep, (b) a kinked 4 mm or 1/16" line, (c) a leak at one of the Loctite-577 joints. Tell Martin if you suspect (c).

## 3. Electrolysis (V and I at 2.5 % LED D)

Confirm each unit produces electrolysis numbers matching what Martin recorded on the bench during [PreTransport](PreTransportCheck-EdMSc26.md#3-wet-electrolysis).

1. With the bicarbonate-filled vial seated in the Pioreactor, set LED channel D to **2.5 %** in the web UI.
2. Within 30 s you should see bubbles on both electrodes. The cathode (stainless steel, black lead) should bubble at roughly twice the rate of the anode (Pt-plated Ti, red lead). This is the H₂:O₂ molar 2:1 ratio you would expect.
3. Measure **voltage across the electrodes** with a multimeter on the DC volts range, probes on the two ring-crimp terminals. Record V on the calibration sheet.
4. Measure **current through the electrodes** by breaking one electrode lead, putting the multimeter inline on the DC current range (mA), and reconnecting. Record I on the calibration sheet.
5. Compare V and I against Martin's reference values from PreTransport. If they are noticeably off, flag to Martin before going further.
6. Set LED D back to 0 % at the end of the check.

Once steps 1–3 are signed off for both ed04 and ed05, the units are ready to run [Operation.md](Operation.md) for real.
