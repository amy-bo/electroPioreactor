import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { mergeVertices, toCreasedNormals } from 'three/addons/utils/BufferGeometryUtils.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';

const PARTS = JSON.parse(document.getElementById('parts-data').textContent);
const EXTRA = JSON.parse(document.getElementById('extra-data').textContent);
const META = {};

// ---------------------------------------------------------------- setup
const $ = (id) => document.getElementById(id);
const app = $('app');
const STILL = /(^|[#&])still\b/.test(location.hash);
const WHITE0 = /(^|[#&])white\b/.test(location.hash) || document.documentElement.classList.contains('white');   // a host page can pre-set .white
const HASH_VIEW = (location.hash.match(/[#&](assembly|cap|optics|base)\b/) || [])[1];
const REDUCED = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
if (STILL) app.classList.add('still');

function fail(title, detail) {
  const card = $('statusCard');
  card.classList.add('error');
  $('statusT').textContent = title;
  $('statusS').textContent = detail;
  card.querySelector('.progress').style.display = 'none';
  $('status').classList.remove('gone');
}

if (META && META.built) {
  const d = String(META.built).slice(0, 10);
  const el = $('built'); el.textContent = 'Built ' + d; el.hidden = false;
}

function webglOK() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGL2RenderingContext && c.getContext('webgl2'));
  } catch (e) { return false; }
}

const INFO = {
  cap: 'Vial Cap · one-piece PC-CF print · GPI 24-400 thread',
  septum: 'Septum · 2 mm silicone',
  cathode: 'Cathode · 316 stainless rod · 100 mm × Ø6 mm',
  anode: 'Anode · MMO-coated Ti tube · 100 mm, 6 OD / 4 ID · 70 mm active',
  anode_ti: 'Anode · bare Ti above the 70 mm MMO coating',
  needles: 'Needles · 14 G blunt (Media Out 80 mm, Media In + 2 gas outlets bent 15°, 75 mm)',
  hubs: 'Luer-lock hubs',
  screws: 'Knurled M3 thumb screws',
  washers: 'M3 washers',
  glass: '40 ml borosilicate vial · 27.5 × 95 mm · 24-400 neck',
  flea: 'Stir flea · PTFE rounded-end rod 15 × 5 mm',
  thermal_pad: 'Thermal pad',
  pcb: 'Heater PCB · Pioreactor aluminium-core board, 27.5 mm · 15 × 3.9 Ω resistors underneath', pcb_copper: 'Heater PCB · pads (underside)', pcb_parts: 'Heater PCB · resistors, TMP1075, hall sensor, 7-way FFC socket (underside)',
  led: 'IR LED · 5 mm · the one LED fitted in the XR optics', led_die: 'IR LED · 5 mm', led_legs: 'IR LED · 5 mm',
  pd: 'XR eye-spy photodiode · Vishay VEMD2000 · 45°, REF, 90°, 135°', pd_die: 'XR eye-spy photodiode · Vishay VEMD2000', pd_board: 'XR eye-spy board · 45°, REF, 90°, 135° from the IR LED',
  temp_module: 'Precision temperature upgrade · Adafruit MLX90632 board in the SPEC pocket',
  temp_module_parts: 'Precision temperature upgrade · STEMMA-QT sockets',
  temp_fov: 'MLX90632 field of view (50°) · reads the vial wall at the liquid',
  temp_probe: 'MLX90632 non-contact IR thermometer · reads the vial wall',
  beam: 'IR light path (shown red; invisible in life)',
};

if (!webglOK()) {
  fail('WebGL is not available', 'This 3D viewer needs WebGL 2. Try a current Chrome, Edge, Firefox or Safari with hardware acceleration enabled.');
  throw new Error('no webgl');
}
if (typeof DecompressionStream === 'undefined') {
  fail('Browser too old', 'This viewer needs DecompressionStream (Chrome 80+, Firefox 113+, Safari 16.4+).');
  throw new Error('no DecompressionStream');
}

// ---------------------------------------------------------------- renderer
const stage = $('stage');
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: false,   /* AA comes from the composer's MSAA target */ preserveDrawingBuffer: true, powerPreference: 'high-performance' });
} catch (e) {
  fail('WebGL could not start', String(e && e.message || e));
  throw e;
}
// phones/tablets (coarse pointer): DPR capped lower and 2x MSAA; desktop: DPR <= 2 and 4x MSAA
const COARSE = window.matchMedia && matchMedia('(pointer: coarse)').matches;
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, COARSE ? 1.75 : 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
stage.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.7;

// studio backdrop: deep blue-slate radial gradient, dithered against banding
const DARK_BG = (() => {
  const S = 512, c = document.createElement('canvas'); c.width = c.height = S;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(S * 0.5, S * 0.42, 0, S * 0.5, S * 0.5, S * 0.78);
  grd.addColorStop(0, '#34465f');
  grd.addColorStop(0.45, '#1c2738');
  grd.addColorStop(1, '#090d15');
  g.fillStyle = grd; g.fillRect(0, 0, S, S);
  const img = g.getImageData(0, 0, S, S), d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    const n = (Math.random() - 0.5) * 3;
    d[i] += n; d[i + 1] += n; d[i + 2] += n;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();
scene.background = DARK_BG;

const camera = new THREE.PerspectiveCamera(32, 1, 1, 4000);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotateSpeed = 0.7;
controls.minDistance = 25;
controls.maxDistance = 1200;

// The composer renders the scene off-screen, so the canvas's own antialias does nothing for it:
// without a multisampled target every thin edge (needles, knurls, cap striations, boards) crawls
// as the turntable moves. A 4x MSAA half-float target fixes the crawl at the source.
const composer = new EffectComposer(renderer, new THREE.WebGLRenderTarget(1, 1, {
  type: THREE.HalfFloatType, samples: Math.min(COARSE ? 2 : 4, renderer.capabilities.maxSamples || 4),
}));
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.7, 0.45, 3.6);
composer.addPass(bloom);
composer.addPass(new OutputPass());
// white page: tone mapping turns a white backdrop light grey; lift the white point so the page is pure #fff
const whitePoint = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uWhite: { value: 0.885 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: 'uniform sampler2D tDiffuse; uniform float uWhite; varying vec2 vUv; void main(){ vec4 c = texture2D(tDiffuse, vUv); gl_FragColor = vec4(min(c.rgb / uWhite, vec3(1.0)), c.a); }',
});
whitePoint.enabled = false;
composer.addPass(whitePoint);

// ---------------------------------------------------------------- materials
const phys = (o) => new THREE.MeshPhysicalMaterial(o);
const capMat = phys({ color: '#2b2d31',   /* PC-CF charcoal */ roughness: 0.65, metalness: 0, clearcoat: 0, clearcoatRoughness: 0.4, sheen: 0.25, sheenRoughness: 0.8, sheenColor: 0x50555e });
const steel = (r) => phys({ color: 0xbfc3c9, metalness: 1, roughness: r + 0.1, envMapIntensity: 0.42 });   // brushed/satin: the room's ceiling panels were mirroring off flat metal faces as big white glare

const ledDieMat = new THREE.MeshStandardMaterial({ color: 0x220000, emissive: 0xff1a20, emissiveIntensity: 60 });
const pdDieMat = phys({ color: 0x241a3d, metalness: 0.15, roughness: 0.18, iridescence: 1, iridescenceIOR: 1.9, iridescenceThicknessRange: [180, 520], clearcoat: 1, emissive: 0xff2030, emissiveIntensity: 0.6 });

const BEAM = {
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(1.0, 0.13, 0.22) },
    uIntensity: { value: 3.2 },
    uX0: { value: 1 }, uX1: { value: -1 }, uWhite: { value: 0 },
  },
  vertexShader: /* glsl */`
    varying vec3 vObj; varying vec3 vN; varying vec3 vV;
    void main() {
      vObj = position;
      vec4 mv = modelViewMatrix * vec4(position, 1.0);
      vN = normalize(normalMatrix * normal);
      vV = -mv.xyz;
      gl_Position = projectionMatrix * mv;
    }`,
  fragmentShader: /* glsl */`
    uniform float uTime, uIntensity, uX0, uX1, uWhite; uniform vec3 uColor;
    varying vec3 vObj; varying vec3 vN; varying vec3 vV;
    void main() {
      float ndv = abs(dot(normalize(vN), normalize(vV)));
      float core = pow(ndv, 2.2);                       // bright through the middle, soft at the silhouette
      float t = clamp((uX0 - vObj.x) / (uX0 - uX1), 0.0, 1.0);   // 0 at the LED, 1 at the photodiode
      float along = mix(1.0, 0.32, pow(t, 0.8)) * smoothstep(0.0, 0.03, t) * (0.55 + 0.45 * smoothstep(1.0, 0.9, t));
      float flow = 0.78 + 0.22 * sin(vObj.x * 1.35 + uTime * 5.0) * (0.6 + 0.4 * sin(vObj.x * 0.37 + uTime * 2.1));
      vec3 col = uColor * core * along * flow * uIntensity;
      col += vec3(1.0, 0.55, 0.6) * pow(ndv, 9.0) * along * 0.9;  // hot white-pink core
      if (uWhite > 0.5) {                               // white page: normal blending, alpha carries the beam
        float a = clamp(core * along * flow * 1.5 + pow(ndv, 9.0) * along * 0.35, 0.0, 0.92);
        gl_FragColor = vec4(mix(vec3(0.93, 0.08, 0.18), vec3(1.0, 0.35, 0.42), pow(ndv, 9.0)), a);
      } else gl_FragColor = vec4(col, 1.0);
    }`,
};
const beamMat = new THREE.ShaderMaterial({
  uniforms: BEAM.uniforms, vertexShader: BEAM.vertexShader, fragmentShader: BEAM.fragmentShader,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
});

