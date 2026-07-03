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

# Knallgas uptake stoichiometry (H₂ : O₂ : CO₂)

This protocol measures the molar ratio in which a hydrogen-oxidising culture consumes hydrogen, oxygen and carbon dioxide during active growth. Two routes are given: an optimal continuous-flow route for best accuracy, and a lower-kit sealed-bottle budget route.

Safety governs everything below. The ideal knallgas mixture sits inside the hydrogen–oxygen explosive range and the stoichiometric mixture is detonable. Every step is written to keep the gas phase outside the flammable envelope by inert dilution, with no ignition source present. Treat every gas phase in this protocol as potentially explosive at all times.

## Optimal protocol

Continuous mass balance on a growing culture: the three uptake rates are read directly from inlet and off-gas analysis, biomass is tracked in parallel, and the ratio is the quotient of the rates over the exponential window.

### Kit

- Process mass spectrometer (magnetic-sector or quadrupole bioprocess MS) configured to resolve H₂, O₂, CO₂ and N₂; or an equivalent multi-channel off-gas analyser. Mass spectrometry is preferred because it resolves hydrogen, which paramagnetic-oxygen and NDIR-carbon-dioxide sensor stacks do not.
- Mass-flow controllers for H₂, O₂, CO₂ and N₂.
- Stirred bench bioreactor (or the electro-bioreactor itself, once its gas generation is calibrated).
- Fume hood with forced ventilation.
- Spectrophotometer for OD₆₀₀ (onboard if the run is on the electro-bioreactor).
- Dry-cell-weight apparatus (filters, drying oven, balance).
- Flashback arrestors on every gas line.
- Nitrogen supply for inert dilution and as a non-consumed flow tracer.

### Reagents

- Minimal autotrophic medium (Sydow 2017 formulation).
- *Cupriavidus necator* inoculum.
- Cylinder hydrogen.
- Cylinder oxygen.
- Cylinder carbon dioxide.
- Cylinder nitrogen (inert balance and internal tracer).

### Method

1. Work in the fume hood with forced ventilation running. Fit flashback arrestors to all gas lines and remove any spark or hot-surface source from the area.
2. Charge the reactor with medium and inoculate with the culture.
3. Set the mass-flow controllers to deliver a metered hydrogen / oxygen / carbon dioxide / nitrogen blend at a known total inlet rate and known inlet composition, using enough nitrogen dilution to hold the gas phase outside the flammable envelope. For a chemostat run, additionally hold a fixed dilution rate so growth reaches steady state.
4. Start stirring and hold the culture at 30 °C.
5. Sample the inlet and the off-gas continuously into the mass spectrometer and log H₂, O₂, CO₂ and N₂ throughout the run.
6. In parallel, draw broth samples at intervals for optical density, and take periodic dry-cell-weight samples to calibrate against optical density.
7. From the optical-density trace, identify the exponential growth window (or, for a chemostat, the steady-state period).
8. Read the H₂, O₂ and CO₂ uptake rates the analyser software reports over that window. The software uses the constant nitrogen tracer to recover the off-gas flow, so no manual flow correction is needed.
9. Repeat the whole run across at least three independent cultivations.
10. Record the three measured uptake values (H₂, O₂ and CO₂, in consistent units) in the three columns of the **Knallgas ratio** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.
11. Inactivate culture waste (autoclave or approved disinfectant) before disposal; do not pour live culture to drain.

## Budget protocol

Same uptake ratio from sealed serum bottles using only a gas chromatograph, a pressure gauge and a syringe: no mass-flow controllers, no mass spectrometer and no continuous flow.

### Kit

- Gas chromatograph fitted with a thermal-conductivity detector (and a flame-ionisation detector if organics are of interest); one GC-TCD run resolves H₂, O₂, CO₂ and N₂.
- Shaking incubator at 30 °C.
- Spectrophotometer for OD₆₀₀.
- Dry-cell-weight apparatus.
- Digital manometer or pressure transducer that reads through the septum.
- Fume hood with forced ventilation.
- Serum bottles, 120–250 mL, with butyl rubber septa and aluminium crimp caps.
- A crimping tool.
- Gastight syringes.
- Flashback arrestors on every gas line.
- Nitrogen supply for inert dilution.

### Reagents

- Minimal autotrophic medium (Sydow 2017 formulation).
- *Cupriavidus necator* inoculum.
- Cylinder hydrogen.
- Cylinder oxygen.
- Cylinder carbon dioxide.
- Cylinder nitrogen.

### Method

