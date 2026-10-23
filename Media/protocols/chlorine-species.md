---
state: authored
author: [claude-sonnet-5.5]
checked: []
reviewed: []
authorised:
source_type: external
description: "Free and combined chlorine in spent medium (DPD)"
sources:
  - https://hach.com/p-chlorine-free-and-total-reagent-sets/2459500
  - https://www.nemi.gov/methods/method_summary/7431
  - https://www.epa.gov/system/files/documents/2024-02/dbp-rules-methods-table.pdf
  - https://cdn.hach.com/7FYZVWYB/at/nb4wq78sqgvm2wgfhxcp4vx4/DR_4000_Chlorine-Free_Method_10102.pdf
  - https://blog.hannaservice.eu/false-free-chlorine-readings/
  - https://www.gov.nl.ca/ecc/files/waterres-training-adww-2014-16-marcphilippe-camara.pdf
created: 2026-10-21
recorded_at: 2026-10-21
cssclasses: [trust-authored]
tags: [electropioreactor, protocol, chlorine, chloramine, DPD, chemistry]
---

# Free and combined chlorine in spent medium (DPD)

The anode oxidises some chloride in the medium to free chlorine (HOCl/OCl⁻). The ammonium in the medium reacts with it to give monochloramine. This protocol measures how much free and how much combined chlorine is present in spent UdG phosphate medium after 24 hours of abiotic electrolysis, so the model's monochloramine lifetime can be checked.

Current baseline: ed04, MMO tube assembly, *Xanthobacter tagetidis*, chloride-free AM003, 30 °C; read Summary D21/D22 and predictions with those selections. This assay retains its historical objective: spent chloride-bearing UdG after abiotic electrolysis. The UdG/Pt–Ti/25 °C conditions below are historical comparison conditions only. Before executing that comparison, the owner must specify and record its medium, hardware, temperature, power and schedule and the matching model selections. An AM003 oxidant screen is a separate measurement, not a substitute for the UdG monochloramine-lifetime assay.

## Optimal protocol

Best accuracy: a DPD photometer or the DPD ferrous titration.

### Kit

- Either (a) a DPD colorimeter or photometer with matched sample cells (for example a Hach pocket colorimeter or benchtop unit using the free-chlorine and total-chlorine DPD powder pillows, range about 0.02 to 2.00 mg/L as Cl₂ for a 10 mL sample), or (b) the DPD ferrous ammonium sulphate (FAS) titration of Standard Methods 4500-Cl F, with its burette or titrator, DPD indicator, phosphate buffer and standardised FAS titrant.
- Two matched sample cells reserved for this work: one marked FREE, one marked TOTAL. Do not swap them, because traces of iodide from the total-chlorine reagent carried over into the free-chlorine cell give a false free reading when monochloramine is present.
- A set of identical vials, each run for 24 h, so that each gives a separate sample (see the method). Use at least 3, plus 1 blank vial (same medium, same stirring and pulses, no current).
- Disposable 1 mL and 5 mL pipettes and tips, or calibrated glass pipettes. A small volumetric flask or measuring cylinder for dilutions.
- A timer.
- The reactor controller and electrodes used in the main experiments, in the same vial geometry.
- Nitrile gloves and eye protection.

### Reagents

- Fresh UdG phosphate medium made with the CaCl₂ and NH₄⁺ at the normal recipe concentrations. Record the exact masses and which CaCl₂ (anhydrous or dihydrate) was used.
- DPD free-chlorine and DPD total-chlorine reagents from the same supplier as the photometer, in date, kept dry. For the titration route: DPD indicator, phosphate buffer, potassium iodide crystals (for total) and standardised ferrous ammonium sulphate titrant.
- Chlorine-demand-free water for dilutions. Use laboratory deionised water and check it first: a 10 mL portion plus the DPD reagent must read zero. If it does not, use fresh deionised water or a different source.
- Optional: sodium arsenite and potassium iodide for the manganese correction (see Interferences). Sodium arsenite is toxic and its waste is hazardous: only use it if manganese is a problem.

### Method

