// =====================================================================
//  SPDX-FileCopyrightText: 2026 andeye Ltd (trading as AMYBO)
//  SPDX-License-Identifier: CERN-OHL-S-2.0
//
//  Copyright andeye Ltd 2026.
//
//  This source describes Open Hardware and is licensed under the
//  CERN-OHL-S v2 (https://ohwr.org/cern_ohl_s_v2.txt).
//
//  You may redistribute and modify this source and make products using
//  it under the terms of the CERN-OHL-S v2. This source is distributed
//  WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF
//  MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A PARTICULAR
//  PURPOSE. Please see the CERN-OHL-S v2 for applicable conditions.
//
//  Source location:
//    https://github.com/amy-bo/electroPioreactor/tree/main/Components/CentrifugeTubeCoupler
//
//  More permissive terms are available from AMYBO: see the README.
// =====================================================================

// =====================================================================
//  50 ml centrifuge-tube coupler
//
//  A double-ended threaded collar that joins two 50 ml conical
//  centrifuge tubes (Corning 352070-style) rim to rim. Each tube screws
//  into one end until the two rim faces meet in the middle: no central
//  wall, shoulder or seal seat, so the passage through the coupler is
//  the tubes' own bore.
//
//  Self-contained: no libraries needed (own helical thread module).
//  Print standing upright, as modelled (axis = Z), no supports.
//
//  Measurements, provenance and printing notes: see README.md.
// =====================================================================

/* [What to build] */
// "coupler" = the full double-ended collar; "gauge" = one 12 mm
// threaded ring for a 15-minute test-fit print; "section" = coupler cut
// in half for inspection (do not print).
part = "coupler"; // [coupler, gauge, section]

/* [Tube thread] */
// Tube figures are measured, not taken from a drawing; see README.
// Override them if your tubes differ.
// Outside diameter over the tube's thread crests, mm.
tube_thread_od  = 30.75;
// Outside diameter at the tube's thread root, at the opening, mm.
tube_root_od    = 28.89;
// Outside diameter of the tube body at the base of the thread skirt, mm.
tube_body_od    = 27.69;
// Inner diameter of the tube rim, mm. Nothing in this part narrows the
// bore to anywhere near it.
tube_rim_id     = 27.81;
// Thread pitch, mm.
thread_pitch    = 3.0;
// Number of thread starts.
thread_starts   = 1;
// Axial thickness of the TUBE's own thread ridge, mm.
tube_ridge_w    = 1.12;
// Thread zone on the tube, measured down from the rim face, mm: the
// thread starts tube_thread_top below the rim and ends tube_thread_end
// below it. These two set the length of the coupler: each half is
// tube_thread_end + mid_relief, so the rim of a tube screwed fully in
// lands on the middle plane and the two rims meet.
tube_thread_top = 1.67;
tube_thread_end = 9.89;

/* [Fit / clearance] */
// Radial clearance between the tube's thread crests and the printed
// bore, mm per side. 0.3-0.4 for a 0.4 mm nozzle; increase if it binds.
radial_clearance = 0.35;
// Diameter over the printed thread crests AS DRAWN, mm. This is the one
// number that decides whether the coupler grips: it is drawn large to
// allow for print shrink. If it binds, raise it by 0.2 at a time; if it
// strips or feels shallow, lower it.
crest_dia_design = 30.0;
// Diameter lost in printing, mm. Used only to echo the predicted
// printed crest; it does not change the geometry.
print_shrink     = 0.2;
// Axial (flank) clearance in the tube's groove, mm, total. The printed
// ridge is made this much narrower than the measured groove.
axial_clearance  = 0.25;
// Gap left between the top of the printed thread and the start of the
// tube's thread, mm, so the printed ridge never runs up against the
// plain neck above the tube's thread.
thread_top_gap   = 0.3;
// Flank angle measured from the tube axis (= from horizontal, for a
// straight flank), degrees. 45 = printable upright without supports.
// Do not go below ~40.
flank_angle      = 45;
// Angle of the DOWNWARD-FACING flank only, i.e. the one printed as an
// overhang, degrees. Equal to flank_angle leaves the standard 45 deg
// self-supporting slope and does not change the fit. Do not exceed 50.
flank_angle_lower = 45;
// Lead-in at each mouth, mm: a straight relief band of radial width
// mouth_chamfer (height mouth_relief_h) at the very end of the bore,
// then a 45 deg chamfer up to the thread root. The straight band keeps
// the first layer wide and stops elephant's foot narrowing the thread
// entry. The thread starts at mouth_relief_h + mouth_chamfer above the
// end face.
mouth_chamfer    = 0.4;
mouth_relief_h   = 0.6;
// Plain bore between the end of the thread and the middle plane, mm.
// This is the band the two rims meet in: it is bored to the thread root
// diameter, so there is no shoulder, step or register near the rims.
// Keep it at 0.5 mm or more.
mid_relief       = 1.0;

