---
id: step-04-install-electropioreactor-plugin
order: 4
title: "Install the electroPioreactor plugin"
guide: [aep]
---

Install the [electroPioreactor plugin](../../AEP-Plugin), following [AEP-Plugin/README.md](../../AEP-Plugin/README.md)

<details>
<summary>What this plugin replaces</summary>

This is the AEP's own plugin, not a Pioreactor one. It replaces the AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile: a single background job drives electrolysis on LED D, sparges CO₂ on the PWM 4 relay, pauses electrolysis for the duration of each sparge, and pauses OD reading for the sparge plus a settle window.

</details>

<!-- TODO: hard-coded step numbers here and in step-05 ("step 8") and step-09 ("step 4", "step 5") will drift if the steps are ever reordered - reference by title or slug instead | assignee: @Martin -->

Install it before going any further. The electrolysis check in step 5 runs through this job, so that its 10% power clamp is protecting the electrodes the first time they are ever driven.

## If the Pioreactor cannot reach a network

The instructions above need the unit on a LAN and need the unit itself to reach the internet. Where neither is available, everything the unit needs goes onto the microSD card instead, and the unit raises its own WiFi network for you to install over. Start before you flash the card at step 3, and work through it in order; nothing here assumes you have done it before.

You need the microSD card, a computer with a card reader, and **internet on that computer** up to step 6. The Pioreactor never needs internet.

1. Open a terminal on that computer (on a Mac: Applications → Utilities → Terminal) and download this repository:

   ```bash
   git clone https://github.com/amy-bo/electroPioreactor.git
   cd electroPioreactor
   ```

   Stay in this folder for steps 4 and 7.

2. Flash the card as at step 3, with one change: on Raspberry Pi Imager's WiFi page, leave **WiFi configuration disabled**. Write down the hostname and password you set - you need both at step 8. The examples below use `ed04`; substitute your own.

3. Imager ejects the card when it finishes. Take it out of the reader and put it straight back in. A `bootfs` volume appears. If the computer offers to initialise or reformat a disk, click **Ignore** - it is offering to format the Linux part of the card, which it cannot read.

4. Put the plugins on the card:

   ```bash
   bash AEP-Plugin/scripts/stage-sd-card.sh /Volumes/bootfs GB pioreactor-precision-temperature-plugin
   ```

   `GB` is your two-letter country code, for the WiFi the unit will broadcast. Name `pioreactor-precision-temperature-plugin` only if the Precision Temperature Upgrade Kit is fitted; it cannot be installed later without internet. The script prints what it wrote.

5. Eject the card (drag to the bin, or `diskutil eject /Volumes/bootfs`), put it in the Pi, and power up. First boot takes a few minutes and ends with the HAT blinking its blue LED. Nothing appears on a monitor - the image has no screen output.

6. On the computer, open the WiFi menu and join the network **`pioreactor`**, password **`raspberry`**. The computer has no internet while it is on this network.

7. Connect to the unit, using the hostname from step 2:

   ```bash
   ssh pioreactor@ed04.local
   ```

   Type `yes` when it asks about the authenticity of the host, then the password from step 2. Nothing appears as you type it; that is normal.

8. Install, on the unit:

   ```bash
   bash /boot/firmware/electropioreactor/install.sh
   ```

   It finishes with `Done (install mode: ...)`. If it stops on `[PWM] 4 = 'waste'`, that is the stock Pioreactor default rather than anything you wired, and the CO₂ solenoid needs that channel - re-run it as `EP_FORCE_PWM4=1 bash /boot/firmware/electropioreactor/install.sh`. If a waste pump really is on channel 4, move it in the UI's **Configuration** page first.

9. Set the clock, in a second terminal window on the computer - with no internet the unit's clock is wrong, and so is every timestamp it records:

   ```bash
   ssh pioreactor@ed04.local "sudo date -u -s '$(date -u +'%Y-%m-%d %H:%M:%S')'"
   ```

10. In a browser, open `http://ed04.local` and hard-refresh (Ctrl/Cmd+Shift+R). Under **Pioreactors → `ed04` → Manage → Activities** you should see **electroPioreactor**. Carry on from step 5 of this guide.

<!-- TODO: this procedure is a second copy of the one in AEP-Plugin/README.md, written for the guide's reader; the two have to be changed together until one of them becomes a pointer to the other | assignee: @Martin -->

<details>
<summary>Why the install cannot simply be done on the card</summary>

The computer can only see the card's small FAT boot partition. The plugin has to end up in `/opt/pioreactor/venv` or `~/.pioreactor/`, both on the Linux partition, which macOS and Windows cannot mount at all. So step 4 stages the parts and step 8 does the install, on the unit, where those paths exist.

Two things go onto the boot partition at step 4: Pioreactor's [`local_access_point`](https://docs.pioreactor.com/user-guide/local-access-point) file, whose entire contents are the country code, which is what makes the unit broadcast its own WiFi; and the plugins themselves, built into wheels because the unit's Python has no build tools of its own.

</details>

<details>
<summary>If a cable is easier than all of this</summary>

With a USB-C-to-ethernet adapter and an ethernet cable into the Raspberry Pi 5's ethernet port, none of the above is needed: turn on macOS **Internet Sharing** to that adapter ([Pioreactor's instructions](https://docs.pioreactor.com/user-guide/internet-sharing)) and the unit gets real internet through the computer. The normal instructions at the top of this step then work as written, as do `pio update` and the temperature plugin.

</details>
