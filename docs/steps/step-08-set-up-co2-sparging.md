---
id: step-08-set-up-co2-sparging
order: 8
title: "CO₂ sparging"
guide: [aep]
parts:
  - {component: co2-regulator, qty: 1, cat: part}
  - {component: regulator-outlet-o-ring, qty: 1, cat: part}
  - {component: reducing-nipple, qty: 1, cat: part}
  - {component: loctite-577, qty: 1, cat: consumable}
  - {component: solenoid-valve, qty: 1, cat: part}
  - {component: co2-needle-valve, qty: 1, cat: part}
  - {component: blanking-plug, qty: 1, cat: part}
  - {component: cylinder-regulator-adapter, qty: 1, cat: part}
  - {component: sodastream-co2-cylinder, qty: 1, cat: consumable}
  - {component: polyurethane-co2-tube, qty: 1, cat: part}
  - {component: hydrophobic-vent-filter, qty: 3, cat: part}
  - {component: barb-1-8-to-male-luer-lock, qty: 1, cat: part}
  - {component: male-to-male-luer-lock-adapter, qty: 1, cat: part}
  - {component: anode-feed-tube, qty: 1, cat: part}
  - {component: luer-lock-cap, qty: 1, cat: part}
  - {component: solenoid-wiring, qty: 1, cat: part}
  - {component: co2-cylinder-dovetail-holder, qty: 1, cat: prev}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: crimp-connector, qty: 1, cat: prev}
  - {component: crimp-housing, qty: 1, cat: prev}
tools:
  - {component: gas-cylinder-wrench, qty: 1}
  - {component: banded-oil-filter-wrench, qty: 1}
  - {component: cryogenic-gloves, qty: 1}
  - {component: eye-face-protection, qty: 1}
  - {component: lab-coat, qty: 1}
  - {component: needle-nose-pliers, qty: 1}
safety: |
  Put on all PPE, including cryogenic gloves, before tightening the cylinder joint. [Follow the instructions included with the SodaStream adapter](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894). Never fit a mismatched adapter to a high-pressure CO₂ joint: only full thread engagement holds it, and a partial, mismatched engagement fails suddenly.
  Keep the solenoid manual override closed (horizontal line pointing at 0 on the front of the solenoid).
  The solenoid valve must be 3-way venting (3/2). A 2-way valve traps CO₂ between the valve and the broth on closing; the CO₂ dissolves and draws liquid back up the line (BoM 3.1).
checks_draft: true
checks:
  - id: joint-before-gas
    question: "Was the regulator screwed fully onto the adapter, pin backed off, before any CO₂ was admitted?"
    issues:
      - {problem: "Gas escaped while tightening", fix: "Back off the adapter's pin to stop the gas. Screw the regulator fully onto the adapter, then open the pin again. Never fit a mismatched adapter."}
  - id: override-closed
    question: "Is the solenoid manual override closed (horizontal line pointing at 0)?"
    issues:
      - {problem: "CO₂ flows all the time", fix: "Close the manual override."}
  - id: gas-tight
    question: "Once CO₂ is admitted, is the train free of hissing or leaks?"
    issues:
      - {problem: "A threaded joint leaks", fix: "Every threaded joint without an o-ring seat needs Loctite 577. It fixtures in 10 to 60 minutes at 22 °C and reaches full pressure rating after 24 hours."}
      - {problem: "The 4 mm tube leaks at a barb or ferrule", fix: "Soften the tube end in hot water and reseat it. The 1/8\" barb must grip the 4 mm tube, or the joint leaks under pressure."}
      - {problem: "The blanking plug leaks", fix: "It seals on its o-ring, not on sealant. Check the o-ring is present, and tighten with the wrench."}
  - id: pwm4
    question: "Is the solenoid connector plugged into PWM channel 4?"
    issues:
      - {problem: "It is on another channel", fix: "Move it to PWM channel 4: the plugin maps that channel to the relay."}
---

