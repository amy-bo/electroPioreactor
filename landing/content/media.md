---
title: Culture media
description: The AMYBO chloride-free minimal media for growing hydrogen-oxidising bacteria with in-culture electrolysis, with recipes, rationale, preparation and sterilisation.
section: research
audience: expert
order: 30
---

The electroPioreactor's culture medium does two jobs. It feeds the bacteria, and it is the electrolyte the electrodes split to make hydrogen and oxygen. So it must contain no chloride, which the anode would turn into chlorine and bleach, and it must keep for a long time on the shelf. This page gives the recipes and the reasons for them.

> **Note:** Abbreviations: HOB, hydrogen-oxidising bacteria; SID, strong-ion difference; UdG, University of Girona. AMYBO media are numbered AM001, AM002, AM003 (AMYBO Media). AM002 was formerly called MC02, AM001 MC01. <!-- source: Media/README.md -->

## Which medium to use

| Medium | Status | What it is |
| --- | --- | --- |
| **AM003** | **Recommended** | Teo Reid's final medium: AM002's salts with 30 + 30 mM phosphate, 40 mM sodium bicarbonate and a fifth of the iron. The AMYBO minimal medium for HOB lab work and enrichments |
| AM002 | Historical | The Sydow et al. (2017) optimal medium with its trace metals split into two acidified stocks; chloride-free, long shelf life. Used in the early electroPioreactor runs |
| AM001 | Historical, don't use | As AM002, but only the iron stock was acidified; its mineral stock precipitated |
| UdG phosphate | External reference | The University of Girona HOB medium (Pous et al. 2022, 2023). Known to work, but contains calcium chloride |

<!-- source: Media sheet of Media/electroPioreactorGasModel.xlsx, rows 14-17 -->

Every medium's full recipe, and the chemistry computed from it, sit side by side on the **Media** sheet of [`electroPioreactorGasModel.xlsx`](repo:Media/electroPioreactorGasModel.xlsx). To add a medium, type a new column there; the [gas model](/gas-model/) then calculates its ion balance, pH, conductivity and chlorine risk.

## Why a chloride-free medium

Most HOB media were designed for hydrogen supplied as a gas. Under electrolysis, many of their ingredients cause trouble: chloride is oxidised at the anode to chlorine and hypochlorous acid, a biocide, and some formulations evolve ammonia. [`LiteratureMedia.md`](repo:Media/LiteratureMedia.md) surveys over ten papers that grew HOB with in-culture electrolysis and selects the Sydow et al. (2017) "Optimal Medium" as the starting point, because:

- it is low in chloride and free of organic carbon, so it is electrochemically stable;
- Sydow et al. reported fast electroautotrophic growth of *Cupriavidus necator* (specific growth rate about 0.09 h⁻¹), essentially no lag, and no visible electrode fouling;
- its aim, rapid growth, matches ours, unlike media designed to stress cells into storing polyhydroxybutyrate.

Sydow's trace-element stock was acidified with hydrochloric acid, its only chloride. Researchers in the corresponding author's current lab reported that the stock turns from blue to yellow within days and precipitates within weeks to months. [`MediaFormulation.md`](repo:Media/MediaFormulation.md) explains why: at pH above 1, Fe²⁺ oxidises to Fe³⁺ in air, which hydrolyses and precipitates and can carry the other trace metals with it; Cu²⁺ speeds that oxidation; and HCl gas escapes each time the bottle is opened.

So the AMYBO media split the trace metals into two stocks, an iron(II) stock and a mineral stock, both in 0.2 M sulphuric acid. If the iron precipitates, only the iron stock needs remaking; sulphuric acid does not gas off; and the medium becomes fully chloride-free. An early mineral stock made in deionised water precipitated; adding sulphuric acid to 0.1 M redissolved it, and the protocol moved to 0.2 M. <!-- source: Media/MediaFormulation.md, "Composition" -->

## Macronutrients

| Nutrient | Source |
| --- | --- |
| Hydrogen, H₂ | Electrolysis of water at the cathode |
| Oxygen, O₂ | Electrolysis of water at the anode |
| Carbon dioxide, CO₂ | Pulsed from a SodaStream cylinder |

Hydrogen is meant to be the limiting nutrient. Electrolysis makes more oxygen than the bacteria use, so the CO₂ pulses also flush oxygen from the headspace; the [gas model](/gas-model/) sizes those pulses for each reactor rather than fixing them here.

## AM003 (recommended)

Grams per litre of finished medium. <!-- source: Media sheet of Media/electroPioreactorGasModel.xlsx, column AM003 -->

