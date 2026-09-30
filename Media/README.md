# Medium for HOB fermentation with in-culture electrolysis

## Background

This document details our proposed total nutrients for hydrogen-oxidising bacteria (HOB) fermentation.  
Nutrients are broken down into:

1. Macronutrient gases,
2. Mesonutrient solution as per [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252), and
3. Our modified two-bottle Micronutrient solution.

We require an optimal nutrient solution for HOB fermentation that is also appropriate to use as an electrolyte for in-culture electrolysis to generate hydrogen and oxygen for HOB. The solution should be relatively easy to formulate, and its trace elements component should have a long shelf life.

While many standard and optimised formulations exist for general HOB fermentation, most contain compounds that would have deleterious consequences when subject to electrolysis, for example, evolving ammonia and chlorine, forming hypochlorous acid, etc.

Our companion literature review surveys over ten papers describing media used specifically for HOB fermentation with in-culture electrolysis. Of these, it selects [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252)'s 'Optimal Medium' as the basis for our medium formulation: it avoids the chloride and other species that would evolve chlorine or ammonia under electrolysis, and it is electrochemically stable. From that starting point we derived the longer shelf-life two-bottle trace element solution below, re-casting the trace metals into an acidified mineral stock and a separate acidified iron(II) stock so that each keeps for years.

## Macronutrients

| Component | Formula | Source |
|---|---|---|
| Hydrogen | H₂ | electrolysis of water |
| Oxygen | O₂ | electrolysis of water |
| Carbon Dioxide | CO₂ | sparged from SodaStream cylinder |

Hydrogen should be the limiting nutrient, so its production will be maximised without causing excessive electrode degradation.

Oxygen is produced to excess at a rate that will cause accumulation that limits electrolysis unless purged by carbon dioxide.

The carbon dioxide purge rate is set with this, and hydrogen combustion risk reduction, in mind. The rate is derived in `electroPioreactorGasModel.xlsx`, which ships alongside this document; it is set per reactor from the measured oxygen-evolution rate and the sparge schedule rather than fixed here.

## Mesonutrients

