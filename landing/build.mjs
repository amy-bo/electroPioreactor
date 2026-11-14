// electropioreactor.org: static site generator.
//
//   Home (/)            the Vial Cap 3D viewer as a full-screen hero, with hover labels on the parts
//                       and a guided tour (wording from Components/Vial Cap/render/callouts.mjs),
//                       then cards to the content pages.
//   Content (/<slug>/)  every landing/content/<slug>.md (files starting with "_" are skipped).
//   Sections            /learn/ /build/ /research/ /about/ list their pages (a content page whose slug
//                       is the section name replaces the generated index and gets the list appended).
//   Also                404.html, sitemap.xml, robots.txt, _redirects, _headers, og.jpg, favicon.
//
// usage (from the repo root):
//   cd landing && npm install          # once: marked + gray-matter
//   node landing/build.mjs [--viewer path/to/viewer.html] [--no-strict] [--examples]
//     --viewer      defaults to "Components/Vial Cap/render/renders/Vial Cap viewer.html"
//                   (made by Components/Vial Cap/render/build-viewer.mjs)
//     --no-strict   report broken internal links / missing repo: paths as warnings, not errors
//     --examples    also build content files whose names start with "_" (generator testing)
//   Writes landing/dist/.
//
// preview:  npx serve landing/dist          (or: npx wrangler pages dev landing/dist)
// deploy (Mac, from the repo root; Cloudflare Pages Direct Upload):
//   npx wrangler pages deploy landing/dist --project-name electropioreactor-home --branch main --commit-dirty=true
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import matter from 'gray-matter';
import { Marked } from 'marked';
import { SITE, SECTIONS, AUDIENCE, BRANCH } from './templates/site.mjs';
import { esc, head, siteHeader, siteFooter, SITE_JS } from './templates/layout.mjs';
import { contentPage, sectionPage, notFoundPage } from './templates/page.mjs';
import { heroHeader, tourMarkup, belowFold } from './templates/home.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.dirname(here);
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : undefined; };
const STRICT = !flag('--no-strict');
const EXAMPLES = flag('--examples');
const viewerPath = opt('--viewer') || (args[0] && !args[0].startsWith('--') ? args[0] : null)
  || path.join(repo, 'Components/Vial Cap/render/renders/Vial Cap viewer.html');
const calloutsPath = path.join(repo, 'Components/Vial Cap/render/callouts.mjs');
const contentDir = path.join(here, 'content');
const out = path.join(here, 'dist');
const built = new Date().toISOString().slice(0, 10);

const problems = [];
const problem = (msg) => problems.push(msg);
const die = (msg) => { console.error('error: ' + msg); process.exit(1); };

