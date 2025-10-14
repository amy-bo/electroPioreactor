//
// Plain GPI 24-400 vial cap (female) — single file
// Uses Dan Kirshner’s metric_thread (included inline)
//
// -------- USER PARAMS --------
gpi_major_d   = 24.0;   // mm  male thread OD across crests (24-400)
gpi_pitch     = 3.175 ;   // mm  0.125"
thread_len    = 8.0;    // mm  engagement inside cap

wall_thickness = 2.0;   // mm  cap wall outside the thread roots
fit_add        = 0.20;  // mm  tweak fit (adds to nominal diameter passed to thread lib)
lid_thick      = 3.0;   // mm  solid top thickness
cap_h          = 12.0;  // mm  total cap height
bore_margin    = 0.60;  // mm  extra clearance for UNTHREADED zone above the thread

$fn = 128;

// Derived OD so the wall is what you asked for
cap_od = (gpi_major_d + fit_add) + 2*wall_thickness;

// Guard
if (thread_len > cap_h - lid_thick)
  echo("WARNING: thread_len exceeds available height; reduce thread_len or increase cap_h/lid_thick.");

// -------- MODEL --------
difference() {
  // Outer shell
  cylinder(h=cap_h, d=cap_od);

  // 1) Subtract the INTERNAL 24-400 thread from base upward
  metric_thread(
    diameter = gpi_major_d + fit_add,  // male OD + small fit tweak
    pitch    = gpi_pitch,
    length   = thread_len,
    internal = true,
    leadin   = 2,       // entry chamfer inside
    n_starts = 1,
    angle    = 30       // 60° included (metric V) → angle=30 in this lib
  );

  // 2) Unthreaded clearance above the thread up to the underside of lid
  unthreaded_h = max(0, cap_h - lid_thick - thread_len);
  if (unthreaded_h > 0)
    translate([0,0,thread_len])
      cylinder(h=unthreaded_h, d=(gpi_major_d + fit_add + bore_margin));
}

/* ============================================================================
   Dan Kirshner's metric_thread library (verbatim, compact)
   ========================================================================== */
function segments (diameter) = min (50, max (ceil (diameter*6), 25));

module metric_thread (diameter=8, pitch=1, length=1, internal=false, n_starts=1,
                      thread_size=-1, groove=false, square=false, rectangle=0,
                      angle=30, taper=0, leadin=0, leadfac=1.0, test=false)
{
   local_thread_size = thread_size == -1 ? pitch : thread_size;
   local_rectangle = rectangle ? rectangle : 1;

   n_segments = segments (diameter);
   h = (square || rectangle) ? local_thread_size*local_rectangle/2 : local_thread_size / (2 * tan(angle));

   h_fac1 = (square || rectangle) ? 0.90 : 0.625;
   h_fac2 = (square || rectangle) ? 0.95 : 5.3/8;

   tapered_diameter = diameter - length*taper;

   difference () {
      union () {
         if (! groove && ! test)
            metric_thread_turns (diameter, pitch, length, internal, n_starts,
                                 local_thread_size, groove, square, rectangle, angle, taper);

         difference () {
            if (groove) {
               cylinder (r1=diameter/2, r2=tapered_diameter/2, h=length, $fn=n_segments);
            } else if (internal) {
               cylinder (r1=diameter/2 - h*h_fac1, r2=tapered_diameter/2 - h*h_fac1, h=length, $fn=n_segments);
            } else {
               cylinder (r1=diameter/2 - h*h_fac2, r2=tapered_diameter/2 - h*h_fac2, h=length, $fn=n_segments);
            }
            if (groove && ! test)
               metric_thread_turns (diameter, pitch, length, internal, n_starts,
                                    local_thread_size, groove, square, rectangle, angle, taper);
         }

         if (internal) {
            if (leadin == 2 || leadin == 3)
               cylinder (r1=diameter/2, r2=diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac, $fn=n_segments);
            if (leadin == 1 || leadin == 2)
               translate ([0, 0, length + 0.05 - h*h_fac1*leadfac])
                 cylinder (r1=tapered_diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac, r2=tapered_diameter/2, $fn=n_segments);
         }
      }

      if (! internal) {
         if (leadin == 2 || leadin == 3)
            difference () {
               cylinder (r=diameter/2 + 1, h=h*h_fac1*leadfac, $fn=n_segments);
               cylinder (r2=diameter/2, r1=diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac, $fn=n_segments);
            }
         if (leadin == 1 || leadin == 2)
            translate ([0, 0, length + 0.05 - h*h_fac1*leadfac])
              difference () {
                 cylinder (r=diameter/2 + 1, h=h*h_fac1*leadfac, $fn=n_segments);
                 cylinder (r1=tapered_diameter/2, r2=tapered_diameter/2 - h*h_fac1*leadfac, h=h*h_fac1*leadfac, $fn=n_segments);
              }
      }
   }
}

