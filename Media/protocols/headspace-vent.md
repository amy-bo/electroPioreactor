---
state: authored
author: [claude-sonnet-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "Headspace vent characterisation: outflow-only, open vent or air exchange, and the exchange flow"
sources:
  - https://www.presens.de/products/detail/self-adhesive-oxygen-sensor-spot-sp-pst3-sa
  - https://www.presens.de/products/detail/oxygen-sensor-spot-sp-pst8-yau
  - https://www.healthcarepackaging.com/machinery/inspection/press-release/13289741/protecting-oxygensensitive-goods
  - https://instrumentationdemo.yodify.com/Documentation/Document/g3KEp/manual-pressure-gauge-u-pipe-pum.pdf
  - https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6003363
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, vent, headspace, gas-exchange]
---

# Headspace vent characterisation

Decides which vent model is true (Outflow only, Open vent or Air exchange) and, for Air exchange, measures the exchange flow. This is the single highest-leverage open input: the model's CO2 pulse interval moves roughly 15 times across plausible vents (historical sensitivity examples: about 12.6 min for a check valve, about 9 min for an open vent, under 1 min for 0.5 mL/min exchange; not current commands). Do this protocol before the [headspace gas safety check](headspace-gas-safety.md).

## Before you start

- **Fix the known cap leak first** (note L8 on the CO2 flows sheet). A leaking cap is itself an air-exchange path and will be mistaken for the vent. Soap-test every cap seal, port fitting and septum (steps below) and reseal until none bubbles, with the vent port temporarily plugged.
- Vial: the real 20 mL vial with about 15 mL medium and the headspace left as built. Record the actual medium volume.
- Medium: the medium in use, at 30 C, stirrer at operating speed.
- **Electrolysis OFF** for the whole protocol, so no H2 or O2 is made. Gas exchange with the stirred liquid still occurs even with electrolysis off. Before interpreting O₂ return, demonstrate that liquid O₂ exchange is negligible over the measurement window, or use a coupled gas/liquid inventory model constrained by simultaneous DO and headspace measurements. A headspace sensor at its floor does not prove deoxygenated liquid.
- Make the medium CO2-equilibrated first: run the pulse schedule for 5 to 10 intervals before measuring. Otherwise fresh medium absorbs CO2 from the headspace, the headspace pressure falls, and that suction is mistaken for vent back-draw.
- Ventilate and keep naked flames away as normal good practice; no hydrogen is made in this protocol.

## Optimal protocol

Two measurements on the same vial: a pressure trace across pulses, and an optical O2 return after a CO2 fill.

### Kit

- A low-pressure transducer (bidirectional gauge/differential range covering expected positive and negative excursions, with resolution of 10 Pa or better on both sides of zero) with a short, small-bore tube to a spare headspace port, plus a logger at 1 Hz or faster. Keep the dead volume of the tube small against the few mL of headspace.
- An optical O2 sensor spot inside the headspace, read from outside through the glass (for example a PreSens self-adhesive spot SP-PSt3-SA, 0 to 100 % O2, or the 0 to 10 % SP-PSt8-YAU for better low-end resolution) and its reader. Stick the spot to the inside wall above the liquid line before sealing, clear of splash.
- The CO2 supply and solenoid exactly as in normal running.
- Soap solution (washing-up liquid in water) for the leak check.
- A second port plug or blank to close the vent port for the leak check.

### Reagents

- The medium in use.
- CO2 at the operating supply pressure.

### Method

1. Leak-check first. Plug the vent port. Pressurise the headspace gently by a CO2 pulse, brush soap solution on the cap seal, each port fitting and each septum, and watch for bubbles for 1 minute. Reseal anything that bubbles and repeat until nothing does. Then unplug the vent.
2. Fit the transducer tube to a spare headspace port and confirm that the reading is flat at ambient pressure when the vent is open and no pulse is firing. Zero-calibrate against ambient, verify response to both pressure signs without clipping, and record baseline drift per minute.
3. Equilibrate the medium with CO2 as described above.
4. Pressure trace. Log pressure at 1 Hz or faster through at least 5 full pulse intervals at the operating schedule (read and record Summary D14/D16 for ed04, MMO tube, Xanthobacter tagetidis, AMYBO03, 30 °C). For each pulse note: peak overpressure, time for the pressure to return to ambient, and any dip below ambient (underpressure) before the next pulse.
5. Interpret the pressure trace:
   - Pressure rises on the pulse and returns to ambient, with no dip below ambient afterwards: outflow-only or open vent; go to the O2 test to tell them apart.
   - Pressure returns to ambient and then sits below it between pulses, recovering slowly: record the pressure deficit and recovery time constant. This is consistent with possible ingress, but gas/liquid exchange also changes pressure; corroborate with the inventory and O₂ evidence before assigning back-draw or a leak.
   - Pressure stays above ambient long after the pulse (slow decay, minutes): the vent is restrictive or sticking. Record the decay time constant.
