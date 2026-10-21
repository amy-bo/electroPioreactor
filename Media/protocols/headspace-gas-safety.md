---
state: authored
author: [claude-sonnet-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "Headspace H2/O2 composition during lag phase: flammability check before any unattended run"
sources:
  - https://en.wikipedia.org/wiki/Limiting_oxygen_concentration
  - https://www.fire.tc.faa.gov/2013Conference/files/General_Systems_Fire/RehnHydrogen/RehnHydrogenPres.pdf
  - https://careers.kiwa.com/globalassets/netherlands/kiwa-technology/downloads/igrc2024-the-lower-flammability-limit-of-hydrogen-oral-presentation-bart-vogelzang.pdf
  - https://gcms.cz/labrulez-bucket-strapi-h3hsga3/paper/5991-3199EN.pdf
  - https://hiq.linde-gas.com/en/analytical_methods/gas_chromatography/thermal_conductivity_detector
  - https://ohsonline.com/articles/2004/05/accurate-measurement-of-flammable-gases.aspx
  - https://sensidyne.com/wp-content/uploads/2024/03/Hydrogen-Catalytic-Bead-100percent-LEL-sensor-specs_823-0211-33rD.pdf
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, safety, hydrogen, flammability, headspace]
---

# Headspace H2/O2 composition (lag-phase flammability check)

Measures the real gas mixture in the headspace while electrolysis runs with no cells (or with cells not yet consuming H2), and compares it with the model. **Must be done before any unattended run from inoculation.** Do the [headspace vent characterisation](headspace-vent.md) first: if this check disagrees with the model, the vent model is the first suspect.

## Safety, read before starting

- Hydrogen in air is flammable from a lower flammability limit (LFL) of about 4 % by volume; published values vary a little by source (the FAA has cited 4.7 %). Treat 4 % as the working figure.
- A nominal hydrogen LOC is about 5 % O2 with nitrogen dilution (the cited secondary table gives 5.2 % with CO2). These and the air LFL are conservative hazard-screen references, not a complete classification of H2/O2/CO2/N2 mixtures. Owner verification of applicable mixture limits and margins against appropriate primary guidance, including current NFPA 69, is a prerequisite to accepting conditions. Below either quoted threshold does not establish safety.
- Read Summary D51 (lag O2) and D52 (mean lag H2) with the recorded selections. Treat the headspace as potentially flammable; neither predictions nor this screen certify safety.
- No ignition sources: no naked flames, no sparking switches or hot plates near the vial or the vent outlet, no static (earth yourself, avoid synthetic clothing when handling), and no mobile phones in use at the vent. Use only instruments rated for the gas they sample.
- Work in a fume hood or ventilated cabinet and vent the outlet into the extraction. Keep the cap and ports closed except for sampling.
- Switch **electrolysis OFF** before opening the cap or a port to room air, before moving the vial, and before any syringe operation not covered by the validated sampling procedure. Closed-septum sampling under current is permitted only if that procedure explicitly covers it. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance.
- Keep volumes small. Take no more than 1 mL per sample and do not pool or store samples; analyse within minutes. Do not store hydrogen-containing gas in sealed vessels.
- Wear safety glasses. Tell a colleague you are working and keep the run supervised throughout.
- If any reading exceeds the LFL at the vent outlet or in the room, stop electrolysis, keep ventilation running, and step away until it clears.

## Before you start

- The vial exactly as it will run: about 15 mL medium, the real vent fitted (the vent used in the vent protocol), cap leaks fixed, ed04, MMO tube assembly, chloride-free AMYBO03 at 30 °C, recorded operating power and the schedule read from Summary D21/D22. Record the *Xanthobacter tagetidis* selection even though there are no cells. No cells (lag source).
- Prerequisite: validate sampling apparatus for mixture response, range, recovery, dead volume and disturbance. Demonstrate that withdrawals, syringe flushes and pump flow do not materially alter pressure, induce air ingress or shift composition; otherwise report vent readings only or use a separately validated arrangement.
- Run the full schedule for at least 1 hour before sampling and establish a repeating cycle.
- Know the model values before you start: Summary D52 (mean H2), Summary D51 (O2), Summary D50 (growth-phase O2).

## Optimal protocol

### Kit

