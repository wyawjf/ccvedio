import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { Overlay } from './lib/overlay.js';
import { loadData } from './lib/viz.js';
import { seg, clamp } from './lib/util.js';

import protein, { text as tx1 } from './shots/protein.js';
import stairs, { text as tx2 } from './shots/stairs.js';
import title, { text as tx3 } from './shots/title.js';
import walls, { text as tx4 } from './shots/walls.js';
import door, { text as tx5 } from './shots/door.js';

const W = 1080, H = 1920;
const CUT_LEAD = 0.28; // cut slightly before a shot's first line starts

const tl = await (await fetch('/build/timeline.json')).json();
const T = Object.fromEntries(tl.lines.map((l) => [l.id, l]));
const OUTRO = tl.outro ?? 3.4;
const DURATION = tl.duration + OUTRO;

const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.toneMapping = THREE.NeutralToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const pmrem = new THREE.PMREMGenerator(renderer);
const env = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

const target = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const composer = new EffectComposer(renderer, target);
const renderPass = new RenderPass(new THREE.Scene(), new THREE.PerspectiveCamera());
const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.5, 0.55, 0.88);
const output = new OutputPass();
const finish = new ShaderPass({
  uniforms: {
    tDiffuse: { value: null }, uTime: { value: 0 }, uFade: { value: 0 }, uFadeColor: { value: new THREE.Color('#000') },
    uVig: { value: 0.55 }, uCA: { value: 1.0 }, uGrain: { value: 0.035 }, uRes: { value: new THREE.Vector2(W, H) },
    uInk: { value: 0.0 }, uTone: { value: 0.0 }, uSpeed: { value: 0.0 }, uSpeedC: { value: new THREE.Vector2(0.5, 0.5) },
    uSpeedColor: { value: new THREE.Color('#15121b') }, uStreak: { value: 0.0 }, uBars: { value: 0.0 },
  },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uTime, uFade, uVig, uCA, uGrain, uInk, uTone, uSpeed, uStreak, uBars;
    uniform vec3 uFadeColor, uSpeedColor; uniform vec2 uRes, uSpeedC; varying vec2 vUv;
    float hash(vec2 p){ p = fract(p * vec2(443.897, 441.423) + uTime); p += dot(p, p.yx + 19.19); return fract((p.x + p.y) * p.x); }
    float h1(float n){ return fract(sin(n * 91.73) * 43758.5453); }
    float luma(vec3 c){ return dot(c, vec3(0.299, 0.587, 0.114)); }
    float L(vec2 uv){ return luma(texture2D(tDiffuse, uv).rgb); }
    void main(){
      vec2 px = 1.0 / uRes;
      vec2 d = vUv - 0.5;
      vec2 off = d * uCA * 0.0045;
      vec3 c = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);
      // anamorphic streaks from bright sources
      if (uStreak > 0.0) {
        vec3 s = vec3(0.0);
        for (int i = -14; i <= 14; i++) {
          vec3 t = texture2D(tDiffuse, vUv + vec2(float(i) * 7.0 * px.x, 0.0)).rgb;
          s += max(t - 0.8, 0.0) * (1.0 - abs(float(i)) / 15.0);
        }
        c += s * uStreak * vec3(0.62, 0.52, 1.0) * 0.16;
      }
      // comic ink: sobel on luminance
      if (uInk > 0.0) {
        vec2 e = px * 1.4;
        float tl = L(vUv + vec2(-e.x, e.y)), tt = L(vUv + vec2(0.0, e.y)), tr = L(vUv + e);
        float ll = L(vUv - vec2(e.x, 0.0)), rr = L(vUv + vec2(e.x, 0.0));
        float bl = L(vUv - e), bb = L(vUv - vec2(0.0, e.y)), br = L(vUv + vec2(e.x, -e.y));
        float gx = -tl - 2.0 * ll - bl + tr + 2.0 * rr + br, gy = -bl - 2.0 * bb - br + tl + 2.0 * tt + tr;
        float edge = smoothstep(0.2, 0.5, length(vec2(gx, gy)));
        c = mix(c, vec3(0.082, 0.07, 0.105), edge * uInk);
      }
      // halftone screen in the shadows
      if (uTone > 0.0) {
        float lum = luma(c);
        vec2 p = vUv * uRes;
        vec2 q = mat2(0.7071, -0.7071, 0.7071, 0.7071) * p / 7.0;
        vec2 f = fract(q) - 0.5;
        float dark = clamp((0.6 - lum) / 0.6, 0.0, 1.0);
        float dt = 1.0 - smoothstep(-0.04, 0.04, length(f) - 0.62 * sqrt(dark));
        c = mix(c, c * 0.5 + vec3(0.05, 0.03, 0.14), dt * uTone);
      }
      // manga concentration lines
      if (uSpeed > 0.0) {
        vec2 sd = (vUv - uSpeedC) * vec2(1.0, uRes.y / uRes.x);
        float ang = atan(sd.y, sd.x), rad = length(sd);
        float k = (ang + 3.14159) / 6.28318 * 150.0, idx = floor(k), fr = fract(k);
        float fseed = floor(uTime * 37.0);
        float hs = h1(idx + fseed * 13.0), hw = h1(idx * 3.1 + 7.0);
        float wedge = step(abs(fr - 0.5), 0.06 + 0.22 * hw) * step(0.45, hs);
        float ramp = smoothstep(0.32 + 0.3 * hs, 0.95 + 0.2 * hs, rad);
        c = mix(c, uSpeedColor, wedge * ramp * uSpeed);
      }
      float v = smoothstep(1.05, 0.28, length(d * vec2(1.25, 0.95)) * 1.18);
      c *= mix(1.0, v, uVig);
      c += (hash(vUv * uRes) - 0.5) * uGrain;
      c = mix(c, uFadeColor, uFade);
      float bar = 0.115 * uBars;
      if (vUv.y < bar || vUv.y > 1.0 - bar) c = vec3(0.012, 0.01, 0.02);
      gl_FragColor = vec4(c, 1.0);
    }`,
});
composer.addPass(renderPass);
composer.addPass(bloom);
composer.addPass(output);
composer.addPass(finish);

const overlay = new Overlay(document.getElementById('overlay'));

// Make sure every glyph we will use is loaded before anything draws text into a canvas.
const allText = tx1 + tx2 + tx3 + tx4 + tx5
  + '0123456789,.:·→=+%—「」？！ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
await Promise.all(['900', '700', '500'].map((w) => document.fonts.load(`${w} 64px 'Noto Sans SC'`, allText)));
await document.fonts.load("64px 'Anton'", '0123456789,.:→=+%');
await Promise.all(['600', '800'].map((w) => document.fonts.load(`${w} 64px 'Inter'`, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789·/')));
await document.fonts.ready;

// ---- shots ----------------------------------------------------------------------------------
const ctx = { renderer, env, W, H, T, tl, DURATION };
const order = [
  ['protein', protein], ['stairs', stairs], ['title', title], ['walls', walls], ['door', door],
];
const shots = order.map(([id, make], i) => {
  const first = tl.lines.find((l) => l.shot === id);
  const start = i === 0 ? 0 : first.start - CUT_LEAD;
  return { id, start, inst: make({ ...ctx, shotStart: start }) };
});
shots.forEach((s, i) => { s.end = i + 1 < shots.length ? shots[i + 1].start : DURATION; });
ctx.shots = shots;

// ---- subtitles ------------------------------------------------------------------------------
function subtitle(t, theme) {
  const items = [];
  tl.lines.forEach((l, i) => {
    const next = tl.lines[i + 1];
    const end = Math.min(l.end + Math.min(l.pause, 0.6), next ? next.start - 0.04 : 1e9);
    if (t < l.start - 0.12 || t > end) return;
    const a = seg(t, l.start - 0.12, l.start + 0.08) * (1 - seg(t, end - 0.1, end));
    const dark = theme === 'dark';
    items.push({
      id: 'sub', html: l.sub, x: 540, y: 1468, ax: 0.5, ay: 0, size: 44, weight: 700, lh: 1.35, wrap: 'balance',
      color: dark ? '#F4F1EC' : '#15121b', opacity: a, ty: (1 - a) * 8, width: 900, align: 'center', ls: 0.02,
      shadow: dark ? '0 2px 18px rgba(0,0,0,.55)' : '0 0 16px rgba(246,243,238,.95), 0 0 4px rgba(246,243,238,.9)',
    });
  });
  return items;
}

// ---- render entry point -------------------------------------------------------------------------
window.__duration = DURATION;
window.renderAt = async (t) => {
  t = clamp(t, 0, DURATION - 1e-4);
  const shot = shots.find((s) => t >= s.start && t < s.end) || shots[shots.length - 1];
  const r = shot.inst.update(t, t - shot.start) || {};
  renderPass.scene = shot.inst.scene;
  renderPass.camera = shot.inst.camera;
  bloom.strength = r.bloom?.[0] ?? 0.45;
  bloom.radius = r.bloom?.[1] ?? 0.55;
  bloom.threshold = r.bloom?.[2] ?? 0.88;
  renderer.toneMappingExposure = r.exposure ?? 1.0;
  finish.uniforms.uTime.value = (t * 30) % 97.0 * 0.0137;
  finish.uniforms.uFade.value = r.fade?.[1] ?? 0;
  finish.uniforms.uFadeColor.value.set(r.fade?.[0] ?? '#000');
  finish.uniforms.uVig.value = r.vignette ?? 0.5;
  finish.uniforms.uGrain.value = r.grain ?? 0.03;
  finish.uniforms.uCA.value = r.ca ?? 1.0;
  finish.uniforms.uInk.value = r.ink ?? 0.55;
  finish.uniforms.uTone.value = r.tone ?? 0.28;
  finish.uniforms.uSpeed.value = r.speed ?? 0;
  finish.uniforms.uSpeedC.value.set(...(r.speedC ?? [0.5, 0.5]));
  finish.uniforms.uSpeedColor.value.set(r.speedColor ?? '#15121b');
  finish.uniforms.uStreak.value = r.streak ?? 0;
  finish.uniforms.uBars.value = r.bars ?? 0;
  composer.render();
  const clean = new URLSearchParams(location.search).has('clean');
  overlay.render(clean ? [] : [...(r.overlay || []), ...(r.noSubs || tl.silent ? [] : subtitle(t, r.theme))]);
  await new Promise((res) => requestAnimationFrame(() => res()));
};

await loadData();
// decode every photo up front and keep them alive so overlay <img> tags paint on their first frame
const keep = document.createElement('div');
keep.style.cssText = 'position:absolute;left:-5000px;top:0;width:10px;height:10px;overflow:hidden';
document.body.appendChild(keep);
await Promise.all(['retina', 'rocket', 'astronaut', 'grace_hopper', 'human_mitosis', 'hubble_deep_field'].map((n) => {
  const im = new Image(); im.src = `/assets/img/${n}.png`; keep.appendChild(im); return im.decode();
}));
for (const s of shots) if (s.inst.init) await s.inst.init();
window.__ready = true;
