---
state: authored
author: [claude-opus-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "pH through a growth run: tests the acid released by nitrogen uptake"
sources:
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2758785/
  - https://www.hamiltoncompany.com/process-analytics/ph-and-orp-knowledge/ph-sensor-calibration
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, ph, nitrogen, growth]
---

# pH through a growth run

The workbook predicts that the pH falls as the culture grows on ammonium. Each ammonium ion taken up releases one H⁺, and the model works out the end-of-run pH from the biomass at the end of the run. That biomass is Summary row 17 (X_end_gL), and the end-of-run pH is Summary row 28 (res_pH_end). The workbook also compares the medium options in Summary rows 64–67: nitrate uptake consumes acid, and urea uptake neither releases nor consumes it.

This run tests those predictions, and the assumed biomass nitrogen content (11.4 %, Chemistry D335), against a real culture.

Conditions:
- Run the schedule from Summary rows 21–22, with the organism, medium, reactor and temperature selected on the Summary.
- Record the nitrogen source (Summary row 16).

## Optimal protocol

**Kit:**
- A pH probe that fits the vial without touching the stir bar or the electrodes. A micro combination electrode is suitable, or an optical pH spot read through the wall.
- Two-point calibration buffers bracketing the band: pH 4 and 7, or 7 and 10. Take them to the run temperature.
- The Pioreactor OD readings, plus three dry-weight samples so OD can be converted to g/L dry weight.

**Steps:**
1. Calibrate the probe at the run temperature. Record the slope; reject the probe if the slope is below 95 %.
2. Start the run and log pH every 10 minutes. Note when each pulse happens, because pH dips just after a CO₂ pulse; use the mean over a whole cycle.
3. At three points through the run (early, middle, end), take a small sample for dry weight and record the matching OD.
4. At the end, recheck the probe against the pH 7 buffer. A drift of more than 0.05 means the trace must be drift-corrected, or the run repeated.

**Analysis:**
1. Convert OD to dry weight with the three samples.
2. Plot cycle-mean pH against biomass. With ammonium the model predicts a near-straight fall. Its slope is −f_N/(14.007 × β), where f_N is the biomass nitrogen fraction (0.114, Chemistry D335) and β is the open-system buffer capacity at today's dissolved CO₂.
3. Enter the final biomass on Summary row 17 and compare Summary row 28 with the measured final pH.

**Acceptance:**
- The start-of-run pH should match Summary row 27 within 0.05. If it doesn't, check the medium and the schedule before reading anything else.
- The end-of-run pH should match within 0.05.
- If the measured fall is consistently larger or smaller than predicted, fit f_N to it. Record the fit in the Calibrations experiment record (Result Done, with the organism, medium and temperature filled).

## Cheapest protocol

Take start and end samples to a bench pH meter, measured at the run temperature. Record the final OD and one dry weight.

This tests the end-of-run prediction only. Record it in the experiment record as Approximate.
