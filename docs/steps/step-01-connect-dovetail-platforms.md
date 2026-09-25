---
id: step-01-connect-dovetail-platforms
order: 1
title: "Connect the platforms"
media: [vid-02-platform-setup]
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
    question: "Front to back, is the raft Pioreactor, pumps, product bottle (left) and media bottle (right), then the SodaStream holder?"
    issues:
      - {problem: "The layout differs", fix: "Rearrange the platforms in the order above, male dovetails away from you and to the left (SodaStream holder as in action 5)."}
      - {problem: "Several AEPs do not join into one raft", fix: "Alternate media and product bottles between units, so the media bottle platforms form the backbone of the raft."}
  - id: sd-card-clearance
    question: "Does the pumping dovetail platform sit down fully without pressing on the SD card?"
    issues:
      - {problem: "The platform catches on the SD card", fix: "Stop. Check the platform's SD card cutout clears your card before forcing anything down."}
---

On every platform except the SodaStream holder (see item 5), the male dovetails point away from you and to the left.

1. Place the Pioreactor platform first, turned so the Pi's USB and ethernet ports have room.
2. Join the pump platform to it, so the pump leads reach the PWM channels.
3. Join the 250 ml media and product bottle platforms directly behind the pumps.
4. Join the SodaStream holder at the back, centred on the Pioreactor platform.
5. Orient the SodaStream holder to suit the cylinder:
   - Loose cylinder: dovetails away from you and to the left, like the rest.
   - Tight cylinder: rotate the holder so they point away and to the right. Its gap is then free to open for larger cylinders.
6. Check the pumping dovetail platform's cutout clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->
7. Press every joint down until the raft sits flat on the table. The last joint may need some force.

<!-- The recording (session-20 0:00:12) built the raft SodaStream-first; this order is the corrected one from Martin, 2026-09-24. -->

<img width="555" height="998" alt="Dovetail platforms joined into one raft on a bench (AEP0.1 photograph)" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />
<!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

<details>
<summary>Several AEPs on one bench</summary>

Alternate media and product bottles between units, so the media bottle holders form the backbone of the raft.

</details>
