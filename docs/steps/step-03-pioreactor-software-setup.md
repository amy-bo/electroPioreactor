---
id: step-03-pioreactor-software-setup
order: 3
title: "Pioreactor software setup"
guide: [aep]
parts:
  - {component: microsd-card, qty: 1, cat: part}
  - {component: precision-temperature-upgrade-kit, qty: 1, cat: prev, when: {temp-kit: true}}
tools:
  - {component: computer-with-microsd-reader, qty: 1}
checks_draft: true
checks:
  - id: version-26-5
    question: "Fallback route only (no card bundle): is the Pioreactor software 26.5.0 or later?"
    issues:
      - {problem: "It is older", fix: "Run `pio update`."}
      - {problem: "The unit has no internet, so `pio update` fails", fix: "Flash the latest image instead, or give the unit internet over a cable: see **Internet over an ethernet cable** in **Check the plugin**."}
  - id: xr-model-set
    question: "In Inventory, is this unit's model set to the XR variant?"
    issues:
      - {problem: "It still shows the standard model", fix: "Set it to the XR variant in Inventory. Until then, OD readings are interpreted against the wrong channel map."}
  - id: xr-config
    question: "Fallback route only (no card bundle): are the XR photodiode channel values in config.ini?"
    issues:
      - {problem: "They are missing", fix: "Add them as listed at the end of the XR assembly guide."}
  - id: temp-plugin
    when: {temp-kit: true}
    question: "Is pioreactor-precision-temperature-plugin listed under Plugins in the Pioreactor UI?"
    issues:
      - {problem: "The install fails because the unit has no internet", fix: "Give the unit internet over a cable (see **Internet over an ethernet cable** in **Check the plugin**), then install it."}
---

The plugins go onto the card while you flash it, so the unit boots ready. Text as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#from-the-card).


1. Two changes to make while following Pioreactor's software set-up guide, which comes next:
   - At its step 3, in **App Options**, switch off **Eject media when finished** (1) before you set the **Content Repository** (2), so the card stays mounted after the write.

     ![Imager's App Options: 1 Eject media when finished switched off, 2 Content Repository Edit](https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/AEP-Plugin/docs/imager-app-options.png)

   - At its step 15, for your leader, leave the Wi-Fi page blank if you can't add devices to your lab's Wi-Fi then reach them through it (typical at universities); the leader Pioreactor then makes its own network.
   - Worker-only units: follow the same steps with a **Worker** image. Flash each worker with the step 15 Wi-Fi page set to network `pioreactor`, password `raspberry`, and at step 3 below do not drag the `local_access_point` file across. The plugin installs when you add the unit from the leader's **Inventory** page. Hotspot cluster: boot the leader first.

   With those in mind, follow [Pioreactor's software set-up guide](https://docs.pioreactor.com/user-guide/software-set-up) up to **Write**, and come back here while the card writes.
2. Download and unzip the [AEP card bundle](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-AEP-card-bundle.zip).
3. When the write finishes, drag the `pioreactor` folder from the bundle onto the `bootfs` drive. If you left the Wi-Fi page blank (for the leader Pioreactor to make its own network), also drag across the `local_access_point` file, after changing `GB` in it to your country code\*. DO NOT drag it across for workers, or if you set your Pioreactors up to join a Wi-Fi network. If the card was ejected anyway, remove and reinsert it.
4. Eject the card. One change to the rest of Pioreactor's guide: for a unit that makes its own Wi-Fi, join the network `pioreactor` (password `raspberry`) and open `http://pioreactor.local`. Then continue the guide from its step 18; the model dialog at its step 21 does not appear, because the bundle has set the model. **electroPioreactor** is under **Activities** on the unit's *Manage* page, and the precision temperature plugin is installed.

   \* If your country code is not GB, open `local_access_point` in TextEdit/Notepad and replace `GB` with the ISO two-letter code (CA, IE, DE, AU, NZ, GL, US, etc.; see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) and save; the file should contain just those two letters. Do nothing if you live in the United Kingdom of Great Britain and Northern Ireland (GB).

If it is missing, put the card back in your computer: `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong.

<details>
<summary>Without the card bundle (older Pioreactor OS)</summary>

Pioreactor OS needs boot-partition plugin support for the card route. On an older release: flash and boot as Pioreactor's guide says, run `pio update` (26.5.0 is the minimum), set the unit's model to the XR variant in **Inventory**, add the XR photodiode channel values to `config.ini` from the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly), and install the plugins over SSH as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh).

</details>

<details>
<summary>Notes</summary>

- On the recording the unit was named `ed06`: location (Edinburgh) plus unit number.
- Until the model is set to XR in Inventory, OD readings are interpreted against the wrong channel map.

</details>
