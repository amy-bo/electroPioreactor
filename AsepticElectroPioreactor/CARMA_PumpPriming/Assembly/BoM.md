# Aseptic electroPioreactor AEP0.2 — Bill of Materials

Quantities are per one complete AEP0.2 unit. See [assembly instructions](README.md).

Items marked **Critical** must meet the specification. Items marked **Generic** are satisfied by anything meeting it.

## 1. Pioreactor platform

| Ref | Item | Qty | Specification |
| --- | --- | --- | --- |
| 1.1 | Pioreactor 40 ml v1.5 | 1 | **Critical.** Pioreactor 40 ml, hardware v1.5, regional mains variant. Ships with vial, stir bar and caps. The whole add-on is built around the 40 ml vial and the Pioreactor HAT. |
| 1.2 | XR upgrade kit | 1 | **Critical** unless the unit was ordered as an XR. Adds 45° and 135° scattering alongside 90°, for the lower OD detection limit. |
| 1.3 | Precision Temperature Upgrade Kit | 1 | **Optional.** MLX90632 far-infrared sensor replacing the thermistor, seating in the SPEC position. Only needed if the protocol calls for controlled temperature. |
| 1.4 | Raspberry Pi 5 | 1 | **Generic.** 1 GB or larger; any Pi supported by the current Pioreactor OS. One per Pioreactor. |
| 1.5 | 27 W USB-C power supply | 1 | **Generic.** 5.1 V / 5 A USB-C PD, regional plug. Actual draw is about 15.3 W per Pioreactor. For four or more units, one multi-port GaN charger giving at least 15.3 W per port. |
| 1.6 | microSD card | 1 | **Generic.** 32 GB or larger, A2 / U3 / V30 class, flashed with Pioreactor OS 26.5.0 or later. |
| 1.7 | 12 V peristaltic pumps | 1 pair | **Critical.** Must be the Pioreactor pump, so the HAT can drive it. Supplied as a pair with pump tubing. |
| 1.8 | Pumping dovetail platform | 1 | **Generic** on print settings, **critical** on geometry. 3D printed PLA or PETG, 0.2 mm layer, ~20% infill, with the SD-card cutout. |
| 1.9 | Dovetail holders for GL45 bottles | 2 | **Generic** on print settings, **critical** on bottle OD. 3D printed PLA or PETG, sized for a 250 ml GL45 bottle at about 70 mm OD. |
| 1.10 | GL45 caps | 2 | **Critical.** Polypropylene multi-port screw cap, ports sized for 1/8" OD tubing, autoclavable. Port count and bore must match the tubing runs. |
| 1.11 | Spare vial | 1 per n units | **Generic.** Pioreactor 40 ml glass vial. Shared spare, not consumed per build. |
| 1.12 | Spare magnetic flea | 1 per n units | **Generic.** PTFE-coated stir bar as supplied with the Pioreactor, octagonal, about 10 mm. |

## 2. Electrochemical cell

| Ref | Item | Qty | Specification |
| --- | --- | --- | --- |
| 2.1 | MMO anode, 100 mm length x 6 mm OD, 4mm ID | 1 | **Critical.** Titanium substrate with a mixed-metal-oxide (DSA) coating of iridium and tantalum oxide (IrO₂-Ta₂O₅), the valve-metal-stabilised OER coating, not the RuO₂ type. Hollow tube, open at the base: CO₂ enters the top and leaves through the base, so the part is both anode and CO₂ conduit. |
| 2.2 | Stainless steel cathode, 100 mm length x 6 mm diameter | 1 | **Critical.** 316 stainless round bar, marine grade. Must stay strictly cathodic: reversed, stainless corrodes quickly and leaches Cr, Ni and Fe into the culture. |
| 2.3 | Vial cap and electrode holder | 1 | **Critical and custom.** One-piece PCCF (poly carbonate blend filled with carbon fibers) 3D-printed cap and electrode top-stop sealing on a full-width silicone septum, with no cap or electrode o-rings. GPI 24-400 internal thread, Pioreactor-1.5 poka-yoke flange. Parametric OpenSCAD source at [Components/Vial Cap](../../../Components/Vial%20Cap); electrode length and desired protrusion set the column height, so insertion depth is built in. |
| 2.4 | Silicone septum, 2mm thick | 1 | **Critical and custom.** Full-width sheet sized to the cap's `seal = "septum"` mode: it seals the vial mouth, each electrode and every port, and self-heals sampling-needle tracks. Not a stock size. |
| 2.5 | 0.2 µm hydrophobic vent filters | 5 | **Critical.** 25 mm syringe filter, 0.2 µm PTFE membrane, female Luer-Lok inlet and male Luer-slip outlet. Pore size and membrane are the aseptic barrier. |
| 2.6 | Stainless steel needle port | 1 | **Generic.** 75 mm blunt stainless needle with a female luer-lock hub. 304 is standard; 316 is available for more acidic, basic or salty media. Each Pioreactor already ships with four. |

