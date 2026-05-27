// GL45BottleHolder – Pioreactor dovetail GL45 bottle holder
//
// The upstream Duran holders (e.g. Printables 1058356) have lettering
// cut into the four corners. Those recessed letter shapes trap residue
// and are awkward to clean. This SCAD fills them with smooth pillars
// while leaving the rest of the geometry untouched. The 0.25 L version
// renders to GL45_holder_250ml.stl – that's the file to print.
import("duran_holder_platform_center_0.25L.stl");

module cover()  {
    translate([7.75,13,0])
    rotate([0,0,45])
    scale([1.4,.6])cylinder(30, d=12);
}

cover();
translate([64.5,65,0]) cover();
translate([20.8,70.2,0]) rotate([0,0,90]) cover();
translate([85.4,5.8,0]) rotate([0,0,90]) cover();