- A GC with a thermal conductivity detector (GC-TCD) set up for H2, O2, N2 and CO2. H2 is normally run with argon carrier on a TCD (helium is usually unsuitable for H2, and argon lowers the sensitivity of the other permanent gases, so calibrate each gas separately). A molecular-sieve column separates H2, O2 and N2; CO2 needs a column that retains it (a porous-polymer column, or a two-column set) or is read separately.
- A gastight syringe, 0.5 to 1 mL, with a valve or a side-port needle, checked for leaks.
- A calibration gas mixture of H2, O2, N2 and CO2 bracketing the expected values (for example 5 % and 20 % H2 in a balance of CO2 and N2 with 5 to 10 % O2), or separate certified standards.
- A timer, and a note sheet.
- Septum or a Luer sampling port on the vial headspace.

### Reagents

- The medium in use; certified calibration gas; GC carrier gas (argon).

### Method

1. Calibrate the GC with the standard mixture, with three injections of the same volume you will sample, and check the response is reproducible to within 5 %.
2. Run the vial at its full schedule for at least 1 hour. Note the exact time of each CO2 pulse.
3. Sample A, end of interval: starting about 30 s before the next pulse, take 0.5 mL of headspace gas through the septum port with the gastight syringe. Rinse is not possible, so discard the first draw if the syringe was open to air; flush the syringe once with headspace gas and take a second draw. Record the time since the last pulse.
4. Inject at once into the GC. Record H2, O2, N2 and CO2 as percentages.
5. Wait for the next pulse and the full interval. Sample B, mid-interval: at 0.5 × Summary D22 minutes after the pulse, repeat steps 3 and 4.
6. Repeat sample A and sample B for at least 3 intervals, switching electrolysis off while you change the syringe only if the port is open to air; closed-septum sampling under current is allowed only by the validated sampling procedure above.
7. If you want the dilution by air from the sampling itself checked, inject a CO2 blank drawn the same way and read N2 and O2. A large air signal means the syringe or the port is leaking; discard and re-do.
8. Report sample A (end-of-interval) and B (mid-interval) means and spreads separately. Their average is not the time mean of a nonlinear cycle. For a model cycle-mean comparison, obtain a validated trace or sufficient phase samples for a time-weighted integral over complete settled cycles and report integration uncertainty.
9. Compare with the model (below). Then switch electrolysis off. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance.

## Budget protocol

No GC. A portable H2 meter or combustible-gas detector at the vent outlet. Gives H2 and a flammable-gas reading, not O2 and CO2 as well.

### Kit

- A portable hydrogen meter, or a combustible-gas detector that is calibrated for hydrogen. Two types are common. Catalytic bead sensors read 0 to 100 % of the LFL, need oxygen to work (one H2 bead sensor specifies at least 10 % O2 by volume), and can read low or zero in a rich mixture above the upper limit. Thermal-conductivity sensors do not need oxygen and read up to 100 % by volume but must be calibrated for the specific gas, and CO2 in the mix affects them. Neither suits a pure CO2 and H2 headspace without checking: read the meter's manual for oxygen and CO2 limits.
- An O2 meter (optional) for headspace O2.
- A short tube from the vent outlet to the meter inlet, and a gas-sample bag or a gastight syringe if the meter needs a sampling line.
- Timer.

### Reagents

- The medium in use. A hydrogen span gas if the meter can be field-checked (a certified bottle at a known concentration).

### Method

1. Check the meter against its span gas or its stated bump-test procedure, in the fume hood, and zero it in clean air.
2. Run the vial at its full schedule for at least 1 hour. The vent outlet must lead out into the extraction.
3. Place the meter inlet at the vent outlet, not in the vial. Even the lowest pump flow can induce air ingress or change pressure. Demonstrated non-perturbing sampling is a prerequisite to treating the result as headspace composition; otherwise label results as vent readings only.
4. Record the H2 reading (or % LFL, converting with 4 % = 100 % LFL) every 30 s through at least 3 full intervals. Mark every pulse time on the log.
5. Record end-of-interval and mid-interval vent readings separately with their times. A pumped vent trace need not peak at the expected phase. Only after sampling validation may a time-weighted mean over complete cycles be compared with the model headspace mean.
6. For over-range readings, implausible zeros or an unvalidated oxygen/CO2 matrix, stop interpreting the meter and use a suitable validated analyser or the optimal route. Do not add air to an unknown hydrogen-rich sample: this can create a flammable mixture and multiplication cannot repair oxygen dependence or CO2 interference.
7. Switch electrolysis off. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance.

## What the spreadsheet does with it

