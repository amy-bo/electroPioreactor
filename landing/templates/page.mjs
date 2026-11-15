// Content page: /<slug>/index.html from landing/content/<slug>.md.
import { esc, head, siteHeader, siteFooter, SITE_JS } from './layout.mjs';
import { SITE } from './site.mjs';

export function card(p) {
  return `<li><a class="card" href="/${p.slug}/">
    <span class="card-title">${esc(p.title)}</span>
    <span class="card-desc">${esc(p.description)}</span>
    <span class="card-go" aria-hidden="true">Read →</span>
  </a></li>`;
}

function pager(prev, next) {
  if (!prev && !next) return '';
  const a = (p, rel, label) => p
    ? `<a class="pager-${rel}" href="/${p.slug}/" rel="${rel}"><span>${label}</span><b>${esc(p.title)}</b></a>`
    : '<span></span>';
  return `<nav class="pager" aria-label="Other pages">${a(prev, 'prev', '← Previous')}${a(next, 'next', 'Next →')}</nav>`;
}

export function contentPage({ page, prev, next, built }) {
  const base = '../';
  return `${head({ title: page.title, description: page.description, urlPath: `/${page.slug}/`, base })}
<body class="page">
<a class="skip" href="#main">Skip to content</a>
${siteHeader({ base, current: page.slug })}
<div class="page-wrap">
  <main id="main" class="page-main">
    <header class="page-head">
      <h1>${esc(page.title)}</h1>
      ${page.description ? `<p class="lede">${esc(page.description)}</p>` : ''}
    </header>
    <article class="prose">
${page.html}
    </article>
    ${pager(prev, next)}
    <p class="page-src"><a href="${SITE.repoBlob}landing/content/${encodeURIComponent(page.slug)}.md">View the source of this page on GitHub</a></p>
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
