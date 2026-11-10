// ================================================================ PRESENTATION
// Runs in the viewer's module scope (concatenated by build.mjs).
//   → ↓ Space Enter: next animation step     ← ↑ Backspace: back one step
//   PageDown / PageUp: jump to the next/previous page (each reactor version jumps to its finished state)
//   Click the version tag: turntable on/off      Home / End     B or . : black     F: full screen
//   E: camera edit mode (S saves this step's camera, X clears it, C copies all saved cameras)
window.__viewerTip = () => null;
renderer.localClippingEnabled = true;

const DZ20 = -34;                 // 20 ml vial (61 mm tall): everything above the cut sits 34 mm lower than on the 40 ml vial
const ZC = -60;                   // where the glass is cut to make the short vial (straight wall either side)
const L20 = -52.5;                // 15 ml in the 20 ml vial
const L40 = -23;                  // 30 ml in the 40 ml vial
const OLD_TOP = 12.3;             // top of the O-ring caps (40 ml frame)
const ROD_TOP = OLD_TOP + 35 + 10;
const TIP_OLD = -71 - DZ20;       // old electrode tips, 40 ml frame (-71 absolute)
const LVL20 = L20 - DZ20;         // the 15 ml level in the 40 ml frame
const PI = Math.PI;

const ride = new THREE.Group(); ride.name = 'ride'; root.add(ride);   // the vial top and everything held by the cap
const OBJ = {};
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const seg = (v, a, b) => ease(clamp01((v - a) / (b - a)));

// ---------------------------------------------------------------- materials (nothing transmissive inside the glass: it would vanish)
const ptTi = phys({ color: 0xc9cbcf, metalness: 1, roughness: 0.35, envMapIntensity: 0.6 });
const ss = steel(0.34);
const mmo = phys({ color: 0x4d5560, metalness: 0.6, roughness: 0.5, iridescence: 0.25, iridescenceIOR: 1.6, iridescenceThicknessRange: [250, 420] });
const tiMat = phys({ color: 0xa3a39f, metalness: 1, roughness: 0.55, envMapIntensity: 0.45 });
const silicone = phys({ color: 0xe8eded, roughness: 0.38, clearcoat: 0.4, clearcoatRoughness: 0.3, side: THREE.DoubleSide });
const exaWhite = phys({ color: 0xf6f6f2, roughness: 0.45, clearcoat: 0.3 });
const exaRed = phys({ color: 0xe0482a, roughness: 0.35, clearcoat: 0.5 });
const redMat = phys({ color: 0xc8202a, roughness: 0.45, clearcoat: 0.4 });
const blackMat = phys({ color: 0x1b1c1f, roughness: 0.45, clearcoat: 0.4 });
const brass = phys({ color: 0xd8b26a, metalness: 1, roughness: 0.4 });
const pdBlack = phys({ color: 0x0c0c0e, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.05 });
const oringMat = phys({ color: 0x5a3820, roughness: 0.6, sheen: 0.3 });
const capOld = capMat.clone(); capOld.side = THREE.DoubleSide;
const MEP_BLUE = new THREE.Color(0x2f6fd0);   // MEP caps printed in blue PETG; the AEPs' are PC-CF
const waterMat = phys({ color: 0xdff2ff, roughness: 0.04, clearcoat: 1, transparent: true, opacity: 0.55, envMapIntensity: 1.6, depthWrite: false });
const syrMat = phys({ color: 0xf2f6f8, roughness: 0.2, clearcoat: 1, transparent: true, opacity: 0.45, depthWrite: false });
const greenHub = phys({ color: 0x8a9a2c, roughness: 0.45 });

