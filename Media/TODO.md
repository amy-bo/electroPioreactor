# electroPioreactorGasModel – open work

Two lists, mirrored on the Summary tab.
- **Experiments to improve accuracy** are bench measurements that replace an estimate or fill a data gap in the workbook (Summary rows 131–157). The protocols are in `protocols/`.
- **Potential model improvements** are changes to the spreadsheet itself (Summary rows 160–161).

Done work is in `CHANGELOG.md`.

## Experiments to improve accuracy

The order matches the Summary. Impact runs HIGH > MED > LOW. Within each impact level, effort runs low > med > high, and within each impact and effort pair the most leverage comes first. So reading top to bottom is a sensible programme.

Summary column D shows each experiment's status in the situation selected on the Summary (reactor, electrode, organism, medium and temperature):
- **Done:** green.
- **Approximate:** amber. Useful data that could be improved.
- **Not done:** red.
- **Not needed:** green, when the selection makes the experiment irrelevant.

How the status is found:
- An included run in the matching Calibrations section counts.
- So does a row in the **experiment record** at the bottom of the Calibrations tab. In a record row, any condition left blank means the result holds for any value of it.
- `Calibrations!xs_*` holds the logic for each experiment.

Enter results in the matching Calibrations section where there is one. Leave Include blank until the protocol's acceptance, species-balance and transferability gates are met. The numbers quoted below are for the AMYBO03 baseline: ed04, MMO tube, *Xanthobacter tagetidis*, 30 °C.

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
  - Approximate in UdG phosphate: about 3.4 V at 3 % in Exp 1, with the meter not recorded. Not done in AMYBO03.
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
  - Protocol: `protocols/knallgas-stoichiometry.md`.

### MED impact

- [ ] **CO₂ flow calibration for each reactor.** MED, low effort.
  - Approximate: only ed04 is calibrated.
- [ ] **Vial wall thickness.** MED, low effort.
  - Measure with calipers, at the same time as the vial volume.
- [ ] **Free and combined chlorine (DPD).** MED, low effort.
  - Protocol: `protocols/chlorine-species.md`.
  - Not needed in chloride-free AMYBO03.
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
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet. **Parked:** a high risk of breaking references for a naming nit.

## Notes

- The model shows that CO₂ alone cannot dilute electrolytic O₂ to the DO target and also hold pH in band (Summary row 95).
- The owner's route is to fix the medium (T7). Summary rows 64–67 compare the options at today's schedule for the end-of-run biomass in row 17. On AMYBO03 with 1 g/L biomass:
  - Ammonium (no change): minimum pH 6.43.
  - Add 0.81 g/L NaHCO₃: holds the 6.50 floor for the whole run.
  - Nitrate or urea in place of (NH₄)₂SO₄: minimum 6.49, the start-of-run value.
- With nitrate or urea there is no ammonia to scavenge free chlorine. In a chloride-containing medium such as UdG, free chlorine would then accumulate to the chloride pool (Chemistry D139).
