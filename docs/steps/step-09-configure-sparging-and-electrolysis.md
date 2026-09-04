---
id: step-09-configure-sparging-and-electrolysis
order: 9
title: "Configure sparging and electrolysis"
guide: [aep]
parts:
  - {component: solenoid-valve, qty: 1, cat: prev}
---

The plugin was installed at step 4 and has been driving the electrodes since step 5. Now set it up for the full cycle, with the CO₂ train built.

1. The plugin's installer patches `config.ini` for you. It should end up containing:

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

2. Restart **electroPioreactor** from the **Activities** tab of the *Manage* screen with the sparge interval you actually want. You should now hear the solenoid open and CO₂ rush into the vial. All four parameters are editable live from the **Settings** panel.
3. Electrolysis power stays clamped to 10% at runtime to protect the electrodes.
