// Home page pieces: the hero overlay that replaces the viewer's own title, the hotspot layer
// over the 3D model, and the sections below the hero.
import { esc, amyboTile } from './layout.mjs';
import { SITE } from './site.mjs';
import { card } from './page.mjs';

const ext = '<span class="ext" aria-hidden="true">↗</span>';

// First sentence is Martin's, from the AEP0.2 explainer.
export const INTRO = 'A sealed, open-source electro-bioreactor that uses renewable electricity to grow protein-rich bacteria from water and carbon dioxide. It\u2019s built on the <a href="https://pioreactor.com">Pioreactor</a>, and the designs, bill of materials and assembly guide are all on GitHub.';

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
      <p class="hint" id="heroHint">Drag to turn · hover the dots · click, then scroll to zoom</p>
      <p class="built" id="built" hidden></p>
    </header>`;
}

// The hotspots on the model, coloured by the explainer's key; home.js positions and wires them.
export function hotspots({ callouts }) {
  const dots = callouts.map((c) => `<button class="hs-dot k-${esc(c.kind || 'control')}" type="button" data-id="${esc(c.id)}" aria-describedby="hs-label" aria-label="${esc(c.head)}" hidden></button>`).join('');
  return `<div class="hs-layer" id="hsLayer" aria-hidden="false">${dots}<div class="hs-label" id="hs-label" role="tooltip" hidden></div></div>`;
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
    ${group('g-new', 'Learn', 'The basics', 'What hydrogen-oxidising bacteria are, why we grow them with electricity, and how the vial works.', learn)}
    ${group('g-pro', 'Build and research', 'The detail', 'Specs, the gas and electrolysis model, media, software and variants, linked to the repository and the assembly guide.', build, `<p class="group-more"><a class="btn btn-primary" href="${SITE.guide}">Open the Assembly Video Guide <span aria-hidden="true">→</span></a></p>`)}
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
