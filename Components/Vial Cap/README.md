# Vial Cap + electrode holder

`Vial Cap.scad` is a parametric vial cap, septum and electrode top-stop in one OpenSCAD file. It supersedes the original O-ring cap and the separate ElectrodeTopStop, and can still reproduce the old O-ring cap via `seal = "oring"`.

`AEP2.0/Vessel Cap.stl` is the AEP0.2 cap as printed: a render of the `Vial Cap.scad` defaults (the one-piece holder). `Vial Cap.stl` is the earlier July 2026 render (PR #25), from before the August 2026 revision of the `.scad`; it is kept for reference and is not the printed part.

## Requires

BOSL2 for the GPI 24-400 internal thread (same as the original cap): https://github.com/BelfrySCAD/BOSL2

For fast rendering: use the nightly OpenSCAD and set Preferences -> Advanced -> Backend to "Manifold (new/fast)".

## What it does

- Seals with a full-width silicone septum instead of O-rings. One sheet seals the vial mouth, around each electrode, every port, and self-heals sampling-needle tracks. That is `seal = "gasket"`, the default; set `seal = "oring"` to bring back the original cap O-ring groove and the electrode O-ring grooves instead.
- Holds the electrodes with no play: a long journal bore plus an M3 wire clamp, referenced back to the cap.
- Parametric insertion depth: enter the electrode length and the protrusion you want into the vial, and the column height follows.
- Pioreactor-1.5 poka-yoke flange (rotatable via `flange_angle`), grip ribs (optional), GPI 24-400 thread.
- Prints support-free, either as a separate cap + top stop (`pieces = 2`) or as one piece (`pieces = 1`, top-stop down on the bed).
- Optional big septum openings (with an adjustable wall tilt) and optional per-port needle guides at the top-stop face.

## Options

All options are at the top of the file and commented inline. The main ones:

- Display / build: `view`, `part`, `pieces`
- Cap: `seal` (`"gasket"` = the full-width silicone septum, or `"oring"`), `port_style`, `ribs`, `flange_angle`
- Counts and sizes (as the original cap): `rods`, `rod_diameter`, `num_ports`, `port_diameter`
- Column height: `rod_length` and `insertion_depth` (these change the printed top stop; the printed AEP0.2 cap uses the defaults, 60 and 23)
- Septum access: `openings`, `opening_tilt`
- Needle guides: `guides`, `guide_height`, `guide_wall_multiple`
- Print settings: `layer_height`, `min_wall`

In `oring` mode the seal sizes are `cap_oring_thickness`, `rod_oring_thickness` and `rod_port_relief`; the closed-top thickness grows automatically so there is enough material to seat the cap O-ring (the electrodes used 5 mm ID / 9 mm OD / 2 mm CS O-rings).
