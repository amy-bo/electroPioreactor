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

- An optical (luminescence-quenching) dissolved-oxygen sensor for the vial, with a temperature-compensating meter: either an O₂ patch adhered inside the vial wall and read through the glass, or a fibre needle microsensor through the cap's hypodermic-needle gap. A body-style insertion probe will not fit, as the two electrode ports are occupied and the 1.4 mm ports are too small. Optical is preferred over a Clark-type electrode here: it does not consume oxygen, is insensitive to the stirring, and the patch needs no cap port.
- A thermometer for the medium.
- A barometer, if available.
- Enough clean vials to run each dissolved-oxygen setpoint in duplicate.
- The Pioreactor running the reactor under test, with the real CO₂ sparge line and electrolysis electrodes it uses in service.

### Reagents

- The actual medium in use (for example [AM002](../README.md)).
- A freshly made sodium sulphite (Na₂SO₃) solution for the zero point: about 1 g or more per litre of deionised water. A trace of cobalt(II) chloride speeds the reaction, but CoCl₂ is a carcinogen and skin sensitiser: if you use it, wear gloves and route the spent solution to heavy-metal waste. The sulphite zeroes the probe on its own without the catalyst, just more slowly, so dropping it is the safer default. Make the solution immediately before use, as it re-oxygenates from air within hours.
- Air-saturated water, or a source of water-saturated air, for the span point.

### Method

1. Zero the probe: immerse it in the freshly made sodium sulphite solution, wait 2 to 3 minutes until the reading is stable and low, and set the meter's zero to that reading.
2. Span the probe: hold it in water-saturated air just above a stirred water surface with no droplets on the membrane or patch, or in vigorously air-sparged water. Enter the local temperature and barometric pressure on the meter, wait for the reading to settle, and set the span to air saturation. At 30 °C this air-saturation span sits at about 7.54 mg/L; that single span point is the only anchor, so any reading above it is extrapolated.
3. Set the meter's compensation temperature to the run temperature, 30 °C for the current Xanthobacter tagetidis baseline. For an amperometric probe, also enter the medium salinity or conductivity. An optical probe needs only the temperature for its own reading, but converting that reading to mg/L still needs the medium's salinity or solubility correction unless the probe reports per cent saturation or oxygen partial pressure directly.
4. Position the sensor to read the well-mixed bulk: a wall patch below the liquid line and clear of the stir-bar sweep, or a needle microsensor tip in the bulk through the hypodermic-needle gap, in both cases clear of the stir bar and the surface, with no bubble trapped on the sensing face. Note its position so every run matches.
5. Fill the vial with the working medium at the operating volume, hold it at 30 °C, and run the stirrer at the operating setpoint for the whole measurement.
6. Choose a series of dissolved-oxygen setpoints spanning from near zero up towards the suspected toxic ceiling. A historical C. necator example spans 0.5, 1, 2, 2.5, 3, 4, 6, 9 and 11 mg/L; it supplies no Xanthobacter tagetidis thresholds. Owner selection of organism-specific setpoints and a method that controls or independently measures hydrogen availability is a prerequisite. Varying electrolysis changes H₂ as well as O₂; without matched or accounted-for H₂ supply, growth differences cannot be assigned to DO. Hold each level manually in closed loop off the probe: raise or lower electrolysis power only within 3–10 % (the model fit refuses outside this band and plugin runtime clamps at 10 %); stop if the target cannot be held within ±0.3 mg/L using that band, with the CO₂ sparge running throughout. The high setpoints (about 9 and 11 mg/L) sit above the air-saturation span, so their held values are extrapolated above the calibration point and carry more uncertainty than the in-range ones. Keep temperature and starting cell density matched and document the controlled or measured gas availability for each setpoint; a constant CO₂ schedule alone does not hold H₂ supply constant.
7. **Safety (in-culture electrolysis):** H₂ and O₂ evolve together. Read Summary D51/D52 (lag O₂/H₂) for the recorded ed04/MMO tube/Xanthobacter tagetidis/AM003/30 °C selections and the D21/D22 schedule; do not attribute historical gas fractions to this run. Treat the headspace as potentially flammable. Routine CO₂ pulses dilute gases but do not establish inerting. Keep the vent open, ventilate and exclude ignition sources. Resolve the [headspace hazard screen](headspace-gas-safety.md), applicable mixture limits and margins before accepting conditions; the Summary verdict is not certification.
8. At each held setpoint, inoculate to the same starting cell density and let the culture grow while the reactor logs optical density over time. Grow through the full exponential phase into early stationary, typically 24 to 48 h, with enough logged points to fit the exponential slope cleanly (at least five or six points across the exponential phase). Read the specific growth rate µ for that setpoint from the slope of the reactor's optical-density log.
9. Plot µ for each setpoint against the dissolved-oxygen level it was held at. Read four levels off the plotted curve. The optimum is the dissolved oxygen at the peak of the curve. The minimum is where the curve first rises off the flat baseline. The impairment level is the higher dissolved oxygen at which µ has fallen to about 80 per cent of its peak. The toxic level is the dissolved oxygen at which µ has fallen to 10 per cent or less of its peak.
10. Re-read the air-saturation span point at the end of each run. Discard any run whose end reading has drifted beyond the probe's stated accuracy.
11. Run each setpoint in at least duplicate vials.
12. Validate the running dissolved oxygen in a separate balanced growth run at the recorded model operating inputs: fixed power, stirring and Summary D21/D22 schedule, with continuous DO logging. Do not hold DO at the organism optimum by feedback, because feedback changes the oxygen source being validated. Compare the measured steady or cycle-mean DO and uncertainty with the corresponding prediction for those inputs. If feedback is studied, explicitly model and compare its logged source instead. Complete flow, current, Faradaic, uptake and surface-kLa calibrations first. Agreement supports the balance within measurement uncertainty; it does not prove it.
13. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** log (its own sheet, linked from the **Calibrations** overview). Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- A low-cost optical dissolved-oxygen probe and meter.
- The Pioreactor and vial as above.

