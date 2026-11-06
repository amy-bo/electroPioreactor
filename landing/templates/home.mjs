// Home page pieces: the hero overlay that replaces the viewer's own title, the "How it works"
// panel + hotspot layer over the 3D model, and the sections below the hero.
import { esc, amyboTile } from './layout.mjs';
import { SITE } from './site.mjs';
import { card } from './page.mjs';

const ext = '<span class="ext" aria-hidden="true">↗</span>';

// Every claim here is checked against AsepticElectroPioreactor/README.md and README.md.
export const INTRO = 'The Aseptic electroPioreactor (AEP) adapts a <a href="https://pioreactor.com">Pioreactor</a> into a sealed bioreactor for research on hydrogen-oxidising bacteria (HOB). Electrodes in the culture split water into hydrogen and oxygen only as they are needed, so the bacteria can turn CO₂ into biomass without stored hydrogen. The designs, bill of materials and assembly guide are open on GitHub.';

export function heroHeader({ base, learnHref }) {
  return `<header class="title landing">
      <h1>Aseptic electroPioreactor</h1>
      <p class="sub">AEP0.2 · open hardware for hydrogen-oxidising bacteria</p>
      <p class="hero-intro">${INTRO}</p>
      <a class="cta" href="${SITE.guide}">Assembly Video Guide <span aria-hidden="true">→</span></a>
      <ul class="hero-links">
        <li><a href="${learnHref}">Learn how it works</a></li>
        <li><a href="${SITE.github}">GitHub ${ext}</a></li>
      </ul>
      <a class="by-amybo" href="${SITE.amybo}"><span class="by-k">Developed by</span>${amyboTile(base, 'sm')}<span class="by-n">AMYBO</span></a>
      <p class="hint" id="heroHint">Drag to turn the vial · click it, then scroll to zoom</p>
      <p class="built" id="built" hidden></p>
    </header>`;
}

// The numbered hotspots and the panel that lists them; home.js positions and wires them.
export function hotspots({ callouts, learnHref }) {
  const dots = callouts.map((c, i) => `<button class="hs-dot" type="button" data-id="${esc(c.id)}" data-n="${i + 1}" aria-describedby="hs-label" aria-label="${i + 1}. ${esc(c.head)}" hidden>${i + 1}</button>`).join('');
  const items = callouts.map((c, i) => `<li><button class="hiw-item" type="button" data-id="${esc(c.id)}" aria-pressed="false">
        <span class="hiw-n" aria-hidden="true">${i + 1}</span>
        <span class="hiw-t"><b>${esc(c.head)}</b><span>${esc(c.body)}</span></span>
      </button></li>`).join('');
  return `<div class="hs-layer" id="hsLayer" aria-hidden="false">${dots}<div class="hs-label" id="hs-label" role="tooltip" hidden></div></div>
  <div class="hiw-tools" id="hiwTools">
    <button class="hiw-pill" id="hiwToggle" type="button" aria-expanded="false" aria-controls="hiwPanel">How it works <span class="hiw-count">${callouts.length}</span></button>
    <button class="hiw-pill hiw-dots" id="dotsToggle" type="button" aria-pressed="true" title="Show or hide the numbers on the model"><span class="hiw-led" aria-hidden="true"></span>Numbers</button>
  </div>
  <section class="hiw-panel" id="hiwPanel" aria-labelledby="hiwTitle" hidden>
    <div class="hiw-head">
      <h2 id="hiwTitle">How it works</h2>
      <button class="hiw-close" id="hiwClose" type="button" aria-label="Close the How it works panel">×</button>
    </div>
    <p class="hiw-intro">Pick a part to turn the model towards it. The numbers match the dots on the vial.</p>
    <ol class="hiw-list" id="hiwList">
      ${items}
    </ol>
    ${learnHref && learnHref.startsWith('/') ? `<p class="hiw-more"><a href="${learnHref}">Read the full guide: How it works →</a></p>` : ''}
  </section>`;
}

export function belowFold({ learn, build, base, aboutHref }) {
  const group = (id, kicker, title, blurb, pages, more) => `<section class="home-group" aria-labelledby="${id}">
      <div class="home-group-head">
        <p class="kicker">${kicker}</p>
        <h2 id="${id}">${title}</h2>
        <p>${blurb}</p>
      </div>
      ${pages.length ? `<ul class="cards">${pages.map(card).join('')}</ul>` : '<p class="muted">Pages coming soon.</p>'}
      ${more || ''}
    </section>`;
  return `<main id="explore" class="home-main">
  <div class="home-in">
    <section class="home-intro-mobile" aria-label="Introduction">
      <p>${INTRO}</p>
    </section>
    ${group('g-new', 'New to this?', 'Start with the basics', 'What hydrogen-oxidising bacteria are, why grow them with electricity, and how the vial on this page works. No background needed.', learn)}
    ${group('g-pro', 'For researchers and builders', 'Specifications, models and research', 'Design details, the gas and electrolysis model, media, software and variants, with links into the repository and the assembly guide.', build, `<p class="group-more"><a class="btn btn-primary" href="${SITE.guide}">Open the Assembly Video Guide <span aria-hidden="true">→</span></a></p>`)}
    <section class="key-links" aria-labelledby="g-links">
      <h2 id="g-links" class="sr-only">Key links</h2>
      <ul>
        <li><a href="${SITE.guide}"><b>Assembly guide</b><span>Step-by-step videos for AEP0.2</span></a></li>
        <li><a href="${SITE.github}"><b>GitHub</b><span>Designs, BoM, plugin, data</span></a></li>
        <li><a href="${SITE.radicle}"><b>Radicle</b><span>The same repository, peer to peer</span></a></li>
        <li><a href="${SITE.forum}"><b>Forum</b><span>Questions and build reports</span></a></li>
        <li><a href="${SITE.bibliography}"><b>Bibliography</b><span>HOB fermentation by in-culture electrolysis</span></a></li>
      </ul>
    </section>
    <section class="partners" aria-labelledby="g-partners">
      <h2 id="g-partners" class="kicker">Funding and partners</h2>
      <p>The Aseptic electroPioreactor is funded by <a href="${SITE.carma}">CARMA Hub Pump Priming</a>, led by <a href="${SITE.imperial}">Dr Sonja Billerbeck</a> (Imperial College London) and <a href="${SITE.edinburgh}">Prof. Chris French</a> (University of Edinburgh), with <a href="${SITE.amybo}">AMYBO</a> as designer and trainer and <a href="${SITE.labcrafter}">LabCrafter</a> as the UK vendor.${aboutHref ? ` <a href="${aboutHref}">More about the project</a>.` : ''}</p>
    </section>
  </div>
</main>`;
}
