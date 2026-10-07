---
id: step-13-admit-co2
order: 13
media: [vid-08b-admit-co2]
title: "Admit CO₂"
guide: [aep]
parts:
  - {component: co2-regulator, qty: 1, cat: prev}
  - {component: co2-needle-valve, qty: 1, cat: prev}
  - {component: polyurethane-co2-tube, qty: 1, cat: part}
  - {component: hydrophobic-vent-filter, qty: 3, cat: part}
  - {component: barb-1-8-to-male-luer-lock, qty: 1, cat: part}
  - {component: anode-feed-tube, qty: 1, cat: prev}
  - {component: male-to-male-luer-lock-adapter, qty: 2, cat: prev}
  - {component: luer-lock-cap, qty: 1, cat: part}
  - {component: solenoid-valve, qty: 1, cat: prev}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: crimp-connector, qty: 2, cat: prev}
  - {component: crimp-housing, qty: 1, cat: prev}
tools:
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: lab-coat, qty: 1}
  - {component: needle-nose-pliers, qty: 1}
safety: |
  Keep all PPE on, including cryogenic gloves: if the adapter leaks you tighten the cylinder joint further, under pressure.
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid).
checks_draft: true
checks:
  - id: gas-tight
    question: "With CO₂ admitted, where can you hear or feel gas escaping?"
    options:
      - {label: "Nowhere along the train", correct: true}
      - {label: "At a threaded joint of the solenoid or needle valve", fix: "Every threaded joint without an o-ring seat needs Loctite 577. It fixtures in 10 to 60 minutes at 22 °C and reaches full pressure rating after 24 hours."}
      - {label: "Where the 4 mm tube meets a barb or ferrule", fix: "Soften the tube end in hot water and reseat it. The 1/8\" barb must grip the 4 mm tube, or the joint leaks under pressure."}
      - {label: "Round the blanking plug in the solenoid", fix: "It seals on its o-ring, not on sealant. Check the o-ring is present, and tighten with the wrench."}
      - {label: "At the adapter on the cylinder", fix: "Tighten the adapter further with the gas cylinder wrench, wearing the cryogenic gloves."}
  - id: pwm4
    question: "Which PWM channel is the solenoid connector plugged into?"
    options:
      - {label: "PWM 4", correct: true}
      - {label: "PWM 3", fix: "Move it to PWM channel 4: the plugin maps that channel to the relay. PWM 3 is the product pump's."}
      - {label: "PWM 2", fix: "Move it to PWM channel 4: the plugin maps that channel to the relay. PWM 2 is the media pump's."}
---

The gas train was built and checked in [CO₂ gas train](step-12-co2-gas-train.md), with the pin backed off.

1. Open the adapter's pin to admit CO₂. The cylinder gauge reads about 60 bar when full. If the adapter leaks, tighten it further. <!-- from video: session-21 0:33:43-0:36:13 - the adapter leaked until tightened further -->
2. Screw the regulator in until its outlet gauge reads about 1 bar.
3. Remove the compression nut and ferrule from the top of the needle valve, thread the nut onto the 4 mm polyurethane CO₂ tube, and push the tube fully onto the needle valve (dip it in hot water if it will not go). Refit the ferrule, and screw the nut down.
4. Cut the tube just long enough to run over the regulator and down to the vial's CO₂ inlet (cut every other unit's tube to the same length), and push a 1/8" hose barb to male luer lock adapter into the free end (hot water if needed).
5. Fit the male end of a 0.2 μm vent filter to the female luer on the CO₂ inlet, and connect the tube's luer to that filter. <!-- kits from 2026-09-24 include six vent filters; the recorded build had none -->
6. Fit the female ends of two 0.2 μm vent filters to the male-to-male adapters on the two gas outlets (fitted in [Ports](step-11-ports.md)), and cap any unused luer lock with a luer lock cap.
7. Route the solenoid lead down behind the Pioreactor and through the pumps, and plug it into PWM channel 4.

<!-- VIDEO CUT: session-21 - this step starts where the pin is opened (about 0:33:43). -->

<details>
<summary>Notes</summary>

- CO₂ enters through the anode and leaves through its open base. The gas rises past the anode surface and clears oxygen bubbles from it, with no separate sparge tube. <!-- TODO: frit dispersion at the anode base is deferred to AEP0.3 | assignee: @Martin -->

</details>
