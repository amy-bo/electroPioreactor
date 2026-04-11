# Home HOB Enrichment Methodology – Crymlyn Fen

A home-lab protocol for enriching hydrogen-oxidising bacteria (HOB) from environmental samples using the [AEP0.1](https://github.com/amy-bo/electroPioreactor) electroPioreactor. Developed for the AMYBO community; intended as a living document to be iterated on as results come in.

---

## Medium

Two formulation options are presented. Option A is [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media), the medium used in the CARMA Hub project by Imperial College and University of Edinburgh, adapted only where necessary for home accessibility. Option B is a potential literature synthesis that is more accessible to home users who cannot source NaH₂PO₄·2H₂O, but departs more from [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and results will not be directly comparable with CARMA Hub experiments. For results directly comparable with CARMA Hub experiments, use Option A.

---

### Option A – [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media) (recommended for CARMA Hub compatibility)

#### Mesonutrients (per litre final medium)

| Component | Formula | Amount |
|---|---|---|
| Disodium hydrogen phosphate | Na₂HPO₄ | 2.895 g |
| Sodium dihydrogen phosphate dihydrate | NaH₂PO₄·2H₂O | 3.060 g |
| Potassium sulphate | K₂SO₄ | 0.170 g |
| Calcium sulphate dihydrate | CaSO₄·2H₂O | 0.097 g |
| Magnesium sulphate heptahydrate | MgSO₄·7H₂O | 0.800 g |
| Ammonium sulphate | (NH₄)₂SO₄ | 0.943 g |

This gives a phosphate buffer molarity of ~40 mM and a conductivity of ~6.1 mS/cm, consistent with Sydow et al. (2017) optimal medium. MgSO₄ at 0.800 g/L follows Sydow et al. (2017) and [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media); Givirovskiy et al. (2019) use 0.5 g/L. Either is defensible; 0.800 g/L is used here for [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media) consistency.

> **CaSO₄ preparation note:** CaSO₄·2H₂O (gypsum) has very low solubility (~2.4 g/L at 25°C). At 0.097 g/L the working concentration is well within this limit, but a concentrated stock is not feasible. Add CaSO₄·2H₂O directly to the final medium volume rather than preparing a stock solution. Home source: homebrew/winemaking supplier (food-grade gypsum).

> **NaH₂PO₄·2H₂O availability note:** Monosodium phosphate dihydrate is available from online laboratory suppliers (e.g. Labpals, Sigma via Amazon). If genuinely unavailable, see Option B for a KH₂PO₄-based alternative and its trade-offs.

#### Trace elements – Iron Solution (make 100 mL, dose 3.40 mL per litre of medium)

| Component | Formula | Amount |
|---|---|---|
| Iron(II) sulphate heptahydrate | FeSO₄·7H₂O | 1.50 g |
| Sulphuric acid (0.2 M) | H₂SO₄ | to 100 mL |

H₂SO₄ at 0.2 M is the preferred acidulant: no carbon source, no chloride, lower vapour pressure than HCl, and longer shelf life. At home, battery acid (typically ~30–35% H₂SO₄) can be used to prepare a 0.2 M solution by careful dilution into water. Handle with gloves and eye protection; always add acid to water, never the reverse.

If H₂SO₄ is genuinely inaccessible, HCl (sold as brick acid/patio cleaner at B&Q, typically 30–36%) is the next best option. It introduces a small chloride contribution but at this dilution it is negligible in the final medium. HCl is Sydow et al.'s original acidulant.

> **Why not citric acid:** Citric acid is a readily metabolisable carbon source for heterotrophs and some HOB. In a protocol designed to select against heterotrophs in Stages 2–3, adding any free carbon source to the iron stock undermines the selective pressure and means autotrophic growth cannot be confirmed as the sole basis for OD increase. Note that ferric ammonium citrate, used by Givirovskiy et al. (2019) at 5 mg/L, is a different case – at that concentration the carbon load is negligible and chelation improves iron bioavailability. However, it introduces ammonium and is harder to source at home than FeSO₄, so it is not recommended here.

> **Iron stock shelf life:** Store in an amber bottle at 4°C. Purge headspace with CO₂ from the SodaStream after each use. Remake when the solution turns yellow-brown or precipitate appears.

#### Trace elements – Mineral Solution (make 50 mL, dose 0.050 mL per litre of medium)

| Component | Formula | Amount |
|---|---|---|
| Sodium molybdate dihydrate | Na₂MoO₄·2H₂O | 0.090 g |
| Zinc sulphate heptahydrate | ZnSO₄·7H₂O | 0.120 g |
| Manganese(II) sulphate monohydrate | MnSO₄·H₂O | 0.120 g |
| Copper(II) sulphate pentahydrate | CuSO₄·5H₂O | 0.024 g |
| Nickel(II) sulphate hexahydrate | NiSO₄·6H₂O | 0.075 g |
| Cobalt(II) sulphate heptahydrate | CoSO₄·7H₂O | 0.002 g |

Prepare in 0.2 M H₂SO₄ (or HCl if H₂SO₄ unavailable). Store in amber bottle at 4°C.

#### Yeast extract (Stage 4 only)

1.0 g/L, prepared as a separate stock in distilled water and pressure-cooked before use. Do not include in Stages 2–3.

#### NaHCO₃ (optional)

0.10 g/L, added directly to the medium. In a CO₂-sparged reactor, dissolved inorganic carbon is replenished continuously by sparging and NaHCO₃ is not needed during normal operation. Include it if the reactor will be run without sparging for any period, as it provides an inorganic carbon reserve at startup.

#### Conductivity supplement (optional, for future optimisation)

Givirovskiy et al. (2019) add 5.45 g/L Na₂SO₄ to increase medium conductivity and reduce ohmic losses during electrolysis. This may materially help reduce ohmic constraints depending on current density and electrode geometry, and could be worth investigating once baseline enrichment is established. Na₂SO₄ is available as washing soda decahydrate from hardware shops. Not recommended for first enrichment attempts; record baseline conductivity and voltage first.

---

### Option B – Potential literature synthesis

This option is more accessible to home users who cannot source NaH₂PO₄·2H₂O, but departs more from [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media) and results will not be directly comparable with CARMA Hub experiments.

#### Key differences from Option A

| Parameter | Option A ([MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media)) | Option B | Trade-off |
|---|---|---|---|
| Phosphate buffer | Na-based (NaH₂PO₄·2H₂O + Na₂HPO₄) | K/Na mixed (KH₂PO₄ + Na₂HPO₄) | Option B raises K⁺ from ~2 mM to ~20 mM. Dinges et al. (2024) show that neither all-K⁺ nor all-Na⁺ buffer performs as well as a mixed buffer for *C. necator*; 20 mM K⁺ is a meaningful departure from Sydow's optimum, though a second-order concern for an enrichment culture of unknown composition |
| Potassium source | K₂SO₄ (0.17 g/L, separate) | Via KH₂PO₄ (excess) | Option A gives tighter control of K⁺ |
| Nitrogen source | (NH₄)₂SO₄ | (NH₄)₂SO₄ | Same |
| Calcium source | CaSO₄·2H₂O | CaSO₄·2H₂O | Same |
| Iron acidulant | H₂SO₄ preferred, HCl acceptable | HCl (brick acid) | HCl more accessible at home |
| Trace elements | Full 6-component mineral solution | Full 6-component mineral solution | Same – see note below |

> **Trace element note:** Both options use the full 6-component mineral solution. Mn and Zn in particular are cofactors for key metalloenzymes in HOB and must not be omitted in Stages 2–3 where there is no yeast extract to compensate.

#### Option B mesonutrients (per litre)

| Component | Formula | Amount |
|---|---|---|
| Potassium dihydrogen phosphate | KH₂PO₄ | 2.67 g |
| Disodium hydrogen phosphate | Na₂HPO₄ | 2.90 g |
| Ammonium sulphate | (NH₄)₂SO₄ | 0.94 g |
| Magnesium sulphate heptahydrate | MgSO₄·7H₂O | 0.80 g |
| Calcium sulphate dihydrate | CaSO₄·2H₂O | 0.097 g |

CaSO₄ preparation note applies identically – add directly to final medium volume, do not prepare as a concentrated stock.

Iron solution and mineral solution: prepare as per Option A.

---

## Methodology

### Equipment and materials checklist

- AEP0.1 (fully assembled with electrodes, CO₂ sparging, and peristaltic pumps)
- SodaStream cylinder, connected and regulated
- Multimeter
- Stovetop pressure cooker
- Clean sealable sample jars (scalded with boiling water)
- OpenFlexure microscope
- Disposable sterile syringe (from pharmacy) for yeast extract addition in Stage 4
- Medium prepared as per chosen option above, without yeast extract
- Yeast extract stock prepared separately in distilled water and pressure-cooked
- 12V battery and leads (optional – see field pre-conditioning below)

---

### Safety note – hydrogen

Water electrolysis produces H₂ at the cathode. H₂ is explosive at 4–75% v/v in air. Before biomass is established and actively consuming H₂, headspace concentrations may approach or exceed the lower explosive limit. During all stages, and especially Stages 2–3 before growth is confirmed:

- Work in a well-ventilated space
- Keep all ignition sources away from the reactor (naked flames, sparking switches, unsleeved electrical connections)
- Do not seal the reactor headspace – the AEP0.1 vial must remain vented as designed

Once sustained growth is confirmed by rising OD, biomass consumption will keep headspace H₂ well below the explosive limit under normal operating conditions.

---

### Stage 1 – Sampling at Crymlyn Fen

> **NNR/SSSI note:** Crymlyn is a designated National Nature Reserve. Check with Natural Resources Wales whether a sampling licence is required before visiting with collection equipment. Do not skip this step.

Sample from an open water or swamp margin, not dense reed bed. The target community is at the oxic-anoxic interface where H₂ produced by anaerobes below diffuses upward into oxygenated water – this is where HOB naturally concentrate. Take a few centimetres of interface sediment and ~200 mL of overlying water from the same location. Avoid deep sediment, which will be dominated by methanogens and sulphate reducers.

Keep samples cool and dark during transport and process within 4 hours.

Take an OpenFlexure micrograph of the raw inoculum before doing anything else. This documents starting community morphology for comparison at later stages. 100× oil immersion will resolve rod vs coccus morphology and track gross community shifts but is not sufficient to identify HOB specifically.

> **Optional field pre-conditioning:** If travelling by car with a 12V battery available, the AEP0.1 can be run at the sampling site with fen water as the initial electrolyte, with a CO₂ sparge before departure and again on return. Pre-conditioning the community to electrolysis conditions before lab enrichment improves reproducibility of subsequent community development (Pagaling et al., 2014). Given the ~2-mile distance from the Marina the transit time is short, but the practical risks – electrolyte spillage, vibration disrupting electrode contacts, and difficulty maintaining temperature during transit – should be weighed against the modest benefit. If conditions are calm and the reactor can be secured safely, it is worth doing; otherwise process the sample at home promptly.

---

### Stage 2 – Initial HOB selection (no yeast extract, no sterilisation required)

Without yeast extract, sterilisation of the medium is unnecessary. Environmental heterotrophs have no added carbon or energy source to bloom on in minimal mineral medium. H₂ and CO₂ selectively favour HOB from the outset.

Set the AEP0.1 to **30°C**. This is the standard temperature used across published HOB enrichments (Givirovskiy et al., 2019; Yang et al., 2021; Pous et al., 2022) and will substantially reduce lag phase compared with UK ambient temperatures of 17–21°C.

Fill the AEP0.1 to working volume (~14–15 mL with electrodes present). Before inoculating, run the reactor for 30 minutes with medium only and record the OD baseline. The electrodes are positioned above the OD light path and bubbles are not expected to sink into it, but establishing a pre-inoculation baseline is necessary to distinguish any residual scatter from genuine turbidity increases later.

Inoculate with ~0.7 mL (~5% v/v) of fen water with a small amount of interface sediment suspended within it.

**Begin electrolysis immediately.** In the AEP0.1, electrolysis is driven by LED D – the fourth LED channel on the Pioreactor HAT, repurposed to drive electrolysis current rather than its default illumination function. Set LED D power to 2.5%, or the lowest level that produces consistent visible bubble formation on both electrodes – whichever is higher. Record the resulting voltage and current using the multimeter. LED D power percentage is not transferable between different electrode configurations; voltage and current are the transferable reference values for anyone replicating this protocol with different hardware.

**Begin CO₂ sparging immediately.** CO₂ sparging serves two simultaneous purposes: supplying inorganic carbon for autotrophic growth, and purging excess O₂ from the headspace. Water electrolysis produces H₂ and O₂ at a 2:1 ratio but HOB consume them at approximately 4:1, so O₂ will accumulate in excess without active management. However, over-sparging will strip dissolved H₂ and CO₂ from the medium, directly limiting HOB growth. Use Pous et al. (2022) as the reference point: **twice-weekly 10-minute CO₂ flushes**. At higher electrolysis currents, O₂ may accumulate faster than this regime can clear in the AEP0.1's small working volume; if OD stalls or declines unexpectedly, increase to daily sparging as the first diagnostic step.

Set stir rate to **500 rpm** initially. Note the rate used – if results are unexpected, stir rate is a variable to revisit.

> **Troubleshooting:** If no OD increase above baseline is observed after several days, check electrode function with the multimeter to confirm current is flowing, confirm CO₂ sparging is operating, and consider collecting a fresh inoculum from a different location at the sampling site. The oxic-anoxic interface varies spatially; a different sampling point may yield a richer HOB community.

**Milestone to advance:** OD rising consistently and sustainably above the pre-inoculation baseline across multiple readings.

---

### Stage 3 – Pre-conditioning serial transfer

Once the Stage 2 milestone is met, transfer ~0.7 mL (~5% v/v) of the culture into a fresh vial of identical medium (no yeast extract, no sterilisation). Resume electrolysis, sparging, and temperature immediately. Take an OpenFlexure micrograph.

Repeat once more.

**Milestone to advance:** OD rising to a consistent level detectably faster in the second transfer than in the first.

---

### Stage 4 – Yeast extract boost

The HOB community established in Stages 2–3 now receives a growth boost via yeast extract, providing vitamins and trace organics that accelerate growth. This must be delivered in **batch mode**, not via the turbidostat. Even after two rounds of autotrophic selection, residual heterotrophs remain in the culture at low abundance. If yeast extract is introduced while the turbidostat is running, any heterotrophic growth it stimulates will be continuously amplified by dilution; delivering it as a batch pulse allows the culture to consume it and reach stationary phase before continuous dilution resumes, limiting the window during which heterotrophs can compete.

**Procedure:**

1. Turn off the turbidostat automation (switch to batch mode)
2. Using a disposable sterile syringe, add a pulse of pressure-cooked yeast extract stock directly to the running culture (target 1.0 g/L final concentration in the vial)
3. Allow the culture to consume it and reach stationary phase – indicated by OD plateauing and remaining stable for at least one hour
4. Switch the medium reservoir to yeast-extract-free medium and turn the turbidostat back on

The turbidostat will now gradually wash out any heterotrophs that grew on the yeast extract, while HOB continue on H₂ and CO₂.

**Milestone to advance:** OD stable through at least three volume turnovers of yeast-extract-free medium.

---

### Stage 5 – Electrolysis-dependence confirmation

Stop electrolysis. Continue CO₂ sparging and turbidostat operation unchanged. Confirm electrolysis has stopped by measuring current draw with the multimeter – it should drop to near zero.

If OD declines over subsequent readings and does not recover until electrolysis is restored, the culture is electrolysis-dependent. Restore electrolysis and confirm OD recovers.

Take a final OpenFlexure micrograph and compare morphology to the Stage 1 inoculum image.

**What this confirms:** The dominant organisms require electrolytically produced H₂ to grow. Obligate heterotrophs are absent or non-dominant.

**What this cannot confirm without sequencing:** Obligate chemolithotrophs and mixotrophs are not distinguishable by this protocol. Some facultative HOB (e.g. *Hydrogenophaga*, *Achromobacter*) can persist on trace organics even after washout. Electrolysis-dependence is a functional criterion, not a purity criterion – but for home-lab purposes it is the meaningful feasible endpoint.

---

## References

- Dinges et al. (2024) https://doi.org/10.1002/cssc.202301721
- Givirovskiy et al. (2019) https://doi.org/10.3390/en12101904
- Pagaling et al. (2014) https://doi.org/10.1038/ismej.2013.150
- Pous et al. (2022) http://doi.org/10.1016/j.biteb.2022.101010
- Pous et al. (2023) http://doi.org/10.1016/j.jece.2023.111550
- Sydow et al. (2017) https://doi.org/10.1002/elsc.201600252
- Yang et al. (2021) https://doi.org/10.1016/j.jclepro.2021.125921