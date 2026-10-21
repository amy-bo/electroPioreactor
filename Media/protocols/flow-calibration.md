---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "CO₂ flow calibration (per reactor)"
sources:
  - https://patents.google.com/patent/US4691577A/en
  - https://tameson.com/pages/solenoid-valve-timer
  - https://link.springer.com/article/10.1007/s12665-024-11836-3
  - https://www.sigmaaldrich.com/US/en/product/supelco/20433u
  - https://lab-training.com/measurement-gas-volumes-laboratories/
  - https://sciencing.com/measure-gas-using-water-displacement-7912117.html
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, co2, flow-calibration, sparging]
---

# CO₂ flow calibration (per reactor)

## Optimal protocol

### Kit

- An inverted burette or graduated gas-collection tube (1 mL graduations) standing mouth-down in a water trough, or a calibrated soap-film / bubble flow meter.
- A stopwatch (a phone stopwatch is fine).
- The Pioreactor running the reactor under test, with its real CO₂ line, regulator and solenoid.

### Reagents

- Acidified water for the trough and collection tube: tap water with a few drops of acid (vinegar or citric acid solution) added until it tests below pH 4 on indicator paper or a meter. Saturated brine may be used instead.

### Method

Secure the CO₂ cylinder upright and vent CO₂ only in a well-ventilated area: CO₂ is denser than air and can pool in a confined space. Prerequisite: demonstrate CO₂ recovery for the capture liquid and apparatus over the relevant flow/pulse range, or use a suitable calibrated capture method. Acidification alone does not establish recovery.

1. Fill the collection tube with acidified water, cover the mouth, invert it into the trough and uncover it under the surface so it stays full with no trapped air.
2. Connect the CO₂ line so it delivers into the mouth of the collection tube instead of into the reactor vial.
3. With the line outlet held away from the collection tube, clear air from the tubing by venting CO₂ for a few seconds, then close the line and position the outlet under the mouth of the collection tube.
4. Trigger the CO₂ solenoid fully open (via the Pioreactor interface/relay), not a manual regulator or bypass - the calibration measures the solenoid's open-flow rate - and start the stopwatch at the same instant.
5. Let gas collect until the tube holds a comfortably readable volume, then close the solenoid and stop the stopwatch at the same instant. Note the elapsed time.
6. Raise or lower the collection tube until the liquid level inside matches the level in the trough, so the collected gas sits at ambient pressure, then read the collected gas volume off the graduations. Record collection temperature, absolute pressure and wet/dry basis; correct for water vapour where applicable.
7. Repeat steps 3 to 6 at least five times, refilling the tube each time. If the five readings spread by more than ~10 %, check the solenoid seating and repeat.
8. Record collection temperature and absolute pressure, recovery correction, and wet/dry basis in notes. Convert the measured volume to the model’s stated reference conditions before entry (or resolve the conversion with the owner if the tab cannot represent it). Record, for each measurement, the corrected volume of CO₂ (mL) and the time taken (s) in the **CO₂ flow** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; leave Include blank or n. Leave the Computed, Type and value-in-use cells to the spreadsheet. This can enable the model’s flow-calibration gate, but does not validate short-pulse delivery. Keep the new row excluded until steps 9–10 establish the applicable pulse model and any significant intercept is resolved.
9. Required before relying on a short-pulse schedule or setting the solenoid floor: command short pulses (for example 1.0, 0.5, 0.3, 0.25, 0.2 and 0.1 s), collecting 10 pulses of each length and reading the total. The shortest length whose per-pulse volume stays repeatable (within about 10 % across three repeats) and on the line through the longer pulses is the minimum pulse. Record it in the **Min pulse (s)** column of the same CO₂ flow row; include it only after the attached-sparger validation in step 10; the most recent included entry for the reactor becomes the solenoid floor.
10. Required attached-sparger delivery check before relying on the short-pulse schedule: repeat steps 3 to 6 once with the CO₂ line connected through the reactor's own sparger/sinter, the sinter submerged at its working depth in a beaker of acidified water (or in the vial filled to its working volume), collecting the gas that bubbles up from the liquid surface into the inverted collection tube. Compare the flow with the open-line flow. In the reactor the gas also has to overcome the sinter's bubble point and the liquid head (a few kPa), which can slightly lower the delivered flow and the fixed per-pulse volume. This checks attached-sparger steady flow only. Agreement within about 5 % does not validate short-pulse volume. Repeat step 9 with the sparger attached over durations bracketing Summary D14; fit per-pulse delivered volume against commanded duration, recording slope, intercept and uncertainty. Resolve how the workbook represents a significant intercept before relying on flow × duration for short pulses. Set Include to y only after both the attached-sparger pulse validation and intercept representation are resolved and recorded.

