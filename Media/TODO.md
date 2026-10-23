# electroPioreactorGasModel – open work

Two lists, mirrored on the Summary tab.
- **Experiments to improve accuracy** are bench measurements that replace an estimate or fill a data gap in the workbook (Summary rows 131–157). The protocols are in `protocols/`.
- **Potential model improvements** are changes to the spreadsheet itself (Summary rows 160–161 and 204–210). Growth-validation experiments continue at rows 213–215.

**Objective clarified on 22 October 2026: highest measured growth/productivity.**
The current pulse-rule calculation is a candidate generator, not a growth optimiser.
Completing only the original experiment list and the two original refinements would
not establish an optimum. Summary row 32 now qualifies the candidate explicitly.
The baseline still misses the pH band and the lag DO target is unreachable at the
current power/kLa. Do not interpret the candidate plugin numbers as validated settings.

Done work is in `CHANGELOG.md`.

## Experiments to improve accuracy

The order matches the Summary. Impact runs HIGH > MED > LOW. Within each impact level, effort runs low > med > high, and within each impact and effort pair the most leverage comes first. So reading top to bottom is a sensible programme.

Summary column D shows each experiment's status in the situation selected on the Summary (reactor, electrode, organism, medium and temperature):
- **Done:** green.
- **Approximate:** amber. Useful data that could be improved.
- **Not done:** red.
- **Not needed:** green, when the selection makes the experiment irrelevant.

How the status is found:
- An included run in the matching calibration log counts.
- So does a row in the **experiment record** on the Experiments sheet. In a record row, any condition left blank means the result holds for any value of it.
- `Calibrations!xs_*` holds the logic for each experiment.

Enter results in the matching calibration log where there is one. Leave Include blank until the protocol's acceptance, species-balance and transferability gates are met. The numbers quoted below are for the AM003 baseline: ed04, MMO tube, *Xanthobacter tagetidis*, 30 °C.

### HIGH impact

- [!] **Vial total volume and true headspace (blocker for the pulse).** HIGH, low effort.
  - The total vial volume (20 mL nominal) and the cylinder geometry (`A_x`·`D_int` ≈ 27.6 mL) disagree by about 38 %, and the pulse moves almost 1:1 with the headspace.
  - `Geometry!geom_check` reads INCONSISTENT until this is measured.
  - Protocol: `protocols/vial-geometry.md`.
- [ ] **CO₂ flow of the reactor in use.** HIGH, low effort.
  - Done for ed04 (CO2 flows, 17 Jun 2026).
  - An AEP0.2 build needs its own run.
  - Record the collection humidity, temperature and pressure.
  - Protocol: `protocols/flow-calibration.md`.
- [ ] **Electrode mass-transfer coefficient.** HIGH, low effort.
  - Protocol: `protocols/electrode-mass-transfer.md`, at the Summary rpm and temperature.
  - It sets the cathodic O₂ loss, the peroxide source and sink, the chlorine cap and the electrode-surface pH verdict.
- [ ] **Low-power current curve below 3 %.** HIGH, low effort; raised from MED in this pass.
  - The start-up power for the lag DO target (Summary row 24, about 1.0 % at baseline) is extrapolated below Gerrit's Law, which is fitted from 3 % up.
  - That extrapolation is the worst class of data in the model. It shows as DATA GAP on Summary rows 24, 60 and 128.
  - Protocol: `protocols/gerrit-current.md`.
- [ ] **Electrochemist review of the calculated electrochemistry.** HIGH, low effort.
  - The weakest inputs are the anodic exchange-current density (four decades of spread in the literature) and the electrode mass-transfer coefficient.
- [ ] **Cell voltage at a known setpoint.** HIGH, low effort.
  - Approximate in UdG phosphate: about 3.4 V at 3 % in Exp 1, with the meter not recorded. Not done in AM003.
  - The budget predicts about 2.65 V of the 5 V rail.
- [ ] **Headspace H₂/O₂ during lag, before any unattended run.** HIGH, med effort.
  - The model puts the lag headspace at about 9–10 % H₂ mean and 14 % before each pulse at the growth schedule, and 3 % before each pulse at the start-up schedule.
  - It needs an owner-approved, non-perturbing sampling and gas-clearance procedure first.
  - Protocol: `protocols/headspace-gas-safety.md`.
- [ ] **Vent back-draw flow.** HIGH, med effort.
  - This is `Q_backdraw` (Mass Transfer D385), the biggest remaining input to the interval.
  - Protocol: `protocols/headspace-vent.md`.
