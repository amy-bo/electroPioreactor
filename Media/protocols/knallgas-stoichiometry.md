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

Safety governs everything below. The ideal knallgas mixture sits inside the hydrogen–oxygen explosive range and the stoichiometric mixture is detonable. Inert dilution and ignition exclusion are required, but this document does not certify a gas charge as outside the flammable envelope; applicable mixture limits and margins require owner verification. Treat every gas phase in this protocol as potentially explosive at all times.

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

- The actual medium in use (for example [AM002](../README.md)).
- *Xanthobacter tagetidis* inoculum for the current AM003 baseline; record strain identity. The C. necator discussion below is a literature example, not a Xanthobacter threshold or uptake ratio.
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
10. Record the three measured uptake values (H₂, O₂ and CO₂, in consistent units) in the three columns of the **Knallgas ratio** log (its own sheet, linked from the **Calibrations** overview). Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.
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

- The actual medium in use (for example [AM002](../README.md)).
- *Xanthobacter tagetidis* inoculum for the current AM003 baseline; record strain identity. The C. necator discussion below is a literature example, not a Xanthobacter threshold or uptake ratio.
- Cylinder hydrogen.
- Cylinder oxygen.
- Cylinder carbon dioxide.
- Cylinder nitrogen.

### Method

1. Work in the fume hood with forced ventilation running and no spark or hot-surface source present.
2. Fill each serum bottle with a defined volume of medium, inoculate, and seal with a butyl septum and aluminium crimp cap.
3. Before charging bottles, obtain owner approval of the mixture, pressure, applicable flammability limits and margin for the apparatus. A nominal hydrogen LOC of about 5 % O₂ is only a hazard-screen reference, not certification of the H₂/O₂/CO₂/N₂ charge. Historical dosing examples used 2–3 % O₂ and about 1.5 atm absolute (2 % gives pO₂ about 0.03 atm); these are not approved charge instructions. Record exact composition and partial pressures and resolve apparatus validation before execution.
4. Prepare a set of replicate bottles spanning a range of oxygen doses, and one uninoculated control bottle charged the same way.
5. Incubate all bottles at 30 °C with shaking. The shaking incubator is a non-flameproof (non-ATEX) appliance with a motor that can spark: verify no bottle leaks before loading, and ventilate the chamber.
6. At each timepoint (for example 0, 6, 12, 24, 36 and 48 hours): first read the sealed total headspace pressure with the manometer, before withdrawing any gas; then withdraw a fixed volume with a gastight syringe into the GC-TCD and record the H₂, O₂, CO₂ and N₂ composition.
7. At intervals, sacrifice replicate bottles for optical density and dry cell weight rather than repeatedly sampling one bottle.
8. Convert each pre-withdrawal timepoint to gas inventory: p_i = y_i × P_absolute and n_i = p_i × V_headspace/(R T), with consistent wet/dry composition and pressure bases. Record every withdrawal volume, pressure, temperature and composition, and calculate moles removed for each species. Form a sampling-corrected inventory n_i,corr(t) = n_i,remaining(t) + cumulative n_i,removed(t); include any additions explicitly. Positive uptake = −dn_i,corr/dt over the growth interval, in mmol per bottle per hour. N₂ partial pressure need not remain constant after withdrawals: compare its inventory with expected sampling loss (and gas/liquid partitioning); unexplained residual loss may indicate leakage and requires investigation or rejection.
9. Cross-check CO₂ uptake with the change in total inorganic carbon inventory (headspace plus dissolved inorganic carbon, including bicarbonate/carbonate and withdrawn liquid) and biomass carbon gain. Record pH and quantify DIC changes; an uninoculated control does not automatically correct culture-driven pH changes. Total dry cell weight already includes PHB: use measured total biomass carbon, or separate residual biomass mass (total dry mass minus PHB) and PHB mass with appropriate carbon fractions. Historical approximations are about 0.5 g C/g residual biomass and 0.56 g C/g PHB, not independent additions to total dry mass; report uncertainty and use changes from inoculation.
10. Confirm the H₂ : O₂ : CO₂ ratio is consistent across the range of oxygen doses.
11. Record the three measured uptake values (H₂, O₂ and CO₂, in consistent units – the three positive, sampling- and inventory-corrected uptake rates) in the three columns of the **Knallgas ratio** log (its own sheet, linked from the **Calibrations** overview). Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet, which forms and averages the ratio for you; do not pre-compute a ratio yourself.
12. Inactivate culture waste (autoclave or approved disinfectant) before disposal; do not pour live culture to drain.