// ---------------------------------------------------------------- objects: slide in/out along `off`, or a custom pose; no fading (fades pop)
function reg(name, obj, { parent = root, off = [0, 0, 60], pose, enterMs = 1300, exitMs = 900 } = {}) {
  const w = new THREE.Group(); w.name = 'w_' + name;
  parent.add(w); w.add(obj);
  obj.traverse((o) => { if (o.isMesh && o.userData.part === undefined) { o.castShadow = true; o.receiveShadow = true; } });
  OBJ[name] = { name, w, obj, off: V3(...off), pose, v: 0, target: 0, enterMs, exitMs };
  w.visible = false;
  return OBJ[name];
}
function mesh(g, m) { const o = new THREE.Mesh(g, m); o.castShadow = true; o.receiveShadow = true; return o; }
function rod(x, y, z0, z1, r, m) {
  const g = new THREE.CylinderGeometry(r, r, z1 - z0, 48); g.rotateX(PI / 2); g.translate(x, y, (z0 + z1) / 2);
  return mesh(g, m);
}
function tube(pts, r = 1.5, m = silicone) {
  const c = new THREE.CatmullRomCurve3(pts.map((p) => V3(...p)), false, 'centripetal');
  return { o: mesh(new THREE.TubeGeometry(c, 140, r, 16, false), m), c };
}
function ringGeo(ri, ro, z0, z1, segs = 64) {      // a turned ring (tube wall) about Z
  const pr = [[ri, z0], [ro, z0], [ro, z1], [ri, z1], [ri, z0]].map(([r, z]) => new THREE.Vector2(Math.max(0.001, r), z));
  const g = new THREE.LatheGeometry(pr, segs); g.rotateX(PI / 2); return g;
}
function exapureAt(p, t, inlet = false) {        // Exapure 25 mm 0.2 µm PTFE syringe filter: orange-red housing, white centre and luers
  const g = new THREE.Group();
  const rim = mesh(new THREE.CylinderGeometry(12.5, 12.5, 7.4, 64), exaRed);
  const top = mesh(new THREE.CylinderGeometry(9.4, 9.4, 5.0, 48), exaWhite);
  const luer1 = mesh(new THREE.CylinderGeometry(2.0, 2.8, 7, 24), exaWhite); luer1.position.y = -6.5;
  const luer2 = mesh(new THREE.CylinderGeometry(2.4, 2.4, 6, 24), exaWhite); luer2.position.y = 6;
  if (inlet) { luer1.position.y = 6.5; luer1.rotation.z = PI; luer2.position.y = -6; }   // gas flows from the cylinder: female inlet away from the line
  g.add(rim, top, luer1, luer2);
  g.position.copy(p).add(t.clone().multiplyScalar(inlet ? 5.5 : 10));
  g.quaternion.setFromUnitVectors(V3(0, 1, 0), t);
  return g;
}
const exapure = (c, inlet) => exapureAt(c.getPoint(1), c.getTangent(1), inlet);
function croc(x, z, out, m) {      // crocodile clip lying horizontally, its jaws biting the rod from either side
  const g = new THREE.Group();
  const jaw = (s) => {
    const j = new THREE.Group();
    const plate = mesh(new THREE.BoxGeometry(24, 1.4, 6), steel(0.35)); plate.position.x = 12;
    const lip = mesh(new THREE.BoxGeometry(9, 2.2, 6.4), steel(0.3)); lip.position.set(2.5, -s * 0.7, 0);
    j.add(plate, lip); j.position.y = s * 3.6; j.rotation.z = s * 0.1; return j;
  };
  const boot = mesh(new THREE.CylinderGeometry(4.2, 5.4, 22, 32), m); boot.rotation.z = PI / 2; boot.position.x = 24;
  const spring = mesh(new THREE.TorusGeometry(2.4, 0.6, 10, 24), steel(0.3)); spring.position.x = 11;
  g.add(jaw(1), jaw(-1), boot, spring);
  g.scale.x = out; g.position.set(x, 0, z);
  const lead = tube([[x + out * 34, 0, z], [x + out * 48, 0, z + 2], [x + out * 62, 0, z + 25], [x + out * 66, 0, z + 90]], 1.5, m);
  const all = new THREE.Group(); all.add(g, lead.o); return all;
}
function bolt(x, z, out, m) {      // M3 hex-socket bolt into the top stop's captive nut, ring terminal and lead
  const g = new THREE.Group();
  const shank = mesh(new THREE.CylinderGeometry(1.5, 1.5, 9, 16), steel(0.3)); shank.rotation.z = PI / 2; shank.position.set(x - out * 2, 0, z);
  const head = mesh(new THREE.CylinderGeometry(2.8, 2.8, 3, 32), steel(0.25)); head.rotation.z = PI / 2; head.position.set(x + out * 3.5, 0, z);
  const hex = mesh(new THREE.CylinderGeometry(1.35, 1.35, 1.2, 6), new THREE.MeshStandardMaterial({ color: 0x050505, roughness: 0.9 }));
  hex.rotation.z = PI / 2; hex.position.set(x + out * 4.5, 0, z);
  const ring = mesh(new THREE.TorusGeometry(3.2, 0.7, 10, 32), brass); ring.rotation.y = PI / 2; ring.position.set(x + out * 1.6, 0, z);
  const lead = tube([[x + out * 1.6, 0, z + 3.5], [x + out * 6, 0, z + 12], [x + out * 18, 0, z + 45], [x + out * 24, 0, z + 90]], 1.5, m);
  g.add(shank, head, hex, ring, lead.o);
  return g;
}
function photodiode(ang, r, z) {   // a 5 mm black photodiode in its pocket, dome facing the vial
  const g = new THREE.Group();
  const body = mesh(new THREE.CylinderGeometry(2.5, 2.5, 5.2, 32), pdBlack); body.rotation.z = PI / 2; body.position.x = 2.6;
  const dome = mesh(new THREE.SphereGeometry(2.5, 32, 16, 0, PI * 2, 0, PI / 2), pdBlack); dome.rotation.z = PI / 2;
  const flange = mesh(new THREE.CylinderGeometry(2.9, 2.9, 1, 32), pdBlack); flange.rotation.z = PI / 2; flange.position.x = 5.6;
  g.add(body, dome, flange);
  for (const s of [-1, 1]) { const l = mesh(new THREE.CylinderGeometry(0.25, 0.25, 9, 8), steel(0.4)); l.rotation.z = PI / 2; l.position.set(10.5, s * 1.27, 0); g.add(l); }
  const outer = new THREE.Group(); outer.add(g);
  g.position.x = r; outer.rotation.z = ang; outer.position.z = z;
  return outer;
}
function syringe() {              // 1 ml syringe with a hypodermic needle; tip at the origin, pointing down -Z
  const g = new THREE.Group();
  const needle = rod(0, 0, 0, 40, 0.35, steel(0.25));
  const hub = rod(0, 0, 40, 47, 1.6, greenHub);
  const barrel = rod(0, 0, 47, 107, 3.4, syrMat);
  const plunger = rod(0, 0, 60, 125, 2.3, phys({ color: 0xf4f4f4, roughness: 0.5 }));
  const bung = rod(0, 0, 60, 63, 3.2, blackMat);
  const thumb = rod(0, 0, 125, 127, 5.5, phys({ color: 0xf4f4f4, roughness: 0.5 }));
  g.add(needle, hub, barrel, plunger, bung, thumb);
  return g;
}
// The 24-400 glass vial with its thread: outer and inner wall turned in one profile, plus a swept helical thread.
function vialGeometry() {
  const prof = [[0, -85.3], [11.6, -85.3], [12.9, -84.9], [13.55, -84.0], [13.75, -82.6], [13.75, -7.6], [13.4, -6.6], [12.2, -5.8], [11.3, -5.0], [11.2, -4.0],
    [11.2, 9.0], [10.95, 9.6], [10.4, 9.75], [9.0, 9.75], [8.7, 9.5], [8.6, 9.0], [8.6, -2.5], [9.4, -4.0], [11.4, -5.6], [12.6, -6.6], [12.8, -7.6],
    [12.8, -82.2], [12.6, -83.4], [11.8, -84.2], [10.8, -84.4], [0.01, -84.4]];
  const g = new THREE.LatheGeometry(prof.map(([r, z]) => new THREE.Vector2(Math.max(0.01, r), z)), 160);
  g.rotateX(PI / 2);
  const turns = 1.25, N = 260, tp = [[11.1, -0.95], [11.95, -0.32], [11.95, 0.32], [11.1, 0.95]];
  const pos = [], idx = [];
  for (let i = 0; i <= N; i++) {
    const t = i / N, a = t * turns * PI * 2 + 0.6, zc = 0.8 + t * turns * 3.175;
    const taper = Math.max(0.08, Math.min(1, t * 6, (1 - t) * 6));
    for (const [r, dz] of tp) { const rr = 11.1 + (r - 11.1) * taper; pos.push(Math.cos(a) * rr, Math.sin(a) * rr, zc + dz * (0.4 + 0.6 * taper)); }
  }
  for (let i = 0; i < N; i++) for (let k = 0; k < 3; k++) { const a = i * 4 + k, b = a + 4; idx.push(a, b, a + 1, a + 1, b, b + 1); }
  const th = new THREE.BufferGeometry(); th.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); th.setIndex(idx); th.computeVertexNormals();
  return { body: g, thread: th };
}
// Split a part into its separate pieces (connected triangles), e.g. the four needles.
function pieces(geo) {
  const p = geo.attributes.position.array, na = geo.attributes.normal.array, n = p.length / 9;
  const par = Int32Array.from({ length: n }, (_, i) => i);
  const f = (x) => { while (par[x] !== x) { par[x] = par[par[x]]; x = par[x]; } return x; };
  const own = new Map();
  for (let t = 0; t < n; t++) for (let k = 0; k < 3; k++) {
    const o = t * 9 + k * 3, key = `${Math.round(p[o] * 200)},${Math.round(p[o + 1] * 200)},${Math.round(p[o + 2] * 200)}`;
    if (own.has(key)) par[f(t)] = f(own.get(key)); else own.set(key, t);
  }
  const groups = new Map();
  for (let t = 0; t < n; t++) { const r = f(t); if (!groups.has(r)) groups.set(r, []); groups.get(r).push(t); }
  return [...groups.values()].map((ts) => {
    const pp = new Float32Array(ts.length * 9), nn = new Float32Array(ts.length * 9);
    ts.forEach((t, i) => { pp.set(p.subarray(t * 9, t * 9 + 9), i * 9); nn.set(na.subarray(t * 9, t * 9 + 9), i * 9); });
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pp, 3)); g.setAttribute('normal', new THREE.BufferAttribute(nn, 3));
    g.computeBoundingBox(); return g;
  });
}
function flipCap(g) { const m = new THREE.Mesh(g, capOld); m.rotation.x = PI; m.position.z = OLD_TOP; m.castShadow = true; m.receiveShadow = true; return m; }
function coneToGlass(A, dir, r0, slope, Rc, far, segs = 64) {
  const u = new THREE.Vector3(0, 0, 1).cross(dir).normalize(), v = dir.clone().cross(u).normalize();
  const pos = [], idx = [];
  const at = (s, w) => A.clone().add(dir.clone().multiplyScalar(s)).add(w.clone().multiplyScalar(r0 + slope * s));
  const rr = (p) => Math.hypot(p.x, p.y);
  for (let i = 0; i <= segs; i++) {
    const th = i / segs * PI * 2, w = u.clone().multiplyScalar(Math.cos(th)).add(v.clone().multiplyScalar(Math.sin(th)));
    // walk along the generator to where it meets the glass cylinder, then bisect
    let s0 = far ? 60 : 0.01, s1 = s0, step = far ? -0.25 : 0.25, inside0 = rr(at(s0, w)) < Rc;
    for (let k = 0; k < 400; k++) { s1 = s0 + step; if ((rr(at(s1, w)) < Rc) !== inside0) break; s0 = s1; }
    for (let k = 0; k < 30; k++) { const m = (s0 + s1) / 2; if ((rr(at(m, w)) < Rc) === inside0) s0 = m; else s1 = m; }
    const a = at(0, w), b = at((s0 + s1) / 2, w);
    pos.push(a.x, a.y, a.z, b.x, b.y, b.z);
  }
  for (let i = 0; i < segs; i++) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 2, a + 1, a + 3); }
  if (far) {                                         // end face lying on the glass: a fan from where the axis meets it
    let s0 = 60, s1 = 60; const ax = (q) => A.clone().add(dir.clone().multiplyScalar(q));
    for (let k = 0; k < 400; k++) { s1 = s0 - 0.25; if (Math.hypot(ax(s1).x, ax(s1).y) < Rc) break; s0 = s1; }
    for (let k = 0; k < 30; k++) { const m = (s0 + s1) / 2; if (Math.hypot(ax(m).x, ax(m).y) < Rc) s1 = m; else s0 = m; }
    const c = ax((s0 + s1) / 2), ci = pos.length / 3; pos.push(c.x, c.y, c.z);
    for (let i = 0; i < segs; i++) idx.push(ci, i * 2 + 3, i * 2 + 1);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
  return g;
}
function lidTop(re) {             // flat top plate of the old cap (in use, 40 ml frame): 6 mm (or O-ring) electrode holes + five 3.3 mm ports
  const sh = new THREE.Shape(); sh.absarc(0, 0, 13.0, 0, PI * 2, false);
  const hole = (x, y, r) => { const h = new THREE.Path(); h.absarc(x, y, r, 0, PI * 2, true); sh.holes.push(h); };
  hole(-4.8, 0, re); hole(4.8, 0, re);
  for (const k of ['A', 'BL', 'BR', 'CL', 'CR']) hole(PORT[k][0], PORT[k][1], 1.65);
  const g = new THREE.ExtrudeGeometry(sh, { depth: 0.8, bevelEnabled: false, curveSegments: 48 });
  g.translate(0, 0, OLD_TOP - 0.75); return g;
}
async function stl(name) { return decode(name, EXTRA[name]); }
const centre = (g) => g.boundingBox.getCenter(new THREE.Vector3());

// ---------------------------------------------------------------- animated parameters (eased between steps)
const PAR = {};                     // name -> { v, from, to, t0, dur }
const par = (k) => (PAR[k] ? PAR[k].v : 0);
// twist-on: drop straight down onto the thread, then one turn (the 24-400 thread's single 3.175 mm pitch)
const twistOn = (o) => {
  const v = o.v, k = seg(v, 0.5, 1);
  o.w.position.set(0, 0, v < 0.5 ? 3.175 + 60 * (1 - seg(v, 0, 0.5)) : 3.175 * (1 - k));
  o.w.rotation.z = PI * 2 * (1 - k);                       // turning clockwise seen from above as it goes down: righty-tighty
};

// ---------------------------------------------------------------- old-cap ports (in use, 40 ml frame) and the lines through them
const PORT = { A: [0, -8.2], BL: [-3.9, -7.3], BR: [3.9, -7.3], CL: [-3.9, 6.5], CR: [3.9, 6.5], D: [0, 7.8] };
const inner = ([x, y]) => { const s = 5.4 / Math.hypot(x, y); return [x * s, y * s]; };
function line(port, endZ, out) {   // through its port hole, then in from the neck, down to endZ; out: [x, y, z] far end
  const [x, y] = PORT[port], [ix, iy] = inner(PORT[port]);
  const pts = [];
  if (endZ < 0) pts.push([ix, iy, endZ], [ix, iy, -4], [x * 0.9, y * 0.9, 4]);
  else pts.push([x, y, endZ]);
  pts.push([x, y, OLD_TOP - 1], [x, y, OLD_TOP + 8], [x * 1.6, y * 1.6, OLD_TOP + 24], out);
  return tube(pts, 1.5);
}
const CO2_END = inner(PORT.BL), IN_END = inner(PORT.CR), OUT_END = inner(PORT.CL);

