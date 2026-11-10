---
title: AEP0.2 specification
description: Every documented dimension, material, channel and rating of the Aseptic electroPioreactor AEP0.2, part by part, with links to the source files and the assembly guide.
section: build
audience: expert
order: 10
---

The Aseptic electroPioreactor (AEP) 0.2 is a Pioreactor 40 ml bioreactor with two electrodes and a carbon dioxide (CO₂) supply added. Electrolysis in the culture makes hydrogen and oxygen for hydrogen-oxidising bacteria (HOB), and timed CO₂ pulses supply their carbon. This page lists what each part is, in tables; the [assembly guide](https://docs.electropioreactor.org/AEP/) says how to build it, and [How it works](/how-it-works/) explains the idea in plain words.

Every value comes from a component file in [`docs/components/`](repo:docs/components/), a guide step in [`docs/steps/`](repo:docs/steps/), or the Vial Cap model in [`Components/Vial Cap/`](repo:Components/Vial%20Cap/). The bill of materials (BoM) itself now lives as those component files; [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) keeps only the items still to specify. Where a value is still open, the table says so.

> **Note:** Abbreviations used below: OD, optical density; IR, infrared; MMO, mixed metal oxide; PC-CF, carbon-fibre-filled polycarbonate; PWM, pulse-width modulation (a switched output of the Pioreactor HAT, the board on the Raspberry Pi); PTFE, polytetrafluoroethylene; PU, polyurethane; BSP, British Standard Pipe thread; ID/OD, inner/outer diameter.

## At a glance

| Item | AEP0.2 |
| --- | --- |
| Base unit | [Pioreactor 40 ml v1.5](repo:docs/components/pioreactor-40ml.yaml), fitted with the [XR upgrade kit](repo:docs/components/xr-upgrade-kit.yaml) from the start |
| Vessel | 40 ml borosilicate glass vial, ~30 ml working volume |
| Computer | [Raspberry Pi 5](repo:docs/components/raspberry-pi.yaml), 1 GB RAM or more |
| Software | Pioreactor OS 26.5.0 or later, with the [electroPioreactor plugin](/software/) |
| Electrodes | MMO-coated titanium tube anode and 316 stainless steel rod cathode, both 6 mm OD × 100 mm |
| Electrolysis drive | Pioreactor LED channel D, clamped to 10 % by the plugin |
| Gas supply | SodaStream CO₂ cylinder, regulator, 3/2 venting solenoid on PWM 4, needle valve |
| Seal | One-piece 3D-printed Vial Cap with a single 2 mm silicone septum |
| Aseptic barrier | 0.2 µm PTFE hydrophobic vent filters on every gas path |
| Sterilisation | Procedure awaiting approval (see [Sterilisation](#sterilisation-and-aseptic-barrier)) |

## Vessel and base unit

| Parameter | Value | Source |
| --- | --- | --- |
| Pioreactor | 40 ml, hardware v1.5, regional mains variant | [pioreactor-40ml](repo:docs/components/pioreactor-40ml.yaml) |
| Model set in the Pioreactor Inventory | 40 ml, XR variant | [Step 5](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) |
| Vial | 40 ml borosilicate glass, GPI 24-400 neck | [pioreactor-vial-40ml](repo:docs/components/pioreactor-vial-40ml.yaml), [`Vial Cap.scad`](repo:Components/Vial%20Cap/Vial%20Cap.scad) |
| Working volume | 30 ml, set by the Media Out needle depth and checked by weighing | [Step 11](https://docs.electropioreactor.org/AEP/step-11-ports/) |
| Vial neck, internal diameter | 17 mm (measured; the Vial Cap keeps 0.6 mm clearance to the glass) | `neck_inner_diameter`, `neck_clearance` in [`Vial Cap.scad`](repo:Components/Vial%20Cap/Vial%20Cap.scad) |
| Stir bar | 15 × 6 mm PTFE-coated, from the Pioreactor box (spare: Pioreactor SKU 2046); stirrer on PWM 1. The 20 ml Pioreactor (MEP) uses a 3 × 12 mm bar (SKU 2003) | [stir-bar](repo:docs/components/stir-bar.yaml), [stir-bar-20ml](repo:docs/components/stir-bar-20ml.yaml), [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Not used from the Pioreactor box | The stock Vial Cap S and its stainless steel ports (replaced by the AEP Vial Cap) | [stock-vial-cap](repo:docs/components/stock-vial-cap.yaml) |

<!-- source: docs/components/stir-bar.yaml (v1.1.0, 15 × 6 mm, SKU 2046) and stir-bar-20ml.yaml (3 × 12 mm, SKU 2003; early 20 ml units shipped a bar of about 10 mm, so measure the one in hand) -->

## Vial Cap and electrode holder

A one-piece cap, printed in PC-CF, that screws onto the vial, holds both electrodes at a fixed depth and carries every port. It replaces the AEP0.1 cap, its O-rings and the separate ElectrodeTopStop. Source: [`Components/Vial Cap/`](repo:Components/Vial%20Cap/) (OpenSCAD, needs the BOSL2 library); component file [vial-cap](repo:docs/components/vial-cap.yaml), design version 2.0.1.

| Parameter | Value | Source |
| --- | --- | --- |
| Material and print settings | PC-CF, 100 % infill, default PC-CF profile, 0.16 mm layer height; prints without supports | [vial-cap](repo:docs/components/vial-cap.yaml), [README](repo:Components/Vial%20Cap/README.md) |
| Thread | GPI 24-400, internal (BOSL2) | [`Vial Cap.scad`](repo:Components/Vial%20Cap/Vial%20Cap.scad) |
| Cap body | 27 mm OD, 12.3 mm high, 2 mm wall | `cap_outer_diameter`, `cap_height`, `wall_thickness` |
| Locating flange | Pioreactor 1.5 poka-yoke flange (fits one way only), 93° arc, 3.5 mm radial push | `flange_arc`, `flange_push` |
| Electrode bores | 2 × 6.2 mm modelled bore for the 6 mm electrodes: +0.15 mm friction fit in the cap, +0.3 mm more in the column | `rod_diameter`, `cap_rod_clearance`, `insert_clearance` |
| Electrode spacing | 4.8 mm from the cap axis to each bore, so 9.6 mm centre to centre (3.6 mm between the 6 mm electrode surfaces), confirmed from the printed cap's STL and used by the gas model | `rod_offset`; [`AEP2.0/Vessel Cap.stl`](repo:Components/Vial%20Cap/AEP2.0/Vessel%20Cap.stl) <!-- source: Media/CHANGELOG.md 2026-11-06 --> |
| Electrode clamp | M3 thumb screw into a captive M3 nut, through a 3.4 mm clearance hole, clamping a ring terminal against the electrode | `m3bolt_clearance`, `nut_across_flats`; [Step 7](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) |
| Needle ports | 5 × 2.2 mm, each with a 3 mm needle guide | `num_ports`, `port_diameter`, `guides` |
| Large septum opening | 1, at the front, for inoculation by syringe | `openings` |
| Ports in total | 8: anode and CO₂ in, cathode, Media In, Media Out, Gas Out, Gas Out – safety, inoculation, spare | [Step 11](https://docs.electropioreactor.org/AEP/step-11-ports/) |
| Electrode depth | Set by the column height: electrode tops sit flush with the top of the cap | [Step 7](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) |
| Standard insertion depth | Not yet fixed: to be measured on the first build (BoM open item 2.3) | [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) |
| Legacy mode | `seal = "oring"`, `pieces = 2` still reproduces the AEP0.1 O-ring cap | [README](repo:Components/Vial%20Cap/README.md) |

> **Expert:** The column height is `rod_length − insertion_depth − cap_height`. The file defaults (`rod_length` 60 mm, `insertion_depth` 23 mm) predate the 100 mm AEP0.2 electrodes, and the component file deliberately leaves them at the defaults until the first measured build. A cap printed from the published defaults gives a 37 mm high stack, so a flush 100 mm electrode would reach about 63 mm below the cap. <!-- CHECK: arithmetic from Vial Cap.scad defaults; confirm against the cap actually shipped -->

### Septum

| Parameter | Value | Source |
| --- | --- | --- |
| Material | Silicone sheet, 2 mm thick, 60 Shore A | [silicone-septum](repo:docs/components/silicone-septum.yaml) |
| Process | Laser cut, full width of the cap | [silicone-septum](repo:docs/components/silicone-septum.yaml) |
| Modelled size | 23.9 mm diameter, in a 24.2 mm seat, held by a 22.5 mm inward lip | `gasket_diameter`, `gasket_seat_diameter`, `ridge_inner_diameter` |
| Function | One sheet seals the vial mouth, both electrodes and every port, and self-heals needle tracks. No cap or electrode O-rings in AEP0.2 | [Step 7](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) |
| Cut outline | Not yet published (BoM open item 2.4) | [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) |

### Needles

| Port | Needle | Tip position |
| --- | --- | --- |
| Media Out | [80 mm, 316 stainless, 16 G, blunt, female luer lock](repo:docs/components/needle-80mm-316.yaml) | At the liquid surface: its depth sets the 30 ml level |
| Media In | [75 mm, 304 stainless, 16 G, blunt, female luer lock](repo:docs/components/needle-75mm-304.yaml) (from the Pioreactor box) | Above the liquid |
| Gas Out, Gas Out – safety | 2 × the same 75 mm 304 needles, bent, each with a male-to-male luer adapter and a vent filter | Above the liquid |
| Inoculation | No needle fitted: a syringe goes through the septum. 21 to 23 G balances septum life against transfer speed | – |
| Spare | Left unpierced | – |
| Spare needle | The Pioreactor box's 85 mm 316 stainless 15 G needle, kept to replace Media In if the 304 needle corrodes | – |

<!-- source: docs/steps/step-11-ports.md; docs/components/needle-*.yaml (16 G; the Vial Cap render now matches) -->

## Electrodes

| Parameter | Anode | Cathode |
| --- | --- | --- |
| Part | [MMO anode](repo:docs/components/mmo-anode.yaml) | [Stainless steel cathode](repo:docs/components/stainless-steel-cathode.yaml) |
| Form | Hollow tube, open at the base | Round bar |
| Material | Grade 1 titanium with an IrO₂–Ta₂O₅ mixed-metal-oxide coating, 8 µm thick | 316 (marine grade) stainless steel |
| Dimensions | 100 mm long, 6 mm OD, 4 mm ID | 100 mm long, 6 mm diameter |
| Active length | 70 mm coated, at the bottom; the top is bare titanium | Whole immersed length |
| Reaction | Oxygen evolution | Hydrogen evolution |
| Second job | CO₂ conduit: gas fed down its bore leaves through the open base | – |
| Lead | Red, 30 cm, ring terminal | Black, 30 cm, ring terminal |

> **Safety:** Never swap the leads. Reversed, the stainless steel becomes the anode, corrodes quickly and leaches chromium, nickel and iron into the culture. <!-- source: docs/steps/step-07-set-up-electrolysis.md -->

| Fixing and wiring | Value | Source |
| --- | --- | --- |
| Terminal stack | Flat washer against the cap, spring washer, ring terminal, M3 thumb screw head | [Step 7](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) |
| Thumb screws | M3, knurled | [thumb-screw](repo:docs/components/thumb-screw.yaml) |
| Pioreactor end | Crimp contacts in one crimp housing: clip away from you, black left, red right | [Step 7](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) |
| Electrode cables | 2 runs, 30 cm each | [electrode-cable](repo:docs/components/electrode-cable.yaml) |

## Electrolysis drive

| Parameter | Value | Source |
| --- | --- | --- |
| Output | Pioreactor HAT LED channel D, catch upwards (the plugin's `led_channel` can move it to A, B or C) | [Step 8](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/), [plugin](/software/) |
| Control | `electrolysis_power`, 0 to 10 % of the channel's full output; values above 10 % are clamped | [`electropioreactor.py`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/pioreactor_electropioreactor_plugin/electropioreactor.py) |
| Default setting | 2.5 % | [`additional_config.ini`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/pioreactor_electropioreactor_plugin/additional_config.ini) |
| First-test setting | About 3.5 %, raised until bubbles form | [Step 8](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/) |
| Cell voltage at 3.5 % | About 2.8 to 3.05 V across the electrodes (2.82 V recorded on the first AEP0.2 build) | [Step 8](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/) |
| Current | Not measured on AEP0.2 yet. The gas model's default fit is I ≈ 1.03 mA per % + 2.6 mA, valid 3 to 10 %: about 6.2 mA at 3.5 % and 12.9 mA at the 10 % clamp | [Gas model](/gas-model/), [`gerrit-current.md`](repo:Media/protocols/gerrit-current.md) |
| Expected bubbling | About twice as many bubbles on the cathode as on the anode (H₂ : O₂ = 2 : 1) | [Step 8](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/) |
| Operating envelope | Applied voltage or current, submerged area and duty cycle: still to specify (BoM open item) | [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) |

> **Safety:** Drive the electrodes only from the electroPioreactor job, never by setting LED channel D by hand: only the job applies the 10 % clamp. <!-- source: docs/steps/step-08-test-electrolysis.md -->

## CO₂ gas train

From the cylinder to the vial, in order. Built in [Step 12](https://docs.electropioreactor.org/AEP/step-12-co2-gas-train/), opened in [Step 13](https://docs.electropioreactor.org/AEP/step-13-admit-co2/).

| # | Part | Specification |
| --- | --- | --- |
| 1 | [SodaStream CO₂ cylinder](repo:docs/components/sodastream-co2-cylinder.yaml) | Blue screw-in type, TR21-4 thread; about 60 bar on the gauge when full. Bought locally |
| 2 | [Cylinder-to-regulator adapter](repo:docs/components/cylinder-regulator-adapter.yaml) | KegLand KL15578, pin-adjustment type, W21.8 male (UK and EU) to TR21-4 female. Elsewhere, the local equivalent (for example CGA320 in North America) |
| 3 | [CO₂ regulator](repo:docs/components/co2-regulator.yaml) | With pressure-relief valve; set to about 1 bar outlet. Its 3/8" John Guest push-fit outlet is removed |
| 4 | [Regulator outlet O-ring](repo:docs/components/regulator-outlet-o-ring.yaml) | 8 mm ID, 2 mm cross-section; seats against the reducer, so no sealant on this joint |
| 5 | [Reducing hexagon nipple](repo:docs/components/reducing-nipple.yaml) | 1/4" BSP male to 1/8" BSP male, stainless steel |
| 6 | [Solenoid valve](repo:docs/components/solenoid-valve.yaml) | 3-way venting (3/2), 12 V DC coil, 1/8" ports, manual override (0 = normal, closed unpowered; 1 = always open) |
| 7 | [Blanking plug](repo:docs/components/blanking-plug.yaml) | 1/8" male, nickel-plated brass, integral NBR O-ring; no sealant |
| 8 | [Needle valve](repo:docs/components/co2-needle-valve.yaml) | 1/8" BSPP/NPS male thread, 4 or 6 mm hose, rated 4 bar, worked at 1 bar |
| 9 | [PU CO₂ tube](repo:docs/components/polyurethane-co2-tube.yaml) | 6 mm OD × 4 mm ID, 1 m, rated 10 bar; cut to the same length on every unit |
| 10 | [1/8" barb to male luer lock](repo:docs/components/barb-1-8-to-male-luer-lock.yaml) | Must grip the 4 mm tube bore, or the joint leaks under pressure |
| 11 | [Vent filter](repo:docs/components/hydrophobic-vent-filter.yaml) | 0.2 µm PTFE, 25 mm, female Luer-Lok in, male Luer-slip out |
| 12 | [Anode feed tube](repo:docs/components/anode-feed-tube.yaml) | Silicone, 1 mm ID × 3 mm OD, 100 mm, threaded through the anode and trimmed at its base; female luer at the top is the CO₂ inlet |

| Parameter | Value | Source |
| --- | --- | --- |
| Solenoid drive | PWM channel 4, labelled `relay` in `config.ini`; opened at 100 % duty, 16 Hz PWM | [plugin source](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/pioreactor_electropioreactor_plugin/electropioreactor.py) |
| Solenoid wiring | Two-core, 12 V DC rated, 60 cm; red (positive) on the left terminal | [solenoid-wiring](repo:docs/components/solenoid-wiring.yaml) |
| Sealing | O-rings where a joint has a seat; Loctite 577 anaerobic thread sealant on the second thread elsewhere; no PTFE tape | [Step 12](https://docs.electropioreactor.org/AEP/step-12-co2-gas-train/) |
| Loctite 577 cure | Fixtures in 10 to 60 minutes at 22 °C; full pressure rating after 24 hours | [Step 12](https://docs.electropioreactor.org/AEP/step-12-co2-gas-train/) |
| Plugin default schedule | 10 s open every 60 min; set your own in the job's Settings | [`additional_config.ini`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/pioreactor_electropioreactor_plugin/additional_config.ini) |
| Flow calibration | Timed displacement into a water-filled measuring cylinder at 1 bar, adjusted with the needle valve | [Steps 15](https://docs.electropioreactor.org/AEP/step-15-set-up-co2-flow-test/) and [16](https://docs.electropioreactor.org/AEP/step-16-calibrate-co2-flow/) |
| Open items | Solenoid orifice, maximum pressure, coil power and duty rating; regulator pressure range and inlet thread; BSPP or NPT against the solenoid port | [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) |

> **Safety:** The solenoid must be a 3-way venting type. A 2-way valve traps CO₂ between the valve and the broth when it closes; the CO₂ dissolves and draws liquid back up the line. Why: [`VentingSolenoids.md`](repo:Components/CO2%20transfer/VentingSolenoids.md). Wear cryogenic gloves (safe to at least −80 °C) and eye protection when making the cylinder joint.

## Media pumps and tubing

| Parameter | Value | Source |
| --- | --- | --- |
| Pumps | [12 V peristaltic pumps](repo:docs/components/peristaltic-pump.yaml), a pair per Pioreactor, the Pioreactor model so the HAT can drive them | [Step 9](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/) |
| Channels (AEP) | Media pump PWM 2 (`media`), product pump PWM 3 (`waste`) | [Step 9](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/) |
| Bottles | 2 × [250 ml GL45 borosilicate](repo:docs/components/gl45-bottle.yaml) (about 70 mm OD), one media, one product; bought locally | [gl45-bottle](repo:docs/components/gl45-bottle.yaml) |
| Bottle caps | 2 × [GL45 polypropylene caps](repo:docs/components/gl45-cap.yaml) with luer ports for 1/8" OD tubing, autoclavable; a vent filter on each vent port | [gl45-cap](repo:docs/components/gl45-cap.yaml) |
| Tubing | [1/8" OD × 1/16" ID](repo:docs/components/silicone-tubing.yaml), 50 cm per unit, autoclavable | [silicone-tubing](repo:docs/components/silicone-tubing.yaml) |
| Fittings | 2 × [1/16" barb to male luer lock](repo:docs/components/barb-1-16-to-male-luer-lock.yaml), 2 × [1/16" barb to female luer lock](repo:docs/components/barb-1-16-to-female-luer-lock.yaml) | [Step 9](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/) |
| In-line parts on the media lines | Non-return valves (not filters) | [Step 9](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/) |
| Calibration | Pioreactor pump calibration on the 12 V supply, with a balance of 0.1 g resolution | [Step 10](https://docs.electropioreactor.org/AEP/step-10-calibrate-pumps/) |
| Dosing mode | Turbidostat | [Step 11](https://docs.electropioreactor.org/AEP/step-11-ports/) |

## Heating and temperature

| Parameter | Value | Source |
| --- | --- | --- |
| Heater | Pioreactor heater PCB under the vial: an aluminium-core board heated by surface-mount resistors, with a thermal pad against the glass; PWM 5 | [`Vial Cap render.scad`](repo:Components/Vial%20Cap/Vial%20Cap%20render.scad) comments; [Step 14](https://docs.electropioreactor.org/AEP/step-14-configure-sparging-and-electrolysis/) |
| Heater board design | The same board as the Pioreactor 20 ml heater (Pioreactor's published `heater_20ml` design) sits under the 40 ml v1.5 vial | [`Vial Cap render.scad`](repo:Components/Vial%20Cap/Vial%20Cap%20render.scad) comments <!-- CHECK: inferred in the render file from Pioreactor's docs photos and published hardware, not confirmed by Pioreactor --> |
| Run temperature | 30 °C for the AEP media | [`Media/README.md`](repo:Media/README.md) |
| Precision temperature kit (optional, included in AEP0.2 kits) | [MLX90632 far-infrared sensor](repo:docs/components/precision-temperature-upgrade-kit.yaml) on a STEMMA QT board in the holder's SPEC position, LED pad to the right, wired to the nearest eye-spy; non-contact, it reads the culture through the glass and replaces the thermistor | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Its software | `pioreactor-precision-temperature-plugin`, installed from the AEP card bundle | [Step 5](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) |

## Optics (XR)

| Parameter | Value | Source |
| --- | --- | --- |
| Kit | Pioreactor [XR upgrade kit](repo:docs/components/xr-upgrade-kit.yaml), fitted instead of the v1.5 optics | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Light source | One IR LED under an LED cap | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Detectors | Four eye-spy photodiode boards: 45° (the board labelled 0x4B), REF (white-marked), 90° (unmarked), 135° | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Reused from the v1.5 kit | 2 eye-spys, 3 optics covers, 12 × 8 mm screws, 1 LED cap, 50 mm STEMMA-QT wire | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| XR kit supplies | The other eye-spys, the XR top vial holder and its X-section O-ring | [xr-upgrade-kit](repo:docs/components/xr-upgrade-kit.yaml) |
| Why XR | 45° and 135° scatter added to 90° give a lower OD detection limit and earlier signs of growth | [Step 4](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/) |
| Configuration | XR photodiode channel values in `config.ini` (set by the card bundle, or by hand from Pioreactor's XR guide) | [Step 5](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) |
| OD and bubbles | The plugin pauses OD reading during each sparge plus a settle time, and around electrolysis ON phases only when electrolysis cycles (OFF time above 0) | [Software](/software/) |

## Computer and power

| Parameter | Value | Source |
| --- | --- | --- |
| Raspberry Pi | Raspberry Pi 5, 1 GB or larger | [raspberry-pi](repo:docs/components/raspberry-pi.yaml) |
| microSD card | 32 GB or larger, A2 / U3 / V30 | [microsd-card](repo:docs/components/microsd-card.yaml) |
| Pi supply | [27 W USB-C PD](repo:docs/components/usb-c-power-supply.yaml), 5.1 V, 5 A; actual draw about 15.3 W per Pioreactor. Four or more units can share one multi-port charger giving at least 15.3 W per port | [usb-c-power-supply](repo:docs/components/usb-c-power-supply.yaml) |
| 12 V supply | [12 V DC, at least 1 A](repo:docs/components/power-supply-12v.yaml), 2.1 × 5.5 mm barrel, centre-positive, into the HAT's barrel jack; powers the PWM rail (pumps and solenoid), not the Pi | [power-supply-12v](repo:docs/components/power-supply-12v.yaml) |
| HAT shunt | On the two pins closest to the LED outputs, so PWM 1 to 4 run from 12 V. Check: Manage → System → Voltage on PWM rail reads about 12 V | [Steps 3](https://docs.electropioreactor.org/AEP/step-03-raspberry-pi-and-hat/) and [9](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/) |

### Channel map

| HAT output | AEP0.2 use | `config.ini` label |
| --- | --- | --- |
| PWM 1 | Stirrer | `stirring` |
| PWM 2 | Media pump | `media` |
| PWM 3 | Product (waste) pump | `waste` |
| PWM 4 | CO₂ solenoid | `relay` |
| PWM 5 | Heater | `heating` |
| LED D | Electrode pair | `[electropioreactor.config] led_channel = D` |

The Mixed-culture electroPioreactor (MEP) swaps the two pumps: media on PWM 3, waste on PWM 2. See [Variants](/variants/).

## Sterilisation and aseptic barrier

| Item | Status | Source |
| --- | --- | --- |
| Whole-unit sterilisation procedure | Awaiting approval by the project's principal investigators (PIs) | [Step 17](https://docs.electropioreactor.org/AEP/step-17-sterilise/) |
| Gas-path filtration | 0.2 µm PTFE vent filters on the media bottle vent, product bottle vent, CO₂ inlet and both gas outlets; 6 per kit including a spare | [hydrophobic-vent-filter](repo:docs/components/hydrophobic-vent-filter.yaml) |
| Inoculation | By syringe through the septum, with no open port | [Step 11](https://docs.electropioreactor.org/AEP/step-11-ports/) |
| Tubing and bottle caps | Listed as autoclavable | [silicone-tubing](repo:docs/components/silicone-tubing.yaml), [gl45-cap](repo:docs/components/gl45-cap.yaml) |
| Medium | Base solution autoclaved (121 °C liquid cycle); trace-metal stocks filter-sterilised (0.2 µm) | [Media](/media/) |
| Vial Cap (PC-CF) | Autoclave tolerance not yet documented | <!-- CHECK: AsepticElectroPioreactor/README.md claims autoclave-ability for the variant, but no repo source states the PC-CF cap's autoclave rating --> – |
| Filter replacement interval | Still to specify (BoM open item 2.5) | [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) |

## What changed from AEP0.1.1

| Area | AEP0.1.1 | AEP0.2 |
| --- | --- | --- |
| Vessel | Pioreactor 20 ml v1.1, ~15 ml working volume | Pioreactor 40 ml v1.5 + XR upgrade kit, ~30 ml working volume |
| Computer | Raspberry Pi Zero 2W or Pi 4 4 GB, micro-USB or USB-C supply | Raspberry Pi 5 1 GB, 27 W USB-C supply |
| Vial cap | Separate cap + [ElectrodeTopStop](repo:Components/ElectrodeTopStop), cap O-ring + 2 electrode O-rings | One-piece [Vial Cap and electrode holder](repo:Components/Vial%20Cap), single silicone septum |
| Anode | Platinised titanium rod, 100 mm | MMO (IrO₂–Ta₂O₅) tube, 100 mm, CO₂ delivered through its open base |
| Electrode fixing | M3 bolt through captive nut | Ring terminal + thumb screw, M3 nut and spring washer |
| Ports | Flexelene 135C tubing | Stainless steel needles |
| Gas sealing | PTFE tape on every threaded joint | O-rings where possible, Loctite 577 elsewhere |
| CO₂ inlet | Regulator tightened onto the cylinder against escaping gas | KegLand KL15578 pin-adjustment adapter: tighten first, then open the pin |
| Sparging control | `pioreactor-relay-plugin` + experiment profile YAML | [electroPioreactor plugin](/software/): electrolysis, sparging and OD pausing in one job |
| Dropped | Bubble counter, pinch-slider inoculation port, jubilee clips | Inoculation by syringe through the septum |

<!-- source: docs/steps/step-00-before-you-start.md, "What changed from AEP0.1.1". The archived instructions are AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md. -->

## Still to specify

These are open in [`BoM.md`](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md); until they close, treat the related rows above as provisional.

- Standard electrode insertion depth (2.3) and the published septum outline (2.4): these block third-party sourcing.
- Operating parameters: applied voltage or current, electrode spacing and submerged area, medium and duty cycle.
- Whether the 304 needles or the 316 upgrade suit the AEP medium (2.6).
- Solenoid, regulator and fitting ratings and thread standards (3.1, 4.2, 4.6).
- Wire sizes, crimp part numbers and crimp tool (3.2, 3.3, 3.8, 3.9).
- Luer body materials, tubing wall and hardness (5.3 to 5.7).
- Sterilisation procedure, pending PI approval.

Want one built for you? See [Get one](/get-one/). Terms are defined in the [Glossary](/glossary/).
