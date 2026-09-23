---
id: step-00-before-you-start
order: 0
title: "Before you start"
guide: [aep]
parts:
  - {component: spare-vial, qty: 1, cat: consumable}
  - {component: spare-magnetic-flea, qty: 1, cat: consumable}
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
profile: true
checks_draft: true
checks:
  - id: parts-counted
    question: "Does every row of the parts checklist on this page match what you received?"
    issues:
      - {problem: "A part is short or missing", fix: "Use the Missing parts panel under the checklist to email whoever you bought from; it lists each part and how many are missing."}
      - {problem: "The SodaStream cylinders or the 250 ml GL45 bottles are missing from a LabCrafter kit", fix: "These are regional consumables that LabCrafter does not supply: buy them locally (see the links in item 1 above)."}
  - id: tools-to-hand
    question: "Do you have every Required Tool to hand, including PPE?"
    issues:
      - {problem: "The analytical balance is not accurate enough", fix: "Pioreactor's pump calibration only requires 0.1 g accuracy."}
      - {problem: "A required tool is missing", fix: "Source it before starting: the Required Tools are needed in the steps that list them, and the cryogenic gloves and eye/face protection are needed before the CO₂ cylinder joint is made."}
---

> Parts list: the [components](../components/) of this guide. AEP0.1.1 instructions are archived in [AEP0.1.1_Assembly.md](../../AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md).

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

## Before you start

1. Procure the [Bill of Materials](../components/) ([LabCrafter](https://labcrafter.co.uk) can supply a kit that is only missing the required [SodaStream blue screw in cylinders](https://sodastream.co.uk/products/refill), two [250ml GL45 "Duran" Flasks](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate), [nutrient solution](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and inoculum)
2. Check your HOB are growing happily heterotrophically.

<!-- TODO: these tool lists duplicate the tools: block in this step's frontmatter - decide which is canonical before the renderer is written, or the two will drift | assignee: @Martin -->

## Required Tools

1. Computer with microSD card reader (or SD card reader and microSD to SD adapter)
2. Phillips PH0 Screwdriver
3. 28mm Gas cylinder wrench
4. Vernier Callipers
5. Analytical balance for pump calibration (Pioreactor docs only require 0.1g accuracy)
6. Cryogenic gloves (safe to at least -80°C)
7. Eye/face protection
8. Lab coat
9. Other PPE as directed by your supervisor/department/employer/H&S advisor

## Recommended Tools

1. Multitool and/or needle nose pliers (for general assembly and tubing adjustment)
2. Multimeter (for checking electrolysis)
3. Banded oil filter wrench (optional - if you struggle with CO2 canister tightening)

## Spares

Carry boxed spares of the fragile and consumable items — at minimum a spare vial and a spare magnetic flea per few units. A vial was dropped and smashed during the AEP0.1 training.