// ---------------------------------------------------------------- build the scene
const DRIPS = {};
let fleaShadow, ledC, dropMesh = null, anodeParts = null, sleeves = [], capMEPmesh = null, capPlate = null, inocMesh = null, pinchFrame = null;
async function buildScene() {
  // glass: bottom half stays put, top half rides with the cap; the whole vial drops in from above
  const vg = vialGeometry();
  const gm = meshes.glass.material;
  const mk = (geo, plane) => { const m = new THREE.Mesh(geo, gm.clone()); m.material.clippingPlanes = [plane]; m.renderOrder = 1; m.userData.part = 'glass'; m.castShadow = false; m.receiveShadow = false; return m; };
  const below = new THREE.Plane(V3(0, -1, 0), ZC), above = new THREE.Plane(V3(0, 1, 0), -ZC);
  const glassBot = mk(vg.body, below), glassTop = mk(vg.body, above), thread = mk(vg.thread, above);
  root.remove(meshes.glass);
  const vial = new THREE.Group(); vial.add(glassBot);
  const top = new THREE.Group(); top.add(glassTop, thread); ride.add(top);
  reg('glass', vial, { enterMs: 1600, pose: (o, e) => { const z = 90 * (1 - e); o.w.position.set(0, 0, z); top.position.z = z; top.visible = o.v > 0.001; below.constant = ZC + z; above.constant = -(ZC + z); } });
  for (const m of [glassBot, glassTop, thread]) { m.castShadow = false; m.receiveShadow = false; }

  const take = (list) => { const g = new THREE.Group(); for (const p of list) if (meshes[p]) { meshes[p].parent?.remove(meshes[p]); g.add(meshes[p]); } return g; };
  // flea: drops in; its shadow stays on the vial floor
  if (fleaPivot) {
    const c = centre(meshes.flea.geometry);
    fleaShadow = new THREE.Mesh(new THREE.CircleGeometry(1, 40), new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false }));
    fleaShadow.geometry.scale(7.2, 3.0, 1); fleaShadow.position.set(c.x, c.y, -84.25); fleaShadow.renderOrder = 1.5; fleaShadow.visible = false;
    root.add(fleaShadow);
    root.remove(fleaPivot);
    reg('flea', fleaPivot, { enterMs: 1800, pose: (o, e) => {
      o.w.position.set(0, 0, 78 * (1 - e) * (1 - e));
      meshes.flea.castShadow = o.v >= 0.999;
      fleaShadow.visible = o.v > 0.001 && o.v < 0.999; fleaShadow.material.opacity = 0.4 * e;
      const s = 0.6 + 0.4 * e; fleaShadow.scale.set(s, s, 1);
    } });
  }
  // heater PCB: rises from below upside down (components showing), flips while still below the vial, then rises into place
  {
    const g = take(['thermal_pad', 'pcb', 'pcb_copper', 'pcb_parts']);
    const pivot = new THREE.Group(); pivot.position.z = -87; g.position.z = 87; pivot.add(g);
    reg('heater', pivot, { enterMs: 3000, pose: (o) => {
      const v = o.v;
      o.w.position.set(0, 0, -70 + 45 * seg(v, 0, 0.3) + 25 * seg(v, 0.7, 1));
      pivot.rotation.x = PI * (1 - seg(v, 0.32, 0.68));
    } });
  }
  // IR LED alone (off), then one light cone out of it, then the photodiodes
  {
    reg('led', take(['led', 'led_die', 'led_legs']), {});
    ledC = centre(meshes.led_die.geometry);
    const dir = V3(-ledC.x, -ledC.y, 0).normalize();
    OBJ.led.off.set(-dir.x * 30, -dir.y * 30, 0);
    const A0 = V3(ledC.x + dir.x * 1.5, ledC.y + dir.y * 1.5, ledC.z);
    const cg = coneToGlass(A0, dir, 0.8, 0.09, 12.75, true);
    root.remove(meshes.beam);
    const cone = new THREE.Mesh(cg, beamMat); cone.renderOrder = 2; cone.userData.part = 'beam'; cone.castShadow = false; cone.receiveShadow = false;
    meshes.beam = cone;
    BEAM.uniforms.uX0.value = ledC.x; BEAM.uniforms.uX1.value = ledC.x + dir.x * 33;
    const piv = new THREE.Group(); piv.position.copy(ledC); cone.position.copy(ledC).multiplyScalar(-1); piv.add(cone);
    reg('beam', piv, { enterMs: 1600, pose: (o, e) => { const s = Math.max(0.001, e); piv.scale.set(s, s, s); } });
    const ang = Math.atan2(ledC.y, ledC.x), R = Math.hypot(ledC.x, ledC.y) + 0.5;
    const pdOff = (a) => [Math.cos(a) * 30, Math.sin(a) * 30, 0];
    reg('pd90', photodiode(ang + PI / 2, R, ledC.z), { off: pdOff(ang + PI / 2) });
    reg('pdref', photodiode(ang + 0.52, R, ledC.z), { off: pdOff(ang + 0.52) });
    // XR: your eye-spy boards at the four positions, each arriving radially
    const boards = pieces(meshes.pd_board.geometry);
    const pcbG = await stl('eyespy_pcb'), conG = await stl('eyespy_conn'), parG = await stl('eyespy_parts');
    const pcbM = phys({ color: 0x1d6b3a, roughness: 0.45, clearcoat: 0.5 }), conM = phys({ color: 0xf0ede4, roughness: 0.6 }), parM = phys({ color: 0x2a2c30, roughness: 0.4, metalness: 0.2 });
    const xr = new THREE.Group();
    for (const b of boards) {
      const c = centre(b), bb = b.boundingBox, a = Math.atan2(c.y, c.x);
      const rh = V3(Math.cos(a), Math.sin(a), 0), tg = V3(-Math.sin(a), Math.cos(a), 0);
      const g = new THREE.Group();
      for (const [geo, m] of [[pcbG, pcbM], [conG, conM], [parG, parM]]) g.add(mesh(geo, m));
      const M = new THREE.Matrix4().makeBasis(tg, V3(0, 0, 1), rh);
      M.setPosition(rh.clone().multiplyScalar(Math.hypot(c.x, c.y) - 1.6).add(tg.clone().multiplyScalar(-6.5)).add(V3(0, 0, bb.min.z)));
      g.applyMatrix4(M);
      const slot = new THREE.Group(); slot.add(g); slot.userData.rh = rh; xr.add(slot);
    }
    xr.add(take(['pd_die']));
    root.remove(meshes.pd); root.remove(meshes.pd_board);
    reg('xr', xr, { pose: (o, e) => { for (const s of xr.children) if (s.userData.rh) s.position.copy(s.userData.rh).multiplyScalar(30 * (1 - e)); } });
  }
  {
    const pc = centre(meshes.temp_probe.geometry), d = V3(-pc.x, -pc.y, 0).normalize();
    meshes.temp_fov.geometry = coneToGlass(pc, d, 0.4, Math.tan(25 * PI / 180), 13.78, false);
    meshes.temp_fov.material.side = THREE.DoubleSide;
  }
  reg('temp', take(['temp_module', 'temp_module_parts', 'temp_probe', 'temp_fov']), { off: [40, 25, 0] });

  // ---- MEP / AEP0.1 / AEP0.1.1 (ride; 40 ml frame)
  {
    // five-port cap. On the MEP the top was flat with plain 6 mm electrode holes (a push fit). A thin flat top plate with
    // 6 mm holes sits on the cap model's top face; AEP0.1's "ports" step opens its electrode holes out to the 7.8 mm O-ring holes.
    const capM = flipCap(await stl('cap5'));
    capM.material = capOld.clone(); capM.material.color.set(MEP_BLUE); capM.material.sheenColor = new THREE.Color(0x6f9bd8);
    const plate = new THREE.Mesh(lidTop(3.0), capM.material); plate.castShadow = true; plate.receiveShadow = true;
    capMEPmesh = capM; capPlate = plate;
    const g = new THREE.Group(); g.add(capM, plate);
    reg('cap5', g, { parent: ride, enterMs: 2400, exitMs: 1800, pose: twistOn });
  }
  reg('cap6', flipCap(await stl('cap6')), { parent: ride, enterMs: 2400, exitMs: 1800, pose: twistOn });
  const lifted = (o, e) => { o.w.position.set(0, 0, o.off.z * (1 - e) + 75 * par('lift')); };
  reg('cath', rod(4.8, 0, TIP_OLD, ROD_TOP, 3, ss), { parent: ride, off: [0, 0, 110], enterMs: 1800, pose: lifted });
  reg('ano', rod(-4.8, 0, TIP_OLD, ROD_TOP, 3, ptTi), { parent: ride, off: [0, 0, 110], enterMs: 1800, pose: lifted });
  reg('orings', (() => { const g = new THREE.Group(); for (const x of [-4.8, 4.8]) { const t = mesh(new THREE.TorusGeometry(3.95, 0.75, 16, 48), oringMat); t.position.set(x, 0, OLD_TOP - 1.3); g.add(t); } return g; })(), { parent: ride, off: [0, 0, 30], enterMs: 1500 });
  reg('clipC', croc(4.8, ROD_TOP - 16, 1, blackMat), { parent: ride, off: [60, 0, 0] });
  reg('clipA', croc(-4.8, ROD_TOP - 16, -1, redMat), { parent: ride, off: [-60, 0, 0] });
  const guide = new THREE.Mesh(await stl('spacer'), capOld); guide.position.z = OLD_TOP;
  reg('guide', guide, { parent: ride, off: [0, -45, 0] });     // slides in from behind, open side first
  const mkStop = async (n) => { const m = new THREE.Mesh(await stl(n), capOld); m.rotation.x = PI; m.position.z = ROD_TOP + 2; return m; };
  reg('stop01', await mkStop('topstop01'), { parent: ride, off: [0, 0, 40] });
  reg('stop011', await mkStop('topstop011'), { parent: ride, off: [0, 0, 40] });
  reg('boltC', bolt(13.3, ROD_TOP - 5, 1, blackMat), { parent: ride, off: [40, 0, 0] });
  reg('boltA', bolt(-13.3, ROD_TOP - 5, -1, redMat), { parent: ride, off: [-40, 0, 0] });
  const tIn = line('CR', LVL20 + 16, [30, 28, 120]), tOut = line('CL', LVL20, [-14, 34, 120]), tCO2 = line('BL', TIP_OLD + 2, [-26, -30, 70]);
  const ex1 = line('A', 4, [0, -26, 66]), ex2 = line('BR', 4, [26, -30, 58]);
  const IA = V3(-8, 20, 33), IB = V3(-52, 64, 33), IDIR = IB.clone().sub(IA).normalize(), ILEN = IB.distanceTo(IA);
  const lerpI = (f) => IA.clone().lerp(IB, f).toArray();
  const inoc = tube([[0, 7.8, 4], [0, 7.8, OLD_TOP - 1], [0, 7.8, OLD_TOP + 8], [-3, 13, 27], IA.toArray(), lerpI(0.25), lerpI(0.5), lerpI(0.75), IB.toArray()], 1.5875);
  inoc.o.geometry.userData.orig = Float32Array.from(inoc.o.geometry.attributes.position.array);
  inocMesh = inoc.o;
  reg('tIn', tIn.o, { parent: ride, off: [0, 0, 80] });
  reg('tOut', tOut.o, { parent: ride, off: [0, 0, 80] });
  reg('tCO2', tCO2.o, { parent: ride, off: [0, 0, 100] });
  reg('tEx', (() => { const g = new THREE.Group(); g.add(ex1.o, ex2.o, exapure(ex1.c), exapure(ex2.c)); return g; })(), { parent: ride, off: [0, 0, 70] });
  reg('filterCO2', exapure(tCO2.c, true), { parent: ride, off: [-30, -30, 40] });
  reg('tInoc', (() => { const g = new THREE.Group(); g.add(inoc.o); const ring = mesh(new THREE.RingGeometry(0.79, 1.5875, 32), silicone); ring.position.copy(inoc.c.getPoint(1)); ring.quaternion.setFromUnitVectors(V3(0, 0, 1), inoc.c.getTangent(1)); g.add(ring); return g; })(), { parent: ride, off: [0, 0, 60] });
  DRIPS.tIn = { x: IN_END[0], y: IN_END[1], z: LVL20 + 16 };
  {
    // pinch slider: threads on over the free end of the inoculation line, open hole round the tube, then slides across so the
    // tube is squeezed into the narrow slot. Its bung rides on the tube (so it can't be lost); its bar then goes into the round
    // hole, so the tube can't slip back out of the closed slot.
    const parts = pieces(await stl('pinch')).sort((a, b) => a.boundingBox.min.x - b.boundingBox.min.x);
    const pm = phys({ color: 0x2b2d31, roughness: 0.65 });
    const p = IA.clone().add(IDIR.clone().multiplyScalar(ILEN * 0.42)), tg = IDIR.clone();
    const q = new THREE.Quaternion().setFromUnitVectors(V3(0, 0, 1), tg);
    const side = V3(1, 0, 0).applyQuaternion(q);
    pinchFrame = { p, tg, sq: V3(0, 1, 0).applyQuaternion(q), side };
    const along = tg.clone().multiplyScalar(ILEN * 0.58 + 40);
    const bodyG = parts[0], bungGs = parts.slice(1);
    const bm = mesh(bodyG, pm), bd = bodyG.boundingBox.max.z - bodyG.boundingBox.min.z;
    bm.position.set(-1.8, 0, -bd / 2);                 // open hole (x = 1.8 in the part) on the tube
    const holder = new THREE.Group(); holder.add(bm); holder.quaternion.copy(q);
    reg('pinch', holder, { parent: ride, enterMs: 1600, pose: (o, e) => {
      holder.position.copy(p).add(along.clone().multiplyScalar(1 - e)).add(side.clone().multiplyScalar(4.1 * par('pinch')));
    } });
    const bung = new THREE.Group(); bung.quaternion.copy(q);
    for (const g of bungGs) { const m = mesh(g, pm); m.rotation.x = PI; m.position.set(-15.1, 0, 6); bung.add(m); }   // collar hole on the tube, bar 4.1 mm beside it
    reg('bung', bung, { parent: ride, enterMs: 1600, pose: (o, e) => {
      bung.position.copy(p).add(along.clone().multiplyScalar(1 - e)).add(tg.clone().multiplyScalar(24 * (1 - par('bung'))));
    } });
  }

  // ---- AEP0.2 top (ride; 40 ml frame)
  meshes.septum.material = phys({ color: 0xf3eee6, roughness: 0.32, transmission: 0.82, thickness: 2, ior: 1.41, attenuationColor: new THREE.Color(0xe9dcc8), attenuationDistance: 6, sheen: 0.25, sheenColor: 0xffffff });
  reg('septum02', take(['septum']), { parent: ride, off: [0, 0, 50] });
  reg('cap02', take(['cap']), { parent: ride, enterMs: 2600, exitMs: 1800, pose: twistOn });
  reg('cath02', take(['cathode']), { parent: ride, off: [0, 0, 110], enterMs: 1800 });
  {
    // anode: arrives as a rod; a bore opens down its length; a 4 mm OD / 1 mm ID silicone line goes through it
    const b = meshes.anode.geometry.boundingBox, ax = (b.min.x + b.max.x) / 2, ay = (b.min.y + b.max.y) / 2, ar = 3.0;
    const zt = meshes.anode_ti.geometry.boundingBox.max.z, zm = b.max.z;
    root.remove(meshes.anode); root.remove(meshes.anode_ti);
    const lower = mesh(ringGeo(0.001, ar, b.min.z, zm), mmo), upper = mesh(ringGeo(0.001, ar, zm, zt), tiMat);
    for (const m of [lower, upper]) m.position.set(ax, ay, 0);
    const g = new THREE.Group(); g.add(lower, upper);
    anodeParts = { lower, upper, ar, z0: b.min.z, zm, zt, cur: 0 };
    reg('ano02', g, { parent: ride, off: [0, 0, 110], enterMs: 1800 });
    const sil = mesh(ringGeo(0.5, 1.9, b.min.z + 0.2, zt, 96), silicone); sil.position.set(ax, ay, 0);
    reg('sil02', sil, { parent: ride, off: [0, 0, 105], enterMs: 2600 });
    {
      const f = new THREE.Group();
      const barb = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.95, 6, 24), exaWhite); barb.rotation.x = PI / 2; barb.position.z = zt - 3;
      const ridge = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 1.05, 1.2, 24), exaWhite); ridge.rotation.x = PI / 2; ridge.position.z = zt - 4.5;
      const hex = new THREE.Mesh(new THREE.CylinderGeometry(3.3, 3.3, 1.6, 6), exaWhite); hex.rotation.x = PI / 2; hex.position.z = zt + 0.8;
      const body = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 2.9, 9, 32), exaWhite); body.rotation.x = PI / 2; body.position.z = zt + 6.1;
      const lugs = new THREE.Mesh(new THREE.BoxGeometry(8.4, 1.6, 1.4), exaWhite); lugs.position.z = zt + 10;
      for (const m of [barb, ridge, hex, body, lugs]) { m.castShadow = true; m.receiveShadow = true; f.add(m); }
      f.position.set(ax, ay, 0);
      reg('barb02', f, { parent: ride, off: [0, 0, 40], enterMs: 1800 });
    }
  }
  {
    const sc = pieces(meshes.screws.geometry), wa = pieces(meshes.washers.geometry);
    for (const side of [-1, 1]) {
      const g = new THREE.Group();
      for (const p of sc) if (Math.sign(centre(p).x) === side) g.add(mesh(p, MATS.screws));
      for (const p of wa) if (Math.sign(centre(p).x) === side) g.add(mesh(p, MATS.washers));
      reg(side < 0 ? 'screwL02' : 'screwR02', g, { parent: ride, off: [side * 40, 0, 0], enterMs: 1400 });
    }
    root.remove(meshes.screws); root.remove(meshes.washers);
  }
  {
    // needles and their hubs: two gas outs (rear), media in and media out (front); filters on the gas outs
    const nd = pieces(meshes.needles.geometry), hb = pieces(meshes.hubs.geometry);
    root.remove(meshes.needles); root.remove(meshes.hubs);
    for (const n of nd) {
      const c = centre(n), b = n.boundingBox;
      const name = c.y < 0 ? (c.x < 0 ? 'gasL02' : 'gasR02') : (b.min.z > -20 ? 'mediaIn02' : 'mediaOut02');
      const hub = hb.filter((h) => Math.sign(centre(h).x) === Math.sign(c.x) && Math.sign(centre(h).y) === Math.sign(c.y))[0];
      let g = new THREE.Group(); g.add(mesh(n, MATS.needles)); if (hub) g.add(mesh(hub, MATS.hubs));
      const gasNeedle = c.y < 0, gInner = g;
      if (c.y < 0 && hub) {        // male-to-male luer adapter + Exapure filter on the hub
        const hp = hub.attributes.position.array, n3 = hp.length / 3, mc = V3(0, 0, 0);
        for (let i = 0; i < hp.length; i += 3) mc.add(V3(hp[i], hp[i + 1], hp[i + 2]));
        mc.multiplyScalar(1 / n3);
        let d = V3(0, 0.3, 1).normalize();                 // principal axis of the hub (power iteration on its covariance)
        for (let it = 0; it < 30; it++) {
          const nd = V3(0, 0, 0);
          for (let i = 0; i < hp.length; i += 3) { const v = V3(hp[i] - mc.x, hp[i + 1] - mc.y, hp[i + 2] - mc.z); nd.add(v.multiplyScalar(v.dot(d))); }
          d = nd.normalize();
        }
        if (d.z < 0) d.negate();
        let hmax = -1e9; for (let i = 0; i < hp.length; i += 3) hmax = Math.max(hmax, V3(hp[i] - mc.x, hp[i + 1] - mc.y, hp[i + 2] - mc.z).dot(d));
        const tp = mc.clone().add(d.clone().multiplyScalar(hmax));
        const ad = new THREE.Group();
        const a1 = mesh(new THREE.CylinderGeometry(2.1, 2.1, 9, 24), exaWhite), hx = mesh(new THREE.CylinderGeometry(3.6, 3.6, 2.4, 6), exaWhite);
        ad.add(a1, hx); ad.position.copy(tp).add(d.clone().multiplyScalar(1.0)); ad.quaternion.setFromUnitVectors(V3(0, 1, 0), d);
        gInner.add(ad, exapureAt(tp.clone().add(d.clone().multiplyScalar(2.2)), d));
      }
      if (gasNeedle) {           // turn the bent needle about its straight shaft so the two filters splay apart
        const pp = n.attributes.position.array; let sx = 0, sy = 0, k = 0;
        for (let i = 0; i < pp.length; i += 3) if (pp[i + 2] < 30) { sx += pp[i]; sy += pp[i + 1]; k++; }
        const axx = sx / k, axy = sy / k, piv = new THREE.Group();
        piv.position.set(axx, axy, 0); gInner.position.set(-axx, -axy, 0); piv.add(gInner); piv.rotation.z = c.x < 0 ? -0.75 : 0.75;
        g = piv;
      }
      reg(name, g, { parent: ride, off: [0, 0, 70], enterMs: 1600 });
      OBJ[name].tip = { x: (b.min.x + b.max.x) / 2, y: (b.min.y + b.max.y) / 2, z: b.min.z, r: Math.min(1, (b.max.x - b.min.x) / 2) };
      if (name === 'mediaIn02') DRIPS.mediaIn02 = { x: OBJ[name].tip.x, y: OBJ[name].tip.y, z: b.min.z };
    }
    if (OBJ.mediaOut02) OBJ.mediaOut02.pose = (o, e) => { o.w.position.set(0, 0, 90 * (1 - e) - par('drop')); };
  }
  // hypodermic needle through the septum at the large port, 15° from vertical
  {
    const s = syringe();
    const tip = V3(0, 4.6, 1.5), u = V3(0, Math.sin(PI / 12), Math.cos(PI / 12));
    s.quaternion.setFromUnitVectors(V3(0, 0, 1), u);
    reg('syringe', s, { parent: ride, enterMs: 10, exitMs: 10, pose: () => { s.position.copy(tip).add(u.clone().multiplyScalar(180 * (1 - par('syr')))); } });
  }

  dropMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 20, 14), waterMat, 32);
  dropMesh.count = 0; dropMesh.frustumCulled = false; dropMesh.renderOrder = 7; root.add(dropMesh);
  // guard: no NaN normals anywhere (a NaN pixel blooms into a black flash)
  scene.traverse((o) => {
    const n = o.isMesh && o.geometry.attributes.normal; if (!n) return;
    const a = n.array; for (let i = 0; i < a.length; i++) if (!Number.isFinite(a[i])) a[i] = i % 3 === 2 ? 1 : 0;
  });
  root.updateMatrixWorld(true);
}
function updateParams() {
  if (anodeParts && anodeParts.cur !== par('hole')) {
    const h = par('hole'), A = anodeParts, ri = 0.001 + 2.0 * h;
    A.lower.geometry.dispose(); A.lower.geometry = ringGeo(ri, A.ar, A.z0, A.zm, 96);
    A.upper.geometry.dispose(); A.upper.geometry = ringGeo(ri, A.ar, A.zm, A.zt, 96);
    A.cur = h;
  }
  const p = par('ports');
  if (inocMesh && pinchFrame && inocMesh.userData.p !== par('pinch')) {
    const pp = par('pinch'), g = inocMesh.geometry, o = g.userData.orig, a = g.attributes.position.array, F = pinchFrame;
    const v = new THREE.Vector3(), c = new THREE.Vector3();
    for (let i = 0; i < o.length; i += 3) {
      v.set(o[i], o[i + 1], o[i + 2]);
      const sA = v.clone().sub(F.p).dot(F.tg), w = Math.abs(sA) < 4.5 ? Math.pow(1 - (sA / 4.5) ** 2, 2) : 0;
      if (!w) { a[i] = o[i]; a[i + 1] = o[i + 1]; a[i + 2] = o[i + 2]; continue; }
      c.copy(F.p).add(F.tg.clone().multiplyScalar(sA));
      const d = v.clone().sub(c), dy = d.dot(F.sq), dx = d.dot(F.side), k = pp * w;
      d.add(F.sq.clone().multiplyScalar(dy * (-0.55 * k))).add(F.side.clone().multiplyScalar(dx * 0.45 * k));
      a[i] = c.x + d.x; a[i + 1] = c.y + d.y; a[i + 2] = c.z + d.z;
    }
    g.attributes.position.needsUpdate = true; g.computeVertexNormals(); inocMesh.userData.p = pp;
  }
  if (capMEPmesh) { capMEPmesh.material.color.copy(MEP_BLUE).lerp(capOld.color, par('pccf')); if (capPlate.userData.p !== p) { capPlate.geometry.dispose(); capPlate.geometry = lidTop(3.0 + 0.9 * p); capPlate.userData.p = p; } }
}

