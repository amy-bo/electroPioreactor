// Electrode Seating Guide
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

stop_height = 35;           // mm, overall height of the figure-eight stop
shell_wall = 0.8;          // mm extra wall around each electrode sleeve

// Derived dimensions
electrode_port_od = electrode_od + electrode_tol + electrode_cutout;
outer_shell_od = electrode_port_od + 2 * shell_wall;
separation = (electrode_offset - ((electrode_od + electrode_tol) / 2))*2;
assert(separation > 0, "electrode_offset must be greater than half electrode_od");

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
union() {
  difference() {
  electrode_shell(stop_height);

  // Openings for the electrodes
  for (offset = [-electrode_offset, electrode_offset])
    translate([-offset, 0, 0])
      cylinder(d = electrode_port_od, h = stop_height, center = false);

  // Remove 3/4 of cross-section to allow easy removal
  translate([-outer_shell_od *2, 0, 0])
    cube([outer_shell_od *4, outer_shell_od, stop_height], center = false);
  for (offset = [-electrode_offset*2, electrode_offset*2])
    translate([offset, 0 , stop_height/2])
      cube([outer_shell_od, outer_shell_od, stop_height], center = true);
  }
  // Central cylinder to protrude beyond centre point for better seating
      cylinder(d = separation, h = stop_height, center = false);

  // Pull handle
    translate([0,-outer_shell_od/2 - separation/4,0])
      cylinder(d = separation, h = stop_height, center = false); 
}
