---
id: step-03-mep-pioreactor-hardware-setup
order: 3
title: "Pioreactor hardware setup"
guide: [mep, baep]
parts:
  - {component: pioreactor-20ml, qty: 1, cat: part}
  - {component: raspberry-pi-zero-2w, qty: 1, cat: part}
  - {component: raspberry-pi-power-supply, qty: 1, cat: part}
  - {component: pioreactor-vial-20ml, qty: 1, cat: part}
  - {component: stir-bar, qty: 1, cat: part}
  - {component: power-supply-12v, qty: 1, cat: part}
tools:
  - {component: phillips-ph0-screwdriver, qty: 1}
checks_draft: true
checks:
  - id: external-power
    question: "What is plugged into the HAT's barrel jack?"
    options:
      - {label: "The 12 V supply", correct: true}
      - {label: "Nothing yet", fix: "Set it up now, before any calibration, following Pioreactor's external power guide for your HAT. Without it the pumps and the PWM 4 CO₂ solenoid run on the Pi's own supply, and the solenoid will not drive."}
  - id: boots
    question: "On a Zero 2 W, which socket is the Raspberry Pi power supply in?"
    options:
      - {label: "The frontmost micro-USB on the bottom board", correct: true}
      - {label: "The other micro-USB on the bottom board", fix: "Move it to the frontmost socket, with the Pioreactor logo facing you: that is the Pi's power socket. The unit then boots within about 90 seconds."}
      - {label: "A socket on the HAT, not the Pi", fix: "The HAT takes the 12 V supply. Plug the Raspberry Pi supply into the Pi's own power socket: the frontmost micro-USB on the bottom board."}
---

Follow Pioreactor's [20 ml v1.1 hardware setup guide](https://docs.pioreactor.com/user-guide/20ml-v11-hardware-setup-intro), with these changes.

1. Build it on a Raspberry Pi Zero 2 W. A Raspberry Pi 4B also works.
2. Set the vial's own cap aside: the O-ring vial cap replaces it in **Set up electrolysis**.
3. Plug the stirrer into PWM channel 1.
4. Connect the 12 V power supply to the HAT's barrel jack, following Pioreactor's [external power guide](https://docs.pioreactor.com/user-guide/external-power) for your HAT.

   :::caution[Before any calibration]
   The peristaltic pumps and the PWM 4 CO₂ solenoid need the 12 V supply. Without it the solenoid will not drive, and sparging looks like a gas train fault. Setting up external power later also invalidates any stirring and pump calibration.
   :::
5. Connect the Raspberry Pi power supply to the Pi's power socket (micro-USB on a Zero 2 W: the frontmost socket on the bottom board, with the Pioreactor logo facing you). The unit boots within about 90 seconds.

<details>
<summary>Notes</summary>

- Four or more Pioreactors on one bench can share one multi-port charger instead of one supply each: see [powering a cluster](https://docs.pioreactor.com/user-guide/powering-cluster).

</details>