// ---------------------------------------------------------------- liquid set-ups (absolute; menisci keyed to the part that makes them)
const elOld = (x, key) => ({ x, y: 0, r: 3, ri: 0, z0: -71, key, el: true });
function liqCfg(name) {
  switch (name) {
    case 'old':
      return { level: L20, cat: elOld(4.8), ano: elOld(-4.8), co2: { x: CO2_END[0], y: CO2_END[1], r: 1.5, z0: TIP_OLD + 2 + DZ20 },
        men: [elOld(4.8, 'cath'), elOld(-4.8, 'ano'), { x: OUT_END[0], y: OUT_END[1], r: 1.5, z0: L20, key: 'tOut' }, { x: CO2_END[0], y: CO2_END[1], r: 1.5, z0: -69, key: 'tCO2' }] };
    case 'v40': return { level: L40, men: [] };
    case 'a02': {
      const c = meshes.cathode.geometry.boundingBox, A = anodeParts, mo = OBJ.mediaOut02.tip;
      const cat = { x: (c.min.x + c.max.x) / 2, y: (c.min.y + c.max.y) / 2, r: (c.max.x - c.min.x) / 2, z0: c.min.z };
      const ano = { x: -4.8, y: 0, r: A.ar, z0: A.z0 };
      return { level: L40, cat: { ...cat, ri: 0 }, ano: { ...ano, ri: 2.0 }, co2: ano,
        men: [{ ...cat, key: 'cath02', el: true }, { ...ano, key: 'ano02', el: true }, { x: mo.x, y: mo.y, r: mo.r, z0: mo.z, key: 'mediaOut02' }] };
    }
  }
  return { level: L20, men: [] };
}

