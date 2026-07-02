---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Dissolved oxygen: probe + organism DO bands"
sources:
  - https://www.mdpi.com/2306-5354/9/5/204
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC9138072/
  - https://www.sciencedirect.com/science/article/abs/pii/S1096717620300781
  - https://bacdive.dsmz.de/strain/2008
  - https://www.sciencedirect.com/topics/engineering/oxygen-limitation
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9815084/
  - https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration
  - https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
  - https://onlinelibrary.wiley.com/doi/10.1002/bies.201500002
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, dissolved-oxygen, DO, biology]
---

# Dissolved oxygen: probe + organism DO bands

## Optimal protocol

### Kit

- The Pioreactor running the reactor under test, with the real CO2 sparge line and electrolysis electrodes it uses in service.
- An optical (luminescence-quenching) dissolved-oxygen probe or sensor patch sized for the vial, with a meter that has temperature compensation. Optical is preferred over a Clark-type electrode in this small stirred vial: it does not consume oxygen, is insensitive to the stirring, and the patch form factor fits without displacing much liquid.
- The Pioreactor's built-in optical-density logging, which reports the growth rate for a run directly.
- Enough clean vials to run each dissolved-oxygen setpoint in duplicate.
- A thermometer for the medium and, if available, a barometer.

### Reagents

- The working growth medium.
- A freshly made sodium sulphite (Na2SO3) solution for the zero point: about 1 g or more per litre of deionised water, optionally with a trace of cobalt(II) chloride as catalyst. Make it immediately before use, as it re-oxygenates from air within hours.
- Air-saturated water, or a source of water-saturated air, for the span point.

### Method

1. Zero the probe: immerse it in the freshly made sodium sulphite solution, wait 2 to 3 minutes until the reading is stable and low, and set the meter's zero to that reading.
2. Span the probe: hold it in water-saturated air just above a stirred water surface with no droplets on the membrane or patch, or in vigorously air-sparged water. Enter the local temperature and barometric pressure on the meter, wait for the reading to settle, and set the span to air saturation.
3. Set the meter's compensation temperature to the run temperature, 30 °C for Cupriavidus necator. For an amperometric probe, also enter the medium salinity or conductivity; an optical probe needs only the temperature.
4. Fit the probe through the cap so the sensing tip sits in the well-mixed bulk, clear of the stir bar and clear of the surface, with no bubble trapped on it. Note the depth so every run matches.
5. Fill the vial with the working medium at the operating volume, hold it at 30 °C, and run the stirrer at the operating setpoint for the whole measurement.
6. Choose a series of dissolved-oxygen setpoints spanning from near zero up towards the suspected toxic ceiling. For C. necator, a spread such as 0.5, 1, 2, 2.5, 3, 4, 6, 9 and 11 mg/L works. Set and hold each level using the electrolysis current and CO2 sparge together, keeping temperature, gas supply and starting cell density the same for every setpoint.
7. At each held setpoint, inoculate to the same starting cell density and let the culture grow while the reactor logs optical density over time. Read the growth rate for that setpoint from the reactor's optical-density log.
8. Plot the growth rate for each setpoint against the dissolved-oxygen level it was held at. Read four levels off the plotted curve: the optimum is the dissolved oxygen at the peak of the curve; the minimum is where the curve first rises off the flat baseline; the impairment is the higher dissolved oxygen at which the curve has clearly dropped below the peak; the toxic level is where growth falls away towards zero. Note how you judged each point so later organisms are read the same way.
9. Re-read the air-saturation span point at the end of each run. Discard any run whose end reading has drifted beyond the probe's stated accuracy.
10. Run each setpoint in at least duplicate vials.
11. Validate the running dissolved oxygen: run one balanced growth experiment with the sparge schedule the model recommends and the dissolved oxygen held at the organism's optimum, logging the probe reading continuously through growth. Note the average steady reading and compare it against the steady-state dissolved oxygen the model predicts. Close agreement confirms the oxygen balance; a large gap flags the transfer coefficient, Faradaic efficiency or uptake ratio upstream.
12. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- The Pioreactor and vial as above.
- A low-cost optical dissolved-oxygen probe and meter.

### Reagents

- The working growth medium.
- Air-saturated water, or water-saturated air, for the span point. The sodium sulphite zero is the part you can skip on a budget, accepting reduced accuracy at the low end.

### Method

