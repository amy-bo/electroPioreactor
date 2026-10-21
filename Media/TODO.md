# electroPioreactorGasModel – open work

Two lists, mirrored on the Summary tab. **Experiments to improve accuracy** are bench measurements that replace an estimate or a data gap in the workbook (Summary rows 105–131); the protocols are in `protocols/`. **Potential model improvements** are changes to the spreadsheet itself, each waiting on the owner decision or data named (Summary rows 133–139). Done work is in `CHANGELOG.md`.

## Experiments to improve accuracy

In rough leverage order. Enter results in the matching **Calibrations** section where one exists, leaving Include blank until the protocol's acceptance, species-balance and transferability gates are met. Numbers quoted are for the AMYBO03 baseline (ed04, MMO tube, *Xanthobacter tagetidis*, 30 °C); read the workbook for other selections.

- [!] **Vial geometry and true headspace (blocker for the pulse).** Total vial volume (20 mL nominal) and the cylinder geometry (`A_x`·`D_int` ≈ 27.6 mL) disagree by about 38 %, and the pulse moves almost 1:1 with the headspace. `Geometry!geom_check` flags INCONSISTENT until measured (`protocols/vial-geometry.md`; Calibrations vial-geometry section). Wall thickness with calipers at the same time.
- [ ] **Vent back-draw flow.** The vent type is settled (open: tubes or needles to 0.2 µm PTFE filters, no check valve; owner T5) and the cap leak is taken as fixed (T6), so what remains is the air drawn back after each pulse (`Q_backdraw`, Mass Transfer D385, an estimate), the biggest remaining input to the interval (`protocols/headspace-vent.md`, pressure trace or headspace O₂ tracer). Pressure sensing must resolve both signs around ambient, and liquid O₂ exchange must be shown negligible or modelled jointly.
- [ ] **Surface kLa** (`protocols/surface-kla.md`; Calibrations surface-kLa section, 1/h). Sets how far DO must sit above the headspace and the feasibility margin of the DO strategy (growth 1.74×, lag 0.61× on the estimate).
- [ ] **Electrode mass-transfer coefficient** (`protocols/electrode-mass-transfer.md`; Calibrations rows 142–149, at the Summary rpm and temperature). Sets the cathodic O₂ loss, the peroxide source and sink, the chlorine cap and the electrode-surface pH verdict.
- [ ] **Abiotic DO trace under the schedule** (`protocols/abiotic-do-trace.md`). One cell-free run tests the whole headspace balance against the lag predictions (Summary rows 61–62, and row 33 at the start-up schedule).
- [ ] **Headspace H₂/O₂ during lag, before any unattended run** (`protocols/headspace-gas-safety.md`). The model puts the lag headspace near 9 % H₂ mean and 15 % before each pulse at the growth schedule, 3 % before each pulse at the start-up schedule (Summary row 33). Needs an owner-approved, non-perturbing sampling and gas-clearance procedure first; the workbook is a screen, not a certificate.
- [ ] **Off-gas H₂ at steady growth** and the **knallgas uptake ratio** (`protocols/knallgas-stoichiometry.md`; Calibrations knallgas section). Sets the O₂ surplus (`bio_O2`, up to ±200 % on the schedule) and the carbon demand.
- [ ] **Cathodic and anodic Faradaic efficiency** (`protocols/faradaic-efficiency.md`). The collection rig is not finalised and separation changes O₂ crossover: establish recovery, species balance and transferability to the undivided cell before including a result. A low H₂ yield alone cannot quantify ORR.
- [ ] **Cell voltage at a known setpoint** (multimeter) and the **electrode centre-to-centre gap** (calipers). The budget predicts about 2.65 V of the 5 V rail at 3 % (Electrochemistry D119).
- [ ] **Dissolved Cu/Ni/Fe in spent medium.** The anode sits about 1.2 V above Cu²⁺/Cu, so dissolution is allowed; closes the anodic charge budget and tests the prime suspect for the Exp-2 death.
- [ ] **CO₂ flow of the reactor actually used, and per-reactor flows** (`protocols/flow-calibration.md`). ed04 stands in as the only calibrated reactor; an AEP0.2 build needs its own run, then select it in Summary D2. Record collection humidity, temperature and pressure (gas reference conditions).
- [ ] **Per-pulse CO₂ volume with the sparger attached and the shortest reliable pulse** (flow-calibration steps 9–10). Keep new calibration rows excluded until short-pulse delivery and the per-pulse intercept are validated.
- [ ] **No-carryover maximum flow** per reactor (CO2 flows column M; Summary D45 reads "not measured").
- [ ] **Free and combined chlorine (DPD)** in spent UdG (`protocols/chlorine-species.md`; Calibrations rows 155–162). Settles the monochloramine lifetime (moves the UdG interval about ±32 %); AMYBO03 is chloride-free. Confirm the CaCl₂ hydrate state at the same time (−24 % on every chlorine figure).
- [ ] **Organism DO bands** for the non-*necator* organisms and the minimum-DO column (`protocols/dissolved-oxygen.md`; Calibrations DO section). Owner must set the screen's controls and analysis first: gas-matched current-density controls, replicates and equivalence margins.
- [ ] **AMYBO03 conductivity at the operating temperature.** The finite-strength factor 0.78 is anchored near I ≈ 0.1 M; AMYBO03 is about 0.2 M.
- [ ] **Low-power current curve below 3 %** (`protocols/gerrit-current.md`). Off and below-fit settings are rejected today; needed before a start-up current ramp can be modelled.
- [ ] **Supplier facts:** the LED-driver rail and compliance, and whether the strain current-density limits are per anode or cathode, geometric or wetted area.
- [ ] **Electrochemist review** of the calculated electrochemistry. The weakest inputs are the anodic exchange-current density (four decades in the literature) and the mass-transfer coefficient.

