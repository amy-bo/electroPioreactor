// Parametric cylinder for vial cap test
cap_height = 8;     // mm
cap_diameter = 27;  // mm

// cylinder(h = cap_height, d = cap_diameter, center = true); // replaced by GPI 24-400 threaded ring
gpi_24_400_threaded_ring(od=cap_diameter, h=cap_height);

// =========================
// Internal (female) thread support (Dan Kirshner metric threads, extracted verbatim)
// Source: Dan Kirshner, GPLv3 — ISO metric/English thread generator (Version 2.5, 2020-04-11)
// Minimal set of modules/functions required for internal threads in this project.
// =========================

// Helper for segment count based on diameter
function segments (diameter) = min (50, max (ceil (diameter*6), 25));

module metric_thread (diameter=8, pitch=1, length=1, internal=false, n_starts=1,
                      thread_size=-1, groove=false, square=false, rectangle=0,
                      angle=30, taper=0, leadin=0, leadfac=1.0, test=false)
{
   // thread_size: size of thread "V" different than travel per turn (pitch).
   // Default: same as pitch.
   local_thread_size = thread_size == -1 ? pitch : thread_size;
   local_rectangle = rectangle ? rectangle : 1;

   n_segments = segments (diameter);
   h = (test && ! internal) ? 0 : (square || rectangle) ? local_thread_size*local_rectangle/2 : local_thread_size / (2 * tan(angle));

   h_fac1 = (square || rectangle) ? 0.90 : 0.625;

   // External thread includes additional relief.
   h_fac2 = (square || rectangle) ? 0.95 : 5.3/8;

   tapered_diameter = diameter - length*taper;

   difference () {
      union () {
         if (! groove) {
            if (! test) {
               metric_thread_turns (diameter, pitch, length, internal, n_starts,
                                    local_thread_size, groove, square, rectangle, angle,
                                    taper);
            }
         }

         difference () {

            // Solid center, including Dmin truncation.
            if (groove) {
               cylinder (r1=diameter/2, r2=tapered_diameter/2,
                         h=length, $fn=n_segments);
            } else if (internal) {
               cylinder (r1=diameter/2 - h*h_fac1, r2=tapered_diameter/2 - h*h_fac1,
                         h=length, $fn=n_segments);
            } else {

               // External thread.
               cylinder (r1=diameter/2 - h*h_fac2, r2=tapered_diameter/2 - h*h_fac2,
                         h=length, $fn=n_segments);
            }

            if (groove) {
               if (! test) {
                  metric_thread_turns (diameter, pitch, length, internal, n_starts,
                                       local_thread_size, groove, square, rectangle,
                                       angle, taper);
               }
            }
         }

         // Internal thread lead-in: take away from external solid.
         if (internal) {

            // "Negative chamfer" z=0 end if leadin is 2 or 3.
            if (leadin == 2 || leadin == 3) {
               cylinder (r1=diameter/2, r2=diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac,
                         $fn=n_segments);
            }

            // Chamfer z-max end if leadin is 1 or 2.
            if (leadin == 1 || leadin == 2) {
               translate ([0, 0, length + 0.05 - h*h_fac1*leadfac]) {
                  cylinder (r1=tapered_diameter/2, r2=tapered_diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac,
                            $fn=n_segments);
               }
            }
         }

         // External thread lead-in: add to external solid.
         if (! internal) {
            // "Negative chamfer" z=0 end if leadin is 2 or 3.
            if (leadin == 2 || leadin == 3) {
               difference () {
                  cylinder (r=diameter/2 + 1, h=h*h_fac1*leadfac, $fn=n_segments);

                  cylinder (r2=diameter/2, r1=diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac,
                            $fn=n_segments);
               }
            }

            // Chamfer z-max end if leadin is 1 or 2.
            if (leadin == 1 || leadin == 2) {
               translate ([0, 0, length + 0.05 - h*h_fac1*leadfac]) {
                  difference () {
                     cylinder (r=diameter/2 + 1, h=h*h_fac1*leadfac, $fn=n_segments);

                     cylinder (r1=tapered_diameter/2, r2=tapered_diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac,
                               $fn=n_segments);
                  }
               }
            }
         }
      }
   }
}

