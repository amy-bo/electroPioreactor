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
- **Sensitivity analysis** done (`electroPioreactorGasModel-sensitivity.py`, a Python re-implementation of the model — reviewable and reproducible, kept in sync with the sheet). One-at-a-time sweep of the uncertain inputs over plausible ranges. Headline: the O₂:H₂ *consumption ratio* (`bio_O2`, the "2" of 6:2:1) is the single biggest lever on the O₂ surplus (100% swing), ahead of `etaF` (50%), because `O2_excess` is a small difference of two larger flows. `etaF` (D78) is a strong second and uniquely also drives throughput and carbon margin. The "gas stripping alone is insufficient" verdict is robust — `strip_ratio` stays well below 1 across every uncertain input; only the operating knobs (`Q_CO2`, duty) move it materially. Highest-value measurements to pin down, in order: the biological O₂:H₂ uptake ratio, then `etaF`.

## Phase 1.3 — vial dimensions checked against Pioreactor source

Verified the AEP0.2 (40 mL) placeholders against Pioreactor's software (`core/pioreactor/models.py`) and docs. Key finding: the 40 mL vial is the **same diameter as the 20 mL** (the source inherits `reactor_diameter_mm` = 27.0 for both and overrides only capacity and fill volume — a taller vial, not a wider one).

- `vial_OD_2` (D25): 28 → 27.48 (same diameter as the measured 20 mL; was a guess, now literature-supported). Measure to confirm.
- `Vmax_2` (D29): 25 → 30 (Pioreactor recommends 10–30 mL working volume for the 40 mL vial).
- `D_int_2` (D27): note updated — still a measure-it, but now flagged as ~double the 20 mL depth given the equal diameter.
- Confirmed correct: `Vmax_1` (D28) = 16 (top of the 8–16 mL recommended range for the 20 mL).
- Still genuine gaps (Pioreactor publishes neither wall, internal diameter, nor heights): `D_int_1`, `D_int_2`, `Vtot_1`, `Vtot_2`, `vial_wall`. Pioreactor's extra published figures for reference: max fill 18 mL (20 mL vial) and 36 mL (40 mL vial).

Source: Pioreactor `models.py`, docs `prepare-vial-for-cultures`.

## Reference audit (2026-06-16)

Checked every value sourced to a paper/reference against what the source actually gives. Cells referenced by name (row numbers drift as rows are inserted). DOI resolution is firewalled in the container, so literature values were corroborated via the source's own formula or an independent cross-check where the row couldn't be pulled directly.

Verified correct:
- Defined/standard constants — `F_const`, `R_gas`, `T_ref`, `g_const`, `Pa_per_atm`, `z_e_H2`, `z_e_O2`, `M_CO2`: exact (NIST CODATA / SI definitions).
- `sigma` 0.0712 N/m — IAPWS R1-76 at 30 °C gives 0.07118. ✓
- `rho_L` 995.65 kg/m³ — IAPWS-95 at 30 °C. ✓
- `H_O2ref` 1.3e-5 mol/m³/Pa — consistent with O₂ solubility (~1.24e-5 from 1.26 mmol/L at 1 atm, within 5%). ✓
- `H_O2T` 1500 K — consistent with the van 't Hoff coefficient for O₂ (≈1450–1560 K). ✓
- `O2_ceil_atm` 0.30 atm — ~0.30 atm O₂ growth-inhibition threshold corroborated for *C. necator*. ✓
- `mend_a`/`mend_b` 2.14/0.505 — standard Mendelson (1967) coefficients. ✓
- DURAN pore-size midpoints — arithmetic correct. ✓
- Vial dimensions — audited against Pioreactor source (Phase 1.3 above). ✓

Corrected:
- `D_O2` 2.4e-9 → **2.249e-9 m²/s**. The cited Han & Bartels (1996) fit, log₁₀(D[cm²/s]) = −4.410 + 773.8/T − (506.4/T)², gives 2.25e-9 at 303.15 K, not 2.4e-9. Effect is tiny (kL ∝ √D_O2; strip_ratio already ≪1).