1. Work in the fume hood with forced ventilation running and no spark or hot-surface source present.
2. Fill each serum bottle with a defined volume of medium, inoculate, and seal with a butyl septum and aluminium crimp cap.
3. Flush each headspace with a measured, non-explosive gas charge: H₂ and CO₂, plus a small, growth-limiting O₂ dose heavily diluted with N₂. The limiting oxygen concentration (LOC) for hydrogen is about 5 % O₂ by volume: below this, no H₂/O₂/N₂ mixture will propagate a flame whatever the hydrogen fraction. Keep the O₂ mole fraction of the whole bottle charge well under this, and target 2–3 % for margin. Worked ceiling: at a total charge of about 1.5 atm absolute, a 2 % O₂ mole fraction is an O₂ partial pressure of roughly 0.03 atm; even the bare 5 % LOC ceiling is only about 0.075 atm. Record the exact partial pressures charged. If in doubt, reduce the O₂ dose; a mischarged bottle shaken for hours is a detonation hazard – charge behind a blast screen or in the fume hood.
4. Prepare a set of replicate bottles spanning a range of oxygen doses, and one uninoculated control bottle charged the same way.
5. Incubate all bottles at 30 °C with shaking. The shaking incubator is a non-flameproof (non-ATEX) appliance with a motor that can spark: verify no bottle leaks before loading, and ventilate the chamber.
6. At each timepoint (for example 0, 6, 12, 24, 36 and 48 hours): first read the sealed total headspace pressure with the manometer, before withdrawing any gas; then withdraw a fixed volume with a gastight syringe into the GC-TCD and record the H₂, O₂, CO₂ and N₂ composition.
7. At intervals, sacrifice replicate bottles for optical density and dry cell weight rather than repeatedly sampling one bottle.
8. Convert each timepoint to moles per bottle, then fit the uptake rate: for each gas i, multiply its GC mole fraction by the manometer total pressure to get its partial pressure p_i, then apply the ideal-gas law n_i = p_i · V_headspace / (R · T) so every value is in mmol per bottle. For each gas, fit the slope of n_i (mmol per bottle) against time (hours) over the growth interval; that slope is the uptake rate in mmol per bottle per hour. Keep all three gases in these same units. The constant N₂ partial pressure corrects for sampling losses and small leaks; discard any bottle whose N₂ drifts.
9. Cross-check the CO₂ uptake against the biomass carbon balance and against the uninoculated control (which quantifies abiotic CO₂ loss). Biomass carbon fixed = dry cell weight × cell carbon fraction (about 0.5 g C per g dry cell weight) + carbon in any stored polymer (for polyhydroxybutyrate, about 0.56 g C per g PHB). Converted to moles of carbon, this should agree with the CO₂ consumed from the headspace.
10. Confirm the H₂ : O₂ : CO₂ ratio is consistent across the range of oxygen doses.
11. Record the three measured uptake values (H₂, O₂ and CO₂, in consistent units – the three fitted slopes) in the three columns of the **Knallgas ratio** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.
12. Inactivate culture waste (autoclave or approved disinfectant) before disposal; do not pour live culture to drain.

## What the spreadsheet does with it

The Calibrations tab takes the three uptake values (H₂, O₂ and CO₂) you record for each run, forms the H₂ : O₂ : CO₂ ratio itself, and averages those ratios across the included runs for each organism, feeding that average as the gas requirement ratio used downstream. That single ratio sets the surplus oxygen the schedule must vent and the carbon demand it must meet, so both the oxygen budget and the carbon budget are driven by this measured number rather than by the cylinder feed composition.

## Principle & background

*Cupriavidus necator* grows autotrophically by oxidising hydrogen as electron donor, reducing oxygen as terminal electron acceptor, and fixing carbon dioxide as its sole carbon source via the Calvin–Benson–Bassham cycle. Because the three consumption rates are tied together by the cell's energy and carbon balance, they hold an approximately constant molar ratio during steady autotrophic growth. That ratio is what this protocol measures.

The distinction between feed and uptake is central. The feed optimum reported in the literature is about 7 : 2 : 1 (the gas supplied), whereas the uptake ratio (the gas the culture actually consumes) sits lower on oxygen and carbon dioxide relative to hydrogen: reported ranges are an oxygen-to-hydrogen ratio of roughly 0.29–0.35 and a carbon-dioxide-to-hydrogen ratio of roughly 0.15–0.19. Scaled to a hydrogen basis of 6, that is about 6 : 1.8–2.1 : 0.9–1.15. Uptake, not feed, is what matters here, because the surplus oxygen to vent and the carbon demand are driven by what the cells take up, not by the cylinder composition.