const MATS = {
  cap: capMat,
  glass: phys({
    color: 0xffffff, metalness: 0, roughness: 0.07, transmission: 1, ior: 1.5, thickness: 1.5,
    attenuationColor: new THREE.Color(0x9fe0d0), attenuationDistance: 40,
    specularIntensity: 0.85, specularColor: 0xffffff, envMapIntensity: 1.2, clearcoat: 0.15, clearcoatRoughness: 0.18,   // softer: a sharp glass highlight was blooming
    depthWrite: false,   // lets the additive light path draw inside the vial
  }),
  septum: phys({ color: 0xf2ede4, roughness: 0.45, transmission: 0.3, thickness: 2, ior: 1.41, sheen: 0.4, sheenColor: 0xffffff }),
  cathode: steel(0.34),
  anode_ti: phys({ color: 0xa3a39f, metalness: 1, roughness: 0.55, envMapIntensity: 0.45 }),
  anode: phys({ color: 0x4d5560, metalness: 0.6, roughness: 0.5, iridescence: 0.25, iridescenceIOR: 1.6, iridescenceThicknessRange: [250, 420] }),
  needles: steel(0.3),
  screws: phys({ color: 0xaaaeb4, metalness: 1, roughness: 0.56, envMapIntensity: 0.36 }),   // flat knurled heads face the camera: the worst glare
  washers: steel(0.4),
  led_legs: phys({ color: 0xc4c6ca, metalness: 1, roughness: 0.42, envMapIntensity: 0.45 }),
  hubs: phys({ color: 0x8a9a2c, roughness: 0.4, transmission: 0.55, thickness: 2.5, ior: 1.49, attenuationColor: new THREE.Color(0x6d7f1c), attenuationDistance: 6 }),
  flea: phys({ color: 0xc4c4c0, roughness: 0.6, envMapIntensity: 0.5 }),
  thermal_pad: phys({ color: 0x8c8e94, roughness: 0.92 }),
  pcb: phys({ color: 0x9ba1a8, metalness: 0.7, roughness: 0.52, envMapIntensity: 0.6 }),   // aluminium-core board: bare aluminium faces the vial
  pd_board: phys({ color: 0x0b0d10, roughness: 0.5, clearcoat: 0.6, clearcoatRoughness: 0.4 }),
  temp_module: phys({ color: 0x0b0d10, roughness: 0.5, clearcoat: 0.6, clearcoatRoughness: 0.4 }),
  temp_module_parts: phys({ color: 0xe4dccb, roughness: 0.6 }),
  temp_fov: new THREE.MeshBasicMaterial({ color: 0xff8a1e, transparent: true, opacity: 0.32, depthWrite: false, side: THREE.DoubleSide }),
  temp_probe: phys({ color: 0x2a2c30, metalness: 0.4, roughness: 0.25, clearcoat: 1 }),
  pcb_copper: phys({ color: 0xe6c27a, metalness: 1, roughness: 0.32, envMapIntensity: 0.6 }),
  pcb_parts: phys({ color: 0xd9ccb0, roughness: 0.6 }),
  led: phys({ color: 0xe6f0ff, roughness: 0.04, transmission: 1, thickness: 3, ior: 1.54, attenuationColor: new THREE.Color(0x8fb4ff), attenuationDistance: 4, clearcoat: 1 }),
  led_die: ledDieMat,
  pd: phys({ color: 0x0c0c0e, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.05 }),
  pd_die: pdDieMat,
  beam: beamMat,
};
const NO_SHADOW_CAST = new Set(['glass', 'beam', 'temp_fov', 'led', 'septum']);

