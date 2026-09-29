---
id: step-12-co2-gas-train
order: 12
media: [vid-08-co2-gas-train]
title: "CO₂ gas train"
guide: [aep]
parts:
  - {component: anode-feed-tube, qty: 1, cat: part}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: co2-regulator, qty: 1, cat: part}
  - {component: regulator-outlet-o-ring, qty: 1, cat: part}
  - {component: reducing-nipple, qty: 1, cat: part}
  - {component: loctite-577, qty: 1, cat: consumable}
  - {component: solenoid-valve, qty: 1, cat: part}
  - {component: co2-needle-valve, qty: 1, cat: part}
  - {component: blanking-plug, qty: 1, cat: part}
  - {component: cylinder-regulator-adapter, qty: 1, cat: part}
  - {component: sodastream-co2-cylinder, qty: 1, cat: consumable}
  - {component: co2-cylinder-dovetail-holder, qty: 1, cat: prev}
tools:
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: banded-oil-filter-wrench, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: lab-coat, qty: 1}
safety: |
  Put on all PPE, including cryogenic gloves, before tightening the cylinder joint. [Follow the instructions included with the SodaStream adapter](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894). Never fit a mismatched adapter to a high-pressure CO₂ joint: only full thread engagement holds it, and a partial, mismatched engagement fails suddenly.
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid).
  The solenoid valve must be 3-way venting (3/2). A 2-way valve traps CO₂ between the valve and the broth on closing; the CO₂ dissolves and draws liquid back up the line.
checks_draft: true
checks:
  - id: joint-before-gas
    question: "Before any gas goes in, where do the adapter's pin and the regulator stand?"
    options:
      - {label: "Pin backed off; regulator screwed fully onto the adapter", correct: true}
      - {label: "Pin screwed in; regulator screwed fully onto the adapter", fix: "Back the pin off now (thumbscrew out and loose). The pin admits the gas, and **Admit CO₂** opens it once the Loctite 577 has fixtured."}
      - {label: "Pin backed off; regulator part way onto the adapter", fix: "Screw the regulator fully onto the adapter and tighten it. Only full thread engagement holds a high-pressure joint. Never fit a mismatched adapter."}
  - id: override-closed
    question: "What does the solenoid's manual override point at?"
    options:
      - {label: "0 (horizontal line at 0)", correct: true}
      - {label: "1 (horizontal line at 1)", fix: "Turn it to 0. At 1 the solenoid is always open, so CO₂ would flow all the time."}
---

This step builds the gas train with the adapter's pin backed off, so no gas goes in. **Admit CO₂**, next, opens it.

1. Thread the 1 mm-bore anode feed tube through the MMO anode, and pull it tight at the top.
2. Trim the feed tube's lower end with sharp scissors, as close to the bottom of the anode as you can.
3. Push a female luer onto the feed tube's top end: this is the CO₂ inlet.
4. Work in a well-ventilated room. Put the SodaStream cylinder into its holder at the rear of the raft.
5. Put on all PPE, including cryogenic gloves.
6. Back off the KegLand adapter's pin (thumbscrew out and loose), and seat the o-ring on top of the cylinder. <!-- from video: session-21 0:18:57 - "the critical thing we need is the o-ring ... I tend to just put the o-ring on top of the cylinder"; no component names this o-ring -->
7. Screw the adapter on, tighten it with the gas cylinder wrench, and turn the cylinder so the adapter faces the front.
8. Unscrew the John Guest push-fit from the regulator outlet port.

   <img width="1330" height="1767" alt="The regulator outlet port with the John Guest push-fit unscrewed (AEP0.1 photograph)" src="https://github.com/user-attachments/assets/3cbc619c-be7c-4abb-87d3-048d8350dcfc" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

9. Insert the o-ring into the regulator outlet port. It seats against the reducer, so this joint needs no Loctite. <!-- kits from 2026-09-24 include this o-ring; the recorded build had none and used Loctite 577 instead -->

   <img width="1767" height="1330" alt="The o-ring seated inside the regulator outlet port (AEP0.1 photograph)" src="https://github.com/user-attachments/assets/3316cd49-21c7-4fb3-a931-dd5c0798a27b" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

10. Screw the reducing nipple (1/4" male to 1/8" male) into the regulator outlet port, and tighten with the wrench.

   <img width="1767" height="1330" alt="The reducer screwed into the regulator outlet port (AEP0.1 photograph)" src="https://github.com/user-attachments/assets/800812cb-2ccb-4a8f-8198-f8e381757552" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

11. Apply Loctite 577 to the second thread (not the end one) of the reducer's 1/8" male outlet, and screw the solenoid valve's left port onto it, electronics to the rear. Work up to vertical; do not pass it and turn back.

   <img width="1767" height="1330" alt="The solenoid valve screwed onto the reducer by its left port, electronics to the rear (AEP0.1 photograph)" src="https://github.com/user-attachments/assets/ec433749-5866-476b-a965-ec070b80083e" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

12. Holding the solenoid, screw the blanking plug into its right port with a 5 mm hex key. Use no sealant. <!-- from video: session-21 0:28:08 - the blanking plug went in before the needle valve; the text had it after -->
13. Apply Loctite 577 to the needle valve's inlet thread (second thread), and screw it into the solenoid's front port, stopping with it pointing straight up.
14. Close the needle valve (clockwise), and check the solenoid manual override is at 0.
15. Close the regulator (turn its flathead screw fully anti-clockwise), then screw it onto the adapter and tighten.
16. Wait for the Loctite 577 to fixture before admitting gas: 10 to 60 minutes at 22 °C. It reaches full pressure rating after 24 hours.

<!-- VIDEO CUT: session-21 - cut after the regulator is screwed onto the adapter (item 15), before the pin is opened to admit gas (about 0:33:43); Admit CO₂ starts there. -->

<details>
<summary>Notes</summary>

- Solenoid override: 0 is normal (closed without power); 1 is always open.
- Use an o-ring wherever the joint has a seat for one, and Loctite 577 on every other threaded joint. Loctite 577 is anaerobic thread sealant, not glue. Skipping the end thread keeps it out of the gas path. Clean the threads with ethanol first where you can.
- Do not use PTFE tape in the gas train. Applied correctly it seals, but it is fiddly and leaks too often.

</details>
