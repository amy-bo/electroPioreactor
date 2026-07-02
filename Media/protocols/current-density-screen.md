---
state: authored
author: [claude-opus-4.8]
checked: []
reviewed: []
authorised:
source_type: external
description: "Current-density screen: find a strain's optimal & tolerated electrolysis current density when no literature value exists"
sources:
  - https://www.sciencedirect.com/science/article/abs/pii/S0959652620316437
  - https://www.researchgate.net/publication/359193104_Electro-cultivation_of_hydrogen-oxidizing_bacteria_to_accumulate_ammonium_and_carbon_dioxide_into_protein-rich_biomass
  - https://www.sciencedirect.com/science/article/pii/S2405844018368130
  - https://mdpi.com/1996-1073/12/10/1904/htm
created: 2026-07-01
recorded_at: 2026-07-01
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, electrochemistry, current-density, strain, calibration]
---

# Current-density screen (optimal & tolerated j for a new strain)

**Feeds:** the strain lookup table on the Electrochemistry sheet (`j_opt_strain`, `j_ceiling_strain`) that the current-density traffic light reads. Use this when a strain has no published in-culture current-density value.

**Why it matters:** in an undivided in-culture cell the current density is not a free knob — it simultaneously sets the H₂/O₂ substrate supply *and* the oxidative/pH stress on the cells. The optimum is the balance point between those two, and it is strain-specific. The model's traffic light is only as good as the `j_opt`/`j_ceiling` pair fed into it; for an uncharacterised strain those must be measured, not guessed.

## Principle

