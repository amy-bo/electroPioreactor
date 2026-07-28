# Vial Cap – open work

Open backlog and parked items. Done work is in `CHANGELOG.md`.

Raised by the Opus 5 code review of `Vial Cap.scad` (2026-07-28). The twelve
mechanical defects that review found are fixed and logged in `CHANGELOG.md`;
what follows is everything it deliberately did **not** touch, because each one
needs a design decision rather than a patch.

## Design context – ports are needles now

The cap is being designed around **Pioreactor v1.5 (Vial Cap S) stainless
luer-lock needles**, not the 3.175 mm silicone tubes the older cap used.
`port_d = 2.2` is therefore intentional, not the regression the review first
read it as. Everything under "docs and model still describe tubes" below flows
from that change not having been carried through the rest of the repo yet.

## Open

- [ ] **Confirm the needle gauge and how the hub lands.** 2.2 mm takes a shaft
  up to ~14 G (2.11 mm OD). Pioreactor's own guidance of 21–23 G is for the
  self-healing sampling plug, not for the through-cap ports, so it does not
  settle this. Needs the actual v1.5 needle measured, plus a decision on
  whether the luer hub seats on the cap top face or stands clear of it.
- [ ] **Docs and model still describe tubes.** `Media/electroPioreactorGasModel.py`
  lines 78, 81 and 95 set `spg_OD` = `eff_OD` = `xtube_OD` = 3.175 mm for all
  five cap-penetrating lines, and `Components/README.md:52` buys 1/16" ID
  silicone. Every headspace and DO figure in the gas model therefore describes
  a cap that no longer exists. Re-run the model against the needle bore once
  the gauge above is fixed.
- [ ] **Protocols cite a third figure.** `Media/protocols/dissolved-oxygen.md:32`
  and `Media/protocols/surface-kla.md:37` both say "1.4 mm ports", matching
  neither 3.175 nor 2.2. Correct to whatever the needle decision lands on.
- [ ] **`seal="oring"` + `pieces=2` leaks through the top.** The peg hole
  (r 1.650 at ±2.0) and the rod bore (r 3.675 at ±4.8) are 5.200 apart against
  a radius sum of 5.325 – the two voids merge with 0.125 mm of overlap, opening
  an unsealed slot straight through the closed top. The peg itself clears the
  bore by 0.025 mm, so it survives as a knife edge and cannot plug the slot.
  Needs a `peg_off` or `peg_d` change, not a local patch.
- [ ] **Tube guides never render for `pieces=2`.** `guides_solid()` is gated on
  the global `part=="cap"` and `guides_topstop()` is only reachable from
  `holder1()` (`pieces==1`), so the printed two-piece build gets no guides at
  all. Simply enabling `guides_solid()` collides: a tower at (3.4, 5.889) with
  rg 1.94 reaches y 3.95, inside the racetrack's ±4.639. Wants an explicit
  `guides_on_cap` option and a placement that clears the column.
- [ ] **Front top-stop guides roof the needle-access window.** Half-discs of
  Rf 4.03 at (±3.4, 4.639) cut the straight-down aperture from 6.05 mm to
  3.90 mm of y, and `dissolved-oxygen.md:32` / `surface-kla.md:37` both depend
  on that gap for a fibre-needle DO microsensor. A genuine tension between
  guiding the needles and reaching past them – decide which wins.
- [ ] **`guide_pts()` duplicates the port ring and has already diverged.** It
  re-derives placement independently of `port_holes2d()` and implements only
  one of that function's three branches. At the documented `rods=0` it returns
  60/120/240/300/270 deg against ports at 0/72/144/216/288 – five guides where
  there is no hole and five holes where there is no guide, with the guide domes
  never bored. `n_ports=0` still yields one phantom point. Wants one shared
  placement function, not two hand-synced copies.
- [ ] **Nothing has been rendered.** The container has no OpenSCAD binary, so
  every fix in `CHANGELOG.md` is verified numerically and by bracket balance
  only. Open the file in OpenSCAD (nightly, Manifold backend) and render
  `view="print"` for `pieces=1` and `pieces=2`, both `seal` values, before
  trusting any of it on a printer.
- [ ] **Cap README describes a cap that is not built.** Its only note is the
  5 mm ID / 2 mm CS electrode O-ring, which no default build now has, and
  `MixedElectroPioreactor/Assembly-EdMSc26.md:43` still tells a student to seat
  electrode O-rings that have no groove.
- [ ] **Insertion-depth datum is undefined by 10 mm.** `Assembly-EdMSc26.md:49`
  says "bases 33 mm below the bottom of the vial cap" against
  `insertion_depth = 23`. The two only reconcile if the datum is the septum
  plane (23 + 9.7 = 32.7), which is stated nowhere. Name the datum.
- [ ] **`electroPioreactorGasModel.xlsx` is dirty in the working tree.**
  `Reactor_sel` is switched from ed04 to imp12 and `led_intensity` from 3 to
  12, so the Summary block opens on `#N/A` and "calibrate this reactor first",
  and D49 flips from "EXCEED" to "OK". Raw XML diff confirms zero formula
  changes and 280 cached-value changes from a genuine Excel save, so the caches
  are sound – it just needs switching back with Excel open. Deliberately left
  out of this branch.
