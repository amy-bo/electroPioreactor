# electroPioreactorGasModel – changelog

Done-work audit for `electroPioreactorGasModel-modular.xlsx`. Newest first. Open work is in `TODO.md`.

## 2026-06-19

- [x] **Experiment-protocol set + index** (`6ac8224`) — eight standalone bench SOPs in `protocols/`, each with an optimal and a budget route and tied to the exact model cell it feeds (vial geometry, surface kLa, faradaic efficiency, dissolved O2 + DO bands, per-reactor flow calibration, knallgas stoichiometry, sinter porosity, Gerrit current). Leverage-ordered `README.md` index; hyperlinked from the Summary improvements rows and the geometry-check row. Methods web-grounded and cited.
- [x] **Release-readiness review fixes** (`30b63be`, `2177e6b`, `472917d`) — from a multi-expert adversarially-verified review (verdict: RELEASE-WITH-FIXES). Calibration guard so an uncalibrated reactor shows "calibrate first" not `#DIV/0!`; dropdowns tightened to exact key columns; "Sinter OOR" now reddens on the right cell; conditional formatting + alert tokens extended; O2 Henry constant corrected to 1.2e-5 (Sander 2023, ceiling 10.7 mg/L); etaF=1 upper-bound banner; `kL_surf_crit` threshold cell; folded-block units, leaked-metadata cleanup; old single-sheet file removed; a geometry-consistency check added (flags the open B1).
- [x] **Selectors moved to the top of Summary** (`5a11ef7`, `b863b5e`) — reactor / electrode / organism / media dropdowns as the first control block; sinter porosity demoted; calibration `Reactor` key repointed.
- [x] **Imports-at-top reorg + Summary unit column** (`4261d25`) — every parameter sheet reordered top-to-bottom (imports, then calc, then lookup tables), all references/ranges/dropdowns/hyperlinks remapped; units moved into the Unit column.
- [x] **Folded the Dosing tab into Mass Transfer** (`2d01dfc`) — colliding names merged to single definitions, no behavioural change; six tabs.
- [x] **Dual schedule regime exposed** (`60960ec`) — O2-limited (~1.4 min) vs carbon-limited (~178 min) intervals both surfaced with a verdict, so neither is presented as definitive while `kL_surf` is unmeasured.
- [x] **Front-page input consolidation** (`e85196e`) — all experiment inputs on Summary (reactor/electrode/organism/media + LED intensity, stir rpm, media volume, temperature, pressure); warnings, ranked improvements, conditional formatting, source hyperlinks.
- [x] **CO2 flows single-table calibration** (`6b2d1ef`, `d0606c0`, `cb5bc24`) — one researcher-extensible table; reactor→latest-date lookup via SUMPRODUCT (replaced version-specific MAXIFS that errored on the user's Excel).
- [x] **Selector wiring + lookup tables** (`cf7812f`, `d82ed97`, `e47b6e0`) — reactor→type→geometry (VLOOKUP across all four types, fixing an NA cascade), electrode→sparger/z_e_ORR, organism→DO thresholds; steady-state DO band check; five lookup tables with dynamic dropdowns.

Earlier single-sheet history (pre-modular: cathodic O2 balance, surface-aeration path, sensitivity analysis, reference audit, gas-generation rates) is in the git log.
