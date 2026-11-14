---
id: step-06-mep-test-electrolysis
order: 6
title: "Test electrolysis"
guide: [mep, baep]
parts:
  - {component: vial-cap-oring, qty: 1, cat: prev}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
  - {component: pioreactor-20ml, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
  - {component: multimeter, qty: 1}
safety: |
  Drive the electrodes from the electroPioreactor job, never by setting LED channel D by hand: only the job clamps electrolysis power to 10%.
checks_draft: true
checks:
  - id: bubbles
    question: "Within 30 seconds of starting the job, where do the bubbles form?"
    options:
      - {label: "On both, about twice as fast on the cathode", correct: true}
      - {label: "On both, about twice as fast on the anode", fix: "The cables are swapped. Stop the job and swap them as in the first check of **Set up electrolysis**."}
      - {label: "On neither: no bubbles after 30 seconds", fix: "Check the cables are tight under the ElectrodeTopStop bolts and plugged into LED channel D, and the job is running."}
---

The electrodes were fitted, and their polarity and depth checked, in [Set up electrolysis](step-05-mep-set-up-electrolysis.md).

1. Weigh the dry empty vial and record its weight.
2. Fill it to 14 ml, the working volume, with nutrient solution or 2 M bicarbonate solution.
3. Screw the vial cap fully onto the vial.
4. Connect the electrodes to LED channel D, catch upwards.
5. Start **electroPioreactor** from **Activities** on the **Manage** screen, with **electrolysis power** at 2.5% in the job's **Settings** panel. Set a long sparge interval until CO₂ is set up.
6. Check bubbles form on both electrodes within 30 seconds, roughly twice as many on the cathode as on the anode: the 2:1 ratio of H₂ to O₂.
7. Measure the voltage across the electrodes with a multimeter on DC volts, probes on the two ring terminals, and record it.
8. Measure the current: break into one electrode lead, put the multimeter in line on the DC mA range, reconnect, and record it.
9. Stop the job, and seat the vial in the Pioreactor.

<details>
<summary>Notes</summary>

- Check the voltage and current again before and after each experiment. A significant change means recalibrating.
- Graphite electrodes are for testing only. Run them in bicarbonate solution, not nutrient solution, which corrodes them faster.
- Record any loose connection at an ElectrodeTopStop bolt, a change in bubble rate or anode discolouration with the run.

</details>
