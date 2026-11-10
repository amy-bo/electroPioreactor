# Aseptic electroPioreactor (AEP)

The **Aseptic electroPioreactor (AEP)** is a variant of the [electroPioreactor](../) developed for reproducible monoculture research on Hydrogen Oxidising Bacteria (HOB). It is based on the [Pioreactor](https://pioreactor.com), adapted to add in-culture electrolysis and CO₂ sparging; the "Aseptic" variant adds the gas-line filtration, sealing and autoclave-ability needed to keep a monoculture free of contamination.

In-culture electrolysis generates H₂ (at the cathode) and O₂ (at the anode) *in situ* from the medium, so HOB can fix CO₂ autotrophically without the hazards of sparged hydrogen.

## Why an AEP?

- **Safe** – hydrogen and oxygen are produced only as needed, dissolved in the medium, rather than stored.
- **Aseptic** – luer-lock 0.2 μm vent filters on entry/exhaust ports and a sealed vial cap allow defined monoculture work.
- **Affordable** – built on the low-cost open Pioreactor platform, supplied in the UK by [LabCrafter](https://labcrafter.co.uk) and in the rest of the world by [Pioreactor](https://pioreactor.com).
- **Automated** – turbidostat dosing, peristaltic media/product handling, and relay-driven intermittent CO₂ sparging all run from the Pioreactor UI using the [electroPioreactor plugin](../AEP-Plugin).
- **Open & reproducible** – parametric designs, BoM and assembly procedures are version-controlled here.

Design criteria, applied in order: 
1. Safe
2. Accurate & repeatable
3. Automated
4. Good value

## Origins

The electroPioreactor was created by [AMYBO](https://amybo.org) to facilitate affordable, safe, local production of HOB as a sustainable alternative protein.

The **Aseptic** variant focuses that platform on monoculture research. The current AEP0.1 line was assembled and trained on by Imperial and Edinburgh students in November 2025 (see [AEP0.1 Training](CARMA_PumpPriming/Results/AEP0.1%20Training/README.md)).

## CARMA Hub Pump Priming

This work is funded under [**CARMA Hub Pump Priming**](https://carmahub.co.uk/about-us/pump-priming-projects/#:~:text=Affordable%20Aseptic%20Electro-Bioreactor%20for%20Reproducible%20Hydrogen%20Oxidising%20Bacteria%20(HOB)%20Research) ("Affordable Aseptic Electro-Bioreactor for Reproducible HOB Research"), led by:

- [Dr Sonja Billerbeck](https://profiles.imperial.ac.uk/s.billerbeck) – PI, Imperial College London (Bezos Centre for Alternative Proteins)
- [Prof. Chris French](https://biology.ed.ac.uk/chris-french-laboratory) – PI/collaborator, University of Edinburgh

with [AMYBO](https://amybo.org) as design and training subcontractor/collaborator and [LabCrafter](https://labcrafter.co.uk) as named vendor.

## Directory

- 🗂 [**CARMA_PumpPriming/**](CARMA_PumpPriming) — AEP work under CARMA Hub Pump Priming
  - [Meetings.md](CARMA_PumpPriming/Meetings.md) — meeting notes
  - 🗂 [**Assembly/**](CARMA_PumpPriming/Assembly) — build procedures
    - [README.md](CARMA_PumpPriming/Assembly/README.md) — **latest** assembly instructions (AEP0.2)
    - [BoM.md](CARMA_PumpPriming/Assembly/BoM.md) — AEP0.2 bill of materials
    - [AEP0.1.1_Assembly.md](CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md) — archived AEP0.1.1 instructions
    - 🗂 [**Superseded/**](CARMA_PumpPriming/Assembly/Superseded) — earlier assembly docs
      - [AEP0.1_Assembly.md](CARMA_PumpPriming/Assembly/Superseded/AEP0.1_Assembly.md)
      - [AEP0.1 Assembly.opml](CARMA_PumpPriming/Assembly/Superseded/AEP0.1%20Assembly.opml)
  - 🗂 [**Results/**](CARMA_PumpPriming/Results) — experimental results
    - 🗂 [**AEP0.1 Training/**](CARMA_PumpPriming/Results/AEP0.1%20Training) — Nov 2025 joint training (Imperial + Edinburgh)
      - [README.md](CARMA_PumpPriming/Results/AEP0.1%20Training/README.md) — training write-up
      - [Training Notes (Biological and experimental notes - Amir).docx](CARMA_PumpPriming/Results/AEP0.1%20Training/Training%20Notes%20%28Biological%20and%20experimental%20notes%20-%20Amir%29.docx)
      - [AnodeDiscolouration.jpg](CARMA_PumpPriming/Results/AEP0.1%20Training/AnodeDiscolouration.jpg)
    - 🗂 [**Anode discolouration/**](CARMA_PumpPriming/Results/Anode%20discolouration) — anode discolouration images
    - 🗂 [**Gas sparging/**](CARMA_PumpPriming/Results/Gas%20sparging) — CO₂ sparging investigation
      - [Continuous or Intermittent CO2 sparging.md](CARMA_PumpPriming/Results/Gas%20sparging/Continuous%20or%20Intermittent%20CO2%20sparging.md)
      - [EXAPURE_Filters_2009.pdf](CARMA_PumpPriming/Results/Gas%20sparging/EXAPURE_Filters_2009.pdf)
      - [Measuring cylinder recently full of CO2 IMG_8702.DNG](CARMA_PumpPriming/Results/Gas%20sparging/Measuring%20cylinder%20recently%20full%20of%20CO2%20IMG_8702.DNG)

---
<sub>O4.7: this README was drafted by Claude (Opus 4.7) from repo contents & reviewed by Martin Currie.</sub>
