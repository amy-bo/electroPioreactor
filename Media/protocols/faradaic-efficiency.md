---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Faradaic efficiency (cathodic η_F, anodic η_F,OER)"
sources:
  - https://www.nature.com/articles/s41467-023-36880-8
  - https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
  - https://www.sciencedirect.com/topics/engineering/faradic-efficiency
  - https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
  - https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment)
  - https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987
  - https://www.science.org/doi/10.1126/sciadv.adi3180
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, electrochemistry, faradaic-efficiency, electrolysis]
---

# Faradaic efficiency (cathodic η_F, anodic η_F,OER)

## Apparatus note (separating cathode and anode gas)

Read this before the Kit and Method: the apparatus this protocol needs does not yet exist and is a design task for the team.

Measuring the cathodic and anodic Faradaic efficiencies *separately* requires the gas evolved at each electrode to be collected separately. The standard cell CANNOT do this. In the real cell both electrodes are two 6 mm rods passing through a single cap into one ~15–20 mL vial; the chamber is undivided and the gases mix by crossover. You cannot seal one collection tube over the cathode and a second over the anode in that geometry – there is no wall between them – so any "seal a tube over each electrode" instruction is physically impossible as written.

To collect each electrode's gas on its own you need a purpose-built rig. This rig is NOT yet finalised. Three realistic options, to be chosen and validated by the team:

- **(a) Internal gas-tight divider.** Put a separator or membrane between the two electrodes inside the cell, with its own gas-withdrawal port on each side. This is the cleanest split, but making the divider genuinely gas-tight around the rods and cap is non-trivial.
- **(b) Close-fitting shrouds / inverted funnels.** Fit a shroud or small inverted funnel over each electrode that channels only that electrode's gas to its own port. Only feasible if there is room around the two rods inside the vial.
- **(c) Two separate half-cells joined by a salt bridge or narrow channel.** Simplest to build, since each half-cell is a normal open vial. But the long inter-electrode path raises the ohmic drop and can bias how current distributes between the electrodes, so results from this geometry must be validated against a known cell before they are trusted.

Until one of these rigs exists, two things are still possible with the undivided vial: a **total-gas check against Faraday's law** (total charge in versus total gas out), and, going further, a **stirred initial-slope screen** (next section) that puts a bound on the *cathodic* loss in situ without any rig. Neither resolves the full cathode-versus-anode split, but the initial-slope screen does turn "we assume 1.0" into a measured bound on the cathodic crossover sink. The numbered Methods further below are written for the divided/shrouded test cell for when it is built; substitute whichever rig the team settles on.

## Interim method (undivided vial, no rig): stirred initial-slope screen

This is what you can do tonight, on the standard vial, with only the electrolysis drive and a gas burette. It bounds the cathodic Faradaic loss (model variable `etaF`) in the real, undivided geometry. It does **not** resolve the anodic efficiency (`etaF_OER`); that still needs one of the rigs above.

Why it works: strip the electrolyte of dissolved oxygen first and the cathode starts clean, so both electrodes run near-ideal and gas comes off at close to the Faradaic maximum (I/2F of H₂ plus I/4F of O₂, about 3I/4F in total). As the run proceeds, oxygen from the anode accumulates in the bulk, reaches the cathode, and is reduced there: the oxygen reduction reaction sits about 1.2 V positive of hydrogen evolution, so a cathode presented with dissolved oxygen reduces it in preference to splitting water. That reaction steals cathodic electrons from hydrogen and re-consumes oxygen that would otherwise escape, so the total-gas rate decays from its initial value to a lower steady plateau. The size of that drop is the crossover sink, in situ, in the geometry the culture actually runs in.

### Method (interim)

1. Work in a fume hood with forced ventilation, exclude all ignition sources, fit a flashback arrestor, do not fully seal the collection vessel, and vent the mixed off-gas immediately after reading. Set up the standard vial as normally operated, with the stirrer on and a gas burette or inverted graduated cylinder over the single headspace outlet.
2. Purge: sparge CO₂ hard for a few minutes to strip dissolved oxygen from the electrolyte and inert the headspace, then stop the sparge. Do **not** sparge during collection: the CO₂ volume is on the order of 50 times the knallgas, and its run-to-run jitter alone would bury the signal.
3. Start the electrolysis drive at about 10 mA (the upper operating current gives the largest gas signal and pushes the crossover into a detectable range), stirrer running, and start the clock.
4. Log the cumulative collected gas volume against time at short intervals (about every 30 to 60 s) for long enough to see the rate settle, typically 20 to 40 min. Equalise levels and subtract the water-vapour pressure when reading, as in the main method.
5. Re-purge and repeat for at least three runs.

