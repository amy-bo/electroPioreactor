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
---

1. SodaStream at rear with expansion gap to right.
2. 250ml GL45 "Duran" product bottle in front and to the left of the SodaStream.
3. 250ml GL45 "Duran" media bottle in front and to the right of the SodaStream. (alternate media and product if multiple AEPs, forming a backbone of media bottle dovetail platforms)
4. Peristaltic pumps centred in front of product and media bottles
5. Pioreactor in front of Peristaltic pumps
6. The setup should look like this:

   <img width="555" height="998" alt="image" src="https://github.com/user-attachments/assets/0f4a6756-ea78-466b-bb35-c8b1a1c2c4af" />
   <!-- TODO: AEP0.1 photograph used as a placeholder - reshoot for AEP0.2 and commit through docs/media/ | assignee: @Martin -->

7. The pumping dovetail platform has a cutout for the SD card. Check it clears your SD card before forcing anything down. <!-- TODO: confirm Pi 5 clearance on the current platform revision and photograph it | assignee: @Martin -->
