// node build.mjs [out.html]  -> one self-contained, offline presentation file
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import * as esbuild from 'esbuild';

const here = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(here, '..');
const TPL = path.join(REPO, 'Components/Vial Cap/render/viewer.template.html');
const BUILT = path.join(REPO, 'Components/Vial Cap/render/renders/Vial Cap viewer.html');
const AMY = here;
const out = process.argv[2] || path.join(here, 'AEP0.2 presentation.html');

const tpl = fs.readFileSync(TPL, 'utf8');
const built = fs.readFileSync(BUILT, 'utf8');
const PARTS = built.match(/const PARTS = (\{.*?\});\n/)[1];

// earlier-version parts: STL (ASCII or binary) -> binary -> gzip -> base64
function toBinary(buf) {
  const head = buf.slice(0, 5).toString();
  if (head !== 'solid' || !buf.toString('latin1', 0, Math.min(buf.length, 4000)).includes('facet')) return buf;
  const v = [...buf.toString().matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g)].map((m) => [+m[1], +m[2], +m[3]]);
  const n = v.length / 3, b = Buffer.alloc(84 + n * 50);
  b.writeUInt32LE(n, 80);
  for (let i = 0; i < n; i++) {
    const o = 84 + i * 50;
    for (let k = 0; k < 3; k++) { const p = v[i * 3 + k]; b.writeFloatLE(p[0], o + 12 + k * 12); b.writeFloatLE(p[1], o + 16 + k * 12); b.writeFloatLE(p[2], o + 20 + k * 12); }
  }
  return b;
}
const EXTRA = {};
for (const n of ['cap5', 'cap6', 'spacer', 'topstop01', 'topstop011', 'eyespy_pcb', 'eyespy_conn', 'eyespy_parts', 'pinch']) {
  EXTRA[n] = zlib.gzipSync(toBinary(fs.readFileSync(path.join(here, 'stl', n + '.stl'))), { level: 9 }).toString('base64');
}

// engine: viewer module + presentation, bundled with three.js so it runs offline
const main = fs.readFileSync(path.join(here, 'src/main.js'), 'utf8')
  .replace('//__PRESENT__', () => fs.readFileSync(path.join(here, 'src/present.js'), 'utf8'));
fs.writeFileSync(path.join(here, 'src/_entry.js'), main);
const bundle = await esbuild.build({
  entryPoints: [path.join(here, 'src/_entry.js')], bundle: true, format: 'esm', minify: true, write: false,
  alias: { 'three/addons': path.join(here, 'node_modules/three/examples/jsm') }, nodePaths: [path.join(here, 'node_modules')],
  logLevel: 'warning',
});
const js = bundle.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');

const b64 = (f, type) => `data:${type};base64,${fs.readFileSync(f).toString('base64')}`;
const web = fs.readFileSync(path.join(here, 'src/web.html'), 'utf8')
  .replace('__LOGO__', b64(path.join(AMY, 'assets/amybo_dark.svg'), 'image/svg+xml'))
  .replace('__FOREST__', b64(path.join(AMY, 'assets/free-forest.jpg'), 'image/jpeg'))
  .replace('__EVENTWEBM__', b64(path.join(AMY, 'assets/video/event-header.webm'), 'video/webm'))
  .replace('__EVENTVIDEO__', b64(path.join(AMY, 'assets/video/event-header.mp4'), 'video/mp4'))
  .replace('__EVENTPOSTER__', b64(path.join(AMY, 'assets/video/event-header-poster.jpg'), 'image/jpeg'));   // amybo.org/events/2026-11-13-london header
// photo steps: assets/photos/<key>.(jpg|png); a key with no file simply has no step
const PHOTO_DIR = path.join(AMY, 'assets/photos'), PHOTOS = {};
for (const f of fs.existsSync(PHOTO_DIR) ? fs.readdirSync(PHOTO_DIR) : []) {
  const m = f.match(/^(.+)\.(jpe?g|png)$/i); if (m) PHOTOS[m[1]] = b64(path.join(PHOTO_DIR, f), m[2].toLowerCase() === 'png' ? 'image/png' : 'image/jpeg');
}
const cams = fs.existsSync(path.join(here, 'cams.json')) ? fs.readFileSync(path.join(here, 'cams.json'), 'utf8') : '{}';

let html = tpl
  .replace(/<title>[^<]*<\/title>/, '<title>AMYBO · electroPioreactor</title>')
  .replace('</style>', () => fs.readFileSync(path.join(here, 'src/present.css'), 'utf8') + '\n</style>')
  .replace(/<script type="importmap">[\s\S]*?<\/script>\s*<script type="module">[\s\S]*?<\/script>/, () =>
    `<script type="application/json" id="parts-data">${PARTS}</script>\n` +
    `<script type="application/json" id="extra-data">${JSON.stringify(EXTRA)}</script>\n` +
    `<script type="application/json" id="cams-data">${cams}</script>\n` +
    `<script type="application/json" id="photos-data">${JSON.stringify(PHOTOS)}</script>\n` +
    `<script type="module">${js}</script>`)
  .replace(/<div id="tip"/, () => web + '\n<div id="tip"');
fs.writeFileSync(out, html);
console.log(`wrote ${out}: ${(fs.statSync(out).size / 1048576).toFixed(1)} MB`);
