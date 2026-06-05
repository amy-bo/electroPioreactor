# Vial cap + electrode holder redesign — concept

Working concept for optimising the [Vial Cap](../Components/Vial%20Cap) and
[ElectrodeTopStop](../Components/ElectrodeTopStop) against the brief: parametric
insertion depth, easy electrode insertion, reliable wire-to-electrode contact,
**rigidly held (non-wobble) electrodes**, a full-width self-sealing silicone
septum, Pioreactor-1.5-style poka-yoke, and **support-free printing on a single
filament Bambu**.

This folder is the ideation trail, kept so the design process can be retold
later. It is scratch — not the production part.

## Files

One source file; iterations live in git history, not in `v2`/`v3` files.

| File | What it is |
|---|---|
| `electrode-holder.scad` | **The design.** Cap + septum + column in one file. Options at the top. |
| `electrode-holder-figure.png` | Top views (both port styles) + clamp cross-section + print orientation. |
| `vial-cap-s.3mf` | Pioreactor Vial Cap S — the poka-yoke reference. |
| `pokayoke-from-3mf.png` | Slices through that mesh, how the tab geometry was read off it. |
| `make_figure.py` | Generator for the figure (plain-stdlib SVG, no dependencies). |

Options (choices listed inline in the file):
`view = "exploded" | "assembled" | "section" | "print"`,
`part = "all" | "cap" | "column" | "septum"`,
`port_style = "ports" | "open"`,
`pieces = 2 | 1`.

Requires BOSL2 (same as the current `Vial Cap.scad`) — the GPI 24-400 thread is
the real one now.

## Design notes

- **Thread + septum ridge.** Real GPI 24-400 internal thread (BOSL2, verbatim
  from `Vial Cap.scad`). A small chamfered inward **ridge** under the seat keeps
  the silicone septum from dropping out when the vial is removed.
- **Poka-yoke** is the real Vial-Cap-S tab: a *constant-radius plateau* (outer
  edge ~17 mm from centre, ~±28°) filleted into the cap, read off `vial-cap-s.3mf`.
- **Fits** (two parameters): `cap_fit` is a snug friction fit so the **cap** grips
  the electrode; `insert_extra` is the additional clearance in the **column** for
  easy insertion (the bolts do the holding there). Column bore = `cap_fit +
  insert_extra`, so tuning `cap_fit` moves both together.
- **Ports** at `r = (cap_o_ring_id − port_dia)/2 ≈ 7.785 mm`, inside the neck.
- **Clamp** (outside-in): Allen bolt → **outer wall** → **non-rotating nut** (thin
  side along the bolt) → **inner wall** → wire pinched on the electrode. Sits at
  the top face so it lands on the bed when printed; the nut pocket opens
  downward-in-use (upward-in-print) so there's no bridge. Robust PC-CF walls.
- **Open port style** keeps a **full-width** x-spine that carries the electrodes
  and fully surrounds the pegs, leaving two large septum windows with **rounded
  corners** (no sharp dirt traps).
- **Pegs** are plain, `top_th` deep, so they sit flush with the cap's inside
  ceiling and don't push the septum.
- **1 vs 2 pieces** (`pieces`). `2` = separate cap + top stop (pegs register
  them). `1` = the whole holder printed as one part: it prints **top-stop-down**,
  and **V-legs** splay out from the top stop to the cap rim — they hold the wide
  cap up at ≤45° (no supports) and sit clear of the ports so needles still reach
  the septum between them. The leg count/positions (`leg_angles`) are a starting
  point — print-test and tune the cap-disc bridging between legs.

## Print check (no supports)

Cap (closed-top-down): cavity opens up; thread, ports, peg holes all vertical;
septum ridge is a ≤45° barb; tab is a vertical lobe. Column (flush-face-down,
pegs up): bores vertical; clamp ears reach the bed; nut pocket and wire slot open
upward-in-print; bolt holes teardropped. **Render-check** the BOSL2 thread, the
ridge, and the `offset()` tab/windows when you open it — there's no OpenSCAD in
the dev box to do it here.

## The design problem (and the one idea that reframed it)

The electrodes were located at two points — soft cap O-rings below and a top
stop above. Both points being on **compliant** features (O-rings; a top stop
that floats on the electrodes) meant the electrodes could pivot, and the
electrode pair could move as a couple. The brief wants **zero degrees of
freedom** once the M3 bolts bite.

The reframing idea: **separate the two jobs that were fighting in one feature.**
Sealing and holding do not belong together.

- **Holding** → rigid plastic, in a part referenced to the cap.
- **Sealing** → the soft silicone septum, which grips nothing.

## How the electrodes reach zero DOF

A rod has five DOF worth constraining (its spin is harmless): two lateral
translations, two tilts, one axial slide.

| Feature | Lateral | Tilt | Axial |
|---|---|---|---|
| Long vertical bore through the **solid column** (a journal bearing) | locked | locked | — |
| Two **pegs** locking the column to the cap (so that bearing is referenced to the cap, not floating) | — | — | — |
| **M3 clamp** pushing the wire onto the electrode | — | — | locked |

The pegs are the part that was missing from v1: without them the column +
electrodes are rigid only *as a couple that floats*. Pegging the column to the
cap ties the bearing back to the vessel.

## How the septum seals

A self-sealing septum needs **axial compression + radial confinement**. The
silicone disc sits in the cap against the closed-top underside, confined by the
cavity wall; screwing the cap onto the vial drives the glass rim up into it.
That single squeeze seals the vial mouth, seals around each electrode, seals
every port, and self-heals sampling-needle tracks. It replaces the cap O-ring
*and* both electrode O-rings *and* the per-port seals with one sheet.

Two port strategies (a parameter):

- **`ports`** — a 6×3.2 mm ring (matches the current design), each self-sealed.
- **`open`** — open septum windows, so a needle can go in anywhere.

## Insertion depth is parametric

The column rests on the cap and the electrode is pushed flush with the column's
top face, so:

```
column_height = electrode_length − insertion_depth − cap_height
```

Enter your electrode length `L` and desired protrusion `g`; the column height
follows, and "flush with the top" is then exactly the right depth.

## Why every printed part is support-free

Proven in `view = "print"` and the figure's bottom panel.

- **Cap** prints **closed-top-down, mouth-up** — exactly how a normal screw cap
  prints. The interior cavity opens upward, the thread is self-supporting at
  this scale (the current cap already prints this way), and every port /
  electrode / peg hole is a vertical hole. Moving to the septum also *deletes*
  the old O-ring grooves, which were the only overhanging features.
- **Column** prints **flush-face-down, pegs up.** The bores are vertical; the
  only horizontal features are the M3 clamps, drawn as a **teardrop** clearance
  hole and a **vertex-up hex** nut trap — the standard self-supporting patterns.

## Poka-yoke

A flat on the cap OD (a vertical wall, so still support-free) keys the vial to
one rotational orientation in the Pioreactor, matching the 1.5+ approach.

## Status / next steps

Concept geometry only — simple primitives, schematic tolerances. To productionise:
wire in the real GPI 24-400 thread (BOSL2, as the current cap), measure the
20 ml vial rim and chosen electrode/septum stock, set real print clearances, and
test-print the cap thread fit and the clamp nut trap.
