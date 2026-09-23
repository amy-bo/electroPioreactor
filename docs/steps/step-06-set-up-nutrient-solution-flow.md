---
id: step-06-set-up-nutrient-solution-flow
order: 6
title: "Set up nutrient solution flow"
guide: [aep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: part}
  - {component: gl45-bottle, qty: 2, cat: part}
  - {component: gl45-cap, qty: 2, cat: part}
  - {component: silicone-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 2, cat: part}
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

1. Follow Pioreactor peristaltic pump setup guide: <https://docs.pioreactor.com/user-guide/using-pumps>
2. Follow the Pioreactor guide to attaching a 12V power supply: <https://docs.pioreactor.com/user-guide/external-power> — the HAT's shunt connector was moved for this during hardware setup; check it before calibrating, because calibrating on the wrong supply means doing it twice.
3. Calibrate peristaltic pumps as per <https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration>
4. Weigh dry empty vial
5. Fill vial with DI water via the pumps, then weigh vials and adjust tube lengths until vial volume is 30ml
6. Measure electrodes immersion depths, if necessary adjust to the standard, and record the insertion depth of each electrode
7. Set up Pioreactor in turbidostat mode: <https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat>
