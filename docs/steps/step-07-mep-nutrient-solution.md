---
id: step-07-mep-nutrient-solution
order: 7
title: "Nutrient solution"
guide: [mep, baep]
parts:
  - {component: peristaltic-pump, qty: 2, cat: part}
  - {component: gl45-bottle, qty: 2, cat: part}
  - {component: gl45-cap, qty: 2, cat: part}
  - {component: silicone-tubing, qty: 1, cat: part}
  - {component: barb-1-16-to-male-luer-lock, qty: 2, cat: part}
  - {component: barb-1-16-to-female-luer-lock, qty: 2, cat: part}
  - {component: power-supply-12v, qty: 1, cat: prev}
  - {component: pioreactor-vial-20ml, qty: 1, cat: prev}
  - {component: vial-cap-oring, qty: 1, cat: prev}
tools:
  - {component: analytical-balance, qty: 1}
checks_draft: true
checks:
  - id: channels
    question: "Does the **Configuration** page show `[PWM]` 2 = `waste`, 3 = `media` and 4 = `relay`?"
    issues:
      - {problem: "Channel 2 is `media`", fix: "That is Pioreactor's own example. On the MEP, 2 is the waste pump and 3 the media pump: set them and click **Save**."}
  - id: calibrated-on-12v
    question: "Were the pumps calibrated with the 12 V supply connected?"
    issues:
      - {problem: "They were calibrated on the Pi's own supply", fix: "Connect the 12 V supply (see **Pioreactor hardware setup**) and calibrate again."}
  - id: fourteen-ml
    question: "After running both pumps, does the vial hold 14 ml by weight?"
    issues:
      - {problem: "It fills or drains", fix: "Move the Media Out tube: it sets the level. It should be only just submerged at 14 ml."}
---

Follow Pioreactor's [peristaltic pump setup guide](https://docs.pioreactor.com/user-guide/using-pumps), with these channels.

1. On the unit's **Configuration** page, set `[PWM]` channel 2 to `waste` and 3 to `media`, leave 4 as `relay`, and click **Save**.

   :::note
   Pioreactor's pump guide uses PWM 2 for a media pump as an example. On the MEP, keep 2 for waste (product) and 3 for media.
   :::
2. Seat the pumps.
3. Plug the product pump into PWM 2 and the media pump into PWM 3.
4. Lead the cables out through the notches.
5. Put the media and product bottles, with their GL45 caps, into their holders.
6. Connect each bottle to its pump with the silicone tubing and luer fittings, then each pump to its tube on the vial cap: media to Media In, waste to Media Out.
7. Check the 12 V supply is in the HAT's barrel jack ([external power](https://docs.pioreactor.com/user-guide/external-power)).

   :::caution
   Calibrate only after this. Calibrating on the wrong supply means calibrating twice.
   :::
8. Fill the media bottle with water.
9. [Calibrate the pumps](https://docs.pioreactor.com/user-guide/hardware-calibrations#pump-calibration) on the **Protocols** page, waste on PWM 2 and media on PWM 3: catch each dispense in a tared weighing boat on the analytical balance and enter what it weighed (1 g of water is about 1 ml).
10. Unscrew the cap, empty, rinse and dry the vial, and fill it to 14 ml with water.
11. Screw the cap back on, and weigh the vial to confirm the volume.
12. Adjust the Media Out tube so it is only just submerged at that level.
13. Run the media and waste pumps, then weigh the vial again.
14. Repeat from item 12 until the vial holds 14 ml after running the pumps.

<details>
<summary>Why the Media Out tube sets the level</summary>

The waste pump over-runs each dilution by design, so the height of the Media Out tube is the level setpoint, not the ratio of media to waste volume. See [forum #801](https://forum.pioreactor.com/t/dosing-volumes-how-to-keep-the-volume-added-and-the-volume-removed-to-be-equal/801).

</details>
