// Content page: /<slug>/index.html from landing/content/<slug>.md, and section index pages.
import { esc, head, siteHeader, siteFooter, SITE_JS } from './layout.mjs';
import { SITE, SECTIONS, AUDIENCE } from './site.mjs';

export function badge(audience) {
  const a = AUDIENCE[audience] || AUDIENCE.everyone;
  return `<span class="badge badge-${esc(audience || 'everyone')}" title="${esc(a.long)}">${esc(a.label)}</span>`;
}

export function card(p) {
  return `<li><a class="card" href="/${p.slug}/">
    <span class="card-top"><span class="card-sec">${esc(SECTIONS[p.section]?.title || '')}</span>${badge(p.audience)}</span>
    <span class="card-title">${esc(p.title)}</span>
    <span class="card-desc">${esc(p.description)}</span>
    <span class="card-go" aria-hidden="true">Read →</span>
  </a></li>`;
}

function toc(headings) {
  const items = headings.filter((h) => h.depth === 2 || h.depth === 3);
  if (items.filter((h) => h.depth === 2).length < 3) return '';
  return `<nav class="toc" aria-labelledby="toc-h">
    <details open>
      <summary id="toc-h">On this page</summary>
      <ol>${items.map((h) => `<li class="toc-${h.depth}"><a href="#${h.id}">${h.text}</a></li>`).join('')}</ol>
    </details>
  </nav>`;
}

function pager(prev, next) {
  if (!prev && !next) return '';
  const a = (p, rel, label) => p
    ? `<a class="pager-${rel}" href="/${p.slug}/" rel="${rel}"><span>${label}</span><b>${esc(p.title)}</b></a>`
    : '<span></span>';
  return `<nav class="pager" aria-label="More in this section">${a(prev, 'prev', '← Previous')}${a(next, 'next', 'Next →')}</nav>`;
}

export function contentPage({ page, prev, next, built, children = [] }) {
  const base = '../';
  const sec = SECTIONS[page.section];
  const secLink = SITE.sectionHref[page.section];
  const t = toc(page.headings);
  return `${head({ title: page.title, description: page.description, urlPath: `/${page.slug}/`, base })}
<body class="page">
<a class="skip" href="#main">Skip to content</a>
${siteHeader({ base, current: page.section })}
<div class="page-wrap${t ? ' has-toc' : ''}">
  <main id="main" class="page-main">
    <header class="page-head">
      <p class="crumbs">${sec && secLink !== `/${page.slug}/` ? `<a href="${secLink}">${esc(sec.title)}</a><span aria-hidden="true">/</span>` : ''}${badge(page.audience)}</p>
      <h1>${esc(page.title)}</h1>
      ${page.description ? `<p class="lede">${esc(page.description)}</p>` : ''}
    </header>
    ${t ? `<div class="toc-inline">${t.replace('<details open>', '<details>')}</div>` : ''}
    <article class="prose">
${page.html}
    </article>
    ${children.length ? `<section class="section-list" aria-labelledby="sl-h"><h2 id="sl-h">In this section</h2><ul class="cards">${children.map(card).join('')}</ul></section>` : ''}
    ${pager(prev, next)}
    <p class="page-src"><a href="${SITE.repoBlob}landing/content/${encodeURIComponent(page.slug)}.md">View the source of this page on GitHub</a></p>
  </main>
  ${t ? `<aside class="toc-side">${t}</aside>` : ''}
</div>
${siteFooter({ base, built })}
${SITE_JS(base)}
</body>
</html>
`;
}

export function sectionPage({ id, pages, built }) {
  const base = '../';
  const sec = SECTIONS[id];
  return `${head({ title: sec.title, description: sec.blurb, urlPath: `/${id}/`, base })}
<body class="page">
<a class="skip" href="#main">Skip to content</a>
${siteHeader({ base, current: id })}
<div class="page-wrap">
  <main id="main" class="page-main page-wide">
    <header class="page-head">
      <h1>${esc(sec.title)}</h1>
      <p class="lede">${esc(sec.blurb)}</p>
    </header>
    ${pages.length ? `<ul class="cards">${pages.map(card).join('')}</ul>` : '<p>Pages for this section are being written.</p>'}
  </main>
</div>
${siteFooter({ base, built })}
${SITE_JS(base)}
</body>
</html>
`;
}

export function notFoundPage({ built, pages }) {
  const base = '/';
  return `${head({ title: 'Page not found', description: 'This page does not exist.', urlPath: '/404.html', base })}
<body class="page">
<a class="skip" href="#main">Skip to content</a>
${siteHeader({ base })}
<div class="page-wrap">
  <main id="main" class="page-main page-wide">
    <header class="page-head">
      <p class="crumbs"><span class="badge">404</span></p>
      <h1>Page not found</h1>
      <p class="lede">There is no page at this address. It may have moved. The assembly instructions live in the <a href="${SITE.guide}">assembly video guide</a>.</p>
    </header>
    <p><a class="btn btn-primary" href="/">Go to the home page</a></p>
    ${pages.length ? `<h2>Pages on this site</h2><ul class="cards">${pages.map(card).join('')}</ul>` : ''}
  </main>
</div>
${siteFooter({ base, built })}
${SITE_JS(base)}
</body>
</html>
`;
}
