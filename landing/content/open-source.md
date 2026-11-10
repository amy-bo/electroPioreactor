---
title: Open source
description: What is in the electroPioreactor repository, where to find it on GitHub and Radicle, its licence, how to contribute, and how the guide is built.
section: about
audience: everyone
order: 20
---
Everything about the electroPioreactor is published in one public repository: the 3D designs, parts lists, build guide source, software plugin, culture media, gas model and research write-ups. You can read it, copy it and suggest changes.

## Where it lives

The repository is synchronised in two places: <!-- source: README.md (GitHub & Radicle) -->

- **GitHub:** [github.com/amy-bo/electroPioreactor](https://github.com/amy-bo/electroPioreactor)
- **Radicle:** [rad:zY4GuyErQo91xGYdLi4r2bea9QDJ](https://app.radicle.xyz/nodes/iris.radicle.xyz/rad%3AzY4GuyErQo91xGYdLi4r2bea9QDJ). [Radicle](https://radicle.xyz/) is a peer-to-peer code network that does not depend on one company's servers; the project encourages you to try it.

## Repository map

| Folder | What is in it |
|---|---|
| [AsepticElectroPioreactor/](repo:AsepticElectroPioreactor/) | The Aseptic electroPioreactor (AEP): CARMA Hub Pump Priming work, open bill of materials (BoM) items, archived AEP0.1 and AEP0.1.1 assembly instructions, meeting index and results, including the AEP0.1 training write-up |
| [MixedElectroPioreactor/](repo:MixedElectroPioreactor/) | The Mixed-culture electroPioreactor (MEP): assembly, calibration, operation and pre-transport checks |
| [Components/](repo:Components/) | Parametric OpenSCAD designs and STL files for the printed parts (Vial Cap, ElectrodeTopStop, GL45 bottle holder, PinchSlider), notes on the CO₂ gas train, and the original MEP parts list |
| [AEP-Plugin/](repo:AEP-Plugin/) | The electroPioreactor Pioreactor plugin (Python), its tests and install scripts, including the offline install from the microSD card |
| [card-bundle/](repo:card-bundle/) | The script that builds the AEP and MEP card bundles: files copied onto a freshly flashed Pioreactor card so it boots with the right plugins |
| [Media/](repo:Media/) | Culture media formulations and the electroPioreactor gas model (Python and Excel), with its checks and calibration protocols |
| [Literature/](repo:Literature/) | The bibliography on hydrogen-oxidising bacteria (HOB) fermentation by in-culture electrolysis (BibTeX and JSON) |
| [Methodologies/](repo:Methodologies/) | Enrichment protocols for HOB from environmental samples |
| [PastResearch/](repo:PastResearch/) | Outputs of past student projects: Harvey Mudd College (anode and valve) and Brown University's Harris Lab (CO₂ backflow) |
| [docs/](repo:docs/) | Source of the build guides: one YAML file per part in `components/`, one Markdown file per step in `steps/`, video and photo manifests in `media/`, and the glossary |
| [site/](repo:site/) | The Astro Starlight site that builds [docs.electropioreactor.org](https://docs.electropioreactor.org) from `docs/` |
| [landing/](repo:landing/) | The generator for this site, electropioreactor.org |
| [CHANGELOG.md](repo:CHANGELOG.md) | Done-work log, newest first |

<!-- source: top-level folders on branch AEP02; docs/README.md; card-bundle/make-card-bundles.sh -->
<!-- CHECK: docs/, site/, landing/, CHANGELOG.md and docsandeye.config.yaml exist on branch AEP02 but not yet on main; repo: links to them only resolve once AEP02 is merged into main (or if the generator points repo: links at AEP02) -->

Where to start: builders go to the [build guide](https://docs.electropioreactor.org/AEP/); people adapting the hardware go to [Components/](repo:Components/) and [Specifications](/specifications/); software users go to [AEP-Plugin/README.md](repo:AEP-Plugin/README.md) and [Software](/software/); researchers go to [Research](/research/).

## Licence

The licence position is not yet complete, so check before you reuse anything:

- **The electroPioreactor plugin** ([AEP-Plugin/](repo:AEP-Plugin/)) is released under the **MIT License**, "Copyright (c) 2026 Martin Currie / Amybo". The full text is in [AEP-Plugin/LICENSE.txt](repo:AEP-Plugin/LICENSE.txt). <!-- source: AEP-Plugin/LICENSE.txt; AEP-Plugin/setup.py (license="MIT") -->
- **Everything else** in the repository (hardware designs, parts lists, guides, media, data and write-ups) has no licence file yet. Until one is published, ask before reusing it: email [hello@amybo.org](mailto:hello@amybo.org) or ask on the [forum](https://forum.amybo.org).

<!-- CHECK: a repository-wide LICENSE (CC BY-SA 4.0 for 3D models and images, CERN-OHL-S-2.0 for other hardware, AGPL-3.0-or-later for software, CC BY 4.0 for text and data) is drafted in brain2 (AMYBO/electroPioreactor-LICENSE-draft.md, state authored) but not in the repo; update this section when it lands -->

Third-party designs keep their own licences: the [Pioreactor](https://pioreactor.com) hardware and software, and community models such as those on Printables, are licensed by their authors.

## Contributing

Contributions of every size help: a corrected step, a photograph, a better part, a new medium or a set of results.

- **Discuss first** on the [AMYBO forum](https://forum.amybo.org), where design questions such as the [CO₂ backflow problem](https://forum.amybo.org/t/co2-sparger-drawback/52) have been worked through in public.
- **Report a problem** with the guide, a design or the plugin by opening an [issue on GitHub](https://github.com/amy-bo/electroPioreactor/issues).
- **Propose a change** with a pull request on GitHub, or a patch on Radicle. Small, focused changes are easiest to review. Log what you changed in [CHANGELOG.md](repo:CHANGELOG.md).
- **Share data**: see [Contribute data](/research/#contribute-data).
- **Email** [hello@amybo.org](mailto:hello@amybo.org) if none of these suits you.

Open design questions are kept in the "Still to specify" list of the AEP0.2 [BoM.md](repo:AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) and in `<!-- TODO -->` comments in the step files under `docs/steps/`. These are good places to help. <!-- source: CHANGELOG.md (header) -->

## How the build guide is made

The guides at [docs.electropioreactor.org](https://docs.electropioreactor.org) are generated from the repository, so the guide and the designs cannot drift apart unnoticed. <!-- source: docs/README.md; docsandeye.config.yaml; CHANGELOG.md 2026-09-29 -->

1. **Parts** are one YAML file each in [docs/components/](repo:docs/components/), with their specification, supplier, source design file and a changelog with a version number.
2. **Steps** are one Markdown file each in [docs/steps/](repo:docs/steps/), listing their parts, tools, safety notes and checks, with the instructions in the body. Steps shared by the AEP, MEP and BAEP guides are written once.
3. **Guides** (AEP, MEP and BAEP), the questions the guide asks you, and the parts checklist are declared in [docsandeye.config.yaml](repo:docsandeye.config.yaml).
4. **Docs&I** (`docsandeye`) checks it all: every part a step names must exist, every printed part must have a source file, and every video or photo must name the part versions it shows, so it can be flagged out of date when a part changes. It also renders the printed parts from their OpenSCAD sources.
5. **Astro Starlight** in [site/](repo:site/) builds the website, which is published on Cloudflare Pages.

To change the guide, edit the files in `docs/` and open a pull request; you do not need to touch the website code.
