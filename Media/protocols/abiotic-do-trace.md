---
state: authored
author: [claude-sonnet-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "Abiotic dissolved-O2 trace under the model's schedule"
sources:
  - https://www.presens.de/products/detail/self-adhesive-oxygen-sensor-spot-sp-pst3-sa
  - https://patents.google.com/patent/US6330819
  - https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/
  - https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration
  - https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/
  - https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, dissolved-oxygen, abiotic, lag-phase, vent]
---

# Abiotic dissolved-O₂ trace under the model's schedule

One run with no cells. It measures the dissolved-oxygen sawtooth the model predicts for the lag phase, when there is no oxygen uptake and no hydrogen uptake, so the electrolytic oxygen has only two ways out: the CO₂ pulse and the free surface (via the vent). The shape of the trace tells you which parts of the model are wrong.

Conditions for the whole run: about 20 mL glass vial, about 15 mL of UdG phosphate medium (with CaCl₂ and NH₄⁺), cap sealed, CO₂ sparge line pulsed by the solenoid, Pt/Ti electrodes electrolysing at 3 % power, stirrer at 1000 rpm, 25 °C. Use the schedule exactly as it is entered on the Summary (Summary D14 is the pulse duration and D16 the interval; the model's schedule as typed is 0.65 s every 9 min). Read both cells on the day and write them in the run record; do not copy the numbers from this page.

## Optimal protocol

Best accuracy: a continuous optical trace through the vial wall.

### Kit

- An optical (luminescence-quenching) O₂ sensor spot adhered inside the vial wall below the liquid line, read through the glass from outside by a fibre and meter (for example a PreSens spot such as SP-PSt3-SA with its fibre meter, or a PyroScience spot with its meter). Optical is chosen because it consumes no oxygen and does not care about stirring. Fix the spot well clear of the stir-bar sweep and away from the electrodes, so that gas bubbles do not sit on it.
- A temperature probe or the meter's own temperature input. A barometer or the day's station pressure.
- A thermostatted bench or water bath that holds the vial at 25 °C throughout.
- The Pioreactor (or equivalent controller) running the real CO₂ sparge line, solenoid, electrodes and stirrer exactly as in service.
- A logger set to record DO, temperature and time stamp every 5 to 10 s. The pulse itself is under a second long, so also log the solenoid pulse times (or note the wall-clock time of the first pulse and rely on the controller log).
- Two clean calibration vessels (small beakers or vials) for the zero and span points.
- A fume-extracted or well-ventilated bench with no ignition sources (see the safety step).

### Reagents

- The medium in use (UdG phosphate medium with CaCl₂ and NH₄⁺), freshly made, no cells.
- For the zero point: a freshly made sodium sulphite (Na₂SO₃) solution, about 1 g per 100 mL of deionised water. Make it immediately before use because it re-oxygenates from air within hours. Cobalt(II) chloride is sometimes added to speed it up; it is a carcinogen, so leave it out unless you are an experienced user.
- For the span point: air-saturated water at the same temperature (stir deionised water open to air for at least 30 minutes, or bubble air through it).
- CO₂ from the line the reactor normally uses.

### Method

1. Record the day's settings first. Write down the Summary reactor and medium selections, the pulse duration (Summary D14) and interval (Summary D16), the power (3 %), the stirrer speed (1000 rpm), the station pressure and the sensor model. Stop and tell the model owner if D14 or D16 shows an error rather than a number: the reactor then needs its CO₂ flow calibration first ([flow-calibration.md](flow-calibration.md)).
2. Calibrate the sensor spot at two points, at 25 °C, before the vial is filled.
   a. Zero: put the sensor (or a spare identical spot, if your spot is fixed in the run vial) in the freshly made sulphite solution, stir, wait 2 to 3 minutes until the reading is low and stable, and set the zero.
   b. Span: put the sensor in air-saturated water at 25 °C, wait until stable, enter the temperature and the station pressure, and set 100 % air saturation.
   c. If the spot is permanently glued into the run vial, do the zero and span in that same vial before the run: fill with sulphite, calibrate zero, rinse three times with deionised water, fill with air-saturated water, calibrate span, then rinse and empty. Check the sulphite is completely rinsed out, since any remaining sulphite will consume oxygen in the run.
3. Cross-check the span: at 25 °C and about 1 atm, fresh water that is 100 % air-saturated holds about 8.26 mg/L (see the Fondriest table in Sources); the medium's salts lower it a little. Write down the number your meter reports for the span, so that the conversion between per cent saturation and mg/L is the same one you use later.
4. Fill the vial with 15 mL of medium (the working volume used on the Summary). Fit the cap, electrodes, sparge line and vent exactly as in service. Do not leave any extra opening, and do not add a headspace tube, because the vent behaviour is one of the things being tested.
5. **Safety before electrolysis.** With no cells, nothing consumes the hydrogen, so the headspace is a flammable H₂/O₂ mix diluted only by the CO₂ pulses; the model (TODO.md, wave 5) puts it near 11 % H₂ on average and about 18 % just before each pulse, which is above the 4 % lower flammability limit. Run in a ventilated place, away from any flame, spark or hot surface. Do not block the vent. Do not open the vial while current is flowing; switch the electrolysis off first and wait at least one pulse interval. Wear eye protection.
6. Equilibrate with no electrolysis. Start the stirrer at 1000 rpm and hold 25 °C for at least 30 minutes with no CO₂ pulses and no current, until the DO reading is flat. This baseline should sit close to air saturation. Log it. If it drifts steadily, there is a sensor, temperature or leak problem; fix that before continuing.
7. Start the run. Start the logger. Then at one instant start the CO₂ pulse schedule and the 3 % electrolysis together, and write down the clock time as time zero. Do not touch the vial, cap or fibre again for the whole run.
8. Run for at least 6 hours. The trace first falls or rises away from the baseline while the liquid saturates with CO₂ (the model's review puts that at about an hour), and then settles into a repeating sawtooth: a rise between pulses as electrolytic O₂ builds, and a drop after each pulse. Keep going until you have at least 10 full cycles after the sawtooth has settled (at a 9 min interval, at least 90 minutes of settled trace). It has settled when the cycle-to-cycle shift in the just-before-pulse peak is smaller than the sensor's noise, judged by eye on 3 consecutive cycles.
9. End the run. Switch off the electrolysis first, leave the CO₂ pulses and logging running for a further 30 minutes so that you can see the decay back towards the baseline, then stop the logger and the pulses.
10. Re-check the span: put the sensor back in air-saturated water at 25 °C (repeat step 2b). If the reading has moved by more than the sensor's stated accuracy, mark the whole run as drifted and repeat it.
11. Analyse the trace. Use only the settled cycles from step 8.
    a. Cycle mean: the average DO over exactly a whole number of complete cycles (from one pulse to the pulse N cycles later), converted to mg/L. Use at least 10 cycles.
    b. Peak: for each cycle, the highest value just before the next pulse. Average those peaks over the same cycles.
    c. Amplitude: the peak minus the minimum just after the pulse, averaged. Also note the time taken from the pulse to the minimum.
    d. Note the spread (standard deviation) of each over the cycles used.
12. Compare with the model. Read, on the same day and with the same Summary selections, the lag-phase predictions: Summary D116 (cycle-mean DO in the lag phase, about 4.7 mg/L when this page was written) and Summary D117 (peak DO in the lag phase, about 5.7 mg/L). Tabulate model, measured, and the difference as a percentage. Record the temperature and pressure at which the sensor was calibrated and at which the run was done.
13. Record the numbers in the TODO.md measurement entry or the run notes: raw trace file name, cycle mean, peak, amplitude, Summary D14, D16, D111 (the vent selection), D116 and D117 as read on the day. These are comparison values only; the Calibrations tab has no section for them yet, and the workbook must not be edited by this protocol.

## Budget protocol

A handheld probe (polarographic or optical) sampled at fixed times in the cycle, because a continuous trace is not available.

### Kit

- A handheld dissolved-oxygen meter with a small probe that fits the vial opening or the cap's needle gap. Check the probe tip is narrow enough that the cap can still seal around it. Note the type: a polarographic (Clark) probe consumes oxygen and needs flow across the membrane; an optical probe does not.
- A stopwatch or a phone with a clock, and the same thermostatted bench or water bath and CO₂ line as the optimal route.
- Enough identical vials to sacrifice (see the method). A single vial opened repeatedly will not give a clean trace.

### Reagents

As in the optimal route, but you can skip the sulphite zero if you accept reduced accuracy at the low end; the span in air-saturated water is the essential point.

### Method

1. Record the day's settings as in step 1 of the optimal route, and calibrate the meter at 25 °C: span in air-saturated water, zero in fresh sulphite if you have it. Enter the temperature and station pressure on the meter.
2. Decide the sampling times. Take the time of the last pulse as zero within a cycle. Choose 5 points per cycle, for example immediately before the pulse, then about 1 minute after it, and then evenly across the remaining interval. Use the same five times in every sampled cycle.
3. Because every reading disturbs the vial, use one of two arrangements.
   a. A set of identical vials started together, each run to the same total time and then read once or twice, then discarded. Use this if you can, since each reading is then free of earlier disturbance.
   b. One vial with a probe permanently in the cap seal, read in place without lifting the cap. This is cleaner, but only works if the probe fits through a port without letting air in.
4. Follow steps 4 to 9 of the optimal route for filling, safety, equilibration and starting the run. The same safety rules apply: stop the electrolysis and wait one interval before opening any vial.
5. Take the readings in at least 10 cycles after the sawtooth has settled. Allow the probe to stabilise (a polarographic probe typically needs 30 s to a few minutes; follow its manual). Note that a polarographic probe in a 15 mL vial removes a measurable amount of oxygen and reads low unless the liquid is stirred across the membrane. Hold the stirrer at 1000 rpm and wait for the reading to hold steady before writing it down.
6. Remember each reading perturbs the system: the opening lets in air and lets out the headspace gas, which resets the vent and headspace state, and the probe adds its own oxygen draw. Discard the first cycle after each opening, and if you used one vial, treat the result as a lower-confidence estimate of the peak and mean.
7. Plot DO against time within the cycle and average the points at the same position across cycles. Use the highest of the five points as the peak, and the average of all five as a rough cycle mean (it is weighted by where you chose to sample, so quote it as provisional).
8. Compare with Summary D116 and D117 exactly as in step 12 of the optimal route. Record the probe type alongside, since a polarographic probe can bias the mean low.
9. Check the span again at the end (step 10 of the optimal route).

## Temperature, pressure and calibration notes

- Run at 25 °C. Oxygen solubility changes by roughly 2 % per degree in this range, so a 1 °C error in the bath shifts every mg/L number by about the same amount. Hold the bath steady to ±0.2 °C and let the sensor read the temperature of the liquid, not the room.
- Enter the real station pressure on the meter and on the Summary's ambient-pressure cell. The model's default is 101325 Pa; a 1 % pressure change is a 1 % change in saturation DO.
- Optical sensors report per cent saturation or oxygen partial pressure; converting to mg/L still needs the temperature and the medium's solubility. Use the same conversion for the model and the measurement, otherwise the comparison with D116 and D117 will carry an artificial offset.
- Calibrate at the start and re-check the span at the end. A two-point calibration (zero in sulphite, 100 % in air-saturated water) is the standard approach; a single-point (air only) calibration is the budget fallback and loses accuracy at low DO.
- The model's lag-phase predictions sit around 57 % and 69 % of air saturation. Both are inside the calibrated range, so no extrapolation is needed.
- Check the sensor spot manufacturer's datasheet for compatibility with chlorine and peroxide-type oxidants, which the electrolysis produces in the medium. A spot that drifts during the run, shown by the end-of-run span check, is a failed run.

## What the spreadsheet does with it

Nothing, directly: there is no Calibrations section for this trace yet, and this protocol does not edit the workbook. Read the measurement against two model outputs and use the pattern of the mismatch to choose the next measurement.

- Cycle-mean DO against Summary D116, and peak DO against Summary D117. Both come from the model's closed-form sawtooth in the lag phase (no uptake), which depends on the vent model chosen in Summary D111, the surface kLa and the electrolytic oxygen generation.
- Mean too low (measured mean well below D116): oxygen is leaving faster than the model assumes. The first suspect is the vent model (D111), for example a leak or a plain open vent that exchanges more gas than the model allows; the second is a surface kLa larger than the model's penetration-theory proxy. Check the cap for leaks, then run [surface-kla.md](surface-kla.md).
- Mean too high (measured mean well above D116): oxygen is leaving more slowly than the model assumes. Suspect a check-valve-like vent (outflow only) rather than the plain open vent, a surface kLa smaller than the proxy. A faradaic efficiency different from the assumed value shifts the oxygen source and so also moves the mean (see [faradaic-efficiency.md](faradaic-efficiency.md)).
- Sawtooth amplitude (peak minus trough) wrong while the mean is about right: this points at the surface kLa, because the speed of the decay after a pulse is set mainly by how quickly oxygen is transferred out through the surface. A larger amplitude than predicted means a slower surface transfer; a smaller one means faster.
- If the mean and the amplitude are both off in the same direction, change the vent assumption first (it is the highest-leverage open input in TODO.md) and re-compare before touching the kLa.
- Peak against D117 matters most for the oxygen-impairment test, since the peak sets the worst-case DO the cells would see. Quote it with its spread.

## Principle & background

In the lag phase the culture takes up nothing, so the oxygen made at the anode builds up in the liquid. It leaves by two routes: stripped by the CO₂ pulse, and diffusing across the free surface into a headspace that is vented. The model describes this as a repeating sawtooth: DO rises between pulses at the rate electrolysis adds oxygen, and falls after each pulse. Because the surplus is a small difference between two large flows, the answer is sensitive to the vent behaviour (Summary D111) and the surface kLa; the model's review reports the interval moving by over an order of magnitude across plausible vents. The abiotic run isolates these two from the biology: with no cells there is nothing else to change. One run therefore tests the vent hypotheses and the lag-phase predictions together.

Why optical: a luminescence-quenching spot consumes no oxygen and is not affected by stirring, whereas a Clark-type electrode consumes oxygen and is flow-dependent, which in a 15 mL vial is a real error source. The spot is also small enough to be read through the vial wall without any extra port.

Why the long run: CO₂ must first saturate the liquid before it begins to behave as the model assumes, so the early part of the trace is a transient. Only the settled limit cycle is compared with the model.

The same caveats as in [dissolved-oxygen.md](dissolved-oxygen.md) apply: calibration before every run is the largest single error source, and the zero and span points should be recorded with each trace.

## Sources

- Optical sensor spot, range and two-point calibration: [PreSens SP-PSt3-SA oxygen sensor spot](https://www.presens.de/products/detail/self-adhesive-oxygen-sensor-spot-sp-pst3-sa).
- Sodium sulphite zero for dissolved-oxygen calibration (general method, not specific to optical spots): [US patent 6330819, Method and apparatus for calibrating a dissolved oxygen analyzer](https://patents.google.com/patent/US6330819).
- DO calibration practice: [Hamilton, DO sensor calibration](https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration); [US EPA, Dissolved oxygen QA bulletin](https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf).
- Air-saturation solubility versus temperature and pressure: [Fondriest, Dissolved Oxygen](https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/).
- Optical versus Clark sensors: [Optical Oxygen Sensing and Clark Electrode: Face-to-Face in a Biosensor Case Study (PMC9572888)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/); [USGS, Field Comparison of Optical and Clark Cell Dissolved Oxygen Sensors](https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf).
