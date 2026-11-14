---
id: step-10-calibrate-pumps
order: 10
title: "Calibrate the pumps"
guide: [aep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: prev}
  - {component: power-supply-12v, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
checks_draft: true
checks:
  - id: pumps-calibrated
    question: "Which pumps have you calibrated?"
    options:
      - {label: "The media pump and the waste pump", correct: true}
      - {label: "The media pump, not the waste pump", fix: "Calibrate the waste (product) pump too."}
      - {label: "The waste pump, not the media pump", fix: "Calibrate the media pump too."}
---

1. [Calibrate the pumps](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration). The vial is filled and levelled in [Ports](step-11-ports.md), once its needles are in.
