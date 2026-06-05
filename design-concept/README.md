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

| File | What it is |
|---|---|
| `electrode-holder-v3.scad` | **The current concept.** Open in OpenSCAD; set `view` and `port_style`. |
| `electrode-holder-v3-figure.png` | Top view (ports in the neck) + corrected clamp + print orientation. |
| `vial-cap-redesign.scad` | **Production cap**, derived from the real `Vial Cap.scad` (thread/ribs/ports kept; O-rings → septum seat; pegs + poka-yoke added). Needs a render-check in OpenSCAD. |
| `vial-cap-s.3mf` | Pioreactor Vial Cap S — the poka-yoke reference. |
| `pokayoke-from-3mf.png` | Slices through that mesh, how the tab geometry was read off it. |
| `electrode-holder-v2.scad` / `…-concept.scad` | Earlier concepts (v2, v1). Superseded — kept to show the progression. |
| `make_*.py` | Generators for the figures (plain-stdlib SVG, no dependencies). |

Open the concept SCAD and try: `view = "exploded" | "assembled" | "section" | "print"`,
and `port_style = "ports" | "open"`.

## Fixes from the v2 review

- **Poka-yoke** is an *additive rounded tab* on one side of the cap (read off
  `vial-cap-s.3mf`), not the subtractive flat v2 had.
- **Ports** sit at the current cap's radius, `r = (cap_o_ring_id − port_dia)/2 ≈
  7.785 mm`, inside the vial neck — v2 had them too far out.
- **Clamp** is the correct stack, outside-in: Allen bolt → **outer wall** →
  **captive nut** (drops into a top slot sized to its flats, so it can't rotate)
  → **inner wall** (retains the nut) → wire pinched on the electrode. Walls are
  thicker PC-CF than the current part, which Grace cracked by over-torquing.

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
