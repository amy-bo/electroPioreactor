# Media

Manifests (`<id>.yaml`, one per video or photo) are only written for media that exists in this repository as committed files. None does yet: the assembly instructions embed external images (GitHub user-attachments) at Method steps 1.6, 8.1, 8.2, 8.3 and 8.5, which are not ingested. When a clip or photo is committed, its manifest must declare the components it shows as `hero` pins (`<component id>@<design_version>`), so the site can flag it stale when a component changes.

## Shoot list

For each step, the hero components a future clip or photo must declare (ids as in `../components/`):

| Step | Hero components | Notes |
| --- | --- | --- |
| step-00-before-you-start | — | Tools flat-lay optional: phillips-ph0-screwdriver, gas-cylinder-wrench, vernier-callipers, cryogenic-gloves |
| step-01-connect-dovetail-platforms | pumping-dovetail-platform, gl45-bottle-holder, co2-cylinder-dovetail-holder | Replaces the external raft photo (README 1.6); show dovetails to front and left and the SD-card cutout (1.7) |
| step-02-press-the-raft-together | pumping-dovetail-platform, gl45-bottle-holder, co2-cylinder-dovetail-holder | The finished raft sitting flat (photo-01-raft); second half of vid-02-platform-setup once cut |
| step-03-raspberry-pi-and-hat | raspberry-pi, pioreactor-40ml | The shunt connector on the two pins closest to the LED outputs, and on the wrong pair, for the check |
| step-04-vial-holder-and-xr | pioreactor-40ml, xr-upgrade-kit, precision-temperature-upgrade-kit | Only the AEP-specific choices (skip v1.5 optics, XR parts kept aside); the four eye-spy positions labelled; the upstream guide covers the rest |
| step-05-pioreactor-software-setup | — | Screen capture: Inventory model = XR, config.ini channel values |
| step-06-install-electropioreactor-plugin | — | Screen capture of the plugin install |
| step-07-set-up-electrolysis | vial-cap, silicone-septum, mmo-anode, stainless-steel-cathode, ring-terminal, thumb-screw | Red to anode, black to cathode in frame; electrode tops flush with the cap |
| step-08-test-electrolysis | vial-cap, mmo-anode, stainless-steel-cathode | Bubbles on the cathode vs anode |
| step-09-set-up-nutrient-solution-flow | peristaltic-pump, gl45-bottle, gl45-cap, silicone-tubing | Pump leads in PWM 2 and 3 |
| step-10-calibrate-pumps | peristaltic-pump | Vial on the balance at 30 ml |
| step-11-ports | vial-cap, needle-75mm-304 | Top-down of the eight ports, labelled |
| step-12-co2-gas-train | co2-regulator, regulator-outlet-o-ring, reducing-nipple, solenoid-valve, co2-needle-valve, blanking-plug, cylinder-regulator-adapter | Replaces the four external photos (README 8.1, 8.2, 8.3, 8.5); manual override at 0; pin backed off before tightening |
| step-13-admit-co2 | co2-regulator, hydrophobic-vent-filter, anode-feed-tube | Vent filters on the CO₂ inlet and gas outlets; the solenoid lead in PWM 4 |
| step-14-configure-sparging-and-electrolysis | solenoid-valve | Screen capture of the Settings panel plus the solenoid opening |
| step-15-set-up-co2-flow-test | co2-regulator | Outlet gauge at 1 bar; one outlet capped, the other into the measuring cylinder |
| step-16-calibrate-co2-flow | co2-needle-valve | Measuring cylinder over water |
| step-17-sterilise | — | Pending the approved procedure |
