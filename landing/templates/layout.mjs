// Shared page chrome: <head>, site header, site footer.
// Every page gets `base`: the relative path back to the site root ('' on /, '../' on /slug/),
// used for assets so dist/ also renders straight from disk (file://) for screenshots.
import { SITE } from './site.mjs';

export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

export const FONTS = `<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">`;

const ext = '<span class="ext" aria-hidden="true">↗</span>';

export function head({ title, description, urlPath, base, extra = '' }) {
  const full = title ? `${title} · ${SITE.name}` : `${SITE.name} · ${SITE.tagline}`;
  const canonical = SITE.origin + urlPath;
  return `<!doctype html>
<html lang="en"${urlPath === '/' ? ' class="home"' : ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(full)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${canonical}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0c121c" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#fbfbf9" media="(prefers-color-scheme: light)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(SITE.name)}">
<meta property="og:title" content="${esc(title || SITE.longName)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${canonical}">
<meta property="og:image" content="${SITE.origin}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The AEP0.2 vial and cap rendered on a dark studio background">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="${base}favicon.svg" type="image/svg+xml">
${FONTS}
<link rel="stylesheet" href="${base}assets/site.css">
${extra}
</head>`;
}

// `current` is the active section id (learn/build/research/about) for aria-current.
export function siteHeader({ base, current = '', overHero = false }) {
  const link = (id, label) => {
    const href = SITE.sectionHref[id];
    return `<li><a href="${href}"${current === id ? ' aria-current="page"' : ''}>${label}</a></li>`;
  };
  return `<header class="site-header${overHero ? ' over-hero' : ''}">
  <div class="site-header-in">
    <a class="brand" href="/" aria-label="${esc(SITE.name)} home">
      <img src="${base}favicon.svg" alt="" width="26" height="26">
      <span>electro<b>Pioreactor</b></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="menu-icon" aria-hidden="true"><i></i><i></i><i></i></span><span class="menu-label">Menu</span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
        ${link('learn', 'Learn')}
        ${link('build', 'Build')}
        ${link('research', 'Research')}
        ${link('about', 'About')}
        <li class="nav-ext"><a href="${SITE.guide}">Assembly guide ${ext}</a></li>
        <li class="nav-ext"><a href="${SITE.github}">GitHub ${ext}</a></li>
      </ul>
    </nav>
  </div>
</header>`;
}

export function amyboTile(base, size = 'sm') {
  return `<span class="amybo-tile amybo-${size}"><img src="${base}assets/amybo-logo.png" alt="AMYBO" width="400" height="400"></span>`;
}

export function siteFooter({ base, built }) {
  return `<footer class="site-footer">
  <div class="site-footer-in">
    <div class="foot-brand">
      <a class="foot-amybo" href="${SITE.amybo}">
        ${amyboTile(base, 'md')}
        <span><span class="foot-kicker">Developed by</span> AMYBO</span>
      </a>
      <p>The electroPioreactor is open hardware for research on hydrogen-oxidising bacteria (HOB), made by AMYBO. The Aseptic variant is developed with Imperial College London and the University of Edinburgh.</p>
      <p class="funding">Funded by <a href="${SITE.carma}">CARMA Hub Pump Priming</a>.</p>
    </div>
    <nav class="foot-cols" aria-label="Footer">
      <div>
        <h2>Project</h2>
        <ul>
          <li><a href="${SITE.sectionHref.learn}">Learn</a></li>
          <li><a href="${SITE.sectionHref.build}">Build</a></li>
          <li><a href="${SITE.sectionHref.research}">Research</a></li>
          <li><a href="${SITE.sectionHref.about}">About</a></li>
        </ul>
      </div>
      <div>
        <h2>Elsewhere</h2>
        <ul>
          <li><a href="${SITE.guide}">Assembly guide ${ext}</a></li>
          <li><a href="${SITE.github}">GitHub ${ext}</a></li>
          <li><a href="${SITE.radicle}">Radicle ${ext}</a></li>
          <li><a href="${SITE.forum}">Forum ${ext}</a></li>
          <li><a href="${SITE.bibliography}">Bibliography ${ext}</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="mailto:${SITE.email}">${SITE.email}</a></li>
          <li><a href="${SITE.amybo}">amybo.org ${ext}</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <p class="foot-meta"><span>electropioreactor.org · an AMYBO project</span><span>Last built ${esc(built)}</span></p>
</footer>`;
}

export const SITE_JS = (base) => `<script src="${base}assets/site.js" defer></script>`;
