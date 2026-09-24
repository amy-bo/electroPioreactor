---
id: step-06-set-up-nutrient-solution-flow
order: 6
title: "Nutrient solution"
guide: [aep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: part}
  - {component: gl45-bottle, qty: 2, cat: part}
  - {component: gl45-cap, qty: 2, cat: part}
  - {component: silicone-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 2, cat: part}
  - {component: hydrophobic-vent-filter, qty: 2, cat: part}
  - {component: power-supply-12v, qty: 1, cat: prev}
  - {component: pioreactor-vial-40ml, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
  - {component: vernier-callipers, qty: 1}
checks_draft: true
checks:
  - id: calibrated-on-12v
    question: "Were the pumps calibrated with the 12V supply connected and the HAT's shunt moved?"
    issues:
      - {problem: "They were calibrated before the shunt was moved or the 12V supply connected", fix: "Move the shunt (see hardware setup), connect the 12V supply, and calibrate again: calibrating on the wrong supply means doing it twice."}
  - id: thirty-ml
    question: "Weighed against the dry empty vial, does the vial hold 30 ml when filled with DI water via the pumps?"
    issues:
      - {problem: "The volume is not 30 ml", fix: "Adjust the tube lengths and re-weigh until it is."}
  - id: immersion-recorded
    question: "Are both electrodes at the standard immersion depth, and is each insertion depth recorded?"
    issues:
      - {problem: "A depth is off", fix: "Adjust it to the standard and record the new insertion depth."}
---

Follow Pioreactor's [peristaltic pump setup guide](https://docs.pioreactor.com/user-guide/using-pumps), with these channels.

1. On the unit's **Configuration** page, set `[PWM]` channel 3 to `waste`, leave 4 as `relay`, and save. <!-- from video: session-20 0:05:46 - "we've currently got relay in four ... three then needs to become waste" -->
2. Seat the pumps, plug the media pump into PWM 2 and the product pump into PWM 3, and lead the cables out through the notches. <!-- from video: session-14 0:07:57 - the product pump is the one labelled "waste" -->
3. Put the media and product bottles into their holders, with a 0.2 μm vent filter on each cap's vent port.
4. Connect each bottle to its pump with the silicone tubing and luer fittings. <!-- TODO: add a connector diagram (which luer goes where; male ends mark outlets) - the recording stalled on it (session-20 0:08:20-0:13:04) | assignee: @Martin -->
5. Check the 12V supply is in the HAT's barrel jack and the shunt moved ([external power](https://docs.pioreactor.com/user-guide/external-power)) before calibrating.
6. [Calibrate the pumps](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration).
7. Weigh the dry empty vial.
8. Fill the vial with DI water via the pumps, weigh it, and adjust the tube lengths until it holds 30 ml.
9. Measure the electrode immersion depths, adjust to the standard if necessary, and record each insertion depth.
10. Set up the Pioreactor in [turbidostat mode](https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat).

<details>
<summary>Notes</summary>

- Calibrating on the wrong supply means calibrating twice.
- The kit's in-line parts on the media lines are non-return valves, not filters. <!-- from video: session-20 0:12:45 -->

</details>
