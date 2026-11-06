// =====================================================================
// Vial Cap render scene
//
// The one-piece Vial Cap (from Vial Cap.scad, untouched) in its working
// context: 40 ml glass vial, septum, cathode + hollow anode, needles with
// luer hubs, knurled thumb screws, PTFE stir flea, heater PCB, and the
// LED -> photodiode OD light path.
//
// Open it in OpenSCAD (F5) for a coloured, see-through-glass preview, or
// export one material group at a time with  -D 'component="<name>"'
// (render/build.mjs does that and builds the interactive viewer).
//
// Coordinates are Vial Cap.scad's: cap bottom at z=0, column up +Z,
// openings at +Y ("front"), poka-yoke flange at -X.
// =====================================================================
include <Vial Cap.scad>
view = "none";                 // Vial Cap.scad draws nothing; this file draws the scene

// ---- what to draw ---------------------------------------------------
component = "all";   // "all" (coloured preview) | one material group:
                     // "cap" "septum" "cathode" "anode" "needles" "hubs" "screws" "washers"
                     // "glass" "flea" "thermal_pad" "pcb" "pcb_copper" "pcb_parts"
                     // "temp_module" "temp_module_parts" "temp_probe"
                     // "led" "led_die" "led_legs" "pd" "pd_die" "pd_board" "beam"

// ---- electrodes -----------------------------------------------------
anode_side          = -1;    // -1 = anode on -X: on the RIGHT when viewed with the big syringe opening (+Y) at the front; +1 = on +X
anode_inner_diameter = 4;    // mm - the anode is a tube (MMO / Pt-Ti)
electrode_length     = 100;  // mm - AEP 0.2 kit: MMO anode and 316 cathode are both 100 mm (docs/components/mmo-anode.yaml, stainless-steel-cathode.yaml)
anode_active_length  = 70;   // mm - MMO-coated length at the bottom of the anode; the top is bare Ti
electrode_tip_z      = top_face_z - electrode_length;   // tops flush with the top-stop face (step 07)

// ---- 40 ml EPA vial (24-400 neck) ----------------------------------
vial_od        = 27.5;   // body outer diameter
vial_height    = 95;     // rim to outside of base
vial_wall      = 1.3;    // body wall
vial_base      = 2.0;    // base thickness
neck_od        = 22.4;   // neck at the thread ROOT (24-400 "E" dim; crest ~24): clears the cap thread (minor 22.9) and gasket ridge (22.5) - the glass thread isn't modelled
neck_length    = 12;     // rim down to the start of the shoulder
shoulder_length = 5;     // neck -> body taper
base_corner_radius = 3;
rim_z          = gasket_z;                         // glass rim presses on the septum underside
base_z         = rim_z - vial_height;              // outside of the base
floor_z        = base_z + vial_base;               // inside floor

// ---- needles (14 G blunt, luer hubs) -------------------------------
// [port index (1-based, Vial Cap.scad's guide order), length, tip z, bent?]
// 1/2 straight Media Out (80 mm, sets the level) + Media In; 3/4 bent gas outlets; 5 spare
needle_od = 2.1; needle_id = 1.6; bend_radius = 3;
bend_angle = 15;              // deg - bent gas needles lean radially OUTWARD by this much above the bend
bend_above_top = 6;           // mm - the bend starts this far above the top-stop face
needles = [
  [1, 80, -23, false],     // Media Out - tip at the 30 ml level
  [2, 75, -18, false],     // Media In - above the level
  [3, 75,  -3, true ],     // Gas Out
  [4, 75,  -3, true ],     // Gas Out - safety
];

// ---- thumb screws (DIN 464-style M3 knurled) ------------------------
thumb_head_d = 12; thumb_head_h = 4.5; thumb_collar_d = 6; thumb_collar_h = 2;
washer_od = 7; washer_id = 3.2; washer_t = 0.5;

// ---- stir flea (rounded-end PTFE rod) -------------------------------
flea_length = 15; flea_d = 5; flea_angle = 25;
flea_ring_r = flea_d/2 + 0.125;          // pivot ring outer radius: the flea rests on its ring
flea_axis_z = floor_z + flea_ring_r + 0.05;   // flea axis height (ring 0.05 above the inner floor)
flea_top_z  = flea_axis_z + flea_ring_r;

