# Irvine River HOB Enrichment – Enrichment Protocol

Lab enrichment stages for hydrogen-oxidising bacteria (HOB) following inoculum collection (see [Sampling.md](Sampling.md)) and medium preparation (see [Medium.md](Medium.md)).

---

## Safety note – hydrogen

Water electrolysis produces H₂ at the cathode. H₂ is explosive at 4–75% v/v in air. Before biomass is established and actively consuming H₂, headspace concentrations may approach or exceed the lower explosive limit. During all stages, and especially Stages 2–3 before growth is confirmed:

- Work in a well-ventilated space
- Keep all ignition sources away from the reactor (naked flames, sparking switches, unsleeved electrical connections)
- Do not seal the reactor headspace – the AEP0.1 vial must remain vented as designed

CO₂ is an asphyxiant at high concentrations. The volumes used here are small, but always sparge in a ventilated room, not a sealed enclosure.

Once sustained growth is confirmed by rising OD, biomass consumption should keep headspace H₂ below the explosive limit under normal operating conditions.

---

## Stage 1 – Pre-run calibrations

Complete all calibrations before collecting field samples. The inoculum should go into a running, calibrated reactor with as little delay as possible.

### 1a. Pioreactor calibrations

Follow the standard Pioreactor calibration procedures for OD sensor and peristaltic pumps. Record all calibration values.

### 1b. CO₂ sparge volume calibration

The AEP0.1 headspace is approximately 3 mL (20 mL vial minus 15 mL liquid minus ~2 mL of submerged electrodes and tubing). Each sparge event should deliver 15 mL of CO₂. This volume both displaces the headspace several times and bubbles through the liquid, to saturate it with CO₂ as the primary carbon source for autotrophic growth. Headspace displacement provides a secondary O₂-reduction benefit but cannot maintain low O₂ between sparges in this vented single-chamber configuration (see Stage 2 sparging rationale).

**Calibration procedure:**

1. Fill an inverted measuring cylinder with water and submerge the open end in a basin of water
2. Direct the CO₂ sparging tube into the measuring cylinder
3. Open the solenoid valve for a timed interval (start with 5 seconds) and record the volume of water displaced
4. Repeat at 3, 5, 10 and 15 seconds to establish a flow-rate curve
5. Determine the solenoid-open duration that delivers 15 mL; this is **one sparge event**

Record the calibrated sparge duration. This value is hardware-specific and must be re-measured if the SodaStream cylinder, solenoid, or tubing is changed.

---

## Stage 2 – Initial HOB selection (no yeast extract, no sterilisation required)

Without yeast extract, sterilisation of the medium is unnecessary. Environmental heterotrophs have no added carbon or energy source to bloom on in minimal mineral medium. H₂ and CO₂ selectively favour HOB from the outset.

Set the AEP0.1 to **30°C**. This is the standard temperature used across published HOB enrichments (Givirovskiy et al., 2019; Yang et al., 2021; Pous et al., 2022) and will substantially reduce lag phase compared with UK ambient temperatures.

Add 15 mL of medium. Before inoculating, run the reactor for 30 minutes with medium only and record the OD baseline. The electrodes are positioned above the OD light path and bubbles are not expected to sink into it, but establishing a pre-inoculation baseline is necessary to distinguish any residual scatter from genuine turbidity increases later.

Set stir rate to **500 rpm** initially. Note the rate used – if results are unexpected, stir rate is a variable to revisit.

**Begin electrolysis.** In the AEP0.1, electrolysis is driven by LED D – the fourth LED channel on the Pioreactor HAT, repurposed to drive electrolysis current rather than its default illumination function. Set LED D power to 2.5%, or the lowest level that produces consistent visible bubble formation on both electrodes – whichever is higher. Record the resulting voltage and current using the multimeter. LED D power percentage is not transferable between different electrode configurations; voltage and current are the transferable reference values for anyone replicating this protocol with different hardware.

**Begin automated CO₂ sparging.** CO₂ sparging serves two simultaneous purposes: supplying inorganic carbon for autotrophic growth, and purging accumulated O₂. At 1 atm CO₂ during a sparge, dissolved CO₂ saturates at ~29 mM in 15 mL (~435 µmol). HOB consume CO₂ at ~1 mol per 4 mol H₂, so at expected low currents (single mA range) this reserve lasts tens of hours between sparges.
Sparging also reduces headspace O₂ transiently, but cannot maintain low O₂ between sparges in a vented single-chamber electrolyser. Water electrolysis produces H₂ and O₂ at a 2:1 molar ratio; between sparges the vented headspace trends toward this composition.

**Frequency: 8× per day (every 3 hours)**, using the calibrated sparge duration from Stage 1b. This is driven by CO₂ replenishment timing. If OD stalls or declines unexpectedly, increase CO2 sparge frequency as the first diagnostic step.
Pausing electrolysis during each sparge (LED D → 0% for the sparge duration) provides a marginal benefit by avoiding simultaneous O₂ generation. Implement it in the automation if straightforward, otherwise do not delay starting the enrichment for this.

