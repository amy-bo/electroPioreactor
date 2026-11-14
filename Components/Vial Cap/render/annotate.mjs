// Annotated A4 portrait page for the Vial Cap render: title, subtitle, callouts with
// leader lines, and a short "how it works" footer. One layout, two outputs:
//   - a PDF with real (vector, searchable) text over the render
//   - an HTML/SVG page of the same layout, to screenshot as a PNG
//
// usage: node annotate.mjs <render.png> <out.pdf> <out.html>
// needs: npm i pdf-lib @pdf-lib/fontkit @expo-google-fonts/ibm-plex-sans
//
// The callout anchors are pixel positions on the default "#still&white" Assembly
// render at 1697 x 2400; re-check them if the camera, parts or render size change.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { PDFDocument, rgb } from 'pdf-lib';
import fontkit from '@pdf-lib/fontkit';
import { TITLE, SUBTITLE, CALLOUTS as CALLOUTS_TEXT, FOOTER } from './callouts.mjs';

const require = createRequire(import.meta.url);
const [pngPath, pdfPath, htmlPath] = process.argv.slice(2);
if (!pngPath || !pdfPath || !htmlPath) { console.error('usage: node annotate.mjs <render.png> <out.pdf> <out.html>'); process.exit(1); }

const fontDir = path.dirname(require.resolve('@expo-google-fonts/ibm-plex-sans/package.json'));
const FONT = {
  regular: fs.readFileSync(path.join(fontDir, '400Regular/IBMPlexSans_400Regular.ttf')),
  semibold: fs.readFileSync(path.join(fontDir, '600SemiBold/IBMPlexSans_600SemiBold.ttf')),
  bold: fs.readFileSync(path.join(fontDir, '700Bold/IBMPlexSans_700Bold.ttf')),
};

// ---- page + palette (pt; A4 portrait) -------------------------------
const W = 595.28, H = 841.89, M = 34;
const C = { ink: '#15181d', body: '#3a414b', muted: '#6b7480', line: '#7d8794', accent: '#0e6b66', dot: '#0e6b66' };
const PX_W = 1697, PX_H = 2400;                 // render size the anchors refer to
const k = W / PX_W;                             // px -> pt (the render fills the page)
const disp = (x, y) => [x * 1.2 * k, y * 1.2 * k];   // anchors read off a 1414 x 2000 preview

// ---- content ---------------------------------------------------------
// anchors: pixel positions on a 1414 x 2000 preview of the render, by callout id
const ANCHOR = {
  needles: [655, 455], port: [668, 905], medium: [612, 1195], temp: [548, 1226], cathode: [672, 1345],
  pd: [572, 1455], flea: [690, 1612], gas: [838, 318], screws: [902, 728], cap: [860, 905],
  anode: [762, 1250], co2: [758, 1405], led: [888, 1482], heater: [745, 1708],
};
const CALLOUTS = CALLOUTS_TEXT.map((c) => [c.side, disp(...ANCHOR[c.id]), c.head, c.body]);

// ---- type --------------------------------------------------------------
const T = {
  title: { font: 'bold', size: 22, color: C.ink },
  subtitle: { font: 'regular', size: 13, color: C.accent },
  head: { font: 'semibold', size: 8.4, color: C.ink, lead: 10.4 },
  body: { font: 'regular', size: 7.6, color: C.body, lead: 9.6 },
  footer: { font: 'regular', size: 8.6, color: C.body, lead: 11.6 },
};
const COL_W = 152;                      // callout text width
const COL_X = { L: M, R: W - M - COL_W };
const GAP = 9;                          // min gap between callouts
const TOP_LIMIT = 92, BOTTOM_LIMIT = 742;

// ---- layout (font-metric wrapping, shared by both outputs) ----------------
const pdf = await PDFDocument.create();
pdf.registerFontkit(fontkit);
const F = {};
for (const [n, b] of Object.entries(FONT)) F[n] = await pdf.embedFont(b, { subset: true });
const width = (s, st) => F[st.font].widthOfTextAtSize(s, st.size);
function wrap(text, st, w) {
  const out = []; let line = '';
  for (const word of text.split(/\s+/)) {
    const t = line ? line + ' ' + word : word;
    if (width(t, st) <= w || !line) line = t; else { out.push(line); line = word; }
  }
  if (line) out.push(line);
  return out;
}

const blocks = CALLOUTS.map(([side, anchor, head, body]) => {
  const hl = wrap(head, T.head, COL_W), bl = wrap(body, T.body, COL_W);
  const h = hl.length * T.head.lead + bl.length * T.body.lead;
  return { side, anchor, hl, bl, h, top: anchor[1] - T.head.lead * 0.7 };   // heading's first line level with the anchor
});
for (const side of ['L', 'R']) {                       // stack each column without overlaps, keeping order
  const col = blocks.filter((b) => b.side === side).sort((a, b) => a.anchor[1] - b.anchor[1]);
  let y = TOP_LIMIT;
  for (const b of col) { b.top = Math.max(b.top, y); y = b.top + b.h + GAP; }
  let over = y - GAP - BOTTOM_LIMIT;                   // too low: push the stack back up
  for (let i = col.length - 1; i >= 0 && over > 0; i--) {
    const b = col[i]; const floor = i ? col[i - 1].top + col[i - 1].h + GAP : TOP_LIMIT;
    const move = Math.min(over, b.top - floor); b.top -= move; over -= move;
    for (let j = i + 1; j < col.length; j++) col[j].top = Math.max(col[j].top - move, col[j - 1].top + col[j - 1].h + GAP);
  }
}

