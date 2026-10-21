---
state: authored
author: [claude-sonnet-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "Electrode mass-transfer coefficient (ferricyanide limiting current)"
sources:
  - https://journals.flvc.org/cee/article/view/125389/124389
  - https://www.metrohm.com/en/applications/AN-EC-001
  - https://hal.archives-ouvertes.fr/hal-01945535
  - https://homes.nano.aau.dk/lg/biosensors2010_files/Roffel%20Graaf,%20Diffusion%20coefficient%20for%20FeCN%20ions.pdf
  - https://echem101.gamry.com/cyclic-voltammetry-experiment/
  - https://ri.conicet.gov.ar/handle/11336/78040
  - https://link.springer.com/article/10.1007/BF01019561
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, mass-transfer, electrochemistry, ferricyanide, limiting-current]
---

# Electrode mass-transfer coefficient (ferricyanide limiting current)

Measures k_m, the liquid-side mass-transfer coefficient at the reactor's own electrodes, in the real vial at the real stirrer speed. The probe reaction is the one-electron ferricyanide/ferrocyanide couple, whose current at a mass-transport-limited electrode is set purely by how fast the stirred liquid delivers reactant to the surface.

Run conditions for the whole protocol: the reactor's own vial and insert set, the working fill volume (the same for every run), stirrer at 1000 rpm, 25 °C. The shared preconditions in the [README](README.md) apply, except that the temperature here is 25 °C, not 30 °C, because the literature diffusion coefficients are quoted at 25 °C. The geometric electrode area comes from the [vial geometry protocol](vial-geometry.md) and the reactor drawings.

## Optimal protocol

Best accuracy: a potentiostat with a proper potential sweep and a stable reference.

### Kit

- A potentiostat (two- or three-electrode) able to hold a potential and log current at 1 Hz or faster, with a current range covering about 10 µA to 100 mA.
- The reactor vial with its own electrodes fitted as the working electrode and counter electrode. The counter electrode must have a clearly larger wetted area than the working electrode, or it will limit the current instead of the working electrode. If the two electrodes are equal in area, fit a reference electrode (for example Ag/AgCl) in one of the spare ports, or use the larger-area electrode as the counter and record which is which.
- Nitrogen supply through the vial's sparge tube (optional but preferred).
- Aluminium foil or an opaque sleeve to shade the vial.
- Thermometer or the reactor's temperature control, set to 25 °C.
- Ordinary lab glassware, a balance (0.1 mg) and a 25 mL volumetric flask or measuring cylinder.

### Reagents

- Potassium ferricyanide, K3Fe(CN)6, and potassium ferrocyanide trihydrate, K4Fe(CN)6.3H2O, analytical grade.
- Supporting electrolyte in large excess: 0.5 to 1 M potassium chloride (neutral route) or 0.2 to 1 M sodium hydroxide (the classic alkaline route used in the literature, which keeps the couple stable and the platinum surface clean). Use one route for the whole series and record it.
- De-ionised water.
- Make a solution of 0.005 to 0.01 M of each of ferricyanide and ferrocyanide (equimolar) in the supporting electrolyte. The supporting electrolyte must be at least 50 times the concentration of the redox couple, so that migration is suppressed and only diffusion and stirring move the reactant.

### Method

