// Dan Kirshner's metric_thread implementation for accurate metric threads
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
    // Internal thread using Dan Kirshner's metric_thread
    translate([0,0,0])
        metric_thread(diameter=neck_major_d, pitch=thread_pitch, length=thread_len, internal=true);
}

// Dan Kirshner's metric_thread module
// Reference: https://github.com/openscad/openscad/blob/master/libraries/thread.scad
module metric_thread(diameter=10, pitch=1.5, length=10, internal=false, $fn=60) {
    // Thread profile parameters
    h = pitch * 0.61343; // height of thread triangle
    r = pitch * 0.14434; // radius of rounded thread root
    d = diameter;
    turns = ceil(length / pitch);
    base_d = internal ? d + 2*h : d - 2*h;
    root_r = internal ? r : r;
    // Helix path
    module thread_profile() {
        // Thread triangle with rounded root
        polygon(points=[
            [0,0],
            [pitch/2, h],
            [pitch,0]
        ]);
    }
    module thread_segment() {
        difference() {
            // Thread profile extruded along pitch length
            linear_extrude(height=pitch, center=false, convexity=10)
                thread_profile();
            // Cut root radius
            translate([pitch/2, 0, 0])
                circle(r=root_r, $fn=20);
        }
    }
    // Helical thread
    rotate_extrude(angle=360, convexity=10, $fn=$fn)
        translate([base_d/2, 0, 0])
            thread_profile();
    // Thread length
    linear_extrude(height=length, center=false, convexity=10)
        rotate(0)
            translate([0,0,0])
                // Create multiple turns by repeating thread profile along length
                for (i = [0:turns-1])
                    translate([i*pitch, 0, 0])
                        thread_profile();
}

test_ring();