A valid measured result should land near that envelope: an oxygen-to-hydrogen ratio around 0.29–0.35 and a carbon-dioxide-to-hydrogen ratio around 0.15–0.19. A measured oxygen-to-hydrogen ratio above 0.5 is thermodynamically implausible for knallgas growth and signals abiotic oxygen loss or a leak; flag it rather than record it. Average only over exponential or steady-state growth: during lag, hydrogen uptake is near zero and a ratio computed across the lag phase is meaningless. Carbon dioxide is highly soluble and partitions into the medium and into bicarbonate at higher pH, so a headspace CO₂ drop overstates biological fixation unless dissolved inorganic carbon is accounted for; the uninoculated control and the biomass carbon-balance cross-check guard against this. If the strain accumulates polyhydroxybutyrate, that stored carbon is fixed CO₂ not present in catabolic biomass and must be included in the carbon balance. Oxygen above about 0.30 atmospheres inhibits growth, which the safety-driven sub-stoichiometric oxygen dosing already favours.

Three routes give the ratio, in descending order of accuracy: continuous off-gas analysis on a flow-through reactor with simultaneous biomass tracking (the optimal route); a closed serum-bottle headspace method reading composition by gas chromatography plus total pressure over a growth interval (the budget route); and an elemental biomass balance that infers CO₂ fixed from the carbon content of the biomass produced, used as an independent cross-check on the gas-phase number. Reported bioprocess off-gas mass spectrometry achieves respiratory-quotient accuracy of about plus or minus 4 per cent, and the nitrogen tracer lets uptake be computed from inlet-minus-outlet differences without a perfect flow seal.

Safety is non-negotiable. Hydrogen is flammable in air from about 4 per cent by volume up to about 75–77 per cent, and the window is wider still in pure oxygen; the stoichiometric hydrogen–oxygen mixture is detonable. Any blend near 7 : 2 : 1 in an ignition-capable vessel is explosive. Keep mixtures outside the flammable envelope by inert dilution with nitrogen or surplus carbon dioxide, use flashback arrestors, work in a fume hood with forced ventilation, exclude sparks and hot surfaces, and keep any electrolytic gas-generation rate low.

## Sources

- Ishizaki et al. / standard knallgas feed optimum and growth limits (H₂:O₂:CO₂ 7:2:1; O₂ > 0.30 atm inhibitory; PCO₂ > 0.10 atm slows growth), reviewed in: Minimizing the Lag Phase of *Cupriavidus necator* Growth under Autotrophic, Heterotrophic, and Mixotrophic Conditions, Appl. Environ. Microbiol. https://journals.asm.org/doi/10.1128/aem.02007-22
- Optimal autotrophic gas ratio and CBB-cycle CO₂ fixation by C. necator: Lab-Scale Cultivation of Cupriavidus necator on Explosive Gas Mixtures: Carbon Dioxide Fixation into Polyhydroxybutyrate, Bioengineering (MDPI). https://www.mdpi.com/2306-5354/9/5/204
- Energy metabolism and electron-donor/acceptor roles of H₂ and O₂: The energy metabolism of Cupriavidus necator in different trophic conditions, Appl. Environ. Microbiol. https://journals.asm.org/doi/10.1128/aem.00748-24
- Off-gas mass spectrometry for OTR/CTR and gas uptake rates (incl. H₂/CO measurement, RQ accuracy ~+/-4%): Applications of off-gas mass spectrometry in fed-batch cell culture, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC7007916/
- Off-gas accuracy for CTR/RQ and inert-tracer gas balancing: A new approach to off-gas analysis for shaken bioreactors showing high CTR and RQ accuracy, PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11776160/
- Serum-bottle headspace GC + pressure protocol for gas uptake/production rates: Two Experimental Protocols for Accurate Measurement of Gas Component Uptake and Production Rates in Bioconversion Processes, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC6459910/
- Headspace GC (TCD/FID), digital-manometer pressure reads, and timepoint schedule for microbial gas methods: Methods for Detecting Microbial Methane Production and Consumption by Gas Chromatography, PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC4993457/
- Automated headspace-pressure / gas-monitoring design for closed cultivation bottles: Design, development and validation of an automated gas monitoring equipment for microbial fermentation, PMC. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8892151/
- Hydrogen flammability limits and inert-dilution / LOC safety: Understanding Explosive Limits for Gases, Sensidyne (https://sensidyne.com/application/understanding-explosive-limits/); Limiting oxygen concentration and flammability limits, CDC/NIOSH (https://stacks.cdc.gov/view/cdc/9780/cdc_9780_DS1.pdf); Explosion Characteristics of Hydrogen-Air and Hydrogen-Oxygen, ICHS (https://conference.ing.unipi.it/ichs2005/Papers/120001.pdf)
