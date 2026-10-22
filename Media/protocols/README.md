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

Every tab named throughout this pack (the **Calibrations** tab, the **Summary**, **Mass Transfer**, and the rest) is a worksheet in `electroPioreactorGasModel.xlsx`, which ships with this pack.

## Before you start

These preconditions are shared across every protocol; each protocol assumes them rather than repeating them:

- **Working volume per build** – about 15 mL for the 20 mL build, about 30 mL for the 40 mL build (or the actual working volume you run).
- **Run temperature** – 30 °C.
- **Current baseline** – ed04, MMO tube assembly, *Xanthobacter tagetidis*, chloride-free AMYBO03, 30 °C. Record actual fill, assembly, power, stirring, pressure and Summary selections. Historical examples are not current-run settings.
- **Schedule** – read Summary D21 (pulse duration, s; res_spg_dur_run) and D22 (interval, min; res_spg_int_run) with the recorded selections. Current baseline values are 0.65 s and 7.07 min, not fixed commands. Read gas predictions with those same selections.
- **Power** – the model fit refuses power outside 3–10 %; plugin runtime clamps at 10 %. Historical 25 % diagnostics require a separately authorised test rig, not bypassing the clamp.
- **Gas clearance and sampling** – An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance. Validate sampling apparatus for the mixture, range, recovery and disturbance before interpreting readings as undisturbed headspace. The headspace check is a hazard screen, not safety certification.
- **Ambient pressure** – enter the station pressure for the day on the Summary (see below).

Resolve dependencies before following the priority list:

- The **current-density screen** needs the **electrolysis current calibration** completed first, so the applied current is known.
- The current-density **decoupled-control gas rate** is read from the faradaic and gas figures, so those must be in place before it is meaningful.

Resolve configuration and prerequisites before following each protocol: an **Optimal** route (best accuracy, more kit) and a **Budget** route (minimal kit, with its accuracy trade-off stated), each a numbered method. For most protocols you simply record the raw numbers you measure into the **Calibrations** tab of the workbook, and the spreadsheet does the rest. A few (surface kLa, the DO bands, the knallgas uptake ratio, and the current-density screen) ask you to read or fit a value off your own data first; those protocols tell you exactly how.

## How the Calibrations tab works

Every calibration has its own section on the one **Calibrations** tab. To record a result you fill only the white cells in that section:

- **Researcher**, **Date**, and the key for that calibration – the **Reactor** it was run on, or the **Organism** it applies to.
- The **raw measurements** the protocol tells you to record (for example a volume and a time, or a set of current readings).
- **Include?** – put `y` only on validated rows that satisfy the individual protocol’s acceptance, species-balance and transferability requirements. Leave it blank, or put `n`, to keep a row in the record without using it.

Grey cells are computed for you: the tab derives the reactor **Type** from the reactor name, does every calculation the old protocols used to ask for, and works out the **value in use** that feeds the model. If no rows are included yet, the model quietly falls back to its built-in default.

Multiple people can log multiple runs on multiple reactors or organisms in the same section. How the value in use is chosen depends on the parameter, and is stated under each section's heading:

- **Averaged across included runs** where repeat measurements improve the estimate – Electrolysis current, Faradaic efficiency, surface kLa (per reactor); electrode mass transfer (per reactor and electrode, at the Summary stirrer rate and temperature); monochloramine lifetime (per reactor and medium); dissolved-oxygen bands, knallgas ratio, current-density tolerance (per organism); vial geometry (per reactor type, since all vials of a type are nominally identical).
- **Latest included run wins** where the number is a hardware or valve setting that supersedes older values – CO₂ flow rate and sinter frit grade (per reactor).

The value in use always matches whatever is selected on the Summary: Reactor and Organism, and for the two newest sections also Electrode, Medium, stirrer rate and temperature.

## Order of work

