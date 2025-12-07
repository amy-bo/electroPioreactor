# Aseptic electroPioreactor AEP0.1.1 Assembly instructions

## Before you start

1. Procure Bill of Materials (TBD - contact us or [Labcrafter](https://labcrafter.co.uk) for AEP0.1 BoM)
2. Check your HOB are growing happily heterotrophically.

## Required Tools

1. Computer with SD card reader
2. microSD to SD adapter
3. Philips PH0 Screwdriver
4. 28mm Gas cylinder wrench
5. Cryogenic gloves (safe to at least -80°C)
6. Eye/face protection
7. Lab coat
8. Other PPE as directed by your supervisor/department/employer/H&S advisor
9. Analytical balance for pump calibration (Pioreactor docs only require 0.1g accuracy)

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
   3. Push electrodes fully into their [Electrode Top Stop](../Components/ElectrodeTopStop)
   4. Push down the Electrode Top Stop until it is flush with the top of the Vial Cap
   5. Add nutrient solution (or equal ionic strength phosphate/sulfate) to the Vial
   6. Fully screw the Vial Cap onto the Vial
   7. The electrodes should now protrude into the vial to the standard depth
   8.  If necessary, adjust the electrodes to the standard depth
   9.  Record the distance from the plane of the top of the Vial Cap to the bottom of each electrode.
<<<<<<< HEAD
   1.  Connect the platinised titanium electrode to the positive terminal of channel D on the Pioreactor with the red crocodile clip
   2.  Connect the stainless steel electrode to the negative terminal of channel D with the black crocodile clip
   3.  With electrolyte solution in the Vial, check electrolysis by setting the LED channel D intensity to 10%, and verifying that roughly twice as many bubbles are forming on the cathode
=======
   1.  Connect the platinised titanium anode to the positive terminal of channel D on the Pioreactor with the red crocodile clip
   2.  Connect the stainless steel cathode to the negative terminal of channel D with the black crocodile clip
   3.  With electrolyte solution in the Vial, check electrolysis by setting the LED channel D intensity to 3%, and verifying that roughly twice as many bubbles are forming on the cathode
>>>>>>> eeeb4d6 (initial commit)
   1.  Record the voltage across each electrode, and the current through the electrodes, adjust the LED channel D intensity to attain standard values if necessary
   2.  Insert vial into Pioreactor once satisfied all vials have even electrolysis
1. Set up nutrient solution flow
   1. Follow Pioreactor peristaltic pump setup guide: <https://docs.pioreactor.com/user-guide/using-pumps>
   2. Calibrate peristaltic pumps as per <https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration>
   3. Weigh dry empty vial
   4. Fill vial with DI water via the pumps, then weigh vials and adjust tube lengths until vial volume is 15ml
   5. Measure electrodes immersion depths, if necessary adjust to the standard, and record the insertion depth of each electrode
   6. Set up Pioreactor in turbidostat mode: <https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat>
2. Set up carbon dioxide sparging
   1. Unscrew John-Guest push-fit output from the regulator outlet port
   2. Insert 8mm ID 2mm CS o-ring into the regulator outlet port
   3. Screw in the 1.4" male to 1/8" female reducer to the regulator outlet port
   4. Cut a rectangle of gas PTFE tape to wrap around needle valve inlet thread (the bare metal thread opposite the screw adjustor) 1.5 times.
   5. Wrap gas PTFE tap around needle valve inlet thread 1.5 times.
   6. Screw needle valve into 1/8" female reducer
   7. Close needle valve clockwise
   8. Close regulator (turn flathead screw fully anti-clockwise)
   9. Move plastic washer attached to regulator to between regulator and SodaStream adapter
   10. Sit second plastic washer on top of SodaStream cylinder
   11. **Important:** (while remembering to don all PPE including cryogenic gloves prior to tightening cylinder in one swift, decisive move) **follow instructions included with SodaStream adapter**
   12. Place SodaStream in dovetail raft
   13. Remove o-ring from bubble counter and place over needle valve outlet
   14. Screw bubble counter onto needle valve
   15. Unscrew metal cap from transparent bubble counter tube
   16. Add 2.5 ml (or 2.25 with old type [rounded compression nut, supplied with clear o-ring] bubble counter) of deionised water to the bubble counter
   17. Replace metal cap on transparent buble counter tube
   18. Remove compression nut from the top of the bubble counter
   19. Attach the 4mm tubing to the top of the bubble counter - dip in hot water to soften if necessary
   20. Reattach the compression nut
   21. Attach the male end of an 0.2 μm vent filter to the female luer lock on the vial CO₂ entry port
   22. Attach the female ends of two 0.2 μm vent filters to the two male luer locks on the vial exhaust ports
   23. Cut the 4mm tubing just long enough to run over the regulator so it keeps the bubble counter vertical and down to the CO₂ entry filter
   24. Measure the 4mm tubing cut length and ensure all other 4mm tubing is cut to the same length
   25. Insert a 1/8" (or 5/32" if 1/8" too loose) barb hose to male luer lock adapter in the free end of the 4mm tubing - dip in hot water to soften if necessary
   26. Connect the luer lock to the CO₂ entry filter
3. Calibrate CO₂ flow
    1. Set regulator to 1 bar
    2. Adjust needle valve to give say 30 bubbles per 10 seconds
    3. Wait for system to equilibrate
    4. Repeat from step 1 as needed
    5. Temporarily pinch one of the two gas vent ports closed
    6. Run 1/16" tubing from outlet of open gas vent port to bath until water CO2 concentration is assumed (or if possible measured) to have equilibrated
    7. Record time taken to fill measuring cylinder with CO₂ over water
    8. Determine the actual flow rate
    9. Adjust target bubble count and repeat process until target flow rate is achieved
4. Sterilise
    1. ***(PI's to determine process in accordance with departmental requirements)***