6. O2 return test. With the O2 spot reading, flush the headspace with CO2 until the O2 reading falls to its floor (repeat pulses by hand, or a longer hold-open of the solenoid, as the kit allows). Stop the CO2 and leave the vent as built. Log O2 (%) every 10 s for at least 60 minutes, with the pulse schedule switched OFF for this step while accounting for liquid O₂ exchange as required above. The sensor floor is a detection limit, not proof of zero O₂ inventory.
7. Repeat step 6 with the pulse schedule ON at the operating schedule, logging for at least 4 intervals, so you see O2 return under the real pulse pattern.
8. Interpret the O2 traces only after excluding or modelling liquid exchange and measurement disturbance; otherwise leave classification unresolved:
   - No O2 return in step 6 and none in step 7: supports Outflow only within detection limits.
   - No O2 return in step 6, but a small O2 rise after each pulse in step 7 (a step up in the 1 to 2 minutes after the pulse, then flat): Open vent. The step size gives the back-draw per pulse.
   - O2 climbs steadily in step 6, with no pulses: Air exchange (continuous).
9. Compute the exchange flow (Air exchange case). The gas-only washout applies only when liquid exchange is demonstrated negligible and the headspace is well mixed at effectively constant pressure, volume and temperature. Otherwise fit a validated coupled gas/liquid inventory model, not the gas-only log-slope. With negligible liquid exchange, use the measured initial fraction y₀: y(t) = y_air − (y_air − y₀) exp(−Qt/V). Regress ln[(y_air − y)/(y_air − y₀)] against time, avoiding readings near either sensor limit, and take Q = −V × slope. Use measured free-gas volume V in mL and time in minutes. Put y, y₀ and y_air on the same measured wet/dry basis (dry-air O₂ is about 0.2095); report Q on that basis and convert to the workbook flow reference before entry. Report fit uncertainty and at least three independent runs.
10. Back-draw estimate (Open vent case). After correcting for liquid exchange and pulse/measurement disturbances, a small O₂ step dy from initial fraction y_before supports the approximate ingress volume V × dy/(y_air − y_before), when ingress is small relative to V and pressure is effectively constant. The simpler V × dy/0.209 is justified only for nearly oxygen-free headspace on a dry basis. Otherwise use the finite gas-inventory balance. Divide a validated per-pulse ingress estimate by the recorded interval to obtain Q_backdraw and convert its reference basis before workbook entry.
11. Record the results (below).

### What to enter

- Summary D111 (named `vent_model_sel`): the selector. Choose "Outflow only", "Open vent" or "Air exchange" according to step 8.
- 'Mass Transfer'!D142 (`Q_vent`, mL/min): the measured bidirectional exchange flow from step 9. Enter only if you chose "Air exchange".
- 'Mass Transfer'!D385 (`Q_backdraw`, mL/min; currently 0.015): the back-draw from step 10. Enter only if you chose "Open vent", or if you found a small but measurable back-draw.
- Before entering a number, check the cell's colour and font convention in the sheet (column D font shows input versus formula); if the cell is a formula, ask the owner before overwriting.
- Note the date, the researcher, the reactor and the vent part number alongside the result.

## Budget protocol

No transducer and no optical spot. Slower and less quantitative; good enough to decide the selector, only coarse for Q_vent.

### Kit

- A water U-tube manometer (a clear flexible tube bent into a U on a ruler, half filled with water dyed with food colouring) joined by a short tube to a spare headspace port. It reads small pressures directly in mm of water.
- Soap solution and a small brush.
- A 1 mL and a 5 mL syringe, and a gastight syringe or a plastic syringe with a stopcock, for taking a headspace sample.
- A cheap O2 meter or a colorimetric O2 indicator that reads a few mL of gas (a breath-test style or small sampling O2 analyser), if available. If none is available, use pressure observations in steps 1–5 only; leave O₂-based classification and flow unresolved.
- A beaker of water and a short piece of tube for the inverted-cap bubble test.

### Reagents

- The medium in use; CO2; water and food colouring for the manometer.

### Method

