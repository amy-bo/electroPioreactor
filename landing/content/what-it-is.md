---
title: What it is
description: A small bioreactor that grows hydrogen-oxidising bacteria on electricity, water and carbon dioxide.
order: 10
---
The electroPioreactor is a small bench-top bioreactor that grows hydrogen-oxidising bacteria (HOB) in a sealed glass vial. It is a [Pioreactor](https://pioreactor.com) with two electrodes and a carbon dioxide (CO₂) supply added.

## Hydrogen-oxidising bacteria

HOB can live on three gases. Hydrogen is their energy source, they breathe oxygen, and they build their cells from the carbon in CO₂. Add water, a nitrogen source and some trace minerals, and they have everything they need to grow.

Their cells are rich in protein, and hydrogen and oxygen can be made from water with electricity. So HOB can turn renewable electricity, water and CO₂ into protein, without farmland. [AMYBO](https://amybo.org) created the electroPioreactor to make it possible to produce HOB affordably, safely and locally.

## How it works

Hydrogen is a potentially highly explosive gas. So the electroPioreactor stores none. It makes both hydrogen and oxygen in the culture, and as hydrogen is the rate-limiting nutrient, bacteria in growth phase can consume it as soon as it is produced.

- **Electricity splits water.** Hydrogen forms on the stainless steel cathode. Oxygen forms on the mixed metal oxide (MMO) coating of the hollow titanium anode.
- **CO₂ comes from a SodaStream cylinder.** It flows down the hollow anode in short, timed bursts. It is the bacteria’s carbon source, and it flushes out excess oxygen.
- **The Pioreactor does the rest.** It stirs the culture, maintains its temperature, measures growth by shining infrared light through it, and pumps fresh nutrient liquid in and culture out.
- **One silicone septum seals the vial.** Bacteria can be inoculated by syringe, and samples can be drawn mid-run, maintaining sterility. Two needles with hydrophobic vent filters let excess gas escape to maintain ambient pressure in the vial.
- **The electroPioreactor plugin controls electrolysis and CO₂ sparging.** The Pioreactor software records and charts optical density and temperature in real time. The plugin pauses optical density measurements during and following sparging, and optionally electrolysis.

The [3D model on the home page](/) names each part when you hover over it, and its Tour walks through them in order.

## Critical points

- **The medium is also the electrolyte.** Most HOB media contain chloride, which electrolysis turns into bleach. Ours is chloride-free but the conductivity is critical for electrolysis. See [Research](/research/#the-medium).
- **MMO lowers electrolysis overpotential.** We started with platinum-plated titanium and moved to MMO, which gives the same current at a lower voltage. This reduces the formation of harmful reactive oxygen species. The cathode is plain stainless steel.
- **The CO₂ valve has to vent.** A normal solenoid valve traps CO₂ in the line when it closes. The CO₂ dissolves, and the vacuum it leaves sucks culture back up the tube. Eli Silver at Brown University diagnosed this, and a venting valve fixes it.

## What AEP0.2 improved

- **Tubular anode.** CO₂ is sparged through its centre, so CO₂ bubbles knock excess oxygen bubbles off the anode and the sparging geometry is the same every time.
- **One-piece cap with a single silicone septum.** It replaces multiple O-rings, holds the electrodes parallel at a set height, takes stainless steel needle ports, and has a large self-sealing area for hypodermic needles.
- **Sprung M3 thumbscrews.** They hold the power leads on the electrodes without tools, and make it easier to connect positive to the anode and negative to the cathode.
- **40 ml vial.** Twice the height gives gas room to leave the liquid below the electrodes, as microbubbles were affecting the optical density readings.
- **Pioreactor XR Upgrade Kit.** Light sensors at a shallower angle give a lower limit of detection, so growth shows earlier and failed runs can be stopped sooner.
- **Plugin.** It times electrolysis and gas sparging, suppresses optical density readings after them, limits the electrolysis power to protect the electrodes, and installs from a microSD card in labs where Pioreactors are not allowed internet access.
- **Gas train.** O-rings where possible and anaerobic thread sealant elsewhere, in place of PTFE tape, and a thumbscrew adapter to open the CO₂ cylinder.
- **Raspberry Pi and temperature.** A faster Raspberry Pi with wired Ethernet, and the Pioreactor Precision Temperature Upgrade Kit.

## Two versions

- **The Aseptic electroPioreactor (AEP)** keeps a single strain free of contamination, with filters on every gas path, a septum-sealed cap and parts that can be autoclaved. The current version, AEP0.2, holds 30 ml of culture.
- **The Mixed-culture electroPioreactor (MEP)** is a lower-cost version for mixed cultures, such as bacteria enriched from soil or water, and for student projects.
