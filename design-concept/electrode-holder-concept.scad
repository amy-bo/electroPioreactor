// =====================================================================
// CONCEPT ONLY - electrode holder constraint scheme (NOT the final part)
// Purpose: let you SEE how the electrodes get zero DOF and how it stacks.
// Built from simple primitives only, so the render is predictable.
// Threads, poka-yoke detail, real tolerances come later in the real part.
//
//   view = "exploded"  -> parts pulled apart in assembly order
//   view = "assembled" -> everything seated
//   view = "section"   -> assembled, cut through both electrode centres
// =====================================================================
view = "exploded";

$fn = 48;
eps = 0.05;

// ---- key dimensions (schematic, roughly to scale) ----
el_d    = 6;      // electrode diameter
el_len  = 60;     // electrode length (L)
el_off  = 4.8;    // electrode centre offset from axis
g       = 23;     // protrusion below cap bottom into vial (insertion depth)

cap_od  = 27;     // cap outer diameter
cap_h   = 12;     // cap height
top_th  = 2.5;    // closed-top thickness
wall    = 2;      // cap side wall

boss_h    = 5;    // registration boss height (sticks up from cap top)
boss_wall = 1.6;  // wall around electrode at the boss
sept_t    = 2;    // septum thickness
ts_h      = 10;   // top-stop height
clear     = 0.3;  // bearing clearance (visual)

// ---- derived ----
boss_od   = el_d + 2*boss_wall;          // 9.2
collar_id = boss_od + clear;             // carriage slips over boss
end_r     = el_d/2 + 4;                  // racetrack end radius (7)
H_top     = el_len - g;                  // top-stop top face = electrode flush (37)
post_bot  = cap_h;                       // carriage sits on cap top
post_top  = H_top - ts_h;                // underside of top stop
sept_z    = cap_h - top_th - sept_t;     // septum seat height (7.5)

// ---- colours ----
C_STEEL = [0.72,0.74,0.78];
C_CAP   = [0.81,0.89,0.97];
C_SEPT  = [0.78,0.66,0.92];
C_CARR  = [1.00,0.85,0.62];
C_VIAL  = [0.55,0.88,0.78,0.35];

// ---- explode offsets (0 when not exploded) ----
e        = (view == "exploded") ? 1 : 0;
z_vial   = -e*18;
z_cap    =  0;
z_sept   =  e*10;
z_elec   =  e*34;
z_carr   =  e*62;

// racetrack: hull of two cylinders at the electrode centres
module racetrack(h, r) {
  hull() for (s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r, h=h);
}

// ---------------------------------------------------------------
module electrodes() {
  color(C_STEEL)
  for (s=[-1,1])
    translate([s*el_off, 0, H_top - el_len])
      cylinder(d=el_d, h=el_len);
}

// ---------------------------------------------------------------
module cap() {
  color(C_CAP)
  difference() {
    union() {
      cylinder(d=cap_od, h=cap_h);                       // body
      for (s=[-1,1])                                     // registration bosses
        translate([s*el_off,0,cap_h]) cylinder(d=boss_od, h=boss_h);
    }
    // internal cavity (where the thread + septum live)
    translate([0,0,-eps])
      cylinder(d=cap_od-2*wall, h=cap_h-top_th+eps);
    // electrode guide bores = BEARING 1 (through closed top + bosses)
    for (s=[-1,1])
      translate([s*el_off,0,-eps]) cylinder(d=el_d+clear, h=cap_h+boss_h+2*eps);
  }
}

// ---------------------------------------------------------------
module septum() {
  color(C_SEPT)
  translate([0,0,sept_z])
  difference() {
    cylinder(d=cap_od-2*wall-0.4, h=sept_t);
    for (s=[-1,1])
      translate([s*el_off,0,-eps]) cylinder(d=el_d-0.5, h=sept_t+2*eps); // pierced holes
  }
}

// ---------------------------------------------------------------
module carriage() {
  color(C_CARR)
  difference() {
    union() {
      // top stop block
      translate([0,0,post_top]) racetrack(ts_h, end_r);
      // two side walls down to the cap (the rigid link tying both bores)
      for (sy=[-1,1])
        translate([-(el_off+end_r), sy*end_r - sy*1.2, post_bot])
          cube([2*(el_off+end_r), 1.2, post_top-post_bot]);
      // bottom plate with collars that slip over the bosses = registration
      translate([0,0,post_bot]) racetrack(boss_h, end_r);
    }
    // BEARING 2: upper bores through the top stop
    for (s=[-1,1])
      translate([s*el_off,0,post_top-eps]) cylinder(d=el_d+clear, h=ts_h+2*eps);
    // collar bores: slip over the cap bosses
    for (s=[-1,1])
      translate([s*el_off,0,post_bot-eps]) cylinder(d=collar_id, h=boss_h+2*eps);
    // M3 clamp bolts (horizontal): each pushes a wire onto its electrode
    for (s=[-1,1])
      translate([s*(el_off+end_r), 0, post_top+ts_h/2])
        rotate([0, -s*90, 0]) cylinder(d=3.2, h=end_r+1.5);
  }
}

// ---------------------------------------------------------------
module vial() {
  color(C_VIAL)
    translate([0,0,-40]) cylinder(d=cap_od-2*wall-0.8, h=sept_z+40);
}

// ---------------------------------------------------------------
module assembly() {
  translate([0,0,z_vial]) vial();
  translate([0,0,z_cap])  cap();
  translate([0,0,z_sept]) septum();
  translate([0,0,z_elec]) electrodes();
  translate([0,0,z_carr]) carriage();
}

if (view == "section")
  difference() {
    assembly();
    translate([-200,0,-200]) cube([400,200,400]);   // remove y>0 half
  }
else
  assembly();