1. Work in a well-ventilated room. Put the SodaStream cylinder into its holder at the rear of the raft.
2. Put on all PPE, including cryogenic gloves.
3. Back off the KegLand adapter's pin (thumbscrew out and loose), and seat the o-ring on top of the cylinder. <!-- from video: session-21 0:18:57 - "the critical thing we need is the o-ring ... I tend to just put the o-ring on top of the cylinder"; no component names this o-ring -->
4. Screw the adapter on, tighten it with the gas cylinder wrench, and turn the cylinder so the adapter faces the front.
5. Unscrew the John Guest push-fit from the regulator outlet port.

   <img width="1330" height="1767" alt="image" src="https://github.com/user-attachments/assets/3cbc619c-be7c-4abb-87d3-048d8350dcfc" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

6. Insert the o-ring into the regulator outlet port. It seats against the reducer, so this joint needs no Loctite. <!-- kits from 2026-09-24 include this o-ring; the recorded build had none and used Loctite 577 instead -->

   <img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/3316cd49-21c7-4fb3-a931-dd5c0798a27b" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

7. Screw the 1/4" male to 1/8" male reducer into the regulator outlet port, and tighten with the wrench.

   <img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/800812cb-2ccb-4a8f-8198-f8e381757552" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

8. Apply Loctite 577 to the second thread (not the end one) of the reducer's 1/8" male outlet, and screw the solenoid valve's left port onto it, electronics to the rear. Work up to vertical; do not pass it and turn back.

   <img width="1767" height="1330" alt="image" src="https://github.com/user-attachments/assets/ec433749-5866-476b-a965-ec070b80083e" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

9. Holding the solenoid, screw the blanking plug into its right port with a 5 mm hex key. Use no sealant. <!-- from video: session-21 0:28:08 - the blanking plug went in before the needle valve; the text had it after -->
10. Apply Loctite 577 to the needle valve's inlet thread (second thread), and screw it into the solenoid's front port, stopping with it pointing straight up.
11. Close the needle valve (clockwise), and check the solenoid manual override is at 0.
12. Close the regulator (turn its flathead screw fully anti-clockwise), then screw it onto the adapter and tighten.
13. Open the adapter's pin to admit CO₂. The cylinder gauge reads about 60 bar when full. If the adapter leaks, tighten it further. <!-- from video: session-21 0:33:43-0:36:13 - the adapter leaked until tightened further -->
14. Screw the regulator in until its outlet gauge reads about 1 bar.
15. Remove the compression nut and ferrule from the top of the needle valve, thread the nut onto the 4 mm tube, and push the tube fully onto the needle valve. If it will not go, dip it in hot water.
16. Refit the ferrule, and screw the nut down.
17. Cut the tube just long enough to run over the regulator and down to the vial's CO₂ inlet (cut every other unit's tube to the same length), and push a 1/8" hose barb to male luer lock adapter into the free end (hot water if needed).
18. Fit the male end of a 0.2 μm vent filter to the female luer on the CO₂ inlet, and connect the tube's luer to that filter. <!-- kits from 2026-09-24 include six vent filters; the recorded build had none -->
19. Fit the female ends of two 0.2 μm vent filters to the male luers on the two gas outlets, and cap any unused luer lock with a luer lock cap.
20. Route the solenoid lead down behind the Pioreactor and through the pumps, and plug it into PWM channel 4.

<details>
<summary>Notes</summary>

- Solenoid override: 0 is normal (closed without power); 1 is always open.
- Use an o-ring wherever the joint has a seat for one, and Loctite 577 on every other threaded joint. Loctite 577 is anaerobic thread sealant, not glue. Skipping the end thread keeps it out of the gas path. Clean the threads with ethanol first where you can.
- PTFE tape is no longer used in the gas train. Applied correctly it seals, but it is fiddly and leaked often enough to replace.
- CO₂ enters through the anode and leaves through its open base. The gas rises past the anode surface and clears oxygen bubbles from it, with no separate sparge tube. <!-- TODO: frit dispersion at the anode base is deferred to AEP0.3 | assignee: @Martin -->

</details>
