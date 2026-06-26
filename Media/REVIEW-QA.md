# Model/Plugin Review Programme — Ledger & Completion Plan (working file, not for upstream)

Durable state for the perfection programme: Martin's decisions + the remaining-work
checklist. On "continue" in a new session, read this file + `git log` and resume.
(Dropping the opaque "H-1/H-2" labels — plain descriptions below, per Martin.)

## Decisions (Martin, 2026-06-25)

| Topic | Decision |
|---|---|
| Plugin PR | **Open it** upstream (PR-ready). |
| LED channel | **Read from config.ini only — no UI control.** Keep in *this* branch; it supersedes `configurable-led-channel` and solves Gerrit's needs too. Structure as **separate commits** (LED-from-config / electrolysis cycling / OD-pause). |
| OD-pause logic | Confirmed. **Pause trumps no-pause**: if electrolysis OR CO₂-sparge requests an OD pause, OD is paused; OD only resumes when the last owner releases. (Owner-set already implemented — matches.) A pause offset that is negative *and* ≥ the ON-time in magnitude → OD runs throughout (unless sparge pauses it). |
| Python model file | Merge sensitivity into one file **iff zero downside** (e.g. one module, separate functions/flag); otherwise keep separate. |
| Sparge O₂-vent guards (the "62×" headline bug) | Do the **proper structural fix** (deferred steady-growth model), abstracted so a **post-grad can check it and a human expert can review it**. Not the quick lag-revert. Accuracy + correctness over speed. |
| HOCl biocidal threshold | **Species-specific from the literature**, added to a generalised species DO/tolerance table; use the **conservative (cell-sensitive) end** of the best-justified value. Not a round 1 mg/L. (Note: water-industry thresholds err high — toward over-disinfection — so don't borrow those.) |

## Completion checklist

**Done & pushed**
- [x] Secret-leak closed (`MCTests/` git-ignored) — `ca917c3`
- [x] MC02 strong-ion-difference number bug (missing Mg²⁺/Ca²⁺) — `53b8b3d`
- [x] Review.md wave-1 record + independent Python model (77/77 within 0.5%) + sensitivity refresh — `00bc7e9`
- [x] Bleach flag corrected + over-budget string trimmed — `0d57db6` (HOCl threshold still **interim 1 mg/L**, see below)
- [x] Plugin: feature + 9 verified review fixes, 113 tests — pushed `plugin/electrolysis-cycling-od-pause` `4279d76`
- [x] Plugin: LED config-only confirmed already in tree (not in published_settings/UI); restructured into 4 topic commits (LED / cycling / OD-pause / review-fixes+docs+v0.7.0) on `f6cd8d1` base, each stage suite-green (61/77/95/113), final tree byte-identical to `4279d76` — force-pushed `35b277c`

**To completion**
- [x] Sparge O₂-vent guards: proper steady-growth model replacing the best-case `surf_strip` credit; verify with the Python twin; document for post-grad/expert review. *(high)*
- [x] HOCl threshold: literature research → species-specific, conservative; add a tolerance column to the species table; replace the interim 1 mg/L in `bleach_flag`. *(high)*
- [x] pH solve-grid: add a sign-flip-count guard (flag/#N/A if the residual crosses ≠ once) — closes a silent-wrong-answer mode off-baseline. *(med)*
- [x] Review.md: add a modular-era **Chemistry-sheet section** — verify each van't Hoff Ka vs handbook ΔH, re-derive both SID formulas + phosphate/ammonium sums, confirm the HOCl/bleach stoichiometry. (wave-1 synthesis predated the tab.) *(high)*
- [x] Methodologies/* media recipes (Crymlyn, Irvine/Medium): cross-check vs the Chemistry MC02/UdG g/L rows, or explicitly scope out. *(low)*
- [x] 8 bench protocols: method-correctness review; advance document-control authored→checked→reviewed (never `authorised`). *(med)*
- [x] Summary Improvements: enlarge to the sensitivity-ranked table (+4 measurement rows). *(med)*
- [x] Spreadsheet dump: regenerate (stale — still shows the pre-fix SID); stamp with the source git SHA. *(infra)*
- [x] Python model: merge sensitivity into one file if zero-downside → **kept separate** (downside is non-zero; see Final-cleanup wave below). *(low)*
- [x] Plugin: LED config-only (already config-only — no change needed), restructured into 4 topic commits, PR opened. *(plugin)*
- [x] Wave-2: not re-run — every gap it identified was plugged individually instead (Chemistry-sheet coverage, stale dump, pH-grid guard, Methodologies cross-check, protocol method-review, cross-sheet import-integrity audit). All closed across the wave-3 + final-cleanup waves.

## Final-cleanup wave (2026-06-26)

Three closing tasks of the perfection programme.

- [x] **Cross-sheet import integrity audit — CLEAN.** Programmatic audit of the 7-sheet modular workbook (`electroPioreactorGasModel.xlsx`) after Excel reordered the tabs (Chemistry now 4th, document index 3, retaining the now-out-of-sequence `sheetId=7`). Audited every defined name (312 total, 284 distinct, all sheet-scoped) and every cross-sheet formula reference (148 refs) against the raw OOXML (openpyxl unavailable; PyPI firewalled — used stdlib `xml.etree` on the unzipped XML, the same authoritative structures). Result: **zero defects from the reorder.** Every `localSheetId` is in range (0–6) and resolves to the sheet its target formula points at — all 38 Chemistry-scoped names use `localSheetId="3"`, which correctly resolves to Chemistry at its new index. No `#REF`, no dangling names, no true duplicates (the 28 repeated names are legitimate sheet-scoped copies, each with a distinct `localSheetId` and own-sheet target). `fullCalcOnLoad="1"` set. Independent Python twin corroborates: 80/80 outputs match within 0.5%. The only flagged items — `Summary!D9` (`media_volume`) and `Summary!D10` (`P_atm_set`) empty — are **by design**: optional user-override inputs, both labelled "input/blank", with downstream fallbacks (`Biology!D19 = IF(Summary!$D$10>0, …, 101325)`). No remediation needed; no workbook edit made.

- [x] **Two held protocols advanced — both → reviewed.** Wave-3 held `vial-geometry.md` and `sinter-porosity.md` at `authored` pending high-severity routing fixes (method correct, write-target dead). Both fixed and advanced to `state: reviewed` (`checked` + `reviewed` = claude-opus-4.8; `authorised` left empty — human-only). Routing verified against the live model (the `.py` twin mirrors the workbook):
  - `vial-geometry.md`: was told to write the back-solved total/depth into `Vtot_1/Vtot_2` (Geometry D16/D17) and `D_int_1/D_int_2` (D12/D13) — all four vestigial display cells marked "Superseded by the reactor-type lookup below; not read by any formula." Re-pointed at the reactor-type lookup table `Geometry A83:I87`: total vial → column F, usable depth → column D, of the matching reactor row (AEP0.1.1 = r84, AEP0.2 = r86), with the shared-geometry pairs noted (MEP0.3 = r85, AEP0.2a = r87). The model reads `V_vial_total` (D24, VLOOKUP col F) and `D_int` (D22, VLOOKUP col D). Vestigial cells declared display-only.
  - `sinter-porosity.md`: was told to enter the integer grade into `Mass Transfer!D20` (`por_grade`) "also settable via the Summary dropdown at D42" — but D20 is a read-only import (`=Electrochemistry!$D$32`), D32 is itself a VLOOKUP on the electrode table, and the "Summary D42 dropdown" does not exist (Summary inputs are D2–D10; Mass Transfer D42 is `d_bubble`). Re-pointed at the "sinter porosity" column (E) of the sintered-electrode row (MMO tube, row 37) in the electrode table `Electrochemistry A34:I37`; the grade follows the selected electrode. False Summary-dropdown claim deleted.

- [x] **Python-merge decision — KEEP SEPARATE (downside non-zero, gate not met).** Martin's gate was "merge IFF zero downside." It is not zero. The two files have **different roles AND different physics by design**: `electroPioreactorGasModel.py` is a fidelity twin (every one of 80 outputs must reproduce the workbook exactly; verified 80/80) using the *fixed* post-sparge-fix guard (`O2_src_guard = O2_net_gen`, surface credit withheld). `electroPioreactorGasModel-sensitivity.py` is a deliberately reduced perturb-and-rank sweep that *intentionally keeps the old surf_strip-credited guard form* (`max(0, O2_net − surf_strip)`, `max(1e-12, O2_net − surf_strip)`) — precisely so the sweep can demonstrate how strongly `kL_surf_factor` drives the schedule *because* that credit gated the cap. Merging would force one of the two intentionally-divergent guard implementations to win (or a flag-switch that is itself coupling), destroying the sensitivity script's demonstrative value, and would couple a "reproduce the sheet exactly" module to a "perturb and rank" one while dragging the unused Summary/Chemistry/CO2-flows apparatus into the sweep. The split is the correct design; the rationale already lives in the sensitivity script's own module docstring. Both scripts re-verified running clean after this wave (model 80/80; sensitivity produces its leverage + urgency ranking).

## Perfection wave (2026-06-26)

Multi-agent source-verification + refinement pass, triggered by "are the model and plugin perfect?". Every external constant, citation and hardware-capability claim was re-checked against primary sources (the discipline added because of two prior confident-but-wrong Pioreactor-logging claims). Findings applied only after independent verification.

**Applied (model + docs, branch CO2-modular):**
- Python twin de-staled — `bleach_flag` now gates on `HOCl_max` like the workbook; **genuine 80/80** (the prior 80/80 was false for D109, which had been re-keyed in the workbook but not the twin).
- Chemistry **E109** note de-contradicted (was "chloride-free assumption, enforced" while the formula fires BLEACH RISK); **0.2 mg/L** re-provenanced as WHO residual / MSC lower bound (0.021–0.39), a precautionary floor — not an organism MIC.
- **CaCl₂ E33** — literature 0.01 g/L kept; the 0.1 g/L as-built figure marked UNCONFIRMED (no documentary basis anywhere in repo) — **not entered**. If ever confirmed it gets its own "as-built" cell, never an overwrite of D33.
- **Biology** Henry notes reconciled to the 1.2e-5 O₂ ref (CO₂ ~28×, H₂ ~1.5×); **kL_surf** relabelled Higbie-form proxy (not Danckwerts).
- **LiteratureMedia** Matassa (2016) DOI → Water Research formulation paper 10.1016/j.watres.2016.05.077 (WebSearch-verified, was the Microbial Biotech review).
- **Review.md** — H-5 marked resolved; the Angella bench-survival narrative marked UNCONFIRMED (it appears nowhere in the repo; the model does NOT predict alkaline-run survival — ~2.3 mg/L HOCl at pH 8 still exceeds the 0.2 gate); line 146 O₂ ref → 1.2e-5.
- **Protocols** gerrit-current / flow-calibration / dissolved-oxygen → reviewed (authorised left empty); LED channel un-hardcoded.

**Rejected:** the proposed bleach pH-discriminator block — decorative (D125/D109 already pH-aware via D104) and would have imported an unconfirmed pH-8 input. Removing a criticism surface beats adding a decorative one.

**Routing note:** verify-agents tripped over a stale `-modular.xlsx` in a throwaway worktree (`.claude/worktrees/agent-a4f89dbc…`, commit 29b501e) and mis-reported edits as split across "two files". The single live `Media/electroPioreactorGasModel.xlsx` holds all 7 sheets; every edit was verified against and applied to that one file. (The stale worktree is harmless but a future confusion source — prune when convenient.)

**Confidence statement — what a reasonable reviewer could still criticise, beyond the physical-data gaps already in the Summary Improvements:**
1. **Two anchors stay ungrounded in-repo (highest residual):** the Angella bench run (pH 8→6, lives/dies) and the CaCl₂ 0.1 g/L figure. Both are marked UNCONFIRMED rather than asserted; only your bench/batch-sheet confirmation closes them — cannot be retired from inside the container.
2. The 0.2 mg/L floor is a *chosen* precautionary value, not a measured MIC (C. necator has none; genus chlorine-tolerant). Verdict insensitive — HOCl_max ~8.9 ≫ even 1 mg/L.
3. Mendelson (1967) coefficients 2.14/0.505 unverifiable (paywalled); immaterial (bubble path excluded for sub-mm bubbles).
4. Two citation sub-claims (Dinges 0.2 M phosphate / K⁺-Na⁺ ratios; Yang seven-vitamin list) confirmed at DOI level only, not body level — flagged, not asserted.
5. H₂ Henry T-coefficient 500 K sits at the low edge of Sander's 500–530 K; negligible effect, unverifiable to a unique value behind the firewall.
6. The workbook edits validated structurally + by the twin, and the plugin fix by reading + test symmetry, but **neither was re-rendered in Excel nor run through CI inside the container** — a render-and-eyeball pass (esp. the long E109/E33 notes and the ×/– glyphs) and CI-green are the human sign-off steps.

## Incident log

- **2026-06-25 — force-push landed on wrong ref (recovered).** The local branch
  `plugin/electrolysis-cycling-od-pause` had its upstream set to `origin/AEP-Plugin`
  (the base it was cut from), so `git push --force-with-lease origin <branch>`
  pushed the restructured history onto `refs/heads/AEP-Plugin` (clobbering the
  v0.6.7 base `f6cd8d1`) instead of the feature ref — the exact `git push -u`
  upstream gotcha. Recovered immediately: `f6cd8d1` was preserved as the parent of
  commit 1, so restored AEP-Plugin → `f6cd8d1` via
  `git push --force-with-lease=AEP-Plugin:35b277c origin f6cd8d1:refs/heads/AEP-Plugin`,
  then pushed the feature history with an explicit refspec
  `HEAD:refs/heads/plugin/electrolysis-cycling-od-pause`, and reset the local
  upstream to the feature ref. End state verified: AEP-Plugin = `f6cd8d1` (v0.6.7),
  feature branch = `35b277c`. Lesson (already a memory): for a branch cut from a
  different upstream, push new refs with `HEAD:refs/heads/<name>`, never a bare
  `git push`.

## Assumptions (standing)
- Data gaps: peer-reviewed literature only, cited + ranged; never invent. Unmeasurable values stay in Summary Improvements.
- Authoriser agents give sign-off-readiness verdicts only; never set an `authorised` state (human-only).
- Plugin default `electrolysis_off_seconds = 0` = continuous (no behaviour change for existing users).
- **Stock-Pioreactor logging (corrected 2026-06-26, verified against docs.pioreactor.com/user-guide/export-data + forum):** data lands in the leader's SQLite DB and exports as per-dataset CSVs. Datasets include `od_readings` (raw 90°-scatter photodiode signal), `od_readings_filtered` (normalized), `temperature_readings`, stirring rate, `led_change_events` (every LED-intensity change — so the electrolysis LED channel % and on/off timing **are** logged), `dosing_events`/pump events, `growth_rates` (computed), `logs`, plus a rolled-up **Pioreactor Unit Activity** timeseries (OD/temp/stirring/LED/dosing on one clock). KEY: the OD is a **scatter** reading, calibratable *to* OD600 per-unit — it is NOT a native OD600 (two earlier errors: "OD600", and "OD + temp only"). The export does **NOT** contain measured cell voltage, measured electrolysis current, or pH: voltage is read manually with a multimeter at calibration; current is *computed* via Gerrit's Law from the logged LED intensity (not measured); pH is modelled (Chemistry sheet) or measured manually. On-board OD during electrolysis/sparging is the ~20 h rise-then-nosedive artefact, untrustworthy without the plugin's OD-pause.