// ---- heater PCB under the vial --------------------------------------
// The real Pioreactor heater PCB - Altium "Heater.PcbDoc" rev 20 (2022-10-23), published in
// github.com/Pioreactor/hardware/tree/main/heater_20ml/Heater_Jan_0824_Public (Manufacture/gerber.zip
// + Assembly/Pick Place for Heater(DEV).csv). The same board sits under the 40 ml v1.5 vial
// (docs.pioreactor.com 40 ml v1.5 wetware assembly, steps 3-5: same heater photos, O-ring + 2 screws).
// Aluminium-core board: its flat aluminium back faces UP to the vial (the thermal pad sticks on it),
// the white-soldermasked component side faces DOWN. Board coords below are Altium's top-layer coords.
pcb_d       = 27.5;    // outline circle (Edge.Cuts Heater.GM1: arcs R13.75 about the origin) - same as vial_od
pcb_flat    = 13.5;    // ...cut by four 5.2 mm flats at x = +/-13.5 and y = +/-13.5 (GM1)
pcb_t       = 1.6;     // ASSUMED standard 1.6 mm aluminium MCPCB - thickness is not in the gerbers
pcb_hole_x  = 10;      // 2 non-plated holes at (+/-10, 0) (NC drill Heater-NonPlated.TXT)...
pcb_hole_d  = 3.7;     // ...3.7 mm, under the M2.5 SMT standoffs the holder's 2 brass M2.5 screws go into
thermal_pad_t = 0.5; thermal_pad_d = 26;
pcb_top_z = base_z - thermal_pad_t;   // aluminium face, under the thermal pad
pcb_bot_z = pcb_top_z - pcb_t;        // component side (faces down)
c_heater_mask = [0.95,0.95,0.93];     // white soldermask (docs photos)

// ---- Precision Temperature Upgrade Kit (MLX90632 FIR sensor in the SPEC pocket) ------
// Pioreactor's kit = an Adafruit #6403 "MLX90632 FIR Remote Thermal Temperature Sensor - Medical
// Grade STEMMA QT" breakout + STEMMA-QT cable + optional M2.5 x 8 screws (docs.pioreactor.com/
// user-guide/precision-temperature-upgrade-kit; its photos show the Adafruit board in the SPEC pocket
// of the 40 ml vial holder, LED pad right, 6 header holes left; this repo: docs/steps/step-04-vial-
// holder-and-xr.md). Board geometry is from Adafruit's Eagle file "Adafruit MLX90632 FIR Remote
// Temperature Sensor.brd" (github.com/adafruit/Adafruit-MLX90632-FIR-Remote-Thermal-Temperature-Sensor-PCB).
// It is NON-CONTACT: the MLX90632 (50 deg FOV) looks at the glass through the pocket, no probe touches it.
// Its components face the vial (the photos show the board's bottom silkscreen from outside, with the
// STEMMA-QT cable leaving from behind the board at its lower end); long (25.4) edge vertical.
temp_board_l = 25.4;    // board x: 1.0" outline, 2.54 corner radii (Eagle layer 20) - stands vertical
temp_board_w = 17.78;   // board y: 0.7" (Eagle layer 20) - tangential to the vial
temp_board_t = 1.6;     // ASSUMED Adafruit standard FR4 thickness - not in the .brd
temp_hole_d  = 2.5;     // 4 x MOUNTINGHOLE_2.5_PLATED at (2.54|22.86, 2.54|15.24)
// Where it sits. The XR vial holder CAD is not public, so these are INFERRED from the docs photos:
temp_spec_rel = 157.5;  // RENDER CHOICE (Martin, 2026-11-06): high and to the viewer's LEFT in the front view, clear of the LED's
                        // beam and of the frontal view, reading the liquid through the wall. The stock SPEC pocket was 180:
                        // INFERRED from the docs photos: seen from outside, left to right, the faces read
                        // [eye-spy, its cable going to the sensor] | SPEC | X2 (an LED pocket). On the optics section's
                        // octagon (LED 0, eye-spys -45/45/90/135, CCW = left to right) that puts SPEC at 180: straight
                        // across from the IR LED (the transmitted-light "spectrometer" pocket), next to the 135 eye-spy.
                        // (world angle = optics_rotation + temp_spec_rel, applied in temp_place(): optics_rotation is defined below)
temp_mlx_below_level = 7;    // RENDER CHOICE: MLX90632 centre this far below the 30 ml level (the Media Out needle tip)
temp_board_bot_z = needles[0][2] - temp_mlx_below_level - 12.446;   // (stock: base_z) INFERRED (+/-3 mm) for the stock pocket: the board's lower edge is level with the bottom of the vial holder's
                        // pocket band in the docs photos, i.e. about the outside of the vial base; MLX centre ~12 mm above it
temp_board_r = 22;      // INFERRED: radius of the board's component (vial-side) face. The photos show the 17.78 mm board
                        // recessed into one face of the octagonal collar (face ~23 mm wide -> apothem ~28 mm); a 17.78 mm
                        // board only fits a 45 deg face at r >= 8.89/tan(22.5) = 21.5 mm
temp_mlx_h   = 1.0;     // MLX90632 SFN 3 x 3 x 1 mm package (Melexis datasheet)
temp_mlx_gap = temp_board_r - temp_mlx_h - vial_od/2;   // -> 7.25 mm air/holder-wall from the MLX90632 window to the glass
c_temp_mask  = [0.05,0.05,0.06];   // Adafruit black soldermask (docs photos)

