// =====================================================================
// Vessel cap + rod holder (single source file)
// Iterations are tracked in git, not as v2/v3 files.
//
// Parts:  CAP (seals + ports + GPI thread)  •  GASKET (silicone, seals only)
//         COLUMN / top stop (holds rods, sets depth, clamps the wires)
//
// PRINT ORIENTATIONS (both support-free - see view="print"):
//   CAP    : closed-top on the bed, mouth up.  Build dir = up toward mouth.
//   COLUMN : flush face on the bed, pegs up.    Build dir = up toward pegs.
// In the COLUMN model, "up" (+Z) is the bed side, so the clamp sits at the
// top face (lands ON the bed) and its nut pocket opens downward-in-use
// (= upward-in-print -> no bridge, no supports).
//
// Requires BOSL2.
// =====================================================================
include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// ---- options (choices listed inline) --------------------------------
view       = "print";      // "exploded" | "assembled" | "section" | "print"
part       = "all";        // "all" | "cap" | "column" | "gasket"
port_style = "ports";      // "ports" | "open"
seal       = "gasket";     // "gasket" | "oring"  - oring reproduces the original O-ring grooves
pieces     = 1;            // 2 = separate cap + top stop | 1 = one printed piece
ribs       = "no";         // "yes" | "no"  (grip ribs / knurling - "no" = smooth cap)
openings   = 1;            // 0 | 1 (front) | 2 (front+rear) - big gasket openings replacing the centre ports
wedge      = "sides";      // opening entrance, per opening: "max" (45deg V-wedge across the cap + the side-relief prow - as much material removed as printably possible) | "front" (front prow V only, vertical side walls) | "sides" (RECOMMENDED - prow V with side relief: front + left/right needle access) | "no" (vertical access only)
min_wall   = 0.84;         // mm wall kept between an opening and any port (2 strands @ 0.42 line width, 0.4 nozzle - PC-CF min)
opening_style = "fan";     // "fan" | "tilt" - fan: single graceful window in the ceiling (bounded by the vial throat + septum allowance), extruded straight up + a 45deg tunnel out the front; tilt: straight bore sheared by opening_tilt
opening_tilt = 62;         // deg - tilt of the opening wall above the cap (90 = vertical); pivots about the opening's front line on the cap top; "tilt" style only
layer_height    = 0.2;          // mm - PC-CF print layer height (set to your slicer's value)
guides     = [1,2,3,4,5];  // ports to add a tube guide on (1-based port indices; [0] = none; e.g. [1] or [1,2,3])
guide_height    = 3;            // mm - height of the guide section (above the cap for part="cap"; below the top-stop face otherwise)
guide_wall_multiple = 2;        // guide clearance beyond a port hole, as a multiple of min_wall

$fn = 72;
epsilon = 0.05;               // small epsilon (mm): tiny overlap so coincident faces leave no zero-thickness slivers in CSG booleans

// ---- rods & ports (the original cap's key counts + sizes) -----
rods      = 2;       // number of rods (0 or 2; the top-stop column is built for 2)
rod_diameter            = 6.2;     // rod diameter
num_ports         = 5;       // number of tube ports (auto-placed clear of the rods)
port_diameter          = 2.2;     // port diameter (OD of the 75mm tubes)
neck_inner_diameter         = 17;      // measured INTERNAL diameter of the glass vessel neck
neck_clearance      = 0.6;     // radial clearance kept between the glass and anything through the neck
rod_length          = 60;      // rod length (L)
rod_offset          = 4.8;     // offset from axis to each rod
insertion_depth = 23;      // g: protrusion below the cap bottom into the vessel

// ---- fits (point 8) -------------------------------------------------
cap_rod_clearance      = 0.15;       // friction fit in the CAP (snug - holds rod by friction)
insert_clearance = 0.30;       // EXTRA clearance in the COLUMN for easy insertion (bolts do the holding)
cap_bore = rod_diameter + cap_rod_clearance;                 // friction bore (also the lower bearing)
column_bore = rod_diameter + cap_rod_clearance + insert_clearance;  // easy-insert bore; total tracks cap_rod_clearance

