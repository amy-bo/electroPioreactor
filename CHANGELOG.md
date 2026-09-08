# Changelog

Done-work log for the electroPioreactor repository, newest first. Open work stays in the "Still to specify" list of the AEP0.2 [BoM](AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/BoM.md) and in the `<!-- TODO -->` comments of the step files under `docs/steps/`.

## 2026-09-08

- [x] **Gerrit's BoM answers propagated to the Docs&I guide** — `05ef02f` (Gerrit, 2026-09-04) answered the blocking "For Gerrit" list in BoM.md after the docs tree had already been imported from the older BoM. Rebased AEP02 onto it and carried the answers into `docs/components/` (mmo-anode 70 mm active length / 8 µm coating on grade 1 Ti; vial-cap print settings; silicone-septum 60 Shore laser-cut; crimp-connector and crimp-housing TE AMP part numbers; reducing-nipple BSP stainless; anode-feed-tube 100 mm; pumping-dovetail-platform printed from Printables 679663) with a changelog entry and patch version bump each, fixed the feed-tube length in step 08, and reduced the BoM's open list to what is still unanswered (electrode insertion depth, septum cut outline, crimp contact and tool).
- [x] **Ignore docsandeye `build/`** — render output is regenerated from the `.scad` sources and not committed.
