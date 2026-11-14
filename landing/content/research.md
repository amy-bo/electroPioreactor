---
title: Research
description: The literature behind in-culture electrolysis, past student projects, enrichment methods, CARMA project results, and how to cite and contribute.
section: research
audience: everyone
order: 10
---
The electroPioreactor rests on sixty years of research into growing hydrogen-oxidising bacteria (HOB) on gas made by electrolysis inside the culture. This page collects that literature, the projects that have already improved the design, the methods in use, and how to cite the work or add your own results.

## The bibliography

The project keeps a bibliography on HOB fermentation by in-culture electrolysis: 51 references from 1964 to 2025, as BibTeX and CSL JSON in [Literature/](repo:Literature/). <!-- source: Literature/HOB ferm. in-culture electrolysis.bib (51 entries) -->

**[Browse the bibliography on BibBase](https://bibbase.org/show?bib=https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/Literature/HOB%20ferm.%20in-culture%20electrolysis.bib)**

AMYBO also keeps a small group [Zotero library](https://www.zotero.org/groups/6254483/amybo/library) for its [Journal Club](https://forum.amybo.org/c/journal-club) on the forum. <!-- source: Literature/README.md -->

### Themes

- **Early electrolytic culture (1964 to 1981).** Growing "Knallgas" bacteria (an older name for HOB) on hydrogen and oxygen made by electrolysing the culture medium itself, first for closed life-support systems in space.
- **Bioelectrochemical systems.** Electrode materials, cell voltage and medium design for water electrolysis at neutral pH in a living culture, and hybrid "water-splitting" systems that pair a catalyst with bacteria.
- **Protein from electricity.** Electro-cultivation of HOB as protein-rich biomass for food and feed, including pilot systems with direct air capture of CO₂ and recycled nitrogen.
- **Land and resource use.** Studies of whether microbial protein could decouple protein production from farmland.
- **Chemicals and bioplastics.** Polyhydroxybutyrate (PHB), alcohols and other products from CO₂ by electrosynthesis.

See [What are HOB?](/what-is-hob/) for the plain-language background.

### Key papers

<!-- source: Literature/HOB ferm. in-culture electrolysis.json (author, issued, title, DOI) -->

| Year | Authors | Title |
|---|---|---|
| 1964 | Foster and Litchfield | [A continuous culture apparatus for the microbial utilization of hydrogen produced by electrolysis of water in closed-cycle space systems](https://doi.org/10.1002/bit.260060406) |
| 1965 | Schlegel and Lafferty | [Growth of 'Knallgas' bacteria (Hydrogenomonas) using direct electrolysis of the culture medium](https://doi.org/10.1038/205308b0) |
| 1967 | Schuster and Schlegel | [Chemolithotrophes Wachstum von Hydrogenomonas H16 im Chemostaten mit elektrolytischer Knallgaserzeugung](https://doi.org/10.1007/BF00409745) |
| 2015 | Torella et al. | [Efficient solar-to-fuels production from a hybrid microbial–water-splitting catalyst system](https://doi.org/10.1073/pnas.1424872112) |
| 2016 | Liu et al. | [Water splitting–biosynthetic system with CO₂ reduction efficiencies exceeding photosynthesis](https://doi.org/10.1126/science.aaf5039) |
| 2017 | Sydow et al. | [Growth medium and electrolyte: how to combine the different requirements on the reaction solution in bioelectrochemical systems using *Cupriavidus necator*](https://doi.org/10.1002/elsc.201600252) |
| 2018 | Pikaar et al. | [Decoupling livestock from land use through industrial feed production pathways](https://doi.org/10.1021/acs.est.8b00216) |
| 2019 | Givirovskiy et al. | [Electrode material studies and cell voltage characteristics of the in situ water electrolysis performed in a pH-neutral electrolyte in bioelectrochemical systems](https://doi.org/10.1016/j.heliyon.2019.e01690) |
| 2019 | Givirovskiy et al. | [In situ water electrolyzer stack for an electrobioreactor](https://doi.org/10.3390/en12101904) |
| 2019 | Sillman et al. | [Bacterial protein for food and feed generated via renewable energy and direct air capture of CO₂: can it reduce land and water use?](https://doi.org/10.1016/j.gfs.2019.09.007) |
| 2021 | Ruuskanen et al. | [Neo-Carbon Food concept: a pilot-scale hybrid biological–inorganic system with direct air capture of carbon dioxide](https://doi.org/10.1016/j.jclepro.2020.123423) |
| 2021 | Nyyssölä et al. | [Production of endotoxin-free microbial biomass for food applications by gas fermentation of Gram-positive H₂-oxidizing bacteria](https://doi.org/10.1021/acsfoodscitech.0c00129) |
| 2022 | Angenent et al. | [Hydrogen oxidizing bacteria as novel protein source for human consumption: an overview](https://doi.org/10.2174/18742858-v16-e2207270) |
| 2023 | Pous et al. | [Electricity-driven microbial protein production: effect of current density on biomass growth and nitrogen assimilation](https://doi.org/10.1016/j.jece.2023.111550) |
| 2025 | Rovira-Alsina et al. | [Empowering microbial proteins: continuous electro-fermentation of hydrogen-oxidizing bacteria from water, urea and carbon dioxide](https://doi.org/10.1016/j.cej.2025.171375) |

Sydow et al. (2017) is the basis of the project's culture medium, chosen because it avoids chloride and other species that electrolysis would turn into chlorine or ammonia. See [Media](/media/). <!-- source: Media/MediaFormulation.md (Background) -->

## Past research projects

### Harvey Mudd College clinic: anode and valve

A Harvey Mudd College clinic team worked on two parts of the electroPioreactor, in an anode team and a valve team. Their outputs are in [PastResearch/HMC-Clinic/](repo:PastResearch/HMC-Clinic/), including a [poster](repo:PastResearch/HMC-Clinic/AMYBO%20Poster%20Presentation.pptx.pdf) and the teams' files, dated May 2025. The pinch valve went on to become AMYBO's [OpenValve](https://amybo.org/projects/other-hardware/openvalve/). <!-- source: README.md; PastResearch/HMC-Clinic/ (zip names dated 20250510) -->

- **Anode materials.** The anode team compared electrode pairs (nickel, graphite, platinum and stainless steel) for current density with a potentiostat, and for bacterial growth by the Pioreactor's optical density (OD) reading. A nickel anode with a stainless steel cathode gave the highest current density, but fouled with a black deposit that also distorted OD readings; platinum pairs gave the highest OD. They recommended analysing the debris for food safety before replacing platinum. <!-- source: PastResearch/HMC-Clinic/AnodeTeamFiles/Anode Writeup.docx -->
- **Solenoid pinch valve.** The valve team designed a 3D-printed, lever-assisted solenoid pinch valve that fully closes 1/16 inch bore silicone tubing against CO₂ pressure and opens at 12 V, drawing at most 2.36 A at 11.31 V. They noted alignment and size improvements for a next version. <!-- source: PastResearch/HMC-Clinic/ValveTeamFiles/Valve Team Tests and Results.docx -->

### Brown University, Harris Lab: CO₂ backflow

Culture was being drawn back up the CO₂ sparging tube between sparges, as [reported on the forum](https://forum.amybo.org/t/co2-sparger-drawback/52). Eli Silver of [Brown's Harris Lab](https://sites.brown.edu/harrislab/) reproduced it and found the cause: the solenoid valve then in use had no vent, so pure CO₂ trapped between valve and culture dissolved into the medium, the pressure fell, and the culture was sucked up the tube. A three-way solenoid valve with a vent let air in instead and stopped the backflow. A follow-up tested a revised regulator, needle valve and vented solenoid assembly. <!-- source: PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md; 2.BackflowTestingWithRevisedComponents-EliSilver.md -->

- Diagnosis: [PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md](repo:PastResearch/Brown-HarrisLab/1.CO2backflowDiagnosis-EliSilver.md)
- Testing with revised components: [PastResearch/Brown-HarrisLab/2.BackflowTestingWithRevisedComponents-EliSilver.md](repo:PastResearch/Brown-HarrisLab/2.BackflowTestingWithRevisedComponents-EliSilver.md)
- Venting solenoid options: [Components/CO2 transfer/](repo:Components/CO2%20transfer/)

## CARMA project results

The Aseptic electroPioreactor (AEP) is being developed under CARMA Hub Pump Priming funding (see [About](/about/)). Results so far are in [AsepticElectroPioreactor/CARMA_PumpPriming/Results/](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/), and the project's [meeting notes](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Meetings.md) are in the same folder. The story of the training week, with photographs of the discoloured anodes, is on the [AEP page](/aep/#what-we-learned-from-the-first-runs).

### AEP0.1 training, November 2025

Imperial College London and University of Edinburgh students assembled and calibrated three AEP0.1 prototypes at joint training in Edinburgh from 18 to 21 November 2025. The write-up records: <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md -->

- A heterotrophic culture of *Cupriavidus metallidurans* was established on the project medium plus sodium gluconate.
- An autotrophic run in four reactors (carbon-free medium, 20 ml, about 17 hours at 30 °C) showed no growth. Possible causes listed: medium composition, high voltage, uneven temperature, ineffective CO₂ sparging and oxygen removal, and anode discolouration.
- Continuous CO₂ sparging caused water in the gas lines, made the sparging tube's position critical and disturbed OD readings, so the design returned to intermittent sparging.
- Platinum-plated titanium anodes discoloured brown on the side facing the cathode, with rainbow colours further away (photographs in [AsepticElectroPioreactor/CARMA_PumpPriming/Results/Anode discolouration/](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/Anode%20discolouration/)).
- A software setup fault was traced to a [Raspberry Pi Imager issue](https://github.com/raspberrypi/rpi-imager/issues/1170) and solved with an earlier Imager version.

Full write-up: [AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1%20Training/README.md). What changed in the design as a result is on [Which electroPioreactor?](/variants/).

> **Note:** Calibration results and further culture results from the training are still to be added to the write-up.

## Methodologies

Worked protocols for enriching HOB from environmental samples, in [Methodologies/](repo:Methodologies/): <!-- source: Methodologies/Crymlyn.md; Methodologies/Irvine/README.md -->

- **Crymlyn Fen** ([Methodologies/Crymlyn.md](repo:Methodologies/Crymlyn.md)): a home-lab enrichment protocol using an AEP0.1, with two medium options. Option A is the project medium AM002, adapted only for home access, so results stay comparable with the CARMA experiments.
- **Irvine River** ([Methodologies/Irvine/](repo:Methodologies/Irvine/)): enrichment using an AEP0.1.1 and AM002 medium from the University of Edinburgh, in three documents: [medium](repo:Methodologies/Irvine/Medium.md), [field sampling](repo:Methodologies/Irvine/Sampling.md) and [enrichment](repo:Methodologies/Irvine/Enrichment.md), whose stages run from initial HOB selection and serial transfer to confirming growth depends on electrolysis.

The culture media and the gas and electrolysis model behind them are on [Media](/media/) and [Gas model](/gas-model/). AMYBO's own site has more general pages on the [growth medium](https://amybo.org/projects/media/), [methods](https://amybo.org/projects/methods/) (enrichment, sampling and medium protocols, including one you can follow at home) and [literature](https://amybo.org/projects/literature/).

## Earlier work

The 2024 electroPioreactor v0.02 and how the design got from there to today are on [History](/history/). AMYBO's [first experiments](https://amybo.org/projects/past/experiments/) from 2023 and 2024, including the [anode](https://amybo.org/projects/past/experiments/electrolysis/) and [CO₂ sparging](https://amybo.org/projects/past/experiments/co2-sparging/) pages, are kept on amybo.org.

## How to cite

The repository has no citation file yet. Until it does, cite the repository and the version you used, for example:

> AMYBO. *electroPioreactor*. GitHub, https://github.com/amy-bo/electroPioreactor (commit or release used; accessed *date*).

Cite the build guide as https://docs.electropioreactor.org/AEP/ with its access date, and cite the papers above directly for the science. For the Pioreactor platform, see [pioreactor.com](https://pioreactor.com).

## Contribute data

Results from other labs make the design better for everyone.

- **Share results and questions** on the [AMYBO forum](https://forum.amybo.org), or email [hello@amybo.org](mailto:hello@amybo.org).
- **Add a write-up to the repository** by pull request, alongside the existing ones: results under [AsepticElectroPioreactor/CARMA_PumpPriming/Results/](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/) or a new folder, methods under [Methodologies/](repo:Methodologies/). Say which model you built (for example AEP0.2), its settings, the medium and the organism.
- **Add a medium** by typing a new column on the Media sheet of the gas model workbook, [Media/electroPioreactorGasModel.xlsx](repo:Media/electroPioreactorGasModel.xlsx), so its chemistry is calculated beside the others. <!-- source: Media/README.md (Names) -->
- **Suggest a paper** for the bibliography through the forum's [Journal Club](https://forum.amybo.org/c/journal-club).

See [Open source](/open-source/) for how contributions work.
