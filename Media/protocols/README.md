---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "electroPioreactor experiment protocols"
sources:
  []
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, index]
---

# electroPioreactor experiment protocols

Standalone instructions for the bench experiments that determine the measured / assumed parameters in `electroPioreactorGasModel-modular.xlsx`. Run these to replace the model's default and data-gap (pink) values with measured ones and get optimal figures for everything. Each protocol gives an **optimal** route (best accuracy, more kit) and a **budget** route (minimal kit, stated accuracy trade-off), and states exactly which model cell to enter the result in.

Work top-to-bottom: the order is by leverage (blocker first, then the model's own ranked-improvement priority). The model has live gates that tell you when a measurement has cleared its problem: the Geometry consistency check, and the `kL_surf_crit` threshold on Mass Transfer.

| # | Experiment | Protocol | Feeds (model cell) | Current state | Why it's here |
|---|-----------|----------|--------------------|---------------|----------------|
| 0 | Vial geometry & true headspace | [vial-geometry.md](vial-geometry.md) | Geometry: `V_vial_total`, `A_x`, `D_int`, `vial_ID` | **INCONSISTENT** (20 mL nominal vs ~27.6 mL cylinder) | **Blocker B1** – headline optimal pulse is ~4x sensitive to headspace; clears the `geom_check` flag |
| 1 | Surface O2 transfer (kL_surf) | [surface-kla.md](surface-kla.md) | Mass Transfer: `kLa_meas` → `kLa_surf_used` | proxy only (unvalidated) | **#1 sensitivity (~375%)** – decides the 1.4-min vs 178-min sparge interval; must exceed `kL_surf_crit` (~1.22e-4 m/s) |
| 2 | Faradaic efficiency | [faradaic-efficiency.md](faradaic-efficiency.md) | Electrochemistry: `etaF`, `etaF_OER` | both assumed 1.0 | makes all O2 figures an optimistic upper bound until measured (likely <1 here) |
| 3 | Dissolved oxygen & organism DO bands | [dissolved-oxygen.md](dissolved-oxygen.md) | Biology HOB table (min/opt/impair/toxic DO) | mostly pink gaps; validates `DO_ss` | the organism DO band sets the target operating DO and the schedule |
| 4 | CO2 flow calibration (per reactor) | [flow-calibration.md](flow-calibration.md) | `CO2 flows`!J (flowrate), I (min sparge) | only ed04 done (3.33 ml/s, 0.25 s) | every reactor needs its own; an uncalibrated reactor shows "calibrate first" |
| 5 | Knallgas uptake stoichiometry | [knallgas-stoichiometry.md](knallgas-stoichiometry.md) | Biology: `bio_H2`:`bio_O2`:`bio_CO2` | assumed 6:2:1 (needs a growing culture) | sets the O2 surplus and carbon demand the schedule is built on |
| 6 | Sinter (frit) porosity grade | [sinter-porosity.md](sinter-porosity.md) | Mass Transfer: `por_grade` | gap (only matters if sparger = Sintered) | sets bubble size; clears the "Sinter OOR" regime flag |
| 7 | Gerrit's-Law current calibration | [gerrit-current.md](gerrit-current.md) | Electrochemistry: `gerrit_slope`, `gerrit_int` | fit exists; validated 3-25% intensity | current is the master input for all H2/O2 generation; re-verify per electrode/cell |

## Ambient pressure (no protocol needed)

`Biology!P_atm` defaults to 101325 Pa. For optimal Henry-solubility and gas-volume figures, enter the actual lab pressure on the day: read a barometer, or take the local station pressure from a met service and correct for altitude. It is a minor input (low sensitivity), so the default is fine for design work; record the real value for a publication-grade run.

## How to use

1. Pick the experiment from the table (start at #0, the blocker).
2. Follow the optimal route if you have the kit; otherwise the budget route. Both state their accuracy.
3. Enter the result in the named model cell (each protocol's "Result → model" section is explicit).
4. The model recomputes. Watch the gates: `geom_check` should read OK after #0; measured `kLa` should exceed `kL_surf_crit` after #1; a calibrated reactor stops showing "calibrate first" after #4.
5. Re-read the Summary dashboard: the headline pulse/interval, DO band, and warnings update from your measured inputs.

Provenance and the model's own assumptions are in the workbook (column E "source / assumption" and the Summary key). These protocols cover how to replace the assumptions with measurements.
