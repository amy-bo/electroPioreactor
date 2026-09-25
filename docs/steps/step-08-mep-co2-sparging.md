---
id: step-08-mep-co2-sparging
order: 8
title: "CO₂ sparging"
guide: [mep, baep]
parts:
  - {component: fzone-co2-regulator, qty: 1, cat: part}
  - {component: solenoid-valve, qty: 1, cat: part}
  - {component: loctite-577, qty: 1, cat: consumable}
  - {component: co2-needle-valve, qty: 1, cat: part}
  - {component: blanking-plug, qty: 1, cat: part}
  - {component: right-angle-cylinder-adapter, qty: 1, cat: part}
  - {component: sodastream-co2-cylinder, qty: 1, cat: consumable}
  - {component: polyurethane-co2-tube, qty: 1, cat: part}
  - {component: barb-1-8-to-male-luer-lock, qty: 1, cat: part}
  - {component: vial-cap-oring, qty: 1, cat: prev}
tools:
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: hex-key-5mm, qty: 1}
safety: |
  Fit and open the CO₂ cylinder only in a well-ventilated room, wearing eye protection and cryogenic gloves.
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid) except when venting.
  The solenoid valve must be 3-way venting (3/2). A 2-way valve traps CO₂ between the valve and the broth on closing; the CO₂ dissolves and draws liquid back up the line.
checks_draft: true
checks:
  - id: loctite-cured
    question: "Did the Loctite 577 fixture (10 to 60 minutes at 22 °C) before you admitted gas?"
    issues:
      - {problem: "Gas went in sooner", fix: "Unscrew the adapter's pin screw to close the cylinder, set the override to 1 to vent the line, then back to 0, and leave the joints to fixture. Full pressure rating takes 24 hours."}
  - id: no-leak
    question: "Needle valve closed and override at 1, does the regulator's right-hand gauge hold steady for 60 seconds?"
    issues:
      - {problem: "It drops", fix: "A joint upstream of the needle valve leaks. Pipette washing-up liquid in water onto each Loctite 577 joint and watch for bubbles."}
  - id: pwm4
    question: "Is the solenoid lead in PWM channel 4?"
    issues:
      - {problem: "It is in another channel", fix: "Move it to PWM 4: the electroPioreactor job drives the relay there."}
---

1. Apply Loctite 577 to the second thread (not the end one) of the joint between the regulator outlet and the solenoid valve's left port, and screw the solenoid valve on, electronics to the rear. Work up to vertical; do not pass it and turn back. <!-- TODO: confirm how the FZone outlet meets the solenoid (direct 1/8" thread, or a reducing nipple as on the AEP) | assignee: @Martin -->
2. Holding the solenoid, apply Loctite 577 to the blanking plug's second thread and screw it into the solenoid's right port with the 5 mm hex key.
3. Apply Loctite 577 to the needle valve's inlet thread (second thread), and screw it into the solenoid's front port, stopping with it pointing straight up.
4. Close the needle valve (clockwise), and check the solenoid manual override is at 0.
5. Wait for the Loctite 577 to fixture before admitting gas: 10 to 60 minutes at 22 °C. It reaches full pressure rating after 24 hours.
6. Work in a well-ventilated room. Put the SodaStream cylinder into its holder at the rear of the raft.
7. Put on all PPE, including cryogenic gloves.
8. Screw the regulator onto the right-angle cylinder adapter.
9. Back off the adapter's pin screw, seat the adapter's washer, screw the adapter onto the cylinder in one swift, decisive move, and tighten it with the gas cylinder wrench, regulator to the front and the solenoid to its right. <!-- TODO: confirm what seals the adapter at the cylinder (washer as on AEP0.1.1, or o-ring as on AEP0.2) | assignee: @Martin -->
10. Open the cylinder: screw the adapter's pin screw fully down. If the adapter leaks, tighten it further.
11. Read the two gauges. The left shows the cylinder pressure, your warning that it is running out; the right shows the pressure reaching the solenoid. The FZone's outlet pressure is fixed, so there is nothing to set.
12. Check for leaks: with the needle valve closed, turn the solenoid override to 1 and watch the right-hand gauge for 60 seconds. Any drop means a leak upstream of the needle valve. Turn the override back to 0.
13. Remove the compression nut and ferrule from the top of the needle valve, thread the nut onto the 4 mm polyurethane CO₂ tube, and push the tube fully onto the needle valve (dip it in hot water if it will not go). Refit the ferrule, and screw the nut down.
14. Cut the tube just long enough to run over the regulator and down to the vial cap's CO₂ inlet (cut every other unit's tube to the same length), and push a 1/8" hose barb to male luer lock adapter into the free end (hot water if needed).
15. Connect the tube's luer to the vial cap's CO₂ inlet luer.
16. Route the solenoid lead down behind the Pioreactor and through the pumps, and plug it into PWM channel 4.

<details>
<summary>Notes</summary>

- Solenoid override: 0 is normal (closed without power); 1 is always open.
- Loctite 577 is anaerobic thread sealant, not glue. Skipping the end thread keeps it out of the gas path. Clean the threads with ethanol first where you can.
- Do not use PTFE tape in the gas train. Applied correctly it seals, but it is fiddly and leaks too often.
- With a fixed-pressure regulator the needle valve is the only flow control. It is set in **Calibrate CO₂ flow**.
- Carrying the unit elsewhere: keep the regulator, solenoid and needle valve assembled, and take the cylinder off.

</details>
