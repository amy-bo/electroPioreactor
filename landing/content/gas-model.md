---
title: Gas and electrolysis model
description: How the electroPioreactor gas model turns electrolysis current, culture demand and vial geometry into a CO₂ pulse schedule, what it assumes, how it is verified and where it is still weak.
section: research
audience: expert
order: 20
---

The electroPioreactor makes its own hydrogen and oxygen by electrolysis inside the culture, and adds carbon dioxide (CO₂) in short pulses. The gas model is a spreadsheet, with a Python check, that works out how much gas the electrodes make, how much the bacteria use, and so how long and how often to pulse CO₂. It is a planning and characterisation tool: by its own account it is not yet fit to set an unattended schedule. For the basic idea, read [How it works](/how-it-works/) first.

> **Note:** Abbreviations on this page: HOB, hydrogen-oxidising bacteria; DO, dissolved oxygen; MEP and AEP, the Mixed-culture and Aseptic electroPioreactors (see [Variants](/variants/)); kLa, the volumetric gas–liquid mass-transfer coefficient; ORR and OER, the oxygen reduction and oxygen evolution reactions; SID, strong-ion difference.

## Files

| File | What it is |
| --- | --- |
| [`electroPioreactorGasModel.xlsx`](repo:Media/electroPioreactorGasModel.xlsx) | The model. Excel workbook, 25 sheets, about 3,700 formulas and 1,100 defined names. The reviewable artefact |
| [`electroPioreactorGasModel.py`](repo:Media/electroPioreactorGasModel.py) | An independent re-derivation (the "twin") that recomputes the physics and compares each output with the value Excel cached in the workbook |
| [`electroPioreactorGasModel-sensitivity.py`](repo:Media/electroPioreactorGasModel-sensitivity.py) | One-at-a-time sensitivity sweep: ranks uncertain inputs by how much they move the schedule |
| [`gas_model_verification.py`](repo:Media/gas_model_verification.py) and [`electroPioreactorGasModel-verification.json`](repo:Media/electroPioreactorGasModel-verification.json) | Hashes of every input, formula and defined name, so any edit to the workbook is detected |
| [`gas-model-checks.py`](repo:Media/gas-model-checks.py) | Regression tests (medium selection, fail-closed verification) |
| [`gas-workbook-audit.py`](repo:Media/gas-workbook-audit.py) | Read-only structure and cell-format audit |
| [`protocols/`](repo:Media/protocols/) | Fifteen bench protocols that replace the model's defaults and data gaps with measurements |
| [`TODO.md`](repo:Media/TODO.md), [`CHANGELOG.md`](repo:Media/CHANGELOG.md), [review record](repo:Media/electroPioreactorGasModel-GPT6Astra-Review.md) | Open measurements, done work, and the independent review waves |

## What it computes

The workbook flows Summary → Geometry → Electrochemistry → Chemistry → Biology → Mass Transfer → CO₂ flows, with libraries (Reactors, Electrodes, Organisms, Media) and calibration logs alongside. In order of dependence:

1. **Geometry.** Liquid level, headspace volume and wetted electrode length from the reactor type, the fill volume and the volume displaced by electrodes and needles.
2. **Electrochemistry.** Current from the electrolysis power setting; current density on each electrode against the anode coating's and the organism's limits; Faradaic efficiencies; H₂ and O₂ production; hydrogen peroxide made by oxygen reduction at the cathode; cell voltage.
3. **Chemistry.** Ion concentrations, ionic strength, conductivity and pH of the chosen medium, including dissolved CO₂ and bicarbonate, and chlorine from any chloride.
4. **Biology.** Gas solubilities at the run temperature, the organism's DO band, and its uptake of H₂, O₂ and CO₂.
5. **Mass transfer.** One headspace balance shared by the O₂ sizing, the CO₂ pool and the flammability check; the CO₂ pulse volume and the interval that each constraint allows.
6. **Summary.** A candidate pulse length and interval to type into the plugin, which constraint binds, and traffic-light checks for safety, culture health, operation, hardware and model validity.

