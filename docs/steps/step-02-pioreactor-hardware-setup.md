---
id: step-02-pioreactor-hardware-setup
order: 2
title: "Follow the Pioreactor 40 ml v1.5 hardware setup guide"
guide: [aep]
parts:
  - {component: pioreactor-40ml, qty: 1, cat: part}
  - {component: raspberry-pi, qty: 1, cat: part}
  - {component: usb-c-power-supply, qty: 1, cat: part}
  - {component: pioreactor-vial-40ml, qty: 1, cat: part}
  - {component: stir-bar, qty: 1, cat: part}
  - {component: eye-spy, qty: 2, cat: part}
  - {component: optics-cover, qty: 3, cat: part}
  - {component: screw-8mm, qty: 12, cat: part}
  - {component: led-cap, qty: 1, cat: part}
  - {component: stemma-qt-wire, qty: 1, cat: part}
  - {component: xr-upgrade-kit, qty: 1, cat: part}
  - {component: xr-top-vial-holder, qty: 1, cat: part}
  - {component: xr-o-ring, qty: 1, cat: part}
  - {component: precision-temperature-upgrade-kit, qty: 1, cat: part, when: {temp-kit: true}}
  - {component: power-supply-12v, qty: 1, cat: part}
tools:
  - {component: phillips-ph0-screwdriver, qty: 1}
checks_draft: true
checks:
  - id: shunt-moved
    question: "Was the HAT's shunt connector moved to the position closest to the LED outputs before the vial holder assembly was mounted?"
    issues:
      - {problem: "The shunt was not moved and the unit is already assembled", fix: "Take the unit apart far enough to reach the shunt and move it now. Otherwise PWM channels 1 to 4 ignore the 12V supply and the CO₂ solenoid will not drive."}
      - {problem: "Stirring or pumps were calibrated before the shunt was moved", fix: "Moving the shunt invalidates those calibrations: redo them."}
  - id: xr-not-v15-optics
    question: "Is the XR upgrade kit fitted, with the v1.5 optics left out?"
    issues:
      - {problem: "The v1.5 optics were fitted", fix: "Work through the XR disassembly guide linked in sub-step 3 to recover the parts the XR assembly reuses, then fit the XR kit."}
  - id: temp-sensor-seated
    when: {temp-kit: true}
    question: "Is the Precision Temperature Upgrade Kit's sensor seated in the SPEC position and chained off the nearest eye-spy over STEMMA-QT?"
    issues:
      - {problem: "The sensor is elsewhere or not connected", fix: "Reseat it following the Precision Temperature Upgrade Kit guide linked after sub-step 6."}
  - id: twelve-volt-connected
    question: "Is the 12V supply plugged into the HAT's barrel jack?"
    issues:
      - {problem: "It is not connected", fix: "Connect it: the solenoid needs more power than the Pi alone can supply, and without it the CO₂ sparging step will look like a gas train fault rather than a power one."}
---

Follow Pioreactor's [40 ml v1.5 hardware setup guide](https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro), with these changes.

1. [Assemble the Raspberry Pi and the HAT](https://docs.pioreactor.com/user-guide/40ml-v15-rpi-hat-assembly) on a Raspberry Pi 5 1GB, using the kit's 8 mm screws where the guide says 10 mm, and a hex nut on all four (two for a Zero 2W). <!-- from video: session-15 0:03:45 - the kit had 8 mm screws, not the 10 mm the guide names -->
2. **Move the HAT's shunt connector to the position closest to the LED outputs, now, while the HAT is bare** ([external power](https://docs.pioreactor.com/user-guide/external-power)). <!-- from video: session-15 0:11:31 - Martin describes it as bridging "the two closest to the power supply"; Pioreactor's external-power page says "closest to the LED outputs", kept here -->

   <details>
   <summary>What happens if you miss it</summary>

   Nothing errors. The 12V supply is simply ignored by PWM channels 1 to 4, so the peristaltic pumps and the PWM 4 CO₂ solenoid stay on the Raspberry Pi's own supply: the solenoid will not drive, and CO₂ sparging will look like a gas train fault rather than a power one. Moving the shunt also invalidates any stirring and pump calibration made before it. Once the vial holder assembly is mounted you have to take the unit apart again to reach it.

   </details>
3. **Do not fit the v1.5 optics.** Keep those parts aside for the XR kit.

   <details>
   <summary>Why, and which of those parts the XR kit reuses</summary>

   AEP0.2 is XR from the start, and the XR upgrade would only have you strip the v1.5 optics straight back out. The XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire out of the v1.5 kit; the XR kit supplies the remaining eye-spys, its own top vial holder and the O-ring. If instead you are upgrading a Pioreactor that is already built, work through [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those same parts.

   </details>
4. [Wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly): set the vial's own cap aside, skip the stainless steel ports, fit the X-section o-ring into the XR top vial holder and the round o-ring into the bottom vial holder.
5. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly): each eye-spy under an optics cover with four 8 mm screws (0x4B at 45°, white-marked at REF, unmarked at 90°, the last at 135°), then the heater PCB, thermal pad, LED and LED cap, and the STEMMA-QT chain with the yellow wire down.
6. [Attach the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together): four screws into the square nuts until flush and no further, the 10 mm screw under the button extension, four 8 mm corner screws, the flat flex cable into the orange connector, and the stirrer into PWM channel 1.

<!-- when temp-kit=true -->

**If you have the Precision Temperature Upgrade Kit:** [fit it](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit): lift the cover off the SPEC position, run the STEMMA-QT wire from the sensor PCB to the nearest eye-spy, and seat the sensor in SPEC with its LED pad to the right.

<!-- /when -->

7. Connect the 12V supply to the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)).

<details>
<summary>Notes</summary>

- XR gives 45° and 135° scattering in addition to 90°, for a lower OD detection limit and earlier indication of growth.
- If a square-nut screw meets resistance, back it out and check its tip for plastic debris before driving it home.
- The Precision Temperature kit's MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. Its optional screws may not fit past the STEMMA-QT cable.
- Four or more Pioreactors on one bench can run from a single multi-port charger rather than one supply each: see [powering a cluster](https://docs.pioreactor.com/user-guide/powering-cluster).

</details>
