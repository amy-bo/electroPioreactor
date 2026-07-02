---
state: authored
author:
checked:
reviewed:
authorised:
source_type: external
description: "Faradaic efficiency (cathodic etaF, anodic etaF_OER)"
sources:
  - https://www.nature.com/articles/s41467-023-36880-8
  - https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
  - https://www.sciencedirect.com/topics/engineering/faradic-efficiency
  - https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
  - https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment
  - https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987
  - https://www.science.org/doi/10.1126/sciadv.adi3180
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, electrochemistry, faradaic-efficiency, electrolysis]
---

# Faradaic efficiency (cathodic etaF, anodic etaF_OER)

## Optimal protocol

### Kit

- The electrochemical cell as normally operated (stainless-steel cathode, working anode, normal electrolyte).
- Potentiostat or source-measure unit able to run galvanostatic (constant-current) mode and report the total charge passed in coulombs, with a continuous current log.
- Two calibrated gas-collection tubes (eudiometers or inverted gas burettes), one to seal over the cathode and one over the anode.
- Gas chromatograph fitted with a thermal conductivity detector (TCD) and a fixed-volume sample loop, for species identification of the off-gas.
- Sweep-gas supply and connecting tubing, if the gas chromatograph is run on a swept off-gas stream.
- Thermometer for the electrolyte.
- Barometer.

### Reagents

- None. The calibration runs on the cell's normal operating electrolyte.

### Method

1. Set up the cell as normally operated, with the stainless-steel cathode and the anode immersed in the electrolyte.
2. Seal one calibrated gas-collection tube over the cathode so that all gas evolved there is captured, and seal a second calibrated collection tube over the anode.
3. Connect the cell to the potentiostat or source-measure unit in galvanostatic mode. Set the drive current to the operating point (about 5.7 mA) or to a chosen calibration current within the validated drive range (about 3 to 25 percent intensity). Start the continuous current log.
4. If using the gas chromatograph, flow the cathode off-gas through it and take samples from the fixed loop at recorded times to identify and quantify the hydrogen; do the same on the anode off-gas to identify and quantify the oxygen.
5. Run the cell over a single defined time window, long enough to collect a comfortably readable gas volume (at least one to three hours at 5.7 mA), keeping both electrode collections running over exactly the same window.
6. At the end of the window, for each collection tube, equalise the liquid levels inside and outside the tube so the trapped gas sits at ambient pressure, then read the collected gas volume against the graduations.
7. Read and note the electrolyte temperature and the barometric pressure at the moment of reading.
8. Read the total charge passed from the instrument (in coulombs), and note the start and end times of the run.
9. Vent the collected gas. Do not store the mixed hydrogen and oxygen off-gas.
10. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H2 or anode O2), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- The electrochemical cell as normally operated (stainless-steel cathode, working anode, normal electrolyte).
- A datalogging current meter or coulomb counter that reports accumulated charge in coulombs; or a low-tolerance sense resistor (a few ohms) placed in series with the cell together with a datalogger (USB logger or microcontroller/ADC) set to integrate the current into charge.
- A multimeter, to verify the logged current against a series reading at the start.
- Two inverted, water-filled graduated measuring cylinders, one to invert over the cathode and one over the anode, in a water trough or reservoir.
- Thermometer for the electrolyte.
- Barometer (a phone weather reading or local METAR is adequate for a coarse run).

### Reagents

- None. The calibration runs on the cell's normal operating electrolyte.

### Method

1. Set up the cell as normally operated, with the stainless-steel cathode and the anode immersed in the electrolyte.
2. Invert a water-filled graduated cylinder directly over the cathode so that the rising gas displaces water up the cylinder, and invert a second water-filled cylinder over the anode.
3. Connect the datalogging current meter (or the sense resistor and logger) in series with the cell so it records the charge passed. Confirm the logged current against a multimeter reading in series once at the start.
4. Set the drive current to the operating point (about 5.7 mA) or to a chosen calibration current within the validated drive range, and start logging.
5. Run the cell over a single defined time window, long enough to collect a comfortably readable gas volume (at least one to three hours at 5.7 mA), keeping both electrode collections running over exactly the same window.
6. At the end of the window, for each cylinder, equalise the water levels inside and outside the cylinder so the trapped gas sits at ambient pressure, then read the displaced-gas volume against the graduations.
7. Read and note the electrolyte temperature and the barometric pressure at the moment of reading.
8. Read the total charge passed from the logger (in coulombs), and note the start and end times of the run.
9. Vent the collected gas. Do not store the mixed hydrogen and oxygen off-gas.
10. Record, for each run, the charge passed (coulombs), the gas volume collected (mL), the gas temperature (°C) and pressure (Pa), and which electrode (cathode H2 or anode O2), in the **Faradaic efficiency** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Faradaic efficiency section of the Calibrations tab converts each recorded gas volume to moles using the ideal gas law from the gas temperature and pressure you entered, and divides that by the theoretical moles expected from the charge passed using Faraday's law. That ratio is the Faradaic efficiency for the run. The tab then averages the included runs for each reactor and feeds the cathodic efficiency (etaF) and the anodic efficiency (etaF_OER) into the model. You do no hand calculation; enter only the measured quantities and the spreadsheet does the rest.

## Principle & background

