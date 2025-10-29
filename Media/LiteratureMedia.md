# Literature on Media for HOB fermentation with in-culture electrolysis

## Literature found

The following papers have been [found](../Literature/README.md) which give media compositions for fermentation of hydrogen oxidising bacteria (HOB) using in-culture electrolysis.  We are not considering fermentation where H₂ is supplied from a source external to the culture, as we believe the impact of ionic strength on electrolysis is significant and that chlorides will also adversely impact HOB (through biocidal hypochlorous acid formation) and electrode impacts.  We have likewise excluded formulations for Photoelectroautotrophic growth and Microbial Electrochemical Recovery Cells.

### Original formulations

1. [Liu et al. (2016)](https://doi.org/10.1126/science.aaf5039) detailed Minimal Medium (36 mM phosphate buffer) and high salt version (108 mM) for R. eutropha.
2. [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) focused on the design and characterization of a new minimal medium to enable fast electroautotrophic growth of Cupriavidus necator in microbial electrosynthesis, reporting essentially zero lag phase, a high specific growth rate (~0.09 h⁻¹) and no observable electrode fouling under in‑culture electrolysis.
3. [Al Rowaihi et al. (2018)](https://doi.org/10.1371/journal.pone.0196079) customised nitrogen- and trace metal‑deprivation media specifically to drive PHB accumulation under stress rather than maximise growth.
4. [Feng et al. (2023)](https://doi.org/10.3389/fmicb.2023.1254451) developed specialized high-ionic-strength medium (180 mM phosphate buffer) to enrich halotolerant HOB strains.

### Modifications to [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252)

1. [Stöckl et al. (2020)](https://doi.org/10.1002/cssc.202001235) increased buffer capacity to manage pH during formate utilization.
2. [Dinges et al. (2024)](https://doi.org/10.1002/cssc.202301721) varied K⁺ and Na⁺ ratios (0.2 M phosphate buffer) for improved coupled electro-formate/polyhydroxybutyrate (PHB) synthesis.
3. [Langsdorf et al. (2024)](https://doi.org/10.1016/j.jcou.2024.102800) detailed the minimal medium composition used for direct electroautotrophic PHB production using flue gas.

### Modifications to [Matassa et al. (2016)](https://doi.org/10.1111/1751-7915.12369)

1. Pous et al. ([2022](http://doi.org/10.1016/j.biteb.2022.101010) and [2023](http://doi.org/10.1016/j.jece.2023.111550)) reduced ammonium content but included chloride salt inclusion (CaCl₂).

### Modifications to [Leibniz-Institut DSMZ growth medium number 81](https://www.dsmz.de/microorganisms/medium/pdf/DSMZ_Medium81.pdf)

1. [Givirovskiy et al. (2019)](https://doi.org/10.3390/en12101904) and [Ruuskanen et al. (2021)](https://doi.org/10.1016/j.jclepro.2020.123423) replaced major chloride compounds with sulfates; reduced ferric ammonium citrate; and added Na₂SO₄ to increase conductivity for hybrid biological-inorganic system scale-up.
2. [Nyyssölä et al. (2021)](https://doi.org/10.1021/acsfoodscitech.0c00129) replaced chlorides with sulfates, and included a wide array of vitamins for Gram-positive HOB.

### Patents

1. [Reed et al. (2015)](https://worldwide.espacenet.com/publicationDetails/biblio?FT=D&date=20150721&DB=&locale=&CC=US&NR=9085785B2&KC=B2&ND=1).

## Selection of base formulation

Of the above [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252), most of the papers modifying their formulation and [Al Rowaihi et al. (2018)](https://doi.org/10.1371/journal.pone.0196079) are explicitly chloride free.  Of these Al Rowaihi needed to maximize cellular stress as their main aim was PHB production, whereas Sydow, et al. aimed for rapid growth, requiring optimization for biological vitality.  Sydow et al's aims are therefore aligned with ours.

## Motivation for modification

### Shelf life

Prof. Dirk Holtmann was the corresponding author of [Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252). Personal communication with researchers in his current lab, who use the same formulation, indicated that the solution starts off blue then turns yellow within a couple of days, and starts to precipitate within a couple of weeks or months.  While it is beneficial for the Holtmann lab to maintain consistency between their experiments.  We require media with longer shelf life.

### Omitted Components

[Sydow et al. (2017)](https://doi.org/10.1002/elsc.201600252) and papers based on their formulation omitted the following:

#### Boron

The vast majority of other formulations included boric acid (H₃BO₃).

#### Vanadium

Some DSMZ papers included Sodium Metavanadate (NaVO₃) or Ammonium metavanadate (NH₄VO₃).

#### Chelating agents

In order to make the medium free of carbon sources, chelating agents (which likely prevented precipitation hence lengthening shelf life) were omitted by [Sydow et al.](https://doi.org/10.1002/elsc.201600252).

#### Chlorides

[Sydow et al.](https://doi.org/10.1002/elsc.201600252) sought to be chloride-free, only using HCl to acidify the trace mineral solution.  Nobody at the Holtmann lab was able to explain why they didn't use H₂SO₄ in order to go completely chloride-free.

#### Vitamins and Organic Cofactors

Some media, particularly those designed for specific strains or based on comprehensive formulations like DSMZ-81, include various vitamins, which are generally omitted from the basic minimal media optimized for electroautotrophic C. necator growth by [Sydow et al](https://doi.org/10.1002/elsc.201600252):
• Vitamins: The modified DSMZ81 mineral medium used by [Nyyssölä et al. (2021)](https://doi.org/10.1021/acsfoodscitech.0c00129) and the medium used by [Yang et al. (2021)]() explicitly included a comprehensive vitamin solution. This typically included riboflavin, thiamine-HCl, nicotinic acid, pyridoxine-HCl, Ca-pantothenate, biotin, and vitamin B12. 

[Nyyssölä et al.](https://doi.org/10.1021/acsfoodscitech.0c00129) noted that both strains they tested could also grow in the absence of these vitamins.