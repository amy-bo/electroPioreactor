---
id: step-04-install-electropioreactor-plugin
order: 4
title: "Install the electroPioreactor plugin"
guide: [aep]
---

Install the [electroPioreactor plugin](../../AEP-Plugin), following [AEP-Plugin/README.md](../../AEP-Plugin/README.md)

This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile: a single background job drives electrolysis on LED D, sparges CO₂ on the PWM 4 relay, pauses electrolysis for the duration of each sparge, and pauses OD reading for the sparge plus a settle window.

Install it before going any further. The electrolysis check in step 5 runs through this job, so that its 10% power clamp is protecting the electrodes the first time they are ever driven.
