# electroPioreactor Components

## AEP0.2 (current)

The full AEP0.2 bill of materials is in the assembly guide at <https://docs.electroPioreactor.org/AEP> (its **Before you start** step lists everything a kit should contain) and, as one file per part with specification, supplier and history, in [`docs/components/`](../docs/components/). Specifications still open are listed in [the BoM](../AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md). Quantities below are per unit.

### Unique components

1. 1x [Vial Cap and electrode holder](Vial%20Cap): one printed PC-CF piece sealing on a 2 mm silicone septum, printed from [`AEP2.0/Vessel Cap.stl`](Vial%20Cap/AEP2.0) ([component](../docs/components/vial-cap.yaml))
1. 2x [Dovetail GL45 bottle holders](GL45BottleHolder) ([component](../docs/components/gl45-bottle-holder.yaml))

### Pioreactor

1. 1x [Pioreactor 40 ml v1.5](../docs/components/pioreactor-40ml.yaml), with the [XR upgrade kit](../docs/components/xr-upgrade-kit.yaml) and the [Precision Temperature Upgrade Kit](../docs/components/precision-temperature-upgrade-kit.yaml)
1. 1x [Raspberry Pi 5 1GB](../docs/components/raspberry-pi.yaml) and [27 W USB-C power supply](../docs/components/usb-c-power-supply.yaml); 1x [12 V power supply](../docs/components/power-supply-12v.yaml) for the HAT
1. 2x [12 V peristaltic pumps](../docs/components/peristaltic-pump.yaml)
1. 1x [Pumping dovetail platform](../docs/components/pumping-dovetail-platform.yaml) and 1x [CO₂ cylinder dovetail holder](../docs/components/co2-cylinder-dovetail-holder.yaml)

### Electrolysis

1. 1x [MMO anode](../docs/components/mmo-anode.yaml): 100 mm long, 6 mm OD, 70 mm active length
1. 1x [316 stainless steel cathode](../docs/components/stainless-steel-cathode.yaml): 100 mm long, 6 mm diameter
1. 2x [electrode cables](../docs/components/electrode-cable.yaml) with ring terminals, M3 nuts, flat and spring washers, thumb screws, and a crimp connector housing for LED channel D

### Media and ports

1. 2x [250 ml GL45 bottles](../docs/components/gl45-bottle.yaml) and [GL45 caps](../docs/components/gl45-cap.yaml), [tubing](../docs/components/silicone-tubing.yaml) and 1/16" barb luer locks
1. 1x [80 mm 316 needle](../docs/components/needle-80mm-316.yaml), plus the three 75 mm 304 needles from the Pioreactor box
1. 6x [0.2 µm hydrophobic vent filters](../docs/components/hydrophobic-vent-filter.yaml): five fitted (both bottle vents, the CO₂ inlet and the two gas outlets) and one spare

### CO<sub>2</sub> sparging

1. 1x [SodaStream CO₂ cylinder](../docs/components/sodastream-co2-cylinder.yaml) (blue screw-in) and [cylinder-to-regulator adapter](../docs/components/cylinder-regulator-adapter.yaml)
1. 1x [CO₂ regulator](../docs/components/co2-regulator.yaml), [3/2 venting 12 V solenoid valve](../docs/components/solenoid-valve.yaml) on PWM 4, and [needle valve](../docs/components/co2-needle-valve.yaml)
1. 1x [polyurethane CO₂ tube](../docs/components/polyurethane-co2-tube.yaml) and [anode feed tube](../docs/components/anode-feed-tube.yaml): CO₂ enters through the hollow anode

## MEP0.02 and AEP0.1 parts list (historical)

