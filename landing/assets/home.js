// electropioreactor.org home: 3D hotspots with hover labels over the vial viewer.
// The viewer exposes window.__viewer = { THREE, scene, camera, renderer, controls, root, meshes,
// goView, setTurn, liquid } and fires "viewer-ready"; functions in window.__viewerFrameHooks run
// after each rendered frame. Anchors are computed here from the part meshes, in root-local
// coordinates (OpenSCAD mm, Z up, +Y = the cap's front opening, anode on -X).
(() => {
const $ = (id) => document.getElementById(id);
const app = $('app');
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const COARSE = matchMedia('(pointer: coarse)').matches;
const PHONE = matchMedia('(max-width: 720px)');
let V = null;                 // window.__viewer, once ready
const CALLOUTS = JSON.parse($('callouts-data').textContent);
const byId = Object.fromEntries(CALLOUTS.map((c) => [c.id, c]));

const layer = $('hsLayer');
const label = $('hs-label');
const dots = Object.fromEntries([...layer.querySelectorAll('.hs-dot')].map((b) => [b.dataset.id, b]));

// ---------------------------------------------------------------- header, bar height, hint
const header = document.querySelector('.site-header.over-hero');
const onScroll = () => header && header.classList.toggle('solid', scrollY > app.offsetHeight - 64);
addEventListener('scroll', onScroll, { passive: true });
onScroll();

const bar = app.querySelector('.bar');
if (bar) {
  const setBar = () => app.style.setProperty('--bar-h', bar.offsetHeight + 'px');
  setBar();
  if ('ResizeObserver' in window) new ResizeObserver(setBar).observe(bar);
}
const hint = $('heroHint');
if (hint && COARSE) hint.textContent = 'Drag sideways to turn the vial · tap the dots · pinch to zoom';

// ---------------------------------------------------------------- wheel: scroll the page unless the model is engaged
const stage = $('stage');
let engaged = false, hintTimer = 0;
const zoomHint = document.createElement('div');
zoomHint.className = 'zoom-hint'; zoomHint.setAttribute('aria-hidden', 'true');
zoomHint.textContent = 'Click the model, or hold Ctrl, to zoom';
app.appendChild(zoomHint);
stage.addEventListener('wheel', (e) => {
  if (engaged || e.ctrlKey || e.metaKey) return;   // trackpad pinch arrives as ctrl+wheel
  e.stopPropagation();                              // OrbitControls never sees it: the page scrolls
  if (Math.abs(e.deltaY) > 2 && scrollY < 40) {
    zoomHint.classList.add('show'); clearTimeout(hintTimer);
    hintTimer = setTimeout(() => zoomHint.classList.remove('show'), 1400);
  }
}, { capture: true, passive: true });
stage.addEventListener('pointerdown', () => { engaged = true; zoomHint.classList.remove('show'); });
app.addEventListener('pointerleave', () => { engaged = false; });
addEventListener('scroll', () => { if (scrollY > 60) engaged = false; }, { passive: true });

// ---------------------------------------------------------------- highlight + active state
let active = null, hover = null;
const pos = {};               // id -> { x, y, behind, out }
function showLabel(id, withBody) {
  const c = byId[id], p = pos[id];
  if (!c || !p || p.out) { hideLabel(); return; }
  label.innerHTML = '';
  const b = document.createElement('b'); b.textContent = c.head; label.appendChild(b);
  if (withBody) { const s = document.createElement('span'); s.textContent = c.body; label.appendChild(s); }
  label.hidden = false;
  label.dataset.for = id;
  label.dataset.body = withBody ? '1' : '';
  placeLabel();
}
function hideLabel() { label.hidden = true; label.dataset.for = ''; }
function placeLabel() {
  const id = label.dataset.for;
  if (!id || label.hidden) return;
  const p = pos[id];
  if (!p || p.out) { label.style.visibility = 'hidden'; return; }
  label.style.visibility = '';
  const W = app.clientWidth, w = label.offsetWidth, h = label.offsetHeight, pad = 12;
  let x = p.x + 22, y = p.y - h / 2;
  if (x + w > W - pad) x = p.x - 22 - w;
  if (x < pad) { x = Math.min(Math.max(pad, p.x - w / 2), W - pad - w); y = p.y + 24; }
  y = Math.max(app.querySelector('.overlay') ? 70 : pad, Math.min(y, app.clientHeight - h - pad));
  label.style.transform = `translate(${Math.round(x)}px, ${Math.round(y)}px)`;
}
function setHover(id) {
  if (hover === id) return;
  if (hover) dots[hover]?.classList.remove('hl');
  hover = id;
  if (id) {
    dots[id]?.classList.add('hl');
    showLabel(id, id === active);
  } else if (active) showLabel(active, true);
  else hideLabel();
}
function setActive(id, { turn = true } = {}) {
  if (active) dots[active]?.classList.remove('active');
  active = id;
  if (id) {
    dots[id]?.classList.add('active');
    if (turn) turnTo(id);
    showLabel(id, true);
  } else hideLabel();
}
for (const [id, d] of Object.entries(dots)) {
  d.addEventListener('pointerenter', () => setHover(id));
  d.addEventListener('pointerleave', () => setHover(null));
  d.addEventListener('focus', () => setHover(id));
  d.addEventListener('blur', () => setHover(null));
  d.addEventListener('click', () => {
    if (active === id) { setActive(null); return; }
    setActive(id);
  });
}
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && active) setActive(null); });