- [ ] **Surface kLa.** HIGH, med effort.
  - Protocol: `protocols/surface-kla.md`.
  - The current margins on the estimate are 1.72× in growth and 0.61× in lag.
- [ ] **Abiotic DO trace under the schedule.** HIGH, med effort.
  - Protocol: `protocols/abiotic-do-trace.md`.
- [ ] **pH through a growth run.** HIGH, med effort; new.
  - Protocol: `protocols/ph-growth-run.md`.
  - It tests the nitrogen-uptake acidification: end-of-run pH 6.43 against 6.49 at the start, with 1 g/L biomass on ammonium.
  - It also tests the biomass nitrogen content (11.4 %).
- [ ] **Dissolved Cu/Ni/Fe in spent medium.** HIGH, med effort.
  - The anode sits about 1.2 V above Cu²⁺/Cu.
  - This is the prime suspect for the Exp-2 death.
- [ ] **Cathodic Faradaic efficiency.** HIGH, med effort.
  - Protocol: `protocols/faradaic-efficiency.md`.
- [ ] **Organism DO thresholds.** HIGH, high effort (raised from MED/low, owner 22 Oct 2026).
  - Protocol: `protocols/dissolved-oxygen.md`.
  - They set the DO target fraction behind every schedule, and the owner's screen needs gas-matched controls and replicates.
- [ ] **Off-gas H₂ at steady growth.** HIGH, high effort.
  - Enter accepted biological H₂ uptake divided by H₂ available after anodic re-oxidation in `Biology!H2_util_meas` (D128), with run/condition/uncertainty evidence in F128. The fraction now feeds H₂, O₂ and CO₂ consumption and residual growth H₂. Blank retains the explicitly provisional 100% upper bound; an uptake ratio alone cannot replace this measurement.
  - Protocol: `protocols/knallgas-stoichiometry.md`.

### MED impact

- [ ] **CO₂ flow calibration for each reactor.** MED, low effort.
  - Approximate: only ed04 is calibrated.
- [ ] **Vial wall thickness.** MED, low effort.
  - Measure with calipers, at the same time as the vial volume.
- [ ] **Free and combined chlorine (DPD).** MED, low effort.
  - Protocol: `protocols/chlorine-species.md`.
  - Not needed in chloride-free AM003.
- [ ] **Conductivity of the medium in use at the operating temperature.** MED, low effort.
- [ ] **Electrode centre-to-centre gap.** MED, low effort.
  - Measure with calipers.
- [ ] **Anodic Faradaic efficiency.** MED, med effort.
- [ ] **Knallgas uptake ratio.** MED, high effort.

### LOW impact

- [ ] **Solenoid pulse floor.** LOW, low effort.
  - Approximate: 0.25 s on ed04.
  - It now also matters for the "Shortest reliable pulse" rule (Summary row 18).
- [ ] **Per-pulse CO₂ with the sparger attached.** LOW, low effort.
  - Approximate: the ed04 ladder was collected from the inlet tube.
- [ ] **No-carryover maximum flow.** LOW, low effort.
  - Approximate: 3.33 mL/s set by inspection. CO2 flows column M is still blank.
- [ ] **Sinter porosity.** LOW, low effort.
- [ ] **Lab ambient pressure.** LOW, low effort.

## Potential model improvements

These are changes to the spreadsheet only.

- [ ] **Separate N₂ flush in the sawtooth.**
  - Summary row 14 enters N₂ by its mean flow. That is exact for the mean-field fractions, but not for the sawtooth: pulsing N₂ apart from CO₂ lets H₂ and O₂ build for longer, so the pre-pulse peaks run higher.
  - The flush model would not change whether N₂ is warranted, only how to pulse it safely. It waits until N₂ is chosen (owner, 21 Oct 2026).
- [ ] **Ionic strength of each media option.**
  - The end-of-run pH and the media options (Summary rows 28 and 64–67) keep today's activity coefficients.
  - Solving each option at its own ionic strength would move those pH values by a few hundredths.
