---
state: reviewed
author: [claude-opus-4.8]
checked: [claude-opus-4.8]
reviewed: [claude-opus-4.8]
authorised:
source_type: external
description: "Sinter (frit) porosity grade"
sources:
  - https://www.iso.org/standard/10772.html>
  - https://www.astm.org/Standards/E128.htm>
  - https://www.astm.org/standards/f316>
  - https://www.iso.org/standard/9678.html>
  - https://www.dwk.com/na/technical/sintered-discs>
  - https://www.buch-holm.com/products/filtration/>
  - https://www.sigmaaldrich.com/US/en/product/aldrich/z232440>
  - https://www.filsonfilters.com/sintered-glass-filter/>
  - https://www.pharmtech.com/view/relationship-among-pore-size-ratings-bubble-points-and-porosity>
  - https://www.gkd-group.com/en/glossary/bubble-point-test/>
  - https://wiki.anton-paar.com/en/basics-of-capillary-flow-porometry/>
  - https://scottlab.com/bubble-point-integrity-testing>
  - https://adamschittenden.com/technical/frits>
created: 2026-06-19
recorded_at: 2026-06-20
cssclasses: [trust-reviewed]
tags: [electropioreactor, protocol, sparger, sinter, mass-transfer]
---

# Sinter (frit) porosity grade

**Feeds:** the "sinter porosity" column (E) of the electrode lookup table (Electrochemistry A34:I37), grade 0 - 5 (ISO 4793 / DURAN class). The model sources the grade from that electrode row via por_grade_e (Electrochemistry!D32) -> por_grade (Mass Transfer!D20), both read-only imports; there is no hand-entered grade cell.
**Why it matters:** sets bubble size and clears the "Sinter OOR" regime flag when sparger=Sintered.

## Principle

A sintered (fritted) sparger contains a network of tortuous capillary pores. The largest pore sets both the minimum bubble diameter produced and the capillary pressure threshold that gas must overcome to enter the liquid. The model maps an integer grade (0 = coarsest, 5 = finest) to a nominal maximum pore diameter via the ISO 4793 / DURAN porosity-class table stored in cells por0\_um - por5\_um (Mass Transfer!D33:D38). The grade itself is not a free input: it follows the selected electrode. por\_grade (Mass Transfer!D20) is a formula import of por\_grade\_e (Electrochemistry!D32), which in turn VLOOKUPs the "sinter porosity" column of the electrode table on the selected electrode. So once the sintered electrode's row carries the measured grade, por\_grade is set correctly, d\_bubble (Mass Transfer!D42) becomes valid and the "Sinter OOR" flag clears.

The relevant physics: for a circular capillary wetted by a liquid, the Young - Laplace / Washburn relation gives the pressure difference ΔP required to expel the liquid from a pore of diameter d:

    ΔP = (4 · γ · cos θ) / d

Rearranged to find the maximum pore diameter from a measured bubble-point pressure P\_bp (Pa):

    d_max (m) = (4 · γ · cos θ) / P_bp

where γ is liquid surface tension (N/m) and θ is the liquid - solid contact angle. For water wetting borosilicate glass, cos θ ≈ 1 and γ ≈ 0.072 N/m at 20 °C, giving the practical form (with P\_bp in Pa, d in µm):

    d_max (µm) = (4 × 0.072 × 1) / P_bp × 1 × 10^6
               = 288 000 / P_bp

The bubble-point pressure is the lowest pressure at which a continuous stream of bubbles first emerges from the downstream face of a fully wetted frit.

## Optimal protocol (best accuracy)

**Bubble-point test.** Measures d\_max directly; works on any unlabelled frit.

**Equipment:** frit to test; gas supply (air, N₂ or CO₂) with fine needle valve; liquid-filled trough deep enough to submerge the frit by 5 - 10 mm; low-range pressure gauge or digital manometer (resolution ≤ 0.5 kPa; range 0 - 200 kPa covers grades 1 - 5; grade 0 / 1 may need only 0 - 10 kPa); stopwatch; distilled water or isopropanol (IPA) as wetting liquid.

**Wetting liquid choice:** distilled water (γ = 0.072 N/m at 20 °C) is preferred for borosilicate glass because the contact angle is near zero. IPA (γ = 0.023 N/m at 20 °C) is used where lower pressures ease detection on coarser frits, but yields a lower apparent d\_max by about 3× and requires a correction factor; do not mix results from different liquids without conversion.

**Procedure:**
1. Submerge the frit fully in distilled water for at least 5 minutes; gently agitate to displace trapped air from all pores. The frit must be uniformly wetted - any dry patch gives a falsely low bubble-point.
2. Lift the frit and mount it with one face sealed against a gas line and the other face submerged 5 - 10 mm below the water surface in the trough. A simple arrangement: press the frit face-down onto a rubber O-ring seated over a gas inlet.
3. Open the gas supply to the lowest readable pressure. Wait 30 seconds at each step before increasing. Observe the submerged face closely - individual slow-rising bubbles from isolated pores are normal and indicate the gas is entering; the bubble-point is NOT reached yet.
4. Slowly increase pressure in increments of 0.2 - 1 kPa (smaller steps for finer grades). Record P\_bp as the pressure at which a first continuous, steady stream of bubbles (not isolated sporadic bubbles) issues from a single point on the submerged face. This is the largest pore.
5. Repeat three times, re-wetting fully between runs. Average the three P\_bp values.
6. Calculate d\_max using the formula above (water, cos θ = 1):

        d_max (µm) = 288 000 / P_bp (Pa)

