// =====================================================================
// electroPioreactor - vial cap + electrode holder (single source file)
// Iterations are tracked in git, not as v2/v3 files.
//
// Parts:  CAP (seals + ports + GPI thread)  •  SEPTUM (silicone, seals only)
//         COLUMN / top stop (holds electrodes, sets depth, clamps the wires)
//
// PRINT ORIENTATIONS (both support-free - see view="print"):
//   CAP    : closed-top on the bed, mouth up.  Build dir = up toward mouth.
//   COLUMN : flush face on the bed, pegs up.    Build dir = up toward pegs.
// In the COLUMN model, "up" (+Z) is the bed side, so the clamp sits at the
// top face (lands ON the bed) and its nut pocket opens downward-in-use
// (= upward-in-print -> no bridge, no supports).
//
// Requires BOSL2 (same as the current Vial Cap.scad).
// =====================================================================
include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// ---- options (choices listed inline) --------------------------------
view       = "exploded";   // "exploded" | "assembled" | "section" | "print"
part       = "all";        // "all" | "cap" | "column" | "septum"
port_style = "ports";      // "ports" | "open"

$fn = 72;
eps = 0.05;

// ---- electrodes -----------------------------------------------------
el_d            = 6;       // electrode diameter
el_len          = 60;      // electrode length (L)
el_off          = 4.8;     // offset from axis to each electrode
insertion_depth = 23;      // g: protrusion below the cap bottom into the vial

// ---- fits (point 8) -------------------------------------------------
cap_fit      = 0.15;       // friction fit in the CAP (snug - holds electrode by friction)
insert_extra = 0.30;       // EXTRA clearance in the COLUMN for easy insertion (bolts do the holding)
cap_bore = el_d + cap_fit;                 // friction bore (also the lower bearing)
col_bore = el_d + cap_fit + insert_extra;  // easy-insert bore; total tracks cap_fit

// ---- cap ------------------------------------------------------------
cap_od = 27; cap_h = 12.3; top_th = 2.5; wall_t = 2;
ribs   = 84; rib_d = 0.856;
// GPI 24-400 thread (verbatim from Components/Vial Cap/Vial Cap.scad)
T_nom = 24.30; dia_clear = 0.50; pitch = 25.4/8; starts = 1; leadin_len = 0.6*pitch;
D_maj_int = T_nom + dia_clear; depth_rad = 0.3*pitch; D_minor_int = D_maj_int - 2*depth_rad;
// septum + retaining ridge (point 9)
sept_t = 2.0; sept_d = 23.9; sept_seat_d = 24.2;
ridge_id = 22.5; ridge_h = 1.6;            // inward lip that keeps the septum from dropping out
// ports
cap_o_ring_id = 18.7706; port_d = 3.2; port_R = (cap_o_ring_id - port_d)/2;  // 7.785, in the neck
port_angles = [60,90,120,240,270,300];
// open septum field
spine_hw = 5; R_open = cap_od/2 - wall_t - 1.5; win_round = 1.6;
// poka-yoke tab (constant-radius plateau read off vial-cap-s.3mf)
tab_R = 17; tab_halfangle = 26; tab_round = 2.5;

// ---- registration pegs ---------------------------------------------
peg_d = 3; peg_off = 3; peg_clear = 0.3; peg_h = top_th;   // flush with the cap inside ceiling

// ---- column + clamp -------------------------------------------------
bearing_r = el_d/2 + 1.8;
m3_bolt   = 3.4; nut_af = 5.7; nut_th = 2.6; nut_ac = nut_af/cos(30);
clamp_in  = 1.8; clamp_out = 2.2;          // robust PC-CF walls (Grace-proof)

col_h  = el_len - insertion_depth - cap_h; // sets the insertion depth
H_top  = cap_h + col_h;                     // electrode flush face
xe     = el_off + col_bore/2;               // bore outer edge
x_nut0 = xe + clamp_in; x_nut1 = x_nut0 + nut_th; x_out = x_nut1 + clamp_out;
ear_h  = 8; ear_hw = nut_af/2 + 1.6;
zc     = H_top - 4;                         // bolt axis, near the top face
sept_z = cap_h - top_th - sept_t;

C_CAP=[0.78,0.87,0.97]; C_SEPT=[0.74,0.62,0.92]; C_CARR=[1,0.83,0.58];
C_STEEL=[0.72,0.74,0.78]; C_VIAL=[0.55,0.88,0.78,0.32];

// ---- helpers --------------------------------------------------------
module racetrack(h,r) hull() for(s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r,h=h);

module body2d() offset(r=tab_round) offset(r=-tab_round) union() {   // cap outline + filleted tab
  circle(d=cap_od, $fn=160);
  rotate(-90) intersection() {
    circle(r=tab_R, $fn=160);
    polygon([[0,0],[tab_R*1.6*cos(-tab_halfangle),tab_R*1.6*sin(-tab_halfangle)],
             [tab_R*1.6,0],[tab_R*1.6*cos(tab_halfangle),tab_R*1.6*sin(tab_halfangle)]]);
  }
}

