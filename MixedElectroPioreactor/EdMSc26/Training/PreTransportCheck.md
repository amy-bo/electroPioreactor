# MEP Pre-Transport Check (ed04, ed05)

Bench checks Martin runs in Coventry the week before transport to Edinburgh, so that on arrival the only remaining steps are: media fill, the bagged-anode install on ed04, and (for both units) a SodaStream attach.

Two MEP0.02 units in scope: **ed04** and **ed05**. ed01–ed03 are Bingqiao's. ed04 will receive the bagged Pt-plated Ti anode at Edinburgh; ed05 has all the newest other parts and its electrodes are already installed and will not change.

The values Martin records below are the references students will compare their own measurements to during [Calibration.md](Calibration.md). Each "**Record:**" line is a deliberate action, not just a tick.

## Bench tests (per unit)

Run on ed04, then repeat on ed05. Don't transport a unit with an unticked row.

### 1. Boot and network

- [ ] Power on, Pi boots within ~90 s
- [ ] Web UI reachable at `http://ed04.local/` (resp. `http://ed05.local/`)
- [ ] Unit appears in cluster, MQTT online

### 2. Stirring

- [ ] Stirring starts from web UI, fan spins, no rattle
- [ ] Stops cleanly

### 3. Wet electrolysis

ed04 bench-tests with whatever electrodes are currently installed; those get swapped for the bagged fresh anode at Edinburgh, and a new reference V and I recorded then. ed05's installed electrodes are the experiment set and don't change.

- [ ] Vial filled with bicarbonate solution, electrodes at standard depth
- [ ] LED D set to **2.5 %**
- [ ] Bubbles visible on both electrodes within 30 s; cathode bubble rate roughly twice anode rate
- [ ] **Record (ed05 only):** V across electrodes ____ V, I through electrodes ____ mA. This is the reference for [Calibration § 3](Calibration.md#3-electrolysis-v-and-i-at-25--led-d).
- [ ] **Record (ed04, sanity only):** V ____ V, I ____ mA. Student reference for ed04 is set on arrival post-anode-swap.
- [ ] LED D back to 0 % at end of test

### 4. Pumps

- [ ] Media pump (PWM 3) ticks forwards on a manual dose, fluid moves through
- [ ] Waste pump (PWM 2) ticks forwards on a manual dose, fluid moves through
- [ ] Both stop cleanly

### 5. Solenoid (CO₂ relay on PWM 4)

- [ ] With CO₂ cylinder open and needle valve cracked, manual relay-on produces a visible bubble stream into the vial via the entry filter
- [ ] Bubble rate varies smoothly when the PWM duty is stepped (10 %, 50 %, 100 %)
- [ ] Solenoid clicks audibly on each toggle
- [ ] Closes cleanly with no continued bubbling

## FZone leak check

All three threaded ports around the FZone solenoid (regulator side, needle-valve side, blanking-plug side) were sealed with **Loctite 577 anaerobic thread sealant** for the first time on 2026-04-30. Cure is well past. Two checks below.

### A. Baseline flow comparison vs AEP0.1.1's ODL setup

The AEP0.1.1 reference uses the [Premium ODL SodaStream regulator](../../../Components/CO2%20transfer/Regulators.md) at 1 bar. FZone has a fixed, non-adjustable outlet pressure, so MEP flow is set by the needle valve alone. We want MEP flow comparable to ODL@1bar so the experiment regime ports across.

- [ ] Connect ed04's FZone + solenoid + needle-valve stack to its SodaStream
- [ ] With solenoid held open and needle valve cracked, time to fill a 100 ml inverted measuring cylinder over water: ed04 ____ s, ed05 ____ s
- [ ] Repeat with AEP0.1.1's ODL stack (regulator at 1 bar): reference ____ s
- [ ] **Record:** needle-valve setting (turns from fully closed) that makes each MEP fill comparably to the ODL reference: ed04 ____ turns, ed05 ____ turns. Target for [Calibration § 2](Calibration.md#2-co-flow-rate-needle-valve-only).
- [ ] **Record:** ml CO₂ per second of solenoid-open at the target setting: ed04 ____ ml/s, ed05 ____ ml/s. Target for [Calibration § 2](Calibration.md#2-co-flow-rate-needle-valve-only).

### B. Pressure-decay (snoop + rate-stability)

FZone has no usable outlet gauge, so the test is soapy water plus rate-stability over time.

- [ ] Cylinder open, needle valve closed downstream of solenoid, solenoid open
- [ ] Paint soapy water onto each Loctite-577 joint; observe per joint for 60 s, no new bubbles = pass
- [ ] Open needle valve to a steady bubble rate into a water bath; record initial bubbles per minute, leave 30 min, recount
- [ ] Cylinder closed at end of test, system bled down before pack

## Pack and transport

- [ ] Vial drained, rinsed, dried, packed inside Pioreactor
- [ ] Solenoid + needle valve + regulator stack kept assembled; SodaStream **detached** for transport
- [ ] ed04's spare bagged anode kept sealed in its bag
- [ ] PSUs, ethernet, multimeter, balance, cryo gloves (for SodaStream re-attach), bicarbonate solution in the shared kit box

## On arrival (Edinburgh, Martin)

1. Tighten each unit's SodaStream onto its FZone regulator (cryo gloves on for the swift tighten).
2. **ed04 only:** unbag the fresh Pt-plated Ti anode, install through the captive-nut [Electrode Top Stop](../../../Components/ElectrodeTopStop) following [Assembly § Electrodes](Assembly.md#electrodes-ed04-only--fresh-anode), set down to standard depth.
3. **ed04 only:** re-run [wet electrolysis](#3-wet-electrolysis) at 2.5 % LED D. **Record:** new V ____ V, new I ____ mA. This is the student reference for ed04 (the bench numbers above were for the now-removed test electrodes).
4. Fill media bottles, prime media and waste pumps.
5. Hand off to students for [Assembly.md](Assembly.md) → [Operation.md](Operation.md) → [Calibration.md](Calibration.md).
