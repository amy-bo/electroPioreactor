---
id: step-03-pioreactor-software-setup
order: 3
title: "Follow the Pioreactor software setup guide"
guide: [aep]
parts:
  - {component: microsd-card, qty: 1, cat: part}
  - {component: precision-temperature-upgrade-kit, qty: 1, cat: prev, when: {temp-kit: true}}
tools:
  - {component: computer-with-microsd-reader, qty: 1}
checks_draft: true
checks:
  - id: version-26-5
    question: "Is the Pioreactor software at release 26.5.0 or later?"
    issues:
      - {problem: "It is older", fix: "Run `pio update` before going further."}
      - {problem: "The unit has no internet, so `pio update` fails", fix: "Flash the latest image instead: an offline unit cannot be updated on site (see the offline route in the plugin install step)."}
  - id: xr-model-set
    question: "In Inventory, is this unit's model set to the XR variant?"
    issues:
      - {problem: "It still shows the standard model", fix: "Set it to the XR variant in Inventory: until you do, OD readings are interpreted against the wrong channel map."}
  - id: xr-config
    question: "Are the XR photodiode channel values in `config.ini`?"
    issues:
      - {problem: "They are missing", fix: "Add them as listed at the end of the XR assembly guide."}
  - id: temp-plugin
    when: {temp-kit: true}
    question: "Is `pioreactor-precision-temperature-plugin` listed under Plugins in the Pioreactor UI?"
    issues:
      - {problem: "The install fails because the unit has no internet", fix: "Stage the plugin onto the card with the offline route in the plugin install step (name it as the third argument), or give the unit internet over an ethernet cable with Internet Sharing."}
---

<!-- TODO: this line restates the step title - see the note in step-02 | assignee: @Martin -->

Follow the Pioreactor software setup guide: <https://docs.pioreactor.com/user-guide/software-set-up>

> **If this Pioreactor cannot reach a network**, read [step 4](step-04-install-electropioreactor-plugin.md#if-the-pioreactor-cannot-reach-a-network) before you flash the card: the offline route changes what you set in Raspberry Pi Imager, and the plugins have to go onto the card while you still have internet.

1. The XR kit needs Pioreactor release 26.1.30 or later and the electroPioreactor plugin needs 26.5.0 or later, so treat **26.5.0 as the minimum** for an AEP0.2 and run `pio update` before going further.
2. In the web UI open **Inventory** and set this unit's model to the XR variant. Until you do, OD readings are interpreted against the wrong channel map.
3. Add the XR photodiode channel values to `config.ini`, as listed at the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly).

<!-- when temp-kit=true -->

4. If the Precision Temperature Upgrade Kit is fitted, open **Plugins** in the Pioreactor UI and install `pioreactor-precision-temperature-plugin`. The equivalent from a shell on the unit is:

   ```bash
   pio plugins install pioreactor-precision-temperature-plugin
   ```

<!-- /when -->
