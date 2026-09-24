---
id: step-01-connect-dovetail-platforms
order: 1
title: "Connect empty dovetail platforms in raft, with dovetails always to front and left"
guide: [aep, mep]
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

1. Put the SodaStream holder at the rear, expansion slot to the right. <!-- from video: session-20 0:00:12 - the SodaStream holder "needs to go the wrong way", lugs pointing away from you and to the left, unlike the others; the transcript is garbled about the other platforms (0:00:54 says the pumps also go "away and to the left"), so check the picture against "dovetails to front and left" in the title and here -->
2. Join the product bottle holder in front and to the left of it, dovetails to the front and left.
3. Join the media bottle holder in front and to the right of it, the same way.
4. Join the two pump holders to each other first, then centre them in front of the bottle holders. <!-- from video: session-14 0:05:04 and session-20 0:01:07 show two pump pieces plus a Pioreactor platform; the frontmatter lists one pumping-dovetail-platform -->
5. Join the Pioreactor platform at the front, turned so the Pi's USB and ethernet ports have room.
6. Press every joint down until the raft sits flat on the table; the last joint may need some force.
7. Check the pumping dovetail platform's cutout clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->

<img width="555" height="998" alt="image" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />
<!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

<details>
<summary>Several AEPs on one bench</summary>

Alternate media and product bottles between units, so the media bottle holders form the backbone of the raft.

</details>
