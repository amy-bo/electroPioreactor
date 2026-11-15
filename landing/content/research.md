---
title: Research
description: The literature behind the design, our medium, the gas model and other results.
order: 30
---
People have grown hydrogen-oxidising bacteria (HOB) on gases made by electrolysis inside the culture since the 1960s. This page links to that literature, and to our own medium, model and results in the repository.

## The literature

Our [bibliography](https://bibbase.org/show?bib=https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/Literature/HOB%20ferm.%20in-culture%20electrolysis.bib) has 51 references on HOB fermentation by in-culture electrolysis, from 1964 to 2025. The files are in [Literature/](repo:Literature/), and the forum's [Journal Club](https://forum.amybo.org/c/journal-club) discusses new papers.

## The medium

The culture medium both feeds the bacteria and carries the current between the electrodes. Chloride would be turned into bleach at the anode, so ours has none. It is based on the medium of [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252).

The current recipe, AM003, is Teo Reid's (MRes thesis, Imperial College London, 2026). It has a stronger phosphate buffer than Sydow's, added bicarbonate and a fifth of the iron. The recipe and the reasons for it are in [Media/](repo:Media/README.md).

- **Why the medium changed.** Electrolysis and CO₂ sparging together acidify the medium. With the earlier recipe the pH fell to about 4.8 and the bacteria did not grow. A Good's buffer (MOPS) reacted under electrolysis. More phosphate with sodium bicarbonate holds the pH at or above about 6.6.
- **Growth on CO₂.** To date AM003 is the only medium to have given growth on CO₂ in an electroPioreactor. One *Xanthobacter tagetidis* culture in an AEP0.1.1, with a mixed metal oxide anode and a stainless steel cathode, was moved from sodium gluconate to electrolytic hydrogen and sparged CO₂ over 3 to 5 weeks. A platinum-plated titanium anode did not support the transition. Further experiments are ongoing.
- **Operating conditions that worked.** CO₂ sparged for 3 seconds every 10 minutes at 1 bar(g), electrolysis at 5% alternating 5 minutes on and 5 minutes off, 30 °C and 1000 rpm stirring.

Bingqiao Zhao also had electrolysis raise the final optical density of formate-fed *Cupriavidus necator* cultures.

## The gas model

The [gas model](repo:Media/electroPioreactorGasModel.xlsx) is a spreadsheet that works out how much hydrogen and oxygen the electrodes make, how much the bacteria use, and so how long and how often to pulse CO₂. It is a planning tool, and it is not yet fit to set an unattended schedule.

## Other results

- **AEP0.1 training, Edinburgh, November 2025.** Imperial and Edinburgh students built three prototypes. *Cupriavidus metallidurans* grew on sodium gluconate, but a run on CO₂ alone showed no growth, and the platinum-plated anodes discoloured. The [write-up](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1%20Training/README.md) lists what we changed for AEP0.2.
- **Harvey Mudd College clinic.** Student teams [compared anode materials and designed a solenoid pinch valve](repo:PastResearch/HMC-Clinic/), which became AMYBO's [OpenValve](https://amybo.org/projects/other-hardware/openvalve/).
- **Brown University, Harris Lab.** Eli Silver [diagnosed the CO₂ backflow problem](repo:PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md) and tested the venting valve that fixed it.
- **Enrichments from nature.** [Methodologies/](repo:Methodologies/) has protocols for enriching HOB from environmental samples.

## Share your results

Results from other labs make the design better for everyone. Post them on the [forum](https://forum.amybo.org), or add a write-up to the repository with a pull request.
