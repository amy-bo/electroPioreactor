---
title: Research
description: The literature behind the design, our medium, the gas model and the results so far.
order: 30
---
People have grown hydrogen-oxidising bacteria (HOB) on gases made by electrolysis inside the culture since the 1960s. This page links to that literature, and to our own medium, model and results in the repository.

## The literature

Our [bibliography](https://bibbase.org/show?bib=https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/Literature/HOB%20ferm.%20in-culture%20electrolysis.bib) has 51 references on HOB fermentation by in-culture electrolysis, from 1964 to 2025. The files are in [Literature/](repo:Literature/), and the forum's [Journal Club](https://forum.amybo.org/c/journal-club) discusses new papers.

## The medium

The culture medium both feeds the bacteria and carries the current between the electrodes. Chloride would be turned into bleach at the anode, so ours has none. It is based on the medium of [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252).

The current recipe, AM003, is Teo Reid's (MRes thesis, Imperial College London, 2026). It has a stronger phosphate buffer than Sydow's, added bicarbonate and a fifth of the iron. To date it is the only medium to have given growth on CO₂ in the electroPioreactor, with *Xanthobacter tagetidis*, a mixed metal oxide anode and a stainless steel cathode. The recipe and the reasons for it are in [Media/](repo:Media/README.md).

Bingqiao Zhao has also grown *Cupriavidus necator* autotrophically on formate.

## The gas model

The [gas model](repo:Media/electroPioreactorGasModel.xlsx) is a spreadsheet that works out how much hydrogen and oxygen the electrodes make, how much the bacteria use, and so how long and how often to pulse CO₂. It is a planning tool, and it is not yet fit to set an unattended schedule.

## Results so far

- **AEP0.1 training, Edinburgh, November 2025.** Imperial and Edinburgh students built three prototypes. *Cupriavidus metallidurans* grew on sodium gluconate, but a run on CO₂ alone showed no growth, and the platinum-plated anodes discoloured. The [write-up](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1%20Training/README.md) lists what we changed for AEP0.2.
- **Harvey Mudd College clinic.** Student teams [compared anode materials and designed a solenoid pinch valve](repo:PastResearch/HMC-Clinic/), which became AMYBO's [OpenValve](https://amybo.org/projects/other-hardware/openvalve/).
- **Brown University, Harris Lab.** Eli Silver [diagnosed the CO₂ backflow problem](repo:PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md) and tested the venting valve that fixed it.
- **Enrichments from nature.** [Methodologies/](repo:Methodologies/) has protocols for enriching HOB from environmental samples.

## Share your results

Results from other labs make the design better for everyone. Post them on the [forum](https://forum.amybo.org), or add a write-up to the repository with a pull request.
