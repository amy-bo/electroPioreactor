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

## Optimal protocol

### Kit
- The Pioreactor running the target reactor, with the real electrolytic cell fitted and the same electrode assembly that experiments will use.
- A source-measure unit or data-logging precision ammeter (for example a Keithley 2400, or a Fluke 289 logging multimeter connected in series), capable of a 4-wire (Kelvin) connection to the cell.
- A laptop or Raspberry Pi terminal, or the Pioreactor web interface, for applying intensity setpoints.
- A thermometer to record electrolyte temperature.
- A timer.

### Reagents
- The working electrolyte, at the same composition and volume that experiments will use.

### Method
1. Prepare the cell with the working electrolyte at the composition and volume you will use in experiments. Record the electrolyte composition and its temperature.
2. Connect the ammeter (or source-measure unit) in series with the cell, observing correct polarity. Use a 4-wire connection so the meter leads do not add resistance to the reading.
3. Run the cell at 15% intensity for 10 minutes to pre-condition the electrodes. Do not record any calibration points during this period.
4. Set the Pioreactor channel to the first intensity setpoint in the sweep list below. Read the LED channel from the plugin configuration for this build; do not assume a fixed channel.
5. Wait 120 seconds at that setpoint before recording. Watch the current reading settle; only record once it has stopped drifting.
6. Record the steady current in milliamps at that setpoint, taken as the average over a 30-second window.
7. Move to the next setpoint and repeat steps 5 and 6. Work through the full sweep: 1, 2, 3, 5, 7, 10, 13, 16, 20, 25, 28, 30%.
8. Repeat the whole sweep at least once more as an independent run, re-conditioning the electrodes beforehand (step 3). Keep each run's points separate; do not merge them by hand.
9. Record the electrolyte temperature again at the end.
10. Record each (intensity %, measured current mA) pair in the **Gerrit current** section of the **Calibrations** tab - one row per point. Fill in Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit
- The Pioreactor with the electrolytic cell fitted, as above.
- A precision sense resistor of known, measured value (nominally 1 ohm, 1% tolerance, wire-wound type preferred for stability, rated for the expected current).
- A digital multimeter able to read millivolts (for example a 4.5-digit meter).
- Short connecting wire.
- A timer.

### Reagents
- The working electrolyte, at the same composition and volume that experiments will use.

### Method
1. Measure the sense resistor's resistance with the multimeter in 4-wire ohms mode before fitting it. Write down the measured value; use that measured value, not the printed nominal, whenever you convert a voltage reading to a current.
2. Wire the sense resistor in series with the cell, between the cell's negative terminal and circuit ground. Keep the leads short and twisted together.
3. Prepare the cell with the working electrolyte and record its composition and temperature.
4. Run the cell at 15% intensity for 10 minutes to pre-condition the electrodes. Do not record any points during this period.
5. Set the Pioreactor channel to the first intensity setpoint. Read the LED channel from the plugin configuration for this build; do not assume a fixed channel.
6. Wait 120 seconds, then read the voltage across the sense resistor three times over 30 seconds and average the three readings.
7. Convert that average voltage to a current: current in milliamps equals the average voltage in millivolts divided by the measured resistance in ohms. Note the resulting current for that setpoint.
8. Move to the next setpoint and repeat steps 6 and 7. Work through the full sweep: 1, 2, 3, 5, 7, 10, 13, 16, 20, 25, 28, 30%.
9. Repeat the whole sweep on a separate day with a freshly prepared electrolyte batch, keeping the runs separate.
10. Record each (intensity %, measured current mA) pair in the **Gerrit current** section of the **Calibrations** tab - one row per point. Fill in Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab fits a straight line of current against intensity to your recorded points, giving a slope and an intercept for the run. It averages those results across every included run for that reactor, and feeds the averaged slope and intercept into the electrolysis current law that sets the gas generation rates. You do not need to do any of this arithmetic by hand; just enter your measured points and mark them included.

## Principle & background

The Pioreactor controls its LED/PWM channels by a dimensionless intensity setpoint expressed as a percentage (0-100%). When a channel drives an electrolytic cell, the resulting current is not commanded directly; it is a consequence of the cell's electrochemistry and the channel's output at that setpoint. Gerrit's Law encodes the empirical relationship as a straight line: current (mA) equals a slope times intensity (%) plus an intercept.

The linear form follows from the roughly linear relationship between PWM duty cycle and mean output current for a resistive, or near-resistive, load, analogous to the way LED dimmer drivers hold linear current against duty-cycle ([Pioreactor LED automations docs](https://docs.pioreactor.com/user-guide/led-automations); [PWM-to-current linearity](https://www.allaboutcircuits.com/news/LED-controller-linear-constant-current-control-high-current-diodes-inc/)). The intercept captures any non-zero current that flows at very low setpoints due to power-supply floor effects or cell conditioning. The model has been validated over roughly the 3-25% band; extrapolation below 3% is outside that range and must be treated with caution, and a negative extrapolated current has no physical meaning.

The fitted slope and intercept feed Faraday's law to set volumetric H2 and O2 generation rates: the molar hydrogen rate is the Faradaic efficiency times current divided by two Faradays, and the molar oxygen rate is the Faradaic efficiency times current divided by four Faradays, with the Faraday constant 96 485 C mol-1 ([Faraday's laws of electrolysis, Wikipedia](https://en.wikipedia.org/wiki/Faraday%27s_laws_of_electrolysis); [quantitative electrolysis](https://scienceinfo.com/quantitative-electrolysis/)). A 1% error in current propagates directly to a 1% error in gas rate, which is why the measurement discipline matters.

Electrode conditioning - gradual changes in surface state, oxide-layer growth and bubble coverage - causes the current at a fixed setpoint to drift during the first minutes of operation, so every measurement follows a defined settling period. For the budget method, the sense resistor's accuracy sets the accuracy of every current: a 1% error in its resistance becomes a 1% error in all readings, so a cheap 5%-tolerance component is not adequate. A 4-wire connection (optimal method) or a short, twisted sense-resistor lead (budget method) keeps lead resistance and inductive pickup out of the reading ([Tektronix, shunt resistors](https://www.tek.com/en/blog/measuring-current-using-shunt-resistors); [Firgelli current-sense calculator](https://www.firgelliauto.com/blogs/engineering-calculators/current-sense-resistor-calculator-measuring-current-with-a-shunt); [Analog Devices AN-105](https://www.analog.com/en/resources/app-notes/an-105fa.html)).

Things to watch for. A poor straight-line fit points to non-linearity from electrolyte depletion, gas-bubble occlusion on the electrodes, or thermal drift; refresh the electrolyte and hold the temperature stable (within 1 degC) across the sweep. Continued drift after settling means the electrodes are not conditioned or the electrolyte is contaminated; extend conditioning or replace the electrolyte. If the lowest setpoints (1-2%) sit at or below the channel's turn-on threshold they can pull the fitted intercept negative; these sub-3% points characterise the extrapolated region but should be treated separately. Curvature at the top of the range can mean the PWM driver is saturating, in which case the trustworthy range is the linear portion. Electrolyte conductivity, and hence cell current at fixed voltage, is temperature-dependent, so record the temperature alongside the run. Finally, mind the power budget: at about 3.3 V and 30 mA the cell dissipates roughly 0.1 W, and the LED/PWM channel has a limited continuous-current rating - confirm that rating before long runs at high setpoints ([Pioreactor external power docs](https://docs.pioreactor.com/user-guide/external-power)).

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
