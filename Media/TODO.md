# electroPioreactorGasModel – open work

Open backlog and parked items. Done work is in `CHANGELOG.md`. Bench SOPs for the measurement items are in `protocols/`.

## Open

- [!] **B1 – reconcile vial geometry (blocker).** The vial total volume (20 mL nominal) and the cylinder geometry (`A_x`*`D_int` ~ 27.6 mL) disagree ~38%, and the headline optimal pulse is ~4x sensitive to the resulting headspace. Needs a bench measurement of the true fill-to-septum free-gas volume + uniform-bore depth (only the user can do this). Until then `Geometry!geom_check` flags INCONSISTENT and the optimal pulse is marked provisional. Method: `protocols/vial-geometry.md`.
- [ ] **Run the experiment protocols** (`protocols/README.md`, in leverage order) to replace the model's assumed/data-gap (pink) values with measured ones. Use the protocols only after their apparatus, sampling and analysis prerequisites are resolved. Include validated, transferable measurements in the matching **Calibrations** section and re-read the Summary dashboard; retain unresolved measurements as excluded records.
- [ ] **Measure surface kLa.** Record it in the **Calibrations** tab (Surface kLa section, in 1/h) and confirm it exceeds `kLa_surf_req`. Since wave-4 it no longer switches the sheet between two schedules — it sets how far dissolved O2 must sit above the headspace, and the ratio to `kLa_surf_req` is the feasibility margin of the whole DO strategy (`protocols/surface-kla.md`).
- [ ] **Measure cathodic faradaic efficiency `etaF`.** The model calculates it (read Electrochemistry D18 at the current inputs) from the oxygen competing for the cathode current rather than assuming 1.0, but that calculation rests on an estimated electrode mass-transfer coefficient, so the oxygen prediction remains conditional on that estimate and the ORR species balance. A measured hydrogen-efficiency deficit alone does not identify an oxygen sink.
- [ ] **Per-reactor CO2 flow calibration** for reactors other than ed04 (`protocols/flow-calibration.md`); an uncalibrated reactor shows "calibrate first" by design.
- [ ] **Fill the HOB DO bands** for the non-necator organisms and the minimum-DO column (currently pink gaps).
### Nelly set-up (2026-10-21: ed04, MMO tube, *Xanthobacter tagetidis*, AMYBO03, 30 °C)

- [ ] **Calibrate the reactor actually used.** ed04 (MEP0.3: 20 mL vial, 16 mL max) stands in because it is the only reactor with a CO₂ flow calibration; an AEP0.2 build (ed06–ed08) needs its own `protocols/flow-calibration.md` run, then select it in Summary D2.

### From the Codex/Astra review (2026-10-21)

- [ ] **Record gas-flow reference conditions.** The model now consistently balances dry species, but CO₂ and air flows are expressed as dry-equivalent volumes at reactor pressure/temperature; the existing collection data do not record gas humidity, collection temperature or pressure. Measure/record these before claiming absolute molar dosing accuracy.
- [ ] **Validate pressure closure through the real vent.** Positive assumed ingress does not prove enough make-up air enters after CO₂ absorption. Measure the required make-up flow / pressure trace; the workbook now labels closure unverified instead of asserting that the headspace refills.
- [ ] **Measure AMYBO03 conductivity at operating temperature.** Keep the empirical finite-strength factor until measured; its old I≈0.1 M anchor does not validate it at I≈0.2 M. Trace-ion mobilities, phosphate speciation and metal complexation remain disclosed approximations, not invented constants.