// ---------------------------------------------------------------- the story (page: PageUp/PageDown jump points)
const STEPS = [];
const S = (id, f, page = false) => STEPS.push({ id, f, page });
const base = () => ({ web: 'home', show: new Set(), dz: DZ20, fill: 'empty', liq: 'old', gate: { H: false, O: false, CO2: false }, pulse: false,
  beam: false, tag: '', focus: null, turn: false, drip: [], par: { lift: 0, ports: 0, hole: 0, drop: 0, syr: 0, pinch: 0, bung: 0, pccf: 0 }, snap: new Set() });
const show = (s, ...n) => n.forEach((x) => s.show.add(x));
const hide = (s, ...n) => n.forEach((x) => s.show.delete(x));
const power = (s, on) => { s.gate.H = on; s.gate.O = on; };

S('home', (s) => { s.web = 'home'; }, true);
S('strap', (s) => { s.web = 'strap'; }, true);
for (const w of ['strap-sp', 'strap-sp1', 'strap-sp2', 'strap-all', 'strap-all1']) S(w, (s) => { s.web = w; });
S('mission', (s) => { s.web = 'mission'; }, true);
for (const k of ['hunger', 'poverty', 'biodiversity', 'climate', 'delicious', 'wholesome', 'sustainable', 'accessible']) S('m-' + k, (s) => { s.web = 'm-' + k; });
S('epo', (s) => { s.web = 'done'; }, true);

