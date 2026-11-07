---
title: How it works
description: The electroPioreactor end to end, from the Pioreactor base to the vial cap, in-culture electrolysis, CO₂ sparging and the plugin that runs it.
section: learn
audience: newcomer
order: 20
---
The electroPioreactor is a small glass vial of liquid culture sitting on a Pioreactor base. Two electrodes split a little of the culture's water into hydrogen and oxygen for the bacteria to use, and a timed puff of carbon dioxide (CO₂) gives them carbon. The Pioreactor stirs, heats, measures growth and pumps fresh medium in, all on its own.

This page follows the Aseptic electroPioreactor, version AEP0.2. The [3D model on the home page](/) names each part when you hover over it, and its Tour walks through them in order.

![The AEP0.2 vial with its one-piece cap, needles, electrodes, sensors and heater](/img/vial-cap-a4-white.png)

## The big picture

1. **The base** is a [Pioreactor](https://pioreactor.com): a Raspberry Pi computer with a circuit board (the HAT) that stirs the vial, heats it, shines light through it to measure growth, and runs pumps and valves. <!-- source: docs/glossary.yaml (HAT, PWM channel) -->
2. **The vial** holds 30 ml of culture medium: water with dissolved minerals, and the bacteria. <!-- source: Components/Vial Cap/render/callouts.mjs (medium) -->
3. **The vial cap** holds two electrodes and several needles, and seals the vial.
4. **Electricity** through the electrodes makes hydrogen (H₂) and oxygen (O₂) inside the culture.
5. **CO₂** from a SodaStream cylinder is fed down the inside of one electrode in short, timed bursts.
6. **The electroPioreactor plugin**, software on the Pioreactor, runs the electrolysis and the CO₂ and pauses the growth readings so bubbles do not spoil them.

## Inside the vial, part by part

### The culture

**Culture medium, 30 ml.** Hydrogen-oxidising bacteria (HOB) fix CO₂ using the H₂ and O₂ made in the culture. The medium is also the electrolyte that carries the current between the electrodes, so its recipe avoids salts, such as chlorides, that electrolysis would turn into chlorine or other harmful products. See [Media](/media/). <!-- source: callouts.mjs (medium); Media/MediaFormulation.md (Background) -->

**Magnetic stir flea.** A small PTFE-coated magnetic bar (15 × 6 mm in the AEP0.2's 40 ml vial) on the bottom of the vial, spun by a magnet in the base. It keeps the culture mixed and the gases dissolving. <!-- source: callouts.mjs (flea); docs/components/stir-bar.yaml -->

### The cap

**One-piece vial cap.** 3D-printed in PC-CF (polycarbonate filled with carbon fibre). One silicone septum seals the vial, both electrodes and every port, and the cap sets how deep the electrodes reach. <!-- source: callouts.mjs (cap); docs/components/vial-cap.yaml -->

A **septum** is a soft rubber-like disc that a needle can pass through and that closes up again when the needle is removed. Here it is a 2 mm silicone disc under the cap. <!-- source: docs/glossary.yaml (septum) -->

**Knurled thumb screws.** Clamp the power leads to the electrodes: red to the anode, black to the cathode. <!-- source: callouts.mjs (screws) -->

> **Safety:** The leads must never be swapped. Wired the wrong way round, the stainless steel cathode corrodes quickly and releases chromium, nickel and iron into the culture. <!-- source: docs/steps/step-07-set-up-electrolysis.md (safety) -->

### Making hydrogen and oxygen: the electrodes

Passing an electric current through water splits it. This is **electrolysis**: hydrogen forms on the negative electrode (the cathode) and oxygen on the positive one (the anode), two molecules of hydrogen for every one of oxygen. That is why you see about twice as many bubbles on the cathode. <!-- source: docs/glossary.yaml (electrolysis, cathode); docs/steps/step-08-test-electrolysis.md (bubble check) -->

**Cathode: 316 stainless steel.** Electrolysis makes fine H₂ bubbles here, the bacteria's energy source. <!-- source: callouts.mjs (cathode) -->

**Anode: hollow MMO-coated titanium.** A titanium tube coated with mixed metal oxide (MMO, iridium and tantalum oxides), which resists the harsh conditions where oxygen forms. Electrolysis makes O₂ on its surface. CO₂ is fed down its bore. <!-- source: callouts.mjs (anode); docs/glossary.yaml (MMO anode) -->

The electrodes are powered from one of the Pioreactor's LED outputs (channel D). The plugin limits this to at most 10 % power, to protect the electrodes. <!-- source: AEP-Plugin/README.md; docs/steps/step-08-test-electrolysis.md (safety) -->

### Feeding carbon: CO₂ sparging

**Sparging** means bubbling a gas through a liquid. CO₂ flows from a SodaStream cylinder through a pressure regulator, an electric valve (a solenoid) and a fine needle valve, then through a sterile filter and down the hollow anode. <!-- source: docs/glossary.yaml (regulator, solenoid valve, needle valve, sparging); docs/steps/step-13-admit-co2.md -->

**CO₂ bubbles.** Rise from the anode's open base, supplying carbon and sweeping O₂ bubbles off the anode. <!-- source: callouts.mjs (co2) -->

The CO₂ comes in short bursts on a timer, not as a steady stream. Early tests with continuous sparging found that the bubbles spoilt the growth readings and that the low flow made it hard to clear oxygen from the anode. Timed bursts let the plugin pause the readings around each burst. <!-- source: AsepticElectroPioreactor/CARMA_PumpPriming/Results/AEP0.1 Training/README.md (Sparging) -->

> **Expert:** How long and how often to sparge depends on how much oxygen the electrodes make, how fast it leaves the liquid, and the medium's pH. The [gas model](/gas-model/) works out a schedule for a given reactor, organism and medium.

### Letting gas out

**Gas outlets.** Two bent needles vent spent gas from above the liquid. Each carries a 0.2 µm vent filter, so gas can leave but microbes cannot get in. <!-- source: callouts.mjs (gas); docs/steps/step-13-admit-co2.md (items 5 and 6) -->

### Medium in and out

**Media In and Media Out needles.** Blunt 16 G (about 1.6 mm) stainless steel needles through the septum. Fresh medium is pumped in. The Media Out tip sets the 30 ml level and removes culture as the Pioreactor doses. <!-- source: callouts.mjs (needles) -->

Two peristaltic pumps move liquid between the vial and two bottles: one of fresh medium, one for the product (the culture that is taken out). A peristaltic pump squeezes flexible tubing with rollers, so the liquid never touches the pump. <!-- source: docs/steps/step-09-set-up-nutrient-solution-flow.md; docs/glossary.yaml (peristaltic pump) -->

The Pioreactor can run them as a **turbidostat**: when the culture gets cloudier than a set point, it adds fresh medium, and the Media Out needle removes the same amount of culture. That holds the culture at a steady density so it can keep growing. Batch and chemostat modes are possible too. <!-- source: docs/glossary.yaml (turbidostat); MixedElectroPioreactor/Operation.md (modes) -->

**Inoculation port.** A syringe goes straight through the self-sealing silicone septum. This is how the bacteria are added. <!-- source: callouts.mjs (port) -->

### Measuring growth

As bacteria multiply, the culture gets cloudier. The Pioreactor measures this cloudiness as **optical density (OD)**.

**IR LED and light path.** Infrared light crosses the culture below the electrodes (drawn in red on the model; invisible in life). <!-- source: callouts.mjs (led) -->

**Photodiodes (Pioreactor XR).** Read scattered infrared light at 45°, 90° and 135°, plus a reference, to track growth as optical density. The XR upgrade adds the extra angles for a lower detection limit. <!-- source: callouts.mjs (pd); docs/glossary.yaml (XR upgrade kit) -->

Bubbles scatter light too, so the plugin pauses OD readings around each CO₂ burst and resumes them once the bubbles have cleared. If electrolysis is set to run in on/off cycles rather than continuously, it also pauses OD during each on phase and reads in the gaps. <!-- source: AEP-Plugin/README.md -->

### Keeping it warm

**Heater PCB.** An aluminium-core heater under the vial holds the set temperature. <!-- source: callouts.mjs (heater) -->

**Precision temperature sensor.** An MLX90632 infrared thermometer reads the culture through the glass, without contact. <!-- source: callouts.mjs (temp) -->

## Keeping it aseptic

"Aseptic" means free of unwanted microbes. For research on a single strain, nothing else must get in. The AEP does this in three ways: <!-- source: AsepticElectroPioreactor/README.md -->

- **Filters on every gas path.** 0.2 µm hydrophobic vent filters on the CO₂ inlet, both gas outlets and the vent of each medium bottle. Gas passes; microbes and liquid do not. <!-- source: docs/glossary.yaml (vent filter); docs/steps/step-09, step-13 -->
- **Sealing.** One septum seals the vial, the electrodes and every port. Needles go through it, and it closes behind them.
- **Autoclaving.** The design aims for parts that can be sterilised by autoclaving (steam under pressure). <!-- CHECK: AsepticElectroPioreactor/README.md claims autoclave-ability, but the AEP0.2 sterilisation procedure (docs/steps/step-17-sterilise.md) is still awaiting PI approval, and the repo does not say which parts are autoclaved -->

> **Note:** The AEP0.2 sterilisation procedure is still awaiting approval. See the [Sterilise step](https://docs.electropioreactor.org/AEP/step-17-sterilise/) of the build guide for its current state.

## The software

The [electroPioreactor plugin](/software/) adds one job, **electroPioreactor**, to the Pioreactor's web interface. It: <!-- source: AEP-Plugin/README.md -->

- drives electrolysis at a set power, continuously or in on/off cycles;
- opens the CO₂ valve for a set time at a set interval;
- pauses electrolysis during each CO₂ burst;
- pauses OD readings around each CO₂ burst, and around electrolysis when it runs in cycles.

Everything else, stirring, heating, OD, dosing, is the standard Pioreactor software. All its timing and power settings can be changed live from a web browser; only the choice of electrode channel needs a restart.

## Why electrolysis inside the culture?

Hydrogen is flammable, and stored or piped hydrogen needs special handling. Making it in the culture means: <!-- source: AsepticElectroPioreactor/README.md (Why an AEP?) -->

- **No hydrogen cylinder.** Hydrogen and oxygen are made only as needed, a little at a time, and dissolve straight into the medium where the bacteria use them.
- **Low voltage.** The electrodes run at a few volts from the Pioreactor's own supply. <!-- source: docs/steps/step-08-test-electrolysis.md (about 2.8 to 3.05 V at 3.5 %) -->
- **The CO₂ also clears oxygen.** Each CO₂ burst sweeps oxygen bubbles off the anode and out of the vial, which helps keep the gas above the liquid away from flammable mixtures. <!-- source: Media/MediaFormulation.md (Macronutrients: CO₂ purge rate set with O₂ accumulation and hydrogen combustion risk reduction in mind) -->

The idea is not new: researchers grew HOB this way in the 1960s, partly for life support in space, and several groups use it today. See [Research](/research/). <!-- source: Literature bib (1964 continuous culture apparatus for closed-cycle space systems; 1965 Electrolysis-Hydrogenomonas life support; 1965 and 1967 Hydrogenomonas papers) -->

## Where next

- [What we have learned](/lessons/): the lessons behind the design.
- [Specifications](/specifications/): sizes, materials and electrical details.
- [Variants](/variants/): AEP, MEP and the budget aseptic version.
- [Get one](/get-one/): buy a kit or build your own.
- [Build guide](https://docs.electropioreactor.org/AEP/): the full step-by-step assembly instructions.
