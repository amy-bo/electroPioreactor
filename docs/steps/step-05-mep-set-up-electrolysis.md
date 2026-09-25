---
id: step-05-mep-set-up-electrolysis
order: 5
title: "Set up electrolysis"
guide: [mep, baep]
parts:
  - {component: vial-cap-oring, qty: 1, cat: printed}
  - {component: cap-o-ring, qty: 1, cat: part}
  - {component: electrode-o-ring, qty: 2, cat: part}
  - {component: stainless-steel-cathode-60mm, qty: 1, cat: part}
  - {component: pt-ti-anode, qty: 1, cat: part}
  - {component: electrode-top-stop, qty: 1, cat: printed}
  - {component: electrode-cable, qty: 2, cat: part}
  - {component: ring-terminal, qty: 2, cat: part}
  - {component: m3-bolt, qty: 2, cat: part}
  - {component: m3-nut, qty: 2, cat: part}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
  - {component: pioreactor-20ml, qty: 1, cat: prev}
tools:
  - {component: hex-key-2-5mm, qty: 1}
  - {component: vernier-callipers, qty: 1}
  - {component: analytical-balance, qty: 1}
  - {component: multimeter, qty: 1}
safety: |
  Fix the red cable to the platinum-plated titanium anode and the black cable to the stainless steel cathode. Never swap them. Reversed, the stainless steel cathode dissolves into the culture.
  Drive the electrodes from the electroPioreactor job, never by setting LED channel D by hand: only the job clamps electrolysis power to 10%.
checks_draft: true
checks:
  - id: polarity
    question: "Is the red cable on the platinum-plated titanium anode and the black on the stainless steel cathode?"
    issues:
      - {problem: "They are the other way round", fix: "Stop electrolysis and swap them now. Reversed, the stainless steel dissolves into the solution."}
  - id: depth
    question: "Are both electrode bases 33 mm below the bottom of the vial cap?"
    issues:
      - {problem: "One is deeper or shallower", fix: "Loosen its M3 bolt, adjust the height with a gentle twist, and tighten again."}
  - id: bubbles
    question: "Within 30 seconds, do both electrodes bubble, the cathode roughly twice as fast as the anode?"
    issues:
      - {problem: "No bubbles", fix: "Check the cables are tight under the ElectrodeTopStop bolts and plugged into LED channel D, and the job is running."}
      - {problem: "The anode bubbles faster", fix: "The cables are swapped: see the first check."}
---

1. Seat the cap O-ring in the [O-ring vial cap](../../Components/Vial%20Cap), and an electrode O-ring in each electrode bore.
2. Push the stainless steel cathode very gently up through the anode's O-ring with a twisting motion, then twist it back out. This eases the O-ring for the more delicate anode.
3. Twist the cathode up through its own O-ring.
4. Unwrap the platinum-plated titanium anode without touching its platinised section, and twist it gently up through its O-ring.
5. Check both electrode O-rings are still seated.
6. Adjust both electrodes so their bases are 33 mm below the bottom of the vial cap. Measure with the vernier callipers.
7. Lay each electrode cable's ring terminal in the [ElectrodeTopStop](../../Components/ElectrodeTopStop) so it will meet its electrode when the bolt is tightened: red on the anode side, black on the cathode side.
8. Push the ElectrodeTopStop down fully onto the electrodes.
9. Tighten the red cable onto the anode with an M3 bolt through the captive M3 nut, using the 2.5 mm hex key: firmly, not hard.
10. Tighten the black cable onto the cathode the same way.
11. Check both bases are still 33 mm below the cap.
12. Weigh the dry empty vial and record its weight.
13. Fill it to 14 ml, the working volume, with nutrient solution or 2 M bicarbonate solution.
14. Screw the vial cap fully onto the vial.
15. Connect the electrodes to LED channel D, catch upwards.
16. Start **electroPioreactor** from **Activities** on the **Manage** screen, with **electrolysis power** at 2.5% in the job's **Settings** panel. Set a long sparge interval until CO₂ is set up.
17. Check bubbles form on both electrodes within 30 seconds, roughly twice as many on the cathode as on the anode: the 2:1 ratio of H₂ to O₂.
18. Measure the voltage across the electrodes with a multimeter on DC volts, probes on the two ring terminals, and record it.
19. Measure the current: break into one electrode lead, put the multimeter in line on the DC mA range, reconnect, and record it.
20. Stop the job, and seat the vial in the Pioreactor.

<details>
<summary>Notes</summary>

- The electrodes are 60 mm long, so 33 mm below the cap puts both well into the 14 ml working volume.
- Check the voltage and current again before and after each experiment. A significant change means recalibrating.
- Overtightening a bolt can crack the ElectrodeTopStop. Stop once the ring terminal is firm against the electrode.
- Graphite electrodes are for testing only. Run them in bicarbonate solution, not nutrient solution, which corrodes them faster.
- Record any loose connection at an ElectrodeTopStop bolt, a change in bubble rate or anode discolouration with the run.

</details>