The table is a priority list by leverage, not an execution sequence; the Summary experiments list (rows 131–157) gives the recommended programme order and, in column D, whether each is done for the selections in use. DO operating validation (#7) needs flow (#8), current (#12), Faradaic (#5), surface kLa (#2) and uptake (#9) inputs first. Abiotic DO (#3) follows vent (#1) and surface kLa (#2); headspace screening (#4) requires vent characterisation and validated sampling. Resolve the Faradaic collection-rig prerequisite before using its results. Current-density tolerance requires owner-approved equivalence margins, analysis and replication. The model has live gates that tell you when a measurement has cleared its problem: the Geometry consistency check, and the `kL_surf_crit` threshold on Mass Transfer.

| # | Experiment | Protocol | Calibrations section | Why it's here |
|---|-----------|----------|----------------------|----------------|
| 0 | Vial geometry & true headspace | [vial-geometry.md](vial-geometry.md) | Vial geometry | Biggest lever on the pulse: it is sized to about one headspace volume; clears the geometry consistency flag |
| 1 | Headspace vent characterisation | [headspace-vent.md](headspace-vent.md) | None yet: set Summary D11 and, for Air exchange, Mass Transfer D142 | Decides the vent model, the single biggest input to the interval (historical sensitivity example: about 0.9 to 12.7 min across plausible vents; read Summary D22 for the current selections). Fix the cap leak first |
| 2 | Surface O₂ transfer (kLa) | [surface-kla.md](surface-kla.md) | Surface kLa | Sets how far dissolved O₂ sits above the headspace and the margin of the whole DO strategy |
| 3 | Abiotic DO trace under the schedule | [abiotic-do-trace.md](abiotic-do-trace.md) | None: compare with Summary D46–D47 | One cell-free run that tests the whole headspace balance; do it after #1 and #2 |
| 4 | Headspace H₂/O₂ (lag-phase flammability) | [headspace-gas-safety.md](headspace-gas-safety.md) | None: compare with Summary D50–D52 | Safety: required before any unattended run from inoculation |
| 5 | Faradaic efficiency | [faradaic-efficiency.md](faradaic-efficiency.md) | Faradaic efficiency | The cathodic efficiency is calculated from an estimated mass-transfer coefficient; measuring it constrains the schedule’s O₂ source only with a supported species balance |
| 6 | Electrode mass-transfer coefficient | [electrode-mass-transfer.md](electrode-mass-transfer.md) | Electrode mass transfer (feeds Electrochemistry D83) | Sets the cathodic O₂ loss, the peroxide source, the chlorine cap and the electrode-surface pH verdict |
| 7 | Dissolved oxygen & organism DO bands | [dissolved-oxygen.md](dissolved-oxygen.md) | Dissolved-oxygen thresholds | The organism's DO band sets the target operating DO and the schedule |
| 8 | CO₂ flow calibration | [flow-calibration.md](flow-calibration.md) | CO₂ flow | Every reactor needs its own; an uncalibrated reactor reads "calibrate first". Step 10 checks it with the sparger attached |
| 9 | Knallgas uptake stoichiometry | [knallgas-stoichiometry.md](knallgas-stoichiometry.md) | Knallgas ratio | Sets the O₂ surplus and carbon demand the schedule is built on |
| 10 | Free and combined chlorine (DPD) | [chlorine-species.md](chlorine-species.md) | Monochloramine lifetime (feeds Chemistry D142, per medium) | Settles the monochloramine lifetime, about +15 %/−7 % on the UdG interval |
| 11 | Sinter (frit) porosity grade | [sinter-porosity.md](sinter-porosity.md) | Sinter porosity | Sets bubble size; only matters when the sparger is a sintered frit |
| 12 | Electrolysis current calibration | [gerrit-current.md](gerrit-current.md) | Electrolysis current | Current is the master input for all H₂/O₂ generation; re-check per electrode and cell. Below 3 % it is a DATA GAP that the start-up power (Summary D24) depends on |
| 13 | pH through a growth run | [ph-growth-run.md](ph-growth-run.md) | Experiment record (Calibrations) | Tests the acid released by ammonium uptake (end-of-run pH, Summary D28) and the media options (Summary D64–D67) |
| – | Current-density screen (new strain) | [current-density-screen.md](current-density-screen.md) | Current density | Only when a strain has no trustworthy published current-density tolerance |

## Ambient pressure (no protocol needed)

The model defaults ambient pressure to 101325 Pa. For the best Henry-solubility and gas-volume figures, enter the day's station pressure in the Ambient pressure cell on the Summary. It is a low-sensitivity input, so the default is fine for design work; record the real value for a publication-grade run.

## How to use

1. Pick the experiment from the table, starting at #0. Protocols marked "None" in the Calibrations column are not on the tab yet: compare your result with the cells named and record it in your lab notebook; taking these as model inputs is on the Summary list of potential model improvements (rows 133 onwards).
2. Follow the Optimal route if you have the kit; otherwise the Budget route. Both state their accuracy.
3. Record your raw numbers in that section of the Calibrations tab, filling Researcher, Date and the key, and leaving Include blank or `n` until that protocol’s acceptance, species-balance and transferability gates are met. Only then set Include to `y`.
4. The model recomputes. Watch the gates on the Summary: the geometry check should read OK after #0; the measured kLa should exceed its critical value after #2 (compare kLa with kL_surf_crit × a_surf in consistent units); a calibrated reactor stops reading "calibrate first" after #8.
5. Re-read the Summary: the headline pulse and interval, the DO band, the current-density status and the warnings all update from your measured inputs.
