---
id: step-12-add-vent-filters
order: 12
title: "Add the vent filters"
guide: [baep]
parts:
  - {component: hydrophobic-vent-filter, qty: 5, cat: part}
  - {component: gl45-cap, qty: 2, cat: prev}
  - {component: vial-cap-oring, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: five-fitted
    question: "Where are vent filters fitted now?"
    options:
      - {label: "Both bottle cap vents, the CO₂ inlet and both gas outlets", correct: true}
      - {label: "Both bottle cap vents, the CO₂ inlet and one gas outlet", fix: "Fit the female end of a filter to the other gas outlet luer too. If a luer will not take the filter: each filter has a female inlet and a male outlet, so where two female luers would meet, add a male-to-male luer lock adapter."}
      - {label: "The CO₂ inlet and both gas outlets, no bottle cap vents", fix: "Fit one to each bottle cap's vent port too."}
---

Filter every gas path with five 25 mm, 0.2 μm hydrophobic vent filters, the ones the AEP0.2 uses. This turns a Mixed-culture electroPioreactor into a budget aseptic one.

1. Fit one to the media bottle cap's vent port.
2. Fit one to the product bottle cap's vent port.
3. Take the CO₂ tube's luer off the vial cap's CO₂ inlet, fit the male end of a filter to the inlet, and connect the tube's luer to the filter.
4. Fit the female end of a filter to each of the vial cap's two gas outlet luers.