## Potential model improvements

Spreadsheet changes. Each needs the decision or data named before it can be made well.

- [ ] **Separate N₂ flush in the sawtooth.** Summary D14 enters N₂ by its mean flow, exact for the mean-field fractions. Pulsing N₂ midway between CO₂ pulses (owner T7) adds a second flush per cycle and would lower the pre-pulse peaks a little further. Waits on: whether N₂ is used at all; the owner prefers fixing the medium.
- [ ] **Nitrate or urea instead of NH₄⁺.** Ammonium uptake releases acid as the culture grows; the model holds NH₄⁺ at its recipe value. Part of fixing the medium. Waits on: the owner's nitrogen source and a measured uptake rate.
- [ ] **Pulse length from the shortest reliable pulse.** Summary D18 is a rule of thumb (about one headspace volume per pulse). A twin trial at a 0.25 s floor held pH and growth DO on about 7 % less CO₂ but raised lag-phase DO. Waits on: the measured solenoid floor and per-pulse volume.
- [ ] **Start-up current ramp.** Lag DO stays unreachable at the estimated surface kLa at any interval (Summary row 66), so the remaining lever is less current until uptake starts. Waits on: the low-power current curve.
- [ ] **Carbon bound on the pool trough.** The carbon interval (Mass Transfer D112) is sized on mean supply; Mass Transfer D435 warns when a long interval lets the pool run dry within the cycle. Only reachable with N₂ at present. Waits on: the owner's trough margin over RuBisCO Km (Biology D98).
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet – **parked**: high reference-break risk for a naming nit.

## Notes
The model shows that CO₂ alone cannot dilute electrolytic O₂ to the DO target and hold pH in band (Summary D52). The owner's route is to fix the medium (T7): Summary rows 80–81 give the NaHCO₃ for the band floor at today's schedule (about 0.13 g/L on AMYBO03). N₂ remains available as an input, pulsed apart from CO₂ if used.
