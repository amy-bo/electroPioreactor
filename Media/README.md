# Media for HOB fermentation with in-culture electrolysis

## Background

This document details our proposed total nutrients for hydrogen-oxidising bacteria (HOB) fermentation.  
Nutrients are broken down into 
1. Macronutrient gasses, 
2. Mesonutrient solution as per [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252), and 
3. Our modified two-bottle Micronutrient solution.

We require a long shelf life, relatively easy to formulate, optimal micronutrient solution for HOB fermentation that is also appropriate to use as an electrolyte for in-culture electrolysis to generate hydrogen and oxygen for HOB.  

While many standard and optimised formulations exist for general HOB fermentation, most contain compounds that would have deleterious consequences when subject to electrolysis, for example, evolving chlorine, ammonia, etc.

[LiteratureMedia.md](LiteratureMedia.md) discusses over 10 papers describing media used specifically for HOB fermentation with in-culture electrolysis.  Of these it explains the selection of [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) as the basis for our media formulation. [MediaFormulation.md](MediaFormulation.md) goes on to explain how we derived the longer shelf life trace element solution below from this.

## Macronutrients

| Component | Formula | Source |
|---|---|---|
| Oxygen | O₂ | electrolysis of water |
| Hydrogen | H₂ | electrolysis of water |
| Carbon Dioxide | CO₂ | sparged from Sodastream cylinder |

All of the above are delivered to excess.  

Hydrogen should be the limiting nutrient, so its production will be maximised without causing excessive electrode degradation.

Oxygen is produced at a rate that will cause accumulation that limits electrolysis unless purged by carbon dioxide.  

The carbon dioxide purge rate will be set with this and hydrogen combustion risk reduction in mind.  [See calculations](https://docs.google.com/spreadsheets/d/1Aeqz_CXZz-brBo-cXe8sFfjbX8h42vEcrhPH9bGLhIA/edit?gid=0#gid=0).

## Mesonutrients

[Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252)'s Supporting Information Table S1 gives their "Optimal Medium as:

| Component | Formula | Concentration (g/L) |
|---|---|---|
| Disodium hydrogen phosphate | Na₂HPO₄ | 2.895 |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 3.060 |
| Potassium sulfate | K₂SO₄ | 0.170 |
| Calcium sulfate dihydrate | CaSO₄·2H₂O | 0.097 |
| Magnesium sulfate heptahydrate | MgSO₄·7H₂O | 0.800 |
| Ammonium sulfate | (NH₄)₂SO₄ | 0.943 |

With trace elements given in 'Sydow Trace Nutrients in final media' below.

## Micronutrients / Trace Element Solution

Our two-bottle trace element solution, [modified](MediaFormulation.md) from [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) is made up in batches, at concentrations such that a few drops are added to a batch of macronutrient solution.

### Mineral solution

| Component | Formula | Concentration (g/L H₂O) |
|------------|----------|--------------------------------------|
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 1.8 |
| Zinc sulfate heptahydrate | ZnSO₄·7H₂O | 2.4 |
| Manganese(II) sulfate monohydrate | MnSO₄·H₂O | 2.4 |
| Copper(II) sulfate pentahydrate | CuSO₄·5H₂O | 0.48 |
| Nickel(II) sulfate hexahydrate | Ni₂SO₄·6H₂O | 1.5 |
| Cobalt(II) sulfate heptahydrate | CoSO₄·7H₂O | 0.040 |

### Iron solution

| Component | Formula | Concentration (g/L in 0.2 M H₂SO₄) |
|------------|----------|--------------------------------------|
| Iron(II) sulfate heptahydrate | FeSO₄·7H₂O | 15.0 |

### Storage and shelf life

We anticipate that, if refrigerated at 4 °C in amber bottles (kept dark), the mineral solution may remain stable for multiple years (target >5 years), and the acidified iron solution for >3 years if the bottle headspace is purged with an inert gas (e.g. N₂ or Ar) after opening.

### Sydow Trace Elements in final media

| Component | Formula | Concentration (g/L) |
|---|---|---|
| Iron(II) sulfate heptahydrate | FeSO₄·7H₂O | 0.051 |
| Manganese(II) sulfate monohydrate | MnSO₄·H₂O | 1.2 ×10⁻⁴ |
| Zinc sulfate heptahydrate | ZnSO₄·7H₂O | 1.2 ×10⁻⁴ |
| Copper(II) sulfate pentahydrate | CuSO₄·5H₂O | 2.4 ×10⁻⁵ |
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 9 ×10⁻⁵ |
| Nickel(II) sulfate hexahydrate | Ni₂SO₄·6H₂O | 7.5 ×10⁻⁵ |
| Cobalt(II) sulfate heptahydrate | CoSO₄·7H₂O | 2.01 ×10⁻⁶ |

## Final Media

[Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252)'s Supporting Information Table S1 gives the following elemental composition:

| Element | Symbol | Concentration (g/L) |
|---|---|---|
| Sodium | Na | 1.389 |
| Potassium | K | 76 ×10⁻³ |
| Nitrogen | N | 0.2 |
| Magnesium | Mg | 79 ×10⁻³ |
| Calcium | Ca | 22.6 ×10⁻³ |
| Iron | Fe | 10 ×10⁻³ |
| Nickel | Ni | 2.7 ×10⁻⁵ |
| Copper | Cu | 6.1 ×10⁻⁶ |
| Chromium | Cr | - |
| Cobalt | Co | 4.2 ×10⁻⁷ |
| Manganese | Mn | 3.9 ×10⁻⁵ |
| Zinc | Zn | 2.73 ×10⁻⁵ |
| Potassium | P | 1.24 |
| Sulphur | S | 0.39 |
| Molybdenum | Mo | 3.6 ×10⁻⁵ |
| Chlorine | Cl | - |
| Carbon | C | - |

Their media was also supplied with 200 μg/mL kanamycin for pEG7c maintenance, it is assumed that this will not be required with our strains.

They also note the following:

| Parameter | Value |
|---|---|
| Buffer molarity | 40 mM |
| Conductivity | 6.1 mS/cm |

And that the solution has no carbon species, is not pH stable but is electrochemically stable.