## 3. Electrical, wiring and fixings

| Ref | Item | Qty | Specification |
| --- | --- | --- | --- |
| 3.1 | Solenoid valve | 1 | **Critical.** 1/8" ports, 12 V DC coil, **3-way venting (3/2)**, with manual override. A 2-way valve traps CO₂ between the valve and the broth on closing; it dissolves and draws liquid back up the line. |
| 3.2 | Wiring, solenoid | 1 | **Generic.** Two-core cable rated for a 12 V DC coil, crimped for the connector at 3.8. |
| 3.3 | Wiring, electrode cables | 1 | **Generic** cable, **critical** terminations. One run per electrode, ring terminal at the electrode end and connector at the Pioreactor end. Colour-code red anode, black cathode, and never swap. |
| 3.4 | Ring terminals | 2 | **Generic.** M3 stud, sized to the electrode cable gauge. |
| 3.5 | Thumb screws | 2 | **Generic.** M3, clamping the ring terminal to the electrode stud. Avoid a galvanic mismatch with the stainless cathode. |
| 3.6 | M3 nuts | 2 | **Generic.** A2 or A4 stainless to match the cathode. |
| 3.7 | M3 spring washers | 2 | **Generic.** Stainless, under the nut, to hold the fixing through vibration and thermal cycling. |
| 3.8 | Crimp connector | 1 | **Critical.** Must carry the solenoid coil and electrode currents and match the housing at 3.9 and the Pioreactor header. A mismatch blocks assembly. |
| 3.9 | Crimp housing | 1 | **Critical.** Matching series and pin count to 3.8, pinned out to the Pioreactor board. |

## 4. CO₂ supply

| Ref | Item | Qty | Specification |
| --- | --- | --- | --- |
| 4.1 | Dovetail holder, CO₂ cylinder | 1 | **Generic** on print settings. 3D printed, sized for a SodaStream-diameter cylinder on the standard dovetail rail. |
| 4.2 | CO₂ regulator | 1 | **Critical** on the outlet. 3/8" John Guest push-fit outlet with a built-in pressure relief valve, able to carry a mounted solenoid and needle-valve train. The inlet is a generic cylinder thread, not SodaStream-native, and pairs with the adapter at 4.3. |
| 4.3 | Cylinder-to-regulator adapter | 1 | **Critical and regional.** Pin-adjustment type, so the joint is made before gas is admitted. UK and EU: W21.8 male × TR21-4 female with a thumbscrew pin. Elsewhere, the equivalent for the local cylinder standard, for example CGA320 in North America. |
| 4.4 | 12 V power supply | 1 | **Generic.** 12 V DC, at least 1 A, 2.1 mm × 5.5 mm centre-positive barrel plug. Powers the solenoid, not the Pioreactor. |
| 4.5 | 1/4" to 1/8" reducing hexagon nipple | 1 | **Critical.** Male to male, matching the regulator outlet on one end and the 1/8" train on the other. |
| 4.6 | 1/8" blanking plug | 1 | **Generic.** External 1/8" thread, nickel-plated brass, sealing on an integral NBR o-ring, so no thread sealant is needed. |
| 4.7 | SodaStream CO₂ cylinder (blue screw-in) | consumable | **Regional consumable, not supplied by LabCrafter.** Standard screw-in SodaStream-compatible cylinder, TR21-4 thread. Buy locally. Example: <https://sodastream.co.uk/products/refill> |
| 4.8 | Loctite 577 thread sealant | shared | **Critical** for gas-tight threaded joints with no o-ring seat. One-part anaerobic, medium strength, thixotropic. Fixture on steel in 10 to 60 minutes at 22 °C, full pressure rating after 24 hours. Gap-fills to 0.25 mm, works on stainless without activation, rated to 100% hydrogen (KIWA GASTEC QA AR 214). One tube covers many builds. |

