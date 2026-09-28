---
id: step-06-install-electropioreactor-plugin
order: 6
title: "Check the plugin"
guide: [aep]
checks_draft: true
checks:
  - id: in-activities
    question: "What does Pioreactors → your unit → Manage → Activities show?"
    options:
      - {label: "A list that includes **electroPioreactor**", correct: true}
      - {label: "A list without **electroPioreactor**", fix: "Hard-refresh the page (Ctrl/Cmd+Shift+R). Card route: put the card back in your computer; `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong. Running unit: `pio plugins list` should show `pioreactor-electropioreactor-plugin`."}
      - {label: "Nothing: `<hostname>.local` will not load", fix: "While the unit runs its own access point, open http://10.42.0.1 or http://pioreactor.local instead."}
  - id: installer-done
    question: "How did the plugin install end?"
    options:
      - {label: "It finished, with no error shown", correct: true}
      - {label: "It stopped on `[PWM] 4 = 'waste'`", fix: "That is the stock Pioreactor default. Move any real waste pump to another channel, set PWM 4 to `relay` on the UI's **Configuration** page, then install again."}
      - {label: "The computer offered to reformat the card", fix: "Click **Ignore**. The computer cannot read the card's Linux partition; nothing needs formatting."}
  - id: clock-right
    question: "Compared with your computer's clock, what date and time does the unit show?"
    options:
      - {label: "The same date and time, to the minute", correct: true}
      - {label: "A different date, or a time minutes out", fix: "An offline unit has no time source. Set its clock from the computer with the `sudo date` command on this page."}
---

The plugin installed itself from the card. Check it now: [Test electrolysis](step-08-test-electrolysis.md) drives the electrodes through its job, whose 10% power clamp protects them.

1. Open the unit's web interface and hard-refresh (Ctrl/Cmd+Shift+R).
2. Check **electroPioreactor** is listed under **Pioreactors → your unit → Manage → Activities**.
3. If it is missing, put the card back in your computer and read the log in `pioreactor/plugins/failed/` on the bootfs drive. Then install over SSH, as in [AEP-Plugin/README.md](../../AEP-Plugin/README.md#over-ssh).
4. If the unit has no internet, set its clock from the computer, replacing `<hostname>` with the unit's hostname:

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
<summary>Internet over an ethernet cable</summary>

Plug a USB-C-to-ethernet adapter into the computer and run an ethernet cable to the Raspberry Pi 5. Turn on macOS **Internet Sharing** to that adapter ([Pioreactor's instructions](https://docs.pioreactor.com/user-guide/internet-sharing)). The unit then has internet through the computer, so `pio update`, the temperature plugin install and the clock work.

</details>