// --- MEP
S('mep-vial', (s) => { s.web = null; s.tag = 'MEP'; show(s, 'glass'); s.focus = 'vial20'; });
S('mep-medium', (s) => { s.fill = 'full'; });
S('mep-flea', (s) => { show(s, 'flea'); s.focus = 'base'; });
S('mep-heater', (s) => { show(s, 'heater'); s.focus = 'base'; });
S('mep-led', (s) => { show(s, 'led'); s.focus = 'optics'; });
S('mep-led-on', (s) => { show(s, 'beam'); s.beam = true; });
S('mep-pd', (s) => { show(s, 'pd90', 'pdref'); });
S('mep-cap', (s) => { show(s, 'cap5'); s.focus = 'top20'; });
S('mep-cathode', (s) => { show(s, 'cath'); s.focus = 'vial20tall'; });
S('mep-anode', (s) => { show(s, 'ano'); });
S('mep-power', (s) => { show(s, 'clipC', 'clipA'); power(s, true); s.focus2 = 'bubbles20'; });
S('mep-media-in', (s) => { show(s, 'tIn'); s.drip = ['tIn']; s.focus = 'dripOld'; });
S('mep-media-out', (s) => { show(s, 'tOut'); s.focus = 'vial20wide'; });
S('mep-co2', (s) => { show(s, 'tCO2'); s.gate.CO2 = true; s.focus = 'co2Old'; }, true);

// --- AEP0.1: same kit, plus O-rings on the electrodes, the top stop, and filters on the gas lines
S('a01-off', (s) => { s.tag = 'AEP0.1'; power(s, false); s.gate.CO2 = false; hide(s, 'clipC', 'clipA'); s.focus = 'top20tall'; });
S('a01-lift', (s) => { s.par.lift = 1; s.focus = 'top20tall'; });
S('a01-pccf', (s) => { s.par.pccf = 1; });
S('a01-ports', (s) => { s.par.ports = 1; s.focus = 'ports'; });
S('a01-orings', (s) => { show(s, 'orings'); s.focus = 'ports'; });
S('a01-rods-in', (s) => { s.par.lift = 0; s.focus = 'top20tall'; });
S('a01-guide', (s) => { show(s, 'guide'); s.flyMs = 3600; });
S('a01-stop', (s) => { show(s, 'stop01'); });
S('a01-guide-out', (s) => { hide(s, 'guide'); });
S('a01-power', (s) => { show(s, 'clipC', 'clipA'); power(s, true); s.gate.CO2 = true; s.focus = 'top20tall'; });
S('a01-co2-filter', (s) => { show(s, 'filterCO2'); s.focus = 'top20wide'; });
S('a01-gas-out', (s) => { show(s, 'tEx'); s.focus = 'top20wide'; }, true);

// --- AEP0.1.1
S('a011-bolts', (s) => { s.tag = 'AEP0.1.1'; hide(s, 'clipC', 'clipA', 'stop01'); show(s, 'stop011', 'boltC', 'boltA'); s.focus = 'top20tall'; });
S('a011-hole', (s) => { hide(s, 'cap5'); show(s, 'cap6'); s.snap.add('cap5'); s.snap.add('cap6'); s.focus = 'ports'; });
S('a011-inoc', (s) => { show(s, 'tInoc'); s.focus = 'top20wide'; });
S('a011-pinch-on', (s) => { show(s, 'pinch', 'bung'); s.focus = 'pinch'; });
S('a011-pinch', (s) => { s.par.pinch = 1; s.focus = 'pinch'; });
S('a011-bung', (s) => { s.par.bung = 1; s.focus = 'pinch'; });
S('a011-pulse', (s) => { s.pulse = true; s.focus = 'vial20wide'; }, true);

// --- AEP0.2
S('a02-off', (s) => { s.tag = 'AEP0.2'; power(s, false); s.gate.CO2 = false; s.pulse = false; s.drip = [];
  hide(s, 'cap6', 'orings', 'cath', 'ano', 'stop011', 'boltC', 'boltA', 'tIn', 'tOut', 'tCO2', 'tEx', 'filterCO2', 'tInoc', 'pinch', 'bung', 'pd90', 'pdref'); s.focus = 'vial20wide'; });
S('a02-vial', (s) => { s.liq = 'v40'; s.dz = 0; s.focus = 'vial40'; });
S('a02-septum', (s) => { s.liq = 'a02'; show(s, 'septum02'); s.focus = 'top40'; });
S('a02-cap', (s) => { show(s, 'cap02'); });
S('a02-xr', (s) => { show(s, 'xr'); s.focus = 'optics'; });
S('a02-temp', (s) => { show(s, 'temp'); s.focus = 'tempv'; });
S('a02-cathode', (s) => { show(s, 'cath02'); s.focus = 'vial40'; });
S('a02-anode', (s) => { show(s, 'ano02'); });
S('a02-screws', (s) => { show(s, 'screwL02', 'screwR02'); s.focus = 'top40'; });
S('a02-power', (s) => { power(s, true); s.focus = 'bubbles40'; });
S('a02-bore', (s) => { s.par.hole = 1; s.focus = 'anodeTop'; });
S('a02-co2-line', (s) => { show(s, 'sil02'); s.focus = 'anodeTop'; });
S('a02-barb', (s) => { show(s, 'barb02'); s.focus = 'anodeTop'; });
S('a02-co2', (s) => { s.gate.CO2 = true; s.focus = 'anodeBase'; });
S('a02-gas1', (s) => { show(s, 'gasL02'); s.focus = 'top40wide'; });
S('a02-gas2', (s) => { show(s, 'gasR02'); s.focus = 'top40wide'; });
S('a02-media-in', (s) => { show(s, 'mediaIn02'); s.drip = ['mediaIn02']; s.focus = 'drip02'; });
S('a02-media-out', (s) => { show(s, 'mediaOut02'); s.focus = 'vial40'; });
S('a02-lower', (s) => { s.par.drop = 5; });
S('a02-raise', (s) => { s.par.drop = 0; });
S('a02-syringe-in', (s) => { show(s, 'syringe'); s.par.syr = 1; s.focus = 'septumPort'; });
S('a02-syringe-out', (s) => { show(s, 'syringe'); s.par.syr = 0; });
S('a02-run', (s) => { hide(s, 'syringe'); s.pulse = true; s.focus = 'vial40'; }, true);

function stateAt(i) { const s = base(); for (let k = 0; k <= i; k++) { s.focus = null; s.focus2 = null; s.flyMs = 0; s.snap = new Set(); STEPS[k].f(s); } return s; }

// ---------------------------------------------------------------- camera
const CAM_KEY = 'aep-pres-cams-v3';
let CAMS = {};
try { CAMS = JSON.parse(document.getElementById('cams-data').textContent || '{}'); } catch (e) { CAMS = {}; }
try { Object.assign(CAMS, JSON.parse(localStorage.getItem(CAM_KEY) || '{}')); } catch (e) { /* private window */ }
const DIR = V3(-0.55, 0.42, -1.0);
function focusBox(f) {
  // [zmin, zmax, radius, margin, cx, cy, dir] in OpenSCAD mm (absolute); world: x = x, y = z, z = -y
  const D = DZ20;
  const F = {
    vial20: [-90, 25 + D, 18, 1.0], vial20tall: [-90, 62 + D, 20, 1.0], vial20wide: [-90, 75 + D, 26, 1.0], vial40: [-92, 88, 20, 0.95],
    base: [-92, -62, 22, 1.2], optics: [-88, -52, 26, 1.0], top20: [-12 + D, 30 + D, 18, 1.25], top20tall: [-12 + D, 70 + D, 20, 1.1],
    top20wide: [-15 + D, 75 + D, 28, 1.1], top40: [-25, 90, 22, 1.0], top40wide: [-10, 110, 30, 1.0], tempv: [-60, 0, 28, 1.25],
    ports: [OLD_TOP - 14 + D, OLD_TOP + 10 + D, 12, 1.15, 0, 0, V3(-0.4, 1.0, -0.8)],
    co2Old: [-82, -50, 11, 1.2, CO2_END[0], CO2_END[1], V3(0.25, 0.55, -1.0)],
    anodeTop: [20, 44, 8, 1.3, -4.8, 0, V3(-0.5, 1.0, -0.8)], anodeBase: [-72, -52, 8, 1.2, -4.8, 0, V3(-0.6, 0.15, -1.0)],
    bubbles20: [-76, -46, 13, 1.05], bubbles40: [-68, -18, 13, 1.05],
    pinch: [38 + D - 14, 38 + D + 14, 14, 1.1, -24, 42, V3(-0.7, 0.45, -1.0)],
    dripOld: [-58 , -30, 9, 1.15, 2.8, 4.6, V3(0.5, 0.35, -1.0)], drip02: [-30, -8, 9, 1.15, -3.4, 5.9, V3(-0.5, 0.35, -1.0)],
    septumPort: [-10, 60, 22, 1.0, 0, 6, V3(-1.0, 0.5, -0.6)],
  }[f] || [-90, 45, 20, 1.0];
  const [z0, z1, r, m, cx = 0, cy = 0, dir = DIR] = F;
  return { box: new THREE.Box3(V3(cx - r, z0, -cy - r), V3(cx + r, z1, -cy + r)), margin: m, dir };
}
function shot(i) {
  const id = STEPS[i].id;
  if (CAMS[id]) { const c = CAMS[id]; return { pos: V3(...c.p), target: V3(...c.t) }; }
  if (i > 0 && !stateAt(i).focus && stateAt(i - 1).web === null) return shot(i - 1);
  let f = null; for (let k = i; !f && k >= 0; k--) f = stateAt(k).focus;
  const { box, margin, dir } = focusBox(f || 'vial20');
  return viewFrom(box, dir, margin * 0.95);
}
let busyUntil = 0;
function flyTo(v, dur = 1600) {
  if (REDUCED || !dur) { tween = null; camera.position.copy(v.pos); controls.target.copy(v.target); return; }
  resumeTurn = false; controls.autoRotate = false;
  tween = { t0: performance.now(), dur, p0: camera.position.clone(), q0: controls.target.clone(), p1: v.pos, q1: v.target };
  busyUntil = Math.max(busyUntil, performance.now() + dur);
}

