# Surface oxygen transfer (kL_surf) by dynamic gassing-out

**Feeds:** Mass Transfer!kL_surf / kLa_surf_used (enter the measured value into kLa_meas so the model uses it instead of the proxy). Compare to kL_surf_crit.

**Why it matters:** ~375% model sensitivity; decides the 1.4-min vs 178-min sparge interval.

## Principle

The electro-bioreactor makes O2 at the anode, and in this stirred 16 mL vial the dominant route for getting that O2 back out of the liquid is transfer across the free surface into the vented headspace - there is no continuous air sparge doing the work. The rate of that transfer is set by a surface volumetric oxygen mass-transfer coefficient, kLa_surf, where kL_surf is the liquid-film coefficient (m/s) and a_surf is the gas-liquid interfacial area per unit liquid volume (1/m). The model currently estimates kL_surf from a Danckwerts surface-renewal proxy (kL_surf = 2*sqrt(D_O2*s_renew/pi), with the surface-renewal frequency s_renew = tip_speed/vial_ID). That proxy is unvalidated and is the single most sensitive number in the whole model, so it has to be replaced by a measured value.

The standard way to measure kLa without a culture is the dynamic gassing-out method ("gas-out / gas-in"). You strip the dissolved oxygen out of the working volume by sparging an inert gas (nitrogen), stop the strip, then let the liquid re-aerate from its own free surface while the stirrer runs at the real operating speed. A dissolved-oxygen (DO) probe records the re-aeration curve. With no oxygen uptake (no cells) and a well-mixed liquid, the dissolved-O2 balance is dC/dt = kLa*(C_star - C), where C_star is the saturation DO in equilibrium with the gas above the surface. That integrates to ln(C_star - C) = -kLa*t + const, so a plot of ln(C_star - C) against time is a straight line whose slope is -kLa. The slope is the surface kLa, because surface transfer is the only path operating once the N2 is off and there is no sparge. This is the established and widely used approach because it needs only a DO probe, no off-gas analyser, no hazardous reagents and no organism (see Garcia-Ochoa / BioProcess International, and the Eppendorf and bioprocesstools method notes in Sources).

Two things make this measurement specific rather than generic. First, surface renewal scales with stirring, so the run MUST be at the operating stirrer speed (500 rpm here) and in the actual vial geometry - the same free-surface area and the same inserts that sit in the real reactor - or kL_surf will not match what the reactor sees. Second, the DO probe has its own first-order response lag; if that lag is not small compared with the mass-transfer time constant it flattens the early part of the curve and makes kLa read low, so the lag must be checked and, if needed, corrected (see Tribe 1995 and the Torres 2017 system-delay algorithm in Sources).

## Optimal protocol (best accuracy)

Use a fast lab-grade DO probe and the real reactor geometry.

1. Fill a clean reactor vial with the operating working volume of de-ionised water or, better, the actual Sydow 2017 minimal medium (salts shift solubility and coalescence slightly, so medium is the more faithful choice). Hold it at the operating temperature, 30 degC, in the Pioreactor or a jacketed block. Run the magnetic stir bar at the operating setpoint, 500 rpm, for the entire measurement.

2. Fit a fast optical (luminescence-quenching) DO probe or a small Clark-type electrode through the cap so the sensing tip sits in the well-mixed bulk, clear of the stir bar and clear of the surface. Avoid trapping a bubble on the tip. Note the probe's quoted response time (t63 or t95) from its datasheet - you need it for the lag check below.

3. Calibrate the probe two-point: zero in fully N2-sparged (or sodium-sulfite) water, and span at 100% air saturation by bubbling air through the stirred medium until the reading is stable. At 30 degC and ~1 atm, 100% air saturation in fresh water is about 7.54 mg/L - use this as a sanity check on C_star, but read your actual stable air-saturated plateau as the working C_star because salts and local pressure shift it.

4. Deoxygenate: sparge nitrogen through the vial (via the existing sparge tube) at the operating temperature and stir speed until the DO reading falls to near zero and stays there (typically below ~5% of air saturation). Do not over-sparge longer than needed; you only need a low, stable start point.

5. Stop the nitrogen cleanly and let the headspace return to its vented (air or operating-gas) composition. Start logging DO against time immediately, at 1 s intervals or faster, while the stirrer keeps running at 500 rpm. Record until the curve flattens at the air-saturated plateau (this defines C_star for the fit). A single re-aeration sweep from ~0 to plateau is the dataset.

