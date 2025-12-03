// Input parameters
TubingODimp = 1/8; // tubing outer diameter in inches
TubingIDimp = 1/16; // tubing inner diameter in inches

// Design parameters
SlotRatio = 3; // ratio of slot length to width
OpenTolerance = 0.2; // outer diameter print tolerance in mm
Margin = 2; // multiple of TubingOD to use as printed area around slot

// Calculated parameters
TubingID = TubingIDimp * 25.4; // Tubing inner diameter in mm
TubingOD = TubingODimp * 25.4; // Tubing outer diameter in mm
TubingCompressed = TubingOD-TubingID; // compressed tubing wall thickness in mm
OpenWidth = TubingOD + OpenTolerance; // open slot width in mm
ClosedWidth = TubingCompressed; // closed slot width in mm
OpenLength = OpenWidth; // open slot length in mm
ClosedLength = SlotRatio * ClosedWidth; // closed slot length in mm
ThinBodyLength = ClosedLength + Margin*TubingOD; // thin body width in mm
ThickBodyLength = OpenLength + Margin*TubingOD; // thick body length in mm
ThinBodyWidth = ClosedWidth + 2*Margin*TubingOD; // thin body width in mm
ThickBodyWidth = OpenWidth + 2*Margin*TubingOD; // thick body width in mm
Depth = Margin*TubingOD; // body depth in mm

$fn = 64;

// 2D capsule used for rounded bodies and slots
module capsule2d(length, width) {
  r = width/2;
  hull() {
    translate([r, 0]) circle(r = r);
    translate([length - r, 0]) circle(r = r);
  }
}

// -----------------------------
// Model
// -----------------------------
difference() {
  // Body
  linear_extrude(Depth) {
    union() {
      translate([-ThinBodyLength, 0])
        capsule2d(ThinBodyLength, ThinBodyWidth);
      capsule2d(ThickBodyLength, ThickBodyWidth);
    }
  }

  // Slot
  translate([-ClosedLength, 0, 0])
    linear_extrude(Depth)
      capsule2d(ClosedLength, ClosedWidth);

  // Open slot is now a circular cutout
  translate([OpenLength/2, 0, 0])
    cylinder(h = Depth, d = OpenWidth, center = false);
}
