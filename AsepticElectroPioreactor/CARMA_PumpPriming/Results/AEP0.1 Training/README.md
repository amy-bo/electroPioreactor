# Joint in-person training

## Time & Location

Initial in-person training was provided by AMYBO's Dr Martin Currie for both Imperial College and Edinburgh students at Edinburgh University's Chris French Laboratory from 18-21 November 2025.
<!-- TODO: let me know if you'd like your names mentioned here and I'll add them, we could also link to our LinkedIn profiles or link-in-bios if you like | assignee: @Bingqiao @Amir @Teo -->

## Assembly and Calibration

### Procedure

The main focus of the training was assembly and calibration of three AEP0.1 prototypes following the [AEP0.1_Assembly.md](AsepticElectroPioreactor/CARMA_PumpPriming/Assembly/AEP0.1_Assembly.md) guide.  One prototype was assembled by each of the three students.

### Software issues

Following the documented software installation, we were unable to SSH into the AEPs.  This issue took a long time to diagnose and required consultation with Labcrafter and Pioreactor.  We conflated the issue with a trivial LED not lighting issue which was resolved by Pioreactor in that day's nightly Pioreactor software build. Cameron Davidson-Pilon of Pioreactor found that it was due to an [issue with the Raspberry Pi Imager](https://github.com/raspberrypi/rpi-imager/issues/1170) which was resolved by using an earlier version of the Imager.

## Media

Media was made up as per [MediaFormulation.md 2025-11-12](https://github.com/amy-bo/electroPioreactor/blob/ba442ae67962f1ee57649e94e9f0302e0077b55f/Media/MediaFormulation.md) <!-- TODO: insert variations from MediaFormulation.md 2025-11-12 | assignee: @Bingqiao or anyone who noted details -->.

Versions were sterilised by autoclaving and by filter sterilisation.
<!-- TODO: define filter type - was it 0.2 μm? what material? | assignee: @Bingqiao or anyone who noted details -->
<!-- TODO: detail the media discolouration and precipitation issues | assignee: @Bingqiao or anyone who noted details -->

## Heterotrophic culture

A heterotrophic culture of Cupriavidus metallidurans was established using the above Media plus gluconic acid (sodium salt) as the carbon and energy source.

<!-- TODO: insert results | assignee: @Bingqiao or anyone who noted them -->

## Sparging

The system was set up for continuous sparging of CO₂, however this presented three issues:

### Water in CO₂ lines

The bubble counters, when set up as per manufacturers instructions, resulted in rising bubbles passing water into the downstream CO₂ lines.  This was unacceptable as over time it would impact the hydrophobic gas filters.

Various configurations were discussed and a number of them tested.  Replacing the distilled water with mineral oil improved the situation, but still required a restrictively low gas flow to ensure no mineral oil entered the downstream CO₂ lines.

### Oxygen purging

The low flow rates of CO₂ made the

### Optical Density Measurement

## Electrode Discolouration

## Other Issues

### Vial Fragility

One of the [vials](https://labcrafter.co.uk/products/20ml-glass-vial-cap-s-with-ports-and-stir-bar) dropped and smashed. It would be prudent to carry boxed spares of critical components.

### Vial Cap O-Ring Dislodgement

The vial cap o-rings tended to fall out, making aseptic technique difficult.  This inspired a vial cap [design improvement](https://github.com/amy-bo/electroPioreactor/commit/88e3c8db04196599436d371a5588a67b8afb526a) with a lip to retain the o-ring.