// ---- cap ------------------------------------------------------------
cap_outer_diameter = 27; cap_height = 12.3; wall_thickness = 2;
rib_count = 84; rib_diameter = 0.856;   // number of grip ribs (when ribs=="yes")
// GPI 24-400 thread
thread_nominal_diameter = 24.30; thread_diameter_clearance = 0.50; pitch = 25.4/8; thread_starts = 1; lead_in_length = 0.6*pitch;
thread_major_diameter = thread_nominal_diameter + thread_diameter_clearance; thread_depth_radial = 0.3*pitch; thread_minor_diameter = thread_major_diameter - 2*thread_depth_radial;
// gasket + retaining ridge (point 9)
gasket_thickness = 2.0; gasket_diameter = 23.9; gasket_seat_diameter = 24.2;
ridge_inner_diameter = 22.5; ridge_height = 1.6;            // inward lip that keeps the gasket from dropping out
// O-ring seal (only used when seal=="oring"; reproduces the original)
cap_oring_thickness       = 1.7;   // mm - cap O-ring cross-section (dovetail groove in the bore wall)
rod_oring_thickness = 2.5;   // mm - rod O-ring cross-section
rod_port_relief    = 1.0;   // mm - rod port relief; also sets the rod O-ring id
rod_oring_diameter = rod_diameter - rod_port_relief/2 + rod_oring_thickness/2;
// closed-top thickness depends on the seal: 3 PC-CF layers is plenty to hold the GASKET
// down, but the O-RING needs a solid top to seat against, so in oring mode make the top
// at least the cap O-ring cross-section + 2 layers (~2.5mm with defaults).
top_thickness = (seal=="oring") ? max(cap_oring_thickness + 4*layer_height, 3*layer_height) : 3*layer_height;
// ports
cap_oring_diameter = 18.7706;
// ports on the largest circle whose TUBES still clear the glass neck bore
port_ring_radius = neck_inner_diameter/2 - port_diameter/2 - neck_clearance;
assert(2*(port_ring_radius + port_diameter/2) <= neck_inner_diameter - 2*neck_clearance + epsilon, "tube envelope too big for the vessel neck");
assert(2*(rod_offset + rod_diameter/2) <= neck_inner_diameter - 2*neck_clearance + epsilon, "rod envelope too big for the vessel neck");
// open gasket field
divider_half_width = 4.65; open_window_radius = cap_outer_diameter/2 - wall_thickness - 1.0; window_corner_radius = 2.0;
// poka-yoke FLANGE (pushed-out chord section):
// a chord-section of the cap is pushed straight out, so the outer edge keeps the cap
// curvature, the sides are straight, and the grip ribs continue along it.
flange_arc   = 93;      // deg - angular width of the pushed-out section
flange_push  = 3.5;     // mm - radial push
flange_angle = 180;       // deg - ROTATE the poka-yoke around the cap (0 = +X side; 90 = front; -90 = rear; etc.)
tab_fillet_radius    = 2.5;     // fillet at the flange/cap junction

// ---- registration pegs ---------------------------------------------
peg_diameter = 3; peg_offset = 2; peg_clearance = 0.3; peg_height = top_thickness;   // flush with the cap inside ceiling

// ---- column + clamp -------------------------------------------------
// journal wall around each rod, capped so the racetrack sides clear the ring-port tubes
rod_column_radius = min(rod_diameter/2 + 1.8, port_ring_radius*sin(60) - port_diameter/2 - 0.15);
m3bolt_clearance = 3.4;        // M3 bolt clearance-hole diameter
nut_across_flats      = 5.9;        // M3 nut width across flats (spanner size)
nut_thickness         = 2.8;
nut_across_corners    = nut_across_flats/cos(30);  // nut point-to-point diameter
clamp_inner_wall  = 1.8; clamp_outer_wall = 2.2;          // robust PC-CF walls
// 1-piece build

column_height  = rod_length - insertion_depth - cap_height; // sets the insertion depth
top_face_z  = cap_height + column_height;                     // rod flush face
bore_edge_x     = rod_offset + column_bore/2;               // bore outer edge
nut_pocket_x0 = bore_edge_x + clamp_inner_wall; nut_pocket_x1 = nut_pocket_x0 + nut_thickness; clamp_outer_x = nut_pocket_x1 + clamp_outer_wall;
// the top stop's top face is ONE rounded rectangle (long faces flush with the racetrack)
clamp_height = 8; clamp_width = 2*rod_column_radius; clamp_corner_radius = 3;
bolt_axis_z     = top_face_z - 4;                         // bolt axis, near the top face
gasket_z = cap_height - top_thickness - gasket_thickness;
bore_ceiling_z = cap_height - top_thickness - (seal=="gasket" ? gasket_thickness : 0);   // bore ceiling: leave the gasket slab only for the gasket seal

color_cap=[0.78,0.87,0.97]; color_gasket=[0.74,0.62,0.92]; color_column=[1,0.83,0.58];
color_steel=[0.72,0.74,0.78]; color_vessel=[0.55,0.88,0.78,0.32];

// ---- helpers --------------------------------------------------------
module racetrack(h,r) hull() for(s=[-1,1]) translate([s*rod_offset,0,0]) cylinder(r=r,h=h);

