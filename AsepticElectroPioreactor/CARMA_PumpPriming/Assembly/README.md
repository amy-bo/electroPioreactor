# Aseptic electroPioreactor AEP0.2 Assembly instructions

> Parts list: [BoM.md](BoM.md). AEP0.1.1 instructions are archived in [AEP0.1.1_Assembly.md](AEP0.1.1_Assembly.md).

## What changed from AEP0.1.1

| Area | AEP0.1.1 | AEP0.2 |
| --- | --- | --- |
| Vessel | Pioreactor 20 ml v1.1, ~15 ml working volume | Pioreactor 40 ml v1.5 + XR upgrade kit, ~30 ml working volume |
| Computer | RPi Zero 2W / RPi 4 4GB, micro-USB or USB-C supply | RPi 5 1GB, 27 W USB-C supply |
| Vial cap | Separate cap + [ElectrodeTopStop](../../../Components/ElectrodeTopStop), cap o-ring + 2 electrode o-rings | One-piece [Vial Cap and electrode holder](../../../Components/Vial%20Cap), single silicone septum |
| Anode | Platinised titanium rod, 100 mm | MMO (IrO₂-Ta₂O₅) tube, 100 mm, CO₂ delivered through its open base |
| Electrode fixing | M3 bolt through captive nut | Ring terminal + thumb screw, M3 nut and spring washer |
| Ports | Flexelene 135C tubing | Stainless steel needles |
| Gas sealing | PTFE tape on every threaded joint | O-rings where possible, Loctite 577 anaerobic thread sealant elsewhere |
| CO₂ inlet | Regulator tightened onto the cylinder against escaping gas | KegLand KL15578 pin-adjustment adapter: tighten first, then open the pin |
| Sparging control | `pioreactor-relay-plugin` + experiment profile YAML | [electroPioreactor plugin](../../../AEP-Plugin) (electrolysis, sparging and OD pausing in one job) |
| Dropped | Bubble counter, pinch slider inoculation port, jubilee clips | Inoculation is now by syringe through the septum |

## Before you start

