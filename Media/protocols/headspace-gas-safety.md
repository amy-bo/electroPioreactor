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
- Hydrogen in nitrogen-diluted air cannot burn below a limiting oxygen concentration (LOC) of about 5 % O2 by volume (Wikipedia's table lists 5 vol % with nitrogen dilution and 5.2 vol % with CO2 dilution). The model's headspace sits at roughly 6.5 % O2 in lag, so it is only a little above this, which is why the check matters. Confirm the safety margin you apply against the current NFPA 69 text; secondary sources disagree on the rule, so do not rely on them.
- The model's lag-phase headspace (about 11.5 % H2 mean, about 17 % just before each pulse, about 6.5 % O2) is predicted to be above the LFL. Treat the headspace as **flammable until measured otherwise**.
- No ignition sources: no naked flames, no sparking switches or hot plates near the vial or the vent outlet, no static (earth yourself, avoid synthetic clothing when handling), and no mobile phones in use at the vent. Use only instruments rated for the gas they sample.
- Work in a fume hood or ventilated cabinet and vent the outlet into the extraction. Keep the cap and ports closed except for sampling.
- Switch **electrolysis OFF** before opening anything, before changing syringes at a port, and before moving the vial. Wait at least 2 pulse intervals (or flush with CO2) before opening the cap.
- Keep volumes small. Take no more than 1 mL per sample and do not pool or store samples; analyse within minutes. Do not store hydrogen-containing gas in sealed vessels.
- Wear safety glasses. Tell a colleague you are working and keep the run supervised throughout.
- If any reading exceeds the LFL at the vent outlet or in the room, stop electrolysis, keep ventilation running, and step away until it clears.

## Before you start

- The vial exactly as it will run: about 15 mL medium, the real vent fitted (the vent used in the vent protocol), cap leaks fixed, the operating electrolysis power and the operating pulse schedule (0.67 s every about 9 min unless changed). No cells (lag source).
- Run the full schedule for at least 1 hour before sampling, so the headspace reaches its repeating cycle.
- Know the model values before you start: Summary D126 (mean H2), Summary D125 (O2), Summary D124 (growth-phase O2, about 4 %).

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
5. Wait for the next pulse and the full interval. Sample B, mid-interval: about 4 to 5 minutes after the pulse, repeat steps 3 and 4.
6. Repeat sample A and sample B for at least 3 intervals, switching electrolysis off while you change the syringe only if the port is open to air; a closed septum sample does not need it.
7. If you want the dilution by air from the sampling itself checked, inject a CO2 blank drawn the same way and read N2 and O2. A large air signal means the syringe or the port is leaking; discard and re-do.
8. Compute the mean of the sample A values and the mean of the sample B values, and the average of all samples as the "mean" headspace.
9. Compare with the model (below). Then switch electrolysis off and let the vial sit for 2 intervals before any handling.

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
3. Place the meter inlet at the vent outlet, not in the vial. Draw sample gas through a short tube at the lowest flow the meter allows; a high draw dilutes the sample with room air.
4. Record the H2 reading (or % LFL, converting with 4 % = 100 % LFL) every 30 s through at least 3 full intervals. Mark every pulse time on the log.
5. The peak reading just before each pulse is the end-of-interval value (sample A). The reading mid-interval is sample B. Take the mean of the readings across the interval as the mean headspace.
6. If the meter reads over-range or zero in an obviously rich mixture, do not trust it: dilute a known volume of vent gas with a known volume of air in a gas-sample bag, re-read, and multiply back, or move to the optimal route.
7. Switch electrolysis off, flush with CO2, and let the vial sit for 2 intervals before any handling.

## What the spreadsheet does with it

The model predicts the lag-phase headspace from a single well-mixed balance that depends on the vent model: mean H2 (Summary D126, about 11.5 %), O2 (Summary D125, about 6.5 %), and, for growth phase, O2 (Summary D124, about 4 %). It compares the lag-phase mix against the H2 LFL and the O2 LOC with an NFPA 69 margin and returns a verdict with a remedy. The result is not entered in a Calibrations section; it is a **validation** of those cells. Record the measured mean, the end-of-interval and mid-interval values, the date and the researcher in the lab record, and note it against the TODO item "Headspace H2/O2 during lag before any unattended run".

### What to compare, and what counts as agreement

- Compare your measured mean H2 with Summary D126, measured O2 with Summary D125 (lag), and, if you run the growth-phase case, O2 with Summary D124.
- Within +/-30 % of the model's mean is consistent. (For example, 11.5 % predicted is consistent with 8 to 15 %.)
- Outside +/-30 %: the headspace balance is wrong, and the first suspect is the vent model. Do [headspace-vent.md](headspace-vent.md) first and update Summary D111, then re-compare.
- Whatever the model says, **act on the measurement**: if the measured H2 at any time exceeds 4 % while O2 exceeds about 5 %, the headspace is flammable and the run must not be left unattended.

### Remedy if flammable

The model's remedy is to sparge CO2 more often, or to add a small N2 sweep to the headspace. Be aware that more CO2 pulses push the pH below the band (Summary D128 reads NO for CO2 alone doing all three jobs). An N2 sweep addition (about 1 mL/min was proposed in the TODO) is **not yet modelled** and is a TODO in the model; it must be measured on the bench rather than taken from the spreadsheet.

## Principle and background

Electrolysis makes H2 at the cathode and O2 at the anode; the headspace receives both, and the CO2 pulse dilutes them. With no cells consuming H2, H2 builds up between pulses and is flushed at each pulse, so the headspace swings between a low value just after a pulse and a high value just before the next. That is why one sample is not enough: the check needs the peak (end of interval) and a mid-interval value, and the mean sets the comparison with the model.

A GC with a TCD is the usual route for permanent gases (H2, O2, N2, CO2), since a flame detector cannot see them. Catalytic bead sensors detect H2 by burning it on a heated bead and therefore need oxygen; thermal-conductivity sensors work on the high thermal conductivity of H2 and can read up to 100 % by volume but need calibrating for the specific gas.

## Sources

- Hydrogen LOC about 5 vol % O2 with nitrogen dilution (5.2 with CO2): [Wikipedia – Limiting oxygen concentration](https://en.wikipedia.org/wiki/Limiting_oxygen_concentration). The NFPA 69 margin rule itself was not verified; check the standard.
- Hydrogen LFL, about 4 vol %, and the FAA 4.7 % figure: [FAA – Rehn, hydrogen flammability presentation](https://www.fire.tc.faa.gov/2013Conference/files/General_Systems_Fire/RehnHydrogen/RehnHydrogenPres.pdf); [Kiwa – The lower flammability limit of hydrogen](https://careers.kiwa.com/globalassets/netherlands/kiwa-technology/downloads/igrc2024-the-lower-flammability-limit-of-hydrogen-oral-presentation-bart-vogelzang.pdf).
- GC-TCD for permanent gases and hydrogen with argon carrier: [Agilent application note 5991-3199EN](https://gcms.cz/labrulez-bucket-strapi-h3hsga3/paper/5991-3199EN.pdf); [Linde – Thermal conductivity detector](https://hiq.linde-gas.com/en/analytical_methods/gas_chromatography/thermal_conductivity_detector).
- Catalytic bead versus thermal-conductivity flammable-gas sensors: [OH&S – Accurate measurement of flammable gases](https://ohsonline.com/articles/2004/05/accurate-measurement-of-flammable-gases.aspx); [Sensidyne – Hydrogen catalytic bead sensor specification](https://sensidyne.com/wp-content/uploads/2024/03/Hydrogen-Catalytic-Bead-100percent-LEL-sensor-specs_823-0211-33rD.pdf).
