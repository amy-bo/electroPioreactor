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

// -----------------------------
// Model
// -----------------------------
difference() {
  // Body
  union() {
    // Thin section
    translate([-ThinBodyLength, -ThinBodyWidth/2, 0])
      cube([ThinBodyLength, ThinBodyWidth, Depth]);

    // Thick section
    translate([0, -ThickBodyWidth/2, 0])
      cube([ThickBodyLength, ThickBodyWidth, Depth]);
  }

  // Slot
    // Thin section
    translate([-ClosedLength, -ClosedWidth/2, 0])
      cube([ClosedLength, ClosedWidth, Depth]);

    // Thick section
    translate([0, -OpenWidth/2, 0])
      cube([OpenLength, OpenWidth, Depth]);
}
