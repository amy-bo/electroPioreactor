// BOSL2 GPI 24-400 internal thread cap (test ring)
// Requires BOSL2 in your OpenSCAD libraries path:
//   https://github.com/BelfrySCAD/BOSL2
// If your path differs, adjust the `use <...>` lines.

include <BOSL2/std.scad>
include <BOSL2/threading.scad>

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
helix_turns   = thread_len / pitch;   // BOSL2 thread_helix expects 'turns' in this version
leadin_len    = 0.6*pitch;   // modest entry chamfer; set 0 for none

// Render quality
$fn = 180;

// Internal-thread major diameter at the crests (what the bottle’s thread “sees”).
D_maj_int = T_nom + dia_clear;

// ISO V-thread geometry for internal thread using BOSL2 thread_helix trapezoid
depth_rad    = 0.541265 * pitch;           // radial thread depth (ISO V) = 5/8 * H = 0.541265*P
D_minor_int  = D_maj_int - 2*depth_rad;    // base (inner) diameter for internal threads

// -----------------------------
// Model
// -----------------------------
difference() {
  // Outer body (simple ring)
  cylinder(d=cap_od, h=cap_h);

  // Core bore: leave stock for the thread between bore and minor diameter
  // If we bore out to D_minor_int, the helix has nothing to cut. Keep ~0.6 mm diametral stock.
  bore_d = D_minor_int - 0.60;   // adjust 0.4–0.8 to tune how much land remains
  translate([0,0,top_th-0.1])
    cylinder(d=bore_d, h=thread_len+0.2);

  // Subtract a solid internal thread using BOSL2.
  // Produces a 60° ISO V thread with internal relief.
  translate([0,0,top_th])
    thread_helix(
      d            = D_minor_int,     // base (inner) diameter for internal thread
      pitch        = pitch,
      turns        = helix_turns,
      thread_depth = depth_rad,       // RADIAL thread depth (ISO V)
      flank_angle  = 30,              // 60° included
      starts       = starts,
      internal     = true
    );
}