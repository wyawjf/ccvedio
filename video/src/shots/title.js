// Shot 3 — "当智慧，像电一样便宜": the cube on a vast paper plain, light racing out like a power grid.
import * as THREE from 'three';
import { studio, mats, contactShadow, C } from '../lib/stage.js';
import { brainCube } from './stairs.js';
import { revealHTML, capBox } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutSine, noise1, wordTime } from '../lib/util.js';

export const text = '当智慧，像电一样便宜为什么这一次最大？想让芯片性能继续翻倍，需要的研究员是年代的倍。好点子，正在越来越难找斯坦福等AI一个装在数据中心里的「天才国度」数百万个诺奖级大脑小时不休息速度是人类的Dario Amodei，Anthropic CEO';

function gridPaths(seed) {
  const r = rng(seed), paths = [];
  const dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]];
  const walk = (x, z, d, len, depth, startDist) => {
    const pts = [[x, z]];
    let dist = startDist;
    const dists = [dist];
    for (let k = 0; k < len; k++) {
      const step = 1.5 + Math.floor(r() * 4) * 1.5;
      x += dirs[d][0] * step; z += dirs[d][1] * step; dist += step;
      pts.push([x, z]); dists.push(dist);
      if (depth < 3 && r() < 0.35) walk(x, z, (d + (r() < 0.5 ? 1 : 3)) % 4, Math.floor(len * 0.6), depth + 1, dist);
      if (r() < 0.3) d = (d + (r() < 0.5 ? 1 : 3)) % 4;
    }
    paths.push({ pts, dists });
  };
  for (let i = 0; i < 16; i++) walk(0, 0, i % 4, 9 + Math.floor(r() * 6), 0, 0);
  return paths;
}

