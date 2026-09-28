---
id: step-08-mep-nutrient-solution
order: 8
title: "Nutrient solution"
guide: [mep, baep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: part}
  - {component: gl45-bottle, qty: 2, cat: part}
  - {component: gl45-cap, qty: 2, cat: part}
  - {component: silicone-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 2, cat: part}
  - {component: power-supply-12v, qty: 1, cat: prev}
  - {component: vial-cap-oring, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: channels
    question: "Under `[PWM]` on the **Configuration** page, what do channels 2 to 4 say?"
    options:
      - {label: "`2=waste`, `3=media`, `4=relay`", correct: true}
      - {label: "`2=media`, `3=waste`, `4=relay`", fix: "That is Pioreactor's own example, and the AEP's mapping. On the MEP, 2 is the waste pump and 3 the media pump: set them and click **Save**."}
      - {label: "`2=waste`, `3=media`, `4=waste`", fix: "Set 4 back to `relay`, and click **Save**: the CO₂ solenoid is driven there."}
  - id: pump-leads
    question: "Which PWM channel is the media pump's lead plugged into?"
    options:
      - {label: "PWM 3", correct: true}
      - {label: "PWM 2", fix: "Swap the leads: product (waste) pump on PWM 2, media pump on PWM 3."}
      - {label: "PWM 4", fix: "Move it to PWM 3: PWM 4 drives the CO₂ solenoid relay."}
  - id: calibrated-on-12v
    question: "What is plugged into the HAT's barrel jack now?"
    options:
      - {label: "The 12 V supply", correct: true}
      - {label: "Nothing: it came out", fix: "Plug the 12 V supply back in (see **Pioreactor hardware setup**) before you calibrate. Calibrating on the Pi's own supply means calibrating twice."}
---

Follow Pioreactor's [peristaltic pump setup guide](https://docs.pioreactor.com/user-guide/using-pumps), with these channels. Stop before calibrating: that is the next step, once this one's checks pass.

1. On the unit's **Configuration** page, set `[PWM]` channel 2 to `waste` and 3 to `media`, leave 4 as `relay`, and click **Save**.

   :::note
   Pioreactor's pump guide uses PWM 2 for a media pump as an example. On the MEP, keep 2 for waste (product) and 3 for media.
   :::
2. Seat the pumps.
3. Plug the product pump into PWM 2 and the media pump into PWM 3.
4. Lead the cables out through the notches.
5. Put the media and product bottles, with their GL45 caps, into their holders.
6. Connect each bottle to its pump with the silicone tubing and luer fittings, then each pump to its tube on the vial cap: media to Media In, waste to Media Out.
7. Check the 12 V supply is in the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)).

   :::caution
   Calibrate only after this. Calibrating on the wrong supply means calibrating twice.
   :::
