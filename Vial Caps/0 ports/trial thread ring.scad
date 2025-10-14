// BOSL2 GPI 24-400 internal thread cap (test ring)
// Requires BOSL2 in your OpenSCAD libraries path:
//   https://github.com/BelfrySCAD/BOSL2
// If your path differs, adjust the `use <...>` lines.

use <BOSL2/std.scad>
use <BOSL2/threads.scad>

// -----------------------------
// Cap & thread parameters
// -----------------------------
cap_od        = 27;          // mm (outer diameter of ring/cap)
cap_h         = 8;           // mm (overall height)
top_th        = 0;           // mm (flat top thickness; 0 = open ring)

// GPI 24-400 basics
T_nom         = 24.10;       // "T" dimension (outside dia over threads)
dia_clear     = 0.30;        // diametral print clearance (tune 0.20–0.50)
pitch         = 25.4/8;      // 8 TPI -> 3.175 mm pitch
starts        = 1;           // 400 = single-start
thread_len    = cap_h - top_th;   // run thread through the height
leadin_len    = 0.6*pitch;   // modest entry chamfer; set 0 for none

// Render quality
$fn = 180;

// Internal-thread major diameter at the crests (what the bottle’s thread “sees”).
D_maj_int = T_nom + dia_clear;

// -----------------------------
// Model
// -----------------------------
difference() {
  // Outer body (simple ring)
  cylinder(d=cap_od, h=cap_h);

  // Subtract a solid internal thread using BOSL2.
  // Produces a 60° ISO V thread with internal relief.
  translate([0,0,top_th])
    thread_helix(
      d        = D_maj_int,        // internal major (crest) diameter
      pitch    = pitch,
      length   = thread_len + 0.1, // slight overlength for clean cut
      starts   = starts,
      profile  = "iso",            // 60° V ISO profile
      internal = true,             // internal clearances
      leadin   = leadin_len,       // entry bevel
      leadout  = 0,
      rounded  = true              // rounded truncations
    );
}