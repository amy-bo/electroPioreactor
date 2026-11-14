---
id: step-11-mep-admit-co2
order: 11
title: "Admit CO₂"
guide: [mep, baep]
parts:
  - {component: fzone-co2-regulator, qty: 1, cat: prev}
  - {component: solenoid-valve, qty: 1, cat: prev}
  - {component: right-angle-cylinder-adapter, qty: 1, cat: part}
  - {component: sodastream-co2-cylinder, qty: 1, cat: consumable}
  - {component: polyurethane-co2-tube, qty: 1, cat: part}
  - {component: barb-1-8-to-male-luer-lock, qty: 1, cat: part}
  - {component: vial-cap-oring, qty: 1, cat: prev}
tools:
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
safety: |
  Fit and open the CO₂ cylinder only in a well-ventilated room, wearing eye protection and cryogenic gloves.
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid) except when venting.
checks_draft: true
checks:
  - id: no-leak
    question: "Needle valve closed and override at 1, what does the regulator's right-hand gauge do over 60 seconds?"
    options:
      - {label: "Holds steady at the same reading", correct: true}
      - {label: "Falls steadily from its first reading", fix: "A joint upstream of the needle valve leaks. Pipette washing-up liquid in water onto each Loctite 577 joint and watch for bubbles."}
      - {label: "Stays at zero from the start", fix: "The cylinder is not open: screw the adapter's pin screw fully down."}
  - id: pwm4
    question: "Which PWM channel is the solenoid lead plugged into?"
    options:
      - {label: "PWM 4", correct: true}
      - {label: "PWM 3", fix: "Move it to PWM 4: the electroPioreactor job drives the relay there. PWM 3 is the media pump's."}
      - {label: "PWM 2", fix: "Move it to PWM 4: the electroPioreactor job drives the relay there. PWM 2 is the waste pump's."}
---

The valve train was built and left to fixture in [CO₂ gas train](step-10-mep-co2-gas-train.md).

1. Work in a well-ventilated room. Put the SodaStream cylinder into its holder at the rear of the raft.
2. Put on all PPE, including cryogenic gloves.
3. Screw the regulator onto the right-angle cylinder adapter.
4. Back off the adapter's pin screw, seat the adapter's washer, screw the adapter onto the cylinder in one swift, decisive move, and tighten it with the gas cylinder wrench, regulator to the front and the solenoid to its right. <!-- TODO: confirm what seals the adapter at the cylinder (washer as on AEP0.1.1, or o-ring as on AEP0.2) | assignee: @Martin -->
5. Open the cylinder: screw the adapter's pin screw fully down. If the adapter leaks, tighten it further.
6. Read the two gauges. The left shows the cylinder pressure, your warning that it is running out; the right shows the pressure reaching the solenoid. The FZone's outlet pressure is fixed, so there is nothing to set.
7. Check for leaks: with the needle valve closed, turn the solenoid override to 1 and watch the right-hand gauge for 60 seconds. Any drop means a leak upstream of the needle valve. Turn the override back to 0.
8. Remove the compression nut and ferrule from the top of the needle valve, thread the nut onto the 4 mm polyurethane CO₂ tube, and push the tube fully onto the needle valve (dip it in hot water if it will not go). Refit the ferrule, and screw the nut down.
9. Cut the tube just long enough to run over the regulator and down to the vial cap's CO₂ inlet (cut every other unit's tube to the same length), and push a 1/8" hose barb to male luer lock adapter into the free end (hot water if needed).
10. Connect the tube's luer to the vial cap's CO₂ inlet luer.
11. Route the solenoid lead down behind the Pioreactor and through the pumps, and plug it into PWM channel 4.

<details>
<summary>Notes</summary>

- With a fixed-pressure regulator the needle valve is the only flow control. It is set in **Calibrate CO₂ flow**.
- Carrying the unit elsewhere: keep the regulator, solenoid and needle valve assembled, and take the cylinder off.

</details>
