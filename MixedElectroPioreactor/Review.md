# MEP Training Docs – Review

A working file for picking which of the suggested doc improvements/issues to action. Not for students; not committed.

**Pass 2 (2026-05-20):** old item 4 (stirring section) removed – fixed in commit `6b26f24`. Old item 2 reference updated (§ 1 → § 2 post-renumbering). Items 12–15 added on re-review of the just-committed Calibration/Operation/Assembly changes.

**Pass 3 (2026-05-20):** anchor links added throughout (internal `#section` slugs + external `#anchor` or `:~:text=…` fragments). All 11 external sources re-fetched and verified; wording corrected on items 3 (chemostat field is **`exchange volume`** not `volume`), 7 (CLI form needs `--source <location>`), 8 (BOM lists 1× crocodile clip with no assembly text), 10 (mechanism is intentional waste over-removal + tube-height setpoint, not multi-cycle drift). Item 2 body clarified to address "isn't 1 mL = 1 g?" challenge — yes, balance is fine; the real reframe is input shape (mL, not seconds).

**Pass 4 (2026-05-20):** actioned 12 items (2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15); deferred 3 (1 awaiting plugin-side validation per your override, 8 BOM lives on amybo.org separate from this repo, 9 PSU travels with units from Newmilns per your note — no change to verify). Mid-flow addition: **§ 3 OD calibration** added to Calibration.md per your "OD calibration as opposed to OD blanking" question. That renumbers Calibration § 3 Level → § 4, § 4 CO₂ → § 5, § 5 Electrolysis → § 6 — PreTransport anchors updated to match. Coventry typo in item 9 corrected to Newmilns. Item 4's "should this also be added to calibration?" answered inline: no — OD **blanking** is per-experiment so it belongs in Operation. OD **calibration** (the cell-density-vs-photodiode curve) is per-unit and now lives in Calibration § 3. File saved but **not committed** so you can review in VS Code.

