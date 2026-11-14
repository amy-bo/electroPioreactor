# Medium for HOB fermentation with in-culture electrolysis

**Names.** AMYBO media are numbered AM001, AM002, AM003… (AMYBO Media, said "Amo 03"): the general AMYBO minimal medium line for HOB lab work and environmental enrichments. A medium formulated for a particular task or organism gets its own name. This document describes **AM003**, Teo Reid's final medium and the current recommendation. AM002 (formerly MC02) is the earlier formulation; AM001 (formerly MC01) acidified only the iron stock, and its mineral stock precipitated. Every medium's full recipe and the chemistry calculated from it are side by side on the **Media** sheet of `electroPioreactorGasModel.xlsx`; add a medium there by typing a new column.

## Background

This document details our proposed total nutrients for hydrogen-oxidising bacteria (HOB) fermentation.  
Nutrients are broken down into:

1. Macronutrient gases,
2. Mesonutrient solution, after [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) with a stronger buffer, and
3. Our modified two-bottle Micronutrient solution.

We require an optimal nutrient solution for HOB fermentation that is also appropriate to use as an electrolyte for in-culture electrolysis to generate hydrogen and oxygen for HOB. The solution should be relatively easy to formulate, and its trace elements component should have a long shelf life.

While many standard and optimised formulations exist for general HOB fermentation, most contain compounds that would have deleterious consequences when subject to electrolysis, for example, evolving ammonia and chlorine, forming hypochlorous acid, etc.

[LiteratureMedia.md](LiteratureMedia.md) discusses over 10 papers describing media used specifically for HOB fermentation with in-culture electrolysis.  Of these it explains the selection of [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252)'s 'Optimal Medium' as the basis for our media formulation. [MediaFormulation.md](MediaFormulation.md) goes on to explain how we derived the longer shelf life trace element solution below from this.

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

Our current mesonutrients are those of Table 2 of Teo Reid's MRes thesis (Imperial College London, 2026), per litre of water. They replace MC02, the earlier formulation still described in [Methodologies/Irvine/Medium.md](../Methodologies/Irvine/Medium.md) and [Methodologies/Crymlyn.md](../Methodologies/Crymlyn.md), which is what those enrichments used:

| Component | Formula | Concentration (g/L) | Concentration (mM) |
|---|---|---|---|
| Disodium hydrogen phosphate | Na₂HPO₄ | 4.26 | 30 |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 4.68 | 30 |
| Potassium sulfate | K₂SO₄ | 0.170 | 0.98 |
| Calcium sulfate dihydrate | CaSO₄·2H₂O | 0.097 | 0.56 |
| Magnesium sulfate heptahydrate | MgSO₄·7H₂O | 0.800 | 3.25 |
| Ammonium sulfate | (NH₄)₂SO₄ | 0.943 | 7.14 |
| Sodium bicarbonate | NaHCO₃ | 3.36 | 40 |

With trace elements given in 'Trace elements in the final medium' below.

### Why this differs from Sydow

