// =====================================================================
// electroPioreactor - vial cap + electrode holder (single source file)
// Iterations are tracked in git, not as v2/v3 files.
//
// Parts:  CAP (seals + ports + GPI thread)  •  SEPTUM (silicone, seals only)
//         COLUMN / top stop (holds electrodes, sets depth, clamps the wires)
//
// PRINT ORIENTATIONS (both support-free - see view="print"):
//   CAP    : closed-top on the bed, mouth up.  Build dir = up toward mouth.
//   COLUMN : flush face on the bed, pegs up.    Build dir = up toward pegs.
// In the COLUMN model, "up" (+Z) is the bed side, so the clamp sits at the
// top face (lands ON the bed) and its nut pocket opens downward-in-use
// (= upward-in-print -> no bridge, no supports).
//
// Requires BOSL2 (same as the current Vial Cap.scad).
// =====================================================================
include <BOSL2/std.scad>
include <BOSL2/threading.scad>

// ---- options (choices listed inline) --------------------------------
view       = "print";      // "exploded" | "assembled" | "section" | "print"
part       = "all";        // "all" | "cap" | "column" | "septum"
port_style = "ports";      // "ports" | "open"
seal       = "septum";     // "septum" | "oring"  - oring reproduces the original Vial Cap.scad O-ring grooves
pieces     = 1;            // 2 = separate cap + top stop | 1 = one printed piece
ribs       = "no";         // "yes" | "no"  (grip ribs / knurling - "no" = smooth cap)
openings   = 1;            // 0 | 1 (front) | 2 (front+rear) - big septum openings replacing the centre ports
min_wall   = 0.84;         // mm wall kept between an opening and any port (2 strands @ 0.42 line width, 0.4 nozzle - PC-CF min)
opening_tilt = 50;         // deg - tilt of the opening wall above the cap (90 = vertical); pivots about the opening's front line on the cap top
layer_h    = 0.2;          // mm - PC-CF print layer height (set to your slicer's value)
guides     = [1,2,3,4,5];  // ports to add a needle guide on (1-based port indices; [0] = none; e.g. [1] or [1,2,3])
guide_h    = 3;            // mm - height of the guide section (above the cap for part="cap"; below the top-stop face otherwise)
guidexmin_wall = 2;        // guide clearance beyond a port hole, as a multiple of min_wall

$fn = 72;
eps = 0.05;

// ---- electrodes & ports (the original cap's key counts + sizes) -----
electrodes      = 2;       // number of electrodes (0 or 2; the top-stop column is built for 2)
el_d            = 6.2;     // electrode diameter
n_ports         = 5;       // number of tube/needle ports (auto-placed clear of the electrodes)
port_d          = 2.2;     // port diameter (OD of the 75mm needles)
el_len          = 60;      // electrode length (L)
el_off          = 4.8;     // offset from axis to each electrode
insertion_depth = 23;      // g: protrusion below the cap bottom into the vial

// ---- fits (point 8) -------------------------------------------------
cap_fit      = 0.15;       // friction fit in the CAP (snug - holds electrode by friction)
insert_extra = 0.30;       // EXTRA clearance in the COLUMN for easy insertion (bolts do the holding)
cap_bore = el_d + cap_fit;                 // friction bore (also the lower bearing)
col_bore = el_d + cap_fit + insert_extra;  // easy-insert bore; total tracks cap_fit

