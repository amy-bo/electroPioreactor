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
- [ ] Python model: merge sensitivity into one file if zero-downside. *(low)*
- [x] Plugin: LED config-only (already config-only — no change needed), restructured into 4 topic commits, PR opened. *(plugin)*
- [ ] Wave-2: re-run the plug-the-gaps + synthesise phases that died on the session limit.

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