// ---------------------------------------------------------------- decode
const loader = new STLLoader();
async function decode(name, b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  const buf = await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
  let g = loader.parse(buf);
  g.deleteAttribute('normal');
  g = mergeVertices(g, 1e-4);
  g = toCreasedNormals(g, THREE.MathUtils.degToRad(35));
  g = dropDegenerate(g);
  g.computeBoundingBox(); g.computeBoundingSphere();
  return g;
}
// OpenSCAD exports zero-area slivers (cap: 132, needles: 128). toCreasedNormals gives their
// vertices NaN normals; at some turntable angles a sliver covers a pixel, that pixel shades to
// NaN and UnrealBloomPass's blur smears it into a big black block: a whole-frame black flash.
// Drop the slivers (they have no area to show) and repair any normal that is still not finite.
function dropDegenerate(g) {
  const p = g.attributes.position.array, n = g.attributes.normal.array;   // non-indexed after toCreasedNormals
  const keepP = [], keepN = [];
  for (let t = 0; t < p.length; t += 9) {
    const ax = p[t + 3] - p[t], ay = p[t + 4] - p[t + 1], az = p[t + 5] - p[t + 2];
    const bx = p[t + 6] - p[t], by = p[t + 7] - p[t + 1], bz = p[t + 8] - p[t + 2];
    const cx = ay * bz - az * by, cy = az * bx - ax * bz, cz = ax * by - ay * bx;
    const area2 = Math.hypot(cx, cy, cz);
    if (!(area2 > 1e-9)) continue;
    for (let k = 0; k < 9; k += 3) {
      let x = n[t + k], y = n[t + k + 1], z = n[t + k + 2];
      const l = Math.hypot(x, y, z);
      if (!(l > 1e-6)) { x = cx / area2; y = cy / area2; z = cz / area2; } else { x /= l; y /= l; z /= l; }
      keepN.push(x, y, z);
    }
    for (let k = 0; k < 9; k++) keepP.push(p[t + k]);
  }
  if (keepP.length === p.length) return g;
  const o = new THREE.BufferGeometry();
  o.setAttribute('position', new THREE.Float32BufferAttribute(keepP, 3));
  o.setAttribute('normal', new THREE.Float32BufferAttribute(keepN, 3));
  return o;
}

const root = new THREE.Group();
root.rotation.x = -Math.PI / 2;          // OpenSCAD Z-up -> three.js Y-up
scene.add(root);
const meshes = {};

async function loadAll() {
  const names = Object.keys(PARTS);
  if (!names.length) { fail('No parts embedded', 'This is the unfilled template. Run build-viewer.mjs to embed the STL parts.'); return false; }
  let done = 0;
  const errs = [];
  await Promise.all(names.map(async (n) => {
    try {
      const g = await decode(n, PARTS[n]);
      const m = new THREE.Mesh(g, MATS[n] || phys({ color: 0x9aa3ad, roughness: 0.5 }));
      m.name = n; m.userData.part = n;
      m.castShadow = !NO_SHADOW_CAST.has(n);
      m.receiveShadow = n !== 'beam' && n !== 'glass';
      if (n === 'glass') m.renderOrder = 1;
      if (n === 'beam') m.renderOrder = 2;
      meshes[n] = m; root.add(m);
    } catch (e) { errs.push(n); console.error('part', n, e); }
    done++;
    $('statusS').textContent = `Decoding parts ${done} / ${names.length}`;
    $('bar').style.width = (100 * done / names.length) + '%';
  }));
  if (errs.length === names.length) { fail('Could not decode the model', 'All parts failed to decode: ' + errs.join(', ')); return false; }
  if (errs.length) console.warn('Parts that failed to decode:', errs.join(', '));
  return true;
}

// ---------------------------------------------------------------- framing
const boxOf = (names) => {
  const b = new THREE.Box3();
  for (const n of names) if (meshes[n]) b.expandByObject(meshes[n]);
  return b;
};
let ALL = new THREE.Box3();
let VIEWS = {};

function fitDistance(radius) {
  const vfov = THREE.MathUtils.degToRad(camera.fov);
  const hfov = 2 * Math.atan(Math.tan(vfov / 2) * camera.aspect);
  return radius / Math.sin(Math.min(vfov, hfov) / 2);
}
function viewFrom(box, dir, margin = 1) {
  const c = box.getCenter(new THREE.Vector3());
  const s = box.getBoundingSphere(new THREE.Sphere());
  const d = fitDistance(s.radius * margin);
  return { pos: c.clone().add(dir.clone().normalize().multiplyScalar(d)), target: c };
}
// front of the cap (OpenSCAD +Y, the openings) is three.js -Z after the -90° X rotation
function computeViews() {
  ALL = new THREE.Box3().setFromObject(root);
  const capBox = boxOf(['cap', 'septum', 'screws', 'washers', 'hubs']);
  const opticsBox = boxOf(['beam', 'led', 'led_legs', 'pd', 'pd_board']);
  const baseBox = boxOf(['flea', 'thermal_pad', 'pcb', 'pcb_copper', 'pcb_parts']);
  VIEWS = {
    assembly: () => viewFrom(ALL, new THREE.Vector3(-0.55, 0.42, -1.0), 0.86),   // from the front (+Y, the syringe opening), a little to the right: the anode (-X) on the right
    cap: () => viewFrom(capBox.isEmpty() ? ALL : capBox, new THREE.Vector3(-0.6, 0.62, -1.0), 0.95),   // from the opening side
    optics: () => {
      const b = opticsBox.isEmpty() ? ALL : opticsBox;
      const v = viewFrom(b, new THREE.Vector3(-0.58, 0.0, -1.0), 1.25);   // through the empty LED pockets: no board in the way
      v.pos.y = v.target.y = b.getCenter(new THREE.Vector3()).y;    // at optics height
      return v;
    },
    base: () => viewFrom(baseBox.isEmpty() ? ALL : baseBox, new THREE.Vector3(-0.8, 0.75, -1.0), 1.15),
  };
}

// ---------------------------------------------------------------- lights, floor
const keyLight = new THREE.DirectionalLight(0xfff3e6, 2.2);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
keyLight.shadow.bias = -0.0004;
keyLight.shadow.normalBias = 0.25;
const rimLight = new THREE.DirectionalLight(0x9cc6ff, 0.8);
const fillLight = new THREE.DirectionalLight(0xc8d6ff, 0.75);
const hemi = new THREE.HemisphereLight(0xbfd2ff, 0x1a1f28, 0.25);
scene.add(keyLight, keyLight.target, rimLight, rimLight.target, fillLight, fillLight.target, hemi);

const ledSpill = new THREE.PointLight(0xff2a35, 0, 60, 2);
const pdSpill = new THREE.PointLight(0xff2a35, 0, 40, 2);
scene.add(ledSpill, pdSpill);

