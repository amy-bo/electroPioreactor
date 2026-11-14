---
title: History
description: How the electroPioreactor started, from the 2023 experiments and the 2024 v0.02 mixed-culture design, with its original bill of materials, to today's AEP and MEP.
section: about
audience: everyone
order: 30
---
The electroPioreactor began in 2023 and 2024 as a Pioreactor with an electrode pushed through a 3D-printed cap and a CO₂ line from a SodaStream cylinder. This page keeps the early notes for the record. For current designs, see [Which electroPioreactor?](/variants/).

## Timeline

- **2023 and 2024.** First experiments by the AMYBO community, including [CO₂ sparging](https://amybo.org/projects/past/experiments/co2-sparging/) on a stock Pioreactor and [anode tests](https://amybo.org/projects/past/experiments/electrolysis/). They are kept on amybo.org with the rest of AMYBO's [first experiments](https://amybo.org/projects/past/experiments/).
- **From 2023.** Harvey Mudd College clinic teams worked on the anode and on a solenoid pinch valve that became [OpenValve](https://amybo.org/projects/other-hardware/openvalve/); their final outputs are dated May 2025. See [Research](/research/#past-research-projects). <!-- source: amybo.org past/experiments/electrolysis (2023 Anode Team); PastResearch/HMC-Clinic/ (zip names dated 20250510) -->
- **2024.** The electroPioreactor v0.02, a mixed-culture design (MEP0.02), written up below.
- **Along the way.** Eli Silver at Brown University's Harris Lab diagnosed CO₂ backflow up the sparging line, which led to the venting solenoid. See [Research](/research/#past-research-projects).
- **2025.** The first Aseptic electroPioreactors (AEP0.1 and AEP0.1.1) were built, and students trained on them in Edinburgh in November. See [AEP](/aep/).
- **2026.** AEP0.2, the electroPioreactor plugin and the [assembly guide](https://docs.electropioreactor.org/AEP/). Two MEP0.3 units went to the University of Edinburgh's MSc projects. See [MEP](/mep/).

## The 2024 idea: an affordable electrobioreactor

The 2024 notes described the electroPioreactor like this. It builds on the well-established [Pioreactor](https://pioreactor.com) by adding in-culture electrodes and CO₂ sparging, turning it into an electrobioreactor:

- **In-culture electrodes** generate hydrogen, the energy source of hydrogen-oxidising bacteria (HOB), and oxygen, the terminal electron acceptor for their aerobic respiration.
- **CO₂ sparging** supplies the bacteria's carbon source and purges excess oxygen.

That is still how it works; what has changed is the detail. See [How it works](/how-it-works/) and [What we have learned](/lessons/).

## electroPioreactor v0.02 (2024)

> **Note:** This is a historical parts list, kept as it was published in 2024. Links may have changed or gone, and several choices were later replaced: the two-port solenoid by a venting one, platinum and graphite anodes by mixed metal oxide, and crocodile clips by a clamped top stop. Do not build from it; use the [current guides](/variants/).

The v0.02 mixed-culture electroPioreactor came in two versions: MEP0.02Pt with a platinum-plated titanium anode and MEP0.02C with a graphite anode.

### Pioreactor

1. 1 × [Pioreactor 20 ml v1.1 with Raspberry Pi and microSD card](https://pioreactor.com/products/pioreactor-20ml), [normally configured](https://docs.pioreactor.com/user-guide/hardware-setup-intro)
2. 1 × [Dovetail platform for Raspberry Pi](https://www.printables.com/model/679663-pioreactor-platform-with-dovetails-for-b-models/files)

### Electrolysis

1. Either 1 × platinum-plated titanium anode (MEP0.02Pt: 6 mm diameter, 60 mm total length, 35 mm platinised length), or 1 × graphite anode (MEP0.02C: 6 mm diameter, 60 mm total length)
2. 1 × crocodile clip
3. 1 × stainless steel 60 mm M4 bolt (the cathode)
4. 1 × stainless steel M4 locking nut
5. 1 × ring crimp terminal
6. 1 × [Pioreactor vial cap with hole for 6 mm electrode](https://www.printables.com/model/974845-pioreactor-vial-cap-with-hole-for-6mm-electrode)
7. 4 × female Dupont cables: [Amazon.co.uk](https://amzn.eu/d/fKdnqrx) (also needed for CO₂ sparging)

### CO₂ sparging

1. 1 × SodaStream cylinder: [Amazon.co.uk](https://amzn.eu/d/1dZqKsi) (classic blue, not quick-connect pink)
2. 1 × [SodaStream holder for Pioreactor](https://www.printables.com/model/855700-sodastream-holder-for-pioreactor)
3. 1 × W21.8-14 to TR21-4 adaptor: [Amazon.co.uk](https://amzn.eu/d/1eZLJ7n). Chosen because it is also a 90° bend, but this one is uncomfortably stiff to adjust.
4. 1 × CO₂ regulator and solenoid: [Amazon.co.uk](https://amzn.eu/d/gSnMfxg). In 2024, [Harvey Mudd](https://forum.amybo.org/t/keeping-up-with-hmc-clinic-project/126/32) were working on a pinch valve to improve on this.
5. About 20 cm of 4 mm PU tubing: [Amazon.co.uk](https://amzn.eu/d/h9DJO5H)
6. 2 × check valves: [Amazon.co.uk](https://amzn.eu/d/giKnew4)
7. 1 × 3/16" barb male luer lock: [Amazon.co.uk](https://amzn.eu/d/83w3N6F)
8. 1/16" barb luer locks: 2 × male, [Amazon.co.uk](https://amzn.eu/d/5yACgUp), and 2 × female, [Amazon.co.uk](https://amzn.eu/d/deEBv9w)
9. About 20 cm of 1/16" internal diameter silicone tubing: [Amazon.co.uk](https://amzn.eu/d/bOQ02Ow)
10. 1 × 2.1 × 5.5 mm male barrel plug, to connect the Raspberry Pi to the solenoid: [Amazon.co.uk](https://amzn.eu/d/d5QFCxD)

### Continuous flow

1. 2 × [12 V peristaltic pump](https://pioreactor.com/collections/accessories-and-parts/products/peristaltic-pump)
2. 2 × [dovetail peristaltic pump holder](https://www.printables.com/model/298240-pioreactor-platform-with-dovetails/files#preview:file-NvR1r)
3. 2 × centrifuge tubes: [Amazon.co.uk](https://amzn.eu/d/57WO7D8)
4. 2 × [dovetail centrifuge tube holders](https://github.com/oplz/DormantBioLabResources/blob/main/Prints/dovetailed_rack/50ml_tube_rack.stl)

### Reagents

See the forum post on [HOB culture medium ingredients](https://forum.amybo.org/d/22-hob-culture-medium-ingredients/7). Today's media are on [Media](/media/).

### Optional extras

1. Spare 20 ml glass vials: [Amazon.co.uk](https://amzn.eu/d/fbFWJ66)

### Recommended budget labware

1. 1 × [1 to 5 ml pipettor](https://amzn.eu/d/9jKUSIx) and [tips](https://amzn.eu/d/cSiLNzj)
2. Nitrile gloves: [Amazon.co.uk](https://amzn.eu/d/iIR5cf6)
3. 1 × spatula: [Amazon.co.uk](https://amzn.eu/d/houYNco)
4. 1 × weighing boat: [Amazon.co.uk](https://amzn.eu/d/iaNhVpD)
5. Jewellers' scales
6. 1 × 1 L volumetric flask: [Labpals](https://www.labpals.co.uk/product-page/1000ml-volumetric-flask-with-polyethylene-stopper-borosilicate-glass-class-a)
7. 1 × 1 L reagent bottle: [Labpals](https://www.labpals.co.uk/product-page/clear-borosilicate-glass-reagent-bottle-with-screw-cap-1000-ml-with-graduations)
8. 1 × 1 L amber reagent bottle: [Labpals](https://www.labpals.co.uk/product-page/amber-borosilicate-glass-reagent-bottle-with-screw-cap-1000-ml-with-graduations)
9. 1 × 1 L wash bottle: [Labpals](https://www.labpals.co.uk/product-page/1000-ml-performance-plastic-wash-bottle-distilled-water-labeled-4-color)

### Recommended tools for assembly

1. 1 × crimping pliers: [Amazon.co.uk](https://amzn.eu/d/5pGr9b4)
2. 1 × 150 mm pliers wrench: [Amazon.co.uk](https://amzn.eu/d/3nkLCuu)
3. 1 × needle-nose pliers: [Amazon.co.uk](https://amzn.eu/d/74U0lou)
4. 1 × PH0 screwdriver

The original MEP parts list also lives in the repository, in [Components/](repo:Components/). These notes were first published on amybo.org.