// ---- cap ------------------------------------------------------------
cap_od = 27; cap_h = 12.3; wall_t = 2;
rib_count = 84; rib_d = 0.856;   // number of grip ribs (when ribs=="yes")
// GPI 24-400 thread (verbatim from Components/Vial Cap/Vial Cap.scad)
T_nom = 24.30; dia_clear = 0.50; pitch = 25.4/8; starts = 1; leadin_len = 0.6*pitch;
D_maj_int = T_nom + dia_clear; depth_rad = 0.3*pitch; D_minor_int = D_maj_int - 2*depth_rad;
// septum + retaining ridge (point 9)
sept_t = 2.0; sept_d = 23.9; sept_seat_d = 24.2;
ridge_id = 22.5; ridge_h = 1.6;            // inward lip that keeps the septum from dropping out
// O-ring seal (only used when seal=="oring"; reproduces the original Vial Cap.scad)
cap_o_ring_cs       = 1.7;   // mm - cap O-ring cross-section (dovetail groove in the bore wall)
electrode_o_ring_cs = 2.5;   // mm - electrode O-ring cross-section
electrode_cutout    = 1.0;   // mm - electrode port relief; also sets the electrode O-ring id
electrode_o_ring_id = el_d - electrode_cutout/2 + electrode_o_ring_cs/2;
// closed-top thickness depends on the seal: 3 PC-CF layers is plenty to hold the SEPTUM
// down, but the O-RING needs a solid top to seat against, so in oring mode make the top
// at least the cap O-ring cross-section + 2 layers (~2.5mm with defaults).
top_th = (seal=="oring") ? max(cap_o_ring_cs + 4*layer_h, 3*layer_h) : 3*layer_h;
// ports
cap_o_ring_id = 18.7706; port_R = (cap_o_ring_id - port_d)/2;  // 7.785, in the neck
// open septum field
spine_hw = 4.65; R_open = cap_od/2 - wall_t - 1.0; win_round = 2.0;
// poka-yoke FLANGE (pushed-out chord section, assimilated from Gerrit's cap / vial-cap-s):
// a chord-section of the cap is pushed straight out, so the outer edge keeps the cap
// curvature, the sides are straight, and the grip ribs continue along it.
flange_arc   = 93;      // deg - angular width of the pushed-out section
flange_push  = 3.5;     // mm - radial push
flange_angle = 180;       // deg - ROTATE the poka-yoke around the cap (0 = +X side; 90 = front; -90 = rear; etc.)
tab_round    = 2.5;     // fillet at the flange/cap junction

// ---- registration pegs ---------------------------------------------
peg_d = 3; peg_off = 2; peg_clear = 0.3; peg_h = top_th;   // flush with the cap inside ceiling

// ---- column + clamp -------------------------------------------------
bearing_r = el_d/2 + 1.8;
m3_bolt   = 3.4; nut_af = 5.9; nut_th = 2.8; nut_ac = nut_af/cos(30);
clamp_in  = 1.8; clamp_out = 2.2;          // robust PC-CF walls (Grace-proof)
// 1-piece build
cap_R   = cap_od/2;                // flange_angle (above) sets the poka-yoke position; 0 = +X rises with a side ramp

col_h  = el_len - insertion_depth - cap_h; // sets the insertion depth
H_top  = cap_h + col_h;                     // electrode flush face
xe     = el_off + col_bore/2;               // bore outer edge
x_nut0 = xe + clamp_in; x_nut1 = x_nut0 + nut_th; x_out = x_nut1 + clamp_out;
// the top stop's top face is ONE rounded rectangle (long faces flush with the racetrack)
clamp_h = 8; clamp_W = 2*bearing_r; clamp_corner = 3;
zc     = H_top - 4;                         // bolt axis, near the top face
sept_z = cap_h - top_th - sept_t;
bore_top = cap_h - top_th - (seal=="septum" ? sept_t : 0);   // bore ceiling: leave the septum slab only for the septum seal

C_CAP=[0.78,0.87,0.97]; C_SEPT=[0.74,0.62,0.92]; C_CARR=[1,0.83,0.58];
C_STEEL=[0.72,0.74,0.78]; C_VIAL=[0.55,0.88,0.78,0.32];

// ---- helpers --------------------------------------------------------
module racetrack(h,r) hull() for(s=[-1,1]) translate([s*el_off,0,0]) cylinder(r=r,h=h);

