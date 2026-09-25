---
id: step-07-ports
order: 7
title: "Ports"
guide: [aep]
parts:
  - {component: needle-port, qty: 4, cat: part}
  - {component: mmo-anode, qty: 1, cat: prev}
  - {component: stainless-steel-cathode, qty: 1, cat: prev}
  - {component: vial-cap, qty: 1, cat: prev}
  - {component: silicone-septum, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: eight-ports
    question: "Can you identify all eight ports on the cap, with the spare port sealed?"
    issues:
      - {problem: "The spare port is open", fix: "Seal it. Every unused opening lets contamination in."}
  - id: four-needles
    question: "Are the four needle ports (Media In, Media Out, Gas Out and Gas Out – safety) through the septum?"
    issues:
      - {problem: "You have fewer than four needles", fix: "Each Pioreactor ships with four, and the BoM adds one per unit. Check the parts checklist in Before you start, and use its **Missing parts** email if any are short."}
---

1. Push a female luer onto the media pump's inlet tubing. It is a tight fit (1 mm bore). <!-- from video: session-21 0:00:13 -->
2. Push the 80 mm needle (Media Out) down through the septum to the liquid level you want: it sets the level. <!-- from video: session-21 0:01:07 - 80 mm 316 stainless for the outlet, 75 mm for the inlet; the needle-port component lists 75 mm, 304 -->
3. Push the 75 mm needle (Media In) straight through the septum.
4. After each needle goes through, pull it back out, clear any silicone plug, and reinsert it through the same hole.

   :::tip
   Light visible through the needle means it is clear. Otherwise blow it clear with a syringe.
   :::
5. Set the level by weighing the vial while running the pumps, so Media Out just maintains it.
6. Fit a male-to-male luer adapter to each outlet needle, so outlets are marked as outlets.
7. Push the two bent needles (Gas Out and Gas Out – safety) through the septum, above the liquid level. <!-- from video: session-21 0:11:35 - Bingqiao suggests the bent needles may stretch the septum unevenly -->
8. Thread the 1 mm-bore anode feed tube through the MMO anode, and pull it tight at the top.
9. Trim the feed tube's lower end with sharp scissors. <!-- from video: session-21 0:12:53 - done after the vial was filled; Martin: "might have been clever to do this before we got the liquid in"; which end was trimmed is not clear from the transcript -->
10. Check the Media Out needle is at the water level, every other needle is higher, and none is plugged with silicone.

    :::tip[Bent needles]
    You cannot look through a bent needle. Blow gas or air through it at a steady pressure and compare the flow with a clear needle.
    :::
11. Push a female luer onto the feed tube's top end: this is the CO₂ inlet.
12. Seal the spare port.
