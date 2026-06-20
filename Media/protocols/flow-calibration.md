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

**Feeds:** 'CO2 flows'!J (nominal flowrate, ml/s) + I (minimum sparge, s) -> flowrate_cal / min_sparge_cal / Q_CO2. Baseline ed04: 3.33 ml/s, 0.25 s.

**Why it matters:** sets CO2 supply rate and the pulse floor; every reactor needs its own (only ed04 done).

## Principle

CO2 reaches the vial from a SodaStream-type cylinder through a regulator and a solenoid that the Pioreactor pulses open for a commanded duration. The model needs two numbers per reactor: the nominal volumetric flowrate while the solenoid is fully open (ml/s) and the minimum reliable sparge duration (s) below which a single pulse no longer delivers a repeatable volume.

The flowrate is found by capturing the sparged gas volumetrically over a range of solenoid-open durations and fitting captured volume against open-time. The slope of that line is the nominal flowrate (ml/s); fitting the slope rather than dividing one capture by one time cancels the fixed open/close bolus, which appears as a non-zero intercept rather than as an error on the flowrate. This is the same primary-standard idea behind the soap-film / bubble flow meter, where a known gas volume is timed between calibrated marks to give a volumetric rate ( https://patents.google.com/patent/US4691577A/en ).

The minimum reliable sparge is the shortest commanded duration that still yields a repeatable per-shot volume. A small solenoid opens and closes within a few to ~10 ms, and its open and close times are fixed for a given valve and drive ( https://tameson.com/pages/solenoid-valve-timer ). When the commanded open-time falls toward that mechanical timescale the fixed open/close bolus plus timing jitter dominate, so per-pulse volume scatters. In practice the floor sits around 0.2 s; below it the per-pulse flow is erratic and the value should not be used in scheduling.

A correction matters for the capture medium. CO2 is far more soluble in plain water than O2 or H2, and it reacts to bicarbonate so it does not simply obey Henry's law: at pH below ~4.5 dissolved inorganic carbon is overwhelmingly free CO2 gas, while at pH 8.3 and above it is mostly bicarbonate and is lost from the captured volume ( https://link.springer.com/article/10.1007/s12665-024-11836-3 ). Capturing over plain tap water therefore under-reads CO2. Suppress the loss by collecting over acidified water (a few drops of acid to pH < 4) or over CO2-pre-saturated water / saturated brine, and keep the capture brief.

## Optimal protocol (best accuracy)

Kit: inverted burette or graduated gas-collection tube (1 ml graduations) over a water trough, or a calibrated soap-film / bubble flow meter ( https://www.sigmaaldrich.com/US/en/product/supelco/20433u ); acidified water (pH < 4) or saturated brine as the trough liquid; a thermometer and a barometer; the Pioreactor running the reactor under test with the real CO2 line and solenoid in place.

1. Run the CO2 line to the inverted collection tube instead of into the vial, with the tube filled with acidified water / brine and its open mouth submerged. Purge the line first by venting a few seconds of CO2 to clear air and dead volume.
2. Record trough liquid temperature, ambient pressure and the liquid head above the trough surface; these set the gas correction at read-out.
3. Command a single solenoid pulse at a fixed open-time, let the captured gas settle, equilibrate the level so the inside and outside liquid heights match (so the trapped gas sits at ambient pressure), then read the captured volume. Gas volume is only meaningful once its pressure is known and equilibrated to atmospheric ( https://lab-training.com/measurement-gas-volumes-laboratories/ ).
4. Repeat across at least five open-times spanning the working range (for example 0.25, 0.5, 1, 2, 4 s), with at least five replicate pulses at each, resetting the tube between points. Sum replicate pulses if a single pulse is too small to read, and divide back out.
5. Plot captured volume (corrected to the reactor's temperature and pressure via the ideal-gas law, as the model already does for the electrolytic gases) against commanded open-time. Fit a straight line. The slope is the nominal flowrate in ml/s; the intercept is the fixed open/close bolus and is expected to be small and positive.
6. For the minimum reliable sparge, step the open-time down (1, 0.5, 0.35, 0.25, 0.2, 0.15 s), ten replicates each, and record the per-shot volume and its spread. The minimum reliable sparge is the shortest open-time whose replicate spread stays within tolerance (suggest coefficient of variation <= 10%). Expect this to land near 0.2 s and to degrade sharply below it.

## Budget protocol (minimal kit)

Kit: a graduated measuring cylinder, a basin of water, a length of tubing, a phone stopwatch, and a little vinegar or citric acid to acidify the water.

1. Fill the cylinder with acidified water, cover the mouth, invert it into the basin and uncover it under water so it stays full ( https://sciencing.com/measure-gas-using-water-displacement-7912117.html ). Feed the CO2 tubing up into the mouth.
2. Purge the line, then deliver a known number of solenoid pulses at one open-time (use many pulses, e.g. 20, at a short open-time so the total is comfortably readable) and read the displaced volume.
3. Repeat at three or more open-times and divide each total by its pulse count to get per-pulse volume, then plot per-pulse volume against open-time and take the slope as the flowrate; the cheap method trades the equilibrated-pressure read-out for more replicates.
4. For the minimum sparge, deliver 10 single pulses at each of 0.5, 0.35, 0.25, 0.2, 0.15 s, eyeball the per-pulse volume scatter, and take the shortest open-time that still gives visibly consistent bubbleslugs as the floor.

Note the budget route over plain water will under-read because CO2 dissolves; acidifying the water is the cheap fix and keeps the bias small.

## Result -> model

Open the workbook, go to the 'CO2 flows' tab, and add a new row for this calibration. In that row enter the reactor ID (for example ed05) in the reactor-ID column, the calibration date in the date column, the fitted nominal flowrate (ml/s) in column J, and the minimum reliable sparge (s) in column I. Do not overwrite the existing ed04 row (3.33 ml/s, 0.25 s); add a fresh dated row. The model reads the latest-dated row per reactor into flowrate_cal, min_sparge_cal and Q_CO2 automatically, so the newest dated entry for a given reactor wins and no formula edits are needed. To revise a calibration later, add another dated row rather than editing the old one, so the history is preserved.

## Acceptance checks & pitfalls

- Linearity: the volume-vs-open-time fit should be close to straight (R^2 >= 0.99). Curvature means the regulator pressure is sagging during long pulses or the line is not fully purged.
- Intercept sanity: a small positive intercept is the open/close bolus and is fine; a large or negative intercept means timing offset or a leak.
- Repeatability floor: confirm the chosen minimum sparge has replicate CV within tolerance and that the next step down clearly fails; do not push the floor below ~0.2 s.
- Pressure equilibration: always level the inside and outside liquid before reading, and correct the captured volume to the reactor temperature and pressure; an un-equilibrated read is biased by the liquid head.
- Dissolution loss: capture over acidified or CO2-saturated water, work quickly, and do not let gas sit over plain water; plain-water capture under-reads CO2.
- Leaks and dead volume: purge the line before each run and check fittings; trapped air reads as extra volume on the first pulses.
- Same line, same regulator: calibrate with the exact solenoid, tubing length and regulator setting the reactor will run, since the flowrate and bolus depend on all three.

## Sources

- Soap-film / bubble flow meter as a primary volumetric gas-flow standard: https://patents.google.com/patent/US4691577A/en and https://www.sigmaaldrich.com/US/en/product/supelco/20433u
- Gas collection by water displacement and the need to equilibrate pressure before reading volume: https://lab-training.com/measurement-gas-volumes-laboratories/ and https://sciencing.com/measure-gas-using-water-displacement-7912117.html
- Solenoid valve open/close timescale (few to ~10 ms) and fixed, repeatable switching times: https://tameson.com/pages/solenoid-valve-timer
- CO2 speciation vs pH (free CO2 below ~4.5, bicarbonate above ~8.3), motivating acidified / saturated capture liquid: https://link.springer.com/article/10.1007/s12665-024-11836-3
