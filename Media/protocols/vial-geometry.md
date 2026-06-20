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

**Feeds:** Geometry!V_vial_total, A_x, D_int, vial_ID (+ clears the geom_check INCONSISTENT flag). Current: nominal 20/42 mL vs cylinder ~27.6 mL.

**Why it matters:** headline optimal-pulse ~4x sensitive to headspace_V.

## Principle

The model needs three internally consistent numbers for each vial type (the 20 mL "AEP0.1.1" build and the 40 mL "AEP0.2" build): the uniform internal bore cross-section A_x, the uniform-bore internal depth D_int, and the total internal volume V_vial_total. Right now these are pulled from two unrelated sources that disagree by about 38 percent. V_vial_total is a nominal catalogue figure (20 mL or 42 mL); A_x times D_int comes from the measured internal diameter (vial_ID 25.28 mm, derived from OD 27.48 mm minus two 1.1 mm walls) and a measured usable depth (55 mm), which multiply to roughly 27.6 mL. They cannot both be right. The downstream headspace_V = V_vial_total - V_charge - V_inserts (the free gas volume above the liquid) inherits the whole error, and the headline sparge pulse is roughly four times as sensitive to headspace_V as to most other inputs, so this is the model's number-one blocker.

The fix is to stop guessing the total and instead directly measure the free gas space that the model actually cares about, with the real electrode and tube inserts in place. We measure two things per vial type. First, the true free-gas headspace volume: with the vial charged to its normal working liquid level and the full insert set (two electrodes, sparge tube, efflux tube, extra headspace tubes) seated as in a real run, the volume of gas between the liquid surface and the underside of the septum/cap. Second, the true uniform-bore internal depth D_int: the straight cylindrical body height that the model approximates as a plain cylinder, measured from the inside base to the underside of the cap, excluding the curved shoulder/neck where the bore is not uniform.

The interface between measurement and model is deliberate. We measure free headspace at working fill (the load-bearing quantity), and we measure bore depth. The geometry sheet already computes A_x from vial_ID and computes V_inserts and V_charge. So once we have measured headspace at a known V_charge and insert set, we can back-solve a self-consistent V_vial_total ( = measured headspace + V_charge + V_inserts ) and check it against A_x times D_int. When those two agree to within tolerance, the geom_check consistency cell reads OK.

Gravimetric water displacement is the reference method because mass on a lab balance is far more precise and repeatable than reading a meniscus, and water density at the working temperature is known to better than 0.1 percent (about 997.0 kg/m3 at 25 degC, 995.6 kg/m3 at 30 degC), so volume follows directly from mass divided by density. The graduated-syringe variant trades that precision for needing only a syringe.

## Optimal protocol (best accuracy)

Kit: analytical or precision balance (0.01 g resolution or better, capacity > 100 g), deionised water at known temperature, a thermometer, a fine-tipped wash bottle or 1 mL syringe for topping up to the line, the actual vial of each type, the actual cap/septum, and the actual insert set (two 6 mm electrode rods, sparge tube, efflux tube, the three extra headspace tubes) seated at their normal depths. Work at the vial's normal run temperature so the density value matches.

Measure the free headspace at working fill (the number the model needs):

1. Assemble the vial exactly as for a real run: seat all inserts through the cap to their normal insertion depths, and charge the vial with the normal working liquid volume V_charge for that vial type (the volume the model would charge - the integer mL that brings the level to the working datum). Use water as a liquid stand-in if you do not want to consume media; the headspace geometry is identical.
2. Place the assembled, charged vial on the balance and tare it.
3. Through one of the headspace tubes (or by briefly lifting the septum), inject deionised water from the syringe/wash bottle into the headspace until the gas space is completely filled to the underside of the septum line - i.e. water reaches the exact plane the cap seals against, with no trapped bubble. Tilt slightly and tap to chase out any bubble clinging to an insert or the shoulder.
4. Read the mass added, m_head (g). The free-gas headspace volume is headspace_V = m_head / rho_water, with rho_water in g/mL at the measured temperature (0.99705 g/mL at 25 degC, 0.99565 g/mL at 30 degC). Repeat three times (empty, dry, re-assemble between runs) and take the mean; the spread across the three is your measurement uncertainty.

Measure the uniform-bore internal depth D_int (for the A_x x D_int cross-check):