// ---------------------------------------------------------------- applying a state
let cur = null, idx = -1, rideZ = DZ20, rideFrom = DZ20, rideT0 = 0, rideDur = 0, rideTo = DZ20;
let fillFrom = 0, fillTo = null, fillT0 = 0, fillDur = 0, liqKey = null;
let pulseOn = false, pulseT = 0, dripOn = [], manualTurn = null, pendingShot = null;
const drops = [];

function setVis(o, v) {
  o.v = v;
  const e = v <= 0 ? 0 : v >= 1 ? 1 : ease(v);
  o.w.visible = v > 0.001;
  if (o.pose) o.pose(o, e); else o.w.position.copy(o.off).multiplyScalar(1 - e);
}
const targetLevel = (s) => (s.fill === 'empty' ? LIQUID.zFloor : liqCfg(s.liq).level - s.par.drop);
function apply(i, instant = false) {
  const s = stateAt(i);
  webShow(s.web, instant);
  const tag = $('vtag');
  if (tag.textContent !== s.tag) { tag.classList.remove('in'); setTimeout(() => { tag.textContent = s.tag; if (s.tag) tag.classList.add('in'); }, instant ? 0 : 250); }
  else if (s.tag) tag.classList.add('in');
  const out = [], inn = [];
  for (const o of Object.values(OBJ)) {
    const want = s.show.has(o.name) ? 1 : 0;
    if (want === o.target) continue;
    o.target = want; (want ? inn : out).push(o);
  }
  const t = performance.now();
  let end = t;
  for (const o of out) { o.t0 = t; o.dur = s.snap.has(o.name) ? 0 : o.exitMs; o.from = o.v; end = Math.max(end, t + o.dur); }
  let inDelay = out.some((o) => !s.snap.has(o.name)) ? 800 : 0;
  const nextShot = s.web === null && !instant ? shot(i) : null;
  if (nextShot && cur && cur.web === null && (nextShot.pos.distanceTo(camera.position) > 8 || nextShot.target.distanceTo(controls.target) > 4)) inDelay = Math.max(inDelay, 1500);
  for (const o of inn) { o.t0 = t + inDelay; o.dur = s.snap.has(o.name) ? 0 : o.enterMs; o.from = o.v; end = Math.max(end, o.t0 + o.dur); }
  for (const [k, v] of Object.entries(s.par)) {
    const p = PAR[k] || (PAR[k] = { v, from: v, to: v, t0: 0, dur: 0 });
    if (instant) { p.v = p.from = p.to = v; p.dur = 0; }
    else if (p.to !== v) { p.from = p.v; p.to = v; p.t0 = t + inDelay; p.dur = k === 'syr' ? 2600 : 1700; end = Math.max(end, p.t0 + p.dur); }
  }
  if (s.dz !== rideTo) { rideFrom = rideZ; rideTo = s.dz; rideT0 = t + (out.length ? 1000 : 0); rideDur = 2400; end = Math.max(end, rideT0 + rideDur); }
  if (s.liq !== liqKey) {
    liqKey = s.liq;
    const keep = LIQUID.level;
    LIQUID.configure(liqCfg(s.liq));
    LIQUID.setFill(cur && !instant ? keep : targetLevel(s));
  }
  const target = targetLevel(s);
  if (instant) { fillDur = 0; LIQUID.setFill(target); fillTo = target; }
  else if (target !== fillTo) {
    fillFrom = LIQUID.level; fillTo = target;
    fillT0 = t + (cur && s.dz !== cur.dz ? 1800 : 0) + (cur && s.par.drop !== cur.par.drop ? inDelay + 1500 : 0);
    fillDur = Math.abs(target - fillFrom) > 15 ? 3400 : 1700;
    end = Math.max(end, fillT0 + fillDur);
  }
  pulseOn = s.pulse; dripOn = s.drip;
  const delay = instant ? 0 : (inn.length ? 1400 : 300);
  clearTimeout(apply.gt);
  apply.gt = setTimeout(() => {
    LIQUID.setGate('H', s.gate.H); LIQUID.setGate('O', s.gate.O);
    if (!s.pulse) LIQUID.setGate('CO2', s.gate.CO2);
    pulseT = 0;
  }, delay);
  if (!s.gate.H) LIQUID.setGate('H', false);
  if (!s.gate.O) LIQUID.setGate('O', false);
  if (!s.gate.CO2) LIQUID.setGate('CO2', false);
  if (instant) { for (const o of Object.values(OBJ)) { o.t0 = 0; o.dur = 0; setVis(o, o.target); } rideZ = rideTo = s.dz; ride.position.z = rideZ; setBeam(s.beam); updateParams(); }
  else if (!cur || s.beam !== cur.beam) setBeam(s.beam);
  busyUntil = end + 300;
  controls.autoRotate = false; resumeTurn = false;
  if (s.web === null) flyTo(nextShot || shot(i), instant ? 0 : (s.flyMs || 1900));
  manualTurn = null;
  pendingShot = s.web === null && s.focus2 && !CAMS[STEPS[i].id + ':2'] ? (() => { const { box, margin, dir } = focusBox(s.focus2); return viewFrom(box, dir, margin * 0.95); })() : (CAMS[STEPS[i].id + ':2'] ? { pos: V3(...CAMS[STEPS[i].id + ':2'].p), target: V3(...CAMS[STEPS[i].id + ':2'].t) } : null);
  if (instant && pendingShot) { flyTo(pendingShot, 0); pendingShot = null; }
  cur = s; idx = i;
  $('stepno').textContent = `${i + 1} / ${STEPS.length} · ${STEPS[i].id}`;
  try { history.replaceState(null, '', '#' + STEPS[i].id); } catch (e) { /* file:// */ }
}
const M4 = new THREE.Matrix4();
function animate() {
  const t = performance.now(), dt = 1 / 60;
  for (const o of Object.values(OBJ)) {
    if (o.v === o.target || o.t0 === undefined || t < o.t0) continue;
    const k = o.dur ? Math.min(1, (t - o.t0) / o.dur) : 1;
    setVis(o, o.from + (o.target - o.from) * k);
  }
  let parMoved = false;
  for (const p of Object.values(PAR)) {
    if (p.v === p.to || t < p.t0) continue;
    const k = p.dur ? Math.min(1, (t - p.t0) / p.dur) : 1;
    p.v = k >= 1 ? p.to : p.from + (p.to - p.from) * ease(k); parMoved = true;
  }
  if (parMoved) { updateParams(); for (const o of Object.values(OBJ)) if (o.pose && o.w.visible) o.pose(o, o.v >= 1 ? 1 : ease(o.v)); }
  if (rideZ !== rideTo && t >= rideT0) {
    const k = Math.min(1, (t - rideT0) / rideDur);
    rideZ = rideFrom + (rideTo - rideFrom) * ease(k); ride.position.z = rideZ;
    if (k >= 1) rideZ = rideTo;
  }
  if (fillDur && t >= fillT0) {
    const k = Math.min(1, (t - fillT0) / fillDur);
    LIQUID.setFill(fillFrom + (fillTo - fillFrom) * (1 - Math.pow(1 - k, 2)));
    if (k >= 1) fillDur = 0;
  }
  if (pulseOn && cur) { pulseT += dt; LIQUID.setGate('CO2', cur.gate.CO2 && (pulseT % 11) < 4); }
  // turntable: starts once everything has finished moving (so you know a step is done); the tag toggles it
  if (pendingShot && !tween && t > busyUntil - 300) { const v = pendingShot; pendingShot = null; flyTo(v, 1700); busyUntil = t + 2000; }
  if (cur && cur.web === null && !editing && !tween) controls.autoRotate = manualTurn !== null ? manualTurn : (STEPS[idx].page && t > busyUntil);
  // menisci follow the parts that make them: only once the part's tip is below the surface
  for (const m of LIQUID.mens) {
    const o = OBJ[m.key];
    m.m.visible = !!(o && o.w.visible && m.z0 + o.w.position.z < LIQUID.level - 0.05);
  }
  // drips from the media-in lines
  for (const key of dripOn) {
    const d = DRIPS[key], o = OBJ[key];
    if (!d || !o || o.v < 0.999) continue;
    d.next = (d.next || 0) - dt;
    if (d.next <= 0) { d.next = 1.1 + Math.random() * 0.5; drops.push({ x: d.x, y: d.y, z: d.z + ride.position.z, r: 0.2, age: 0, v: 0, zz: d.z + ride.position.z }); }
  }
  let n = 0;
  for (let i = drops.length - 1; i >= 0; i--) {
    const p = drops[i]; p.age += dt;
    if (p.age < 0.6) { p.r = 0.2 + 0.9 * p.age / 0.6; p.zz = p.z - p.r; }
    else { p.v += 900 * dt; p.zz -= p.v * dt; }
    if (p.zz <= LIQUID.level) { LIQUID.ripple(p.x, p.y, 0.25); drops.splice(i, 1); continue; }
    M4.makeScale(p.r * 0.9, p.r * 0.9, p.r * (p.age < 0.6 ? 1 : 1.3)).setPosition(p.x, p.y, p.zz);
    if (n < 32) dropMesh.setMatrixAt(n++, M4);
  }
  if (dropMesh) { dropMesh.count = n; dropMesh.instanceMatrix.needsUpdate = true; }
}
window.__viewerFrameHooks.push(animate);

