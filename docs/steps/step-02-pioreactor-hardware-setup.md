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
2. [Wetware assembly](https://docs.pioreactor.com/user-guide/40ml-v15-wetware-assembly)
3. [Attaching the wetware to the HAT assembly](https://docs.pioreactor.com/user-guide/40ml-v15-putting-it-together)
4. **Do not fit the v1.5 optics.** AEP0.2 is XR from the start, and the XR upgrade would only have you strip them straight back out. Keep the v1.5 optics parts in the box for the next step: the XR assembly reuses 2 eye-spys, 3 optics covers, 12x 8 mm screws, 1 LED cap and the 50 mm STEMMA-QT wire out of the v1.5 kit, and the XR kit supplies the remaining eye-spys, its own top vial holder and the O-ring. If instead you are upgrading a Pioreactor that is already built, work through [the XR disassembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-disassembly) to recover those same parts.
5. [Fit the XR upgrade kit](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly) (45° and 135° scattering in addition to 90°) — this is standard on AEP0.2 and gives the lower OD detection limit for earlier indication of growth.
6. [Fit the Precision Temperature Upgrade Kit](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit) — the MLX90632 far-infrared sensor replaces the thermistor for faster, hotter, contactless temperature control. It seats in the SPEC position and chains off the nearest eye-spy over STEMMA-QT.
7. The solenoid needs more power than the Pi alone can supply: follow <https://docs.pioreactor.com/user-guide/external-power>. Four or more Pioreactors on one bench can be powered from a single multi-port charger rather than one supply each — see <https://docs.pioreactor.com/user-guide/powering-cluster>.