1. Prepare the solution in the dark or under dim light: weigh equal moles of ferricyanide and ferrocyanide, dissolve them in the supporting electrolyte, and make up to volume. Note the exact concentration C_bulk (mol/m3) of each species. Store in an amber or foil-wrapped bottle and use within a day.
2. Assemble the reactor vial with its own electrodes. Wrap the vial in foil, leaving a gap for viewing if needed, because ferricyanide is photosensitive and decomposes in light, which changes the concentration.
3. Fill the vial to the working volume (the same fill as the reactor normally runs, and the same for every run) with the solution. Hold it at 25 °C and run the stirrer at 1000 rpm. Wait 5 minutes for the temperature to settle.
4. If nitrogen is available, sparge for 5 minutes and then stop the sparge and keep a gentle nitrogen blanket over the headspace. Dissolved oxygen is reduced at the cathode alongside ferricyanide and adds to the current, so deaeration removes that error. If nitrogen is not available, go to step 5 and note "not deaerated" in the lab notebook; in that case read the current plateau at the potential window where the oxygen contribution is smallest (see the background).
5. Choose the electrode to study and make it the working electrode. The current is limited by whichever reaction is on the working electrode; with an equimolar couple both the ferricyanide reduction (cathodic) and ferrocyanide oxidation (anodic) have a bulk concentration equal to the other, so either sweep direction works. Record which electrode was the working electrode and whether the run was a reduction or an oxidation.
6. Run a slow linear sweep (5 to 10 mV/s) from open-circuit potential in the direction that drives the chosen reaction, out to about 0.5 V beyond the foot of the wave. A current plateau should appear: a flat region at least 100 mV wide where the current changes by less than about 3 %. If the current keeps rising without a plateau, the electrode is also driving a side reaction (oxygen or hydrogen evolution, or oxygen reduction); stop the sweep earlier, before the side reaction starts, or deaerate better.
7. Read I_lim as the mean current across the middle of the plateau. If the plateau is noisy, hold the potential at the middle of the plateau for 60 s and take the mean of the last 30 s.
8. Repeat steps 6 and 7 three times with the same filling, and take the mean. If the three values spread by more than about 5 %, check for a trapped bubble on the electrode, a drifting temperature or a worn electrode surface, and repeat.
9. Repeat steps 6 to 8 at two or three further stirrer speeds, for example 500, 750 and 1500 rpm (so you have 3 or 4 speeds in all, including 1000). Allow 2 minutes for each new speed to settle. Keep volume, temperature and solution unchanged.
10. Calculate k_m for each speed: k_m = I_lim / (n F A C_bulk), where n = 1 (one electron per ferri/ferrocyanide), F = 96485 C/mol, A is the electrode area in m2 and C_bulk is the bulk concentration of the reacting species in mol/m3 (1 mol/L = 1000 mol/m3). The result is in m/s. Take care with A: use the area wetted by the solution at the working fill, not the full length of the electrode rod, and say which you used (see the background).
11. Plot log(k_m) against log(rpm) for the series; the slope is the rpm exponent (the Sherwood-type dependence, commonly roughly 0.5 to 0.8 for stirred cells, to be read from your own data rather than assumed). Record the rpm, I_lim, area, concentration, k_m and temperature for each point in the lab notebook.
12. Rinse the cell and electrodes with de-ionised water, collect the used solution in a labelled waste bottle (see Safety and disposal) and do not allow it to acidify.

## Budget protocol

Lower-kit variant: a bench power supply, a resistor and a multimeter, stepping the voltage and reading the current plateau by hand. The potential at the working electrode is not controlled as well, so the result is provisional.

### Kit

- A bench DC power supply with adjustable output (0 to 5 V) and current display or a second multimeter.
- A series resistor of 10 to 100 ohm, 1 W, to limit the current and to allow the current to be read as a voltage across it. (Value: pick the resistor so that I_lim times the resistance is about 0.1 to 0.5 V.)
- A multimeter reading millivolts or microamps for the current, and, if possible, a second multimeter and a small reference electrode (for example Ag/AgCl) to read the working electrode potential directly.
- The same vial, electrodes, shading, thermometer and optional nitrogen as above.

### Reagents

- As for the optimal protocol.

### Method

1. Prepare the solution, assemble the vial, shade it, fill to the working volume and bring it to 25 °C and 1000 rpm exactly as in steps 1 to 4 of the optimal protocol.
2. Wire the supply, resistor, a multimeter (as ammeter, or across the resistor as a voltmeter) and the two electrodes in series. Use the larger-area electrode as the counter electrode and the one under study as the working electrode. Set the supply to 0 V and the current limit to a safe value (for example 100 mA).
3. Raise the voltage in steps of 0.1 V. After each step wait 30 s and read the current. If you have the reference electrode, also read the working electrode potential against it.
4. Plot current against voltage (or against working-electrode potential if you measured it). The current rises, flattens into a plateau, then rises again when oxygen or hydrogen evolves. The plateau is I_lim. It should be flat to within about 3 % across at least two successive 0.1 V steps; if there is no flat region, reduce the step to 0.05 V and deaerate with nitrogen.
5. Take I_lim as the mean current across the plateau steps. Repeat the whole step sequence three times, going upwards each time, and take the mean. If the three spread by more than about 10 %, check for a bubble on the electrode or a drifting temperature and repeat.
6. Repeat at two or three further stirrer speeds (500, 750 and 1500 rpm), as in step 9 of the optimal protocol.
7. Calculate k_m = I_lim / (n F A C_bulk) with n = 1, as in step 10 of the optimal protocol, and record the series as in step 11.
8. Rinse and dispose as in step 12 of the optimal protocol.

