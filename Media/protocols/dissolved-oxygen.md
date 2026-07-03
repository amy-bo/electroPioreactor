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

- An optical (luminescence-quenching) dissolved-oxygen probe or sensor patch sized for the vial, with a meter that has temperature compensation. Optical is preferred over a Clark-type electrode in this small stirred vial: it does not consume oxygen, is insensitive to the stirring, and the patch form factor fits without displacing much liquid.
- A thermometer for the medium.
- A barometer, if available.
- Enough clean vials to run each dissolved-oxygen setpoint in duplicate.
- The Pioreactor running the reactor under test, with the real CO₂ sparge line and electrolysis electrodes it uses in service.

### Reagents

- The working growth medium.
- A freshly made sodium sulphite (Na₂SO₃) solution for the zero point: about 1 g or more per litre of deionised water. A trace of cobalt(II) chloride speeds the reaction, but CoCl₂ is a carcinogen and skin sensitiser: if you use it, wear gloves and route the spent solution to heavy-metal waste. The sulphite zeroes the probe on its own without the catalyst, just more slowly, so dropping it is the safer default. Make the solution immediately before use, as it re-oxygenates from air within hours.
- Air-saturated water, or a source of water-saturated air, for the span point.

### Method

1. Zero the probe: immerse it in the freshly made sodium sulphite solution, wait 2 to 3 minutes until the reading is stable and low, and set the meter's zero to that reading.
2. Span the probe: hold it in water-saturated air just above a stirred water surface with no droplets on the membrane or patch, or in vigorously air-sparged water. Enter the local temperature and barometric pressure on the meter, wait for the reading to settle, and set the span to air saturation. At 30 °C this air-saturation span sits at about 7.54 mg/L; that single span point is the only anchor, so any reading above it is extrapolated.
3. Set the meter's compensation temperature to the run temperature, 30 °C for Cupriavidus necator. For an amperometric probe, also enter the medium salinity or conductivity. An optical probe needs only the temperature for its own reading, but converting that reading to mg/L still needs the medium's salinity or solubility correction unless the probe reports per cent saturation or oxygen partial pressure directly.
4. Fit the probe through the cap so the sensing tip sits in the well-mixed bulk, clear of the stir bar and clear of the surface, with no bubble trapped on it. Note the depth so every run matches.
5. Fill the vial with the working medium at the operating volume, hold it at 30 °C, and run the stirrer at the operating setpoint for the whole measurement.
6. Choose a series of dissolved-oxygen setpoints spanning from near zero up towards the suspected toxic ceiling. For C. necator, a spread such as 0.5, 1, 2, 2.5, 3, 4, 6, 9 and 11 mg/L works. Hold each level manually in closed loop off the probe: raise the electrolysis power a step when the reading sits below the setpoint and lower it a step when it sits above, so the reading stays within ±0.3 mg/L of target for the whole assay, with the CO₂ sparge running throughout. The high setpoints (about 9 and 11 mg/L) sit above the air-saturation span, so their held values are extrapolated above the calibration point and carry more uncertainty than the in-range ones. Keep temperature, gas supply and starting cell density the same for every setpoint.
7. **Safety (in-culture electrolysis):** in-culture electrolysis evolves hydrogen and oxygen together; here the CO₂ sparge runs and inerts the headspace. Keep the sparge running whenever current flows, do not occlude the vent, ventilate the area, and exclude ignition sources. This applies with force at the top setpoints, where holding up to 11 mg/L drives the electrolysis current hard.
8. At each held setpoint, inoculate to the same starting cell density and let the culture grow while the reactor logs optical density over time. Grow through the full exponential phase into early stationary, typically 24 to 48 h, with enough logged points to fit the exponential slope cleanly (at least five or six points across the exponential phase). Read the specific growth rate µ for that setpoint from the slope of the reactor's optical-density log.
9. Plot µ for each setpoint against the dissolved-oxygen level it was held at. Read four levels off the plotted curve. The optimum is the dissolved oxygen at the peak of the curve. The minimum is where the curve first rises off the flat baseline. The impairment level is the higher dissolved oxygen at which µ has fallen to about 80 per cent of its peak. The toxic level is the dissolved oxygen at which µ has fallen to 10 per cent or less of its peak. Applying those numeric rules keeps every organism read the same way.
10. Re-read the air-saturation span point at the end of each run. Discard any run whose end reading has drifted beyond the probe's stated accuracy.
11. Run each setpoint in at least duplicate vials.
12. Validate the running dissolved oxygen: run one balanced growth experiment with the sparge schedule the model recommends and the dissolved oxygen held at the organism's optimum, logging the probe reading continuously through growth. Note the average steady reading and compare it against the steady-state dissolved oxygen the model predicts. Close agreement confirms the oxygen balance; a large gap flags the transfer coefficient, Faradaic efficiency or uptake ratio upstream. This step leans on the flow, knallgas and kLa calibrations, so do it after those are done – otherwise the predicted steady-state value it checks against is not yet trustworthy.
13. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- A low-cost optical dissolved-oxygen probe and meter.
- The Pioreactor and vial as above.

### Reagents

- The working growth medium.
- Air-saturated water, or water-saturated air, for the span point. The sodium sulphite zero is the part you can skip on a budget, accepting reduced accuracy at the low end.

### Method

