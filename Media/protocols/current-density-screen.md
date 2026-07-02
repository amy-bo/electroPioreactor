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

## Optimal protocol

Best accuracy. Use this route whenever the strain has no trustworthy published in-culture current-density value and the result will be relied on.

### Kit

- At least 4 electroPioreactor units (more is better – this is a dose-response curve).
- The onboard OD reader for logging growth. Blank the OD reading against a cell-free vial of medium only (or bicarbonate-only) before inoculation.
- A viability assay: plate counts or a live/dead stain.
- A calibrated in-line current measurement (per [gerrit-current.md](gerrit-current.md)) so the current density is known, not assumed.
- pH and dissolved-oxygen (DO) probes.
- A way to deliver H₂/O₂/CO₂ by sparging without electrolysis, for the decoupled control arm: gas cylinders or a separate external electrolyser.

### Reagents

- Culture medium. A chloride-free medium is strongly preferred so the result isolates the pure current-density effect (see Principle & background).
- Inoculum of the strain under test.
- Consumables for the viability assay (plating agar, or the live/dead stain kit).
- H₂/O₂/CO₂ gas supply for the decoupled control arm.

### Method

1. Fix everything except current. Use the same medium, temperature, stir speed, sparge schedule, inoculum, and the same electrode set throughout, so the submerged electrode area – and therefore the current-density-per-unit-intensity – stays constant.
2. Choose the current-density series. The Calibrations tab lists the intensity setpoints to use for your electrode's area; read them off there. Pick a series spanning sub-optimal to clearly toxic, for example 0.5, 1, 2, 3, 5, 7.5, 10 and 15 mA/cm². Skip any setpoint the tab flags as outside the validated intensity band, or record it as extrapolated.
3. Run the electrolysis arm. Assign one unit (or replicate group) per current density. Inoculate every unit identically. Log growth continuously and sample for viability at fixed timepoints. Record pH, DO and temperature at each current density throughout – these are the mechanism read-outs.
4. Run the decoupled control arm (the key control). In parallel, grow the strain with H₂/O₂/CO₂ delivered by external sparging at a gas rate matched to the mid-series electrolytic gas production, but with no in-culture current (or the lowest current density that still drives the sparger). This arm shows what growth looks like when substrate is present but electrode stress is absent.
5. Replicate and randomise. Run at least two units per current density. Randomise the unit-to-current-density assignment across runs so a "hot" unit is not confounded with a current-density level. Re-condition or clean the electrodes between runs.
6. Read out three numbers per current density: specific growth rate µ in exponential phase, final biomass or product titre, and relative viability against the decoupled control.
7. Determine the two reportable numbers. The optimum current density is the one that maximises volumetric productivity (µ × biomass, or product rate). The tolerated ceiling is the highest current density whose viability is statistically indistinguishable from the decoupled control. Also note the onset-of-inhibition current density – the first at which µ or viability drops below the control by more than the assay noise – even if it equals the ceiling.
8. Record the optimum and tolerated-ceiling current densities (mA/cm²) you determined for the strain in the **Current density** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet.

## Budget protocol

Reduced kit. Faster and cheaper, but the result is provisional: without the decoupled control you cannot cleanly separate substrate limitation from toxicity.

### Kit

- 2–3 electroPioreactor units.
- The onboard OD reader only.
- pH strips or a pH probe.
- No separate viability assay and no decoupled control arm.

### Reagents

- Culture medium (chloride-free still preferred).
- Inoculum of the strain under test.
- pH strips if no probe is fitted.

### Method

1. Choose a coarser current-density series, for example 1, 3, 7.5 and 15 mA/cm². The Calibrations tab lists the intensity setpoints to use for your electrode's area; read them off there.
2. Run each current density to a full growth curve. Take µ and final OD.
3. Determine the provisional numbers. The optimum is the peak of the OD-versus-current-density curve. The ceiling is one step below the first current density at which final OD or µ falls and pH or culture appearance shows electrode stress (bleaching, clearing, pellet loss).
4. Record the optimum and tolerated-ceiling current densities (mA/cm²) you determined for the strain in the **Current density** section of the **Calibrations** tab. Fill Researcher, Date and Organism; set Include to y. Leave the Computed and value-in-use cells to the spreadsheet. Because there was no decoupled control, note the values as provisional in the Researcher/Date entry and treat their confidence as low.

