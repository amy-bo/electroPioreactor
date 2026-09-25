---
id: step-09-configure-sparging-and-electrolysis
order: 9
title: "Configure sparging and electrolysis"
guide: [aep]
parts:
  - {component: solenoid-valve, qty: 1, cat: prev}
checks_draft: true
checks:
  - id: config-ini
    question: "Does config.ini show 4=relay under [PWM] and an [electropioreactor.config] section?"
    issues:
      - {problem: "PWM 4 is still `waste`", fix: "Set it to `relay` on the UI's **Configuration** page (see the plugin install step)."}
      - {problem: "The `[electropioreactor.config]` section is missing", fix: "Re-run the plugin install (see the plugin install step). The installer patches `config.ini`."}
  - id: solenoid-sparges
    question: "When the job sparges, do you hear the solenoid open and CO₂ rush into the vial?"
    issues:
      - {problem: "No click from the solenoid", fix: "Check the 12V supply is in the HAT's barrel jack and the shunt was moved during hardware setup. Without both, PWM 4 cannot drive the solenoid."}
      - {problem: "The solenoid clicks but no gas flows", fix: "Check the adapter pin and the regulator are open. The needle valve was closed during CO₂ sparging setup: open it."}
  - id: settings-live
    question: "Can you see and change all four parameters in the job's **Settings** panel?"
    issues:
      - {problem: "A change to the OD pause does not seem to take effect", fix: "`od_pause_after_sparge_seconds` takes effect on the next sparge cycle, not the one in progress."}
---

1. On the **Configuration** page, check `config.ini` contains the following. The installer adds `4=relay` and the `[electropioreactor.config]` section; channel 3 was set to `waste` in [Nutrient solution](step-06-set-up-nutrient-solution-flow.md). <!-- from video: session-20 0:05:46 - media pump on PWM 2, waste on 3; the text had 2=waste, 3=media -->

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
3. For a test, set the sparge interval to 1 minute and the sparge duration to 1 second.
4. Listen for the solenoid clicking open at each sparge.
5. Watching the bubbles in the vial, open the needle valve until the flow looks right.
6. Set your working sparge interval and duration in the job's **Settings** panel.

   <img width="877" height="167" alt="image" src="https://github.com/user-attachments/assets/71183531-ccc0-4fb2-b36e-4153a897ce3b" />
   <!-- TODO: AEP0.1.1 screenshot of the pioreactor-relay-plugin toggle, used as a placeholder - retake showing the electroPioreactor job in Activities and its Settings panel | assignee: @Martin -->

<details>
<summary>Notes</summary>

- All four parameters are editable live from **Settings**. `od_pause_after_sparge_seconds` applies from the next sparge.
- Electrolysis power stays clamped to 10% at runtime to protect the electrodes.

</details>