1. Do the leak-check exactly as step 1 of the optimal route (plug the vent, soap all seals, fix leaks).
2. Inverted-cap bubble test of the vent direction. Connect the vent outlet by a short tube so its end sits 5 mm under water in a beaker. Fire one pulse. Watch: bubbles leaving the tube means outflow. After the pulse, record any water rising in the tube, its height and subsequent motion. This is liquid displacement in an altered, submerged-outlet configuration, not evidence of ambient-air ingress in normal operation. Restore the normal outlet and corroborate with gas/liquid inventory and O₂ evidence before assigning operating back-draw or a vent model.
3. Fit the U-tube manometer to a spare headspace port with the vent open and no pulse firing, and confirm both legs are level. Fire one pulse and note the peak difference in mm of water and how long until the legs are level again. Repeat for 5 pulses.
4. Watch the manometer for a dip below level between pulses (water drawn toward the vial): that establishes a pressure deficit, not its cause or a flow rate. Attribute back-draw or a leak only with corroborating gas/liquid inventory and O₂ evidence.
5. For continuous exchange, plug the manometer (not the vent) and leave the vent open with no pulses for 30 minutes. A steady level does not establish absence of exchange; this method cannot see exchange that is pressure-neutral, so go on to step 6.
6. Measure O₂ return after a CO₂ fill only with validated non-perturbing sensing, independent sacrificial runs (one terminal measurement per fresh run), or a validated gas-inventory model that accounts for every withdrawal, induced ingress and replacement. Repeated 1 mL samples materially disturb this few-mL headspace; adding CO₂ back also dilutes O₂. Simply noting the withdrawals does not correct the washout curve. Record the initial measured O₂ and the actual pulse history; compare pulse-off and real-schedule runs. If these measurement prerequisites cannot be met, leave the vent classification and Q_vent unresolved.
7. With valid measurements, use the selector criteria below: absence of a pressure dip and O₂ return supports Outflow only within detection limits; O₂ return tied to pulses supports Open vent; O₂ rising with no pulses supports Air exchange. Exclude sampling-induced ingress and demonstrate negligible liquid O₂ exchange, or correct it with the coupled inventory model, before assigning these interpretations.
8. For Air exchange, fit the optimal-route washout equation only to undisturbed or independent sacrificial measurements with negligible liquid exchange. For repeated withdrawals/replacements, fit the validated inventory model instead. Report measurement and fit uncertainty; no factor-of-two accuracy is assumed.
9. Record the results (below).

### What to enter

As for the optimal route: Summary D111; 'Mass Transfer'!D142 for Air exchange; 'Mass Transfer'!D385 for Open vent. State that the value came from the budget route.

## What the spreadsheet does with it

The vent selector (Summary D111, `vent_model_sel`) tells the model how gas leaves and enters the headspace. "Outflow only" is a check-valve vent: the headspace empties after each pulse and nothing returns, giving the longest pulse interval (about 12.6 min). "Open vent" lets a small amount of air be drawn back after each pulse, sized by `Q_backdraw` ('Mass Transfer'!D385) and is the default until measured (read Summary D16 for the selected configuration). "Air exchange" has air exchanged continuously at `Q_vent` ('Mass Transfer'!D142), which shortens the interval sharply and shifts the headspace O2 and the lag-phase H2 levels the model predicts. The choice therefore changes the headline CO2 schedule, the pH band check, and the lag-phase flammability check. Once you have the selector, re-read the lag-phase headspace predictions (Summary D125 for O2 and D126 for H2) before running the [headspace gas safety check](headspace-gas-safety.md).

## Principle and background

A vent is either a one-way valve, a restriction that equalises pressure, or a leak path that exchanges gas both ways. Pressure indicates a driving pressure difference; actual flow depends on the vent path and requires corroborating inventory or flow evidence. Oxygen return can indicate outside-air ingress only after residual dissolved O₂ release, subsequent liquid absorption, and sampling effects are excluded or modelled. Flushing a headspace does not by itself remove the liquid oxygen reservoir. The gas-only time constant V/Q assumes negligible liquid exchange; a coupled inventory is needed when the stirred liquid materially stores or releases oxygen. Pressure recovery likewise needs an actual trace: underpressure alone does not prove the direction or magnitude of subsequent flow.

Optical O2 spots read oxygen in the gas phase through the glass, without consuming oxygen, so they suit an undisturbed few-mL headspace. Water U-tube manometers read small pressures directly in mm of water. Bubble methods are used for leak detection, but very small leaks make bubble counts unreliable, which is why the budget route can decide the selector but gives only a coarse flow.

## Sources

- Optical oxygen spot for gas-phase measurement through the wall: [PreSens SP-PSt3-SA](https://www.presens.de/products/detail/self-adhesive-oxygen-sensor-spot-sp-pst3-sa); [PreSens SP-PSt8-YAU](https://www.presens.de/products/detail/oxygen-sensor-spot-sp-pst8-yau).
- Optical O2 sensing for headspace oxygen and closure tightness: [Healthcare Packaging – Protecting oxygen-sensitive goods](https://www.healthcarepackaging.com/machinery/inspection/press-release/13289741/protecting-oxygensensitive-goods).
- Water U-tube manometer for low pressures, read in mm of water: [KOBOLD PUM U-tube manometer manual](https://instrumentationdemo.yodify.com/Documentation/Document/g3KEp/manual-pressure-gauge-u-pipe-pum.pdf).
- Bubble leak detection and its small-leak limits: [US patent 6003363, Leak detection apparatus and method](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6003363).