1. Record the day's settings: the Summary reactor and medium, pulse duration and interval, power (3 %), stirring (1000 rpm), temperature (25 °C), and the CaCl₂ form used.
2. Prepare the vials. Fill each test vial with 15 mL medium and the blank vial with 15 mL of the same medium. Fit the electrodes, cap, sparge line and vent exactly as in service.
3. **Safety.** With no cells, the headspace is potentially flammable (see [abiotic-do-trace.md](abiotic-do-trace.md), step 5). Run in a ventilated area away from ignition sources, do not block the vent, and switch the current off before opening any vial. An owner-approved gas-clearance procedure and acceptance criterion are prerequisites before opening or handling; elapsed intervals or routine CO₂ pulses alone do not establish clearance. Free chlorine and chloramine are irritants: work in a ventilated place and avoid breathing the headspace when you open a vial.
4. Run electrolysis at 3 % power with the CO₂ pulse schedule, stirring at 1000 rpm and 25 °C for 24 hours. Run the blank vial with the pulses and stirring but no current, so you see what the medium and the reagent give on their own. For a time course, also run extra vials and stop them at 6 h and 12 h; this tells you whether the combined chlorine has reached a plateau (step 13).
5. Stop the vial at 24 h. Switch off the current first. Uncap only after the approved gas-clearance criterion is met; waiting one interval is not clearance. Record the delay and any clearance-related sample change because chlorine can decay during it. Start the timer. Sample immediately: chlorine species decay and react with the glass and the air, so every minute counts. Do not store, freeze or acidify the sample.
6. Dilute because the vial is small. A standard photometer reading uses a 10 mL sample, which is two-thirds of the vial. Take 5 mL of spent medium with a pipette and make up to 10 mL in a clean dry cell with chlorine-demand-free water (a 1 + 1 dilution, factor 2). Do the same in the second cell. Keep the pipette tip below the surface and do not shake or stir vigorously, since this strips chlorine. Write down the dilution factor you used. If the first reading is above the top of the range, dilute further and repeat from a fresh portion; if it is below range after dilution, use a sufficiently sensitive validated method or report the dilution-adjusted reporting limit. Pooling can supply volume and avoid dilution but does not concentrate an undiluted sample.
7. Free chlorine first. In the FREE cell add the DPD free-chlorine reagent, swirl gently for the time in the reagent's instructions (usually about 20 seconds), and read within one minute. A longer wait lets monochloramine react slowly with the DPD and gives a false high free reading.
8. Total chlorine second, using a separate portion in the TOTAL cell. Add the DPD total-chlorine reagent (which contains iodide), swirl, wait the time in the reagent's instructions (typically 3 minutes), and read. Do not use the same cell as for free.
9. Zero the instrument with a portion of the same sample before the reagent is added, as the instrument manual tells you, so that the colour of the medium does not count. Also read the blank vial (no current) by the same steps; subtract its readings if they are above zero.
10. Calculate. Multiply each reading by the dilution factor to get mg/L as Cl₂ in the vial.
    - Free chlorine = the free reading × dilution factor.
    - Total chlorine = the total reading × dilution factor.
    - Combined chlorine = total minus free. Monochloramine is expected to be most of it.
11. Titration route instead of the photometer (Standard Methods 4500-Cl F): to a measured sample volume add buffer and DPD indicator, titrate with FAS until the red colour just disappears (this is free chlorine). Add a few crystals of potassium iodide and continue the titration to the next colourless end point; the total titrated is total chlorine, and the difference is combined. The titration needs a larger sample than the vial gives, so pool vials or scale down the volumes as the method allows, and record the volumes used.
12. Replicates: at least 3 vials at 24 h. Report the mean and spread of free, total and combined chlorine.
13. Plateau check. If you ran the 6 h and 12 h vials, plot combined chlorine against time. A steady combined concentration needs the 12 h and 24 h values to agree; if the values are still rising, the 24 h figure is a lower bound and the lifetime derived from it is also a lower bound. Say so in the notes.
14. Confirm the CaCl₂ form. Read the bottle label and certificate for the CaCl₂ used in the medium: anhydrous CaCl₂ is 110.98 g/mol, dihydrate is 147.01 g/mol. If the model assumes one form and the bottle holds the other, every chlorine figure is off by about 24 %. Tell the model owner which form was used. To check an unlabelled bottle, weigh about 2 g in a tared dish, heat at 200 °C for 2 hours, cool in a desiccator and re-weigh; a mass loss of about 24.5 % (arithmetic from the molar masses) matches the dihydrate, about 0 % the anhydrous salt (which is hygroscopic, so some small loss is possible), and about 49 % the hexahydrate. Record the result.
15. Record the numbers in the run notes (see below). The workbook is not edited by this protocol.

## Budget protocol

A DPD test kit or strips, accepting a coarser reading.

### Kit