// ---- optics: Pioreactor 40 ml v1.5 + XR kit: one IR LED, four eye-spy photodiode boards
// Pockets sit on the faces of the octagonal vial-holder collar, 45 deg apart. Going
// counter-clockwise seen from above (= left to right seen from outside), docs photos:
//   "45" pocket (-45) | IR LED (0) | REF (+45) | 90 (+90) | 135 (+135)
// (scatter angle is symmetric, so the "45" pocket sits on the LED's other side.)
// The three other faces (180/225/270) are the unused LED pockets (B/C/D, capped) - INFERRED.
optics_rotation = 232.5;           // world angle of the IR LED (deg, CCW from +X): puts the 3 empty pockets (rel. 225-315) facing a camera at the front (+Y) right, so no board hides the vial
pd_rel    = [-45, 45, 90, 135];    // eye-spy pockets rel. to the LED: 45, REF, 90, 135
pd_is_ref = [false, true, false, false];
optics_z  = (electrode_tip_z + flea_top_z)/2;   // light path height: centred between the electrode tips and the flea top (real holder height unknown)
led_gap   = 2.0;                   // LED dome tip to glass (APPROX)
pd_gap    = 2.5;                   // eye-spy PCB back face (vial side) to glass; the holder wall + window lie between (APPROX)
// eye-spy PCB (hardware/eye-spy/Source/eye-spy.kicad_pcb, Pioreactor/hardware): 13 x 33 x 1.582, R2.54 corners,
// 4x d2.7 holes at (+-3.96, 2.54 / 30.46); VEMD2000X01 reverse-mount photodiode 6.42 above the bottom edge,
// looking through a d2.3 hole at the vial; JST connectors at the top (board mounted upright).
es_w = 13; es_h = 33; es_t = 1.582; es_r = 2.54; es_pd_v = 6.42;
beam_r0   = 1.4;                   // beam radius at the LED dome
beam_r1   = 3.5;                   // beam radius at the far wall
scat_r    = 0.35;                  // scatter-ray radius

assert(optics_z - beam_r1 > flea_top_z + 1, "light path must clear the flea");
assert(optics_z + beam_r1 < electrode_tip_z - 1, "light path must pass under the electrode tips");
assert(optics_z + beam_r1 < min([for (n=needles) n[2]]) - 1, "light path must pass under the needle tips");

// ---- colours (OpenSCAD preview only; the web viewer sets real materials)
// Vial Cap.scad colours its own parts inside cap()/column()/gasket(), and an inner color()
// beats ours - so override its colour variables (literals: a reassignment is evaluated
// where the variable was FIRST defined) to get a one-colour cap and an off-white septum.
color_cap = [0.16,0.17,0.19]; color_column = color_cap; color_gasket = [0.93,0.90,0.86,0.9];
c_cap = color_cap; c_septum = color_gasket; c_steel=[0.78,0.80,0.83]; c_mmo=[0.30,0.29,0.31];
c_hub=[0.45,0.62,0.22,0.85]; c_glass=[0.80,0.93,0.95,0.22]; c_flea=[0.97,0.97,0.96];
c_pcb=[0.06,0.20,0.12]; c_copper=[0.85,0.66,0.30]; c_parts=[0.92,0.88,0.78]; c_pad=[0.62,0.62,0.66];
c_led=[0.75,0.85,1,0.55]; c_die=[1,0.2,0.2]; c_pd=[0.08,0.08,0.09]; c_beam=[1,0.15,0.2,0.18];

// =====================================================================
module want(name, c) if (component=="all" || component==name) color(c) children();

// ---- glass vial -----------------------------------------------------
module vial2d() {   // half-section (x = radius), z absolute
  R = vial_od/2; Rn = neck_od/2; ri = neck_inner_diameter/2; Rb = R - vial_wall;
  zn = rim_z - neck_length; zs = zn - shoulder_length;
  offset(r=0.35, $fn=16) offset(delta=-0.35)    // round the rim and every convex edge
  difference() {
    union() {   // round ONLY the base corner (rounding the whole outline would dome the narrow rim)
      hull() {
        translate([-5,base_z]) square([5+R-base_corner_radius, 0.01]);
        translate([R-base_corner_radius, base_z+base_corner_radius]) circle(r=base_corner_radius, $fn=32);
        translate([-5,zs-0.01]) square([5+R, 0.01]);
      }
      polygon([[-5,zs-0.01],[R,zs-0.01],[R,zs],[Rn,zn],[Rn,rim_z],[-5,rim_z]]);   // shoulder + neck
    }
    offset(r=base_corner_radius-0.8, $fn=32) offset(delta=-(base_corner_radius-0.8))
      polygon([[-5,floor_z],[Rb,floor_z],[Rb,zs+1.2],[ri,zn+0.8],[ri,rim_z+5],[-5,rim_z+5]]);
  }
}
module glass() rotate_extrude($fn=160) intersection() { vial2d(); translate([0,base_z-1]) square([vial_od, vial_height+2]); }