// ------------------------------------------------------------------ content
const RESERVED = new Set(['assets', 'img', '404', 'index', 'favicon.svg', 'og.jpg']);
const slugify = (s) => String(s).toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z0-9#]+;/g, '')
  .replace(/[^\p{L}\p{N}\s-]/gu, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-') || 'section';
const plain = (html) => html.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

function repoUrl(p) {
  // repo:<path> -> GitHub blob (file) or tree (directory) on BRANCH; "#anchor" kept
  let [file, hash = ''] = p.split('#');
  let decoded;
  try { decoded = decodeURIComponent(file); } catch { decoded = file; }
  decoded = decoded.replace(/^\.?\//, '');
  const abs = path.join(repo, decoded);
  let isDir = decoded.endsWith('/') || decoded === '';
  if (fs.existsSync(abs)) isDir = fs.statSync(abs).isDirectory();
  else problem(`repo: link to a path that does not exist on this branch: ${decoded}`);
  const enc = decoded.replace(/\/$/, '').split('/').map(encodeURIComponent).join('/');
  return (isDir ? SITE.repoTree : SITE.repoBlob) + enc + (hash ? '#' + hash : '');
}

const CALLOUT_KINDS = { note: 'Note', tip: 'Tip', safety: 'Safety', expert: 'Expert' };

function renderMarkdown(md, slug) {
  const headings = [];
  const used = new Set();
  const marked = new Marked({ gfm: true });
  marked.use({
    renderer: {
      heading({ tokens, depth }) {
        const inner = this.parser.parseInline(tokens);
        let id = slugify(plain(inner)), k = 2;
        while (used.has(id)) id = `${slugify(plain(inner))}-${k++}`;
        used.add(id);
        headings.push({ depth, id, text: inner.replace(/<a [^>]*>|<\/a>/g, '') });
        if (depth === 1) problem(`${slug}.md: uses a level-1 heading ("${plain(inner)}"); the page title is the h1, start at ##`);
        return `<h${depth} id="${id}"><a class="anchor" href="#${id}" aria-hidden="true" tabindex="-1">#</a>${inner}</h${depth}>\n`;
      },
      blockquote({ tokens }) {
        const body = this.parser.parse(tokens);
        const m = /^<p><strong>(Note|Tip|Safety|Expert):?<\/strong>:?\s*/i.exec(body);
        if (!m) return `<blockquote>\n${body}</blockquote>\n`;
        const kind = m[1].toLowerCase();
        return `<aside class="callout callout-${kind}" role="note" aria-label="${CALLOUT_KINDS[kind]}">
<p class="callout-title"><span class="callout-icon" aria-hidden="true"></span>${CALLOUT_KINDS[kind]}</p>
<p>${body.slice(m[0].length)}</aside>\n`;
      },
    },
  });
  let html = marked.parse(md);
  html = html
    .replace(/<!--[\s\S]*?-->/g, '')                                         // source/CHECK notes stay in the .md
    .replace(/(href|src)="repo:([^"]*)"/g, (_, a, p) => `${a}="${repoUrl(p)}"`)
    .replace(/<table>/g, '<div class="table-wrap" tabindex="0"><table>').replace(/<\/table>/g, '</table></div>')
    .replace(/src="(?:\.\/)?img\//g, 'src="/img/')                          // img/x.png and /img/x.png both work
    .replace(/<img /g, '<img loading="lazy" decoding="async" ')
    .replace(/<p>\s*<\/p>\n?/g, '');
  return { html, headings };
}

function loadContent() {
  if (!fs.existsSync(contentDir)) return [];
  const pages = [];
  for (const f of fs.readdirSync(contentDir).sort()) {
    if (!f.endsWith('.md')) continue;
    if (f.startsWith('_') && !EXAMPLES) continue;
    const slug = f.slice(0, -3).replace(/^_/, '');
    if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) die(`content file name must be a lowercase slug: ${f}`);
    if (RESERVED.has(slug)) die(`content slug "${slug}" is reserved`);
    const { data, content } = matter(fs.readFileSync(path.join(contentDir, f), 'utf8'));
    if (!data.title) die(`${f}: front matter needs a title`);
    const section = String(data.section || '').trim();
    if (!SECTIONS[section]) die(`${f}: section must be one of ${Object.keys(SECTIONS).join(', ')} (got "${section}")`);
    const audience = String(data.audience || 'everyone').trim();
    if (!AUDIENCE[audience]) die(`${f}: audience must be one of ${Object.keys(AUDIENCE).join(', ')} (got "${audience}")`);
    if (!data.description) problem(`${f}: front matter has no description (used for cards and <meta>)`);
    const { html, headings } = renderMarkdown(content, slug);
    pages.push({
      slug, file: f, title: String(data.title), description: String(data.description || ''),
      section, audience, order: Number.isFinite(+data.order) ? +data.order : 100, html, headings,
    });
  }
  const bySec = (a, b) => Object.keys(SECTIONS).indexOf(a.section) - Object.keys(SECTIONS).indexOf(b.section)
    || a.order - b.order || a.title.localeCompare(b.title);
  return pages.sort(bySec);
}

// ------------------------------------------------------------------ viewer (home hero)
function loadViewer() {
  if (!fs.existsSync(viewerPath)) die(`viewer not found: ${viewerPath} (build it with Components/Vial Cap/render/build-viewer.mjs)`);
  let v = fs.readFileSync(viewerPath, 'utf8');
  const need = (re, what) => { if (!re.test(v)) die(`viewer lacks ${what}`); };
  need(/<header class="title">[\s\S]*?<\/header>/, '<header class="title">');
  need(/<style>[\s\S]*?<\/style>/, '<style>');
  need(/<div id="tip"/, '<div id="tip">');
  need(/<div id="stage"/, '<div id="stage">');
  v = v.replace(/<title>[\s\S]*?<\/title>\s*/, '').replace(/<meta name="claude:[^>]*>\s*/g, '')
    .replace(/<link rel="preconnect"[^>]*>\s*/g, '').replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>\s*/g, '');
  const style = /<style>[\s\S]*?<\/style>/.exec(v)[0];
  v = v.replace(style, '');

  // Until the viewer exposes window.__viewer itself, add the same hooks here (the shape the
  // viewer template is adopting): window.__viewer, a "viewer-ready" event, __viewerFrameHooks.
  if (!v.includes('__viewer')) {
    const loop = 'renderer.setAnimationLoop(frame);';
    const render = /composer\.render\(dt\);\n\}/;
    if (v.split(loop).length === 2 && render.test(v)) {
      v = v.replace(render, `composer.render(dt);\n  for (const f of (window.__viewerFrameHooks || [])) { try { f(dt); } catch (e) { console.error(e); } }\n}`);
      v = v.replace(loop, `${loop}
  let __loopOn = true;
  window.__viewer = { THREE, scene, camera, renderer, controls, root, meshes, goView, setTurn, liquid: LIQUID,
    animate(on) { if (on === __loopOn) return; __loopOn = on; renderer.setAnimationLoop(on ? frame : null); } };
  window.dispatchEvent(new Event('viewer-ready'));`);
      console.log('note: viewer has no window.__viewer yet; added a build-time shim');
    } else {
      problem('viewer has no window.__viewer and the shim could not be applied: hotspots will not show');
    }
  }
  return { style, body: v };
}

