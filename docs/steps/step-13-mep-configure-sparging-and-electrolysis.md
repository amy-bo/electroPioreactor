---
id: step-13-mep-configure-sparging-and-electrolysis
order: 13
title: "Configure sparging and electrolysis"
guide: [mep, baep]
checks_draft: true
checks:
  - id: solenoid-clicks
    question: "During the test sparge, what do you hear and see each minute?"
    options:
      - {label: "A click, then bubbles entering the vial", correct: true}
      - {label: "A click, but no bubbles entering the vial", fix: "Check the cylinder is open (pin screw fully down) and the needle valve is not closed."}
      - {label: "No click, and no bubbles entering the vial", fix: "Check the solenoid lead is in PWM 4, `4=relay` is in `config.ini`, and the 12 V supply is connected."}
  - id: closes-cleanly
    question: "When the solenoid clicks shut, what does the bubbling do?"
    options:
      - {label: "Stops with the click", correct: true}
      - {label: "Carries on after the click", fix: "Check the solenoid override is at 0."}
---

1. On the **Configuration** page, check `config.ini` contains the following. The installer adds `4=relay` and the `[electropioreactor.config]` section; channels 2 and 3 were set in **Nutrient solution**.

   ```ini
   [PWM]
   # map the PWM channels to externals.
   # hardware PWM are available on channels 1 & 3.
   1=stirring
   2=waste
   3=media
   4=relay
   5=heating

   [electropioreactor.config]
   led_channel=D                            ; LED channel for the electrode pair (A/B/C/D)
   electrolysis_power=2.5                   ; LED intensity (0-10 %, clamped at runtime)
   electrolysis_on_seconds=60.0             ; electrolysis ON time per cycle (s, > 0)
   electrolysis_off_seconds=0.0             ; electrolysis OFF time per cycle (s, >= 0; 0 = continuous)
   od_pause_after_electrolysis_seconds=5.0  ; OD settle window after electrolysis ON ends (s); negative allowed
   sparge_duration_seconds=10.0             ; solenoid open time per cycle (s)
   sparge_interval_minutes=60.0             ; cycle frequency (min)
   od_pause_after_sparge_seconds=5.0        ; OD settle window after sparge ends (s); negative allowed
   ```

2. Open **electroPioreactor** from **Activities** on the **Manage** screen.
3. Set a test sparge in the job's **Settings** panel: interval 1 minute, duration 1 second.
4. Listen for the solenoid clicking open at each sparge.
5. Open the needle valve while watching the vial, until the bubbling looks right.
6. Set your working sparge interval and duration in the job's **Settings** panel. The MEP runs 3 seconds every hour.

<details>
<summary>Notes</summary>

- The job's **Settings** panel has seven live settings: **Electrolysis Power** (%), **Electrolysis ON Time** (s), **Electrolysis OFF Time** (s, 0 = continuous), **OD Pause After Electrolysis** (s), **Sparging Duration** (s), **Sparging Interval** (min) and **OD Pause After Sparge** (s), plus a **Reset to Defaults** toggle that puts them all back to the `config.ini` values. A change applies from the next phase or sparge, not the one in progress.
- `led_channel` is not a live setting: change it in `config.ini`, then restart the job.
- Electrolysis power stays clamped to 10% at runtime to protect the electrodes.

</details>
