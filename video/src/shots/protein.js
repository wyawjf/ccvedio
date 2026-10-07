// Shot 1 — cold open. A lone figure before a small heap of proteins (50 years of human work);
// at "两亿" a mountain of proteins erupts behind it.
import * as THREE from 'three';
import { studio, mats, glowSprite, lightCone, dust, radialTexture } from '../lib/stage.js';
import { InkFigure, PROPS, poses } from '../lib/figure.js';
import { proteinGeometry } from '../lib/protein.js';
import { revealHTML } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutCubic, easeOutBack, easeOutExpo, noise1, wordTime } from '../lib/util.js';

export const text = '过去50年·全人类2022·1个AI这不是高潮。这只是预告片。';

const fmt = (n) => Math.round(n).toLocaleString('en-US');

export default function make({ env, T, shotStart }) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(36, 1080 / 1920, 0.1, 2000);
  const { key, hemi } = studio(scene, env, { dark: true, fogNear: 40, fogFar: 170, key: 0.0, keyPos: [12, 40, 30], keyColor: '#e9e2ff', shadows: false, hemi: 0.25 });
  key.target.position.set(0, 10, -40);

  const tBoom = wordTime(T.hook2, '两亿') - 0.05;
  const tEnd = T.stairs.start - 0.28;

  // --- the small heap: 50 years of structural biology ---
  const r = rng(7);
  const variants = Array.from({ length: 6 }, (_, i) => proteinGeometry(rng(100 + i), { segments: 5, detail: 1 }));
  const lowVariants = Array.from({ length: 5 }, (_, i) => proteinGeometry(rng(200 + i), { segments: 3, detail: 0.5 }));
  const heapMat = mats.violet();
  heapMat.emissiveIntensity = 0.35;
  const heapCenter = new THREE.Vector3(-0.2, 0, -4.6);
  const heap = variants.map((g) => {
    const m = new THREE.InstancedMesh(g, heapMat, 20);
    m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
    return m;
  });
  const heapItems = [];
  for (let i = 0; i < 90; i++) {
    const a = r() * Math.PI * 2, rr = Math.sqrt(r()) * 2.1;
    const h = 1.5 * Math.pow(Math.max(0, 1 - rr / 2.3), 1.1);
    const p = new THREE.Vector3(Math.cos(a) * rr, 0.3 + r() * h, Math.sin(a) * rr * 0.75).add(heapCenter);
    heapItems.push({ p, q: new THREE.Quaternion().setFromEuler(new THREE.Euler(r() * 6, r() * 6, r() * 6)), s: 0.42 + r() * 0.2, v: i % 6 });
  }
  heapItems.sort((a, b) => a.p.y - b.p.y);
  heapItems.forEach((it, i) => { it.t = lerp(0.9, 5.2, i / heapItems.length) + r() * 0.25; });

  // --- the mountain: 200,000,000 ---
  const mountMat = mats.violet();
  mountMat.emissive.set('#4a20f0');
  mountMat.emissiveIntensity = 0.16;
  const MC = new THREE.Vector3(0, 0, -52), R = 58, HM = 36;
  const mount = lowVariants.map((g) => { const m = new THREE.InstancedMesh(g, mountMat, 460); m.frustumCulled = false; scene.add(m); return m; });
  const mountItems = [];
  for (let i = 0; i < 2200; i++) {
    const a = r() * Math.PI * 2, rr = R * Math.pow(r(), 0.62);
    const h = HM * Math.pow(Math.max(0, 1 - (rr / R) * (rr / R)), 0.9);
    const y = h * (0.72 + 0.28 * Math.pow(r(), 0.4));
    const p = new THREE.Vector3(Math.cos(a) * rr, y, Math.sin(a) * rr * 0.7).add(MC);
    mountItems.push({
      p, axis: new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5).normalize(), a0: r() * 6, spin: 0.15 + r() * 0.35,
      s: 1.5 + r() * 1.4, v: i % 5, d: 0.05 + (y / HM) * 1.1 + (rr / R) * 0.35 + r() * 0.35,
    });
  }

  // --- figure ---
  const fig = new InkFigure([{ P: PROPS.adult, pose: poses.lookUp() }], { height: 1.75, seed: 3, shadow: false, ink: '#100d16' });
  fig.group.position.set(0.35, 0, 0);
  scene.add(fig.group);
  const blob = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.7), new THREE.MeshBasicMaterial({ map: radialTexture('rgba(0,0,0,0.9)', 'rgba(0,0,0,0)'), transparent: true, depthWrite: false }));
  blob.rotation.x = -Math.PI / 2; blob.position.set(0.35, 0.01, 0.05);
  scene.add(blob);

  // --- light ---
  const spot = new THREE.SpotLight('#d9ccff', 160, 30, 0.3, 0.55, 1.4);
  spot.position.set(0.3, 12, -3.5); spot.target.position.copy(heapCenter);
  spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024);
  scene.add(spot, spot.target);
  const beam = lightCone({ rTop: 0.2, rBottom: 2.3, height: 12, color: '#9d80ff', opacity: 0.2, additive: true });
  beam.position.set(heapCenter.x, 12, heapCenter.z);
  scene.add(beam);
  const heapGlow = glowSprite('#7a55ff', 5, 0.18);
  heapGlow.position.set(heapCenter.x, 0.9, heapCenter.z);
  scene.add(heapGlow);
  const back = new THREE.PointLight('#7d5bff', 0, 160, 1.0);
  back.position.set(0, 30, -70);
  scene.add(back);
  const mountGlow = glowSprite('#5a35ff', 150, 0);
  mountGlow.position.set(0, 26, -80);
  scene.add(mountGlow);

  // shockwave ring
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.96, 1, 128), new THREE.MeshBasicMaterial({ color: '#a58bff', transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2; ring.position.set(0, 0.05, MC.z + 8);
  scene.add(ring);

  const motes = dust({ count: 500, box: [40, 26, 50], center: [0, 10, -15], size: 0.07, color: '#b9a6ff', opacity: 0.5 });
  scene.add(motes);

  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sv = new THREE.Vector3(), pv = new THREE.Vector3();
  const look = new THREE.Vector3();

  function update(t) {
    // heap
    const counts = heap.map(() => 0);
    for (const it of heapItems) {
      const u = seg(t, it.t, it.t + 0.35);
      if (u <= 0) continue;
      const k = easeOutBack(u, 2.2);
      pv.copy(it.p); pv.y += (1 - easeOutCubic(u)) * 0.6;
      sv.setScalar(it.s * Math.max(0.001, k));
      m4.compose(pv, it.q, sv);
      heap[it.v].setMatrixAt(counts[it.v]++, m4);
    }
    heap.forEach((m, i) => { m.count = counts[i]; m.instanceMatrix.needsUpdate = true; });

    // mountain
    const mc = mount.map(() => 0);
    if (t > tBoom) {
      for (const it of mountItems) {
        const u = seg(t, tBoom + it.d, tBoom + it.d + 1.1);
        if (u <= 0) continue;
        pv.copy(it.p); pv.y -= (1 - easeOutExpo(u)) * 14;
        q.setFromAxisAngle(it.axis, it.a0 + t * it.spin);
        sv.setScalar(it.s * easeOutCubic(u));
        m4.compose(pv, q, sv);
        mount[it.v].setMatrixAt(mc[it.v]++, m4);
      }
    }
    mount.forEach((m, i) => { m.count = mc[i]; m.instanceMatrix.needsUpdate = true; });

    const boom = seg(t, tBoom, tBoom + 1.6);
    back.intensity = 900 * easeOutCubic(boom);
    key.intensity = 2.6 * easeOutCubic(boom);
    mountGlow.material.opacity = 0.16 * easeOutCubic(boom);
    hemi.intensity = 0.25 + 0.3 * boom;
    const rw = seg(t, tBoom + 0.05, tBoom + 1.8);
    ring.scale.setScalar(2 + easeOutCubic(rw) * 70);
    ring.material.opacity = 0;
    spot.intensity = 160 * seg(t, 0.2, 1.4) * (1 - 0.92 * boom);
    heapGlow.material.opacity = 0.18 * (1 - boom);
    beam.material.uniforms.opacity.value = 0.2 * seg(t, 0.3, 1.6) * (1 - 0.7 * boom);
    motes.userData.update(t);

    // camera
    const a = easeInOutCubic(seg(t, tBoom - 0.1, tBoom + 3.4));
    const pre = seg(t, 0, tBoom);
    const p0 = new THREE.Vector3(lerp(2.4, 1.5, pre), lerp(0.8, 0.9, pre), lerp(12.5, 10.6, pre));
    const p1 = new THREE.Vector3(lerp(0.4, -1.2, seg(t, tBoom + 3, tEnd)), lerp(2.4, 3.2, seg(t, tBoom + 3, tEnd)), lerp(36, 39, seg(t, tBoom + 3, tEnd)));
    camera.position.lerpVectors(p0, p1, a);
    look.lerpVectors(new THREE.Vector3(0, 1.45, -4), new THREE.Vector3(0, 14, -40), a);
    const shake = Math.exp(-(t - tBoom) * 3) * (t > tBoom ? 1 : 0);
    camera.position.x += noise1(t * 9, 1) * 0.35 * shake + noise1(t * 0.6, 2) * 0.05;
    camera.position.y += noise1(t * 9, 3) * 0.3 * shake + noise1(t * 0.5, 4) * 0.04;
    camera.lookAt(look);
    fig.face(camera);

    // overlay
    const o = [];
    const counterIn = seg(t, 0.7, 1.2), counterOut = 1 - seg(t, T.trailer.start - 0.35, T.trailer.start);
    const val = t < tBoom ? 170000 * easeOutCubic(seg(t, 0.9, 5.4)) : 170000 + (2e8 - 170000) * easeOutExpo(seg(t, tBoom, tBoom + 0.9));
    const big = t >= tBoom;
    const punch = big ? 1 + 0.12 * Math.exp(-(t - tBoom) * 6) : 1;
    o.push({ id: 'lbl', html: big ? '2022 · 一个 AI' : '过去 50 年 · 全人类', x: 540, y: 300, ax: 0.5, size: 40, weight: 700, ls: 0.18,
      color: big ? '#B9A3FF' : 'rgba(240,236,230,0.78)', opacity: counterIn * counterOut });
    o.push({ id: 'num', html: fmt(val), x: 540, y: 360, ax: 0.5, size: big ? 178 : 200, font: "'Anton', sans-serif", weight: 400, ls: 0.01,
      color: big ? '#A88BFF' : '#F4F1EC', opacity: counterIn * counterOut, scale: punch,
      shadow: big ? '0 0 40px rgba(110,70,255,.85), 0 0 90px rgba(110,70,255,.55)' : '0 0 30px rgba(0,0,0,.4)' });
    o.push({ id: 'unit', html: big ? '个蛋白质结构 · 预测' : '个蛋白质结构 · 实验解析', x: 540, y: 600, ax: 0.5, size: 34, weight: 500, ls: 0.12,
      color: 'rgba(240,236,230,0.6)', opacity: counterIn * counterOut * seg(t, 1.2, 1.8) });
    const h1 = easeOutCubic(seg(t, T.trailer.start - 0.05, T.trailer.start + 0.45));
    const h2 = easeOutCubic(seg(t, wordTime(T.trailer, '这只是') - 0.1, wordTime(T.trailer, '这只是') + 0.4));
    o.push({ id: 'h1', html: revealHTML(['这不是高潮。'], [h1]), x: 540, y: 300, ax: 0.5, size: 66, weight: 700, color: 'rgba(244,241,236,.82)', opacity: h1 > 0 ? 1 : 0 });
    o.push({ id: 'h2', html: revealHTML(['这只是<span style="color:#E2D8FF;text-shadow:0 0 30px rgba(140,100,255,.9)">预告片</span>。'], [h2]), x: 540, y: 400, ax: 0.5, size: 132, weight: 900, color: '#F6F3EE', opacity: h2 > 0 ? 1 : 0,
      shadow: '0 6px 40px rgba(0,0,0,.35)' });

    const fadeIn = 1 - seg(t, 0, 0.7);
    const toWhite = seg(t, tEnd - 0.32, tEnd);
    return {
      overlay: o, theme: 'dark',
      bloom: [lerp(0.55, 0.7, boom), 0.6, 0.78],
      fade: toWhite > 0 ? ['#F6F3EE', easeOutCubic(toWhite)] : ['#000', fadeIn],
      vignette: 0.75, grain: 0.04, ca: 0.7,
    };
  }

  return { scene, camera, update };
}
