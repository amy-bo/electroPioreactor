// Home page pieces: the hero overlay that replaces the viewer's own title, the tour card
// over the 3D model, and the sections below the hero.
import { esc, amyboTile } from './layout.mjs';
import { SITE } from './site.mjs';
import { card } from './page.mjs';

const ext = '<span class="ext" aria-hidden="true">↗</span>';

// All wording comes from landing/content/home.md (`home`: title, strapline, button, intro, more).
export function heroHeader({ base, learnHref, home }) {
  return `<header class="title landing">
      <h1>${esc(home.title)}</h1>
      <p class="sub">${esc(home.strapline)}</p>
      <p class="hero-intro">${home.intro}</p>
      <a class="cta" href="${SITE.guide}">${esc(home.button)} <span aria-hidden="true">→</span></a>
      <ul class="hero-links">
        <li><a href="${learnHref}">Learn how it works</a></li>
        <li><a href="${SITE.github}">GitHub ${ext}</a></li>
      </ul>
      <a class="by-amybo" href="${SITE.amybo}"><span class="by-k">Developed by</span>${amyboTile(base, 'sm')}<span class="by-n">AMYBO</span></a>
      <p class="hint" id="heroHint">Drag to turn · hover a part · click, then scroll to zoom</p>
      <p class="built" id="built" hidden></p>
    </header>`;
}

// The tour card; home.js fills it from the callouts data and drives the camera.
export function tourMarkup() {
  return `<section class="tour" id="tour" aria-labelledby="tourTitle" hidden>
    <p class="tour-n" id="tourN"></p>
    <h2 id="tourTitle"></h2>
    <div class="tour-body" id="tourBody" aria-live="polite"></div>
    <div class="tour-nav">
      <button type="button" id="tourPrev" aria-label="Previous">←</button>
      <button type="button" id="tourNext" class="tour-next">Next →</button>
      <button type="button" id="tourClose" class="tour-close" aria-label="End the tour">×</button>
    </div>
  </section>`;
}

export function belowFold({ pages, home }) {
  return `<main id="explore" class="home-main">
  <div class="home-in">
    <section class="home-intro-mobile" aria-label="Introduction">
      <p>${home.intro}</p>
    </section>
    <section class="home-group" aria-labelledby="g-pages">
      <div class="home-group-head">
        <h2 id="g-pages">${esc(home.pagesHeading)}</h2>
      </div>
      <ul class="cards">${pages.map(card).join('')}</ul>
      <p class="group-more"><a class="btn btn-primary" href="${SITE.guide}">${esc(home.button)} <span aria-hidden="true">→</span></a></p>
    </section>
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
    ${home.more ? `<section class="partners prose-lite">${home.more}</section>` : ''}
  </div>
</main>`;
}