### What the numbers mean

- Fit the cumulative curve to two slopes: the initial slope extrapolated back to t = 0 (dissolved oxygen still low, so near crossover-free) and the steady plateau slope (net operating rate, crossover included). The fractional drop from initial to plateau bounds the cathodic crossover loss, and hence 1 − `etaF`. Record both slopes; enter the resulting `etaF` estimate as the cathodic figure with a Comments note that it came from the initial-slope screen, not from an isolated-electrode collection (the tab's per-electrode charge-versus-volume formula assumes the latter).

### Scope and caveats (state these with the result)

- **Cathode only.** It bounds the cathodic sink; it says nothing about the anodic split, so leave `etaF_OER` at its rig-measured or default value.
- **Chloride corrupts it.** On a chloride-bearing electrolyte the anode also makes Cl₂, which is a gas, and at more gas-moles per electron than oxygen, so it rides along in the total volume and contaminates it. Run the screen on a chloride-free electrolyte, or treat the total as contaminated. After the Exp-2 chlorine review this is the live risk, not a hypothetical one.
- **It is a screen, not a precise efficiency.** At 10 mA the knallgas is only about 7 mL/hour and a burette reads to roughly ±5 %, while the crossover drop is itself only a few to about 15 %, set by stirring and electrode spacing. Read stirred (thin diffusion layer gives a larger and more operationally representative drop), fit the whole curve rather than eyeballing two points, and quote the result as a bound, not a three-significant-figure number.

## Optimal protocol

### Kit

Barrier equipment first.

- Gas chromatograph fitted with a thermal conductivity detector (TCD) and a fixed-volume sample loop, for species identification of the off-gas.
- Potentiostat or source-measure unit able to run galvanostatic (constant-current) mode and report the total charge passed in coulombs, with a continuous current log (e.g. BioLogic SP-150 or Keithley 2450).
- Fume hood with forced ventilation.
- Two calibrated gas-collection tubes (eudiometers or inverted gas burettes).
- Flashback arrestor for the gas line.
- Sweep-gas supply.
- Connecting tubing.
- Barometer.
- Thermometer for the electrolyte.
- The divided/shrouded test cell (see the apparatus note above).

### Reagents

- None. The calibration runs on the cell's normal operating electrolyte.

### Method

1. Work in a fume hood with forced ventilation. Exclude all ignition sources (sparks, hot surfaces) from the cell, the headspace and the collection vessels. Set up the divided/shrouded test cell (see apparatus note) as normally operated, with the stainless-steel cathode and the anode immersed in the electrolyte.
2. Confirm that the gas evolved at the cathode is channelled into one calibrated collection tube and the gas evolved at the anode into the second, with no path between them. Do NOT fully seal either collection tube against pressure build-up.
3. Connect the cell to the potentiostat or source-measure unit in galvanostatic mode. Set the drive current to the operating point (about 5.7 mA) or to a chosen calibration current within the validated range (about 3 to 30 mA).
4. Pre-condition the electrodes: run the cell at a set intensity for about 10 min before opening the collection window, consistent with the electrolysis current calibration. Faradaic efficiency depends on electrode history, so a fresh or freshly cleaned electrode must be conditioned before it is measured.
5. Start the continuous current log. If using the gas chromatograph, flow each electrode's off-gas through it and take samples from the fixed loop at recorded times – the cathode stream to identify and quantify the hydrogen, the anode stream to identify and quantify the oxygen.
6. Run the cell over a defined collection window, long enough to collect a comfortably readable gas volume (about one to three hours at 5.7 mA), keeping both electrode collections running over exactly the same window. Keep collected gas volumes small.
7. At the end of the window, for each collection tube, equalise the liquid levels inside and outside the tube so the trapped gas sits at ambient pressure, then read the collected gas volume against the graduations.
8. Read and note the electrolyte temperature and the barometric pressure at the moment of reading. Read the total charge passed from the instrument (in coulombs), and note the start and end times of the run.
9. Vent the collected H₂/O₂ mixture immediately after reading. Never store or compress it.
10. Repeat the collection window at least three times per electrode.
11. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H₂ or anode O₂), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