| Component | Formula | g/L |
| --- | --- | --- |
| Disodium hydrogen phosphate | Na₂HPO₄ | 4.26 |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 4.68 |
| Sodium bicarbonate | NaHCO₃ | 3.36 |
| Potassium sulphate | K₂SO₄ | 0.170 |
| Calcium sulphate dihydrate | CaSO₄·2H₂O | 0.097 |
| Magnesium sulphate heptahydrate | MgSO₄·7H₂O | 0.800 |
| Ammonium sulphate | (NH₄)₂SO₄ | 0.943 |
| Iron stock (below) | – | 0.68 ml/L, giving 0.0102 g/L FeSO₄·7H₂O |
| Mineral stock (below) | – | 0.05 ml/L |

That is 30 mM of each phosphate and 40 mM bicarbonate. Per the recipe source, each solution is filter-sterilised. An optional 50 ml/L of 10 % sodium gluconate allows growth on a carbon source; the gas model does not include it. The source is Teo Reid's MRes thesis (Table 2 and the Medium section), which is not in the repository. <!-- CHECK: the full AM003 preparation sequence (in particular how the bicarbonate is added and sterilised) is only summarised in the workbook as "Filter-sterilise each solution"; confirm against the thesis -->

## AM002

The base salts are Sydow et al. (2017) Supporting Information Table S1; the trace metals come from the two stocks below. <!-- source: Media/README.md -->

| Component | Formula | g/L |
| --- | --- | --- |
| Disodium hydrogen phosphate | Na₂HPO₄ | 2.895 |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 3.060 |
| Potassium sulphate | K₂SO₄ | 0.170 |
| Calcium sulphate dihydrate | CaSO₄·2H₂O | 0.097 |
| Magnesium sulphate heptahydrate | MgSO₄·7H₂O | 0.800 |
| Ammonium sulphate | (NH₄)₂SO₄ | 0.943 |
| Iron stock | – | 3.40 ml/L |
| Mineral stock | – | 0.050 ml/L |

Sydow et al. give the medium a buffer molarity of 40 mM and a conductivity of 6.1 mS/cm, and note it has no carbon species, is not pH-stable, but is electrochemically stable. Their medium also carried 200 µg/ml kanamycin to maintain a plasmid; we assume our strains will not need it.

## Trace-element stocks

Both stocks are made up in 0.2 M H₂SO₄, filter-sterilised and never autoclaved. AM002 and AM003 use the same stocks; AM003 doses a fifth as much iron stock.

**Mineral stock** (dose 0.050 ml per litre of medium):

| Component | Formula | g/L of stock | g/L in medium |
| --- | --- | --- | --- |
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 1.8 | 9 × 10⁻⁵ |
| Zinc sulphate heptahydrate | ZnSO₄·7H₂O | 2.4 | 1.2 × 10⁻⁴ |
| Manganese(II) sulphate monohydrate | MnSO₄·H₂O | 2.4 | 1.2 × 10⁻⁴ |
| Copper(II) sulphate pentahydrate | CuSO₄·5H₂O | 0.48 | 2.4 × 10⁻⁵ |
| Nickel(II) sulphate hexahydrate | NiSO₄·6H₂O | 1.5 | 7.5 × 10⁻⁵ |
| Cobalt(II) sulphate heptahydrate | CoSO₄·7H₂O | 0.0402 | 2.01 × 10⁻⁶ |

**Iron stock**: iron(II) sulphate heptahydrate, FeSO₄·7H₂O, 15.0 g/L of stock. At 3.40 ml/L (AM002) it gives 0.051 g/L in the medium; at 0.68 ml/L (AM003), 0.0102 g/L.

> **Expert:** Sydow et al.'s Table S1 lists "Ni₂SO₄·6H₂O", which appears to be a typographical error; nickel(II) sulphate hexahydrate is used here. We believe their elemental table carried the error forward, and that their true Ni concentration would be 1.67 × 10⁻⁵ g/L rather than 2.7 × 10⁻⁵ g/L. We do not expect this to have affected their results. <!-- source: Media/README.md, Media/MediaFormulation.md -->

**Storage.** Refrigerated at 4 °C in amber bottles, the mineral stock is expected to keep for several years (target more than 5) and the iron stock nearly as long (target more than 3) if its headspace is purged with nitrogen or argon after opening. These are targets, not measured shelf lives.

## Computed composition

From the Media sheet, as weighed (before any speciation solve). Ionic strength counts the stock acid's protons as free ions, which overstates AM002's by about 2 % ([`TODO.md`](repo:Media/TODO.md)).