Faradaic efficiency is the fraction of the charge passed through an electrode that goes to the reaction of interest, rather than to any competing reaction. For hydrogen at the cathode, etaF = n(H2) measured / n(H2) theoretical, and for oxygen at the anode, etaF_OER = n(O2) measured / n(O2) theoretical. The theoretical amount comes straight from Faraday's law applied to the charge actually delivered: the charge Q is the integral of the current over the run (in coulombs), and n_theoretical = Q / (z F), where F = 96485 C/mol and z is the electrons per molecule – z = 2 for hydrogen (2 H+ + 2 e- gives H2) and z = 4 for oxygen (2 H2O gives O2 + 4 H+ + 4 e-). The gas actually evolved is measured and its volume converted to moles with the ideal gas law, n = P V / (R T), at the measured temperature and pressure. Because the collected gas is water-saturated, the water vapour pressure at the measured temperature is subtracted from the total pressure first: n = (P_total - P_water) V / (R T). At 30 °C the water vapour pressure is a non-trivial fraction of the total, so this correction is significant. The whole method rests on two independent measurements – charge in and gas out – so accuracy is limited by whichever of the two is measured worst.

In this cell the cathode is the interesting case. The model currently assumes etaF = 1, which says every electron arriving at the stainless-steel cathode makes hydrogen. In a single-chamber, undivided, oxygen-rich cell that is optimistic: dissolved oxygen produced at the anode can diffuse to the cathode and be reduced there (the oxygen reduction reaction, ORR), consuming cathodic current that would otherwise make hydrogen. That pulls etaF below 1. Because the model derives the net oxygen reaching the dissolved pool as the anodic oxygen minus this cathodic ORR sink, a measured etaF below 1 directly lowers every downstream oxygen figure: the net oxygen generation, the oxygen surplus, the steady-state dissolved oxygen, and the sparge interval all move from their current upper-bound values toward realistic numbers. Measuring etaF replaces an assumed upper bound with a real number.

The gas chromatograph is the reference route for the numerator because it identifies the species, so it separates real hydrogen from any air ingress or oxygen carry-over, which a bare volume reading cannot do. With a sweep-gas flow and a calibrated instrument it yields a molar production rate directly, which can be integrated over the same window as the charge. The eudiometer and water-displacement routes are simpler and measure volume only; they are cleaner for the cathodic hydrogen figure than for the anodic oxygen figure.

Several pitfalls bias the result and should be checked. Charge-balance sanity: at low oxygen and a clean cathode the cathodic etaF should sit close to 1; a value far above 1 means the charge is under-counted (check the current log or sense resistor) or the gas volume is over-read (air ingress, a leak, or un-equalised levels), while a value below 1 is the expected, interesting result here – the ORR sink showing up. Level equalisation and the water-vapour correction are the two most common volumetric errors; reading the trapped gas before equalising, or omitting the vapour-pressure subtraction, both bias the moles and hence etaF. Undivided-cell crossover: because the anode and cathode share one chamber with no membrane, the evolved gases mix and some hydrogen and oxygen can recombine or be re-consumed before capture, making the captured volume under-read true production and biasing etaF low for reasons unrelated to ORR; collect close to each electrode over a defined window to minimise mixing time, and treat a low cathodic etaF as an upper estimate of the ORR sink alone. The oxygen measurement is confounded by the cathodic sink: the measured etaF_OER is the gross oxygen leaving the anode, whereas the model needs the net oxygen reaching the dissolved pool, so etaF_OER should be interpreted as the anodic source term only and the model combines it with the cathodic etaF to obtain net oxygen; measuring net dissolved oxygen directly is a separate experiment (a dissolved-oxygen probe under the same drive). Finally, Faradaic efficiency can depend on current density, temperature, electrolyte, and electrode history, so the operating current, temperature, pressure, run duration, and electrode materials should always be recorded with the result, noting whether etaF was measured at the 5.7 mA operating point or at an elevated calibration current.

Safety: hydrogen and oxygen evolved together in one chamber form a flammable mixture – a hydrogen stream above roughly 4 percent oxygen, or an oxygen stream above roughly 4 percent hydrogen, is in the explosive range. Keep collected gas volumes small, vent rather than store the mixed off-gas, and keep ignition sources away from the headspace and collection vessels.

## Sources

- Reliable reporting of Faradaic efficiencies for electrocatalysis research, Nature Communications (2023): https://www.nature.com/articles/s41467-023-36880-8
- A Guideline to Determine Faradaic Efficiency in Electrochemical CO2 Reduction, ACS Energy Letters (2024): https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
- Faradaic Efficiency - an overview, ScienceDirect Topics: https://www.sciencedirect.com/topics/engineering/faradic-efficiency
- Eudiometer / molar volume of a gas, vapour-pressure and level-equalisation corrections (De Anza College lab B1): https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
- Experimental Determination of the Gas Constant (water-displacement gas collection, ideal gas law), Chemistry LibreTexts: https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment)
- Membrane-free water electrolysis - gas crossover, O2-to-cathode current loss and the H2/O2 explosive range, Angewandte Chemie / Science Advances: https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987 and https://www.science.org/doi/10.1126/sciadv.adi3180
- ORR on stainless steel cathodes (oxygen reduction at SS surfaces): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
