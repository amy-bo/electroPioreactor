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

The apparatus this protocol needs does not yet exist and is a design task for the team.

Measuring cathodic and anodic Faradaic efficiencies *separately* requires species-specific gas recovery from each electrode. The current baseline is ed04 with the MMO tube assembly, chloride-free AM003, the Xanthobacter tagetidis model selection and 30 °C; record the actual assembly and operating inputs. The standard undivided vial mixes gases and does not itself provide separate collection. Geometry alone does not prove shrouds impossible: room, sealing, recovery and crossover must be assessed and validated.

To collect each electrode's gas on its own you need a purpose-built rig. This rig is NOT yet finalised. Three realistic options, to be chosen and validated by the team:

- **(a) Internal gas-tight divider.** Put a separator or membrane between the two electrodes inside the cell, with its own gas-withdrawal port on each side. This is the cleanest split, but making the divider genuinely gas-tight around the assembly and cap is non-trivial.
- **(b) Close-fitting shrouds / inverted funnels.** Fit a shroud or small inverted funnel over each electrode that channels only that electrode's gas to its own port. Only feasible if there is room around the actual MMO tube assembly inside the vial.
- **(c) Two separate half-cells joined by a salt bridge or narrow channel.** Simplest to build, since each half-cell is a normal open vial. But the long inter-electrode path raises the ohmic drop and can bias how current distributes between the electrodes, so results from this geometry must be validated against a known cell before they are trusted.

Until one of these rigs exists and is validated, the undivided vial can provide a total-gas check against charge and an initial-to-plateau mixed-gas screen. Neither resolves the cathodic/anodic split or gives an isolated-electrode efficiency. Rig selection, validated species recovery and crossover control are prerequisites for the numbered per-electrode methods below.

## Interim method (undivided vial, no rig): stirred initial-slope screen

This proposed undivided-vial screen records mixed-gas behaviour only. It cannot determine or bound cathodic `etaF` without a separately supported species balance, and cannot determine `etaF_OER`. Approved gas handling and clearance and validated collection are prerequisites before execution.

Interpretation: oxygen reduction (ORR) can both divert cathodic electrons from hydrogen production and consume anode-derived oxygen; hydrogen oxidation (HOR), gas dissolution, collection recovery and other side reactions can also change the total-gas slope. A declining slope therefore screens mixed-gas behaviour, not an isolated cathodic loss. Even idealised pure ORR does not make the fractional total-gas drop equal to 1 − etaF.

### Method (interim)

1. Work in a fume hood with forced ventilation, exclude all ignition sources, fit a flashback arrestor, do not fully seal the collection vessel, and vent the mixed off-gas immediately after reading. Set up the standard vial as normally operated, with the stirrer on and a gas burette or inverted graduated cylinder over the single headspace outlet.
2. Establish a documented low-DO start using a validated preparation and gas-handling arrangement approved by the owner; routine CO₂ pulses or a timed flush do not demonstrate inerting. Stop the preparation flow before collection and account for residual CO₂ and dissolution; continued CO₂ flow can obscure the electrolysis gas signal.
3. Start electrolysis at the recorded operating power within 3–10 % and log actual current, stirring and time. Runtime clamps at 10 %; no historical high-power diagnostic authorises bypassing it.
4. Log the cumulative collected gas volume against time at short intervals (about every 30 to 60 s) for long enough to see the rate settle, typically 20 to 40 min. Equalise levels and subtract the water-vapour pressure when reading, as in the main method.
5. Re-purge and repeat for at least three runs.

### What the numbers mean

- Fit and record the initial and plateau cumulative-gas slopes, current, collection conditions and uncertainties in notes only. Keep the fractional drop as a mixed-gas screen; do not enter it or 1 minus it as `etaF` in Calibrations. ORR and HOR contributions and recovery are unresolved, and even pure ORR does not justify that conversion.

### Scope and caveats (state these with the result)

- **Mixed gas only.** Neither electrode efficiency is isolated; leave both calibration entries unchanged pending validated per-electrode collection.
- **Chloride corrupts it.** On a chloride-bearing electrolyte the anode also makes Cl₂, which is a gas, and at more gas-moles per electron than oxygen, so it rides along in the total volume and contaminates it. Run the screen on a chloride-free electrolyte, or treat the total as contaminated. After the Exp-2 chlorine review this is the live risk, not a hypothetical one.
- **It is a mixed-gas screen.** Fit the curve and report slope uncertainty and recovery limitations. Do not report a cathodic efficiency or bound from total volume alone.

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