## Budget protocol

### Kit

- A graduated measuring cylinder.
- A basin of water.
- A length of tubing.
- A phone stopwatch.

### Reagents

- Acidified water as above (a little vinegar or citric acid in tap water, acidified to below pH 4).

### Method

Secure the CO₂ cylinder upright and vent CO₂ only in a well-ventilated area: CO₂ is denser than air and can pool in a confined space. Prerequisite: demonstrate CO₂ recovery for the capture liquid and apparatus over the relevant flow/pulse range, or use a suitable calibrated capture method. Acidification alone does not establish recovery.

1. Fill the measuring cylinder with acidified water, cover the mouth, invert it into the basin and uncover it under the surface so it stays full with no trapped air.
2. Feed the CO₂ tubing up into the mouth of the cylinder.
3. With the tubing outlet held away from the cylinder, clear air from the line by venting CO₂ for a few seconds, then stop the flow and position the outlet under the mouth of the cylinder.
4. Trigger the CO₂ solenoid fully open (via the Pioreactor interface/relay), not a manual regulator or bypass - the calibration measures the solenoid's open-flow rate - and start the stopwatch at the same instant.
5. Let gas collect until the cylinder holds a comfortably readable volume, then close the solenoid and stop the stopwatch at the same instant. Note the elapsed time.
6. Lift or lower the cylinder until the water level inside matches the basin surface, then read the collected gas volume off the graduations. Record collection temperature, absolute pressure and wet/dry basis; correct for water vapour where applicable.
7. Repeat steps 3 to 6 at least five times, refilling the cylinder each time. If the five readings spread by more than ~10 %, check the solenoid seating and repeat.
8. Record collection temperature and absolute pressure, recovery correction, and wet/dry basis in notes. Convert the measured volume to the model’s stated reference conditions before entry (or resolve the conversion with the owner if the tab cannot represent it). Record, for each measurement, the corrected volume of CO₂ (mL) and the time taken (s) in the **CO₂ flow** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; leave Include blank or n. Leave the Computed, Type and value-in-use cells to the spreadsheet. This can enable the model’s flow-calibration gate, but does not validate short-pulse delivery. Keep the new row excluded until steps 9–10 establish the applicable pulse model and any significant intercept is resolved.
9. Required before relying on a short-pulse schedule or setting the solenoid floor: command short pulses (for example 1.0, 0.5, 0.3, 0.25, 0.2 and 0.1 s), collecting 10 pulses of each length and reading the total. The shortest length whose per-pulse volume stays repeatable (within about 10 % across three repeats) and on the line through the longer pulses is the minimum pulse. Record it in the **Min pulse (s)** column of the same CO₂ flow row; include it only after the attached-sparger validation in step 10; the most recent included entry for the reactor becomes the solenoid floor.
10. Required attached-sparger delivery check before relying on the short-pulse schedule: repeat steps 3 to 6 once with the CO₂ line connected through the reactor's own sparger/sinter, the sinter submerged at its working depth in a beaker of acidified water (or in the vial filled to its working volume), collecting the gas that bubbles up from the liquid surface into the inverted collection tube. Compare the flow with the open-line flow. In the reactor the gas also has to overcome the sinter's bubble point and the liquid head (a few kPa), which can slightly lower the delivered flow and the fixed per-pulse volume. This checks attached-sparger steady flow only. Agreement within about 5 % does not validate short-pulse volume. Repeat step 9 with the sparger attached over durations bracketing Summary D14; fit per-pulse delivered volume against commanded duration, recording slope, intercept and uncertainty. Resolve how the workbook represents a significant intercept before relying on flow × duration for short pulses. Set Include to y only after both the attached-sparger pulse validation and intercept representation are resolved and recorded.