const WEB = $('web');
function webShow(w, instant) {
  WEB.classList.toggle('gone', w === null);
  document.body.classList.toggle('on3d', w === null);
  if (w === null) return;
  const home = w === 'home';
  WEB.dataset.page = home ? 'home' : 'about';
  WEB.dataset.step = w;
  const M = w.startsWith('m-') ? { b: 'mission', ring: w.slice(2), lines: [w.slice(2)] }
    : ({ strap: { b: 'strap' }, 'strap-sp': { b: 'strap', ring: 'sp' }, 'strap-sp1': { b: 'strap', ring: 'sp', lines: ['sp1'] }, 'strap-sp2': { b: 'strap', ring: 'sp', lines: ['sp1', 'sp2'] },
      'strap-all': { b: 'strap', ring: 'all' }, 'strap-all1': { b: 'strap', ring: 'all', lines: ['all'] }, mission: { b: 'mission' }, done: { b: 'done' } }[w] || {});
  WEB.querySelectorAll('[data-k]').forEach((el) => el.classList.toggle('lit', el.dataset.k === M.ring));
  WEB.querySelectorAll('[data-l]').forEach((el) => el.classList.toggle('on', (M.lines || []).includes(el.dataset.l)));
  WEB.querySelectorAll('[data-b]').forEach((el) => el.classList.toggle('on', el.dataset.b === M.b));
  if (!home && cur && cur.web === 'home' && !instant) {
    const b = $('missionBtn'); b.classList.add('press');
    WEB.dataset.page = 'home';
    setTimeout(() => { b.classList.remove('press'); WEB.dataset.page = 'about'; }, 450);
  }
}

// ---------------------------------------------------------------- input
let editing = false;
function next() { if (idx < STEPS.length - 1) apply(idx + 1); }
function prev() { if (idx > 0) apply(idx - 1); }
// pages: the amybo.org pages, electroPioreactor.org, then each reactor version in its finished state (jumped to directly)
const jump = (i) => apply(i, stateAt(i).web === null);
function nextPage() { let i = idx + 1; while (i < STEPS.length && !STEPS[i].page) i++; if (i < STEPS.length) jump(i); }
function prevPage() { let i = idx - 1; while (i > 0 && !STEPS[i].page) i--; if (i >= 0 && i < idx) jump(i); }
addEventListener('keydown', (e) => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const k = e.key;
  if (['ArrowRight', 'ArrowDown', ' ', 'Enter', 'n'].includes(k)) { e.preventDefault(); next(); }
  else if (['ArrowLeft', 'ArrowUp', 'Backspace', 'p'].includes(k)) { e.preventDefault(); prev(); }
  else if (k === 'PageDown') { e.preventDefault(); nextPage(); }
  else if (k === 'PageUp') { e.preventDefault(); prevPage(); }
  else if (k === 'Escape' && MENU.classList.contains('open')) { e.preventDefault(); toggleMenu(false); }
  else if (k === 'm' || k === 'M') toggleMenu();
  else if (k === 'Home') apply(0, true);
  else if (k === 'End') apply(STEPS.length - 1, true);
  else if (k === 'b' || k === 'B' || k === '.') document.body.classList.toggle('blackout');
  else if (k === 'f' || k === 'F') { if (!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.(); }
  else if (k === 'e' || k === 'E') { editing = !editing; document.body.classList.toggle('editing', editing); controls.autoRotate = false; }
  else if (editing && (k === 's' || k === 'S')) {
    const key = STEPS[idx].id + (e.shiftKey && cur && cur.focus2 ? ':2' : '');
    CAMS[key] = { p: camera.position.toArray().map((x) => +x.toFixed(2)), t: controls.target.toArray().map((x) => +x.toFixed(2)) };
    try { localStorage.setItem(CAM_KEY, JSON.stringify(CAMS)); } catch (e) { /* ignore */ }
    flash('Saved camera for ' + key);
  }
  else if (editing && (k === 'c' || k === 'C')) {
    const txt = JSON.stringify(CAMS);
    navigator.clipboard?.writeText(txt).then(() => flash('Copied ' + Object.keys(CAMS).length + ' cameras'), () => { prompt('Copy this:', txt); });
  }
  else if (editing && (k === 'x' || k === 'X')) { delete CAMS[STEPS[idx].id]; try { localStorage.setItem(CAM_KEY, JSON.stringify(CAMS)); } catch (e) { /* ignore */ } flash('Cleared camera for ' + STEPS[idx].id); apply(idx); }
});
WEB.addEventListener('click', (e) => { if (e.pointerType !== 'touch' && !(e.sourceCapabilities && e.sourceCapabilities.firesTouchEvents)) next(); });
$('vtag').addEventListener('click', (e) => { e.stopPropagation(); manualTurn = !controls.autoRotate; controls.autoRotate = manualTurn; flash(manualTurn ? 'Turntable on' : 'Turntable off'); });
// AMYBO logo: menu of the main pages (a version's name starts it from scratch, "finished" jumps to its end state)
const MENU = $('menu');
function toggleMenu(on = !MENU.classList.contains('open')) { MENU.classList.toggle('open', on); }
{ const at = (id) => STEPS.findIndex((s) => s.id === id);
  const startOf = (i) => () => { if (i > 0) apply(i - 1, true); apply(i); };
  const rows = [['Front page', at('home')], ['Sustainable Protein for All', at('strap')], ['Mission statement', at('mission')], ['electroPioreactor.org', at('epo')]];
  const vers = [['MEP', 'mep-vial', 'mep-co2'], ['AEP0.1', 'a01-off', 'a01-gas-out'], ['AEP0.1.1', 'a011-bolts', 'a011-pulse'], ['AEP0.2', 'a02-off', 'a02-run']];
  const add = (label, fn, cls = '') => { const b = document.createElement('button'); b.textContent = label; b.className = cls; b.addEventListener('click', (e) => { e.stopPropagation(); toggleMenu(false); fn(); }); return b; };
  for (const [t, i] of rows) { const r = document.createElement('div'); r.className = 'row'; r.append(add(t, () => apply(i, true))); MENU.append(r); }
  for (const [t, a, b] of vers) { const r = document.createElement('div'); r.className = 'row'; r.append(add(t, startOf(at(a))), add('finished', () => jump(at(b)), 'end')); MENU.append(r); }
  $('logo').addEventListener('click', (e) => { e.stopPropagation(); toggleMenu(); });
  MENU.addEventListener('click', (e) => e.stopPropagation());
  addEventListener('click', (e) => { if (MENU.classList.contains('open') && !e.target.closest('#menu, #logo')) toggleMenu(false); }, true);
}
// touch (phone/tablet): tap the right of the screen for next, the left for back; drag still turns the model
{ let d = null;
  addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') d = { x: e.clientX, y: e.clientY, t: performance.now() }; }, true);
  addEventListener('pointerup', (e) => {
    if (e.pointerType === 'mouse' || !d || e.target.closest('#vtag, #logo, #menu')) { d = null; return; }
    if (Math.hypot(e.clientX - d.x, e.clientY - d.y) < 10 && performance.now() - d.t < 400) (e.clientX > innerWidth * 0.35 ? next : prev)();
    d = null;
  }, true); }
// the cursor hides while the presentation runs and comes back when the mouse moves
{ let ct = 0; const wake = () => { document.body.classList.remove('idle'); clearTimeout(ct); ct = setTimeout(() => document.body.classList.add('idle'), 1500); };
  addEventListener('mousemove', wake); addEventListener('mousedown', wake); wake(); }
function flash(msg) { const f = $('flash'); f.textContent = msg; f.classList.add('show'); clearTimeout(flash.t); flash.t = setTimeout(() => f.classList.remove('show'), 1800); }

// ---------------------------------------------------------------- go
(async () => {
  let ok = false;
  try { ok = await loadAll(); }
  catch (e) { console.error(e); fail('Could not load the model', String(e && e.message || e)); }
  if (!ok) return;
  setupFlea();
  root.updateMatrixWorld(true);
  computeViews();
  placeLights();
  await buildScene();
  setWhite(false);
  bloom.threshold = 9; bloom.strength = 0.5;
  setTurn(false);
  controls.autoRotateSpeed = 0.9;
  goView('assembly', true);
  // compile every material up front: first-use shader compiles were stalling frames (stutter / flashes) mid-talk
  if (window.__noPrecompile) { renderer.shadowMap.enabled = false; bloom.enabled = false; renderer.setPixelRatio(0.6); resize(); }   // test harness only: software GL
  if (!window.__noPrecompile) try {
    $('statusS').textContent = 'Preparing materials';
    const vis = Object.values(OBJ).map((o) => [o, o.w.visible]);
    for (const [o] of vis) { o.w.visible = true; if (o.extra) for (const x of o.extra) x.visible = true; }
    for (const s of sleeves) s.visible = true;
    await (renderer.compileAsync ? renderer.compileAsync(scene, camera) : Promise.resolve(renderer.compile(scene, camera)));
    composer.render(0);
    for (const [o, v] of vis) o.w.visible = v;
  } catch (e) { console.warn('precompile', e); }
  const start = Math.max(0, STEPS.findIndex((s) => '#' + s.id === location.hash));
  window.__dbg = 'apply'; apply(start, true);
  window.__dbg = 'frame'; frame(); window.__dbg = 'framed';
  $('status').classList.add('gone');
  renderer.setAnimationLoop(frame);
  requestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; document.documentElement.dataset.ready = '1'; }));
  window.__pres = { apply, STEPS, OBJ, LIQUID, get idx() { return idx; } };
})();
