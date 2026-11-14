// node landing/build.mjs --watch
// Rebuilds landing/dist/ whenever a file in landing/content, landing/templates, landing/assets or
// the callouts file changes, serves it at http://localhost:4321 and reloads the open browser tab.
// Builds are --no-strict, so a broken link is reported in the terminal without stopping the preview.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.join(here, 'dist');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.xml': 'application/xml', '.txt': 'text/plain' };
const RELOAD = `<script>new EventSource('/__reload').onmessage = () => location.reload();</script>`;

export function watch(args) {
  const port = +(process.env.PORT || 4321);
  const clients = new Set();
  let running = false, again = false;
  const build = () => {
    if (running) { again = true; return; }
    running = true;
    const extra = args.includes('--no-strict') ? args : [...args, '--no-strict'];
    const child = spawn(process.execPath, [path.join(here, 'build.mjs'), ...extra], { stdio: 'inherit' });
    child.on('exit', (code) => {
      running = false;
      if (again) { again = false; build(); return; }
      if (code === 0) for (const res of clients) res.write('data: reload\n\n');
      console.log(code === 0 ? `[${new Date().toLocaleTimeString()}] rebuilt` : 'build failed: fix the error above and save again');
    });
  };

  let timer;
  const changed = () => { clearTimeout(timer); timer = setTimeout(build, 150); };
  const targets = [path.join(here, 'content'), path.join(here, 'templates'), path.join(here, 'assets'), path.join(here, 'static'),
    path.join(path.dirname(here), 'Components/Vial Cap/render/callouts.mjs')];
  for (const t of targets) if (fs.existsSync(t)) fs.watch(t, { recursive: fs.statSync(t).isDirectory() }, changed);

  http.createServer((req, res) => {
    const url = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (url === '/__reload') {
      res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
      res.write('retry: 500\n\n');
      clients.add(res);
      req.on('close', () => clients.delete(res));
      return;
    }
    let file = path.join(dist, url);
    if (!file.startsWith(dist)) { res.writeHead(403).end(); return; }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    let status = 200;
    if (!fs.existsSync(file)) { file = path.join(dist, '404.html'); status = 404; }
    if (!fs.existsSync(file)) { res.writeHead(503, { 'Content-Type': 'text/html' }).end(`<p>Building…</p>${RELOAD}`); return; }
    const type = TYPES[path.extname(file)] || 'application/octet-stream';
    let body = fs.readFileSync(file);
    if (type.startsWith('text/html')) body = body.toString().replace('</body>', `${RELOAD}</body>`);
    res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' }).end(body);
  }).listen(port, () => console.log(`\nPreview: http://localhost:${port}\nEdit the files in landing/content/ and save; the page reloads. Ctrl-C to stop.\n`));

  build();
  return new Promise(() => {});   // keep running
}
