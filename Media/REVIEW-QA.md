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
- **Stock-Pioreactor logging (correction, 2026-06-26):** a stock Pioreactor export records **OD600 and temperature only** — NOT cell voltage, NOT electrolysis current, NOT pH. Cell voltage is read manually (multimeter) during calibration; electrolysis current is *computed* via Gerrit's Law from LED intensity (not measured); pH is modelled (Chemistry sheet) or measured manually. Earlier analysis wrongly implied the export carries V/I/pH — do not repeat. On-board OD during electrolysis/sparging is the ~20 h rise-then-nosedive artefact and is not trustworthy without the plugin's OD-pause.
