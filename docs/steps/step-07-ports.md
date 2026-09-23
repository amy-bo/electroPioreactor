---
id: step-07-ports
order: 7
title: "Ports"
guide: [aep]
parts:
  - {component: needle-port, qty: 4, cat: part}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: stainless-steel-cathode, qty: 1, cat: prev}
  - {component: vial-cap, qty: 1, cat: prev}
  - {component: silicone-septum, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: eight-ports
    question: "Can you identify all eight ports on the cap, with the spare port sealed?"
    issues:
      - {problem: "The spare port is open", fix: "Seal it: every unused opening is a route for contamination."}
  - id: four-needles
    question: "Are the four needle ports (Media In, Media Out, Gas Out and Gas Out – safety) through the septum?"
    issues:
      - {problem: "You have fewer than four needles", fix: "Each Pioreactor ships with four, and the BoM adds one more per unit: check the parts checklist in Before you start and use its Missing parts email if any are short."}
---

The AEP0.2 cap carries eight ports, all stainless steel needles rather than the Flexelene 135C tubing used in AEP0.1:

1. Anode and CO₂ In – 6mm
2. Cathode – 6mm
3. Media In
4. Media Out
5. Gas Out
6. Gas Out – safety
7. Inoculation (large) – syringe through the septum, no dedicated tube and no pinch slider
8. Spare port (sealed)