module metric_thread_turns (diameter, pitch, length, internal, n_starts,
                            thread_size, groove, square, rectangle, angle, taper)
{
   n_turns = floor (length/pitch);
   intersection () {
      for (i=[-1*n_starts : n_turns+1])
         translate ([0, 0, i*pitch])
           metric_thread_turn (diameter, pitch, internal, n_starts, thread_size, groove, square, rectangle, angle, taper, i*pitch);
      translate ([0, 0, length/2]) cube ([diameter*3, diameter*3, length], center=true);
   }
}

module metric_thread_turn (diameter, pitch, internal, n_starts, thread_size,
                           groove, square, rectangle, angle, taper, z)
{
   n_segments = segments (diameter);
   fraction_circle = 1.0/n_segments;
   for (i=[0 : n_segments-1])
      rotate ([0, 0, i*360*fraction_circle])
        translate ([0, 0, i*n_starts*pitch*fraction_circle])
          thread_polyhedron ((diameter - taper*(z + i*n_starts*pitch*fraction_circle))/2,
                             pitch, internal, n_starts, thread_size, groove, square, rectangle, angle);
}

module thread_polyhedron (radius, pitch, internal, n_starts, thread_size,
                          groove, square, rectangle, angle)
{
   n_segments = segments (radius*2);
   fraction_circle = 1.0/n_segments;

   local_rectangle = rectangle ? rectangle : 1;

   h = (square || rectangle) ? thread_size*local_rectangle/2 : thread_size / (2 * tan(angle));
   outer_r = radius + (internal ? h/20 : 0);
   h_fac1 = (square || rectangle) ? 1.1 : 0.875;
   inner_r = radius - h*h_fac1;

   translate_y = groove ? outer_r + inner_r : 0;
   reflect_x   = groove ? 1 : 0;

   x_incr_outer = (! groove ? outer_r : inner_r) * fraction_circle * 2 * PI * 1.02;
   x_incr_inner = (! groove ? inner_r : outer_r) * fraction_circle * 2 * PI * 1.02;
   z_incr = n_starts * pitch * fraction_circle * 1.005;

   z0_outer = (outer_r - inner_r) * tan(angle);

   bottom = internal ? 0.235 : 0.25;
   top    = internal ? 0.765 : 0.75;

   translate ([0, translate_y, 0]) {
      mirror ([reflect_x, 0, 0]) {
         polyhedron (
           points = [
             [-x_incr_inner/2, -inner_r, 0],
             [x_incr_inner/2, -inner_r, z_incr],
             [x_incr_inner/2, -inner_r, thread_size + z_incr],
             [-x_incr_inner/2, -inner_r, thread_size],

             [-x_incr_outer/2, -outer_r, z0_outer],
             [x_incr_outer/2, -outer_r, z0_outer + z_incr],
             [x_incr_outer/2, -outer_r, thread_size - z0_outer + z_incr],
             [-x_incr_outer/2, -outer_r, thread_size - z0_outer]
           ],
           faces = [
             [0, 3, 7, 4],
             [1, 5, 6, 2],
             [0, 1, 2, 3],
             [4, 7, 6, 5],
             [7, 2, 6],
             [7, 3, 2],
             [0, 5, 1],
             [0, 4, 5]
           ]
         );
      }
   }
}