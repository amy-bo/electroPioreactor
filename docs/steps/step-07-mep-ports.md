---
id: step-07-mep-ports
order: 7
title: "Ports"
guide: [mep, baep]
parts:
  - {component: silicone-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 3, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: vial-cap-oring, qty: 1, cat: prev}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: five-tubes
    question: "Where do the two gas outlet tubes end?"
    options:
      - {label: "Just below the cap, above the 14 ml level", correct: true}
      - {label: "Down in the liquid, below the 14 ml level", fix: "Pull it up until it is clear of the liquid at 14 ml, or culture will be pushed out through it."}
  - id: co2-deep
    question: "Where does the CO₂ In tube end?"
    options:
      - {label: "Near the base of the vial, clear of the stir bar", correct: true}
      - {label: "Near the base of the vial, touching the stir bar", fix: "Pull it up until the stir bar spins freely."}
      - {label: "Halfway down the vial, well above the stir bar", fix: "Push it down to near the base of the vial, clear of the stir bar."}
---

The cap has seven openings: the electrodes fill two, and a tube goes through each of the five 3.2 mm ports.

- Media In
- Media Out: sets the liquid level
- CO₂ In: the sparge tube
- Gas Out
- Gas Out – safety

1. Cut five lengths of tubing, and push one through each port from the top.
2. Push Media In down until it is below the liquid level.
3. Push Media Out down to the 14 ml level. It is fine-tuned in **Calibrate the pumps and set the level**.
4. Push CO₂ In down to near the base of the vial, clear of the stir bar.
5. Leave both gas outlets just below the cap, above the liquid.
6. Fit a female luer to the top of Media In, Media Out and CO₂ In, and a male luer to each gas outlet, so outlets are marked as outlets.
7. Leave the gas outlet luers free: you inoculate and sample through one with a syringe.

<!-- TODO: confirm the MEP port tubing lengths, and which luer goes on each port (the tubing is the AEP0.2 1/8" OD 1/16" ID tubing, no longer Flexelene, per Gerrit 2026-10-07) | assignee: @Martin -->
