// electropioreactor.org home: hover labels on the vial's parts and a guided tour, both in the
// wording of Martin's AEP0.2 explainer.
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
const DATA = JSON.parse($('callouts-data').textContent);
const byId = Object.fromEntries(DATA.parts.map((c) => [c.id, c]));
const STEPS = DATA.tour;

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
if (hint && COARSE) hint.textContent = 'Drag sideways to turn · tap a part · pinch to zoom';

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

// ---------------------------------------------------------------- 3D state
let anchors = {}, axis = null, level = 0, lastHook = 0, home = null, anodeBox = null;

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
  const level_ = needles ? needles.min.z : (glass ? glass.max.z - 32 : -23);   // the Media Out tip sets the level
  const out = (p, mm) => {                                                   // push radially out from the vial axis
    const d = v3(p.x - ax.x, p.y - ax.y, 0); if (d.lengthSq() < 1e-6) return p;
    return p.clone().add(d.normalize().multiplyScalar(mm));
  };
  const A = {};
  const sept = box('septum');
  if (needles && cap) A.needles = v3(ax.x, needles.max.y - 1, cap.max.z + 9);
  if (sept) A.port = v3(ax.x, ax.y + (sept.max.y - ax.y) * 0.45, sept.max.z + 0.5);
  if (glass) A.medium = v3(ax.x + R * 0.5, ax.y + R * 0.62, level_ - (level_ - glass.min.z) * 0.5);
  const tm = box('temp_module'); if (tm) A.temp = mid(tm);
  const ca = box('cathode');
  if (ca) A.cathode = v3((ca.min.x + ca.max.x) / 2, (ca.min.y + ca.max.y) / 2, level_ - (level_ - ca.min.z) * 0.4);
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
    A.anode = v3(x, y, level_ - 8);
    A.co2 = v3(x, y, an.min.z - 4);
  }
  const led = box('led_die') || box('led'); if (led) A.led = out(mid(led), 3);
  const pcb = box('pcb');
  if (pcb) { const r = (pcb.max.x - pcb.min.x) / 2; A.heater = v3(ax.x + r * 0.68, ax.y + r * 0.68, (pcb.min.z + pcb.max.z) / 2); }
  axis = ax; level = level_; anodeBox = an;
  return A;
}

// ---------------------------------------------------------------- hover labels
// The viewer raycasts and hands us { part, point (root-local mm), glassOnly }; we name the area.
const PART_TO = {
  septum: 'port', screws: 'screws', washers: 'screws', cathode: 'cathode', flea: 'flea',
  anode_ti: 'co2', pcb: 'heater', pcb_copper: 'heater', pcb_parts: 'heater', thermal_pad: 'heater',
  led: 'led', led_die: 'led', led_legs: 'led', pd: 'led', pd_die: 'led', pd_board: 'led', beam: 'led',
  temp_module: 'temp', temp_module_parts: 'temp', temp_fov: 'temp', temp_probe: 'temp',
};
function areaFor(hit) {
  const { part, point: P } = hit;
  if (part === 'needles' || part === 'hubs') return axis && P.y < axis.y ? 'gas' : 'needles';   // rear pair vent gas
  if (part === 'anode') return anodeBox && P.z < anodeBox.min.z + 10 ? 'co2' : 'anode';
  if (part === 'glass') return hit.glassOnly && P.z < level ? 'medium' : null;
  return PART_TO[part] || null;
}
function installTips() {
  window.__viewerTip = (hit) => {
    const c = byId[areaFor(hit)];
    return c ? { title: c.head, body: c.body } : null;
  };
}

