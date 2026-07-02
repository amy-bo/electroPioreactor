---
state: authored
author: [claude-opus-4.8]
checked:
reviewed:
authorised:
source_type: external
description: "Knallgas uptake stoichiometry (H2:O2:CO2)"
sources:
  - https://journals.asm.org/doi/10.1128/aem.02007-22
  - https://www.mdpi.com/2306-5354/9/5/204
  - https://journals.asm.org/doi/10.1128/aem.00748-24
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7007916/
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11776160/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC6459910/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC4993457/
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8892151/
  - https://sensidyne.com/application/understanding-explosive-limits/
  - https://stacks.cdc.gov/view/cdc/9780/cdc_9780_DS1.pdf
  - https://conference.ing.unipi.it/ichs2005/Papers/120001.pdf
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, stoichiometry, knallgas, biology]
---

# Knallgas uptake stoichiometry (H2 : O2 : CO2)

This protocol measures the molar ratio in which a hydrogen-oxidising culture consumes hydrogen, oxygen and carbon dioxide during active growth. Two routes are given: an optimal continuous-flow route for best accuracy, and a lower-kit sealed-bottle budget route.

Safety governs everything below. The ideal knallgas mixture sits inside the hydrogen – oxygen explosive range and the stoichiometric mixture is detonable. Every step is written to keep the gas phase outside the flammable envelope by inert dilution, with no ignition source present. Treat every gas phase in this protocol as potentially explosive at all times.

## Optimal protocol

Continuous mass balance on a growing culture: the three uptake rates are read directly from inlet and off-gas analysis, biomass is tracked in parallel, and the ratio is the quotient of the rates over the exponential window.

### Kit

- Stirred bench bioreactor (or the electro-bioreactor itself, once its gas generation is calibrated).
- Mass-flow controllers for hydrogen, oxygen, carbon dioxide and nitrogen.
- Process mass spectrometer (magnetic-sector or quadrupole bioprocess MS) configured to resolve hydrogen, oxygen, carbon dioxide and nitrogen; or an equivalent multi-channel off-gas analyser. Mass spectrometry is preferred because it resolves hydrogen, which paramagnetic-oxygen and NDIR-carbon-dioxide sensor stacks do not.
- Spectrophotometer for optical density at 600 nm.
- Dry-cell-weight apparatus (filters, drying oven, balance).
- Flashback arrestors on every gas line.
- Fume hood with forced ventilation.
- Nitrogen supply for inert dilution and as a non-consumed flow tracer.

### Reagents

- Minimal autotrophic medium (Sydow 2017 formulation).
- *Cupriavidus necator* inoculum.
- Cylinder hydrogen, oxygen and carbon dioxide.
- Cylinder nitrogen (inert balance and internal tracer).

### Method

1. Work in the fume hood with forced ventilation running. Fit flashback arrestors to all gas lines and remove any spark or hot-surface source from the area.
2. Charge the reactor with medium and inoculate with the culture.
3. Set the mass-flow controllers to deliver a metered hydrogen / oxygen / carbon dioxide / nitrogen blend at a known total inlet rate and known inlet composition, using enough nitrogen dilution to hold the gas phase outside the flammable envelope. For a chemostat run, additionally hold a fixed dilution rate so growth reaches steady state.
4. Start stirring and hold the culture at 30 degrees Celsius.
5. Sample the inlet and the off-gas continuously into the mass spectrometer and log hydrogen, oxygen, carbon dioxide and nitrogen throughout the run.
6. In parallel, draw broth samples at intervals for optical density, and take periodic dry-cell-weight samples to calibrate against optical density.
7. From the optical-density trace, identify the exponential growth window (or, for a chemostat, the steady-state period).
8. Read the hydrogen, oxygen and carbon dioxide uptake rates the analyser software reports over that window. The software uses the constant nitrogen tracer to recover the off-gas flow, so no manual flow correction is needed.
9. Repeat the whole run across at least three independent cultivations.
10. Record the three measured uptake values (H2, O2 and CO2, in consistent units) in the three columns of the **Knallgas ratio** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.

## Budget protocol

Same uptake ratio from sealed serum bottles using only a gas chromatograph, a pressure gauge and a syringe: no mass-flow controllers, no mass spectrometer and no continuous flow.

### Kit