[Sydow et al. (2017)'s Supporting Information](https://analyticalsciencejournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Felsc.201600252&file=elsc999-sup-0001-SuppMat.docx) Table S1 gives their 'Optimal Medium' as:

| Component | Formula | Concentration (g/L) |
|---|---|---|
| Disodium hydrogen phosphate | Na₂HPO₄ | 2.895 |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 3.060 |
| Potassium sulphate | K₂SO₄ | 0.170 |
| Calcium sulphate dihydrate | CaSO₄·2H₂O | 0.097 |
| Magnesium sulphate heptahydrate | MgSO₄·7H₂O | 0.800 |
| Ammonium sulphate | (NH₄)₂SO₄ | 0.943 |

With trace elements given in 'Sydow Trace Elements in final medium' below.

## Micronutrients / Trace Element Solution

Our two-bottle trace element solution, modified from [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252), is made up in batches, at concentrations such that 0.050 mL of Mineral Solution and 3.40 mL of Iron Solution are added per 1.000 L of Mesonutrient solution.

### Mineral Solution

| Component | Formula | Concentration (g/L in 0.2 M H₂SO₄) |
|------------|----------|--------------------------------------|
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 1.8 |
| Zinc sulphate heptahydrate | ZnSO₄·7H₂O | 2.4 |
| Manganese(II) sulphate monohydrate | MnSO₄·H₂O | 2.4 |
| Copper(II) sulphate pentahydrate | CuSO₄·5H₂O | 0.48 |
| Nickel(II) sulphate hexahydrate | NiSO₄·6H₂O | 1.5 |
| Cobalt(II) sulphate heptahydrate | CoSO₄·7H₂O | 0.0402 |

### Iron Solution

| Component | Formula | Concentration (g/L in 0.2 M H₂SO₄) |
|------------|----------|--------------------------------------|
| Iron(II) sulphate heptahydrate | FeSO₄·7H₂O | 15.0 |

### Storage and shelf life

We anticipate that, if refrigerated at 4 °C in amber bottles (kept dark), the mineral solution may remain stable for multiple years (target >5 years), and the acidified iron solution for nearly as long (target >3 years) if the bottle headspace is purged with an inert gas (e.g. N₂ or Ar) after opening.

### Sydow Trace Elements in final medium

| Component | Formula | Concentration (g/L) |
|---|---|---|
| Iron(II) sulphate heptahydrate | FeSO₄·7H₂O | 0.051 |
| Manganese(II) sulphate monohydrate | MnSO₄·H₂O | 1.2 ×10⁻⁴ |
| Zinc sulphate heptahydrate | ZnSO₄·7H₂O | 1.2 ×10⁻⁴ |
| Copper(II) sulphate pentahydrate | CuSO₄·5H₂O | 2.4 ×10⁻⁵ |
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 9 ×10⁻⁵ |
| Nickel(II) sulphate hexahydrate | NiSO₄·6H₂O | 7.5 ×10⁻⁵ |
| Cobalt(II) sulphate heptahydrate | CoSO₄·7H₂O | 2.01 ×10⁻⁶ |

## Preparation

_Verify against your local practice: exact steps and equipment depend on the lab; treat the following as the intended scheme, not a validated SOP._

The medium is assembled from three separately prepared parts so that the heat-sensitive and precipitation-prone components are never autoclaved: an autoclaved base solution, a filter-sterilised mineral (trace-element) stock, and a filter-sterilised iron(II) stock. The two stocks are made up once in dilute acid and stored (see Storage and shelf life); only the base is made fresh for each batch.

**Safety – trace-element salts.** The mineral stock salts, in particular NiSO₄, CoSO₄ and CuSO₄, are CMR (carcinogenic, mutagenic or toxic to reproduction) hazards, and are made up in dilute sulphuric acid (H₂SO₄). Weigh them wearing gloves inside a balance enclosure or fume hood, avoid raising dust, and wear the standard PPE for handling dilute acid (safety glasses, gloves, lab coat). Handle the CaSO₄ and MgSO₄ base salts with routine care.

### Base (phosphate/salt) solution

1. Dissolve the Mesonutrient salts – both phosphates, K₂SO₄, CaSO₄·2H₂O, MgSO₄·7H₂O and (NH₄)₂SO₄ – in most of the final volume of purified water, adding them one at a time and allowing each to dissolve before the next. Add the phosphates first, as they set the buffer; CaSO₄·2H₂O is only sparingly soluble and may need stirring and time.
2. Make up to the working volume.
3. Check the pH. The disodium/monosodium phosphate pair targets a near-neutral phosphate buffer of about pH 7.0; adjust if your salt lots pull it off target, and record the value. (The finished medium is not strongly pH-stable in use – see the note under Final Medium.)
4. Autoclave the base solution (standard 121 °C liquid cycle) and allow it to cool to room temperature before adding the sterile stocks.

### Mineral and iron(II) stocks

1. Make up the Mineral Solution and the Iron Solution in 0.2 M H₂SO₄ at the concentrations tabulated above.
2. **Filter-sterilise both stocks** (0.2 μm) into sterile bottles. **Do not autoclave them:** heating oxidises Fe²⁺ to Fe³⁺ and drives CaSO₄ and iron precipitation, so an autoclaved stock no longer delivers the intended soluble trace metals.
3. Store as described under Storage and shelf life.

### Combining

1. To the cooled, sterile base solution, aseptically add the sterile stocks at the rates given above – 0.050 mL of Mineral Solution and 3.40 mL of Iron Solution per 1.000 L of base – and mix.
2. Add it to the reactor at the working volume for the build (about 15 mL for the 20 mL build, about 30 mL for the 40 mL build) and run at 30 °C.

## Final Medium

[Sydow et al. (2017)'s Supporting Information](https://analyticalsciencejournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Felsc.201600252&file=elsc999-sup-0001-SuppMat.docx) S1 gives the following elemental composition:

| Element | Symbol | Concentration (g/L) |
|---|---|---|
| Sodium | Na | 1.389 |
| Potassium | K | 76 ×10⁻³ |
| Nitrogen | N | 0.2 |
| Magnesium | Mg | 79 ×10⁻³ |
| Calcium | Ca | 22.6 ×10⁻³ |
| Iron | Fe | 10 ×10⁻³ |
| Nickel | Ni | _2.7 ×10⁻⁵ <sup>*</sup>_ |
| Copper | Cu | 6.1 ×10⁻⁶ |
| Chromium | Cr | - |
| Cobalt | Co | 4.2 ×10⁻⁷ |
| Manganese | Mn | 3.9 ×10⁻⁵ |
| Zinc | Zn | 2.73 ×10⁻⁵ |
| Phosphorus | P | 1.24 |
| Sulphur | S | 0.39 |
| Molybdenum | Mo | 3.6 ×10⁻⁵ |
| Chlorine | Cl | - |
| Carbon | C | - |

_<sup>*</sup>_ We believe that [Sydow et al. (2017)'s Supporting Information](https://analyticalsciencejournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Felsc.201600252&file=elsc999-sup-0001-SuppMat.docx)'s calculation has carried forward the Ni₂SO₄·6H₂O typo, and that the actual concentration of Ni would be 1.67 ×10⁻⁵. We do not anticipate this affecting their results.

Their medium was also supplied with 200 μg/mL kanamycin for pEG7c maintenance. We assume this will not be required with our strains.

They also note the following:

| Parameter | Value |
|---|---|
| Buffer molarity | 40 mM |
| Conductivity | 6.1 mS/cm |

And that the solution has no carbon species, is not pH stable, but is electrochemically stable.