// ---- electrodes -----------------------------------------------------
module electrode(x, id=0, z0=0, h=electrode_length) translate([x,0,electrode_tip_z+z0]) difference() {   // z0/h: a section of it, from the tip
  cylinder(d=rod_diameter, h=h, $fn=64);
  if (id>0) translate([0,0,-1]) cylinder(d=id, h=h+2, $fn=48);
}

// ---- needles + luer hubs -------------------------------------------
function port_xy(i) = guide_pts()[i-1];
module tube2d() difference() { circle(d=needle_od, $fn=24); circle(d=needle_id, $fn=20); }
module hub(ear_angle=0) {   // female luer-lock hub, axis +Z, needle end at z=0; ears at ear_angle, ear_angle+180
  difference() {
    union() {
      rotate_extrude($fn=48) polygon([[0,-1.5],[1.6,-1.5],[2.1,0],[2.6,8],[3.1,9],[3.1,15],[0,15]]);
      for (a=[0,180]) rotate(ear_angle+a) translate([2.6,-1.4,13.6]) cube([1.8,2.8,1.4]);     // luer-lock ears
      for (a=[45,135,225,315]) rotate(a) translate([2.3,-0.35,1]) cube([0.9,0.7,8]);   // grip fins
    }
    translate([0,0,-2]) cylinder(d=needle_od-0.05, h=4, $fn=24);
    translate([0,0,7.5]) cylinder(d1=2.6, d2=4.3, h=7.6, $fn=40);               // luer taper
    translate([0,0,1.5]) cylinder(d=1.2, h=7, $fn=16);
  }
}
// straight: one tube up from the tip. bent: vertical shaft up to bend_above_top over the top
// face -> bend of bend_angle (radius bend_radius) leaning radially OUTWARD -> straight run
// (the rest of the needle length) -> hub.
function bend_z(n)   = top_face_z + bend_above_top;
function bend_arc()  = bend_angle*PI/180*bend_radius;
function bend_run(n) = n[1] - (bend_z(n) - n[2]) - bend_arc();
function bend_end()  = [bend_radius*(1-cos(bend_angle)), 0, bend_radius*sin(bend_angle)];   // arc end, local (x = radial out)
module needle_path(n) {
  p = port_xy(n[0]); L = n[1]; zt = n[2]; bent = n[3];
  a = atan2(p[1], p[0]);                                   // bent ones lean radially outward
  if (!bent) translate([p[0],p[1],zt]) linear_extrude(L) tube2d();
  else {
    assert(bend_run(n) > 0, "needle too short for its bend height");
    translate([p[0],p[1],zt]) linear_extrude(bend_z(n)-zt) tube2d();
    translate([p[0],p[1],bend_z(n)]) rotate(a) {
      translate([bend_radius,0,0]) rotate([90,0,0]) rotate([0,0,180-bend_angle])
        rotate_extrude(angle=bend_angle, $fn=32) translate([bend_radius,0]) tube2d();
      translate(bend_end()) rotate([0,bend_angle,0]) linear_extrude(bend_run(n)) tube2d();
    }
  }
}
module needle_hub(n) {
  p = port_xy(n[0]); L = n[1]; zt = n[2]; a = atan2(p[1], p[0]);
  if (!n[3]) translate([p[0],p[1],zt+L]) hub(90);   // ears along Y: the straight hubs are only 6.8 mm apart along X
  else translate([p[0],p[1],bend_z(n)]) rotate(a) translate(bend_end()) rotate([0,bend_angle,0]) translate([0,0,bend_run(n)]) hub(90);
}

// ---- knurled thumb screws -------------------------------------------
module thumb_screw() {   // axis +X, clamp outer face at x=0; head sits on the washer
  shank = clamp_outer_x-(rod_offset+rod_diameter/2);
  translate([-shank,0,0]) rotate([0,90,0]) cylinder(d=2.9, h=shank+washer_t+0.1, $fn=24);   // M3 shank, tip on the rod
  translate([washer_t,0,0]) rotate([0,90,0]) {
    cylinder(d=thumb_collar_d, h=thumb_collar_h, $fn=48);
    translate([0,0,thumb_collar_h]) difference() {
      hull() {
        cylinder(d=thumb_head_d-1, h=0.01, $fn=96);
        translate([0,0,0.5]) cylinder(d=thumb_head_d, h=thumb_head_h-1, $fn=96);
        translate([0,0,thumb_head_h-0.01]) cylinder(d=thumb_head_d-1, h=0.01, $fn=96);
      }
      for (k=[0:39]) rotate(k*9) translate([thumb_head_d/2,0,-1]) rotate(45) cube([0.55,0.55,thumb_head_h+2], center=false);   // straight knurl
    }
  }
}
module washer() rotate([0,90,0]) difference() { cylinder(d=washer_od, h=washer_t, $fn=48); translate([0,0,-1]) cylinder(d=washer_id, h=3, $fn=24); }
module screws_at() for (m=[0,1]) mirror([m,0,0]) translate([clamp_outer_x,0,bolt_axis_z]) children();