// ---------------------------------------------------------------- 3D: anchors, projection, turning
let anchors = {}, axis = null, tween = null, lastHook = 0;
let tmp, tmpA, tmpC;

function anchorPoints() {
  const { THREE, meshes } = V;
  const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
  const box = (n) => {
    const m = meshes[n]; if (!m) return null;
    if (!m.geometry.boundingBox) m.geometry.computeBoundingBox();
    m.updateMatrix();
    return m.geometry.boundingBox.clone().applyMatrix4(m.matrix);   // root-local
  };
  const mid = (b) => b.getCenter(v3());
  // the mesh vertex nearest to a guide point (root-local): puts a dot on a part's real surface
  const nearest = (n, guide) => {
    const m = meshes[n]; if (!m) return null;
    const p = m.geometry.attributes.position, v = v3(); let best = null, bd = Infinity;
    const step = Math.max(1, Math.floor(p.count / 60000));
    for (let i = 0; i < p.count; i += step) {
      v.fromBufferAttribute(p, i).applyMatrix4(m.matrix);
      const d = v.distanceToSquared(guide);
      if (d < bd) { bd = d; best = v.clone(); }
    }
    return best;
  };
  const glass = box('glass'), cap = box('cap'), needles = box('needles');
  const ax = glass ? mid(glass) : v3(0, 0, 0);
  const R = glass ? (glass.max.x - glass.min.x) / 2 : 14;
  const level = needles ? needles.min.z : (glass ? glass.max.z - 32 : -23);   // the Media Out tip sets the level
  const out = (p, mm) => {                                                   // push radially out from the vial axis
    const d = v3(p.x - ax.x, p.y - ax.y, 0); if (d.lengthSq() < 1e-6) return p;
    return p.clone().add(d.normalize().multiplyScalar(mm));
  };
  const A = {};
  const sept = box('septum');
  if (needles && cap) A.needles = v3(ax.x, needles.max.y - 1, cap.max.z + 9);
  if (sept) A.port = v3(ax.x, ax.y + (sept.max.y - ax.y) * 0.45, sept.max.z + 0.5);
  if (glass) A.medium = v3(ax.x + R * 0.5, ax.y + R * 0.62, level - (level - glass.min.z) * 0.5);
  const tm = box('temp_module'); if (tm) A.temp = mid(tm);
  const ca = box('cathode');
  if (ca) A.cathode = v3((ca.min.x + ca.max.x) / 2, (ca.min.y + ca.max.y) / 2, level - (level - ca.min.z) * 0.4);
  const pd = nearest('pd_die', v3(ax.x - 40, ax.y, -70)) || (box('pd_board') && mid(box('pd_board')));
  if (pd) A.pd = out(pd, 1.5);
  const fl = box('flea'); if (fl) A.flea = mid(fl);
  const gas = meshes.hubs ? nearest('hubs', v3(ax.x - 10, ax.y - 14, 200)) : (needles && v3(needles.min.x, needles.min.y, needles.max.z));
  if (gas) A.gas = gas;
  const sc = box('screws'); if (sc) A.screws = v3(sc.max.x, (sc.min.y + sc.max.y) / 2, (sc.min.z + sc.max.z) / 2);
  if (meshes.cap) A.cap = nearest('cap', v3(ax.x - 30, ax.y + 30, cap ? (cap.min.z + cap.max.z) * 0.62 : 22));
  const an = box('anode');
  if (an) {
    const x = (an.min.x + an.max.x) / 2, y = (an.min.y + an.max.y) / 2;
    A.anode = v3(x, y, level - 8);
    A.co2 = v3(x, y, an.min.z - 4);
  }
  const led = box('led_die') || box('led'); if (led) A.led = out(mid(led), 3);
  const pcb = box('pcb');
  if (pcb) { const r = (pcb.max.x - pcb.min.x) / 2; A.heater = v3(ax.x + r * 0.68, ax.y + r * 0.68, (pcb.min.z + pcb.max.z) / 2); }
  axis = ax;
  return A;
}