| Quantity | AM002 | AM003 | UdG phosphate |
| --- | --- | --- | --- |
| Total phosphate (mM) | 40.0 | 60.0 | 37.3 |
| Bicarbonate (mM) | 0 | 40.0 | 12.5 |
| Ammonium (mM) | 14.3 | 14.3 | 7.1 |
| Chloride (mM) | 0 | 0 | 0.18 |
| Strong-ion difference (mM) | 44.7 | 115.4 | 63.1 |
| Ionic strength (mM) | 123 | 200 | 110 |
| Ideal conductivity, Kohlrausch sum (mS/cm) | 9.7 | 16.3 | 9.1 |

The ideal conductivity is before the model's ionic-strength and temperature corrections, so it is higher than a measured value would be. Higher ionic strength lowers the electrolyte's resistance and so the cell voltage; [Liu et al. (2016)](https://doi.org/10.1126/science.aaf5039) reported better electrolysis performance at higher phosphate concentration.

## Preparation

> **Note:** Verify against your local practice. Exact steps and equipment depend on the lab; this is the intended scheme for AM002, not a validated standard operating procedure. <!-- source: Media/README.md, "Preparation" -->

The medium is made from three parts, so that heat-sensitive and precipitation-prone components are never autoclaved: an autoclaved base solution, a filter-sterilised mineral stock and a filter-sterilised iron(II) stock. The stocks are made once and stored; only the base is made fresh.

**Base solution**

1. Dissolve the base salts in most of the final volume of purified water, one at a time, each fully before the next. Add the phosphates first, as they set the buffer. Calcium sulphate dissolves only slowly and may need stirring and time.
2. Make up to volume.
3. Check the pH. The phosphate pair targets about pH 7.0; adjust if your salt lots pull it off target, and record the value.
4. Autoclave (standard 121 °C liquid cycle) and cool to room temperature.

**Stocks**

1. Make up the mineral and iron stocks in 0.2 M H₂SO₄ at the concentrations above.
2. Filter-sterilise each (0.2 µm) into sterile bottles. Do not autoclave them: heat oxidises Fe²⁺ to Fe³⁺ and drives iron and calcium sulphate precipitation.
3. Store as above.

**Combining**

1. To the cooled, sterile base, add the stocks aseptically at their doses per litre, and mix.
2. Fill the reactor to its working volume: about 30 ml for the 40 ml AEP0.2, about 15 ml for 20 ml builds. Run at 30 °C.

> **Safety:** The nickel, cobalt and copper sulphates in the mineral stock are carcinogenic, mutagenic or toxic to reproduction. Weigh them wearing gloves inside a balance enclosure or fume hood, avoid raising dust, and wear safety glasses, gloves and a lab coat for the dilute sulphuric acid.

## Tests on your medium

These [protocols](repo:Media/protocols/) check how a medium behaves in the reactor, and feed the [gas model](/gas-model/):

- [pH through a growth run](repo:Media/protocols/ph-growth-run.md): ammonium uptake releases acid, and the phosphate buffer must absorb it.
- [Free and combined chlorine](repo:Media/protocols/chlorine-species.md): a DPD assay, needed for any medium with chloride.
- [Dissolved oxygen](repo:Media/protocols/dissolved-oxygen.md): the organism's oxygen band in your medium.

## Literature behind it

The survey in [`LiteratureMedia.md`](repo:Media/LiteratureMedia.md) groups the media found by lineage:

| Lineage | Papers |
| --- | --- |
| Original formulations | Liu et al. 2016 (low ionic strength phosphate, better at higher); Sydow et al. 2017 (chloride-low, organic-free minimal); Al Rowaihi et al. 2018 (nutrient deprivation for polyhydroxybutyrate) |
| From Sydow et al. | Stöckl et al. 2020; Dinges et al. 2024; Langsdorf et al. 2024 |
| From Liu et al. | Feng et al. 2023 (higher phosphate to enrich halotolerant HOB) |
| From Matassa et al. 2016 | Pous et al. 2022, 2023 (less ammonium, chloride retained) |
| From DSMZ medium 81 | Givirovskiy et al. 2019 and Ruuskanen et al. 2021 (chlorides replaced with sulphates); Nyyssölä et al. 2021 (with vitamins) |

Components left out of Sydow's medium, and so of AM002, include boron, vanadium, chelating agents and vitamins. Several other media include them; we only intend to add them if an organism of interest needs them.

Sourcing the reagents: see the forum thread [HOB culture medium ingredients](https://forum.amybo.org/d/22-hob-culture-medium-ingredients/7). For what HOB are and why they matter, see [What is HOB?](/what-is-hob/); for open questions, [Research](/research/).