**Pass 4.1 (2026-05-20):** OD calibration link **verified against source** (you caught me having drafted it un-checked). Page is at [`/user-guide/calibrate-od600`](https://docs.pioreactor.com/user-guide/calibrate-od600) (titled "Standard curves for OD600 readings"), **not** `hardware-calibrations#od-calibration` as Pass 4 had it. Section anchor `#running-the-calibration` confirmed. Two facts added to the section while I was there: lives on the **Protocols** page (Device = `od90`); recommended re-calibration cadence is **every 6 months or on optical-setup change**.

## How to answer

For each item:

- Tick the **`Apply`** box to accept the suggestion as written.
- Or write a one-line **`Override`** to do something different.
- Leave both blank to skip.

When done, tell me "action it" and I'll edit the docs accordingly.

---

## 1. Refresh experiment-profile YAML schema

CARMA's example uses `hours_elapsed` and `repeat_every_hours`; current schema is `t` (with unit suffixes like `10s`, `1h`) and `every`. Affects [Operation.md § Batch step 5.iv](Operation.md#1-batch-experiment) (look for *"the pioreactor-relay-plugin profile"*) and any YAML pasted from CARMA. Fix: inline a refreshed YAML, or warn students against copying CARMA's verbatim.

Source verified: [experiment-profiles-schema § Actions](https://docs.pioreactor.com/user-guide/experiment-profiles-schema#actions) — exact wording: *"`t`: Use either a bare number (interpreted in hours) or a string with a unit suffix (s, m, h, or d, such as 30s, 0.5h, or 2d)"*; loops use `every: <time_string_or_float>`. Note: `hours_elapsed()` exists as an expression helper inside `${{…}}`, not as a top-level field — so CARMA's `hours_elapsed:` key shape is wrong against the current schema.

- [ ] Apply
- Please check with the electroPioreactor plugin and ensure everything is correct.

---

## 2. Pump calibration: doc framing doesn't match UI input shape

The UI's "Duration-based pump calibration" (Protocols page) asks the student to **enter target volumes in mL** (comma-separated), runs the pump for a computed duration, then asks the student to **report the actual volume dispensed**. [Calibration.md § 2 Peristaltic pumps](Calibration.md#2-peristaltic-pumps) (look for *"Run the pump for the calibration duration the UI requests"*) currently describes the inverse — enter durations, weigh the output. The balance is fine as a precision aid (1 mL water ≈ 1 g at room temp), but the workflow framing won't match what students see. Reframe: "Run the UI's Duration-based pump calibration. The UI will prompt you for target volumes; use the analytical balance to measure the actual dispensed volume more accurately than the eyeball."

Source verified: [hardware-calibrations § Pump calibration](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration) — *"Enter the target volumes to calibrate around (comma-separated values, in mL)"*.

- [x] Apply


---

## 3. Dosing-automation parameter names don't match the UI

In the live UI: **chemostat** takes `duration` (minutes) and **`exchange volume`** (mL — not just "volume"). **Turbidostat** takes `exchange volume` (mL, recommended 1.0–2.0 mL for fast-growing cultures), `target biomass`, and `biomass signal` (default `auto`; options `normalized_od` / `od_fused` / `od` / `auto`). [Operation.md § 2 Chemostat](Operation.md#2-chemostat) says "Volume per dose / Interval"; [§ 3 Turbidostat](Operation.md#3-turbidostat) says "OD target / Volume per dose". Update labels to match what students will see.

Source verified: [dosing-automations § Chemostat](https://docs.pioreactor.com/user-guide/dosing-automations#chemostat) and [§ Turbidostat](https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat). Confirmed: chemostat field label is "exchange volume", not "volume" — Review.md wording fixed in this pass.

- [x] Apply
- Override:

---

## 4. OD blanking step is missing and 26.4.x is stricter about it

26.4.0 moved OD blank correction upstream into `od_reading` per-experiment, and the OD reader now refuses to start with calibrations or fused estimators enabled if a blank exists. [Operation.md § 1 Batch experiment, step 5.ii](Operation.md#1-batch-experiment) (look for *"Start; check the OD trace updates"*) skips blanking. Add a step before inoculation: read a blank against the bicarbonate-only (or media-only) vial.

Source verified: [Pioreactor 26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110#:~:text=od_blank%20correction%20is%20now%20applied%20upstream) — exact wording: *"od_blank correction is now applied upstream in od_reading on a per-experiment basis before readings reach growth_rate_calculating … If a blank exists for the experiment, od_reading now refuses to start with OD calibrations or fused estimators enabled, instead raising a ValueError."*

- [x] Apply - should this also be added to calibration?
- Override:

---

## 5. Bioreactor config key renamed: `max_working_volume_ml` → `efflux_tube_volume_ml`

26.4.x renamed this key in `[bioreactor]`. [Operation.md § Modes at a glance](Operation.md#modes-at-a-glance) and [§ 2 Chemostat](Operation.md#2-chemostat) reference *"Working volume is 15 ml"* in prose. Add an aside so students recognise `efflux_tube_volume_ml` if they open `config.ini`. UI label is now "Efflux tube level".

Source verified: [Pioreactor 26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110#:~:text=Renamed%20the%20shared%20bioreactor%20volume%20setting) — exact wording: *"Renamed the shared bioreactor volume setting max_working_volume_ml to efflux_tube_volume_ml, including the UI label (Efflux tube level), MQTT/API state, and device config/cache migration during update."*

- [x] Apply   - but we need to suggest that they fill to 14ml max to accomodate the volume of the electrodes and sparging tube
- Override:

---

## 6. Pioreactor's pump example uses PWM 2 = media (wrong vs canonical)

Pioreactor's [using-pumps](https://docs.pioreactor.com/user-guide/using-pumps#:~:text=PWM%20channel%202) page uses PWM channel 2 as a generic media-pump example — exact wording: *"In our case, if we were to use the pump as a media pump, we would connect the pump to PWM channel 2."* Canonical config and our [PR #17](https://github.com/amy-bo/electroPioreactor/pull/17) have 2=waste. Students who follow Pioreactor's example will swap media and waste tubing. Add one defensive sentence to [Assembly-EdMSc26.md § Vial and PWM connections](Assembly-EdMSc26.md#vial-and-pwm-connections-both-units): "If you read Pioreactor's pump docs, ignore any example that uses PWM 2 for media; ed04/ed05 use the canonical 2=waste, 3=media."

- [x] Apply
- Override:

---

## 7. UI plugin installer is now first-class

The "Plugins" item in the left nav surfaces installed and recommended plugins; the CLI fallback is `pio plugins install <name-of-plugin> --source <location of .whl file>` (the `--source` flag is required per the docs example, not the bare form). Useful if a microSD has to be re-flashed on the day. Add a one-liner to [PreTransportCheck-EdMSc26.md § On arrival](PreTransportCheck-EdMSc26.md#on-arrival-edinburgh-martin) (or [Assembly-EdMSc26.md](Assembly-EdMSc26.md)): "If a unit needs the relay or electroPioreactor plugin reinstalled, click Plugins in the left nav rather than dropping to a shell."

Source verified: [using-community-plugins](https://docs.pioreactor.com/user-guide/using-community-plugins#:~:text=Plugins%27%20button%20on%20the%20left%20navigation%20bar) — *"From your Pioreactor's interface, the 'Plugins' button on the left navigation bar will display all your currently installed plugins, and some recommended plugins."*

- [x] Apply
- Override:

---

## 8. Published amybo MEP0.02 BOM lists a crocodile clip, not captive-nut Top Stops

The [BOM at amybo.org](https://amybo.org/docs/electropioreactor/electropioreactor-v0.02/) lists *"1× Crocodile clip"* under its Electrolysis section (singular, no assembly text on how it connects to the electrodes). The kit going to Edinburgh uses AEP0.1.1 captive-nut Top Stops per your direction. A student going by the published BOM alone wouldn't know the connection method, but if they default to "crocodile clip means alligator-clip on bare wire" they'd mismatch the Top Stop captive-nut approach. Either update the published BOM, or add an aside to [Assembly-EdMSc26.md § Electrodes](Assembly-EdMSc26.md#electrodes-ed04-only--fresh-anode): "The published MEP0.02 BOM may list a crocodile clip in its electrolysis parts; the kit you've received uses AEP0.1.1 captive-nut Top Stops instead."

- [ ] Apply
- Override:  Update the BOM

---

## 9. PSU swap invalidates stirring and pump calibrations

If Edinburgh's bench PSU isn't identical to the one used in Newmilns, the calibrations from PreTransport are invalid. Add a checkbox to [PreTransportCheck-EdMSc26.md § On arrival](PreTransportCheck-EdMSc26.md#on-arrival-edinburgh-martin): "Confirm Edinburgh PSU model and voltage match the bench setup; otherwise re-calibrate stirring and pumps before [Calibration](Calibration.md)."

Source verified: [external-power](https://docs.pioreactor.com/user-guide/external-power#:~:text=When%20changing%20the%20default%20power%20supply) — exact wording: *"When changing the default power supply, any stirring calibration and pump calibrations will need to be updated."*

- [ ] Apply
- Override:  Where do you get Coventry from?  We’re in Newmilns, Gerrit’s in Swansea, Imperial in London and Bingqiao in Edinburgh.  The MSc PSU’s were the ones I used in Newmilns.

---

## 10. Chemostat: waste pump intentionally over-removes — tube height is the level setpoint

Forum thread [#801](https://forum.pioreactor.com/t/dosing-volumes-how-to-keep-the-volume-added-and-the-volume-removed-to-be-equal/801) clarifies that Pioreactor's defaults intentionally remove **more** waste than media added (e.g. add 0.5 mL, remove 1.5 mL) to prevent overflow. The vial level is set by the **waste tube height**, not the media/waste volume ratio. Recommended mitigation: position the waste tube at the desired vial level before starting. A `waste_removal_multiplier` config exists but tuning it is flagged as risky in the thread.

(Previous Pass-2 framing described "drift over many cycles" — that was wrong; the agent's re-read of the thread shows the mechanism is intentional over-removal + tube-position convergence, not accumulated dosing error.)

Replace the suggested Pass-2 caveat with: add to [Operation.md § 2 Chemostat](Operation.md#2-chemostat) — "Position the waste tube at your desired vial level before starting. The waste pump over-runs each dilution cycle by design; tube height is the level setpoint, not the media/waste volume ratio."

- [x] Apply
- Override:

---

## 11. Relative cross-references break if students read docs outside the repo

Your relative links (`../Components/ElectrodeTopStop`, `../PastResearch/Brown-HarrisLab/...`) work on GitHub from `MixedElectroPioreactor/`, but 404 if a student opens just the `MixedElectroPioreactor/` folder locally without the parent tree. Two options:

- **(a)** Keep relative; explicitly tell students to clone the whole repo.
- **(b)** Convert the cross-tree links to absolute `https://github.com/amy-bo/electroPioreactor/...` URLs.

If you tick Apply with no override, I'll do (b). Tick (a) by writing `a` in the override.

- [x] Apply (option b)
- Override:

---

## 12. Stirring section in Calibration.md links to the wrong Pioreactor page

[Calibration.md § 1 Stirring](Calibration.md#1-stirring) currently anchors to `pre-flight-hardware-check#step-1-run-a-self-test` — the Self-Test guide, the *same URL* [§ 0 Self test](Calibration.md#0-self-test) already uses. Should point to the stirring-calibration procedure proper. Fix: replace the link with [hardware-calibrations#stirring-calibration](https://docs.pioreactor.com/user-guide/hardware-calibrations#stirring-calibration) (or whichever page in the [26.4.x release notes](https://forum.pioreactor.com/t/new-pioreactor-release-26-4-x/1110) covers the multi-unit simultaneous-calibration flow).

- [x] Apply
- Override:

---

## 13. Calibration.md step numbering jumps

Two sections in Calibration.md jump in their numbered lists (note: post-Pass-4, these are now § 4 Level and § 6 Electrolysis after the OD calibration insert):

- [§ 4 Level](Calibration.md#4-level): was `1, 2, 3, 5, 6, 7, 8` (no step 4) — fixed to consecutive 1–7
- [§ 6 Electrolysis](Calibration.md#6-electrolysis-v-and-i-at-25--led-d): was `1, 2, 3, 4, 6` (no step 5) — fixed to consecutive 1–5

Markdown renders these as-typed (it doesn't auto-correct gaps the way it auto-renumbers `1, 1, 1`). Fix: renumber consecutively.

- [x] Apply
- Override:

---

## 14. Operation.md "Fed batch" intro vs "Batch" elsewhere

The [intro paragraph in Operation.md](Operation.md) says "**Fed batch**, **chemostat**, and **turbidostat**", but the [Modes-at-a-glance table](Operation.md#modes-at-a-glance) row and the [§ 1 Batch experiment](Operation.md#1-batch-experiment) heading still say "Batch". § 1's procedure also describes a one-time fill, no media in, no waste out — which is plain batch, not fed-batch. Pick one term and use it everywhere (likely revert intro to "Batch" rather than rename, since the procedure isn't fed-batch).

- [ ] Apply (revert intro to "Batch")
- Override:  The procedure jolly well is fed-batch, what are the macronutrients?  CO2 H2 O2 - explain this once in the document then explain that for brevitry we will call it batch thereafter.

---

## 15. PreTransportCheck cross-ref anchors to Calibration are broken

The renumbering (and Pass-4 OD-calibration insert) moved Calibration [§ 2 CO₂](Calibration.md#5-co-flow-rate) → **§ 5** and [§ 3 Electrolysis](Calibration.md#6-electrolysis-v-and-i-at-25--led-d) → **§ 6**. Three links in [PreTransportCheck-EdMSc26.md](PreTransportCheck-EdMSc26.md) were anchoring to old section numbers and 404'ing:

- line 54: `Calibration.md#3-electrolysis-v-and-i-at-25--led-d` → fixed to `#6-electrolysis-v-and-i-at-25--led-d`
- line 81: `Calibration.md#2-co-flow-rate-needle-valve-only` → fixed to `#5-co-flow-rate`
- line 82: same as 81 → fixed

Each anchor (and the visible "§ 2"/"§ 3" labels, now "§ 5"/"§ 6") updated to match the new section numbers.

- [x] Apply
- Override:

---

## Sign off

When you're done filling in the boxes, tell me "action it" and I'll apply your decisions in a single commit.