function placeLights() {
  const c = ALL.getCenter(new THREE.Vector3());
  const r = ALL.getBoundingSphere(new THREE.Sphere()).radius;
  keyLight.position.copy(c).add(new THREE.Vector3(-0.7, 1.8, -0.9).normalize().multiplyScalar(r * 3));
  keyLight.target.position.copy(c);
  const sc = keyLight.shadow.camera;
  sc.left = sc.bottom = -r * 1.25; sc.right = sc.top = r * 1.25;
  sc.near = r * 0.5; sc.far = r * 6;
  sc.updateProjectionMatrix();
  rimLight.position.copy(c).add(new THREE.Vector3(0.6, 0.7, 1.2).normalize().multiplyScalar(r * 3));
  rimLight.target.position.copy(c);
  fillLight.position.copy(c).add(new THREE.Vector3(1.2, 0.2, -0.6).normalize().multiplyScalar(r * 3));
  fillLight.target.position.copy(c);

  // shadow-catcher just under the PCB (or the lowest part)
  const pcbBox = boxOf(['pcb', 'pcb_copper', 'pcb_parts']);
  const floorY = (pcbBox.isEmpty() ? ALL.min.y : pcbBox.min.y) - 0.1;
  floor = new THREE.Mesh(new THREE.PlaneGeometry(r * 12, r * 12), new THREE.ShadowMaterial({ color: 0x000000, opacity: 0.42 }));
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(c.x, floorY, c.z);
  floor.receiveShadow = true;
  floor.userData.skipPick = true;
  scene.add(floor);

  // beam fade runs LED (+X) -> photodiode; spill lights sit at each end at optics height
  const bb = boxOf(['beam']);
  if (meshes.beam) {
    const gb = meshes.beam.geometry.boundingBox;      // object space = OpenSCAD coords
    BEAM.uniforms.uX0.value = gb.max.x; BEAM.uniforms.uX1.value = gb.min.x;
  }
  const ledBox = boxOf(['led_die']).isEmpty() ? boxOf(['led']) : boxOf(['led_die']);
  if (!ledBox.isEmpty()) ledSpill.position.copy(ledBox.getCenter(new THREE.Vector3())).add(new THREE.Vector3(-3, 0, 0));
  else if (!bb.isEmpty()) ledSpill.position.set(bb.max.x, bb.getCenter(new THREE.Vector3()).y, bb.getCenter(new THREE.Vector3()).z);
  const pdBox = boxOf(['pd_die']).isEmpty() ? boxOf(['pd']) : boxOf(['pd_die']);
  if (!pdBox.isEmpty()) pdSpill.position.copy(pdBox.getCenter(new THREE.Vector3())).add(new THREE.Vector3(2.5, 0, 0));
  else if (!bb.isEmpty()) pdSpill.position.set(bb.min.x, bb.getCenter(new THREE.Vector3()).y, bb.getCenter(new THREE.Vector3()).z);
}

// ---------------------------------------------------------------- UI state
let floor = null;
let whiteOn = false;
function setWhite(on) {               // white page for print/PDF: flat white, normal-blended beam, lighter shadow
  whiteOn = on;
  scene.background = on ? new THREE.Color(0xffffff) : DARK_BG;
  BEAM.uniforms.uWhite.value = on ? 1 : 0;
  beamMat.blending = on ? THREE.NormalBlending : THREE.AdditiveBlending;
  beamMat.needsUpdate = true;
  bloom.threshold = on ? 4.0 : 3.6;
  whitePoint.enabled = on;
  bloom.strength = on ? 0.45 : 0.7;
  renderer.toneMappingExposure = on ? 0.95 : 1.05;
  if (floor) floor.material.opacity = on ? 0.22 : 0.42;
  document.documentElement.classList.toggle('white', on);
  $('whiteBtn')?.setAttribute('aria-pressed', String(on));
}
let beamOn = true;
function setBeam(on) {
  beamOn = on;
  if (meshes.beam) meshes.beam.visible = on;
  ledDieMat.emissiveIntensity = on ? 60 : 0.4;
  pdDieMat.emissiveIntensity = on ? 0.6 : 0;
  ledSpill.intensity = on ? 18 : 0;
  pdSpill.intensity = on ? 6 : 0;
  $('beamBtn').setAttribute('aria-pressed', String(on));
}
function setTurn(on) {
  controls.autoRotate = on;
  $('turnBtn').setAttribute('aria-pressed', String(on));
}
$('beamBtn').addEventListener('click', () => setBeam(!beamOn));
$('liquidBtn').addEventListener('click', () => LIQUID.setVisible(!LIQUID.on));
$('turnBtn').addEventListener('click', () => setTurn(!controls.autoRotate));
$('whiteBtn')?.addEventListener('click', () => setWhite(!whiteOn));
// View pop-up: camera presets and display toggles
{
  const btn = $('viewBtn'), menu = $('viewMenu');
  const setMenu = (open) => { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); };
  btn.addEventListener('click', (e) => { e.stopPropagation(); setMenu(menu.hidden); });
  menu.addEventListener('click', (e) => { e.stopPropagation(); if (e.target.closest('[data-view]')) setMenu(false); });
  document.addEventListener('click', () => setMenu(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { setMenu(false); btn.focus(); } });
}

