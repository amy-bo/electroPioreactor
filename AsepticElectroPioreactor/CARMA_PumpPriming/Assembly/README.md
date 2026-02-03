# Aseptic electroPioreactor AEP0.1.1 Assembly instructions

## Before you start

1. Procure Bill of Materials (TBD - contact us or [Labcrafter](https://labcrafter.co.uk) for AEP0.1.1 BoM)
2. Check your HOB are growing happily heterotrophically.

## Required Tools

1. Computer with SD card reader
2. microSD to SD adapter
3. Phillips PH0 Screwdriver
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
   2. 250ml duran product bottle in front and to the left of the SodaStream.
   3. 250ml duran media bottle in front and to the right of the SodaStream. (alternate media and waste if multiple AEPs, forming a backbone of media bottle dovetail platforms)
   4. Peristaltic pumps in front of product bottle
   5. Pioreactor in front of Peristaltic pumps
   6. The setup should look like this:
<img width="555" height="998" alt="image" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />

2. Follow relevant Pioreactor hardware setup guide: <https://docs.pioreactor.com/user-guide/20ml-v11-hardware-setup-intro>
3. Follow relevant Pioreactor software setup guide: <https://docs.pioreactor.com/user-guide/software-set-up>
4. Set up electrolysis (NOTE: ~struck through~ lines will already have been completed if you received a kit from Labcrafter)
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
   2. Follow the Pioreactor guide to attaching a 12V power supply: <https://docs.pioreactor.com/user-guide/external-power>
   3. Calibrate peristaltic pumps as per <https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration>
   4. Weigh dry empty vial
   5. Fill vial with DI water via the pumps, then weigh vials and adjust tube lengths until vial volume is 15ml
   6. Measure electrodes immersion depths, if necessary adjust to the standard, and record the insertion depth of each electrode
   7. Set up Pioreactor in turbidostat mode: <https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat>
6. Set up carbon dioxide sparging
   1. Unscrew John-Guest push-fit output from the regulator outlet port
<img width="1330" height="1767" alt="image" src="https://github.com/user-attachments/assets/3cbc619c-be7c-4abb-87d3-048d8350dcfc" />

   2. Insert 8mm ID 2mm CS o-ring into the regulator outlet port
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/3316cd49-21c7-4fb3-a931-dd5c0798a27b" />

   3. Screw in the 1/4" male to 1/8" male reducer to the regulator outlet port and tighten with wrench.
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/800812cb-2ccb-4a8f-8198-f8e381757552" />

   4. Cut a rectangle of gas PTFE tape to wrap around 1/8" male outlet thread 1.5 times.
   5. Wrap gas PTFE tape around 1/8" male outlet thread 1.5 times.
   6. Screw left port of the solenoid valve (with solenoid electronics to rear) into 1/8" male outlet. Ensure solinoid manual overide is closed (horizontal line pointing at 0 on the front on the solinoid).
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/ec433749-5866-476b-a965-ec070b80083e" />

   7. Cut a rectangle of gas PTFE tape to wrap around needle valve inlet thread (the bare metal thread opposite the screw adjustor) 1.5 times.
   8. Wrap gas PTFE tape around needle valve inlet thread 1.5 times.
   9. Screw needle valve into 1/8" front port of solenoid valve
   10. Close needle valve clockwise
   11. Cut a rectangle of gas PTFE tape to wrap around 1/8" male blanking plug thread 1.5 times.
   12. Wrap gas PTFE tape around 1/8" male blanking plug thread 1.5 times.
   13. Screw male blanking plug thread into right port of solenoid valve and tighten with wrench.
   14.  Close regulator (turn flathead screw fully anti-clockwise)
   15.  Move plastic washer attached to regulator to between regulator and SodaStream adapter
   16.  Sit second plastic washer on top of SodaStream cylinder
   17. **Important:** (while remembering to don all PPE including cryogenic gloves prior to tightening cylinder in one swift, decisive move) [**follow instructions included with SodaStream adapter**](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894)
   18. Place SodaStream in dovetail raft
   19. Remove compression nut from the top of the needle valve
   20. Attach the 4mm tubing to the needle valve ferrule - dip in hot water to soften if necessary
   21. Reattach the compression nut
   22. Attach the male end of an 0.2 μm vent filter to the female luer lock on the vial CO₂ entry port
   23. Attach the female ends of two 0.2 μm vent filters to the two male luer locks on the vial exhaust ports
   24. Cut the 4mm tubing just long enough to run over the regulator and down to the CO₂ entry filter
   25. Measure the 4mm tubing cut length and ensure all other 4mm tubing is cut to the same length
   26. Insert a 1/8" (or 5/32" if 1/8" too loose) barb hose to male luer lock adapter in the free end of the 4mm tubing - dip in hot water to soften if necessary
   27. Connect the luer lock to the CO₂ entry filter
   28. Connect the solenoid connector to PWM channel 4 on the Pioreactor.
8. Set up software for sparging
   1. [Install](https://docs.pioreactor.com/user-guide/using-community-plugins#installing-plugins) the `pioreactor-relay-plugin` plugin.
   2. In your Pioreactor configuration, make sure that PWM channel 4 is set to `relay`:
   ```
   [PWM]
   # map the PWM channels to externals.
   # hardware PWM are available on channels 2 & 4.
   1=stirring
   2=media
   3=waste
   4=relay
   5=heating
   ```
   3. Test that it works by manually turning on the relay in the **Activities** tab of the *Manage* screen of the Pioreactor UI. You should hear the solenoid turn on and CO2 rushing into the Pioreactor vial. You can adjust the amount of CO2 sparged using the needle valve (for consistency maintain regulator pressure at 1 bar).

      <img width="877" height="167" alt="image" src="https://github.com/user-attachments/assets/71183531-ccc0-4fb2-b36e-4153a897ce3b" />

   4. Create a new [experiment profile](https://docs.pioreactor.com/user-guide/experiment-profiles) and copy and paste the following into the profile:
   ```yaml
   experiment_profile_name: CO2 sparging every hour
   
   metadata:
     author: Gerrit Niezen
     description: Turns on the relay for 10 seconds every hour
   
   common:
     jobs:
       relay:
         actions:
           - type: repeat
             hours_elapsed: 1.0
             repeat_every_hours: 1.0
             actions:
               - type: log
                 hours_elapsed: 0.0  # relative to the repeat loop, 1h
                 options:
                   message: "Sparging CO2 for 10 seconds"
                   level: info
               - type: start
                 hours_elapsed: 0.0
                 options:
                   start_on: True
               - type: stop
                 hours_elapsed: 0.00278
   ```
   When the experiment profile is running it should sparge CO2 for 10 seconds every hour.
9. Calibrate CO₂ flow
    1. Set regulator to 1 bar
    2. Adjust needle valve to give target flow rate
    3. To start sparging, turn on the relay in the Pioreactor UI
    4. Temporarily close one of two outlet gas vents with luer plug
    5. Run 1/16" tubing from outlet of open gas vent port to bath until water CO2 concentration is assumed (or if possible measured) to have equilibrated
    6. Record time taken to fill measuring cylinder with CO₂ over water
    7. Determine the actual flow rate
    8.  Adjust needle valve and repeat process until target flow rate is achieved
10. Sterilise
    1. <!-- TODO: PI's to approve process in accordance with departmental requirements | assignee: @Amir @Teo @Bingqiao @Chris @Sonja -->
