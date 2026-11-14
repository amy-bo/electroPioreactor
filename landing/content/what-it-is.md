---
title: What it is
description: A small bioreactor that grows hydrogen-oxidising bacteria on electricity, water and carbon dioxide.
order: 10
---
The electroPioreactor is a small bench-top bioreactor that grows hydrogen-oxidising bacteria (HOB) in a sealed glass vial. It is a [Pioreactor](https://pioreactor.com) with two electrodes and a carbon dioxide (CO₂) supply added.

## Hydrogen-oxidising bacteria

HOB can live on three gases. Hydrogen is their energy source, they breathe oxygen, and they build their cells from the carbon in CO₂. Add water and a few dissolved minerals and they have everything they need to grow.

Their cells are rich in protein, and hydrogen and oxygen can be made from water with electricity. So HOB can turn renewable electricity, water and CO₂ into protein, without farmland. [AMYBO](https://amybo.org) created the electroPioreactor to make it possible to produce HOB affordably, safely and locally.

## How it works

![The AEP0.2 vial with its one-piece cap, needles, electrodes, sensors and heater](/img/vial-cap-a4-white.png)

Hydrogen is an awkward gas. A sealed vial of hydrogen and oxygen is unlikely to get past any sensible risk assessment. So the electroPioreactor stores none. It makes both gases in the culture, only as fast as we choose to make them.

- **Electricity splits water.** Hydrogen forms on the stainless steel cathode. Oxygen forms on the hollow titanium anode, which has a mixed metal oxide (MMO) coating.
- **CO₂ comes from a SodaStream cylinder.** It flows down the hollow anode in short, timed bursts. It is the bacteria’s carbon source, and it flushes out excess oxygen.
- **The Pioreactor does the rest.** It stirs and heats the culture, measures growth by shining infrared light through it, and pumps fresh nutrient liquid in and culture out.
- **One silicone septum seals the vial.** Bacteria go in by syringe needle, and samples can be drawn mid-run, maintaining sterility. Two needles let unused gas escape, so pressure cannot build up.
- **The electroPioreactor plugin runs it.** This software on the Pioreactor times the electrolysis and the CO₂, and pauses the growth readings so bubbles do not spoil them.

The [3D model on the home page](/) names each part when you hover over it, and its Tour walks through them in order.

## What we have learned

Three things took us a while to learn, and each one shaped the design.

- **The medium is also the electrolyte.** Most HOB media contain chloride, which electrolysis turns into bleach. Ours is chloride-free. See [Research](/research/#the-medium).
- **Anodes matter more than cathodes.** We started with platinum-plated titanium and moved to MMO, which gives the same current at a lower voltage. The cathode is plain stainless steel.
- **The CO₂ valve has to vent.** A normal solenoid valve traps CO₂ in the line when it closes. The CO₂ dissolves, and the vacuum it leaves sucks culture back up the tube. Eli Silver at Brown University diagnosed this, and a venting valve fixes it.

## Two versions

- **The Aseptic electroPioreactor (AEP)** keeps a single strain free of contamination, with filters on every gas path, a septum-sealed cap and parts that can be autoclaved. The current version, AEP0.2, holds 30 ml of culture.
- **The Mixed-culture electroPioreactor (MEP)** is a lower-cost version for mixed cultures, such as bacteria enriched from soil or water, and for student projects.
