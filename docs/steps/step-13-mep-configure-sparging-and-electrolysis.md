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
   electrolysis_power=2.5              ; LED D intensity (0-10 %, clamped at runtime)
   sparge_duration_seconds=10.0        ; solenoid open time per cycle (s)
   sparge_interval_minutes=60.0        ; cycle frequency (min)
   od_pause_after_sparge_seconds=5.0   ; OD settle window after sparge ends (s)
   ```

2. Open **electroPioreactor** from **Activities** on the **Manage** screen.
3. Set a test sparge in the job's **Settings** panel: interval 1 minute, duration 1 second.
4. Listen for the solenoid clicking open at each sparge.
5. Open the needle valve while watching the vial, until the bubbling looks right.
6. Set your working sparge interval and duration in the job's **Settings** panel. The MEP runs 3 seconds every hour.

<details>
<summary>Notes</summary>

- All four parameters are editable live from **Settings**. `od_pause_after_sparge_seconds` applies from the next sparge.
- Electrolysis power stays clamped to 10% at runtime to protect the electrodes.

</details>
