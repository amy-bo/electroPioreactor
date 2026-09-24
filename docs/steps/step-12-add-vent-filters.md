---
id: step-12-add-vent-filters
order: 12
title: "Add the vent filters (budget AEP)"
guide: [baep]
parts:
  - {component: hydrophobic-vent-filter, qty: 5, cat: part}
  - {component: gl45-cap, qty: 2, cat: prev}
  - {component: vial-cap, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: five-fitted
    question: "Are five filters fitted: one on each bottle cap vent, one on the CO₂ inlet, one on each of the two gas outlets?"
    issues:
      - {problem: "A luer will not take the filter", fix: "Filters are male-to-female: the male end goes to a female luer. Add a male-to-male adapter where both ends are female."}
---

A Mixed-culture electroPioreactor becomes a budget aseptic one by filtering every gas path. Five 0.2 μm hydrophobic vent filters:

1. Media bottle cap: filter on the vent port.
2. Product bottle cap: filter on the vent port.
3. Vial cap CO₂ inlet: filter between the gas line and the inlet luer.
4. Vial cap gas outlets: a filter on each of the two outlet luers.
5. Keep the sixth filter as a spare.
