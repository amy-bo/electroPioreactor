---
title: Get or build one
description: How to buy the parts, print the custom pieces, assemble an electroPioreactor with the video guide, and get help.
section: build
audience: everyone
order: 20
---
You build an electroPioreactor yourself, from a Pioreactor bioreactor plus a kit of electrodes, a printed vial cap and a CO₂ gas train. A step-by-step video guide takes you through the whole assembly. This page tells you what to buy, what you need to hand and where to get help.

> **Tip:** The assembly itself is in the **[Assembly Video Guide](https://docs.electropioreactor.org/AEP/)**. Each step has a short video, a parts list, checks and photographs. Start at [Before you start](https://docs.electropioreactor.org/AEP/step-00-before-you-start/), which asks which model you are building and how many units, and then shows a checklist of every part you should have received.

Not sure which model? See [Which electroPioreactor?](/variants/) first. The rest of this page is about the Aseptic electroPioreactor (AEP) AEP0.2. The Mixed-culture (MEP) and Budget aseptic (BAEP) builds follow the same pattern, with their own guides at [/MEP/](https://docs.electropioreactor.org/MEP/) and [/BAEP/](https://docs.electropioreactor.org/BAEP/).

## 1. Buy the parts

**The Pioreactor.** The electroPioreactor is built on the open-source [Pioreactor](https://pioreactor.com). In the UK it is supplied by [LabCrafter](https://labcrafter.co.uk); in the rest of the world, by [Pioreactor](https://pioreactor.com). An AEP0.2 uses the [Pioreactor 40 ml v1.5](https://labcrafter.co.uk/products/pioreactor-40ml-v1-5) with the [XR upgrade kit](https://labcrafter.co.uk/products/pioreactor-40ml-v1-5-xr-upgrade-kit). <!-- source: AsepticElectroPioreactor/README.md; docs/components/pioreactor-40ml.yaml; docs/components/xr-upgrade-kit.yaml -->

**The electroPioreactor kit.** You have three routes, and the guide asks which one you took so it can show the right parts checklist: <!-- source: docsandeye.config.yaml (profile: supplier) -->

| Route | What you get |
|---|---|
| **LabCrafter kit** (UK) | The Pioreactor, XR and Precision Temperature Upgrade Kits, Raspberry Pi, peristaltic pumps, printed parts, electrodes, needles, vent filters, tubing and the CO₂ gas train. The vial cap arrives printed, with its septum seated and the electrode cables attached. |
| **Pioreactor** (outside the UK) | The Pioreactor, XR and Precision Temperature Upgrade Kits, Raspberry Pi and power supply, microSD card, peristaltic pumps and GL45 bottle caps. Source the electroPioreactor-specific parts yourself from the parts list. |
| **Self-sourced** | Everything from the parts list. |

<!-- source: docs/steps/step-00-before-you-start.md; docs/components/vial-cap.yaml (receipt note) -->

A LabCrafter kit does not include regional consumables. Buy these locally: <!-- source: docs/steps/step-00-before-you-start.md -->

- SodaStream blue screw-in CO₂ cylinders (not the pink quick-connect type)
- two 250 ml GL45 "Duran" glass bottles, one for fresh medium and one for product
- nutrient solution: see [Media](/media/)
- an inoculum: a culture of the hydrogen-oxidising bacteria (HOB) you want to grow, checked first to grow well on ordinary food (heterotrophically)

**The parts list.** The AEP0.2 bill of materials (BoM) is built into the guide: every part has its own page with its specification and supplier, and each step lists the parts it uses. The source is one file per part in [docs/components/](repo:docs/components/). A few specifications are still open and are listed in [AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md). <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md -->

> **Note:** The repository does not publish prices. Ask [LabCrafter](https://labcrafter.co.uk) or [Pioreactor](https://pioreactor.com) for a quote, or price the parts list from each part's supplier link.

**Spares.** Buy spare 40 ml glass vials and 15 × 6 mm PTFE magnetic stir bars (Pioreactor SKU 2046), at least one of each for a few units, and more if your floor is hard or your sink has no fine strainer. A spare silicone septum is worth having too, because each needle track wears it a little. <!-- source: docs/steps/step-00-before-you-start.md (How many spares should I buy?); docs/components/stir-bar.yaml -->

## 2. Printed parts

If you are not buying a LabCrafter kit, you print these yourself. <!-- source: docs/components/*.yaml (kind: printed) -->

| Part | Source | Print notes |
|---|---|---|
| Vial cap and electrode holder | [Components/Vial Cap/](repo:Components/Vial%20Cap/) (OpenSCAD source and STL) | PC-CF (carbon-fibre polycarbonate), 100% infill, 0.16 mm layers |
| Pumping dovetail platform (one Pioreactor platform, two pump holders) | [Printables model 679663](https://www.printables.com/model/679663) | PLA or PETG, 0.2 mm layers, about 20% infill |
| Dovetail holders for the GL45 bottles | [Components/GL45BottleHolder/](repo:Components/GL45BottleHolder/) (based on Printables model 1058356) | Sized for 250 ml bottles |
| Dovetail holder for the CO₂ cylinder | [Printables model 855700](https://www.printables.com/model/855700-sodastream-holder-for-pioreactor) | Community model |

<!-- CHECK: the Printables 679663 URL is built from the model number only (docs/components/pumping-dovetail-platform.yaml gives no URL); confirm it resolves -->

The custom designs are parametric OpenSCAD files, so you can change sizes. See [Components/](repo:Components/) and [Specifications](/specifications/).

## 3. Tools and safety kit

<!-- source: docs/steps/step-00-before-you-start.md (tools, Tool notes) -->

**Required**

- a computer with a microSD reader (or an SD reader and a microSD adapter) and Raspberry Pi Imager, to set up the Pioreactor's card
- a Phillips PH0 screwdriver
- a 28 mm gas cylinder wrench
- vernier callipers
- a balance reading to 0.1 g, for pump calibration (a jewellery scale will do)
- cryogenic gloves safe to at least −80 °C, eye or face protection and a lab coat, plus any other personal protective equipment (PPE) your supervisor, department or health and safety adviser requires

**Recommended**

- needle-nose pliers or a multitool, for assembly and tubing
- a multimeter, for checking electrolysis
- a banded oil filter wrench, only if the CO₂ cylinder is hard to tighten

> **Safety:** Electrolysis makes hydrogen, which is explosive in air at 4 to 75% by volume, and CO₂ is an asphyxiant at high concentrations. Work in a well-ventilated room, keep ignition sources away and never seal the vial's headspace. Fitting a CO₂ cylinder can release very cold gas: wear the cryogenic gloves and eye protection. <!-- source: Methodologies/Irvine/Enrichment.md (Safety note); docs/steps/step-00-before-you-start.md (checks) -->

## 4. Time and skills

The guide does not give a total build time. Plan for at least two sessions: the Loctite 577 thread sealant on the gas train needs 10 to 60 minutes before gas can go in, and 24 hours to reach its full pressure rating. <!-- source: docs/steps/step-12-co2-gas-train.md -->

You do not need to be an engineer. You will:

- flash a microSD card and use a web browser to set up the Pioreactor
- use small hand tools and make up threaded gas joints
- handle a pressurised CO₂ cylinder safely
- calibrate pumps by weighing water, and measure a gas flow
- use basic sterile technique, for the aseptic AEP

The guide checks your work as you go: each step ends with a short question about what you can see, and every wrong answer comes with its fix. <!-- source: docs/README.md (Step checks) -->

## 5. Assemble

Follow the [AEP guide](https://docs.electropioreactor.org/AEP/) in order. In outline: <!-- source: site/dist/AEP/ (step slugs) -->

1. [Before you start](https://docs.electropioreactor.org/AEP/step-00-before-you-start/): count the parts and gather the tools
2. [Connect the dovetail platforms](https://docs.electropioreactor.org/AEP/step-01-connect-dovetail-platforms/) and [press the raft together](https://docs.electropioreactor.org/AEP/step-02-press-the-raft-together/)
3. [Raspberry Pi and HAT](https://docs.electropioreactor.org/AEP/step-03-raspberry-pi-and-hat/), [vial holder and XR](https://docs.electropioreactor.org/AEP/step-04-vial-holder-and-xr/)
4. [Pioreactor software setup](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) and [install the electroPioreactor plugin](https://docs.electropioreactor.org/AEP/step-06-install-electropioreactor-plugin/)
5. [Set up](https://docs.electropioreactor.org/AEP/step-07-set-up-electrolysis/) and [test electrolysis](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/)
6. [Nutrient solution flow](https://docs.electropioreactor.org/AEP/step-09-set-up-nutrient-solution-flow/), [calibrate the pumps](https://docs.electropioreactor.org/AEP/step-10-calibrate-pumps/) and fit the [ports](https://docs.electropioreactor.org/AEP/step-11-ports/)
7. [CO₂ gas train](https://docs.electropioreactor.org/AEP/step-12-co2-gas-train/) and [admit CO₂](https://docs.electropioreactor.org/AEP/step-13-admit-co2/)
8. [Configure sparging and electrolysis](https://docs.electropioreactor.org/AEP/step-14-configure-sparging-and-electrolysis/), then [set up](https://docs.electropioreactor.org/AEP/step-15-set-up-co2-flow-test/) and [calibrate the CO₂ flow](https://docs.electropioreactor.org/AEP/step-16-calibrate-co2-flow/)
9. [Sterilise](https://docs.electropioreactor.org/AEP/step-17-sterilise/)

The Pioreactor's own setup is covered by [Pioreactor's documentation](https://docs.pioreactor.com); the guide tells you where the electroPioreactor differs. If your build site has no network at all, the plugin can be installed from the microSD card: see [AEP-Plugin/README.md](repo:AEP-Plugin/README.md) and [Software](/software/).

## 6. Sterilise

The AEP0.2 sterilisation procedure is awaiting approval by the project's principal investigators, so the guide's [Sterilise](https://docs.electropioreactor.org/AEP/step-17-sterilise/) step is a placeholder for now. Follow your own institution's procedures until it is published. Several parts, including the GL45 caps and the silicone tubing, are rated autoclavable. <!-- source: docs/steps/step-17-sterilise.md; docs/components/gl45-cap.yaml; docs/components/silicone-tubing.yaml -->

## 7. First run

Once built and calibrated, the unit is run from the Pioreactor web interface. The electroPioreactor plugin runs electrolysis, CO₂ sparging and pauses in optical density (OD) reading as one job, with its settings editable live. <!-- source: AEP-Plugin/README.md -->

- [AEP protocol](https://docs.electropioreactor.org/AEP/protocol/): running an experiment (being written up; until then the plugin README covers starting the job and its settings)
- [MEP protocol](https://docs.electropioreactor.org/MEP/protocol/): calibration and operation for the MEP and BAEP
- [Methodologies/](repo:Methodologies/): worked protocols for enriching HOB from environmental samples
- [Media](/media/) and the [gas model](/gas-model/): what to feed the culture and how much gas it gets

## Getting help

- **A part is missing from your kit:** the guide's parts checklist has a "Missing something?" line that emails your supplier. <!-- source: docsandeye.config.yaml (contacts) -->
- **Questions about a step, or anything else:** ask on the [AMYBO forum](https://forum.amybo.org) or email [hello@amybo.org](mailto:hello@amybo.org).
- **Pioreactor hardware and software:** [Pioreactor's documentation](https://docs.pioreactor.com) and [forum](https://forum.pioreactor.com).
- **Found a mistake?** Open an issue on [GitHub](https://github.com/amy-bo/electroPioreactor/issues). See [Open source](/open-source/).

Common questions are answered in the [FAQ](/faq/), and terms are explained in the [Glossary](/glossary/).
