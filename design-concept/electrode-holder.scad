// =====================================================================
// electroPioreactor - vial cap + electrode holder (single source file)
// Iterations are tracked in git, not as v2/v3 files. Only the genuine
// option (port style) is a parameter, not a separate file.
//
// Parts:  CAP (seals + ports)  •  SEPTUM (silicone, seals only)
//         COLUMN (holds electrodes rigid, sets depth, clamps the wires)
//
// Zero-DOF: a long vertical bore in the solid COLUMN is a journal bearing
// (kills tilt + lateral); two pegs lock the column to the cap so that
// bearing is referenced to the vessel; the M3 clamp kills axial + spin.
// Support-free: cap prints closed-top-down; column prints flush-face-down
// with conical pegs up, teardrop bolt holes, and a top-opening nut pocket.
//
// NOTE: the cap bore here is a plain cylinder for fast, predictable
// rendering. PRODUCTION: replace it with the GPI 24-400 BOSL2 thread block
// from Components/Vial Cap/Vial Cap.scad (unchanged) - marked below.
// =====================================================================

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
fit_clear       = 0.3;     // ONE electrode fit - used by BOTH cap and column
bore_d          = el_d + fit_clear;   // 6.3, identical snug fit in both parts

// ---- cap ------------------------------------------------------------
cap_od  = 27; cap_h = 12.3; top_th = 2.5; wall_t = 2;
ribs    = 84; rib_d = 0.856;
// septum
sept_t  = 2.0; sept_d = 23.9; sept_seat_d = sept_d + 0.3;
// ports (radius taken from the current cap: (cap_o_ring_id - port_d)/2)
cap_o_ring_id = 18.7706; port_d = 3.2; port_R = (cap_o_ring_id - port_d)/2;  // 7.785
port_angles = [60,90,120,240,270,300];
// poka-yoke tab (constant-radius plateau read off vial-cap-s.3mf)
tab_R = 17; tab_halfangle = 26; tab_round = 2.5;

// ---- registration pegs ---------------------------------------------
peg_d = 3; peg_off = 3; peg_h = 4; peg_clear = 0.3; peg_cone = 1.4;

// ---- column + clamp -------------------------------------------------
bearing_r = el_d/2 + 1.8;          // slim journal sleeve
m3_bolt   = 3.4;                   // M3 clearance
nut_af    = 5.7; nut_th = 2.6;     // M3 nut across-flats / thickness (+clearance)
nut_ac    = nut_af/cos(30);
clamp_in  = 1.8; clamp_out = 2.2;  // robust PC-CF walls (Grace-proof)

col_h  = el_len - insertion_depth - cap_h;   // sets the insertion depth
H_top  = cap_h + col_h;                       // electrode flush face
xe     = el_off + bore_d/2;                   // electrode bore outer edge
x_nut0 = xe + clamp_in;                        // inner wall ends
x_nut1 = x_nut0 + nut_th;                       // nut pocket ends
x_out  = x_nut1 + clamp_out;                    // outer face (bolt head bears here)
zc     = H_top - 4.5;                           // bolt axis, near the top
ear_h  = 8;
sept_z = cap_h - top_th - sept_t;

C_CAP=[0.78,0.87,0.97]; C_SEPT=[0.74,0.62,0.92]; C_CARR=[1,0.83,0.58];
C_STEEL=[0.72,0.74,0.78]; C_VIAL=[0.55,0.88,0.78,0.32];

// ---- helpers --------------------------------------------------------
module racetrack(h,r) hull() for(s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r,h=h);

// cap outline with the poka-yoke tab, cusps filleted away
module body2d() offset(r=tab_round) offset(r=-tab_round) union() {
  circle(d=cap_od, $fn=160);
  rotate(-90)                                       // tab points -Y
    intersection() {
      circle(r=tab_R, $fn=160);
      polygon([[0,0],
               [tab_R*1.6*cos(-tab_halfangle), tab_R*1.6*sin(-tab_halfangle)],
               [tab_R*1.6, 0],
               [tab_R*1.6*cos(tab_halfangle),  tab_R*1.6*sin(tab_halfangle)]]);
    }
}

