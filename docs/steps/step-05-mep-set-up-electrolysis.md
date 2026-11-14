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
tools:
  - {component: hex-key-2-5mm, qty: 1}
  - {component: vernier-callipers, qty: 1}
safety: |
  Fix the red cable to the platinum-plated titanium anode and the black cable to the stainless steel cathode. Never swap them. Reversed, the stainless steel cathode dissolves into the culture.
checks_draft: true
checks:
  - id: polarity
    question: "Which electrode is the red cable bolted onto?"
    options:
      - {label: "The platinum-plated titanium anode", correct: true}
      - {label: "The stainless steel cathode", fix: "Swap the cables now, before anything drives the electrodes: loosen both M3 bolts, swap the ring terminals, and tighten again, firmly, not hard. Reversed, the stainless steel dissolves into the solution."}
  - id: depth
    question: "Measured with the callipers, how far below the bottom of the vial cap are the electrode bases?"
    options:
      - {label: "Both 33 mm", correct: true}
      - {label: "One or both less than 33 mm", fix: "Loosen its M3 bolt, lower it to 33 mm with a gentle twist, and tighten again."}
      - {label: "One or both more than 33 mm", fix: "Loosen its M3 bolt, raise it to 33 mm with a gentle twist, and tighten again."}
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

<details>
<summary>Notes</summary>

- The electrodes are 60 mm long, so 33 mm below the cap puts both well into the 14 ml working volume.
- Overtightening a bolt can crack the ElectrodeTopStop. Stop once the ring terminal is firm against the electrode.

</details>
