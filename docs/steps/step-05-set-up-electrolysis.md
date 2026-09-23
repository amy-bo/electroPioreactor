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
  - {component: vernier-callipers, qty: 1}
  - {component: multimeter, qty: 1}
renders:
  - {id: vial-cap-iso, component: vial-cap, view: iso, explode: false, format: png}
  - {id: vial-cap-exploded, component: vial-cap, view: iso, explode: true, format: png}
viewer: {component: vial-cap, format: glb}
safety: |
  Fix the red cable's ring terminal to the MMO anode and the black cable's ring terminal to the stainless steel cathode. BoM 3.3: "Colour-code red anode, black cathode, and never swap." BoM 2.2: the stainless steel cathode "Must stay strictly cathodic: reversed, stainless corrodes quickly and leaches Cr, Ni and Fe into the culture."
  Drive the electrodes from this job rather than setting LED channel D by hand: the job clamps electrolysis power to 10% at runtime, and nothing does so if you drive the channel directly.
checks_draft: true
checks:
  - id: polarity
    question: "Is the red cable fixed to the MMO anode (the tube) and the black cable to the stainless steel cathode (the rod)?"
    issues:
      - {problem: "They are swapped", fix: "Stop the job and swap the ring terminals before driving the electrodes again. Reversed, the stainless steel corrodes quickly and leaches Cr, Ni and Fe into the culture."}
  - id: bubbles
    question: "With electroPioreactor running, do roughly twice as many bubbles form on the cathode as on the anode?"
    issues:
      - {problem: "No bubbles on either electrode", fix: "Check the electrodes are connected to LED channel D (catch upwards), the vial holds nutrient solution or bicarbonate of equal ionic strength, and the job was started from the Activities tab."}
      - {problem: "More bubbles on the anode than the cathode", fix: "The leads are probably reversed: stop the job and check the red lead is on the anode and the black lead on the cathode."}
      - {problem: "Bubbling is weak", fix: "Adjust electrolysis power in the job's Settings panel rather than setting LED channel D by hand: the job clamps power to 10% to protect the electrodes."}
  - id: depth
    question: "With the cap fully screwed on and the septum compressed evenly, are the electrode tops flush with the top of the vial cap?"
    issues:
      - {problem: "An electrode sits proud of or below the cap top", fix: "Push it through the septum until it seats in its journal bore with its top flush: the cap's column height sets the standard depth."}
      - {problem: "The cap will not screw fully on", fix: "Check the septum lies flat across the vial mouth so it compresses evenly."}
---

NOTE: ~struck through~ lines will already have been completed if you received a kit from LabCrafter

1. ~Seat the silicone septum in the [Vial Cap](../../Components/Vial%20Cap)~

   <details>
   <summary>What the septum replaced</summary>

   One sheet seals the vial mouth, each electrode and every port, and self-heals sampling-needle tracks. There are no electrode o-rings and no cap o-ring in AEP0.2.

   </details>
2. ~Push each electrode through the septum and up into its journal bore in the one-piece cap and electrode holder~ — the MMO anode is the tube, the stainless steel rod is the cathode.
3. ~Crimp a ring terminal onto each electrode cable~
4. ~Fix the red cable's ring terminal to the MMO anode with an M3 nut and spring washer, tightened by thumb screw~
5. ~Fix the black cable's ring terminal to the stainless steel cathode the same way~
6. ~Set the electrode insertion depth. The holder is parametric: the column height already sets the electrode length and the protrusion into the vial, so the electrodes seat at the standard depth if their tops are flush with the top of the vial cap.~ <!-- TODO: record the AEP0.2 standard depth here once the first build is measured | assignee: @Bingqiao @Amir @Teo @Martin -->
7. Add nutrient solution (or equal ionic strength bicarbonate) to the Vial
8. Fully screw the Vial Cap onto the Vial, compressing the septum evenly
9. The electrodes should now protrude into the vial to the standard depth
10. Record the distance from the plane of the top of the Vial Cap to the bottom of each electrode.
11. Connect the electrodes to LED channel D (catch upwards)
12. With electrolyte solution in the Vial, start **electroPioreactor** from the **Activities** tab of the *Manage* screen and verify that roughly twice as many bubbles form on the cathode as on the anode. Drive the electrodes from this job rather than setting LED channel D by hand: the electroPioreactor limits electrolysis power to 10% to avoid damage to the electrodes. Set a long sparge interval so the relay is not actuating into thin air, until CO₂ is set up in a later step.
13. Record the voltage across each electrode and the current through them, adjusting **electrolysis power** in the job's **Settings** panel to reach the standard values if necessary
14. Insert vial into Pioreactor once satisfied all vials have even electrolysis
