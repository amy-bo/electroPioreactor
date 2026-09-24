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

The plugins go onto the card while you flash it, so the unit boots ready. Three things to do while following Pioreactor's software set-up guide, which comes at the end of this list:

1. Before you start, download and unzip the card bundle for your kit: [AEP](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-AEP-card-bundle.zip) (electroPioreactor, XR settings and the precision temperature plugin) or [MEP](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-MEP-card-bundle.zip).
2. At Pioreactor's step 3, in **App Options**, switch off **Eject media when finished** before you set the **Content Repository**, so the card stays mounted after the write.

   ![Imager's App Options: 1 Eject media when finished switched off, 2 Content Repository Edit](https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/AEP-Plugin/docs/imager-app-options.png)

3. At its step 15, for your leader, leave the Wi-Fi page blank if you can't add devices to your lab's Wi-Fi then reach them through it (typical at universities); the leader then makes its own network. Workers: set the Wi-Fi page to network `pioreactor`, password `raspberry`, and boot the leader first.
4. Choose **Raspberry Pi 5**, Pioreactor OS **Leader and worker** for the first unit and **Worker** for the rest, a hostname (for example `ed06`), username `pioreactor` and a password; note them.
5. When the write finishes, drag the `pioreactor` folder from the bundle onto the `bootfs` drive. If you left the Wi-Fi page blank, also drag across the `local_access_point` file, after changing `GB` in it to your country code\*. Do not drag it across for workers, or if your Pioreactors join a Wi-Fi network. If the card was ejected anyway, remove and reinsert it.
6. Eject the card, put it in the Pi and power up. For a leader that makes its own network, join `pioreactor` (password `raspberry`) on your computer and open `http://pioreactor.local`; otherwise continue Pioreactor's guide from its step 18. The model dialog does not appear: the bundle has set the model.

With those in mind, follow [Pioreactor's software set-up guide](https://docs.pioreactor.com/user-guide/software-set-up).

\* If your country code is not GB, open `local_access_point` in TextEdit/Notepad and replace `GB` with the ISO two-letter code (CA, IE, DE, AU, NZ, GL, US, etc.; see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) and save; the file should contain just those two letters. Do nothing if you live in the United Kingdom of Great Britain and Northern Ireland (GB).

<details>
<summary>Without the card bundle (older Pioreactor OS)</summary>

Pioreactor OS needs boot-partition plugin support for the card route. On an older release: flash and boot as Pioreactor's guide says, run `pio update` (26.5.0 is the minimum), set the unit's model to the XR variant in **Inventory**, add the XR photodiode channel values to `config.ini` from the end of the [XR assembly guide](https://docs.pioreactor.com/user-guide/40ml-v15-to-XR-upgrade-assembly), and install the plugins over SSH as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh).

</details>

<details>
<summary>Notes</summary>

- On the recording the unit was named `ed06`: location (Edinburgh) plus unit number.
- Until the model is set to XR in Inventory, OD readings are interpreted against the wrong channel map.

</details>
