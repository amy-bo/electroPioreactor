---
title: Mixed-culture electroPioreactor (MEP)
description: The original, lower-cost electroPioreactor for enrichment cultures and teaching, rebuilt in 2026 for the University of Edinburgh's MSc projects.
section: build
audience: everyone
order: 7
---
The Mixed-culture electroPioreactor (MEP) is where all of this started: a standard Pioreactor vial with an electrode pair through the cap and a carbon dioxide (CO₂) line, and none of the sealing that makes the [AEP](/aep/) aseptic. It is cheaper and simpler, and it suits the job we first built it for, which is enrichment.

## What it is for

Take a spoonful of mud or river water, put it in a chloride-free medium with hydrogen and CO₂ as the only food, and see what grows. Whatever keeps growing through a few rounds of that, and stops when the electrolysis stops, is very likely a hydrogen-oxidising bacterium (HOB), and it might be one nobody has grown before. Worked enrichment protocols are in [Methodologies/](repo:Methodologies/) and summarised on [Research](/research/#methodologies). <!-- source: Methodologies/Irvine/Enrichment.md (stages: HOB selection, serial transfer, electrolysis dependence) -->

The MEP was the only electroPioreactor until the AEP came along. We picked it up again in 2026 as the low-cost version, and built two MEP0.3 units for the [School of Biological Sciences](https://biology.ed.ac.uk/) at the University of Edinburgh, for its 2026 MSc Industrial Projects. <!-- source: MixedElectroPioreactor/README.md; MixedElectroPioreactor/Assembly-EdMSc26.md (MEP0.3) -->

How it differs from the AEP, part by part, is in the side-by-side table on [Which electroPioreactor?](/variants/#side-by-side). An MEP with vent filters on every gas path is the Budget aseptic electroPioreactor (BAEP), described on the same page.

<figure>
<img src="/img/pinch-sliders.jpg" alt="Five small black 3D-printed pinch sliders with keyhole slots, one fitted on a length of clear silicone tubing" width="1200" height="1091">
<figcaption>Pinch sliders: a few pence of PETG that closes a silicone line without a valve. The design is in <a href="repo:Components/PinchSlider/">Components/PinchSlider/</a>. Photo: AMYBO, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</figcaption>
</figure>

## Build and run one

- **Guide:** the [MEP guide](https://docs.electropioreactor.org/MEP/) at docs.electropioreactor.org, with a video and drawings for each step. It shares the steps the MEP has in common with the [AEP guide](https://docs.electropioreactor.org/AEP/).
- **Running it:** the [MEP protocol](https://docs.electropioreactor.org/MEP/protocol/), covering calibration and operation.
- **Plugin:** the [MEP card bundle](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/releases/latest/download/electroPioreactor-MEP-card-bundle.zip) installs the electroPioreactor plugin from the SD card. See [Software](/software/#installing).

The documents written for the Edinburgh students are in [MixedElectroPioreactor/](repo:MixedElectroPioreactor/). They assume you have never seen a Pioreactor before:

- [Assembly](repo:MixedElectroPioreactor/Assembly-EdMSc26.md)
- [Calibration](repo:MixedElectroPioreactor/Calibration.md)
- [Operation](repo:MixedElectroPioreactor/Operation.md): 14 ml of medium in a 20 ml vial, and what to do each day
- [Pre-transport check](repo:MixedElectroPioreactor/PreTransportCheck-EdMSc26.md): what we test before a unit leaves the workshop

## History

The 2024 electroPioreactor v0.02, the design the MEP grew from, is on [History](/history/), with its full bill of materials. The 2023 and 2024 experiments behind it are on amybo.org: [first experiments](https://amybo.org/projects/past/experiments/). The [Crymlyn Fen home enrichment protocol](repo:Methodologies/Crymlyn.md) is written for an AEP0.1, but the stages are the same on an MEP.
