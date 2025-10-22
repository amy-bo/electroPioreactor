# Venting Solenoid Valves

## Selection Criteria

### Venting
Non‑venting solenoid valves result in backflow because, when they shut, they trap a volume of CO₂ between the solenoid and the broth (largely water). As determined by [Eli Silver at Brown](../../Past%20research/Brown%20-%20Harris%20Lab/1.%20CO2%20backflow%20diagnosis%20-%20Eli%20Silver.md), this CO₂ completely dissolves in the water, drawing the water back up to the valve. Given that the aseptic electroPioreactor requires filters between the solenoid valve and the broth, this is unacceptable. As [demonstrated by Eli Silver](../../Past%20research/Brown%20-%20Harris%20Lab/2.%20Backflow%20testing%20with%20revised%20components%20-%20Eli%20Silver.md), this can be resolved by employing a **3/2 venting** solenoid which connects the reactor to the CO₂ supply when closed and vents the reactor to atmosphere when open.

### Other selection criteria
- **Direct‑acting operation:** Must function from 0 bar differential pressure (no pilot assist).
- **Voltage:** Pioreactor peristaltic pumps are most [accurate at 12 V DC](https://pioreactor.com/products/peristaltic-pump?srsltid=AfmBOopqCva4IPJAFzWi4JB8_vKfOdVNGJQGYBdzjM64rJHtXwWiJc7H&amp;utm_source=chatgpt.com). If a second power supply is used for this purpose, it’s preferable not to require a third for the solenoid valve. If 12 V is not available, 5 V DC solenoids could potentially run from the Raspberry Pi power supply; however, 5 V DC **venting** solenoids are rare, sub‑miniature, and often use push‑fit or non‑standard connectors.
- **Venting function:** Must exhaust trapped CO₂ to atmosphere when closed.
- **CO₂ compatibility:** All wetted materials must tolerate dry (and ideally also humid) CO₂ exposure without swelling or corrosion.
- **Wetted materials:** Prefer food‑grade, non‑cytotoxic materials (e.g., FKM, EPDM, PTFE, PPS, or stainless steel).
- **Sterilisability:** Ideally capable of cleaning or sterilisation (EtOH, peracetic acid, or autoclave resistance desirable).
- **Operation:** Manual actuation, bistable or latching preferred so the valve does not need to be continuously actuated or removed for continuous CO₂ sparging.
- **Certifications:** CE/UKCA and RoHS compliance required; FDA/EU 1935/2004 desirable.
- **Form factor:** Compact size for integration with the electroPioreactor system; standard threads to allow short, direct connections to other equipment.
- **Pressure &amp; temperature:** Suitable for ~0–8 bar and 0–70 °C operating conditions.

## Why not use the valve trialled at Brown?
The [solenoid valve trialled at Brown](https://a.co/d/0sMpHv1) is harder to procure in the UK. Both it and a [1/8″ BSP version](https://amzn.eu/d/7Ma3tM2) sold via amazon.co.uk are pilot‑operated (minimum ~1.7 bar) and not intended for aseptic use.

## Preferred options

### Bürkert 6014
The [Bürkert 6014 209280](https://tameson.co.uk/products/solenoid-valve-3-2-way-g1-8-bistable-brass-fkm-0-16bar-232psi-12vdc-latching-6014-209280) is a **3/2 venting**, **12 V DC**, **direct‑acting** valve available in G 1/8″ BSPP configuration, with options for latching coils, FKM or EPDM seals, and materials compliant with FDA, EU 1935/2004, and USP Class VI standards.

### HP Control R23 (Selected low‑cost direct‑acting valve)
The [HP Control R23](https://hpcontrol.uk/elektrozawor-r23-1-8-cala-2-lub-3-drogowy-laczony-w-grupy.html) is a low‑cost venting valve selected for its direct‑acting design and ability to operate from 0 bar. It has 1/8″ BSPP in/out ports (interchangeable with the Bürkert 6014), an M5 vent, a 12 V DC coil, and a manual override. Although not food‑grade, it is CE‑ and RoHS‑certified and suitable for dry CO₂ use post‑regulator.

### Low‑cost valve assessment summary
A full comparative assessment of all valves considered (including the R23, TAILONZ 3V210‑08, and other sub‑£30 models) can be found in [Venting Solenoids under £30.md](Venting%20Solenoids%20under%20£30.md). That concludes that the R23 provides the best compromise for low‑pressure CO₂ venting.