- [ ] **Approve gas measurement and clearance procedures before execution.** The current workbook is a conservative H₂/O₂ screen, not a validated flammability envelope or clearance certificate. Define mixture-appropriate limits, instrumentation, non-perturbing/sacrificial sampling, safe venting and an explicit clearance criterion; elapsed CO₂ pulse intervals do not prove clearance. Repeated headspace withdrawals need an inventory correction before vent classification or Q_vent fitting; residual liquid O₂ exchange must also be shown negligible or modelled jointly. Pressure sensing must resolve both signs around ambient.
- [ ] **Validate the separated-gas Faradaic-efficiency apparatus and transferability.** The collection rig is not finalised, and separation changes oxygen crossover. Establish recovery, species balance and applicability to the undivided cell before including its calibration. A low H₂ yield alone cannot quantify ORR.
- [ ] **Define biological-screen controls and analysis.** Owner must choose feasible organism-specific DO setpoints with controlled or measured H₂ supply, gas-matched current-density controls, replicates and equivalence margins. Non-significance does not establish a no-effect limit, final OD is not productivity, and a literature inhibition condition is not the protocol’s toxic endpoint.
- [ ] **Validate attached-sparger short-pulse flow and intercept representation.** A steady-flow Calibrations entry selects a zero-intercept route; ed04’s CO2 flows fit includes an intercept. Keep new calibration rows excluded until pulse delivery, minimum pulse and any significant intercept are resolved. Collection recovery and reference-condition conversion need independent validation.

### From the wave-4 review (2026-08-12; detail and derivations in `electroPioreactorGasModel-GPT6Astra-Review.md`)


- [ ] **Measure the electrode mass-transfer coefficient** (`protocols/electrode-mass-transfer.md`; ferricyanide limiting current, same vial, same rpm). It now sets the cathodic O2 loss, the peroxide source, the chlorine cap and the electrode-surface pH verdict — the single most load-bearing estimate in the new electrochemistry.
- [ ] **Measure the electrode centre-to-centre gap** with calipers — sets the ohmic term in the cell-voltage budget.
- [ ] **Read the cell voltage at a known setpoint** with a multimeter. The current AMYBO03 budget predicts about 2.65 V of a 5 V rail at 3 % (read Electrochemistry D119 for the selected conditions); the reading either confirms the electrochemical picture or localises which term is wrong.
- [ ] **Assay dissolved Cu/Ni/Fe in spent medium.** The operating anode (~1.58 V vs SHE) sits ~1.2 V above the Cu2+/Cu standard potential, so dissolution is thermodynamically allowed; this closes the anodic charge budget and tests the prime suspect for the Exp-2 death.
- [ ] **Get the new electrochemistry reviewed by an electrochemist.** The six questions to put to them are in the review's "Changes applied" section; the weakest inputs are the anodic exchange-current density (spans four decades in the literature) and the mass-transfer coefficient.
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet for consistency – **parked**: high reference-break risk for nit-level value; revisit only if a clean rename harness exists.

### From the wave-5 review (2026-10-21; reports summarised in `electroPioreactorGasModel-GPT6Astra-Review.md`)

Measurements, in leverage order. Numerical examples inherited from wave 5 describe its UdG/25 °C baseline unless explicitly labelled AMYBO03; use the current workbook for the actual configuration.

- [ ] **Characterise the headspace vent** (`protocols/headspace-vent.md`; decides Summary D111 `vent_model`, the single highest-leverage open input): is the MEP0.3 vent outflow-only or does it exchange air, and at what flow? Pressure-decay test with a transducer on a headspace tube, or an optical O₂ spot in the headspace after a CO₂ fill. A check valve gives 12.7 min / pH 6.16, a plain open vent (the default until measured; back-draw input `Q_backdraw` 0.015 mL/min, gold) 9.0 min / pH 6.19, a 0.5 mL/min air exchange 0.87 min / pH 6.23. Fix the cap leak noted on CO2 flows L8 first.
- [ ] **Abiotic DO trace under the real schedule** (`protocols/abiotic-do-trace.md`) (3 % power, no cells = lag source, optical DO patch): one run discriminates the vent hypotheses and checks the Summary rows 114–117 predictions.
- [ ] **Headspace H₂/O₂ during lag before any unattended run** (`protocols/headspace-gas-safety.md`): the model puts it at ~9 % H₂ mean and ~15 % just before each pulse, ~5 % O₂ (potential flammability screen; AMYBO03, 30 °C). Use only a validated non-perturbing measurement and gas-clearance procedure; a vent sensor is representative only if demonstrated.
- [ ] **Free + combined chlorine (DPD kit) in spent UdG after 24 h** (`protocols/chlorine-species.md`): settles the chloramine lifetime `tau_NH2Cl`, which now moves the interval ±32 % through the free chloride share.
- [ ] **Per-pulse CO₂ volume with the sparger attached** (`protocols/flow-calibration.md` step 10): the calibration collects at the end of the CO₂ line; one run through the submerged sinter tests the fitted per-pulse intercept and flow against the real back-pressure; do not replace that fit with a zero-intercept calibration until attached-sparger short-pulse delivery is validated.
- [ ] **Off-gas H₂ at steady growth**: measures the H₂ uptake fraction, which sets the O₂ surplus (`bio_O2`, ±200 % on the schedule).
- [ ] **Confirm UdG CaCl₂ hydrate state** (anhydrous 110.98 vs dihydrate 147.01 g/mol: −24 % on every chlorine figure), the LED-driver rail and compliance, and whether the strain current-density limits are anode or cathode, geometric or wetted area.