// primitives in top-left page coordinates (pt)
const P = { texts: [], lines: [], dots: [] };
const text = (s, x, y, st) => P.texts.push({ s, x, y, st });
text(TITLE, M, M + 20, T.title);
text(SUBTITLE, M, M + 39, T.subtitle);
for (const b of blocks) {
  const x = COL_X[b.side];
  let y = b.top + T.head.size;
  for (const l of b.hl) { text(l, x, y, T.head); y += T.head.lead; }
  y += T.body.lead - T.head.lead;
  for (const l of b.bl) { text(l, x, y, T.body); y += T.body.lead; }
  // leader: from beside the heading, a short level stub, then straight to the anchor
  const ly = b.top + T.head.size * 0.62;
  const hw = Math.max(...b.hl.map((l) => width(l, T.head)));
  const x0 = b.side === 'L' ? x + Math.min(COL_W, hw) + 4 : x - 4;
  const x1 = b.side === 'L' ? Math.max(x0 + 6, COL_X.L + COL_W + 8) : Math.min(x0 - 6, COL_X.R - 8);
  P.lines.push([[x0, ly], [x1, ly], b.anchor]);
  P.dots.push(b.anchor);
}
const footLines = wrap(FOOTER, T.footer, W - 2 * M);
let fy = H - M - footLines.length * T.footer.lead + T.footer.size;
P.lines.push([[M, fy - T.footer.size - 9], [W - M, fy - T.footer.size - 9]]);   // rule above the footer
for (const l of footLines) { text(l, M, fy, T.footer); fy += T.footer.lead; }

// ---- PDF -----------------------------------------------------------------
const hex = (h) => rgb(parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255);
const page = pdf.addPage([W, H]);
const png = await pdf.embedPng(fs.readFileSync(pngPath));
page.drawImage(png, { x: 0, y: 0, width: W, height: W * png.height / png.width });
for (const pts of P.lines) for (let i = 1; i < pts.length; i++)
  page.drawLine({ start: { x: pts[i - 1][0], y: H - pts[i - 1][1] }, end: { x: pts[i][0], y: H - pts[i][1] }, thickness: pts.length > 2 ? 0.55 : 0.4, color: hex(pts.length > 2 ? C.line : '#c9ced5') });
for (const [x, y] of P.dots) {
  page.drawCircle({ x, y: H - y, size: 2.3, color: rgb(1, 1, 1) });
  page.drawCircle({ x, y: H - y, size: 1.5, color: hex(C.dot) });
}
for (const t of P.texts) page.drawText(t.s, { x: t.x, y: H - t.y, size: t.st.size, font: F[t.st.font], color: hex(t.st.color) });
pdf.setTitle(`${TITLE}: ${SUBTITLE}`);
pdf.setAuthor('electroPioreactor project');
fs.writeFileSync(pdfPath, await pdf.save());

// ---- HTML/SVG (same layout) for a PNG screenshot ----------------------------
const ff = (n, b) => `@font-face{font-family:Plex;font-weight:${n};src:url(data:font/ttf;base64,${b.toString('base64')}) format("truetype")}`;
const fw = { regular: 400, semibold: 600, bold: 700 };
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const svg = [
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="100%" height="100%">`,
  `<image href="data:image/png;base64,${fs.readFileSync(pngPath).toString('base64')}" x="0" y="0" width="${W}" height="${W * PX_H / PX_W}"/>`,
  ...P.lines.map((pts) => `<polyline points="${pts.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${pts.length > 2 ? C.line : '#c9ced5'}" stroke-width="${pts.length > 2 ? 0.55 : 0.4}"/>`),
  ...P.dots.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="2.3" fill="#fff"/><circle cx="${x}" cy="${y}" r="1.5" fill="${C.dot}"/>`),
  ...P.texts.map((t) => `<text x="${t.x}" y="${t.y}" font-family="Plex" font-weight="${fw[t.st.font]}" font-size="${t.st.size}" fill="${t.st.color}">${esc(t.s)}</text>`),
  '</svg>',
].join('\n');
fs.writeFileSync(htmlPath, `<!doctype html><html><head><meta charset="utf-8"><title>${esc(TITLE)}</title><style>${Object.entries(FONT).map(([n, b]) => ff(fw[n], b)).join('')}html,body{margin:0;height:100%;background:#fff}svg{display:block}</style></head><body>${svg}<div id="ok"></div></body></html>`);
console.log('wrote', pdfPath, 'and', htmlPath);
