# Aseptic electroPioreactor AEP0.1.1 Assembly instructions

## Before you start

1. Procure Bill of Materials (TBD - contact us or [Labcrafter](https://labcrafter.co.uk) for AEP0.1.1 BoM)
2. Check your HOB are growing happily heterotrophically.

## Required Tools

1. Computer with SD card reader
2. microSD to SD adapter
3. Philips PH0 Screwdriver
4. 28mm Gas cylinder wrench
5. Vernier Callipers
6. Analytical balance for pump calibration (Pioreactor docs only require 0.1g accuracy)
7. Cryogenic gloves (safe to at least -80°C)
8. Eye/face protection
9. Lab coat
10. Other PPE as directed by your supervisor/department/employer/H&S advisor


## Method

1. Connect empty dovetail platforms in raft, with dovetails always to front and left
   1. SodaStream at rear with expansion gap to right.
   2. 250ml duran product bottle in front of SodaStream
   3. 250ml duran media bottle to right of product bottle (alternate media and waste if multiple AEPs, forming a backbone of media bottle dovetail platforms)
   4. Peristaltic pumps in front of product bottle
   5. Pioreactor in front of Peristaltic pumps
2. Follow relevant Pioreactor hardware setup guide: <https://docs.pioreactor.com/user-guide/20ml-v11-hardware-setup-intro>
3. Follow relevant Pioreactor software setup guide: <https://docs.pioreactor.com/user-guide/software-set-up>
4. Set up electrolysis
   1. ~Insert electrode o-rings into the [Vial Cap](../Components/Vial%20Cap)~
   2. ~Insert electrodes half-way into Vial Cap using a twisting motion to avoid dislodging the o-rings~
   3. ~Push electrodes fully into their [Electrode Top Stop](../Components/ElectrodeTopStop)~
   4. ~Connect red electrode cable to platinum plated anode by tightening M3 bolt through captive nut~
   5. ~Connect black electrode cable to stainless steel cathode by tightening M3 bolt through captive nut~
   6. ~Push down the Electrode Top Stop until the electrodes are at the standard depth <!-- TODO: Agree standard depth and produce protocol to repeatably attain it | assignee: @Bingqiao @Amir @Teo @Martin -->~
   7. Add nutrient solution (or equal ionic strength bicarbonate) to the Vial
   8. Fully screw the Vial Cap onto the Vial <!-- TODO: Agree standard depth and insert protocol to attain it using callipers | assignee: @Bingqiao @Amir @Teo @Martin -->
   9. The electrodes should now protrude into the vial to the standard depth
   10. If necessary, adjust the electrodes to the standard depth
   11. Record the distance from the plane of the top of the Vial Cap to the bottom of each electrode.
   12.  Connect the electrodes to LED channel D (catch upwards)
   13.  With electrolyte solution in the Vial, check electrolysis by setting the LED channel D intensity to 3%, and verifying that roughly twice as many bubbles are forming on the cathode
   14.  Record the voltage across each electrode, and the current through the electrodes, adjust the LED channel D intensity to attain standard values if necessary
   15.  Insert vial into Pioreactor once satisfied all vials have even electrolysis
5. Set up nutrient solution flow
   1. Follow Pioreactor peristaltic pump setup guide: <https://docs.pioreactor.com/user-guide/using-pumps>
   2. Calibrate peristaltic pumps as per <https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration>
   3. Weigh dry empty vial
   4. Fill vial with DI water via the pumps, then weigh vials and adjust tube lengths until vial volume is 15ml
   5. Measure electrodes immersion depths, if necessary adjust to the standard, and record the insertion depth of each electrode
   6. Set up Pioreactor in turbidostat mode: <https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat>
6. Set up carbon dioxide sparging
   1. Unscrew John-Guest push-fit output from the regulator outlet port
   2. Insert 8mm ID 2mm CS o-ring into the regulator outlet port
   3. Screw in the 1.4" male to 1/8" male reducer to the regulator outlet port and tighten with wrench.
   4. Cut a rectangle of gas PTFE tape to wrap around 1/8" male outlet thread 1.5 times.
   5. Wrap gas PTFE tap around 1/8" male outlet thread 1.5 times.
   6. Screw left port of the solenoid valve (with solenoid electronics to rear) into 1/8" male outlet
   7. Cut a rectangle of gas PTFE tape to wrap around needle valve inlet thread (the bare metal thread opposite the screw adjustor) 1.5 times.
   8. Wrap gas PTFE tap around needle valve inlet thread 1.5 times.
   9. Screw needle valve into 1/8" front port of solenoid valve
   10. Close needle valve clockwise
   11. Cut a rectangle of gas PTFE tape to wrap around 1/8" male blanking plug thread 1.5 times.
   12. Wrap gas PTFE tap around 1/8" male blanking plug thread 1.5 times.
   13. Screw male blanking plug thread into right port of solenoid valve and tighten with wrench.
   14.  Close regulator (turn flathead screw fully anti-clockwise)
   15.  Move plastic washer attached to regulator to between regulator and SodaStream adapter
   16.  Sit second plastic washer on top of SodaStream cylinder
   17. **Important:** (while remembering to don all PPE including cryogenic gloves prior to tightening cylinder in one swift, decisive move) [**follow instructions included with SodaStream adapter**](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894)
   18. Place SodaStream in dovetail raft
   19. Remove o-ring from bubble counter and place over needle valve outlet <!-- TODO: Confirm if units still ship with bubble counters, or where o-ring comes from | assignee: @Gerrit -->
   20. Remove compression nut from the top of the needle valve
   21. Attach the 4mm tubing to the needle valve ferrule - dip in hot water to soften if necessary
   22. Reattach the compression nut
   23. Attach the male end of an 0.2 μm vent filter to the female luer lock on the vial CO₂ entry port
   24. Attach the female ends of two 0.2 μm vent filters to the two male luer locks on the vial exhaust ports
   25. Cut the 4mm tubing just long enough to run over the regulator so it keeps the bubble counter vertical and down to the CO₂ entry filter
   26. Measure the 4mm tubing cut length and ensure all other 4mm tubing is cut to the same length
   27. Insert a 1/8" (or 5/32" if 1/8" too loose) barb hose to male luer lock adapter in the free end of the 4mm tubing - dip in hot water to soften if necessary
   28. Connect the luer lock to the CO₂ entry filter
7. Calibrate CO₂ flow
    1. Set regulator to 1 bar
    2. Adjust needle valve to give target flow rate
    3. <!-- TODO: Insert software setup for sparging and instructions on ad hoc sparge software command | assignee: @Gerrit -->
    4. Temporarily close one of two outlet gas vents with luer plug
    5. Run 1/16" tubing from outlet of open gas vent port to bath until water CO2 concentration is assumed (or if possible measured) to have equilibrated
    6. Record time taken to fill measuring cylinder with CO₂ over water
    7. Determine the actual flow rate
    8.  Adjust needle valve and repeat process until target flow rate is achieved
8. Sterilise
    1. ***(PI's to determine process in accordance with departmental requirements)***
