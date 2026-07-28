# Vial Cap – changelog

Done work, newest first. Open backlog is in `TODO.md`.

## 2026-07-28

[x] **Opus 5 code review of `Vial Cap.scad` – twelve mechanical defects fixed.**
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