## What the spreadsheet does with it

The Calibrations tab divides entered volume by open time and uses the latest included flow for each reactor. It has no collection-temperature/pressure fields: retain raw volumes and collection conditions in notes and convert to the model’s stated conditions before entry, with owner agreement on the input basis. Applying reactor conditions to an uncorrected collected volume is not a conditions conversion. When a Calibrations-tab steady flow is selected, the model uses that slope with zero intercept. Otherwise it fits V = V₀ + Q_fit·t to the selected reactor’s accepted CO2 flows E/F data (Mass Transfer D401–D408); ed04 currently has a nonzero fitted intercept. Thus step 10 alone measures steady flow, while attached-sparger step 9 measures per-pulse delivery and its intercept. A significant intercept remains an unresolved model-input decision. The latest included Min pulse entry sets the solenoid floor; without one the workbook falls back to its defaults, which are not measured delivery.

## Principle & background

CO₂ reaches the vial from a SodaStream-type cylinder through a regulator and a solenoid that the Pioreactor pulses open for a commanded duration. The model needs the volumetric flow rate delivered while the solenoid is fully open (mL/s). Measuring a collected volume against the time the solenoid was open gives that rate directly, which is the same primary-standard idea behind the soap-film / bubble flow meter, where a known gas volume is timed between calibrated marks to give a volumetric rate (https://patents.google.com/patent/US4691577A/en, https://www.sigmaaldrich.com/US/en/product/supelco/20433u).

Gas volume requires collection temperature and absolute pressure as well as level equalisation. Convert wet gas using its dry pressure (subtract water-vapour pressure when applicable). For a demonstrated recovered volume, V_ref = V_col × (P_dry,col/P_ref) × (T_ref/T_col), with temperatures in kelvin and a consistent dry/wet basis. Record the raw and converted volumes and correction basis; resolve the workbook’s input convention before including the row.

The minimum sparge time - the shortest pulse that still delivers a repeatable volume - is measured separately (step 9); it does not follow from the flow rate. A small solenoid opens and closes within a few to about 10 ms, and those switching times are fixed for a given valve and drive (https://tameson.com/pages/solenoid-valve-timer). When a commanded pulse approaches that mechanical timescale the fixed open/close bolus and timing jitter dominate, so the usable floor sits near 0.2 s and shorter pulses are erratic.

The capture liquid matters. CO₂ is far more soluble in plain water than O₂ or H₂, and it reacts to form bicarbonate, so it does not simply obey Henry's law: below about pH 4.5 dissolved inorganic carbon is overwhelmingly free CO₂ gas, while at pH 8.3 and above it is mostly bicarbonate and is lost from the captured volume (https://link.springer.com/article/10.1007/s12665-024-11836-3). Capturing over plain water therefore under-reads CO₂. Acid suppresses bicarbonate formation but does not eliminate physical CO₂ dissolution. Neither acidification, saturation nor brine alone demonstrates negligible loss; use demonstrated recovery over the measurement range or a suitable calibrated capture method.

## Sources

- Soap-film / bubble flow meter as a primary volumetric gas-flow standard: https://patents.google.com/patent/US4691577A/en and https://www.sigmaaldrich.com/US/en/product/supelco/20433u
- Gas collection by water displacement and the need to equilibrate pressure before reading volume: https://lab-training.com/measurement-gas-volumes-laboratories/ and https://sciencing.com/measure-gas-using-water-displacement-7912117.html
- Solenoid valve open/close timescale (few to about 10 ms) and fixed, repeatable switching times: https://tameson.com/pages/solenoid-valve-timer
- CO₂ speciation vs pH (free CO₂ below about 4.5, bicarbonate above about 8.3), motivating acidified / saturated capture liquid: https://link.springer.com/article/10.1007/s12665-024-11836-3