1. Procure the [Bill of Materials](BoM.md) (contact us or [LabCrafter](https://labcrafter.co.uk) for the AEP0.2 BoM or procure directly from LabCrafter and add at least one [SodaStream blue screw in cylinder](https://sodastream.co.uk/products/refill) and two [250ml GL45 "Duran" Flasks](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate))
2. Check your HOB are growing happily heterotrophically.

## Required Tools

1. Computer with microSD card reader (or SD card reader and microSD to SD adapter)
2. Phillips PH0 Screwdriver
3. 28mm Gas cylinder wrench
4. Vernier Callipers
5. Analytical balance for pump calibration (Pioreactor docs only require 0.1g accuracy)
6. Cryogenic gloves (safe to at least -80°C)
7. Eye/face protection
8. Lab coat
9. Other PPE as directed by your supervisor/department/employer/H&S advisor

## Recommended Tools

1. Multitool and/or needle nose pliers (for general assembly and tubing adjustment)
2. Multimeter (for checking electrolysis)
3. Banded oil filter wrench (optional - if you struggle with CO2 canister tightening)

## Method

1. Connect empty dovetail platforms in raft, with dovetails always to front and left
   1. SodaStream at rear with expansion gap to right.
   2. 250ml GL45 "Duran" product bottle in front and to the left of the SodaStream.
   3. 250ml GL45 "Duran" media bottle in front and to the right of the SodaStream. (alternate media and product if multiple AEPs, forming a backbone of media bottle dovetail platforms)
   4. Peristaltic pumps centred in front of product and media bottles
   5. Pioreactor in front of Peristaltic pumps
   6. The setup should look like this:
<img width="555" height="998" alt="image" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />

   7. The pumping dovetail platform has a cutout for the SD card. Check it clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->

2. Follow the Pioreactor 40 ml v1.5 hardware setup guide: <https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro>
   1. [Assembling the Raspberry Pi and the HAT](https://docs.pioreactor.com/user-guide/40ml-v15-rpi-hat-assembly) — use a Raspberry Pi 5 1GB with the 27 W USB-C supply.
   2. [Wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly)
   3. [Attaching the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together)
   4. **Do not fit the v1.5 optics.** AEP0.2 is XR from the start, and the XR upgrade would only have you strip them straight back out. Keep the v1.5 optics parts in the box for the next step: the XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire out of the v1.5 kit, and the XR kit supplies the remaining eye-spys, its own top vial holder and the O-ring. If instead you are upgrading a Pioreactor that is already built, work through [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those same parts.
   5. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly) (45° and 135° scattering in addition to 90°) — this is standard on AEP0.2 and gives the lower OD detection limit for earlier indication of growth.
   6. [Fit the Precision Temperature Upgrade Kit](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit) — the MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. It seats in the SPEC position and chains off the nearest eye-spy over STEMMA-QT.
   7. The solenoid needs more power than the Pi alone can supply: follow <https://docs.pioreactor.com/user-guide/external-power>. Four or more Pioreactors on one bench can be powered from a single multi-port charger rather than one supply each — see <https://docs.pioreactor.com/user-guide/powering-cluster>.
3. Follow the Pioreactor software setup guide: <https://docs.pioreactor.com/user-guide/software-set-up>
   1. The XR kit needs Pioreactor release 26.1.30 or later and the electroPioreactor plugin needs 26.5.0 or later, so treat **26.5.0 as the minimum** for an AEP0.2 and run `pio update` before going further.
   2. In the web UI open **Inventory** and set this unit's model to the XR variant. Until you do, OD readings are interpreted against the wrong channel map.
   3. Add the XR photodiode channel values to `config.ini`, as listed at the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly).
   4. If the Precision Temperature Upgrade Kit is fitted, open **Plugins** in the Pioreactor UI and install `pioreactor-precision-temperature-plugin`. The equivalent from a shell on the unit is:

      ```bash
      pio plugins install pioreactor-precision-temperature-plugin
      ```
4. Install the [electroPioreactor plugin](../../../AEP-Plugin), following [AEP-Plugin/README.md](../../../AEP-Plugin/README.md)

   This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile: a single background job drives electrolysis on LED D, sparges CO₂ on the PWM 4 relay, pauses electrolysis for the duration of each sparge, and pauses OD reading for the sparge plus a settle window.

   Install it before going any further. The electrolysis check in step 5 runs through this job, so that its 10% power clamp is protecting the electrodes the first time they are ever driven.
5. Set up electrolysis (NOTE: ~struck through~ lines will already have been completed if you received a kit from LabCrafter)
   1. ~Seat the silicone septum in the [Vial Cap](../../../Components/Vial%20Cap)~ — one sheet seals the vial mouth, each electrode and every port, and self-heals sampling-needle tracks. There are no electrode o-rings and no cap o-ring in AEP0.2.
   2. ~Push each electrode through the septum and up into its journal bore in the one-piece cap and electrode holder~ — the MMO anode is the tube, the stainless steel rod is the cathode.
   3. ~Crimp a ring terminal onto each electrode cable~
   4. ~Fix the red cable's ring terminal to the MMO anode with an M3 nut and spring washer, tightened by thumb screw~
   5. ~Fix the black cable's ring terminal to the stainless steel cathode the same way~
   6. ~Set the electrode insertion depth. The holder is parametric: the column height already encodes the electrode length and the protrusion into the vial, so the electrodes seat at the standard depth without adjustment.~ <!-- TODO: record the AEP0.2 standard depth here once the first build is measured | assignee: @Bingqiao @Amir @Teo @Martin -->
   7. Add nutrient solution (or equal ionic strength bicarbonate) to the Vial
   8. Fully screw the Vial Cap onto the Vial, compressing the septum evenly
   9. The electrodes should now protrude into the vial to the standard depth
   10. Record the distance from the plane of the top of the Vial Cap to the bottom of each electrode.
   11. Connect the electrodes to LED channel D (catch upwards)
   12. With electrolyte solution in the Vial, start **electroPioreactor** from the **Activities** tab of the *Manage* screen and verify that roughly twice as many bubbles form on the cathode as on the anode. Drive the electrodes from this job rather than setting LED channel D by hand: the job clamps electrolysis power to 10% at runtime, and nothing does so if you drive the channel directly. The CO₂ side of the job does nothing yet, since the solenoid is not connected until step 8 — set a long sparge interval so the relay is not actuating into thin air.
   13. Record the voltage across each electrode and the current through them, adjusting **electrolysis power** in the job's **Settings** panel to reach the standard values if necessary
   14. Insert vial into Pioreactor once satisfied all vials have even electrolysis
6. Set up nutrient solution flow
   1. Follow Pioreactor peristaltic pump setup guide: <https://docs.pioreactor.com/user-guide/using-pumps>
   2. Follow the Pioreactor guide to attaching a 12V power supply: <https://docs.pioreactor.com/user-guide/external-power>
   3. Calibrate peristaltic pumps as per <https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration>
   4. Weigh dry empty vial
   5. Fill vial with DI water via the pumps, then weigh vials and adjust tube lengths until vial volume is 30ml (the 40 ml vessel's working volume — 15 ml was the AEP0.1.1 figure)
   6. Measure electrodes immersion depths, if necessary adjust to the standard, and record the insertion depth of each electrode
   7. Set up Pioreactor in turbidostat mode: <https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat>
7. Ports

   The AEP0.2 cap carries eight ports, all stainless steel needles rather than the Flexelene 135C tubing used in AEP0.1:

   1. Anode and CO₂ In – 6mm
   2. Cathode – 6mm
   3. Media In
   4. Media Out
   5. Gas Out
   6. Gas Out – safety
   7. Inoculation (large) – syringe through the septum, no dedicated tube and no pinch slider
   8. Spare port (sealed)

8. Set up carbon dioxide sparging
   1. Unscrew John-Guest push-fit output from the regulator outlet port
<img width="1330" height="1767" alt="image" src="https://github.com/user-attachments/assets/3cbc619c-be7c-4abb-87d3-048d8350dcfc" />

   2. Insert 8mm ID 2mm CS o-ring into the regulator outlet port
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/3316cd49-21c7-4fb3-a931-dd5c0798a27b" />

   3. Screw in the 1/4" male to 1/8" male reducer to the regulator outlet port and tighten with wrench.
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/800812cb-2ccb-4a8f-8198-f8e381757552" />

   4. Apply Loctite 577 anaerobic thread sealant to the 1/8" male outlet thread. PTFE tape is no longer used anywhere in the gas train: applied correctly it seals, but the process is fiddly and it leaked often enough to be worth replacing. Use an o-ring wherever the joint has a seat for one, and Loctite 577 on every threaded joint that has not.
   5. Screw left port of the solenoid valve (with solenoid electronics to rear) into 1/8" male outlet. Ensure the solenoid manual override is closed (horizontal line pointing at 0 on the front of the solenoid).
<img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/ec433749-5866-476b-a965-ec070b80083e" />

   6. Apply Loctite 577 to the needle valve inlet thread (the bare metal thread opposite the screw adjustor)
   7. Screw needle valve into 1/8" front port of solenoid valve
   8. Close needle valve clockwise
   9. Fit the o-ring blanking plug to the right port of the solenoid valve and tighten with wrench. The plug seals on its o-ring, so it needs no thread sealant.
   10. Close regulator (turn flathead screw fully anti-clockwise)
   11. Fit the KegLand KL15578 pin-adjustment SodaStream adapter to the cylinder with the pin **backed off**, then screw the regulator onto the adapter. Tightening no longer races escaping CO₂ — the joint is made first and gas is admitted afterwards.
   12. **Important:** don all PPE including cryogenic gloves before tightening the cylinder joint, and [follow the instructions included with the SodaStream adapter](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894). Never fit a mismatched adapter to a high-pressure CO₂ joint: retention comes from full thread engagement, and a partial mismatched engagement fails suddenly.
   13. With the joint made and the regulator closed, open the adapter's thumbscrew pin to admit CO₂ to the regulator.
   14. Place SodaStream in dovetail raft
   15. Remove compression nut from the top of the needle valve
   16. Attach the 4mm tubing to the needle valve ferrule - dip in hot water to soften if necessary
   17. Reattach the compression nut
   18. Attach the male end of an 0.2 μm vent filter to the female luer lock on the vial CO₂ entry port
   19. Attach the female ends of two 0.2 μm vent filters to the two male luer locks on the vial exhaust ports
   20. Cut the 4mm tubing just long enough to run over the regulator and down to the CO₂ entry filter
   21. Measure the 4mm tubing cut length and ensure all other 4mm tubing is cut to the same length
   22. Insert a 1/8" hose barb to male luer lock adapter in the free end of the 4mm tubing - dip in hot water to soften if necessary
   23. Connect the luer lock to the CO₂ entry filter
   24. Connect the filter's outlet to the head of the tubular MMO anode with a male-to-male luer lock adapter and the short 1 mm ID / 3 mm OD silicone feed tube. CO₂ enters through the anode and leaves through its open base, so the gas rises past the anode surface and clears oxygen bubbles from it without any separately positioned sparge tube. <!-- TODO: fix the feed tube length and ID once the first build is measured; frit dispersion at the anode base is deferred to AEP0.3 | assignee: @Martin -->
   25. Cap any unused luer lock with a luer lock cap
   26. Connect the solenoid connector to PWM channel 4 on the Pioreactor.
9. Configure sparging and electrolysis

   The plugin was installed at step 4 and has been driving the electrodes since step 5. Now set it up for the full cycle, with the CO₂ train built.
   1. The plugin's installer patches `config.ini` for you. It should end up containing:
   ```ini
   [PWM]
   # map the PWM channels to externals.
   # hardware PWM are available on channels 1 & 3.
   1=stirring
   2=waste
   3=media
   4=relay
   5=heating

   [electropioreactor.config]
   electrolysis_power=2.5              ; LED D intensity (0-10 %, clamped at runtime)
   sparge_duration_seconds=10.0        ; solenoid open time per cycle (s)
   sparge_interval_minutes=60.0        ; cycle frequency (min)
   od_pause_after_sparge_seconds=5.0   ; OD settle window after sparge ends (s)
   ```
   2. Restart **electroPioreactor** from the **Activities** tab of the *Manage* screen with the sparge interval you actually want. You should now hear the solenoid open and CO₂ rush into the vial. All four parameters are editable live from the **Settings** panel.
   3. Electrolysis power stays clamped to 10% at runtime to protect the electrodes.
10. Calibrate CO₂ flow
    1. Set regulator to 1 bar
    2. Adjust needle valve to give target flow rate
    3. Start the **electroPioreactor** job, or turn on the relay in the Pioreactor UI, to sparge
    4. Temporarily close one of two outlet gas vents with luer plug
    5. Run 1/16" tubing from outlet of open gas vent port to bath until water CO2 concentration is assumed (or if possible measured) to have equilibrated
    6. Record time taken to fill measuring cylinder with CO₂ over water
    7. Determine the actual flow rate
    8. Adjust needle valve and repeat process until target flow rate is achieved
11. Sterilise
    1. <!-- TODO: PI's to approve process in accordance with departmental requirements | assignee: @Amir @Teo @Bingqiao @Chris @Sonja -->

## Spares

Carry boxed spares of the fragile and consumable items — at minimum a spare vial and a spare magnetic flea per few units. A vial was dropped and smashed during the AEP0.1 training.
