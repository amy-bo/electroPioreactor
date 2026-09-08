---
id: step-08-set-up-co2-sparging
order: 8
title: "Set up carbon dioxide sparging"
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
  **Important:** don all PPE including cryogenic gloves before tightening the cylinder joint, and [follow the instructions included with the SodaStream adapter](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894). Never fit a mismatched adapter to a high-pressure CO₂ joint: retention comes from full thread engagement, and a partial mismatched engagement fails suddenly.
  Ensure the solenoid manual override is closed (horizontal line pointing at 0 on the front of the solenoid).
  The solenoid valve must be 3-way venting (3/2). BoM 3.1: "A 2-way valve traps CO₂ between the valve and the broth on closing; it dissolves and draws liquid back up the line."
---

1. Unscrew John-Guest push-fit output from the regulator outlet port

   *Reference photograph: the source README embeds an external image here, which is not ingested; see the shoot list in [docs/media/README.md](../media/README.md).*

2. Insert 8mm ID 2mm CS o-ring into the regulator outlet port

   *Reference photograph: the source README embeds an external image here, which is not ingested; see the shoot list in [docs/media/README.md](../media/README.md).*

3. Screw in the 1/4" male to 1/8" male reducer to the regulator outlet port and tighten with wrench.

   *Reference photograph: the source README embeds an external image here, which is not ingested; see the shoot list in [docs/media/README.md](../media/README.md).*

4. Apply Loctite 577 anaerobic thread sealant to the 1/8" male outlet thread. PTFE tape is no longer used anywhere in the gas train: applied correctly it seals, but the process is fiddly and it leaked often enough to be worth replacing. Use an o-ring wherever the joint has a seat for one, and Loctite 577 on every threaded joint that has not.
5. Screw left port of the solenoid valve (with solenoid electronics to rear) into 1/8" male outlet. Ensure the solenoid manual override is closed (horizontal line pointing at 0 on the front of the solenoid).

   *Reference photograph: the source README embeds an external image here, which is not ingested; see the shoot list in [docs/media/README.md](../media/README.md).*

6. Apply Loctite 577 to the needle valve inlet thread (the bare metal thread opposite the screw adjustor)
7. Screw needle valve into 1/8" front port of solenoid valve
8. Close needle valve clockwise
9. Fit the o-ring blanking plug to the right port of the solenoid valve and tighten with wrench. The plug seals on its o-ring, so it needs no thread sealant.
10. Close regulator (turn flathead screw fully anti-clockwise)
11. Fit the KegLand KL15578 pin-adjustment SodaStream adapter to the cylinder with the pin **backed off**, then screw the regulator onto the adapter. Tightening no longer races escaping CO₂ — the joint is made first and gas is admitted afterwards.
12. **Important:** don all PPE including cryogenic gloves before tightening the cylinder joint, and [follow the instructions included with the SodaStream adapter](https://cdn.shopify.com/s/files/1/2268/6279/files/BrewKegTap_Sodastream_Adapter_Instructions.pdf?v=1763549894). Never fit a mismatched adapter to a high-pressure CO₂ joint: retention comes from full thread engagement, and a partial mismatched engagement fails suddenly.
13. With the joint made and the regulator closed, open the adapter's thumbscrew pin to admit CO₂ to the regulator.
14. Place SodaStream in dovetail raft
15. Remove compression nut from the top of the needle valve
16. Attach the 4mm tubing to the needle valve ferrule - dip in hot water to soften if necessary
17. Reattach the compression nut
18. Attach the male end of an 0.2 μm vent filter to the female luer lock on the vial CO₂ entry port
19. Attach the female ends of two 0.2 μm vent filters to the two male luer locks on the vial exhaust ports
20. Cut the 4mm tubing just long enough to run over the regulator and down to the CO₂ entry filter
21. Measure the 4mm tubing cut length and ensure all other 4mm tubing is cut to the same length
22. Insert a 1/8" hose barb to male luer lock adapter in the free end of the 4mm tubing - dip in hot water to soften if necessary
23. Connect the luer lock to the CO₂ entry filter
24. Connect the filter's outlet to the head of the tubular MMO anode with a male-to-male luer lock adapter and the 100 mm silicone feed tube (1 mm ID / 3 mm OD). CO₂ enters through the anode and leaves through its open base, so the gas rises past the anode surface and clears oxygen bubbles from it without any separately positioned sparge tube. <!-- TODO: frit dispersion at the anode base is deferred to AEP0.3 | assignee: @Martin -->
25. Cap any unused luer lock with a luer lock cap
26. Connect the solenoid connector to PWM channel 4 on the Pioreactor.
