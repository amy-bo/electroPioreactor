---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Sinter (frit) porosity grade"
sources:
  - https://www.iso.org/standard/10772.html
  - https://www.astm.org/Standards/E128.htm
  - https://www.astm.org/standards/f316
  - https://www.iso.org/standard/9678.html
  - https://www.dwk.com/na/technical/sintered-discs
  - https://www.buch-holm.com/products/filtration/
  - https://www.sigmaaldrich.com/US/en/product/aldrich/z232440
  - https://www.filsonfilters.com/sintered-glass-filter/
  - https://www.pharmtech.com/view/relationship-among-pore-size-ratings-bubble-points-and-porosity
  - https://www.gkd-group.com/en/glossary/bubble-point-test/
  - https://wiki.anton-paar.com/en/basics-of-capillary-flow-porometry/
  - https://scottlab.com/bubble-point-integrity-testing
  - https://adamschittenden.com/technical/frits
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, sparger, sinter, mass-transfer]
---

# Sinter (frit) porosity grade

## Optimal protocol

### Kit

- The sintered frit to be tested, clean and freshly rinsed. If the frit has been in service, acid-clean it and rinse it thoroughly with distilled water before testing.
- A gas supply (air, nitrogen or CO2) fitted with a fine needle valve.
- A rubber O-ring and a gas inlet fitting, so that one face of the frit can be sealed against the gas line.
- A trough deep enough to submerge one face of the frit by 5 to 10 mm.
- A low-range pressure gauge or digital manometer reading in kPa, with a resolution of 0.5 kPa or finer. A 0 to 200 kPa range covers the finer frits; the coarsest frits need only a 0 to 10 kPa range.
- A stopwatch (a phone stopwatch is fine).

### Reagents

- Distilled water as the wetting liquid.

### Method

1. Take a clean, freshly rinsed frit. If it has been in service, acid-clean it and rinse it thoroughly with distilled water first.
2. Submerge the frit fully in distilled water for at least 5 minutes, gently agitating it to drive trapped air out of every pore. Check that the whole frit is uniformly wetted, with no dry patches: a dry patch gives a falsely low reading.
3. Seal one face of the frit against the gas line by pressing it face-down onto the rubber O-ring over the gas inlet, and submerge the other face 5 to 10 mm below the water surface in the trough.
4. Open the gas supply to the lowest pressure the gauge can read and wait 30 seconds. Slow, isolated bubbles rising from single pores are normal at this stage and are not the reading you want.
5. Raise the pressure in small steps, waiting 30 seconds after each step. Use steps of about 0.2 to 1 kPa, taking the smaller steps for finer frits.
6. Watch the submerged face. Note the pressure at which a first continuous, steady stream of bubbles issues from one point on the face, rather than the sporadic isolated bubbles seen earlier.
7. Close the gas supply, re-wet the frit fully and repeat twice more, so the reading is confirmed on three separate runs. The three readings should agree closely; if one is much lower than the others, suspect incomplete wetting and re-wet before trusting it.
8. Record the bubble-point pressure (kPa) at which the first steady stream of bubbles appears, in the **Sinter porosity** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## Budget protocol

### Kit

- Good lighting, and a hand lens if the marking is small.
- Access to the manufacturer's catalogue or datasheet, for looking up the catalogue number stamped on the glassware.

### Reagents

- None.

### Method

1. Examine the frit body, the funnel and any supplied documentation under good light for a porosity marking such as "P3", "Por. 3", "G3" or a bare numeral (0 to 5).
2. If the frit carries no porosity marking but its source is known, find the catalogue number stamped on the glassware and look that number up in the supplier's catalogue or datasheet. The porosity class is always listed there.
3. Read off the manufacturer's porosity class. Note that grade numbering is not universal: most laboratory glassware follows the DURAN / ISO numbering the model expects, but a few suppliers number their finest grades differently, so where the supplier's convention is uncertain the optimal bubble-point test is the reliable choice.
4. If neither a marking nor a datasheet can be found, treat the frit as unknown. Do not record a grade and do not rely on the sintered sparger mode until the frit is identified or a bubble-point test has been done.
5. Record the manufacturer's stated porosity grade in the **Sinter porosity** section of the **Calibrations** tab. Fill Researcher, Date and Reactor; set Include to y. Leave the Computed, Type and value-in-use cells to the spreadsheet.

