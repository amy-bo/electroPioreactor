---
id: step-07-ports
order: 7
title: "Ports"
guide: [aep]
parts:
  - {component: needle-port, qty: 4, cat: part}
  - {component: male-to-male-luer-lock-adapter, qty: 2, cat: part}
  - {component: anode-feed-tube, qty: 1, cat: part}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: stainless-steel-cathode, qty: 1, cat: prev}
  - {component: vial-cap, qty: 1, cat: prev}
  - {component: silicone-septum, qty: 1, cat: prev}
  - {component: pioreactor-vial-40ml, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
  - {component: vernier-callipers, qty: 1}
checks_draft: true
checks:
  - id: eight-ports
    question: "Can you identify all eight ports on the cap, with the spare port left unpierced?"
    issues:
      - {problem: "A needle went into the spare port", fix: "Pull it out. The septum self-heals the needle track and keeps the port sealed."}
  - id: four-needles
    question: "Are the four needle ports (Media In, Media Out, Gas Out and Gas Out – safety) through the septum?"
    issues:
      - {problem: "You have fewer than four needles", fix: "Each Pioreactor ships with four, and the BoM adds one per unit. Check the parts checklist in Before you start, and use the **Missing something?** line under it if any are short."}
  - id: thirty-ml
    question: "Filled with DI water via the pumps and weighed against the dry empty vial, does the vial hold 30 ml?"
    issues:
      - {problem: "The volume is not 30 ml", fix: "Move the Media Out needle up or down, run the pumps and re-weigh until it is."}
  - id: immersion-recorded
    question: "Are both electrodes at the standard immersion depth, and is each insertion depth recorded?"
    issues:
      - {problem: "A depth is off", fix: "Adjust it to the standard and record the new insertion depth."}
---

The cap has eight ports. The electrodes already fill two, this step puts needles through four, and the septum keeps the last two closed:

- Anode and CO₂ In (6 mm)
- Cathode (6 mm)
- Media In
- Media Out
- Gas Out
- Gas Out – safety
- Inoculation (the large port): a syringe goes straight through the septum, with no tube and no pinch slider
- Spare: left unpierced, so the septum seals it

1. Push a female luer onto the media pump's inlet tubing. It is a tight fit (1 mm bore). <!-- from video: session-21 0:00:13 -->
2. Push the 80 mm needle (Media Out) down through the septum to the liquid level you want: it sets the level. <!-- from video: session-21 0:01:07 - 80 mm 316 stainless for the outlet, 75 mm for the inlet; the needle-port component lists 75 mm, 304 -->
3. Push the 75 mm needle (Media In) straight through the septum.
4. After each needle goes through, pull it back out, clear any silicone plug, and reinsert it through the same hole.

   :::tip
   Light visible through the needle means it is clear. Otherwise blow it clear with a syringe.
   :::
5. Push the two bent needles (Gas Out and Gas Out – safety) through the septum, above the liquid level. <!-- from video: session-21 0:11:35 - Bingqiao suggests the bent needles may stretch the septum unevenly -->
6. Fit a male-to-male luer adapter to each of the two gas outlet needles, so outlets are marked as outlets.
7. Thread the 1 mm-bore anode feed tube through the MMO anode, and pull it tight at the top.
8. Trim the feed tube's lower end with sharp scissors. <!-- from video: session-21 0:12:53 - done after the vial was filled; Martin: "might have been clever to do this before we got the liquid in"; which end was trimmed is not clear from the transcript --> <!-- TODO: state the trim length | assignee: @Martin -->
9. Push a female luer onto the feed tube's top end: this is the CO₂ inlet.
10. Fill the vial with DI water via the pumps, and weigh it against the dry empty vial.
11. Move the Media Out needle up or down until the vial holds 30 ml and Media Out just maintains that level while the pumps run.
12. Measure the electrode immersion depths, adjust them to the standard if needed, and record each insertion depth. <!-- TODO: the AEP0.2 standard depth is still to be measured on the first build (BoM open item 2.3) | assignee: @Martin -->
13. Check the Media Out needle is at the water level, every other needle is higher, and none is plugged with silicone.

    :::tip[Bent needles]
    You cannot look through a bent needle. Blow gas or air through it at a steady pressure and compare the flow with a clear needle.
    :::
14. Set up the Pioreactor in [turbidostat mode](https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat).
