---
title: Glossary
description: Plain-language definitions of the terms used across the electroPioreactor site and build guide.
section: learn
audience: everyone
order: 40
---
Plain-language definitions of the terms used on this site and in the [build guide](https://docs.electropioreactor.org/AEP/), in alphabetical order. The build guide shows these same definitions as tooltips. <!-- source: docs/glossary.yaml, plus terms used on the learn pages -->

## A

**AEP**: Aseptic electroPioreactor: the version for single-strain research, with vent filters on every gas path and a septum-sealed cap so no other microbes get in. The current version is AEP0.2. [More](/variants/)

**aseptic**: Free of unwanted microbes. Aseptic equipment and technique keep a culture to the one organism you put in.

**autoclave** (also: autoclaving): A pressure vessel that sterilises equipment and liquids with hot steam under pressure.

**autotroph** (also: autotrophic, autotrophically): An organism that builds its own body from CO₂. Plants are autotrophs powered by light; HOB are autotrophs powered by hydrogen.

## B

**BAEP**: Budget aseptic electroPioreactor: an MEP with the AEP's five 0.2 µm vent filters added to every gas path. [More](https://docs.electropioreactor.org/BAEP/)

**batch culture** (also: batch): Growing a culture on one fixed fill of medium, with no liquid added or removed. In the electroPioreactor the gases are still fed, so strictly it is fed-batch.

**blanking plug**: A 1/8" threaded plug that seals the solenoid's unused right port. It seals on its own o-ring, so it needs no sealant.

**bootfs**: The small boot partition of the flashed microSD card, and the only part a Mac or PC can open. The card bundle's files go here.

## C

**captive nut**: A nut held in a pocket in the printed part, so a bolt can be tightened into it with one tool.

**card bundle**: A zip from the electroPioreactor releases page. Copied onto the card's bootfs drive, it installs the plugins and sets the model on first boot.

**cathode**: The negative electrode: a stainless steel rod. Hydrogen forms on it, so it shows about twice the bubbles of the anode. It must never be wired as the anode.

**chemostat**: A dosing mode that adds fresh medium and removes culture at a fixed rate. Cells either grow fast enough to keep up, reaching a steady state, or wash out.

***Cupriavidus necator***: The best-studied hydrogen-oxidising bacterium. Older papers call it *Ralstonia eutropha* or *Hydrogenomonas*.

## D

**DI water**: Deionised water: water with its dissolved ions removed. Used here to set the vial level by weight, 1 g per ml.

**dovetail**: The sliding joint that locks the printed platforms into one raft. A male dovetail on one platform drops into the female slot on the next.

## E

**electrode**: A conductor through which electric current enters or leaves the liquid. The electroPioreactor has two: the anode and the cathode.

**ElectrodeTopStop**: The printed block that sits on top of the MEP's O-ring vial cap. It holds both electrodes parallel and clamps each cable's ring terminal to its electrode with an M3 bolt through a captive nut.

**electrolysis**: Splitting water with an electric current: hydrogen at the cathode, oxygen at the anode. It supplies the hydrogen the HOB grow on.

**electrolyte**: A liquid that conducts electricity because it contains dissolved ions. Here the culture medium is also the electrolyte.

**enrichment**: Growing a mixed sample, such as soil or river water, under conditions that favour the microbes you want, so they come to dominate. [In the repo](repo:Methodologies/)

**eye-spy**: A small Pioreactor sensor board that reads light from the vial. The eye-spys are chained together with STEMMA-QT wires.

## F

**ferrule**: The ring inside a compression fitting. Tightening the nut squeezes it onto the tube to make a gas-tight seal.

**FZone**: The MEP's budget CO₂ regulator. Its outlet pressure is fixed, so the needle valve alone sets the CO₂ flow. Left gauge: cylinder pressure; right gauge: pressure reaching the solenoid.

## G

**gas model**: AMYBO's spreadsheet model of the gases in the vial. It works out a CO₂ sparging schedule for a given reactor, organism and medium. [More](/gas-model/)

**GL45**: A standard 45 mm screw thread on lab bottles such as Duran. The media and product bottles and their multi-port caps use it.

## H

**HAT**: The Pioreactor circuit board that plugs onto the Raspberry Pi's pin header. It carries the PWM and LED outputs and the 12V barrel jack. HAT stands for Hardware Attached on Top.

**heterotrophically** (also: heterotrophic): Growing on organic carbon, such as sugars, instead of on hydrogen and CO₂. A quick way to check a HOB culture is alive before it goes into the reactor.

**HOB**: Hydrogen-oxidising bacteria: microbes that grow on hydrogen and CO₂. The electroPioreactor is built to grow them as a sustainable protein source.

**hostname**: The unit's network name, chosen when flashing the card. Its web interface is then at http://hostname.local. [Pioreactor docs](https://docs.pioreactor.com/user-guide/zeroconf-networking)

## I

**inoculum** (also: inoculate, inoculation): The starter culture of bacteria added to fresh medium. Adding it is inoculation; in the AEP it goes in by syringe through the septum.

**IR**: Infrared: light just beyond red, invisible to the eye. The Pioreactor measures optical density with an infrared LED.

## J

**John Guest push-fit** (also: push-fit): A push-in tube fitting: push the tube in and it grips and seals. The regulator's outlet port comes with one, which this build unscrews and replaces with the reducer.

**journal bore**: The close-fitting hole in the vial cap's column that each electrode seats in. The column height sets how far the electrode reaches into the vial.

## K

**KegLand adapter**: The cylinder-to-regulator adapter (KegLand KL15578). Back its pin off while making the joint, then screw the pin in to let gas through.

**Knallgas bacteria**: An older name for hydrogen-oxidising bacteria. Knallgas, German for "bang gas", is a mixture of hydrogen and oxygen.

## L

**leader**: The Pioreactor that hosts the web interface and config.ini for a cluster. A single stand-alone unit is its own leader (Leader + Worker).

**LED channel D** (also: LED D): One of the HAT's four LED outputs, A to D. The electroPioreactor job drives the electrodes from channel D, clamped to 10% power.

**local access point** (also: access point, hotspot, own Wi-Fi): The leader makes its own Wi-Fi network, pioreactor (password raspberry). Use it where you cannot add devices to the site Wi-Fi. [Pioreactor docs](https://docs.pioreactor.com/user-guide/local-access-point)

**Loctite 577** (also: thread sealant, anaerobic thread sealant): An anaerobic thread sealant: it cures only without air, inside a tightened thread. Fixtures in 10 to 60 minutes at 22 °C; full pressure after 24 hours.

**luer lock** (also: luer, luers, male luer, female luer): A standard medical screw fitting. A male luer (the spigot) screws into a female luer (the socket). In this build, male ends mark outlets.

## M

**manual override** (also: solenoid override): The dial on the front of the solenoid. 0 is normal (closed without power); 1 holds the valve open.

**medium** (also: culture medium, nutrient solution): The liquid the bacteria grow in: water with dissolved minerals. In the electroPioreactor it is also the electrolyte. AMYBO media are numbered AM001, AM002, AM003. [More](/media/)

**MEP**: Mixed-culture electroPioreactor: the lower-cost version for mixed cultures, built on the Pioreactor 20 ml with an O-ring vial cap. [More](/variants/)

**mixed culture**: A culture of several kinds of microbe growing together, such as a community enriched from a natural sample.

**MMO**: Mixed metal oxide: a hard-wearing coating, here of iridium and tantalum oxides (IrO₂-Ta₂O₅) on titanium, used for the anode because it resists the conditions where oxygen forms.

**MMO anode** (also: anode): The positive electrode: a titanium tube coated with mixed metal oxide (IrO₂-Ta₂O₅). Oxygen forms on it, and CO₂ flows down its bore into the vial.

**monoculture** (also: single strain): A culture of one strain of one organism, with nothing else growing in it.

## N

**needle valve**: A fine-adjustment valve on the solenoid's front port. It sets how fast CO₂ flows; turn clockwise to close.

## O

**OD**: Optical density: how cloudy the culture is, read from scattered light. It tracks cell growth. [Pioreactor docs](https://docs.pioreactor.com/user-guide/calibrate-od600)

**OD600**: Optical density at 600 nm, the standard laboratory measure of culture cloudiness on a spectrophotometer. Pioreactor OD readings can be calibrated against it.

## P

**PC-CF**: Polycarbonate filled with carbon fibre: the stiff, heat-resistant 3D printing material of the AEP0.2 vial cap.

**peristaltic pump**: A pump that squeezes liquid along flexible tubing with rollers, so the liquid never touches the pump. [Pioreactor docs](https://docs.pioreactor.com/user-guide/using-pumps)

**photodiode**: A light sensor. The Pioreactor's photodiodes read infrared light scattered by the culture to measure optical density.

**Pioreactor**: An open, low-cost bench-top bioreactor built on a Raspberry Pi. It stirs, heats, measures optical density and runs pumps. The electroPioreactor is built on it. [More](https://pioreactor.com)

**plugin** (also: electroPioreactor plugin): Add-on software for the Pioreactor. The electroPioreactor plugin adds one job that runs electrolysis and CO₂ sparging and pauses OD readings around each sparge (and around electrolysis when it cycles). [More](/software/)

**PPE**: Personal protective equipment, such as eye protection, gloves and a lab coat.

**precision temperature plugin** (also: pioreactor-precision-temperature-plugin, temperature plugin): The Pioreactor software plugin that runs the Precision Temperature Upgrade Kit's sensor. The AEP card bundle installs it; the MEP bundle has none.

**Precision Temperature Upgrade Kit** (also: Precision Temperature kit, temperature kit): An optional Pioreactor kit. Its MLX90632 far-infrared sensor reads the vial's temperature without contact, replacing the thermistor. [Pioreactor docs](https://docs.pioreactor.com/user-guide/precision-temperature-upgrade-kit)

**PWM channel** (also: PWM): One of the HAT's five switched power outputs. In this build: 1 stirring, 2 media pump, 3 waste (product) pump, 4 CO₂ solenoid (relay), 5 heating. PWM stands for pulse-width modulation.

## R

**Raspberry Pi**: The small single-board computer inside every Pioreactor. AEP0.2 uses a Raspberry Pi 5.

**Raspberry Pi Imager** (also: Imager): The free Raspberry Pi app that writes the Pioreactor operating system image onto the microSD card. [Pioreactor docs](https://docs.pioreactor.com/user-guide/software-set-up)

**reducer** (also: reducing nipple): The 1/4" BSP to 1/8" BSP hexagon nipple that joins the regulator outlet to the solenoid valve.

**REF** (also: REF position): The reference photodiode position on the vial holder (photodiode channel 1=REF in config.ini). Its eye-spy is the white-marked one.

**regulator**: Drops the cylinder's pressure (about 60 bar when full) to a working pressure, about 1 bar here. Its flathead screw fully anti-clockwise is closed.

## S

**self test**: Pioreactor's built-in hardware check, run from the unit's Manage screen. It confirms each part of the unit responds. [Pioreactor docs](https://docs.pioreactor.com/user-guide/pre-flight-hardware-check#step-1-run-a-self-test)

**septum**: The 2 mm silicone disc in the vial cap. It seals the vial mouth, both electrodes and every needle port, and self-heals needle holes.

**shunt** (also: shunt connector): A small jumper on the HAT. In the position closest to the LED outputs it feeds the 12V supply to PWM channels 1 to 4. [Pioreactor docs](https://docs.pioreactor.com/user-guide/external-power)

**single-cell protein** (also: SCP): Protein-rich biomass of microbes, such as bacteria, yeasts or algae, grown as food or animal feed.

**solenoid valve** (also: solenoid): An electric valve on PWM channel 4 that opens to sparge. It must be 3-way venting (3/2), so the line vents when it closes.

**sparging** (also: sparge, sparges): Bubbling gas through the culture. Here, CO₂ from the cylinder flows down the anode on a timer set in the electroPioreactor job.

**SPEC** (also: SPEC position): A sensor position on the vial holder, covered when not in use. In this build the Precision Temperature Upgrade Kit's sensor seats there.

**SSH**: Secure Shell: a command line on the Pioreactor from your computer's terminal, for example ssh pioreactor@hostname.local.

**STEMMA-QT**: A small 4-pin plug-and-socket standard for sensor boards. The eye-spys and the temperature sensor daisy-chain over it.

**sterilise** (also: sterilisation): To kill every microbe on equipment or in a liquid, for example by autoclaving or by passing a liquid through a 0.2 µm filter.

## T

**turbidostat**: A dosing mode that adds fresh media and removes culture to hold optical density at a set point. [Pioreactor docs](https://docs.pioreactor.com/user-guide/dosing-automations#turbidostat)

## V

**vent filter**: A 0.2 µm hydrophobic membrane on luer fittings. Gas passes; microbes and liquid do not, so each gas path stays sterile.

## W

**wheel**: A Python package file (.whl). The card bundle carries the plugins as wheels; one that fails to install lands in pioreactor/plugins/failed/ on bootfs, with a log.

**worker**: A Pioreactor that runs experiments under a leader. It has no web interface of its own and takes its config.ini from the leader.

## X

**XR upgrade kit** (also: XR kit): Pioreactor's extended-range optics. Extra eye-spys read light scattered at 45° and 135° as well as 90°, for a lower OD detection limit. [Pioreactor docs](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly)