// ------------------------------------------------------------------ pages
function homePage({ pages, callouts }) {
  const base = '';
  const viewer = loadViewer();
  const has = (s) => pages.some((p) => p.slug === s);
  const learnHref = has('how-it-works') ? '/how-it-works/' : '#explore';
  let body = viewer.body
    .replace(/<header class="title">[\s\S]*?<\/header>/, () => heroHeader({ base, learnHref }))
    // the site's Dark / Light / Auto switch replaces the viewer's own white-background toggle
    .replace(/\s*<button[^>]*id="whiteBtn"[^>]*>[\s\S]*?<\/button>/, '')
    .replace(/<div class="view-wrap">/, () => `<button class="tour-btn" id="tourBtn" type="button"><span aria-hidden="true">▶</span> Tour</button>\n      <div class="view-wrap">`)
    .replace(/<div id="tip"/, () => `${tourMarkup()}\n  <a class="scroll-cue" href="#explore" aria-label="Scroll to explore the project"><span>Explore</span><i aria-hidden="true"></i></a>\n\n  <div id="tip"`);
  const learn = pages.filter((p) => p.section === 'learn');
  const build = pages.filter((p) => p.section === 'build' || p.section === 'research');
  const description = 'The Aseptic electroPioreactor (AEP0.2): open hardware that grows hydrogen-oxidising bacteria on CO₂ with in-culture electrolysis. Interactive 3D model, how it works, and the assembly video guide.';
  return `${head({ title: '', description, urlPath: '/', base, extra: `${viewer.style}\n<link rel="stylesheet" href="assets/home.css">` })}
<body class="home-body">
<a class="skip" href="#explore">Skip the 3D model</a>
${siteHeader({ base, overHero: true })}
${body}
${belowFold({ learn, build, base, aboutHref: has('about') ? '/about/' : null })}
${siteFooter({ base, built })}
<script type="application/json" id="callouts-data">${JSON.stringify(callouts).replace(/</g, '\\u003c')}</script>
<script src="assets/home.js" defer></script>
${SITE_JS(base)}
</body>
</html>
`;
}

// ------------------------------------------------------------------ link check
function checkLinks(files, pages) {
  const ok = new Set(['/', '/404.html', '/sitemap.xml', '/robots.txt', '/og.jpg', '/favicon.svg']);
  for (const p of pages) ok.add(`/${p.slug}/`);
  for (const s of Object.keys(SECTIONS)) ok.add(`/${s}/`);
  for (const [file, html] of files) {
    for (const m of html.matchAll(/(?:href|src)="(\/[^"#?]*)/g)) {
      const u = m[1];
      if (ok.has(u) || u.startsWith('//')) continue;
      if (/^\/(img|assets)\//.test(u) && fs.existsSync(path.join(out, decodeURIComponent(u)))) continue;
      if (!u.endsWith('/') && ok.has(u + '/')) { problem(`${file}: link ${u} should end with "/" (${u}/)`); continue; }
      problem(`${file}: broken internal link ${u}`);
    }
  }
}

// ------------------------------------------------------------------ go
const { EXPLAINER, EXPLAINER_TITLE, EXPLAINER_LEAD, NUTSHELL } = await import(pathToFileURL(calloutsPath).href);
if (!Array.isArray(EXPLAINER) || !EXPLAINER.length) die(`no EXPLAINER in ${calloutsPath}`);
// hover labels + tour, all in Martin's explainer wording: an overview, the 12 parts in process order, the nutshell
const callouts = {
  parts: EXPLAINER.map(({ id, kind, head: h, body }) => ({ id, kind, head: h, body })),
  tour: [
    { id: 'overview', head: EXPLAINER_TITLE, body: EXPLAINER_LEAD },
    ...EXPLAINER.map(({ id, kind, head: h, body }) => ({ id, kind, head: h, body })),
    { id: 'nutshell', head: 'In a nutshell', rows: NUTSHELL },
  ],
};

const pages = loadContent();
fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
// copy by read/write (not cpSync): on some mounted file systems cpSync carries odd modes (e.g. --w-------)
const copyDir = (from, to) => {
  if (!fs.existsSync(from)) return;
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    if (e.name.startsWith('.')) continue;
    const a = path.join(from, e.name), b = path.join(to, e.name);
    if (e.isDirectory()) copyDir(a, b); else fs.writeFileSync(b, fs.readFileSync(a));
  }
};
copyDir(path.join(here, 'static'), out);
copyDir(path.join(here, 'assets'), path.join(out, 'assets'));
copyDir(path.join(contentDir, 'img'), path.join(out, 'img'));
fs.writeFileSync(path.join(out, 'favicon.svg'), fs.readFileSync(path.join(repo, 'site/public/favicon.svg')));
for (const f of fs.existsSync(path.join(out, 'img')) ? fs.readdirSync(path.join(out, 'img')) : []) {
  const kb = fs.statSync(path.join(out, 'img', f)).size / 1024;
  if (kb > 400) problem(`content/img/${f} is ${kb.toFixed(0)} KB; keep images under ~300 KB`);
}

const files = new Map();   // dist-relative path -> html
const write = (rel, html) => { files.set(rel, html); };

// rewrite site-root image paths in content to page-relative ones so dist/ also works from disk
const relImgs = (html, base) => html.replace(/src="\/(img\/[^"]+)"/g, `src="${base}$1"`);

