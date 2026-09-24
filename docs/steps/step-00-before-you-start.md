---
id: step-00-before-you-start
order: 0
title: "Before you start"
media: [vid-01-preparation]
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

1. Procure the [Bill of Materials](../components/). A [LabCrafter](https://labcrafter.co.uk) kit lacks only the [SodaStream blue screw-in cylinders](https://sodastream.co.uk/products/refill), two [250ml GL45 "Duran" flasks](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate), [nutrient solution](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and inoculum.
2. Check your HOB are growing happily heterotrophically.
3. Unpack the kit and tick every part off the checklist on this page.
4. Gather the tools and PPE listed on this page.

<details>
<summary>Notes on the tools</summary>

- Required: the computer needs a microSD reader (or an SD reader and a microSD-to-SD adapter); the gas cylinder wrench is 28 mm; the analytical balance only needs 0.1 g accuracy for Pioreactor's pump calibration, so a jewellery scale will do; cryogenic gloves must be safe to at least -80°C; add any other PPE your supervisor, department, employer or H&S advisor directs.
- Recommended, not required: a multitool and/or needle-nose pliers (general assembly and tubing), a multimeter (checking electrolysis), and a banded oil filter wrench (only if you struggle to tighten the CO₂ cylinder).

<!-- from video: session-14 0:02:14 - Martin says the callipers were "much more necessary in previous versions ... for this version you hopefully don't need those"; the tools list still has them as required -->

</details>

<details>
<summary>Spares</summary>

Carry boxed spares of the fragile and consumable items: at minimum a spare vial and a spare magnetic flea per few units, and spare silicone septa. A vial was dropped and smashed during the AEP0.1 training.

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