6. Probe-lag check and correction: the rule of thumb is that the probe time constant should be under about one tenth of the mass-transfer time constant (1/kLa) for its effect to be negligible; more strictly, tau_probe*kLa should stay below ~0.02-0.05. Surface kLa in a small stirred vial is slow (likely on the order of 0.001-0.01 1/s, i.e. a time constant of minutes), and lab probes respond in 10-100 s, so the lag is often acceptable here - but check it. If tau_probe*kLa exceeds ~0.05, fit a two-parameter model that convolves the first-order liquid response with the first-order probe response (or use the Torres 2017 system-delay algorithm), rather than the bare log-slope, otherwise kLa reads low.

7. Fit: take only the points between roughly 10% and 90% of the approach to C_star (early points are most lag-sensitive; late points have a tiny, noisy driving force). Plot ln(C_star - C) versus time. The slope magnitude is kLa_surf in 1/s. Convert to 1/h by *3600 for entry into the model.

8. Replicates and controls: run at least three re-aeration sweeps and report the mean and spread. Run one sweep with the stirrer OFF as a contrast - it should give a markedly lower kLa, confirming the measurement is genuinely surface-renewal-driven and not dominated by a leak or a trapped bubble.

## Budget protocol (minimal kit)

Use a low-cost optical DO probe (for example an inexpensive optical DO module or a hobby galvanic DO meter) and the same vial.

1. Same vial, same working volume, same 30 degC, same 500 rpm. If you cannot hold 30 degC, run at measured room temperature and record it - solubility and diffusivity are temperature-dependent, so the temperature must be logged either way.

2. Two-point calibrate the cheap probe: zero against water that has been vigorously N2-sparged (or a fresh sodium-sulfite / sodium-metabisulfite solution, which scavenges O2 to ~0), and span against air-saturated stirred water. Accept that a low-cost optical probe responds 2-4x slower than a Clark electrode (tens of seconds), which makes the lag check below more important.

3. Deoxygenate by N2 sparge through the sparge tube until the reading bottoms out and is steady. If no N2 is available, a freshly made sodium-sulfite charge will pull DO to near zero, but then you must change to fresh aerating medium before the re-aeration sweep because residual sulfite keeps consuming O2 and corrupts the slope - N2 sparging is cleaner and is preferred.

4. Stop the gas, start a stopwatch or the meter's logger, and record DO every 2-5 s while stirring at 500 rpm until it plateaus. Phone-timestamped manual readings work if no logger is available, but log densely over the first minute.

5. Fit exactly as in the optimal protocol: ln(C_star - C) vs time, slope = -kLa_surf. Because the budget probe is slow, compute tau_probe*kLa; if it exceeds ~0.05, either restrict the fit to later points where the lag matters less and flag the result as a lower bound, or borrow a faster probe for one confirmatory run. Report the budget figure as provisional and note the probe model and its response time.

6. Do at least two sweeps. If the two disagree by more than ~20%, suspect probe lag, a trapped bubble, or an unstable C_star plateau, and repeat.

## Result -> model

1. Enter the measured surface kLa, in 1/h, into Mass Transfer!kLa_meas (currently 0). The model's kLa_surf_used switches to the measured value automatically when kLa_meas > 0 (kLa_surf_used = IF(kLa_meas>0, kLa_meas/3600, kLa_surf)), so everything downstream - the steady-state DO check, the surface strip rate, and the schedule regime - then runs on your measurement instead of the proxy.

2. If you want kL_surf itself (m/s) rather than the lumped kLa, divide by the model's area-per-volume term: kL_surf = kLa_surf / a_surf, where a_surf = interface_A / V_charge is the free-surface area per liquid volume (Mass Transfer!a_surf, in 1/m). Use the model's geometry value for a_surf so the conversion is consistent with the rest of the sheet; you only need this if you are comparing the measured kL_surf directly against the model's proxy kL_surf or against kL_surf_crit.

