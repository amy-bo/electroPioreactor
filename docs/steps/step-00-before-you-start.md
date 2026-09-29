---
id: step-00-before-you-start
order: 0
title: "Before you start"
media: [vid-01-preparation]
guide: [aep]
tools:
  - {component: computer-with-microsd-reader, qty: 1}
  - {component: phillips-ph0-screwdriver, qty: 1}
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: vernier-callipers, qty: 1}
  - {component: analytical-balance, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: lab-coat, qty: 1}
  - {component: needle-nose-pliers, qty: 1}
  - {component: multimeter, qty: 1}
  - {component: banded-oil-filter-wrench, qty: 1}
receipt: true
checks_draft: true
checks:
  - id: parts-counted
    question: "Checking the parts checklist on this page against the kit, what did you find?"
    options:
      - {label: "Every row ticked, nothing short", correct: true}
      - {label: "One or more rows short of a part", fix: "Email your supplier from the **Missing something?** line under the checklist."}
      - {label: "Only the SodaStream cylinders or GL45 bottles absent", fix: "LabCrafter does not supply these regional consumables. Buy them locally: links in item 1."}
  - id: tools-to-hand
    question: "Which items under **Tools** are not yet to hand?"
    options:
      - {label: "None: every tool and all the PPE", correct: true}
      - {label: "Only the analytical balance", fix: "Pump calibration needs only 0.1 g accuracy: a jewellery scale will do."}
      - {label: "The cryogenic gloves or eye protection", fix: "Get them before **CO₂ gas train**: you need both before making the CO₂ cylinder joint."}
      - {label: "Another tool on the list", fix: "Get it before the step that lists it."}
---

> Parts: the [components](../components/) of this guide. Archived AEP0.1.1 instructions: [AEP0.1.1_Assembly.md](../../AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md).

1. Buy the [Bill of Materials](../components/). A [LabCrafter](https://labcrafter.co.uk) kit lacks only the [SodaStream blue screw-in cylinders](https://sodastream.co.uk/products/refill), two [250 ml GL45 "Duran" bottles](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate), [nutrient solution](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and inoculum.
2. Check your HOB culture grows well heterotrophically.
3. Unpack the kit and tick off every part under **Count what you received**.
4. Gather everything under **Tools**.

:::note[AEP0.2 kits]
An AEP0.2 kit includes the XR upgrade kit and the Precision Temperature Upgrade Kit.
:::

<details>
<summary>Tool notes</summary>

- The computer needs a microSD reader, or an SD reader with a microSD adapter, and Raspberry Pi Imager to flash the card.
- The gas cylinder wrench is 28 mm.
- The analytical balance needs only 0.1 g accuracy, for pump calibration: a jewellery scale will do.
- Cryogenic gloves must be safe to at least -80 °C.
- Add any other PPE your supervisor, department, employer or H&S advisor requires.
- Recommended, not required:
  - a multitool or needle-nose pliers, for assembly and tubing;
  - a multimeter, for checking electrolysis;
  - a banded oil filter wrench, only if the CO₂ cylinder is hard to tighten.

<!-- from video: session-14 0:02:14 - Martin says the callipers were "much more necessary in previous versions ... for this version you hopefully don't need those"; the tools list still has them as required -->

</details>

<details>
<summary>How many spares should I buy?</summary>

Spares are not part of the per-unit kit. Buy spare [40 ml glass vials](https://pioreactor.com/products/40ml-glass-vial) and magnetic stir bars separately, at least one of each for a few units, and more if:

- you or your students are prone to dropping things: vials are glass;
- your lab floor is hard: a dropped vial rarely survives tiles or concrete;
- your sink has no fine mesh strainer or steel drain cover: stir bars are small and slip down the drain when a vial is rinsed, and a steel cover holds them by their magnet.

A spare [silicone septum](../components/) is worth having too: each needle track wears it a little.

</details>

<details>
<summary>What changed from AEP0.1.1</summary>

| Area | AEP0.1.1 | AEP0.2 |
| --- | --- | --- |
| Vessel | Pioreactor 20 ml v1.1, ~15 ml working volume | Pioreactor 40 ml v1.5 + XR upgrade kit, ~30 ml working volume |
| Computer | RPi Zero 2W / RPi 4 4GB, micro-USB or USB-C supply | RPi 5 1GB, 27 W USB-C supply |
| Vial cap | Separate cap + [ElectrodeTopStop](../../Components/ElectrodeTopStop), cap o-ring + 2 electrode o-rings | One-piece [Vial Cap and electrode holder](../../Components/Vial%20Cap), single silicone septum |
| Anode | Platinised titanium rod, 100 mm | MMO (IrO₂-Ta₂O₅) tube, 100 mm, CO₂ delivered through its open base |
| Electrode fixing | M3 bolt through captive nut | Ring terminal + thumb screw, M3 nut and spring washer |
| Ports | Flexelene 135C tubing | Stainless steel needles |
| Gas sealing | PTFE tape on every threaded joint | O-rings where possible, Loctite 577 anaerobic thread sealant elsewhere |
| CO₂ inlet | Regulator tightened onto the cylinder against escaping gas | KegLand KL15578 pin-adjustment adapter: tighten first, then open the pin |
| Sparging control | `pioreactor-relay-plugin` + experiment profile YAML | [electroPioreactor plugin](../../AEP-Plugin) (electrolysis, sparging and OD pausing in one job) |
| Dropped | Bubble counter, pinch slider inoculation port, jubilee clips | Inoculation is now by syringe through the septum |

</details>
