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

Conditions for the whole run: ed04 at the recorded working volume, chloride-free AMYBO03, no cells (abiotic counterpart of the *Xanthobacter tagetidis* baseline), MMO tube assembly, 30 °C, recorded operating power and stirring. Read and record Summary D19 (pulse duration, s) and D21 (interval, min) with these selections; do not copy fixed commands.

## Optimal protocol

Best accuracy: a continuous optical trace through the vial wall.

### Kit

- An optical (luminescence-quenching) O₂ sensor spot adhered inside the vial wall below the liquid line, read through the glass from outside by a fibre and meter (for example a PreSens spot such as SP-PSt3-SA with its fibre meter, or a PyroScience spot with its meter). Optical is chosen because it consumes no oxygen and does not care about stirring. Fix the spot well clear of the stir-bar sweep and away from the electrodes, so that gas bubbles do not sit on it.
- A temperature probe or the meter's own temperature input. A barometer or the day's station pressure.
- A thermostatted bench or water bath that holds the vial at 30 °C throughout.
- The Pioreactor (or equivalent controller) running the real CO₂ sparge line, solenoid, electrodes and stirrer exactly as in service.
- A logger set to record DO, temperature and time stamp every 5 to 10 s. The pulse itself is under a second long, so also log the solenoid pulse times (or note the wall-clock time of the first pulse and rely on the controller log).
- Two clean calibration vessels (small beakers or vials) for the zero and span points.
- A fume-extracted or well-ventilated bench with no ignition sources (see the safety step).

### Reagents

- The medium in use (chloride-free AMYBO03), freshly made, no cells.
- For the zero point: a freshly made sodium sulphite (Na₂SO₃) solution, about 1 g per 100 mL of deionised water. Make it immediately before use because it re-oxygenates from air within hours. Cobalt(II) chloride is sometimes added to speed it up; it is a carcinogen, so leave it out unless you are an experienced user.
- For the span point: air-saturated water at the same temperature (stir deionised water open to air for at least 30 minutes, or bubble air through it).
- CO₂ from the line the reactor normally uses.

### Method

1. Record the day's settings first. Write down the Summary reactor and medium selections, the pulse duration (Summary D19) and interval (Summary D21), the recorded power and stirrer speed, the station pressure and the sensor model. Stop and tell the model owner if D19 or D21 shows an error rather than a number: the reactor then needs its CO₂ flow calibration first ([flow-calibration.md](flow-calibration.md)).
2. Calibrate the sensor spot at two points, at 30 °C, before the vial is filled.
   a. Zero: put the sensor (or a spare identical spot, if your spot is fixed in the run vial) in the freshly made sulphite solution, stir, wait 2 to 3 minutes until the reading is low and stable, and set the zero.
   b. Span: put the sensor in air-saturated water at 30 °C, wait until stable, enter the temperature and the station pressure, and set 100 % air saturation.
   c. If the spot is permanently glued into the run vial, do the zero and span in that same vial before the run: fill with sulphite, calibrate zero, rinse three times with deionised water, fill with air-saturated water, calibrate span, then rinse and empty. Check the sulphite is completely rinsed out, since any remaining sulphite will consume oxygen in the run.
