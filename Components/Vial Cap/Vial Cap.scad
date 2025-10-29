// BOSL2 GPI 24-400 internal thread cap (test ring)
// Requires BOSL2 in OpenSCAD libraries path:
//   https://github.com/BelfrySCAD/BOSL2

include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// -----------------------------
// Parameters
// -----------------------------
// Input parameters
// Cap
cap_od = 27; // mm (outer diameter of ring/cap)
cap_h = 10; // mm (overall height)
top_th = 2.2; // mm (flat top thickness; 0 = open ring)
ribs = 84; // number or ribs to add to the cap for grip (Cam used ~84)
rib_dia = 0.856; // mm (diameter of ribs, Cam used 0.856)
bore_len = cap_h - top_th; // mm (length of bore; usually same as cap_h - top_th)
// Cap O-ring
cap_o_ring_id = 18.7706; // mm (inner diameter of o-ring)
cap_o_ring_cs = 1.7; // mm (cross-sectional diameter of o-ring)
// Electrodes
electrodes = 2; // electrode ports (0 = none, 2 = two opposite)
electrode_od = 6; // mm (outer diameter of electrode)
electrode_tol = 0.4; // mm (diametral print tolerance for electrode port)
electrode_offset = 5; // mm (distance from center to electrode port center)
electrode_port_od = electrode_od + electrode_tol; // mm (diameter of electrode port)
electrode_o_ring_cs = 1.8; // mm (cross-sectional diameter of o-ring)
electrode_o_ring_id = electrode_od + (electrode_o_ring_cs/2); // mm (inner diameter of o-ring)

// Ports
ports = 5; // number of ports
port_dia = 3.2; // mm (diameter of silicone tube ports)
port_limit = cap_o_ring_id; // mm (maximum distance from centre to far edge of port)
// Print quality
$fn = 180; // render quality - facets for smoothness

// GPI 24-400 basics
T_nom = 24.10; // "T" dimension (outside dia over threads)
dia_clear = 0.30; // diametral print clearance (tune 0.20–0.50)
pitch = 25.4/8; // theoretically 8 TPI -> 3.175 mm pitch
starts = 1; // 400 = single-start
thread_len = bore_len - pitch; // run thread through the height
helix_turns = thread_len / pitch; // BOSL2 thread_helix expects 'turns' in this version
leadin_len = 0.6*pitch; // modest entry chamfer; set 0 for none
D_maj_int = T_nom + dia_clear; // Internal-thread major diameter at the crests (what the bottle’s thread “sees”).
depth_rad = 0.3 * pitch; // theoretically radial thread depth (ISO V) = 5/8 * H = 0.541265*P
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

    // Ribs for grip
    if (ribs > 0) {
      for (i = [0 : ribs - 1]) {
        rotate([0,0,i*360/ribs])
          translate([cap_od/2,0,0])
            cylinder(d=rib_dia, h=cap_h);
      }
    } 

    // O-ring wedge
      // *** NOT YET IMPLEMENTED ***
  }
  // Anything beyond this point is subtracted from the cap

  // Chamfer top edge
    // *** NOT YET IMPLEMENTED ***

  // Cap O-ring groove
  translate([0,0,top_th])
    rotate_extrude(convexity = 10, $fn = 100)
      translate([(cap_o_ring_id+cap_o_ring_cs)/2, 0, 0])
          circle(d = cap_o_ring_cs, $fn = 100);
  // ***
  // Ports
  // ***
  // Electrodes
  if (electrodes > 0)
    for (i = [0 : electrodes - 1]) {
      rotate([0,0,i*360/electrodes])
        translate([electrode_offset,0,0])
          union() {
            // Electrode port
            cylinder(d=electrode_port_od, h=cap_h);
            // Electrode O-ring groove
            translate([0,0,top_th/2])
              rotate_extrude(convexity = 10, $fn = 100)
                translate([(electrode_o_ring_id)/2, 0, 0])
                    circle(d = electrode_o_ring_cs, $fn = 100);
          }
          
    }
  // Tube ports
  if (ports > 0)
    if (electrodes == 0 || electrode_offset == 0)
      for (i = [0 : ports - 1]) {
        rotate([0,0,i*360/ports])
          translate([(port_limit-port_dia)/2,0,0])
            cylinder(d=port_dia, h=cap_h);
      }
    else if (ports < 3)
      for (j = [0 : ports - 1]) {
        rotate([0,0,90+j*360/ports])
          translate([(port_limit-port_dia)/2,0,0])
            cylinder(d=port_dia, h=cap_h);
      }
    else // ports >= 3
      {
        ring_ports = (ports < 4) ? ports : 4;  // limit to 4, or fewer if ports<4
        for (k = [0 : 2 + ring_ports - 1]) {
          rotate([0,0,k*360/6])
            translate([(port_limit-port_dia)/2,0,0])
              if (k==0 || k==3) { /* skip electrodes at 0° and 180° */ } else
              cylinder(d=port_dia, h=cap_h);
        }
      }
  if (ports > 4)
    for (l = [0 : ports - 5]) {
      rotate([0,0,90+l*180])
        translate([(port_limit-port_dia)/2,0,0])
          cylinder(d=port_dia, h=cap_h);
    }
}