---
id: step-04-install-electropioreactor-plugin
order: 4
title: "Install the electroPioreactor plugin"
guide: [aep]
---

Install the [electroPioreactor plugin](../../AEP-Plugin), following [AEP-Plugin/README.md](../../AEP-Plugin/README.md)

<details>
<summary>What this plugin replaces</summary>

This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile: a single background job drives electrolysis on LED D, sparges CO₂ on the PWM 4 relay, pauses electrolysis for the duration of each sparge, and pauses OD reading for the sparge plus a settle window.

</details>

<details>
<summary>No network at the build site</summary>

The install above needs the unit on a LAN, and internet on the unit to `git clone`.
Without either, stage the install onto the microSD card before it is ejected and let
the Pioreactor raise its own WiFi to install over: [Offline: stage the install on the
SD card](../../AEP-Plugin/README.md#offline-stage-the-install-on-the-sd-card-no-lan-no-internet).
Decide before step 3 - the same missing internet stops `pio update` and the
temperature kit's plugin there.

</details>

<!-- TODO: the offline card-staging route this links to was first run on ed06 (2026-09-22): staging, the access point and the install all worked, and it turned up the missing setuptools on the unit, the unstaged temperature plugin and the stock [PWM] 4=waste collision. Those three fixes have not themselves been run on hardware yet - re-run the whole route once before relying on it for the AEP0.2 instruction video | assignee: @Martin -->

<!-- TODO: hard-coded step numbers here and in step-05 ("step 8") and step-09 ("step 4", "step 5") will drift if the steps are ever reordered - reference by title or slug instead | assignee: @Martin -->

Install it before going any further. The electrolysis check in step 5 runs through this job, so that its 10% power clamp is protecting the electrodes the first time they are ever driven.
