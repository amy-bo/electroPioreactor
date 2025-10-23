# Venting Solenoid Valves
## Selection Criteria
### Venting
Non-venting solenoid valves result in backflow as, when they shut, they trap a volume of CO2 between the solenoid and the broth (largely water).  As [determined by Eli Silver at Brown](../../Past%20research/Brown%20-%20Harris%20Lab/1.%20CO2%20backflow%20diagnosis%20-%20Eli%20Silver.md) this CO2 completely dissolves in the water drawing the water back up to the valve.  Given that the Aseptic electroPioreactor requires filters between the solenoid valve and the broth, this is unacceptable.  

As [demonstrated by Eli Silver](../../Past%20research/Brown%20-%20Harris%20Lab/2.%20Backflow%20testing%20with%20revised%20components%20-%20Eli%20Silver.md) this can be resolved by employing a 3/2 venting solenoid which connects the reactor to the CO2 supply when closed and vents the reactor to atmosphere when open.

### Other selection criteria
1. **Voltage:** Pioreactor peristaltic pumps are most [accurate at 12 V DC](https://pioreactor.com/products/peristaltic-pump?srsltid=AfmBOopqCva4IPJAFzWi4JB8_vKfOdVNGJQGYBdzjM64rJHtXwWiJc7H&utm_source=chatgpt.com), if a second power supply is being used for this purpose, it would likely be preferable to not require a third for the solenoid valve.  If 12 V was not being supplied for the peristaltic pumps, 5 V DC solenoids could potentially run from the single Raspberry Pi power supply, however 5 V DC venting solenoids tend to be rare, sub-miniature and use push-fit or non-standard connectors.
1. **Direct-acting operation:** Must function from 0 bar differential pressure (no pilot assist).
1. **CO₂ compatibility:** All wetted materials must tolerate dry (and ideally also humid) CO₂ exposure without swelling or corrosion.
1. **Wetted materials:** Prefer food-grade, non-cytotoxic materials (e.g. FKM, EPDM, PTFE, PPS, or stainless steel).
1. **Sterilisability:** Ideally capable of cleaning or sterilisation (EtOH, peracetic acid, or autoclave resistance desirable).
1. **Operation:** Manual actuation, bistable or latching preferred so solenoid valve does not need to be continuously actuated or removed for continuous CO₂ sparging.
1. **Certifications:** CE/UKCA and RoHS compliance required; FDA/EU 1935/2004 desirable.
1. **Form factor:** Compact size for integration with the electroPioreactor system; standard threads to allow short, direct connections to other equipment.

## Why not use the valve trialled at Brown?
The [solenoid valve trialled at Brown](https://a.co/d/0sMpHv1) is harder to procure in the UK. Both it, and a [1/8" BSP version](https://amzn.eu/d/7Ma3tM2) sold via amazon.co.uk are  pilot operated, requiring minimum 1.7 bar.  They are also not intended for aseptic use.

## Preferred options
### FDA / EC 1935/2004 compliant
[Bürkert Type 7017 20076521](https://www.burkert.co.uk/en/products/solenoid-valves/general-purpose-3-2-solenoids/20076521#technische-details) £99.40
3/2 universal, 12 V DC, direct-acting, PPS body, FKM seals, –1 to 1.5 bar, media-separated, chemically sterilisable, implicitly CO₂ compatible, FDA / EC 1935 / 2004 / NSF 169 compliant, 6 mm push-fit ports.
Not autoclavable above 80 °C, latching, or with standard threaded connectors.

### Latching with standard ports
The [6014 / Article number 343200](https://www.burkert.co.uk/en/products/process-and-control-valves/shut-off-valves-on-off/pneumatic-control/343200) £167
3/2 NC, 12 V DC, direct-acting, stainless-steel body, FKM seals, 0–16 bar, chemically sterilisable, implicitly CO₂ compatible, latching (pulse version) with G 1/8" BSPP ports.
Not autoclavable above 120 °C, media-separated, or food-certified.

### HP Control R23 (Selected Low-Cost Direct-Acting Valve)
The [HP Control R23](https://hpcontrol.uk/elektrozawor-r23-1-8-cala-2-lub-3-drogowy-laczony-w-grupy.html) £11.29
3/2 or 2/2 universal, 12 V DC, direct-acting, aluminium body, NBR seal, 0–8 bar (16 bar max), filtered air medium, manual override, IP65 coil with LED DIN plug, G 1/8″ BSPP ports plus M5 exhaust connector, group-mountable (modular valve island type).
Not media-separated, chemically sterilisable, or food-certified.

### Low cost valve Assessment Summary
A comparative assessment of a number valves considered (including the R23, TAILONZ 3V210-08, and other sub-£30 models) can be found in [Venting Solenoids under £30.md](Venting%20Solenoids%20under%20£30.md).