### Reagents

- The actual medium in use (for example [AM002](../README.md)).
- Air-saturated water, or water-saturated air, for the span point. The sodium sulphite zero is the part you can skip on a budget, accepting reduced accuracy at the low end.

### Method

1. Calibrate the probe against air saturation only: hold it in water-saturated air or vigorously air-sparged water, enter the local temperature and barometric pressure, and set the span once the reading settles. Set the meter's compensation temperature to 30 °C for the current baseline.
2. For each organism, take the minimum, optimum, impairment and toxic levels from published literature where they exist. The following C. necator literature examples are not Xanthobacter tagetidis thresholds; leave unsupported Xanthobacter levels blank. For a C. necator comparison, resolve the source-specific basis before using these summaries:

   | Level | C. necator value | Basis |
   | --- | --- | --- |
   | Minimum | not established | data gap – leave blank |
   | Optimum | low, operated below ~1.6 mg/L | gas-fermentation practice |
   | Impairment | not established | data gap – leave blank |
   | Reported inhibition condition | ~11 mg/L equivalent | 0.30 atm O₂ inhibition; not evidence for the defined ≤10%-growth toxic endpoint |

   Where the literature gives only a range, take the range or its midpoint and note that you did. Leave any level the literature does not support blank rather than inventing one.
3. During a normal balanced growth run, take a few spot dissolved-oxygen readings with the probe rather than a continuous trace. Compare them against the steady-state dissolved oxygen the model predicts: readings clustered near the prediction support the oxygen balance within uncertainty, while a consistent large offset flags it.
4. Record the organism's minimum, optimum, impairment and toxic dissolved-oxygen levels (mg/L) in the **DO thresholds** log (its own sheet, linked from the **Calibrations** overview). Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab averages the included dissolved-oxygen levels recorded for each organism, so every additional experiment sharpens the estimate of that organism's band. The averaged minimum, optimum, impairment and toxic levels set the dissolved-oxygen band the model works to, which in turn fixes the target operating dissolved oxygen and the sparge schedule that holds it.

## Principle & background

The model carries a four-point dissolved-oxygen band for each hydrogen-oxidising organism: the minimum, below which growth is oxygen-limited; the optimum, at which the specific growth rate peaks; the impairment level, at which growth is measurably reduced; and the toxic level, at which growth is strongly inhibited or the cells die. These four numbers set the target operating dissolved oxygen and, through the sparge schedule, the whole gas regime. They are found by holding the culture at a series of dissolved-oxygen levels and watching how the growth rate changes, which is why the optimal protocol sweeps setpoints and reads the band off the growth-rate curve.

Two distinct quantities are involved and must not be confused. The band is an organism property: it is the same whatever reactor the cells are in, and it is located by varying dissolved oxygen and measuring growth rate. The running dissolved oxygen the probe reads during a balanced culture is a reactor-plus-organism property: it is what the oxygen balance predicts the surface should settle at during a controlled run. A single growth run gives that running value, not the band; the band needs the setpoint sweep. The optimal protocol measures both, so the live probe trace validates the predicted running level while the growth-rate assays locate the band.

The C. necator literature is not a source of Xanthobacter thresholds. C. necator has oxygen-tolerant hydrogenases; oxygen responses are enzyme- and condition-specific, so generic hydrogenase oxygen lability is not a valid explanation for its operating DO band. Whole-cell growth inhibition must be assessed separately. The reported 0.30 atm O₂ inhibition condition corresponds approximately to 11 mg/L using the 30 °C fresh-water anchor, but it does not by itself establish this protocol’s toxic endpoint (≤10 % of peak growth). Do not enter that endpoint without evidence matching its definition, strain and conditions. Limiting oxygen in a hydrogen-containing headspace also concerns mixture hazards, independently of biological tolerance.

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
