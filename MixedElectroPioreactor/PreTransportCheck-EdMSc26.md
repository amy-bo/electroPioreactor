# MEP Pre-Transport Check (ed04, ed05)

Bench checks Martin runs in Newmilns the week before transport to Edinburgh, so that on arrival the only remaining steps are: media fill, the bagged-anode install on ed04, and (for both units) a SodaStream attach.

Two MEP0.02 units in scope: **ed04** and **ed05** each set up as solo leader-workers. ed01–ed03 are Bingqiao's, already in active use in Chris French lab. ed04 will receive the new RPi Zero 2W once ed05 confirmed working then the bagged Pt-plated Ti anode at Edinburgh; ed05 has all the newest other parts and its electrodes are already installed and will not change.

The values Martin records below are the references students will compare their own measurements to during [Calibration.md](Calibration.md). Each "**Record:**" line is a deliberate action, not just a tick.

## Bench tests

Run on ed05, then swap pio01's RPi 4B for the new RPi Zero 2W, insert ed04's TF, and repeat on ed04. Each check below has paired ed05 and ed04 boxes so you can tick per unit. Don't transport a unit with an unticked row.

### 1. Boot and network

- [x] ed05: Power on, Pi boots within ~90 s - 35s
- [ ] ed04: Power on, Pi boots within ~90 s
- [ ] ed05: Web UI reachable at http://ed05.local/
- [ ] ed04: Web UI reachable at http://ed04.local/
- [ ] ed05: Activity dashboard updates live (local MQTT broker up)
- [ ] ed04: Activity dashboard updates live (local MQTT broker up)
- [ ] ed05: `amybo` + own-hotspot fallback configured via nmcli (autoconnect-priority 20 / 0)
- [ ] ed04: `amybo` + own-hotspot fallback configured via nmcli (autoconnect-priority 20 / 0)
- [ ] ed05: `amybo` off → falls back to own hotspot within ~60 s, SSH via 10.42.0.1 works
- [ ] ed04: `amybo` off → falls back to own hotspot within ~60 s, SSH via 10.42.0.1 works
- [ ] ed05: `amybo` back on → rejoins, SSH via ed05.local works
- [ ] ed04: `amybo` back on → rejoins, SSH via ed04.local works

### 2. Stirring

- [ ] ed05: Stirring starts from web UI, fan spins, no rattle
- [ ] ed04: Stirring starts from web UI, fan spins, no rattle
- [ ] ed05: Stops cleanly
- [ ] ed04: Stops cleanly

### 3. Solenoid (CO₂ relay on PWM 4)

- [ ] ed05: With CO₂ cylinder open and needle valve cracked, manual relay-on produces a visible bubble stream into the vial via the entry filter
- [ ] ed04: With CO₂ cylinder open and needle valve cracked, manual relay-on produces a visible bubble stream into the vial via the entry filter
- [ ] ed05: Solenoid clicks audibly on each toggle
- [ ] ed04: Solenoid clicks audibly on each toggle
- [ ] ed05: Closes cleanly with no continued bubbling
- [ ] ed04: Closes cleanly with no continued bubbling

### 4. Wet electrolysis

ed05 bench-tests with its own installed electrodes (the experiment set, not changing). Those electrodes are then moved to ed04 for its bench test and returned to ed05 afterwards. ed04 is left with the bagged fresh Pt-plated Ti anode at Edinburgh, where a new reference V and I are recorded.

