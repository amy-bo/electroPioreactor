---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Gerrit's Law: LED-intensity to electrolysis-current calibration"
sources:
  - https://docs.pioreactor.com/user-guide/led-automations
  - https://www.allaboutcircuits.com/news/LED-controller-linear-constant-current-control-high-current-diodes-inc/
  - https://en.wikipedia.org/wiki/Faraday%27s_laws_of_electrolysis
  - https://www.tek.com/en/blog/measuring-current-using-shunt-resistors
  - https://docs.pioreactor.com/user-guide/intro-python-scripting
  - https://www.firgelliauto.com/blogs/engineering-calculators/current-sense-resistor-calculator-measuring-current-with-a-shunt
  - https://www.analog.com/en/resources/app-notes/an-105fa.html
  - https://docs.pioreactor.com/user-guide/external-power
  - https://scienceinfo.com/quantitative-electrolysis/
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, electrochemistry, gerrit, calibration]
---

# Gerrit's Law: LED-intensity to electrolysis-current calibration

**Feeds:** Electrochemistry!gerrit_slope, gerrit_int (+ the 3-25% validity band).
**Why it matters:** current is the master input setting all H2/O2 generation.

## Principle

The Pioreactor controls its LED/PWM channels by a dimensionless intensity setpoint expressed as a percentage (0-100%). When one of those channels drives an electrolytic cell, the resulting current through the cell is not directly commanded - it is a consequence of the cell's electrochemistry and the channel's output characteristic at that setpoint. Gerrit's Law encodes the empirical relationship as a straight line: I (mA) = gerrit_slope × intensity (%) + gerrit_int.