The list below is the original electroPioreactor parts list, from before AEP0.2: a Pioreactor 20 ml with 60 mm electrodes (MEP0.02Pt / MEP0.02C). It is kept for reference and for existing units; the current MEP build is in the [MEP guide](https://docs.electroPioreactor.org/MEP).

### Unique Components

- 1x [Vial Cap](Vial%20Cap), the O-ring generation (`seal = "oring"`, two pieces), with the separate [ElectrodeTopStop](ElectrodeTopStop)

### Pioreactor

1. 1x [Pioreactor 20ml](https://pioreactor.com/products/pioreactor-20ml?variant=46984254586936)
1. 1x [Peristaltic Pumps](https://pioreactor.com/products/peristaltic-pump)
1. 1x [Dovetail Platform for Pioreactor and Pumps](https://pioreactor.com/collections/accessories-and-parts/products/pioreactor-and-pump-dovetail-platform?variant=42835335872568)

### Media vessel options

#### Centrifuge Tubes

1. 2x [Autoclavable](https://www.starlabgroup.com/GB-en/product/50-ml-centrifuge-tubes-pf-sl-9455674.html?utm_source=chatgpt.com&childSku=E1450-0400) or [Not](https://amzn.eu/d/9wjwtFf)
1. 2x [Dovetail centrifuge tube holders](https://github.com/oplz/DormantBioLabResources/blob/main/Prints/dovetailed_rack/50ml_tube_rack.stl)

OR

#### GL45 Bottles

1. 2x [Caps](https://pioreactor.com/collections/accessories-and-parts/products/gl45-cap-with-luer-lock-connectors?variant=46788561371192)
1. 2x [250 ml Bottles](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate/)
1. 2x [Dovetail Duran holders 0.25L](https://www.printables.com/model/1058356-duran-bottle-holding-platform-for-pioreactor-platf/files)

### Electrolysis

1. Either  
   - 1x Platinum plated titanium anode (for MEP0.02Pt – 6mm diameter, 60mm total length, 35mm platinised length), or  
   - 1x Graphite anode (for MEP0.02C – 6mm diameter, 60mm total length)  
1. 1x Crocodile clip
1. Either
   - Bolt option
     1. 1x Stainless Steel 60mm M4 bolt
     2. 1x Stainless Steel M4 Locking Nut
     3. 1x Ring Crimp Terminal, or
    - 1x Stainless Steel anode (6mm diameter, 60mm total length)
1. 4x Female Dupont Cables: [Amazon.co.uk](https://amzn.eu/d/fKdnqrx) (also needed for CO<sub>2</sub> sparging)

#### CO<sub>2</sub> sparging

1. 1x Sodastream cylinder: [Amazon.co.uk](https://amzn.eu/d/1dZqKsi) (classic blue NOT quick connect pink)
1. 1x [Sodastream holder for Pioreactor](https://www.printables.com/model/855700-sodastream-holder-for-pioreactor)
1. 1x W21.8-14 to TR21-4 adaptor: [Amazon.co.uk](https://amzn.eu/d/1eZLJ7n) [^1]
1. 1x CO<sub>2</sub> Regulator and Solenoid: [Amazon.co.uk](https://amzn.eu/d/gSnMfxg)
1. ~ 20cm 4mm PU tubing: [Amazon.co.uk](https://amzn.eu/d/h9DJO5H)
1. 2x Check valves: [Amazon.co.uk](https://amzn.eu/d/giKnew4)
1. 1x 3/16" barb male Luer lock: [Amazon.co.uk](https://amzn.eu/d/83w3N6F)
1. 1/16" barb Luer Locks - 2x Male: [Amazon.co.uk](https://amzn.eu/d/5yACgUp) & 2x Female: [Amazon.co.uk](https://amzn.eu/d/deEBv9w)
1. ~ 20cm 1/16" ID Silicone tubing: [Amazon.co.uk](https://amzn.eu/d/bOQ02Ow)
1. 1x 2.1mm x 5.5mm Male Barrel Plug: [Amazon.co.uk](https://amzn.eu/d/d5QFCxD) - to connect Raspberry Pi to solenoid with:

#### Reagents

* See this post: https://forum.amybo.org/d/22-hob-culture-medium-ingredients/7

### Optional extras

1. Spare 20ml glass vials: [Amazon.co.uk](https://amzn.eu/d/fbFWJ66)

#### Recommended Budget Labware

1. 1x [1-5ml Pipettor](https://amzn.eu/d/9jKUSIx) & [tips](https://amzn.eu/d/cSiLNzj)
1. 1x Nitrile Gloves: [Amazon.co.uk](https://amzn.eu/d/iIR5cf6)
1. 1x Spatula: [Amazon.co.uk](https://amzn.eu/d/houYNco)
1. 1x Weighing Boat: [Amazon.co.uk](https://amzn.eu/d/iaNhVpD)
1. Jewellers Scales
1. 1x 1L volumetric flask: [Labpals](https://www.labpals.co.uk/product-page/1000ml-volumetric-flask-with-polyethylene-stopper-borosilicate-glass-class-a)
1. 1x 1L Reagent Bottle: [Labpals](https://www.labpals.co.uk/product-page/clear-borosilicate-glass-reagent-bottle-with-screw-cap-1000-ml-with-graduations)
1. 1x 1L Amber Reagent Bottle: [Labpals](https://www.labpals.co.uk/product-page/amber-borosilicate-glass-reagent-bottle-with-screw-cap-1000-ml-with-graduations)
1. 1x 1L Wash Bottle: [Labpals](https://www.labpals.co.uk/product-page/1000-ml-performance-plastic-wash-bottle-distilled-water-labeled-4-color)

#### Recommended Tools for Assembly
1. 1x Crimping Pliers: [Amazon.co.uk](https://amzn.eu/d/5pGr9b4)
1. 1x 150mm Pliers Wrench: [Amazon.co.uk](https://amzn.eu/d/3nkLCuu)
1. 1x Needle-Nose Pliers: [Amazon.co.uk](https://amzn.eu/d/74U0lou)
1. 1x PH0 Screwdriver: [Amazon.co.uk](https://amzn.eu/d/houYNco)

[^1]: Could be improved, I got this as it is also a 90° bend, but mine is uncomfortably stiff to adjust
