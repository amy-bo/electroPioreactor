---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "CO2 flow calibration (per reactor)"
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

# CO2 flow calibration (per reactor)

## Optimal protocol

### Kit

- The Pioreactor running the reactor under test, with the real CO2 line, regulator and solenoid it will use in service.
- An inverted burette or graduated gas-collection tube (1 mL graduations) standing mouth-down in a water trough, or a calibrated soap-film / bubble flow meter.
- A stopwatch (a phone stopwatch is fine).

### Reagents

- Acidified water for the trough and collection tube: tap water with a few drops of acid (vinegar or citric acid solution) added until it tastes or tests clearly sour (pH below 4). Saturated brine may be used instead.

### Method

1. Fill the collection tube with acidified water, cover the mouth, invert it into the trough and uncover it under the surface so it stays full with no trapped air.
2. Connect the CO2 line so it delivers into the mouth of the collection tube instead of into the reactor vial.
3. Vent CO2 through the line for a few seconds to clear air from the tubing, then close the valve.
4. Open the CO2 valve and start the stopwatch at the same instant.
5. Let gas collect until the tube holds a comfortably readable volume, then close the valve and stop the stopwatch at the same instant. Note the elapsed time.
6. Raise or lower the collection tube until the liquid level inside matches the level in the trough, so the collected gas sits at ambient pressure, then read the collected gas volume off the graduations.
7. Repeat steps 3 to 6 at least five times, refilling the tube each time, so you have five independent measurements for this reactor.
8. Record, for each measurement, the volume of CO2 collected (mL) and the time taken (s) in the **CO₂ flow** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- A graduated measuring cylinder.
- A basin of water and a length of tubing.
- A phone stopwatch.

### Reagents

- Acidified water as above (a little vinegar or citric acid in tap water, sour to taste, pH below 4).

### Method

1. Fill the measuring cylinder with acidified water, cover the mouth, invert it into the basin and uncover it under the surface so it stays full with no trapped air.
2. Feed the CO2 tubing up into the mouth of the cylinder.
3. Vent CO2 through the tubing for a few seconds to clear air, then stop the flow.
4. Start the stopwatch and open the CO2 flow at the same instant.
5. Let gas collect until the cylinder holds a comfortably readable volume, then stop the flow and the stopwatch at the same instant. Note the elapsed time.
6. Lift or lower the cylinder until the water level inside matches the basin surface, then read the collected gas volume off the graduations.
7. Repeat steps 3 to 6 at least five times, refilling the cylinder each time.
8. Record, for each measurement, the volume of CO2 collected (mL) and the time taken (s) in the **CO₂ flow** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab divides the collected volume by the time taken to obtain the CO2 flow rate for that measurement; you enter only the volume and the time, and the model applies its own reactor temperature and pressure rather than any conditions recorded at the trough. For each reactor it then uses the most recent included calibration: a flow rate is a fixed property of that reactor's regulator, valve and tubing, so the latest measurement replaces the older ones rather than being averaged with them. That flow rate feeds both the CO2 dosing flow rate and the minimum sparge time used elsewhere in the model.

## Principle & background

CO2 reaches the vial from a SodaStream-type cylinder through a regulator and a solenoid that the Pioreactor pulses open for a commanded duration. The model needs the volumetric flow rate delivered while the solenoid is fully open (mL/s). Measuring a collected volume against the time the valve was open gives that rate directly, which is the same primary-standard idea behind the soap-film / bubble flow meter, where a known gas volume is timed between calibrated marks to give a volumetric rate (https://patents.google.com/patent/US4691577A/en, https://www.sigmaaldrich.com/US/en/product/supelco/20433u).

Gas volume is only meaningful once its pressure is known and equilibrated to atmospheric, which is why the collection tube is levelled against the trough surface before reading, and why the reading is later corrected to the reactor's temperature and pressure by the ideal-gas law (https://lab-training.com/measurement-gas-volumes-laboratories/, https://sciencing.com/measure-gas-using-water-displacement-7912117.html).

The minimum sparge time - the shortest pulse that still delivers a repeatable volume - follows from the same flow rate. A small solenoid opens and closes within a few to about 10 ms, and those switching times are fixed for a given valve and drive (https://tameson.com/pages/solenoid-valve-timer). When a commanded pulse approaches that mechanical timescale the fixed open/close bolus and timing jitter dominate, so the usable floor sits near 0.2 s and shorter pulses are erratic.

The capture liquid matters. CO2 is far more soluble in plain water than O2 or H2, and it reacts to form bicarbonate, so it does not simply obey Henry's law: below about pH 4.5 dissolved inorganic carbon is overwhelmingly free CO2 gas, while at pH 8.3 and above it is mostly bicarbonate and is lost from the captured volume (https://link.springer.com/article/10.1007/s12665-024-11836-3). Capturing over plain water therefore under-reads CO2. Acidifying the trough water to below pH 4 (or using CO2-saturated water / saturated brine) and working quickly keeps that loss small.

## Sources

- Soap-film / bubble flow meter as a primary volumetric gas-flow standard: https://patents.google.com/patent/US4691577A/en and https://www.sigmaaldrich.com/US/en/product/supelco/20433u
- Gas collection by water displacement and the need to equilibrate pressure before reading volume: https://lab-training.com/measurement-gas-volumes-laboratories/ and https://sciencing.com/measure-gas-using-water-displacement-7912117.html
- Solenoid valve open/close timescale (few to about 10 ms) and fixed, repeatable switching times: https://tameson.com/pages/solenoid-valve-timer
- CO2 speciation vs pH (free CO2 below about 4.5, bicarbonate above about 8.3), motivating acidified / saturated capture liquid: https://link.springer.com/article/10.1007/s12665-024-11836-3