7. Map d\_max to the ISO 4793 class table (see Result -> model) and set por\_grade accordingly.

**Expected pressures for water at 20 °C (approximate):**

| Grade | ISO P-class | d\_max (µm) | P\_bp (kPa) |
|-------|-------------|-------------|-------------|
| 0     | P250        | 160 - 250   | 1.2 - 1.8   |
| 1     | P160        | 100 - 160   | 1.8 - 2.9   |
| 2     | P100        | 40 - 100    | 2.9 - 7.2   |
| 3     | P40         | 16 - 40     | 7.2 - 18    |
| 4     | P16         | 10 - 16     | 18 - 29     |
| 5     | P1.6        | 1.0 - 1.6   | 180 - 288   |

Note on grade 5: the DURAN 6-grade system (which the model's lookup table uses) maps grade 5 to the ISO P 1.6 class (1.0 - 1.6 µm, midpoint ~1.3 µm). This differs from the Pyrex / generic-vendor convention that calls grade 5 = P 10 = 4 - 10 µm (sometimes quoted 1 - 10 µm). Confirm which system your frit's supplier uses before recording the grade - the bubble-point pressures above assume the DURAN P 1.6 mapping for grade 5.

## Budget protocol (minimal kit)

**Read the manufacturer label or datasheet.** Most laboratory sintered frits are marked with their porosity class on the frit itself, on the funnel body, or in the supplied documentation.

1. Examine the frit body under good light for a stamped or etched mark such as "P3", "Por. 3", "G3", "4", or similar. DURAN / Schott frits use the numeric class (0 - 5); some ASTM-aligned glassware uses coarser designations (EC, M, F, XF, UF) that map approximately to ISO grades 0/1, 2, 3, 4, 5 respectively.
2. If the frit is unlabelled but its source is known, look up the product datasheet. Search the supplier catalogue for the catalogue number stamped on the glassware; the porosity class is always listed.
3. Read the nominal pore size range from the datasheet and match to the ISO 4793 table:

   | Grade (por\_grade) | ISO 4793 class | Nominal d\_max (µm) |
   |--------------------|----------------|---------------------|
   | 0                  | P250           | 160 - 250           |
   | 1                  | P160           | 100 - 160           |
   | 2                  | P100           | 40 - 100            |
   | 3                  | P40            | 16 - 40             |
   | 4                  | P16            | 10 - 16             |
   | 5                  | P1.6           | 1.0 - 1.6           |

   The DURAN numeric class (printed on DWK Life Sciences / Schott glassware) is identical to the por\_grade integer. A frit marked "Por. 3" maps to por\_grade = 3. Caution: DURAN grade 5 is the ultra-fine P 1.6 class (1.0 - 1.6 µm), finer than the "grade 5 = 4 - 10 µm" used by some other manufacturers (Pyrex, Filson). The model's lookup uses the DURAN mapping; if your frit is from a vendor using the coarser convention, read its actual stated pore range and pick the por\_grade whose DURAN range matches, rather than copying the vendor's grade number blindly.

4. If no label or datasheet is available and no bubble-point test is possible, the sparger should be treated as unknown and the model's Sintered sparger mode should not be used until the grade is confirmed.

## Result -> model

The grade follows the selected electrode, so it is set on the electrode lookup table, **not** by hand-entering a free cell. Enter the integer grade (0 - 5) into the **"sinter porosity" column (E) of the sintered electrode's row in the electrode table at Electrochemistry A34:I37** - the sintered electrode is the "MMO tube" row (row 37), whose column E currently holds 0. (The two rod electrodes, rows 35 - 36, carry "n/a" because they sparge through an open tube, not a frit.)

Do not write into Mass Transfer!D20 or Electrochemistry!D32: both are read-only formula imports (D20 = `=Electrochemistry!$D$32`; D32 = a VLOOKUP on the electrode table), so overwriting them severs the link. There is no Summary-sheet dropdown for por\_grade (Summary inputs sit at D2 - D10; Mass Transfer!D42 is d\_bubble, not a selector) - the only place the grade is set is the electrode-table "sinter porosity" column.

With the electrode row updated and that electrode selected, por\_grade\_e (Electrochemistry!D32) picks up the grade, por\_grade (Mass Transfer!D20) imports it, and the model indexes the lookup array por0\_um - por5\_um (Mass Transfer!D33:D38) to retrieve d\_max in µm, then sets d\_bubble (D42) for the mass-transfer calculations. Once por\_grade is a valid integer and sparger = Sintered, the "Sinter OOR" flag in bubble\_regime (D64) will clear if d\_bubble falls within the validated bubble-size range used by the Mendelson rise-velocity and kL correlations.

## Acceptance checks & pitfalls

**Check 1 - flag clears:** after setting the grade on the electrode table and selecting that electrode, confirm that bubble\_regime (Mass Transfer!D64) no longer reads "Sinter OOR". If it still shows OOR, the resulting d\_bubble is outside the validated range for the active correlation; consider whether the frit grade is appropriate for the application or whether a different sparger type should be selected.

**Check 2 - cross-check against visual bubble size:** if you can observe sparging in the Pioreactor vial, bubbles from a grade 3 - 4 frit (16 - 40 µm pores, d\_bubble ≈ 0.5 - 1.5 mm at this scale) should be visibly much finer than those from a simple tube sparger (grade 0 - 1 or open tube, d\_bubble ≈ 2 - 5 mm). A qualitative match between observation and model output is a useful sanity check.

**Pitfall - wetting in bubble-point test:** incomplete wetting is the most common error. A dry pore produces bubbles at anomalously low pressure, giving an artificially large d\_max and a coarser grade assignment than correct. Always soak for ≥ 5 minutes and confirm uniform wetting visually before starting the pressure ramp.

**Pitfall - clogged frit:** a used frit may have pores partially blocked by cell debris, precipitate, or biofilm. This raises the apparent bubble-point pressure (smaller apparent d\_max, finer apparent grade). Always use a clean, freshly rinsed frit; if testing a frit from service, acid-clean and rinse with distilled water before testing.

**Pitfall - temperature:** γ decreases ~0.15 mN/m per °C for water. The nominal γ = 0.072 N/m is for 20 °C. At 30 °C, γ ≈ 0.071 N/m - a ~1% correction, negligible for grade mapping. If testing at temperatures below 15 °C or above 35 °C, apply the appropriate γ value.

**Pitfall - mixed standards:** ASTM and DIN coarse/medium/fine designations do not map directly to ISO 4793 P-numbers. Always confirm which standard the manufacturer is referencing before recording a grade number.

## Sources

- ISO 4793:1980 - Laboratory sintered (fritted) filters - porosity grading, classification and designation (defines the eight-class P-designation system). Geneva: ISO. <https://www.iso.org/standard/10772.html>
- ASTM E128-99(2019) - Standard test method for maximum pore diameter and permeability of rigid porous filters for laboratory use (the primary standard for bubble-point testing of sintered glass frits; defines d = 4γcosθ/P). West Conshohocken: ASTM International. <https://www.astm.org/Standards/E128.htm>
- ASTM F316-03(2019) - Standard test methods for pore size characteristics of membrane filters by bubble point and mean flow pore test. West Conshohocken: ASTM International. <https://www.astm.org/standards/f316>
- ISO 4003:1977 - Permeable sintered metal materials - determination of bubble test pore size (uses IPA as wetting fluid; slow-ramp guidance). Geneva: ISO. <https://www.iso.org/standard/9678.html>
- DURAN / DWK Life Sciences sintered disc technical page - pore size classes (grades 0 - 5, ISO 4793; grade 5 = P 1.6 = 1.0 - 1.6 µm). <https://www.dwk.com/na/technical/sintered-discs>
- Buch & Holm catalogue entries confirming DURAN grade pore-size ranges: por. 3 = 16 - 40 µm, por. 4 = 10 - 16 µm. <https://www.buch-holm.com/products/filtration/>
- Sigma-Aldrich DURAN funnel listings confirming por. 2 = 40 - 100 µm, por. 3 = 16 - 40 µm, and the grade-5 = P 1.6 mapping. <https://www.sigmaaldrich.com/US/en/product/aldrich/z232440>
- Filson Filters - sintered glass filter disc grades 0 - 5 (note: Filson uses the coarser grade-5 = 1 - 10 µm convention, not the DURAN P 1.6 mapping). <https://www.filsonfilters.com/sintered-glass-filter/>
- Young - Laplace / Washburn bubble-point equation derivation and ASTM F316 context: Pharmaceutical Technology, "The relationship among pore-size ratings, bubble points, and porosity". <https://www.pharmtech.com/view/relationship-among-pore-size-ratings-bubble-points-and-porosity>
- GKD Group glossary: bubble-point test overview. <https://www.gkd-group.com/en/glossary/bubble-point-test/>
- Anton Paar wiki: capillary flow porometry basics (Washburn equation, wetting liquids, contact angle). <https://wiki.anton-paar.com/en/basics-of-capillary-flow-porometry/>
- Scott Laboratories: bubble-point integrity testing procedure (wetting fluid, first-bubble criterion). <https://scottlab.com/bubble-point-integrity-testing>
- Adams & Chittenden Scientific Glass: fritted glass filters - ASTM vs ISO porosity class comparison. <https://adamschittenden.com/technical/frits>
