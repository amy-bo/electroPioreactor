---
id: step-05-set-up-electrolysis
order: 5
title: "Set up electrolysis"
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
  - {component: pioreactor-40ml, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
  - {component: vernier-callipers, qty: 1}
  - {component: multimeter, qty: 1}
renders:
  - {id: vial-cap-iso, component: vial-cap, view: iso, explode: false, format: png}
  - {id: vial-cap-exploded, component: vial-cap, view: iso, explode: true, format: png}
viewer: {component: vial-cap, format: glb}
safety: |
  Fix the red cable's ring terminal to the MMO anode and the black cable's to the stainless steel cathode. Never swap them. Reversed, the stainless steel cathode corrodes quickly and leaches Cr, Ni and Fe into the culture.
  Drive the electrodes from the electroPioreactor job, never by setting LED channel D by hand: only the job clamps electrolysis power to 10%.
checks_draft: true
checks:
  - id: polarity
    question: "Is the red cable fixed to the MMO anode (the tube) and the black cable to the stainless steel cathode (the rod)?"
    issues:
      - {problem: "They are swapped", fix: "Stop the job and swap the ring terminals before driving the electrodes again. Reversed, the stainless steel corrodes quickly and leaches Cr, Ni and Fe into the culture."}
  - id: bubbles
    question: "With electroPioreactor running, do roughly twice as many bubbles form on the cathode as on the anode?"
    issues:
      - {problem: "No bubbles on either electrode", fix: "Check the electrodes are on LED channel D (catch upwards), the vial holds nutrient solution or bicarbonate of equal ionic strength, and the job was started from **Activities**."}
      - {problem: "More bubbles on the anode than the cathode", fix: "The leads are probably reversed. Stop the job and check red is on the anode, black on the cathode."}
      - {problem: "Bubbling is weak", fix: "Raise electrolysis power in the job's **Settings** panel, not by setting LED channel D by hand: the job clamps power to 10% to protect the electrodes."}
  - id: depth
    question: "With the cap fully screwed on and the septum compressed evenly, are the electrode tops flush with the top of the vial cap?"
    issues:
      - {problem: "An electrode sits proud of or below the cap top", fix: "Push it through the septum until it seats in its journal bore, top flush. The cap's column height sets the standard depth."}
      - {problem: "The cap will not screw fully on", fix: "Check the septum lies flat across the vial mouth so it compresses evenly."}
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
12. Record the distance from the top of the Vial Cap to the bottom of each electrode.
13. Connect the electrodes to LED channel D, catch upwards.
14. Start **electroPioreactor** from **Activities** on the **Manage** screen. Set a long sparge interval until CO₂ is set up.
15. Raise **electrolysis power** in the job's **Settings** panel until bubbles form. <!-- from video: session-17 1:18 (file 023 35:00-39:00) - power raised from 2.5 to 3.5% -->
16. Check roughly twice as many bubbles form on the cathode as on the anode.
17. Measure the voltage across the electrodes with a multimeter, and record it. <!-- from video: session-18 0:03:28 - 2.82 V at 3.5%; current not measured, as it needs a lead broken into -->
18. If you can break into a lead, measure and record the current too.
19. Insert the vial into the Pioreactor once all vials show even electrolysis.

<details>
<summary>Notes</summary>

- One septum seals the vial mouth, each electrode and every port, and self-heals sampling-needle tracks. AEP0.2 has no electrode o-rings and no cap o-ring.
- The cap's column height sets each electrode's length and protrusion into the vial, so flush tops give every unit the same standard depth.
- If the unit misbehaves before electrolysis starts (fan starting and stopping, no response), run a self test from its **Manage** screen. Power-cycle it if that hangs.

</details>
