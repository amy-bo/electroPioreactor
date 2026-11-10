---
title: Software and plugin
description: The electroPioreactor Pioreactor plugin, its single background job, every setting, the hardware channels, installation online and from the SD card, calibration, safety behaviour and troubleshooting.
section: build
audience: expert
order: 30
---

The electroPioreactor runs on the standard Pioreactor software, plus one plugin of its own. The plugin adds a single job, **electroPioreactor**, that switches electrolysis on and off, opens the carbon dioxide (CO₂) valve on a timer, and pauses the optical density (OD) reading while bubbles would spoil it. Everything is set from the Pioreactor web interface.

> **Note:** Abbreviations: PWM, pulse-width modulation (the switched outputs on the Pioreactor HAT, the board on the Raspberry Pi); LED channel, one of the HAT's four LED outputs, A to D, normally used for lights; MQTT, the messaging system Pioreactor jobs use; AEP and MEP, the Aseptic and Mixed-culture electroPioreactors (see [Variants](/variants/)).

## At a glance

| Item | Value |
| --- | --- |
| Package | `pioreactor-electropioreactor-plugin`, version 0.7.3, released 6 November 2026 as [`plugin-v0.7.3`](https://github.com/amy-bo/electroPioreactor/releases/tag/plugin-v0.7.3) with fresh card bundles (see its changelog for the latest), MIT licence |
| Source | [`pioreactor-electroPioreactor-plugin`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin), main code [`electropioreactor.py`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/pioreactor_electropioreactor_plugin/electropioreactor.py), history in [`CHANGELOG.md`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/CHANGELOG.md) |
| Job name | `electropioreactor` (shown as **electroPioreactor** under Activities) |
| Requires | Pioreactor software 26.5.0 or later |
| Hardware it drives | Electrode pair on an LED channel (default D); CO₂ solenoid on the PWM channel labelled `relay` (default 4) |
| Replaces | The AEP0.1.1 combination of `pioreactor-relay-plugin` and a hand-written experiment profile |

## What the job does

Once started, the job runs four timed behaviours together:

1. **Electrolysis.** It sets the electrode channel to `electrolysis_power` and cycles it ON for `electrolysis_on_seconds`, then OFF for `electrolysis_off_seconds`, repeating. An OFF time of 0 means continuous electrolysis.
2. **CO₂ sparging.** Every `sparge_interval_minutes` it opens the solenoid (100 % duty on the relay channel) for `sparge_duration_seconds`. The first sparge comes one full interval after the job starts.
3. **Electrolysis pause during each sparge.** The electrode channel goes to 0 for the sparge and comes back on as soon as the solenoid closes, if the cycle is in an ON phase.
4. **OD pausing.** It pauses Pioreactor's `od_reading` job around each sparge and, when electrolysis cycles (an OFF time above 0), around each electrolysis ON phase, by publishing a sleeping state to it, then wakes it again. If `od_reading` is not running, this does nothing.

The two OD pauses are independent and counted by owner: OD reading resumes only when neither a sparge nor an electrolysis phase still holds it paused.

**OD pause windows**, each measured from the start of the event:

  sparge window = `sparge_duration_seconds` + `od_pause_after_sparge_seconds`
  electrolysis window = `electrolysis_on_seconds` + `od_pause_after_electrolysis_seconds`

Both are floored at 0. The "after" offsets may be negative: a negative offset resumes OD before the event ends, and an offset of −(event length) or less disables that pause. Worked example with a 10 s ON phase:

| `od_pause_after_electrolysis_seconds` | Window | Behaviour |
| --- | --- | --- |
| +5 | 15 s | OD off for the 10 s ON phase plus 5 s to settle. Typical |
| 0 | 10 s | OD off for exactly the ON phase |
| −3 | 7 s | OD resumes 3 s before electrolysis ends |
| −10 or less | 0 | OD never paused for electrolysis |

> **Expert:** Continuous electrolysis (the default, `electrolysis_off_seconds = 0`) has no bubble-free gap to read in, so it does not pause OD: OD is read throughout, and paused only around each sparge plus its settle time. The electrolysis OD pause applies only when electrolysis cycles. OD then reads for `electrolysis_off_seconds` − `od_pause_after_electrolysis_seconds` in each cycle; if that is zero or less (for example ON 60 s, OFF 3 s, settle 5 s), OD never reads and the job logs a warning. Plugin versions 0.7.0 to 0.7.2 had a bug that kept OD paused for the whole run with the default settings; 0.7.3 fixes it. <!-- source: AEP-Plugin/CHANGELOG.md (v0.7.3); AEP-Plugin/README.md --> <!-- CHECK: v0.7.3 not yet hardware-tested; remove the Note below once it is -->

> **Note:** The 0.7.3 fix is not yet tested on hardware. The card bundles on the releases page carry 0.7.3. A unit still running 0.7.0 to 0.7.2 should be upgraded (see [Installing](#installing)); until then, with continuous electrolysis it needs `od_pause_after_electrolysis_seconds` set to −`electrolysis_on_seconds` or lower to read OD.

## Settings

Installation writes these defaults into `config.ini`. Every numeric setting can also be changed live in the job's **Settings** panel; a change applies from the next phase or cycle, not the one in progress. Live values are saved to the unit's own config files (`config_<unit>.ini` and `unit_config.ini`), so they survive a restart.

| Key | Default | Allowed values | Live? |
| --- | --- | --- | --- |
| `led_channel` | `D` | `A`, `B`, `C` or `D`; anything else stops the job at start with an error | No: hardware binding, read at start. Edit `config.ini` and restart the job |
| `electrolysis_power` | 2.5 % | 0 to 10 %. Higher values are clamped to 10; negative or non-finite values become 0 | Yes |
| `electrolysis_on_seconds` | 60 s | Greater than 0 | Yes |
| `electrolysis_off_seconds` | 0 s | 0 or more; 0 = continuous | Yes |
| `od_pause_after_electrolysis_seconds` | 5 s | Any finite number, negative allowed | Yes |
| `sparge_duration_seconds` | 10 s | Greater than 0 | Yes |
| `sparge_interval_minutes` | 60 min | Greater than 0; a change reschedules the next sparge | Yes |
| `od_pause_after_sparge_seconds` | 5 s | Any finite number, negative allowed | Yes |
| Reset to Defaults | off | A toggle: reloads every value above from `config.ini`, then switches itself off | Yes |

Settings that are not finite numbers, or out of range, are rejected rather than passed on to a timer. Choosing a sparge schedule for your culture is what the [gas model](/gas-model/) is for; the defaults above are starting points, not recommendations.

From the command line on the unit (each option falls back to `config.ini`):

```bash
pio run electropioreactor \
    --electrolysis-power 2.5 \
    --electrolysis-on-seconds 60 \
    --electrolysis-off-seconds 0 \
    --od-pause-after-electrolysis-seconds 5 \
    --sparge-duration-seconds 10 \
    --sparge-interval-minutes 60 \
    --od-pause-after-sparge-seconds 5
```

## Hardware channels

| Function | Default | How to change it |
| --- | --- | --- |
| Electrode pair | LED channel D, connector catch upwards | `[electropioreactor.config] led_channel` in `config.ini`, then restart the job |
| CO₂ solenoid | PWM 4, driven at 16 Hz | The job opens whichever PWM channel is labelled `relay`. Wire the solenoid to another channel and set, for example, `[PWM] 2 = relay` instead of `4 = relay` |

Neither channel is hard-coded, so the plugin does not assume a fixed channel is free. The full channel map for each variant is on the [specification page](/specifications/#channel-map): on the AEP, PWM 2 is the media pump and PWM 3 the waste pump; the MEP swaps them.

> **Safety:** The HAT's shunt connector must sit on the two pins closest to the LED outputs, with the 12 V supply in the barrel jack. Otherwise PWM channels 1 to 4 run from the Pi's own supply, the solenoid will not open, and sparging looks like a gas-train fault. Check **Manage → System → Voltage on PWM rail** reads about 12 V. <!-- source: docs/steps/step-03-raspberry-pi-and-hat.md, step-09 -->

## Installing

### From the SD card (offline)

This route needs no internet on the unit, which suits university networks. It relies on Pioreactor OS support for installing plugins from the card's boot partition; the AEP plugin's README notes this was [proposed upstream](https://github.com/Pioreactor/CustoPiZer/pull/21) and accepted by Pioreactor; Pioreactor's founder, Cam Davidson-Pilon, welcomed it on 24 September 2026. Until a Pioreactor OS release ships it, use the SSH route below. <!-- CHECK: AEP-Plugin/README.md says "until it ships, use the SSH route", while the AEP guide step 5 treats the card route as the main one; confirm the Pioreactor OS release that ships boot-partition plugin support -->

1. Follow Pioreactor's [software set-up guide](https://docs.pioreactor.com/user-guide/software-set-up) up to **Write**, with **Eject media when finished** switched off in Raspberry Pi Imager's App Options.
2. Download and unzip the [AEP card bundle](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/releases/latest/download/electroPioreactor-AEP-card-bundle.zip) (MEP: the [MEP card bundle](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/releases/latest/download/electroPioreactor-MEP-card-bundle.zip)).
3. When the write finishes, drag the bundle's `pioreactor` folder onto the card's `bootfs` drive. For a leader that makes its own Wi-Fi network, also copy `local_access_point`, with `GB` changed to your two-letter country code.
4. Boot. The plugin installs itself; the AEP bundle also installs the precision temperature plugin and sets the unit's model.

<figure>
<img src="/img/imager-app-options.png" alt="Raspberry Pi Imager's App Options dialog with Eject media when finished switched off and the Content Repository Edit button circled" width="1452" height="1056">
<figcaption>The one change to make in Raspberry Pi Imager for the card install: switch off "Eject media when finished", so the card stays mounted and the plugin can be dropped onto it.</figcaption>
</figure>

If **electroPioreactor** does not appear under Activities, put the card back in your computer: `pioreactor/plugins/failed/` on `bootfs` holds the wheel and a log of what went wrong. Full steps: [AEP guide, step 5](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) and the plugin [README](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/README.md#from-the-card).

### Over SSH (a running unit)

For a unit that is already running, or an OS release without card support. From the unzipped bundle's `pioreactor/plugins` folder, with `<hostname>` replaced by the unit's name:

```bash
scp *.whl pioreactor@<hostname>.local:
ssh pioreactor@<hostname>.local 'for w in *.whl; do n=${w%%-*}; /opt/pioreactor/venv/bin/pio plugins install ${n//_/-} --source "$w"; done'
```

Then refresh the web interface. On an older unit, run `pio update` first (26.5.0 is the minimum).

### What the installer changes

It adds `[PWM] 4 = relay` and an `[electropioreactor.config]` section with the defaults above to `config.ini`, keeping any values already there. If PWM 4 is already labelled something else it refuses rather than overwrite it. The stock Pioreactor default `4 = waste` is the common case: move any real waste pump to another channel, set PWM 4 to `relay` on the **Configuration** page, and install again. Source: [`patch-config-ini.py`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/scripts/patch-config-ini.py).

## After installing

| Check | Expected | Guide |
| --- | --- | --- |
| Activities list | Includes **electroPioreactor** (hard-refresh the page) | [Step 6](https://docs.electropioreactor.org/AEP/step-06-install-electropioreactor-plugin/) |
| Unit model in Inventory | Pioreactor 40 ml, XR variant (AEP0.2); until set, OD is read against the wrong channel map | [Step 5](https://docs.electropioreactor.org/AEP/step-05-pioreactor-software-setup/) |
| Clock | Matches your computer to the minute. An offline unit has no time source, so every timestamp would be wrong: set it with `sudo date` over SSH | [Step 6](https://docs.electropioreactor.org/AEP/step-06-install-electropioreactor-plugin/) |
| `config.ini` | `[PWM]` 1 `stirring`, 2 `media`, 3 `waste`, 4 `relay`, 5 `heating`, and an `[electropioreactor.config]` section | [Step 14](https://docs.electropioreactor.org/AEP/step-14-configure-sparging-and-electrolysis/) |

A unit with no internet can borrow it over an ethernet cable from a computer with Internet Sharing turned on ([Pioreactor's instructions](https://docs.pioreactor.com/user-guide/internet-sharing)).

## Calibration

| What | How | Guide |
| --- | --- | --- |
| Stirring | Pioreactor's stirring calibration | [MEP calibration](repo:MixedElectroPioreactor/Calibration.md) |
| Pumps | Pioreactor's pump calibration, on the 12 V supply, with a 0.1 g balance | [AEP step 10](https://docs.electropioreactor.org/AEP/step-10-calibrate-pumps/) |
| OD | Pioreactor's OD600 standard curve per unit, redone every 6 months or when the optics change; plus an OD blank at the start of each experiment | [MEP calibration](repo:MixedElectroPioreactor/Calibration.md) |
| Working volume | Weigh the vial; move the Media Out needle until it holds 30 ml (AEP0.2) with the pumps running | [AEP step 11](https://docs.electropioreactor.org/AEP/step-11-ports/) |
| Electrolysis | Start the job, raise power until bubbles form (about 3.5 %); expect about twice as many bubbles on the cathode; record the cell voltage (about 2.8 to 3.05 V at 3.5 %) and, if you can break into a lead, the current | [AEP step 8](https://docs.electropioreactor.org/AEP/step-08-test-electrolysis/) |
| CO₂ flow | Regulator at 1 bar, one gas outlet capped, the other into an inverted water-filled measuring cylinder; time it and adjust the needle valve | [AEP steps 15](https://docs.electropioreactor.org/AEP/step-15-set-up-co2-flow-test/) and [16](https://docs.electropioreactor.org/AEP/step-16-calibrate-co2-flow/) |
| Current against power setting | A sweep at 3, 5, 7 and 10 %, for the gas model | [`gerrit-current.md`](repo:Media/protocols/gerrit-current.md) |

Repeat the electrolysis voltage and current checks before and after each experiment; a significant change means recalibrating. <!-- source: MixedElectroPioreactor/Calibration.md -->

## Safety behaviour

| Protection | What the plugin does |
| --- | --- |
| Power clamp | Electrolysis power is limited to 10 % of the channel, to protect the electrodes. Only the job applies the clamp, so never drive the electrode channel by hand |
| Sparge interlock | Electrolysis is off for the whole of each sparge |
| Stop or pause | The job cancels its timers, closes the solenoid, turns the electrode channel off and resumes OD reading. Each step is attempted even if another fails |
| Disconnect | As above, and releases the PWM channel |
| Bad input | Non-finite or out-of-range timings are rejected; a bad LED channel stops the job at start |
| PWM lock | The job locks its solenoid channel while it runs |
| Manual override | Hardware, not software: the solenoid's override at 0 is normal (closed unpowered); at 1 the valve is always open |

> **Safety:** The plugin does not monitor gas composition. Electrolysis makes hydrogen and oxygen together, and the [gas model](/gas-model/)'s review found the headspace can become flammable just after inoculation. Do not leave a culture unattended from inoculation without a nitrogen sweep or hydrogen monitoring.

## Compatibility

| Item | Status |
| --- | --- |
| Pioreactor software | 26.5.0 or later. Earlier releases needed a UI patch; the plugin now simply requires 26.5.0 |
| AEP0.2 | Pioreactor 40 ml v1.5 with the XR kit, Raspberry Pi 5; AEP card bundle (includes the precision temperature plugin) |
| MEP | Pioreactor 20 ml; MEP card bundle (no temperature plugin); pumps on the opposite PWM channels |
| Clusters | Leader and worker images both work; on workers, the plugin installs when you add the unit from the leader's Inventory page |
| Data | Pioreactor logs every LED-channel change, so electrolysis power and timing appear in exports. Cell voltage and current are not logged: read them with a multimeter |

<!-- source: AEP-Plugin/CLAUDE.md (26.5.0 / PR 615), AEP-Plugin/README.md, Media/REVIEW-QA.md (logging) -->

## Troubleshooting

| Symptom | Likely cause and fix |
| --- | --- |
| **electroPioreactor** missing from Activities | Hard-refresh. Card route: read the log in `pioreactor/plugins/failed/` on `bootfs`. Running unit: `pio plugins list` should show `pioreactor-electropioreactor-plugin` |
| Install stops on `[PWM] 4 = 'waste'` | The stock default. Move any real waste pump, set PWM 4 to `relay` on the Configuration page, install again |
| `<hostname>.local` will not load | While the unit runs its own access point, join its `pioreactor` network and open `http://pioreactor.local` |
| Computer offers to reformat the card | Click Ignore: it cannot read the card's Linux partition |
| Solenoid never clicks | 12 V supply missing or HAT shunt in the wrong place; check the PWM rail reads about 12 V |
| Clicks but no bubbles | Cylinder pin, regulator or needle valve closed |
| No electrolysis bubbles | Electrodes not on LED channel D (catch upwards), plain water instead of medium, or job not started from Activities |
| Only a few slow bubbles | Raise **Electrolysis Power** in Settings, not the LED channel by hand |
| More bubbles on the anode than the cathode | Leads reversed: stop the job and put red on the anode, black on the cathode |
| Job refuses to start | Check `led_channel` is A, B, C or D and the timings are positive numbers |
| OD trace flat or missing while the job runs | Plugin 0.7.0 to 0.7.2 with continuous electrolysis: update the plugin, or see the note under [What the job does](#what-the-job-does). With cycling, make the OFF time longer than the electrolysis settle time; the job log warns if OD can never read |
| An OD-pause change seems ignored | It applies from the next cycle |
| Unit misbehaves before electrolysis starts | Run a self test from **Manage**; power-cycle if it hangs |

## For developers

```bash
git clone https://github.com/amy-bo/pioreactor-electroPioreactor-plugin.git
cd pioreactor-electroPioreactor-plugin
pip install -e ".[dev]"
pytest tests/        # off-device: the tests stub the pioreactor package
```

The design notes for electrolysis cycling are in [`DESIGN-electrolysis-cycling.md`](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/blob/main/DESIGN-electrolysis-cycling.md). Issues and pull requests are welcome on [the plugin repository](https://github.com/amy-bo/pioreactor-electroPioreactor-plugin/issues); questions on the [forum](https://forum.amybo.org). Our fixes to Pioreactor's own software go upstream through our [amy-bo/pioreactor](https://github.com/amy-bo/pioreactor) and [amy-bo/CustoPiZer](https://github.com/amy-bo/CustoPiZer) forks. Common questions: [FAQ](/faq/).