## What the spreadsheet does with it

The Calibrations tab converts the recorded bubble-point pressure to the largest-pore size and then to the ISO 4793 / DURAN porosity grade. For each reactor it uses the most recent included measurement: the fitted frit is a piece of hardware, so the latest measurement replaces the older ones rather than being averaged with them. That grade feeds the sinter porosity grade used for bubble-size modelling elsewhere in the model. On the budget route, if you already know the frit's manufacturer porosity grade you do not need a Calibrations entry at all, because the selected electrode already carries its grade in the model; the Sinter porosity section is there for measuring an actual frit by its bubble-point.

## Principle & background

A sintered (fritted) sparger is a network of tortuous capillary pores. The single largest pore sets both the smallest bubble the sparger can produce and the capillary pressure that gas must overcome to break through a fully wetted frit, so characterising the largest pore characterises the sparger for the mass-transfer calculations. The porosity grade is a compact label for that largest pore: 0 is the coarsest class and 5 the finest.

For a circular capillary wetted by a liquid, the Young – Laplace / Washburn relation gives the pressure difference required to expel the liquid from a pore of diameter d as ΔP = 4·γ·cosθ / d, where γ is the liquid surface tension and θ the liquid – solid contact angle. The bubble-point pressure is the lowest pressure at which a continuous stream of bubbles first emerges from the downstream face of a fully wetted frit, and rearranging the relation recovers the largest pore diameter from that measured pressure. This is the basis of the standard bubble-point test for rigid porous filters (https://www.astm.org/Standards/E128.htm, https://www.astm.org/standards/f316, https://www.pharmtech.com/view/relationship-among-pore-size-ratings-bubble-points-and-porosity, https://wiki.anton-paar.com/en/basics-of-capillary-flow-porometry/).

The wetting liquid matters. Distilled water (γ ≈ 0.072 N/m at 20 °C) is preferred for borosilicate glass because the contact angle is near zero, so cos θ ≈ 1 and no correction is needed. Isopropanol (γ ≈ 0.023 N/m at 20 °C) is sometimes used on coarse frits because it breaks through at lower, more easily read pressures, but it yields a proportionally smaller apparent pore size and needs a correction factor; results from water and from isopropanol must never be combined without converting between them (https://www.iso.org/standard/9678.html, https://scottlab.com/bubble-point-integrity-testing, https://www.gkd-group.com/en/glossary/bubble-point-test/).

The spreadsheet maps each grade to a nominal maximum pore diameter using the ISO 4793 / DURAN porosity classes:

| Grade | ISO 4793 class | Nominal d_max (µm) | Water bubble-point (kPa) |
|-------|----------------|--------------------|--------------------------|
| 0     | P250           | 160–250            | 1.2–1.8                  |
| 1     | P160           | 100–160            | 1.8–2.9                  |
| 2     | P100           | 40–100             | 2.9–7.2                  |
| 3     | P40            | 16–40              | 7.2–18                   |
| 4     | P16            | 10–16              | 18–29                    |
| 5     | P1.6           | 1.0–1.6            | 180–288                  |

The DURAN six-grade system used by the model maps grade 5 to the ISO P 1.6 class (1.0–1.6 µm). This differs from the Pyrex / generic-vendor convention that calls grade 5 the coarser P 10 class (4–10 µm, sometimes quoted 1–10 µm). Confirm which system a frit's supplier uses before trusting a stamped grade number; the bubble-point test sidesteps the ambiguity because it measures the pore directly (https://www.dwk.com/na/technical/sintered-discs, https://www.buch-holm.com/products/filtration/, https://www.sigmaaldrich.com/US/en/product/aldrich/z232440, https://www.filsonfilters.com/sintered-glass-filter/, https://adamschittenden.com/technical/frits).

Four things degrade a bubble-point reading:

- **Incomplete wetting** is the commonest error. A dry pore breaks through at anomalously low pressure, giving too large a pore diameter and too coarse a grade. Soak for at least 5 minutes and confirm uniform wetting by eye before ramping the pressure.
- **A clogged or used frit** has pores partly blocked by debris, precipitate or biofilm, which raises the apparent bubble-point and reports too fine a grade. Test only clean frits; acid-clean and rinse any frit taken out of service before testing.
- **Temperature** shifts surface tension by about 0.15 mN/m per °C for water. The 0.072 N/m figure is for 20 °C; at 30 °C the roughly 1% change is negligible for grade mapping, but below 15 °C or above 35 °C the appropriate γ should be used.
- **Mixed standards.** ASTM and DIN coarse / medium / fine designations do not map one-to-one to the ISO 4793 P-numbers. Confirm which standard a manufacturer references before recording a grade.

## Sources

- ISO 4793:1980 – Laboratory sintered (fritted) filters: porosity grading, classification and designation (defines the P-designation classes). Geneva: ISO. https://www.iso.org/standard/10772.html
- ASTM E128-99(2019) – Standard test method for maximum pore diameter and permeability of rigid porous filters for laboratory use (the primary standard for bubble-point testing of sintered glass frits; defines d = 4γcosθ/P). West Conshohocken: ASTM International. https://www.astm.org/Standards/E128.htm
- ASTM F316-03(2019) – Standard test methods for pore size characteristics of membrane filters by bubble point and mean flow pore test. West Conshohocken: ASTM International. https://www.astm.org/standards/f316
- ISO 4003:1977 – Permeable sintered metal materials: determination of bubble test pore size (uses isopropanol as wetting fluid; slow-ramp guidance). Geneva: ISO. https://www.iso.org/standard/9678.html
- DURAN / DWK Life Sciences sintered disc technical page: pore size classes (grades 0–5, ISO 4793; grade 5 = P 1.6 = 1.0–1.6 µm). https://www.dwk.com/na/technical/sintered-discs
- Buch & Holm catalogue entries confirming DURAN grade pore-size ranges: por. 3 = 16–40 µm, por. 4 = 10–16 µm. https://www.buch-holm.com/products/filtration/
- Sigma-Aldrich DURAN funnel listings confirming por. 2 = 40–100 µm, por. 3 = 16–40 µm, and the grade-5 = P 1.6 mapping. https://www.sigmaaldrich.com/US/en/product/aldrich/z232440
- Filson Filters, sintered glass filter disc grades 0–5 (note: Filson uses the coarser grade-5 = 1–10 µm convention, not the DURAN P 1.6 mapping). https://www.filsonfilters.com/sintered-glass-filter/
- Young – Laplace / Washburn bubble-point equation derivation and ASTM F316 context: Pharmaceutical Technology, "The relationship among pore-size ratings, bubble points, and porosity". https://www.pharmtech.com/view/relationship-among-pore-size-ratings-bubble-points-and-porosity
- GKD Group glossary: bubble-point test overview. https://www.gkd-group.com/en/glossary/bubble-point-test/
- Anton Paar wiki: capillary flow porometry basics (Washburn equation, wetting liquids, contact angle). https://wiki.anton-paar.com/en/basics-of-capillary-flow-porometry/
- Scott Laboratories: bubble-point integrity testing procedure (wetting fluid, first-bubble criterion). https://scottlab.com/bubble-point-integrity-testing
- Adams & Chittenden Scientific Glass: fritted glass filters, ASTM vs ISO porosity class comparison. https://adamschittenden.com/technical/frits
