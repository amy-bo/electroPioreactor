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
layer_h    = 0.2;          // mm - PC-CF print layer height (set to your slicer's value)
guides     = [1,2,3,4,5];  // ports to add a tube guide on (1-based port indices; [0] = none; e.g. [1] or [1,2,3])
guide_h    = 3;            // mm - height of the guide section (above the cap for part="cap"; below the top-stop face otherwise)
guidexmin_wall = 2;        // guide clearance beyond a port hole, as a multiple of min_wall

$fn = 72;
eps = 0.05;

// ---- rods & ports (the original cap's key counts + sizes) -----
rods      = 2;       // number of rods (0 or 2; the top-stop column is built for 2)
rod_d            = 6.2;     // rod diameter
n_ports         = 5;       // number of tube ports (auto-placed clear of the rods)
port_d          = 2.2;     // port diameter - sized for Pioreactor v1.5 (Vial Cap S) stainless
                           // luer-lock NEEDLES, not the older 3.175mm silicone tubes. 2.2 takes
                           // a needle shaft up to ~14G (2.11mm OD); hub sits above the cap.
neck_id         = 17;      // measured INTERNAL diameter of the glass vessel neck
neck_clear      = 0.6;     // radial clearance kept between the glass and anything through the neck
rod_len          = 60;      // rod length (L)
rod_off          = 4.8;     // offset from axis to each rod
insertion_depth = 23;      // g: protrusion below the cap bottom into the vessel

// ---- fits (point 8) -------------------------------------------------
cap_fit      = 0.15;       // friction fit in the CAP (snug - holds rod by friction)
insert_extra = 0.30;       // EXTRA clearance in the COLUMN for easy insertion (bolts do the holding)
cap_bore = rod_d + cap_fit;                 // friction bore (also the lower bearing)
col_bore = rod_d + cap_fit + insert_extra;  // easy-insert bore; total tracks cap_fit

// ---- cap ------------------------------------------------------------
cap_od = 27; cap_h = 12.3; wall_t = 2;
rib_count = 84; rib_d = 0.856;   // number of grip ribs (when ribs=="yes")
// GPI 24-400 thread
T_nom = 24.30; dia_clear = 0.50; pitch = 25.4/8; starts = 1; leadin_len = 0.6*pitch;
D_maj_int = T_nom + dia_clear; depth_rad = 0.3*pitch; D_minor_int = D_maj_int - 2*depth_rad;
// gasket + retaining ridge (point 9)
gask_t = 2.0; gask_d = 23.9; gask_seat_d = 24.2;
ridge_id = 22.5; ridge_h = 1.6;            // inward lip that keeps the gasket from dropping out
// O-ring seal (only used when seal=="oring"; reproduces the original)
cap_o_ring_cs       = 1.7;   // mm - cap O-ring cross-section (dovetail groove in the bore wall)
rod_o_ring_cs = 2.5;   // mm - rod O-ring cross-section
rod_cutout    = 1.0;   // mm - rod port relief; also sets the rod O-ring id
rod_o_ring_id = rod_d - rod_cutout/2 + rod_o_ring_cs/2;
// closed-top thickness depends on the seal: 3 PC-CF layers is plenty to hold the GASKET
// down, but the O-RING needs a solid top to seat against, so in oring mode make the top
// at least the cap O-ring cross-section + 2 layers (~2.5mm with defaults).
top_th = (seal=="oring") ? max(cap_o_ring_cs + 4*layer_h, 3*layer_h) : 3*layer_h;
// ports
cap_o_ring_id = 18.7706;
// ports on the largest circle whose TUBES still clear the glass neck bore
port_R = neck_id/2 - port_d/2 - neck_clear;
// port_R is DEFINED to satisfy the tube envelope, so checking it against the neck is a
// tautology; the real failure mode is the neck being too small to hold the ring at all.
assert(port_R > port_d/2, "vessel neck too small for a needle port ring");
assert(2*(rod_off + rod_d/2) <= neck_id - 2*neck_clear + eps, "rod envelope too big for the vessel neck");
// open gasket field
spine_hw = 4.65; R_open = cap_od/2 - wall_t - 1.0; win_round = 2.0;
// poka-yoke FLANGE (pushed-out chord section):
// a chord-section of the cap is pushed straight out, so the outer edge keeps the cap
// curvature, the sides are straight, and the grip ribs continue along it.
flange_arc   = 93;      // deg - angular width of the pushed-out section
flange_push  = 3.5;     // mm - radial push
flange_angle = 180;       // deg - ROTATE the poka-yoke around the cap (0 = +X side; 90 = front; -90 = rear; etc.)
tab_round    = 2.5;     // fillet at the flange/cap junction

