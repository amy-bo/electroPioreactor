// =====================================================================
// CONCEPT v2 - electrode holder, redesigned for ZERO-DOF + SUPPORT-FREE
// =====================================================================
// Three printed/sheet parts:
//   CAP     (blue)   - seals vial, carries ports, prints closed-top-DOWN
//   SEPTUM  (purple) - silicone sheet, seals everything, grips nothing
//   COLUMN  (orange) - solid racetrack, holds electrodes rigid + sets depth
//
// Why it is support-free (print orientations shown in view="print"):
//   CAP    : printed closed-top on the bed, mouth up. Every feature is a
//            vertical hole or an upward-opening cavity. No overhang.
//   COLUMN : printed flush-face on the bed, pegs pointing up. Bores are
//            vertical; the only horizontal features (M3 clamp) are a
//            teardrop hole + a vertex-up hex nut trap = self-supporting.
//
// Why the electrodes get ZERO degrees of freedom:
//   - the long vertical bore in the solid COLUMN is a journal bearing:
//     it pins X-Y AND kills both tilts over its whole length
//   - two PEGS lock the COLUMN to the CAP (X-Y + rotation), so that
//     bearing is referenced to the cap/vial, not floating
//   - the M3 clamp pushes the wire onto the electrode = electrical
//     contact AND kills the last DOF (axial slide + spin)
//
//   view       : "exploded" | "assembled" | "section" | "print"
//   port_style : "ports" (6x3.2mm ring) | "open" (max septum field)
// =====================================================================
view       = "exploded";
port_style = "ports";

$fn = 56;
eps = 0.05;

// ---- electrodes ----
el_d   = 6;     // electrode diameter
el_len = 60;    // electrode length  (L)
el_off = 4.8;   // offset from axis to each electrode
g      = 23;    // protrusion below cap bottom into the vial (insertion depth)

// ---- cap ----
cap_od = 27;    // outer diameter
cap_h  = 12;    // height
top_th = 2.5;   // closed-top thickness
wall   = 2;     // side wall
flat_d = 2.2;   // poka-yoke flat depth on the OD

// ---- septum ----
sept_t = 2;     // silicone sheet thickness

// ---- column / clamp ----
clear   = 0.3;  // print clearance
col_endr= el_d/2 + 2.8;     // racetrack end radius
peg_d   = 3;                // registration peg diameter
peg_h   = 4;                // peg length
peg_off = 4;                // pegs on the y-axis (clear of bores, flat and ports)
m3_bolt = 3.2;              // M3 clearance
nut_af  = 5.8;              // M3 nut across-flats (+clearance)
nut_t   = 2.6;              // nut thickness

// ---- ports ----
port_d = 3.2;
port_r = 10;
port_angles = [60, 90, 120, 240, 270, 300];   // all clear of the column footprint

// ---- derived ----
col_h  = el_len - g - cap_h;          // column height (sets depth) = 25
H_top  = cap_h + col_h;               // electrode flush face = el_len - g
sept_d = cap_od - 2*wall - 0.6;
sept_z = cap_h - top_th - sept_t;     // septum seat (against closed-top underside)

C_CAP   = [0.78,0.87,0.97];
C_SEPT  = [0.74,0.62,0.92];
C_CARR  = [1.00,0.83,0.58];
C_STEEL = [0.72,0.74,0.78];
C_VIAL  = [0.55,0.88,0.78,0.32];

// ============ helpers =================================================
module racetrack(h, r)
  hull() for (s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r, h=h);

// teardrop hole, axis = +X, apex toward -Z (so it self-supports when the
// part is printed flush-face-down, i.e. -Z is the build-up direction)
module teardrop_x(d, len) {
  r = d/2;
  hull() {
    rotate([0,90,0]) cylinder(r=r, h=len);
    translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01, h=len, $fn=6);
  }
}
// hex pocket, axis = +X, vertices at +/-Z (self-supporting roof)
module hexhole_x(af, len)
  rotate([0,90,0]) cylinder(d=af/cos(30), h=len, $fn=6);

// ============ parts ===================================================
module cap() color(C_CAP) difference() {
  // body with the poka-yoke flat on +x
  difference() {
    cylinder(d=cap_od, h=cap_h);
    translate([cap_od/2-flat_d, -cap_od, -eps]) cube([cap_od, 2*cap_od, cap_h+2*eps]);
  }
  // interior cavity (thread + septum live here) - opens at the mouth (z=0)
  translate([0,0,-eps]) cylinder(d=cap_od-2*wall, h=cap_h-top_th+eps);
  // electrode clearance holes (cap only guides loosely; column does the holding)
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d+clear+0.6, h=cap_h+2*eps);
  // peg registration holes
  for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+clear, h=top_th+2*eps);
  // ports OR open septum field
  if (port_style == "ports")
    for (a=port_angles) rotate([0,0,a]) translate([port_r,0,-eps]) cylinder(d=port_d, h=cap_h+2*eps);
  else
    for (s=[-1,1]) translate([0, s*8, -eps]) scale([1.7,1,1]) cylinder(d=8.5, h=cap_h+2*eps);
}

module septum() color(C_SEPT)
  translate([0,0,sept_z])
  difference() {
    cylinder(d=sept_d, h=sept_t, $fn=72);
    for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d-0.4, h=sept_t+2*eps);  // pre-pierced for electrodes
  }

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, col_endr);          // solid fused column
    for (s=[-1,1]) translate([0,s*peg_off,cap_h-peg_h]) cylinder(d=peg_d, h=peg_h+eps);  // pegs
  }
  // long journal bearings (the rigidity) - vertical through-bores
  for (s=[-1,1]) translate([s*el_off,0,cap_h-eps]) cylinder(d=el_d+clear, h=col_h+2*eps);
  // wire channel: vertical slot on the bolt side of each electrode, open to the top
  zc = cap_h + col_h/2;
  for (s=[-1,1])
    translate([s*(el_off+el_d/2+0.3)-0.8, -0.9, zc]) cube([1.6, 1.8, col_h]);
  // M3 clamp: teardrop bolt hole + vertex-up hex nut trap, from each end
  for (m=[0,1]) mirror([m,0,0]) {
    end_x = -(el_off+col_endr);
    translate([end_x-eps, 0, zc]) teardrop_x(m3_bolt, col_endr+el_d/2+1.4);   // bolt -> electrode
    translate([end_x-eps, 0, zc]) hexhole_x(nut_af, nut_t+eps);               // captive nut
  }
}

module vial() color(C_VIAL)
  translate([0,0,-38]) cylinder(d=cap_od-2*wall-1.2, h=38+sept_z+eps);

// ============ assembly / views ========================================
e      = (view=="exploded") ? 1 : 0;
z_vial = -e*38;
z_sept = -e*17;
z_cap  =  0;
z_elec =  e*18;
z_col  =  e*42;

module electrodes() color(C_STEEL)
  for (s=[-1,1]) translate([s*el_off,0,H_top-el_len]) cylinder(d=el_d, h=el_len);

module assembly() {
  translate([0,0,z_vial]) vial();
  translate([0,0,z_sept]) septum();
  translate([0,0,z_cap])  cap();
  translate([0,0,z_elec]) electrodes();
  translate([0,0,z_col])  column();
}

if (view == "section")
  difference() { assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view == "print") {
  // each printed part laid in its real print orientation on the bed (z=0)
  translate([-18,0,cap_h])       rotate([180,0,0]) cap();      // closed-top on bed
  translate([ 18,0,cap_h+col_h]) rotate([180,0,0]) column();   // flush-face on bed, pegs up
}
else
  assembly();
