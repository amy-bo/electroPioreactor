---
id: step-00-mep-before-you-start
order: 0
title: "Before you start"
guide: [mep, baep]
tools:
  - {component: computer-with-microsd-reader, qty: 1}
  - {component: phillips-ph0-screwdriver, qty: 1}
  - {component: hex-key-2-5mm, qty: 1}
  - {component: hex-key-5mm, qty: 1}
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: vernier-callipers, qty: 1}
  - {component: analytical-balance, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: lab-coat, qty: 1}
  - {component: needle-nose-pliers, qty: 1}
  - {component: multimeter, qty: 1}
checks_draft: true
checks:
  - id: parts-to-hand
    question: "Do you have every part the steps of this guide list?"
    issues:
      - {problem: "A part is missing", fix: "Each step lists its parts. [Components/README.md](../../Components/README.md) links suppliers for most of them."}
  - id: tools-to-hand
    question: "Are the tools under **Tools** to hand, including cryogenic gloves and eye protection?"
    issues:
      - {problem: "No cryogenic gloves", fix: "Do not fit the CO₂ cylinder without them. Everything up to **CO₂ sparging** can go ahead."}
---

> The Mixed-culture electroPioreactor (MEP) is the lower-cost electroPioreactor for mixed cultures. Source documents: [MixedElectroPioreactor](../../MixedElectroPioreactor/).

1. Buy the parts each step of this guide lists, plus two [SodaStream blue screw-in cylinders](https://sodastream.co.uk/products/refill), two [250 ml GL45 "Duran" bottles](https://www.theconsumablescompany.com/250ml-reagent-bottle-borosilicate), [nutrient solution](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and inoculum.
2. Check your culture grows well.
3. Gather everything under **Tools**.

:::note[BAEP]
The Budget aseptic electroPioreactor (BAEP) is an MEP with five 0.2 μm vent filters on its gas and bottle vents. Its guide has the same steps, plus **Add the vent filters** at the end.
:::

<details>
<summary>Tool notes</summary>

- The computer needs a microSD reader, or an SD reader with a microSD adapter, and Raspberry Pi Imager to flash the card.
- The 2.5 mm hex key fits the ElectrodeTopStop's M3 bolts; the 5 mm hex key fits the blanking plug.
- The gas cylinder wrench is 28 mm.
- The analytical balance needs only 0.1 g accuracy, for pump calibration: a jewellery scale will do.
- The vernier callipers set the electrode depth.
- Cryogenic gloves must be safe to at least -80 °C.
- Add any other PPE your supervisor, department, employer or H&S advisor requires, and gloves for handling media.
- Recommended, not required: needle-nose pliers, for assembly and tubing; a multimeter, for checking electrolysis.

</details>

<details>
<summary>Spares</summary>

Keep spares: at least one vial and one magnetic stir bar per few units. Vials break.

</details>

<details>
<summary>How the MEP differs from the AEP0.2</summary>

| Area | AEP0.2 | MEP |
| --- | --- | --- |
| Culture | Single strain, aseptic | Mixed culture; the BAEP adds vent filters |
| Vessel | Pioreactor 40 ml v1.5 + XR upgrade kit, ~30 ml working volume | Pioreactor 20 ml v1.1, 14 ml working volume |
| Computer | RPi 5 1GB, 27 W USB-C supply | RPi Zero 2 W (or 4B), its own 5 V supply |
| Vial cap | One-piece cap and electrode holder, single silicone septum | [O-ring vial cap](../../Components/Vial%20Cap) + [ElectrodeTopStop](../../Components/ElectrodeTopStop), cap O-ring + 2 electrode O-rings |
| Electrodes | MMO tube anode and stainless steel cathode, 100 mm | Platinum-plated titanium anode and stainless steel cathode, 60 mm |
| Electrode fixing | Ring terminal + thumb screw, M3 nut and spring washer | M3 bolt through a captive nut in the ElectrodeTopStop |
| Ports | Stainless steel needles through the septum | Tubes through the cap's five 3.2 mm ports |
| CO₂ regulator | Adjustable, set to about 1 bar | FZone, fixed outlet pressure: the needle valve alone sets the flow |
| Pumps | PWM 2 media, PWM 3 waste | PWM 2 waste, PWM 3 media |
| Card bundle | AEP bundle: sets the model, adds the precision temperature plugin | MEP bundle: electroPioreactor plugin only |
| Not in the MEP | Precision Temperature Upgrade Kit; vent filters (see the BAEP) | |

</details>