- [ ] ed05: Vial filled with bicarbonate solution, electrodes at standard depth
- [ ] ed04: Vial filled with bicarbonate solution, electrodes at standard depth
- [ ] ed05: LED D set to **2.5 %**
- [ ] ed04: LED D set to **2.5 %**
- [ ] ed05: Bubbles visible on both electrodes within 30 s; cathode bubble rate roughly twice anode rate
- [ ] ed04: Bubbles visible on both electrodes within 30 s; cathode bubble rate roughly twice anode rate
- [ ] **Record (ed05 only):** V across electrodes ____ V, I through electrodes ____ mA. This is the reference for [Calibration § 3](Calibration.md#3-electrolysis-v-and-i-at-25--led-d).
- [ ] **Record (ed04, sanity only):** V ____ V, I ____ mA. Student reference for ed04 is set on arrival post-anode-swap.
- [ ] ed05: LED D back to 0 % at end of test
- [ ] ed04: LED D back to 0 % at end of test

### 5. Pumps

- [ ] ed05: Media pump (PWM 3) ticks forwards on a manual dose, fluid moves through
- [ ] ed04: Media pump (PWM 3) ticks forwards on a manual dose, fluid moves through
- [ ] ed05: Waste pump (PWM 2) ticks forwards on a manual dose, fluid moves through
- [ ] ed04: Waste pump (PWM 2) ticks forwards on a manual dose, fluid moves through
- [ ] ed05: Both stop cleanly
- [ ] ed04: Both stop cleanly



## Solenoid leak check

All three threaded ports around the HPcontrols solenoid (regulator side, needle-valve side, blanking-plug side) were sealed with **Loctite 577 anaerobic thread sealant** for the first time on 2026-04-30. Cure is well past. Two checks below.

### A. Baseline flow comparison vs AEP0.1.1's ODL setup

The AEP0.1.1 reference uses the [Premium ODL SodaStream regulator](../Components/CO2%20transfer/Regulators.md) at 1 bar. FZone has a fixed, non-adjustable outlet pressure, so MEP flow is set by the needle valve alone. We want MEP flow comparable to ODL@1bar so the experiment regime ports across.

- [ ] Connect ed04's FZone + solenoid + needle-valve stack to its SodaStream
- [ ] With solenoid held open and needle valve cracked, time to fill a 100 ml inverted measuring cylinder over water: ed04 ____ s, ed05 ____ s
- [ ] Repeat with AEP0.1.1's ODL stack (regulator at 1 bar): reference ____ s
- [ ] **Record:** needle-valve setting (turns from fully closed) that makes each MEP fill comparably to the ODL reference: ed04 ____ turns, ed05 ____ turns. Target for [Calibration § 2](Calibration.md#2-co-flow-rate-needle-valve-only).
- [ ] **Record:** ml CO₂ per second of solenoid-open at the target setting: ed04 ____ ml/s, ed05 ____ ml/s. Target for [Calibration § 2](Calibration.md#2-co-flow-rate-needle-valve-only).

### B. Pressure-decay (snoop + rate-stability)

FZone has cylinder and outlet gauges, so a glance at the outlet gauge during a quiescent period is the first tell. The two checks below are the more sensitive follow-ups for the slow leaks Loctite-577 might still let through: snoop with soapy water, then watch flow-rate stability over 30 min.

- [ ] Cylinder open, needle valve closed downstream of solenoid, solenoid open
- [ ] Outlet gauge holds steady for 60 s with the needle valve closed: ed05 ____ , ed04 ____ (any drop = leak upstream of the needle valve)
- [ ] Paint soapy water onto each Loctite-577 joint; observe per joint for 60 s, no new bubbles = pass
- [ ] Open needle valve to a steady bubble rate into a water bath; record initial bubbles per minute, leave 30 min, recount
- [ ] Cylinder closed at end of test, system bled down before pack

## Pack and transport

- [ ] Vial drained, rinsed, dried, packed inside Pioreactor
- [ ] Solenoid + needle valve + regulator stack kept assembled; SodaStream **detached** for transport
- [ ] ed04's spare bagged anode kept sealed in its bag
- [ ] PSUs, ethernet, multimeter, balance, cryo gloves (for SodaStream re-attach), bicarbonate solution in the shared kit box
- [ ] microSD reader (already owned, bring it for on-site recovery if `amybo` fallback misbehaves)

## On arrival (Edinburgh, Martin)

1. Tighten each unit's SodaStream onto its FZone regulator (cryo gloves on for the swift tighten).
2. **ed04 only:** unbag the fresh Pt-plated Ti anode, install through the captive-nut [Electrode Top Stop](../Components/ElectrodeTopStop) following [Assembly § Electrodes](Assembly-EdMSc26.md#electrodes-ed04-only--fresh-anode), set down to standard depth.
3. **ed04 only:** re-run [wet electrolysis](#4-wet-electrolysis) at 2.5 % LED D. **Record:** new V ____ V, new I ____ mA. This is the student reference for ed04 (the bench numbers above were for the now-removed test electrodes).
4. Fill media bottles, prime media and waste pumps.
5. Hand off to students for [Assembly](Assembly-EdMSc26.md) → [Operation](Operation.md) → [Calibration](Calibration.md).
