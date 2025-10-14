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

// Internal thread module (Dan Kirshner's metric_thread simplified for internal thread)
// This is a compact implementation for internal ISO metric thread
module internal_thread(major_d, pitch, length) {
    // Thread profile parameters
    h = pitch * 0.61343; // Thread height
    r = pitch * 0.14434; // Root radius
    R = pitch * 0.14434; // Crest radius
    half_angle = 30; // Thread flank angle in degrees

    // Thread profile polygon (equilateral triangle with truncated roots and crests)
    thread_profile = polygon(points=[
        [0,0],
        [pitch*0.5 - r, h],
        [pitch*0.5 + r, h],
        [pitch,0],
        [pitch*0.5 + R, -h*0.1],
        [pitch*0.5 - R, -h*0.1]
    ]);

    // Number of threads to generate
    n_threads = ceil(length / pitch);

    // Helix parameters
    turns = length / pitch;
    thread_radius = major_d / 2 - h;

    // Create the internal thread by subtracting the helix
    difference() {
        // Cylinder with minor diameter
        cylinder(h = length, d = major_d - 2 * h, center = false, $fn=100);

        // Helical thread cutout
        for (i = [0 : n_threads-1]) {
            rotate_extrude(angle = 360, $fn=100)
                translate([thread_radius, 0, 0])
                    linear_extrude(height = pitch)
                        offset(r = 0)
                            thread_profile;
            translate([0,0,i*pitch])
                rotate([0,0,i*360])
                    translate([0,0,0])
                        difference();
        }
    }
}

test_ring();