Accuracy note: boundary-layer stress is worst right at the electrode, so a strain can look healthy in bulk OD while the near-anode population is being killed and diluted back. The optimal protocol's viability assay and decoupled control catch this; the budget route does not. Do not promote a budget number to high confidence.

## What the spreadsheet does with it

The Current density section of the Calibrations tab averages the included optimum and tolerated-ceiling values for each organism and feeds those averages to the current-density traffic lights on the Summary. The Summary flag compares the operating current density against the biological optimum and ceiling and, separately, against the electrode material's rated plating limit; the biological ceiling and the plating limit are independent checks, and the reported flag is the worse of the two. Setting Include to n on a row keeps it in the record but excludes it from the average.

## Principle & background

This screen feeds the current-density traffic light that reads the per-organism optimum and ceiling. Use it when a strain has no published in-culture current-density value, because the traffic light is only as good as the optimum/ceiling pair fed into it, and for an uncharacterised strain those must be measured, not guessed.

In an undivided in-culture cell the current density is not a free knob – it simultaneously sets the H₂/O₂ substrate supply and the oxidative/pH stress on the cells. The optimum is the balance point between those two, and it is strain-specific.

Current density j = I / A_wetted (mA/cm²), where I is the electrolysis current (Gerrit's Law, [gerrit-current.md](gerrit-current.md)) and A_wetted is the submerged electrode area (shape-aware – a rod counts its end face, a tube does not). Raising j does two opposing things at once:

1. **Helps:** more current → more dissolved H₂ (and O₂) per Faraday's law → more substrate for the hydrogen-oxidiser, up to the point where mass transfer or the organism's uptake saturates.
2. **Hurts:** more current → more anodic oxidant (O₂, and any free chlorine if chloride is present), a larger local pH excursion at both electrodes, and more Joule heat – all of which impair or kill cells, first in the electrode boundary layer and then in the bulk.

So a growth-rate-versus-j curve rises, peaks at the optimum j, then falls. The tolerated ceiling is the highest j at which viability is not measurably worse than a current-free (or decoupled-gas) control. The single hardest part of the measurement is separating the "helps" axis from the "hurts" axis, because a naïve single-arm screen conflates substrate limitation at low j with toxicity at high j. The decoupled control arm is what breaks that degeneracy.

### Acceptance checks & pitfalls

- **Substrate/toxicity confound:** a monotonically rising OD-versus-j curve with no peak usually means you never reached the toxic regime – extend the series upward. A monotonically falling one means even your lowest j is already inhibitory – extend downward. A real optimum has a peak.
- **Area basis must match the model:** j is meaningless without its area. Use the shape-aware A_wetted (rod versus tube differ by the end face) and record which electrode was fitted. Re-deriving j against a different area later will move the thresholds.
- **Chloride confound:** if the medium carries chloride, part of the "toxicity" is free chlorine, not current per se; a chloride-free medium isolates the pure current-density effect. Report the medium's chloride with the result.
- **Electrode conditioning drift:** current at a fixed intensity drifts in the first minutes (bubble coverage, oxide growth). Follow the gerrit-current.md settling period so the j you assign is the j the cells actually saw.
- **Do not extrapolate past the validated intensity band:** j targets that need an intensity beyond the validated band may not deliver the assumed current as cell voltage nears the rail; verify with the in-line current measurement rather than trusting the setpoint.
- **One strain's number is not another's:** HOB tolerances span at least an order of magnitude across the literature. Do not reuse an optimum j across strains; the whole point of the screen is that it is strain-specific.

## Sources

- [Rosa/Kracke – Power to hydrogen-oxidizing bacteria: effect of current density on bacterial activity and community spectra (J Cleaner Prod 2020)](https://www.sciencedirect.com/science/article/abs/pii/S0959652620316437)
- [Electro-cultivation of hydrogen-oxidizing bacteria to accumulate ammonium and CO₂ into protein-rich biomass](https://www.researchgate.net/publication/359193104_Electro-cultivation_of_hydrogen-oxidizing_bacteria_to_accumulate_ammonium_and_carbon_dioxide_into_protein-rich_biomass)
- [Givirovskiy – Electrode material studies, in-situ water electrolysis in pH-neutral electrolyte (Heliyon 2019)](https://www.sciencedirect.com/science/article/pii/S2405844018368130)
- [Givirovskiy – In-situ water electrolyzer stack for an electrobioreactor (Energies 2019)](https://mdpi.com/1996-1073/12/10/1904/htm)