Current density j = I / A_wetted (mA/cm²), where I is the electrolysis current (Gerrit's Law, [gerrit-current.md](gerrit-current.md)) and A_wetted is the submerged electrode area (shape-aware — see the wetted-area block on the Electrochemistry sheet; a rod counts its end face, a tube does not). Raising j does two opposing things at once:

1. **Helps:** more current → more dissolved H₂ (and O₂) per Faraday's law → more substrate for the hydrogen-oxidiser, up to the point where mass transfer or the organism's uptake saturates.
2. **Hurts:** more current → more anodic oxidant (O₂, and any free chlorine if chloride is present), a larger local pH excursion at both electrodes, and more Joule heat — all of which impair or kill cells, first in the electrode boundary layer and then in the bulk.

So a growth-rate-versus-j curve rises, peaks at the **optimum j**, then falls. The **tolerated ceiling** is the highest j at which viability is not measurably worse than a current-free (or decoupled-gas) control. The single hardest part of the measurement is separating the "helps" axis from the "hurts" axis, because a naïve single-arm screen conflates substrate limitation at low j with toxicity at high j. The decoupled control arm below is what breaks that degeneracy.

## Optimal protocol (best accuracy)

Kit: ≥ 4 electroPioreactor units (more is better — this is a dose-response curve), a way to log OD/growth rate (the onboard OD reader, blanked per [Calibration](../../MixedElectroPioreactor/Calibration.md)), a viability assay (plate counts or a live/dead stain), a calibrated in-line current measurement (per [gerrit-current.md](gerrit-current.md) so j is known, not assumed), pH and DO probes, and — for the decoupled control — a way to deliver H₂/O₂/CO₂ by sparging without electrolysis (gas cylinders or a separate external electrolyser).

Fix everything except current. Same medium, temperature, stir speed, sparge schedule, inoculum, and the **same electrode set** (so A_wetted, and therefore the j-per-mA, is constant and known from the model).

1. **Choose the j series from the model, not from intensity %.** Read A_wetted for the installed electrode from the Electrochemistry sheet, then pick target current densities spanning sub-optimal to clearly-toxic — e.g. 0.5, 1, 2, 3, 5, 7.5, 10, 15 mA/cm². Back-calculate the LED intensity for each from Gerrit's Law (I = slope·intensity + intercept, then intensity = (j·A_wetted·... )). Discard any target that needs an intensity outside the validated 3–25 % band, or note it as extrapolated.
2. **Run the electrolysis arm.** One unit (or replicate group) per j. Inoculate identically. Log growth continuously; sample for viability at fixed timepoints. Record pH, DO, and temperature at each j throughout — these are the mechanism read-outs.
3. **Run the decoupled control arm (the key control).** In parallel, grow the strain with H₂/O₂/CO₂ delivered by external sparging at a gas rate matched to the mid-series electrolytic gas production, but with **no in-culture current** (or the lowest j that still drives the sparger). This arm shows what growth looks like when substrate is present but electrode stress is absent. Any shortfall of an electrolysis arm below this control at matched substrate delivery is the toxic penalty of that current density.
4. **Replicate and randomise.** At least duplicate each j; randomise unit-to-j assignment across runs to avoid confounding a "hot" unit with a j level. Re-condition/clean electrodes between runs.
5. **Read out three numbers per j:** specific growth rate µ (exponential phase), final biomass / product titre, and relative viability vs the decoupled control.

Interpretation:

- **Optimum j** = the j that maximises volumetric productivity (µ·biomass, or product rate). This is what goes into `j_opt_strain`.
- **Tolerated ceiling j** = the highest j whose viability is statistically indistinguishable from the decoupled control (no die-off penalty). This goes into `j_ceiling_strain`; the traffic light turns amber above optimum and red above ceiling.
- **Onset-of-inhibition j** = first j where µ or viability drops below the control by more than the assay noise. Record it in the source column even if it equals the ceiling.

## Budget protocol (minimal kit)

Kit: 2–3 units, the onboard OD reader only, pH strips/probe, no separate viability assay, no decoupled arm.

1. Pick a coarser j series (e.g. 1, 3, 7.5, 15 mA/cm²) from the model's A_wetted as above.
2. Run each to a growth curve; take µ and final OD.
3. Without the decoupled control you cannot cleanly separate substrate limitation from toxicity, so treat the result as **provisional**: the optimum is the peak of the OD-vs-j curve, and the ceiling is one step below the first j where final OD or µ falls *and* pH/appearance shows electrode stress (bleaching, clearing, pellet loss). Mark the entered values `(provisional, no decoupled control)` in the strain table source column and flag the confidence LOW.

Accuracy note: the boundary-layer stress is worst right at the electrode, so a strain can look healthy in bulk OD while the near-anode population is being killed and diluted back. The optimal protocol's viability assay and decoupled control catch this; the budget route does not. Do not promote a budget number to `confidence: high`.

## Result -> model

Per strain, add or edit its row in the strain lookup table on the Electrochemistry sheet:

- `j_opt` (mA/cm²): the productivity-maximising current density.
- `j_ceiling` (mA/cm²): the highest non-inhibitory current density (vs the decoupled control).
- Source/date column: "in-house screen, <date>, <optimal|budget>, n=<replicates>"; note the electrode set and area basis used, since j depends on which A_wetted was assumed.
- Set the confidence marker so the traffic light's own note can caveat a LOW-confidence strain.

Then select that strain in the Summary dropdown; the current-density flag will compare the operating j against these two numbers and, separately, against the electrode material's rated limit (see the material-limit block — the biological ceiling and the plating limit are independent checks and the reported flag is the worse of the two).

## Acceptance checks & pitfalls

- **Substrate/toxicity confound:** a monotonically rising OD-vs-j with no peak usually means you never reached the toxic regime — extend the series upward. A monotonically falling one means even your lowest j is already inhibitory — extend downward. A real optimum has a peak.
- **Area basis must match the model:** j is meaningless without its area. Use the model's shape-aware A_wetted (rod vs tube differ by the end face) and record which electrode was fitted. Re-deriving j against a different area later will move the thresholds.
- **Chloride confound:** if the medium carries chloride, part of the "toxicity" is free chlorine, not current per se (see [the chlorine block]); a chloride-free medium isolates the pure current-density effect. Report the medium's chloride with the result.
- **Electrode conditioning drift:** current at a fixed intensity drifts in the first minutes (bubble coverage, oxide growth). Follow the gerrit-current.md settling period so the j you assign is the j the cells actually saw.
- **Don't extrapolate past the validated Gerrit band:** j targets that need intensity > 25 % may not deliver the assumed current as cell voltage nears the rail; verify with the in-line current measurement rather than trusting the setpoint.
- **One strain's number is not another's:** HOB tolerances span at least an order of magnitude across the literature. Do not reuse a `j_opt` across strains; the whole point of the screen is that it is strain-specific.

## Sources

- [Rosa/Kracke — Power to hydrogen-oxidizing bacteria: effect of current density on bacterial activity and community spectra (J Cleaner Prod 2020)](https://www.sciencedirect.com/science/article/abs/pii/S0959652620316437)
- [Electro-cultivation of hydrogen-oxidizing bacteria to accumulate ammonium and CO₂ into protein-rich biomass](https://www.researchgate.net/publication/359193104_Electro-cultivation_of_hydrogen-oxidizing_bacteria_to_accumulate_ammonium_and_carbon_dioxide_into_protein-rich_biomass)
- [Givirovskiy — Electrode material studies, in-situ water electrolysis in pH-neutral electrolyte (Heliyon 2019)](https://www.sciencedirect.com/science/article/pii/S2405844018368130)
- [Givirovskiy — In-situ water electrolyzer stack for an electrobioreactor (Energies 2019)](https://mdpi.com/1996-1073/12/10/1904/htm)
</content>
</invoke>