module english_thread (diameter=1/4*25.4, threads_per_inch=20, length=1,
                       internal=false, n_starts=1, thread_size=-1, groove=false,
                       square=false, rectangle=0, angle=30, taper=0,
                       leadin=0, leadfac=1.0, test=false)
{
   pitch = 25.4 / threads_per_inch;
   metric_thread (diameter, pitch, length, internal, n_starts, thread_size,
                  groove, square, rectangle, angle, taper, leadin, leadfac, test);
}

module metric_thread_turns (diameter, pitch, length, internal, n_starts,
                            thread_size, groove, square, rectangle, angle,
                            taper)
{
   // Number of turns needed.
   n_turns = floor (length/pitch);

   intersection () {

      // Start one below z = 0.  Gives an extra turn at each end.
      for (i=[-1*n_starts : n_turns+1]) {
         translate ([0, 0, i*pitch]) {
            metric_thread_turn (diameter, pitch, internal, n_starts,
                                thread_size, groove, square, rectangle, angle,
                                taper, i*pitch);
         }
      }

      // Cut to length.
      translate ([0, 0, length/2]) {
         cube ([diameter*3, diameter*3, length], center=true);
      }
   }
}

module metric_thread_turn (diameter, pitch, internal, n_starts, thread_size,
                           groove, square, rectangle, angle, taper, z)
{
   n_segments = segments (diameter);
   fraction_circle = 1.0/n_segments;
   for (i=[0 : n_segments-1]) {
      rotate ([0, 0, i*360*fraction_circle]) {
         translate ([0, 0, i*n_starts*pitch*fraction_circle]) {
            //current_diameter = diameter - taper*(z + i*n_starts*pitch*fraction_circle);
            thread_polyhedron ((diameter - taper*(z + i*n_starts*pitch*fraction_circle))/2,
                               pitch, internal, n_starts, thread_size, groove,
                               square, rectangle, angle);
         }
      }
   }
}

module thread_polyhedron (radius, pitch, internal, n_starts, thread_size,
                          groove, square, rectangle, angle)
{
   n_segments = segments (radius*2);
   fraction_circle = 1.0/n_segments;

   local_rectangle = rectangle ? rectangle : 1;

   h = (square || rectangle) ? thread_size*local_rectangle/2 : thread_size / (2 * tan(angle));
   outer_r = radius + (internal ? h/20 : 0); // Adds internal relief.
   //echo (str ("outer_r: ", outer_r));

   // A little extra on square threads.
   thread_fac1 = (square || rectangle) ? 0.90 : 0.625;
   thread_fac2 = (square || rectangle) ? 0.95 : 5.3/8;

   // The thread "tooth" cross-section is a trapezoid (or rectangle for square threads).
   // Points A, B, C, D going up the "tooth" on the near side.
   //   A: at inner radius
   //   B: at inner radius + 1/8*h (or for square, + thread_size*local_rectangle/2)
   //   C: at outer radius - 1/8*h (or for square, + thread_size*local_rectangle/2)
   //   D: at outer radius
   A = [radius - h*thread_fac1, 0, 0];
   B = [radius - h*thread_fac2, 0, 0];
   C = [outer_r + h*thread_fac2, 0, 0];
   D = [outer_r + h*thread_fac1, 0, 0];

   // Inner and outer rectangles for groove and square/rectangle options.
   inner_rect = square || rectangle ? [[radius - thread_size*local_rectangle/2, 0, 0],
                                       [radius - thread_size*local_rectangle/2, 0, 0],
                                       [radius - thread_size*local_rectangle/2, 0, 0],
                                       [radius - thread_size*local_rectangle/2, 0, 0]]
                                   : [[radius - h*thread_fac1, 0, 0],
                                      [radius - h*thread_fac1, 0, 0],
                                      [radius - h*thread_fac1, 0, 0],
                                      [radius - h*thread_fac1, 0, 0]];

   outer_rect = square || rectangle ? [[outer_r + thread_size*local_rectangle/2, 0, 0],
                                       [outer_r + thread_size*local_rectangle/2, 0, 0],
                                       [outer_r + thread_size*local_rectangle/2, 0, 0],
                                       [outer_r + thread_size*local_rectangle/2, 0, 0]]
                                   : [[outer_r + h*thread_fac1, 0, 0],
                                      [outer_r + h*thread_fac1, 0, 0],
                                      [outer_r + h*thread_fac1, 0, 0],
                                      [outer_r + h*thread_fac1, 0, 0]];

   // Construct polyhedron for a single segment of the helix.
   for (j=[0 : n_starts-1]) {
      rotate ([0, 0, j*360/n_starts]) {
         polyhedron (
            points = [
                       // Near-side trapezoid (A-B-C-D rotated around)
                       A, B, C, D,
                       // Far-side trapezoid rotated by one segment
                       let (ang = 360*fraction_circle)
                         [ for (p=[A,B,C,D]) [ p[0]*cos(ang) - p[1]*sin(ang), p[0]*sin(ang) + p[1]*cos(ang), p[2] + pitch*fraction_circle ] ],
                       // Inner rectangle (near and far)
                       inner_rect[0], inner_rect[1], inner_rect[2], inner_rect[3],
                       let (ang = 360*fraction_circle)
                         [ for (p=inner_rect) [ p[0]*cos(ang) - p[1]*sin(ang), p[0]*sin(ang) + p[1]*cos(ang), p[2] + pitch*fraction_circle ] ],
                       // Outer rectangle (near and far)
                       outer_rect[0], outer_rect[1], outer_rect[2], outer_rect[3],
                       let (ang = 360*fraction_circle)
                         [ for (p=outer_rect) [ p[0]*cos(ang) - p[1]*sin(ang), p[0]*sin(ang) + p[1]*cos(ang), p[2] + pitch*fraction_circle ] ]
                     ],
            faces = [
                       // Connect near and far trapezoids
                       [0, 1, 5, 4],  // Lower near-to-far
                       [1, 2, 6, 5],  // Middle
                       [2, 3, 7, 6],  // Upper

                       // Close the trapezoids
                       [0, 4, 7, 3],  // Front-side trapezoid
                       [1, 5, 6, 2],  // Back-side trapezoid

                       [0, 1, 2, 3],  // Inner rectangle

                       [4, 7, 6, 5],  // Outer rectangle

                       // These are not planar, so do with separate triangles.
                       [7, 2, 6],     // Upper rectangle, bottom
                       [7, 3, 2],     // Upper rectangle, top

                       [0, 5, 1],     // Lower rectangle, bottom
                       [0, 4, 5]      // Lower rectangle, top
                      ]
         );
      }
   }
}

