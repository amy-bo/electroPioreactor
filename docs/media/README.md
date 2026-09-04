# Media

Manifests (`<id>.yaml`, one per video or photo) are only written for media that exists in this repository as committed files. None does yet: the assembly instructions embed external images (GitHub user-attachments) at Method steps 1.6, 8.1, 8.2, 8.3 and 8.5, which are not ingested. When a clip or photo is committed, its manifest must declare the components it shows as `hero` pins (`<component id>@<design_version>`), so the site can flag it stale when a component changes.

## Shoot list

For each step, the hero components a future clip or photo must declare (ids as in `../components/`):

| Step | Hero components | Notes |
| --- | --- | --- |
| step-00-before-you-start | — | Tools flat-lay optional: phillips-ph0-screwdriver, gas-cylinder-wrench, vernier-callipers, cryogenic-gloves |
| step-01-connect-dovetail-platforms | pumping-dovetail-platform, gl45-bottle-holder, co2-cylinder-dovetail-holder | Replaces the external raft photo (README 1.6); show dovetails to front and left and the SD-card cutout (1.7) |
| step-02-pioreactor-hardware-setup | pioreactor-40ml, xr-upgrade-kit, precision-temperature-upgrade-kit, raspberry-pi | Only the AEP-specific choices (skip v1.5 optics, XR parts kept aside); the upstream guide covers the rest |
| step-03-pioreactor-software-setup | — | Screen capture: Inventory model = XR, config.ini channel values |
| step-04-install-electropioreactor-plugin | — | Screen capture of the plugin install |
| step-05-set-up-electrolysis | vial-cap, silicone-septum, mmo-anode, stainless-steel-cathode, ring-terminal, thumb-screw | Red to anode, black to cathode in frame; bubbles on the cathode vs anode |
| step-06-set-up-nutrient-solution-flow | peristaltic-pump, gl45-bottle, gl45-cap, silicone-tubing | Vial on the balance at 30 ml |
| step-07-ports | vial-cap, needle-port | Top-down of the eight ports, labelled |
| step-08-set-up-co2-sparging | co2-regulator, regulator-outlet-o-ring, reducing-nipple, solenoid-valve, co2-needle-valve, blanking-plug, cylinder-regulator-adapter, hydrophobic-vent-filter, anode-feed-tube | Replaces the four external photos (README 8.1, 8.2, 8.3, 8.5); manual override at 0; pin backed off before tightening |
| step-09-configure-sparging-and-electrolysis | solenoid-valve | Screen capture of the Settings panel plus the solenoid opening |
| step-10-calibrate-co2-flow | co2-needle-valve, co2-regulator | Measuring cylinder over water |
| step-11-sterilise | — | Pending the approved procedure |