// poka-yoke flange outline: a chord-section of the cap hull'd with itself pushed out
module flange2d() {
  R = cap_od/2; cd = R*cos(flange_arc/2);
  rotate(flange_angle) hull() for (dx=[0, flange_push])
    translate([dx,0]) intersection() {
      circle(r=R, $fn=180);
      translate([cd+R,0]) square([2*R, 4*R], center=true);
    }
}
module body2d() offset(r=tab_round) offset(r=-tab_round) union() {   // cap outline + flange
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

// tube/needle port positions (2D), n_ports placed clear of the electrodes - the
// original Vial Cap.scad placement logic
module port_holes2d() {
  R = (cap_o_ring_id - port_d)/2;
  if (n_ports > 0) {
    if (electrodes == 0 || el_off == 0)
      for (i=[0:n_ports-1]) rotate(i*360/n_ports) translate([R,0]) circle(d=port_d,$fn=24);
    else if (n_ports < 3)
      for (j=[0:n_ports-1]) rotate(90+j*360/n_ports) translate([R,0]) circle(d=port_d,$fn=24);
    else {
      ring_ports = (n_ports < 4) ? n_ports : 4;
      for (k=[0:2+ring_ports-1]) rotate(k*360/6) translate([R,0]) if (k==0||k==3) {} else circle(d=port_d,$fn=24);
    }
  }
  n_centre = (n_ports > 4) ? min(n_ports-4, 2-openings) : 0;          // centre ports that still fit beside the opening(s)
  for (k=[0:n_centre-1]) rotate(90+(openings+k)*180) translate([R,0]) circle(d=port_d,$fn=24);  // placed opposite the opening(s)
}

// big septum openings that replace the centre port(s): expand to fill the open-window
// region on that side, but stop min_wall short of every remaining port.
// one opening footprint (side sy): rounded 4-sided sector, kept min_wall off the ports
module opening_one2d(sy) {
  R = (cap_o_ring_id - port_d)/2;
  half = max(1, 30 - asin((port_d/2 + min_wall)/R));      // sector half-width: ring ports flank at +-30deg
  ca = (sy>0) ? 90 : 270;                                 // 90 front / 270 rear
  offset(r=win_round) offset(r=-win_round)                // round the corners
  intersection() {
    circle(r=R_open, $fn=140);                            // outer = cap-rim arc (the curved side)
    translate([-cap_od, sy>0 ? spine_hw : -spine_hw-2*cap_od, 0]) square([2*cap_od, 2*cap_od]); // inner = spine line
    polygon([[0,0], 2*R_open*[cos(ca-half),sin(ca-half)], 2*R_open*[cos(ca+half),sin(ca+half)]]);  // two straight sides
  }
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

// teardrop hole, axis +X, apex toward -Z (= up in print -> self-supporting)
module teardrop_x(d,len){ r=d/2; hull(){ rotate([0,90,0]) cylinder(r=r,h=len);
  translate([0,0,-(r+0.8)]) rotate([0,90,0]) cylinder(r=0.01,h=len,$fn=6);} }

// septum retaining ridge: triangular barb (both faces <=45deg from vertical)
module septum_ridge() rotate_extrude($fn=140)
  polygon([[sept_seat_d/2, sept_z+0.05],
           [ridge_id/2,    sept_z-ridge_h/2],
           [sept_seat_d/2, sept_z-ridge_h]]);

// O-ring dovetail profile (verbatim from Vial Cap.scad) - retains the O-ring in its groove
module dovetail(top) {
  bottom = top + 0.3; thickness = 1;
  polygon(points=[[0,0],[bottom,0],[top+0.15,thickness],[0.15,thickness]]);
}

// the whole top-stop top face = one rounded rectangle
module clampband2d() offset(r=clamp_corner) square([2*x_out-2*clamp_corner, clamp_W-2*clamp_corner], center=true);

// ---- needle guides --------------------------------------------------
function lsum(v,i=0) = i >= len(v) ? 0 : v[i] + lsum(v,i+1);
// the tube/needle port centres, in the same order port_holes2d() places them (1-based
// in `guides`). Assumes the standard layout (n_ports>=3, electrodes at 0/180).
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
    gxw = guidexmin_wall * min_wall;
    front = [for (p=pts) if (near_open(p)) p];
    back  = [for (p=pts) if (!near_open(p)) p];
    translate([0,0,H_top-guide_h]) linear_extrude(guide_h) {
      if (len(back) > 0) {                                            // back: one semicircle, clipped to BEYOND the
        bis = atan2(lsum([for(p=back) p[1]]), lsum([for(p=back) p[0]]));   // top-stop long edge (so it doesn't block
        rotate(bis) intersection() {                                      // the electrodes/clamp, and seats on the edge)
          circle(r = port_R + port_d/2 + gxw, $fn=140);
          translate([clamp_W/2, -cap_od]) square([cap_od, 2*cap_od]);  // keep local x > clamp_W/2 (past the edge)
        }
      }
      for (p=front) {                                                // front: a semicircle per port, seated on the
        sy = (p[1] >= 0) ? 1 : -1;                                    // near long edge (flush, no longer floating)
        ey = sy * clamp_W/2;
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
    if (seal=="septum") septum_ridge();              // lip that retains the septum
    if (part=="cap") color(C_CAP) guides_solid();    // cap-top guides only when viewing the cap alone
  }
  // smooth septum seat under the closed top (septum seal only)
  if (seal=="septum") translate([0,0,sept_z]) cylinder(d=sept_seat_d, h=sept_t+eps);
  // cap O-ring groove in the bore wall, near the closed top (oring seal only)
  if (seal=="oring")
    translate([0,0,bore_top]) mirror([0,0,1]) rotate_extrude($fn=100)
      translate([(cap_o_ring_id+cap_o_ring_cs)/2, 0, 0]) dovetail(cap_o_ring_cs);
  // electrode bores (friction bore for septum; looser port + O-ring groove for oring)
  if (electrodes>0) for (i=[0:electrodes-1]) rotate([0,0,i*360/electrodes]) translate([el_off,0,0]) {
    translate([0,0,-eps]) cylinder(d = (seal=="oring") ? el_d+cap_fit+electrode_cutout : cap_bore, h=cap_h+2*eps);
    if (seal=="oring")
      translate([0,0,bore_top-electrode_o_ring_cs]) rotate_extrude($fn=100)
        translate([electrode_o_ring_id/2, 0, 0]) circle(d=electrode_o_ring_cs, $fn=64);
  }
  // peg holes (through the closed top only) - 2-piece only; the 1-piece is fused, no pegs
  if (pieces==2) for (s=[-1,1]) translate([0,s*peg_off,cap_h-top_th-eps]) cylinder(d=peg_d+peg_clear, h=top_th+2*eps);
  // ports OR an open septum field (full-width spine, rounded window corners)
  if (port_style=="ports")
    translate([0,0,-eps]) {
      linear_extrude(cap_h + (len(guide_sel)>0 ? guide_h : 0) + 2*eps) port_holes2d();  // ports bored through any guide too
      linear_extrude(cap_h+2*eps) openings2d();
    }
  else
    translate([0,0,cap_h-top_th-eps]) linear_extrude(top_th+2*eps)
      offset(r=win_round) offset(r=-win_round) difference() {   // OPENING -> rounds the window's convex corners
        circle(r=R_open, $fn=140);
        square([2*cap_od, 2*spine_hw], center=true);   // spine spans the full width
      }
}

module septum() color(C_SEPT) translate([0,0,sept_z]) difference() {
  cylinder(d=sept_d, h=sept_t, $fn=96);
  for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=el_d-0.4, h=sept_t+2*eps);
}

module column() color(C_CARR) difference() {
  union() {
    translate([0,0,cap_h]) racetrack(col_h, bearing_r);
    translate([0,0,H_top-clamp_h]) linear_extrude(clamp_h) clampband2d();   // single rounded-rect top
    if (pieces==2) for (s=[-1,1]) translate([0,s*peg_off,cap_h]) rotate([180,0,0]) cylinder(d=peg_d, h=peg_h);  // pegs (2-piece only)
  }
  for (s=[-1,1]) translate([s*el_off,0,cap_h-eps]) cylinder(d=col_bore, h=col_h+2*eps);  // journal bores
  for (m=[0,1]) mirror([m,0,0]) {
    // bolt clearance: teardrop from the outer face in to pinch the wire on the electrode
    translate([el_off+el_d/2-0.4, 0, zc]) teardrop_x(m3_bolt, x_out-(el_off+el_d/2)+0.9);
    // captive nut: pocket opens at the band BOTTOM (down-in-use = up-in-print, no bridge);
    // width = across-flats so it can't rotate; inner+outer walls trap it along the bolt
    translate([x_nut0, -nut_af/2, H_top-clamp_h-eps]) cube([nut_th, nut_af, (zc+nut_ac/2)-(H_top-clamp_h)+eps]);
    // wire guide slot, top face down to the bolt
    translate([el_off+el_d/2-0.4, -0.9, zc]) cube([1.5,1.8, H_top-zc+eps]);
  }
}

module vial() color(C_VIAL) translate([0,0,-38]) cylinder(d=cap_od-2*wall_t-1.2, h=38+sept_z+eps);
module electrodes() color(C_STEEL) for(s=[-1,1]) translate([s*el_off,0,H_top-el_len]) cylinder(d=el_d,h=el_len);

// ===== 1-piece construction =====
// Uses the REAL cap (set port_style="open") so the thread, septum seat and
// septum-holding structure stay.
// The connector is now a SOLID funnel covering the FULL circumference: it runs
// from the cap outline (incl. the poka-yoke) all the way down to the racetrack.
// Every layer is a ring no bigger than the one below it (<=45deg overhang), so
// NOTHING starts in mid-air - both sides and front/rear all land on the
// racetrack. funnel_h is taller than the cap overhang so the slope is steeper
// than 45deg everywhere (i.e. the connection starts lower down the print).
funnel_h = 14;                                        // > cap_R-bearing_r (8.7) => steeper than 45deg
z_join   = cap_h + funnel_h;
module rt_outline2d() hull() for(s=[-1,1]) translate([s*el_off,0]) circle(r=bearing_r, $fn=48);

// the cap's port openings (matches cap()'s port_style) - used to bore straight up
module ports2d() {
  if (port_style=="ports")
    { port_holes2d(); openings2d(); }
  else
    offset(r=win_round) offset(r=-win_round) difference() {
      circle(r=R_open, $fn=140);
      square([2*cap_od, 2*spine_hw], center=true);
    }
}

module holder1() {
  difference() {
    union() {
      cap();                                          // real cap (thread + open spine + septum)
      // solid funnel: cap rim (+poka-yoke) -> racetrack, then clipped to the cap/poka-yoke
      // footprint extruded straight up, so the hull can't bulge out past the flange join
      // (removes the overhang above where the poka-yoke meets the round cap).
      color(C_CARR) intersection() {
        hull() {
          translate([0,0,cap_h-0.05]) linear_extrude(0.1) body2d();
          translate([0,0,z_join])     linear_extrude(0.1) rt_outline2d();
        }
        translate([0,0,cap_h]) linear_extrude(z_join-cap_h+1) body2d();
      }
    }
    // (1) septum-access wedge - only where there is an opening: apex line on the CAP
    // SURFACE (x=0, z=cap_h), faces rising up-and-out at 45deg, 5mm central spine left
    // uncut. openings=0 -> no wedge; openings=1 -> front only; openings=2 -> front+rear.
    if (openings > 0)
      difference() {
        rotate([90,0,0]) linear_extrude(height=cap_od*3, center=true)
          polygon([[0,cap_h],[60,cap_h+60],[60,300],[-60,300],[-60,cap_h+60]]);
        translate([-cap_od, -2.5, -50]) cube([2*cap_od, 5, 400]);              // the 5mm spine stays
        if (openings < 2)                                                       // 1 opening -> keep the rear solid
          translate([-cap_od, -cap_od-2.5, -50]) cube([2*cap_od, cap_od, 400]);
      }
    // (2) septum access: circular ports straight up; openings tilted by opening_tilt
    if (port_style=="ports") {
      translate([0,0,cap_h-top_th-eps]) linear_extrude(H_top-(cap_h-top_th)+5) port_holes2d();
      opening_bore_tilted();
    } else
      translate([0,0,cap_h-top_th-eps]) linear_extrude(H_top-(cap_h-top_th)+5) ports2d();
    // (3) keep the electrode path clear: the funnel/spine fills the bore line, so
    // bore the two electrode holes straight through it (ramp/spine only OUTSIDE the bores)
    for (s=[-1,1]) translate([s*el_off,0,-eps]) cylinder(d=col_bore, h=H_top+5, $fn=48);
  }
  column();                                           // re-added whole: fills the centre, untouched by the wedge
  // needle guides at the top-stop face - added AFTER the wedge/opening cuts so the front
  // ones survive; only the port channels are bored through them.
  difference() {
    color(C_CARR) guides_topstop();
    translate([0,0,cap_h-top_th-eps]) linear_extrude(H_top-(cap_h-top_th)+5) port_holes2d();
  }
}

// ---- assembly / views ----------------------------------------------
e = (view=="exploded") ? 1 : 0;

module holder() {
  if (pieces==1) holder1();                // open-neck single piece
  else { cap(); translate([0,0,e*42]) column(); }
}

module assembly() {
  translate([0,0,-e*38]) vial();
  if (seal=="septum") translate([0,0,-e*17]) septum();   // no septum in oring mode
  holder();
  translate([0,0,e*18]) electrodes();
}

if (part=="cap") cap();
else if (part=="column") translate([0,0,-cap_h]) column();
else if (part=="septum") translate([0,0,-sept_z]) septum();
else if (view=="section") difference(){ assembly(); translate([-200,0,-200]) cube([400,200,400]); }
else if (view=="print") {
  if (pieces==1) translate([0,0,H_top]) rotate([180,0,0]) holder();   // whole holder, flush face on bed
  else {
    translate([-18,0,cap_h]) rotate([180,0,0]) cap();                 // closed-top on bed
    translate([ 20,0,H_top]) rotate([180,0,0]) column();              // flush-face on bed, pegs up
  }
} else assembly();