- Serum bottles, 120 – 250 mL, with butyl rubber septa and aluminium crimp caps, plus a crimping tool.
- Gas chromatograph fitted with a thermal-conductivity detector (and a flame-ionisation detector if organics are of interest); one GC-TCD run resolves hydrogen, oxygen, carbon dioxide and nitrogen.
- Gastight syringes.
- Digital manometer or pressure transducer that reads through the septum.
- Shaking incubator at 30 degrees Celsius.
- Spectrophotometer and dry-cell-weight apparatus.
- Flashback arrestors, fume hood with forced ventilation, and a nitrogen supply for inert dilution.

### Reagents

- Minimal autotrophic medium (Sydow 2017 formulation).
- *Cupriavidus necator* inoculum.
- Cylinder hydrogen, carbon dioxide, oxygen and nitrogen.

### Method

1. Work in the fume hood with forced ventilation running and no spark or hot-surface source present.
2. Fill each serum bottle with a defined volume of medium, inoculate, and seal with a butyl septum and aluminium crimp cap.
3. Flush each headspace with a measured, non-explosive gas charge: hydrogen and carbon dioxide, plus a small, growth-limiting oxygen dose heavily diluted with nitrogen and held below the limiting oxygen concentration for hydrogen ignition. Record the exact partial pressures charged.
4. Prepare a set of replicate bottles spanning a range of oxygen doses, and one uninoculated control bottle charged the same way.
5. Incubate all bottles at 30 degrees Celsius with shaking.
6. At each timepoint (for example 0, 6, 12, 24, 36 and 48 hours): first read the sealed total headspace pressure with the manometer, before withdrawing any gas; then withdraw a fixed volume with a gastight syringe into the GC-TCD and record the hydrogen, oxygen, carbon dioxide and nitrogen composition.
7. At intervals, sacrifice replicate bottles for optical density and dry cell weight rather than repeatedly sampling one bottle.
8. For each gas, work out its uptake rate from the slope of its headspace partial pressure against time over the growth interval (read the slope off your own plot), keeping to consistent units throughout. The constant nitrogen partial pressure corrects for sampling losses and small leaks; discard any bottle whose nitrogen drifts.
9. Check the reported carbon-dioxide uptake against the biomass carbon-balance cross-check (dry-cell-weight carbon, with any stored polymer accounted for) and against the uninoculated control, which quantifies abiotic carbon-dioxide loss.
10. Confirm the H2 : O2 : CO2 ratio is consistent across the range of oxygen doses.
11. Record the three measured uptake values (H2, O2 and CO2, in consistent units) in the three columns of the **Knallgas ratio** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.

## What the spreadsheet does with it

The Calibrations tab takes the three uptake values (H2, O2 and CO2) you record for each run, forms the H2 : O2 : CO2 ratio itself, and averages those ratios across the included runs for each organism, feeding that average as the gas requirement ratio used downstream. That single ratio sets the surplus oxygen the schedule must vent and the carbon demand it must meet, so both the oxygen budget and the carbon budget are driven by this measured number rather than by the cylinder feed composition.

## Principle & background

*Cupriavidus necator* grows autotrophically by oxidising hydrogen as electron donor, reducing oxygen as terminal electron acceptor, and fixing carbon dioxide as its sole carbon source via the Calvin – Benson – Bassham cycle. Because the three consumption rates are tied together by the cell's energy and carbon balance, they hold an approximately constant molar ratio during steady autotrophic growth. That ratio is what this protocol measures.

The distinction between feed and uptake is central. The feed optimum reported in the literature is about 7 : 2 : 1 (the gas supplied), whereas the uptake ratio (the gas the culture actually consumes) sits lower on oxygen and carbon dioxide relative to hydrogen: reported ranges are an oxygen-to-hydrogen ratio of roughly 0.29 – 0.35 and a carbon-dioxide-to-hydrogen ratio of roughly 0.15 – 0.19. Scaled to a hydrogen basis of 6, that is about 6 : 1.8 – 2.1 : 0.9 – 1.15. Uptake, not feed, is what matters here, because the surplus oxygen to vent and the carbon demand are driven by what the cells take up, not by the cylinder composition.

