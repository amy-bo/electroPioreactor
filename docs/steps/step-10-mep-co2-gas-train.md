---
id: step-10-mep-co2-gas-train
order: 10
title: "CO₂ gas train"
guide: [mep, baep]
parts:
  - {component: fzone-co2-regulator, qty: 1, cat: part}
  - {component: solenoid-valve, qty: 1, cat: part}
  - {component: loctite-577, qty: 1, cat: consumable}
  - {component: co2-needle-valve, qty: 1, cat: part}
  - {component: blanking-plug, qty: 1, cat: part}
tools:
  - {component: hex-key-5mm, qty: 1}
safety: |
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid) except when venting.
  The solenoid valve must be 3-way venting (3/2). A 2-way valve traps CO₂ between the valve and the broth on closing; the CO₂ dissolves and draws liquid back up the line.
checks_draft: true
checks:
  - id: loctite-cured
    question: "How long ago did you screw in the needle valve, the last Loctite 577 joint?"
    options:
      - {label: "An hour or more ago", correct: true}
      - {label: "Between 10 and 60 minutes ago", fix: "It may not have fixtured yet: at 22 °C that takes 10 to 60 minutes. Wait until the hour is up before admitting gas. Full pressure rating takes 24 hours."}
      - {label: "Less than 10 minutes ago", fix: "Wait: Loctite 577 fixtures in 10 to 60 minutes at 22 °C. Admit gas only after that. Full pressure rating takes 24 hours."}
  - id: override-closed
    question: "What does the solenoid's manual override point at?"
    options:
      - {label: "0 (horizontal line at 0)", correct: true}
      - {label: "1 (horizontal line at 1)", fix: "Turn it to 0. At 1 the solenoid is always open, so gas would flow as soon as the cylinder opens."}
---

This step builds the valve train with no cylinder fitted. **Admit CO₂**, next, fits the cylinder and opens it once the Loctite 577 has fixtured.

1. Apply Loctite 577 to the second thread (not the end one) of the joint between the regulator outlet and the solenoid valve's left port, and screw the solenoid valve on, electronics to the rear. Work up to vertical; do not pass it and turn back. <!-- TODO: confirm how the FZone outlet meets the solenoid (direct 1/8" thread, or a reducing nipple as on the AEP) | assignee: @Martin -->
2. Holding the solenoid, apply Loctite 577 to the blanking plug's second thread and screw it into the solenoid's right port with the 5 mm hex key.
3. Apply Loctite 577 to the needle valve's inlet thread (second thread), and screw it into the solenoid's front port, stopping with it pointing straight up.
4. Close the needle valve (clockwise), and check the solenoid manual override is at 0.
5. Wait for the Loctite 577 to fixture before admitting gas: 10 to 60 minutes at 22 °C. It reaches full pressure rating after 24 hours.

<details>
<summary>Notes</summary>

- Solenoid override: 0 is normal (closed without power); 1 is always open.
- Loctite 577 is anaerobic thread sealant, not glue. Skipping the end thread keeps it out of the gas path. Clean the threads with ethanol first where you can.
- Do not use PTFE tape in the gas train. Applied correctly it seals, but it is fiddly and leaks too often.

</details>