That linear form is justified by the roughly linear relationship between PWM duty cycle and mean output current for a resistive - or near-resistive - load, analogous to the way LED dimmer drivers maintain linear current vs duty-cycle control ([Pioreactor LED automations docs](https://docs.pioreactor.com/user-guide/led-automations); [general PWM-to-current linearity](https://www.allaboutcircuits.com/news/LED-controller-linear-constant-current-control-high-current-diodes-inc/)). The intercept gerrit_int captures any non-zero current that flows at very low setpoints due to power-supply floor effects or cell conditioning; the model currently extrapolates this intercept below 3%, which is outside the validated range and must be treated with caution.

The fitted slope and intercept feed directly into Faraday's law to set volumetric H2 and O2 generation rates: ṅ_H2 = η_F × I / (2F) and ṅ_O2 = η_F × I / (4F), where F = 96 485 C mol⁻¹ and η_F is the Faradaic efficiency ([Faraday's laws of electrolysis, Wikipedia](https://en.wikipedia.org/wiki/Faraday%27s_laws_of_electrolysis)). A 1% error in current propagates directly to a 1% error in gas rate.

Electrode conditioning - gradual changes in surface state, oxide layer growth, and bubble coverage - causes the current at a fixed setpoint to drift during the first minutes of operation. All measurements must therefore follow a defined settling period.

## Optimal protocol (best accuracy)

Kit: a source-measure unit (SMU) or data-logging precision ammeter (e.g. Keithley 2400, or a Fluke 289 logging multimeter in series) with 4-wire connection to the electrolytic cell; the Pioreactor running the target reactor with the real electrolytic cell in place; a laptop or Raspberry Pi terminal for issuing setpoint commands; a thermometer to record electrolyte temperature; a timer.

1. Prepare the electrolytic cell with the same electrolyte concentration and volume that will be used in experiments. Record electrolyte composition and temperature at the start and end of each run.
2. Pre-condition the electrodes by running the cell at 15% intensity for 10 minutes before recording any calibration data. This stabilises the electrode surface and reduces drift in subsequent measurements.
3. Connect the SMU or logging ammeter in series with the electrolytic cell, observing correct polarity. A 4-wire (Kelvin) connection eliminates lead-resistance error ([Tektronix, measuring current with shunt resistors](https://www.tek.com/en/blog/measuring-current-using-shunt-resistors)).
4. Set the Pioreactor channel to the first intensity setpoint. Use the Python API (`from pioreactor.actions.led_intensity import led_intensity; led_intensity({'D': <value>})`) or the web UI to apply each setpoint ([Pioreactor Python scripting](https://docs.pioreactor.com/user-guide/intro-python-scripting)).
5. Allow 120 seconds of settling at each setpoint before recording. Monitor the current trace on the SMU display; record only once the drift rate falls below 0.5 mA min⁻¹.
6. Record the mean current (mA) over a 30-second logging window at each setpoint. Log at ≥ 1 Hz and report the mean and standard deviation.
7. Step through intensity setpoints: 1, 2, 3, 5, 7, 10, 13, 16, 20, 25, 28, 30%. This covers the validated range (3-25%), extends two points below (1, 2%) to characterise the extrapolated intercept region, and adds three points above (28, 30%) to test whether linearity holds outside the validated band.
8. Repeat the full sweep at least twice (two independent runs, re-conditioning between runs) and average the replicate currents at each setpoint.
9. Fit I (mA) vs intensity (%) by ordinary least squares. Report slope (mA %⁻¹), intercept (mA), R², and n. The validated range for the updated model is the span over which R² ≥ 0.998 and residuals show no systematic curvature.

## Budget protocol (minimal kit)

Kit: a precision low-value resistor (sense resistor, R_sense = 1 Ω ± 1%, rated for the expected current; wire-wound type preferred for stability); a digital multimeter (DMM) capable of reading millivolts (e.g. 4½-digit); connecting wire; the Pioreactor with the electrolytic cell; a timer.

The sense resistor is placed in series with the electrolytic cell, between the negative terminal and circuit ground. The voltage across it gives the current directly: I (mA) = V (mV) / R_sense (Ω) ([shunt resistor current measurement, Firgellauto](https://www.firgelliauto.com/blogs/engineering-calculators/current-sense-resistor-calculator-measuring-current-with-a-shunt); [Analog Devices AN-105](https://www.analog.com/en/resources/app-notes/an-105fa.html)).

1. Verify R_sense with the DMM in 4-wire ohms mode before installation. Record its measured resistance; use the measured value, not the nominal, in the I = V/R calculation.
2. Wire R_sense in series with the cell. Keep leads short and twisted to minimise inductive pickup. The voltage drop across R_sense at 30 mA is 30 mV, which is comfortably above DMM noise on the 200 mV range.
3. Pre-condition the electrodes at 15% intensity for 10 minutes before recording, as per the optimal protocol.
4. Set each intensity setpoint via the Pioreactor web UI. Allow 120 seconds of settling, then read the voltage across R_sense three times over 30 seconds and average. Convert to current: I = V_avg / R_sense.
5. Step through the same setpoints as above: 1, 2, 3, 5, 7, 10, 13, 16, 20, 25, 28, 30%.
6. Repeat the sweep on a separate day with a freshly prepared electrolyte batch to check inter-run reproducibility.
7. Fit I (mA) vs intensity (%) by least squares, as per step 9 of the optimal protocol.

Note: a 1% error in R_sense propagates directly to a 1% error in all currents. Use a resistor whose tolerance is known and measured; a cheap 5%-tolerance component is not adequate for a calibration that feeds the gas generation model.

## Result -> model

Enter the fitted coefficients directly into the Electrochemistry sheet:

- `gerrit_slope` (mA %⁻¹): the OLS slope.
- `gerrit_int` (mA): the OLS intercept.
- Update the validity band annotation (currently 3-25%) to reflect the range over which the new fit meets the acceptance criteria below.

The model computes H2 and O2 volumetric generation rates from gerrit_slope and gerrit_int via Faraday's law. If the new intercept differs substantially from zero, check whether the model's treatment of sub-3% operation (extrapolation vs. clamp-to-zero) needs revision - a negative extrapolated current has no physical meaning.

If you run the calibration at a different electrolyte temperature from the design condition, note that electrolyte conductivity (and hence cell current at fixed voltage) is temperature-dependent. Record the temperature and flag it alongside the coefficients.

## Acceptance checks & pitfalls

**R² < 0.995:** non-linearity in the I vs intensity relationship, possibly from electrolyte depletion, gas bubble occlusion on the electrodes, or thermal drift. Re-run after refreshing the electrolyte and check that the electrolyte temperature is stable (± 1 °C) across the sweep.

**Drift > 0.5 mA min⁻¹ after 120 s settling:** electrodes not yet conditioned, or the electrolyte is contaminated. Extend the pre-conditioning period or replace the electrolyte.

**Intercept < 0:** the fitted line implies negative current at zero intensity, which is unphysical. This usually means the lowest setpoints (1-2%) are genuinely at or below the channel's turn-on threshold and are pulling the intercept negative. Exclude sub-3% points and refit; flag the sub-threshold behaviour separately.

**Residuals showing curvature:** the true relationship may be sub-linear at high setpoints if the channel's PWM driver saturates. Restrict the validated range to the linear portion and note the saturation onset setpoint.

**Run-to-run scatter > 5% at mid-range (e.g. 15%):** check that the sense resistor or ammeter leads have not shifted. Re-seat connections and re-condition electrodes.

**Cross-check:** at 15% intensity, the model's current prediction from the prior gerrit_slope and gerrit_int should agree with your measured value within 5%. If it does not, the electrode assembly or electrolyte has changed from the original calibration; investigate before updating the model.

**Power budget:** at 3.3 V cell voltage and 30 mA, the cell dissipates ~0.1 W. The Pioreactor's LED/PWM channel is rated for limited continuous current ([Pioreactor external power docs](https://docs.pioreactor.com/user-guide/external-power)); confirm the channel's continuous current rating before running long calibrations at high setpoints.

## Sources

- [Faraday's laws of electrolysis - Wikipedia](https://en.wikipedia.org/wiki/Faraday%27s_laws_of_electrolysis)
- [Pioreactor LED automations documentation](https://docs.pioreactor.com/user-guide/led-automations)
- [Pioreactor Python scripting guide](https://docs.pioreactor.com/user-guide/intro-python-scripting)
- [Pioreactor: supplying more power to PWM channels](https://docs.pioreactor.com/user-guide/external-power)
- [Measuring current with shunt resistors - Tektronix](https://www.tek.com/en/blog/measuring-current-using-shunt-resistors)
- [Current sense resistor calculator - Firgelli Automation](https://www.firgelliauto.com/blogs/engineering-calculators/current-sense-resistor-calculator-measuring-current-with-a-shunt)
- [Analog Devices AN-105: Current sense circuit collection](https://www.analog.com/en/resources/app-notes/an-105fa.html)
- [LED controller linear constant-current control - All About Circuits](https://www.allaboutcircuits.com/news/LED-controller-linear-constant-current-control-high-current-diodes-inc/)
- [Quantitative electrolysis and Faraday's law - ScienceInfo](https://scienceinfo.com/quantitative-electrolysis/)