// ---- registration pegs ---------------------------------------------
peg_d = 3; peg_off = 2; peg_clear = 0.3; peg_h = top_th;   // flush with the cap inside ceiling

// ---- column + clamp -------------------------------------------------
// journal wall around each rod, capped so the racetrack sides clear the ring-port tubes
bearing_r = min(rod_d/2 + 1.8, port_R*sin(60) - port_d/2 - 0.15);
m3_bolt   = 3.4; nut_af = 5.9; nut_th = 2.8; nut_ac = nut_af/cos(30);
clamp_in  = 1.8; clamp_out = 2.2;          // robust PC-CF walls
// 1-piece build
cap_R   = cap_od/2;                // flange_angle (above) sets the poka-yoke position; 0 = +X rises with a side ramp

col_h  = rod_len - insertion_depth - cap_h; // sets the insertion depth
H_top  = cap_h + col_h;                     // rod flush face
xe     = rod_off + col_bore/2;               // bore outer edge
x_nut0 = xe + clamp_in; x_nut1 = x_nut0 + nut_th; x_out = x_nut1 + clamp_out;
// the top stop's top face is ONE rounded rectangle (long faces flush with the racetrack)
clamp_h = 8; clamp_W = 2*bearing_r; clamp_corner = 3;
zc     = H_top - 4;                         // bolt axis, near the top face
gask_z = cap_h - top_th - gask_t;
bore_top = cap_h - top_th - (seal=="gasket" ? gask_t : 0);   // bore ceiling: leave the gasket slab only for the gasket seal

C_CAP=[0.78,0.87,0.97]; C_GASKET=[0.74,0.62,0.92]; C_CARR=[1,0.83,0.58];
C_STEEL=[0.72,0.74,0.78]; C_VESSEL=[0.55,0.88,0.78,0.32];

// ---- helpers --------------------------------------------------------
module racetrack(h,r) hull() for(s=[-1,1]) translate([s*rod_off,0,0]) cylinder(r=r,h=h);

// poka-yoke flange outline: a chord-section of the cap hull'd with itself pushed out
module flange2d() {
  R = cap_od/2; cd = R*cos(flange_arc/2);
  rotate(flange_angle) hull() for (dx=[0, flange_push])
    translate([dx,0]) intersection() {
      circle(r=R, $fn=180);
      translate([cd+R,0]) square([2*R, 4*R], center=true);
    }
}
// cap outline + flange. CLOSING (dilate-erode) then OPENING (erode-dilate): the closing
// is what actually fillets the flange/cap junction, which is a REENTRANT corner - an
// opening on its own leaves it perfectly sharp and only cuts back the flange's convex
// corners. The trailing opening keeps that convex rounding.
module body2d() offset(r=tab_round) offset(r=-2*tab_round) offset(r=tab_round) union() {
  circle(d=cap_od, $fn=160);
  flange2d();
}
// grip ribs continued along the pushed flange edge (arc + the two straight sides)
module flange_ribs() {
  R = cap_od/2; ha = flange_arc/2;
  px = flange_push*cos(flange_angle); py = flange_push*sin(flange_angle);
  rib_step = 360/rib_count;
  n_arc = max(1, floor(flange_arc/rib_step));
  for (k=[0:n_arc]) {
    th = flange_angle - ha + k*flange_arc/n_arc;
    translate([R*cos(th)+px, R*sin(th)+py, 0]) cylinder(d=rib_d, h=cap_h);
  }
  n_side = max(1, round(flange_push/(rib_step*PI/180*R)));
  for (s=[-1,1]) for (m=[0:n_side]) {
    th = flange_angle + s*ha; t = m/n_side;
    translate([R*cos(th)+t*px, R*sin(th)+t*py, 0]) cylinder(d=rib_d, h=cap_h);
  }
}

