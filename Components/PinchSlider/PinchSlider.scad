// Input parameters
TubingOD = 1/8; // tubing outer diameter
TubingID = 1/16; // tubing inner diameter
TubingUnits = "inches"; // units of input parameters: "inches" or "mm"

// Design parameters
SlotRatio = 3; // ratio of slot length to width
OpenTolerance = 0.2; // outer diameter print tolerance in mm
ClosedTolerance = 0.05; // closed slot print tolerance in mm
Margin = 2; // multiple of TubingOD to use as printed area around slot

// Calculated parameters
conversionFactor = (TubingUnits == "inches") ? 25.4 : (TubingUnits == "mm") ? 1 : undef;
TubingIDc = TubingID * conversionFactor; // Tubing inner diameter in mm
TubingODc = TubingOD * conversionFactor; // Tubing outer diameter in mm
TubingCompressed = TubingODc-TubingIDc; // compressed tubing wall thickness in mm
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
BridgeApexFraction = 0.6; // 0–1 along closed slot length from its far end toward the open slot: larger values give a bigger bump to retain tubing in closed position
BridgeBaseLength = OpenWidth; // base length of connecting triangle

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

// -----------------------------
// Model
// -----------------------------
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
