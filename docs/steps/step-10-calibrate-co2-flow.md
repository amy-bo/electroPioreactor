---
id: step-10-calibrate-co2-flow
order: 10
title: "Calibrate CO₂ flow"
guide: [aep]
parts:
  - {component: co2-regulator, qty: 1, cat: prev}
  - {component: co2-needle-valve, qty: 1, cat: prev}
  - {component: luer-lock-cap, qty: 1, cat: prev}
  - {component: silicone-tubing, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: one-bar
    question: "Is the regulator set to 1 bar?"
    issues:
      - {problem: "It reads more or less", fix: "Adjust the regulator to 1 bar before touching the needle valve."}
  - id: gas-at-vent
    question: "While sparging, with one gas outlet capped, does gas leave the other?"
    issues:
      - {problem: "No gas leaves the open outlet", fix: "Check the job is sparging (or the relay is on) and the needle valve is open."}
  - id: target-flow
    question: "Does the measured flow rate match your target?"
    issues:
      - {problem: "It is off target", fix: "Adjust the needle valve, and repeat the measurement until it matches."}
---

<!-- from video: session-21 0:45:37-0:47:14 - this calibration was described, not performed (no scales in the room) -->

1. Set the regulator to 1 bar.
2. Cap one of the two gas outlets with a luer lock cap.
3. Run 1/16" tubing from the open gas outlet into a water bath, under a measuring cylinder full of water.
4. Start the **electroPioreactor** job, or turn on the relay in the Pioreactor UI.
5. Sparge until the water's CO₂ concentration has equilibrated (assumed, or measured if you can).
6. Record how long the CO₂ takes to fill the measuring cylinder.
7. Calculate the flow rate.
8. Adjust the needle valve, and repeat until you reach the target flow rate.

<details>
<summary>Shutting the gas off after a session</summary>

1. Turn the regulator anti-clockwise until its screw hangs loose: it is then fully off.
2. Close the adapter's pin.
3. Turn the solenoid override to 1 to vent the line to zero, then back to 0.

<!-- from video: session-21 0:47:14-0:48:15 - shown on camera; "back to 0" is not heard in the transcript but the safety text requires the override closed -->

</details>