/* [Body] */
// Wall thickness outside the thread root, mm.
sleeve_wall    = 2.2;
// Number of grip flutes around the outside (0 = plain).
grip_flutes    = 18;
// Flute radius, mm.
grip_flute_r   = 1.2;

/* [Printability] */
// Radial width of the printed foot flange at the bottom end, mm
// (0 = none). This is a brim that is part of the model: it widens the
// first layer to a wide continuous ring so the part cannot peel off the
// bed. It tapers back into the body at 45 deg. Trim it off with a knife
// afterwards if you want (it is outside everything functional).
foot_flange   = 0.8;
// Straight height of the flange before it tapers back, mm.
foot_h        = 0.5;
// true = the same flange at the top as at the bottom, so the collar is
// symmetric end to end (either end takes a tube). It is the bottom
// flange mirrored, so its UNDERSIDE is a 45 deg cone flaring outward as
// it rises - not a square-edged disc, which would be a 90 deg overhang
// needing support. It sits inside the existing length and adds nothing
// to the height.
flange_both_ends = true;
// 45 deg outer chamfer at the TOP end, mm, used only when
// flange_both_ends = false (the top flange replaces it). There is never
// an outer chamfer at the bottom: it would narrow the first layer.
top_chamfer   = 0.8;
// Axial length of the ramp at each end of the thread ridge, mm.
// 0 = cut the ridge off flat, which leaves a flat downward-facing face
// in the upper socket (and at the thread start of the lower one).
// Setting it to thread_depth (0.9) makes those ends 45 deg cones
// instead; it also gives the tube an easier start. The ramp eats
// thread_end_ramp of engagement at each end of the threaded zone.
thread_end_ramp = 0.9;

/* [Quality] */
// Segments per turn for the thread and circles.
segs = 96;
$fn  = segs;

// ---------------------------------------------------------------------
//  Derived dimensions
// ---------------------------------------------------------------------
eps = 0.01;
lead          = thread_pitch * thread_starts;          // advance per turn
r_int_root    = tube_thread_od / 2 + radial_clearance; // sleeve thread root
r_int_crest   = crest_dia_design / 2;                  // sleeve thread crest
ridge_height  = r_int_root - r_int_crest;              // printed ridge height
outer_r       = r_int_root + sleeve_wall;
tube_depth    = (tube_thread_od - tube_root_od) / 2;   // 0.93
tube_groove_w = thread_pitch - tube_ridge_w;           // 1.88
thread_length = tube_thread_end - tube_thread_top;     // 8.22

// Printed ridge, as a straight-flanked trapezoid measured from the
// MID-DEPTH radius outward and inward. ridge_embed is how far the base
// is buried in the sleeve wall; the flanks keep their angle through it,
// so the printed underside really is at flank_angle.
ridge_embed   = 0.2;
// Width at mid depth: the tube's groove, less the flank clearance.
ridge_mid     = tube_groove_w - axial_clearance;
r_ridge_mid   = r_int_crest + ridge_height / 2;
r_ridge_base  = r_int_root + ridge_embed;
// z offsets of the four profile corners (upper = +, lower = -)
dz_crest_up   =  ridge_mid / 2 - (ridge_height / 2) * tan(flank_angle);
dz_crest_lo   = -ridge_mid / 2 + (ridge_height / 2) * tan(flank_angle_lower);
dz_base_up    =  ridge_mid / 2 + (r_ridge_base - r_ridge_mid) * tan(flank_angle);
dz_base_lo    = -ridge_mid / 2 - (r_ridge_base - r_ridge_mid) * tan(flank_angle_lower);
ridge_crest   = dz_crest_up - dz_crest_lo;             // flat at the tip
ridge_base    = dz_base_up - dz_base_lo;               // width in the wall
assert(ridge_base < thread_pitch - 0.1,
       "Thread ridges overlap: increase pitch or reduce depth/flank angle");
assert(ridge_crest > 0.3,
       "Thread crest flat is thinner than a nozzle: reduce flank_angle_lower");
assert(flank_angle_lower >= flank_angle && flank_angle_lower <= 50,
       "flank_angle_lower must be between flank_angle and 50");

// One half = the tube's thread zone + the plain band the rims meet in.
// With half_h set from tube_thread_end, a tube screwed all the way in
// puts its rim on the middle plane, and the printed thread sits exactly
// over the tube's thread: from mid_relief (= thread_z0) at the bottom
// to thread_top_gap short of the tube's first thread at the top.
thread_z0 = mouth_relief_h + mouth_chamfer;            // where the thread starts
half_h    = tube_thread_end + mid_relief;              // mouth to middle plane
thread_z1 = half_h - tube_thread_top - thread_top_gap; // where it ends
total_h   = 2 * half_h;
// Grip flutes: inset by the same amount at BOTH ends, so they clear the
// flange at each end and both flanges stay unbroken rings.
flute_z0  = foot_h + foot_flange + 0.3;                // inset at each end
flute_h   = total_h - 2 * flute_z0;                    // span of one flute

