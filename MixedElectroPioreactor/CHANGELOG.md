# MixedElectroPioreactor — Session Changelog

Gitignored (see `.gitignore`). Done items + open items + handover notes for the MEP/Edinburgh-MSc training docs. Pair-doc is `Review.md` (12-item Apply/Override sign-off, currently committed and awaiting your input).

## 2026-05-09 — actioning curly-brace comments + repo-wide solenoid-naming sweep

Branch: `MScTraining`. Pushed: `3051a8c` on `origin/MScTraining`.

### Done

- **`PreTransportCheck-EdMSc26.md`** — actioned all three of your `{...}` comments:
  - §1–5 now have paired `ed05:` / `ed04:` boxes per check (run order: ed05 first, swap to ed04 after RPi 4B → Zero 2W swap).
  - Dropped the wrong "PWM duty stepped 10/50/100 %" solenoid line in §3.
  - Replaced the wrong "no usable outlet gauge" claim in §B with a corrected paragraph and a new check: outlet gauge holds steady for 60 s with the needle valve closed (any drop = leak upstream of the needle valve).
- **Anchor fixes** after your earlier section reorder (Solenoid → 3, Wet electrolysis → 4):
  - PreTransport on-arrival step 3: `#3-wet-electrolysis` → `#4-wet-electrolysis`.
  - `Calibration.md` §3: same anchor swap.
  - `Calibration.md` §2: `#fzone-leak-check` → `#solenoid-leak-check` (broken by your "FZone leak check" → "Solenoid leak check" rename).
- **Solenoid brand correction sweep**: regulator = FZone, solenoid = HPcontrols. Confirmed all other repo `FZone` mentions correctly attach to "regulator". `PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md` line 5 left as "FZone solenoid valve" per your revert (historical record).
- **Memory writes** at `~/.claude/projects/-workspace/memory/` (outside repo, outside `/learnings`):
  - `feedback_no_explainer_after_correction.md` — when you correct my draft, fix silently, no reader-facing explainer prose.
  - `reference_mep_co2_stack_brands.md` — FZone = regulator, HPcontrols = solenoid; AEP0.1.1 uses Premium ODL regulator instead.
- **Stash recovery**: vibe context-switch had parked the WIP in `stash@{1}` ("MScTraining WIP — vss v0.7 detour"). Popped on MScTraining, dropped my reverted EliSilver edit, committed and pushed. `stash@{0}` (vibe-managed `.gitignore` block) left untouched.

### Open / next

- **§B pressure-decay execution** on ed04 and ed05 — snoop with soapy water, 30 min rate-stability, plus the new outlet-gauge-hold step. Sealant cured 2026-04-30, well past.
- **`Review.md` 12-item sign-off** still awaiting your Apply/Override boxes. When you're ready, tell me "action it" and I'll apply your decisions in a single commit.
- **MSc WiFi issues** — flagged as separate chat.

### Notes

- `AEP-Plugin/CLAUDE.md` asks each new vibe session in this repo to surface unchecked `AEP-Plugin/TODO.md` v0.7 items first. v0.7.0 (configurable LED channel) shipped on `configurable-led-channel` (commit `d5bb20d`); Path 2 (on-device install + sanity) and Path 3 (live actuation) remain open in that TODO. Separate from MEP work.
- `AEP-Plugin/CHANGELOG.md` is the AEP-Plugin release-notes file (committed, follows the vibe TODO ↔ CHANGELOG convention with both files tracked). This MEP CHANGELOG.md mirrors the naming but is gitignored — it's a working/handover doc, not a release artifact.
- Currently no `MixedElectroPioreactor/TODO.md`. If you want one (mirroring the AEP-Plugin pattern), say the word.
- Returned the working tree to `configurable-led-channel` after the push, so when you resume your v0.7 work it's already where you left it.
