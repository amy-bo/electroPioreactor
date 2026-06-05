// =====================================================================
// CONCEPT v3 - fixes from review: real poka-yoke tab, port radius taken
// from the current Vial Cap.scad (inside the vial neck), and a CORRECT
// captive-nut clamp. Primitives only, so the render is predictable.
// The production cap should be the real Vial Cap.scad + these changes
// (see vial-cap-redesign.scad); this file is the visual concept.
//
//   view       : "exploded" | "assembled" | "section" | "print"
//   port_style : "ports" (6x3.2 ring, r=7.785 as current) | "open"
// =====================================================================
view       = "exploded";
port_style = "ports";

$fn = 56;
eps = 0.05;

// electrodes
el_d=6; el_len=60; el_off=4.8; g=23;
// cap
cap_od=27; cap_h=12; top_th=2.5; wall=2;
// septum
sept_t=2;
// registration + clamp
clear=0.3;
bearing_r = el_d/2 + 1.8;            // slim journal sleeve wall
peg_d=3; peg_h=4; peg_off=4;         // pegs on the y-axis
m3_bolt=3.4;                         // M3 clearance
nut_af=5.7; nut_t=2.7;               // M3 nut across-flats / thickness (+clearance)
nut_ac = nut_af/cos(30);
t_inner=2.2; t_outer=2.6;            // robust PC-CF clamp walls (Grace-proof)
// ports (matching current Vial Cap.scad: r = (cap_o_ring_id - port_dia)/2)
port_d=3.2; port_r=(18.7706-3.2)/2;  // = 7.785
port_angles=[60,90,120,240,270,300];

col_h = el_len - g - cap_h;          // sets insertion depth
H_top = cap_h + col_h;

// clamp geometry along +x (mirrored for -x)
xe     = el_off + (el_d+clear)/2;    // electrode bore outer edge = 7.95
x_nut0 = xe + t_inner;               // inner wall ends
x_nut1 = x_nut0 + nut_t;             // nut pocket ends
x_out  = x_nut1 + t_outer;           // outer face (bolt head bears here)
ear_h  = 8;
zc     = cap_h + col_h/2;            // clamp height
sept_z = cap_h - top_th - sept_t;
sept_d = cap_od - 2*wall - 0.4;

C_CAP=[0.78,0.87,0.97]; C_SEPT=[0.74,0.62,0.92]; C_CARR=[1,0.83,0.58];
C_STEEL=[0.72,0.74,0.78]; C_VIAL=[0.55,0.88,0.78,0.32];

module racetrack(h,r) hull() for(s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r,h=h);
// teardrop hole, axis +X, apex toward -Z (printable; column prints flush-face down)
module teardrop_x(d,len){ r=d/2; hull(){ rotate([0,90,0]) cylinder(r=r,h=len);
  translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01,h=len,$fn=6);} }

module cap() color(C_CAP) difference() {
  union() {
    cylinder(d=cap_od, h=cap_h);
    translate([0,-(cap_od/2-1),0]) cylinder(d=8, h=cap_h);   // poka-yoke tab (additive lobe, -Y)
  }
  translate([0,0,-eps]) cylinder(d=cap_od-2*wall, h=cap_h-top_th+eps);          // cavity (mouth up when printed)
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d+clear+0.6, h=cap_h+2*eps); // electrode clearance
  for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+clear, h=top_th+2*eps); // peg holes
  if (port_style=="ports")
    for (a=port_angles) rotate([0,0,a]) translate([port_r,0,-eps]) cylinder(d=port_d, h=cap_h+2*eps);
  else
    for (s=[-1,1]) translate([0,s*6.5,-eps]) scale([1.7,1,1]) cylinder(d=7, h=cap_h+2*eps);
}

module septum() color(C_SEPT) translate([0,0,sept_z]) difference() {
  cylinder(d=sept_d, h=sept_t, $fn=72);
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d-0.4, h=sept_t+2*eps);
}

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, bearing_r);                 // slim journal column
    for (m=[0,1]) mirror([m,0,0])                                       // clamp ears
      translate([(xe+x_out)/2, 0, zc]) cube([x_out-xe, nut_af+3.2, ear_h], center=true);
    for (s=[-1,1]) translate([0,s*peg_off,cap_h-peg_h]) cylinder(d=peg_d, h=peg_h+eps); // pegs
  }
  for (s=[-1,1]) translate([s*el_off,0,cap_h-eps]) cylinder(d=el_d+clear, h=col_h+2*eps); // bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from outer face in to the electrode (pinches wire on electrode)
    translate([el_off+el_d/2-0.4, 0, zc]) teardrop_x(m3_bolt, x_out-(el_off+el_d/2)+0.9);
    // captive nut: drops in from the top; width = across-flats => can't rotate;
    // inner + outer walls keep it from escaping along the bolt
    translate([x_nut0, -nut_af/2, zc-nut_ac/2]) cube([nut_t, nut_af, H_top-(zc-nut_ac/2)+eps]);
    // wire guide slot, top down to the bolt, just outboard of the electrode
    translate([el_off+el_d/2-0.4, -0.9, zc]) cube([1.5,1.8,H_top-zc+eps]);
  }
}

module vial() color(C_VIAL) translate([0,0,-38]) cylinder(d=cap_od-2*wall-1.2, h=38+sept_z+eps);
module electrodes() color(C_STEEL) for(s=[-1,1]) translate([s*el_off,0,H_top-el_len]) cylinder(d=el_d,h=el_len);

e=(view=="exploded")?1:0;
module assembly() {
  translate([0,0,-e*38]) vial();
  translate([0,0,-e*17]) septum();
  cap();
  translate([0,0,e*18]) electrodes();
  translate([0,0,e*42]) column();
}

if (view=="section")
  difference(){ assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view=="print") {
  translate([-18,0,cap_h])        rotate([180,0,0]) cap();      // closed-top on bed
  translate([ 20,0,cap_h+col_h])  rotate([180,0,0]) column();   // flush-face on bed, pegs up
}
else assembly();
