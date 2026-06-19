# Faradaic efficiency (cathodic etaF, anodic etaF_OER)

**Feeds:** Electrochemistry!etaF (cathode H2, now =1 assumed) and etaF_OER (anode O2, =1).

**Why it matters:** etaF=1 makes all O2 figures an upper bound; likely <1 in this O2-rich undivided cell.

## Principle

Faradaic efficiency is the fraction of the charge passed through an electrode that goes to the reaction of interest, rather than to any competing reaction. For hydrogen at the cathode etaF = n(H2)measured / n(H2)theoretical, and for oxygen at the anode etaF_OER = n(O2)measured / n(O2)theoretical. The theoretical amount comes straight from Faraday's law applied to the charge actually delivered: integrate the current over the run to get the charge Q = integral of I dt (in coulombs), then n_theoretical = Q / (z F), where F = 96485 C/mol and z is the electrons per molecule - z = 2 for H2 (2 H+ + 2 e- -> H2) and z = 4 for O2 (2 H2O -> O2 + 4 H+ + 4 e-). Measure the gas actually evolved, convert that volume to moles with the ideal gas law n = PV / (RT) at the measured temperature and pressure, and divide. The whole method rests on two independent measurements - charge in, gas out - so accuracy is limited by whichever of the two you measure worst.

In this cell the cathode is the interesting case. The model currently sets etaF = 1, which says every electron arriving at the stainless-steel cathode makes H2. In a single-chamber, undivided, O2-rich cell that is optimistic: dissolved O2 produced at the anode can diffuse to the cathode and be reduced there (the oxygen reduction reaction, ORR), consuming cathodic current that would otherwise make H2. That pulls etaF below 1 and, because the model derives the net O2 going to the dissolved pool as anodic O2 minus this cathodic ORR sink (Electrochemistry!O2_cathode_ORR and O2_net_gen), a measured etaF < 1 directly lowers every downstream O2 figure - O2_net_gen, the O2 surplus, steady-state DO, and the sparge interval. Measuring etaF replaces an assumed upper bound with a real number.

## Optimal protocol (best accuracy)

Goal: tight charge accounting plus quantitative gas measurement, ideally with the gas identified not just measured by volume.

