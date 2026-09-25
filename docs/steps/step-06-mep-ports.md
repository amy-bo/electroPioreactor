---
id: step-06-mep-ports
order: 6
title: "Ports"
guide: [mep, baep]
parts:
  - {component: flexelene-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 3, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: vial-cap-oring, qty: 1, cat: prev}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: five-tubes
    question: "Are all five ports filled: Media In, Media Out and CO₂ In reaching into the vial, the two gas outlets above the liquid?"
    issues:
      - {problem: "A gas outlet dips into the liquid", fix: "Pull it up until it is clear of the liquid at 14 ml, or culture will be pushed out through it."}
  - id: co2-deep
    question: "Does the CO₂ In tube end near the base of the vial, clear of the stir bar?"
    issues:
      - {problem: "It fouls the stir bar", fix: "Pull it up until the stir bar spins freely."}
---

The cap has seven openings: the electrodes fill two, and a tube goes through each of the five 3.2 mm ports.

- Media In
- Media Out: sets the liquid level
- CO₂ In: the sparge tube
- Gas Out
- Gas Out – safety

1. Cut five lengths of Flexelene tubing, and push one through each port from the top.
2. Push Media In down until it is below the liquid level.
3. Push Media Out down to the 14 ml level. It is fine-tuned in **Nutrient solution**.
4. Push CO₂ In down to near the base of the vial, clear of the stir bar.
5. Leave both gas outlets just below the cap, above the liquid.
6. Fit a female luer to the top of Media In, Media Out and CO₂ In, and a male luer to each gas outlet, so outlets are marked as outlets.
7. Leave the gas outlet luers free: you inoculate and sample through one with a syringe.

<!-- TODO: confirm the MEP port tubing (Flexelene 135C as on AEP0.1.1?), its lengths, and which luer goes on each port | assignee: @Martin -->