Corrected (citations):
- **`etaF` "Nat. Commun. 2022" → Clary et al. 2020 (PNAS 117:32947).** The original citation was unidentifiable. Replaced with a verified paper that measures neutral-water HER at ~97% Faradaic yield — directly on point, since neutral pH is exactly this cell's hard regime (FE near 100% is routine in acid/alkali; neutral is where O₂ reduction competes). Value (1.0) unchanged as a stated optimistic bound.

Resolved (see Task 1 below):
- **`bio` 6:2:1 — citation was wrong** (aem.02007-22 is a lag-phase paper, not stoichiometry). Note rewritten to Lu & Yu (2019); value kept at 6:2:1 as the defensible central estimate, with ranges stated. Reasoning in the Task 1 section.

Not externally verifiable (not papers): Gerrit's Law fit (`gerrit_slope`/`int`/`min`/`max`) is the Pioreactor team's empirical calibration; NIST/ISO/DURAN/Pioreactor are standards/data/software, not journal articles.

### Zotero
All cited sources are now in the library (userID 9492620), tagged `electroPioreactorGasModel`. **Papers (8):** Lu & Yu 2019, Amer & Kim 2023 (lag phase), Lambauer & Kratzer 2022 (explosive-mix feed), Sander 2023 (Henry), Wagner & Pruß 2002 (IAPWS-95), Han & Bartels 1996 (O₂ diffusivity), Mendelson 1967 (bubble rise), Clary et al. 2020 (neutral-water HER FE). Mendelson's DOI was corrected during entry (10.1002/aic.690130213). **Non-paper sources (7):** NIST CODATA constants, NIST Chemistry WebBook, ISO 4793:1980, DURAN porosity catalogue, IAPWS R6-95 (density), IAPWS R1-76 (surface tension), Pioreactor docs/source.

## Task 1 — bio consumption ratio: research + decision (2026-06-16)

You can't measure the uptake ratio pre-growth, so this is a reasoned choice with stated ranges, biased toward reaching growth.

**Research.** The uptake ratio is genuinely *not* a fixed constant — Lu & Yu (2019) show it's set by how the cell splits reducing power between O₂ respiration (energy) and CO₂ fixation, and that split shifts with cell density and growth phase. Hard anchors: the knallgas energy reaction (2H₂ + O₂ → 2H₂O) caps O₂:H₂ at 0.5; autotrophic growth diverts ~30–40% of reducing equivalents to fixation, which puts O₂:H₂ ≈ 0.29–0.35 and CO₂:H₂ ≈ 0.15–0.19. The widely-cited *feed* optimum is 7:2:1 (Ishizaki 2001), which reliably gives <12 h lag — but feed ≠ consumption.

**Decision: keep 6:2:1 as the central consumption estimate.** O₂:H₂ = 0.33 and CO₂:H₂ = 0.17 both sit mid-range of the anchors above, so 6:2:1 is defensible without inventing a new number I can't source. Ranges now recorded in the cell notes:
- O₂:H₂ ∈ [0.29, 0.35] → `bio_O2` ∈ [1.75, 2.1] (with `bio_H2` = 6)
- CO₂:H₂ ∈ [0.15, 0.19] → `bio_CO2` ∈ [0.9, 1.15]

**Most-likely-to-reach-growth caveat.** The binding risk to establishing growth is O₂ inhibition (Amer & Kim 2023), so the *design* should be stress-tested at the lean-O₂ end (`bio_O2` ≈ 1.8 → ~20% larger O₂ surplus to remove). The sensitivity sweep already spans this. One-line change if you want the value itself biased that way rather than just the range: set `bio_O2` = 1.8. Carbon is non-limiting across the whole CO₂ range (supply ≈ 22× demand), so `bio_CO2` doesn't move the dosing conclusion — but see the over-dosing point in the section 5/9 review below, which is the *real* CO₂ story.

