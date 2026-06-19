# Dissolved oxygen: probe + organism DO bands

**Feeds:** Biology HOB table (minimum/optimum/impairment/toxic DO per organism); validates DO_ss.
**Why it matters:** organism DO band sets the target operating DO and the whole sparge schedule.

## Principle

The model carries a four-point dissolved-oxygen (DO) band for each hydrogen-oxidising organism: minimum DO (below which growth is O2-limited), optimum DO (peak specific growth rate), impairment DO (growth measurably reduced), and toxic/inhibition DO (growth strongly inhibited or cells die). These four numbers live in the Biology HOB lookup table (rows 52-57, columns minimum / optimum / impairment / toxic) and are read by DO_min, DO_opt, DO_impair and DO_toxic on the Biology tab. They set the target operating DO and, through the Mass Transfer tab, the entire sparge schedule. Cupriavidus necator is microaerophilic: in gas-fermentation studies DO was deliberately held below roughly 1.6 mg/L, and whole-cell growth is inhibited above about 0.30 atm O2 partial pressure (Wilde & Schlegel), which the model converts via Henry's law to roughly 11.5 mg/L dissolved as the toxic ceiling. Most other organisms in the table, and the minimum DO for every organism, are pink DATA GAPS.

Two distinct quantities are involved and must not be confused. The DO band is an organism property: it is the same whatever reactor the cells are in, and it is found by varying DO and watching growth rate. DO_ss (the steady-state surface DO the model predicts from the O2 balance, Mass Transfer D108) is a reactor-plus-organism property: it is what the DO probe should actually read during a balanced run. This protocol measures both - the probe trace validates the DO_ss prediction, and the growth-rate-versus-DO assays locate the band.

The measurement principle is amperometric or optical quenching. A Clark-type electrode reduces O2 at a polarised cathode behind a gas-permeable membrane; the current is proportional to O2 partial pressure (hence DO) and the electrode consumes a little O2, so it needs flow across the membrane and drifts over time. An optical (luminescent) probe measures the O2-dependent quenching of a fluorescent dye, is flow- and salt-independent, drifts less, and comes as small patches or pill sensors that suit a 16-30 mL Pioreactor vial. Both report partial pressure, so both need temperature compensation, and amperometric probes additionally need salinity compensation because dissolved salts lower O2 solubility.

## Optimal protocol (best accuracy)

Goal: map the full DO band for the organism and validate DO_ss against a live probe trace.

