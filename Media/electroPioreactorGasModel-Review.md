# electroPioreactorGasModel.xlsx – review and change log

This is the review and Phase 1.2 change record for the gas model (`electroPioreactorGasModel.xlsx`). It supersedes the ad-hoc review notes and is kept alongside the spreadsheet so the xlsx stays the reviewable artifact and this file is the audit trail.

Provenance is in git, not here: the version chain (`CO2.xlsx` → `electroPioreactor_model_phase1{,_1,_2}.xlsx` → this file) and its origin are recorded in the import-commit messages on the `CO2-model` branch (`git log`, `git show <sha>:Media/<name>`).

## What the model does

It sizes CO₂ dosing and O₂ management for an aseptic electro-bioreactor growing *C. necator* on electrolytic H₂/O₂ plus dosed CO₂, in a Pioreactor vial. The agent-facing modelling rules (cell discipline, colour conventions, units) live in `Media/CLAUDE.md`. In brief: column-E fill = confidence (six levels, legend in the sheet); column-D font = input (blue) vs formula (black).

---

# Wave-4 review (2026-08-12) — workbook at `091ca50`

Scope: the whole workbook (8 sheets, 394 defined names, 695 formula cells) plus the two Python
companions, reviewed along four independent dimensions (chemistry; mass transfer + biology;
geometry/electrochemistry/flows/calibrations; cross-cutting integrity and house rules). Live
selector state behind every cached value: ed04 / Pt-Ti rod / UdG (mixed) / UdG phosphate,
LED 3 %, stir **1000 rpm**, T **25 °C**.

Nothing below is an arithmetic error. Every cached value in the workbook reproduces from its own
formula; the headline chain (I_app → H₂/O₂ generation → O₂ surplus → duty floors → interval and
pulse → Summary D13/D15) re-derives from first principles to machine precision. The findings are
modelling-logic, wiring, provenance and verification-harness defects.

## Blockers — these change a headline number or a safety verdict

**B1. The 375 %-uncertain surface-kLa proxy still decides the headline interval — through a branch
instead of a subtraction.** `Mass Transfer!D91` is
`IF(spg_int_regime="SURFACE-HELD", spg_int_carbon, MIN(…, spg_int_max))`, and `spg_int_regime`
(D134) is computed *from* `kLa_surf_used`. So the structural fix recorded in the 2026-06-26 wave
(withhold the surface credit inside the guards, `O2_src_guard` = `O2_net_gen`) is satisfied in
letter and defeated in effect: the shipped interval is **181.07 min against a 3.09 min O₂-limited
fallback, a factor 58.5**. Two further problems compound it:

- D134 tests `DO_ss_sawtooth` (D133, the *steady* surplus source) even though `E133`/`E134`/`E135`
  all state the shipped guard sizes on the **lag** source. On the lag basis (D135) the SURFACE-HELD
  verdict survives by only **×1.42** — inside the stated kL_surf uncertainty; at the operating point
  the sheet's own notes and the Python twin are written for (500 rpm, 30 °C) the lag criterion
  **fails** while the shipped steady criterion still reads SURFACE-HELD.
- `E89` says the fallback "applies only if measured kL_surf < kL_surf_crit (D131)". D91 never
  references D131, and D131 is `#N/A` because `DO_impair` is a data gap — the gate does not exist.

**B2. The O₂ safety guard is sized on a default that appears only because the organism data is
missing.** `target_DO_frac` (D84) falls back to **0.5** when `DO_opt`/`DO_toxic` are `#N/A` — which
they are for every organism except partial *C. necator*. For the one organism with data the true
ratio is 3/11.5 = **0.26**, so the fallback is ~1.9× *less* protective, and it scales `spg_int_max`
and 1/`duty_O2vent` linearly. Summary D34 does flag the gap; the number in use is still the
optimistic one, and `E84` reads "Input." on a formula and never mentions the fallback.