// First layer: the bottom face is the ring between the bore relief and
// the outside of the foot flange, with nothing cut into it.
first_ring_id = 2 * (r_int_root + mouth_chamfer);
first_ring_od = 2 * (outer_r + foot_flange);
first_ring_w  = (first_ring_od - first_ring_id) / 2;

echo(str("Coupler: OD ", 2 * outer_r, " mm, length ", total_h,
         " mm, clear bore ", 2 * r_int_root, " mm, thread zone ",
         thread_z0, "-", thread_z1, " mm from each end (",
         (thread_z1 - thread_z0) / lead, " turns), ridge crest flat ",
         ridge_crest, " mm, ridge width at mid depth ", ridge_mid,
         " mm in a ", tube_groove_w, " mm groove"));
echo(str("Thread engagement: crest ", crest_dia_design,
         " mm as drawn, about ", crest_dia_design - print_shrink,
         " mm printed, against a tube measuring ", tube_thread_od,
         " mm over its crests = ",
         (tube_thread_od - (crest_dia_design - print_shrink)) / 2,
         " mm radial (a cap that grips has 0.39 mm). Printed ridge ",
         ridge_height, " mm high in a ", tube_depth, " mm deep groove."));
echo(str("First layer: ring ", first_ring_id, " - ", first_ring_od,
         " mm dia = ", first_ring_w, " mm wide, continuous (flutes start at ",
         flute_z0, " mm)"));
assert(first_ring_w >= 2.0,
       "First layer ring is under 2 mm wide: raise foot_flange or lower mouth_chamfer");
assert(mid_relief >= 0.5,
       "mid_relief must be at least 0.5 mm so the thread cannot reach the rims");
assert(2 * r_int_root > tube_thread_od,
       "Bore is narrower than the tube rim: the coupler would touch the rim faces");
assert(thread_z1 > thread_z0 + thread_end_ramp * 2 + 0.5,
       "Threaded zone is too short for the end ramps");
assert(ridge_height > 0.4 && ridge_height < tube_depth,
       "Printed ridge must be shallower than the tube's groove and at least 0.4 mm: change crest_dia_design");
assert(ridge_mid > 0.5, "Printed ridge is too thin: check tube_ridge_w and the pitch");

// ---------------------------------------------------------------------
//  Helical ridge (internal thread), built as one polyhedron.
//  Profile in (radius, z-offset): base embedded in the wall, crest inward.
//  The ends are ramped out at 45 deg rather than cut off flat, so the
//  upper socket has no flat downward-facing thread end.
// ---------------------------------------------------------------------
module helix_ridge(lead, z0, z1, start_angle = 0) {
    turns = (z1 - z0) / lead + 2;          // overshoot, trimmed later
    n     = ceil(turns * segs);
    prof  = [ [r_ridge_base, dz_base_lo], [r_int_crest, dz_crest_lo],
              [r_int_crest, dz_crest_up], [r_ridge_base, dz_base_up] ];
    pts = [ for (i = [0:n]) let(a = start_angle + i * 360 / segs,
                                z = z0 - lead + i * lead / segs)
              for (p = prof) [p[0] * cos(a), p[0] * sin(a), z + p[1]] ];
    side = [ for (i = [0:n - 1]) for (j = [0:3])
               let(a = i * 4 + j, b = i * 4 + (j + 1) % 4)
               [a, a + 4, b + 4, b] ];   // outward-facing winding
    caps = [ [0, 1, 2, 3], [n * 4 + 3, n * 4 + 2, n * 4 + 1, n * 4] ];
    ramp = min(thread_end_ramp, (z1 - z0) / 2 - 0.1);
    // The ramp cones run from just inside the bore wall (so what is left
    // of the ridge at each end is buried in the wall, never a loose
    // sliver) to just past the crest, at 45 deg when ramp = thread_depth.
    ra_out = r_int_root + 0.1;
    ra_in  = r_int_crest - 0.1;
    intersection() {
        polyhedron(points = pts, faces = concat(side, caps), convexity = 10);
        difference() {
            translate([0, 0, z0]) cylinder(r = r_ridge_base + 1, h = z1 - z0);
            if (ramp > 0) {
                // ramp in at the start: ridge flush with the wall at z0,
                // full depth at z0 + ramp
                translate([0, 0, z0 - eps])
                    cylinder(r1 = ra_out, r2 = ra_in, h = ramp + 0.2 + eps);
                // and out again at the end
                translate([0, 0, z1 - ramp - 0.2])
                    cylinder(r1 = ra_in, r2 = ra_out, h = ramp + 0.2 + eps);
            }
        }
    }
}