// poka-yoke flange outline: a chord-section of the cap hull'd with itself pushed out
module flange2d() {
  R = cap_outer_diameter/2; cd = R*cos(flange_arc/2);
  rotate(flange_angle) hull() for (dx=[0, flange_push])
    translate([dx,0]) intersection() {
      circle(r=R, $fn=180);
      translate([cd+R,0]) square([2*R, 4*R], center=true);
    }
}
module body2d() offset(r=tab_fillet_radius) offset(r=-tab_fillet_radius) union() {   // cap outline + flange
  circle(d=cap_outer_diameter, $fn=160);
  flange2d();
}
// grip ribs continued along the pushed flange edge (arc + the two straight sides)
module flange_ribs() {
  R = cap_outer_diameter/2; ha = flange_arc/2;
  px = flange_push*cos(flange_angle); py = flange_push*sin(flange_angle);
  rib_step = 360/rib_count;
  n_arc = max(1, floor(flange_arc/rib_step));
  for (k=[0:n_arc]) {
    th = flange_angle - ha + k*flange_arc/n_arc;
    translate([R*cos(th)+px, R*sin(th)+py, 0]) cylinder(d=rib_diameter, h=cap_height);
  }
  n_side = max(1, round(flange_push/(rib_step*PI/180*R)));
  for (s=[-1,1]) for (m=[0:n_side]) {
    th = flange_angle + s*ha; t = m/n_side;
    translate([R*cos(th)+t*px, R*sin(th)+t*py, 0]) cylinder(d=rib_diameter, h=cap_height);
  }
}

// tube port positions (2D), num_ports placed clear of the rods - the
// original Vessel Cap.scad placement logic
module port_holes2d() {
  R = port_ring_radius;
  if (num_ports > 0) {
    if (rods == 0 || rod_offset == 0)
      for (i=[0:num_ports-1]) rotate(i*360/num_ports) translate([R,0]) circle(d=port_diameter,$fn=24);
    else if (num_ports < 3)
      for (j=[0:num_ports-1]) rotate(90+j*360/num_ports) translate([R,0]) circle(d=port_diameter,$fn=24);
    else {
      ring_ports = (num_ports < 4) ? num_ports : 4;
      for (k=[0:2+ring_ports-1]) rotate(k*360/6) translate([R,0]) if (k==0||k==3) {} else circle(d=port_diameter,$fn=24);
    }
  }
  n_centre = (num_ports > 4) ? min(num_ports-4, 2-openings) : 0;          // centre ports that still fit beside the opening(s)
  for (k=[0:n_centre-1]) rotate(90+(openings+k)*180) translate([R,0]) circle(d=port_diameter,$fn=24);  // placed opposite the opening(s)
}

// big gasket openings that replace the centre port(s): expand to fill the open-window
// region on that side, but stop min_wall short of every remaining port.
// ---- ceiling window (the "fan") -------------------------------------
// The CEILING is the slab underside that clamps the septum onto the glass rim
// (ceiling_z). The window's outer arc there = vessel throat + septum thickness + one
// layer, so a syringe sliding down the 45deg entrance wall crosses the septum top at
// the arc and passes the glass edge with exactly the one-layer allowance.
ceiling_z  = cap_height - top_thickness;                 // slab underside = septum top
ceiling_window_radius  = neck_inner_diameter/2 + gasket_thickness + layer_height;   // window arc radius AT the ceiling
tower_radius = port_diameter/2 + min_wall;            // tube-channel keep-out around each flanking port
tower_front_y = port_ring_radius*sin(60) + tower_radius;  // the keep-outs' front line

