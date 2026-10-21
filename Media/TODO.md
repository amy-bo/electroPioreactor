# electroPioreactorGasModel – open work

Open backlog and parked items. Done work is in `CHANGELOG.md`. Bench SOPs for the measurement items are in `protocols/`.

## Open

- [!] **B1 – reconcile vial geometry (blocker).** The vial total volume (20 mL nominal) and the cylinder geometry (`A_x`*`D_int` ~ 27.6 mL) disagree ~38%, and the headline optimal pulse is ~4x sensitive to the resulting headspace. Needs a bench measurement of the true fill-to-septum free-gas volume + uniform-bore depth (only the user can do this). Until then `Geometry!geom_check` flags INCONSISTENT and the optimal pulse is marked provisional. Method: `protocols/vial-geometry.md`.
- [ ] **Run the experiment protocols** (`protocols/README.md`, in leverage order) to replace the model's assumed/data-gap (pink) values with measured ones. The protocols are now follow-blind: record the raw numbers in the matching section of the **Calibrations** tab and the model updates itself; re-read the Summary dashboard after each.
- [ ] **Measure surface kLa.** Record it in the **Calibrations** tab (Surface kLa section, in 1/h) and confirm it exceeds `kLa_surf_req`. Since wave-4 it no longer switches the sheet between two schedules — it sets how far dissolved O2 must sit above the headspace, and the ratio to `kLa_surf_req` is the feasibility margin of the whole DO strategy (`protocols/surface-kla.md`).
- [ ] **Measure cathodic faradaic efficiency `etaF`.** Since wave-4 the model calculates it (0.974) from the oxygen competing for the cathode current rather than assuming 1.0, but that calculation rests on an estimated electrode mass-transfer coefficient, so the O2 figures are still an upper bound until it is measured.
- [ ] **Per-reactor CO2 flow calibration** for reactors other than ed04 (`protocols/flow-calibration.md`); an uncalibrated reactor shows "calibrate first" by design.
- [ ] **Fill the HOB DO bands** for the non-necator organisms and the minimum-DO column (currently pink gaps).
### From the wave-4 review (2026-08-12; detail and derivations in `electroPioreactorGasModel-Review.md`)


- [ ] **Measure the electrode mass-transfer coefficient** (`protocols/electrode-mass-transfer.md`; ferricyanide limiting current, same vial, same rpm). It now sets the cathodic O2 loss, the peroxide source, the chlorine cap and the electrode-surface pH verdict — the single most load-bearing estimate in the new electrochemistry.
- [ ] **Measure the electrode centre-to-centre gap** with calipers — sets the ohmic term in the cell-voltage budget.
- [ ] **Read the cell voltage at a known setpoint** with a multimeter. The budget predicts 2.85 V of a 5 V rail at 3 % (3.26 V before k_geom was corrected from 2 to 1; the reading discriminates the two); the reading either confirms the electrochemical picture or localises which term is wrong.
- [ ] **Assay dissolved Cu/Ni/Fe in spent medium.** The operating anode (~1.58 V vs SHE) sits ~1.2 V above the Cu2+/Cu standard potential, so dissolution is thermodynamically allowed; this closes the anodic charge budget and tests the prime suspect for the Exp-2 death.
- [ ] **Get the new electrochemistry reviewed by an electrochemist.** The six questions to put to them are in the review's "Changes applied" section; the weakest inputs are the anodic exchange-current density (spans four decades in the literature) and the mass-transfer coefficient.
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet for consistency – **parked**: high reference-break risk for nit-level value; revisit only if a clean rename harness exists.

### From the wave-5 review (2026-10-21; reports summarised in `electroPioreactorGasModel-Review.md`)

Measurements, in leverage order:

- [ ] **Characterise the headspace vent** (`protocols/headspace-vent.md`; decides Summary D111 `vent_model`, the single highest-leverage open input): is the MEP0.3 vent outflow-only or does it exchange air, and at what flow? Pressure-decay test with a transducer on a headspace tube, or an optical O₂ spot in the headspace after a CO₂ fill. A check valve gives 12.7 min / pH 6.16, a plain open vent (the default until measured; back-draw input `Q_backdraw` 0.015 mL/min, gold) 9.0 min / pH 6.19, a 0.5 mL/min air exchange 0.87 min / pH 6.23. Fix the cap leak noted on CO2 flows L8 first.
- [ ] **Abiotic DO trace under the real schedule** (`protocols/abiotic-do-trace.md`) (3 % power, no cells = lag source, optical DO patch): one run discriminates the vent hypotheses and checks the Summary rows 114–117 predictions.
- [ ] **Headspace H₂/O₂ during lag before any unattended run** (`protocols/headspace-gas-safety.md`): the model puts it at ~11 % H₂ mean and ~18 % just before each pulse, ~6 % O₂ (flammable). Syringe sample to a portable meter, or a catalytic H₂ sensor at the vent.
- [ ] **Free + combined chlorine (DPD kit) in spent UdG after 24 h** (`protocols/chlorine-species.md`): settles the chloramine lifetime `tau_NH2Cl`, which now moves the interval ±32 % through the free chloride share.
- [ ] **Per-pulse CO₂ volume with the sparger attached** (`protocols/flow-calibration.md` step 10): the calibration collects at the end of the CO₂ line; one run through the submerged sinter confirms the fixed 0.375 mL per pulse and the flow hold against the real back-pressure.
- [ ] **Off-gas H₂ at steady growth**: measures the H₂ uptake fraction, which sets the O₂ surplus (`bio_O2`, ±200 % on the schedule).
- [ ] **Confirm UdG CaCl₂ hydrate state** (anhydrous 110.98 vs dihydrate 147.01 g/mol: −24 % on every chlorine figure), the LED-driver rail and compliance, and whether the strain current-density limits are anode or cathode, geometric or wetted area.

Owner decisions (questions T4–T8 in brain2 `AMYBO/electroPioreactor-fromClaude.md`):

- [ ] **Size for lag or growth** (Summary D112). Lag is unreachable at the estimated surface kLa (margin 0.66×); both phases are shown either way.
- [ ] **Consider a ~1 mL/min N₂ headspace sweep**: it would keep lag-phase H₂ below the flammable limit and hold the O₂ target without pushing pH below the band; the model shows CO₂ cannot do all three jobs (Summary D128 reads NO).

Model work not yet done (mirrored in the Summary TODO, rows 145 onwards):

- [ ] **Timed N₂ pulses in the headspace balance.** CO₂ alone cannot hold the DO target and the pH band (Summary D128). N₂ pulsed between CO₂ pulses would dilute O₂ and H₂, leaving CO₂ for carbon and pH, so CO₂ pulse, interval and N₂ dose can be solved together. Needs the objective (least CO₂ with pH ≥ 6.5 is the proposed default), the N₂ hardware (own solenoid or shared line) and the N₂ flow.
- [ ] **Couple added alkalinity into the model.** Summary D131–D132 (Chemistry rows 302–308) now give the NaHCO₃ for a target pH at first order: 2.6 g/L (31 mM) lifts pH to the 6.5 floor at today's dissolved CO₂. Still to do: an added-alkalinity input that feeds the charge balance, ionic strength and the CO₂ storage (DIC_cap), so pH and the schedule respond to it. Also nitrate or urea instead of NH₄⁺ (ammonium uptake acidifies as the culture grows).
- [ ] **Pulse length from the shortest reliable pulse.** D13 is a rule of thumb (about one headspace volume per pulse). At a fixed CO₂ dose, shorter, more frequent pulses cut the DO, pH and H₂ swings; use the measured solenoid floor and solve the interval for the dose.
- [ ] **Start-up regime.** The schedule is sized for growth; cover lag (flammable headspace, higher DO peaks) by ramping the electrolysis current with biomass or N₂ during lag only.
- [ ] **Measured electrode k_m and chlorine lifetime as Calibrations-tab inputs** (`electrode-mass-transfer.md`, `chlorine-species.md`); today they are compared by hand.
- [ ] **Record the no-carryover maximum flow** per reactor in CO2 flows column M (Summary D29 reads "not measured" until then).


## Notes
Wave 5 (2026-10-21) recalculated the workbook in real Excel for the first time and closed the wave-4 items and the wave-5 review findings (see `CHANGELOG.md` and the wave-5 section of `electroPioreactorGasModel-Review.md`). What remains is measurement and owner decisions: the model now shows that CO₂ alone cannot dilute electrolytic O₂ to the DO target and hold pH in band (Summary D128), and its headline interval rests mainly on the vent behaviour, the chloramine lifetime and the H₂ uptake ratio.
