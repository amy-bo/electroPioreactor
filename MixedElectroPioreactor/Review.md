# MEP Training Docs – Review

A working file for picking which of the 12 suggested doc improvements to action. Not for students; not committed.

## How to answer

For each item:

- Tick the **`Apply`** box to accept the suggestion as written.
- Or write a one-line **`Override`** to do something different.
- Leave both blank to skip.

When done, tell me "action it" and I'll edit the docs accordingly.

---

## 1. Refresh experiment-profile YAML schema

CARMA's example uses `hours_elapsed` and `repeat_every_hours`; current schema is `t` (with unit suffixes like `10s`, `1h`) and `every`. Affects [Operation.md § Batch step 5.iv](Operation.md) (the relay-plugin profile reference) and any YAML pasted from CARMA. Fix: inline a refreshed YAML, or warn students against copying CARMA's verbatim.

Source: [experiment-profiles-schema](https://docs.pioreactor.com/user-guide/experiment-profiles-schema).

- [ ] Apply
- Override:

---

## 2. Pump calibration is volumetric (UI-driven), not gravimetric

Pioreactor's current "Duration-based pump calibration" lives on the **Protocols** page. The UI asks for comma-separated target volumes (mL) and prompts the user to report measured volume after each dispense. [Calibration.md § 1](Calibration.md) prescribes weighing on an analytical balance and references "ml/s at 100 % duty"; balance is fine as a precision aid but the section reads as a parallel procedure rather than a UI walkthrough. Reframe: "Run the UI's Duration-based pump calibration. Use the analytical balance as a more accurate way to measure the dispensed volume."

Source: [hardware-calibrations](https://docs.pioreactor.com/user-guide/hardware-calibrations).

- [ ] Apply
- Override:

---

## 3. Dosing-automation parameter names don't match the UI

In the live UI: **chemostat** takes `volume` (mL) and `duration` (minutes). **Turbidostat** takes `exchange volume` (mL, recommended 1.0–2.0 mL for fast-growing cultures), `target biomass`, and `biomass signal` (default `auto`; options `normalized_od` / `od_fused` / `od` / `auto`). [Operation.md § 2](Operation.md) and [§ 3](Operation.md) say "Volume per dose / Interval" and "OD target / Volume per dose". Update labels to match what students will see.

Source: [dosing-automations](https://docs.pioreactor.com/user-guide/dosing-automations).

- [ ] Apply
- Override:

---

## 4. Stirring calibration is missing from `Calibration.md`

Pioreactor calibrates RPM vs PWM duty for stirring; 26.4.4 added a multi-Pioreactor simultaneous flow so ed04 and ed05 can be calibrated in parallel (~5 min). Without it, students will see odd stirring behaviour and blame assembly. Add a short § 0 (or § 4) in [Calibration.md](Calibration.md) for stirring calibration before pumps.

Source: [Pioreactor 26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110).

- [ ] Apply
- Override:

---

## 5. OD blanking step is missing and 26.4.x is stricter about it

26.4.0 moved OD blank correction upstream into `od_reading` per-experiment, and the OD reader refuses to start with calibrations or fused estimators enabled if a blank exists. [Operation.md § Batch step 5.ii](Operation.md) says "Start OD reading; check trace updates" but skips blanking. Add a step before inoculation: read a blank against the bicarbonate-only (or media-only) vial.

Source: [Pioreactor 26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110).

- [ ] Apply
- Override:

---

## 6. Bioreactor config key renamed: `max_working_volume_ml` → `efflux_tube_volume_ml`

26.4.x renamed this key in `[bioreactor]`. [Operation.md § Modes at a glance](Operation.md) and § Chemostat reference "working volume is 15 ml" in prose. Add an aside so students recognise `efflux_tube_volume_ml` if they open `config.ini`.

Source: [Pioreactor 26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110).

- [ ] Apply
- Override:

---

## 7. Pioreactor's pump example uses PWM 2 = media (wrong vs canonical)

Pioreactor's [using-pumps](https://docs.pioreactor.com/user-guide/using-pumps) page uses "PWM channel 2" as a generic media-pump example. Canonical config and our [PR #17](https://github.com/amy-bo/electroPioreactor/pull/17) have 2=waste. Students who follow Pioreactor's example will swap media and waste tubing. Add one defensive sentence to [Assembly-EdMSc26.md § Vial and PWM connections](Assembly-EdMSc26.md): "If you read Pioreactor's pump docs, ignore any example that uses PWM 2 for media; ed04/ed05 use the canonical 2=waste, 3=media."

- [ ] Apply
- Override:

---

## 8. UI plugin installer is now first-class

The "Plugins" item in the left nav surfaces installed and recommended plugins; `pio plugins install <name>` still works as a CLI fallback. Useful if a microSD has to be re-flashed on the day. Add a one-liner to [PreTransportCheck-EdMSc26.md § On arrival](PreTransportCheck-EdMSc26.md) (or [Assembly-EdMSc26.md](Assembly-EdMSc26.md)): "If a unit needs the relay or electroPioreactor plugin reinstalled, click Plugins in the left nav rather than dropping to a shell."

Source: [using-community-plugins](https://docs.pioreactor.com/user-guide/using-community-plugins).

- [ ] Apply
- Override:

---

## 9. Published amybo MEP0.02 BOM lists crocodile clips, not captive-nut Top Stops

The [BOM at amybo.org](https://amybo.org/docs/electropioreactor/electropioreactor-v0.02/) describes crocodile-clip electrode connection. The kit going to Edinburgh uses AEP0.1.1 captive-nut Top Stops per your direction. Either update the published BOM, or add an aside to [Assembly-EdMSc26.md § Electrodes](Assembly-EdMSc26.md): "The published MEP0.02 BOM may show crocodile clips; the kit you've received uses AEP0.1.1 captive-nut Top Stops instead."

- [ ] Apply
- Override:

---

## 10. PSU swap invalidates stirring and pump calibrations

Pioreactor's [external-power](https://docs.pioreactor.com/user-guide/external-power) guide warns that stirring and pump calibrations must be re-run if the PSU model changes. If Edinburgh's bench PSU isn't identical to the one used in Coventry, the calibrations from PreTransport are invalid. Add a checkbox to [PreTransportCheck-EdMSc26.md § On arrival](PreTransportCheck-EdMSc26.md): "Confirm Edinburgh PSU model and voltage match the bench setup; otherwise re-calibrate stirring and pumps before [Calibration](Calibration.md)."

- [ ] Apply
- Override:

---

## 11. Chemostat: small media-add vs waste-remove asymmetry is known

Forum thread [#801](https://forum.pioreactor.com/t/dosing-volumes-how-to-keep-the-volume-added-and-the-volume-removed-to-be-equal/801) flags that media-add and waste-remove volumes can drift apart slightly over many cycles, so vial level can creep. Add a one-line caveat to [Operation.md § 2 Chemostat](Operation.md): "Vial level can drift slightly over many dilution cycles. Check at the end of the run; top up or bleed as needed."

- [ ] Apply
- Override:

---

## 12. Relative cross-references break if students read docs outside the repo

Your relative links (`../Components/ElectrodeTopStop`, `../PastResearch/Brown-HarrisLab/...`) work on GitHub from `MixedElectroPioreactor/`, but 404 if a student opens just the `MixedElectroPioreactor/` folder locally without the parent tree. Two options:

- **(a)** Keep relative; explicitly tell students to clone the whole repo.
- **(b)** Convert the cross-tree links to absolute `https://github.com/amy-bo/electroPioreactor/...` URLs.

If you tick Apply with no override, I'll do (b). Tick (a) by writing `a` in the override.

- [ ] Apply (option b)
- Override:

---

## Sign off

When you're done filling in the boxes, tell me "action it" and I'll apply your decisions in a single commit.