Charge (the denominator). Drive the cell at the normal operating current (about 5.7 mA via the LED_D channel per Gerrit's Law) and log current continuously through a calibrated source-measure unit or potentiostat in galvanostatic mode. Integrate to get Q = integral of I dt. If the supply holds current truly constant, Q = I x t and a stopwatch plus a verified current reading suffices, but logging the actual current trace is better because it captures any drift or compliance limiting. Run long enough to evolve a comfortably measurable gas volume - at 5.7 mA the cathode makes only about 0.043 mL H2 per minute at 30 C, so plan for at least 1 to 3 hours of accumulation, or raise the current within the validated Gerrit's Law range (3 to 25 percent intensity) for the calibration run and report etaF at that current.

Gas (the numerator). Two acceptable routes:

1. Calibrated eudiometer / inverted gas burette over the electrode. Seal a graduated gas-collection tube over the cathode so all evolved gas is captured, read the volume against the graduations, and equalise the liquid levels inside and outside the tube before reading so the trapped gas sits at ambient pressure. Record liquid temperature and barometric pressure at the moment of reading.

2. Gas chromatography (GC) on the off-gas. Flow the headspace or a swept cathode off-gas stream through a GC with a thermal conductivity detector (TCD), sampling a fixed loop volume at known times, to quantify H2 (and to confirm O2 and any N2 dilution). GC is the reference method because it identifies the species, so it separates real H2 from any air ingress or O2 carry-over - which a bare volume reading cannot do. With a sweep-gas flow and a calibrated GC you get a molar H2 production rate directly and can integrate it over the same window as the charge.

Anode (etaF_OER). Repeat the gas measurement over the anode to get O2 evolved, using z = 4. In practice run the two electrodes' collections simultaneously in the same charge window so both efficiencies come from one experiment. Interpret the anodic number with the caveat in the pitfalls section.

Convert and divide. For each gas, correct the collected volume to dry-gas moles. With water-saturated collection, subtract the water vapour pressure at the measured temperature from the total pressure before applying the ideal gas law: n = (P_total - P_water) V / (R T). Then etaF = n_measured / (Q / (z F)).

## Budget protocol (minimal kit)

Goal: a usable etaF with no potentiostat and no GC.

Charge (the denominator) from a sense resistor. Put a known, stable sense resistor (a few ohms, low tolerance) in series with the cell and log the voltage across it - a cheap USB datalogger, an Arduino/ADC, or even periodic multimeter readings on a constant current. Current I = V_sense / R_sense, and Q = integral of I dt (sum V/R over the logged samples times the sample interval). If the drive current is genuinely constant, a single good current reading times the run duration gives Q with adequate accuracy. Verify the sense-resistor current against a multimeter in series once at the start.

Gas (the numerator) by water displacement. Capture the evolved gas under an inverted, water-filled graduated cylinder (or measuring cylinder) positioned directly over the electrode, so the rising gas displaces water and you read the volume off the graduations. This is the same physics as the eudiometer, just lower resolution. Read volume, liquid temperature, and barometric pressure (a phone weather reading or local METAR is good enough for a coarse run; a cheap barometer is better). Equalise the inside/outside water levels before reading so the gas is at ambient pressure.

Convert and divide exactly as in the optimal protocol: n = (P_atm - P_water) V / (R T), then etaF = n_measured / (Q / (z F)). The budget route gives you the cathodic etaF for H2 cleanly. It gives a weaker anodic number because displacement volume cannot tell O2 apart from anything else, and the O2 figure is confounded by the cathodic sink (see pitfalls) - treat the budget anodic result as indicative only.

## Result -> model

Cathode: enter the measured cathodic value into Electrochemistry!etaF (cell D18), replacing the assumed 1. This automatically reduces rH2_gen, raises the cathodic O2 sink O2_cathode_ORR (which scales with 1 - etaF), and lowers O2_net_gen and every figure fed from it - O2 surplus, steady-state DO, and the sparge interval all drop from their current upper-bound values toward realistic numbers.

Anode: enter the measured anodic value into Electrochemistry!etaF_OER (cell D26), replacing the assumed 1. This scales rO2_gen, the gross anodic O2 source.

Record the current, temperature, pressure, charge window, and gas volumes alongside the entered numbers in the Source / assumption column, and reclassify both cells from "DATA GAP - need to measure" to the measured tier in the Summary KEY. If the calibration run used a higher current than 5.7 mA, note that etaF can be current-dependent and flag whether it was checked at the operating point.

## Acceptance checks & pitfalls

Charge-balance sanity. The two independent measurements should be self-consistent: at low O2 and a clean cathode, cathodic etaF should sit close to 1; a value far above 1 means the charge is under-counted (check the sense resistor / current log) or the gas volume is over-read (air ingress, leak, un-equalised levels). A value below 1 is the expected, interesting result here - that is the ORR sink showing up.

Equalise levels and correct for water vapour. Reading the trapped gas before equalising inside/outside liquid levels, or forgetting to subtract the water vapour pressure, are the two most common volumetric errors - both bias the moles and so etaF. At 30 C water vapour is a non-trivial fraction of total pressure, so the correction matters.

Undivided-cell crossover and recombination. Because anode and cathode share one chamber with no membrane, evolved gases mix. Some H2 and O2 can chemically recombine or be re-consumed before you capture them, which makes the captured volume under-read true production and biases etaF low for reasons unrelated to ORR. Stirring, proximity of the electrodes, and a catalytic stainless surface all promote this. Run the calibration with collection close to each electrode and over a defined window to minimise mixing time, and treat a low cathodic etaF as an upper estimate of the ORR sink alone (recombination eats into it too).

O2 measurement is confounded by the cathodic sink. The anodic etaF_OER you measure is the gross O2 leaving the anode, but the number the model actually needs for DO is the net O2 reaching the dissolved pool - gross anode O2 minus whatever the cathode reduces. The volumetric/GC anode measurement does not separate these on its own. Interpret etaF_OER as the anodic source term only, and let the model combine it with the cathodic etaF (which carries the sink) to get net O2. Measuring net dissolved O2 directly is a different experiment (a DO probe under the same drive), not this one.

Safety. H2 and O2 evolved together in one chamber is a flammable mixture - an H2 stream above roughly 4 percent O2, or an O2 stream above roughly 4 percent H2, is in the explosive range. Keep collected gas volumes small, vent rather than store the mixed off-gas, and keep ignition sources away from the headspace and collection vessels.

Report the conditions, not just the number. Faradaic efficiency can depend on current density, temperature, electrolyte, and electrode history. Always record the operating current, T, P, run duration, and electrode materials with the result, and note whether etaF was measured at the 5.7 mA operating point or at an elevated calibration current.

## Sources

- Reliable reporting of Faradaic efficiencies for electrocatalysis research, Nature Communications (2023): https://www.nature.com/articles/s41467-023-36880-8
- A Guideline to Determine Faradaic Efficiency in Electrochemical CO2 Reduction, ACS Energy Letters (2024): https://pubs.acs.org/doi/10.1021/acsenergylett.3c02362
- Faradaic Efficiency - an overview, ScienceDirect Topics: https://www.sciencedirect.com/topics/engineering/faradic-efficiency
- Eudiometer / molar volume of a gas, vapour-pressure and level-equalisation corrections (De Anza College lab B1): https://www.deanza.edu/chemistry/documents/1b/experiments/Experiment%20B1-%20Gases.pdf
- Experimental Determination of the Gas Constant (water-displacement gas collection, ideal gas law), Chemistry LibreTexts: https://chem.libretexts.org/Ancillary_Materials/Laboratory_Experiments/Wet_Lab_Experiments/General_Chemistry_Labs/Online_Chemistry_Lab_Manual/Chem_10_Experiments/10%3A_Experimental_Determination_of_the_Gas_Constant_(Experiment)
- Membrane-free water electrolysis - gas crossover, O2-to-cathode current loss and the H2/O2 explosive range, Angewandte Chemie / Science Advances: https://onlinelibrary.wiley.com/doi/10.1002/anie.202417987 and https://www.science.org/doi/10.1126/sciadv.adi3180
- ORR on stainless steel cathodes (oxygen reduction at SS surfaces): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8934858/