function update() {
  if (!V) return;
  const { camera, root, renderer } = V;
  const W = renderer.domElement.clientWidth || app.clientWidth, H = renderer.domElement.clientHeight || app.clientHeight;
  root.updateMatrixWorld();
  const camPos = camera.position;
  for (const [id, P] of Object.entries(anchors)) {
    const d = dots[id]; if (!d) continue;
    tmp.copy(P); root.localToWorld(tmp);
    tmpA.set(axis.x, axis.y, P.z); root.localToWorld(tmpA);
    const radial = tmpC.copy(tmp).sub(tmpA);
    const behind = radial.lengthSq() > 4 && radial.dot(tmpA.clone().sub(camPos).negate()) < 0;
    tmp.project(camera);
    const x = (tmp.x + 1) / 2 * W, y = (1 - tmp.y) / 2 * H;
    const out = tmp.z > 1 || x < -20 || y < -20 || x > W + 20 || y > H + 20;
    const p = pos[id] || (pos[id] = {});
    if (p.behind !== behind) d.classList.toggle('behind', behind);
    if (p.out !== out) d.classList.toggle('out', out);
    p.x = x; p.y = y; p.behind = behind; p.out = out;
    d.style.translate = `${x.toFixed(1)}px ${y.toFixed(1)}px`;
    d.style.zIndex = behind ? '0' : '1';
  }
  placeLabel();
}

function turnTo(id) {
  if (!V || !anchors[id]) return;
  const { THREE, camera, controls, root } = V;
  const P = anchors[id];
  const pw = root.localToWorld(P.clone());
  const aw = root.localToWorld(new THREE.Vector3(axis.x, axis.y, P.z));
  const d = pw.sub(aw);
  if (d.lengthSq() < 4) return;                       // on the axis: visible from every side
  V.setTurn && V.setTurn(false);
  const sph = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));
  let delta = Math.atan2(d.x, d.z) - sph.theta - 0.25;   // a little off-square, so it reads as 3D
  delta = Math.atan2(Math.sin(delta), Math.cos(delta));
  tween = { t0: performance.now(), th0: sph.theta, delta, dur: REDUCED ? 0 : 900 };
  if (REDUCED) stepTween();
}
function stepTween() {
  if (!tween) return;
  const { THREE, camera, controls } = V;
  const k = tween.dur ? Math.min(1, (performance.now() - tween.t0) / tween.dur) : 1;
  const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
  const off = camera.position.clone().sub(controls.target);
  const sph = new THREE.Spherical().setFromVector3(off);
  sph.theta = tween.th0 + tween.delta * e;
  camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(sph));
  camera.lookAt(controls.target);
  if (k >= 1) tween = null;
}