// Internal thread for one socket, mouth at z = 0, going up to z = len.
module internal_thread(len) {
    for (s = [0:thread_starts - 1])
        helix_ridge(lead, thread_z0, len, s * 360 / thread_starts);
}

// Mouth treatment at z = 0, cutting upwards: a straight relief band
// (elephant's-foot insurance, and it keeps the first layer wide), then
// a 45 deg chamfer up to the thread root.
module mouth() {
    translate([0, 0, -eps])
        cylinder(r = r_int_root + mouth_chamfer, h = mouth_relief_h + eps);
    translate([0, 0, mouth_relief_h - eps])
        cylinder(r1 = r_int_root + mouth_chamfer, r2 = r_int_root,
                 h = mouth_chamfer + eps);
}

// The whole bore: one straight through-hole, plus a mouth at each end.
// No step, shoulder, seat or divider anywhere along it.
module bore() {
    translate([0, 0, -eps]) cylinder(r = r_int_root, h = total_h + 2 * eps);
    mouth();
    translate([0, 0, total_h]) mirror([0, 0, 1]) mouth();
}

// One grip flute, standing on z = 0, flute_h tall, tapered 45 deg at
// both ends. The top taper matters: a plain cylinder has a FLAT cap, so
// a blind flute would leave a small flat (0 deg) ceiling in each groove
// - 18 little bridges. The cone makes that ceiling a 45 deg face, the
// same angle as everything else on the part. The bottom taper faces up,
// so it costs nothing and makes the two ends match.
module flute() {
    r = grip_flute_r;
    union() {
        cylinder(r1 = 0, r2 = r, h = r, $fn = 16);
        translate([0, 0, r]) cylinder(r = r, h = flute_h - 2 * r, $fn = 16);
        translate([0, 0, flute_h - r]) cylinder(r1 = r, r2 = 0, h = r, $fn = 16);
    }
}

module grip() {
    // vertical flutes: print cleanly upright, give finger grip. They
    // start above the foot flange so they cannot nibble the first layer
    // into 18 separate islands; their floor faces up, so no overhang.
    if (grip_flutes > 0)
        for (i = [0:grip_flutes - 1])
            rotate(i * 360 / grip_flutes)
                translate([outer_r + grip_flute_r * 0.35, 0, flute_z0])
                    flute();
    // outer chamfer at the TOP end, only when there is no top flange
    if (top_chamfer > 0 && !flange_both_ends)
        translate([0, 0, total_h])
            rotate_extrude() polygon([[outer_r - top_chamfer, eps],
                                      [outer_r + 1, eps],
                                      [outer_r + 1, -(top_chamfer + 1)]]);
}

// Printed flange at z = 0: a brim that is part of the model. Straight
// for foot_h, then back to the body at 45 deg. Mirrored to the top end
// by coupler() when flange_both_ends is set: upside down, that 45 deg
// face becomes the flange's underside, flaring outward as it rises, so
// it prints without support.
module foot() {
    if (foot_flange > 0)
        rotate_extrude()
            polygon([[outer_r - eps, 0],
                     [outer_r + foot_flange, 0],
                     [outer_r + foot_flange, foot_h],
                     [outer_r - eps, foot_h + foot_flange]]);
}

module coupler() {
    union() {
        difference() {
            cylinder(r = outer_r, h = total_h);
            bore();
            grip();
        }
        // one thread per end. Rotate, NOT mirror: mirroring would make a
        // left-hand thread at the top.
        internal_thread(thread_z1);
        translate([0, 0, total_h]) rotate([180, 0, 0]) internal_thread(thread_z1);
        foot();
        if (flange_both_ends) translate([0, 0, total_h]) mirror([0, 0, 1]) foot();
    }
}

// Test ring: one threaded socket, open at both ends, with the same
// bottom-end treatment as the coupler so the test print tests that too.
module gauge() {
    h = half_h;          // one socket, exactly as on the real part
    union() {
        difference() {
            cylinder(r = outer_r, h = h);
            translate([0, 0, -eps]) cylinder(r = r_int_root, h = h + 2 * eps);
            mouth();
        }
        helix_ridge(lead, thread_z0, thread_z1);
        foot();
    }
}

if (part == "coupler") coupler();
else if (part == "gauge") gauge();
else if (part == "section") {
    echo("*** part = \"section\" is a cutaway for inspection - DO NOT PRINT, and do not export it as an STL ***");
    difference() { coupler(); translate([0, -50, -1]) cube([50, 100, 200]); }
}
