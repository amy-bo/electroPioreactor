---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Surface oxygen transfer (kL_surf) by dynamic gassing-out"
sources:
  - https://www.bioprocessintl.com/sponsored-content/improving-bioreactor-performance-measuring-dissolved-oxygen-to-determine-kla
  - https://www.eppendorf.com/ie-en/lab-academy/applied-industries/bioprocessing/measuring-the-kla-of-cell-culture-bioreactors/
  - https://bioprocesstools.com/blog/how-to-calculate-kla/
  - https://www.biologydiscussion.com/cell-biology/assessment-of-kla-oxygen-transfer-coefficient-6-methods/7681
  - https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/pdf/10.1002/bit.260460412
  - https://scijournals.onlinelibrary.wiley.com/doi/10.1002/jctb.5157
  - https://www.bioprocessintl.com/bioreactors/measuring-kla-for-better-bioreactor-performance
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
  - https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf
  - https://www.scientificbio.com/blog/how-to-choose-the-right-dissolved-oxygen-sensor/
  - https://www.sciencedirect.com/topics/engineering/surface-aeration
  - https://www.bioprocessintl.com/bioreactors/lessons-in-bioreactor-s-scale-up-part-4-physiochemical-factors-affecting-oxygen-transfer-and-the-volumetric-mass-transfer-coefficient-in-stirred-tanks
  - https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, mass-transfer, kla, dissolved-oxygen]
---

# Surface oxygen transfer (kL_surf) by dynamic gassing-out

## Optimal protocol

Best accuracy: a fast lab-grade dissolved-oxygen probe in the real reactor geometry.

### Kit

- A fast dissolved-oxygen (DO) probe: an optical luminescence-quenching probe (for example a PreSens or Hamilton VisiFerm) or a small Clark-type electrode. Note its quoted response time (t63 or t95) from the datasheet before you start.
- A DO logger or logging software able to record at 1 Hz or faster.
- A nitrogen supply feeding the vial's existing sparge tube.
- A small air source (for example an aquarium air pump) for the saturation/span step.
- A clean reactor vial of the exact operating geometry, fitted with the same inserts that sit in the real reactor.

### Reagents

- The actual Sydow 2017 minimal medium (preferred), or de-ionised water. Medium is the more faithful choice because its salts shift oxygen solubility and coalescence slightly.
- Nitrogen, as the inert stripping gas.

### Method

1. Fill the vial with the operating working volume of medium (or de-ionised water).
2. Hold the vial at 30 °C and run the stir bar at 500 rpm. Keep both steady for the whole measurement.
3. Fit the DO probe through the cap so the sensing tip sits in the well-mixed bulk, clear of the stir bar and clear of the surface. Make sure no bubble is trapped on the tip.
4. Calibrate the probe at two points: set zero in fully nitrogen-sparged water, and set span at 100% air saturation by bubbling air through the stirred medium until the reading is stable. Read your own stable air-saturated plateau as the working saturation value C*.
5. Deoxygenate the liquid: sparge nitrogen through the sparge tube, at 30 °C and 500 rpm, until the DO reading falls to near zero and holds steady. Do not sparge longer than needed to reach a low, stable start point.
6. Stop the nitrogen cleanly and let the headspace return to its vented composition. Start logging DO against time immediately, at 1 s intervals or faster, with the stirrer still at 500 rpm.
7. Keep logging until the curve flattens at the air-saturated plateau.
8. Run one further sweep with the stirrer switched OFF as a contrast. This one must re-aerate markedly more slowly than the stirred sweep. If it does not, gas is entering by some other path (ingress or a leak): discard the dataset, reseal the vial and inserts, and start again.
9. Repeat the stirred sweep so you have at least three good stirred datasets in all.
10. For each stirred sweep, compute kLa from the re-aeration curve:
    a. Take C* as the stable air-saturated plateau at the run temperature.
    b. For each logged point form ln(C* − C).
    c. Linear-regress ln(C* − C) against time over the window from the tenth to the ninetieth percentile of the approach to the plateau (the 10–90% approach window).
    d. kLa = −slope, in per second.
    Take the mean of your stirred sweeps.
11. Probe-lag gate: multiply the probe response time τ by the measured kLa. If τ·kLa exceeds about 0.05, the simple log-slope reads low; fit the two-parameter model that convolves the first-order probe response with the first-order liquid response (probe + kLa together) instead of the bare log-slope, and use that fitted kLa.
12. Record the measured surface mass-transfer coefficient kLa (per second) from your dissolved-oxygen re-aeration fit in the **Surface kLa** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet. The kLa is only valid if the run conditions match the real reactor, so record the stirrer speed, vial, working volume and insert set alongside it in the Notes (the fixed operating values are 500 rpm, ~16 mL working volume and the standard insert set).

## Budget protocol

Lower-kit variant: a low-cost optical DO probe (an inexpensive optical DO module or a hobby galvanic DO meter) in the same vial. A cheap probe responds two to four times slower than a Clark electrode, so its result is provisional.

