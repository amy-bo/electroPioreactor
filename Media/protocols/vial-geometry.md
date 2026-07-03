---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Vial geometry & true headspace"
sources:
  - https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5861554
  - https://www.sciencedirect.com/science/article/abs/pii/S0955598615000631
  - https://www.sciencedirect.com/science/article/pii/S2472630325001414
  - https://kg-m3.com/material/water-25c
  - https://kg-m3.com/material/water-30c
  - https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html
  - https://www.westlab.com/blog/how-to-read-a-meniscus-when-using-graduated-cylinders
  - https://www.needle.tube/product-articles-3/measuring-liquid-volumes-in-syringes-importance-and-best-practices-2
  - https://pioreactor.com/products/20ml-glass-vial
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, geometry, headspace, calibration]
---

# Vial geometry & true headspace

## Protocol

### Kit

- Analytical or precision balance, 0.01 g resolution or better, capacity above ~150 g.
- A thermometer.
- A fine-tipped wash bottle or a 1 mL syringe for topping up to the sealing plane.
- The actual vial of each reactor type to be calibrated.
- The actual cap and septum for that vial.
- The actual insert set for that vial, seated at its normal depths: the two 6 mm electrode rods, the sparge tube, the efflux tube, and the three headspace tubes (one medium-in and two gas-out), each seated at its normal protrusion.

### Reagents

- Deionised water.

### Method

1. Bring the vial and the deionised water to the run temperature, 30 °C, and hold them there throughout.
2. Assemble the vial exactly as for a real run, every insert seated to its normal depth, and weigh it empty. You need not tare, though taring before you add water is fine if it helps.
3. Meter in the working volume for that reactor type (about 15 mL for the 20 mL build, about 30 mL for the 40 mL build) and weigh again; the increase is the working volume.
4. Inject deionised water into the gas space above the liquid, through a headspace tube or by briefly lifting the septum, until it reaches the exact plane the cap seals against, with no trapped air.
5. Tilt and tap the vial to chase out any bubble clinging to an insert or the shoulder, top up to the septum plane again, and inspect against the light. Weigh again; the increase over step 3 is the headspace mass.
6. Empty and dry the vial, re-assemble and re-charge it as in steps 2 to 5, and take the headspace mass twice more, so you have three fills of the same vial. Record each fill as its own vial row. If one fill differs by more than about 0.3 mL from the others, re-wet, chase bubbles and re-run.
7. Remove the inserts and the cap, empty and dry the vial, and weigh it empty. Fill the whole vial body with deionised water up to the rim, the top reference plane being the internal lip of the neck where the cap seats. Chase out any bubble as before and weigh again; the increase is the body mass.
8. Note the water temperature.
9. Record your results in the **Vial geometry** section of the **Calibrations** tab, one row per vial; the column headers name what each cell wants. Set Include to y and leave the computed cells to the spreadsheet.

## What the spreadsheet does with it

The tab converts each recorded mass to a volume using the density of water at the recorded temperature, giving the true free headspace above the working liquid and the effective bore depth of the vial body. It then averages the included vials of the same reactor type. From those averages it feeds the model the total vial volume and the usable bore depth for that reactor type.

## Principle & background

The model needs three internally consistent numbers for each vial type, currently the 20 mL AEP0.1.1 build and the 40 mL AEP0.2 build: the uniform internal bore cross-section, the uniform-bore internal depth, and the total internal volume. Historically these came from two unrelated sources that disagreed by about 38 per cent. The total was taken from a nominal catalogue figure, 20 mL or 42 mL, while cross-section times depth was built from a measured internal diameter of 25.28 mm, derived from an outer diameter of 27.48 mm minus two 1.1 mm walls, and a measured usable depth of about 55 mm, which multiply to roughly 27.6 mL. Both cannot be right. The free gas volume above the liquid inherits the whole error, and the headline sparge pulse is roughly four times as sensitive to that headspace volume as to most other inputs, so the disagreement was the model's number-one blocker.

The fix is to stop guessing the total and instead directly measure the free gas space the model actually cares about, with the real electrode and tube inserts in place. Two things are measured per vial type. First, the true free headspace at working fill: with the vial charged to its normal working level and the full insert set seated as in a real run, the gas volume between the liquid surface and the underside of the septum the cap seals against. Second, the water-fillable volume of the whole body, from which the effective uniform-bore depth follows: the height of a plain cylinder of the same volume and bore, which is exactly what the model approximates, so it is the right number to feed even though the real vial has a rounded base and a tapering shoulder.

Gravimetric water displacement is the reference method because mass on a laboratory balance is far more precise and repeatable than reading a meniscus, and the density of water at the working temperature is known to better than 0.1 per cent, about 997.0 kg/m³ at 25 °C and 995.6 kg/m³ at 30 °C, so volume follows directly from mass divided by density.

Three sources of bias dominate and are handled in the method. A single trapped bubble of a few tenths of a millilitre, clinging to an electrode or in the shoulder, biases the headspace low, so every fill is tilted, tapped and inspected against the light. The headspace is bounded by the underside of the septum, not the top of the cap, so the fill must reach exactly that sealing plane and neither stop at the neck nor run into the cap recess. And the free volume depends on how far the inserts protrude, so they must sit at their true run depth on every measurement. Recording the water temperature lets the tab use the correct density rather than assuming 1.000 g/mL, which would add a small but avoidable bias. Both vial types must be measured; calibrating only one leaves the other inconsistent.

## Sources

- [Gravimetric container fill / headspace by water mass and density - USPTO 5,861,554](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5861554)
- [Water density formulations for gravimetric volume calibration - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0955598615000631)
- [Guide to liquid volume measurements: methods and technologies - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2472630325001414)
- [Water density at 25 °C (997.0 kg/m³)](https://kg-m3.com/material/water-25c)
- [Water density at 30 °C (995.6 kg/m³)](https://kg-m3.com/material/water-30c)
- [Water density vs temperature table - Engineering ToolBox](https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html)
- [Reading a meniscus and graduated-vessel tolerances - Westlab](https://www.westlab.com/blog/how-to-read-a-meniscus-when-using-graduated-cylinders)
- [Measuring liquid volumes in syringes: best practices](https://www.needle.tube/product-articles-3/measuring-liquid-volumes-in-syringes-importance-and-best-practices-2)
- [Pioreactor 20 mL glass vial (OD 27.48 mm, total height 57.4 mm)](https://pioreactor.com/products/20ml-glass-vial)
