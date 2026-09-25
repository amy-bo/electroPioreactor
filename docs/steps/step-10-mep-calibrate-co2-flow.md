---
id: step-10-mep-calibrate-co2-flow
order: 10
title: "Calibrate CO₂ flow"
guide: [mep, baep]
parts:
  - {component: luer-lock-cap, qty: 1, cat: part}
  - {component: silicone-tubing, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: target-reached
    question: "Did you reach your target flow within sensible needle valve travel?"
    issues:
      - {problem: "The needle valve drifts", fix: "Needle valve creep: re-measure after a few sparges and adjust."}
      - {problem: "Flow is low whatever the setting", fix: "Look for a kinked line, then a leak at a Loctite 577 joint: pipette washing-up liquid in water onto each joint and watch for bubbles."}
---

The FZone regulator's outlet pressure is fixed, so the needle valve alone sets the flow. Aim for the flow of an AEP0.1.1 at 1 bar, so experiments port across. BAEP: fit the vent filters first; they change the flow.

1. Check the cylinder is open: the adapter's pin screw is fully down.
2. Cap one of the two gas outlets with a luer lock cap.
3. Run 1/16" tubing from the open gas outlet into a water bath, under a measuring cylinder full of water.
4. Open the solenoid: turn on the relay in the Pioreactor UI, or run sparges from the **electroPioreactor** job.
5. Sparge until the water is saturated with CO₂ (when its pH stops falling, if you can measure it), then open the solenoid for a fixed time.
6. Record the volume of CO₂ collected.
7. Calculate the flow rate, in ml of CO₂ per second of solenoid open time.
8. Adjust the needle valve, and repeat until you reach the target flow rate.
9. Record the needle valve setting, in turns from fully closed.

<details>
<summary>Shutting the gas off after a session</summary>

1. Close the cylinder: unscrew the adapter's pin screw.
2. Turn the solenoid override to 1 to vent the line to zero, then back to 0.

</details>