Owner decisions (questions T4–T8 in brain2 `AMYBO/electroPioreactor-fromClaude.md`):

- [ ] **Size for lag or growth** (Summary D112). Lag is unreachable at the estimated surface kLa (margin 0.66×); both phases are shown either way.
- [ ] **Consider a ~1 mL/min N₂ headspace sweep**: the model predicts it would keep lag-phase H₂ below the nominal screening threshold (not a mixture safety certification) and hold the O₂ target without pushing pH below the band; the model shows CO₂ cannot do all three jobs (Summary D128 reads NO).

Model work not yet done (mirrored in the Summary TODO, rows 145 onwards):

- [ ] **Timed N₂ pulses in the headspace balance.** CO₂ alone cannot hold the DO target and the pH band (Summary D128). N₂ pulsed between CO₂ pulses would dilute O₂ and H₂, leaving CO₂ for carbon and pH, so CO₂ pulse, interval and N₂ dose can be solved together. Needs the objective (least CO₂ with pH ≥ 6.5 is the proposed default), the N₂ hardware (own solenoid or shared line) and the N₂ flow.
- [ ] **Couple added alkalinity into the model.** Summary D131–D132 (Chemistry rows 302–308) now give the NaHCO₃ for a target pH at first order: At the current AMYBO03 baseline the first-order estimate is about 0.124 g/L (1.48 mM) for the 6.5 floor; the earlier UdG example was 2.6 g/L (31 mM). Still to do: an added-alkalinity input that feeds the charge balance, ionic strength and the CO₂ storage (DIC_cap), so pH and the schedule respond to it. Also nitrate or urea instead of NH₄⁺ (ammonium uptake acidifies as the culture grows).
- [ ] **Pulse length from the shortest reliable pulse.** D13 is a rule of thumb (about one headspace volume per pulse). A twin trial at the 0.25 s default floor: 0.25 s every 4.4 min holds the same pH and growth DO on about 7 % less CO₂ with smaller swings (peak DO equals the mean, because the liquid cannot follow a 4-min headspace swing), but lag-phase mean DO rises from 4.7 to 6.2 mg/L. Not adopted: the floor and the 0.375 mL per-pulse volume it leans on are unmeasured (flow-calibration steps 9 and 10).
- [ ] **Start-up regime.** The schedule is sized for growth; cover lag (flammable headspace, higher DO peaks) by ramping the electrolysis current with biomass or N₂ during lag only.
- [ ] **Measured electrode k_m and chlorine lifetime as Calibrations-tab inputs** (`electrode-mass-transfer.md`, `chlorine-species.md`); today they are compared by hand.
- [ ] **Record the no-carryover maximum flow** per reactor in CO2 flows column M (Summary D29 reads "not measured" until then).


- [ ] **Characterise the low-power/start-up current curve.** The fit is now restricted to the validated range intersected with the plugin runtime limit (3–10 %). Off and below-range settings are deliberately unsupported by this schedule model; a nonzero regression intercept is not evidence of off-state electrolysis. Measure before adding start-up predictions.

## Notes
Wave 5 (2026-10-21) recalculated the workbook in real Excel for the first time and closed the wave-4 items and the wave-5 review findings (see `CHANGELOG.md` and the wave-5 section of `electroPioreactorGasModel-GPT6Astra-Review.md`). What remains is measurement and owner decisions: the model now shows that CO₂ alone cannot dilute electrolytic O₂ to the DO target and hold pH in band (Summary D128), and its headline interval rests mainly on the vent behaviour, the chloramine lifetime and the H₂ uptake ratio.
