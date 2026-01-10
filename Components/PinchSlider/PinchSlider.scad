// Input parameters
TubingOD = 3; // tubing outer diameter
TubingPinched = 1.5; // tubing thickness when fully pinched
TubingUnits = "mm"; // units of input parameters: "inches" or "mm"

// Design parameters
SlotRatio = 3; // ratio of slot length to width
OpenTolerance = 0.6; // outer diameter print tolerance in mm
ClosedTolerance = 0.05; // closed slot print tolerance in mm
Margin = 2; // multiple of TubingOD to use as printed area around slot
BridgeApexFraction = 0.6; // 0–1 along closed slot length from its far end toward the open slot: larger values give a bigger bump to retain tubing in closed position
BungDepthMultiplier = 2.5; // bung is this many times deeper than body depth
TubeHoleTolerance = TubingOD/6 + OpenTolerance; // clearance for tubing through bung

// Calculated parameters
conversionFactor = (TubingUnits == "inches") ? 25.4 : (TubingUnits == "mm") ? 1 : undef;
TubingODc = TubingOD * conversionFactor; // Tubing outer diameter in mm
TubingCompressed = TubingPinched * conversionFactor; // compressed tubing wall thickness in mm
OpenWidth = TubingODc + OpenTolerance; // open slot width in mm
ClosedWidth = TubingCompressed + ClosedTolerance; // closed slot width in mm
OpenLength = OpenWidth; // open slot length in mm
ClosedLength = SlotRatio * ClosedWidth; // closed slot length in mm
MarginMM = Margin*TubingODc; // margin distance in mm
ThinBodyLength = ClosedLength + 2*MarginMM; // thin body length in mm (margin each end)
ThinBodyWidth = ClosedWidth + 2*MarginMM; // thin body width in mm (margin each side)
OpenBodyDiameter = OpenWidth + 2*MarginMM; // thick body diameter in mm
OpenBodyRadius = OpenBodyDiameter/2;
Depth = MarginMM; // body depth in mm
BridgeBaseLength = OpenWidth; // base length of connecting triangle
BungTolerance = OpenTolerance; // clearance on bung profile to allow insertion
CollarThickness = max(MarginMM/4, 1); // collar wall thickness around tubing
CollarHeight = Depth/2; // collar height
BungOffset = OpenLength/2 + OpenBodyRadius + MarginMM + max(BridgeBaseLength/2, OpenWidth/2); // place bung one margin away

$fn = 64;

// 2D capsule used for rounded bodies and slots
module capsule2d(length, width) {
  r = width/2;
  hull() {
    translate([r, 0]) circle(r = r);
    translate([length - r, 0]) circle(r = r);
  }
}

// Centered capsule helper
module capsule2d_centered(length, width) {
  translate([-length/2, 0]) capsule2d(length, width);
}

// Bung 2D profile (triangle + circle) with configurable clearance
module bung_profile_2d(tol = 0) {
  baseLen = max(BridgeBaseLength - tol, tol);
  circleD = max(OpenWidth - tol, tol);
  apexX = -ClosedLength + ClosedLength*BridgeApexFraction;
  union() {
    translate([OpenLength/2, 0]) circle(d = circleD);
    polygon(points = [
      [apexX, 0],
      [OpenLength/2, -baseLen/2],
      [OpenLength/2,  baseLen/2]
    ]);
  }
}

// Bung solid with retaining collar
module bung() {
  holeD = TubingODc + TubeHoleTolerance;
  holeR = holeD/2;
  collarOuterR = holeR + CollarThickness;
  bungDepth = BungDepthMultiplier * Depth;
  collarX = -ClosedLength/2; // centered on midpoint of closed slot

  difference() {
    union() {
      linear_extrude(bungDepth)
        bung_profile_2d(BungTolerance);

      translate([collarX, 0, 0])
          cylinder(h = CollarHeight, r = collarOuterR, center = false);
    }

    // Through-hole for tubing
    translate([collarX, 0, -1])
      cylinder(h = bungDepth + CollarHeight + 2, r = holeR, center = false);
  }
}

// -----------------------------
// Model
// -----------------------------
module pinch_slider_body() {
  difference() {
    // Body
    linear_extrude(Depth) {
      union() {
        translate([-ClosedLength/2, 0])
          capsule2d_centered(ThinBodyLength, ThinBodyWidth);
        translate([OpenLength/2, 0])
          circle(r = OpenBodyRadius);
      }
    }

    // Slot
    translate([-ClosedLength/2, 0, 0])
      linear_extrude(Depth)
        capsule2d_centered(ClosedLength, ClosedWidth);

    // Triangular cutout joining far closed end to open center
    linear_extrude(Depth)
      polygon(points = [
        [-ClosedLength + ClosedLength*BridgeApexFraction, 0], // apex along closed slot
        [OpenLength/2, -BridgeBaseLength/2],
        [OpenLength/2,  BridgeBaseLength/2]
      ]);

    // Open slot is now a circular cutout
    translate([OpenLength/2, 0, 0])
      cylinder(h = Depth, d = OpenWidth, center = false);
  }
}

// Assemble body and bung with spacing
pinch_slider_body();
translate([BungOffset, 0, 0]) bung();
