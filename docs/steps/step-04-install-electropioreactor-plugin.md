---
id: step-04-install-electropioreactor-plugin
order: 4
title: "Install the electroPioreactor plugin"
guide: [aep]
checks_draft: true
checks:
  - id: in-activities
    question: "Under Pioreactors → your unit → Manage → Activities, do you see electroPioreactor?"
    issues:
      - {problem: "It is not listed", fix: "Hard-refresh the page (Ctrl/Cmd+Shift+R). On the card route, put the card back in your computer: `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong. On a running unit, `pio plugins list` should show `pioreactor-electropioreactor-plugin`."}
      - {problem: "The page at `<hostname>.local` will not load while the unit runs its own access point", fix: "On its own access point the unit is at 10.42.0.1, and the UI also answers to http://pioreactor.local."}
  - id: installer-done
    question: "Did the install finish without stopping on an error?"
    issues:
      - {problem: "It stopped on `[PWM] 4 = 'waste'`", fix: "That is the stock Pioreactor default. Set PWM 4 to `relay` on the UI's Configuration page (moving any real waste pump to another channel first), then install again."}
      - {problem: "The computer offered to initialise or reformat the card", fix: "Click Ignore: it is offering to format the Linux part of the card, which it cannot read. Nothing needs formatting."}
  - id: clock-right
    question: "Does the unit show the correct date and time?"
    issues:
      - {problem: "The clock is wrong on an offline unit", fix: "With no internet the unit has no time source: set it from the computer with the `sudo date` command in this step."}
---

Install the [electroPioreactor plugin](../../AEP-Plugin) before going further: the electrolysis check in [Set up electrolysis](step-05-set-up-electrolysis.md) runs through its job, so its 10% power clamp protects the electrodes the first time they are driven.

1. Install it by one of the two routes in [AEP-Plugin/README.md](../../AEP-Plugin/README.md): [From the card](../../AEP-Plugin/README.md#from-the-card) straight after flashing, or [Over SSH](../../AEP-Plugin/README.md#over-ssh) on a unit that is already running.
2. Open the unit's web interface and hard-refresh (Ctrl/Cmd+Shift+R).
3. Check **electroPioreactor** is listed under **Pioreactors → your unit → Manage → Activities**.
4. If the unit has no internet, set its clock from the computer:

   ```bash
   ssh pioreactor@<hostname>.local "sudo date -u -s '$(date -u +'%Y-%m-%d %H:%M:%S')'"
   ```

<details>
<summary>What this plugin replaces</summary>

This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile: a single background job drives electrolysis on LED D, sparges CO₂ on the PWM 4 relay, pauses electrolysis for the duration of each sparge, and pauses OD reading for the sparge plus a settle window.

</details>

<details>
<summary>Why the clock matters</summary>

With no internet the unit has no time source, so its clock is wrong, and so is every timestamp it records.

</details>

<details>
<summary>If a cable is easier</summary>

With a USB-C-to-ethernet adapter and an ethernet cable into the Raspberry Pi 5's ethernet port, turn on macOS **Internet Sharing** to that adapter ([Pioreactor's instructions](https://docs.pioreactor.com/user-guide/internet-sharing)) and the unit gets real internet through the computer. `pio update`, the temperature plugin and the clock then work as normal.

</details>
