# Knallgas uptake stoichiometry (H2:O2:CO2)

**Feeds:** Biology!bio_H2 : bio_O2 : bio_CO2 (currently 6:2:1).

**Why it matters:** sets O2 surplus and carbon demand the schedule is built on.

## Principle

The hydrogen-oxidising bacterium *Cupriavidus necator* grows autotrophically by oxidising H2 as electron donor, reducing O2 as terminal electron acceptor, and fixing CO2 as its sole carbon source via the Calvin - Benson - Bassham cycle. The amount of each gas the culture removes per unit time is not free to vary independently - it is fixed by the cell's energy and carbon balance, so the three consumption rates hold an approximately constant molar ratio during steady autotrophic growth. That ratio is what this protocol measures, and it is what the model holds as bio_H2 : bio_O2 : bio_CO2 (Biology!D10 : D11 : D12).

The distinction the model already flags matters here: the *feed* optimum reported in the literature is about 7:2:1 (the gas you supply), whereas the *uptake* ratio (the gas the culture actually consumes) sits lower on O2 and CO2 relative to H2 - reported ranges are O2:H2 of roughly 0.29 - 0.35 and CO2:H2 of roughly 0.15 - 0.19, i.e. about 6 : 1.8 - 2.1 : 0.9 - 1.15 when scaled to H2 = 6. The current 6:2:1 entry is the central value of those ranges. We measure uptake, not feed, because every downstream quantity the schedule sizes against - the surplus O2 to vent (O2_excess, Biology!D16) and the carbon demand (CO2_cons, Biology!D15) - is driven by what the cells take up, not by the cylinder composition.

The measurement reduces to: during a window of active exponential growth, track how much H2, O2 and CO2 disappear, and divide. Three routes give this, in descending order of accuracy: (1) continuous off-gas analysis on a flow-through reactor with simultaneous biomass tracking (the optimal route); (2) a closed serum-bottle headspace method reading composition by GC plus total pressure over a growth interval (the budget route); (3) an elemental/biomass balance that infers CO2 fixed from the carbon content of the biomass produced, used as an independent cross-check on the gas-phase number.

Safety note carried from the model: the ideal knallgas mixture (H2:O2:CO2 near 7:2:1) sits squarely inside the H2 - O2 explosive range. Hydrogen is flammable in air from about 4 vol% (LEL) to about 75 - 77 vol% (UEL), and the window is even wider in pure O2; the stoichiometric H2 - O2 mixture is detonable. Every variant below must therefore be designed so that no ignition source meets a flammable mixture: dilute with inert gas (N2 or surplus CO2) to keep the gas phase outside the flammable envelope where the protocol allows, eliminate sparks and hot surfaces, use flashback arrestors on gas lines, work in a fume hood with forced ventilation, and keep electrolytic gas generation rates low. Treat the gas phase as explosive at all times.

## Optimal protocol (best accuracy)

Goal: continuous mass-balance on a growing culture so the three uptake rates are read directly and the ratio falls out as their quotient, with biomass measured in parallel to confirm the rates track growth.

Reactor and gassing. Run *C. necator* in a stirred bench bioreactor (or the electro-bioreactor itself once gas generation is calibrated) under either of two regimes:

- Batch with a defined inlet gas. Feed a metered H2 / O2 / CO2 / N2 blend through mass-flow controllers at a known total inlet rate and known inlet composition. N2 acts both as an inert balance and as a non-consumed internal tracer - because the culture does not take up N2, the ratio of any reactive gas to N2 between inlet and outlet gives its consumption without needing a perfect flow seal.
- Chemostat. Hold steady-state growth at fixed dilution rate; at steady state the uptake rates are constant and the ratio is most cleanly defined.

Gas analysis. Sample inlet and outlet (off-gas) continuously with a process mass spectrometer (e.g. a magnetic-sector or quadrupole bioprocess MS), or a multi-channel analyser, configured to resolve H2, O2, CO2 and the N2 tracer. Mass spectrometry is preferred because it resolves H2 (which standard paramagnetic-O2 / NDIR-CO2 sensor stacks do not) and gives all four species on one instrument; reported bioprocess off-gas MS achieves RQ accuracy of about +/-4% and CTR resolution below 0.01 mmol/L/h. Compute the molar uptake rate of each gas from the inlet - outlet difference, normalised to liquid volume (the standard OTR / CTR framing): uptake_i = Q_in * y_in,i - Q_out * y_out,i, with Q_out recovered from the inert N2 balance (Q_out = Q_in * y_in,N2 / y_out,N2).

Biomass tracking. In parallel, sample the broth for optical density (OD600) and periodic dry-cell-weight calibration, so each instantaneous uptake triple can be paired with a specific growth rate. This confirms the gases are being consumed by growth (not by abiotic dissolution or leakage) and lets you report the ratio specifically over the exponential phase, where it is most stable.

Window and replication. Average the three uptake rates over a clean exponential window (batch) or over steady state (chemostat). Repeat across at least three independent cultivations. Report bio_H2 : bio_O2 : bio_CO2 normalised to H2 = 6, with confidence intervals.

## Budget protocol (minimal kit)

Goal: get the same uptake ratio from sealed serum bottles using only a GC, a pressure gauge and a syringe - no MFCs, no mass spec, no continuous flow.

