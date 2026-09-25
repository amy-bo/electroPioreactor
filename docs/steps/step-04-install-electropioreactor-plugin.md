---
id: step-04-install-electropioreactor-plugin
order: 4
title: "Check the plugin"
guide: [aep]
checks_draft: true
checks:
  - id: in-activities
    question: "Under Pioreactors → your unit → Manage → Activities, do you see electroPioreactor?"
    issues:
      - {problem: "It is not listed", fix: "Hard-refresh the page (Ctrl/Cmd+Shift+R). Card route: put the card back in your computer; `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong. Running unit: `pio plugins list` should show `pioreactor-electropioreactor-plugin`."}
      - {problem: "The page at `<hostname>.local` will not load while the unit runs its own access point", fix: "On its own access point the unit is at 10.42.0.1. The UI also answers at http://pioreactor.local."}
  - id: installer-done
    question: "Did the install finish without stopping on an error?"
    issues:
      - {problem: "It stopped on `[PWM] 4 = 'waste'`", fix: "That is the stock Pioreactor default. Move any real waste pump to another channel, set PWM 4 to `relay` on the UI's **Configuration** page, then install again."}
      - {problem: "The computer offered to initialise or reformat the card", fix: "Click **Ignore**. It cannot read the Linux part of the card and is offering to format it. Nothing needs formatting."}
  - id: clock-right
    question: "Does the unit show the correct date and time?"
    issues:
      - {problem: "The clock is wrong on an offline unit", fix: "An offline unit has no time source. Set its clock from the computer with the `sudo date` command under **If the unit has no internet, set its clock**."}
---

The plugin installed itself from the card in the previous step. Check it now: [Set up electrolysis](step-05-set-up-electrolysis.md) runs the electrodes through its job, whose 10% power clamp protects them.

1. Open the unit's web interface and hard-refresh (Ctrl/Cmd+Shift+R).
2. Check **electroPioreactor** is listed under **Pioreactors → your unit → Manage → Activities**.
3. If it is missing, put the card back in your computer and open the bootfs drive: `pioreactor/plugins/failed/` holds the wheel and a log.
4. Then install over SSH instead, as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh).
5. If the unit has no internet, set its clock from the computer, replacing `<hostname>` with the unit's hostname:

   ```bash
   ssh pioreactor@<hostname>.local "sudo date -u -s '$(date -u +'%Y-%m-%d %H:%M:%S')'"
   ```

   :::note
   With no internet the unit has no time source, so its clock is wrong, and so is every timestamp it records.
   :::

<details>
<summary>What this plugin replaces</summary>

This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile. One background job:

- drives electrolysis on LED D;
- sparges CO₂ on the PWM 4 relay;
- pauses electrolysis during each sparge;
- pauses OD reading for the sparge plus a settle window.

</details>

<details>
<summary>If a cable is easier</summary>

Plug a USB-C-to-ethernet adapter into the computer and run an ethernet cable to the Raspberry Pi 5. Turn on macOS **Internet Sharing** to that adapter ([Pioreactor's instructions](https://docs.pioreactor.com/user-guide/internet-sharing)). The unit then has real internet through the computer, so `pio update`, the temperature plugin and the clock work as normal.

</details>