// =========================
// Wrapper: female (internal) metric thread for vial cap use
// =========================
module vial_cap_internal_thread(d=27, pitch=3, length=8, n_starts=1,
                                angle=30, taper=0, leadin=1, leadfac=1.0, test=false)
{
   // This creates the *thread geometry*; typically you would `difference()` it from the cap wall.
   metric_thread(diameter=d, pitch=pitch, length=length, internal=true, n_starts=n_starts,
                 angle=angle, taper=taper, leadin=leadin, leadfac=leadfac, test=test);
}


// =========================
// GPI 24-400 threaded test ring (internal thread goes through)
// =========================
// Defaults per GPI 24-400: T ≈ 24.13 mm, E ≈ 21.97 mm, 8 TPI (pitch 3.175 mm), 60° thread (angle=30)
module gpi_24_400_threaded_ring(od=27, h=8,
                                T=24.13,        // outside diameter over finish threads ("T")
                                E=21.97,        // minor diameter below threads ("E")
                                clearance=0.30, // diametral clearance added to T for print fit
                                threads_per_inch=8,
                                leadin=0)
{
  // Practical through-bore for guaranteed clearance at the thread minor
  // IMPORTANT: leave material for the thread to be cut — bore slightly *smaller* than E
  bore_d = E - 0.30;           // provides stock for the cutter to form crests
  cutter_d = T + clearance;    // oversize the external-thread cutter for fit
  
  difference() {
    // Outer ring
    cylinder(h=h, d=od, center=false);
    
    // Ensure a through-hole at least as large as E (slightly over)
    translate([0,0,-0.05])
      cylinder(h=h+0.10, d=bore_d, center=false);
    
    // Subtract an EXTERNAL thread "cutter" to create the INTERNAL thread profile
    // Using english_thread wrapper (8 TPI => 3.175 mm pitch). Keep angle=30 (i.e. 60° included).
    english_thread(diameter=cutter_d,
                   threads_per_inch=threads_per_inch,
                   length=h+0.10,     // tiny overlength to guarantee full cut
                   internal=false,    // external thread solid acts as cutter
                   n_starts=1,
                   thread_size=-1,
                   groove=false,
                   square=false,
                   rectangle=0,
                   angle=30,
                   taper=0,
                   leadin=leadin,
                   leadfac=1.0,
                   test=false);
  }
}