---
id: step-14-configure-sparging-and-electrolysis
order: 14
title: "Configure sparging and electrolysis"
guide: [aep]
parts:
  - {component: solenoid-valve, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: config-ini
    question: "What does `config.ini` show for PWM 4 and the plugin?"
    options:
      - {label: "`4=relay`, and an `[electropioreactor.config]` section", correct: true}
      - {label: "`4=waste`, and an `[electropioreactor.config]` section", fix: "Set PWM 4 to `relay` on the UI's **Configuration** page (see **Check the plugin**)."}
      - {label: "`4=relay`, but no `[electropioreactor.config]` section", fix: "Re-run the plugin install (see **Check the plugin**). The installer patches `config.ini`."}
  - id: solenoid-sparges
    question: "At each test sparge, what do you hear and see?"
    options:
      - {label: "A click, then CO₂ bubbling into the vial", correct: true}
      - {label: "A click, but no bubbling in the vial", fix: "Check the adapter pin and the regulator are open, then open the needle valve: **CO₂ gas train** left it closed."}
      - {label: "No click, and no bubbling in the vial", fix: "Check the 12V supply is in the HAT's barrel jack and the shunt is on the pins closest to the LED outputs (**Raspberry Pi and HAT**). Without both, PWM 4 cannot drive the solenoid."}
  - id: settings-live
    question: "Which parameters can you change in the job's **Settings** panel?"
    options:
      - {label: "All four, including the OD pause", correct: true}
      - {label: "Three: an OD pause change seems ignored", fix: "It is not ignored: `od_pause_after_sparge_seconds` takes effect on the next sparge cycle, not the one in progress."}
---

1. On the **Configuration** page, check `config.ini` contains the following. The installer adds `4=relay` and the `[electropioreactor.config]` section; channel 3 was set to `waste` in [Nutrient solution](step-09-set-up-nutrient-solution-flow.md). <!-- from video: session-20 0:05:46 - media pump on PWM 2, waste on 3; the text had 2=waste, 3=media -->

   ```ini
   [PWM]
   # map the PWM channels to externals.
   # hardware PWM are available on channels 1 & 3.
   1=stirring
   2=media
   3=waste
   4=relay
   5=heating

   [electropioreactor.config]
   electrolysis_power=2.5              ; LED D intensity (0-10 %, clamped at runtime)
   sparge_duration_seconds=10.0        ; solenoid open time per cycle (s)
   sparge_interval_minutes=60.0        ; cycle frequency (min)
   od_pause_after_sparge_seconds=5.0   ; OD settle window after sparge ends (s)
   ```

2. Open **electroPioreactor** from **Activities** on the **Manage** screen.
3. Set a test sparge in the job's **Settings** panel: interval 1 minute, duration 1 second.
4. Listen for the solenoid clicking open at each sparge.
5. Open the needle valve while watching the vial, until the bubbling looks right.
6. Set your working sparge interval and duration in the job's **Settings** panel.

   <img width="877" height="167" alt="The pioreactor-relay-plugin on/off toggle in the Pioreactor UI (AEP0.1.1 screenshot)" src="https://github.com/user-attachments/assets/71183531-ccc0-4fb2-b36e-4153a897ce3b" />
   <!-- TODO: AEP0.1.1 screenshot of the pioreactor-relay-plugin toggle, used as a placeholder - retake showing the electroPioreactor job in Activities and its Settings panel | assignee: @Martin -->

<details>
<summary>Notes</summary>

- All four parameters are editable live from **Settings**. `od_pause_after_sparge_seconds` applies from the next sparge.
- Electrolysis power stays clamped to 10% at runtime to protect the electrodes.

</details>