// ---------------------------------------------------------------- tour
const tourEl = $('tour'), tourBtn = $('tourBtn');
const HL_PARTS = {
  port: ['septum'], screws: ['screws', 'washers'], cathode: ['cathode'], anode: ['anode'],
  co2: ['anode_ti', 'anode'], flea: ['flea'], temp: ['temp_module', 'temp_module_parts', 'temp_probe'],
  led: ['led', 'pd_board', 'pd'], heater: ['pcb', 'thermal_pad'],
};
const KIND_COL = { power: 0xd0661f, gas: 0x3a6cf0, liquid: 0x22a35a, control: 0x8a4ee0 };
let step = -1, cam = null, wasTurning = false, lit = [], glowT = 0;

function light(id, kind) {
  for (const { m, mat } of lit) { m.material.dispose(); m.material = mat; }
  lit = [];
  for (const n of HL_PARTS[id] || []) {
    const m = V.meshes[n]; if (!m || !m.material || !('emissive' in m.material)) continue;
    const mat = m.material, c = mat.clone();
    c.emissive = new V.THREE.Color(KIND_COL[kind] || 0xff5a6e);
    m.material = c; lit.push({ m, mat });
  }
}
function glow(dt) {
  if (!lit.length) return;
  glowT += dt || 0.016;
  const k = 0.06 + 0.06 * Math.sin(glowT * 3.5);   // a gentle pulse, not a repaint
  for (const { m } of lit) m.material.emissiveIntensity = k;
}
// camera to a part: look at it from outside the vial, a little above and off-square, close in
function shotFor(id) {
  const { THREE, root } = V;
  if (id === 'overview' || id === 'nutshell' || !anchors[id]) return home;
  const P = anchors[id];
  const tw = root.localToWorld(P.clone());
  const aw = root.localToWorld(new THREE.Vector3(axis.x, axis.y, P.z));
  let d = tw.clone().sub(aw); d.y = 0;
  if (d.lengthSq() < 4) d = V.camera.position.clone().sub(V.controls.target).setY(0);   // on the axis: keep the side we're on
  d.normalize().applyAxisAngle(new THREE.Vector3(0, 1, 0), -0.35).add(new THREE.Vector3(0, 0.3, 0)).normalize();
  const D = home.pos.distanceTo(home.target);          // sizes relative to the opening framing
  const near = D * ({ port: 0.34, needles: 0.5, gas: 0.5, screws: 0.42, co2: 0.42, medium: 0.6, heater: 0.45 }[id] || 0.45);
  const target = tw.clone().lerp(aw, 0.4);              // keep a little of the vial in frame
  return { pos: target.clone().add(d.multiplyScalar(near)), target };
}
function fly(shot) {
  if (!shot) return;
  const { camera, controls } = V;
  cam = { t0: performance.now(), dur: REDUCED ? 0 : 1400, p0: camera.position.clone(), q0: controls.target.clone(), p1: shot.pos.clone(), q1: shot.target.clone() };
  stepCam();
}
function stepCam() {
  if (!cam) return;
  const { camera, controls } = V;
  const k = cam.dur ? Math.min(1, (performance.now() - cam.t0) / cam.dur) : 1;
  const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
  camera.position.lerpVectors(cam.p0, cam.p1, e);
  controls.target.lerpVectors(cam.q0, cam.q1, e);
  camera.lookAt(controls.target);
  if (k >= 1) { cam = null; tourEl.dataset.settled = step >= 0 ? '1' : ''; }
}
function render(i) {
  const s = STEPS[i];
  $('tourN').textContent = `${i + 1} / ${STEPS.length}`;
  $('tourTitle').textContent = s.head;
  const b = $('tourBody'); b.innerHTML = '';
  if (s.rows) for (const r of s.rows) {
    const p = document.createElement('p'); const k = document.createElement('b');
    k.textContent = r.k; p.append(k, ' ', r.v); b.appendChild(p);
  } else { const p = document.createElement('p'); p.textContent = s.body; b.appendChild(p); }
  tourEl.dataset.kind = s.kind || '';
  $('tourPrev').disabled = i === 0;
  $('tourNext').textContent = i === STEPS.length - 1 ? 'Finish' : 'Next →';
}
function go(i) {
  if (!V || i < 0) return;
  if (i >= STEPS.length) { endTour(); return; }
  step = i;
  tourEl.dataset.settled = '';
  render(i);
  V.hideTip && V.hideTip();
  light(STEPS[i].id, STEPS[i].kind);
  fly(shotFor(STEPS[i].id));
}
function startTour() {
  if (!V) return;
  if (scrollY > 10) scrollTo({ top: 0, behavior: REDUCED ? 'auto' : 'smooth' });
  wasTurning = V.controls.autoRotate;
  V.setTurn(false);
  tourEl.hidden = false; app.classList.add('touring');
  go(0);
  $('tourNext').focus({ preventScroll: true });
}
function endTour() {
  if (step < 0) return;
  step = -1; light(null);
  tourEl.hidden = true; app.classList.remove('touring');
  fly(home);
  if (wasTurning) setTimeout(() => { if (step < 0) V.setTurn(true); }, REDUCED ? 0 : 1400);
  tourBtn && tourBtn.focus({ preventScroll: true });
}
tourBtn && tourBtn.addEventListener('click', startTour);
$('tourNext').addEventListener('click', () => go(step + 1));
$('tourPrev').addEventListener('click', () => go(step - 1));
$('tourClose').addEventListener('click', endTour);
document.addEventListener('keydown', (e) => {
  if (step < 0) return;
  if (e.key === 'Escape') endTour();
  else if (e.key === 'ArrowRight') go(step + 1);
  else if (e.key === 'ArrowLeft' && step > 0) go(step - 1);
});

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

