---
title: What are hydrogen-oxidising bacteria?
description: Bacteria that grow on hydrogen, oxygen and carbon dioxide, and why they could make protein from air and electricity.
section: learn
audience: newcomer
order: 10
---
Hydrogen-oxidising bacteria (HOB) are microbes that can live on gases. They get their energy from hydrogen, breathe oxygen, and build their bodies from carbon dioxide (CO₂) taken from the air. The electroPioreactor is a small, low-cost bioreactor for growing them.

## What they are

Most living things you know get their energy from food: sugars, fats or proteins made by other living things. HOB can do something different. When there is no food around, they can live on three gases:

| Gas | What the bacteria use it for |
|---|---|
| Hydrogen (H₂) | Energy. They "burn" it slowly with oxygen inside the cell, the way we burn sugar. |
| Oxygen (O₂) | To breathe, as we do. |
| Carbon dioxide (CO₂) | Building material. The carbon in every new cell comes from CO₂. |

Add water and a few dissolved minerals (nitrogen, phosphorus, sulphur, iron and other trace elements) and they have everything they need to grow and divide. <!-- source: Media/MediaFormulation.md (macronutrient gases, mesonutrients, trace elements) -->

A living thing that makes its own body from CO₂ is called an **autotroph**. Plants are autotrophs that run on sunlight. HOB are autotrophs that run on hydrogen. Because a mixture of hydrogen and oxygen is called *Knallgas* in German ("bang gas"), older papers call them **Knallgas bacteria**. <!-- source: Literature/HOB ferm. in-culture electrolysis.bib (titles using 'Knallgas' bacteria) -->

Many HOB can also grow on ordinary food, such as sugars. That is useful in the lab: you can check a culture is alive and healthy on sugar before asking it to live on gases alone. <!-- source: docs/steps/step-00-before-you-start.md; docs/glossary.yaml (heterotrophically) -->

## Why people are interested

HOB turn hydrogen, oxygen and CO₂ into cells that are rich in protein. Hydrogen and oxygen can be made from water with electricity, so in principle you can make protein from air, water, a few minerals and electricity.

- **Protein without farmland.** Studies of HOB protein for food and animal feed suggest it could need much less land and water than crops or livestock. <!-- source: Literature bib: Pikaar et al. 2018, doi 10.1021/acs.est.8b00216; Sillman et al. 2019, doi 10.1016/j.gfs.2019.09.007 -->
- **Protein-rich cells.** Published work on HOB grown this way reports biomass of roughly a third to well over half protein by dry weight, depending on the organism. <!-- source: Literature bib: Nyyssölä et al. 2021, doi 10.1021/acsfoodscitech.0c00129 (33 to 37 % protein); R. opacus electrobioreactor thesis abstract (63 %) -->
- **Local production.** A bioreactor that runs on electricity, CO₂ and water does not depend on climate, season or soil, so it could in principle be run almost anywhere.
- **More than food.** Researchers also use HOB to make bioplastics and other chemicals from CO₂. <!-- source: Literature bib (several PHB / bioplastic titles) -->

> **Note:** HOB protein for people is still an active research field. Reviews describe HOB as a novel protein source for human consumption, but that is a research and industry direction, not something the electroPioreactor does. It is laboratory research equipment. <!-- source: Literature bib: Angenent et al. 2022, doi 10.2174/18742858-v16-e2207270 -->

## Some example organisms

HOB are not one species. The ability to live on hydrogen turns up in many unrelated bacteria. A few that appear in this project's sources:

- ***Cupriavidus necator*** is the best-studied HOB. It has had several names over the years (*Hydrogenomonas*, *Ralstonia eutropha*), so you will see all three in the literature. Much of the early work on growing HOB with electrolysis inside the culture used it. <!-- source: Literature bib (Hydrogenomonas H16, Ralstonia eutropha and C. necator titles; Sydow et al. 2017) -->
- ***Xanthobacter tagetidis*** is the baseline organism in this project's gas model. <!-- source: Media/electroPioreactorGasModel.py (organism_sel) -->
- ***Cupriavidus metallidurans*** was grown in the first joint training on the Aseptic electroPioreactor in November 2025. <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md -->
- ***Rhodococcus opacus*** and other Gram-positive HOB have been studied as food-grade protein sources. <!-- source: Literature bib: Nyyssölä et al. 2021 -->

You can also start with no single organism at all, and let a mixed community of HOB from soil, water or a fen develop in the reactor. That is called an **enrichment**. See the methods in `repo:Methodologies/`.

## Where AMYBO and the electroPioreactor fit

[AMYBO](https://amybo.org) created the electroPioreactor to make HOB production affordable, safe and local, as a sustainable alternative protein. <!-- source: README.md; AsepticElectroPioreactor/README.md (Origins) -->

To grow HOB you need a steady supply of hydrogen. Large plants store hydrogen in tanks, which is a fire and explosion risk. The electroPioreactor avoids storing it: it splits a little of the culture's own water with electricity, inside the vial, so hydrogen and oxygen form only as the bacteria need them. CO₂ comes from a SodaStream cylinder. It is built on the [Pioreactor](https://pioreactor.com), an open, low-cost bench-top bioreactor. <!-- source: AsepticElectroPioreactor/README.md -->

There are two main versions:

- The **Aseptic electroPioreactor (AEP)** keeps a single strain free of contamination, for reproducible research. It is being developed with Imperial College London and the University of Edinburgh under CARMA Hub Pump Priming funding.
- The **Mixed-culture electroPioreactor (MEP)** is a lower-cost version for mixed cultures and student projects.

See [Variants](/variants/) for the differences.

## Where next

- [How it works](/how-it-works/): the system end to end, part by part.
- [FAQ](/faq/): safety, cost, what you can grow, and more.
- [Glossary](/glossary/): every term on these pages.
- [Research](/research/): the bibliography, past projects and results.
