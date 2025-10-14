// Parameters
neck_major_d = 24;       // Nominal neck major diameter (outer diameter of thread)
thread_pitch = 2.7;      // Thread pitch in mm
thread_len = 8;          // Length of thread in mm
wall_thickness = 2;      // Wall thickness in mm
fit_add = 0.1;           // Fit allowance for clearance
cap_h = 8;               // Total height of the cap in mm

// Derived parameters
thread_minor_d = neck_major_d - 2 * (1.226869 * thread_pitch); // Approx minor diameter of internal thread
inner_d = neck_major_d - 2 * wall_thickness; // Inner diameter of outer cylinder

// Main module
module test_ring() {
    // Outer cylinder (neck)
    difference() {
        cylinder(h = cap_h, d = neck_major_d + 2 * wall_thickness, center = false, $fn=100);
        // Hollow inside
        translate([0,0,0])
            cylinder(h = cap_h, d = inner_d, center = false, $fn=100);
    }
    // Internal thread
    translate([0,0,0])
        internal_thread(neck_major_d - fit_add, thread_pitch, thread_len);
}

// Internal thread module (simplified placeholder)
module internal_thread(major_d, pitch, length) {
    h = pitch * 0.61343;
    n_turns = ceil(length / pitch);
    difference() {
        // Main bore
        cylinder(h=length, d=major_d - 2*h, $fn=100);
        // Helical thread subtraction (simplified representation)
        for (i = [0:n_turns-1]) {
            translate([0,0,i*pitch])
                rotate_extrude(angle=360, $fn=100)
                    translate([major_d/2 - h, 0, 0])
                        polygon([[0,0],[pitch/2,h],[pitch,0]]);
        }
    }
}

test_ring();