- A DPD comparator or photometer with suitable free- and total-chlorine ranges. Select the range using the raw free and combined concentrations, not Summary D30 (res_Cl2): that Summary value is a toxicity-weighted effective index, not a DPD concentration. If a result is below range, report its limit or use a sufficiently sensitive validated method. Pooling increases volume, not concentration.
- The same vials, pipettes and timer as above.

### Reagents

- As above for the medium; DPD tablets or strips within date; chlorine-demand-free water.

### Method

1. Follow steps 1 to 5 of the optimal route for the settings, vials, safety and sampling.
2. Fill the test tube of the comparator to its mark with undiluted spent medium if the kit needs a volume that your vials can supply (use two vials in turn for free and total), or dilute 1 + 1 if the vial is short. Write down the dilution factor.
3. Free chlorine: add one DPD No. 1 tablet (or dip the free pad), crush and mix gently, and read the colour against the scale within one minute. Do not wait.
4. Total chlorine: in a fresh tube, add a DPD No. 1 tablet then a DPD No. 3 tablet (or dip the total pad), mix and wait the time the kit says (typically 2 minutes), and read.
5. Combined = total minus free. Multiply by the dilution factor.
6. Read a blank vial (no current) the same way, and note any colour. Repeat for at least 3 vials. Because the colour match is by eye, state in the notes that each reading is good to about one scale step.
7. Confirm the CaCl₂ form as in step 14 of the optimal route.
8. Treat strips and comparators as screens unless their validated sensitivity and interference control resolve the raw free/combined concentrations of interest. Do not infer a monochloramine lifetime from a below-range result.

## Sample handling and interferences

- Measure immediately. Free chlorine and chloramines decay on standing, in light, in warm vials and by reaction with the container, and DPD readings for free chlorine drift upwards with time if monochloramine is present.
- Use clean glass cells that have never held strong oxidant or iodide. Rinse with chlorine-demand-free water and check that a blank gives zero.
- Oxidised manganese gives a false positive for both free and total chlorine. UdG medium has trace manganese; the correction is to adjust the pH to 6 to 7, add potassium iodide, then sodium arsenite, test this treated portion and subtract its reading from the untreated one. Only use this if a blank vial (no current) reads positive. The arsenite waste is hazardous.
- Monochloramine causes a positive error on the free-chlorine reading that depends on time, temperature and the ratio of chloramine to free chlorine. Read at the stated time and no later. Arsenite and iodide do not remove it.
- Other oxidants, including hydrogen peroxide (a cathodic product of oxygen reduction at the electrodes) and any other halogen-type oxidant, may also give a colour with DPD. A blank (no current) separates the medium; to see if peroxide contributes, measure a deliberately peroxide-spiked blank on the same instrument and compare. Report the measurement as "DPD-active oxidant as Cl₂" rather than as chlorine alone if you cannot exclude it.
- Colour and turbidity in the sample: zero the instrument on the sample first. Cells or debris (when this is repeated with a culture) will stain and consume chlorine, so this protocol is for the abiotic medium only.
- The pH of the DPD buffer is set for the reagent; the phosphate medium is close to that, but a heavily acidified sample from CO₂ pulses may need the reagent's pH check. Follow the supplier's instructions if the reagent colours incorrectly.
- Dilution lowers concentration and hence the reading; for a small vial, use accurate pipettes and keep the diluent chlorine-demand-free. Dilute immediately before reading.

## What the spreadsheet does with it

Enter the result in the **Monochloramine lifetime** section of the Calibrations tab (rows 155–162); otherwise this protocol does not edit the workbook. Compare the numbers with two model quantities:

- The monochloramine lifetime `tau_NH2Cl` is Chemistry!D142. It sets how much free chloride the chloramine ties up, and so how much chlorine the anode can make. Across 1 min to 5 h it moves the UdG headline CO₂ interval from 9.4 to 7.6 min against 8.1 min at the 1 h default (about +15 %/−7 %).
- Compare measured combined chlorine (mg/L as Cl₂) with Chemistry D143 (NH2Cl_mgL, on the HOCl mass basis) multiplied by Chemistry D223/D222 (M_Cl2/M_HOCl). Compare free chlorine separately with Chemistry D140 converted by the same mass ratio and divided by Chemistry D104 (pH_fHOCl): D140 is HOCl alone, whereas free DPD reads HOCl + OCl⁻ (at UdG's pH the hypochlorite adds about 7 %, more as pH rises). Summary D30 (res_Cl2) is C_eff_Cl2, which discounts monochloramine by its relative potency and adds an enrichment-weighted free term; it is not the raw DPD assay prediction. The old ~0.34 mg/L UdG example was this effective index and must not set an assay range or lifetime.

To turn the measurement into a lifetime, invert the model's own steady state rather than dividing by a production rate. The model holds combined chlorine at B = min(C·kτ/(1+kτ), P·τ): C is the chloride pool (Chemistry D47, mol/L), k the anodic chloride turnover (Chemistry D271, 1/s) and P the efficiency-limited chlorine production (Chemistry D315, mol/L/s). None of the three depends on τ, so read them with the Summary set to the run's reactor, electrode, medium, power, rpm and temperature (do not use Chemistry D134, which itself moves with τ). Both terms rise with τ, so τ = max(B/(k(C − B)), B/P), with B the plateau as mol/L Cl₂-equivalent (mg/L as Cl₂ ÷ 70 906 mg/mol, Calibrations D198). On the Calibrations tab (rows 155–162) enter Reactor, Medium (the medium the run used, e.g. UdG phosphate), the plateau combined chlorine in mg/L as Cl₂, and k, C and P; the tab computes τ in hours (column I), or says the plateau is not invertible when it reaches the chloride pool. A plateau set by the ammonium nitrogen capacity (Chemistry D312 not OK) does not determine τ either; leave such a run excluded. Set Include = `y` only once a reviewer has agreed the plateau and the three readings. The mean of the included runs for the selected reactor and medium (Calibrations D163, `cal_tau_NH2Cl`) then replaces the default in Chemistry D142 (`tau_NH2Cl`); the default stays in Chemistry D314. A run in one medium is never applied to another: AM003 is chloride-free, so a UdG result is used only while the Summary medium is UdG phosphate. Do not overwrite D142 by hand.

A second check: if the CaCl₂ is the other hydrate from the one the model assumes, every chlorine figure moves by about 24 % (anhydrous 110.98 g/mol against dihydrate 147.01 g/mol). Fix this before reading the lifetime from the data, otherwise a chloride error is read as a lifetime error.

## Principle & background

DPD (N,N-diethyl-p-phenylenediamine) is oxidised by free chlorine to a magenta product, which a photometer reads at about 530 nm. Without iodide, only free chlorine reacts quickly. With iodide added, combined chlorine (chloramines) also liberates iodine that colours the DPD, so the second reading is total chlorine. Combined chlorine is therefore total minus free. Monochloramine is expected to dominate the difference here, because the medium carries ammonium and the pH sits near neutral, which favours monochloramine over the dichloramine and trichloramine forms at the chlorine-to-nitrogen ratios the electrolysis produces.

The measurement matters because the model treats the free chlorine as being mostly mopped up by ammonium, so the standing free-chlorine level is low and the combined level is longer-lived. How long monochloramine lasts is the model's `tau_NH2Cl`; it controls how much chloride is tied up in the recycled pool and so the free chloride share available to the anode. A measured steady combined chlorine, inverted through the same steady state the model uses (see above), gives that lifetime.

Results are reported as mg/L as Cl₂ (the DPD convention), the same convention the model uses for its Cl₂-equivalent figure.

## Sources

- DPD free and total chlorine reagents, range and method numbers: [Hach, Chlorine (Free and Total) Reagent Set, DPD, 10 mL](https://hach.com/p-chlorine-free-and-total-reagent-sets/2459500).
- DPD colorimetric method summary (Standard Methods 4500-Cl G): [NEMI method summary](https://www.nemi.gov/methods/method_summary/7431).
- Standard Methods 4500-Cl F (DPD ferrous titrimetric) as an approved disinfectant-residual method: [US EPA, disinfection byproduct rules methods table](https://www.epa.gov/system/files/documents/2024-02/dbp-rules-methods-table.pdf).
- Manganese correction and chloramine interference with free chlorine (use dedicated free and total cells): [Hach DR 4000 procedure, Chlorine, Free, Method 10102](https://cdn.hach.com/7FYZVWYB/at/nb4wq78sqgvm2wgfhxcp4vx4/DR_4000_Chlorine-Free_Method_10102.pdf); [Hanna Instruments, False free chlorine readings](https://blog.hannaservice.eu/false-free-chlorine-readings/).
- Split-sample interference treatment and combined chlorine by subtraction: [Newfoundland and Labrador water resources training, DPD chlorine analysis](https://www.gov.nl.ca/ecc/files/waterres-training-adww-2014-16-marcphilippe-camara.pdf).