1. Work in a fume hood with forced ventilation. Exclude all ignition sources (sparks, hot surfaces) from the cell, the headspace and the collection vessels. Set up the divided/shrouded test cell (see apparatus note) as normally operated, with the recorded MMO tube assembly and electrolyte, documenting any rig-related changes from the operating cell.
2. Confirm that the gas evolved at the cathode is channelled into one calibrated collection tube and the gas evolved at the anode into the second, with no path between them. Do NOT fully seal either collection tube against pressure build-up.
3. Connect the cell to the potentiostat or source-measure unit in galvanostatic mode. Set the drive current to the measured operating current corresponding to the recorded 3–10 % power input, or a rig-authorised calibration current with its transferability to operation documented.
4. Pre-condition the electrodes: run the cell at a set intensity for about 10 min before opening the collection window, consistent with the electrolysis current calibration. Faradaic efficiency depends on electrode history, so a fresh or freshly cleaned electrode must be conditioned before it is measured.
5. Start the continuous current log. If using the gas chromatograph, flow each electrode's off-gas through it and take samples from the fixed loop at recorded times – the cathode stream to identify and quantify the hydrogen, the anode stream to identify and quantify the oxygen.
6. Run the cell over a defined collection window, long enough to collect a comfortably readable gas volume (choose the duration from the measured current and validated collection resolution), keeping both electrode collections running over exactly the same window. Keep collected gas volumes small.
7. At the end of the window, for each collection tube, equalise the liquid levels inside and outside the tube so the trapped gas sits at ambient pressure, then read the collected gas volume against the graduations.
8. Read and note the electrolyte temperature and the barometric pressure at the moment of reading. Read the total charge passed from the instrument (in coulombs), and note the start and end times of the run.
9. Vent each separately collected electrode stream through the approved gas-handling arrangement after reading. Never store or compress it; mixed streams invalidate the per-electrode measurement.
10. Repeat the collection window at least three times per electrode.
11. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H₂ or anode O₂), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; leave Include blank or n until collection recovery, species balance and transferability to the undivided operating cell are established. Set y only for accepted results that support the workbook’s ORR interpretation; otherwise retain the excluded measurement. Leave the Computed, Type and value-in-use cells to the spreadsheet.

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

1. Work in a fume hood with forced ventilation. Exclude all ignition sources (sparks, hot surfaces) from the cell, the headspace and the collection vessels. Set up the divided/shrouded test cell (see apparatus note) as normally operated, with the recorded MMO tube assembly and electrolyte, documenting any rig-related changes from the operating cell.
2. Invert a water-filled graduated cylinder over the cathode side of the rig, and invert a second water-filled cylinder over the anode side, in the water trough. Do NOT fully seal either cylinder against pressure build-up.
3. Connect the datalogging coulomb counter (or the sense resistor and logger) in series with the cell so it records the charge passed. Confirm the logged current against a multimeter reading in series once at the start.
4. Set the drive current to the measured operating current corresponding to the recorded 3–10 % power input, or a rig-authorised calibration current with its transferability to operation documented.
5. Pre-condition the electrodes: run the cell at a set intensity for about 10 min before opening the collection window, consistent with the electrolysis current calibration. Efficiency depends on electrode history, so condition a fresh electrode before measuring it.
6. Start logging and run the cell over a defined collection window, long enough to collect a comfortably readable gas volume (choose the duration from the measured current and validated collection resolution), keeping both electrode collections running over exactly the same window. Keep collected gas volumes small.
7. At the end of the window, for each cylinder, equalise the water levels inside and outside the cylinder so the trapped gas sits at ambient pressure, then read the displaced-gas volume against the graduations.
8. Read and note the electrolyte temperature and the barometric pressure at the moment of reading. Read the total charge passed from the logger (in coulombs), and note the start and end times of the run.
9. Vent each separately collected electrode stream through the approved gas-handling arrangement after reading. Never store or compress it; mixed streams invalidate the per-electrode measurement.
10. Repeat the collection window at least three times per electrode.
11. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H₂ or anode O₂), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; leave Include blank or n until collection recovery, species balance and transferability to the undivided operating cell are established. Set y only for accepted results that support the workbook’s ORR interpretation; otherwise retain the excluded measurement. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Faradaic efficiency section of the Calibrations tab converts each recorded gas volume to moles using the ideal gas law from the gas temperature and pressure you entered, and divides that by the theoretical moles expected from the charge passed using Faraday's law. That ratio is the Faradaic efficiency for the run. Before including a divided-cell result, demonstrate that its efficiency transfers to the undivided reactor: separation changes oxygen crossover. Otherwise retain it as a rig-characterisation result, excluded from operating calibration. The tab then averages the included runs for each reactor and feeds the cathodic efficiency (model variable `etaF`) and the anodic efficiency (model variable `etaF_OER`) into the model.

## Principle & background

Faradaic efficiency is the fraction of the charge passed through an electrode that goes to the reaction of interest, rather than to any competing reaction. For hydrogen at the cathode, η_F, the cathodic Faradaic efficiency, is n(H₂) measured / n(H₂) theoretical, and for oxygen at the anode, η_F,OER is n(O₂) measured / n(O₂) theoretical. The theoretical amount comes straight from Faraday's law applied to the charge actually delivered: the charge Q is the integral of the current over the run (in coulombs), and n_theoretical = Q / (z F), where F = 96485 C/mol and z is the electrons per molecule – z = 2 for hydrogen (2 H⁺ + 2 e⁻ gives H₂) and z = 4 for oxygen (2 H₂O gives O₂ + 4 H⁺ + 4 e⁻). The gas actually evolved is measured and its volume converted to moles with the ideal gas law, n = P V / (R T), at the measured temperature and pressure. Because the collected gas is water-saturated, the water vapour pressure at the measured temperature is subtracted from the total pressure first: n = (P_total − P_water) V / (R T). At 30 °C the water vapour pressure is a non-trivial fraction of the total, so this correction is significant. The whole method rests on two independent measurements – charge in and gas out – so accuracy is limited by whichever of the two is measured worst.