## Deep review — sections 6–10 (2026-06-16)

Recomputed every formula in 6–10 independently (Python, exact sheet formulas, post-D_O2-fix). **No arithmetic, unit, or reference errors found** — the chain is dimensionally clean and self-consistent. Spot values (active build, sinter P0, etaF=1): d_bubble 2.08 mm, u_rise 0.290 m/s, kLa_sparge 7.5 /h, kLa_avg 0.13 /h, strip_ratio 0.039, We 0.13 (static), carryover 151× margin. The findings below are modelling limitations and one important missing diagnostic, not bugs.

**Added: O₂ time-to-ceiling diagnostic (`t_O2_ceiling`, `t_O2_ceiling_strip`, section 10).** This is the operational number the model was missing. Without active O₂ removal, dissolved O₂ rises from zero to the 0.30 atm inhibition ceiling in **~18.5 min** at current settings; crediting time-averaged gas-bubble stripping extends it to only **~19.2 min**. That single comparison makes the central result concrete: gas-bubble stripping is not the O₂ mechanism.

**The core O₂ tension (synthesis across 5/7/9/10).** The same CO₂ bubbles do two jobs — deliver carbon and strip O₂ — but the two have wildly mismatched rate needs:
- Carbon: CO₂ supply is ~22× demand at the current schedule (`CO2_sd_ratio`). Carbon is hugely non-limiting; if anything the schedule *over-doses* CO₂. High dissolved CO₂/pCO₂ extends lag (Amer & Kim 2023), so over-dosing is itself a growth risk, not free insurance.
- O₂ stripping: at *best-case* driving force (bulk DO at the ceiling) and **continuous** sparging, gas stripping would remove ~2.3× the O₂ surplus — so capacity isn't the problem. But you only sparge ~1.7% of the time (because that's all the CO₂ you need), so time-averaged stripping delivers ~4% of requirement. To strip the surplus you'd need near-continuous sparging, i.e. ~60× more CO₂ (`CO2_sd` → ~1300×). You cannot.
- Therefore O₂ management cannot come from the CO₂ bubbles. It must come from (a) the cathode (`O2_cathode_ORR`, active once etaF<1), (b) running low electrolysis current so the absolute O₂ rate is small, and/or (c) a *separate* O₂-stripping gas decoupled from CO₂ dosing. **The strongest Phase-2 recommendation: consider a dedicated strip gas (or headspace sweep) so O₂ removal isn't hostage to the CO₂ dosing rate.**

