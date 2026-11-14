---
id: step-09-mep-calibrate-pumps
order: 9
title: "Calibrate the pumps and set the level"
guide: [mep, baep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: prev}
  - {component: gl45-bottle, qty: 2, cat: prev}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
  - {component: vial-cap-oring, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
checks_draft: true
checks:
  - id: pumps-calibrated
    question: "Which pumps have you calibrated?"
    options:
      - {label: "The waste pump and the media pump", correct: true}
      - {label: "The waste pump, not the media pump", fix: "Calibrate the media pump (PWM 3) too."}
      - {label: "The media pump, not the waste pump", fix: "Calibrate the waste pump (PWM 2) too."}
  - id: fourteen-ml
    question: "After running both pumps, what does the vial hold by weight?"
    options:
      - {label: "14 ml, the same as before the run", correct: true}
      - {label: "More than 14 ml: it has filled", fix: "Push the Media Out tube a little lower: it sets the level, and should be only just submerged at 14 ml."}
      - {label: "Less than 14 ml: it has drained", fix: "Pull the Media Out tube up a little: it sets the level, and should be only just submerged at 14 ml."}
---

The pump channels and the 12 V supply were checked in [Nutrient solution](step-08-mep-nutrient-solution.md).

1. Fill the media bottle with water.
2. [Calibrate the pumps](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration) on the **Protocols** page, waste on PWM 2 and media on PWM 3: catch each dispense in a tared weighing boat on the analytical balance and enter what it weighed (1 g of water is about 1 ml).
3. Unscrew the cap, empty, rinse and dry the vial, and fill it to 14 ml with water.
4. Screw the cap back on, and weigh the vial to confirm the volume.
5. Adjust the Media Out tube so it is only just submerged at that level.
6. Run the media and waste pumps, then weigh the vial again.
7. Repeat from item 5 until the vial holds 14 ml after running the pumps.

<details>
<summary>Why the Media Out tube sets the level</summary>

The waste pump over-runs each dilution by design, so the height of the Media Out tube is the level setpoint, not the ratio of media to waste volume. See [forum #801](https://forum.pioreactor.com/t/dosing-volumes-how-to-keep-the-volume-added-and-the-volume-removed-to-be-equal/801).

</details>