3. Compare to the critical threshold. The model computes a critical surface coefficient, kL_surf_crit (Mass Transfer; currently about 1.2e-4 m/s), which is the minimum kL_surf at which surface stripping alone holds dissolved O2 under the impairment band. The measured kL_surf must EXCEED kL_surf_crit. Report the margin as the ratio measured / kL_surf_crit: greater than 1 means surface stripping alone can hold DO (carbon-limited regime, long interval near ~178 min); below 1 means it cannot, and the schedule stays O2-limited (short interval near ~1.4 min). Equivalently, watch DO_ss (the model's predicted steady-state DO under surface stripping) against DO_impair once your measured value is in - sched_regime resolves the 1.4-min vs 178-min outcome from exactly this comparison.

## Acceptance checks & pitfalls

- Run at the operating stir rate (500 rpm) and real geometry. Surface renewal scales with tip speed, so a measurement at the wrong rpm or in a different vessel does not transfer. Record the actual rpm, vial, working volume and which inserts were fitted.
- Confirm C_star independently. The fit is only as good as the saturation value you subtract. Read C_star as your own stable air-saturated plateau; cross-check against ~7.54 mg/L at 30 degC, ~1 atm in fresh water and note that medium salts and local pressure shift it.
- Check the probe lag every time: compute tau_probe*kLa. Negligible if below ~0.02-0.05; otherwise the bare log-slope reads low and you must use the convolved two-parameter fit or a faster probe. A slow budget probe is the most likely reason a measurement comes out artificially under kL_surf_crit.
- Fit the linear middle of the curve (~10-90% of approach to C_star). Including the lag-dominated early points or the noisy near-plateau tail biases the slope.
- Watch for a trapped bubble on the probe tip or a stuck stir bar - both flatten the curve and read low. The stirrer-off contrast run should give a clearly lower kLa; if it does not, the rig is leaking gas in some other way and the surface number is not what you measured.
- No cells, no O2-consuming residue. Sodium sulfite left in the liquid keeps eating O2 and corrupts the slope; prefer N2 stripping, and if sulfite is used to deoxygenate, swap to fresh medium before the re-aeration sweep.
- Replicate (>=3 optimal, >=2 budget) and report mean and spread. A single sweep is not an acceptance.
- Decision rule: measured kL_surf must exceed kL_surf_crit (or DO_ss must sit under DO_impair). Report the margin, not just pass/fail, because the schedule interval swings from ~1.4 min to ~178 min across this threshold.

## Sources

- Dynamic gassing-out method, overview and steps: [BioProcess International - Improving Bioreactor Performance: Measuring Dissolved Oxygen to Determine kLa](https://www.bioprocessintl.com/sponsored-content/improving-bioreactor-performance-measuring-dissolved-oxygen-to-determine-kla); [Eppendorf - Measuring the kLa of Cell Culture Bioreactors](https://www.eppendorf.com/ie-en/lab-academy/applied-industries/bioprocessing/measuring-the-kla-of-cell-culture-bioreactors/); [bioprocesstools - How to Calculate kLa](https://bioprocesstools.com/blog/how-to-calculate-kla/); [Assessment of kLa - 6 Methods](https://www.biologydiscussion.com/cell-biology/assessment-of-kla-oxygen-transfer-coefficient-6-methods/7681).
- Probe-lag (first-order sensor) errors and correction: [Tribe et al. 1995, Determination of kLa using the dynamic gas out-gas in method: errors caused by dissolved oxygen probes (Biotechnol. Bioeng.)](https://analyticalsciencejournals.onlinelibrary.wiley.com/doi/pdf/10.1002/bit.260460412); [Torres et al. 2017, Automated algorithm to determine kLa considering system delay (J. Chem. Technol. Biotechnol.)](https://scijournals.onlinelibrary.wiley.com/doi/10.1002/jctb.5157); [BioProcess International - Measuring kLa for Better Bioreactor Performance](https://www.bioprocessintl.com/bioreactors/measuring-kla-for-better-bioreactor-performance).
- Probe choice (optical vs Clark) - response time and accuracy: [Optical Oxygen Sensing and Clark Electrode: Face-to-Face in a Biosensor Case Study (PMC9572888)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/); [USGS - Field Comparison of Optical and Clark Cell Dissolved Oxygen Sensors](https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf); [Scientific Bioprocessing - How to Choose the Right Dissolved Oxygen Sensor](https://www.scientificbio.com/blog/how-to-choose-the-right-dissolved-oxygen-sensor/).
- Surface aeration and kLa = kL * a in stirred vessels: [ScienceDirect Topics - Surface Aeration](https://www.sciencedirect.com/topics/engineering/surface-aeration); [BioProcess International - Oxygen Transfer and the Volumetric Mass-Transfer Coefficient in Stirred Tanks](https://www.bioprocessintl.com/bioreactors/lessons-in-bioreactor-s-scale-up-part-4-physiochemical-factors-affecting-oxygen-transfer-and-the-volumetric-mass-transfer-coefficient-in-stirred-tanks).
- DO saturation at 30 degC for C_star cross-check: [Fondriest - Dissolved Oxygen (100% air saturation ~7.54 mg/L at 30 degC)](https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/).
