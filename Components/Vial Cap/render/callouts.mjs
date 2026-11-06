// Callout wording shared by the A4 page (annotate.mjs) and the website (landing/build.mjs).
// Edit here; both rebuild from it. `id` keys each callout's anchor in those scripts.
export const TITLE = 'Aseptic electroPioreactor AEP0.2';
export const SUBTITLE = 'Vial components';
export const CALLOUTS = [
  { id: 'needles', side: 'L', head: 'Media In and Media Out needles', body: 'Fresh medium is pumped in. The Media Out tip sets the 30 ml level and removes culture as the Pioreactor doses.' },
  { id: 'port', side: 'L', head: 'Inoculation port', body: 'A syringe goes straight through the self-sealing silicone septum.' },
  { id: 'medium', side: 'L', head: 'Culture medium, 30 ml', body: 'Hydrogen-oxidising bacteria fix CO₂ using the H₂ and O₂ made in the culture.' },
  { id: 'temp', side: 'L', head: 'Precision temperature sensor', body: 'An MLX90632 infrared thermometer reads the culture through the glass, without contact.' },
  { id: 'cathode', side: 'L', head: 'Cathode: 316 stainless steel', body: 'Electrolysis makes fine H₂ bubbles here, the bacteria’s energy source.' },
  { id: 'pd', side: 'L', head: 'Photodiodes (Pioreactor XR)', body: 'Read scattered infrared light at 45°, 90° and 135°, plus a reference, to track growth as optical density.' },
  { id: 'flea', side: 'L', head: 'Magnetic stir flea', body: 'Keeps the culture mixed and the gases dissolving.' },
  { id: 'gas', side: 'R', head: 'Gas outlets', body: 'Two bent needles vent spent gas from above the liquid.' },
  { id: 'screws', side: 'R', head: 'Knurled thumb screws', body: 'Clamp the power leads to the electrodes: red to the anode, black to the cathode.' },
  { id: 'cap', side: 'R', head: 'One-piece vial cap', body: '3D-printed in PC-CF. One silicone septum seals the vial, both electrodes and every port, and the cap sets the electrode depth.' },
  { id: 'anode', side: 'R', head: 'Anode: hollow MMO-coated titanium', body: 'Electrolysis makes O₂ on its surface. CO₂ is fed down its bore.' },
  { id: 'co2', side: 'R', head: 'CO₂ bubbles', body: 'Rise from the anode’s open base, supplying carbon and sweeping O₂ bubbles off the anode.' },
  { id: 'led', side: 'R', head: 'IR LED and light path', body: 'Infrared light crosses the culture below the electrodes (drawn in red; invisible in life).' },
  { id: 'heater', side: 'R', head: 'Heater PCB', body: 'An aluminium-core heater under the vial holds the set temperature.' },
];
export const FOOTER = 'In-culture electrolysis makes hydrogen and oxygen only as they are needed, so hydrogen-oxidising bacteria can turn CO₂ into biomass without stored hydrogen. The Pioreactor runs dosing, stirring, heating, optical density, electrolysis and CO₂ sparging automatically.';