5. With the vial empty, dry and capped but with inserts removed, tare on the balance, then fill the entire vial body with deionised water up to the underside of the cap and weigh: m_body (g). The water-fillable internal volume is V_body = m_body / rho_water.
6. Separately measure the internal diameter at mid-body with calipers (or take the model's vial_ID 25.28 mm) and compute A_x = pi/4 x vial_ID^2. The effective uniform-bore depth is D_int = V_body / A_x (use consistent units: V_body in mm^3 = mL x 1000, A_x in mm^2, gives D_int in mm). Because the real vial has a rounded base and a tapering shoulder, this "effective" D_int is the height of a plain cylinder of the same volume and bore - which is exactly what the model assumes, so it is the right number to feed.

## Budget protocol (minimal kit)

Kit: a graduated syringe sized close to the volume being measured (a 20-30 mL syringe for headspace, larger if filling the whole body), deionised water, the real vial, cap and full insert set. No balance needed.

Measure the free headspace at working fill:

1. Assemble and charge the vial exactly as in the optimal protocol step 1 (all inserts seated, normal working volume of liquid in place).
2. Draw a known volume of water into the graduated syringe (e.g. fill the barrel to a round graduation). Inject water into the headspace through a headspace tube until the gas space is full to the underside of the septum line, no trapped bubble.
3. Read the syringe before and after; the volume delivered is headspace_V directly (mL). Read at the meniscus with your eye level to it to avoid parallax, and read syringes at the top of the meniscus. Repeat three times and average.

Measure the uniform-bore internal depth D_int:

4. With the vial empty and inserts removed, fill it from the syringe up to the underside of the cap, recording total volume delivered V_body (mL). If it exceeds one syringe-fill, refill and keep a running total.
5. Compute A_x = pi/4 x vial_ID^2 and D_int = V_body x 1000 / A_x (mm), as in the optimal protocol step 6.

Accuracy note: a graduated syringe is typically good to about plus or minus 1 percent of full scale, so a 20 mL syringe gives roughly plus or minus 0.2 mL per fill - tolerable here because the headspace is several mL, but pick the smallest syringe that holds the volume to keep the absolute error down, and prefer the gravimetric method if you have a balance.

## Result -> model

Per vial type, enter into the Geometry sheet:

- Back-solve the total: V_vial_total = headspace_V (measured) + V_charge (the working volume you used) + V_inserts (the value the sheet computes for that insert set). Enter this into Vtot_1 (20 mL build, currently placeholder 20) or Vtot_2 (40 mL build, currently placeholder 40). This is the single change that makes headspace_V correct, because headspace_V = V_vial_total - V_charge - V_inserts will now reproduce your measured headspace by construction at that fill.
- Enter the measured/effective uniform-bore depth into D_int_1 (currently 55 mm) or D_int_2 (currently 95 mm).
- Leave A_x derived from vial_ID as is, unless your caliper internal-diameter reading differs from 25.28 mm, in which case update vial_OD or vial_wall so vial_ID matches the measured bore.
- Record the measured numbers, the temperature, the density value used, and the three-run spread in the Source/assumption column so the figures are no longer placeholders.

The consistency-check (geom_check) compares the entered V_vial_total against the cylinder estimate A_x x D_int. After this protocol the two should agree because both now trace to measured water volumes, and the flag should clear from INCONSISTENT to OK.

## Acceptance checks & pitfalls

- geom_check reads OK: entered V_vial_total agrees with A_x x D_int / 1000 to within about plus or minus 5 percent (tighten the tolerance band if your three-run spread is smaller).
- Sanity vs catalogue: the back-solved V_vial_total for the 20 mL vial should land a little above 20 mL (the nominal figure is "to fill line", the true to-septum volume is larger), consistent with the 57.4 mm total height and 25.28 mm bore. A result near the old 27.6 mL cylinder estimate is the expected reconciliation, not an error.
- Trapped bubble is the dominant error: a single 0.3 mL bubble clinging to an electrode or in the shoulder biases headspace low. Tilt, tap, and inspect against the light before reading every time.
- Fill exactly to the septum plane: the model's headspace is bounded by the cap/septum underside, not the cap top. Filling into the cap recess or stopping at the neck both bias the result. Mark the septum plane if it is hard to see.
- Inserts must be at run depth: headspace_V depends on how far the electrodes and tubes protrude. Seat them exactly as in a real run; a different insertion depth changes V_inserts and invalidates the back-solve.
- Match temperature to density: use the rho_water value for the actual water temperature. Using 1.000 g/mL instead of 0.997 g/mL adds a ~0.3 percent bias - small here but free to avoid.
- Do the same for both vial types: the 20 mL and 40 mL builds have separate placeholders (Vtot_1/Vtot_2, D_int_1/D_int_2). Measuring only one leaves the other inconsistent.
- Read the meniscus at eye level (syringe: top of meniscus) to avoid parallax on the budget route.

## Sources

- [Gravimetric container fill / headspace by water mass and density - USPTO 5,861,554](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5861554)
- [Water density formulations for gravimetric volume calibration - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0955598615000631)
- [Guide to liquid volume measurements: methods and technologies - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2472630325001414)
- [Water density at 25 degC (997.0 kg/m3)](https://kg-m3.com/material/water-25c)
- [Water density at 30 degC (995.6 kg/m3)](https://kg-m3.com/material/water-30c)
- [Water density vs temperature table - Engineering ToolBox](https://www.engineeringtoolbox.com/water-density-specific-weight-d_595.html)
- [Reading a meniscus and graduated-vessel tolerances - Westlab](https://www.westlab.com/blog/how-to-read-a-meniscus-when-using-graduated-cylinders)
- [Measuring liquid volumes in syringes: best practices](https://www.needle.tube/product-articles-3/measuring-liquid-volumes-in-syringes-importance-and-best-practices-2)
- [Pioreactor 20 mL glass vial (OD 27.48 mm, total height 57.4 mm)](https://pioreactor.com/products/20ml-glass-vial)