**B3. No gas-phase O₂ back-pressure anywhere in the surface path** (`D73`, `D108`, `D131`, `D133`,
`D135` all write flux = kLa·C, i.e. C\*_headspace ≡ 0). `D108` therefore predicts steady DO
**1.372 mg/L**, below air saturation (8.15 mg/L at 25 °C from the sheet's own Henry constant) — and
the real headspace between pulses is electrolytic gas at roughly 54 % H₂ / 27 % O₂ / 18 % CO₂, i.e.
*worse* than air. The same sheet carries the analogous floor on the CO₂ side (`C_air_CO2`, D146,
bounding D162), so the asymmetry is internal. With an air-equilibrium floor the regime flips to
SPARGE-NEEDED, which is B1's other branch.

**B4. The dissolved-CO₂ sawtooth is not mass-conserving, by 2.4×.** The two-compartment closed form
(D151–D162) lets the headspace vent at `k_vent` independent of what the liquid absorbs. Peak liquid
CO₂ during the gap is **17.42 mol/m³ at t ≈ 205 s = 2.61e-4 mol dissolved**, against **1.068e-4 mol
delivered per pulse** (`CO2_pulse`, which by construction equals the entire headspace inventory
`n_hs_gas`). Liquid capacity at `C_sat` is 4.7× the whole headspace inventory, so the missing
depletion feedback is not a small correction. This sets `CO2aqc_ss` → Chemistry D5 → the endpoint pH
on Summary D35.

**B5. `Chemistry!D148` (`n_e_Cl`) asserts a 1-electron oxidation that cannot happen.** Chlorine goes
Cl(−I) → Cl(+I): two electrons per HOCl on either route. The chloride-arrival-limited current in
D132 correctly uses n = 1 *per arriving chloride*; D134 then divides by that same 1 instead of the
2 electrons per HOCl formed. Correct form is `P_HOCl = I_Cl/(2·F·V)` unconditionally, and D148 is
redundant. Recomputed: P_HOCl 7.729e-8 → **3.865e-8 mol/L/s**, C_eff 0.378 → **0.292 mg/L**
(Summary D36). The verdict text ("sub-lethal") does not change. Note `E134` already states the
correct 2F form, so note and formula disagree; the CHANGELOG records this as a fix correcting a
"~2× under-count" — it is a regression.

**B6. The pH solve uses infinite-dilution constants at I = 0.112 M.** Ionic strength at the root,
computed from the full UdG speciation, is 0.112 M; Davies-corrected conditional constants move the
same charge balance from **7.376 to ≈7.16** (phosphate pKa2 7.20 → 6.76 — the textbook "phosphate
buffer is 6.8 at physiological ionic strength"). Nothing in column E discloses the assumption.
`pH_band_flag` stays green either way; MC02 would land near 6.8. Note this partly offsets B4, which
pushes the modelled pH the other way.

**B7. The measured-kLa path is 3600× wrong.** `Calibrations!C46` labels `cal_kLa` **1/s**;
`Mass Transfer!C97` labels `kLa_meas` **1/h** and `D98` divides by 3600. A researcher who follows the
header and enters s⁻¹ has it divided by 3600 again — corrupting precisely the measurement that
Summary improvement #1 ("HIGH … the single biggest lever") exists to feed.

**B8. Two calibration routes are dead, and the protocols tell researchers to use them.**
`cal_flow` (`Calibrations!D60`) is referenced by no formula anywhere — the flow actually used comes
from the `CO2 flows` sheet by raw range (`Mass Transfer!D117`) — while `protocols/flow-calibration.md`
states the Calibrations entry "feeds both the CO₂ dosing flow rate and the minimum sparge time".
Likewise the vial-geometry headspace masses (`Calibrations!D66:D73`) are collected and discarded:
`headspace_V` is still inferred from the modelled insert budget, which is the thing
`protocols/vial-geometry.md` says the measurement exists to replace. Separately, `Calibrations!D60`
and `D89` contain **`_xludf.MAXIFS`** — the unknown-user-function prefix, which Excel resolves as
`#NAME?`; both are swallowed by `IFERROR`, so a completed calibration silently changes nothing.

**B9. The Summary selectors have no data validation at all.** There is not a single
`<dataValidation>` element on any sheet except Calibrations (four). Summary F2/F3 say "Choose from
the values below. Dropdown." and there is no list below. A mistyped reactor, electrode, organism or
medium produces an `#N/A` cascade rather than being blocked — the "error by design" the house rules
require is only in the IF-chains, not at the input. Related: `ReactorList` = `Geometry!$A$59:$A$70`
is stale against the 22-row reactor table, so ten reactors (ed07, ed08, imp07–imp12, nm01, nm02)
cannot be entered in any calibration table even though Summary accepts them.

## Wrong but contained

- **`Mass Transfer!E76` states the opposite of what its own cell computes.** `DO_vent_eq` = **405.3 µM**
  against the 364.77 µM ceiling — the kL-independent vent leg does *not* hold DO under the ceiling —
  while E76 reads "~8.9 uM … well below the ~336 uM inhibition ceiling … a comfortable backstop".
  Both figures are unreproducible at the live state. This is the wave-1 H-4 mislabel, fixed in the
  formula and re-introduced in the note.
- **`Electrochemistry!D45` takes the submerged electrode length from `elec_sub_L`** (defined at the
  bare datum and labelled "For displacement bookkeeping"), not from the achieved level `h_actual`.
  Wetted area 2.1445 cm² instead of 2.0134 cm² (**+6.5 %**), so every current density reads 6.5 % low.
  Verdicts hold today; a case just under `j_opt_strain` would be reported green when it is amber.
- **`spg_int_max` is an accumulation timescale presented as a removal guard.** `E89`'s premise is
  "sparge vents all O₂", i.e. each pulse resets DO to zero. One pulse removes 7.8 % of the steady
  accumulation and 2.6 % of the lag accumulation; balancing the lag source would need a 4.8 s
  interval, 39× shorter than the 3.09 min the cell reports.
- **`duty_opt` is vestigial in the shipped branch, and `E88` claims otherwise.** `duty_opt` = 7.22e-4
  (O₂-vent-bound), but the recommended schedule runs at `duty_actual` = 7.22e-5 — one tenth of the
  "least feasible CO₂" floor — because D91 bypasses duty entirely under SURFACE-HELD. E88 asserts
  "O₂-venting now binds … true post-fix" while D94 reports "CARBON (surface holds DO)".
- **`Calibrations!I23` omits the water-vapour correction its own protocol mandates**
  (`faradaic-efficiency.md`: "n = (P_total − P_water)V/RT … significant"). etaF biased **high by
  3.1 % at 25 °C / 4.2 % at 30 °C**, and the protocol treats etaF > 1 as the signature of a broken
  measurement.
- **`Electrochemistry!D18` (`etaF`) is a pink DATA-GAP cell returning an invented 1.0**, propagating
  into `rH2_gen`, `O2_cathode_ORR` (forced to zero) and every O₂ figure. The correct pattern is two
  sheets away: `Chemistry!D158` is left genuinely empty and guarded by `ISNUMBER`.
- **`C_eff` is entirely chloride-pool-bound, so it does not "scale with current" as `E145` says.**
  `NH2Cl_mgL` = MIN(14.60, 504.2, **9.454**) — the pool cap binds and combined chlorine is 99.97 % of
  C_eff, leaving `km_Cl`, `A_anode`, `FE_CER` and `I_app` numerically inert at this operating point.
  The block also mixes mass bases inside one `MIN()`: two arguments are mg/L as HOCl (52 460 mg/mol),
  `5.06·NH3_N` is definitionally as Cl₂, and the 0.1/2 mg/L thresholds are free-chlorine values
  conventionally reported as Cl₂ (≈1.35× understated).
- **`Chemistry!D137` (`pKa_NH4` = 9.25) is not van 't Hoff corrected** while `Ka_NH4` (D18) is, so the
  sheet uses two different ammonium pKa's simultaneously. Harmless at 25 °C; at 30 °C `NH3_free` is
  1.4× understated.
- **`Summary!D14`/`D16` return `#VALUE!` for an uncalibrated reactor.** D13/D15 fall back to the text
  "calibrate this reactor first…", and `IF(D13>0.5, ROUND(D13,0), …)` takes the ROUND-of-text branch
  (text sorts above any number in Excel). No `IFERROR` wrapper, and the conditional formatting cannot
  fire either.
- **17 `#DIV/0!` cells on the Calibrations tab** with no rows included, contradicting its own A3 note
  ("the model falls back to its built-in default"). Every consumer is `IFERROR`-wrapped, so it is
  cosmetic — but it is what a researcher opening the tab sees first.
- **`CO2 flows`!J4 = 3.33 mL/s** — the single 15 s run — sets the whole schedule, while every
  sub-second run in the same session reads 3.83–5.20 mL/s and the pulse it computes is 0.78 s. The
  pulse spans 0.50–0.79 s across those values. The conservative pick may be right; no rule in the
  sheet states it, and the eight per-run averages in column H are consumed by nothing.
- **`Biology!D44`'s EXPLOSIVE flag is not an explosivity test** — it compares a dissolved-pool
  turnover rate to 1 h⁻¹. It happens to be right everywhere reachable (turnover ≤ 1 needs I ≤ 0.64 mA
  and Gerrit's Law floors I at 2.6 mA), and the "safe" branch is `"watch"`, never green — but the
  criterion is a proxy, and `D19` returning 2.6 mA at 0 % intensity means "electrolysis off" still
  generates gas downstream.

## Verification harness — both Python companions are detached from the workbook

- `electroPioreactorGasModel.py` prints **"92/92 outputs match the spreadsheet within 0.5 %"** against
  **hard-coded literals**, not the workbook. Those literals were captured at 500 rpm / 30 °C; the
  workbook has been at 1000 rpm / 25 °C since 2026-06-26. Compared against the workbook's actual
  cached values, 43 of the 92 literals disagree — up to 41 % (`DO_ss`), 50 % (tip speed), 12 %
  (carbon margin). Re-run at the workbook's live inputs it scores **86/92**, and the four substantive
  misses are real: line 605 hard-codes `A_anode = 5` where `Chemistry!D130` now imports the
  shape-aware 2.144 cm² (P_HOCl 2.33× out), and `pH_band_flag` returns "above optimum" on the
  `pH < 6.5` branch. It is also a line-by-line transcription with cell refs in the comments, so it
  cannot function as an independent check even when current.
- `electroPioreactorGasModel-sensitivity.py` still implements the **superseded surf_strip-credited
  guards** (its own comment says so) at 500 rpm, and prints `pulse_floor` where it means the computed
  pulse ("0.25 s pulse" vs the model's 0.78 s). Every percentage in the Summary Improvements table —
  the 375 % on kL_surf, 106 % on vial volume, 100 % on etaF, 43 % on etaF_OER, 27 % on pulse_floor —
  comes from that superseded model, so the improvement ranking is not the current model's ranking.

## Operating state and documentation drift

- The workbook sits at **25 °C**, while `README.md`, `protocols/README.md` ("Run temperature — 30 °C")
  and `dissolved-oxygen.md` (7.54 mg/L span, 30 °C compensation) all specify 30 °C, `Biology!E17`
  says "C. necator optimum ~30 °C", and `Biology!E21` justifies the Henry constant by what it
  "reproduces … at 30 degC". Three artefacts now disagree on the operating point: workbook
  25 °C/1000 rpm, twin 30 °C/500 rpm, protocol pack 30 °C.
- **Three water properties are frozen at 30 °C while T is live**: `sigma` (0.0712 N/m), `rho_L`
  (995.65), `D_O2` (2.249e-9). At 25 °C the Han & Bartels fit the sheet itself cites gives
  D_O2 = 1.998e-9 — **12 % high**, so `kL_surf` (∝ √D) is **6 % high**, biasing the very margin in B1.
- The wave-1 status table above still lists H-2/H-3/H-4 as OPEN, and its headline numbers
  (178 min, DO 1.94 mg/L, pH 6.31, HOCl 8.88 mg/L, margin 586×) no longer match the file
  (181 min, 1.37 mg/L, 7.38, superseded, 669×).
- Stale in-sheet cross-references: `E107`/`E125` name "Cl2_prod (D134)" and "free_HOCl (D139)" —
  neither name exists (D134 is `P_HOCl`, D139 is `HOCl_ss`); `E132` says "~0.26 mA" where D132 is
  0.112 mA (0.26 mA is the retired 5 cm² anode); `E89`/`E132`/`E134` cite "the shipped 2.85-min cap"
  where D89 is 3.09 min and is not shipped; `E128` says "~100 % >50 mM" of a cell holding 0.5;
  `E107`/`E125` claim "~40× overstatement" where the as-written ratio is 25.4×.

## House-rule hygiene (CLAUDE.md)

- **Colour conventions.** Summary D2:D8 — the seven cells a user is actually meant to edit — carry no
  blue input font, along with ~25 further hand-entered cells. Purple (fixed-constant) font sits on
  three formula cells (`Electrochemistry!D11`, `D12`, `Chemistry!D130`). The two headline ANSWER cells
  (`Mass Transfer!E90`–`E92`) use a fill outside the six-level legend, so their confidence is
  unreadable. Pink `FFFFC7CE` means DATA GAP in one Summary key and "Problem" in the other, and
  `Biology!E44` deliberately reuses it for hazard.
- **Data-gap flags on dead cells.** `Geometry!D16/D17` carry the pink flag and are, by their own
  notes, read by no formula; the values actually consumed (reactor-type table `F84:F87`, `D84:D87`,
  `G84:G87`) carry no confidence fill and no source at all.
- **Provenance.** ~28 named cells have no column-E note (including `DO_ss`, `spg_dur`, `spg_int`,
  `CO2_sd_ratio`, and all four organism DO thresholds); `Mass Transfer!E99`–`E106` all read
  "From Dosing." — including two handbook constants and a design assumption.
- **Reference by name.** 58 cross-sheet references sit outside the sanctioned import blocks
  (Summary's entire results/checks block, 35 of them), and every lookup table is addressed as a raw
  range with a positional column index — inserting one column into `Geometry!$A$84:$I$87` or
  `Electrochemistry!$A$35:$N$38` silently corrupts every dependent value, which is exactly what the
  "cell position is irrelevant" rule exists to prevent.
- **Embedded data.** `52460` in seven Chemistry formulas; `5.06` and `14007`; `298.15` in the van 't
  Hoff row; the Gerrit fit constants 1.03 / 2.6 inside `IFERROR`; the knallgas 6/2/1 fallbacks;
  `32` (O₂ g/mol), `1.5` (shear limit), `5` (OD window), `0.5` (target-DO fallback), `9999` sentinels
  in Mass Transfer; `8.314`, `96485`, `273.15` and a water-density polynomial in Calibrations —
  where `R_gas` and `F_const` exist as named cells and disagree in the 5th digit.
- `R_gas` is defined twice with different values (`Chemistry!D9` = 8.314, `Mass Transfer!D101` =
  8.3144626180). Six media-composition cells (`Chemistry!C25, C28, C33, D27, D29, D30`) hold a value,
  carry no name, and appear in no SID/PT formula — a future non-zero entry there is silently ignored.
- **Hyperlinks.** 5 of 63 internal links point at the wrong cell: `Summary!E36` → `Chemistry!D139`
  where the value comes from `D145`, and a consistent off-by-one-row drift on `Geometry!E5`,
  `Electrochemistry!E8`, `Biology!E7`, `Biology!E8`.
- **Conditional formatting.** Four rules sit on numeric cells that cannot satisfy them while the
  verdict they were written for is unformatted (`Electrochemistry!D13` vs `D20`; `Biology!D37` vs
  `D44`; `Mass Transfer!D35` vs `D59`; `Mass Transfer!D72` vs `D95`); Geometry's only CF is on lookup
  cells while `geom_check` has none; Chemistry has no CF at all despite three verdict cells;
  `Summary!D26`'s passing state ("×2.0 OK") matches no rule.
- `calcPr` carries no `fullCalcOnLoad`, and `_xludf.MAXIFS` plus the `#DIV/0!` caches show the last
  write came from a non-Excel engine.

## Changes applied (2026-08-12) — `electroPioreactorGasModel-wave4.xlsx`

The fixes were applied to a **copy**, `Media/electroPioreactorGasModel-wave4.xlsx`, because a
`~$electroPioreactorGasModel.xlsx` lock file shows the live workbook is open in Excel and the house
rule is one editor at a time. Close Excel, check the new file, then swap it in:

```
mv Media/electroPioreactorGasModel-wave4.xlsx Media/electroPioreactorGasModel.xlsx
```

Every changed formula ships with its cached value dropped and `fullCalcOnLoad` set, so Excel
recomputes the whole book on open; `calcChain.xml` was removed and rebuilds itself. New parameters
were appended at the bottom of each sheet, which is what the cell-discipline rule sanctions.

### The electrochemistry is now calculated rather than asserted

This is the substantive change. The sheet previously contained no electrochemistry beyond Faraday
bookkeeping on an empirical current fit: both faradaic efficiencies were set to 1, no electrode
potential or cell voltage existed anywhere, and the peroxide the sheet's own 2-electron oxygen
reduction implies was not modelled at all.

- **Cathodic faradaic efficiency** (`Electrochemistry!etaF_calc`) is computed from the oxygen that
  competes for the cathode current: `i = n·F·k_m·C·A` at the design dissolved-O₂ level, with k_m from
  the Eisenberg–Tobias–Wilke correlation. **0.974** at the operating point, **0.900** if DO ever ran
  to the inhibition ceiling. `etaF` now falls back to this instead of to 1, so the net-O₂ chain is
  self-consistent for the first time.
- **Anodic faradaic efficiency** is `1 − chlorine share − metal-dissolution share`; chlorine takes
  **2.5%** of the anodic current at the chloride mass-transport limit, giving **0.975**. It is still
  an upper bound while the metal-dissolution charge is a data gap — and that is now stated rather
  than hidden behind a "chloride-free medium" note on a medium that contains chloride.
- **Hydrogen peroxide** (new block): the 2-electron branch of that cathodic oxygen reduction produces
  **0.94 mg/L/h**. A growing culture clears it — catalase gives a ~3 min half-life at 10⁸ cells/mL,
  so the steady value is 0.064 mg/L against a 0.17 mg/L growth-inhibition threshold. **Lag phase does
  not**: with no biomass to scavenge, peroxide passes that threshold in **11 minutes**. That is a
  previously unmodelled, quantified stressor in the exact window where the culture is most exposed,
  and it is a candidate explanation for the Exp-2 death alongside metal leaching. Precedent: Torella
  2015 (PNAS 112:2337) and Liu 2016 (Science 352:1210) ran this architecture and changed cathode
  material because reactive oxygen and metal leaching poisoned the culture.
- **Cell-voltage budget** (new block): reversible 1.229 V + anodic Tafel overpotential 0.894 V +
  cathodic 0.459 V − 0.15 V phosphate-buffer credit + 0.83 V ohmic drop = **3.26 V against the 5 V
  rail**. The ohmic term comes from a Kohlrausch conductivity sum over the medium recipe
  (**0.71 S/m**) and a parallel-cylinder resistance. This is a **testable prediction**: put a meter
  across the electrodes. It also explains, independently, why Gerrit's Law is only validated to 25%
  intensity — the budget runs out of headroom in that region.
- **Electrode potentials at the operating pH**: chlorine evolution needs **0.74 V more** anodic
  potential than oxygen evolution at this chloride level, so the chlorine current is a generous upper
  bound; an O₂-evolving anode sits **0.50 V above** the Cu²⁺/Cu equilibrium, so copper dissolution is
  thermodynamically allowed — which is what the corrosion suspicion needed.
- **Electrode-surface pH** (new): the phosphate buffer's proton-acceptor flux limits the current
  density to about **2.8 mA/cm²** at the modelled 40 µm diffusion layer — and the cell runs at
  **2.83 mA/cm²**, i.e. the verdict cell reads **BUFFER EXCEEDED**. The anode surface acidifies away
  from the bulk pH by an estimated 0.4–1.0 unit, which also pushes it off the phosphate-saturated
  regime that makes neutral-pH oxygen evolution kinetically cheap, so the two effects compound. The
  verdict flips across the factor-of-two uncertainty on the diffusion-layer thickness, so it is
  undetermined until the mass-transfer measurement is done — but "undetermined, and sitting on the
  line" is a far more useful statement than the silence it replaces.

### The model corrections that followed

- **Dissolved O₂ now has a headspace back-pressure term.** Surface stripping can only move oxygen
  into the headspace, so DO cannot fall below equilibrium with it: `DO = H·y_O2·P + surplus/(kLa·V)`.
  The old form assumed an oxygen-free headspace and so predicted a steady DO *below air saturation*
  in a vessel whose headspace runs about a tenth oxygen.
- **That dissolves the whole SURFACE-HELD/SPARGE-NEEDED branch.** The floor term is set by the CO₂
  flush rate, not by the stirring, so the sparge schedule — not kL_surf — governs dissolved oxygen.
  The interval is now the shortest of the carbon-supply bound (181 min) and the oxygen-dilution bound
  (**16.5 min**), and kL_surf moves the answer continuously instead of switching which formula runs.
  At the previously recommended 181 min this model puts DO at **12.5 mg/L, above the 11.7 mg/L inhibition ceiling** — the old recommendation was not merely optimistic, it was unsafe.
- **The CO₂ limit cycle conserves mass.** One pooled inventory (liquid + headspace at Henry
  equilibrium, justified by a liquid-uptake rate 10× the vent rate) decaying through the vent,
  replacing a two-compartment form in which the liquid absorbed 2.4× the CO₂ ever delivered.
- **The pH solve is activity-corrected.** Davies coefficients at the recipe's ionic strength
  (0.1097 M) move phosphate pKa₂ from 7.20 to **6.76**, and a new `pH_meas` reports the activity-scale
  value a glass electrode actually reads. At the new ~16.5-minute schedule the operating pH is **6.60** — inside the HOB band, but only just, which makes the DO-versus-pH trade-off visible for
  the first time: shorter intervals hold oxygen down and push pH down with it.
- **`n_e_Cl` is the constant 2**, water properties (σ, ρ, D_O₂, D_CO₂) track the temperature input
  instead of being frozen at 30 °C, and the target-DO fraction has one definition on Biology with a
  sourced 0.26 fallback instead of an unsourced 0.5.

### Mechanical fixes

`_xludf.MAXIFS` rewritten as the SUMPRODUCT idiom used elsewhere; all 17 `#DIV/0!` cells on
Calibrations guarded; data validation restored on the four Summary selectors (`ElectrodeList` and
`MediaList` defined, `ReactorList` widened to all 22 reactors); `Summary!D14`/`D16` no longer return
`#VALUE!` for an uncalibrated reactor; five wrong hyperlink targets corrected; four mis-targeted
conditional-format rules moved onto the verdict cells they were written for, Chemistry given the CF
it never had, and the Summary green rule extended to match `×2.0 OK`; blue input font applied to the
cells a user actually edits and purple removed from formula cells; the kLa unit contradiction
resolved in favour of 1/h; `Electrochemistry!D45` now takes the submerged length from the achieved
liquid level (+6.5% on every current density); the duplicate gas constant removed; the HOCl, Cl₂ and
nitrogen molar masses and the breakpoint ratio moved out of formulas into named, sourced cells, with
a new `C_eff_Cl2` giving the like-for-like comparison against thresholds quoted as Cl₂; and every
column-E note that contradicted its own cell rewritten.

Four measurement items were added to the Summary improvements table: the electrode mass-transfer
coefficient (one ferricyanide limiting-current run), the electrode gap, a cell-voltage reading, and a
dissolved-metal assay.

### What remains open

The revised workbook has not been through Excel. The structural checks it has passed are: XML
well-formedness on every part, all 525 defined names resolving and in scope on the sheets that use
them, no formula token unresolved, no orphaned shared-formula group, cells and rows in order, and a
Python evaluation of every new block reproducing the numbers quoted above. What that cannot catch is
an Excel-specific parse difference. **Open it, check the Summary reads sensibly, and save.**

**Excel rejected the first delivery** (2026-08-12) with "repaired records: cell information" on
Geometry, Electrochemistry and Biology. Cause: the editor used to make these changes preserved a
cell's cached value while dropping its `t="str"` type attribute, so four `HYPERLINK` cells carried a
cached string that Excel then tried to parse as a number. Those are exactly the four cells whose link
target was corrected, on exactly those three sheets — Summary's fifth was rewritten later without a
cached value, which is why that sheet came through clean. Fixed at source (the type attribute now
travels with the value), the whole edit chain was rebuilt from the original workbook, and the
structural check now rejects any non-numeric cached value that lacks a type attribute. Scientific
notation was also normalised to Excel's uppercase-E form. **Discard the repaired copy Excel produced
and use the re-delivered file** — Excel's repair removes content rather than fixing it.

Two independent re-implementations (the Python twin, rewritten from the new formulas, and the
sensitivity script) reproduce the electrochemistry block to 5–6 significant figures, and between them
caught a regression introduced by these very fixes: the guard that stops the Calibrations tab showing
`#DIV/0!` returns *text*, and text is not an error, so the consumers' `IFERROR(cal_x, default)`
wrappers would never have fired — `etaF` would have become that message string and every arithmetic
consumer would have gone `#VALUE!` on the first recalculation. All sixteen consumers now test
`ISNUMBER`, which is what the CO₂-flow consumer already did. Worth stating plainly: a fix that looked
purely cosmetic would have broken the workbook, and only an independent implementation caught it.

---

## Checked and clean

Van 't Hoff form, signs and all eight ΔH/K₂₅ pairs (worst K error 2.5 % over 15–40 °C, on a constant
irrelevant at pH 7); all nine molar masses within 0.014 g/mol; both media SID/PT/NT/Cl sums exactly,
with NH₄⁺ correctly outside SID and NaHCO₃'s Na⁺ correctly a strong cation; the charge-residual
expression species-by-species; the 51-row pH grid, its strict monotonicity, the `n_cross` guard and
the interpolation (0.0009 pH against an exact bisection root — independently re-solved). All 76
VLOOKUPs use exact match with correct column offsets; all four selector IF-chains cover exactly their
list values and `NA()` otherwise. Faraday's law with z = 2/4 giving exactly 2:1 H₂:O₂, the ideal-gas
conversion, the ORR split, the shape-aware wetted-area algebra, the current-density ladders and the
"EXCEED at max power" verdict. Tate's law, Mendelson rise, Higbie penetration, holdup and interfacial
area, the sub-mm bubble cut-out, carryover, tip-speed shear, the OD window (which correctly follows
the schedule *in use*), and the pulse-floor and interval-validity checks. Henry constants and their
van 't Hoff coefficients against Sander (2023); the O₂ ceiling chain 0.30 atm → 364.77 µM, with the
lookup table honestly explaining its own 11.5 mg/L discrepancy. The knallgas 6:2:1 uptake against
2:1 electrolytic gas — `O2_excess = CO2_cons` is a structural consequence, not a coincidence. No
circular references; no undefined names; every `cal_*` output except `cal_flow` consumed; the
Calibrations regression and averaging blocks key on the correct column in every table; sinter grade
breakpoints match ISO 4793/DURAN exactly. Zero formula cells missing a cached value.

---

# Wave-1 adversarial review + independent cross-check (2026-06-25)

This is the headline review record. It consolidates a multi-expert adversarial pass over `electroPioreactorGasModel.xlsx` (the **non-modular** workbook: 7 sheets, includes Chemistry) with a from-scratch independent Python reimplementation. The phase-by-phase change history from earlier passes follows below and is retained as the audit trail.

> **Scope note.** Every cell address in this section resolves against `Media/electroPioreactorGasModel.xlsx` (the non-modular file). The modular workbook on this branch (`electroPioreactorGasModel-modular.xlsx`, 6 sheets) has **no Chemistry sheet yet** and uses different Mass-Transfer addresses; the H-1/H-5 (Chemistry) and Mass-Transfer fixes below must be re-applied at the modular addresses when the Chemistry block is ported.

## The eight review dimensions

The model was examined along eight independent dimensions. Each is summarised with what it found.

1. **Dimensional / unit consistency.** Traced end to end. Every derived cell is dimensionally clean; no unit errors. The geometry→electrolysis→Henry→dosing→bubble/strip→surface→pH chain balances. *Clean.*
2. **Formula / reference integrity.** All ~190 defined names resolve, no out-of-range lookups, no circular references (the mode-switched `spg_dur`/`spg_int` confirmed acyclic). Found the H-2/H-3 ref defect: a feasibility-ceiling quantity (`surf_strip`, `Mass Transfer!D73`) wired as a subtractive credit inside two safety guards. *One structural defect.*
3. **Arithmetic vs. independent recompute.** Every output re-derived from inputs in plain Python (`electroPioreactorGasModel.py`); 77/77 match within 0.5%. The defects found are modelling-logic and labelling errors, **not** calculation errors. *Arithmetic faithful.*
4. **Selector / error-by-design logic.** All four dropdowns reject out-of-list values (`errorStyle=stop`); `sched_mode` returns `NA()` on anything but Optimal/Manual. *Clean.*
5. **Chemistry / electrochemistry physics.** Found H-1 (`Chemistry!D36` SID_mc02 drops Mg²⁺/Ca²⁺ charge) and H-5 (`Chemistry!D109` bleach_flag labels a CaCl₂ medium "chloride-free" while D125 red-flags 8.88 mg/L HOCl). Confirmed `etaF_OER=1` and `z_e_ORR=2` are recipe/literature-defensible. *Two findings, one already fixed.*
6. **Mass-transfer / O₂ regime logic.** Found H-2/H-3/H-4: the surf_strip credit disables the frequency cap (`D89`, reads ~1.5×10⁸ min vs intended 2.85 min) and the O₂-vent duty (`D87`, clamps to 0), and the vent-leg note (`D75/D76/E76`) labels a mole ratio a "fraction" and claims the vented-gas DO is "≪ ceiling" when it is above it. *Three findings, open.*
7. **Data-gap / provenance discipline.** Audited every flagged gap. Most are genuine physical measurements correctly listed in Improvements (vial wall/volume, cathodic FE, organism DO bands); only a few are literature-citable. Colour conventions (column-E fill = confidence, column-D font = provenance) applied consistently. *Discipline sound; see data-gap conclusion below.*
8. **Documentation / citation accuracy.** Found `knallgas-stoichiometry.md` re-attributes the 7:2:1 feed optimum to the wrong paper (a lag-phase paper); `dissolved-oxygen.md:33` mislabels the 11.5 mg/L Wilde & Schlegel datum as a Henry conversion; sheet note `Biology!E38` overstates H₂/O₂ relative solubility. *Three doc corrections.*

## Verified bug findings (cell refs + status)

| ID | Cell(s) | Finding | Status |
|---|---|---|---|
| **H-1** | `Chemistry!D36` (SID_mc02) | Cation side omits Mg²⁺ and Ca²⁺ while the anion side subtracts their sulfate: 38.51 mM instead of 46.13 mM, giving pH 5.89 against the documented validated MC02 pH 6.10. Latent (only bites when MC02 is selected; current media is UdG), but it mis-trips the `D110` "<6.5 — reduce CO₂ dose" advisory. | **FIXED** (commit `53b8b3d`; corrected SID = 46.13 mM, pH 6.10 restored. NH₄⁺ correctly stays out of SID, entered via NT_mc02.) |
| **H-2** | `Mass Transfer!D89` (spg_int_max) | Best-case ceiling-evaluated `surf_strip` (D73) ≈ 1.85× `O2_net_gen`, so the denominator `O2_net_gen − surf_strip` clamps to 1e-12 and the frequency cap reads ~1.5×10⁸ min. Intended form `target_DO_frac × t_O2_ceiling_lag` = 2.85 min. Feeds `D91 = MIN(178 min, spg_int_max)`, so this **changes the headline interval 178 → 2.85 min (62×)** and removes the DO-ceiling-breach guard. | **OPEN — judgement call.** Revert to the lag-sized cap now, or replace with the steady-growth sawtooth (Improvement 1)? |
| **H-3** | `Mass Transfer!D87` (duty_O2vent) | Same root cause: `surf_strip > O2_net_gen` so `MAX(O2_net_gen − surf_strip, 0) = 0`, the O₂-vent duty clamps to zero, and `duty_opt` binds on carbon not O₂. The `D88` note "O2-venting binds, not pH" is now **false**. | **OPEN — judgement call** (same fix style as H-2; also correct the D88 note). |
| **H-4** | `Mass Transfer!D75/D76/E76` (vent leg) | `y_O2_vent` (D75) = `O2_excess/CO2_supply` = 0.5 is a mole **ratio** mislabelled "fraction"; `DO_vent_eq` (D76) = 559.5 µM is **above** the 335.7 µM ceiling (Biology D28), yet note E76 says "≪ ceiling → vent-feasible". Even the corrected mole fraction (0.333) gives 373 µM, still above ceiling. Both are leaf cells — zero blast radius. | **OPEN — judgement call.** D75 → `O2_excess/(O2_excess+CO2_supply)`; E76 → state vented-gas DO sits above the ceiling, so the vent leg is not a comfortable kL-independent backstop. |
| **H-5** | `Chemistry!D109` (bleach_flag) vs `D125`/`Summary!D36` | With UdG selected, `pH_Cl` = 0.18 mM (from UdG's 0.01 g/L CaCl₂) sits below D109's arbitrary 0.5 mM gate, so D109 reads **"chloride-free: no bleaching"** — while `D125` = 8.88 mg/L HOCl (≈9× the sheet's own ~1 mg/L bactericidal threshold) fires the `Summary!D36` red band. Two adjacent cells make opposite claims about the same chloride; "chloride-free" is factually wrong for a CaCl₂ medium. | **RESOLVED.** `bleach_flag` (D109) re-keyed from the unsourced 0.5 mM chloride cut to `HOCl_max > 0.2` mg/L free chlorine (Phase 1.12); the cell now reads off the HOCl ceiling, so D109 and D125 agree. Two residuals also fixed: (i) the **E109 note** previously asserted a "chloride-free assumption" and is now corrected to read off free chlorine; (ii) the **Python twin's stale bleach gate** (`HOCl_max > 1`) is being fixed separately to match the new 0.2 mg/L re-key. |

**Root cause shared by H-2/H-3/H-4** (`Mass Transfer!D73`): `surf_strip` is a legitimate feasibility *ceiling* for the diagnostic ratios `surf_ratio` (D74) and `O2_removal_ratio` (D78), but it must not be a subtractive credit inside *safety guards*. A 375%-uncertain `kL_surf` proxy (D70) silently switching off two O₂ guards is the structural defect. All three trace to commit `9bb2bed` ("sparge interval credits surface O2 stripping… not zero"), which implemented a deferred enhancement by **disabling** the guard rather than replacing it with the planned steady-growth sawtooth.

## Data-gap conclusion

Almost nothing in the data-gap set is a literature plug-in. Most flagged gaps are **genuine physical measurements** on the actual rig (caliper/water-fill/gas-collection) or operator setpoints, correctly listed in the Improvements section and not to be invented:

- **Physical measurement (do not invent):** `Geometry!D16/D17` (vial total volumes — water-fill), `D19` (vial wall — high-leverage caliper), `D12/D13/D28/D32/D47` (bore depths, build clearances); `Electrochemistry!D18` (cathodic H₂ FE — HIGH impact, gas-collection); `Electrochemistry!D37` (sparger lookup row — needs the real electrode spec); `Biology!D57` (UdG mixed-consortium DO band — HIGH impact, drives every DO/sparge verdict).
- **Literature-citable (the genuinely fillable few):**
  - knallgas uptake ratio 6:2:1 (`Biology!D10/D11/D12`) — keep central values, cite **Lu & Yu 2019** (uptake-ratio ranges) and **Ishizaki 2001** (7:2:1 feed optimum). Exact culture value needs a growing culture; the literature central is defensible.
  - `etaF_OER = 1` (`Electrochemistry!D26`) — confirmable from the recipe (chloride-free → no competing Cl₂ evolution).
  - `z_e_ORR = 2` (`Electrochemistry!D27`) — 2e⁻ peroxide pathway, SS cathode, neutral pH; literature-supported.

## Independent-model cross-check

A from-scratch independent reimplementation (`Media/electroPioreactorGasModel.py`, standard library only) re-derives every final output from input parameters and physical/chemical constants — **not** read back from the workbook's cached values. It mirrors the sheet structure but re-implements the arithmetic cleanly from the documented formula logic.

**Result of this run: 77/77 outputs match the spreadsheet within 0.5% (text flags exact).** The run prints a per-output table (spreadsheet vs model vs MATCH) and the closing line `77/77 outputs match the spreadsheet within 0.5%.` with no mismatches. Headline outputs confirmed: CO₂ pulse 0.78 s (rounds to 1 s), sparge interval 178 min, steady-state DO 1.94 mg/L, endpoint pH 6.31, max HOCl 8.88 mg/L, carbon margin 586×, H₂ headspace EXPLOSIVE, organism-DO data gap flagged.

The cross-check confirms the spreadsheet's arithmetic is internally faithful: the defects above are modelling-logic and labelling errors, not calculation errors. (Note the 178-min headline is the *current* live value — it is exactly what H-2 inflates; reverting H-2 to the lag-sized cap would drop it to 2.85 min.)

## Improvements (ordered)

1. **Replace the two O₂ proxies with the deferred steady-growth sawtooth** (the clean structural fix that makes H-2/H-3/H-4 go away properly instead of by reverting to lag-conservative forms). Highest leverage.
2. **Until `kLa_meas` is entered, force the schedule onto the lag-conservative O₂ cap** — never let the 375%-uncertain `kL_surf` proxy (D70) gate a safety guard. (The structural guard behind H-2/H-3.)
3. **Per-cell regime labelling** (`Mass Transfer!D87/D89` vs `D108`): state which O₂ figure each cell uses — lag = `O2_net_gen` (5.31e-5), steady = `O2_excess` (1.77e-5, ~3× smaller). A reader treats it as one schedule; it mixes worst- and best-case.
4. **Carry the headspace uncertainty band onto the headline** (`Mass Transfer!D77` → `Summary!D13/D15`): the interval depends on the un-measured `headspace_V` via `hs_flush_time`; propagate the ~4× band, and confirm `hs_flush_time ≈ carbon-limited interval` is genuine, not a coincidence masking a non-binding flush cap.
5. **`u_sg` (D47) — use the insert-free flow area** for the carryover check (D59); full-bore area biases velocity low ~15%, non-conservative.
6. **Don't sum bubble-path and surface-path strip as co-existing steady states** (`O2_removal_ratio` D78 = strip_avg + surf_strip): the swarm never establishes at this sub-second duty; annotate as order-of-magnitude.
7. **Jetting case should also invalidate `d_bubble`** (E64/D42): the regime flag currently only zeroes the sub-mm sinter case, not a high-We jetting case.
8. **`target_DO_frac` (D84) reference consistency:** define optimum and toxic against one reference concentration.
9. **`spg_dur_opt` (D90) flush sizing** assumes CO₂ breakthrough; note the effective flush is smaller during the unsaturated establishment phase.

## Sensitivity ranking (informs the measurement priorities)

`electroPioreactorGasModel-sensitivity.py` was updated to the current live model (calibrated Q_CO2 = 199.8 mL/min for ed04, z_e_ORR = 2, H_O2ref = 1.2e-5, the surf_strip-credited guard form) and re-run. Its baseline reproduces the live 178.1-min schedule, confirming fidelity. Urgency = leverage on the schedule-critical outputs × ignorance (KNOBs excluded as control levers). Ranked data-gaps/estimates to pin down:

1. **`kL_surf_factor`** (surface kLa, DATA-GAP) — **375%** swing. The entire O₂-management strategy rests on the stirred-surface→headspace path and `kL_surf` is only a coarse renewal-theory proxy. Measure by gassing-out. (This is also why H-2/H-3 are dangerous: a 375%-uncertain quantity gates a safety cap.)
2. **`etaF`** (cathodic H₂ FE, DATA-GAP) — ~100%. Drives throughput, the O₂ balance, and the schedule. Gas-collection over a known charge.
3. **`bio_O2`** (O₂:H₂ uptake ratio, DATA-GAP) — ~95% on the steady O₂ surplus. Needs a growing culture; use the lean-O₂ end (1.8) as the growth-protective default meanwhile.
4. **`V_max`** / actual charge volume (ESTIMATE) — ~106% on the schedule (it sets headspace and flush sizing).
5. **`bio_CO2`** (~48%, schedule), **`pulse_floor`** (~27%, the recommended pulse *is* `pulse_floor` — trivial to bench-characterise), **`etaF_OER`** (~43% on removal), **`O2_ceil_atm`** (~33%).
6. Literature constants (Henry O₂/CO₂/H₂, σ, ρ, D_O₂, Mendelson) show ≤17% leverage but are known to a few %, so their urgency scores are ≤2.5. **Knobs:** `intensity` (~99% on schedule), `carbon_margin_min` (~67%), `stir_rpm` (~63%) are the deliberate control levers.

## Open questions for Martin (gate the OPEN findings)

1. **HOCl/bleach threshold (gates H-5). RESOLVED (Phase 1.12).** `bleach_flag` (D109) now keys off `HOCl_max > 0.2` mg/L free chlorine — the WHO minimum free-chlorine residual / lower bound of the published free-chlorine MSC range (0.021–0.39 mg/L), a precautionary floor rather than an organism-specific MIC. E109 note corrected (was "chloride-free assumption"); Python twin's stale `>1` gate being fixed separately.
2. **O₂-guard fix style (gates H-2/H-3).** Quick revert to the lag-conservative cap now (restores the 2.85-min guard immediately), or hold for the steady-growth sawtooth (Improvement 1, larger but the right long-term model)?
3. **`target_DO_frac` intent (D84):** fraction of the same ceiling `O2_ceil_C` represents (inhibition concentration), or of a separate toxic reference?
4. **Modular port:** track a port-checklist in TODO.md for re-applying the H-1/H-5 Chemistry fixes and the Mass-Transfer fixes at the modular addresses once the Chemistry block is ported?

---

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
- `H_O2ref` 1.2e-5 mol/m³/Pa — consistent with O₂ solubility (~1.24e-5 from 1.26 mmol/L at 1 atm); the live workbook value 1.2e-5 nails 7.50 mg/L air-saturation at 30 °C, 1 atm. ✓ (was recorded as 1.3e-5 in an earlier pass; superseded by the calibrated 1.2e-5.)
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

## Phase 1.8 (CO2-optimiser) — full audit pass
Every cell re-checked for stale assumptions, self-flagellation, logic, arithmetic, links and citation accuracy.
- **Arithmetic/logic/links:** all 14 sections recomputed independently — consistent, no errors. 189 names resolve, no out-of-range, **no circular references** (the mode-switched `spg_dur`/`spg_int` confirmed acyclic), selectors + `sched_mode` dropdown intact.
- **Citation/data accuracy:** all literature values re-verified against sources and hold (F, R, M_CO2, σ, ρ, D_O2 fit, Henry O₂/CO₂/H₂ + T-coeffs, Mendelson, DURAN, Clary etaF, Ishizaki/Lu&Yu, Amer&Kim ceiling). **One factual error fixed:** §13 claimed "H₂ ~6× less soluble than O₂" — corrected to the true Henry ratio. (The earlier "~1.7×" figure was computed against the superseded `H_O2ref` = 1.3e-5; against the live, calibrated `H_O2ref` = 1.2e-5 the O₂:H₂ Henry ratio is now **~1.5×**, and the O₂:CO₂ ratio ~28×.)
- **Outdated assumption fixed:** `O2_ceil_uM` note said the DO floor is "set by stripping capacity" (pre-§11, bubble-only) → now "O₂-removal capacity (§11)".
- **Self-flagellation / process notes removed** (kept the science): the "Audit: corrected from…/replaced…" lines on etaF/D_O2/O2_ceil, "was unused" (a_surf), "was implicitly… now explicit" (spg_len), "the verdict cell was removed" (sched_bal), "flow-dependence not modelled" → "valid in the quasi-static regime (see §10)".
- **Stale link removed:** the old mis-citation URL (aem.02007-22) left on the §3 header rows.
- **Minor:** dropped uncertain "form-II" RuBisCO qualifier; "~22×" → "~20×" (Optimal-mode default); fixed a `<12 h lag` attribution (Amer & Kim, not Ishizaki).

## Phase 1.9 — comprehensive sensitivity & urgent-attention ranking (2026-06-17)
Re-ran `electroPioreactorGasModel-sensitivity.py` (rewritten to cover the full model incl. §13/§14, in Optimal mode) over **every non-absolute input** (29 of them; only the defined/exact constants — Faraday, R, g, atm, electron counts, M_CO2, T_ref — excluded). Each input carries an *ignorance tier*; urgency = leverage on the critical outputs (recommended schedule, O₂ time-to-ceiling, O₂-removal feasibility, surface ratio, H₂-escape time) × how poorly we know it. Knobs are reported separately as control authority, not "attention".

**Urgent to pin down (measure these):**
1. **Surface kLa** (`kL_surf_factor`, DATA-GAP) — by far the biggest (≈375% swing on O₂-removal feasibility). The entire O₂-management strategy rests on the stirred-surface→headspace path, and `kL_surf` is only a coarse renewal-theory proxy. Measure by gassing-out (dynamic DO). Even at the low end (¼×) removal stays >1, but this is the dominant unknown.
2. **etaF** (cathodic H₂ faradaic efficiency, DATA-GAP) — ~100–150%; drives throughput, the O₂ balance *and* the recommended schedule. Measure by cathode-gas collection / H₂:O₂ ratio.
3. **`pulse_floor`** (solenoid minimum reliable pulse, DATA-GAP) — ~140% on the schedule. The recommended pulse duration **is** `pulse_floor`, and the interval scales with it, so bench-characterising the solenoid directly fixes the operating schedule. Trivial to measure — do it first.
4. **`bio_O2`** (O₂:H₂ uptake ratio, DATA-GAP) — ~95% on the steady-state O₂ surplus. Can't measure until you *have* growth, so use the lean-O₂ end (1.8) as the growth-protective default meanwhile.

**Worth refining (ESTIMATE tier, moderate leverage):** `etaF_OER` (~43%), `O2_ceil_atm` (~33%), `V_max`/actual charge volume (~20% on the timescales), the Gerrit fit (`gerrit_int`/`slope`, ~8–14%).

**Conditional — matter only off the current operating point (OAT-at-baseline misses these):** `z_e_ORR` is inert while etaF=1 (only bites once etaF<1); `bio_CO2`, `Km_CO2`, `H_CO2ref`, `carbon_margin_min` are all ~0 because carbon is ~586× saturating and the O₂-vent floor binds the schedule, not carbon. If you ever dose far less CO₂ or measure etaF<1, re-rank.

**Don't bother:** the literature constants (Henry O₂/CO₂/H₂, σ, ρ, D_O₂, Mendelson coeffs) show 8–15% leverage at most but are known to a few %, so their urgency scores are ≤2; `u_g_max` carryover has 150× margin.

**Knobs (you turn these deliberately):** `Q_CO2` (~150% on schedule) and `target_DO_frac` (~120%) are the dominant schedule levers; `intensity` (~80%) sets gas generation; `stir_rpm` (~63%) sets the surface removal. `carbon_margin_min` does nothing (O₂-venting binds, not carbon).

Caveat: this is one-at-a-time about the current baseline; it deliberately does not capture interactions (e.g. `z_e_ORR` × etaF). The "conditional" note flags the ones that are silent only because of the baseline.

## Phase 1.10 — fixes from Claude Desktop review (2026-06-17)
1. **`t_O2_ceiling_rem` (lag) used the steady surplus** — corrected `O2_excess` → `O2_net_gen` (lag regime: cells aren't consuming, so removal must offset the full net O₂). Went further than the review: **both `t_O2_ceiling_rem` and `O2_removal_ratio` were double-counting `O2_cathode_ORR`** (it's already inside `O2_net_gen`/`O2_excess`), so the explicit `-O2_cathode_ORR`/`+O2_cathode_ORR` terms were dropped. Invisible at etaF=1; wrong at etaF<1. Reproduced the review's weak-stir case (130 rpm/4 mm): now 15 min, not "9999 holds".
2. **`sched_mode` errored on invalid input** — `spg_dur`/`spg_int` now return `NA()` for any value that isn't `Optimal` or `Manual` (was silently falling through to Manual).
3. **Dropdowns now reject out-of-list entries** — `showErrorMessage`/`errorStyle=stop` enabled on all four validations (D16/17/18/236).
4. **`u_rise` #N/A cascade note corrected** — now states the cascade reaches §7, §9 (per-pulse), §10 (`t_O2_ceiling_strip`) and §11 (`O2_removal_ratio`/`t_O2_ceiling_rem`); §14 optimiser independent. Behaviour kept (the error is intended for unsupported fine sinters).
5. **`H2_safety` gated on the real condition** — `H2_turnover>1` (H₂ escaping to headspace) rather than `rH2_gen>0` (always true). Honest note that it's on at any useful current.
6. **`duty_O2vent` robust to surface pressure** — `O2_ceil_atm` (implicitly the mole fraction) → `O2_ceil_Pa/P_atm`. No change at 1 atm.

Deferred (agreed enhancements, not bugs): the inter-pulse DO-sawtooth replacement for the two O₂ proxies (`duty_O2vent` + `spg_int_max`), and a steady-growth schedule alongside the lag-sized one. Both improve robustness/efficiency without moving the current answer.

## Phase 1.11 — reviewability: concise notes + graceful sinter message (2026-06-17)
- **Notes tightened** to ~64 chars avg (from multi-sentence), sources and caveats kept — word-count down without losing accuracy, since human review is the live risk.
- **#N/A replaced with a clean message.** Fine sinters (sub-mm bubbles) no longer cascade #N/A: `u_rise` computes plainly, the bubble strip term `strip_sparge` is excluded (=0) for d_bubble<1 mm, and `bubble_regime` reads **"Sinter OOR – add fine-bubble model"**. The surface path (§11) still yields a valid O₂ answer, so a fine sinter reads as a known model-scope gap, not a fault.
- Cleared the redundant hydrogenase-clarification row (folded into the `O2_ceil_atm` note).

## Phase 1.12 — wave-3 completion: sparge-model fix, Chemistry verification, HOCl threshold (2026-06-26)

**Sparge-model fix (applied).** Confirmed the surface-O2 best-case proxy (`kL_surf`, ~375% uncertain) was silently disabling two safety guards: `surf_strip` (D73, 9.79e-5 mol/h) exceeded `O2_net_gen` (5.31e-5), so `duty_O2vent` (D87) clamped to 0 and `spg_int_max` (D89) blew up to ~1.5e8 min. The physics is sound (first-order self-limiting surface sink; `DO_ss` is an asymptote, not unbounded accumulation; τ ≈ 3.1 min), and the correct rule is to size the *safety guard* on the worst-case surface-uncredited lag source while keeping the surface credit *diagnostic-only*. Applied:
- New `O2_src_guard` (D132 = `O2_net_gen`), the surface-uncredited guard source. `duty_O2vent` (D87) and `spg_int_max` (D89) now key off it — the `MAX(0,…)` clamp and `MAX(1e-12,…)` denominator are gone.
- `spg_int_max` corrects to **2.846 min** and binds `spg_int_opt` (D91): the headline interval drops **178 → 2.85 min**.
- `opt_binding` (D94) gained a leading **"O2-CEILING"** branch (the fix exposes a latent mislabel: post-fix the 2.85-min cap binds D91 for the first time, and the old D94 would have fallen through to "O2-FREQ", reporting the wrong binding mechanism).
- New diagnostics: `DO_ss_sawtooth` (D133, steady source, 18.07% of ceiling, "SURFACE-HELD"), `spg_int_regime` (D134), and the paired lag readout `DO_ss_sawtooth_lag` (D135, 54.20% of ceiling — what the shipped guard actually banks on). E73/E88 notes re-fence `surf_strip` as a feasibility ceiling only.
- **D75 mole-fraction correction:** `y_O2_vent` changed from `O2_excess/CO2_supply` (a ratio) to `O2_excess/(O2_excess+CO2_supply)` (a true mole fraction). *Correction to the synthesis worked example:* at the live ed04 operating point `O2_excess` (1.77e-5 mol/h) ≪ `CO2_supply` (2.21e-3), so `y_O2_vent` ≈ 0.0079 and `DO_vent_eq` (D76) ≈ **8.9 µM** — well *below* the ~336 µM inhibition ceiling, i.e. at this CO2 dose the vent leg IS a comfortable kL-independent backstop. (The synthesis's "373 µM, exceeds ceiling" figure assumed `O2_excess ≈ CO2_supply`, which does not hold here; the E76 note was written to the true computed value.)

The Python twin (`electroPioreactorGasModel.py`) was updated to the corrected sparge logic and now reproduces all of this: **80/80 outputs match within 0.5%**, including `spg_int_opt = 2.846 min` and `opt_binding = O2-CEILING`.

**Chemistry sheet — independent physical-chemistry verification (wave-2).** Re-derived every load-bearing quantity from first principles (workbook XML parsed directly; openpyxl/PyPI firewall-blocked) at T = 303.15 K, active medium UdG phosphate (Summary!D5). (a) **van't Hoff Ka(T):** all eight constants reproduce stored values to machine precision; every K25 consistent with its labelled 25 °C pKa to ≤0.01 unit; every ΔH magnitude/sign matches CRC handbook (incl. the correctly negative phosphate-Ka1 ΔH). One cosmetic mismatch, now fixed: phosphate Ka3 row was labelled "pKa 12.35" but K25 = 4.2e-13 is pKa 12.38 — **relabelled A17 → "(pKa 12.38)"**. (b) **SID + buffer sums:** both SID formulas re-derive exactly; SID_mc02 = 0.0461275 mol/L (Mg/Ca wave-2 fix confirmed correct, each contributes 2× molarity); full salt inventory electroneutral to 0.000; PT/NT/Cl all reproduce. D36's cached 0.046128 is a stale rounded cache that self-corrects on F9, not a logic bug. (c) **HOCl + bleach stoichiometry:** Henderson–Hasselbalch fraction 0.93903, bleach_rate 371.2 mg/L/h, HOCl_max 8.88 mg/L all reproduce exactly; 52460 mg/mol confirmed = HOCl molar mass (correct basis vs Cl2); bleach_flag correctly keys off the chloride-limited ceiling. (d) **pH solve-grid:** root 6.31258 reproduces pH_op exactly and the residual is strictly monotone at baseline — but the grid silently collapsed pH_op to 0.0 if the root fell outside [4,9], producing a physically absurd result with no error surfaced. **Guard added** (`n_cross` helper at D105 + `IF(n_cross=1,SUM(C50:C100),NA())` in D103); pH_fHOCl and pH_band_flag inherit the guarded pH_op. **Bottom line: Chemistry sheet quantitatively correct on every reproducible value; only substantive issue is the now-guarded grid root, plus the now-fixed Ka3 label and the self-correcting stale D36 cache.**

**Free-chlorine / bleaching model — rebuilt as a graded kinetic penalty (Chemistry rows 128–147).** Two earlier versions were wrong in opposite directions: the FE=1 "all chloride → HOCl" ceiling (~8.9 mg/L, alarmist) and then an over-rosy "≈0" that treated the ammonium sink as instantaneous and perfect. The operative model is now kinetic: chlorine production is capped by the chloride mass-transport limit (so it scales with chloride); a steady **bulk** free-chlorine residual `[HOCl]_ss = P_HOCl/(k₁·[NH₃_free])` is non-zero because only ~0.6 % of ammonium is reactive free NH₃ at pH 7 (k₁ = 4.2×10⁶ M⁻¹s⁻¹, Jafvert & Valentine 1992); a longer-lived **combined** chlorine (monochloramine) term is weighted by its ~25× lower biocidal potency; and an anode boundary-layer enrichment factor accounts for the local spike cells/electrode see. The effective biocidal load `C_eff` is read against a **graded** sub-lethal onset (0.1 mg/L) / kill (2 mg/L). For UdG, `C_eff` ≈ 0.68 mg/L → **MILD sub-lethal penalty** — non-zero and real (matches Sydow 2017, DOI 10.1002/elsc.201600252, which attributes the chloride penalty to anodic Cl₂ and shows a chloride-free medium grows lag-free), but not sterilising (matches UdG running for days). It scales to SEVERE only at high chloride/current (Baek 2021). The uncertain parameters (efficiency plateau, `f_local`, monochloramine residence) are exposed as flagged sensitivity inputs — the model's robust claim is the *graded* shape, not a precise absolute. The FE=1 cells are retained, relabelled "naïve, NOT operative".

**Methodologies cross-check.** MC02 mesonutrient recipe agrees exactly across `Methodologies/Crymlyn.md`, `Methodologies/Irvine/Medium.md`, and Chemistry rows 25–33 col C. UdG scoped OUT (no methodology document defines it). Crymlyn "Option B" (KH2PO4-based) and its optional NaHCO3 0.10 g/L are separate add-ons, not the modelled MC02 base.

**Protocol document control.** surface-kla, faradaic-efficiency, knallgas-stoichiometry advanced authored → reviewed (method + cell routing verified, no fixes). dissolved-oxygen, flow-calibration, gerrit-current advanced authored → checked. `vial-geometry.md` and `sinter-porosity.md` were held at authored pending high-severity routing fixes; **both are now fixed and advanced to reviewed** (final-cleanup wave, 2026-06-26). vial-geometry: "Result → model" re-pointed from the superseded Vtot_1/2 (D16/D17) & D_int_1/2 (D12/D13) display cells to the reactor-type lookup table A83:I87 — total vial → col F, usable depth → col D, of the matching reactor row (AEP0.1.1 r84 / MEP0.3 r85 / AEP0.2 r86 / AEP0.2a r87), since the model reads V_vial_total (D24, VLOOKUP col F) and D_int (D22, VLOOKUP col D). sinter-porosity: re-pointed from the read-only import por_grade (Mass Transfer D20 = `=Electrochemistry!$D$32`) and the non-existent "Summary D42 dropdown" to the "sinter porosity" column (E) of the sintered-electrode row (MMO tube, row 37) in the electrode table Electrochemistry A34:I37; the grade follows the selected electrode. `authorised:` left empty throughout — that is a human act.

**Cross-sheet import integrity audit — CLEAN (final-cleanup wave, 2026-06-26).** After Excel reordered the tabs (Chemistry now 4th, document index 3, retaining the out-of-sequence sheetId=7), a full structural audit of the 7-sheet modular workbook found **zero integrity defects from the reorder**. Every defined name (312 total, 284 distinct, all sheet-scoped) has an in-range `localSheetId` that resolves to the sheet its target formula points at — all 38 Chemistry-scoped names use `localSheetId="3"`, correctly resolving to Chemistry's new index. Every cross-sheet formula reference (148 refs) resolves to an existing sheet (Chemistry referenced 2× from Summary, CO2 flows 17× from Mass Transfer). No `#REF`, no dangling names, no true duplicates (the 28 repeated names are legitimate sheet-scoped copies with distinct `localSheetId`s), `fullCalcOnLoad="1"` set. Audited against raw OOXML via stdlib `xml.etree` (openpyxl/PyPI firewall-blocked), corroborated by the Python twin's 80/80 match. The only flagged cells — empty Summary!D9 (media_volume) and D10 (P_atm_set) — are intentional optional-override inputs (labelled "input/blank") with downstream fallbacks (Biology!D19 = `IF(Summary!$D$10>0,…,101325)`), not defects. No workbook edit required.
