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
  - {component: precision-temperature-upgrade-kit, qty: 1, cat: part}
  - {component: power-supply-12v, qty: 1, cat: part}
tools:
  - {component: phillips-ph0-screwdriver, qty: 1}
---

Follow the Pioreactor 40 ml v1.5 hardware setup guide: <https://docs.pioreactor.com/user-guide/40ml-v15-hardware-setup-intro>

1. [Assembling the Raspberry Pi and the HAT](https://docs.pioreactor.com/user-guide/40ml-v15-rpi-hat-assembly) — use a Raspberry Pi 5 1GB with the 27 W USB-C supply.
2. **Move the HAT's shunt connector to the position closest to the LED outputs, now, while the HAT is bare** ([external power](https://docs.pioreactor.com/user-guide/external-power)). This is what switches PWM channels 1 to 4 over to the 12V barrel jack. Do it before the vial holder assembly is mounted at sub-step 4, or you will be taking the unit apart again to reach it.

   <details>
   <summary>What happens if you miss it</summary>

   Nothing errors. The 12V supply is simply ignored by PWM channels 1 to 4, so the peristaltic pumps and the PWM 4 CO₂ solenoid stay on the Raspberry Pi's own supply — the solenoid will not drive, and step 8 will look like a gas train fault rather than a power one. Moving the shunt also invalidates any stirring and pump calibration made before it, which is the other reason to do it first.

   </details>
3. [Wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly)
4. [Attaching the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together)
5. **Do not fit the v1.5 optics.** Keep the v1.5 optics parts in the box for the next step.

   <details>
   <summary>Why, and which of those parts the XR kit reuses</summary>

   AEP0.2 is XR from the start, and the XR upgrade would only have you strip the v1.5 optics straight back out. The XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire out of the v1.5 kit; the XR kit supplies the remaining eye-spys, its own top vial holder and the O-ring. If instead you are upgrading a Pioreactor that is already built, work through [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those same parts.

   </details>
6. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly) (45° and 135° scattering in addition to 90°) — this is standard on AEP0.2 and gives the lower OD detection limit for earlier indication of growth.
7. [Fit the Precision Temperature Upgrade Kit](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit) — the MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. It seats in the SPEC position and chains off the nearest eye-spy over STEMMA-QT.
8. Connect the 12V supply to the HAT's barrel jack — the solenoid needs more power than the Pi alone can supply, and the shunt was moved for it at sub-step 2: <https://docs.pioreactor.com/user-guide/external-power>. Four or more Pioreactors on one bench can be powered from a single multi-port charger rather than one supply each — see <https://docs.pioreactor.com/user-guide/powering-cluster>.