[Sydow et al. (2017)'s Supporting Information](https://analyticalsciencejournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Felsc.201600252&file=elsc999-sup-0001-SuppMat.docx) Table S1 gives their 'Optimal Medium' with the same four sulfate salts, no bicarbonate, and less of the two phosphates (Na₂HPO₄ 2.895 g/L; NaH₂PO₄·2H₂O 3.060 g/L), giving a buffer of 40 mM in all. Sydow notes their medium is not pH stable, and the CARMA Hub pump priming final report (2026) records it falling to pH 4.84 under sustained electrolysis, with no growth. Ours therefore has 60 mM of phosphate and 40 mM of bicarbonate.

Teo's medium is, to date, the only one to have given autotrophic growth on CO₂ in the electroPioreactor (*Xanthobacter*, through a heterotrophic-to-autotrophic transition, with an iridium oxide anode and a steel cathode; the transition was not achieved with a platinum-plated titanium anode).

**Watch both electrodes for scale.** SEM/EDX of a discoloured Pt/Ti anode from the earlier, carbon-free medium (University of Edinburgh, via Chris French, personal communication, April 2026) found calcium, carbon and oxygen, suggesting a carbonate. Phosphorus cannot be told apart from platinum by EDX, as the P Kα (2.013 keV) and Pt Mα (2.048 keV) peaks overlap; the Pt peak showed no shoulder, so there was probably not much, but calcium phosphate is not ruled out, and WDS could separate the two. Bingqiao Zhao also found an adherent white deposit, and separately a black coating, on the stainless steel cathodes after heterotrophic runs with electrolysis ([forum, 2 April 2026](https://forum.amybo.org/t/trial-experiment-on-heterotrophic-electrolysis/163)).

So with this medium, watch for two things. Hydrogen evolution raises the pH at the cathode, which favours carbonate (and phosphate) precipitation there, while the pH falls at the anode, where a carbonate would tend to dissolve; why carbonate appeared on the anode is unexplained. And at 60 mM, the stronger phosphate buffer may matter as much as the bicarbonate, since calcium phosphate is even less soluble than the carbonate. Track the electrolysis overpotential and inspect both electrodes; a citric acid wash removes either deposit.

## Micronutrients / Trace Element Solution

Our two-bottle trace element solution, [modified](MediaFormulation.md) from [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) is made up in batches, at concentrations such that 0.050 mL of Mineral Solution and 0.68 mL of Iron Solution are added per 1.000 L of Mesonutrient solution.

#### Iron dose

0.68 mL of Iron Solution per litre gives 36.7 µM of iron, a fifth of the ~183 µM that 3.40 mL (Sydow's level) gives. We follow Teo's thesis here because it is the formulation that has worked. The KIT/Holtmann minimal medium protocol (*Ablauf BES*, sent to us by Lisa van der Sande on 20 March 2026) goes lower still, with 5.25 mg/L of FeSO₄·7H₂O, about 19 µM. We understand this may have been a long-standing error carried forward in the protocol (L. van der Sande, KIT, personal communication, April 2026). Our dose sits between the two, and is worth revisiting as evidence comes in.

### Mineral Solution

| Component | Formula | Concentration (g/L in 0.2 M H₂SO₄) |
|------------|----------|--------------------------------------|
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 1.8 |
| Zinc sulfate heptahydrate | ZnSO₄·7H₂O | 2.4 |
| Manganese(II) sulfate monohydrate | MnSO₄·H₂O | 2.4 |
| Copper(II) sulfate pentahydrate | CuSO₄·5H₂O | 0.48 |
| Nickel(II) sulfate hexahydrate | NiSO₄·6H₂O | 1.5 |
| Cobalt(II) sulfate heptahydrate | CoSO₄·7H₂O | 0.0402 |

### Iron Solution

| Component | Formula | Concentration (g/L in 0.2 M H₂SO₄) |
|------------|----------|--------------------------------------|
| Iron(II) sulfate heptahydrate | FeSO₄·7H₂O | 15.0 |

### Preparing the medium

Make each solution separately and filter-sterilise it; autoclaving was found to change the colour of some of them. The mesonutrient solution is made up in water, but the Mineral and Iron Solutions are made up in 0.2 M H₂SO₄ (11 mL of concentrated sulfuric acid per litre), which keeps the iron and trace metals in solution. Then combine, adding 0.68 mL of Iron Solution and 0.050 mL of Mineral Solution to 1.000 L of mesonutrient solution.

For growth on a carbon source, add 50 mL of 10% w/v sodium gluconate solution (100 g/L, 0.46 M) per litre of mesonutrient solution, giving 0.5% w/v (23 mM) in the final medium.

### Storage and shelf life

We anticipate that, if refrigerated at 4 °C in amber bottles (kept dark), the mineral solution may remain stable for multiple years (target >5 years), and the acidified iron solution for nearly as long (target >3 years) if the bottle headspace is purged with an inert gas (e.g. N₂ or Ar) after opening.

### Trace elements in the final medium

| Component | Formula | Concentration (g/L) |
|---|---|---|
| Iron(II) sulfate heptahydrate | FeSO₄·7H₂O | 0.0102 |
| Manganese(II) sulfate monohydrate | MnSO₄·H₂O | 1.2 ×10⁻⁴ |
| Zinc sulfate heptahydrate | ZnSO₄·7H₂O | 1.2 ×10⁻⁴ |
| Copper(II) sulfate pentahydrate | CuSO₄·5H₂O | 2.4 ×10⁻⁵ |
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 9 ×10⁻⁵ |
| Nickel(II) sulfate hexahydrate | NiSO₄·6H₂O | 7.5 ×10⁻⁵ |
| Cobalt(II) sulfate heptahydrate | CoSO₄·7H₂O | 2.01 ×10⁻⁶ |

## Sydow's elemental composition

The table below is Sydow's own, kept for reference. It does not describe our medium: ours has more sodium and phosphorus (the stronger buffer), carbon from the bicarbonate, and a fifth of the iron (2.05 ×10⁻³ g/L, not 10 ×10⁻³).

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

_<sup>*</sup>_ We believe that [Sydow et al. (2017)'s Supporting Information](https://analyticalsciencejournals.onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1002%2Felsc.201600252&file=elsc999-sup-0001-SuppMat.docx)'s calculation has carried forward the Ni₂SO₄·6H₂O typo and the actual concentration of Ni would be 1.67 ×10⁻⁵. While we don't anticipate this impacting their results further investigation may be prudent.

Their media was also supplied with 200 μg/mL kanamycin for pEG7c maintenance, it is assumed that this will not be required with our strains.

They also note the following:

| Parameter | Value |
|---|---|
| Buffer molarity | 40 mM |
| Conductivity | 6.1 mS/cm |

And that their solution has no carbon species, is not pH stable, but is electrochemically stable. Ours carries 40 mM of bicarbonate and a 60 mM phosphate buffer, so neither the carbon nor the buffer molarity above applies to it.
