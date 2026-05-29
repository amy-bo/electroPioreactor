// GL45BottleHolder – Pioreactor dovetail GL45 bottle holder
//
// The upstream Duran holders (e.g. Printables 1058356) have lettering
// cut into the four corners. Those recessed letter shapes trap residue
// and are awkward to clean. This SCAD imports the chosen upstream holder
// and fills its corner lettering with smooth caps, leaving the rest of
// the geometry untouched.
//
// Pick the bottle size below, then render (F6) and export the STL.

// ---- selector ----------------------------------------------------------
bottle_ml = 250;   // [250, 500, 1000]

// ---- source holders ----------------------------------------------------
// 250 ml is an 85.75 mm square platform; 500 ml and 1000 ml share a larger
// 125.7 mm square platform, but their corner labels ("0.5 L" vs "1 L") sit
// in slightly different spots, so each size has its own cover positions.
function source_file(ml) =
      ml == 250  ? "./source/duran_holder_platform_center_0.25L.stl"
    : ml == 500  ? "./source/duran_holder_platform_center_0.5L.stl"
    : ml == 1000 ? "./source/duran_holder_platform_center_1L.stl"
    : undef;

// ---- corner cover positions  [x, y, angle] -----------------------------
// Each cover is a stadium (a rectangle with semicircular ends) laid along the
// corner->centre diagonal so it hugs the diagonal text run. The rounded ends
// keep the cap inside the platform outline near the chamfered corners, so no
// overhang and no clipping are needed. x,y are each cap's centre and the third
// value is its angle; all sit on the 45/135 corner diagonals. Positions were
// dialled in by eye against the rendered holders.

// 250 ml: centres are Gerrit's verified positions (its 0.25 mm-deep engraving
// is too shallow to remeasure).
covers_250 = [
    [ 7.75, 13.00,  45],   // bottom-left
    [72.25, 78.00,  45],   // top-right
    [ 7.80, 77.95, 135],   // top-left
    [72.40, 13.55, 135]    // bottom-right
];

// 500 ml: positions tuned by eye against the rendered 0.5 L holder.
covers_500 = [
    [ 15.5,  21.0,  45],   // bottom-left
    [105.0, 111.0,  45],   // top-right
    [ 15.5, 111.0, 135],   // top-left
    [105.0,  21.0, 135]    // bottom-right
];

// 1000 ml: positions tuned by eye against the rendered 1 L holder.
covers_1000 = [
    [ 12.3,  18.0,  45],   // bottom-left
    [107.7, 113.5,  45],   // top-right
    [ 12.2, 113.5, 135],   // top-left
    [108.0,  18.0, 135]    // bottom-right
];

function covers(ml) =
      ml == 250 ? covers_250
    : ml == 500 ? covers_500
    : covers_1000;

// ---- cap size ----------------------------------------------------------
// len = tip-to-tip along the text, wid = across it (= diameter of the rounded
// ends). 250 ml matches the proven cover envelope (~1.3 mm inside the edge);
// 500/1000 ml sit 12-18 mm in from every edge, so their caps are sized
// generously to swallow the label plus a few mm of measurement slack with minimal
// risk of overhang. Holders are 30 mm tall, so a 30 mm cap is full height.
cover_margin = 1.05;   // 5% extra on every cap X-Y dimension for positioning headroom
cover_len = ((bottle_ml == 250) ? 15 : (bottle_ml == 500) ? 21 : 14) * cover_margin;
cover_wid = ((bottle_ml == 250) ? 8 : (bottle_ml == 500) ? 10 : 10) * cover_margin;

$fn = 48;   // smooth rounded ends

// Full-height (0..30 mm) so the cap top is flush with the platform surface.
module cover(angle) {
    rotate([0, 0, angle])
    hull()
        for (s = [-1, 1])
            translate([s * (cover_len - cover_wid) / 2, 0, 0])
                cylinder(h = 30, d = cover_wid);
}

// ---- build -------------------------------------------------------------
import(source_file(bottle_ml));
for (c = covers(bottle_ml))
    translate([c[0], c[1], 0]) cover(c[2]);
