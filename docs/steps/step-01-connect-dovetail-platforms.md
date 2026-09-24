---
id: step-01-connect-dovetail-platforms
order: 1
title: "Connect the platforms"
guide: [aep, mep, baep]
parts:
  - {component: pumping-dovetail-platform, qty: 1, cat: part}
  - {component: gl45-bottle-holder, qty: 2, cat: printed}
  - {component: co2-cylinder-dovetail-holder, qty: 1, cat: printed}
renders:
  - {id: gl45-bottle-holder-iso, component: gl45-bottle-holder, view: iso, explode: false, format: png}
viewer: {component: gl45-bottle-holder, format: glb}
checks_draft: true
checks:
  - id: raft-layout
    question: "Is the SodaStream holder at the rear, the product bottle in front and to its left, the media bottle in front and to its right, with the pumps and then the Pioreactor in front of them?"
    issues:
      - {problem: "The layout differs", fix: "Rearrange the platforms in the order listed above, with dovetails always to the front and left."}
      - {problem: "Several AEPs do not join into one raft", fix: "Alternate media and product bottles between units so that the media bottle platforms form the backbone of the raft."}
  - id: sd-card-clearance
    question: "Does the pumping dovetail platform sit down fully without pressing on the SD card?"
    issues:
      - {problem: "The platform catches on the SD card", fix: "Stop and check that the platform's SD card cutout clears your card before forcing anything down."}
---

Male dovetails face away from you and to the left on every platform except the SodaStream holder (see 5).

1. Start with the Pioreactor platform, turned so the Pi's USB and ethernet ports have room.
2. Join the pump platform to it, so the pump leads can reach the PWM channels.
3. Join the 250 ml media and product flask platforms straight behind the pumps.
4. Join the SodaStream holder at the back, centred on the Pioreactor platform.
5. SodaStream holder orientation: if the cylinder sits loose, dovetails away from you and to the left like the rest; if it is tight, rotate the holder so they face away from you and to the right, which leaves its gap free to open for larger cylinders.
6. Press every joint down until the raft sits flat on the table; the last joint may need some force.
7. Check the pumping dovetail platform's cutout clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->

<!-- The recording (session-20 0:00:12) built the raft SodaStream-first; this order is the corrected one from Martin, 2026-09-24. -->

<img width="555" height="998" alt="image" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />
<!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

<details>
<summary>Several AEPs on one bench</summary>

Alternate media and product bottles between units, so the media bottle holders form the backbone of the raft.

</details>
