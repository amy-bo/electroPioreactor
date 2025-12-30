// Electrode Top Stop
// Racetrack-shaped cover that keeps the two electrodes parallel and seated
// to a consistent depth. Only the top is open, so the bottom face stops each
// electrode at the same height while also sitting flat on the print bed.
// Modified from Vial Cap.scad by Codex, then hand fixed.

$fn = 160; // smooth cylinders for a better fit

// -----------------------------
// Key parameters
// -----------------------------
electrode_od = 6.0;        // mm, outer diameter of electrode
electrode_tol = 0.6;       // mm, print clearance on each electrode hole
electrode_cutout = 0;      // mm, additional clearance used on the cap
electrode_offset = 4.8;    // mm, distance from origin to each electrode center

stop_height = 12;           // mm, overall height of the figure-eight stop
stop_cap_thickness = 2;    // mm kept solid on top to create the stop surface
shell_wall = 0.8;          // mm extra wall around each electrode sleeve

m3_nut_od = 5.8;
wall = 1.3;
m3_nut_holder_width = m3_nut_od + wall;
m3_nut_width = 2.5;
m3_bolt = 3.1;


// Derived dimensions
electrode_port_od = electrode_od + electrode_tol + electrode_cutout;
outer_shell_od = electrode_port_od + 2 * shell_wall;
stop_hole_depth = stop_height - stop_cap_thickness;
assert(stop_cap_thickness < stop_height, "stop_cap_thickness must be less than stop_height");

// -----------------------------
// Helper modules
// -----------------------------
module electrode_shell(height) {
  union() {
    // Cylindrical sleeves around each electrode port
    for (offset = [-electrode_offset, electrode_offset])
      translate([-offset, 0, 0])
        cylinder(d = outer_shell_od, h = height, center = false);

    // Rectangular bridge that closes the sleeves into a racetrack profile
    translate([- electrode_offset, -outer_shell_od / 2, 0])
      cube([2 * electrode_offset, outer_shell_od, height], center = false);
  }
}

// -----------------------------
// Model
// -----------------------------
difference() {
  hull() {
    electrode_shell(stop_height);
    
    // Nut holders
    for (offset = [-1.4, 1])
      translate([offset * (outer_shell_od + wall), -m3_nut_holder_width / 2, 0])
        cube([m3_nut_width + wall, m3_nut_holder_width, stop_height]);
  }
  
  // Nut traps
  for (offset = [-1.3, 1])
      translate([offset * (outer_shell_od + wall), -m3_nut_od/2, -5])
        cube([m3_nut_width, m3_nut_od, stop_height]);
    
  // Wire holes
  for (offset = [-1.2, 1])
      translate([offset * (outer_shell_od - 1), -m3_bolt/2, 0])
        cube([1, m3_bolt, stop_hole_depth]);
  
  // Bolt holes
  for (offset = [-1, 1])  
      translate([offset * electrode_offset, 0, m3_nut_holder_width/2])
        rotate([offset * 90, 0, 90])
          cylinder(15, d = m3_bolt);

  // Openings for the electrodes from the top only
  for (offset = [-electrode_offset, electrode_offset])
    translate([-offset, 0, stop_cap_thickness])
      cylinder(d = electrode_port_od, h = stop_hole_depth, center = false);
}