// ---- stir flea -------------------------------------------------------
module flea() translate([0,0,flea_axis_z]) rotate(flea_angle) rotate([0,90,0]) union() {
  hull() for (s=[-1,1]) translate([0,0,s*(flea_length-flea_d)/2]) rotate([90,0,0]) sphere(d=flea_d, $fn=40);   // sphere pole off the axis: avoids a degenerate hull
  rotate_extrude($fn=48) translate([flea_ring_r-0.225,0]) scale([0.5,1]) circle(d=0.9, $fn=16);   // pivot ring
}

// ---- heater PCB ------------------------------------------------------
module pcb_outline() intersection() { circle(d=pcb_d, $fn=120); square(2*pcb_flat, center=true); }
module pcb_holes() for (s=[-1,1]) translate([s*pcb_hole_x, 0]) circle(d=pcb_hole_d, $fn=32);
module pcb() translate([0,0,pcb_bot_z]) color(c_heater_mask) linear_extrude(pcb_t) difference() { pcb_outline(); pcb_holes(); }
// Component side, flipped face-down: rotate the Altium top layer 180 deg about Y, so local +z points DOWN
// away from the board and the connector (Altium -Y) stays at -Y, as in the old placeholder.
module heater_side() translate([0,0,pcb_bot_z]) rotate([0,180,0]) children();
// Exposed copper = every top-soldermask opening in Heater.GTS, parsed from the gerber (mask expansion
// 0.05 mm included): [x, y, w, h, corner r]. There is no trace heater - the heat comes from 15 x 3.9 ohm
// 1206 resistors (pick-and-place R12-R28; docs FAQ "How does heating work": "resistors ... convert ... into heat").
heater_pads = [
  [-9.2,-7.5,2.1,2.1,1.05], [9.2,-7.5,2.1,2.1,1.05], [-4.975,10.475,2.1,2.1,1.05], [5.325,6.875,2.1,2.1,1.05],   // 7 round test pads
  [2.95,6.875,2.1,2.1,1.05], [1.075,8.275,2.1,2.1,1.05], [-2.7,10.475,2.1,2.1,1.05],
  [-11.16,-5,1.11,1.83,0.303], [-8.24,-5,1.11,1.83,0.303], [-10.16,6.85,1.11,1.83,0.303], [-7.24,6.85,1.11,1.83,0.303],   // 1206 heater resistors
  [-10.16,4.65,1.11,1.83,0.303], [-7.24,4.65,1.11,1.83,0.303], [-5.81,2.3,1.11,1.83,0.303], [-2.89,2.3,1.11,1.83,0.303],
  [-5.81,4.6,1.11,1.83,0.303], [-2.89,4.6,1.11,1.83,0.303], [-5.81,-2.3,1.11,1.83,0.303], [-2.89,-2.3,1.11,1.83,0.303],
  [-1.46,2.2,1.11,1.83,0.303], [1.46,2.2,1.11,1.83,0.303], [-1.46,0,1.11,1.83,0.303], [1.46,0,1.11,1.83,0.303],
  [-1.46,-2.2,1.11,1.83,0.303], [1.46,-2.2,1.11,1.83,0.303], [7.24,4.65,1.11,1.83,0.303], [10.16,4.65,1.11,1.83,0.303],
  [2.89,-2.3,1.11,1.83,0.303], [5.81,-2.3,1.11,1.83,0.303], [2.89,4.6,1.11,1.83,0.303], [5.81,4.6,1.11,1.83,0.303],
  [2.89,2.3,1.11,1.83,0.303], [5.81,2.3,1.11,1.83,0.303], [8.24,-5,1.11,1.83,0.303], [11.16,-5,1.11,1.83,0.303],
  [7.24,6.85,1.11,1.83,0.303], [10.16,6.85,1.11,1.83,0.303],
  [-3,-5.35,0.7,2,0.206], [-2,-5.35,0.7,2,0.206], [-1,-5.35,0.7,2,0.206], [0,-5.35,0.7,2,0.206],   // J1 FFC contacts (7 x 1.00 mm)
  [1,-5.35,0.7,2,0.206], [2,-5.35,0.7,2,0.206], [3,-5.35,0.7,2,0.206],
  [-6.15,-7.7,2.2,2.9,0.596], [6.15,-7.7,2.2,2.9,0.596],                                             // J1 solder tabs
  [-2.28,7.3,0.78,0.8,0.22], [-3.22,7.3,0.78,0.8,0.22], [1.125,10.165,1.12,1.05,0.292], [1.125,11.635,1.12,1.05,0.292],   // C1-C4, R9
  [-2.64,8.6,1.05,1.12,0.292], [-4.11,8.6,1.05,1.12,0.292], [6,10.495,0.68,0.67,0.19], [6,9.565,0.68,0.67,0.19],
  [6.9,9.965,0.68,0.67,0.19], [6.9,9.035,0.68,0.67,0.19], [2.4,10.105,0.8,0.78,0.22], [2.4,11.045,0.8,0.78,0.22],
  [3.475,8.57,0.38,0.71,0.12], [3.975,8.57,0.38,0.71,0.12], [4.475,8.57,0.38,0.71,0.12], [4.975,8.57,0.38,0.71,0.12],   // U1 TMP1075 WSON-8
  [4.975,10.48,0.38,0.71,0.12], [4.475,10.48,0.38,0.71,0.12], [3.975,10.48,0.38,0.71,0.12], [3.475,10.48,0.38,0.71,0.12],
  [4.225,9.525,1.7,1,0],                                                                              // U1 exposed pad
  [-0.95,4.24,0.72,1.28,0.211], [0.95,4.24,0.72,1.28,0.211], [0,6.31,0.72,1.28,0.211],                 // U2 DRV5021 hall sensor (SOT-23)
  [-10,0,6.1,6.1,3.05], [10,0,6.1,6.1,3.05],                                                          // standoff rings
];
module pad2d(p) translate([p[0],p[1]]) let(w=p[2], h=p[3], r=max(p[4],0.01))
  hull() for (sx=[-1,1], sy=[-1,1]) translate([sx*(w/2-r), sy*(h/2-r)]) circle(r=r, $fn=16);