function stripGeometry(paths, w = 0.06) {
  const pos = [], dist = [], idx = [];
  let base = 0;
  for (const p of paths) {
    for (let i = 0; i < p.pts.length - 1; i++) {
      const [x0, z0] = p.pts[i], [x1, z1] = p.pts[i + 1];
      const dx = x1 - x0, dz = z1 - z0, L = Math.hypot(dx, dz), nx = (-dz / L) * w, nz = (dx / L) * w;
      const ex = (dx / L) * w, ez = (dz / L) * w; // extend so corners overlap
      pos.push(x0 - ex + nx, 0.03, z0 - ez + nz, x0 - ex - nx, 0.03, z0 - ez - nz, x1 + ex + nx, 0.03, z1 + ez + nz, x1 + ex - nx, 0.03, z1 + ez - nz);
      dist.push(p.dists[i], p.dists[i], p.dists[i + 1], p.dists[i + 1]);
      idx.push(base, base + 2, base + 1, base + 1, base + 2, base + 3);
      base += 4;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('dist', new THREE.Float32BufferAttribute(dist, 1));
  g.setIndex(idx);
  return g;
}

export default function make({ env, T, shotStart }) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.1, 2000);
  const { key } = studio(scene, env, { fogNear: 40, fogFar: 150, keyPos: [-30, 50, 20], shadowExtent: 40 });

  const paths = gridPaths(42);
  const lineMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    uniforms: { uProg: { value: 0 }, uColor: { value: new THREE.Color(C.violetHi) } },
    vertexShader: 'attribute float dist; varying float vD; varying float vZ; void main(){ vD = dist; vec4 mv = modelViewMatrix * vec4(position,1.0); vZ = -mv.z; gl_Position = projectionMatrix * mv; }',
    fragmentShader: `uniform float uProg; uniform vec3 uColor; varying float vD; varying float vZ;
      void main(){ if (vD > uProg) discard;
        float head = exp(-(uProg - vD) * 0.45);
        float fade = 1.0 - smoothstep(45.0, 90.0, vZ);
        vec3 c = uColor * (2.2 + 9.0 * head);
        gl_FragColor = vec4(c, fade); }`,
  });
  scene.add(new THREE.Mesh(stripGeometry(paths), lineMat));

  // towns: small clay blocks at path nodes; their roofs light up when the current arrives
  const r = rng(77), towns = [];
  for (const p of paths) for (let i = 2; i < p.pts.length; i += 2) {
    if (r() < 0.8 || p.dists[i] < 8) continue;
    const n = 1 + Math.floor(r() * 3);
    for (let k = 0; k < n; k++) towns.push({ x: p.pts[i][0] + (r() - 0.5) * 1.6 + 0.7, z: p.pts[i][1] + (r() - 0.5) * 1.6 + 0.7, w: 0.35 + r() * 0.45, h: 0.3 + r() * 1.0, d: p.dists[i] });
  }
  const tb = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), mats.clay('#F2EFE9'), towns.length);
  const roofs = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.05, 1), mats.glow(3.5), towns.length);
  tb.castShadow = tb.receiveShadow = true;
  const m4 = new THREE.Matrix4();
  towns.forEach((b, i) => { m4.compose(new THREE.Vector3(b.x, b.h / 2, b.z), new THREE.Quaternion(), new THREE.Vector3(b.w, b.h, b.w)); tb.setMatrixAt(i, m4); });
  // (towns removed: the bare grid reads cleaner)

  const cube = brainCube();
  cube.position.set(0, 2.2, 0);
  cube.scale.setScalar(1.25);
  scene.add(cube);
  const cl = new THREE.PointLight('#8a63ff', 260, 30, 1.6); cl.position.set(0, 2.2, 0); scene.add(cl);
  const cs = contactShadow(5, 5, 0.4); scene.add(cs);

  const L = T.title, B = T.bottleneck, G = T.genius;
  const tElec = wordTime(L, '像电');
  const end = T.disease.start - 0.28;

  function update(t) {
    const u = easeInOutSine(seg(t, shotStart, end));
    const ang = lerp(-0.5, 0.15, u);
    const rad = lerp(9, 12, u), hgt = lerp(13, 28, u);
    camera.position.set(Math.sin(ang) * rad, hgt, Math.cos(ang) * rad);
    camera.lookAt(0, 0, lerp(-5.0, -9.0, u));
    const lt2 = Math.max(0, t - G.start);
    const prog = lt2 * 9 + Math.pow(Math.max(0, t - tElec + 0.3), 2) * 22;
    lineMat.uniforms.uProg.value = prog;
    const on = easeOutCubic(seg(t, G.start - 0.1, G.start + 0.6));
    cube.userData.animate(t, 0.35 + 0.9 * on);
    cl.intensity = 60 + 200 * on;

    const o = [];
    // card 1: the bottleneck
    const b1 = easeOutCubic(seg(t, B.start - 0.05, B.start + 0.4)), bOut = 1 - seg(t, G.start - 0.25, G.start);
    o.push({ id: 'b1', x: 72, y: 214, size: 70, weight: 900, color: '#15121b', opacity: bOut, html: revealHTML(['为什么这一次最大？'], [b1]), shadow: '0 0 26px rgba(246,243,238,.95)' });
    o.push({ id: 'b2', x: 60, y: 300, size: 360, font: "'Anton', sans-serif", weight: 400, color: '#5B2EFF', opacity: bOut, lh: 1.0,
      html: revealHTML(['18×'], [easeOutCubic(seg(t, B.start + 0.25, B.start + 0.7))]), shadow: '10px 10px 0 #15121b' });
    o.push(capBox('b3', '想让芯片性能继续翻倍，需要的研究员，是 1970 年代的 <span class="num p">18</span> 倍。',
      { y: 1150, a: easeOutCubic(seg(t, B.start + 0.6, B.start + 1.0)) * bOut, size: 56, rot: -1.0 }));
    o.push(capBox('b4', '好点子，正在越来越难找。<span style="font-weight:500;font-size:.62em;opacity:.7">　—— 斯坦福等，2020</span>',
      { y: 1440, x: 140, w: 860, a: easeOutCubic(seg(t, B.start + 1.3, B.start + 1.7)) * bOut, size: 46, rot: 1.4, bg: '#15121b', color: '#F6F3EE', shadow: '#5B2EFF' }));
    // card 2: a country of geniuses
    const g1 = easeOutCubic(seg(t, G.start, G.start + 0.4)), gOut = 1 - seg(t, L.start - 0.25, L.start);
    o.push({ id: 'g1', x: 72, y: 214, size: 92, weight: 900, color: '#15121b', lh: 1.12, opacity: gOut, shadow: '0 0 26px rgba(246,243,238,.95)',
      html: revealHTML(['AI ＝', '一个装在数据中心里的', '<span class="p" style="font-size:1.55em">「天才国度」</span>'],
        [g1, easeOutCubic(seg(t, G.start + 0.12, G.start + 0.5)), easeOutCubic(seg(t, G.start + 0.25, G.start + 0.7))]) });
    o.push(capBox('g2', '数百万个诺奖级大脑 · 24 小时不休息 · 速度是人类的 <span class="num p">10–100</span> 倍',
      { y: 1170, a: easeOutCubic(seg(t, G.start + 0.6, G.start + 1.0)) * gOut, size: 54, rot: 1.0 }));
    o.push({ id: 'g3', x: 1008, y: 1500, ax: 1, size: 32, weight: 700, color: 'rgba(21,18,27,.7)', opacity: easeOutCubic(seg(t, G.start + 0.9, G.start + 1.3)) * gOut,
      html: '—— Dario Amodei，Anthropic CEO', shadow: '0 0 16px rgba(246,243,238,.95)' });
    // card 3: the title
    const a1 = easeOutCubic(seg(t, L.start - 0.05, L.start + 0.4));
    const a2 = easeOutCubic(seg(t, tElec - 0.1, tElec + 0.4));
    const out = 1 - seg(t, end - 0.2, end);
    o.push({ id: 'title', x: 72, y: 230, size: 176, weight: 900, lh: 1.06, color: '#15121b', opacity: out, shadow: '0 0 30px rgba(246,243,238,.9)',
      html: revealHTML(['当<span class="p">智慧</span>，', '像<span class="p">电</span>一样', '便宜。'], [a1, a2, easeOutCubic(seg(t, tElec + 0.15, tElec + 0.6))]) });
    const fadeIn = 1 - seg(t, shotStart, shotStart + 0.35);
    return {
      overlay: o, theme: 'light', noSubs: true, bloom: [0.85, 0.5, 1.6], fade: ['#F6F3EE', easeOutCubic(fadeIn)], vignette: 0.4, grain: 0.03, ca: 0.6,
      ink: 0.55, tone: 0.22, streak: 0.5 * on, speed: t > L.start ? 0.7 * Math.exp(-(t - L.start) * 2.0) : 0, speedC: [0.5, 0.62], speedColor: '#15121b',
    };
  }
  return { scene, camera, update };
}
