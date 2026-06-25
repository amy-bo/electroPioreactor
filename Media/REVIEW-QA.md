# Model/Plugin Review Programme — Q&A Ledger (working file, not for upstream)

Async channel so no workstream blocks on a question. Agents log questions here with a
**default assumption** and proceed. The Programme Manager surfaces must-answer ones in the
5-minute chat updates; Martin answers in chat; answers are recorded here.

## Open questions for Martin
| # | Workstream | Question | Default assumption (proceeding on this) | Blocking? |
|---|---|---|---|---|
| Q1 | Plugin | Upstream-PR-ready, or local-only? | Build PR-ready: clean plugin feature, require a minimum Pioreactor version rather than patching; no un-consented system changes (per prior reviewer feedback). | No |
| Q2 | Plugin | Confirm the OD-pause spec: OD reading pauses during + for a user-set period after each electrolysis ON phase; setting that period to −(electrolysis ON time) cancels the pause so OD is logged throughout electrolysis. | Yes, as stated. Period in seconds; negative allowed down to −(ON time). | No |
| Q3 | Python model | Keep electroPioreactorGasModel.py separate from -sensitivity.py, or merge? | Build separate first; merge only if it leaves a single clean, well-documented module. | No |

## Answered
_(none yet)_

## Assumptions log (agents proceeding without asking)
- Data gaps: plug from peer-reviewed literature only, cite source + give range/confidence; never invent. Genuinely unmeasurable values stay in the Summary Improvements list.
- "Authorisor" agents produce sign-off-readiness verdicts only; they NEVER set an `authorised` state (human-only act).