module pcb_copper() heater_side() linear_extrude(0.05)   // HASL/ENIG pads proud of the mask (colour: viewer's copper)
  difference() { union() for (p=heater_pads) pad2d(p); pcb_holes(); }
// Parts from the pick-and-place CSV (centre x, y; rotation). Heights are the ones Pioreactor's footprint
// names encode (R_1206_0.55mm, C_0603_1.0mm, CONN_..._2.7mm, MTL_..._3mm ...); bodies are nominal package sizes.
heater_resistors = [[8.7,4.65],[9.7,-5],[8.7,6.85],[4.35,2.3],[4.35,4.6],[4.35,-2.3],[0,2.2],[0,0],[0,-2.2],
                    [-4.35,2.3],[-4.35,4.6],[-4.35,-2.3],[-8.7,6.85],[-9.7,-5],[-8.7,4.65]];   // R28..R12, 3.9 ohm 1206, rot 180
module box_at(x, y, sx, sy, h) translate([x-sx/2, y-sy/2, 0.05]) cube([sx, sy, h-0.05]);   // body, sitting on the pads
module pcb_parts() heater_side() {
  for (r=heater_resistors) box_at(r[0], r[1], 3.2, 1.6, 0.55);                // 15 x 1206 heater resistors
  // J1 Molex 52207-0760: 7-pos 1.00 mm ZIF FFC, right angle, 2.7 mm tall; mouth faces the -Y board edge
  box_at(0, -7.6, 12.0, 4.6, 2.7);                                            // housing (body size APPROXIMATED)
  box_at(0, -10.5, 13.2, 1.2, 2.2);                                           // beige ZIF actuator bar (APPROXIMATED)
  box_at(4.225, 9.525, 2.0, 2.0, 0.8);                                        // U1 TMP1075 board temperature sensor (WSON-8 2x2)
  box_at(0, 5.275, 2.9, 1.3, 1.2);                                            // U2 DRV5021 hall sensor (stir-bar RPM), SOT-23
  box_at(-3.375, 8.6, 1.6, 0.8, 1.0);  box_at(1.125, 10.9, 0.8, 1.6, 1.0);   // C3, C1 0603 2.2 uF
  box_at(-2.75, 7.3, 1.0, 0.5, 0.7);   box_at(2.4, 10.575, 0.5, 1.0, 0.7);   // C4, C2 0402 0.1 uF
  box_at(6, 10.03, 0.5, 1.0, 0.7);                                            // R9 0402 10k
  for (s=[-1,1]) translate([s*pcb_hole_x, 0, 0.05]) difference() {           // MTL1/2 Wurth 9774030151R M2.5 x 3 mm SMT standoffs
    cylinder(d=5.1, h=3-0.05, $fn=36); translate([0,0,-1]) cylinder(d=2.5, h=5, $fn=20);   // OD APPROXIMATED; M2.5 bore
  }
}

// ---- Precision Temperature Upgrade Kit ---------------------------------
// Built in Adafruit's board coords (x 0..25.4, y 0..17.78, component side up), then stood up at +X:
// board x -> +Z, board y -> +Y (header edge y=0 on the viewer's left), component side -> -X (to the vial).
module temp_place() rotate(optics_rotation + temp_spec_rel)
  translate([temp_board_r, 0, temp_board_bot_z])
  rotate([0,-90,0]) translate([0, -temp_board_w/2, 0]) children();
