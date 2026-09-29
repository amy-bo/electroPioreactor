---
id: step-09-set-up-nutrient-solution-flow
order: 9
media: [vid-07-nutrient-solution]
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
checks_draft: true
checks:
  - id: pwm-config
    question: "Under `[PWM]` on the **Configuration** page, what do channels 2 to 4 say?"
    options:
      - {label: "`2=media`, `3=waste`, `4=relay`", correct: true}
      - {label: "`2=waste`, `3=media`, `4=relay`", fix: "That is the MEP's mapping. On the AEP, set 2 to `media` and 3 to `waste`, and click **Save**."}
      - {label: "`2=media`, `3=waste`, `4=waste`", fix: "Set 4 back to `relay`, and click **Save**: the CO₂ solenoid is driven there."}
  - id: pump-leads
    question: "Which PWM channel is the product pump's lead plugged into?"
    options:
      - {label: "PWM 3", correct: true}
      - {label: "PWM 2", fix: "Swap the leads: media pump on PWM 2, product pump on PWM 3."}
      - {label: "PWM 4", fix: "Move it to PWM 3: PWM 4 drives the CO₂ solenoid relay."}
  - id: calibrated-on-12v
    question: "What is plugged into the HAT's barrel jack now?"
    options:
      - {label: "The 12V supply", correct: true}
      - {label: "Nothing: it came out", fix: "Plug the 12V supply back in before you calibrate. Calibrating on the Pi's own supply means calibrating twice."}
---

Follow Pioreactor's [peristaltic pump setup guide](https://docs.pioreactor.com/user-guide/using-pumps), with these channels. Stop before calibrating: that is the next step, once this one's checks pass.

1. On the unit's **Configuration** page, set `[PWM]` channel 3 to `waste`, leave 4 as `relay`, and click **Save**. <!-- from video: session-20 0:05:46 - "we've currently got relay in four ... three then needs to become waste" -->
2. Seat the pumps.
3. Plug the media pump into PWM 2 and the product pump into PWM 3. <!-- from video: session-14 0:07:57 - the product pump is the one labelled "waste" -->
4. Lead the cables out through the notches.
5. Put the media and product bottles into their holders, with a 0.2 μm vent filter on each GL45 cap's vent port.
6. Connect each bottle to its pump with the silicone tubing and luer fittings. <!-- TODO: add a connector diagram (which luer goes where; male ends mark outlets) - the recording stalled on it (session-20 0:08:20-0:13:04) | assignee: @Martin -->

   :::note
   The kit's in-line parts on the media lines are non-return valves, not filters. <!-- from video: session-20 0:12:45 -->
   :::
7. Check the 12V supply is in the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)). The shunt was checked in [Raspberry Pi and HAT](step-03-raspberry-pi-and-hat.md).

   :::caution
   Calibrate only after this. Calibrating on the wrong supply means calibrating twice.
   :::

<!-- VIDEO CUT: session-20 - cut after the 12V check (item 7), before pump calibration; Calibrate the pumps starts there. -->