Barrier equipment first.

- A datalogging coulomb counter that reports accumulated charge in coulombs; or a precision (≤1 % tolerance) sense resistor (a few ohms) placed in series with the cell together with a datalogger (USB logger or microcontroller/ADC) set to integrate the current into charge.
- Fume hood with forced ventilation.
- A multimeter, to verify the logged current against a series reading at the start.
- Two inverted, water-filled graduated measuring cylinders.
- A water trough or reservoir.
- Flashback arrestor for the gas line.
- Barometer (a phone weather reading or local METAR is adequate for a coarse run).
- Thermometer for the electrolyte.

### Reagents

- None. The calibration runs on the cell's normal operating electrolyte.

### Method

1. Work in a fume hood with forced ventilation. Exclude all ignition sources (sparks, hot surfaces) from the cell, the headspace and the collection vessels. Set up the divided/shrouded test cell (see apparatus note) as normally operated, with the stainless-steel cathode and the anode immersed in the electrolyte.
2. Invert a water-filled graduated cylinder over the cathode side of the rig, and invert a second water-filled cylinder over the anode side, in the water trough. Do NOT fully seal either cylinder against pressure build-up.
3. Connect the datalogging coulomb counter (or the sense resistor and logger) in series with the cell so it records the charge passed. Confirm the logged current against a multimeter reading in series once at the start.
4. Set the drive current to the operating point (about 5.7 mA) or to a chosen calibration current within the validated range (about 3 to 30 mA).
5. Pre-condition the electrodes: run the cell at a set intensity for about 10 min before opening the collection window, consistent with the electrolysis current calibration. Efficiency depends on electrode history, so condition a fresh electrode before measuring it.
6. Start logging and run the cell over a defined collection window, long enough to collect a comfortably readable gas volume (about one to three hours at 5.7 mA), keeping both electrode collections running over exactly the same window. Keep collected gas volumes small.
7. At the end of the window, for each cylinder, equalise the water levels inside and outside the cylinder so the trapped gas sits at ambient pressure, then read the displaced-gas volume against the graduations.
8. Read and note the electrolyte temperature and the barometric pressure at the moment of reading. Read the total charge passed from the logger (in coulombs), and note the start and end times of the run.
9. Vent the collected H₂/O₂ mixture immediately after reading. Never store or compress it.
10. Repeat the collection window at least three times per electrode.
11. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H₂ or anode O₂), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Faradaic efficiency section of the Calibrations tab converts each recorded gas volume to moles using the ideal gas law from the gas temperature and pressure you entered, and divides that by the theoretical moles expected from the charge passed using Faraday's law. That ratio is the Faradaic efficiency for the run. The tab then averages the included runs for each reactor and feeds the cathodic efficiency (model variable `etaF`) and the anodic efficiency (model variable `etaF_OER`) into the model.

## Principle & background

Faradaic efficiency is the fraction of the charge passed through an electrode that goes to the reaction of interest, rather than to any competing reaction. For hydrogen at the cathode, η_F, the cathodic Faradaic efficiency, is n(H₂) measured / n(H₂) theoretical, and for oxygen at the anode, η_F,OER is n(O₂) measured / n(O₂) theoretical. The theoretical amount comes straight from Faraday's law applied to the charge actually delivered: the charge Q is the integral of the current over the run (in coulombs), and n_theoretical = Q / (z F), where F = 96485 C/mol and z is the electrons per molecule – z = 2 for hydrogen (2 H⁺ + 2 e⁻ gives H₂) and z = 4 for oxygen (2 H₂O gives O₂ + 4 H⁺ + 4 e⁻). The gas actually evolved is measured and its volume converted to moles with the ideal gas law, n = P V / (R T), at the measured temperature and pressure. Because the collected gas is water-saturated, the water vapour pressure at the measured temperature is subtracted from the total pressure first: n = (P_total − P_water) V / (R T). At 30 °C the water vapour pressure is a non-trivial fraction of the total, so this correction is significant. The whole method rests on two independent measurements – charge in and gas out – so accuracy is limited by whichever of the two is measured worst.

