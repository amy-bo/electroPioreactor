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
recorded_at: 2026-07-02
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, index]
---

# electroPioreactor experiment protocols

Standalone bench instructions for the measurements that calibrate `electroPioreactorGasModel.xlsx`. Run these to replace the model's default and data-gap values with measured ones.

Each protocol is written to be followed blindly: an **Optimal** route (best accuracy, more kit) and a **Budget** route (minimal kit, with its accuracy trade-off stated), each a numbered, easy-to-follow method. For most protocols you simply record the raw numbers you measure into the **Calibrations** tab of the workbook, and the spreadsheet does the rest. A few (surface kLa, the DO bands, the knallgas uptake ratio, and the current-density screen) ask you to read or fit a value off your own data first; those protocols tell you exactly how.

## How the Calibrations tab works

Every calibration has its own section on the one **Calibrations** tab. To record a result you fill only the white cells in that section:

- **Researcher**, **Date**, and the key for that calibration – the **Reactor** it was run on, or the **Organism** it applies to.
- The **raw measurements** the protocol tells you to record (for example a volume and a time, or a set of current readings).
- **Include?** – put `y` on rows the model should use. Leave it blank, or put `n`, to keep a row in the record without using it.

Everything else is automatic. Grey cells are computed for you: the tab derives the reactor **Type** from the reactor name, does every calculation the old protocols used to ask for, and works out the **value in use** that feeds the model. If no rows are included yet, the model quietly falls back to its built-in default, so an empty tab never breaks anything.

Multiple people can log multiple runs on multiple reactors or organisms in the same section. How the value in use is chosen depends on the parameter, and is stated under each section's heading:

- **Averaged across included runs** where repeat measurements improve the estimate – Gerrit current, Faradaic efficiency, surface kLa (per reactor); dissolved-oxygen bands, knallgas ratio, current-density tolerance (per organism); vial geometry (per reactor type, since all vials of a type are nominally identical).
- **Latest included run wins** where the number is a hardware or valve setting that supersedes older values – CO₂ flow rate and sinter frit grade (per reactor).

The value in use always matches whatever Reactor and Organism are selected on the Summary, so the model uses the right calibration for the run you are setting up.

## Order of work

Work top-to-bottom; the order is by leverage (biggest model uncertainty first). The model has live gates that tell you when a measurement has cleared its problem: the Geometry consistency check, and the `kL_surf_crit` threshold on Mass Transfer.

| # | Experiment | Protocol | Calibrations section | Why it's here |
|---|-----------|----------|----------------------|----------------|
| 0 | Vial geometry & true headspace | [vial-geometry.md](vial-geometry.md) | Vial geometry | Biggest lever – the headline sparge pulse is ~4x as sensitive to headspace as to anything else; clears the geometry consistency flag |
| 1 | Surface O₂ transfer (kLa) | [surface-kla.md](surface-kla.md) | Surface kLa | Highest sensitivity (~375%) – decides a short vs long sparge interval; must exceed the critical value |
| 2 | Faradaic efficiency | [faradaic-efficiency.md](faradaic-efficiency.md) | Faradaic efficiency | Both efficiencies are assumed 1.0 until measured, which makes every O₂ figure an optimistic upper bound |
| 3 | Dissolved oxygen & organism DO bands | [dissolved-oxygen.md](dissolved-oxygen.md) | DO thresholds | The organism's DO band sets the target operating DO and the schedule |
| 4 | CO₂ flow calibration | [flow-calibration.md](flow-calibration.md) | CO₂ flow | Every reactor needs its own; an uncalibrated reactor reads "calibrate first" |
| 5 | Knallgas uptake stoichiometry | [knallgas-stoichiometry.md](knallgas-stoichiometry.md) | Knallgas ratio | Sets the O₂ surplus and carbon demand the schedule is built on |
| 6 | Sinter (frit) porosity grade | [sinter-porosity.md](sinter-porosity.md) | Sinter porosity | Sets bubble size; only matters when the sparger is a sintered frit |
| 7 | Gerrit current calibration | [gerrit-current.md](gerrit-current.md) | Gerrit current | Current is the master input for all H₂/O₂ generation; re-check per electrode and cell |
| – | Current-density screen (new strain) | [current-density-screen.md](current-density-screen.md) | Current density | Only when a strain has no trustworthy published current-density tolerance |

## Ambient pressure (no protocol needed)

The model defaults ambient pressure to 101325 Pa. For the best Henry-solubility and gas-volume figures, enter the actual lab pressure on the day on the Summary: read a barometer, or take the local station pressure and correct for altitude. It is a low-sensitivity input, so the default is fine for design work; record the real value for a publication-grade run.

## How to use

1. Pick the experiment from the table, starting at #0.
2. Follow the Optimal route if you have the kit; otherwise the Budget route. Both state their accuracy.
3. Record your raw numbers in that section of the Calibrations tab, filling Researcher, Date and the key, and setting Include to `y`.
4. The model recomputes. Watch the gates on the Summary: the geometry check should read OK after #0; the measured kLa should exceed its critical value after #1; a calibrated reactor stops reading "calibrate first" after #4.
5. Re-read the Summary: the headline pulse and interval, the DO band, the current-density status and the warnings all update from your measured inputs.