### Kit

- A low-cost optical or galvanic DO meter. Note its response time.
- A small air source (for example an aquarium air pump) for the saturation/span step.
- A nitrogen supply (preferred), or a fresh sodium-sulphite (or sodium-metabisulphite) charge as a fallback deoxygenant.
- A logger, or a stopwatch with phone-timestamped manual readings.
- The same reactor vial and working volume as the optimal route (temperature control and the 500 rpm stirrer are onboard).

### Method

1. Fill the same vial with the same working volume. Hold 30 °C and 500 rpm. If you cannot hold 30 °C, run at room temperature and record the actual temperature.
2. Calibrate the meter at two points: set zero against vigorously nitrogen-sparged water (or a freshly made sodium-sulphite solution), and set span against air-saturated stirred water.
3. Deoxygenate by nitrogen sparge through the sparge tube until the reading bottoms out and holds steady. If no nitrogen is available, use a fresh sodium-sulphite charge to pull DO to near zero, then change to fresh aerating medium before the sweep so no residual sulphite keeps consuming oxygen.
4. Stop the gas, start the logger (or the stopwatch), and record DO every two to five seconds with the stirrer at 500 rpm until the reading plateaus. Log densely over the first minute.
5. Take at least two sweeps. If two sweeps disagree by a large margin, suspect a slow probe, a trapped bubble or an unstable plateau, and repeat.
6. Fit each sweep to the first-order re-aeration model as in the optimal protocol (form ln(C* − C), regress against time over the 10–90% approach window, kLa = −slope) and take the mean. Note the probe model and its response time alongside the result, as this variant is provisional; apply the same probe-lag gate (if τ·kLa exceeds about 0.05, fit the two-parameter probe + kLa model instead).
7. Record the measured surface mass-transfer coefficient kLa (per second) from your dissolved-oxygen re-aeration fit in the **Surface kLa** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet. The kLa is only valid if the run conditions match the real reactor, so record the stirrer speed, vial, working volume and insert set alongside it in the Notes (500 rpm, ~16 mL working volume, standard insert set).

## What the spreadsheet does with it

The Surface kLa section of the Calibrations tab gathers every re-aeration run you enter for a given reactor. For each run marked Include, the tab averages the recorded kLa values for that reactor and uses that measured average in place of the model's built-in penetration-theory proxy. It then compares the measured value against the critical surface coefficient the model derives, and reports the margin between them, so the schedule regime follows from your measurement rather than from the proxy.

## Principle & background

The electro-bioreactor makes oxygen at the anode, and in this stirred ~16 mL working volume the dominant route for getting that oxygen back out of the liquid is transfer across the free surface into the vented headspace – there is no continuous air sparge doing the work. The rate is set by a surface volumetric oxygen mass-transfer coefficient, kLa_surf, where kL_surf is the liquid-film coefficient (m/s) and a_surf is the gas-liquid interfacial area per unit liquid volume (1/m). The model estimates kL_surf from a Higbie penetration-theory proxy (kL_surf = 2·√(D_O₂·s_renew/π), with the surface-renewal frequency s_renew = tip_speed/vial_ID). That proxy is unvalidated and is the single most sensitive number in the whole model – around 375% sensitivity – and it decides whether the sparge interval sits near 1.4 min or near 178 min, so it has to be replaced by a measured value.

The standard way to measure kLa without a culture is the dynamic gassing-out method ("gas-out / gas-in"). You strip the dissolved oxygen out of the working volume by sparging nitrogen, stop the strip, then let the liquid re-aerate from its own free surface while the stirrer runs at the real operating speed. A DO probe records the re-aeration curve. With no oxygen uptake (no cells) and a well-mixed liquid, the dissolved-oxygen balance is dC/dt = kLa·(C_star − C), where C_star is the saturation DO in equilibrium with the gas above the surface. That integrates to ln(C_star − C) = −kLa·t + const, so a plot of ln(C_star − C) against time is a straight line whose slope is −kLa. That slope is the surface kLa, because surface transfer is the only path operating once the nitrogen is off and there is no sparge. It needs only a DO probe – no off-gas analyser, no hazardous reagents and no organism (Garcia-Ochoa / BioProcess International, and the Eppendorf and bioprocesstools method notes in Sources).

Two things make the measurement specific rather than generic. First, surface renewal scales with stirring, so the run must be at the operating stirrer speed (500 rpm) and in the actual vial geometry – the same free-surface area and the same inserts as the real reactor – or the result will not match what the reactor sees. Record the actual rpm, vial, working volume and inserts. Second, the DO probe has its own first-order response lag; the rule of thumb is that the probe time constant should be under about a tenth of the mass-transfer time constant (1/kLa), and more strictly the product of probe time constant and kLa should stay below roughly 0.02 to 0.05. Surface kLa in a small stirred vial is slow (of the order of 0.001 to 0.01 per second, a time constant of minutes) and lab probes respond in tens of seconds, so the lag is often acceptable – but check it. If the product exceeds about 0.05, fit a two-parameter model that convolves the first-order liquid response with the first-order probe response (or use the Torres 2017 system-delay algorithm) rather than the bare log-slope, otherwise kLa reads low. A slow budget probe is the most likely reason a measurement comes out artificially under the critical value (Tribe 1995; Torres 2017; Sources).