**Section-by-section limitations (all correct as written, but bounded):**
- **§6 `d_bubble` (Tate static):** for the *sinter*, single-pore Tate ignores coalescence of bubbles from adjacent active pores at the disc face — real sinter bubbles will be larger than 2.08 mm, rise faster, give less interfacial area, so strip even less. Reinforces the conclusion. For the *tube*, the 4.1 mm bubble is ~16% of the vial ID, so wall effects on rise velocity begin to matter (not modelled). `n_pores_active` = 1 is correctly the worst case for the We check (lowest pore count → highest velocity → most likely dynamic), and even that comes out static, so "Tate valid" is robust.
- **§7 `strip_sparge` driving force = O₂ at the ceiling (364 µM):** explicit best case. The stated operating aim is to *minimise* DO, where the driving force collapses, so the real strip rate is below even the 4% figure. CO₂ bubbles also partly dissolve as they rise (that's the delivery mechanism), shrinking them and changing `a_int` — the coupled CO₂-in/O₂-out behaviour of one bubble population is not modelled (acceptable for Phase 1). Higbie `kL` and `a = 6ε/d_b` are standard and correctly applied.
- **§8 carryover:** correctly uses the during-pulse (peak) velocity; 151× margin, robust.
- **§9 verdict:** logic is sound. Now that `t_O2_ceiling` exists, the verdict could optionally reference the ~18 min timescale, but I left the verdict formula untouched.
- **§10 (the Phase-1.2 additions):** all formulas re-verified; bubble-regime flag and the new diagnostics compute correctly.

## Phase 1.5 — sections 11 & 12: surface-aeration O₂ path, stirring, dissolved CO₂ (2026-06-16)

Built the missing mechanisms the logic pass exposed. All cells recomputed independently; all 167 defined names resolve; dropdowns and recalc intact.

### §11 — O₂ removal via stirred surface to vented headspace (the likely-dominant path)
The model previously removed O₂ only into rising CO₂ bubbles (~0.04× of need) and computed the free-surface area `interface_A` (§1B) without ever using it. §11 wires in the path that area was for: the stir bar renews the liquid surface, O₂ crosses into the headspace, and the CO₂ sparge flushes the headspace out the vent. Two legs:

- **Mass-transfer leg (coarse):** `tip_speed` → surface-renewal frequency `s_renew` (coarse proxy = tip speed / vial ID) → `kL_surf` (Danckwerts) → `kLa_surf` ≈ 19 /h → `surf_strip`, giving **`surf_ratio` ≈ 6×** at ceiling driving force. That is ~150× the bubble path. Caveat: `kL_surf` rides the coarse `s_renew` proxy and is likely high-end (gold-flagged) — **measure kLa by gassing-out** to firm it up. Even if the proxy overestimates by 5×, the path still clears the surplus.
- **Vent-capacity leg (robust, kL-independent):** `y_O2_vent` = the headspace O₂ mole fraction at which the vented CO₂ throughput carries the excess O₂ away = **4.4%**, which corresponds (`DO_vent_eq`) to a dissolved O₂ of only **~53 µM — 7× below the 364 µM ceiling**. So the gas throughput alone is comfortably able to remove the O₂ at a DO well under the inhibition limit; the only question is whether surface transfer is fast enough to feed it (the mass-transfer leg, which says yes with margin).
- **Coupling caveat:** `hs_flush_time` ≈ 39 min — the headspace approaches its steady O₂ level over tens of minutes; the static cells approximate a coupled dynamic. Not fatal (it converges to the favourable low-DO state), but it's why this is Phase-1.5, not a closed result.

**Headline reversal:** the earlier "gas stripping alone is insufficient (0.04×)" verdict was correct *only for the bubble path*. With the stirred surface + vented headspace included, O₂ removal is plausibly sufficient (`O2_removal_ratio` ≈ 6×, `t_O2_ceiling_rem` = "removal holds ceiling"). The separate-strip-gas idea from Phase 1.4 is withdrawn — unnecessary. The remaining real risk is the **lag/establishment** regime: `t_O2_ceiling_lag` = **6.2 min** (cells not yet consuming O₂, so the full net electrolytic O₂ accumulates), worst exactly when establishing growth — so the surface path needs to be working from the start, and low electrolysis current + cathodic O₂ reduction (low etaF) buy proportional time.

Stirring is now an explicit input (`stir_rpm`, `stir_len`). It drives the surface path here; it also enhances bubble breakup/holdup (not quantified — would need vessel-specific constants).

### §12 — dissolved CO₂ & carbon availability (+ pH)
- `CO2_diss` ≈ **29 mM** dissolved during a sparge (Henry, Sander 2023 CO₂ constants), vs RuBisCO `Km_CO2` ~50 µM → **`CO2_carbon_margin` ≈ 590×**. Carbon is saturating for fixation during sparge (duty-averaged is lower but still far above Km). Confirms carbon is not the limiting factor — consistent with the 22× supply:demand but now expressed as the biologically meaningful dissolved concentration.
- `pH_CO2_unbuf` ≈ **3.94** is the UNBUFFERED worst case (pure water saturated with CO₂). The Sydow (2017) phosphate medium (~36–108 mM) buffers pH near setpoint, so this is a lower bound, not the operating pH — proper pH needs the buffer model. Flagged in the cell. This is the lever that connects CO₂ over-dosing to lag (high pCO₂/low pH extends lag, Amer & Kim 2023): it argues for dosing CO₂ to need, not 22× over.

### What lowers lag (your question)
Lag is set by gas partial pressures, not the uptake ratio: keep O₂ partial pressure low (the §11 surface path + low current + cathodic ORR), keep CO₂ moderate not excessive (§12 — over-dosing drops pH and extends lag), and keep mixing good (stir-driven kLa correlates with shorter lag). The bio ratio itself is not the lag lever.

### Caveats / follow-ups
- `kL_surf` / `s_renew` are coarse — measure kLa by gassing-out to convert the 6× from "plausible" to "confirmed".
- `Km_CO2` is order-of-magnitude; `pH_CO2_unbuf` is unbuffered worst-case (needs the Sydow buffer model for true pH).
- The sensitivity script (`electroPioreactorGasModel-sensitivity.py`) now includes the surface path (synced phase 1.5); §13 H₂ availability is not in it (it's a fixed timescale, not an OAT output).

## Re-review of sections 1–5, applying the 6–10 logic lenses (2026-06-16)

The 6–10 pass exposed two error *classes* — a regime mistake (crediting steady-state biology during lag) and a whole omitted mechanism (surface aeration). I re-checked 1–5 for both. Both recur; one is significant. (My first 1–5 pass was arithmetic + assumptions, not this depth — so yes, it needed re-review.)

**Arithmetic/units across 1–5: re-confirmed clean.** Geometry/displacement chain, electrolysis (Faraday), Henry/ceiling, CO₂ dosing — all dimensionally consistent, no errors. Selector error-by-design logic intact.

**Regime error (same class as the O₂ lag miss) — §3.** The section assumes "cells consume 100% of evolved H₂", so `O2_cons`/`CO2_cons` are steady-growth values. During lag/establishment uptake ≈ 0, so they're overstated and the consumption-credited `O2_excess` understates the real lag surplus (which is the full net electrolytic O₂ — captured by `t_O2_ceiling_lag`, §11). Fixed: `H2_cons`/`O2_cons` notes now carry the lag caveat and cross-reference §11/§13.

**Omitted mechanism (the H₂ analogue of the surface-aeration miss) — new §13.** §3 asserted 100% H₂ utilisation with no supporting mechanism. H₂ is barely soluble (`C_H2_sat` ≈ **0.77 mM**, ~6× less than O₂), yet it's evolved at `H2_turnover` ≈ **9× the saturable pool per hour**. So during lag (no uptake), dissolved H₂ saturates in `t_H2_sat` ≈ **6.5 min** — the same fast timescale as O₂ — and beyond that the evolved H₂ bubbles off: **(a)** lost energy (the cells' whole energy source), and **(b)** an explosive H₂+O₂ headspace (`H2_safety`: H₂ is flammable 4–94% in O₂). "100% consumed" therefore holds only once cells are growing fast enough to consume H₂ in near-real-time; it fails exactly during establishment. This is arguably *more* fundamental than CO₂ dosing for reaching growth — if H₂ isn't delivered, nothing grows. It reinforces the same prescription: **low electrolysis current during establishment** (lower H₂ and O₂ evolution rates → both gases consumable, headspace safer), ramp as OD climbs. §13 (H₂), §11 (O₂), §12 (CO₂) now give all three gases an availability/removal treatment.

**Coupling — §5 ↔ §11/§12.** `CO2_supply` feeds §11's vent leg, but CO₂ must first saturate the liquid (~1 h at the current schedule) before it breaks through to the headspace to flush O₂ — so the vent leg is weak during the early/lag phase. Noted on `CO2_sd_ratio`, and the "before stripping use" wording was corrected (bubble stripping is negligible; the real O₂ route is surface→vent, §11) and the over-dosing point added.

**Minor — §2 volumetric gas rows.** Clarified that `V_H2_gen`/`V_O2_gen`/`V_gas_total` are an **abiotic** calibration (collect over water, no cells, to verify Gerrit's Law / etaF); with cells the H₂ and excess O₂ are consumed so you wouldn't collect them.

**Net:** the model now treats all three gases consistently, and the lag regime is flagged wherever steady-state biology was silently assumed. The dominant remaining uncertainties are the same measurables: etaF, surface kLa (gassing-out), and — newly highlighted — whether H₂ can actually be delivered/consumed fast enough during establishment.

## Phase 1.7 (CO2-model) — usability: verdict removed, flags tokenised, conditional formatting
- Removed `sched_verdict` (§9): it scored **only bubble stripping**, so on the tube sparger it could never read "sufficient" (max ~0.9× even at 100% duty) and it ignored the §11 surface/headspace O₂ path that actually removes O₂. Misleading — superseded by §11 and the optimiser.
- Long-sentence value cells → short tokens (`OK`/`RISK`/`Static`/`Dynamic`/`LOW`/`EXPLOSIVE`); full text kept in the E note. Column D narrowed (was forcing horizontal scroll).
- Conditional formatting: traffic-light on tokens; red→green colour scales on the watch ratios (`O2_removal_ratio`, `surf_ratio`, `t_O2_ceiling`/`_lag`, `CO2_sd_ratio`, `We_orifice`, `O2_excess`).

## Phase 2 (CO2-optimiser branch) — §14 optimal sparge schedule (absolute answer)
For a given CO₂ flow the model now **computes** the pulse duration and interval, rather than leaving you to iterate. Mechanism:
- **Two duty floors:** `duty_carbon` (CO₂ supply ≥ margin × fixation demand) and `duty_O2vent` (vented CO₂ throughput carries the worst-case **lag** net O₂ out at ≤ `target_DO_frac` × ceiling). `duty_opt` = the binding of the two.
- **Frequency cap** `spg_int_max` = `target_DO_frac` × `t_O2_ceiling_lag`, so DO can't spike past target between flushes.
- **Answer:** pulse at the solenoid floor (`spg_dur_opt`, shortest → smoothest → best OD windows), interval `spg_int_opt` from the optimal duty, capped by the frequency limit.
- **`sched_mode` selector** (Manual / Optimal): Manual uses your typed `spg_dur_man`/`spg_int_man`; Optimal auto-applies the computed schedule. `spg_dur`/`spg_int` (§5) became mode-switched formulas — verified acyclic (the optimum depends only on Q_CO2, geometry and gas generation, never on the schedule it sets).

**Default result** (Q=10 mL/min, target DO = 0.5 × ceiling): **0.5 s pulse every ~34 s**. The binding constraint is **O₂ venting, not carbon** — so the real lever is `target_DO_frac` (how close to the ceiling you let DO run), which trades O₂ margin against CO₂ dose / pH:

| target_DO_frac | pulse | interval | CO₂ : demand |
|---|---|---|---|
| 0.3 | 0.5 s | 20 s | 33× |
| 0.5 | 0.5 s | 34 s | 20× |
| 0.7 | 0.5 s | 48 s | 14× |
| 0.9 | 0.5 s | 61 s | 11× |

So your manual 1 s / 1 min sits near the 0.5-target optimum; the gains are a shorter, more frequent pulse (smoother DO) and the ability to dial CO₂ down by accepting higher DO.

**Accuracy limit (stated in the section, cell `kinetic_caveat`):** this optimises a **constraint proxy** — the least-dosing schedule that holds DO below the O₂ ceiling, keeps carbon non-limiting, and respects the solenoid floor and flush frequency. It is **not** a fitted growth model: no validated μ(dissolved-O₂, pH, dissolved-CO₂) or lag kinetics exist for *C. necator* under in-culture electrolysis. It gives the lag-**minimising direction**, not a biologically-exact optimum, and is further bounded by etaF (unmeasured), surface kL (coarse), and the unbuffered-pH simplification. Validate empirically.
