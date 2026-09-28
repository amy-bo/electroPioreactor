---
id: step-15-set-up-co2-flow-test
order: 15
title: "Set up the CO₂ flow test"
guide: [aep]
parts:
  - {component: co2-regulator, qty: 1, cat: prev}
  - {component: luer-lock-cap, qty: 1, cat: prev}
  - {component: silicone-tubing, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: one-bar
    question: "What does the regulator's outlet gauge read?"
    options:
      - {label: "About 1 bar", correct: true}
      - {label: "Well under 1 bar", fix: "Screw the regulator in until it reads 1 bar, before touching the needle valve."}
      - {label: "Well over 1 bar", fix: "Turn the regulator anti-clockwise until it reads 1 bar, before touching the needle valve."}
  - id: gas-at-vent
    question: "While sparging, where does the gas leave the vial?"
    options:
      - {label: "Only through the open outlet, into the measuring cylinder", correct: true}
      - {label: "Through both outlets: neither is capped", fix: "Cap one gas outlet with a luer lock cap, or the measuring cylinder catches only part of the flow."}
      - {label: "Nowhere: nothing leaves the open outlet", fix: "Check the job is sparging (or the relay is on) and the needle valve is open."}
---

<!-- from video: session-21 0:45:37-0:47:14 - this calibration was described, not performed (no scales in the room) -->

Set up and check the test here; [Calibrate CO₂ flow](step-16-calibrate-co2-flow.md), next, measures and adjusts the flow. A wrong regulator pressure found after that would mean measuring again.

1. Set the regulator to 1 bar.
2. Cap one of the two gas outlets with a luer lock cap.
3. Run 1/16" tubing from the open gas outlet into a water bath, under a measuring cylinder full of water.
4. Start the **electroPioreactor** job, or turn on the relay in the Pioreactor UI.
5. Sparge until the water's CO₂ concentration has equilibrated (assumed, or measured if you can).

<!-- VIDEO CUT: session-21 - cut after the water has equilibrated (item 5), before the measuring cylinder is timed; Calibrate CO₂ flow starts there. -->
