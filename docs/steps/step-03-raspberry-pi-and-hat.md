---
id: step-03-raspberry-pi-and-hat
order: 3
media: [vid-03-hardware-setup]
title: "Raspberry Pi and HAT"
guide: [aep]
parts:
  - {component: pioreactor-40ml, qty: 1, cat: part}
  - {component: raspberry-pi, qty: 1, cat: part}
  - {component: usb-c-power-supply, qty: 1, cat: part}
tools:
  - {component: phillips-ph0-screwdriver, qty: 1}
checks_draft: true
checks:
  - id: shunt-moved
    question: "Where is the HAT's shunt connector now?"
    options:
      - {label: "On the two pins closest to the LED outputs", correct: true}
      - {label: "On the two pins furthest from the LED outputs", fix: "Move it one pin along, to the two pins closest to the LED outputs, now, while the HAT is bare."}
      - {label: "Off the HAT, not on any of its pins", fix: "Find it and fit it on the two pins closest to the LED outputs, now, while the HAT is bare."}
---

Follow Pioreactor's [40 ml v1.5 hardware setup guide](https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro), with these changes. This step stops at the bare HAT: the vial holder assembly, in the next step, covers the shunt connector.

1. [Assemble the Raspberry Pi and the HAT](https://docs.pioreactor.com/user-guide/40ml-v15-rpi-hat-assembly) on a Raspberry Pi 5 1GB. Use the kit's 8 mm screws where the guide says 10 mm, with a hex nut on all four. <!-- from video: session-15 0:03:45 - the kit had 8 mm screws, not the 10 mm the guide names -->
2. **Move the HAT's shunt connector to the position closest to the LED outputs, now, while the HAT is bare** ([external power](https://docs.pioreactor.com/user-guide/external-power)). <!-- from video: session-15 0:11:31 - Martin describes it as bridging "the two closest to the power supply"; Pioreactor's external-power page says "closest to the LED outputs", kept here -->

   :::caution[Miss this and you take the unit apart again]
   No error shows. PWM channels 1 to 4 ignore the 12V supply, so the peristaltic pumps and the PWM 4 CO₂ solenoid run on the Pi's own supply. The solenoid will not drive, and sparging looks like a gas train fault. Moving the shunt later also invalidates any stirring and pump calibration.
   :::

<!-- Video: vid-03-hardware-setup plays to 9:50 (end_s); the next step plays the rest. -->