// the ceiling window, built for the FRONT and mirrored for the rear: one graceful
// shape, never wider than the tower centrelines. Rear = an arc tangent to both tower
// clearances, kissing the spine line (behind the tower centres it stays inside their
// closest points and closes in that arc). Middle = the strip between the centrelines,
// hugging the tower keep-outs. Front = the graze arc. A morphological OPENING
// (erode-dilate) removes every cusp so all joins are tangent - the tower clearances
// are keep-out zones, not visible cylinders.
module opening_front2d() {
  px = port_ring_radius*cos(60); py = port_ring_radius*sin(60);               // flanking port centres at (+-px, py)
  t  = min(window_corner_radius, port_ring_radius*sin(30) - tower_radius - 0.05);   // smoothing radius, under the tower-gap half-waist
  K  = (tower_radius - 0.05) - divider_half_width;                       // 0.05 INTO the keep-outs: exact tangency is a
  c  = (port_ring_radius*port_ring_radius - K*K) / (2*(py + K));              // non-manifold touch-point; the bites re-cut the
                                                          // overlap and the opening rounds the join
  offset(r=t) offset(r=-t)
  difference() {
    union() {
      translate([0,c]) circle(r=c-divider_half_width, $fn=90);      // rear closing arc
      intersection() {                                    // centreline strip out to the graze arc
        circle(r=ceiling_window_radius, $fn=140);
        translate([-px, py]) square([2*px, 2*cap_outer_diameter]);
      }
    }
    for (s=[-1,1]) translate([s*px, py]) circle(r=tower_radius, $fn=48);  // tower keep-outs
  }
}
module opening_one2d(sy) {
  if (sy>0) opening_front2d();
  else mirror([0,1]) opening_front2d();
}
module openings2d() {
  if (openings > 0) for (sy = (openings>=2) ? [1,-1] : [1]) opening_one2d(sy);
}
// the openings bored UP through the funnel, each tilted by opening_tilt: a shear in the
// opening's radial direction, pivoting about z=cap_height (the cap top) - so at the cap face the
// footprint is unchanged (the front line stays) and the wall leans above it. 90 = vertical.
module opening_bore_tilted() {
  k = cos(opening_tilt) / sin(opening_tilt);              // horizontal run per unit rise (0 at 90deg)
  if (openings > 0) for (sy = (openings>=2) ? [1,-1] : [1])
    multmatrix([[1,0,0,0],[0,1,sy*k,-sy*k*cap_height],[0,0,1,0],[0,0,0,1]])   // shear Y by sy*k*(z-cap_height)
      translate([0,0,cap_height-epsilon]) linear_extrude(top_face_z-cap_height+5) opening_one2d(sy);
}
// the openings swept for needle access from vertical (parallel with the column) down
// to 45deg tilted away from it: rear and side walls stay vertical, the front wall is a
// smooth 45deg shear. Built as (footprint swept forward, vertical prism) INTERSECT
// (footprint swept rearward, prism sheared 45deg forward): the cross-section at height
// h is the footprint stretched forward by h - no steps, every face vertical or 45deg,
// both native to the flipped print. The flanking tube channels keep their min_wall
// towers full-height (they fuse with the column face, so they print anchored).
// the opening cut (front side; mirrored for the rear):
//  - SHAFT: the window extruded straight up. The cavity IS the window shape at every
//    height, so the tower keep-outs read as the window's own waist arcs.
//  - TUNNEL: a 45deg-rising slot from the window's front arc out through the funnel
//    face, giving the 45deg syringe path. Its floor carries a shallow V across the
//    width (prow_floor_slope): the crest where it daylights through the sloping funnel skin
//    then RISES at >=45deg from the centre to the swath walls - anchored at both
//    ends, printable - instead of hanging as a horizontal ridge. The funnel toe
//    under the floor stays, keeping the cap rim's print support; the slot's side
//    walls are vertical planes at the tower centrelines, whose skin crossings are
//    steep by construction.
prow_floor_slope = 1.9;   // prow floor slope across the width; >=1.64 keeps the daylight crest at >=45deg.
                // The prow faces themselves rise at atan(prow_floor_slope) ~ 62deg sideways, so they ARE
                // the side relief once nothing truncates them.
side_wall_slope = 3.4;   // outer side-wall steepness (rise/run, ~74deg): shallower and the wall's own
                // daylight crest through the funnel skin dips below 45deg near the rear corner