temp_holes = [[2.54,2.54],[22.86,2.54],[2.54,15.24],[22.86,15.24]];
module temp_module() temp_place() translate([0,0,-temp_board_t]) linear_extrude(temp_board_t) difference() {
  offset(r=2.54, $fn=32) offset(delta=-2.54) square([temp_board_l, temp_board_w]);
  for (h=temp_holes) translate(h) circle(d=temp_hole_d, $fn=24);
  for (i=[0:5]) translate([6.35+2.54*i, 2.54]) circle(d=1.0, $fn=16);   // JP1 1x6 header holes (unpopulated)
}
// [x, y, size x, size y, height] - centres from the .brd placements (rotation applied), bodies nominal package sizes
temp_parts = [
  [22.67, 8.94, 4.3, 6.1, 2.95],   // CONN3 JST SH 4-pin side-entry STEMMA-QT socket (R90), mouth to the +x board end
  [ 2.74, 8.84, 4.3, 6.1, 2.95],   // CONN4 the same (R270), mouth to the -x end - the cable plugs in here, at the bottom
  [ 8.128, 8.763, 2.9, 1.6, 1.1],  // U2 AP2127K-3.3 regulator, SOT23-5
  [ 7.874, 5.715, 2.0, 1.25, 1.25],// C2 10 uF 0805
  [ 8.128,12.192, 2.0, 1.25, 1.25],// C3 10 uF 0805
  [11.811, 5.715, 1.6, 0.8, 0.8],  // C1 0.1 uF 0603
  [17.145,11.43, 3.2, 1.6, 0.5],   // R3 4 x 10k 0603 resistor pack
  [16.891, 7.747, 1.25, 2.0, 1.0], // Q2 BSS138 dual level-shifter, SOT363 (R90)
  [ 3.556,12.573, 0.8, 1.6, 0.6],  // D1 green power LED 0603 (R90)
  [ 5.588,12.446, 0.8, 1.6, 0.5],  // R1 10k 0603 (R270)
  [18.288, 5.461, 1.6, 0.8, 0.5],  // R2 10k 0603
];
module temp_module_parts() temp_place() for (p=temp_parts) translate([p[0]-p[2]/2, p[1]-p[3]/2, 0]) cube([p[2], p[3], p[4]]);
// U1 MLX90632SLD-DCB (medical grade) at (12.446, 10.033): the far-infrared sensor itself, 3 x 3 x 1 SFN
// the MLX90632's 50 deg field of view, from its window to the glass: shows what it measures (render aid, not a part)
temp_fov_half_angle = 25;
module temp_fov() temp_place() translate([12.446, 10.033, temp_mlx_h]) let(L = temp_mlx_gap + 0.4)
  cylinder(r1=0.6, r2=0.6 + L*tan(temp_fov_half_angle), h=L, $fn=48);
module temp_probe() temp_place() translate([12.446-1.5, 10.033-1.5, 0]) cube([3, 3, temp_mlx_h]);

// ---- optics -----------------------------------------------------------
R_out = vial_od/2;
led_tip_x = R_out + led_gap;
es_rb = R_out + pd_gap;            // eye-spy PCB back (vial-side) face radius
es_rf = es_rb + es_t;              // front (component) face: the photodiode sits here
// All optics modules are built with the IR LED on +X; optics_frame() turns them to optics_rotation.
module optics_frame() rotate(optics_rotation) children();
module led_body() optics_frame() translate([led_tip_x,0,optics_z]) rotate([0,-90,0]) {   // 5 mm IR LED, axis -X, dome tip at x=led_tip_x
  translate([0,0,-8.6]) difference() {
    union() {
      cylinder(d=5.8, h=1, $fn=48);                          // flange (with the cathode flat)
      cylinder(d=5, h=6.1, $fn=48);
      translate([0,0,6.1]) sphere(d=5, $fn=48);
    }
    translate([2.65,-3,-0.1]) cube([1,6,1.2]);
  }
}
module led_die() optics_frame() translate([led_tip_x+5.6,0,optics_z]) cube([0.5,0.5,0.5], center=true);
module led_legs() optics_frame() translate([led_tip_x,0,optics_z]) {
  for (s=[-1,1]) translate([0,s*1.27,0]) {                                  // leads out the back, then bent down (docs: "IR cable pointing downward")
    translate([4.0,-0.25,-0.25]) cube([4.0,0.5,0.5]);
    translate([7.5,-0.25,-10]) cube([0.5,0.5,10.25]);
  }
  translate([5.9,-1.27-0.6,-0.6]) cube([0.6,1.4,1.2]);                     // reflector cup / anvil
}
// one eye-spy, built in a frame whose +X is radially out from the vial axis at pocket i
module es_at(i) optics_frame() rotate(pd_rel[i]) translate([0,0,optics_z]) children();
module es_board2d() difference() {                                          // (u across, v up from the PD), mm
  translate([0,-es_pd_v]) difference() {
    hull() for (u=[-1,1], v=[0,1]) translate([u*(es_w/2-es_r), es_r+v*(es_h-2*es_r)]) circle(r=es_r, $fn=24);
    for (u=[-1,1], v=[2.54, es_h-2.54]) translate([u*3.96, v]) circle(d=2.7, $fn=20);
  }
  circle(d=2.3, $fn=24);                                                    // light window for the reverse-mount photodiode
}
module pd_board() for (i=[0:len(pd_rel)-1]) es_at(i) translate([es_rb,0,0]) rotate([90,0,90]) linear_extrude(es_t) es_board2d();
// Vishay VEMD2000X01 reverse-gullwing photodiode: package sizes from the STEP point cloud in
// Pioreactor/hardware CAD/eye-spy.step (body 2.5 x 2.49, top 2.97 above the PCB, lens d~1.92, leads to +-3.0)
module pd_body() for (i=[0:len(pd_rel)-1]) es_at(i) translate([es_rf,0,0]) {
  rotate([0,90,0]) cylinder(d=1.92, h=1.87, $fn=32);                        // lens, looking back through the PCB window
  translate([1.87,-1.25,-1.245]) cube([1.10,2.5,2.49]);                     // body
  for (s=[-1,1]) for (seg=[[[2.05,1.25],[2.05,1.67]],[[2.05,1.67],[1.97,1.97]],[[1.97,1.97],[0.15,2.40]],[[0.15,2.40],[0.15,3.0]]])
    hull() for (p=seg) translate([p[0], s*p[1], 0]) cube([0.15,0.15,0.5], center=true);   // gull-wing leads (width APPROX)
}
module pd_die() for (i=[0:len(pd_rel)-1]) es_at(i)
  translate([es_rf-0.06, -0.24, -0.24]) cube([0.08,0.48,0.48]);             // active area ~0.23 mm2; drawn at the lens face so it shows through the window
