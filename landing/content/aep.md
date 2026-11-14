---
title: Aseptic electroPioreactor (AEP)
description: The sealed, filtered electroPioreactor for single-strain research, built and tested with Imperial College London and the University of Edinburgh, and what its first runs taught us.
section: build
audience: everyone
order: 6
---
If you want to grow one particular strain of hydrogen-oxidising bacteria (HOB) and be sure that what you are measuring is that strain, you need to keep everything else out. The Aseptic electroPioreactor (AEP) is the electroPioreactor with that in mind: a sealed cap with a silicone septum that closes around each electrode and every port, 0.2 µm hydrophobic filters on the gas in and gas out, luer-lock connections for feeding and sampling, and parts chosen to survive the autoclave. <!-- source: AsepticElectroPioreactor/README.md -->

We designed it to be safe first, then accurate and repeatable, then automated, then good value, in that order. When two of those pull in different directions, the earlier one wins. <!-- source: AsepticElectroPioreactor/README.md (design criteria) -->

The AEP is the subject of the CARMA Hub Pump Priming project led by Dr Sonja Billerbeck (Imperial College London), with Prof. Chris French leading the work at the University of Edinburgh, AMYBO as design and training partner and LabCrafter supplying the kits. See [About](/about/#the-carma-hub-pump-priming-project).

- **Build it:** [AEP guide](https://docs.electropioreactor.org/AEP/), with a video and a drawing for each step.
- **Source:** [AsepticElectroPioreactor/](repo:AsepticElectroPioreactor/) on GitHub.
- **Compare it** with the Mixed-culture version: [Which electroPioreactor?](/variants/)

## Versions

The full version history, with a table of every change, is on [Which electroPioreactor?](/variants/#version-history-aep). In short:

- **AEP0.1 and AEP0.1.1** (2025). Six units built. Three of them were assembled by the students themselves at the [joint training](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1%20Training/README.md) at the University of Edinburgh on 18 to 21 November 2025, one each. The AEP0.1.1 changes came out of what we learned that week, and its [assembly instructions](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md) are archived in the repository.
- **AEP0.2** (2026). A redesigned one-piece cap (a silicone septum instead of O-rings, and thumb screws for the electrode leads), mixed metal oxide anodes, and card bundles so the plugin can go onto a unit that never sees the internet. The first kits reached Edinburgh in September 2026. The step-by-step guide is at [docs.electropioreactor.org/AEP](https://docs.electropioreactor.org/AEP/). <!-- source: docs/steps/step-00-before-you-start.md (What changed from AEP0.1.1) -->

<figure>
<img src="/img/electrode-top-stop.jpg" alt="A 3D-printed grey block with two screws, holding a pair of stainless electrodes with a red and a black wire, held in a hand over a cutting mat" width="1200" height="1025">
<figcaption>The electrode top stop, added after the November 2025 training, holding an electrode pair. In AEP0.2 it is part of the <a href="repo:Components/Vial%20Cap/">parametric cap</a>. Photo: AMYBO, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</figcaption>
</figure>

## What we learned from the first runs

Here is how the November 2025 training week went. Three students each built an AEP0.1. The software set-up then took a long time to diagnose, because none of us could connect to the units over SSH (secure shell); it turned out to be a [bug in the Raspberry Pi Imager](https://github.com/raspberrypi/rpi-imager/issues/1170), which Cam Davidson-Pilon of Pioreactor tracked down, and an older Imager fixed it. A heterotrophic culture of *Cupriavidus metallidurans* (grown on an ordinary food source, here gluconate) was established. The first attempt at autotrophic growth, on hydrogen from the electrodes and CO₂ from the cylinder alone, showed no growth in 17 hours. <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md -->

Also that week: new crocodile clips kept falling off the electrodes, which is where the top stop came from; the SodaStream cylinders moved from the middle of the raft to the back, which made the bottles easier to see and the tubing shorter; and a vial dropped and smashed, so now we carry boxed spares. The write-up lists the suspects for the failed autotrophic run: the medium, too high a voltage, temperature control, whether the CO₂ sparging was actually clearing the oxygen, and the anodes discolouring. The detailed results are on [Research](/research/#aep01-training-november-2025).

That list is what the plugin and AEP0.2 were built to work through: intermittent sparging with the electrolysis paused, current limited rather than voltage set, and one variable at a time.

<div class="photo-row">
<figure>
<img src="/img/anode-discoloured-aep01.jpg" alt="Close-up of a metal electrode rod with a shimmering band of gold, pink and green colours across its surface" width="800" height="297">
<figcaption>An anode after a run: the discolouration everyone noticed.</figcaption>
</figure>
<figure>
<img src="/img/anode-platinised-titanium.jpg" alt="Macro photo of a platinised titanium rod with a rough grey coating, with a smoother patch near one end" width="800" height="600">
<figcaption>The platinised titanium anode we started with. AEP0.2 moves to mixed metal oxide.</figcaption>
</figure>
<figure>
<img src="/img/anode-swabbed.jpg" alt="Macro photo of a discoloured electrode rod with a smear where it has been wiped, showing brighter metal underneath" width="800" height="600">
<figcaption>Swabbed: some of it wipes off. It looks like mineral scale rather than corrosion, but we are still checking.</figcaption>
</figure>
</div>

Photos: AMYBO, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). All of them, and more, are in the [anode discolouration results folder](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/Anode%20discolouration/).

## In the repository

- [Overview, design criteria and directory](repo:AsepticElectroPioreactor/)
- [Results](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/): the training write-up, the anode photos, and [continuous versus intermittent CO₂ sparging](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/Gas%20sparging/Continuous%20or%20Intermittent%20CO2%20sparging.md)
- [Meeting notes](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Meetings.md) of the CARMA Hub project
- [Components and bill of materials](repo:Components/), including the [vial cap](repo:Components/Vial%20Cap/) OpenSCAD source and the [GL45 bottle holder](repo:Components/GL45BottleHolder/); open AEP0.2 specification questions are in [BoM.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md)
- [The plugin](/software/) that runs it from the Pioreactor web interface
- Edinburgh's first runs, written up on the forum: [trial experiment on heterotrophic electrolysis](https://forum.amybo.org/t/trial-experiment-on-heterotrophic-electrolysis/163)

Kits and parts come from [LabCrafter](https://labcrafter.co.uk) in the UK and [Pioreactor](https://pioreactor.com) elsewhere: see [Get or build one](/get-one/).