module tunnel_front() {
  B = 6*cap_outer_diameter; px = port_ring_radius*cos(60);
  if (wedge=="front") {
    // front-only prow slot: crowned, vertical side walls, no side relief
    tw = (ceiling_window_radius - divider_half_width - 0.7)/prow_floor_slope;   // end at a ~0.7mm side wall, before the
    intersection() {                         // floor meets the crown (no feather pinch)
      multmatrix([[1,0,0,0],[0,1,0,0],[ prow_floor_slope,1,1, ceiling_z-ceiling_window_radius],[0,0,0,1]])
        translate([-B/2,-B/2,0]) cube(B);
      multmatrix([[1,0,0,0],[0,1,0,0],[-prow_floor_slope,1,1, ceiling_z-ceiling_window_radius],[0,0,0,1]])
        translate([-B/2,-B/2,0]) cube(B);
      multmatrix([[1,0,0,0],[0,1,0,0],[0,1,1, ceiling_z-divider_half_width],[0,0,0,1]])   // crown: z <= ceiling_z + (y-divider_half_width)
        translate([-B/2,-B/2,-B]) cube(B);
      translate([-tw, ceiling_window_radius-1, ceiling_z-0.2]) cube([2*tw, B/2, B/2]);
      translate([0,0,ceiling_z-0.2]) cylinder(r1=ceiling_window_radius-0.3, r2=ceiling_window_radius-0.3+B, h=B, $fn=140);
    }
  } else intersection() {                    // "sides" / "max": prow V with side relief
    // prow floor: z >= ceiling_z + (y-ceiling_window_radius) + prow_floor_slope*|x|  (one half-space per side of the V)
    multmatrix([[1,0,0,0],[0,1,0,0],[ prow_floor_slope,1,1, ceiling_z-ceiling_window_radius],[0,0,0,1]])
      translate([-B/2,-B/2,0]) cube(B);
    multmatrix([[1,0,0,0],[0,1,0,0],[-prow_floor_slope,1,1, ceiling_z-ceiling_window_radius],[0,0,0,1]])
      translate([-B/2,-B/2,0]) cube(B);
    // leaning outer side walls: |x| <= px + (z - ceiling_z)/side_wall_slope
    multmatrix([[1,0,1/side_wall_slope, px - ceiling_z/side_wall_slope],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
      translate([-B,-B/2,-B/2]) cube(B);
    mirror([1,0,0]) multmatrix([[1,0,1/side_wall_slope, px - ceiling_z/side_wall_slope],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
      translate([-B,-B/2,-B/2]) cube(B);
    // rear bound: vertical plane at the keep-outs' front line, pushed 0.2 into them
    // (an exactly tangent plane is a non-manifold touch-line; the keep-outs re-cut it)
    translate([-B/2, tower_front_y-0.2, ceiling_z-0.5]) cube(B);
    // radial 45deg bound from the window arc (started 0.1 inside it, so it crosses the
    // shaft wall instead of kissing it): tapers the slab's window edge and never
    // pierces the ceiling beyond it - no flat ledge anywhere on the ring
    translate([0,0,ceiling_z-0.2]) cylinder(r1=ceiling_window_radius-0.3, r2=ceiling_window_radius-0.3+B, h=B, $fn=140);
  }
}
module opening_cut_front() {
  H = top_face_z - ceiling_z;
  difference() {
    union() {
      translate([0,0,ceiling_z-0.3]) linear_extrude(H+0.3) opening_front2d();
      if (wedge!="no") tunnel_front();                    // "no" = the vertical shaft only
    }
    for (s=[-1,1]) translate([s*port_ring_radius*cos(60), port_ring_radius*sin(60), ceiling_z-0.4])
      cylinder(r=tower_radius-0.02, h=H+1, $fn=48);            // tube-channel keep-outs (a hair under
                                                          // the window bites, so the shaft's bite
                                                          // walls are never re-cut coincidentally)
  }
}
module opening_fan() {
  if (openings > 0) for (sy = (openings>=2) ? [1,-1] : [1]) {
    if (sy>0) opening_cut_front();
    else mirror([0,1,0]) opening_cut_front();
  }
}

// teardrop hole, axis +X, apex toward -Z (= up in print -> self-supporting)
module teardrop_x(d,len){ r=d/2; hull(){ rotate([0,90,0]) cylinder(r=r,h=len);
  translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01,h=len,$fn=6);} }

// gasket retaining ridge: triangular barb (both faces <=45deg from vertical)
module gasket_ridge() rotate_extrude($fn=140)
  polygon([[gasket_seat_diameter/2, gasket_z+0.05],
           [ridge_inner_diameter/2,    gasket_z-ridge_height/2],
           [gasket_seat_diameter/2, gasket_z-ridge_height]]);

// O-ring dovetail profile - retains the O-ring in its groove
module dovetail(top) {
  bottom = top + 0.3; thickness = 1;
  polygon(points=[[0,0],[bottom,0],[top+0.15,thickness],[0.15,thickness]]);
}

// the whole top-stop top face = one rounded rectangle
module clampband2d() offset(r=clamp_corner_radius) square([2*clamp_outer_x-2*clamp_corner_radius, clamp_width-2*clamp_corner_radius], center=true);

// ---- tube guides --------------------------------------------------
function lsum(v,i=0) = i >= len(v) ? 0 : v[i] + lsum(v,i+1);
// the tube port centres, in the same order port_holes2d() places them (1-based
// in `guides`). Assumes the standard layout (num_ports>=3, rods at 0/180).
function guide_pts() = let(
  R  = port_ring_radius,
  rp = (num_ports < 4) ? num_ports : 4,
  ring = [for (k=[0:2+rp-1]) if (k!=0 && k!=3) [R*cos(k*60), R*sin(k*60)]],
  nc = (num_ports > 4) ? min(num_ports-4, 2-openings) : 0,
  cen = (nc>0) ? [for (k=[0:nc-1]) [R*cos(90+(openings+k)*180), R*sin(90+(openings+k)*180)]] : []
) concat(ring, cen);
// guide section on the cap top: hemispherical-topped tower per individual port, OR one
// semicircle (centred on the ports' layout centre) when the selected ports all sit on one
// side. Either way it stands guide_height tall and clears the ports by min_wall. Port holes are
// bored through it by cap()'s extended port cut.
selected_guides = [for (g=guides) if (g>=1 && g<=len(guide_pts())) g];
module guides_solid() {
  pts = [for (g=selected_guides) guide_pts()[g-1]];
  rg  = port_diameter/2 + min_wall;
  if (len(pts) > 0) {
    bis  = atan2(lsum([for(p=pts) p[1]]), lsum([for(p=pts) p[0]]));     // mean direction of the picks
    span = (len(pts)<2) ? 0 : max([for(p=pts) abs(((atan2(p[1],p[0]) - bis + 540) % 360) - 180)]);
    if (len(pts) > 1 && span <= 90)                                     // full set on one side -> semicircle
      translate([0,0,cap_height]) linear_extrude(guide_height)
        rotate(bis) intersection() {
          circle(r = port_ring_radius + port_diameter/2 + min_wall, $fn=140);
          translate([0,-cap_outer_diameter]) square([cap_outer_diameter, 2*cap_outer_diameter]);            // keep the bisector half (x>=0)
        }
    else                                                                // individual ports -> domed towers
      for (p=pts) translate([p[0],p[1],cap_height]) {
        cylinder(r=rg, h=max(epsilon, guide_height-rg), $fn=48);
        translate([0,0,max(0, guide_height-rg)]) sphere(r=rg, $fn=48);
      }
  }
}

// guides at the TOP-STOP top face (z=top_face_z), extending guide_height DOWN (= up from the bed when
// printed top-stop-down). Ports near an opening -> a semicircle each (flat toward centre);
// the rest (the uninterrupted back) -> ONE semicircle (half-disc from the centre, so it
// merges with the top stop - no gap). Both clear the holes by guide_wall_multiple*min_wall; the
// port channels are bored through by holder1().
function near_open(p) = let(og = concat(openings>=1 ? [90] : [], openings>=2 ? [270] : []))
  len(og)>0 && min([for(o=og) abs(((atan2(p[1],p[0])-o+540)%360)-180)]) <= 45;
module guides_topstop() {
  pts = [for (g=selected_guides) guide_pts()[g-1]];
  if (len(pts) > 0) {
    gxw = guide_wall_multiple * min_wall;
    front = [for (p=pts) if (near_open(p)) p];
    back  = [for (p=pts) if (!near_open(p)) p];
    translate([0,0,top_face_z-guide_height]) linear_extrude(guide_height) {
      if (len(back) > 0) {                                            // back: one semicircle, clipped to BEYOND the
        bis = atan2(lsum([for(p=back) p[1]]), lsum([for(p=back) p[0]]));   // top-stop long edge (so it doesn't block
        rotate(bis) intersection() {                                      // the rods/clamp, and seats on the edge)
          circle(r = port_ring_radius + port_diameter/2 + gxw, $fn=140);
          translate([clamp_width/2, -cap_outer_diameter]) square([cap_outer_diameter, 2*cap_outer_diameter]);  // keep local x > clamp_width/2 (past the edge)
        }
      }
      for (p=front) {                                                // front: a semicircle per port, seated on the
        sy = (p[1] >= 0) ? 1 : -1;                                    // near long edge (flush, no longer floating)
        ey = sy * clamp_width/2;
        Rf = abs(p[1] - ey) + port_diameter/2 + gxw;
        translate([p[0], ey]) intersection() {
          circle(r=Rf, $fn=64);
          translate([-Rf, sy>0 ? 0 : -Rf]) square([2*Rf, Rf]);       // the half bulging out toward the port
        }
      }
    }
  }
}

// ---- parts ----------------------------------------------------------
module cap() color(color_cap) difference() {
  union() {
    difference() {                                   // body (with knurl) minus the core bore
      union() {
        linear_extrude(cap_height) body2d();
        if (ribs=="yes" && rib_count>0) {
          for (i=[0:rib_count-1]) {                             // body ribs, skipped in the flange sector
            a = i*360/rib_count; da = abs(((a-flange_angle+540)%360)-180);
            if (da >= flange_arc/2) rotate([0,0,a]) translate([cap_outer_diameter/2,0,0]) cylinder(d=rib_diameter,h=cap_height);
          }
          flange_ribs();                                        // ribs continued along the flange
        }
      }
      translate([0,0,-epsilon]) cylinder(d=thread_nominal_diameter, h=bore_ceiling_z+epsilon);
    }
    // internal GPI thread (added back inside the bore)
    translate([0,0,pitch/2])
      thread_helix(d=thread_minor_diameter, pitch=pitch, turns=(bore_ceiling_z-pitch)/pitch,
                   thread_depth=thread_depth_radial, flank_angle=30, starts=thread_starts,
                   anchor=BOTTOM, lead_in=lead_in_length, internal=true);
    if (seal=="gasket") gasket_ridge();              // lip that retains the gasket
    if (part=="cap") color(color_cap) guides_solid();    // cap-top guides only when viewing the cap alone
  }
  // smooth gasket seat under the closed top (gasket seal only)
  if (seal=="gasket") translate([0,0,gasket_z]) cylinder(d=gasket_seat_diameter, h=gasket_thickness+epsilon);
  // cap O-ring groove in the bore wall, near the closed top (oring seal only)
  if (seal=="oring")
    translate([0,0,bore_ceiling_z]) mirror([0,0,1]) rotate_extrude($fn=100)
      translate([(cap_oring_diameter+cap_oring_thickness)/2, 0, 0]) dovetail(cap_oring_thickness);
  // rod bores (friction bore for gasket; looser port + O-ring groove for oring)
  if (rods>0) for (i=[0:rods-1]) rotate([0,0,i*360/rods]) translate([rod_offset,0,0]) {
    translate([0,0,-epsilon]) cylinder(d = (seal=="oring") ? rod_diameter+cap_rod_clearance+rod_port_relief : cap_bore, h=cap_height+2*epsilon);
    if (seal=="oring")
      translate([0,0,bore_ceiling_z-rod_oring_thickness]) rotate_extrude($fn=100)
        translate([rod_oring_diameter/2, 0, 0]) circle(d=rod_oring_thickness, $fn=64);
  }
  // peg holes (through the closed top only) - 2-piece only; the 1-piece is fused, no pegs
  if (pieces==2) for (s=[-1,1]) translate([0,s*peg_offset,cap_height-top_thickness-epsilon]) cylinder(d=peg_diameter+peg_clearance, h=top_thickness+2*epsilon);
  // ports OR an open gasket field (full-width spine, rounded window corners)
  if (port_style=="ports") {
    translate([0,0,-epsilon])
      linear_extrude(cap_height + (len(selected_guides)>0 ? guide_height : 0) + 2*epsilon) port_holes2d();  // ports bored through any guide too
    if (opening_style=="fan") opening_fan();              // same tapered cut as the holder - windows always match
    else translate([0,0,-epsilon]) linear_extrude(cap_height+2*epsilon) openings2d();
  }
  else
    translate([0,0,cap_height-top_thickness-epsilon]) linear_extrude(top_thickness+2*epsilon)
      offset(r=window_corner_radius) offset(r=-window_corner_radius) difference() {   // OPENING -> rounds the window's convex corners
        circle(r=open_window_radius, $fn=140);
        square([2*cap_outer_diameter, 2*divider_half_width], center=true);   // spine spans the full width
      }
}

module gasket() color(color_gasket) translate([0,0,gasket_z]) difference() {
  cylinder(d=gasket_diameter, h=gasket_thickness, $fn=96);
  for (s=[-1,1]) translate([s*rod_offset,0,-epsilon]) cylinder(d=rod_diameter-0.4, h=gasket_thickness+2*epsilon);
}

module column() color(color_column) difference() {
  union() {
    translate([0,0,cap_height]) racetrack(column_height, rod_column_radius);
    translate([0,0,top_face_z-clamp_height]) linear_extrude(clamp_height) clampband2d();   // single rounded-rect top
    if (pieces==2) for (s=[-1,1]) translate([0,s*peg_offset,cap_height]) rotate([180,0,0]) cylinder(d=peg_diameter, h=peg_height);  // pegs (2-piece only)
  }
  for (s=[-1,1]) translate([s*rod_offset,0,cap_height-epsilon]) cylinder(d=column_bore, h=column_height+2*epsilon);  // journal bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from the outer face in to pinch the wire on the rod
    translate([rod_offset+rod_diameter/2-0.4, 0, bolt_axis_z]) teardrop_x(m3bolt_clearance, clamp_outer_x-(rod_offset+rod_diameter/2)+0.9);
    // captive nut: pocket opens at the band BOTTOM (down-in-use = up-in-print, no bridge);
    // width = across-flats so it can't rotate; inner+outer walls trap it along the bolt
    translate([nut_pocket_x0, -nut_across_flats/2, top_face_z-clamp_height-epsilon]) cube([nut_thickness, nut_across_flats, (bolt_axis_z+nut_across_corners/2)-(top_face_z-clamp_height)+epsilon]);
    // wire guide slot, top face down to the bolt
    translate([rod_offset+rod_diameter/2-0.4, -0.9, bolt_axis_z]) cube([1.5,1.8, top_face_z-bolt_axis_z+epsilon]);
  }
}

module vessel() color(color_vessel) translate([0,0,-38]) difference() {   // neck bore modelled so
  cylinder(d=cap_outer_diameter-2*wall_thickness-1.2, h=38+gasket_z+epsilon);                    // section view shows the
  translate([0,0,2]) cylinder(d=neck_inner_diameter, h=38+gasket_z);                 // through-neck clearance
}
module rods() color(color_steel) for(s=[-1,1]) translate([s*rod_offset,0,top_face_z-rod_length]) cylinder(d=rod_diameter,h=rod_length);

// ===== 1-piece construction =====
// Uses the REAL cap (set port_style="open") so the thread, gasket seat and
// gasket-holding structure stay.
// The connector is now a SOLID funnel covering the FULL circumference: it runs
// from the cap outline (incl. the poka-yoke) all the way down to the racetrack.
// Every layer is a ring no bigger than the one below it (<=45deg overhang), so
// NOTHING starts in mid-air - both sides and front/rear all land on the
// racetrack. funnel_height is taller than the cap overhang so the slope is steeper
// than 45deg everywhere (i.e. the connection starts lower down the print).
funnel_height = 14;                                        // > cap_outer_diameter/2 - rod_column_radius (8.7) => steeper than 45deg
join_z   = cap_height + funnel_height;
module rt_outline2d() hull() for(s=[-1,1]) translate([s*rod_offset,0]) circle(r=rod_column_radius, $fn=48);

// the cap's port openings (matches cap()'s port_style) - used to bore straight up
module ports2d() {
  if (port_style=="ports")
    { port_holes2d(); openings2d(); }
  else
    offset(r=window_corner_radius) offset(r=-window_corner_radius) difference() {
      circle(r=open_window_radius, $fn=140);
      square([2*cap_outer_diameter, 2*divider_half_width], center=true);
    }
}

module holder1() {
  difference() {
    union() {
      difference() {
        union() {
          cap();                                      // real cap (thread + open spine + gasket)
          // solid funnel: cap rim (+poka-yoke) -> racetrack, then clipped to the cap/poka-yoke
          // footprint extruded straight up, so the hull can't bulge out past the flange join
          // (removes the overhang above where the poka-yoke meets the round cap).
          color(color_column) intersection() {
            hull() {
              translate([0,0,cap_height-0.05]) linear_extrude(0.1) body2d();
              translate([0,0,join_z])     linear_extrude(0.1) rt_outline2d();
            }
            translate([0,0,cap_height]) linear_extrude(join_z-cap_height+1) body2d();
          }
        }
        // (1) the big 45deg V-wedge across the cap (wedge=="max" only), on top of the
        // prow cuts: apex line on the CAP SURFACE (x=0, z=cap_height), faces rising
        // up-and-out at 45deg, 5mm central spine left uncut.
        // openings=1 -> front only; openings=2 -> front+rear.
        if (wedge=="max" && openings > 0)
          difference() {
            rotate([90,0,0]) linear_extrude(height=cap_outer_diameter*3, center=true)
              polygon([[0,cap_height],[60,cap_height+60],[60,300],[-60,300],[-60,cap_height+60]]);
            translate([-cap_outer_diameter, -2.5, -50]) cube([2*cap_outer_diameter, 5, 400]);              // the 5mm spine stays
            if (openings < 2)                                                       // 1 opening -> keep the rear solid
              translate([-cap_outer_diameter, -cap_outer_diameter-2.5, -50]) cube([2*cap_outer_diameter, cap_outer_diameter, 400]);
          }
        // (2) gasket-access openings - flared or tilted per opening_style (open window in
        // "open" style) - cut HERE, before the column is unioned in, so they never carve it
        if (port_style=="ports") {
          if (opening_style=="fan") opening_fan();
          else opening_bore_tilted();
        } else translate([0,0,cap_height-top_thickness-epsilon]) linear_extrude(top_face_z-(cap_height-top_thickness)+5) ports2d();
      }
      column();                                       // re-added whole: untouched by the wedge/openings
      color(color_column) guides_topstop();                 // added after the wedge cuts so the front ones survive
    }
    // (3) tube channels: full circles cut through EVERYTHING they cross (funnel, column
    // wall, clamp band, guides) so the bore stays round all the way down
    translate([0,0,cap_height-top_thickness-epsilon]) linear_extrude(top_face_z-(cap_height-top_thickness)+5) port_holes2d();
    // (4) keep the rod path clear: the funnel/spine fills the bore line, so
    // bore the two rod holes straight through it (ramp/spine only OUTSIDE the bores;
    // +0.02 so this never coincides exactly with the column's own journal bores)
    for (s=[-1,1]) translate([s*rod_offset,0,-epsilon]) cylinder(d=column_bore+0.02, h=top_face_z+5, $fn=48);
  }
}

// ---- assembly / views ----------------------------------------------
explode = (view=="exploded") ? 1 : 0;

module holder() {
  if (pieces==1) holder1();                // open-neck single piece
  else { cap(); translate([0,0,explode*42]) column(); }
}

module assembly() {
  translate([0,0,-explode*38]) vessel();
  if (seal=="gasket") translate([0,0,-explode*17]) gasket();   // no gasket in oring mode
  holder();
  translate([0,0,explode*18]) rods();
}

if (part=="cap") cap();
else if (part=="column") translate([0,0,-cap_height]) column();
else if (part=="gasket") translate([0,0,-gasket_z]) gasket();
else if (view=="section") difference(){ assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view=="print") {
  if (pieces==1) translate([0,0,top_face_z]) rotate([180,0,0]) holder();   // whole holder, flush face on bed
  else {
    translate([-18,0,cap_height]) rotate([180,0,0]) cap();                 // closed-top on bed
    translate([ 20,0,top_face_z]) rotate([180,0,0]) column();              // flush-face on bed, pegs up
  }
} else assembly();
