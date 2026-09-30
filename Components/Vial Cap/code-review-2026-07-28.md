# Vial Cap code review, 2026-07-28 (not yet applied)

The Opus 5 code review of `Vial Cap.scad` found twelve mechanical defects and fixed them in commit `4a78dbc` on the `Opus5-code-review` branch. Those fixes were made against the file as it stood before main's revision #28 (latest vessel cap, descriptive variable names), so they are **not** in the current `Vial Cap.scad` and cannot be cherry-picked: re-apply them by hand to the renamed variables, then render in OpenSCAD and check (they were only checked numerically). At least one defect is still present in the current file: the gasket ridge stops short of the bore wall, so the cap exports as two separate pieces. `code-review-2026-07-28.patch` below is the original commit, kept so the branch can be deleted.

## The fixes (from the review's CHANGELOG)

Ten finder angles ran against the file; seven returned, and every fix below was
confirmed independently by two or more of them plus an arithmetic pass. All
fixes are verified numerically – **not rendered**, as the container has no
OpenSCAD binary (see `TODO.md`).

- **Floating gasket ridge.** `gasket_ridge()` had an outer radius of
  `gask_seat_d/2` = 12.10 against a bore wall at `T_nom/2` = 12.15, so the
  gasket retainer was attached to nothing: the bore cut voided r < 12.15, the
  gasket-seat cut then deleted the only overlapping slice, and the thread
  stopped 1.6 mm short with its lead-in already tapered. The cap exported as
  two disjoint shells and, printed closed-top-down, the ring started in mid-air
  2.6 mm above the bed. Now reaches the wall with 0.05 mm of overlap.
- **`seal="oring"` sealed nothing – both grooves.** The `mirror([0,0,1])` left
  the cap dovetail at z = [8.80, 9.80] against a slab at [9.80, 12.30] – zero
  overlap, removing only a 0.085 mm nick, under one extrusion width. The rod
  groove sat at z = [6.05, 8.55], wholly inside the empty bore. Both relocated
  into the slab, with 1.00 mm and 2.50 mm of overlap respectively.
- **`holder1()` reamed away the cap's friction fit.** Its rod-clearance bore
  ran from z = −0.05 through the whole cap at `col_bore` + 0.02 = 6.67, so the
  documented 6.35 mm friction bore was fully removed even at $fn=48 (inscribed
  radius 3.328 > 3.175). Rods were left with 0.47 mm of diametral slop instead
  of 0.15, located only by the clamp band and cantilevered ~37 mm. The bore now
  starts at the funnel underside.
- **Ceiling was 0.550 mm, not the documented 0.600.** The gasket-seat cut's
  `+eps` extended into the ceiling rather than the coincident plane below it,
  leaving 2.75 layers against `top_th = 3*layer_h`, a knife-edge annular ledge
  on the still-coincident seat floor, and a desynchronised `z_ceil` – the datum
  for the whole fan-window construction. `eps` moved to the bottom.
- **`guides_topstop()` silently dropped guides.** It built one half-disc for the
  entire far set with no angular-span check, unlike `guides_solid()`. At the
  documented `openings=0` all five ports land in the far set spread over 360°,
  and the y ≥ 4.639 clip left the two ports at (±3.4, −5.889) with no guide
  material at all – two of five requested guides vanishing into bare 2.2 mm
  holes. Now merges into one disc only when the far set spans ≤ 90°, otherwise
  builds per-port, and interpenetrates the clamp band by 0.2 mm.
- **`body2d()` filleted the wrong corners.** The morphological *opening*
  (dilate ∘ erode) rounds convex corners, but `tab_round` is documented as the
  fillet at the flange/cap junction, which is reentrant at −43.5°. The stress
  riser the parameter exists to remove was left perfectly sharp while the
  flange's own convex corners were cut back ~0.2 mm. Now closes then opens.
- **Funnel weld had no interpenetration.** The deliberate 0.05 mm overlap was
  clipped straight off by an intersection prism starting at exactly `cap_h`,
  leaving two solids welded on one full coplanar face with zero margin. Clip
  lowered to keep the overlap.
- Cap rod bore extended through the cap-top guides.
- Tautological assert replaced with a real `port_R` guard; new guards for a
  reversed `n_centre` range, for `funnel_h` overhang (using the previously dead
  `cap_R`), and for `col_h > 0`.
- Dead `port_style=="ports"` branch removed from `ports2d()`; stale "8.7"
  comment corrected.
- `port_d`'s comment now records that 2.2 mm is sized for Pioreactor v1.5
  (Vial Cap S) stainless luer-lock needles rather than silicone tube OD.

One suggested deeper fix was rejected as actively wrong: tying `bearing_r`'s
clearance to `min_wall` would give min(4.9, 3.949) = 3.949 and thin the journal
wall to 0.62 mm, worse than the 0.15 mm literal it replaced.

## What the review left open (from its TODO)

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