module beam() {
  optics_frame() hull() {                                                   // main IR beam straight across, to the far inner wall
    translate([led_tip_x,0,optics_z]) rotate([0,-90,0]) cylinder(r=beam_r0, h=0.01, $fn=48);
    translate([-(R_out-vial_wall)+0.05,0,optics_z]) rotate([0,-90,0]) cylinder(r=beam_r1, h=0.01, $fn=48);
  }
  for (i=[0:len(pd_rel)-1]) if (!pd_is_ref[i])                              // faint scatter rays: vial axis -> 45/90/135 photodiodes
    es_at(i) hull() { sphere(r=scat_r, $fn=12); translate([es_rf-0.1,0,0]) sphere(r=scat_r, $fn=12); }
  for (i=[0:len(pd_rel)-1]) if (pd_is_ref[i])                               // REF samples the LED directly, outside the culture (path INFERRED)
    hull() { optics_frame() translate([led_tip_x+1,0,optics_z]) sphere(r=scat_r, $fn=12);
             es_at(i) translate([es_rb-0.1,0,0]) sphere(r=scat_r, $fn=12); }
}

// =====================================================================
anode_x = anode_side*rod_offset;
want("cap",        c_cap)     render() holder();
want("septum",     c_septum)  gasket();
want("cathode",    c_steel)   electrode(-anode_x);
want("anode",      c_mmo)     electrode(anode_x, anode_inner_diameter, 0, anode_active_length);        // MMO-coated active length
want("anode_ti",   c_steel)   electrode(anode_x, anode_inner_diameter, anode_active_length, electrode_length-anode_active_length);   // bare Ti above it
want("needles",    c_steel)   for (n=needles) needle_path(n);
want("hubs",       c_hub)     for (n=needles) needle_hub(n);
want("screws",     c_steel)   screws_at() thumb_screw();
want("washers",    c_steel)   screws_at() washer();
want("flea",       c_flea)    flea();
want("thermal_pad",c_pad)     translate([0,0,base_z-thermal_pad_t]) cylinder(d=thermal_pad_d, h=thermal_pad_t, $fn=96);
want("pcb",        c_pcb)     pcb();
want("pcb_copper", c_copper)  pcb_copper();
want("pcb_parts",  c_parts)   pcb_parts();
want("temp_module",       c_temp_mask) temp_module();        // Precision Temperature kit: Adafruit MLX90632 board
want("temp_module_parts", c_parts)     temp_module_parts();
want("temp_fov",   [1,0.55,0.1,0.35]) temp_fov();
want("temp_probe",        c_pd)        temp_probe();         // the MLX90632 FIR sensor (non-contact)
want("led",        c_led)     led_body();
want("led_die",    c_die)     led_die();
want("led_legs",   c_steel)   led_legs();
want("pd_board",   c_pcb)     pd_board();
want("pd",         c_pd)      pd_body();
want("pd_die",     [0.18,0.16,0.45]) pd_die();
want("beam",       c_beam)    beam();
want("glass",      c_glass)   glass();     // last: transparent objects after the opaque ones
