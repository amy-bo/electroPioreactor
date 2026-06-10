# GL45 Bottle Holder

Pioreactor dovetail platform holder for a GL45 Duran bottle, in 250 ml, 500 ml and 1000 ml sizes.

## What to print

Pick your bottle size:

- [`GL45_holder_250ml.stl`](GL45_holder_250ml.stl)
- [`GL45_holder_500ml.stl`](GL45_holder_500ml.stl)
- [`GL45_holder_1000ml.stl`](GL45_holder_1000ml.stl)

## What this fixes

The upstream Duran holders (e.g. [Printables 1058356](https://www.printables.com/model/1058356-duran-bottle-holding-platform-for-pioreactor-platf/files)) have lettering cut into the four corners. The recessed letter shapes trap residue and resist cleaning. This component renders the same geometry but with the corner lettering filled by smooth caps, leaving the rest untouched.

## Re-rendering / other sizes

`GL45_holder.scad` is the source. Open it in OpenSCAD, set `bottle_ml` to `250`, `500` or `1000`, then render and export. The three STLs above are produced this way, so they stay in sync with the SCAD.

## Files

- [`GL45_holder.scad`](GL45_holder.scad) – source recipe; set `bottle_ml` to choose the size
- `GL45_holder_250ml.stl` / `GL45_holder_500ml.stl` / `GL45_holder_1000ml.stl` – **ready to print**
- `source/` – the upstream Duran holders, kept in-repo so the SCAD renders offline. Not for printing.