const secPages = (id) => pages.filter((p) => p.section === id);
for (const p of pages) {
  const sib = secPages(p.section).filter((q) => q.slug !== p.section);
  const i = sib.indexOf(p);
  const children = p.slug === p.section ? sib : [];
  const html = contentPage({ page: p, prev: i > 0 ? sib[i - 1] : null, next: i >= 0 && i < sib.length - 1 ? sib[i + 1] : null, built, children });
  files.set(`${p.slug}/index.html`, html);
}
for (const id of Object.keys(SECTIONS)) {
  if (pages.some((p) => p.slug === id)) continue;
  files.set(`${id}/index.html`, sectionPage({ id, pages: secPages(id), built }));
}
files.set('index.html', homePage({ pages, callouts }));
files.set('404.html', notFoundPage({ built, pages: pages.filter((p) => p.audience !== 'expert').slice(0, 6) }));

// image references must exist (checked against the copied files, before rewriting)
for (const [file, html] of files) {
  for (const m of html.matchAll(/src="\/(img\/[^"]+)"/g)) {
    if (!fs.existsSync(path.join(out, decodeURIComponent(m[1])))) problem(`${file}: missing image /${m[1]} (put it in landing/content/img/)`);
  }
}
checkLinks(files, pages);
for (const [rel, html] of files) {
  const depth = rel.split('/').length - 1;
  const outHtml = rel === '404.html' ? html : relImgs(html, '../'.repeat(depth));
  fs.mkdirSync(path.dirname(path.join(out, rel)), { recursive: true });
  fs.writeFileSync(path.join(out, rel), outHtml);
}

// sitemap, robots, Cloudflare Pages config
const urls = ['/', ...Object.keys(SECTIONS).filter((s) => !pages.some((p) => p.slug === s)).map((s) => `/${s}/`), ...pages.map((p) => `/${p.slug}/`)];
fs.writeFileSync(path.join(out, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((u) => `  <url><loc>${SITE.origin}${u}</loc><lastmod>${built}</lastmod></url>`).join('\n')}
</urlset>
`);
fs.writeFileSync(path.join(out, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${SITE.origin}/sitemap.xml\n`);
fs.writeFileSync(path.join(out, '_redirects'), `/guide ${SITE.guide} 302\n/AEP ${SITE.guide} 301\n/AEP/* https://docs.electropioreactor.org/AEP/:splat 301\n`);
fs.writeFileSync(path.join(out, '_headers'), `/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/assets/*
  Cache-Control: public, max-age=3600
/img/*
  Cache-Control: public, max-age=86400
`);

const errs = problems.length;
for (const p of problems) console.error((STRICT ? 'error: ' : 'warning: ') + p);
console.log(`wrote ${out}: home + ${pages.length} content page(s) [${pages.map((p) => p.slug).join(', ')}], branch ${BRANCH}`);
if (errs && STRICT) { console.error(`${errs} problem(s); fix them or build with --no-strict`); process.exit(1); }
