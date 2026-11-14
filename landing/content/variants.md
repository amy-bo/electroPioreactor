---
title: Which electroPioreactor?
description: The Aseptic (AEP), Mixed-culture (MEP) and Budget aseptic (BAEP) electroPioreactors compared, with their build guides and version history.
section: build
audience: everyone
order: 5
---
There are three electroPioreactors. The Aseptic electroPioreactor (AEP) is for growing a single strain without contamination. The Mixed-culture electroPioreactor (MEP) is a lower-cost unit for mixed cultures, and the Budget aseptic electroPioreactor (BAEP) is an MEP with filters on every gas path. All three are a [Pioreactor](https://pioreactor.com) bioreactor with electrodes and CO₂ sparging added.

## Pick one

| If you want to... | Build | Guide |
|---|---|---|
| Grow one known strain of hydrogen-oxidising bacteria (HOB), with no other microbes getting in | **AEP0.2** | [docs.electropioreactor.org/AEP/](https://docs.electropioreactor.org/AEP/) |
| Grow a mixed culture, such as an enrichment from soil or water, at lower cost | **MEP** | [docs.electropioreactor.org/MEP/](https://docs.electropioreactor.org/MEP/) |
| Keep a culture aseptic on a smaller budget | **BAEP** | [docs.electropioreactor.org/BAEP/](https://docs.electropioreactor.org/BAEP/) |

"Aseptic" means the culture is kept free of microbes you did not put there. <!-- source: AsepticElectroPioreactor/README.md -->

If you have a unit that is none of these, follow the AEP guide: its parts count shows what a standard build has. <!-- source: site/src/content/docs/index.mdx -->

## The Aseptic electroPioreactor (AEP)

The AEP was developed for reproducible research on single strains (monocultures) of HOB, under the CARMA Hub Pump Priming project with Imperial College London and the University of Edinburgh (see [About](/about/)). It adds what a monoculture needs: 0.2 µm vent filters on every gas and bottle vent, a sealed vial cap with a silicone septum, and parts that can be autoclaved. <!-- source: AsepticElectroPioreactor/README.md -->

The current model is **AEP0.2** (2026). It is built on the Pioreactor 40 ml v1.5 with the XR upgrade kit, and an AEP0.2 kit also includes the Precision Temperature Upgrade Kit. <!-- source: docs/steps/step-00-before-you-start.md; docsandeye.config.yaml -->

- More: [the AEP page](/aep/), with the story of its first runs
- Guide: [AEP guide](https://docs.electropioreactor.org/AEP/), starting at [Before you start](https://docs.electropioreactor.org/AEP/step-00-before-you-start/)
- Running it: [AEP protocol](https://docs.electropioreactor.org/AEP/protocol/) (being written up)
- Source: [AsepticElectroPioreactor/](repo:AsepticElectroPioreactor/)

## The Mixed-culture electroPioreactor (MEP)

The MEP was the only electroPioreactor until work began on the AEP. Work on it has resumed as a lower-cost version for mixed cultures, starting with two units for the 2026 MSc Industrial Projects of the School of Biological Sciences at the University of Edinburgh. <!-- source: MixedElectroPioreactor/README.md -->

It uses the smaller Pioreactor 20 ml v1.1, platinum-plated titanium anodes and an O-ring vial cap with tubes through its ports instead of needles through a septum. It leaves out the AEP-only steps: sterilisation, the temperature kit and the XR optics. <!-- source: docs/README.md (MEP and BAEP steps) -->

- More: [the MEP page](/mep/), on enrichment and the Edinburgh MSc units
- Guide: [MEP guide](https://docs.electropioreactor.org/MEP/)
- Running it: [MEP protocol](https://docs.electropioreactor.org/MEP/protocol/) (calibration and operation)
- Source: [MixedElectroPioreactor/](repo:MixedElectroPioreactor/)

## The Budget aseptic electroPioreactor (BAEP)

The BAEP is an MEP with five 25 mm, 0.2 µm hydrophobic vent filters, the same filters the AEP0.2 uses: one on each bottle cap vent, one on the CO₂ inlet and one on each of the two gas outlets. Its guide is the MEP guide plus one extra step, [Add the vent filters](https://docs.electropioreactor.org/BAEP/step-12-add-vent-filters/), after the CO₂ is admitted. It runs exactly as an MEP. <!-- source: docs/steps/step-12-add-vent-filters.md; site/src/content/docs/baep-protocol.md -->

- Guide: [BAEP guide](https://docs.electropioreactor.org/BAEP/)
- Running it: [BAEP protocol](https://docs.electropioreactor.org/BAEP/protocol/)

> **Note:** The BAEP filters the gas paths but keeps the MEP's O-ring cap and tube ports. It has no sterilisation step in its guide. Whether it is aseptic enough for your work is for you and your supervisor to judge.

## Side by side

<!-- source: docs/steps/step-00-mep-before-you-start.md ("How the MEP differs from the AEP0.2"); docs/steps/step-12-add-vent-filters.md -->

| | AEP0.2 | MEP | BAEP |
|---|---|---|---|
| Culture | Single strain, aseptic | Mixed culture | Mixed culture or aseptic on a budget |
| Pioreactor | 40 ml v1.5 + XR upgrade kit | 20 ml v1.1 | 20 ml v1.1 |
| Working volume | About 30 ml | 14 ml, set by the waste line | 14 ml |
| Computer | Raspberry Pi 5 1GB, 27 W USB-C supply | Raspberry Pi Zero 2 W (or 4B), its own 5 V supply | As MEP |
| Vial cap | One-piece printed cap and electrode holder, single silicone septum | O-ring vial cap + ElectrodeTopStop, cap O-ring + 2 electrode O-rings | As MEP |
| Anode | Mixed metal oxide (MMO) tube, 100 mm, CO₂ delivered through its open base | Platinum-plated titanium, 60 mm | As MEP |
| Cathode | Stainless steel, 100 mm | Stainless steel, 60 mm | As MEP |
| Ports | 16 G stainless steel needles through the septum | Tubes through the cap's five 3.2 mm ports | As MEP |
| Vent filters (0.2 µm) | 5 fitted, 1 spare | None | 5 fitted |
| CO₂ regulator | Adjustable, set to about 1 bar | FZone, fixed outlet pressure: the needle valve alone sets the flow | As MEP |
| Pumps | PWM 2 media, PWM 3 waste | PWM 2 waste, PWM 3 media | As MEP |
| Temperature kit | Precision Temperature Upgrade Kit | Not fitted | Not fitted |
| Sterilisation step | Yes (procedure awaiting approval) | No | No |
| Card bundle | AEP bundle: plugin, precision temperature plugin, XR model | MEP bundle: electroPioreactor plugin only | As MEP |

PWM is pulse-width modulation: the Pioreactor's numbered, switched power outputs for pumps and valves. The "card bundle" is a set of files you copy onto the Pioreactor's microSD card so it installs the right software at first boot. <!-- source: card-bundle/make-card-bundles.sh -->

For measured dimensions and part numbers, see [Specifications](/specifications/). For what the electrodes and gas train do, see [How it works](/how-it-works/).

## Version history (AEP)

<!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/ (Superseded/AEP0.1_Assembly.md, AEP0.1.1_Assembly.md), docs/steps/step-00-before-you-start.md, CARMA_PumpPriming/Results/AEP0.1 Training/README.md -->

### AEP0.1 (2025)

The first Aseptic electroPioreactor, on the Pioreactor 20 ml v1.1. A printed vial cap sealed with a cap O-ring and two electrode O-rings, and a separate ElectrodeTopStop held the platinum-plated titanium anode and stainless steel cathode, connected by crocodile clips. CO₂ went through a bubble counter. Three AEP0.1 prototypes were assembled and calibrated by Imperial and Edinburgh students at joint training in Edinburgh in November 2025. <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md -->

- Instructions (archived): [AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/Superseded/AEP0.1_Assembly.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/Superseded/AEP0.1_Assembly.md)
- Training write-up: [AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1%20Training/README.md)

### AEP0.1.1 (2025)

The training turned up problems that fed straight back into the design: <!-- source: AEP0.1 Training/README.md (Other issues, Sparging solution) -->

- The vial cap O-rings tended to fall out, so the cap gained a lip to hold them.
- Crocodile clips on the electrodes came off easily, so the ElectrodeTopStop was improved: the electrode cables now fix with an M3 bolt through a captive nut, with less risk of connecting the electrodes the wrong way round.
- The raft was laid out with the SodaStream cylinder at the back, for a better view of the bottles and shorter pump tubing.
- Continuous CO₂ sparging carried water from the bubble counters into the gas lines and upset the optical readings, so AEP0.1.1 sparges intermittently, switched by a relay on PWM channel 4, with no bubble counter. <!-- source: AEP0.1.1_Assembly.md (pioreactor-relay-plugin, 4=relay) -->
- Vernier callipers joined the tool list to set electrode depth, and the build gained a 12 V supply for the pumps and solenoid. <!-- source: AEP0.1.1_Assembly.md vs Superseded/AEP0.1_Assembly.md -->

Instructions (archived): [AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1.1_Assembly.md). The AEP guide still serves AEP0.1.1 builds: choose "AEP0.1.1 (2025)" when it asks which model you are building. <!-- source: docsandeye.config.yaml (profile model options) -->

### AEP0.2 (2026)

The current model. What changed from AEP0.1.1: <!-- source: docs/steps/step-00-before-you-start.md ("What changed from AEP0.1.1") -->

| Area | AEP0.1.1 | AEP0.2 |
|---|---|---|
| Vessel | Pioreactor 20 ml v1.1, about 15 ml working volume | Pioreactor 40 ml v1.5 + XR upgrade kit, about 30 ml working volume |
| Computer | Raspberry Pi Zero 2 W or Pi 4 4GB | Raspberry Pi 5 1GB, 27 W USB-C supply |
| Vial cap | Separate cap + ElectrodeTopStop, cap O-ring + 2 electrode O-rings | One-piece vial cap and electrode holder, single silicone septum |
| Anode | Platinised titanium rod, 100 mm | MMO (IrO₂-Ta₂O₅) tube, 100 mm, CO₂ delivered through its open base |
| Electrode fixing | M3 bolt through captive nut | Ring terminal + thumb screw, M3 nut and spring washer |
| Ports | Flexelene 135C tubing | Stainless steel needles |
| Gas sealing | PTFE tape on every threaded joint | O-rings where possible, Loctite 577 thread sealant elsewhere |
| CO₂ inlet | Regulator tightened onto the cylinder against escaping gas | Pin-adjustment adapter: tighten first, then open the pin |
| Sparging control | `pioreactor-relay-plugin` + experiment profile | [electroPioreactor plugin](/software/): electrolysis, sparging and OD pausing in one job |
| Dropped | Bubble counter, pinch slider inoculation port, jubilee clips | Inoculation is now by syringe through the septum |

OD is optical density, the Pioreactor's measure of how cloudy, and so how dense, the culture is.

Some AEP0.2 details are still open, including the standard electrode insertion depth, the septum's cut outline and the sterilisation procedure. The list is kept in [AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md). Day-to-day changes are logged in [CHANGELOG.md](repo:CHANGELOG.md).
