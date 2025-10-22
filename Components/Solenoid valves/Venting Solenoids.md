# Venting Solenoid Valves
## Selection Criteria
### Venting
Non-venting solenoid valves result in backflow as, when they shut, they trap a volume of CO2 between the solenoid and the broth (largely water).  As determined by [Eli Silver at Brown](../../Past%20research/Brown%20-%20Harris%20Lab/1.%20CO2%20backflow%20diagnosis%20-%20Eli%20Silver.md) this CO2 completely dissolves in the water drawing the water back up to the valve.  Given that the Aseptic electroPioreactor requires filters between the solenoid valve and the broth, this is unacceptable.

### Other selection criteria
- **Direct-acting operation:** Must function from 0 bar differential pressure (no pilot assist).
- **Voltage:** 12 V DC or below preferred for compatibility with standard control systems.
- **Venting function:** Must exhaust trapped CO₂ to atmosphere when de-energised.
- **CO₂ compatibility:** All wetted materials must tolerate dry and humid CO₂ exposure without swelling or corrosion.
- **Wetted materials:** Prefer food-grade, non-cytotoxic materials (e.g. FKM, EPDM, PTFE, PPS, or stainless steel).
- **Sterilisability:** Ideally capable of cleaning or sterilisation (EtOH, peracetic acid, or autoclave resistance desirable).
- **Manual override:** Manual actuation preferred for testing and safety.
- **Certifications:** CE/UKCA and RoHS compliance required; FDA/EU 1935/2004 desirable.
- **Pressure and temperature range:** Suitable for 0–8 bar and 0–70 °C operating conditions.
- **Form factor:** Compact size for integration near the reactor vessel; standard BSPP or compatible threads.

## Why Not use the valve trialled at Brown?
The [solenoid valve trialled at Brown](https://a.co/d/0sMpHv1) is harder to procure in the UK, both it, and a [1/8" BSP version](https://amzn.eu/d/7Ma3tM2) sold via amazon.co.uk are not intended for Aseptic use, they are also pilot operated, requiring minimum 1.7 bar.

## Valve selection
### Bürkert 6014 (Optimum / Food-Grade Option)
The [Bürkert 6014](https://tameson.co.uk/products/solenoid-valve-3-2-way-g1-8-bistable-brass-fkm-0-16bar-232psi-12vdc-latching-6014-209280) is available in G 1/8″ BSPP configuration, with versions featuring latching coils, FKM or EPDM seals, and materials compliant with FDA, EU 1935/2004, and USP Class VI standards.  

### HP Control R23 (Selected Low-Cost Direct-Acting Valve)
The [HP Control R23](https://hpcontrol.uk/elektrozawor-r23-1-8-cala-2-lub-3-drogowy-laczony-w-grupy.html) is a low-cost venting valve, selected for its direct-acting design and ability to operate from 0 bar.  
It has 1/8″ BSPP in/out ports (hence interchangeable with the similar Bürkert 6014's) it has an M5 vent, a 12 V DC coil, and includes a manual override.  
Although not food-grade, it is CE- and RoHS-certified and suitable for dry CO₂ use post-regulator.  

### Low cost valve Assessment Summary
A full comparative assessment of all valves considered (including the R23, TAILONZ 3V210-08, and other sub-£30 models) can be found in [Venting Solenoids under £30.md](Venting%20Solenoids%20under%20£30.md).  
That concludes that the R23 provides the best compromise for low-pressure CO₂ venting.

