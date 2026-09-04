---
id: step-03-pioreactor-software-setup
order: 3
title: "Follow the Pioreactor software setup guide"
guide: [aep]
parts:
  - {component: microsd-card, qty: 1, cat: part}
  - {component: precision-temperature-upgrade-kit, qty: 1, cat: prev}
tools:
  - {component: computer-with-microsd-reader, qty: 1}
---

Follow the Pioreactor software setup guide: <https://docs.pioreactor.com/user-guide/software-set-up>

1. The XR kit needs Pioreactor release 26.1.30 or later and the electroPioreactor plugin needs 26.5.0 or later, so treat **26.5.0 as the minimum** for an AEP0.2 and run `pio update` before going further.
2. In the web UI open **Inventory** and set this unit's model to the XR variant. Until you do, OD readings are interpreted against the wrong channel map.
3. Add the XR photodiode channel values to `config.ini`, as listed at the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly).
4. If the Precision Temperature Upgrade Kit is fitted, open **Plugins** in the Pioreactor UI and install `pioreactor-precision-temperature-plugin`. The equivalent from a shell on the unit is:

   ```bash
   pio plugins install pioreactor-precision-temperature-plugin
   ```
