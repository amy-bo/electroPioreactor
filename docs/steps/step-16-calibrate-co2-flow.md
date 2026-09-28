---
id: step-16-calibrate-co2-flow
order: 16
title: "Calibrate CO₂ flow"
guide: [aep]
parts:
  - {component: co2-needle-valve, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: target-flow
    question: "How does the measured flow rate compare with your target?"
    options:
      - {label: "On target, within your tolerance", correct: true}
      - {label: "Above target, beyond your tolerance", fix: "Close the needle valve a little (clockwise), and repeat the measurement until it matches."}
      - {label: "Below target, beyond your tolerance", fix: "Open the needle valve a little (anti-clockwise), and repeat the measurement until it matches."}
---

<!-- from video: session-21 0:45:37-0:47:14 - this calibration was described, not performed (no scales in the room) -->

The regulator was checked at 1 bar in [Set up the CO₂ flow test](step-15-set-up-co2-flow-test.md).

1. Record how long the CO₂ takes to fill the measuring cylinder.
2. Calculate the flow rate.
3. Adjust the needle valve, and repeat until you reach the target flow rate.

<details>
<summary>Shutting the gas off after a session</summary>

1. Turn the regulator anti-clockwise until its screw hangs loose: it is then fully off.
2. Close the adapter's pin.
3. Turn the solenoid override to 1 to vent the line to zero, then back to 0.

<!-- from video: session-21 0:47:14-0:48:15 - shown on camera; "back to 0" is not heard in the transcript but the safety text requires the override closed -->

</details>