In this cell the cathode is the interesting case. The model currently assumes η_F = 1, which says every electron arriving at the stainless-steel cathode makes hydrogen. In a single-chamber, undivided, oxygen-rich cell that is optimistic: dissolved oxygen produced at the anode can diffuse to the cathode and be reduced there (the oxygen reduction reaction, ORR), consuming cathodic current that would otherwise make hydrogen. That pulls η_F below 1. Because the model derives the net oxygen reaching the dissolved pool as the anodic oxygen minus this cathodic ORR sink, a measured η_F below 1 directly lowers every downstream oxygen figure: the net oxygen generation, the oxygen surplus, the steady-state dissolved oxygen, and the sparge interval all move from their current upper-bound values toward realistic numbers. Measuring η_F replaces an assumed upper bound with a real number.

The gas chromatograph is the reference route for the numerator because it identifies the species, so it separates real hydrogen from any air ingress or oxygen carry-over, which a bare volume reading cannot do. With a sweep-gas flow and a calibrated instrument it yields a molar production rate directly, which can be integrated over the same window as the charge. The eudiometer and water-displacement routes are simpler and measure volume only; they are cleaner for the cathodic hydrogen figure than for the anodic oxygen figure.

Several pitfalls bias the result and should be checked. Charge-balance sanity: at low oxygen and a clean cathode the cathodic η_F should sit close to 1; a value far above 1 means the charge is under-counted (check the current log or sense resistor) or the gas volume is over-read (air ingress, a leak, or un-equalised levels), while a value below 1 is the expected, interesting result here – the ORR sink showing up. Level equalisation and the water-vapour correction are the two most common volumetric errors; reading the trapped gas before equalising, or omitting the vapour-pressure subtraction, both bias the moles and hence η_F. Undivided-cell crossover: if the split cannot be enforced by the rig (see the apparatus note), the evolved gases mix and some hydrogen and oxygen can recombine or be re-consumed before capture, making the captured volume under-read true production and biasing η_F low for reasons unrelated to ORR; a genuine per-electrode split is the whole reason the divided/shrouded rig is required, and where mixing cannot be excluded a low cathodic η_F should be treated as an upper estimate of the ORR sink alone. The oxygen measurement is confounded by the cathodic sink: the measured η_F,OER is the gross oxygen leaving the anode, whereas the model needs the net oxygen reaching the dissolved pool, so η_F,OER should be interpreted as the anodic source term only and the model combines it with the cathodic η_F to obtain net oxygen; measuring net dissolved oxygen directly is a separate experiment (a dissolved-oxygen probe under the same drive). Finally, Faradaic efficiency can depend on current density, temperature, electrolyte, and electrode history – which is why the electrodes are pre-conditioned and each figure is the average of at least three runs – so the operating current, temperature, pressure, run duration, and electrode materials should always be recorded with the result, noting whether η_F was measured at the 5.7 mA operating point or at an elevated calibration current.

Safety: hydrogen and oxygen evolved together in one chamber form a flammable mixture – a hydrogen stream above roughly 6 per cent oxygen, or an oxygen stream above roughly 4 per cent hydrogen, is in the explosive range. This protocol collects mixed H₂/O₂ over water for one to three hours in an undivided, crossover-prone geometry, which is a detonation geometry, so the safety controls belong in the Method and not only here: work in a fume hood with forced ventilation, fit a flashback arrestor on any gas line, exclude all ignition sources, do not fully seal the collection tube against pressure build-up, keep collected gas volumes small, and vent the mixed off-gas immediately after each reading rather than storing or compressing it.

## Sources

- Reliable reporting of Faradaic efficiencies for electrocatalysis research, Nature Communications (2023): https://www.nature.com/articles/s41467-023-36880-8
- A Guideline to Determine Faradaic Efficiency in Electrochemical CO2 Reduction, ACS Energy Letters (2024): https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
- Faradaic Efficiency - an overview, ScienceDirect Topics: https://www.sciencedirect.com/topics/engineering/faradic-efficiency
- Eudiometer / molar volume of a gas, vapour-pressure and level-equalisation corrections (De Anza College lab B1): https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
- Experimental Determination of the Gas Constant (water-displacement gas collection, ideal gas law), Chemistry LibreTexts: https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment)
- Membrane-free water electrolysis - gas crossover, O2-to-cathode current loss and the H2/O2 explosive range, Angewandte Chemie / Science Advances: https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987 and https://www.science.org/doi/10.1126/sciadv.adi3180
- ORR on stainless steel cathodes (oxygen reduction at SS surfaces): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