// camera tween
let tween = null, resumeTurn = false;
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function goView(name, instant = false) {
  if (!VIEWS[name]) return;
  const v = VIEWS[name]();
  document.querySelectorAll('[data-view]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.view === name)));
  if (instant || REDUCED) {
    camera.position.copy(v.pos); controls.target.copy(v.target); controls.update(); tween = null; return;
  }
  if (!tween) resumeTurn = controls.autoRotate;
  controls.autoRotate = false;
  tween = { t0: performance.now(), dur: 1200, p0: camera.position.clone(), q0: controls.target.clone(), p1: v.pos, q1: v.target };
}
document.querySelectorAll('[data-view]').forEach((b) => b.addEventListener('click', () => goView(b.dataset.view)));
controls.addEventListener('start', () => {
  if (tween) { tween = null; controls.autoRotate = resumeTurn; }
});

// ---------------------------------------------------------------- hover / tap tooltip
const tip = $('tip');
const ray = new THREE.Raycaster();
const ndc = new THREE.Vector2();
let tipTimer = 0;
function pick(clientX, clientY) {
  const r = renderer.domElement.getBoundingClientRect();
  ndc.set(((clientX - r.left) / r.width) * 2 - 1, -((clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  const hits = ray.intersectObjects(Object.values(meshes).filter((m) => m.visible), false);
  if (!hits.length) return null;
  const solid = hits.find((h) => h.object.userData.part !== 'glass');
  const h = solid || hits[0];
  // part name, the hit point in root-local (OpenSCAD mm) coordinates, and whether only glass was hit
  return { part: h.object.userData.part, point: root.worldToLocal(h.point.clone()), glassOnly: !solid };
}
// A page embedding the viewer can supply its own wording: window.__viewerTip(hit) -> { title, body } | null
function tipText(hit) {
  if (!hit) return null;
  if (typeof window.__viewerTip === 'function') { try { return window.__viewerTip(hit); } catch (e) { console.error('tip', e); return null; } }
  if (!INFO[hit.part]) return null;
  const [title, ...rest] = INFO[hit.part].split(' · ');
  return { title, body: rest.join(' · ') };
}
function showTip(hit, x, y) {
  const t = tipText(hit);
  if (!t) { tip.classList.remove('show'); return; }
  tip.querySelector('b').textContent = t.title;
  const s = tip.querySelector('span');
  s.textContent = t.body || ''; s.style.display = t.body ? '' : 'none';
  tip.classList.add('show');
  const w = tip.offsetWidth, h = tip.offsetHeight, pad = 12;
  let left = x + 16, top = y + 18;
  if (left + w > innerWidth - pad) left = Math.max(pad, x - w - 16);
  if (top + h > innerHeight - pad) top = Math.max(pad, y - h - 14);
  tip.style.left = left + 'px'; tip.style.top = top + 'px';
}
let pending = null;
renderer.domElement.addEventListener('pointermove', (e) => {
  if (e.pointerType !== 'mouse' || e.buttons) { if (e.buttons) tip.classList.remove('show'); return; }
  if (!pending) requestAnimationFrame(() => { const p = pending; pending = null; showTip(pick(p.x, p.y), p.x, p.y); });
  pending = { x: e.clientX, y: e.clientY };
});
renderer.domElement.addEventListener('pointerleave', () => tip.classList.remove('show'));
let down = null;
renderer.domElement.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY, t: performance.now() }; });
renderer.domElement.addEventListener('pointerup', (e) => {
  if (e.pointerType === 'mouse' || !down) return;
  const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
  if (moved < 8 && performance.now() - down.t < 500) {
    showTip(pick(e.clientX, e.clientY), e.clientX, e.clientY);
    clearTimeout(tipTimer);
    tipTimer = setTimeout(() => tip.classList.remove('show'), 3000);
  }
  down = null;
});

// ---------------------------------------------------------------- resize + loop
function resize() {
  const w = stage.clientWidth || innerWidth, h = stage.clientHeight || innerHeight;
  renderer.setSize(w, h, false);
  composer.setPixelRatio(renderer.getPixelRatio());
  composer.setSize(w, h);
  bloom.setSize(w, h);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
addEventListener('resize', resize);
resize();

const clock = new THREE.Clock();
// magnetic stir flea: spins about the vial axis through its own centre (pivot set up in setupFlea)
const FLEA_REV_S = 1.6;          // rev/s: reads as stirring, far from the 2-fold symmetry's 30 rev/s wagon-wheel point at 60 fps
let fleaPivot = null;
function setupFlea() {
  const m = meshes.flea; if (!m) return;
  const c = m.geometry.boundingBox.getCenter(new THREE.Vector3());   // object space = OpenSCAD mm, Z up
  fleaPivot = new THREE.Group(); fleaPivot.name = 'flea_pivot';
  fleaPivot.position.set(c.x, c.y, 0);
  m.position.set(-c.x, -c.y, 0);
  root.add(fleaPivot); fleaPivot.add(m);    // castShadow/receiveShadow stay on the mesh
  fleaPivot.updateMatrixWorld(true);
}
function frame() {
  const dt = Math.min(clock.getDelta(), 0.1);
  BEAM.uniforms.uTime.value += dt;
  if (fleaPivot && !STILL && !REDUCED) fleaPivot.rotation.z += dt * FLEA_REV_S * Math.PI * 2;
  LIQUID.update(dt);
  if (tween) {
    const k = Math.min(1, (performance.now() - tween.t0) / tween.dur), e = ease(k);
    camera.position.lerpVectors(tween.p0, tween.p1, e);
    controls.target.lerpVectors(tween.q0, tween.q1, e);
    if (k >= 1) { tween = null; controls.autoRotate = resumeTurn; }
  }
  controls.update(dt);
  composer.render(dt);
  for (const f of window.__viewerFrameHooks) { try { f(); } catch (e) { console.error('frame hook', e); } }
}
window.__viewerFrameHooks = window.__viewerFrameHooks || [];   // overlays: called after each render, camera in sync

// ---------------------------------------------------------------- liquid + bubbles BEGIN
// Culture medium + electrolysis gas. Everything lives in `root` (OpenSCAD mm, Z up).
// All materials are custom shaders with "premultiplied" blending: rgb = light the surface sends
// to the eye (env reflection, specular), alpha = how much of what lies behind it is blocked.
// That one rule gives bright rims on the dark studio and grey rims on the white page.
const LIQUID = (() => {
  const TS = 0.5;                    // sim seconds per wall second (keeps the faster bubbles readable)
  const POOL = 2600, CO2_POOL = 16, NRIP = 24;
  let rnd = (() => { let a = 0x9e3779b9; return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();
  const U = (a, b) => a + (b - a) * rnd();
  const group = new THREE.Group();
  let ok = false, on = true, T = 0;
  let R = 12.45, zFloor = -83.3, level = -23, cat, ano, needlesAt = [];
  const small = [], co2 = [], sitesH = [], sitesO = [];
  let ripI = 0, nextCO2 = 0.3;
  let smallMesh, co2Mesh;
  const L = new THREE.Vector3(-0.7, 1.8, -0.9).normalize();
  const RIMD = new THREE.Vector3(0.6, 0.7, 1.2).normalize();
  const common = { uWhite: { value: 0 }, uL: { value: L }, uRim: { value: RIMD } };
  const ripU = { value: Array.from({ length: NRIP }, () => new THREE.Vector4(0, 0, -99, 0)) };
  const timeU = { value: 0 };

  const ENV = /* glsl */`
    uniform float uWhite; uniform vec3 uL, uRim;
    vec3 envC(vec3 R) {
      vec3 ground = mix(vec3(0.012, 0.015, 0.022), vec3(0.42, 0.43, 0.45), uWhite);
      vec3 hor = mix(vec3(0.09, 0.12, 0.17), vec3(0.80, 0.81, 0.83), uWhite);
      vec3 sky = mix(vec3(0.40, 0.46, 0.56), vec3(1.0), uWhite);
      vec3 c = R.y < 0.0 ? mix(hor, ground, smoothstep(0.0, -0.45, R.y)) : mix(hor, sky, smoothstep(0.0, 0.6, R.y));
      c += vec3(1.0, 0.96, 0.9) * pow(max(dot(R, uL), 0.0), 18.0) * 1.1;              // key softbox
      c += vec3(0.6, 0.76, 1.0) * 0.55 * smoothstep(0.90, 0.96, dot(R, uRim));        // rim strip
      return c;
    }`;
  const VERT = /* glsl */`
    varying vec3 vWN, vWP, vTx, vTy, vTz; varying vec2 vP;
    void main() {
      vec4 lp = vec4(position, 1.0); vec3 n = normal;
      #ifdef USE_INSTANCING
        lp = instanceMatrix * lp; n = mat3(instanceMatrix) * n;
      #endif
      vec4 wp = modelMatrix * lp; vWP = wp.xyz; vWN = normalize(mat3(modelMatrix) * n);
      vTx = normalize(mat3(modelMatrix) * vec3(1, 0, 0)); vTy = normalize(mat3(modelMatrix) * vec3(0, 1, 0)); vTz = normalize(mat3(modelMatrix) * vec3(0, 0, 1));
      vP = position.xy;
      gl_Position = projectionMatrix * viewMatrix * wp;
    }`;
  const mat = (frag, extra = {}, side = THREE.FrontSide) => new THREE.ShaderMaterial({
    uniforms: { ...common, ...extra }, vertexShader: VERT, fragmentShader: ENV + frag,
    transparent: true, depthWrite: false, side,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
    blendSrcAlpha: THREE.OneFactor, blendDstAlpha: THREE.OneMinusSrcAlphaFactor,
  });

  // gas bubble in water: total-reflection rim, env reflection, crisp highlight, clear centre
  const bubbleMat = () => mat(/* glsl */`
    varying vec3 vWN, vWP, vTx, vTy, vTz; varying vec2 vP;
    void main() {
      vec3 N = normalize(vWN), V = normalize(cameraPosition - vWP);
      float nv = clamp(dot(N, V), 0.0, 1.0);
      float f = pow(1.0 - nv, 2.0);
      vec3 Rr = reflect(-V, N);
      float spec = pow(max(dot(Rr, uL), 0.0), 140.0) * 1.4 + pow(max(dot(Rr, uRim), 0.0), 50.0) * 0.45;   // kept under the bloom threshold: sub-pixel bubbles were sparkling
      float back = pow(max(dot(N, -uL), 0.0), 3.0) * (1.0 - f) * 0.18;       // light focused through the far side
      float rim = smoothstep(0.35, 0.9, 1.0 - nv);                         // the thin bright/dark ring
      vec3 emit = (envC(Rr) * mix(0.8, 0.38, uWhite) + mix(vec3(0.30, 0.36, 0.44), vec3(0.0), uWhite)) * (f * 0.6 + rim * 0.6)
                + vec3(spec) + vec3(0.9, 0.95, 1.0) * back * mix(1.0, 0.4, uWhite);
      float cov = clamp(0.03 + f * 0.5 + rim * mix(0.45, 0.6, uWhite), 0.0, 0.95);
      gl_FragColor = vec4(emit, cov);
    }`);

  // the flat surface (ripples) and the menisci (geometry normals)
  const surfMat = (ripples) => mat(/* glsl */`
    varying vec3 vWN, vWP, vTx, vTy, vTz; varying vec2 vP;
    uniform vec4 uRip[${NRIP}]; uniform float uTime, uRipOn;
    float H(vec2 p) {
      float h = 0.010 * sin(dot(p, vec2(0.9, 0.4)) + uTime * 4.2) + 0.008 * sin(dot(p, vec2(-0.5, 1.1)) - uTime * 3.4)
              + 0.005 * sin(dot(p, vec2(1.9, -1.4)) + uTime * 6.6);
      for (int i = 0; i < ${NRIP}; i++) {
        vec4 r = uRip[i]; float age = uTime - r.z;
        if (age < 0.0 || age > 2.0 || r.w <= 0.0) continue;
        float d = length(p - r.xy), x = d - age * 40.0;
        h += r.w * exp(-age * 2.2) * sin(x * 2.4) * exp(-x * x * 0.25) / (1.0 + d * 0.3);
      }
      return h;
    }
    void main() {
      vec3 N;
      if (uRipOn > 0.5) {
        float e = 0.06, h0 = H(vP);
        vec3 nl = normalize(vec3(-(H(vP + vec2(e, 0)) - h0) / e, -(H(vP + vec2(0, e)) - h0) / e, 1.0));
        N = normalize(vTx * nl.x + vTy * nl.y + vTz * nl.z);
      } else { N = normalize(vWN); if (N.y < 0.0) N = -N; }
      vec3 V = normalize(cameraPosition - vWP);
      float nv = dot(N, V); bool below = nv < 0.0;
      if (below) { N = -N; nv = -nv; }
      float F = 0.02 + 0.98 * pow(1.0 - nv, 5.0);
      F = min(1.0, F * 1.6 + 0.04);
      if (below && nv < 0.66) F = 0.9;                          // total internal reflection seen from under the surface
      vec3 Rr = reflect(-V, N);
      vec3 emit = envC(Rr) * F + vec3(pow(max(dot(Rr, uL), 0.0), 220.0) * 1.2);
      float cov = clamp(F * 0.9 + 0.04, 0.0, 0.96);
      emit += vec3(0.80, 0.86, 0.66) * 0.04 * mix(0.25, 1.0, uWhite);
      gl_FragColor = vec4(emit, cov);
    }`, { uRip: ripU, uTime: timeU, uRipOn: { value: ripples ? 1 : 0 } }, THREE.DoubleSide);

  // the liquid column seen through the glass: faint warm-green tint, edges darken/brighten like a full vial
  const volMat = (side, k) => mat(/* glsl */`
    varying vec3 vWN, vWP, vTx, vTy, vTz; varying vec2 vP;
    uniform float uK;
    void main() {
      vec3 N = normalize(vWN), V = normalize(cameraPosition - vWP);
      if (dot(N, V) < 0.0) N = -N;
      float nv = clamp(dot(N, V), 0.0, 1.0), f = pow(1.0 - nv, 3.0);
      vec3 Rr = reflect(-V, N);
      float cov = (0.055 + f * 0.55) * uK;
      vec3 tint = vec3(0.80, 0.86, 0.62);
      vec3 emit = envC(Rr) * f * 0.45 * uK + tint * cov * mix(0.22, 0.93, uWhite);
      gl_FragColor = vec4(emit, cov);
    }`, { uK: { value: k } }, side);

  function lathe(r0, w, hgt, decay) {      // meniscus profile hugging a cylinder of radius r0, rising hgt at the contact line
    const pts = [];
    for (let i = 0; i <= 24; i++) {
      const d = w * (1 - i / 24);
      pts.push(new THREE.Vector2(r0 + Math.sign(w) * 0 + d, hgt * Math.exp(-Math.abs(d) / decay)));
    }
    const g = new THREE.LatheGeometry(pts.map((p) => new THREE.Vector2(Math.max(0.01, p.x), p.y)), 72);
    return g;
  }
  let menI = 0;
  function addMeniscus(cx, cy, g, ro) {
    const m = new THREE.Mesh(g, surfMat(false));
    // fixed order after the disc: with equal renderOrder three sorts these by distance, and the
    // order of overlapping premultiplied layers flipped as the camera turned (popping at the rings)
    m.rotation.x = Math.PI / 2; m.position.set(cx, cy, level); m.renderOrder = 5.01 + 0.001 * menI++; group.add(m);
  }

  // ---------------------------------------------------------------- simulation
  const vterm = (r) => Math.min(1500 * r * r + 3, 90);         // mm/s (sim), r in mm
  function addRipple(x, y, amp) {
    const v = ripU.value[ripI]; v.set(x, y, T, amp); ripI = (ripI + 1) % NRIP;
  }
  function site(el, kind) {
    // a point on the submerged surface of electrode `el`: side (weighted) or the bottom face
    const s = { el, kind, th: U(0, Math.PI * 2), z: U(el.z0 + 0.2, level - 0.4), bottom: false, rho: 0, wait: U(0, 1.5), b: null };
    if (rnd() < 0.08 * (kind === 'H' ? 1 : 0.5)) { s.bottom = true; s.rho = Math.sqrt(rnd()) * el.r * (kind === 'O' ? 1 : 0.95); if (kind === 'O') s.rho = U(el.ri + 0.15, el.r - 0.1); s.z = el.z0; }
    return s;
  }
  function attachPos(s, b) {
    if (s.bottom) { b.x = s.el.x + Math.cos(s.th) * s.rho; b.y = s.el.y + Math.sin(s.th) * s.rho; b.z = s.el.z0 - b.r * 0.9; }
    else { const rr = s.el.r + b.r * 0.85; b.x = s.el.x + Math.cos(s.th) * rr; b.y = s.el.y + Math.sin(s.th) * rr; b.z = s.z; }
  }
  function spawnOnSite(s) {
    if (small.length >= POOL) return;
    const H = s.kind === 'H';
    const b = { st: 0, r: 0.012, rd: H ? U(0.05, 0.2) : U(0.1, 0.3), grow: 0, vx: 0, vy: 0, vz: 0, tau: 0.06, life: 0, site: s, x: 0, y: 0, z: 0 };
    b.grow = H ? b.rd / U(0.15, 1.0) : b.rd / U(4, 14);
    s.b = b; attachPos(s, b); small.push(b);
  }
  function detach(b, vz = 0, tau = 0.06) {
    if (b.site) { b.site.b = null; b.site.wait = b.site.kind === 'H' ? U(0.02, 0.5) : U(0.5, 4); b.site = null; }
    b.st = 1; b.vz = vz; b.tau = tau;
  }
  function pop(b) { b.st = 3; b.r0 = b.r; }
  function swirl(b, dt) {                                       // slow stirring vortex + jitter
    const w = 0.5, vx = -b.y * w, vy = b.x * w;
    b.vx += (vx - b.vx) * Math.min(1, dt * 3) + (rnd() - 0.5) * dt * 30 * (0.25 + b.r);
    b.vy += (vy - b.vy) * Math.min(1, dt * 3) + (rnd() - 0.5) * dt * 30 * (0.25 + b.r);
  }
  function keepOut(b) {
    for (const e of [cat, ano]) {
      if (b.z < e.z0 - b.r) continue;
      const dx = b.x - e.x, dy = b.y - e.y, d = Math.hypot(dx, dy), m = e.r + b.r * 0.9;
      if (d < m && d > 1e-6) { b.x = e.x + dx / d * m; b.y = e.y + dy / d * m; }
    }
    const d = Math.hypot(b.x, b.y), m = R - 0.15 - b.r;
    if (d > m) { b.x *= m / d; b.y *= m / d; }
  }
  function step(dt) {
    T += dt;
    // nucleation
    if (gate.H) for (const s of sitesH) if (!s.b && s.z < level - 0.4 && (s.wait -= dt) <= 0) spawnOnSite(s);
    if (gate.O) for (const s of sitesO) if (!s.b && s.z < level - 0.4 && (s.wait -= dt) <= 0) spawnOnSite(s);
    const cs = src || ano;
    // CO2 from the anode bore
    if ((nextCO2 -= dt) <= 0 && gate.CO2 && cs.z0 < level - 2 && co2.length < CO2_POOL) {
      nextCO2 = U(0.5, 1.0);
      const away = Math.atan2(cs.y - cat.y, cs.x - cat.x);
      co2.push({ st: 0, r: 0.3, req: U(1.0, 2.0), x: cs.x, y: cs.y, z: cs.z0, vz: 0, phi: away + U(-1.25, 1.25), spin: U(-0.8, 0.8), ph: U(0, 6.28), fz: U(5, 8), age: 0, ox: 0, oy: 0 });
    }
    for (let i = co2.length - 1; i >= 0; i--) {
      const c = co2[i]; c.age += dt;
      if (c.st === 0) {                                   // bulging out of the bore
        c.r = Math.min(c.req, c.r + c.req * dt / 0.35);
        c.x = cs.x + Math.cos(c.phi) * 0.4; c.y = cs.y + Math.sin(c.phi) * 0.4; c.z = cs.z0 - c.r * 0.6;
        if (c.r >= c.req) { c.st = 1; c.vz = 10; c.age = 0; }
        continue;
      }
      c.vz += (80 + 6 * c.r - c.vz) * Math.min(1, dt / 0.08);
      c.z += c.vz * dt;
      c.phi += c.spin * dt;
      const zig = 0.55 * Math.sin(c.age * c.fz * 6.283 * 0.5 + c.ph);
      const dr = cs.r + c.r * 1.0 + 0.25;
      const tx = cs.x + Math.cos(c.phi) * dr - Math.sin(c.phi) * zig, ty = cs.y + Math.sin(c.phi) * dr + Math.cos(c.phi) * zig;
      const k = Math.min(1, dt * 10);
      const px = c.x, py = c.y;
      c.x += (tx - c.x) * k; c.y += (ty - c.y) * k;
      let d = Math.hypot(c.x, c.y), m = R - 0.25 - c.r;
      if (d > m) { c.x *= m / d; c.y *= m / d; }
      c.vx = (c.x - px) / dt; c.vy = (c.y - py) / dt;
      // knock clinging O2 off the anode; they follow in the wake
      for (const b of small) {
        if (b.st !== 0 || !b.site || b.site.kind !== 'O') continue;
        if (Math.abs(b.z - c.z) > c.r + 1.2) continue;
        if (Math.hypot(b.x - c.x, b.y - c.y, b.z - c.z) < c.r * 1.05 + b.r + 0.6) {
          detach(b, c.vz * 0.75, 0.45); b.vx = c.vx * 0.3; b.vy = c.vy * 0.3;
        }
      }
      if (c.z + c.r * 0.4 >= level) { addRipple(c.x, c.y, 0.07 * c.r); co2.splice(i, 1); }
    }
    // small bubbles
    for (let i = small.length - 1; i >= 0; i--) {
      const b = small[i];
      if (b.st === 0) {
        b.r += b.grow * dt;
        attachPos(b.site, b);
        if (b.r >= b.rd) detach(b, 1);
        continue;
      }
      if (b.st === 1) {
        swirl(b, dt);
        b.vz += (vterm(b.r) - b.vz) * Math.min(1, dt / b.tau);
        b.tau += (0.06 - b.tau) * Math.min(1, dt * 1.5);
        b.x += b.vx * dt * 0.6; b.y += b.vy * dt * 0.6; b.z += b.vz * dt;
        keepOut(b);
        if (b.z + b.r >= level) {
          b.z = level - b.r * 0.25;
          if (rnd() < 0.55) { b.st = 2; b.life = U(0.3, 2.5); }
          else { if (b.r > 0.1 && rnd() < 0.25) addRipple(b.x, b.y, 0.05 * b.r); pop(b); }
        }
        continue;
      }
      if (b.st === 3) {                                   // popping: shrink away over ~0.1 s instead of vanishing in one frame
        b.r -= b.r0 * dt / 0.1;
        if (b.r <= 0.004) small.splice(i, 1);
        continue;
      }
      // floating at the surface: drift with the vortex, then pop
      swirl(b, dt); b.x += b.vx * dt * 0.4; b.y += b.vy * dt * 0.4; keepOut(b);
      if ((b.life -= dt) <= 0) { if (b.r > 0.12 && rnd() < 0.3) addRipple(b.x, b.y, 0.05 * b.r); pop(b); }
    }
  }

  const dummy = new THREE.Object3D();
  function writeInstances() {
    const a = smallMesh.instanceMatrix.array;
    let n = 0;
    for (const b of small) {
      const o = n * 16, s = b.r;
      a[o] = s; a[o + 1] = 0; a[o + 2] = 0; a[o + 3] = 0;
      a[o + 4] = 0; a[o + 5] = s; a[o + 6] = 0; a[o + 7] = 0;
      a[o + 8] = 0; a[o + 9] = 0; a[o + 10] = s; a[o + 11] = 0;
      a[o + 12] = b.x; a[o + 13] = b.y; a[o + 14] = b.z; a[o + 15] = 1;
      n++;
    }
    smallMesh.count = n; smallMesh.instanceMatrix.needsUpdate = true;
    n = 0;
    for (const c of co2) {
      const w = c.st ? Math.sin(c.age * c.fz * 6.283 + c.ph) : 0;
      const flat = c.st ? 0.74 + 0.08 * w : 1.08;           // oblate when rising, a hanging drop shape while it grows
      const sxy = c.r / Math.cbrt(flat);
      dummy.position.set(c.x, c.y, c.z);
      dummy.rotation.set(0.22 * w + (c.vy || 0) * 0.004, -0.18 * Math.cos(c.age * c.fz * 3.1 + c.ph) - (c.vx || 0) * 0.004, c.phi);
      dummy.scale.set(sxy * (1 + 0.05 * w), sxy * (1 - 0.05 * w), sxy * flat);
      dummy.updateMatrix(); co2Mesh.setMatrixAt(n++, dummy.matrix);
    }
    co2Mesh.count = n; co2Mesh.instanceMatrix.needsUpdate = true;
  }

  // ---- presentation: reconfigurable vial (level, electrodes, CO2 source), animated fill, gas gates
  const mens = [];
  let gate = { H: false, O: false, CO2: false }, src = null, col = null, topG = null, haveEl = false;
  function addMen(cx, cy, g) {
    const m = new THREE.Mesh(g, surfMat(false));
    m.rotation.x = Math.PI / 2; m.position.set(cx, cy, 0); m.renderOrder = 5.01 + 0.001 * menI++; topG.add(m);
  }
  function configure(cfg) {   // { level, cat, ano, co2, needles }  electrode = {x,y,r,ri,z0}
    try {
      for (const c of [...group.children]) group.remove(c);
      small.length = 0; co2.length = 0; sitesH.length = 0; sitesO.length = 0; needlesAt = []; menI = 0;
      const gb = meshes.glass.geometry.boundingBox;
      R = (gb.max.x - gb.min.x) / 2 - 1.3; zFloor = gb.min.z + 2.0;
      level = cfg.level; src = cfg.co2 || null;
      haveEl = !!(cfg.cat && cfg.ano);
      cat = cfg.cat || { x: 4.8, y: 0, r: 0, ri: 0, z0: 1e3 }; ano = cfg.ano || { x: -4.8, y: 0, r: 0, ri: 0, z0: 1e3 };
      const cyl = new THREE.CylinderGeometry(R - 0.08, R - 0.08, 1, 128, 1, true);
      cyl.rotateX(Math.PI / 2); cyl.translate(0, 0, 0.5);
      col = new THREE.Group(); col.position.z = zFloor;
      const back = new THREE.Mesh(cyl, volMat(THREE.BackSide, 1)); back.renderOrder = 3;
      const front = new THREE.Mesh(cyl, volMat(THREE.FrontSide, 1)); front.renderOrder = 6;
      col.add(back, front); group.add(col);
      topG = new THREE.Group(); group.add(topG);
      const disc = new THREE.Mesh(new THREE.CircleGeometry(R - 3, 128), surfMat(true));
      disc.renderOrder = 5; topG.add(disc);
      addMen(0, 0, lathe(R - 0.06, -3, 1.4, 0.9));
      mens.length = 0;
      for (const t of cfg.men || []) { addMen(t.x, t.y, lathe(t.r + 0.02, t.el ? 2.2 : 1.5, t.el ? 0.8 : 0.6, t.el ? 0.6 : 0.45)); const m = topG.children[topG.children.length - 1]; m.visible = false; mens.push({ m, ...t }); }
      if (!smallMesh) {
        smallMesh = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 2), bubbleMat(), POOL);
        co2Mesh = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 40, 28), bubbleMat(), CO2_POOL);
        for (const m of [smallMesh, co2Mesh]) { m.frustumCulled = false; m.renderOrder = 4; m.count = 0; }
        co2Mesh.renderOrder = 4.1;
      }
      group.add(smallMesh, co2Mesh);
      if (haveEl) {
        for (let i = 0; i < 520; i++) sitesH.push(site(cat, 'H'));
        for (let i = 0; i < 140; i++) sitesO.push(site(ano, 'O'));
      }
      group.traverse((o) => { o.userData.skipPick = true; o.castShadow = false; o.receiveShadow = false; });
      if (!group.parent) root.add(group);
      setFill(level);
      writeInstances();
      ok = true;
    } catch (e) { console.error('liquid', e); }
  }
  let fillZ = 0;
  function setFill(z) {
    fillZ = z; level = z;
    const h = z - zFloor, vis = h > 0.4;
    col.scale.z = Math.max(0.001, h); col.visible = vis;
    topG.position.z = z; topG.visible = vis;
  }
  function setGate(k, v) {
    if (gate[k] === v) return;
    gate[k] = v;
    if (k === 'O' && v) for (const s of sitesO) { if (s.b || s.z > level - 0.4) continue; spawnOnSite(s); if (s.b) { s.b.r = s.b.rd * U(0.1, 0.95); attachPos(s, s.b); } }
  }
  function init() { }
  function update(dt) {
    if (!ok) return;
    common.uWhite.value = whiteOn ? 1 : 0;
    if (!on || REDUCED || STILL) return;
    const s = Math.min(dt, 0.05) * TS;
    step(s);
    timeU.value = T;
    writeInstances();
  }
  function setVisible(v) {
    on = v; group.visible = v;
    const b = $('liquidBtn'); if (b) b.setAttribute('aria-pressed', String(v));
  }
  return { init, update, setVisible, configure, setFill, setGate, mens, ripple: (x, y, a) => addRipple(x, y, a), setSrc: (c) => { src = c; }, get gate() { return gate; }, get level() { return level; }, get zFloor() { return zFloor; }, get on() { return on; } };
})();
// ---------------------------------------------------------------- liquid + bubbles END

//__PRESENT__