- [ ] **Medium-specific O₂ salting-out.** Biology D121–D123 sum ion-specific Setschenow coefficients over the UdG ion set and apply them to every medium. The Media sheet now holds every medium's ion concentrations (rows 37–51), so the sum can be taken over the chosen medium.
- [ ] **Stock-acid protons in the as-weighed ionic strength.** Media row 58 counts the H⁺ of the stock acid as a free z = 1 ion, while row 9 gives it no conductivity because the phosphate buffer takes it up. Converting the equivalent HPO₄²⁻ to H₂PO₄⁻ instead would lower AM002's ionic strength by about 2 % and its conductivity by about 1 % (AM003 much less).
- [ ] **UdG trace elements.** The Media table has UdG's major salts only (Media V16). Enter the trace-element and iron stocks from Pous 2022/2023 if UdG is used again.
- [ ] **AM001 iron-stock acid strength.** Assumed 0.2 M as in AM002 (Media T17, design-assumption fill); the first iron stock's acid strength was not recorded.
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet. **Parked:** a high risk of breaking references for a naming nit.

### Required before claiming growth/productivity optimisation

These match Summary rows 204–210. All remain open; writing an acceptance criterion is not implementing it.

- [ ] **Define the primary measured outcome and operating domain.** Specific growth rate and volumetric product formation can have different optima. State which is primary, the culture phase, calibrated range and uncertainty; do not substitute minimum CO₂ use or a DO target for productivity.
- [ ] **Search duration and interval jointly.** Use executable settings and a response fitted to replicated measurements. Evaluate every rounded pair against all constraints. Report the best measured or predicted schedule within the tested/searched domain, search resolution and uncertainty; do not claim a global optimum from two pulse rules.
- [ ] **Enforce the full constraint envelope.** pH minima/maxima through each pulse and the biomass range, minimum DO and peak impairment, carbon trough and H₂ supply, peroxide/chlorine, carryover, OD-read gap, and validated gas hazard limits in both phases. Return no feasible schedule when appropriate. Today several are diagnostics only; end-of-run pH and mean-pH checks alone do not cover pulse extremes.
- [ ] **Couple uptake, transfer and growth over time.** Fit schedule- and biomass-dependent H₂ utilisation, biological O₂/CO₂ uptake, acidification and lag transition. The new scalar H₂ input fixes a missing measurement route but is not this dynamic model. Solve DIC and electrode reference states self-consistently at every search point.
- [ ] **Propagate uncertainty and check search convergence.** Include calibration/response uncertainty and correlations, including pulse-volume intercept/slope. Agree reliability margins, refine the search and report an indistinguishable optimum region when justified. One-at-a-time sensitivity is not a confidence interval.
- [ ] **Gate calibrations by matching conditions and acceptance evidence.** Confirm every accepted measurement actually replaces an operative parameter for the selected reactor, electrode, strain, medium, temperature, stirring and phase. A `Done` record does not wire a parameter into the model. Fit and validate the low-power current response before treating the extrapolated start-up power as measured.
- [ ] **Validate the recommendation independently.** Predict the winner before collecting held-out runs; compare with neighbouring executable pairs and the existing schedule. Check outcome repeatability and every constraint. If differences cannot be resolved, report equivalent schedules or a plateau.

### Additional experiments required for that objective

These match Summary rows 213–215. Their blue status cells are manual evidence records, not automatic optimisation approval.

- [ ] **Replicated duration × interval response experiment.** Randomise settings within a calibrated feasible domain, with matched controls and independent biological replicates. Record growth rate and productivity separately, all operating conditions, phase, biomass, sensor traces and uncertainty. Use pilot variability to determine replication sufficient to distinguish useful differences.
- [ ] **Cycle-resolved DO, pH, DIC and H₂ at candidate schedules.** Test pulse minima, maxima and means through lag, growth and the target biomass range; account for sensor lag, sampling losses and DIC storage. Measure H₂ utilisation rather than assuming complete uptake.
- [ ] **Independent comparison with neighbouring schedules.** Validate the predicted optimum against neighbouring executable pairs and the existing schedule using new replicated runs. Keep fitting and validation data separate; only claim a best-tested region when evidence supports it.

## Notes

- The model shows that CO₂ alone cannot dilute electrolytic O₂ to the DO target and also hold pH in band (Summary row 95).
- The owner's route is to fix the medium (T7). Summary rows 64–67 compare the options at today's schedule for the end-of-run biomass in row 17. On AM003 with 1 g/L biomass:
  - Ammonium (no change): minimum pH 6.43.
  - Add 0.81 g/L NaHCO₃: holds the 6.50 floor for the whole run.
  - Nitrate or urea in place of (NH₄)₂SO₄: minimum 6.49, the start-of-run value.
- With nitrate or urea there is no ammonia to scavenge free chlorine. In a chloride-containing medium such as UdG, free chlorine would then accumulate to the chloride pool (Chemistry D139).
