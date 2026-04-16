# Irvine River HOB Enrichment – Medium

Medium for HOB enrichment using the [AEP0.1](https://github.com/amy-bo/electroPioreactor) electroPioreactor.

---

## MC02 medium (provided by Edinburgh)

The medium is [MC02](https://github.com/amy-bo/electroPioreactor/tree/main/Media), prepared and provided by Bingqiao of Edinburgh University's Chris French Lab. It arrives as three bottles:

| Bottle | Contents | Dose per litre final medium |
|---|---|---|
| Mesonutrients | Na₂HPO₄, NaH₂PO₄·2H₂O, K₂SO₄, CaSO₄·2H₂O, MgSO₄·7H₂O, (NH₄)₂SO₄ | base solution |
| Iron solution | FeSO₄·7H₂O in 0.2 M H₂SO₄ | 3.40 mL |
| Mineral solution | Na₂MoO₄·2H₂O, ZnSO₄·7H₂O, MnSO₄·H₂O, CuSO₄·5H₂O, NiSO₄·6H₂O, CoSO₄·7H₂O in 0.2 M H₂SO₄ | 0.050 mL |

Combine per the dosing above. The resulting medium gives a phosphate buffer molarity of ~40 mM and a conductivity of ~6.1 mS/cm, consistent with Sydow et al. (2017) optimal medium. See [Media/README.md](../../Media/README.md) for full formulation details and rationale.

### Storage

Store iron and mineral solution bottles in amber bottles at 4°C. Purge iron solution headspace with an inert gas (N₂ or Ar) or CO₂ after each use. Remake if the iron solution turns yellow-brown or precipitate appears. See [Media/README.md](../../Media/README.md) for expected shelf life.

---

## Yeast extract (Stage 4 only)

1.0 g/L, prepared as a separate stock in distilled water and pressure-cooked before use. Do not include in Stages 2–3.

---

## NaHCO₃ (optional)

0.10 g/L, added directly to the medium. In a CO₂-sparged reactor, dissolved inorganic carbon is replenished continuously by sparging and NaHCO₃ is not needed during normal operation. Include it if the reactor will be run without sparging for any period, as it provides an inorganic carbon reserve at startup.

---

## Conductivity supplement (optional, for future optimisation)

Givirovskiy et al. (2019) add 5.45 g/L Na₂SO₄ to increase medium conductivity and reduce ohmic losses during electrolysis. This may materially help reduce ohmic constraints depending on current density and electrode geometry, and could be worth investigating once baseline enrichment is established. Not recommended for first enrichment attempts; record baseline conductivity and voltage first.

---

## References

- Givirovskiy et al. (2019) https://doi.org/10.3390/en12101904
- Sydow et al. (2017) https://doi.org/10.1002/elsc.201600252