## 5. Gas and fluid lines

| Ref | Item | Qty | Specification |
| --- | --- | --- | --- |
| 5.1 | CO₂ needle valve | 1 | **Critical.** 1/8" BSPP/NPS male, screwing directly onto the regulator or solenoid outlet. Accepts 4 mm or 6 mm hose. Rated to 4 bar, against a working pressure of about 1 bar. |
| 5.2 | Polyurethane CO₂ tube, 1 m | 1 | **Generic.** 6 mm OD × 4 mm ID, rated to 10 bar. |
| 5.3 | 1/16" barb to male luer lock | 2 | **Generic.** Barb size and luer gender are the critical match. |
| 5.4 | 1/16" barb to female luer lock | 2 | **Generic.** As above. |
| 5.5 | 1/8" barb to male luer lock | 2 | **Critical** on barb bore: it must grip the 4 mm PU tube OD, or the joint leaks under pressure. Connects the CO₂ line to the syringe filter. |
| 5.6 | Silicone tubing, 50 cm | 1 | **Generic.** 1/8" OD × 1/16" ID, autoclavable. Compatible with 10% acetic acid, CaCl₂, H₂O₂, K₂SO₄, NaCl, 5.5% NaOCl and ZnCl₂. |
| 5.7 | Luer lock cap | 1 | **Generic.** Caps an unused luer port. |
| 5.8 | Male-to-male luer lock adapter | 2 | **Generic.** Joins the CO₂ filter outlet to the anode feed tube. |
| 5.9 | Silicone feed tube, tubular anode | 1 | **Critical** on fit. About 1 mm ID / 3 mm OD, carrying CO₂ from the luer adapter into the top of the anode. |
| 5.10 | 250 ml GL45 borosilicate bottle | 2 | **Regional consumable, not supplied by LabCrafter.** GL45 thread, about 70 mm OD, to match 1.9 and 1.10. Example: <https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate> |

## Still to specify

### For Gerrit — blocking

These stop a third party sourcing or building the unit. @gniezen

- [ ] **2.1 MMO anode.** MMO specification IrO₂-Ta₂O₅ percentage. Coated (active) length against the 100 mm overall length and thickness.
- [ ] **2.3 Vial cap and electrode holder.** Print settings, and the standard electrode insertion depth once a unit is built.
- [ ] **2.4 Silicone septum.** Diameter, silicone grade, Shore hardness, temperature rating and autoclavability.
- [ ] **3.8 / 3.9 Connector and housing.** Manufacturer part numbers, series, pin count, pitch and gender, plus the crimp contact part number and the tool needed.
- [ ] **4.5 Reducing nipple.** Thread standard at both ends, BSPP or BSPT, and material.
- [ ] **5.9 Anode feed tube.** Exact length and confirmation that 1 mm ID / 3 mm OD suits the final anode.
- [ ] **Printed parts.** Publish STL or STEP for 1.8, 1.9, 4.1 and 2.3 so the build is reproducible.

### Secondary

- [ ] 1.10 Number of ports required per GL45 bottle.
- [ ] 2.5 Filter replacement interval.
- [ ] 2.6 Whether 304 or the 316 upgrade is needed for the AEP medium.
- [ ] 3.1 Orifice size, maximum working pressure, coil power and duty-cycle rating.
- [ ] 3.2 / 3.3 Conductor size, insulation rating and finished lengths.
- [ ] 4.2 Working and output pressure range, and the inlet thread standard.
- [ ] 4.6 Thread standard variant, BSPP or NPT, against the solenoid port.
- [ ] 5.3 to 5.5 Body material, and confirmation the luer standard is lock rather than slip.
- [ ] 5.6 Wall thickness and Shore hardness; peristaltic-pump rating if ever used in a pump head.
- [ ] 5.7 Male or female, material, and whether it must be sterilisable.
- [ ] **Operating parameters.** Applied voltage or current, electrode spacing and submerged area, medium, and duty cycle. Several ratings above depend on these.
- [ ] **Sterilisation procedure**, pending PI approval.