3. Cross-check the span: at 30 °C and about 1 atm, fresh water that is 100 % air-saturated holds about 7.54 mg/L (see the Fondriest table in Sources); the medium's salts lower it a little. Write down the number your meter reports for the span, so that the conversion between per cent saturation and mg/L is the same one you use later.
4. Fill the vial to the recorded working volume used on the Summary. Fit the cap, electrodes, sparge line and vent exactly as in service. Do not leave any extra opening, and do not add a headspace tube, because the vent behaviour is one of the things being tested.
5. **Safety before electrolysis.** With no cells, nothing consumes hydrogen. Read Summary D70 (lag O₂) and D71 (mean lag H₂) with the recorded selections; treat the headspace as potentially flammable. Normal CO₂ pulses dilute gases but do not establish inerting. Ventilate, exclude ignition sources, keep the vent open, switch electrolysis off before opening and wear eye protection. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance. See [headspace-gas-safety.md](headspace-gas-safety.md); its thresholds are a hazard screen, not certification.
6. Equilibrate with no electrolysis. Start the stirrer at the recorded operating speed and hold 30 °C for at least 30 minutes with no CO₂ pulses and no current, until the DO reading is flat. This baseline should sit close to air saturation. Log it. If it drifts steadily, there is a sensor, temperature or leak problem; fix that before continuing.
7. Start the run. Start the logger. Then at one instant start the CO₂ pulse schedule and the recorded operating electrolysis power together, and write down the clock time as time zero. Do not touch the vial, cap or fibre again for the whole run.
8. Run for at least 6 hours. The trace first falls or rises away from the baseline while the liquid saturates with CO₂ (the model's review puts that at about an hour), and then settles into a repeating sawtooth: a rise between pulses as electrolytic O₂ builds, and a drop after each pulse. Keep going until you have at least 10 full cycles after the sawtooth has settled (at least 10 × Summary D21 minutes of settled trace). It has settled when the cycle-to-cycle shift in the just-before-pulse peak is smaller than the sensor's noise, judged by eye on 3 consecutive cycles.
9. End the run. Switch off the electrolysis first, leave the CO₂ pulses and logging running for a further 30 minutes so that you can see the decay back towards the baseline, then stop the logger and the pulses. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance.
10. Re-check the span: put the sensor back in air-saturated water at 30 °C (repeat step 2b). If the reading has moved by more than the sensor's stated accuracy, mark the whole run as drifted and repeat it.
11. Analyse the trace. Use only the settled cycles from step 8.
    a. Cycle mean: the average DO over exactly a whole number of complete cycles (from one pulse to the pulse N cycles later), converted to mg/L. Use at least 10 cycles.
    b. Peak: for each cycle, the highest value just before the next pulse. Average those peaks over the same cycles.
    c. Amplitude: the peak minus the minimum just after the pulse, averaged. Also note the time taken from the pulse to the minimum.
    d. Note the spread (standard deviation) of each over the cycles used.
12. Compare with the model. Read, on the same day and with the same Summary selections, the lag-phase predictions: Summary D61 (cycle-mean DO in the lag phase) and Summary D62 (peak DO in the lag phase). Tabulate model, measured, and the difference as a percentage. Record the temperature and pressure at which the sensor was calibrated and at which the run was done.
13. Record the numbers in the TODO.md measurement entry or the run notes: raw trace file name, cycle mean, peak, amplitude, Summary D19, D21, D11 (the vent selection), D61 and D62 as read on the day. These are comparison values only; the Calibrations tab has no section for them yet, and the workbook must not be edited by this protocol.

## Budget protocol

A handheld probe (polarographic or optical) sampled at fixed times in the cycle, because a continuous trace is not available.

### Kit

- A handheld dissolved-oxygen meter with a small probe that fits the vial opening or the cap's needle gap. Check the probe tip is narrow enough that the cap can still seal around it. Note the type: a polarographic (Clark) probe consumes oxygen and needs flow across the membrane; an optical probe does not.
- A stopwatch or a phone with a clock, and the same thermostatted bench or water bath and CO₂ line as the optimal route.
- Enough identical vials to sacrifice (see the method). A single vial opened repeatedly will not give a clean trace.

### Reagents

As in the optimal route, but you can skip the sulphite zero if you accept reduced accuracy at the low end; the span in air-saturated water is the essential point.

### Method

1. Record the day's settings as in step 1 of the optimal route, and calibrate the meter at 30 °C: span in air-saturated water, zero in fresh sulphite if you have it. Enter the temperature and station pressure on the meter.
2. Decide the sampling times. Take the time of the last pulse as zero within a cycle. Choose 5 points per cycle, for example immediately before the pulse, then about 1 minute after it, and then evenly across the remaining interval. Use the same five times in every sampled cycle.
3. Because every reading disturbs the vial, use one of two arrangements.
   a. A set of identical vials started together, each read once at a specified cycle phase. This is usable only if an owner-approved sampling/clearance arrangement preserves the quantity being measured; opening after clearance can change DO and cannot be treated as an undisturbed phase reading. Otherwise use a sealed in-place probe.
   b. One vial with a probe permanently in the cap seal, read in place without lifting the cap. This is cleaner, but only works if the probe fits through a port without letting air in.
4. Follow steps 4 to 9 of the optimal route for filling, safety, equilibration and starting the run. The same safety rules apply: stop electrolysis before opening any vial. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance.
5. Take the readings in at least 10 cycles after the sawtooth has settled. Allow the probe to stabilise (a polarographic probe typically needs 30 s to a few minutes; follow its manual). Note that a polarographic probe in a 15 mL vial removes a measurable amount of oxygen and reads low unless the liquid is stirred across the membrane. Hold the stirrer at the recorded operating speed and wait for the reading to hold steady before writing it down.
6. Use the validated sacrificial-sampling arrangement or a sealed probe specified above. Clearance, opening or probe insertion can change gas composition and DO; do not assume one discarded cycle restores the original state. Subsequent phase measurements require demonstrated recovery under the recorded conditions.
7. Plot DO against time within the cycle and average the points at the same position across cycles. Use the highest sampled value as a provisional peak; estimate a cycle mean by time-weighted integration over the recorded phases and report sampling and probe-lag uncertainty. An unweighted average of unequally spaced phases is not a time mean.
8. Compare with Summary D61 and D62 exactly as in step 12 of the optimal route. Record the probe type alongside, since a polarographic probe can bias the mean low.
9. Check the span again at the end (step 10 of the optimal route).

## Temperature, pressure and calibration notes

- Run at 30 °C. Oxygen solubility changes by roughly 2 % per degree in this range, so a 1 °C error in the bath shifts every mg/L number by about the same amount. Hold the bath steady to ±0.2 °C and let the sensor read the temperature of the liquid, not the room.
- Enter the real station pressure on the meter and on the Summary's ambient-pressure cell. The model's default is 101325 Pa; a 1 % pressure change is a 1 % change in saturation DO.
- Optical sensors report per cent saturation or oxygen partial pressure; converting to mg/L still needs the temperature and the medium's solubility. Use the same conversion for the model and the measurement, otherwise the comparison with Summary D61 and Summary D62 will carry an artificial offset.
- Calibrate at the start and re-check the span at the end. A two-point calibration (zero in sulphite, 100 % in air-saturated water) is the standard approach; a single-point (air only) calibration is the budget fallback and loses accuracy at low DO.
- Convert the recorded Summary D61/D62 predictions to per cent air saturation using the measured 30 °C span (fresh-water example: 100 × DO / 7.54 mg/L at about 1 atm). Use the medium- and pressure-corrected span for the actual comparison and check the calibration range.
- Check the sensor spot manufacturer's datasheet for compatibility with chlorine and peroxide-type oxidants, which the electrolysis produces in the medium. A spot that drifts during the run, shown by the end-of-run span check, is a failed run.

## What the spreadsheet does with it

Nothing, directly: there is no Calibrations section for this trace yet, and this protocol does not edit the workbook. Read the measurement against two model outputs and use the pattern of the mismatch to choose the next measurement.

- Cycle-mean DO against Summary D61, and peak DO against Summary D62. Both come from the model's closed-form sawtooth in the lag phase (no uptake), which depends on the vent model chosen in Summary D11, the surface kLa and the electrolytic oxygen generation.
- Mean too low (measured mean well below Summary D61): the headspace holds less O₂, or the liquid sheds it more easily, than the model assumes. Suspects: less air drawn back through the vent than `Q_backdraw` assumes (air ingress pushes the headspace towards 21 % O₂, so in this abiotic run more ingress raises DO, not lowers it), a surface kLa larger than the model's penetration-theory proxy, or a smaller O₂ source (faradaic efficiency). Run [surface-kla.md](surface-kla.md) and the vent back-draw measurement before adjusting either.
- Mean too high (measured mean well above Summary D61): more air is drawn back than assumed, or the surface sheds O₂ more slowly. Suspect a larger vent back-draw or a leak admitting air, or a surface kLa smaller than the proxy. A faradaic efficiency different from the assumed value shifts the oxygen source and so also moves the mean (see [faradaic-efficiency.md](faradaic-efficiency.md)).
- Sawtooth amplitude (peak minus trough) wrong while the mean is about right: this points at the surface kLa, because the liquid follows the headspace sawtooth only as fast as the surface transfers O₂. A larger amplitude than predicted means faster surface transfer (the liquid tracks the headspace swing more closely); a smaller one means slower. Read this against the recorded vent and schedule, since the headspace swing itself depends on both.
- If the mean and the amplitude are both off in the same direction, change the vent assumption first (it is the highest-leverage open input in TODO.md) and re-compare before touching the kLa.
- Peak against Summary D62 matters most for the oxygen-impairment test, since the peak sets the worst-case DO the cells would see. Quote it with its spread.

## Principle & background

In the lag phase the culture takes up nothing, so the oxygen made at the anode builds up in the liquid. It leaves by two routes: stripped by the CO₂ pulse, and diffusing across the free surface into a headspace that is vented. The model describes this as a repeating sawtooth: DO rises between pulses at the rate electrolysis adds oxygen, and falls after each pulse. Because the surplus is a small difference between two large flows, the answer is sensitive to the vent behaviour (Summary D11) and the surface kLa; the model's review reports the interval moving by over an order of magnitude across plausible vents. The abiotic run isolates these two from the biology: with no cells there is nothing else to change. One run therefore tests the vent hypotheses and the lag-phase predictions together.

Why optical: a luminescence-quenching spot consumes no oxygen and is not affected by stirring, whereas a Clark-type electrode consumes oxygen and is flow-dependent, which in a 15 mL vial is a real error source. The spot is also small enough to be read through the vial wall without any extra port.

Why the long run: CO₂ must first saturate the liquid before it begins to behave as the model assumes, so the early part of the trace is a transient. Only the settled limit cycle is compared with the model.

The same caveats as in [dissolved-oxygen.md](dissolved-oxygen.md) apply: calibration before every run is the largest single error source, and the zero and span points should be recorded with each trace.

## Sources

- Optical sensor spot, range and two-point calibration: [PreSens SP-PSt3-SA oxygen sensor spot](https://www.presens.de/products/detail/self-adhesive-oxygen-sensor-spot-sp-pst3-sa).
- Sodium sulphite zero for dissolved-oxygen calibration (general method, not specific to optical spots): [US patent 6330819, Method and apparatus for calibrating a dissolved oxygen analyzer](https://patents.google.com/patent/US6330819).
- DO calibration practice: [Hamilton, DO sensor calibration](https://www.hamiltoncompany.com/process-analytics/dissolved-oxygen-knowledge/calibration-and-maintenance-for-oxygen-sensors/do-sensor-calibration); [US EPA, Dissolved oxygen QA bulletin](https://www.epa.gov/sites/default/files/2015-06/documents/DissolvedOxygenQABulletinfinal.pdf).
- Air-saturation solubility versus temperature and pressure: [Fondriest, Dissolved Oxygen](https://www.fondriest.com/environmental-measurements/parameters/water-quality/dissolved-oxygen/).
- Optical versus Clark sensors: [Optical Oxygen Sensing and Clark Electrode: Face-to-Face in a Biosensor Case Study (PMC9572888)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572888/); [USGS, Field Comparison of Optical and Clark Cell Dissolved Oxygen Sensors](https://pubs.usgs.gov/of/2006/1047/pdf/ofr2006-1047.pdf).
