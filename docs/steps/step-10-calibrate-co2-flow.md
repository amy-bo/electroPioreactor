---
id: step-10-calibrate-co2-flow
order: 10
title: "Calibrate CO₂ flow"
guide: [aep]
parts:
  - {component: co2-regulator, qty: 1, cat: prev}
  - {component: co2-needle-valve, qty: 1, cat: prev}
  - {component: luer-lock-cap, qty: 1, cat: prev}
  - {component: silicone-tubing, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: one-bar
    question: "Is the regulator set to 1 bar?"
    issues:
      - {problem: "It reads more or less", fix: "Adjust the regulator to 1 bar before touching the needle valve."}
  - id: gas-at-vent
    question: "While sparging, with one outlet vent plugged, does gas leave through the open vent?"
    issues:
      - {problem: "No gas leaves the open vent", fix: "Check the job is sparging (or the relay is on) and that the needle valve is open."}
  - id: target-flow
    question: "Does the measured flow rate match your target?"
    issues:
      - {problem: "It is off target", fix: "Adjust the needle valve and repeat the measurement until it matches."}
---

1. Set regulator to 1 bar
2. Adjust needle valve to give target flow rate
3. Start the **electroPioreactor** job, or turn on the relay in the Pioreactor UI, to sparge
4. Temporarily close one of two outlet gas vents with luer plug
5. Run 1/16" tubing from outlet of open gas vent port to bath until water CO2 concentration is assumed (or if possible measured) to have equilibrated
6. Record time taken to fill measuring cylinder with CO₂ over water
7. Determine the actual flow rate
8. Adjust needle valve and repeat process until target flow rate is achieved
