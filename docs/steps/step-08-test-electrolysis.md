---
id: step-08-test-electrolysis
order: 8
title: "Test electrolysis"
guide: [aep]
parts:
  - {component: vial-cap, qty: 1, cat: prev}
  - {component: pioreactor-vial-40ml, qty: 1, cat: prev}
  - {component: pioreactor-40ml, qty: 1, cat: prev}
tools:
  - {component: vernier-callipers, qty: 1}
  - {component: multimeter, qty: 1}
safety: |
  Drive the electrodes from the electroPioreactor job, never by setting LED channel D by hand: only the job clamps electrolysis power to 10%.
checks_draft: true
checks:
  - id: bubbles
    question: "With electroPioreactor running, where do the bubbles form?"
    options:
      - {label: "On both, about twice as many on the cathode", correct: true}
      - {label: "On both, about twice as many on the anode", fix: "The leads are probably reversed. Stop the job and check red is on the anode, black on the cathode."}
      - {label: "On both, but only a few, and slowly", fix: "Raise electrolysis power in the job's **Settings** panel, not by setting LED channel D by hand: the job clamps power to 10% to protect the electrodes."}
      - {label: "On neither: no bubbles at all", fix: "Check the electrodes are on LED channel D (catch upwards), the vial holds nutrient solution or bicarbonate of equal ionic strength, and the job was started from **Activities**."}
---

1. Record the distance from the top of the Vial Cap to the bottom of each electrode.
2. Connect the electrodes to LED channel D, catch upwards.
3. Start **electroPioreactor** from **Activities** on the **Manage** screen. Set a long sparge interval until CO₂ is set up.
4. Raise **electrolysis power** in the job's **Settings** panel until bubbles form. <!-- from video: session-17 1:18 (file 023 35:00-39:00) - power raised from 2.5 to 3.5% -->
5. Check roughly twice as many bubbles form on the cathode as on the anode.
6. Measure the voltage across the electrodes with a multimeter, and record it. <!-- from video: session-18 0:03:28 - 2.82 V at 3.5%; current not measured, as it needs a lead broken into -->
7. If you can break into a lead, measure and record the current too.
8. Insert the vial into the Pioreactor once all vials show even electrolysis.

<details>
<summary>Notes</summary>

- If the unit misbehaves before electrolysis starts (fan starting and stopping, no response), run a self test from its **Manage** screen. Power-cycle it if that hangs.

</details>
