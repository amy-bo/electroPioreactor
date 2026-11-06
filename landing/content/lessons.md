---
title: What we have learned
description: Five design lessons that took us a while to learn, from constant-current electrolysis and a chloride-free medium to surplus oxygen, anode choice and venting solenoids.
section: learn
audience: everyone
order: 25
---
Making hydrogen inside a living culture sounds simple: two electrodes and a current. In practice a few things took us a while to learn, and each one shaped the design you see today. This page collects them, with links to the experiments behind them.

We built the electroPioreactor because hydrogen-oxidising bacteria (HOB) are a very promising sustainable protein, and hydrogen is an awkward gas. A sealed vial of hydrogen and oxygen is a "knallgas" mixture (the old German name for oxyhydrogen) and unlikely to get past any sensible risk assessment. Making the gases in the culture, only as fast as we choose to make them, gets round that. It also means a whole unit runs from two plug-in power supplies and a SodaStream cylinder. The parts are described on [How it works](/how-it-works/).

## The electrodes are driven by current, not voltage

We drive the electrodes from one of the Pioreactor's LED channels. That channel's driver regulates current rather than voltage, and switches it on and off very fast (pulse-width modulation, PWM). The power setting sets the fraction of time it is on, so the average current is proportional to the setting, and the rate of hydrogen production follows the current. The cell voltage simply settles wherever the electrodes and the medium put it, as long as it stays well below the Raspberry Pi's 5 V rail. <!-- source: Media/protocols/gerrit-current.md (Model: duty-cycle averaging) -->

The evidence is [Gerrit Niezen](https://amy.bo/~gerrit)'s [current measurement experiment](https://forum.amybo.org/t/current-measurement-experiment/166) on the forum. The protocol for repeating it, a sweep at 3, 5, 7 and 10 % power, is in [Media/protocols/gerrit-current.md](repo:Media/protocols/gerrit-current.md), and its results feed the [gas model](/gas-model/).

## The medium is also the electrolyte

The culture medium carries the current between the electrodes. Most standard HOB media contain chloride, which electrolysis turns into hypochlorite (bleach), which kills the culture. Ours is chloride-free and phosphate-buffered, based on Sydow et al. (2017). See [Media](/media/). <!-- source: Media/MediaFormulation.md (Background) -->

## The bacteria use less oxygen than the electrolysis makes

Water splits into two molecules of hydrogen for every one of oxygen, and the bacteria do not need that much oxygen, so it builds up. Bubbling carbon dioxide (CO₂) through the vial purges it, as well as feeding the culture. The plugin pauses the electrolysis while it sparges. How long and how often to sparge is what the [gas model](/gas-model/) works out.

## Anodes matter more than cathodes

We started with platinised titanium anodes and have moved to mixed metal oxide (MMO: iridium and tantalum oxides on titanium), which in [Gerrit's tests](https://forum.amybo.org/t/current-measurement-experiment/166/2) gives the same current at about 0.3 V lower cell voltage. The cathode is plain stainless steel, and that seems to be the right choice: platinum also catalyses hydrogen and oxygen recombining into water, which is the last thing we want at the cathode.

The forum has a whole thread by Gerrit Niezen [evaluating platinised electrodes](https://forum.amybo.org/t/evaluating-platinized-electrodes-for-electrolysis/71), and another on [graphite anodes](https://forum.amybo.org/t/alternative-anode-testing-graphite/95). The Harvey Mudd College clinic's anode comparison is on [Research](/research/#harvey-mudd-college-clinic-anode-and-valve), and photographs of the discoloured anodes from the first aseptic runs are on the [AEP page](/aep/#what-we-learned-from-the-first-runs).

## The solenoid has to vent

A normal two-port solenoid valve traps a slug of CO₂ between itself and the vial when it closes. The CO₂ dissolves, and the vacuum it leaves sucks medium back up the line. Eli Silver at Brown University diagnosed this, and a 3/2 (three-port) venting solenoid fixes it: when it closes, it lets air into the line instead. The full story is on [Research](/research/#past-research-projects), and the valve options are compared in [Components/CO2 transfer/](repo:Components/CO2%20transfer/).

<figure>
<img src="/img/venting-solenoid-on-regulator.jpg" alt="A CO₂ regulator with two pressure gauges on a SodaStream cylinder, with a small silver solenoid valve with a black coil fitted to its outlet" width="1184" height="1573">
<figcaption>The gas train on an early build: SodaStream cylinder, regulator, venting solenoid. Photo: AMYBO, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</figcaption>
</figure>

## Where next

- [How it works](/how-it-works/): the whole unit, part by part.
- [Which electroPioreactor?](/variants/): the Aseptic and Mixed-culture versions.
- [History](/history/): the 2023 and 2024 designs these lessons came from.