1. Calibrate the probe against air saturation only: hold it in water-saturated air or vigorously air-sparged water, enter the local temperature and barometric pressure, and set the span once the reading settles. Set the meter's compensation temperature to 30 °C for C. necator.
2. For each organism, take the minimum, optimum, impairment and toxic levels from published literature where they exist. For C. necator, use the values already summarised in the Principle section below rather than going back to the papers:

   | Level | C. necator value | Basis |
   | --- | --- | --- |
   | Minimum | not established | data gap – leave blank |
   | Optimum | low, operated below ~1.6 mg/L | gas-fermentation practice |
   | Impairment | not established | data gap – leave blank |
   | Toxic ceiling | ~11 mg/L | 0.30 atm O₂ inhibition, scaled from the 30 °C anchor |

   Where the literature gives only a range, take the range or its midpoint and note that you did. Leave any level the literature does not support blank rather than inventing one.
3. During a normal balanced growth run, take a few spot dissolved-oxygen readings with the probe rather than a continuous trace. Compare them against the steady-state dissolved oxygen the model predicts: readings clustered near the prediction confirm the oxygen balance, while a consistent large offset flags it.
4. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab averages the included dissolved-oxygen levels recorded for each organism, so every additional experiment sharpens the estimate of that organism's band. The averaged minimum, optimum, impairment and toxic levels set the dissolved-oxygen band the model works to, which in turn fixes the target operating dissolved oxygen and the sparge schedule that holds it.

## Principle & background

The model carries a four-point dissolved-oxygen band for each hydrogen-oxidising organism: the minimum, below which growth is oxygen-limited; the optimum, at which the specific growth rate peaks; the impairment level, at which growth is measurably reduced; and the toxic level, at which growth is strongly inhibited or the cells die. These four numbers set the target operating dissolved oxygen and, through the sparge schedule, the whole gas regime. They are found by holding the culture at a series of dissolved-oxygen levels and watching how the growth rate changes, which is why the optimal protocol sweeps setpoints and reads the band off the growth-rate curve.

Two distinct quantities are involved and must not be confused. The band is an organism property: it is the same whatever reactor the cells are in, and it is located by varying dissolved oxygen and measuring growth rate. The running dissolved oxygen the probe reads during a balanced culture is a reactor-plus-organism property: it is what the oxygen balance predicts the surface should settle at during a controlled run. A single growth run gives that running value, not the band; the band needs the setpoint sweep. The optimal protocol measures both, so the live probe trace validates the predicted running level while the growth-rate assays locate the band.

Cupriavidus necator is not obligately microaerophilic; it is a facultative chemolithoautotroph that grows aerobically. It is nonetheless run at low dissolved oxygen for two practical reasons rather than an oxygen requirement: its knallgas hydrogenase is oxygen-labile and loses activity as dissolved oxygen rises, and holding the headspace oxygen low keeps the hydrogen–oxygen gas mix out of its explosive range. In gas-fermentation studies the dissolved oxygen was deliberately held below roughly 1.6 mg/L, and whole-cell growth is inhibited above about 0.30 atm oxygen partial pressure (Wilde and Schlegel), which converts through Henry's law – scaled from the 30 °C air-saturation anchor of 7.54 mg/L – to roughly 11.0 mg/L dissolved as the toxic ceiling. Note the tension in those two numbers: the toxic ceiling of about 11 mg/L sits above air saturation, so it is a supersaturation limit the organism only meets under forced oxygenation, not a level ambient air can reach. This supports a low-oxygen operating window with a high, supersaturated toxic ceiling. Most other organisms in the table, and the minimum level for every organism, remain to be measured, so those cells stay flagged as data gaps rather than being filled with a guess.

The measurement itself is either amperometric or optical. A Clark-type electrode reduces oxygen at a polarised cathode behind a gas-permeable membrane; the current is proportional to oxygen partial pressure, but the electrode consumes a little oxygen, so it needs flow across the membrane and drifts over time, and it needs both temperature and salinity compensation. An optical, luminescence-quenching probe measures the oxygen-dependent quenching of a fluorescent dye; it is flow- and salt-independent in its raw reading, drifts less, and comes as small patches or pill sensors that suit a 16 to 30 mL vial, needing only temperature compensation to report partial pressure or per cent saturation – though converting that to mg/L still needs the medium's solubility. Both report partial pressure, so both must be temperature-compensated, and calibration before every run is the single largest error source.

## Sources

- Lab-scale cultivation of Cupriavidus necator on explosive gas mixtures (DO held below ~1.6 mg/L; low-oxygen operation): https://www.mdpi.com/2306-5354/9/5/204 and https://pmc.ncbi.nlm.nih.gov/articles/PMC9138072/
- Metabolic engineering of C. necator H16 under oxygen-limiting conditions (low-oxygen growth vs PHB trade-off): https://www.sciencedirect.com/science/article/abs/pii/S1096717620300781
- BacDive strain record, C. necator H16 (Wilde / Schlegel H16 provenance for the 0.30 atm inhibition lineage): https://bacdive.dsmz.de/strain/2008
- Oxygen limitation and critical DO (specific growth rate becomes DO-dependent below a critical level): https://www.sciencedirect.com/topics/engineering/oxygen-limitation
- Critical-DO threshold methodology, chemostat DO bands (Penicillium chrysogenum example of staged DO thresholds): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9815084/
- DO sensor calibration, sodium-sulphite zero + air-saturation span: https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration
- US EPA QA bulletin, calibration of dissolved-oxygen meters: https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf
- Optical vs Clark electrode, face-to-face biosensor study (flow/salt independence, small-volume suitability): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
- Wolfbeis (2015), luminescent O₂ sensing vs the Clark electrode (BioEssays): https://onlinelibrary.wiley.com/doi/10.1002/bies.201500002