// The free area of the hero, in px relative to #app: below the header (phones: below the title
// block), above the controls bar, right of the title column (desktop).
function freeRect() {
  const W = app.clientWidth, H = app.clientHeight, r0 = app.getBoundingClientRect();
  const rel = (el) => { const r = el.getBoundingClientRect(); return { l: r.left - r0.left, r: r.right - r0.left, t: r.top - r0.top, b: r.bottom - r0.top }; };
  const title = app.querySelector('.title'), barEl = app.querySelector('.bar');
  let top = 70, bottom = H - 16, left = 16, right = W - 16;
  if (barEl) bottom = rel(barEl).t - 14;
  if (PHONE.matches || W < 900) {
    if (title) top = rel(title).b + 10;
  }
  else {
    if (title) left = rel(title).r + 24;
    right = W - 24;
  }
  if (bottom - top < 200) top = Math.max(60, bottom - 200);
  if (right - left < 200) { left = 16; right = W - 16; }
  return { l: left, r: right, t: top, b: bottom, w: right - left, h: bottom - top, cx: (left + right) / 2, cy: (top + bottom) / 2, W, H };
}
let shift = null;   // view-offset tween { x0, y0, x1, y1, t0 }
const viewOff = { x: 0, y: 0 };
function modelRect() {
  const { THREE, camera, root } = V;
  const W = app.clientWidth, H = app.clientHeight;
  const b = new THREE.Box3();
  for (const n of ['glass', 'cap', 'hubs', 'needles', 'pcb', 'pd_board', 'temp_module', 'screws']) if (V.meshes[n]) b.expandByObject(V.meshes[n]);
  if (b.isEmpty()) b.setFromObject(root);
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity; const v = new THREE.Vector3();
  for (let i = 0; i < 8; i++) {
    v.set(i & 1 ? b.max.x : b.min.x, i & 2 ? b.max.y : b.min.y, i & 4 ? b.max.z : b.min.z).project(camera);
    const x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H;
    x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
  }
  return { w: x1 - x0, h: y1 - y0, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2 };
}
function fit(scale, animate = false) {
  const { camera, controls } = V;
  const W = app.clientWidth, H = app.clientHeight;
  camera.clearViewOffset();
  const f = freeRect();
  if (scale) {                       // once: set the distance so the model fills the free height
    const m = modelRect();
    const k = Math.min(1.9, Math.max(0.7, Math.max(m.h / (f.h * 1.16), m.w / (f.w * 1.2))));
    const off = camera.position.clone().sub(controls.target);
    camera.position.copy(controls.target).add(off.multiplyScalar(k));
    controls.update();
  }
  // the target projects to the canvas centre; slide the view so it lands in the free area's centre
  const tx = W / 2 - f.cx, ty = H / 2 - f.cy;
  if (animate && !REDUCED) shift = { x0: viewOff.x, y0: viewOff.y, x1: tx, y1: ty, t0: performance.now() };
  else { shift = null; setOff(tx, ty); }
}
function setOff(x, y) {
  viewOff.x = x; viewOff.y = y;
  const W = app.clientWidth, H = app.clientHeight;
  if (Math.abs(x) < 0.5 && Math.abs(y) < 0.5) V.camera.clearViewOffset();
  else V.camera.setViewOffset(W, H, x, y, W, H);
}
function stepShift() {
  if (!shift) return;
  const k = Math.min(1, (performance.now() - shift.t0) / 450), e = 1 - Math.pow(1 - k, 3);
  setOff(shift.x0 + (shift.x1 - shift.x0) * e, shift.y0 + (shift.y1 - shift.y0) * e);
  if (k >= 1) shift = null;
}

function onFrame() { lastHook = performance.now(); stepTween(); stepShift(); update(); }

function init(v) {
  if (V || !v) return;
  V = v;
  const { THREE, controls } = V;
  tmp = new THREE.Vector3(); tmpA = new THREE.Vector3(); tmpC = new THREE.Vector3();
  try { anchors = anchorPoints(); } catch (e) { console.error('hotspots', e); return; }
  for (const [id, d] of Object.entries(dots)) {
    if (anchors[id]) d.hidden = false;
    else { d.remove(); delete dots[id]; console.warn('hotspot without an anchor:', id); }
  }
  // frame the model in the space the overlays leave free (title, header, controls bar)
  try { fit(true); } catch (e) { console.warn('fit', e); }
  controls.addEventListener('start', () => { tween = null; });
  (window.__viewerFrameHooks = window.__viewerFrameHooks || []).push(onFrame);
  // fallback when the viewer does not call frame hooks (or is paused)
  const tick = () => { if (performance.now() - lastHook > 150) { stepTween(); stepShift(); update(); } requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  addEventListener('resize', () => requestAnimationFrame(() => { try { fit(false); } catch (e) {} update(); }));
  // stop rendering while the hero is scrolled out of view
  if (typeof V.animate === 'function' && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => V.animate(e.isIntersecting), { threshold: 0 }).observe(app);
  }
  update();
  layer.dataset.ready = '1';
}
if (window.__viewer) init(window.__viewer);
else {
  addEventListener('viewer-ready', () => init(window.__viewer), { once: true });
  let n = 0;
  const poll = setInterval(() => { if (window.__viewer) { clearInterval(poll); init(window.__viewer); } else if (++n > 240) clearInterval(poll); }, 250);
}
})();
