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
    question: "Front to back, in what order do the platforms sit?"
    options:
      - {label: "Pioreactor, pumps, both bottle holders side by side, SodaStream holder", correct: true}
      - {label: "Pioreactor, both bottle holders side by side, pumps, SodaStream holder", fix: "Swap them: the pump platform joins the Pioreactor platform, so the pump leads reach the PWM channels, and the bottle holders go directly behind the pumps."}
      - {label: "Pioreactor, pumps, SodaStream holder, both bottle holders side by side", fix: "Move the SodaStream holder to the back, centred on the Pioreactor platform, with the bottle holders directly behind the pumps. Several units on one bench: see the box below."}
  - id: dovetail-direction
    question: "On every platform except the SodaStream holder, which way do the male dovetails point?"
    options:
      - {label: "Away from you and to the left", correct: true}
      - {label: "Away from you and to the right", fix: "Turn that platform round so they point away and to the left. Only the SodaStream holder may point right, for a tight cylinder (item 5)."}
      - {label: "Towards you and to the left", fix: "Turn that platform round so they point away from you and to the left."}
  - id: sd-card-clearance
    question: "Before anything is pressed down, what sits over the Pi's SD card?"
    options:
      - {label: "The pumping platform's cutout, with space round the card", correct: true}
      - {label: "The pumping platform's solid edge, resting on the card", fix: "Stop: do not press down. Shift the platform until its cutout clears the card. If it cannot, contact us before forcing anything."}
---

On every platform except the SodaStream holder (see item 5), the male dovetails point away from you and to the left. Slide each joint together, but do not press it down yet: **Press the raft together**, next, does that once the layout is checked.

1. Place the Pioreactor platform first, turned so the Pi's ports have room.
2. Join the pump platform to it, so the pump leads reach the PWM channels.
3. Join the 250 ml media and product bottle platforms directly behind the pumps.
4. Join the SodaStream holder at the back, centred on the Pioreactor platform.
5. Orient the SodaStream holder to suit the cylinder:
   - Loose cylinder: dovetails away from you and to the left, like the rest.
   - Tight cylinder: rotate the holder so they point away and to the right. Its gap is then free to open for larger cylinders.
6. Check the pumping dovetail platform's cutout clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->

<!-- The recording (session-20 0:00:12) built the raft SodaStream-first; this order is the corrected one from Martin, 2026-09-24. -->
<!-- VIDEO CUT: vid-02-platform-setup covers this step and the next. Cut it where the joints are pressed down (the next step's item 1); this step keeps the part before that. -->

<details>
<summary>Several units on one bench</summary>

Alternate media and product bottles between units, so the media bottle holders form the backbone of the raft.

</details>