**Inoculate via sediment elutriation.** In a clean tube, combine ~1 mL of collected sediment with ~5 mL of river water from the same sampling site. Cap and shake vigorously for 30 seconds. Let coarse material settle for 1-2 minutes. Draw 750 μL (5% v/v) from the upper portion of the liquid for inoculation, avoiding the settled grit at the bottom. This concentrates sediment-associated microbes (including HOB, which are more abundant in sediment than in overlying water) while excluding the coarse mineral fraction that would otherwise risk scratching electrodes, jamming the stir bar, or contributing to OD noise.

**Operating mode: batch with manual volume maintenance.** Stage 2 runs in batch mode - no turbidostat or chemostat automation. At low initial cell densities, any dilution would wash out the sparse inoculum before it could establish. However, evaporative loss through the vent stubs at 30°C is significant over 10-14 days and will concentrate salts, drop the liquid level below the OD path, and eventually expose electrodes. Pause OD measurement and check the liquid level daily manually pumping in sterile deionised water (not fresh medium) to maintain 15 mL. Topping up with medium would progressively concentrate salts; topping up with water replaces only what has evaporated.

**OD growth expectations.** Do not expect detectable OD increases for at least 10–14 days. Environmental HOB are present at low abundance in river water; the inoculum starts at perhaps 10³–10⁴ relevant cells/mL. Autotrophic HOB doubling times are 6–24 hours under favourable conditions and likely longer during initial adaptation. Many doublings are needed before the culture reaches the Pioreactor's OD detection threshold. This lag is normal and consistent with published enrichment timescales.

> **Troubleshooting:** If no OD increase above baseline is observed after 14 days, check electrode function with the multimeter to confirm current is flowing, confirm CO₂ sparging is operating, and consider collecting a fresh inoculum from a different location along the river. The oxic–anoxic interface varies spatially; a different sampling point may yield a richer HOB community.

**Milestone to advance:** OD rising consistently and sustainably above the pre-inoculation baseline. Initial increases may be marginal and only distinguishable from noise by trend across 24–48 hours of readings.

---

## Stage 3 – Pre-conditioning serial transfer

Once the Stage 2 milestone is met, transfer 750 μL (5% v/v) of the culture into a fresh vial of identical medium (no yeast extract, no sterilisation). Resume electrolysis, sparging, and temperature immediately.  Stage 3 also runs in batch mode; maintain daily volume top-ups with sterile deionised water as in Stage 2.

Repeat once more.

**Milestone to advance:** OD rising to a consistent plateau in the second transfer at a similar or higher level to the first, demonstrating the culture is self-sustaining across transfers. With a single enrichment line, genuine community refinement cannot be distinguished from stochastic variation between transfers; the meaningful test is self-sustainability, not speed of growth.

---

## Stage 4 – Yeast extract boost

The HOB community established in Stages 2–3 now receives a growth boost via yeast extract, providing vitamins and trace organics that accelerate growth. This must be delivered in **batch mode**, not via the turbidostat. Even after two rounds of autotrophic selection, residual heterotrophs remain in the culture at low abundance. If yeast extract is introduced while the turbidostat is running, any heterotrophic growth it stimulates will be continuously amplified by dilution; delivering it as a batch pulse allows the culture to consume it and reach stationary phase before continuous dilution resumes, limiting the window during which heterotrophs can compete.

**Procedure:**

1. Turn off the turbidostat automation (switch to batch mode)
2. Using a disposable sterile syringe, add a pulse of pressure-cooked yeast extract stock directly to the running culture (target 1.0 g/L final concentration in the vial)
3. Allow the culture to consume it and reach stationary phase – indicated by OD plateauing and remaining stable for at least 6 hours
4. Switch the medium reservoir to yeast-extract-free medium and turn the turbidostat back on

The turbidostat will now gradually wash out any heterotrophs that grew on the yeast extract, while HOB continue on H₂ and CO₂.

After this milestone, the turbidostat continues running indefinitely as the maintenance mode for the established HOB culture.

**Milestone to advance:** OD stable through at least three volume turnovers of yeast-extract-free medium.

---

## Stage 5 – Electrolysis-dependence confirmation

Stop electrolysis. Continue CO₂ sparging and turbidostat operation unchanged. Confirm electrolysis has stopped by measuring current draw with the multimeter – it should drop to near zero.

If OD declines over subsequent readings and does not recover until electrolysis is restored, the culture is electrolysis-dependent. Restore electrolysis and confirm OD recovers.

**What this confirms:** The dominant organisms require electrolytically produced H₂ to grow. Obligate heterotrophs are absent or non-dominant.

**What this cannot confirm without sequencing:** Obligate chemolithotrophs and mixotrophs are not distinguishable by this protocol. Some facultative HOB (e.g. *Hydrogenophaga*, *Achromobacter*) can persist on trace organics even after washout. Electrolysis-dependence is a functional criterion, not a purity criterion – but for home-lab purposes it is the meaningful feasible endpoint.

---

## References

- Givirovskiy et al. (2019) https://doi.org/10.3390/en12101904
- Pous et al. (2022) https://doi.org/10.1016/j.biteb.2022.101010
- Pous et al. (2023) https://doi.org/10.1016/j.jece.2023.111550
- Rovira-Alsina et al. (2025a) https://doi.org/10.1016/j.jpowsour.2025.236499
- Rovira-Alsina et al. (2025b, preprint) https://doi.org/10.2139/ssrn.5457298
- Yang et al. (2021) https://doi.org/10.1016/j.jclepro.2021.125921