## Key equations

Units are SI unless shown. F = 96 485.332 C/mol, R = 8.314 J/(mol·K).

**Current from power setting.** The plugin sets a percentage, not a current. The default straight-line fit is

  I (mA) = 1.03 × P (%) + 2.6

and the model refuses to run outside 3 to 10 %: below 3 % is unmeasured, and the plugin clamps at 10 %. At 3 % this gives 5.69 mA; at 10 %, 12.9 mA. Replace it with your own unit's calibration ([`gerrit-current.md`](repo:Media/protocols/gerrit-current.md)). The protocol explains why the response is linear: the Pioreactor drives the channel by duty cycle, so the mean current scales with the setting even though the cell itself is not ohmic.

**Gas production (Faraday's law).**

  ṅ(H₂) = η_F · I / (2F)   ṅ(O₂) = η_OER · I / (4F)

converted to volume at the run temperature and pressure with V̇ = ṅ·R·T / P. η_F is the cathode's Faradaic efficiency for hydrogen and η_OER the anode's for oxygen.

**Faradaic efficiencies are calculated, not assumed.**

  η_F = 1 − i_ORR / I

where i_ORR is the current lost to reducing dissolved O₂ back at the cathode, limited by O₂ mass transfer to the electrode. That reduction also makes hydrogen peroxide. On the anode,

  η_OER = 1 − f_Cl − f_H₂O₂ − f_corr − f_HOR

subtracting the fractions of charge spent making chlorine, oxidising peroxide, on corrosion and on re-oxidising H₂ (the last two are data gaps, held at zero until measured).

**Current density.** j = I / A_wet, with A_wet = π·d·L_sub for a tube (plus the end face for a rod) and L_sub the submerged length at the achieved liquid level. It is checked against the anode coating's continuous and maximum ratings and against the organism's optimum and tolerated ceiling.

**Biological demand.** Knallgas stoichiometry, H₂ : O₂ : CO₂ = 6 : 2 : 1 by mole:

  CO₂ demand = H₂ uptake / 6   O₂ demand = H₂ uptake / 3

with H₂ uptake = (H₂ made − H₂ re-oxidised) × utilisation fraction. Electrolysis gives H₂ : O₂ = 2 : 1, the bacteria use 3 : 1, so O₂ is always in surplus; that surplus must be flushed out or the culture's DO rises.

**Solubility.** Henry's law with a van 't Hoff temperature correction, C_sat = H(T)·p, on the dry-gas partial pressure (ambient pressure minus water vapour), with an O₂ salting-out factor for the medium's ionic strength.

**pH and conductivity.** Activity-corrected (Davies) carbonate and phosphate equilibria, solved against the medium's SID; conductivity is a Kohlrausch sum of ion molar conductivities, corrected for ionic strength (× 0.78) and temperature (+2 % per K).

**CO₂ pulse.** The delivered volume per pulse is fitted from flow measurements as V = V₀ + Q·t (34 points at present). The default pulse rule sizes each pulse to flush about one headspace volume. The interval is the shortest of several limits: the carbon-limited interval, the DO-limited interval (from the O₂ surplus and the headspace balance), an H₂-safety interval that keeps the headspace below flammability, and a pH-ceiling interval. A start-up interval is computed separately for the lag phase, when cells take up little gas.

## Inputs

All free inputs are on the Summary sheet; everything else is a sourced parameter, a library row or a calibration log.

| Input | Notes |
| --- | --- |
| Reactor | Picks the reactor type and so its geometry: AEP0.1.1 and MEP0.3 (20 ml vial, 16 ml maximum working volume), AEP0.2 and AEP0.2a (40 ml vial, 30 ml maximum working volume, 42 ml total) |
| Electrode assembly | Pt/Ti rod, MMO rod, MMO tube or graphite rod anode, each against a stainless steel rod cathode |
| Organism | Sets the DO band and current-density limits; most organisms' DO thresholds are still unmeasured |
| Medium | Any column of the Media sheet: AM001, AM002, AM003 or the University of Girona (UdG) phosphate medium (see [Media](/media/)) |
| Electrolysis power, stirring, temperature, fill volume, ambient pressure | Fill and pressure may be left blank for the reactor's maximum and 101 325 Pa |
| Vent model, O₂ sizing phase | Owner decisions: outflow only, open vent or air exchange; growth or lag |
| Pulse rule, solenoid resolution, N₂ sweep, NaHCO₃ added, nitrogen source, end-of-run biomass | Further schedule and chemistry options |

## Outputs

| Output | Use |
| --- | --- |
| Candidate pulse duration (s) and interval (min) | Values for the plugin's `sparge_duration_seconds` and `sparge_interval_minutes` |
| Start-up interval | For the lag phase after inoculation |
| Binding constraint | Which limit sets the interval |
| Mean and peak DO, pH at cycle-average dissolved CO₂, end-of-run pH | Culture-health checks |
| Headspace H₂ and O₂ fractions | Flammability check, in both growth and lag |
| Current, current densities, cell voltage, peroxide, effective chlorine | Electrode and culture checks |
| Qualification verdict | Whether the candidate meets the stated pH and DO targets |

**Current baseline.** The repository copy is set to an MEP unit: an MEP0.3 reactor (20 ml vial, 15 ml fill), MMO tube anode, *Xanthobacter tagetidis*, medium AM003, 3 % power, 1000 rpm, 30 °C. It gives 5.69 mA, an anode current density of 3.29 mA/cm², 0.042 ml/min of H₂ and 0.022 ml/min of O₂, and a candidate of a 0.65 s pulse every 7.07 min with a 1.16 min start-up interval. Its verdict is **NOT FEASIBLE** for the stated targets: pH at the mean CO₂ is 6.49, just under the 6.5 floor. <!-- source: python3 Media/electroPioreactorGasModel.py, run 2026-11-06; Media/CHANGELOG.md 2026-10-22 --> For an AEP0.2 unit, choose one of the AEP0.2 reactors on the Summary and read the results again.

## How to run it

**In Excel.** Open the workbook (it opens on Summary; the Contents sheet explains every tab). Change the blue inputs, then read Results and Checks. Add a medium by typing a new column on the Media sheet, and a measurement by typing a row under the relevant calibration log; the model picks both up with no other edit. The workbook avoids functions newer than 2019.

**In Python** (standard library only; keep the companion files beside the workbook):

```bash
cd Media
python3 electroPioreactorGasModel.py              # twin: recompute and compare with the workbook
python3 electroPioreactorGasModel-sensitivity.py  # sensitivity sweep and ranking
python3 gas-model-checks.py                       # regression tests
python3 gas-workbook-audit.py                     # structure and format audit
```

The twin is a verifier, not a free calculator. Its inputs are declared at the top of the file and checked against the workbook's Summary first; if they differ it names the mismatch and exits non-zero without comparing outputs. To explore other settings, change them in Excel, recalculate, and re-record the definition hashes.

## Verification status

| Check | Result | When |
| --- | --- | --- |
| Twin against the workbook's cached values | 559 of 559 outputs within 0.5 %, inputs identical, on a copy carrying the twin's values until Excel recalculates the 2026-11-06 changes | Run for this page, 2026-11-06 |
| Regression tests | 37 pass | Run for this page, 2026-11-06 |
| Structure and format audit | PASS (25 sheets, 3,704 formulas, 1,133 names) | Run for this page, 2026-11-06 |
| Recalculation in real Excel | All formula values identical after the last restructure | 2026-10-23, [`CHANGELOG.md`](repo:Media/CHANGELOG.md) |
| Independent reviews | Successive review waves (wave 1, June 2026, to wave 5, October 2026), the last with the first full Excel recalculation | [Review record](repo:Media/electroPioreactorGasModel-GPT6Astra-Review.md) |

The reviewers' verdict: the model is **fit to guide the abiotic characterisation runs** it asks for (vent test, cell-free DO trace, lag-phase headspace sample) and to frame design decisions, but **not yet fit to set an unattended schedule for a live culture**.

## Assumptions and limitations

- **Headspace not measured.** The pulse delivers about one headspace volume of a headspace that has never been measured; the geometry check stays red until it is ([`vial-geometry.md`](repo:Media/protocols/vial-geometry.md)).
- **Interval is an upper bound.** It assumes all H₂ made in growth is taken up; at half uptake the interval roughly halves.
- **Vent model dominates.** Across plausible vent assumptions the interval moved about 15-fold in review. The vent test comes first ([`headspace-vent.md`](repo:Media/protocols/headspace-vent.md)).
- **CO₂ cannot do three jobs.** Diluting electrolytic O₂ with CO₂ alone pulls pH below the 6.5 band; a small nitrogen (N₂) headspace sweep would decouple the two. The Summary has an N₂ sweep input; whether to fit one is still an open design decision.
- **Surface O₂ transfer is estimated.** Feasibility rests on an unmeasured surface kLa ([`surface-kla.md`](repo:Media/protocols/surface-kla.md)).
- **Data gaps stay gaps.** Unmeasured values (organism DO thresholds, anode corrosion and H₂ re-oxidisation fractions, current below 3 %) are flagged, not invented. The electrode gap is no longer one: it is taken from the printed cap, 9.6 mm centre to centre (3.6 mm between the 6 mm electrode surfaces), which lowers the baseline cell voltage from 2.65 to 2.59 V and leaves the schedule, pH and DO results unchanged. <!-- source: Media/CHANGELOG.md 2026-11-06 (Electrode gap from the printed Vial Cap); Components/Vial Cap/AEP2.0/Vessel Cap.stl -->
- **Not yet an optimiser.** The pulse rules do not jointly optimise duration and interval for growth; replicated growth experiments and a validated response model are listed as open work in [`TODO.md`](repo:Media/TODO.md).
- **Electrode library.** The "MMO tube" anode is modelled as AEP0.2 builds it: CO₂ leaves through the 1 mm-bore silicone feed tube threaded through the anode and trimmed at its base, with no sintered sparger (a frit is deferred to AEP0.3). Each electrode now carries its own sparge outlet bore; from the 1 mm outlet the model gives a 3.5 mm bubble, which affects only the small bubble O₂ strip, not the schedule, pH or DO. <!-- source: Media/CHANGELOG.md 2026-11-06 (AEP0.2 MMO tube: the CO₂ leaves its 1 mm feed tube); docs/steps/step-12-co2-gas-train.md; docs/components/anode-feed-tube.yaml -->
- **Awaiting an Excel recalculation.** The 2026-11-06 electrode-gap and sparge-outlet changes were patched into the workbook and checked against the Python twin; some cached values in the workbook update only when it is next recalculated in Excel. <!-- source: Media/CHANGELOG.md 2026-11-06 -->

> **Safety:** The review found the lag phase, just after inoculation, the dangerous one: the headspace can become flammable, DO approaches inhibitory levels and peroxide passes its threshold within minutes. Do not run unattended from inoculation without a nitrogen sweep or hydrogen monitoring, and vent to a fume hood. See [`headspace-gas-safety.md`](repo:Media/protocols/headspace-gas-safety.md).

## Measurements that improve it most

The protocols in [`Media/protocols/`](repo:Media/protocols/) each have an Optimal and a Budget route; record results in the matching calibration log and the model updates. In the protocol index's priority order, the first are vial geometry and true headspace, headspace vent characterisation, surface kLa, a cell-free DO trace, lag-phase headspace H₂/O₂, and Faradaic efficiency. The electrolysis current calibration underpins all gas rates. If you run any of these, share the results on the [forum](https://forum.amybo.org). More on the research programme: [Research](/research/).
