# electroPioreactorGasModel.xlsx – review and change log

This is the review and Phase 1.2 change record for the gas model (`electroPioreactorGasModel.xlsx`). It supersedes the ad-hoc review notes and is kept alongside the spreadsheet so the xlsx stays the reviewable artifact and this file is the audit trail.

Provenance is in git, not here: the version chain (`CO2.xlsx` → `electroPioreactor_model_phase1{,_1,_2}.xlsx` → this file) and its origin are recorded in the import-commit messages on the `CO2-model` branch (`git log`, `git show <sha>:Media/<name>`).

## What the model does

It sizes CO₂ dosing and O₂ management for an aseptic electro-bioreactor growing *C. necator* on electrolytic H₂/O₂ plus dosed CO₂, in a Pioreactor vial. The agent-facing modelling rules (cell discipline, colour conventions, units) live in `Media/CLAUDE.md`. In brief: column-E fill = confidence (six levels, legend in the sheet); column-D font = input (blue) vs formula (black).

## First-pass review: the model is sound

I traced every formula. Dimensional analysis is consistent end to end, the selector/error-by-design logic matches the actual data validations, and no arithmetic or unit errors were found. The points below are about modelling assumptions and a few latent traps, not broken cells.

## Phase 1.2 changes applied

All changes are backward-compatible at the current inputs (the headline numbers move only where physically intended).

1. **Cathodic O₂ consumption is now in the balance (was ignored).** The model previously generated excess O₂ at the anode and assumed it all had to be stripped, while its own notes said the real O₂ sink is cathodic reduction (O₂ competing with H₂ at the cathode, which is also why H₂ faradaic efficiency is below 1). New cells `O2_cathode_ORR`, `O2_net_gen`, plus parameters `etaF_OER` (anodic O₂ efficiency) and `z_e_ORR` (electrons per O₂ reduced) wire this in. The cathodic current that does not make H₂, the fraction `(1 - etaF)`, now reduces dissolved O₂, and `O2_excess` nets that out. While `etaF = 1` the term is zero and nothing changes; the moment you measure the real `etaF` below 1, the cathode automatically takes part of the O₂ load off the stripping duty. This is the single highest-value measurement now: `etaF` drives both H₂ yield and the O₂ stripping requirement.

2. **Faradaic efficiency no longer applied symmetrically.** Anodic O₂ generation (`rO2_gen`) now uses `etaF_OER` (anode efficiency, assumed ~1), not the cathodic H₂ efficiency `etaF`. Previously both H₂ and O₂ were scaled by the same `etaF`, which is wrong the moment `etaF < 1`, because the inefficiency in this cell is cathodic, not anodic.

3. **Sparge-tube in-vial length pulled into its own cell.** New `spg_len = D_int - spg_tip_h`. The headspace budget previously reused `elec_ins` for the sparge tube, which was only correct because the sparge release height happened to equal the electrode clearance. Now it is explicit and tracks `spg_tip_h` independently. Value is unchanged (33 mm) at the current geometry.

4. **Media-out tube now counted as annular wall, not solid, in the headspace budget.** Sparge and electrode inserts stay solid (their gas-filled bores do displace), but the efflux/media-out tube's bore is open to the liquid surface, so only its wall displaces. `V_inserts` drops by 0.047 mL and headspace rises from 6.565 to 6.612 mL. The liquid-level displacement calc (`disp_tot`) already treated efflux as annular, so this just brings the headspace budget into line.

5. **Bubble model now self-validates its flow regime.** Tate's law (`d_bubble`) assumes quasi-static detachment. New cells `rho_CO2`, `v_orifice`, `We_orifice` and a `bubble_regime` flag compute the orifice Weber number and flag if flow pushes detachment out of the static regime (We > ~2), in the same idiom as the existing `I_valid` and `carry_flag` checks. At current settings both the sinter (worst case, single active pore) and the bare tube come out **Static**, so Tate's law is validated rather than assumed. For the sinter, `n_pores_active` is flagged as a data gap; 1 is the worst case (highest per-orifice velocity).

