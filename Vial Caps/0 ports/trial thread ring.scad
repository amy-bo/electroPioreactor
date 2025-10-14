// BOSL2 GPI 24-400 internal thread cap (test ring)
// Requires BOSL2 in OpenSCAD libraries path:
//   https://github.com/BelfrySCAD/BOSL2

include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// -----------------------------
// Cap & thread parameters
// -----------------------------
// Input parameters
cap_od = 27; // mm (outer diameter of ring/cap)
cap_h = 8; // mm (overall height)
top_th = 0; // mm (flat top thickness; 0 = open ring)
$fn = 180; // render quality - facets for smoothness

// Derived parameters
bore_len = cap_h - top_th; // mm (length of bore; usually same as cap_h - top_th)

// GPI 24-400 basics
T_nom = 24.10; // "T" dimension (outside dia over threads)
dia_clear = 0.30; // diametral print clearance (tune 0.20–0.50)
pitch = 25.4/8; // 8 TPI -> 3.175 mm pitch
starts = 1; // 400 = single-start
thread_len = bore_len - pitch; // run thread through the height
helix_turns = thread_len / pitch; // BOSL2 thread_helix expects 'turns' in this version
leadin_len = 0.6*pitch; // modest entry chamfer; set 0 for none


// Internal-thread major diameter at the crests (what the bottle’s thread “sees”).
D_maj_int = T_nom + dia_clear;

// ISO V-thread geometry for internal thread using BOSL2 thread_helix trapezoid
depth_rad = 0.541265 * pitch; // radial thread depth (ISO V) = 5/8 * H = 0.541265*P
D_minor_int = D_maj_int - 2*depth_rad; // base (inner) diameter for internal threads

// -----------------------------
// Model
// -----------------------------
difference() {
  // *** 
  // Cap
  // ***
  union() {
    difference() {
      // Cap body
      cylinder(d=cap_od, h=cap_h);

      // Core bore
      translate([0,0,top_th])
        cylinder(d=T_nom, h=bore_len);
    }
    
    // Internal thread (using BOSL2)
    translate([0,0,top_th + pitch/2]) // start half pitch down
      thread_helix(
        d = D_minor_int, // base (inner) diameter for internal thread
        pitch = pitch,
        turns = helix_turns,
        thread_depth = depth_rad, // RADIAL thread depth (ISO V)
        flank_angle = 30, // 60° included
        starts = starts,
        anchor = BOTTOM, // start helix at z=0 (bottom) rather than centered
        lead_in = leadin_len, // length of lead-in chamfer; 0 for none
        internal = true
      );
  }
  // ***
  // Ports
  // ***
}