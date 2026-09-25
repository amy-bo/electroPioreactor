---
id: step-02-pioreactor-hardware-setup
order: 2
title: "Pioreactor hardware setup"
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
    question: "Did you move the HAT's shunt connector to the position closest to the LED outputs before mounting the vial holder assembly?"
    issues:
      - {problem: "The shunt was not moved and the unit is already assembled", fix: "Take the unit apart far enough to reach the shunt, and move it now. Otherwise PWM channels 1 to 4 ignore the 12V supply and the CO₂ solenoid will not drive."}
      - {problem: "Stirring or pumps were calibrated before the shunt was moved", fix: "Moving the shunt invalidates those calibrations. Redo them."}
  - id: xr-not-v15-optics
    question: "Is the XR upgrade kit fitted, with the v1.5 optics left out?"
    issues:
      - {problem: "The v1.5 optics were fitted", fix: "Follow the XR disassembly guide linked in item 3 to recover the parts the XR assembly reuses, then fit the XR kit."}
  - id: temp-sensor-seated
    when: {temp-kit: true}
    question: "Is the Precision Temperature Upgrade Kit's sensor seated in the SPEC position and chained off the nearest eye-spy over STEMMA-QT?"
    issues:
      - {problem: "The sensor is elsewhere or not connected", fix: "Reseat it using the Precision Temperature Upgrade Kit guide linked after item 6."}
  - id: twelve-volt-connected
    question: "Is the 12V supply plugged into the HAT's barrel jack?"
    issues:
      - {problem: "It is not connected", fix: "Connect it. The solenoid needs more power than the Pi can supply; without it, CO₂ sparging fails like a gas train fault rather than a power one."}
---

Follow Pioreactor's [40 ml v1.5 hardware setup guide](https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro), with these changes.

1. [Assemble the Raspberry Pi and the HAT](https://docs.pioreactor.com/user-guide/40ml-v15-rpi-hat-assembly) on a Raspberry Pi 5 1GB. Use the kit's 8 mm screws where the guide says 10 mm, with a hex nut on all four (two for a Zero 2W). <!-- from video: session-15 0:03:45 - the kit had 8 mm screws, not the 10 mm the guide names -->
2. **Move the HAT's shunt connector to the position closest to the LED outputs, now, while the HAT is bare** ([external power](https://docs.pioreactor.com/user-guide/external-power)). <!-- from video: session-15 0:11:31 - Martin describes it as bridging "the two closest to the power supply"; Pioreactor's external-power page says "closest to the LED outputs", kept here -->

   :::caution[Miss this and you take the unit apart again]
   Nothing errors. PWM channels 1 to 4 ignore the 12V supply, so the peristaltic pumps and the PWM 4 CO₂ solenoid run on the Pi's own supply. The solenoid will not drive, and sparging looks like a gas train fault. Moving the shunt later also invalidates any stirring and pump calibration.
   :::
3. **Do not fit the v1.5 optics.** Keep those parts for the XR kit.

   <details>
   <summary>Why, and which of those parts the XR kit reuses</summary>

   AEP0.2 is XR from the start; the XR upgrade would only have you strip the v1.5 optics back out. From the v1.5 kit, the XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire. The XR kit supplies the other eye-spys, its own top vial holder and the O-ring. Upgrading a Pioreactor that is already built? Follow [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those parts.

   </details>
4. [Wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly), with these changes. Set the vial's own cap aside and skip the stainless steel ports. Fit the X-section o-ring into the XR top vial holder and the round o-ring into the bottom vial holder.
5. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly). Fix each eye-spy under an optics cover with four 8 mm screws: 0x4B at 45°, white-marked at REF, unmarked at 90°, the last at 135°. Fit the heater PCB, thermal pad, LED and LED cap, then connect the STEMMA-QT chain, yellow wire down.
6. [Attach the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together). Drive four screws into the square nuts until flush, and no further. Fit the 10 mm screw under the button extension and the four 8 mm corner screws, push the flat flex cable into the orange connector, and plug the stirrer into PWM channel 1.

<!-- when temp-kit=true -->

**If you have the Precision Temperature Upgrade Kit**, [fit it](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit). Lift the cover off the SPEC position, run the STEMMA-QT wire from the sensor PCB to the nearest eye-spy, and seat the sensor in SPEC, LED pad to the right.

<!-- /when -->

7. Connect the 12V supply to the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)).

<details>
<summary>Notes</summary>

- XR adds 45° and 135° scattering to 90°, for a lower OD detection limit and earlier signs of growth.
- If a square-nut screw meets resistance, back it out and check its tip for plastic debris before driving it home.
- The Precision Temperature kit's MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. Its optional screws may not fit past the STEMMA-QT cable.
- Four or more Pioreactors on one bench can share one multi-port charger instead of one supply each: see [powering a cluster](https://docs.pioreactor.com/user-guide/powering-cluster).

</details>
