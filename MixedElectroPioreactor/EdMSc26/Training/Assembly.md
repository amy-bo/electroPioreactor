# MEP Assembly (Edinburgh MSc)

You will assemble two MEP0.02 units: **ed04** and **ed05**. Both arrive with microSDs flashed and the FZone CO₂ regulator stack pre-built and pressure-tested by Martin.

ed04 is the unit that gets a **bagged Pt-plated Ti anode** unwrapped and installed today. ed05 has all the newest other parts; its electrodes are already installed from bench testing.

## PPE

- Eye / face protection
- Lab coat
- Gloves for media handling

You do not need cryogenic gloves. The CARMA AEP0.1.1 instructions call for them when tightening a SodaStream against a bare cylinder; on these MEPs the SodaStream is pre-attached to the FZone regulator and you will not be detaching it.

## Layout

1. Place the dovetail raft on the bench with dovetails to front-left.
2. Mount on the raft, left to right: peristaltic pumps, then Pioreactor, then product bottle, then media bottle, then SodaStream + FZone regulator stack.
3. Connect the Pioreactor 12 V PSU. The unit boots within ~90 s.
4. From a laptop on the same network, open `http://ed04.local/` (or `http://ed05.local/`). Confirm the unit appears in the cluster view.

## Electrodes (ed04 only – fresh anode)

ed05 has its electrodes already installed; skip to "Vial and PWM connections" for ed05.

For ed04:

1. Unwrap the bagged Pt-plated Ti anode. Avoid touching the platinised section.
2. Insert the anode and the stainless-steel cathode into their o-rings in the Vial Cap, half-way, with a twisting motion to avoid dislodging the o-rings.
3. Push each electrode fully into its captive-nut [Electrode Top Stop](../../../Components/ElectrodeTopStop).
4. Tighten the **red** electrode cable onto the Pt-plated Ti **anode** ring crimp using the M3 bolt through the captive nut.
5. Tighten the **black** electrode cable onto the stainless-steel **cathode** ring crimp using the M3 bolt through the captive nut.
   - Polarity matters. Reversing red and black dissolves the platinum coating into solution within minutes.
6. Push the Top Stops down so the electrodes protrude into the vial at the standard depth (use the depth recorded by Martin during PreTransport).

## Vial and PWM connections (both units)

1. Add bicarbonate solution (or your prepared MC02 medium) to the vial.
2. Screw the Vial Cap fully onto the vial.
3. Attach a 0.2 µm vent filter to the male luer on the CO₂ entry port.
4. Attach two 0.2 µm vent filters to the two male luers on the exhaust ports.
5. Seat the vial in the Pioreactor.
6. Connect the solenoid barrel plug to **PWM channel 4** on the Pioreactor HAT.
7. Connect the **media** pump to **PWM channel 3**.
8. Connect the **waste** pump to **PWM channel 2**.

The Pioreactor's `[PWM]` config (canonical map: 1=stirring, 2=waste, 3=media, 4=relay/alt_media, 5=heating) is already on the flashed microSD. You should not need to edit `config.ini`.

## Hand-off

Once both units are assembled, vials seated, and reachable on the network, move on to [Operation.md](Operation.md) for the walkthrough, then [Calibration.md](Calibration.md) for the practical.