Kit. An optical luminescent DO probe or sensor patch sized for the vial (optical is preferred here over Clark for a small stirred vial - it does not consume O2, is insensitive to the stirring hydrodynamics, and the patch form factor fits without displacing much liquid); a meter with temperature compensation; a means of setting and holding several DO levels (the electrolysis current via Gerrit's Law sets O2 input, and the CO2 sparge strips O2, so DO is set by the current/sparge combination); OD measurement for growth rate (Pioreactor OD, or offline OD600).

Calibration (do this before every run, it is the single largest error source).
1. Zero point: immerse the probe in a freshly made sodium sulphite (Na2SO3) solution, roughly 1 g or more per litre of deionised water, optionally with a trace of cobalt(II) chloride as catalyst. This scavenges all O2 to give a true 0 mg/L. Read after 2-3 min once stable. Make it fresh - it re-oxygenates from air within hours.
2. Span point: calibrate to air saturation in water-saturated air (probe held in moist air just above the water surface, no droplets on the membrane/patch), or in vigorously air-sparged water. Enter the local temperature and barometric pressure so the meter computes the correct air-saturation DO (for example about 7.5 mg/L at 30 degC, 1 atm; the meter applies its own water-vs-air correction factor, around 1.023).
3. Temperature and salinity compensation: set the meter to the run temperature (30 degC for C. necator) and, for amperometric probes, enter the medium salinity or conductivity. Optical probes are salt-independent for the reading but still need the temperature.

Band-mapping assays. Run the organism at a series of controlled DO setpoints spanning from near-zero up towards the suspected toxic ceiling - for C. necator something like 0.5, 1, 2, 2.5, 3, 4, 6, 9 and 11 mg/L - holding all else constant (temperature, CO2, H2 supply, OD start). At each setpoint, log OD over time and extract the specific growth rate (the slope of ln(OD) versus time in exponential phase). Plot growth rate against held DO. The resulting curve gives all four band points directly: minimum DO is where growth rate first becomes detectable / where the rising limb crosses a chosen threshold (for example 10 percent of maximum); optimum DO is the DO at peak growth rate; impairment DO is where growth rate has fallen by a defined margin past the peak (for example to 80-90 percent of maximum); toxic DO is where growth rate collapses towards zero. Use the same threshold definitions for every organism so the table is internally consistent, and record the definition alongside the values.

DO_ss validation. Separately, run one balanced growth experiment at the model's intended operating point (organism optimum DO as target, sparge schedule as the model recommends) and log the probe DO continuously through exponential growth. The mean exponential-phase surface DO is the measured DO_ss. Compare it to the model's predicted DO_ss (Mass Transfer D108). Agreement within the probe's accuracy validates the O2 balance; a large gap points to a wrong kLa, Faradaic efficiency, or uptake ratio upstream.

Replication. At least duplicate vials per DO setpoint, and a probe drift check (re-read the air-saturation point at the end of each run) so you can flag and discard drifted traces.

## Budget protocol (minimal kit)

Goal: get a defensible DO band and a sanity-check on DO_ss without the full setpoint sweep.

1. Seed the band from literature. For C. necator, enter optimum 2.6, impairment 3, toxic 11.5 mg/L as already in the table; the microaerophilic "hold below ~1.6 mg/L" guidance and the 0.30 atm inhibition figure support a low-DO optimum and a high-DO toxic ceiling. State a range rather than inventing a precise value where the literature only gives a range, and leave any value the literature does not support as a pink DATA GAP - do not back-fill it with a guess. For the other organisms (Xanthobacter spp., C. metallidurans, the UdG mix), keep the cells pink until a literature value or a measurement exists.
2. Spot DO checks with a low-cost optical probe. Calibrate against air saturation only (the single-point air span is adequate for field-grade work; the sodium-sulphite zero is the part you can skip on a budget, accepting reduced low-end accuracy). Take spot DO readings at a few points during a normal growth run rather than a continuous trace.
3. Cross-check DO_ss. Compare the spot readings during balanced exponential growth against the model's predicted DO_ss (Mass Transfer D108). Even a handful of spot readings clustered near the prediction is a useful validation; a consistent large offset is a flag to revisit kLa and the O2 balance.

The budget route gives you literature-seeded bands plus a coarse DO_ss check. It does not locate the minimum DO or resolve the optimum/impairment split for any organism - those stay literature-seeded or gaps until the optimal setpoint sweep is run.

## Result -> model

Write the four DO values per organism into the Biology HOB lookup table, rows 52-57, columns: minimum DO (B), optimum DO (C), impairment DO (D), toxic DO (E), all in mg/L. These feed DO_min, DO_opt, DO_impair, DO_toxic (Biology D45-D48), which propagate to the Mass Transfer tab's target DO fraction and the sparge schedule, and to the Summary DO-band readout.

Mark provenance using the workbook's existing value-font and KEY colour convention so a reader can tell measured from literature at a glance:
- A value you measured here (the setpoint-sweep band points, or a validated DO_ss): set it to the colour the KEY uses for verified/measured data, and cite this protocol plus the run in the Source/assumption column.
- A value seeded from literature (the current C. necator optimum/impairment/toxic, anything carried from a paper): set it to the literature-supported colour and cite the paper.
- A value still unknown (every "?" cell): leave it as the pink DATA GAP fill - do not type a placeholder number.

Record the threshold definitions you used for minimum / impairment (for example "minimum = 10 percent of max growth rate; impairment = growth rate down to 85 percent of max") in the Source/assumption column so later organisms are scored the same way. The measured DO_ss goes alongside the model's predicted DO_ss (Mass Transfer D108) as a validation note, not as an overwrite of the formula.

## Acceptance checks & pitfalls

- Calibrate every run. Probe drift, especially on amperometric Clark electrodes, is the dominant error. Re-read the air-saturation point at the end of each run; if it has moved more than the probe's stated accuracy, treat that run's DO as suspect.
- Fresh zero solution. Sodium sulphite re-oxygenates from air within hours - make it immediately before use, keep it covered, and confirm the reading reaches a stable near-zero before trusting the span.
- Temperature and salinity. A reading taken at the wrong compensation temperature is wrong by several percent per degree. Confirm the meter is set to 30 degC (C. necator) and, for amperometric probes, to the medium salinity; optical probes need the temperature but not the salinity.
- Probe O2 consumption. A Clark electrode consumes O2 and needs flow across the membrane; in a quiescent micro-volume it will read low. Either keep the stir bar running past the probe or prefer an optical probe in the small vial.
- Surface vs bulk DO. The model's DO_ss is a surface quantity; place the probe consistently (state the depth) and be aware that a sparged, stirred vial can have a DO gradient. Quote where the probe sat.
- Do not confuse the band with DO_ss. The band is an organism property mapped by varying DO; DO_ss is what the probe reads at one operating point. A single growth run gives you DO_ss, not the band - the band needs the setpoint sweep.
- Distinguish O2 limitation from H2 limitation. If growth slows at low DO, confirm it is the O2 and not dissolved H2 running out (the model flags an H2 saturation lag); otherwise you will misattribute the minimum-DO point.
- Ranges, not invented precision. Where literature gives a range, enter the range (or a clearly-flagged midpoint) and say so; never promote a range to a false precise figure in a measured-coloured cell.

## Sources

- Lab-scale cultivation of Cupriavidus necator on explosive gas mixtures (DO held below ~1.6 mg/L; microaerophilic operation): https://www.mdpi.com/2306-5354/9/5/204 and https://pmc.ncbi.nlm.nih.gov/articles/PMC9138072/
- Metabolic engineering of C. necator H16 under oxygen-limiting conditions (low-O2 growth vs PHB trade-off): https://www.sciencedirect.com/science/article/abs/pii/S1096717620300781
- BacDive strain record, C. necator H16 (Wilde / Schlegel H16 provenance for the 0.30 atm inhibition lineage): https://bacdive.dsmz.de/strain/2008
- Oxygen limitation and critical DO (specific growth rate becomes DO-dependent below a critical level): https://www.sciencedirect.com/topics/engineering/oxygen-limitation
- Critical-DO threshold methodology, chemostat DO bands (Penicillium chrysogenum example of staged DO thresholds): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9815084/
- DO sensor calibration, sodium-sulphite zero + air-saturation span: https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration
- US EPA QA bulletin, calibration of dissolved-oxygen meters: https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf
- Optical vs Clark electrode, face-to-face biosensor study (flow/salt independence, small-volume suitability): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
- Wolfbeis (2015), luminescent O2 sensing vs the Clark electrode (BioEssays): https://onlinelibrary.wiley.com/doi/10.1002/bies.201500002