6. **Hidden empty `Lists` sheet deleted.** The dropdowns source from `Model!D17:D20`, so `Lists` was a vestigial leftover from the multi-sheet original and read as an unfinished dependency.

7. **Orphan annotation removed from a Value cell.** The `(O₂-tolerant)` text was a clarifying note sitting in a parameter Value cell, not a parameter. It is demoted to a pure note: the 0.30 atm ceiling is whole-cell growth inhibition, and the O₂-tolerant [NiFe]-hydrogenase is not the binding constraint. I did not make it a dropdown because there is no real choice to select here, only a clarification.

8. **`fullCalcOnLoad` set.** The file is edited without an Excel engine in the container, so Excel and LibreOffice are told to recompute everything on open. All changed numbers were independently recomputed in Python and match.

## Remaining gaps and Phase 2 recommendations

- **Measure `etaF` (cathodic H₂ faradaic efficiency).** It is the dominant unknown and now drives the O₂ balance as well as H₂ yield. Gas collection over a known charge.
- **The stripping verdict is best-case.** `strip_sparge` evaluates with bulk O₂ pinned at the ceiling (364 µM). The stated aim is to minimise dissolved O₂, where the driving force is smaller, so real stripping is worse than the 0.04 ratio shown. Combined with the cathodic sink now in the model, gas stripping looks like a minor O₂ pathway, not the main one. Worth stating as best-case on the cell.
- **Sinter active pore count** (`n_pores_active`) is a data gap; measure or estimate to firm up the bubble regime and interfacial area for the sinter.
- **Input-vs-formula font convention** (blue = input, black = formula) is not yet applied rigorously across the sheet. Pending a decision on whether typed-in physical constants (Faraday, R, g, etc.) count as "input" (blue) or stay black; once decided, apply consistently and show the convention in the key. The section-10 additions already follow it.
- **Sensitivity analysis** done (`sensitivity.py`, a Python re-implementation of the model — reviewable and reproducible, kept in sync with the sheet). One-at-a-time sweep of the uncertain inputs over plausible ranges. Headline: the O₂:H₂ *consumption ratio* (`bio_O2`, the "2" of 6:2:1) is the single biggest lever on the O₂ surplus (100% swing), ahead of `etaF` (50%), because `O2_excess` is a small difference of two larger flows. `etaF` (D78) is a strong second and uniquely also drives throughput and carbon margin. The "gas stripping alone is insufficient" verdict is robust — `strip_ratio` stays well below 1 across every uncertain input; only the operating knobs (`Q_CO2`, duty) move it materially. Highest-value measurements to pin down, in order: the biological O₂:H₂ uptake ratio, then `etaF`.

## Phase 1.3 — vial dimensions checked against Pioreactor source

Verified the AEP0.2 (40 mL) placeholders against Pioreactor's software (`core/pioreactor/models.py`) and docs. Key finding: the 40 mL vial is the **same diameter as the 20 mL** (the source inherits `reactor_diameter_mm` = 27.0 for both and overrides only capacity and fill volume — a taller vial, not a wider one).

- `vial_OD_2` (D25): 28 → 27.48 (same diameter as the measured 20 mL; was a guess, now literature-supported). Measure to confirm.
- `Vmax_2` (D29): 25 → 30 (Pioreactor recommends 10–30 mL working volume for the 40 mL vial).
- `D_int_2` (D27): note updated — still a measure-it, but now flagged as ~double the 20 mL depth given the equal diameter.
- Confirmed correct: `Vmax_1` (D28) = 16 (top of the 8–16 mL recommended range for the 20 mL).
- Still genuine gaps (Pioreactor publishes neither wall, internal diameter, nor heights): `D_int_1`, `D_int_2`, `Vtot_1`, `Vtot_2`, `vial_wall`. Pioreactor's extra published figures for reference: max fill 18 mL (20 mL vial) and 36 mL (40 mL vial).

Source: Pioreactor `models.py`, docs `prepare-vial-for-cultures`.
