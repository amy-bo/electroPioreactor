# Licence

Copyright © 2026 andeye Ltd, trading as AMYBO.

This repository holds several kinds of work — hardware designs, software,
documentation, images and data — and each kind is released under the licence
that suits it. The policy below was published for comment on the AMYBO forum
and adopted without objection:
<https://forum.amybo.org/t/what-license-should-work-done-by-amybo-be-placed-under/47>

## What is licensed how

Unless otherwise specified, AMYBO intellectual property is licensed as follows.

| Kind of work | Licence | Full text |
|---|---|---|
| 3D models, photos, images (including CAD renders), video (outside YouTube) | [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/) | [`LICENCES/CC-BY-SA-4.0.txt`](LICENCES/CC-BY-SA-4.0.txt) |
| Other hardware | [CERN-OHL-S-2.0](https://cern-ohl.web.cern.ch/) | [`LICENCES/CERN-OHL-S-2.0.txt`](LICENCES/CERN-OHL-S-2.0.txt) |
| Pioreactor plugins | [MIT](https://opensource.org/license/mit) | [`LICENCES/MIT.txt`](LICENCES/MIT.txt) |
| Other software | [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html) | [`LICENCES/AGPL-3.0-or-later.txt`](LICENCES/AGPL-3.0-or-later.txt) |
| Text and data | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENCES/CC-BY-4.0.txt`](LICENCES/CC-BY-4.0.txt) |
| Genetic material | To be announced | — |

## Working out which licence applies to a file

In this order:

1. **An `SPDX-License-Identifier:` line in the file wins.** Where a file states
   its own licence, that is the licence for that file.
2. **A `LICENSE` or `LICENCE` file in the same directory wins next,** and covers
   that directory. For example
   [`Components/CentrifugeTubeCoupler/`](Components/CentrifugeTubeCoupler) carries
   the CERN-OHL-S-2.0 text alongside its source, so that the folder stays
   complete if it is copied out on its own.
3. **Otherwise, the table above applies, by the kind of work:**
   - `Components/` — hardware. The design sources (`.scad`), the geometry they
     export (`.stl`, `.3mf`) and physical parts made from them are
     **CERN-OHL-S-2.0**.
   - `AEP-Plugin/`, and any Pioreactor plugin code here — **MIT**.
   - `landing/`, `site/`, and scripts and programs elsewhere (`.mjs`, `.js`,
     `.py`, `.ts`) — **AGPL-3.0-or-later**.
   - `docs/`, `Methodologies/`, `Literature/`, `Media/`, `AsepticElectroPioreactor/`,
     `MixedElectroPioreactor/`, `README.md`, `CHANGELOG.md` and other prose,
     configuration and datasets — **CC-BY-4.0**. (`Media/` here means culture
     media formulation and modelling, not image files.)
   - Photographs, diagrams, CAD renders and video anywhere in the repository —
     **CC-BY-SA-4.0**.

A render is a picture of a design, and the two are licensed differently on
purpose: the image is offered under CC-BY-SA-4.0, while the design it depicts
remains under CERN-OHL-S-2.0. Reusing the image does not grant any licence to
the design.

## More permissive terms

Entities requiring more permissive licensing can obtain it by either:

- entering a contract to pay reasonable royalties to AMYBO, or
- providing AMYBO with regular updates on how people are benefiting from the
  intellectual property, where that IP is used exclusively in
  [Least Developed Countries](https://www.un.org/ohrlls/content/list-ldcs).

Enquiries: <https://forum.amybo.org/>

## What this licence does not cover

- **Third-party contributed work.** `PastResearch/` holds work by others,
  including the Harris Lab at Brown University and a Harvey Mudd College
  Clinic project. Those materials remain the property of their authors and
  their institutions and are included with permission; they are not licensed
  by AMYBO, and this licence grants no rights in them.
- **Vendored and third-party dependencies**, including the packages under
  `site/vendor/` and anything installed from `package.json`. Each keeps the
  licence it was published under.
- **Trademarks and branding.** The AMYBO and andeye names, logos and branding
  are not licensed here. Neither are third-party marks such as Pioreactor,
  Corning, Falcon, Raspberry Pi or SodaStream, which appear only to identify
  the products concerned.
- **No warranty.** Every licence above is offered without warranty of any kind.
  Hardware here involves pressurised gas, electrolysis, hydrogen and biological
  culture. Anyone building or operating it is responsible for their own risk
  assessment.

## Contributing

Contributions are accepted on the basis that they are released under the
licence that applies to the kind of work contributed, as set out above. If you
cannot contribute on those terms, say so in the pull request.
