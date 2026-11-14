# Codex hand-over: full review and fix of the gas model (2026-10-21)

**Goal:** an Astra-led, full adversarial review of the electroPioreactor gas model, with every finding you confirm fixed, verified and committed. **Target: done as early as possible this afternoon.** The owner has a meeting with Nelly and will hand her this workbook.

## What you are reviewing

- `Media/electroPioreactorGasModel.xlsx`: the deliverable. Sheets: Summary, Geometry, Electrochemistry, Chemistry, Biology, Mass Transfer, CO2 flows, Calibrations, AMYBO03.
- `Media/electroPioreactorGasModel.py`: the Python twin. It reproduces the workbook and checks 371 outputs against Excel's cached values. It refuses to run if its declared inputs differ from Summary D2:D10 and D111:D112.
- `Media/electroPioreactorGasModel-sensitivity.py`: a sensitivity analysis with a self-check.
- Context:
  - `Media/electroPioreactorGasModel-Review.md` (read the "Hand-over for the Astra review" section and its update first);
  - `Media/TODO.md`;
  - `Media/CHANGELOG.md`;
  - `Media/CLAUDE.md` (house rules);
  - `Media/protocols/`.

**Baseline to keep (the owner's choices for Nelly; do not change them):** Summary D2 `ed04`, D3 `MMO tube`, D4 `Xanthobacter tagetidis`, D5 `AMYBO03`, D8 `30` °C.

Expected headline: about 0.67 s every 7.45 min, pH 6.49, mean DO 2.28 mg/L. Branch `AEP02`; the last commit before you is `dd5f16b`.

## Jobs, in order

1. **Re-base the sensitivity script** on the baseline above. Its guard currently stops it (organism, medium and temperature drift), and its medium chemistry is hard-wired to the UdG recipe. Make it medium-aware the way the twin is (`_by_media`, with an AMYBO03 branch). Pass condition: self-check passes and the four-combination check passes.
2. **Full review** of the workbook, twin and sensitivity script: correctness of the physics and chemistry, formula errors, unit mistakes, stale notes, house-rule breaches, and disagreement between workbook and twin. Spend the most effort where the review note says to push hardest:
   - the headspace balance;
   - the schedule rule;
   - the electrochemistry resting on an estimated mass-transfer coefficient;
   - the alkalinity estimate;
   - the new AMYBO03 sheet: its strong-ion difference was corrected today, and `kappa_fI` is anchored at I ≈ 0.1 M while AMYBO03 is about 0.2 M.
3. **Fix** every finding you confirm. Leave anything that needs a bench measurement or an owner decision in `Media/TODO.md`, as `[ ]` with the reason.
4. **Verify after every fix:**
   - `python3 Media/electroPioreactorGasModel.py` must report N/N;
   - the sensitivity script's self-checks must pass;
   - every workbook change must be recalculated in real Excel (below).
5. **Commit** with a CHANGELOG entry in the same commit, per the repo's TODO/CHANGELOG convention. **Do not push.**

## Editing the workbook: rules that bite

- Excel on the MBA `claude` account is **View Only**: it recalculates but cannot save. Patch the XML, recalculate in Excel, then inject Excel's values. The tools are in `/workspace/.vibe/gasmodel-tools/` (gitignored). Read its README.
  - Typical round trip: `GM_WORK=<scratch> .vibe/gasmodel-tools/apply.sh edits.json <tag>`, then copy `<scratch>/<tag>.xlsx` over `Media/`.
  - The op list is in the `xlpatch.py` docstring.
- **SSH scope agreed with the owner:** `claude@host.docker.internal` only, using the key in `.vibe/`. Files go only under `~/builds/electroPioreactor/excel`: copy, open, recalculate, read, save copies and take screenshots there, and nothing else on that account.
  - If you edit `dump.applescript`, push it with `xl.sh push`: the MBA runs its own copy.
- **The owner may save the workbook from their own Excel** through Dropbox. Before overwriting `Media/electroPioreactorGasModel.xlsx`, `cmp` it against the file you patched from. If it differs, rebuild on the owner's version.
- **House rules:**
  - blue bold for typed inputs, black for formulas, a confidence fill in column E;
  - sheet-local defined names;
  - formula string literals of 255 characters or fewer (longer ones trigger Excel's repair prompt);
  - match the existing comment density in the twin.
- Never `git push`. Never run git against `/brain2`. Never write to `/learnings`.

## On completion

1. Email the owner (martin@amybo.org). Subject: "Gas model: Codex review complete". Body: the commits, the findings fixed, the findings left on the TODO with reasons, and the verification counts.
   - If you have no tool that can send email from here (the container's outbound traffic is allowlisted), **say so plainly in your final message**. Do not reach for another route without asking.
2. Also leave the same summary at the end of `Media/electroPioreactorGasModel-Review.md` as "## Codex review (2026-10-21)".
