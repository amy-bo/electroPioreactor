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
      - {problem: "The unit has no internet, so `pio update` fails", fix: "Flash the latest image instead, or give the unit internet over an ethernet cable with Internet Sharing (see the plugin install step)."}
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
      - {problem: "The install fails because the unit has no internet", fix: "Give the unit internet over an ethernet cable with Internet Sharing (see the plugin install step), then install it."}
---

Follow Pioreactor's [software setup guide](https://docs.pioreactor.com/user-guide/software-set-up). To install the electroPioreactor plugin from the card, read [Install the electroPioreactor plugin](step-04-install-electropioreactor-plugin.md) before you click **Write**.

1. In Raspberry Pi Imager, open **App options**, edit **Content repository**, choose **Use custom URL**, paste the URL from Pioreactor's guide, then **Apply and restart**.
2. Choose **Raspberry Pi 5**, then the latest Pioreactor OS: **Leader and worker** for the first unit, **Worker** for the rest.
3. Set the hostname (for example `ed06`), username `pioreactor` and a password, and note them.
4. Leave WiFi configuration disabled if the unit will not join a network; enable SSH with password authentication.
5. Write the card, put it in the Pi and power up.
6. Treat **26.5.0 as the minimum** (the XR kit needs 26.1.30, the plugin 26.5.0): run `pio update` before going further.
7. In the web UI open **Inventory** and set this unit's model to the XR variant.
8. Add the XR photodiode channel values to `config.ini`, as listed at the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly).

<!-- when temp-kit=true -->

9. If the Precision Temperature Upgrade Kit is fitted, open **Plugins** in the Pioreactor UI and install `pioreactor-precision-temperature-plugin`. The equivalent from a shell on the unit is:

   ```bash
   pio plugins install pioreactor-precision-temperature-plugin
   ```

<!-- /when -->

<details>
<summary>Notes</summary>

- On the recording the unit was named `ed06`: location (Edinburgh) plus unit number.
- Until the model is set to XR in Inventory, OD readings are interpreted against the wrong channel map.

</details>
