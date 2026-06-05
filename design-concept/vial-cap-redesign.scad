// Vial Cap - REDESIGN (derived from ../Components/Vial Cap/Vial Cap.scad)
// Changes vs the current cap:
//   - O-rings removed (cap O-ring + both electrode O-rings) -> single silicone
//     SEPTUM disc sits on a smooth seat under the closed top; the vial rim
//     compresses it. Seals the mouth, every port and both electrodes.
//   - Electrode holes are now plain CLEARANCE (the separate electrode column
//     holds the electrodes rigid - see electrode-column / electrode-holder-v3).
//   - Two PEG registration holes for the column.
//   - Poka-yoke TAB added on one side (geometry from vial-cap-s.3mf).
// Thread, ribs, dimensions and port layout are unchanged from the original.
// NOTE: BOSL2 thread - render-check in OpenSCAD (no binary in the dev box).
include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// ----- Cap -----
cap_od = 27; cap_h = 12.3; top_th = 2.5;
ribs = 84; rib_dia = 0.856;
bore_len = cap_h - top_th;

// ----- Septum (replaces all O-rings) -----
sept_t  = 2.0;                       // silicone sheet thickness
sept_d  = 23.9;                      // disc diameter (confined by the bore wall)
sept_seat_d = sept_d + 0.3;          // smooth seat diameter under the closed top

// ----- Electrode clearance (held rigid by the column, not the cap) -----
electrodes = 2;
electrode_od = 6.2;
electrode_tol = 0.6; electrode_cutout = 1;
electrode_offset = 4.8;
electrode_port_od = electrode_od + electrode_tol + electrode_cutout;  // loose clearance

// ----- Column registration pegs (on the y-axis) -----
peg_d = 3; peg_off = 4; peg_clear = 0.3;

// ----- Poka-yoke tab (from vial-cap-s.3mf: rounded lobe on one side) -----
tab_d = 8; tab_protrude = 3;

// ----- Ports -----
ports = 6; port_dia = 3.2;
cap_o_ring_id = 18.7706;             // kept only to set the port radius
port_limit = cap_o_ring_id;

$fn = 180;

// GPI 24-400 thread
T_nom = 24.30; dia_clear = 0.50; pitch = 25.4/8; starts = 1;
leadin_len = 0.6*pitch;
D_maj_int = T_nom + dia_clear; depth_rad = 0.3*pitch; D_minor_int = D_maj_int - 2*depth_rad;
// reserve the top sept_t of the bore as a smooth septum seat, thread below it
thread_len  = bore_len - sept_t - pitch;
helix_turns = thread_len / pitch;

difference() {
  // ***** Cap body *****
  union() {
    difference() {
      union() {
        cylinder(d=cap_od, h=cap_h);
        // poka-yoke tab (additive rounded lobe on -Y)
        translate([0, -(cap_od/2 - (tab_d/2 - tab_protrude)), 0]) cylinder(d=tab_d, h=cap_h);
      }
      // core bore
      translate([0,0,top_th]) cylinder(d=T_nom, h=bore_len);
    }
    // internal thread (started below the septum seat)
    translate([0,0,top_th + sept_t + pitch/2])
      thread_helix(d=D_minor_int, pitch=pitch, turns=helix_turns, thread_depth=depth_rad,
                   flank_angle=30, starts=starts, anchor=BOTTOM, lead_in=leadin_len, internal=true);
    // grip ribs
    if (ribs > 0)
      for (i = [0:ribs-1]) rotate([0,0,i*360/ribs]) translate([cap_od/2,0,0]) cylinder(d=rib_dia, h=cap_h);
  }

  // ***** Septum seat (smooth counterbore under the closed top) *****
  translate([0,0,top_th]) cylinder(d=sept_seat_d, h=sept_t);

  // ***** Electrode clearance holes *****
  if (electrodes > 0)
    for (i = [0:electrodes-1])
      rotate([0,0,i*360/electrodes]) translate([electrode_offset,0,0])
        cylinder(d=electrode_port_od, h=cap_h);

  // ***** Peg registration holes (through the closed top, on y-axis) *****
  for (s = [-1,1])
    translate([0, s*peg_off, -0.01]) cylinder(d=peg_d + peg_clear, h=top_th + 0.02);

  // ***** Tube ports (unchanged layout from the original) *****
  if (ports > 0)
    if (electrodes == 0 || electrode_offset == 0)
      for (i = [0:ports-1]) rotate([0,0,i*360/ports]) translate([(port_limit-port_dia)/2,0,0]) cylinder(d=port_dia, h=cap_h);
    else if (ports < 3)
      for (j = [0:ports-1]) rotate([0,0,90+j*360/ports]) translate([(port_limit-port_dia)/2,0,0]) cylinder(d=port_dia, h=cap_h);
    else {
      ring_ports = (ports < 4) ? ports : 4;
      for (k = [0:2+ring_ports-1])
        rotate([0,0,k*360/6]) translate([(port_limit-port_dia)/2,0,0])
          if (k==0 || k==3) { } else cylinder(d=port_dia, h=cap_h);
    }
  if (ports > 4)
    for (l = [0:ports-5]) rotate([0,0,90+l*180]) translate([(port_limit-port_dia)/2,0,0]) cylinder(d=port_dia, h=cap_h);
}