The model predicts the lag-phase headspace from a well-mixed balance depending on the vent model: Summary D50–D52 are flux-weighted (mean-field) fractions, the composition of the gas leaving through the vent; the time means of the sawtooth are Mass Transfer D564 (lag H2), D360 (lag O2) and D338 (growth O2), and the pre-pulse tops D388 (lag H2) and D358 (lag O2). Read them with the recorded configuration and schedule. Its LFL/LOC comparison is a hazard screen, not certification. No Calibrations entry is made: record phase-specific measurements, validated time-weighted means if available, uncertainties and sampling limitations in the lab record against the headspace TODO.

### What to compare, and what counts as agreement

- Compare like with like. A time-weighted mean over complete cycles (a headspace or vent probe logged at a fixed rate) compares with the time means: H2 with Mass Transfer D564, O2 with D360 (lag) or D338 (growth). A flow-weighted vent sample (gas collected in proportion to the vent flow) compares with Summary D52, D51 and D50. The two differ by tens of per cent at long intervals, without any fault in the vent.
- +/-30 % is only a provisional model-comparison screen, not an equivalence or safety margin. Owner-approved equivalence margins and measurement uncertainty are prerequisites for declaring agreement.
- Outside +/-30 %: investigate sampling and analyser uncertainty as well as the balance; the vent model is one suspect. Do [headspace-vent.md](headspace-vent.md) first and update Summary D11, then re-compare.
- Whatever the model says, H2 above 4 % together with O2 above about 5 % flags a potential flammability hazard and excludes unattended operation pending owner review. Below either reference does not establish safety: applicable mixture limits and margins must be verified.

### Proposed remedies after a hazard flag

The model's remedy is to sparge CO2 more often, or to add N2. Be aware that more CO2 pulses push the pH below the band (Summary D93 (chk_DO_pH) reads NO for CO2 alone doing all three jobs); the owner prefers to fix the medium instead (Summary rows 64–69). N2 is modelled by its mean flow (Summary D14, Mass Transfer D424–D425), as timed pulses apart from the CO2 pulses; Summary D56 (res_N2_H2) gives the mean N2 that keeps the lag H2 below the LFL. A separate N2 flush in the sawtooth is still a model improvement, and any N2 schedule must be confirmed on the bench rather than taken from the spreadsheet.

## Principle and background

Electrolysis makes H2 at the cathode and O2 at the anode; the headspace receives both, and the CO2 pulse dilutes them. With no cells consuming H2, H2 builds up between pulses and is flushed at each pulse, so the headspace swings between a low value just after a pulse and a high value just before the next. That is why one sample is not enough: the check needs the peak (end of interval) and a mid-interval value, and the mean sets the comparison with the model.

A GC with a TCD is the usual route for permanent gases (H2, O2, N2, CO2), since a flame detector cannot see them. Catalytic bead sensors detect H2 by burning it on a heated bead and therefore need oxygen; thermal-conductivity sensors work on the high thermal conductivity of H2 and can read up to 100 % by volume but need calibrating for the specific gas.

## Sources

- Hydrogen LOC about 5 vol % O2 with nitrogen dilution (5.2 with CO2): [Wikipedia – Limiting oxygen concentration](https://en.wikipedia.org/wiki/Limiting_oxygen_concentration). The NFPA 69 margin rule itself was not verified; check the standard.
- Hydrogen LFL, about 4 vol %, and the FAA 4.7 % figure: [FAA – Rehn, hydrogen flammability presentation](https://www.fire.tc.faa.gov/2013Conference/files/General_Systems_Fire/RehnHydrogen/RehnHydrogenPres.pdf); [Kiwa – The lower flammability limit of hydrogen](https://careers.kiwa.com/globalassets/netherlands/kiwa-technology/downloads/igrc2024-the-lower-flammability-limit-of-hydrogen-oral-presentation-bart-vogelzang.pdf).
- GC-TCD for permanent gases and hydrogen with argon carrier: [Agilent application note 5991-3199EN](https://gcms.cz/labrulez-bucket-strapi-h3hsga3/paper/5991-3199EN.pdf); [Linde – Thermal conductivity detector](https://hiq.linde-gas.com/en/analytical_methods/gas_chromatography/thermal_conductivity_detector).
- Catalytic bead versus thermal-conductivity flammable-gas sensors: [OH&S – Accurate measurement of flammable gases](https://ohsonline.com/articles/2004/05/accurate-measurement-of-flammable-gases.aspx); [Sensidyne – Hydrogen catalytic bead sensor specification](https://sensidyne.com/wp-content/uploads/2024/03/Hydrogen-Catalytic-Bead-100percent-LEL-sensor-specs_823-0211-33rD.pdf).