// tube port positions (2D), n_ports placed clear of the rods - the
// original Vessel Cap.scad placement logic
module port_holes2d() {
  R = port_R;
  if (n_ports > 0) {
    if (rods == 0 || rod_off == 0)
      for (i=[0:n_ports-1]) rotate(i*360/n_ports) translate([R,0]) circle(d=port_d,$fn=24);
    else if (n_ports < 3)
      for (j=[0:n_ports-1]) rotate(90+j*360/n_ports) translate([R,0]) circle(d=port_d,$fn=24);
    else {
      ring_ports = (n_ports < 4) ? n_ports : 4;
      for (k=[0:2+ring_ports-1]) rotate(k*360/6) translate([R,0]) if (k==0||k==3) {} else circle(d=port_d,$fn=24);
    }
  }
  n_centre = (n_ports > 4) ? min(n_ports-4, 2-openings) : 0;          // centre ports that still fit beside the opening(s)
  if (n_centre > 0)                                                   // guard: [0:-1] otherwise
    for (k=[0:n_centre-1]) rotate(90+(openings+k)*180) translate([R,0]) circle(d=port_d,$fn=24);  // placed opposite the opening(s)
}

// big gasket openings that replace the centre port(s): expand to fill the open-window
// region on that side, but stop min_wall short of every remaining port.
// ---- ceiling window (the "fan") -------------------------------------
// The CEILING is the slab underside that clamps the septum onto the glass rim
// (z_ceil). The window's outer arc there = vessel throat + septum thickness + one
// layer, so a syringe sliding down the 45deg entrance wall crosses the septum top at
// the arc and passes the glass edge with exactly the one-layer allowance.
z_ceil  = cap_h - top_th;                 // slab underside = septum top
R_ceil  = neck_id/2 + gask_t + layer_h;   // window arc radius AT the ceiling
tower_r = port_d/2 + min_wall;            // tube-channel keep-out around each flanking port
y_towerfront = port_R*sin(60) + tower_r;  // the keep-outs' front line

