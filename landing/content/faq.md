---
title: Frequently asked questions
description: Short answers on safety, cost, building, what you can grow, sterility, the AEP and MEP versions, software and getting help.
section: learn
audience: everyone
order: 30
---
Short answers to the questions newcomers and buyers ask most. Each answer links to the page or file with the detail. Terms in **bold** are explained in the [Glossary](/glossary/).

## The basics

### What is the electroPioreactor?

A [Pioreactor](https://pioreactor.com), an open, low-cost bench-top bioreactor, adapted to make hydrogen and oxygen inside the culture by **electrolysis** and to feed it carbon dioxide (CO₂). It is built to grow hydrogen-oxidising bacteria (**HOB**), microbes that live on those three gases. [AMYBO](https://amybo.org) created it to make HOB production affordable, safe and local, as a sustainable alternative protein. See [What are HOB?](/what-is-hob/) and [How it works](/how-it-works/). <!-- source: README.md -->

### What is the difference between the AEP and the MEP?

- The **Aseptic electroPioreactor (AEP)** is for single-strain (monoculture) research. It adds filters on every gas path, a septum-sealed cap and autoclavable parts, so nothing else gets in. The current version, AEP0.2, uses the Pioreactor 40 ml with the XR optics upgrade and about 30 ml of culture. <!-- source: AsepticElectroPioreactor/README.md; docs/steps/step-00-before-you-start.md (What changed) -->
- The **Mixed-culture electroPioreactor (MEP)** is a lower-cost version for mixed cultures, such as communities enriched from the environment, and for student projects. It uses the Pioreactor 20 ml, an O-ring vial cap and a platinum-plated titanium anode. <!-- source: MixedElectroPioreactor/README.md; docs/README.md (MEP and BAEP steps) -->
- A **budget aseptic** version (BAEP) is an MEP with the AEP's five vent filters added. <!-- source: docs/README.md -->

See [Variants](/variants/).

### Is it open source?

Yes. The designs, bill of materials, assembly guides, media recipes and the gas model are published in the [electroPioreactor repository](https://github.com/amy-bo/electroPioreactor), also mirrored on [Radicle](https://app.radicle.xyz/nodes/iris.radicle.xyz/rad%3AzY4GuyErQo91xGYdLi4r2bea9QDJ). The plugin is MIT-licensed. See [Open source](/open-source/). <!-- source: README.md; AEP-Plugin/setup.py (license="MIT") --> <!-- CHECK: the repo root has no LICENSE file; only the plugin's licence (MIT) is confirmed. Do not state a licence for the hardware designs until one is added -->

## Safety

### Is it safe?

Safety is the first of the AEP's design criteria. The main hazards are handled like this: <!-- source: AsepticElectroPioreactor/README.md (Design criteria) -->

- **Hydrogen.** None is stored. Electrolysis makes hydrogen and oxygen a little at a time, inside the culture, as the bacteria need them. Each CO₂ burst sweeps oxygen out of the vial, and the CO₂ rate is set with hydrogen combustion risk in mind. <!-- source: AsepticElectroPioreactor/README.md; Media/MediaFormulation.md (Macronutrients) -->
- **Electricity.** The electrodes run at a few volts from the Pioreactor's supply, and the plugin limits electrolysis to 10 % of the channel's power. <!-- source: AEP-Plugin/README.md; docs/steps/step-08-test-electrolysis.md -->
- **The CO₂ cylinder.** It is under high pressure (about 60 bar when full). The build guide requires eye protection and cryogenic gloves for the cylinder joint, and a venting (3-way) solenoid valve. <!-- source: docs/glossary.yaml (regulator); docs/steps/step-12-co2-gas-train.md (safety) -->
- **Microbes.** Work with them under your institution's biosafety rules.

> **Safety:** Follow the safety notes in each step of the [build guide](https://docs.electropioreactor.org/AEP/), and any extra PPE or procedures your supervisor, department or health and safety advisor requires. <!-- source: docs/steps/step-00-before-you-start.md (Tool notes) -->

### Can I eat what it grows?

No. The electroPioreactor is laboratory research equipment, not a food production device. It has not been designed, tested or approved to make food, and nothing grown in it should be eaten.

HOB protein for food and feed is an active research field, and reviews describe HOB as a possible novel protein source. Turning that into safe food needs food-grade processes, safety testing and regulatory approval, none of which this project provides. <!-- source: Literature bib: Angenent et al. 2022, doi 10.2174/18742858-v16-e2207270 -->

## Getting one

### Where do I get one, and what does it cost?

LabCrafter sells AEP kits in the UK. Pioreactor sells the base Pioreactor worldwide. A LabCrafter kit lacks only the SodaStream CO₂ cylinders, two 250 ml GL45 screw-cap lab bottles, the nutrient solution and your bacteria. You can also buy the parts yourself from the bill of materials. Prices are not published here: ask [LabCrafter](https://labcrafter.co.uk) or [Pioreactor](https://pioreactor.com) for a quote. See [Get one](/get-one/) for the options. <!-- source: AsepticElectroPioreactor/README.md; docs/steps/step-00-before-you-start.md -->

### How long does it take to build?

The [build guide](https://docs.electropioreactor.org/AEP/) has a "Before you start" page and 17 steps, from connecting the base platforms to calibrating the CO₂ flow and sterilising. In the first joint training, in November 2025, three students each assembled and calibrated an earlier version (AEP0.1) over a four-day session that also covered media and first cultures. <!-- source: docs/steps/; AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md --> <!-- CHECK: no build time for AEP0.2 is stated in the repo; the 4-day figure is the whole training, not assembly alone -->

### Do I need a lab?

For the AEP, yes in practice. Aseptic single-strain work needs sterile technique, a way to sterilise parts and media, and somewhere you are allowed to handle bacteria. You also need a CO₂ cylinder, a balance that reads to 0.1 g (a jewellery scale will do) and basic tools. <!-- source: docs/steps/step-00-before-you-start.md (Tools) -->

The MEP is simpler and cheaper, and the project has published methods for enriching HOB from natural samples such as fen and river water. Check what your local rules allow before growing microbes anywhere. <!-- source: Methodologies/Crymlyn.md; Methodologies/Irvine/Medium.md -->

### Can I use a Pioreactor I already have?

Probably, with some parts added. The plugin works on any Pioreactor fitted with an electrode pair on an LED channel and a CO₂ valve on a PWM (pulse-width modulation) channel, one of the Pioreactor's switched power outputs. AEP0.2 is designed around the Pioreactor 40 ml v1.5 with the XR upgrade kit; the MEP uses the Pioreactor 20 ml v1.1. The build guide has a "Custom build" option. <!-- source: AEP-Plugin/README.md; docs/README.md; docsandeye.config.yaml (profile options) -->

## Running it

### What can I grow?

HOB, either a single strain in the AEP or a mixed community in the MEP. Organisms in this project's work include *Cupriavidus metallidurans* (grown at the first training) and *Xanthobacter tagetidis* (the gas model's baseline). *Cupriavidus necator* is the best-studied HOB in the literature. Check a new culture grows well on sugars (heterotrophically) before putting it in the reactor. See [What are HOB?](/what-is-hob/). <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md; Media/electroPioreactorGasModel.py; docs/steps/step-00-before-you-start.md -->

> **Note:** Growing HOB on gases alone is harder than on sugar. In the first training, a culture grew well on sugar, but the first attempt to grow it on gases alone showed no growth; the team listed the likely causes and next steps. Results are published as they come in. See [Research](/research/). <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md (Autotrophic culture) -->

### What does the culture grow in?

A mineral medium that also serves as the electrolyte. It is based on Sydow et al. (2017)'s medium and avoids chlorides and other salts that electrolysis would turn into chlorine or ammonia. The current recommendation is AM003. See [Media](/media/). <!-- source: Media/README.md -->

### Where does the CO₂ come from?

A standard SodaStream cylinder (blue, screw-in), through a regulator, an electric valve and a needle valve. <!-- source: docs/steps/step-00-before-you-start.md; docs/glossary.yaml -->

### Is it sterile?

The AEP is designed to keep a single strain free of contamination: 0.2 µm vent filters on every gas path, one septum sealing the vial and every port, inoculation by syringe through the septum, and autoclavable parts. The AEP0.2 sterilisation procedure is still awaiting approval by the project's principal investigators; see the [Sterilise step](https://docs.electropioreactor.org/AEP/step-17-sterilise/). The MEP is designed for mixed cultures, not aseptic work. <!-- source: AsepticElectroPioreactor/README.md; docs/steps/step-17-sterilise.md; MixedElectroPioreactor/README.md -->

### How is growth measured?

By **optical density (OD)**: how cloudy the culture is. An infrared LED shines through the vial, and photodiodes read the light scattered at 45°, 90° and 135°, plus a reference. The plugin pauses OD readings around each CO₂ burst, and during electrolysis when it runs in on/off cycles, because bubbles scatter light too. You can calibrate OD against your own samples. <!-- source: Components/Vial Cap/render/callouts.mjs (pd, led); AEP-Plugin/README.md; MixedElectroPioreactor/Calibration.md -->

### Does it run on its own?

Yes, once set up. The Pioreactor stirs, heats, reads OD and doses fresh medium (for example as a **turbidostat**), and the plugin runs electrolysis and CO₂ on schedules you set. You watch and change settings from a web browser. <!-- source: AsepticElectroPioreactor/README.md (Automated); AEP-Plugin/README.md -->

### Do I need to know how to code?

No. Running experiments is done from the Pioreactor's web interface. Installing the plugin currently means pasting two given commands into a terminal; a route with no commands at all, copying files onto the Pioreactor's memory card before first boot, is ready for when Pioreactor's operating system supports it. <!-- CHECK: AEP-Plugin/README.md says the card route needs a Pioreactor OS release with boot-partition plugin support, 'accepted by Pioreactor; until it ships, use the SSH route'. Update when it ships --> If your lab Wi-Fi will not accept new devices, the Pioreactor can make its own Wi-Fi network. See [Software](/software/) and the [install step](https://docs.electropioreactor.org/AEP/step-06-install-electropioreactor-plugin/). <!-- source: AEP-Plugin/README.md (Installation) -->

### How much does it produce?

Very little: it is a 30 ml research vessel for studying growth, media and conditions, not a production plant. Its purpose is reproducible experiments that inform larger systems. <!-- source: Components/Vial Cap/render/callouts.mjs (30 ml); AsepticElectroPioreactor/README.md -->

## Help and contact

### How do I get help?

- Ask on the [AMYBO forum](https://forum.amybo.org).
- Read the [build guide](https://docs.electropioreactor.org/AEP/); each step has checks with fixes for common mistakes.
- Report a problem or suggest a change on [GitHub](https://github.com/amy-bo/electroPioreactor).
- For Pioreactor hardware and software, see [Pioreactor's documentation](https://docs.pioreactor.com).
- Email [hello@amybo.org](mailto:hello@amybo.org).

See [About](/about/).

### Who is behind it?

[AMYBO](https://amybo.org) designs it. The Aseptic version is funded by CARMA Hub Pump Priming, with Imperial College London and the University of Edinburgh leading the research. See [About](/about/). <!-- source: README.md; AsepticElectroPioreactor/README.md -->