Setup. Prepare replicate serum bottles (e.g. 120 - 250 mL) with a defined volume of minimal autotrophic medium (the model's Sydow 2017 minimal), inoculated with *C. necator*. Seal with butyl rubber septa and aluminium crimp caps. Flush the headspace with a measured, **non-explosive** gas charge - this is the key safety adaptation: rather than charging the bottle to the explosive 7:2:1, charge with H2 and CO2 plus a deliberately sub-stoichiometric, growth-limiting O2 dose heavily diluted with N2, kept below the limiting oxygen concentration for H2 ignition, and replenish O2 in small increments. Record the exact partial pressures charged.

Incubate and sample over a growth interval. Hold at about 30 C with shaking. At a series of timepoints (e.g. 0, 6, 12, 24, 36, 48 h, mirroring established serum-bottle gas-kinetics schedules) measure:

- Total headspace pressure, with a digital manometer / pressure transducer through the septum, before any gas is withdrawn (do not let the headspace equilibrate to atmospheric - read the sealed pressure).
- Headspace composition, by withdrawing a fixed volume with a gastight syringe into a GC fitted with a TCD (and FID if organics are of interest); a single GC-TCD run resolves H2, O2, CO2 and N2.
- Biomass, by sacrificing replicate bottles at intervals for OD / dry weight (since each withdrawal perturbs a sealed bottle, a sacrifice-replicate design is cleaner than repeated sampling of one bottle).

Compute. Convert each species' partial pressure (total pressure x mole fraction) to moles via PV = nRT in the known headspace volume at each timepoint. The N2 partial pressure should be constant (it is not consumed); use it to correct for sampling losses and small leaks. The drop in moles of H2, O2 and CO2 between the start and end of the growth interval gives the consumed amounts; their ratio is bio_H2 : bio_O2 : bio_CO2. Because O2 is dosed sub-stoichiometrically for safety, run several bottles spanning a range of O2 doses and confirm the H2:O2:CO2 *consumption* ratio is consistent across them (O2-limited bottles still reveal the ratio as long as growth occurs).

Cross-check (no extra gas kit). Independently estimate CO2 fixed from biomass: total carbon in dry biomass produced over the interval (dry-cell-weight x carbon fraction, with C. necator biomass approximated by the standard CH1.8O0.5N0.2 formula unless measured) equals the CO2 carbon consumed, less any carbon stored as PHB. Compare this carbon-balance CO2 against the gas-phase CO2 drop; agreement within error validates the headspace number.

## Result -> model

Enter the measured uptake ratio, normalised so the H2 term is 6, into Biology:

- bio_H2 -> Biology!D10 (hold at 6 as the normalising basis).
- bio_O2 -> Biology!D11 (measured O2:H2 x 6; currently 2).
- bio_CO2 -> Biology!D12 (measured CO2:H2 x 6; currently 1).

These propagate automatically to H2_cons (D13), O2_cons (D14), CO2_cons (D15) and O2_excess (D16) in Biology, and onward to the carbon-margin and O2-vent duty terms in Mass Transfer. Replace the present "central value of literature range" source note with the measured ratio, the organism/medium used, the growth phase it was averaged over, the number of replicates and the confidence interval. If the budget route was used, record both the gas-phase ratio and the carbon-balance cross-check. Once entered, this clears the model's standing caveat that the O2 figures are upper bounds resting on an unmeasured uptake ratio.

## Acceptance checks & pitfalls

- Sanity bounds. A valid result should land near the literature envelope: O2:H2 about 0.29 - 0.35 and CO2:H2 about 0.15 - 0.19 (i.e. bio_O2 about 1.75 - 2.1 and bio_CO2 about 0.9 - 1.15 on the H2 = 6 basis). A measured O2:H2 above 0.5 is thermodynamically implausible for knallgas growth and signals abiotic O2 loss or a leak; flag rather than enter.
- Growth phase. Average over exponential / steady-state growth only. During lag, H2 uptake is near zero, so a ratio computed across the lag phase is meaningless; the model already notes ~0 uptake in lag.
- Closed-bottle leaks. Use the constant N2 partial pressure as the leak/sampling tracer; if N2 drifts, correct or discard that bottle. Do not let the headspace equilibrate to atmosphere before reading pressure.
- Abiotic CO2 dissolution. CO2 is highly soluble and partitions into the medium (and into bicarbonate at higher pH), so the headspace CO2 drop overstates biological fixation unless you account for dissolved inorganic carbon. Run an uninoculated control bottle to quantify abiotic CO2 uptake and subtract it; the carbon-balance cross-check guards against this error.
- PHB storage. Carbon diverted into PHB is fixed CO2 that is not in catabolic biomass; if the strain accumulates PHB, the carbon-balance CO2 estimate must include stored polymer, or it will under-count fixation.
- O2 inhibition. O2 above ~0.30 atm inhibits C. necator growth; keep the dissolved/headspace O2 below that, which the safety-driven sub-stoichiometric dosing already favours.
- Safety (non-negotiable). The optimal-route inlet blend and any bottle charged near 7:2:1 are explosive. Keep mixtures outside the H2 - O2 flammable envelope by inert dilution where the method allows, never near 7:2:1 in an ignition-capable vessel; use flashback arrestors, forced ventilation / fume hood, no sparks or hot surfaces, and low gas-generation rates. Treat every gas phase in this protocol as potentially detonable.

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