// teardrop hole, axis +X, apex toward -Z (printable; column prints top-down)
module teardrop_x(d,len){ r=d/2; hull(){ rotate([0,90,0]) cylinder(r=r,h=len);
  translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01,h=len,$fn=6);} }

// peg with a conical lead-in tip (self-supporting when printed point-up)
module peg(){ cylinder(d=peg_d,h=peg_h); translate([0,0,peg_h]) cylinder(d1=peg_d,d2=0.6,h=peg_cone); }

// rounded clamp ear (footprint corners filleted - no boxy appendage)
module ear2d() translate([(xe+x_out)/2,0]) offset(r=2) offset(r=-2)
  square([x_out-xe, nut_af+2*1.6], center=true);

// ---- parts ----------------------------------------------------------
module cap() color(C_CAP) difference() {
  union() {
    linear_extrude(cap_h) body2d();
    if (ribs>0) for (i=[0:ribs-1]) rotate([0,0,i*360/ribs]) translate([cap_od/2,0,0]) cylinder(d=rib_d,h=cap_h);
  }
  // ***** PRODUCTION: replace this plain bore with the GPI 24-400 BOSL2 thread *****
  translate([0,0,-eps]) cylinder(d=cap_od-2*wall_t, h=cap_h-top_th+eps);
  // septum seat (smooth counterbore under the closed top)
  translate([0,0,sept_z]) cylinder(d=sept_seat_d, h=sept_t+eps);
  // electrode clearance (same fit as the column bore)
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=bore_d, h=cap_h+2*eps);
  // peg registration holes through the closed top
  for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+peg_clear, h=top_th+2*eps);
  // ports OR an open septum field
  if (port_style=="ports")
    for (a=port_angles) rotate([0,0,a]) translate([port_R,0,-eps]) cylinder(d=port_d, h=cap_h+2*eps);
  else
    translate([0,0,cap_h-top_th-eps]) linear_extrude(top_th+2*eps) difference() {
      circle(r=cap_od/2-wall_t-1.5, $fn=140);        // openable area inside the rim
      square([2*9.3, 2*5], center=true);             // keep an x-spine (holds electrodes + pegs)
    }
}

module septum() color(C_SEPT) translate([0,0,sept_z]) difference() {
  cylinder(d=sept_d, h=sept_t, $fn=96);
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d-0.4, h=sept_t+2*eps);
}

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, bearing_r);              // slim journal column
    translate([0,0,zc-ear_h/2]) linear_extrude(ear_h) { ear2d(); mirror([1,0,0]) ear2d(); }
    for (s=[-1,1]) translate([0,s*peg_off,cap_h]) rotate([180,0,0]) peg();   // conical pegs, pointing down
  }
  for (s=[-1,1]) translate([s*el_off,0,cap_h-eps]) cylinder(d=bore_d, h=col_h+2*eps);  // journal bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from outer face in to pinch the wire on the electrode
    translate([el_off+el_d/2-0.4, 0, zc]) teardrop_x(m3_bolt, x_out-(el_off+el_d/2)+0.9);
    // captive nut: drops in from the TOP (open pocket, no bridge); width = across-flats so it can't rotate;
    // inner + outer walls stop it escaping along the bolt
    translate([x_nut0, -nut_af/2, zc-nut_ac/2]) cube([nut_th, nut_af, H_top-(zc-nut_ac/2)+eps]);
    // wire guide slot, top down to the bolt
    translate([el_off+el_d/2-0.4, -0.9, zc]) cube([1.5,1.8,H_top-zc+eps]);
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
  translate([-18,0,cap_h])       rotate([180,0,0]) cap();      // closed-top on bed
  translate([ 20,0,cap_h+col_h]) rotate([180,0,0]) column();   // flush-face on bed, conical pegs up
} else assembly();
