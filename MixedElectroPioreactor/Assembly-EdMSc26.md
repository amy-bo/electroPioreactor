# MEP Assembly (Edinburgh MSc)

You will assemble two MEP0.3 units: **ed04** and **ed05**. Both arrive with microSDs flashed and the FZone-HPControl CO₂ regulator-solenoid stack pre-built by Martin.

ed04 is the unit that gets a **bagged Pt-plated Ti anode** which you can unwrap and instal once you are comfortable using ed05. ed05 has all the newest other parts; its electrodes are already installed from bench testing.

## PPE

- Eye / face protection
- Lab coat
- Gloves for media handling

The CARMA AEP0.1.1 instructions call for cryogenic gloves when tightening a SodaStream against a bare cylinder; on these MEPs the SodaStream is attached via a right-angle adapter with SodaStream-pin-screw by fully unscrewing this, no CO₂ should leak when changing cylinders.  Screw it fully in, so you see the regulator dials rise, when using the electroPioreactors.

## Layout

1. Setup a mobile phone hotspot with SSID AMYBO and password raspberry.
2. Place the dovetail raft on the bench with dovetails to front and left.
3. Familiarise yourself with the raft.  At the rear we have the SodaStream cylinder with the right angle pin screw adapter on top, the CO₂ regulator is on top of this, it's left dial shows the SodaStream pressure (advanced warning that you're running out of CO2) and the right dial showing the pressure reaching the solenoid.  The solenoid is, attached to the right of the regulator with a lead connecting to PWM4, the needle valve comes out of the front of the solenoid.  In front of the SodaStream Cylinder we have the product container left of media container, with their respective peristaltic pumps in front of them, then the electroPioreactor at the very front.
5. Connect the black 12 V PSU to the Pioreactor HAT's barrel jack connector and the white 5V Raspberry Pi PSU to the micro-USB socket on the Raspberry Pi (the frontmost socket on the bottom PCB if the Pioreactor Logo is facing you. The electroPioreactor should boot within ~90 s.
6. From a laptop connected to the mobile phone hotspot, open `http://ed04.local/` (or `http://ed05.local/`). Confirm the unit appears in the cluster view.

## Vial and PWM connections (both units)

1. Add bicarbonate solution (or your prepared MC02 medium) to the vial.
2. Screw the Vial Cap fully onto the vial.
5. Seat the vial in the Pioreactor.

## Hand-off

Once both units are assembled, vials seated, and reachable on the network, move on to [Operation.md](Operation.md) for the walkthrough, then [Calibration.md](Calibration.md) for the practical.

## Electrodes (ed04 only – fresh anode)

ed05 has its Platinum Plated Ti anode and Stainless Steel cathode already installed; ed04 has some low grade graphite electrodes installed, these should be used for testing purposes only - sodium bicarbonate is recommended instead of MC01 for these graphite electrodes, as MC01 corroded them more rapidly.

Once you are confident in operation and ready to install ed04's Platinum Plated Ti anode and Stainless Steel cathode

1. Us a 2.5mm Hex key to gently unscrew the screws on the [TopStop](../Components/ElectrodeTopStop) (with the red and black wires), then gently remove the top stop.
2. Unscrew the vial from the cap and disconnect the tubing (take a photo first so you can remember how to reconnect it.
3. Very gently rotate the graphite electrodes up and out of the vial cap.
4. Ensure the vial cap electrode o-rings are correctly seated in the vial cap and that they stay there throughout the next step.
5. Unwrap the bagged stainless steel cathode.
6. Very very gently rotate and push the stainless steel up through the anode's o-ring (to loosen it, the stainless steel anode is fractionally smaller & less delicate) then gently rotate it back out.
7. Very very gently rotate and push the stainless steel up through the cathode's o-ring.
9. Unwrap the bagged Pt-plated Ti anode. Try to avoid touching the platinised section.
10. Very very gently rotate and push the anode into its o-ring in the Vial Cap.
11. Rotate and adjust the heights of both electrodes so their bases are 33mm below the bottom of the vial cap.
12. Ensure the wires are correctly located in the TopStop so they will come into firm contact with each electrode when the TopStop screws are tightened onto the electrode
13. Push the TopStop down fully onto the electrodes.
14. Tighten the **red** electrode cable onto the Pt-plated Ti **anode** using the M3 bolt through the captive nut.
15. Tighten the **black** electrode cable onto the stainless-steel **cathode** using the M3 bolt through the captive nut.
   - Polarity matters. Reversing red and black dissolves the stainless steel into solution.
12. Reconnect the tubing and screw the vial back into place