A valid measured result should land near that envelope: an oxygen-to-hydrogen ratio around 0.29 – 0.35 and a carbon-dioxide-to-hydrogen ratio around 0.15 – 0.19. A measured oxygen-to-hydrogen ratio above 0.5 is thermodynamically implausible for knallgas growth and signals abiotic oxygen loss or a leak; flag it rather than record it. Average only over exponential or steady-state growth: during lag, hydrogen uptake is near zero and a ratio computed across the lag phase is meaningless. Carbon dioxide is highly soluble and partitions into the medium and into bicarbonate at higher pH, so a headspace carbon-dioxide drop overstates biological fixation unless dissolved inorganic carbon is accounted for; the uninoculated control and the biomass carbon-balance cross-check guard against this. If the strain accumulates polyhydroxybutyrate, that stored carbon is fixed carbon dioxide not present in catabolic biomass and must be included in the carbon balance. Oxygen above about 0.30 atmospheres inhibits growth, which the safety-driven sub-stoichiometric oxygen dosing already favours.

Three routes give the ratio, in descending order of accuracy: continuous off-gas analysis on a flow-through reactor with simultaneous biomass tracking (the optimal route); a closed serum-bottle headspace method reading composition by gas chromatography plus total pressure over a growth interval (the budget route); and an elemental biomass balance that infers carbon dioxide fixed from the carbon content of the biomass produced, used as an independent cross-check on the gas-phase number. Reported bioprocess off-gas mass spectrometry achieves respiratory-quotient accuracy of about plus or minus 4 per cent, and the nitrogen tracer lets uptake be computed from inlet-minus-outlet differences without a perfect flow seal.

Safety is non-negotiable. Hydrogen is flammable in air from about 4 per cent by volume up to about 75 – 77 per cent, and the window is wider still in pure oxygen; the stoichiometric hydrogen – oxygen mixture is detonable. Any blend near 7 : 2 : 1 in an ignition-capable vessel is explosive. Keep mixtures outside the flammable envelope by inert dilution with nitrogen or surplus carbon dioxide, use flashback arrestors, work in a fume hood with forced ventilation, exclude sparks and hot surfaces, and keep any electrolytic gas-generation rate low.

## Sources

- Ishizaki et al. / standard knallgas feed optimum and growth limits (H2:O2:CO2 7:2:1; O2 > 0.30 atm inhibitory; PCO2 > 0.10 atm slows growth), reviewed in: Minimizing the Lag Phase of *Cupriavidus necator* Growth under Autotrophic, Heterotrophic, and Mixotrophic Conditions, Appl. Environ. Microbiol. https://journals.asm.org/doi/10.1128/aem.02007-22
- Optimal autotrophic gas ratio and CBB-cycle CO2 fixation by C. necator: Lab-Scale Cultivation of Cupriavidus necator on Explosive Gas Mixtures: Carbon Dioxide Fixation into Polyhydroxybutyrate, Bioengineering (MDPI). https://www.mdpi.com/2306-5354/9/5/204
- Energy metabolism and electron-donor/acceptor roles of H2 and O2: The energy metabolism of Cupriavidus necator in different trophic conditions, Appl. Environ. Microbiol. https://journals.asm.org/doi/10.1128/aem.00748-24
- Off-gas mass spectrometry for OTR/CTR and gas uptake rates (incl. H2/CO measurement, RQ accuracy ~+/-4%): Applications of off-gas mass spectrometry in fed-batch cell culture, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC7007916/
- Off-gas accuracy for CTR/RQ and inert-tracer gas balancing: A new approach to off-gas analysis for shaken bioreactors showing high CTR and RQ accuracy, PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11776160/
- Serum-bottle headspace GC + pressure protocol for gas uptake/production rates: Two Experimental Protocols for Accurate Measurement of Gas Component Uptake and Production Rates in Bioconversion Processes, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC6459910/
- Headspace GC (TCD/FID), digital-manometer pressure reads, and timepoint schedule for microbial gas methods: Methods for Detecting Microbial Methane Production and Consumption by Gas Chromatography, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC4993457/
- Automated headspace-pressure / gas-monitoring design for closed cultivation bottles: Design, development and validation of an automated gas monitoring equipment for microbial fermentation, PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8892151/
- Hydrogen flammability limits and inert-dilution / LOC safety: Understanding Explosive Limits for Gases, Sensidyne (https://sensidyne.com/application/understanding-explosive-limits/); Limiting oxygen concentration and flammability limits, CDC/NIOSH (https://stacks.cdc.gov/view/cdc/9780/cdc_9780_DS1.pdf); Explosion Characteristics of Hydrogen-Air and Hydrogen-Oxygen, ICHS (https://conference.ing.unipi.it/ichs2005/Papers/120001.pdf)
