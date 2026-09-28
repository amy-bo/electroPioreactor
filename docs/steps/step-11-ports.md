---
id: step-11-ports
order: 11
title: "Ports"
guide: [aep]
parts:
  - {component: needle-port, qty: 4, cat: part}
  - {component: male-to-male-luer-lock-adapter, qty: 2, cat: part}
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
    question: "Which of the cap's eight ports have nothing through them?"
    options:
      - {label: "Inoculation and the spare", correct: true}
      - {label: "Inoculation only", fix: "A needle went into the spare port. Pull it out (the septum self-heals the needle track and keeps the port sealed) and put it through the port it belongs to."}
      - {label: "The spare only", fix: "A needle went into the inoculation port. Pull it out: the inoculation syringe goes straight through the septum there. Put the needle through the port it belongs to."}
      - {label: "Inoculation, the spare and a gas outlet", fix: "Push the second bent needle through as Gas Out – safety. Short of needles? Each Pioreactor ships with four, and the BoM adds one per unit: check **Count what you received** in **Before you start**, and use the **Missing something?** line under it."}
  - id: four-needles
    question: "Where do the needle tips sit relative to the water?"
    options:
      - {label: "Media Out at the surface, all the others above it", correct: true}
      - {label: "Media In under the surface, the others above it", fix: "Pull Media In up above the water: only Media Out sits at the water level."}
      - {label: "A bent gas needle at or under the surface", fix: "Pull it up above the liquid level: only Media Out sits at the water level."}
  - id: thirty-ml
    question: "Filled with DI water via the pumps and weighed against the dry empty vial, what does the vial hold while the pumps run?"
    options:
      - {label: "30 ml, holding steady", correct: true}
      - {label: "More than 30 ml", fix: "Push the Media Out needle a little further down, run the pumps and re-weigh until it holds 30 ml."}
      - {label: "Less than 30 ml", fix: "Pull the Media Out needle up a little, run the pumps and re-weigh until it holds 30 ml."}
  - id: immersion-recorded
    question: "What have you recorded for the electrodes in this step?"
    options:
      - {label: "Each insertion depth, after setting the standard immersion", correct: true}
      - {label: "Each insertion depth, before setting the standard immersion", fix: "Adjust them to the standard immersion depth, then record the new insertion depths."}
      - {label: "Nothing yet for either electrode", fix: "Measure the immersion depths, adjust them to the standard if needed, and record each insertion depth."}
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
7. Fill the vial with DI water via the pumps, and weigh it against the dry empty vial.
8. Move the Media Out needle up or down until the vial holds 30 ml and Media Out just maintains that level while the pumps run.
9. Measure the electrode immersion depths, adjust them to the standard if needed, and record each insertion depth. <!-- TODO: the AEP0.2 standard depth is still to be measured on the first build (BoM open item 2.3) | assignee: @Martin -->
10. Check the Media Out needle is at the water level, every other needle is higher, and none is plugged with silicone.

    :::tip[Bent needles]
    You cannot look through a bent needle. Blow gas or air through it at a steady pressure and compare the flow with a clear needle.
    :::
11. Set up the Pioreactor in [turbidostat mode](https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat).
