# electroPioreactorGasModel.xlsx – review and change log

This is the review and Phase 1.2 change record for the gas model (`electroPioreactorGasModel.xlsx`). It supersedes the ad-hoc review notes and is kept alongside the spreadsheet so the xlsx stays the reviewable artifact and this file is the audit trail.

Provenance: the model began as `CO2.xlsx` (Claude for Excel extension, multi-sheet), was flattened and refined by hand through `electroPioreactor_model_phase1.xlsx`, `_1`, `_2`, and is now this single-sheet file. It originated in Claude Desktop (Opus 4.8) project *AMYBO In-culture electrolysis HOB cultivation*, chat *Electrobioreactor CO₂ dosing optimization*. Each prior version is preserved in git history on the `CO2-model` branch (`git show <sha>:Media/<name>`).

## What the model does

It sizes CO₂ dosing and O₂ management for an aseptic electro-bioreactor growing *C. necator* on electrolytic H₂/O₂ plus dosed CO₂, in a Pioreactor vial. Every cell is a number, text, or a formula; each datum lives in its own named, sourced cell. Confidence is encoded by font colour (black = verified/handbook/defined; blue bold = assumption, input, or to-measure).

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
- **Confidence legend mismatch.** The legend describes six confidence levels but only two are actually used (black and blue-bold), and the legend swatches themselves are not coloured. Either colour the swatches and use the full scale, or simplify the legend to the two levels in use. Not changed here as it is a presentation call, not a correctness one. Happy to do either.
- **Sensitivity analysis** remains deferred per the model's own note. Once `etaF` and `n_pores_active` have measured values, a one-at-a-time sweep of those plus `Q_CO2`, duty cycle and `intensity` would be the natural next step.
