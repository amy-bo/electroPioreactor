#!/usr/bin/env node
// Usage: node build-viewer.mjs <partsDir> <out.html> [template]
//        node build-viewer.mjs <built viewer.html> <out.html> [template]   re-template, keeping its parts
import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";

const [partsDir, outFile, tplArg] = process.argv.slice(2);
if (!partsDir || !outFile) {
  console.error("usage: node build-viewer.mjs <partsDir> <out.html> [template]");
  process.exit(2);
}
const here = path.dirname(fileURLToPath(import.meta.url));
const tplPath = tplArg || path.join(here, "viewer.template.html");
const PARTS = "/*__PARTS__*/{}", META = "/*__META__*/{}";

let tpl;
try { tpl = fs.readFileSync(tplPath, "utf8"); }
catch (e) { console.error(`error: cannot read template ${tplPath}: ${e.message}`); process.exit(1); }
for (const p of [PARTS, META]) {
  if (!tpl.includes(p)) { console.error(`error: template ${tplPath} lacks placeholder ${p}`); process.exit(1); }
}

let parts, meta;
if (partsDir.endsWith(".html")) {           // reuse the parts already embedded in a built viewer
  const built = fs.readFileSync(partsDir, "utf8");
  const grab = (k) => { const m = built.match(new RegExp(`const ${k} = (\\{.*?\\});\\n`)); if (!m) { console.error(`error: no ${k} in ${partsDir}`); process.exit(1); } return JSON.parse(m[1]); };
  parts = grab("PARTS"); meta = grab("META");
} else {
  let names;
  try {
    names = fs.readdirSync(partsDir).filter((f) => f.endsWith(".stl")).map((f) => f.slice(0, -4)).sort();
  } catch (e) { console.error(`error: cannot read ${partsDir}: ${e.message}`); process.exit(1); }
  if (!names.length) { console.error(`error: no .stl files in ${partsDir}`); process.exit(1); }

  parts = {};
  for (const n of names) {
    const raw = fs.readFileSync(path.join(partsDir, n + ".stl"));
    if (!raw.length) { console.error(`error: ${n}.stl is empty`); process.exit(1); }
    parts[n] = zlib.gzipSync(raw, { level: 9 }).toString("base64");
  }
  meta = { built: new Date().toISOString(), parts: names };
}
const names = Object.keys(parts);
// Function replacers: avoid "$&"-style special patterns in replacement strings.
const html = tpl.replace(PARTS, () => JSON.stringify(parts)).replace(META, () => JSON.stringify(meta));
fs.writeFileSync(outFile, html);
const mb = fs.statSync(outFile).size / 1048576;
console.log(`wrote ${outFile}: ${mb.toFixed(2)} MB, ${names.length} parts`);
if (mb > 15) console.warn(`warning: output is ${mb.toFixed(1)} MB (> 15 MB)`);