let lastT = performance.now();
function onFrame() {
  const t = performance.now(), dt = (t - lastT) / 1000; lastT = t;
  lastHook = t; stepCam(); stepShift(); glow(dt);
}

function init(v) {
  if (V || !v) return;
  V = v;
  const { THREE, controls } = V;
  try { anchors = anchorPoints(); } catch (e) { console.error('anchors', e); }
  installTips();
  // site theme: light mode shows the model on the viewer's white stage
  const isLight = () => (typeof window.__themeLight === 'function' ? window.__themeLight() : document.documentElement.classList.contains('white'));
  if (V.setWhite) { V.setWhite(isLight()); addEventListener('themechange', (e) => V.setWhite(e.detail.light)); }
  // frame the model in the space the overlays leave free (title, header, controls bar)
  try { fit(true); } catch (e) { console.warn('fit', e); }
  home = { pos: V.camera.position.clone(), target: controls.target.clone() };
  controls.addEventListener('start', () => { cam = null; });
  (window.__viewerFrameHooks = window.__viewerFrameHooks || []).push(onFrame);
  // fallback when the viewer does not call frame hooks (or is paused)
  const tick = () => { if (performance.now() - lastHook > 150) { stepCam(); stepShift(); } requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  addEventListener('resize', () => requestAnimationFrame(() => { try { fit(false); } catch (e) {} }));
  // stop rendering while the hero is scrolled out of view
  if (typeof V.animate === 'function' && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => V.animate(e.isIntersecting), { threshold: 0 }).observe(app);
  }
  if (tourBtn) tourBtn.disabled = false;
  app.dataset.ready = '1';
  // #tour opens the tour; #tour-5 opens it at stop 5 (links into the tour)
  const m = location.hash.match(/^#tour(?:-(\d+))?$/);
  if (m) setTimeout(() => { startTour(); if (m[1]) go(Math.min(STEPS.length, +m[1]) - 1); }, 300);
}
if (tourBtn) tourBtn.disabled = true;
if (window.__viewer) init(window.__viewer);
else {
  addEventListener('viewer-ready', () => init(window.__viewer), { once: true });
  let n = 0;
  const poll = setInterval(() => { if (window.__viewer) { clearInterval(poll); init(window.__viewer); } else if (++n > 240) clearInterval(poll); }, 250);
}
})();
