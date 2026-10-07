// Shot 1 — cold open. A lone figure before a small heap of proteins (50 years of human work);
// at "两亿" a mountain of proteins erupts behind it.
import * as THREE from 'three';
import { studio, mats, glowSprite, lightCone, dust, radialTexture } from '../lib/stage.js';
import { InkFigure, PROPS, poses } from '../lib/figure.js';
import { proteinGeometry } from '../lib/protein.js';
import { revealHTML, capBox, photo } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutCubic, easeOutBack, easeOutExpo, noise1, wordTime } from '../lib/util.js';

export const text = '过去50年·全人类2022·一个AI这不是高潮。这只是预告片。个蛋白质结构实验解析预测一个博士，往往要读完整个学位，才能解出个几乎是科学界已知的全部蛋白质诺贝尔化学奖它的两位主创，因此获奖真实细胞显微镜下';

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
    // dark scrim behind the top type once the bright mountain is up
    o.push({ id: 'scrim', x: 0, y: 0, z: 2, opacity: 0.9 * seg(t, tBoom + 0.3, tBoom + 1.2),
      html: '<div style="width:1080px;height:1100px;background:linear-gradient(180deg,rgba(7,5,13,.92) 0%,rgba(7,5,13,.75) 35%,rgba(7,5,13,0) 100%)"></div>' });
    const H1 = T.hook1, H2 = T.hook2, NB = T.nobel, TR = T.trailer;
    const counterIn = seg(t, 0.7, 1.2), counterOut = 1 - seg(t, NB.start - 0.25, NB.start);
    const val = t < tBoom ? 170000 * easeOutCubic(seg(t, 0.9, 4.0)) : 170000 + (2e8 - 170000) * easeOutExpo(seg(t, tBoom, tBoom + 0.9));
    const big = t >= tBoom;
    const punch = big ? 1 + 0.14 * Math.exp(-(t - tBoom) * 6) : 1;
    o.push({ id: 'lbl', html: big ? '2022 · 一个 AI' : '过去 50 年 · 全人类', x: 540, y: 300, ax: 0.5, size: 46, weight: 900, ls: 0.14,
      color: big ? '#C2AEFF' : 'rgba(244,241,236,0.86)', opacity: counterIn * counterOut });
    o.push({ id: 'num', html: fmt(val), x: 540, y: 362, ax: 0.5, size: big ? 182 : 214, font: "'Anton', sans-serif", weight: 400, ls: 0.01,
      color: big ? '#B49BFF' : '#F6F3EE', opacity: counterIn * counterOut, scale: punch,
      shadow: big ? '0 0 40px rgba(110,70,255,.9), 0 0 90px rgba(110,70,255,.55)' : '0 0 30px rgba(0,0,0,.5)' });
    o.push({ id: 'unit', html: big ? '个蛋白质结构 · 预测' : '个蛋白质结构 · 实验解析', x: 540, y: 620, ax: 0.5, size: 42, weight: 700, ls: 0.1,
      color: 'rgba(244,241,236,0.75)', opacity: counterIn * counterOut * seg(t, 1.2, 1.8) });
    const c1 = easeOutCubic(seg(t, 1.7, 2.2)) * (1 - seg(t, H2.start - 0.15, H2.start + 0.1));
    o.push(capBox('c1', '一个博士，往往要读完<span class="p">整个学位</span>，才能解出 <span class="num">1</span> 个。',
      { x: 64, y: 1210, w: 600, a: c1, size: 50, bg: '#15121b', color: '#F6F3EE', shadow: '#5B2EFF', rot: -1.5 }));
    o.push(photo('p1', '/assets/img/human_mitosis.png', { x: 700, y: 1170, w: 300, h: 300, rot: 4, a: easeOutCubic(seg(t, 2.1, 2.6)) * (1 - seg(t, H2.start - 0.15, H2.start + 0.1)),
      tag: '真实细胞 · 显微镜下', shadow: '#5B2EFF' }));
    const c2 = easeOutCubic(seg(t, tBoom + 0.9, tBoom + 1.4)) * (1 - seg(t, NB.start - 0.15, NB.start + 0.1));
    o.push(capBox('c2', '几乎是科学界<span class="p">已知的全部</span>蛋白质。', { x: 540, y: 1250, ax: 0.5, w: 820, a: c2, size: 56, rot: 1.2, shadow: '#5B2EFF' }));
    const n1 = easeOutCubic(seg(t, NB.start, NB.start + 0.45)), nOut = 1 - seg(t, TR.start - 0.2, TR.start);
    o.push({ id: 'nb1', html: revealHTML(['2024'], [n1]), x: 540, y: 300, ax: 0.5, size: 260, font: "'Anton', sans-serif", weight: 400, color: '#F6F3EE', opacity: nOut,
      shadow: '0 0 50px rgba(110,70,255,.8)' });
    o.push({ id: 'nb2', html: revealHTML(['诺贝尔化学奖'], [easeOutCubic(seg(t, NB.start + 0.2, NB.start + 0.65))]), x: 540, y: 600, ax: 0.5, size: 128, weight: 900,
      color: '#F6F3EE', opacity: nOut, shadow: '0 4px 30px rgba(7,5,13,.9), 0 0 60px rgba(110,70,255,.7)' });
    o.push(capBox('nb3', '它的两位主创，因此获奖。', { x: 540, y: 1250, ax: 0.5, w: 720, a: easeOutCubic(seg(t, NB.start + 0.6, NB.start + 1.0)) * nOut, size: 56, rot: -1.2, shadow: '#5B2EFF' }));
    const h1 = easeOutCubic(seg(t, TR.start - 0.05, TR.start + 0.45));
    const h2 = easeOutCubic(seg(t, wordTime(TR, '这只是') - 0.1, wordTime(TR, '这只是') + 0.4));
    o.push({ id: 'h1', html: revealHTML(['这不是高潮。'], [h1]), x: 540, y: 300, ax: 0.5, size: 84, weight: 900, color: 'rgba(244,241,236,.88)', opacity: h1 > 0 ? 1 : 0 });
    o.push({ id: 'h2', html: revealHTML(['这只是', '<span style="color:#E2D8FF;text-shadow:0 0 30px rgba(140,100,255,.9)">预告片</span>。'], [h2, easeOutCubic(seg(t, wordTime(TR, '这只是') + 0.1, wordTime(TR, '这只是') + 0.55))]),
      x: 540, y: 420, ax: 0.5, size: 176, weight: 900, color: '#F6F3EE', opacity: h2 > 0 ? 1 : 0, align: 'center', lh: 1.08, shadow: '0 6px 40px rgba(0,0,0,.35)' });

    const fadeIn = 1 - seg(t, 0, 0.7);
    const toWhite = seg(t, tEnd - 0.32, tEnd);
    return {
      overlay: o, theme: 'dark',
      bloom: [lerp(0.55, 0.7, boom), 0.6, 0.78],
      fade: toWhite > 0 ? ['#F6F3EE', easeOutCubic(toWhite)] : ['#000', fadeIn],
      vignette: 0.75, grain: 0.04, ca: 0.7,
      bars: 1 - easeOutCubic(seg(t, tBoom - 0.05, tBoom + 0.5)), ink: 0.4, tone: 0.18, streak: 0.4 + 0.9 * boom,
      speed: t > tBoom ? 0.85 * Math.exp(-(t - tBoom) * 2.2) : 0, speedC: [0.5, 0.42], speedColor: '#efe8ff',
    };
  }

  return { scene, camera, update };
}
