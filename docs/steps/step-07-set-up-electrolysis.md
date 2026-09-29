---
id: step-07-set-up-electrolysis
order: 7
title: "Set up electrolysis"
media: [vid-06-electrolysis]
guide: [aep]
parts:
  - {component: silicone-septum, qty: 1, cat: part}
  - {component: vial-cap, qty: 1, cat: printed}
  - {component: mmo-anode, qty: 1, cat: part}
  - {component: stainless-steel-cathode, qty: 1, cat: part}
  - {component: electrode-cable, qty: 2, cat: part}
  - {component: ring-terminal, qty: 2, cat: part}
  - {component: m3-nut, qty: 2, cat: part}
  - {component: m3-spring-washer, qty: 2, cat: part}
  - {component: thumb-screw, qty: 2, cat: part}
  - {component: crimp-connector, qty: 1, cat: part}
  - {component: crimp-housing, qty: 1, cat: part}
  - {component: pioreactor-vial-40ml, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
renders:
  - {id: vial-cap-iso, component: vial-cap, view: iso, explode: false, format: png}
  - {id: vial-cap-exploded, component: vial-cap, view: iso, explode: true, format: png}
viewer: {component: vial-cap, format: glb}
safety: |
  Fix the red cable's ring terminal to the MMO anode and the black cable's to the stainless steel cathode. Never swap them. Reversed, the stainless steel cathode corrodes quickly and leaches Cr, Ni and Fe into the culture.
checks_draft: true
checks:
  - id: polarity
    question: "Which electrode is the red cable's ring terminal fixed to?"
    options:
      - {label: "The MMO anode (the tube)", correct: true}
      - {label: "The stainless steel cathode (the rod)", fix: "Swap the two ring terminals now, before anything drives the electrodes. Reversed, the stainless steel corrodes quickly and leaches Cr, Ni and Fe into the culture."}
  - id: depth
    question: "With the cap fully screwed on, where are the electrode tops?"
    options:
      - {label: "Both flush with the top of the cap", correct: true}
      - {label: "One or both standing proud of the cap top", fix: "Push it down through the septum until it seats in its journal bore, top flush. The cap's column height sets the standard depth."}
      - {label: "One or both sitting below the cap top", fix: "Unscrew the cap, push the electrode up through the septum until its top is flush, and screw the cap back on."}
      - {label: "Uneven, as the cap will not screw fully on", fix: "Check the septum lies flat across the vial mouth so it compresses evenly."}
---

:::note[LabCrafter kits]
~Struck-through~ items are already done in a LabCrafter kit.
:::

1. ~Seat the silicone septum in the [Vial Cap](../../Components/Vial%20Cap).~
2. ~Push the stainless steel cathode (the rod) up through the septum from below until its top is flush with the top of the cap. Level it with a flat edge.~
3. ~Tighten the thumb screw to hold it in place: firmly, not hard.~ <!-- from video: session-17 0:55:17 - "you tighten that ... not massively"; which fastener is not clear from the transcript; the reviewer named the thumb screw -->
4. ~Repeat with the MMO anode (the tube).~
5. ~Crimp a ring terminal onto each electrode cable.~
6. ~Fix the red cable to the MMO anode: ring terminal, spring washer, then M3 nut.~ <!-- from video: session-17 0:57:04 - this washer order, and the kit's cables came fitted the wrong way round (black on the anode), so they were swapped on camera; the text had "M3 nut and spring washer, tightened by thumb screw" and no flat washer, which is not in the parts list either --> <!-- TODO: add the flat washer to the parts list, or confirm it is part of an existing component | assignee: @Martin -->
7. ~Fix the black cable to the stainless steel cathode the same way.~
8. Check both electrode tops are still flush with the cap top. <!-- TODO: record the AEP0.2 standard depth here once the first build is measured | assignee: @Bingqiao @Amir @Teo @Martin -->
9. Weigh the dry empty vial and record its weight.
10. Fill it to about 30 ml, the working volume, with nutrient solution or bicarbonate of equal ionic strength.
11. Screw the Vial Cap fully onto the vial, compressing the septum evenly.

<!-- VIDEO CUT: session-17 - cut after the Vial Cap is screwed onto the filled vial (item 11), before the electrode distances are recorded; Test electrolysis starts there. -->

<details>
<summary>Notes</summary>

- One septum seals the vial mouth, each electrode and every port, and self-heals sampling-needle tracks. AEP0.2 has no electrode o-rings and no cap o-ring.
- The cap's column height sets each electrode's length and protrusion into the vial, so flush tops give every unit the same standard depth.

</details>