## What the spreadsheet does with it

The uptake **ratio** and the **fraction of available hydrogen consumed** are separate
measurements. The Knallgas ratio table supplies the former. For a steady-growth
off-gas balance, also calculate biological H₂ uptake divided by electrolytic H₂
generation minus anodic H₂ re-oxidation, using consistent molar units and the same
time window. Correct vent/sampling losses and changes in stored gas; do not infer
this fraction from H₂:O₂:CO₂ ratios alone.

Enter an accepted fraction greater than zero and no greater than one in
`Biology!H2_util_meas` (D128), with run identity, matching operating conditions and
uncertainty in F128. A value outside that range signals an invalid balance for the
steady-growth model; zero uptake belongs to the lag/no-growth case. Leave the input
blank until accepted: the workbook then explicitly retains its provisional 100%
upper bound. This fraction now changes biological O₂/CO₂ demand and unconsumed H₂.
It is specific to the measured conditions; clear or replace it when those conditions
change. The workbook does not yet match this scalar input to conditions automatically.


The Calibrations tab takes the three uptake values (H₂, O₂ and CO₂) you record for each run, forms the H₂ : O₂ : CO₂ ratio itself, and averages those ratios across the included runs for each organism, feeding that average as the gas requirement ratio used downstream. That single ratio sets the surplus oxygen the schedule must vent and the carbon demand it must meet, so both the oxygen budget and the carbon budget are driven by this measured number rather than by the cylinder feed composition.

## Principle & background

The following C. necator literature examples do not establish Xanthobacter tagetidis uptake ratios or oxygen thresholds. *Cupriavidus necator* grows autotrophically by oxidising hydrogen as electron donor, reducing oxygen as terminal electron acceptor, and fixing carbon dioxide as its sole carbon source via the Calvin–Benson–Bassham cycle. Because the three consumption rates are tied together by the cell's energy and carbon balance, they hold an approximately constant molar ratio during steady autotrophic growth.

The distinction between feed and uptake is central. The feed optimum reported in the literature is about 7 : 2 : 1 (the gas supplied), whereas the uptake ratio (the gas the culture actually consumes) sits lower on oxygen and carbon dioxide relative to hydrogen: reported ranges are an oxygen-to-hydrogen ratio of roughly 0.29–0.35 and a carbon-dioxide-to-hydrogen ratio of roughly 0.15–0.19. Scaled to a hydrogen basis of 6, that is about 6 : 1.8–2.1 : 0.9–1.15. Uptake, not feed, is what matters here, because the surplus oxygen to vent and the carbon demand are driven by what the cells take up, not by the cylinder composition.

A measured oxygen-to-hydrogen ratio above 0.5 is thermodynamically implausible for knallgas growth and signals abiotic oxygen loss or a leak; flag it rather than record it. Average only over exponential or steady-state growth: during lag, hydrogen uptake is near zero and a ratio computed across the lag phase is meaningless. Carbon dioxide is highly soluble and partitions into the medium and into bicarbonate at higher pH, so a headspace CO₂ drop overstates biological fixation unless dissolved inorganic carbon is accounted for; measure dissolved inorganic carbon and pH as well as headspace CO₂, using the uninoculated control as an abiotic comparison rather than an automatic correction for culture-driven pH shifts. If the strain accumulates PHB, include its carbon once: use residual biomass plus PHB, or measured total biomass carbon, since total dry cell weight already contains PHB. The cited C. necator literature reports inhibition above about 0.30 atm O₂; that is not a Xanthobacter threshold or a safety criterion.

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
