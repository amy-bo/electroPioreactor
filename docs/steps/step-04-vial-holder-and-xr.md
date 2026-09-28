---
id: step-04-vial-holder-and-xr
order: 4
title: "Vial holder and XR optics"
guide: [aep]
parts:
  - {component: pioreactor-40ml, qty: 1, cat: prev}
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
  - id: xr-not-v15-optics
    question: "How many eye-spys are fitted around the vial holder?"
    options:
      - {label: "Four", correct: true}
      - {label: "Two", fix: "Those are the v1.5 optics. Recover the parts the XR assembly reuses with the XR disassembly guide (linked under **Do not fit the v1.5 optics**), then fit the XR kit."}
      - {label: "Three", fix: "One is missing. The XR kit has four positions: 45°, REF, 90° and 135°."}
  - id: eye-spy-0x4b
    question: "Which position holds the eye-spy labelled 0x4B?"
    options:
      - {label: "45°", correct: true}
      - {label: "REF", fix: "Swap them round: 0x4B at 45°, the white-marked one at REF, the unmarked one at 90°, the last at 135°."}
      - {label: "90°", fix: "Swap them round: 0x4B at 45°, the white-marked one at REF, the unmarked one at 90°, the last at 135°."}
      - {label: "135°", fix: "Swap them round: 0x4B at 45°, the white-marked one at REF, the unmarked one at 90°, the last at 135°."}
  - id: temp-sensor-seated
    when: {temp-kit: true}
    question: "How is the Precision Temperature Upgrade Kit's sensor fitted?"
    options:
      - {label: "In SPEC, LED pad to the right, wired to the nearest eye-spy", correct: true}
      - {label: "In SPEC, LED pad to the left, wired to the nearest eye-spy", fix: "Turn it round so the LED pad is to the right."}
      - {label: "In SPEC, LED pad to the right, with no STEMMA-QT wire", fix: "Run the STEMMA-QT wire from the sensor PCB to the nearest eye-spy."}
  - id: twelve-volt-connected
    question: "What is plugged into the HAT's barrel jack?"
    options:
      - {label: "The 12V supply", correct: true}
      - {label: "Nothing yet", fix: "Plug in the 12V supply. The solenoid needs more power than the Pi supplies; without it, sparging fails and looks like a gas train fault."}
---

Carry on with Pioreactor's [40 ml v1.5 hardware setup guide](https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro), with these changes. The shunt must already pass its check in [Raspberry Pi and HAT](step-03-raspberry-pi-and-hat.md): item 4 here covers it.

1. **Do not fit the v1.5 optics.** Keep those parts for the XR kit.

   <details>
   <summary>Why, and which of those parts the XR kit reuses</summary>

   AEP0.2 is XR from the start; the XR upgrade would only have you strip the v1.5 optics back out. From the v1.5 kit, the XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire. The XR kit supplies the other eye-spys, its own top vial holder and the O-ring. Upgrading a Pioreactor that is already built? Follow [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those parts.

   </details>
2. Follow the [wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly), with these changes: set the vial's own cap aside and skip the stainless steel ports. Fit the X-section o-ring into the XR top vial holder and the round o-ring into the bottom vial holder.
3. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly). Fix each eye-spy under an optics cover with four 8 mm screws: the one labelled 0x4B at 45°, the white-marked one at REF, the unmarked one at 90°, the last at 135°. Fit the heater PCB, thermal pad, LED and LED cap, then connect the STEMMA-QT chain, yellow wire down.
4. [Attach the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together). Drive four screws into the square nuts until flush, and no further. Fit the 10 mm screw under the button extension and the four 8 mm corner screws, push the flat flex cable into the orange connector, and plug the stirrer into PWM channel 1.
5. Connect the 12V supply to the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)).

<!-- when temp-kit=true -->

**If you have the Precision Temperature Upgrade Kit**, [fit it](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit). Lift the cover off the SPEC position, run the STEMMA-QT wire from the sensor PCB to the nearest eye-spy, and seat the sensor in SPEC, LED pad to the right.

<!-- /when -->

<!-- VIDEO CUT: session-15 - this step starts after the shunt is moved (0:11:31). -->

<details>
<summary>Notes</summary>

- XR adds 45° and 135° scattering to 90°, for a lower OD detection limit and earlier signs of growth.
- If a square-nut screw meets resistance, back it out and check its tip for plastic debris before driving it home.
- The Precision Temperature kit's MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. Its optional screws may not fit past the STEMMA-QT cable.
- Four or more Pioreactors on one bench can share one multi-port charger instead of one supply each: see [powering a cluster](https://docs.pioreactor.com/user-guide/powering-cluster).

</details>