## What the spreadsheet does with it

The model currently estimates the electrode mass-transfer coefficients from an assumed swirl velocity rather than measuring them. The estimates in use are km_O2 (Electrochemistry!D83, for dissolved oxygen at the cathode), km_exp (Electrochemistry!D84, the experimental or reference coefficient), km_Cl (Chemistry!D129, chloride at the anode) and km_HPO4 and km_HCO3 (Chemistry!D275 and D276, the buffer species). These set the cathodic O2 loss (and so the faradaic efficiency), the peroxide source, the chlorine cap and the electrode-surface pH verdict, which is why the TODO ranks this measurement as the most load-bearing single estimate in the electrochemistry.

A measured ferricyanide k_m converts to each species by the diffusivity ratio, k_m,species = k_m,ferricyanide x (D_species / D_ferricyanide)^(2/3). This exponent follows from the Sherwood correlation Sh proportional to Sc^(1/3) (k proportional to D^(2/3) at fixed viscosity and flow); it is the usual boundary-layer scaling, but check it against your own rpm series, because the exponent in a stirred vial is not guaranteed. Take D_ferricyanide as roughly 7 to 8 x 10^-6 cm2/s (7 to 8 x 10^-10 m2/s) at 25 °C in dilute chloride or hydroxide electrolyte; this range is quoted from general electrochemistry knowledge and is NOT confirmed against the sources listed here. Before use, take the figure for your own electrolyte from the measured ferricyanide values in the Roffel and van de Graaf rotating-disk study and the Bazan and Arvia 1965 study of ferri/ferrocyanide diffusion in NaOH, and write the value and its reference into the notebook. Student CV reports also give values near 5.5 to 5.8 x 10^-6 cm2/s, which shows how much the figure depends on electrolyte and method.

For now: record the measured k_m and the rpm in the lab notebook, scale it by the ratio above for the species you care about, and compare with Electrochemistry!D84 (km_exp). The model does not yet take the measured k_m as a Calibrations-tab input; that is an open item in the TODO. Do not overwrite D83, D84, D129, D275 or D276 by hand.

## Principle & background