// teardrop hole, axis +X, apex toward -Z (= up in print -> self-supporting)
module teardrop_x(d,len){ r=d/2; hull(){ rotate([0,90,0]) cylinder(r=r,h=len);
  translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01,h=len,$fn=6);} }

// septum retaining ridge: triangular barb (both faces <=45deg from vertical)
module septum_ridge() rotate_extrude($fn=140)
  polygon([[sept_seat_d/2, sept_z+0.05],
           [ridge_id/2,    sept_z-ridge_h/2],
           [sept_seat_d/2, sept_z-ridge_h]]);

// clamp ear: flat (flush) inner edge, rounded outer end - no rounding on the body join
module ear2d() hull(){
  translate([x_out-ear_hw,0]) circle(r=ear_hw,$fn=48);
  translate([xe,-ear_hw]) square([0.1, 2*ear_hw]);
}

// ---- parts ----------------------------------------------------------
module cap() color(C_CAP) difference() {
  union() {
    difference() {                                   // body (with knurl) minus the core bore
      union() {
        linear_extrude(cap_h) body2d();
        if (ribs>0) for (i=[0:ribs-1]) rotate([0,0,i*360/ribs]) translate([cap_od/2,0,0]) cylinder(d=rib_d,h=cap_h);
      }
      translate([0,0,-eps]) cylinder(d=T_nom, h=cap_h-top_th-sept_t+eps);
    }
    // internal GPI thread (added back inside the bore)
    translate([0,0,pitch/2])
      thread_helix(d=D_minor_int, pitch=pitch, turns=(cap_h-top_th-sept_t-pitch)/pitch,
                   thread_depth=depth_rad, flank_angle=30, starts=starts,
                   anchor=BOTTOM, lead_in=leadin_len, internal=true);
    septum_ridge();                                  // lip that retains the septum
  }
  // smooth septum seat under the closed top
  translate([0,0,sept_z]) cylinder(d=sept_seat_d, h=sept_t+eps);
  // electrode friction bore
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=cap_bore, h=cap_h+2*eps);
  // peg holes (through the closed top only)
  for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+peg_clear, h=top_th+2*eps);
  // ports OR an open septum field (full-width spine, rounded window corners)
  if (port_style=="ports")
    for (a=port_angles) rotate([0,0,a]) translate([port_R,0,-eps]) cylinder(d=port_d, h=cap_h+2*eps);
  else
    translate([0,0,cap_h-top_th-eps]) linear_extrude(top_th+2*eps)
      offset(r=-win_round) offset(r=win_round) difference() {
        circle(r=R_open, $fn=140);
        square([2*cap_od, 2*spine_hw], center=true);   // spine spans the full width
      }
}

module septum() color(C_SEPT) translate([0,0,sept_z]) difference() {
  cylinder(d=sept_d, h=sept_t, $fn=96);
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d-0.4, h=sept_t+2*eps);
}

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, bearing_r);
    translate([0,0,H_top-ear_h]) linear_extrude(ear_h) { ear2d(); mirror([1,0,0]) ear2d(); }
    for (s=[-1,1]) translate([0,s*peg_off,cap_h]) rotate([180,0,0]) cylinder(d=peg_d, h=peg_h);
  }
  for (s=[-1,1]) translate([s*el_off,0,cap_h-eps]) cylinder(d=col_bore, h=col_h+2*eps);  // journal bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from the outer face in to pinch the wire on the electrode
    translate([el_off+el_d/2-0.4, 0, zc]) teardrop_x(m3_bolt, x_out-(el_off+el_d/2)+0.9);
    // captive nut: pocket opens at the ear BOTTOM (down-in-use = up-in-print, no bridge);
    // width = across-flats so it can't rotate; inner+outer walls trap it along the bolt
    translate([x_nut0, -nut_af/2, H_top-ear_h-eps]) cube([nut_th, nut_af, (zc+nut_ac/2)-(H_top-ear_h)+eps]);
    // wire guide slot, top face down to the bolt
    translate([el_off+el_d/2-0.4, -0.9, zc]) cube([1.5,1.8, H_top-zc+eps]);
  }
}

module vial() color(C_VIAL) translate([0,0,-38]) cylinder(d=cap_od-2*wall_t-1.2, h=38+sept_z+eps);
module electrodes() color(C_STEEL) for(s=[-1,1]) translate([s*el_off,0,H_top-el_len]) cylinder(d=el_d,h=el_len);

// ---- assembly / views ----------------------------------------------
e = (view=="exploded") ? 1 : 0;
module assembly() {
  translate([0,0,-e*38]) vial();
  translate([0,0,-e*17]) septum();
  cap();
  translate([0,0,e*18]) electrodes();
  translate([0,0,e*42]) column();
}

if (part=="cap") cap();
else if (part=="column") translate([0,0,-cap_h]) column();
else if (part=="septum") translate([0,0,-sept_z]) septum();
else if (view=="section") difference(){ assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view=="print") {
  translate([-18,0,cap_h]) rotate([180,0,0]) cap();      // closed-top on bed
  translate([ 20,0,H_top]) rotate([180,0,0]) column();   // flush-face on bed, pegs up
} else assembly();