// the ceiling window, built for the FRONT and mirrored for the rear: one graceful
// shape, never wider than the tower centrelines. Rear = an arc tangent to both tower
// clearances, kissing the spine line (behind the tower centres it stays inside their
// closest points and closes in that arc). Middle = the strip between the centrelines,
// hugging the tower keep-outs. Front = the graze arc. A morphological OPENING
// (erode-dilate) removes every cusp so all joins are tangent - the tower clearances
// are keep-out zones, not visible cylinders.
module opening_front2d() {
  px = port_R*cos(60); py = port_R*sin(60);               // flanking port centres at (+-px, py)
  t  = min(win_round, port_R*sin(30) - tower_r - 0.05);   // smoothing radius, under the tower-gap half-waist
  K  = (tower_r - 0.05) - spine_hw;                       // 0.05 INTO the keep-outs: exact tangency is a
  c  = (port_R*port_R - K*K) / (2*(py + K));              // non-manifold touch-point; the bites re-cut the
                                                          // overlap and the opening rounds the join
  offset(r=t) offset(r=-t)
  difference() {
    union() {
      translate([0,c]) circle(r=c-spine_hw, $fn=90);      // rear closing arc
      intersection() {                                    // centreline strip out to the graze arc
        circle(r=R_ceil, $fn=140);
        translate([-px, py]) square([2*px, 2*cap_od]);
      }
    }
    for (s=[-1,1]) translate([s*px, py]) circle(r=tower_r, $fn=48);  // tower keep-outs
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
// opening's radial direction, pivoting about z=cap_h (the cap top) - so at the cap face the
// footprint is unchanged (the front line stays) and the wall leans above it. 90 = vertical.
module opening_bore_tilted() {
  k = cos(opening_tilt) / sin(opening_tilt);              // horizontal run per unit rise (0 at 90deg)
  if (openings > 0) for (sy = (openings>=2) ? [1,-1] : [1])
    multmatrix([[1,0,0,0],[0,1,sy*k,-sy*k*cap_h],[0,0,1,0],[0,0,0,1]])   // shear Y by sy*k*(z-cap_h)
      translate([0,0,cap_h-eps]) linear_extrude(H_top-cap_h+5) opening_one2d(sy);
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
//    width (prow_m): the crest where it daylights through the sloping funnel skin
//    then RISES at >=45deg from the centre to the swath walls - anchored at both
//    ends, printable - instead of hanging as a horizontal ridge. The funnel toe
//    under the floor stays, keeping the cap rim's print support; the slot's side
//    walls are vertical planes at the tower centrelines, whose skin crossings are
//    steep by construction.
prow_m = 1.9;   // prow floor slope across the width; >=1.64 keeps the daylight crest at >=45deg.
                // The prow faces themselves rise at atan(prow_m) ~ 62deg sideways, so they ARE
                // the side relief once nothing truncates them.
side_k = 3.4;   // outer side-wall steepness (rise/run, ~74deg): shallower and the wall's own
                // daylight crest through the funnel skin dips below 45deg near the rear corner
module tunnel_front() {
  B = 6*cap_od; px = port_R*cos(60);
  if (wedge=="front") {
    // front-only prow slot: crowned, vertical side walls, no side relief
    tw = (R_ceil - spine_hw - 0.7)/prow_m;   // end at a ~0.7mm side wall, before the
    intersection() {                         // floor meets the crown (no feather pinch)
      multmatrix([[1,0,0,0],[0,1,0,0],[ prow_m,1,1, z_ceil-R_ceil],[0,0,0,1]])
        translate([-B/2,-B/2,0]) cube(B);
      multmatrix([[1,0,0,0],[0,1,0,0],[-prow_m,1,1, z_ceil-R_ceil],[0,0,0,1]])
        translate([-B/2,-B/2,0]) cube(B);
      multmatrix([[1,0,0,0],[0,1,0,0],[0,1,1, z_ceil-spine_hw],[0,0,0,1]])   // crown: z <= z_ceil + (y-spine_hw)
        translate([-B/2,-B/2,-B]) cube(B);
      translate([-tw, R_ceil-1, z_ceil-0.2]) cube([2*tw, B/2, B/2]);
      translate([0,0,z_ceil-0.2]) cylinder(r1=R_ceil-0.3, r2=R_ceil-0.3+B, h=B, $fn=140);
    }
  } else intersection() {                    // "sides" / "max": prow V with side relief
    // prow floor: z >= z_ceil + (y-R_ceil) + prow_m*|x|  (one half-space per side of the V)
    multmatrix([[1,0,0,0],[0,1,0,0],[ prow_m,1,1, z_ceil-R_ceil],[0,0,0,1]])
      translate([-B/2,-B/2,0]) cube(B);
    multmatrix([[1,0,0,0],[0,1,0,0],[-prow_m,1,1, z_ceil-R_ceil],[0,0,0,1]])
      translate([-B/2,-B/2,0]) cube(B);
    // leaning outer side walls: |x| <= px + (z - z_ceil)/side_k
    multmatrix([[1,0,1/side_k, px - z_ceil/side_k],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
      translate([-B,-B/2,-B/2]) cube(B);
    mirror([1,0,0]) multmatrix([[1,0,1/side_k, px - z_ceil/side_k],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
      translate([-B,-B/2,-B/2]) cube(B);
    // rear bound: vertical plane at the keep-outs' front line, pushed 0.2 into them
    // (an exactly tangent plane is a non-manifold touch-line; the keep-outs re-cut it)
    translate([-B/2, y_towerfront-0.2, z_ceil-0.5]) cube(B);
    // radial 45deg bound from the window arc (started 0.1 inside it, so it crosses the
    // shaft wall instead of kissing it): tapers the slab's window edge and never
    // pierces the ceiling beyond it - no flat ledge anywhere on the ring
    translate([0,0,z_ceil-0.2]) cylinder(r1=R_ceil-0.3, r2=R_ceil-0.3+B, h=B, $fn=140);
  }
}
module opening_cut_front() {
  H = H_top - z_ceil;
  difference() {
    union() {
      translate([0,0,z_ceil-0.3]) linear_extrude(H+0.3) opening_front2d();
      if (wedge!="no") tunnel_front();                    // "no" = the vertical shaft only
    }
    for (s=[-1,1]) translate([s*port_R*cos(60), port_R*sin(60), z_ceil-0.4])
      cylinder(r=tower_r-0.02, h=H+1, $fn=48);            // tube-channel keep-outs (a hair under
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

// gasket retaining ridge: triangular barb (both faces <=45deg from vertical).
// The outer face must reach the BORE wall (T_nom/2), not the gasket seat (gask_seat_d/2)
// - the seat is 0.05 inside the bore, so seating the barb on it leaves the whole ring
// floating in the bore void with nothing to print onto.
module gasket_ridge() rotate_extrude($fn=140)
  polygon([[T_nom/2 + eps, gask_z+0.05],
           [ridge_id/2,    gask_z-ridge_h/2],
           [T_nom/2 + eps, gask_z-ridge_h]]);

// O-ring dovetail profile - retains the O-ring in its groove
dovetail_th = 1;   // groove depth (the profile's height; see placement in cap())
module dovetail(top) {
  bottom = top + 0.3;
  polygon(points=[[0,0],[bottom,0],[top+0.15,dovetail_th],[0.15,dovetail_th]]);
}

// the whole top-stop top face = one rounded rectangle
module clampband2d() offset(r=clamp_corner) square([2*x_out-2*clamp_corner, clamp_W-2*clamp_corner], center=true);

// ---- tube guides --------------------------------------------------
function lsum(v,i=0) = i >= len(v) ? 0 : v[i] + lsum(v,i+1);
// the tube port centres, in the same order port_holes2d() places them (1-based
// in `guides`). Assumes the standard layout (n_ports>=3, rods at 0/180).
function guide_pts() = let(
  R  = port_R,
  rp = (n_ports < 4) ? n_ports : 4,
  ring = [for (k=[0:2+rp-1]) if (k!=0 && k!=3) [R*cos(k*60), R*sin(k*60)]],
  nc = (n_ports > 4) ? min(n_ports-4, 2-openings) : 0,
  cen = (nc>0) ? [for (k=[0:nc-1]) [R*cos(90+(openings+k)*180), R*sin(90+(openings+k)*180)]] : []
) concat(ring, cen);
// guide section on the cap top: hemispherical-topped tower per individual port, OR one
// semicircle (centred on the ports' layout centre) when the selected ports all sit on one
// side. Either way it stands guide_h tall and clears the ports by min_wall. Port holes are
// bored through it by cap()'s extended port cut.
guide_sel = [for (g=guides) if (g>=1 && g<=len(guide_pts())) g];
module guides_solid() {
  pts = [for (g=guide_sel) guide_pts()[g-1]];
  rg  = port_d/2 + min_wall;
  if (len(pts) > 0) {
    bis  = atan2(lsum([for(p=pts) p[1]]), lsum([for(p=pts) p[0]]));     // mean direction of the picks
    span = (len(pts)<2) ? 0 : max([for(p=pts) abs(((atan2(p[1],p[0]) - bis + 540) % 360) - 180)]);
    if (len(pts) > 1 && span <= 90)                                     // full set on one side -> semicircle
      translate([0,0,cap_h]) linear_extrude(guide_h)
        rotate(bis) intersection() {
          circle(r = port_R + port_d/2 + min_wall, $fn=140);
          translate([0,-cap_od]) square([cap_od, 2*cap_od]);            // keep the bisector half (x>=0)
        }
    else                                                                // individual ports -> domed towers
      for (p=pts) translate([p[0],p[1],cap_h]) {
        cylinder(r=rg, h=max(eps, guide_h-rg), $fn=48);
        translate([0,0,max(0, guide_h-rg)]) sphere(r=rg, $fn=48);
      }
  }
}

// guides at the TOP-STOP top face (z=H_top), extending guide_h DOWN (= up from the bed when
// printed top-stop-down). Ports near an opening -> a semicircle each (flat toward centre);
// the rest (the uninterrupted back) -> ONE semicircle (half-disc from the centre, so it
// merges with the top stop - no gap). Both clear the holes by guidexmin_wall*min_wall; the
// port channels are bored through by holder1().
function near_open(p) = let(og = concat(openings>=1 ? [90] : [], openings>=2 ? [270] : []))
  len(og)>0 && min([for(o=og) abs(((atan2(p[1],p[0])-o+540)%360)-180)]) <= 45;
module guides_topstop() {
  pts = [for (g=guide_sel) guide_pts()[g-1]];
  if (len(pts) > 0) {
    gxw  = guidexmin_wall * min_wall;
    ovl  = 0.2;                                                     // interpenetration into the clamp band: seating
                                                                    // exactly on its edge is a zero-volume weld
    near = [for (p=pts) if (near_open(p)) p];
    far  = [for (p=pts) if (!near_open(p)) p];
    // the far set collapses into ONE semicircle only when it really does sit on one side.
    // Otherwise (e.g. openings=0, where every port is "far" and they ring the whole cap)
    // each port gets its own, exactly as the near ones do - a single half-plane would
    // silently drop every port on the other side while still boring its channel.
    fbis  = (len(far)>0) ? atan2(lsum([for(p=far) p[1]]), lsum([for(p=far) p[0]])) : 0;
    fspan = (len(far)<2) ? 0 : max([for(p=far) abs(((atan2(p[1],p[0]) - fbis + 540) % 360) - 180)]);
    merged = len(far) > 1 && fspan <= 90;
    solo   = merged ? near : pts;
    translate([0,0,H_top-guide_h]) linear_extrude(guide_h) {
      if (merged)                                                    // far side: one semicircle, clipped to just
        rotate(fbis) intersection() {                                // inside the top-stop long edge (so it doesn't
          circle(r = port_R + port_d/2 + gxw, $fn=140);              // block the rods/clamp, and welds to the edge)
          translate([clamp_W/2-ovl, -cap_od]) square([cap_od, 2*cap_od]);
        }
      for (p=solo) {                                                 // a semicircle per port, seated on and
        sy = (p[1] >= 0) ? 1 : -1;                                   // overlapping the near long edge
        ey = sy * (clamp_W/2 - ovl);
        Rf = abs(p[1] - ey) + port_d/2 + gxw;
        translate([p[0], ey]) intersection() {
          circle(r=Rf, $fn=64);
          translate([-Rf, sy>0 ? 0 : -Rf]) square([2*Rf, Rf]);       // the half bulging out toward the port
        }
      }
    }
  }
}

// ---- parts ----------------------------------------------------------
module cap() color(C_CAP) difference() {
  union() {
    difference() {                                   // body (with knurl) minus the core bore
      union() {
        linear_extrude(cap_h) body2d();
        if (ribs=="yes" && rib_count>0) {
          for (i=[0:rib_count-1]) {                             // body ribs, skipped in the flange sector
            a = i*360/rib_count; da = abs(((a-flange_angle+540)%360)-180);
            if (da >= flange_arc/2) rotate([0,0,a]) translate([cap_od/2,0,0]) cylinder(d=rib_d,h=cap_h);
          }
          flange_ribs();                                        // ribs continued along the flange
        }
      }
      translate([0,0,-eps]) cylinder(d=T_nom, h=bore_top+eps);
    }
    // internal GPI thread (added back inside the bore)
    translate([0,0,pitch/2])
      thread_helix(d=D_minor_int, pitch=pitch, turns=(bore_top-pitch)/pitch,
                   thread_depth=depth_rad, flank_angle=30, starts=starts,
                   anchor=BOTTOM, lead_in=leadin_len, internal=true);
    if (seal=="gasket") gasket_ridge();              // lip that retains the gasket
    if (part=="cap") color(C_CAP) guides_solid();    // cap-top guides only when viewing the cap alone
  }
  // smooth gasket seat under the closed top (gasket seal only). The eps goes on the
  // BOTTOM: that is where the coincident plane is (gask_z == bore_top), and putting it
  // on the top would eat the ceiling down from top_th (3 layers) to 2.75.
  if (seal=="gasket") translate([0,0,gask_z-eps]) cylinder(d=gask_seat_d, h=gask_t+eps);
  // cap O-ring groove cut UP into the closed top, mouth (narrow end) at the bore ceiling
  // (oring seal only). The mirror flips the dovetail's taper; the +dovetail_th lands it
  // in the slab instead of hanging it in the bore void below.
  if (seal=="oring")
    translate([0,0,bore_top+dovetail_th]) mirror([0,0,1]) rotate_extrude($fn=100)
      translate([(cap_o_ring_id+cap_o_ring_cs)/2, 0, 0]) dovetail(cap_o_ring_cs);
  // rod bores (friction bore for gasket; looser port + O-ring groove for oring)
  if (rods>0) for (i=[0:rods-1]) rotate([0,0,i*360/rods]) translate([rod_off,0,0]) {
    // bored through any cap-top guide too, or a one-sided guide roofs the rod over
    translate([0,0,-eps]) cylinder(d = (seal=="oring") ? rod_d+cap_fit+rod_cutout : cap_bore,
                                   h = cap_h + ((part=="cap" && len(guide_sel)>0) ? guide_h : 0) + 2*eps);
    if (seal=="oring")   // mid-slab, as the un-flipped original had it at top_th/2;
                         // bore_top MINUS the cs would sit in the bore void and cut nothing
      translate([0,0,bore_top+top_th/2]) rotate_extrude($fn=100)
        translate([rod_o_ring_id/2, 0, 0]) circle(d=rod_o_ring_cs, $fn=64);
  }
  // peg holes (through the closed top only) - 2-piece only; the 1-piece is fused, no pegs
  if (pieces==2) for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+peg_clear, h=top_th+2*eps);
  // ports OR an open gasket field (full-width spine, rounded window corners)
  if (port_style=="ports") {
    translate([0,0,-eps])
      linear_extrude(cap_h + (len(guide_sel)>0 ? guide_h : 0) + 2*eps) port_holes2d();  // ports bored through any guide too
    if (opening_style=="fan") opening_fan();              // same tapered cut as the holder - windows always match
    else translate([0,0,-eps]) linear_extrude(cap_h+2*eps) openings2d();
  }
  else
    translate([0,0,cap_h-top_th-eps]) linear_extrude(top_th+2*eps)
      offset(r=win_round) offset(r=-win_round) difference() {   // OPENING -> rounds the window's convex corners
        circle(r=R_open, $fn=140);
        square([2*cap_od, 2*spine_hw], center=true);   // spine spans the full width
      }
}

module gasket() color(C_GASKET) translate([0,0,gask_z]) difference() {
  cylinder(d=gask_d, h=gask_t, $fn=96);
  for (s=[-1,1]) translate([s*rod_off,0,-eps]) cylinder(d=rod_d-0.4, h=gask_t+2*eps);
}

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, bearing_r);
    translate([0,0,H_top-clamp_h]) linear_extrude(clamp_h) clampband2d();   // single rounded-rect top
    if (pieces==2) for (s=[-1,1]) translate([0,s*peg_off,cap_h]) rotate([180,0,0]) cylinder(d=peg_d, h=peg_h);  // pegs (2-piece only)
  }
  for (s=[-1,1]) translate([s*rod_off,0,cap_h-eps]) cylinder(d=col_bore, h=col_h+2*eps);  // journal bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from the outer face in to pinch the wire on the rod
    translate([rod_off+rod_d/2-0.4, 0, zc]) teardrop_x(m3_bolt, x_out-(rod_off+rod_d/2)+0.9);
    // captive nut: pocket opens at the band BOTTOM (down-in-use = up-in-print, no bridge);
    // width = across-flats so it can't rotate; inner+outer walls trap it along the bolt
    translate([x_nut0, -nut_af/2, H_top-clamp_h-eps]) cube([nut_th, nut_af, (zc+nut_ac/2)-(H_top-clamp_h)+eps]);
    // wire guide slot, top face down to the bolt
    translate([rod_off+rod_d/2-0.4, -0.9, zc]) cube([1.5,1.8, H_top-zc+eps]);
  }
}

module vessel() color(C_VESSEL) translate([0,0,-38]) difference() {   // neck bore modelled so
  cylinder(d=cap_od-2*wall_t-1.2, h=38+gask_z+eps);                    // section view shows the
  translate([0,0,2]) cylinder(d=neck_id, h=38+gask_z);                 // through-neck clearance
}
module rods() color(C_STEEL) for(s=[-1,1]) translate([s*rod_off,0,H_top-rod_len]) cylinder(d=rod_d,h=rod_len);

// ===== 1-piece construction =====
// Uses the REAL cap (set port_style="open") so the thread, gasket seat and
// gasket-holding structure stay.
// The connector is now a SOLID funnel covering the FULL circumference: it runs
// from the cap outline (incl. the poka-yoke) all the way down to the racetrack.
// Every layer is a ring no bigger than the one below it (<=45deg overhang), so
// NOTHING starts in mid-air - both sides and front/rear all land on the
// racetrack. funnel_h is taller than the cap overhang so the slope is steeper
// than 45deg everywhere (i.e. the connection starts lower down the print).
funnel_h = 14;                                        // must exceed cap_R-bearing_r (the +-Y run)
assert(funnel_h > cap_R - bearing_r, "funnel_h too shallow - funnel overhang exceeds 45deg");
assert(col_h > 0, "rod_len too short for insertion_depth + cap_h - column has no height");
z_join   = cap_h + funnel_h;
module rt_outline2d() hull() for(s=[-1,1]) translate([s*rod_off,0]) circle(r=bearing_r, $fn=48);

// the cap's open-gasket window - used to bore straight up. Only ever reached from the
// port_style!="ports" arm in holder1(), so it carries no "ports" branch of its own.
module ports2d()
  offset(r=win_round) offset(r=-win_round) difference() {
    circle(r=R_open, $fn=140);
    square([2*cap_od, 2*spine_hw], center=true);
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
          color(C_CARR) intersection() {
            hull() {
              translate([0,0,cap_h-0.05]) linear_extrude(0.1) body2d();
              translate([0,0,z_join])     linear_extrude(0.1) rt_outline2d();
            }
            // starts 0.05 BELOW cap_h so the hull's deliberate overlap into the cap
            // survives the clip - starting at cap_h exactly cancels it and leaves the
            // funnel butted to the cap on a zero-volume coincident face
            translate([0,0,cap_h-0.05]) linear_extrude(z_join-cap_h+1.05) body2d();
          }
        }
        // (1) the big 45deg V-wedge across the cap (wedge=="max" only), on top of the
        // prow cuts: apex line on the CAP SURFACE (x=0, z=cap_h), faces rising
        // up-and-out at 45deg, 5mm central spine left uncut.
        // openings=1 -> front only; openings=2 -> front+rear.
        if (wedge=="max" && openings > 0)
          difference() {
            rotate([90,0,0]) linear_extrude(height=cap_od*3, center=true)
              polygon([[0,cap_h],[60,cap_h+60],[60,300],[-60,300],[-60,cap_h+60]]);
            translate([-cap_od, -2.5, -50]) cube([2*cap_od, 5, 400]);              // the 5mm spine stays
            if (openings < 2)                                                       // 1 opening -> keep the rear solid
              translate([-cap_od, -cap_od-2.5, -50]) cube([2*cap_od, cap_od, 400]);
          }
        // (2) gasket-access openings - flared or tilted per opening_style (open window in
        // "open" style) - cut HERE, before the column is unioned in, so they never carve it
        if (port_style=="ports") {
          if (opening_style=="fan") opening_fan();
          else opening_bore_tilted();
        } else translate([0,0,cap_h-top_th-eps]) linear_extrude(H_top-(cap_h-top_th)+5) ports2d();
      }
      column();                                       // re-added whole: untouched by the wedge/openings
      color(C_CARR) guides_topstop();                 // added after the wedge cuts so the front ones survive
    }
    // (3) tube channels: full circles cut through EVERYTHING they cross (funnel, column
    // wall, clamp band, guides) so the bore stays round all the way down
    translate([0,0,cap_h-top_th-eps]) linear_extrude(H_top-(cap_h-top_th)+5) port_holes2d();
    // (4) keep the rod path clear: the funnel/spine fills the bore line, so
    // bore the two rod holes straight through it (ramp/spine only OUTSIDE the bores;
    // +0.02 so this never coincides exactly with the column's own journal bores).
    // Starts at the funnel's underside, NOT z=0: running it through the cap as well
    // would ream cap_bore out to col_bore and destroy the cap's friction fit.
    for (s=[-1,1]) translate([s*rod_off,0,cap_h-0.1]) cylinder(d=col_bore+0.02, h=H_top-cap_h+5.1, $fn=48);
  }
}

// ---- assembly / views ----------------------------------------------
e = (view=="exploded") ? 1 : 0;

module holder() {
  if (pieces==1) holder1();                // open-neck single piece
  else { cap(); translate([0,0,e*42]) column(); }
}

module assembly() {
  translate([0,0,-e*38]) vessel();
  if (seal=="gasket") translate([0,0,-e*17]) gasket();   // no gasket in oring mode
  holder();
  translate([0,0,e*18]) rods();
}

if (part=="cap") cap();
else if (part=="column") translate([0,0,-cap_h]) column();
else if (part=="gasket") translate([0,0,-gask_z]) gasket();
else if (view=="section") difference(){ assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view=="print") {
  if (pieces==1) translate([0,0,H_top]) rotate([180,0,0]) holder();   // whole holder, flush face on bed
  else {
    translate([-18,0,cap_h]) rotate([180,0,0]) cap();                 // closed-top on bed
    translate([ 20,0,H_top]) rotate([180,0,0]) column();              // flush-face on bed, pegs up
  }
} else assembly();
