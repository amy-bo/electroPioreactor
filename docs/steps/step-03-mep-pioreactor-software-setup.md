---
id: step-03-mep-pioreactor-software-setup
order: 3
title: "Pioreactor software setup"
guide: [mep, baep]
parts:
  - {component: microsd-card, qty: 1, cat: part}
tools:
  - {component: computer-with-microsd-reader, qty: 1}
checks_draft: true
checks:
  - id: model-set
    question: "In Inventory, is this unit's model set to the Pioreactor 20 ml v1.1?"
    issues:
      - {problem: "It shows another model", fix: "Set it in Inventory. Until then, OD readings are interpreted against the wrong hardware."}
  - id: in-activities
    question: "Is electroPioreactor listed under Pioreactors → your unit → Manage → Activities?"
    issues:
      - {problem: "It is not listed", fix: "Hard-refresh the page (Ctrl/Cmd+Shift+R). Otherwise put the card back in your computer; `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong."}
      - {problem: "The log says `refusing to overwrite [PWM] 4 = 'waste'`", fix: "That is the stock Pioreactor default. Set PWM 4 to `relay` on the UI's **Configuration** page, then install again over SSH."}
  - id: clock-right
    question: "Does the unit show the correct date and time?"
    issues:
      - {problem: "The clock is wrong on an offline unit", fix: "An offline unit has no time source. Set its clock from the computer with the `sudo date` command on this page."}
---

The electroPioreactor plugin goes onto the card while you flash it, so the unit boots ready. Text as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#from-the-card).

1. Two changes to make while following Pioreactor's software set-up guide, which comes next:
   - At its step 3, in **App Options**, switch off **Eject media when finished** (1) before you set the **Content Repository** (2), so the card stays mounted after the write.

     ![Imager's App Options: 1 Eject media when finished switched off, 2 Content Repository Edit](https://raw.githubusercontent.com/amy-bo/electroPioreactor/main/AEP-Plugin/docs/imager-app-options.png)

   - At its step 15, for your leader, leave the Wi-Fi page blank if you can't add devices to your lab's Wi-Fi then reach them through it (typical at universities); the leader Pioreactor then makes its own network.
   - Worker-only units: follow the same steps with a **Worker** image. Flash each worker with the step 15 Wi-Fi page set to network `pioreactor`, password `raspberry`, and at step 3 below do not drag the `local_access_point` file across. The plugin installs when you add the unit from the leader's **Inventory** page. Hotspot cluster: boot the leader first.

   With those in mind, follow [Pioreactor's software set-up guide](https://docs.pioreactor.com/user-guide/software-set-up) up to **Write**, and come back here while the card writes.
2. Download and unzip the [MEP card bundle](https://github.com/amy-bo/electroPioreactor/releases/latest/download/electroPioreactor-MEP-card-bundle.zip).
3. When the write finishes, drag the `pioreactor` folder from the bundle onto the `bootfs` drive. If you left the Wi-Fi page blank (for the leader Pioreactor to make its own network), also drag across the `local_access_point` file, after changing `GB` in it to your country code\*. DO NOT drag it across for workers, or if you set your Pioreactors up to join a Wi-Fi network. If the card was ejected anyway, remove and reinsert it.
4. Eject the card. One change to the rest of Pioreactor's guide: for a unit that makes its own Wi-Fi, join the network `pioreactor` (password `raspberry`) and open `http://pioreactor.local`. Then continue the guide from its step 18. At the model dialog, choose the Pioreactor 20 ml v1.1.

   \* If your country code is not GB, open `local_access_point` in TextEdit/Notepad and replace `GB` with the ISO two-letter code (CA, IE, DE, AU, NZ, GL, US, etc.; see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) and save; the file should contain just those two letters. Do nothing if you live in the United Kingdom of Great Britain and Northern Ireland (GB).
5. Open the unit's web interface and hard-refresh (Ctrl/Cmd+Shift+R).
6. Check **electroPioreactor** is listed under **Pioreactors → your unit → Manage → Activities**. If it is missing, put the card back in your computer and read the log in `pioreactor/plugins/failed/` on the bootfs drive. Then install over SSH, as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh).
7. If the unit has no internet, set its clock from the computer, replacing `<hostname>` with the unit's hostname:

   ```bash
   ssh pioreactor@<hostname>.local "sudo date -u -s '$(date -u +'%Y-%m-%d %H:%M:%S')'"
   ```

   :::note
   With no internet the unit has no time source, so its clock is wrong, and so is every timestamp it records.
   :::

<details>
<summary>What the plugin does</summary>

One background job:

- drives electrolysis on LED D, clamped to 10% power to protect the electrodes;
- sparges CO₂ on the PWM 4 relay;
- pauses electrolysis during each sparge;
- pauses OD reading for the sparge plus a settle window.

</details>

<details>
<summary>Without the card bundle (older Pioreactor OS)</summary>

Pioreactor OS needs boot-partition plugin support for the card route. On an older release: flash and boot as Pioreactor's guide says, run `pio update`, and install the plugin over SSH as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh). A unit already running can also install it from **Plugins** in the web interface's left-hand menu.

</details>

<details>
<summary>Notes</summary>

- Name each unit by location plus unit number, for example `ed04`.
- If the page at `<hostname>.local` will not load while the unit runs its own access point, open http://10.42.0.1 instead.

</details>
