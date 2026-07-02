# electroPioreactorGasModel – open work

Open backlog and parked items. Done work is in `CHANGELOG.md`. Bench SOPs for the measurement items are in `protocols/`.

## Open

- [!] **B1 – reconcile vial geometry (blocker).** The vial total volume (20 mL nominal) and the cylinder geometry (`A_x`*`D_int` ~ 27.6 mL) disagree ~38%, and the headline optimal pulse is ~4x sensitive to the resulting headspace. Needs a bench measurement of the true fill-to-septum free-gas volume + uniform-bore depth (only the user can do this). Until then `Geometry!geom_check` flags INCONSISTENT and the optimal pulse is marked provisional. Method: `protocols/vial-geometry.md`.
- [ ] **Run the experiment protocols** (`protocols/README.md`, in leverage order) to replace the model's assumed/data-gap (pink) values with measured ones. The protocols are now follow-blind: record the raw numbers in the matching section of the **Calibrations** tab and the model updates itself; re-read the Summary dashboard after each.
- [ ] **Measure surface kLa (#1 priority).** After measuring, record it in the **Calibrations** tab (Surface kLa section) and confirm it exceeds `kL_surf_crit`; this resolves the 1.4-min vs 178-min sparge-interval question (`protocols/surface-kla.md`).
- [ ] **Measure cathodic faradaic efficiency `etaF`.** While it is assumed 1.0, all O2 figures (and the sparge interval) are an optimistic upper bound.
- [ ] **Per-reactor CO2 flow calibration** for reactors other than ed04 (`protocols/flow-calibration.md`); an uncalibrated reactor shows "calibrate first" by design.
- [ ] **Fill the HOB DO bands** for the non-necator organisms and the minimum-DO column (currently pink gaps).
- [!] Rename the `Reactor` / `Reactor_sel` / `reactor_sel` defined-name triplet for consistency – **parked**: high reference-break risk for nit-level value; revisit only if a clean rename harness exists.

## Notes
The workbook itself is release-ready bar B1: the multi-expert review's blockers B2/B3/B4 and majors M1–M5 are resolved (see `CHANGELOG.md`). The protocols are what turn the model's default/assumed figures into measured, optimal ones.