The saturation value matters as much as the slope. Read C_star as your own stable air-saturated plateau; cross-check it against about 7.54 mg/L at 30 °C and roughly 1 atm in fresh water, and note that medium salts and local pressure shift it. Fit the linear middle of the curve (about the tenth to the ninetieth percentile of the approach to C_star): the lag-dominated early points and the noisy near-plateau tail both bias the slope. Watch for a trapped bubble on the probe tip or a stuck stir bar, as both flatten the curve and read low; the stirrer-off contrast sweep should give a clearly lower kLa, and if it does not, gas is leaking in by some other path and the surface number is not what you measured. Keep the liquid free of oxygen-consuming residue: sulphite left in the liquid keeps eating oxygen and corrupts the slope, which is why nitrogen stripping is preferred and, if sulphite is used, the medium is swapped before the sweep. Replicate rather than trusting a single sweep (three or more for the optimal protocol, two or more for the budget one) and report the mean and spread.

The decision the measurement drives is a threshold. The model derives a critical surface coefficient, kL_surf_crit (currently about 1.2×10⁻⁴ m/s), the minimum liquid-film coefficient at which surface stripping alone holds dissolved oxygen under the impairment band. The measured kL_surf must exceed kL_surf_crit. Report the margin as the ratio of measured to critical, not just pass or fail: above 1 means surface stripping alone can hold DO and the reactor sits in the carbon-limited regime with the long interval near 178 min; below 1 means it cannot and the schedule stays oxygen-limited with the short interval near 1.4 min. If you want kL_surf itself (m/s) rather than the lumped kLa, divide the measured kLa by the model's area-per-volume term a_surf (the free-surface area per liquid volume, 1/m), using the model's geometry value so the conversion stays consistent with the rest of the sheet.

## Sources

- Dynamic gassing-out method, overview and steps: [BioProcess International – Improving Bioreactor Performance: Measuring Dissolved Oxygen to Determine kLa](https://www.bioprocessintl.com/sponsored-content/improving-bioreactor-performance-measuring-dissolved-oxygen-to-determine-kla); [Eppendorf – Measuring the kLa of Cell Culture Bioreactors](https://www.eppendorf.com/ie-en/lab-academy/applied-industries/bioprocessing/measuring-the-kla-of-cell-culture-bioreactors/); [bioprocesstools – How to Calculate kLa](https://bioprocesstools.com/blog/how-to-calculate-kla/); [Assessment of kLa – 6 Methods](https://www.biologydiscussion.com/cell-biology/assessment-of-kla-oxygen-transfer-coefficient-6-methods/7681).
- Probe-lag (first-order sensor) errors and correction: [Tribe et al. 1995, Determination of kLa using the dynamic gas out-gas in method: errors caused by dissolved oxygen probes (Biotechnol. Bioeng.)](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/pdf/10.1002/bit.260460412); [Torres et al. 2017, Automated algorithm to determine kLa considering system delay (J. Chem. Technol. Biotechnol.)](https://scijournals.onlinelibrary.wiley.com/doi/10.1002/jctb.5157); [BioProcess International – Measuring kLa for Better Bioreactor Performance](https://www.bioprocessintl.com/bioreactors/measuring-kla-for-better-bioreactor-performance).
- Probe choice (optical vs Clark) – response time and accuracy: [Optical Oxygen Sensing and Clark Electrode: Face-to-Face in a Biosensor Case Study (PMC9572888)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/); [USGS – Field Comparison of Optical and Clark Cell Dissolved Oxygen Sensors](https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf); [Scientific Bioprocessing – How to Choose the Right Dissolved Oxygen Sensor](https://www.scientificbio.com/blog/how-to-choose-the-right-dissolved-oxygen-sensor/).
- Surface aeration and kLa = kL · a in stirred vessels: [ScienceDirect Topics – Surface Aeration](https://www.sciencedirect.com/topics/engineering/surface-aeration); [BioProcess International – Oxygen Transfer and the Volumetric Mass-Transfer Coefficient in Stirred Tanks](https://www.bioprocessintl.com/bioreactors/lessons-in-bioreactor-s-scale-up-part-4-physiochemical-factors-affecting-oxygen-transfer-and-the-volumetric-mass-transfer-coefficient-in-stirred-tanks).
- DO saturation at 30 °C for C_star cross-check: [Fondriest – Dissolved Oxygen (100% air saturation ~7.54 mg/L at 30 °C)](https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/).