Limiting current. Hold a working electrode at a potential where the redox reaction is so fast that every ferricyanide molecule reaching the surface reacts at once. The surface concentration then falls to nearly zero and the current is limited only by the rate at which the stirred liquid carries reactant to the surface. That current is I_lim = n F A k_m C_bulk, so k_m = I_lim / (n F A C_bulk). The Chemical Engineering Education teaching article on ferri/ferrocyanide mass transfer sets this out (variables A, C_b, F and n) as the standard route to a forced-convection mass-transfer coefficient (https://journals.flvc.org/cee/article/view/125389/124389). The same method is used for parallel-plate reactors (https://link.springer.com/article/10.1007/BF01019561) and mesh electrodes (https://ri.conicet.gov.ar/handle/11336/78040).

Why this couple. Ferricyanide/ferrocyanide is a fast, reversible, one-electron couple that behaves well on platinum, steel and carbon. An equimolar mixture keeps the bulk concentration of the reacting species fixed and the electrode surface unpoisoned. Excess supporting electrolyte suppresses migration. An Autolab (Metrohm) application note uses 0.05 M of each in 0.2 M NaOH on a platinum disk (https://www.metrohm.com/en/applications/AN-EC-001); lower concentrations (0.005 to 0.01 M) give smaller currents that are easier to handle with a bench supply and avoid a large density gradient at the electrode. A 1965 Electrochimica Acta study of ferro- and ferricyanide diffusion in NaOH notes that solutions with the ferro/ferricyanide couple and NaOH in excess are very often used for this kind of work, because the limiting current is easily found under convective-diffusion control. The rotating-disk and CV literature on ferricyanide diffusivity includes Roffel and van de Graaf (https://homes.nano.aau.dk/lg/biosensors2010_files/Roffel%20Graaf,%20Diffusion%20coefficient%20for%20FeCN%20ions.pdf), a study of diffusivity against viscosity in polymer solutions (https://hal.archives-ouvertes.fr/hal-01945535), and the Gamry cyclic-voltammetry experiment using 2 mM ferricyanide in 0.1 M KCl (https://echem101.gamry.com/cyclic-voltammetry-experiment/).

Why the vial, the rpm and the temperature must match. k_m depends on the flow field at the electrode, so it is only valid for the geometry, fill and stirrer speed at which it was measured. Run the operating rpm and fill, and add the other rpm values to give the dependence. Diffusivity and viscosity both change with temperature (roughly 2 % per kelvin), so hold 25 °C and record the actual temperature; do not compare directly with a value measured at 30 °C without correcting.

Electrode area. The area in the formula must be the area actually exposed to the solution. Using the geometric area of the whole rod overstates A where the rod is above the liquid or inside a seal, and so understates k_m. Work out the wetted length from the working fill volume and the bore depth (see [vial geometry](vial-geometry.md)), then multiply by the circumference for a cylindrical rod. A rough surface has a larger real area than the geometric one; the result is then a geometric-area-based k_m, which is what the model wants, so say so in the notes. If the electrode shields part of itself (close to the vial wall or to another insert) the effective area may be smaller; treat that as an uncertainty, not a correction.

Side reactions. At the potentials needed for the plateau, an unprotected electrode in water can also reduce dissolved oxygen (cathode) or evolve oxygen (anode); in alkali the anodic wave can overlap oxygen evolution. Deaeration, a short plateau window and a potential just beyond the foot of the wave all limit this. If a plateau cannot be found, record the failure rather than reading a current from the rising part of the curve.

Light, and what to avoid. Ferricyanide is photosensitive; light slowly decomposes it and releases cyanide. Keep solutions in the dark and use them within a day. The solution also darkens and loses ferricyanide with age, which lowers C_bulk, so make it fresh.

Safety and disposal. Potassium ferri- and ferrocyanide are complex salts, with the cyanide tightly bound, and have low acute toxicity at these concentrations, but they must never be mixed with acid: acidification (for example with the vinegar or citric acid used in the CO2 flow protocol) can release toxic hydrogen cyanide gas. Keep the waste neutral or alkaline, label the waste bottle "ferricyanide / ferrocyanide waste, NO ACID", store it apart from acids, and hand it over for chemical-waste disposal; do not pour it down the sink. Wear gloves and eye protection, wash hands after handling and wipe any spills with water. Rinse the vial and electrodes thoroughly before using them for any acid-containing protocol, and note that the reactor's electrodes must be cleaned before they are used with culture medium again.

## Sources

- Limiting-current definition, k_m = I_lim/(nFAC_b), ferri/ferrocyanide as a forced-convection mass-transfer probe: https://journals.flvc.org/cee/article/view/125389/124389
- Equimolar ferro/ferricyanide in NaOH supporting electrolyte on platinum (Autolab application note AN-EC-001): https://www.metrohm.com/en/applications/AN-EC-001
- Ferricyanide diffusivity, rotating disk in KCl: https://homes.nano.aau.dk/lg/biosensors2010_files/Roffel%20Graaf,%20Diffusion%20coefficient%20for%20FeCN%20ions.pdf ; and in polymer solutions at 25 °C: https://hal.archives-ouvertes.fr/hal-01945535
- Ferricyanide in 0.1 M KCl, cyclic voltammetry teaching experiment: https://echem101.gamry.com/cyclic-voltammetry-experiment/
- Limiting-current mass transfer in a parallel-plate reactor: https://link.springer.com/article/10.1007/BF01019561 ; on mesh electrodes: https://ri.conicet.gov.ar/handle/11336/78040
- Not found by search, so unconfirmed: the numerical D_ferricyanide at 25 °C (stated above only as a general 7 to 8 x 10^-6 cm2/s range to be verified), the Sc^(1/3) exponent for a stirred vial, and Bazan and Arvia 1965 (Electrochimica Acta) full text.
