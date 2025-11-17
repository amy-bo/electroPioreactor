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
  electrode_shell(stop_height);

  // Openings for the electrodes from the top only
  for (offset = [-electrode_offset, electrode_offset])
    translate([-offset, 0, stop_cap_thickness])
      cylinder(d = electrode_port_od, h = stop_hole_depth, center = false);
}
