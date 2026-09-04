# electroPioreactor guides (Docs&I source)

This tree is the source for the electroPioreactor build guides published at docs.electroPioreactor.org: `components/` holds one YAML file per part, kit sub-item, printed part and tool (imported from the AEP0.2 [bill of materials](../AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) and the [assembly instructions](../AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/README.md), whose original bodies now live here); `steps/` holds one Markdown file per assembly step, with the parts, tools, renders and safety notes for that step in its frontmatter and the instructions in its body; `media/` holds a manifest per committed video or photo (none yet; [media/README.md](media/README.md) is the shoot list). The guides are declared in [`docsandeye.config.yaml`](../docsandeye.config.yaml) at the repository root: `aep` (the Aseptic ElectroPioreactor, served under `/AEP`) and `mep` (the Mixed ElectroPioreactor, served under `/MEP`, which shares steps marked `guide: [aep, mep]` — see "Steps shared with the MEP guide" below). Printed parts reference their OpenSCAD masters under [`Components/`](../Components); the "why this part" notes for the CO₂ train are in [`Components/CO2 transfer/`](../Components/CO2%20transfer).

To build: run `docsandeye check` from the repository root to validate the schemas and cross-references (every part names an existing component, every printed part has a source file, every media manifest pins real component versions); run `docsandeye render` to produce the render plan and, on a machine with OpenSCAD, the component renders and viewer models; then run the Astro/Starlight build to publish the site. Renders are not committed here — they are regenerated from the `.scad` sources whenever a component's `design_version` changes.

## Steps

One file per assembly step, `steps/step-NN-<slug>.md`, where `NN` is the step's `order` and the title is the heading of the corresponding numbered step in the AEP0.2 assembly instructions (Method steps 1 to 11); `steps/step-00-before-you-start.md` carries the "What changed from AEP0.1.1", "Before you start", tools and spares sections. Bodies keep the instructions' wording; frontmatter lists the parts, tools, renders, viewer and safety notes. (This section lives here rather than in `steps/README.md` because the loader treats every `*.md` under `steps/` as a step.)

### Steps shared with the MEP guide

A step is marked `guide: [aep, mep]` only where `MixedElectroPioreactor/Assembly-EdMSc26.md` performs the same operation. The `mep` guide has no step files of its own yet.

- `step-01-connect-dovetail-platforms` — shared. Evidence: Assembly-EdMSc26.md lines 16–17 ("Place the dovetail raft on the bench with dovetails to front and left" and the raft layout: SodaStream at the rear, product container to the left of the media container, peristaltic pumps in front, electroPioreactor at the very front) match AEP Assembly/README.md lines 45–50.

Considered and not shared this cycle (same purpose, different hardware or only a sub-step):

- `step-05-set-up-electrolysis` — Assembly-EdMSc26.md lines 23–25 (add bicarbonate, screw the cap fully, seat the vial) and 40–55 (electrode installation, red to anode, black to cathode, polarity) cover the same purpose as AEP README lines 78–92, but with the AEP0.1-generation cap, o-rings and top stop; the AEP0.2 text would misdirect an MEP builder.
- `step-06-set-up-nutrient-solution-flow` — Assembly-EdMSc26.md line 18 (12 V PSU to the HAT barrel jack) matches only sub-step 6.2 (README line 95); lines 27–28 are a PWM channel note, not the pump setup.
- Steps 2, 3, 4, 7, 8, 9, 10 and 11 — no equivalent operation in Assembly-EdMSc26.md (its CO₂ stack arrives pre-built, line 3).