1. Calibrate the probe against air saturation only: hold it in water-saturated air or vigorously air-sparged water, enter the local temperature and barometric pressure, and set the span once the reading settles. Set the meter's compensation temperature to 30 °C for C. necator.
2. For each organism, take the minimum, optimum, impairment and toxic levels from published literature where they exist. For C. necator, use the published microaerophilic optimum, the impairment level above it, and the high-oxygen toxic ceiling. Where the literature gives only a range, take the range or its midpoint and note that you did. Leave any level the literature does not support blank rather than inventing one.
3. During a normal balanced growth run, take a few spot dissolved-oxygen readings with the probe rather than a continuous trace. Compare them against the steady-state dissolved oxygen the model predicts: readings clustered near the prediction confirm the oxygen balance, while a consistent large offset flags it.
4. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab averages the included dissolved-oxygen levels recorded for each organism, so every additional experiment sharpens the estimate of that organism's band. The averaged minimum, optimum, impairment and toxic levels set the dissolved-oxygen band the model works to, which in turn fixes the target operating dissolved oxygen and the sparge schedule that holds it.

## Principle & background

The model carries a four-point dissolved-oxygen band for each hydrogen-oxidising organism: the minimum, below which growth is oxygen-limited; the optimum, at which the specific growth rate peaks; the impairment level, at which growth is measurably reduced; and the toxic level, at which growth is strongly inhibited or the cells die. These four numbers set the target operating dissolved oxygen and, through the sparge schedule, the whole gas regime. They are found by holding the culture at a series of dissolved-oxygen levels and watching how the growth rate changes, which is why the optimal protocol sweeps setpoints and reads the band off the growth-rate curve.

Two distinct quantities are involved and must not be confused. The band is an organism property: it is the same whatever reactor the cells are in, and it is located by varying dissolved oxygen and measuring growth rate. The running dissolved oxygen the probe reads during a balanced culture is a reactor-plus-organism property: it is what the oxygen balance predicts the surface should settle at during a controlled run. A single growth run gives that running value, not the band; the band needs the setpoint sweep. The optimal protocol measures both, so the live probe trace validates the predicted running level while the growth-rate assays locate the band.

Cupriavidus necator is microaerophilic. In gas-fermentation studies the dissolved oxygen was deliberately held below roughly 1.6 mg/L, and whole-cell growth is inhibited above about 0.30 atm oxygen partial pressure (Wilde and Schlegel), which converts through Henry's law to roughly 11.5 mg/L dissolved as the toxic ceiling. This supports a low-oxygen optimum and a high-oxygen toxic ceiling for that organism. Most other organisms in the table, and the minimum level for every organism, remain to be measured, so those cells stay flagged as data gaps rather than being filled with a guess.

The measurement itself is either amperometric or optical. A Clark-type electrode reduces oxygen at a polarised cathode behind a gas-permeable membrane; the current is proportional to oxygen partial pressure, but the electrode consumes a little oxygen, so it needs flow across the membrane and drifts over time, and it needs both temperature and salinity compensation. An optical, luminescence-quenching probe measures the oxygen-dependent quenching of a fluorescent dye; it is flow- and salt-independent, drifts less, and comes as small patches or pill sensors that suit a 16 to 30 mL vial, needing only temperature compensation. Both report partial pressure, so both must be temperature-compensated, and calibration before every run is the single largest error source.

## Sources

- Lab-scale cultivation of Cupriavidus necator on explosive gas mixtures (DO held below ~1.6 mg/L; microaerophilic operation): https://www.mdpi.com/2306-5354/9/5/204 and https://pmc.ncbi.nlm.nih.gov/articles/PMC9138072/
- Metabolic engineering of C. necator H16 under oxygen-limiting conditions (low-oxygen growth vs PHB trade-off): https://www.sciencedirect.com/science/article/abs/pii/S1096717620300781
- BacDive strain record, C. necator H16 (Wilde / Schlegel H16 provenance for the 0.30 atm inhibition lineage): https://bacdive.dsmz.de/strain/2008
- Oxygen limitation and critical DO (specific growth rate becomes DO-dependent below a critical level): https://www.sciencedirect.com/topics/engineering/oxygen-limitation
- Critical-DO threshold methodology, chemostat DO bands (Penicillium chrysogenum example of staged DO thresholds): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9815084/
- DO sensor calibration, sodium-sulphite zero + air-saturation span: https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration
- US EPA QA bulletin, calibration of dissolved-oxygen meters: https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf
- Optical vs Clark electrode, face-to-face biosensor study (flow/salt independence, small-volume suitability): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
- Wolfbeis (2015), luminescent O2 sensing vs the Clark electrode (BioEssays): https://onlinelibrary.wiley.com/doi/10.1002/bies.201500002