In this cell the cathode is the interesting case. Read the model’s selected η_F and its provenance with the recorded configuration. The ideal reference η_F = 1 means every cathodic electron makes hydrogen; it is not a measurement of the MMO tube assembly. In a single-chamber, undivided, oxygen-rich cell that is optimistic: dissolved oxygen produced at the anode can diffuse to the cathode and be reduced there (the oxygen reduction reaction, ORR), consuming cathodic current that would otherwise make hydrogen. That pulls η_F below 1. The workbook maps the hydrogen-efficiency deficit to an ORR sink as a modelling assumption. A hydrogen measurement alone does not identify the competing reactions or their oxygen stoichiometry. Change downstream oxygen predictions on that basis only when a supported species balance establishes the ORR contribution and the calibration transfers to this undivided cell; otherwise retain the measured hydrogen yield separately and leave the operating calibration excluded.

The gas chromatograph is the reference route for the numerator because it identifies the species, so it separates real hydrogen from any air ingress or oxygen carry-over, which a bare volume reading cannot do. With a sweep-gas flow and a calibrated instrument it yields a molar production rate directly, which can be integrated over the same window as the charge. The eudiometer and water-displacement routes are simpler and measure volume only; they are cleaner for the cathodic hydrogen figure than for the anodic oxygen figure.

Several pitfalls bias the result and should be checked. Charge-balance sanity: at low oxygen and a clean cathode the cathodic η_F should sit close to 1; a value far above 1 means the charge is under-counted (check the current log or sense resistor) or the gas volume is over-read (air ingress, a leak, or un-equalised levels), while a value below 1 can reflect ORR, other reactions or incomplete gas recovery; it does not identify ORR by itself. Level equalisation and the water-vapour correction are the two most common volumetric errors; reading the trapped gas before equalising, or omitting the vapour-pressure subtraction, both bias the moles and hence η_F. Undivided-cell crossover: if the split cannot be enforced by the rig (see the apparatus note), the evolved gases mix and some hydrogen and oxygen can recombine or be re-consumed before capture, making the captured volume under-read true production and biasing η_F low for reasons unrelated to ORR; a genuine per-electrode split is the whole reason the divided/shrouded rig is required, and where mixing or incomplete recovery cannot be excluded, report a collection yield and do not assign an ORR sink without a supported species balance. The oxygen measurement is confounded by the cathodic sink: the measured η_F,OER is the gross oxygen leaving the anode, whereas the model needs the net oxygen reaching the dissolved pool, so η_F,OER should be interpreted as the anodic source term only and the model combines it with the cathodic η_F to obtain net oxygen; measuring net dissolved oxygen directly is a separate experiment (a dissolved-oxygen probe under the same drive). Finally, Faradaic efficiency can depend on current density, temperature, electrolyte, and electrode history – which is why the electrodes are pre-conditioned and each figure is the average of at least three runs – so the operating current, temperature, pressure, run duration, and electrode materials should always be recorded with the result, noting whether η_F was measured at the recorded operating current or at a separately authorised rig current.

Safety: treat undivided mixed gas and any contaminated separated stream as potentially flammable. Quoted air LFL or nominal LOC values are hazard-screen references, not certification of an H₂/O₂/CO₂/N₂ mixture. Applicable mixture limits, margins, collection apparatus and a gas-clearance procedure require owner approval before execution. The optimal and budget methods require separately collected electrode streams; only the interim screen uses undivided mixed gas. Retain forced ventilation, ignition exclusion and the specified flashback protection, avoid pressure build-up, keep collection volumes small and vent via the approved arrangement after reading.

## Sources

- Reliable reporting of Faradaic efficiencies for electrocatalysis research, Nature Communications (2023): https://www.nature.com/articles/s41467-023-36880-8
- A Guideline to Determine Faradaic Efficiency in Electrochemical CO2 Reduction, ACS Energy Letters (2024): https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
- Faradaic Efficiency - an overview, ScienceDirect Topics: https://www.sciencedirect.com/topics/engineering/faradic-efficiency
- Eudiometer / molar volume of a gas, vapour-pressure and level-equalisation corrections (De Anza College lab B1): https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
- Experimental Determination of the Gas Constant (water-displacement gas collection, ideal gas law), Chemistry LibreTexts: https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment)
- Membrane-free water electrolysis - gas crossover, O2-to-cathode current loss and the H2/O2 explosive range, Angewandte Chemie / Science Advances: https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987 and https://www.science.org/doi/10.1126/sciadv.adi3180
- ORR on stainless steel cathodes (oxygen reduction at SS surfaces): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
