// Shot 4 — five walls fall: disease, lifespan, origin, dream, time. Each reveals a vignette.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { studio, mats, contactShadow, glowSprite, lightCone, dust, textPlane, radialTexture, C } from '../lib/stage.js';
import { InkFigure, PROPS, poses } from '../lib/figure.js';
import { revealHTML, capBox, photo } from '../lib/overlay.js';
import { lifeChart, bellCurves, dotsGrid, ecgLine } from '../lib/viz.js';
import { rng, seg, lerp, clamp, easeOutCubic, easeInCubic, easeInOutCubic, easeOutBack, noise1, wordTime } from '../lib/util.js';

export const text = '疾病寿命出身梦想时间年→抱起孙子的那些年全世界最好的老师个人=家公司把时间，还给最爱的人01020304 05DISEASELIFESPANORIGINDREAMTIME医学进步压缩进今天：一款新药要亿美元，会失败AI读眼底照片筛查糖网病获FDA批准岁全球人均寿命下一次翻倍，可能靠多出来的，是还能抱起孙子超过一对一辅导的学生，成绩超过的同龄人。可全世界没有那么多好老师布鲁姆普通课堂现在，大山里的孩子，也能拥有卖了全公司只有个人下一个奇迹，可能只需要敢想的人，先到NASA宇航员SpaceX离家时，你这辈子陪父母的时间，已经用掉了接手重复的工作，把时间还给最爱的人Instagram';

const BEATS = [
  { id: 'disease', word: '疾病', en: 'DISEASE' },
  { id: 'life', word: '寿命', en: 'LIFESPAN' },
  { id: 'origin', word: '出身', en: 'ORIGIN' },
  { id: 'dream', word: '梦想', en: 'DREAM' },
  { id: 'time', word: '时间', en: 'TIME' },
];

// ---------------------------------------------------------------------------- shared pieces
function makeWall(word, idx, en) {
  const pivot = new THREE.Group();
  const wall = new THREE.Mesh(new THREE.BoxGeometry(12, 17, 1.4), mats.clay('#F2EEE7'));
  wall.position.set(0, 8.5, 0.7);
  wall.castShadow = true; wall.receiveShadow = true;
  pivot.add(wall);
  const t = textPlane(word, { font: "900 760px 'Noto Sans SC'", color: C.violet, width: 8.4, height: 14.7, canvasW: 1024, canvasH: 1792, vertical: true, lineGap: 1.0 });
  t.position.set(0, 9.4, 1.42);
  pivot.add(t);
  const lab = textPlane(`0${idx + 1}   ${en}`, { font: "800 104px 'Inter'", color: '#15121b', width: 7.5, height: 0.94, canvasW: 1536, canvasH: 192, align: 'left', ls: 18 });
  lab.position.set(-1.9, 1.05, 1.42);
  pivot.add(lab);
  pivot.userData.labels = [t, lab];
  return pivot;
}

function dustBurst(seed) {
  const r = rng(seed), N = 420, p0 = new Float32Array(N * 3), vel = new Float32Array(N * 3), pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    p0[i * 3] = (r() - 0.5) * 13; p0[i * 3 + 1] = 0.3 + r() * 0.6; p0[i * 3 + 2] = -0.5 - r() * 17.5;
    const side = p0[i * 3] / 6.5;
    vel[i * 3] = side * (2 + r() * 5) + (r() - 0.5) * 2; vel[i * 3 + 1] = 0.6 + r() * 2.6; vel[i * 3 + 2] = (r() - 0.4) * 3.5;
  }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ size: 1.6, color: '#d6cec2', transparent: true, opacity: 0, depthWrite: false, map: radialTexture('rgba(255,255,255,0.85)', 'rgba(255,255,255,0)', 64) });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false;
  pts.userData.update = (tau) => {
    if (tau < 0) { mat.opacity = 0; return; }
    const k = 1 - Math.exp(-tau * 1.6);
    for (let i = 0; i < N; i++) {
      pos[i * 3] = p0[i * 3] + vel[i * 3] * k * 1.4; pos[i * 3 + 1] = p0[i * 3 + 1] + vel[i * 3 + 1] * k; pos[i * 3 + 2] = p0[i * 3 + 2] + vel[i * 3 + 2] * k;
    }
    geo.attributes.position.needsUpdate = true;
    mat.opacity = 0.55 * Math.min(1, tau * 8) * Math.exp(-tau * 0.9);
    mat.size = 1.6 + tau * 1.4;
  };
  return pts;
}

function windowTexture(seed) {
  const cv = document.createElement('canvas'); cv.width = 128; cv.height = 512;
  const g = cv.getContext('2d'), r = rng(seed);
  g.fillStyle = '#000'; g.fillRect(0, 0, 128, 512);
  for (let y = 10; y < 512; y += 18) for (let x = 10; x < 128; x += 22) {
    if (r() < 0.55) { g.fillStyle = `rgba(200,180,255,${0.4 + r() * 0.6})`; g.fillRect(x, y, 12, 8); }
  }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

// ---------------------------------------------------------------------------- vignettes
function dna(scene) {
  const grp = new THREE.Group();
  const N = 110, R = 3.0, step = 0.62;
  const sph = new THREE.InstancedMesh(new THREE.SphereGeometry(0.5, 18, 12), mats.violet(), N * 2);
  const rung = [];
  for (let i = 0; i < N; i++) {
    const a = i * 0.36, y = 0.6 + i * step;
    const p1 = new THREE.Vector3(Math.cos(a) * R, y, Math.sin(a) * R), p2 = new THREE.Vector3(-Math.cos(a) * R, y, -Math.sin(a) * R);
    const m = new THREE.Matrix4();
    sph.setMatrixAt(i * 2, m.makeTranslation(p1.x, p1.y, p1.z));
    sph.setMatrixAt(i * 2 + 1, m.makeTranslation(p2.x, p2.y, p2.z));
    if (i % 2 === 0) {
      const g = new THREE.CylinderGeometry(0.11, 0.11, R * 2, 8); g.rotateZ(Math.PI / 2); g.rotateY(-a); g.translate(0, y, 0);
      rung.push(g);
    }
  }
  sph.castShadow = true;
  const rungs = new THREE.Mesh(mergeGeometries(rung), mats.clay('#EDE8F7'));
  grp.add(sph, rungs);
  return grp;
}

function hourglass() {
  const grp = new THREE.Group();
  const prof = [];
  for (let i = 0; i <= 40; i++) {
    const y = i / 40, b = Math.sin(Math.PI * ((y * 2) % 1)), neck = 0.07;
    prof.push(new THREE.Vector2(neck + 0.33 * Math.pow(b, 0.7), y));
  }
  const glass = new THREE.Mesh(new THREE.LatheGeometry(prof, 64), new THREE.MeshPhysicalMaterial({
    color: '#efeaff', roughness: 0.04, transparent: true, opacity: 0.2, clearcoat: 1, envMapIntensity: 1.1, depthWrite: false,
  }));
  glass.scale.set(9, 15, 9);
  glass.position.y = 0.9;
  const capG = new THREE.CylinderGeometry(3.9, 3.9, 0.9, 64);
  const cap1 = new THREE.Mesh(capG, mats.violet()), cap2 = new THREE.Mesh(capG, mats.violet());
  cap1.position.y = 0.45; cap2.position.y = 16.35;
  const postG = new THREE.CylinderGeometry(0.13, 0.13, 15, 12);
  for (let k = 0; k < 3; k++) {
    const p = new THREE.Mesh(postG, mats.clay('#EDE8F7')); const a = (k / 3) * Math.PI * 2 + 0.5;
    p.position.set(Math.cos(a) * 3.55, 8.4, Math.sin(a) * 3.55); p.castShadow = true; grp.add(p);
  }
  const sandMat = mats.violetMatte();
  const low = new THREE.Mesh(new THREE.ConeGeometry(2.6, 2.4, 48), sandMat); low.position.y = 0.9 + 1.2;
  const up = new THREE.Mesh(new THREE.ConeGeometry(2.6, 2.4, 48, 1, true), sandMat); up.rotation.x = Math.PI;
  const N = 160, sp = new Float32Array(N * 3);
  const sg = new THREE.BufferGeometry(); sg.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  const stream = new THREE.Points(sg, new THREE.PointsMaterial({ size: 0.14, color: '#9d7dff', transparent: true, opacity: 0.95, map: radialTexture('rgba(255,255,255,1)', 'rgba(255,255,255,0)', 32), depthWrite: false }));
  stream.frustumCulled = false;
  cap1.castShadow = cap2.castShadow = true;
  grp.add(cap1, cap2, glass, low, up, stream);
  grp.userData.update = (t, k) => {
    // time runs backwards: the lower mound drains up into the top bulb
    const f = clamp(0.25 + k * 0.6, 0, 1);
    low.scale.set(1 - f * 0.75, 1 - f * 0.8, 1 - f * 0.75);
    low.position.y = 0.9 + 1.2 * (1 - f * 0.8);
    up.scale.set(0.3 + f * 0.7, 0.3 + f * 0.7, 0.3 + f * 0.7);
    up.position.y = 16.0 - 1.2 * (0.3 + f * 0.7);
    for (let i = 0; i < N; i++) {
      const ph = ((i / N) + t * 0.55) % 1;
      sp[i * 3] = Math.sin(i * 12.9) * 0.06; sp[i * 3 + 1] = 3 + ph * 11.5; sp[i * 3 + 2] = Math.cos(i * 7.3) * 0.06;
    }
    sg.attributes.position.needsUpdate = true;
  };
  return grp;
}

function mountains(scene, seed) {
  const r = rng(seed), mat = new THREE.MeshStandardMaterial({ color: '#cdc5ba', roughness: 0.95, flatShading: true });
  const peaks = [[-22, -62, 20], [-36, -84, 30], [-12, -100, 25], [22, -60, 19], [36, -82, 31], [12, -104, 27], [0, -130, 38], [-52, -70, 23], [54, -74, 25]];
  for (const [x, z, h] of peaks) {
    const g = new THREE.ConeGeometry(h * (0.5 + r() * 0.2), h, 6 + Math.floor(r() * 3), 3);
    const pa = g.attributes.position;
    for (let i = 0; i < pa.count; i++) { if (pa.getY(i) < h / 2 - 0.1) { pa.setX(i, pa.getX(i) * (0.85 + r() * 0.3)); pa.setZ(i, pa.getZ(i) * (0.85 + r() * 0.3)); } }
    g.computeVertexNormals();
    const m = new THREE.Mesh(g, mat); m.position.set(x, h / 2 - 0.5, z); m.rotation.y = r() * 3; m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
  }
}

function desk() {
  const grp = new THREE.Group(), m = mats.clay('#F4F1EB');
  const top = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.07, 0.8), m); top.position.y = 0.76; grp.add(top);
  for (const [x, z] of [[-0.68, -0.34], [0.68, -0.34], [-0.68, 0.34], [0.68, 0.34]]) {
    const l = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.76, 0.05), m); l.position.set(x, 0.38, z); grp.add(l);
  }
  const book = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.03, 0.3), mats.violet()); book.position.set(0.25, 0.81, 0.05); book.rotation.y = 0.2; grp.add(book);
  const stool = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.42, 16), m); stool.position.set(-1.05, 0.21, 0); grp.add(stool);
  grp.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return grp;
}

function table() {
  const grp = new THREE.Group(), m = mats.clay('#F4F1EB');
  const top = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.09, 1.3), m); top.position.y = 0.78; grp.add(top);
  for (const [x, z] of [[-1.55, -0.55], [1.55, -0.55], [-1.55, 0.55], [1.55, 0.55]]) {
    const l = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.78, 0.07), m); l.position.set(x, 0.39, z); grp.add(l);
  }
  const vm = mats.violet();
  for (const x of [-1.1, -0.35, 0.4, 1.15]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.12, 0.04, 24), m); p.position.set(x, 0.845, 0.15); grp.add(p); }
  const bowl = new THREE.Mesh(new THREE.SphereGeometry(0.26, 24, 12, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), vm); bowl.rotation.x = Math.PI; bowl.position.set(0, 1.08, -0.1); grp.add(bowl);
  grp.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return grp;
}

function clock() {
  const grp = new THREE.Group();
  const face = new THREE.Mesh(new THREE.CylinderGeometry(7, 7, 0.8, 96), mats.clay('#F4F1EB')); face.rotation.x = Math.PI / 2;
  const rim = new THREE.Mesh(new THREE.TorusGeometry(7.0, 0.42, 16, 128), mats.violet());
  const ticks = [];
  for (let i = 0; i < 12; i++) { const g = new THREE.BoxGeometry(0.28, i % 3 ? 0.9 : 1.6, 0.2); g.translate(0, 5.6 - (i % 3 ? 0 : 0.35), 0.5); g.rotateZ((i / 12) * Math.PI * 2); ticks.push(g); }
  const tk = new THREE.Mesh(mergeGeometries(ticks), mats.violet());
  const hh = new THREE.Mesh(new THREE.BoxGeometry(0.45, 3.6, 0.2).translate(0, 1.5, 0.75), mats.ink());
  const mh = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.2, 0.2).translate(0, 2.3, 0.95), mats.ink());
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.6, 24).rotateX(Math.PI / 2).translate(0, 0, 0.9), mats.violet());
  const solid = new THREE.Group(); solid.add(face, rim, tk, hh, mh, hub);
  solid.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  grp.add(solid);
  // shatter fragments on a polar grid
  const r = rng(31), frags = [];
  for (let ring = 0; ring < 7; ring++) {
    const r0 = ring, r1 = ring + 1, n = 6 + ring * 6;
    for (let k = 0; k < n; k++) {
      const a = ((k + 0.5) / n) * Math.PI * 2, rr = (r0 + r1) / 2;
      frags.push({ p: new THREE.Vector3(Math.cos(a) * rr, Math.sin(a) * rr, 0), w: (2 * Math.PI * rr) / n * 0.96, h: 0.96, a,
        v: new THREE.Vector3(Math.cos(a) * (2 + r() * 5), Math.sin(a) * (2 + r() * 5) + 4 + r() * 6, 3 + r() * 8),
        axis: new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5).normalize(), spin: 2 + r() * 6, violet: r() < 0.5 });
    }
  }
  const fg = new THREE.BoxGeometry(1, 1, 0.25);
  const fW = new THREE.InstancedMesh(fg, mats.clay('#F4F1EB'), frags.length), fV = new THREE.InstancedMesh(fg, mats.violet(), frags.length);
  grp.add(fW, fV);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), q0 = new THREE.Quaternion(), pv = new THREE.Vector3(), sv = new THREE.Vector3();
  grp.userData.update = (t, tShatter) => {
    const tau = t - tShatter;
    solid.visible = tau < 0;
    hh.rotation.z = -t * 0.9; mh.rotation.z = -t * 6.0;
    let nw = 0, nv = 0;
    if (tau >= 0) {
      for (const f of frags) {
        const k = tau * (1 - Math.min(0.5, tau * 0.08));
        pv.copy(f.p).addScaledVector(f.v, k).add(new THREE.Vector3(0, -2.0 * tau * tau * 0.0, 0));
        q0.setFromAxisAngle(new THREE.Vector3(0, 0, 1), f.a - Math.PI / 2);
        q.setFromAxisAngle(f.axis, f.spin * tau).multiply(q0);
        const s = Math.max(0.001, 0.8 - tau * 0.2);
        m4.compose(pv, q, sv.set(f.w * s, f.h * s, s));
        if (f.violet) fV.setMatrixAt(nv++, m4); else fW.setMatrixAt(nw++, m4);
      }
    }
    fW.count = nw; fV.count = nv; fW.instanceMatrix.needsUpdate = fV.instanceMatrix.needsUpdate = true;
  };
  return grp;
}

// ---------------------------------------------------------------------------- shot
export default function make({ env, T, shotStart }) {
  const camera = new THREE.PerspectiveCamera(38, 1080 / 1920, 0.1, 2000);
  const end = T.survive.start - 0.28;
  const beats = BEATS.map((B, i) => {
    const L = T[B.id];
    const cut = i === 0 ? shotStart : L.start - 0.28;
    const fall = B.id === 'dream' ? wordTime(L, '正在倒下') - 0.35 : L.start + 0.2;
    return { ...B, L, cut, fall, impact: fall + 1.05 };
  });
  beats.forEach((b, i) => { b.end = i + 1 < beats.length ? beats[i + 1].cut : end; });

  const sets = beats.map((B, i) => {
    const scene = new THREE.Scene();
    const st = studio(scene, env, { fogNear: 60, fogFar: 230, keyPos: [-26, 42, 34], shadowExtent: 34,
      hemi: B.id === 'origin' ? 0.42 : undefined, key: B.id === 'origin' ? 1.7 : undefined, top: B.id === 'origin' ? '#A79DC4' : undefined });
    st.key.target.position.set(0, 0, -16);
    const wall = makeWall(B.word, i, B.en);
    wall.position.set(0, 0, -0.7);
    scene.add(wall);
    const burst = dustBurst(50 + i); scene.add(burst);
    const fig = new InkFigure([{ P: PROPS.adult, pose: poses.standBack() }], { height: 1.75, seed: 40 + i, shadowAngle: 0.7, shadowLen: 0.9 });
    fig.group.position.set(1.8, 0, 9);
    scene.add(fig.group);
    const set = { scene, wall, burst, figs: [fig], st, upd: [] };
    buildVignette(B.id, set);
    return set;
  });

  function buildVignette(id, set) {
    const { scene } = set;
    if (id === 'disease') {
      const d = dna(); d.position.set(4.5, 0, -30); scene.add(d);
      const g = glowSprite('#8a63ff', 40, 0.25); g.position.set(4.5, 30, -34); scene.add(g);
      const f = new InkFigure([{ P: PROPS.adult, pose: poses.lookUp() }], { height: 1.75, seed: 61, shadowAngle: 0.7 });
      f.group.position.set(1.4, 0, -22); scene.add(f.group); set.figs.push(f);
      scene.add(contactShadow(9, 9, 0.35).translateX(4.5).translateZ(-30));
      set.upd.push((t) => { d.rotation.y = t * 0.45; });
      set.cam = { pos: [-1.5, 1.4, -5], look: [1.6, 11, -30] };
    } else if (id === 'life') {
      const h = hourglass(); h.position.set(2.6, 0, -33); h.scale.setScalar(0.8); scene.add(h);
      scene.add(contactShadow(9, 9, 0.4).translateX(2.6).translateZ(-33));
      const adult = { P: PROPS.adult, pose: poses.lift() };
      // the child is held above the head: put its hips just above the adult's hands
      const f = new InkFigure([adult, { P: PROPS.kid, pose: poses.kidUp([0, PROPS.adult.torso + 1.85]) }], { height: 1.75, seed: 62, shadowAngle: 0.7, shadowLen: 0.75 });
      f.group.position.set(-0.2, 0, -11.0); scene.add(f.group); set.figs.push(f);
      set.upd.push((t, b) => { h.userData.update(t, seg(t, b.impact, b.end)); });
      set.cam = { pos: [0.6, 1.4, 2.0], look: [0.8, 7.4, -33] };
    } else if (id === 'origin') {
      mountains(scene, 9);
      const dk = desk(); dk.position.set(0, 0, -26); dk.rotation.y = -0.35; scene.add(dk);
      const kid = new InkFigure([{ P: PROPS.kid, pose: poses.sitSide(1, { lean: 22, head: 18 }) }], { height: 1.15, seed: 63, shadow: false });
      kid.group.position.set(-0.95, 0.0, -25.7); scene.add(kid.group); set.figs.push(kid);
      const cone = lightCone({ rTop: 0.45, rBottom: 1.35, height: 70, color: '#6a3bff', opacity: 0.55, bottomFade: 0.985 });
      cone.position.set(0, 70, -26); scene.add(cone);
      const pool = new THREE.Mesh(new THREE.CircleGeometry(2.9, 64), new THREE.MeshBasicMaterial({ map: radialTexture('rgba(140,100,255,0.95)', 'rgba(140,100,255,0)'), transparent: true, depthWrite: false, toneMapped: false }));
      pool.rotation.x = -Math.PI / 2; pool.position.set(0, 0.02, -26); scene.add(pool);
      const pl = new THREE.PointLight('#9a7cff', 90, 14, 1.5); pl.position.set(0, 5, -26); scene.add(pl);
      const sparks = dust({ count: 160, box: [3.6, 14, 3.6], center: [0, 7, -26], size: 0.09, color: '#c9b8ff', opacity: 0.9, seed: 4 });
      scene.add(sparks);
      set.upd.push((t, b) => { sparks.userData.update(t * 3); const k = seg(t, b.impact - 0.2, b.impact + 0.8); cone.material.uniforms.opacity.value = 0.55 * k; pool.material.opacity = k; pl.intensity = 90 * k; });
      set.cam = { pos: [3.2, 1.8, -5.5], look: [-0.3, 2.4, -27] };
    } else if (id === 'dream') {
      const r = rng(12), towers = [];
      for (let gx = -6; gx <= 6; gx++) for (let gz = 0; gz < 9; gz++) {
        const x = gx * 5.0 + (r() - 0.5) * 1.6, z = -18 - gz * 7.0 + (r() - 0.5) * 1.6;
        if (z > -30 || (Math.abs(x) < 7 && z > -40)) continue;
        if (r() < 0.45) continue;
        const h = 3 + r() * 8 + gz * 2.2 + (Math.abs(gx) < 3 ? 4 : 0);
        towers.push({ x, z, w: 2.4 + r() * 1.4, d: 2.4 + r() * 1.4, h, delay: Math.hypot(x, z + 22) * 0.035 + r() * 0.25 });
      }
      const tm = mats.violet(); tm.emissive.set('#ffffff'); tm.emissiveMap = windowTexture(3); tm.emissiveIntensity = 1.6;
      const tg = new THREE.BoxGeometry(1, 1, 1); tg.translate(0, 0.5, 0);
      tm.emissiveMap.repeat.set(1, 3);
      const im = new THREE.InstancedMesh(tg, tm, towers.length); im.castShadow = true; im.receiveShadow = true; scene.add(im);
      const f = new InkFigure([{ P: PROPS.adult, pose: poses.armRaised() }], { height: 1.75, seed: 64, shadowAngle: 0.7 });
      f.group.position.set(0.3, 0, -22); scene.add(f.group); set.figs.push(f);
      const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), pv = new THREE.Vector3(), sv = new THREE.Vector3();
      const tRise = wordTime(T.dream, '一个人') - 0.1;
      set.upd.push((t) => {
        towers.forEach((b, i) => {
          const k = easeOutCubic(seg(t, tRise + b.delay, tRise + b.delay + 1.3));
          m4.compose(pv.set(b.x, 0, b.z), q, sv.set(b.w, Math.max(0.001, b.h * k), b.d));
          im.setMatrixAt(i, m4);
        });
        im.instanceMatrix.needsUpdate = true;
      });
      set.cam = { pos: [1.2, 1.1, -9.0], look: [0, 6.5, -40] };
      set.camLate = { at: tRise - 0.2, pos: [2.2, 1.3, -1.0], look: [0, 8.5, -50] };
    } else if (id === 'time') {
      const ck = clock(); ck.position.set(0, 9.2, -34); scene.add(ck);
      const tb = table(); tb.position.set(0, 0, -21); scene.add(tb);
      scene.add(contactShadow(5, 3, 0.35).translateZ(-21));
      const lampY = 2.75;
      const cable = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 20, 6), mats.ink()); cable.position.set(0, lampY + 10, -21.1); scene.add(cable);
      const shade = new THREE.Mesh(new THREE.ConeGeometry(0.42, 0.34, 32, 1, true), new THREE.MeshStandardMaterial({ color: C.violet, side: THREE.DoubleSide, roughness: 0.5 }));
      shade.position.set(0, lampY + 0.12, -21.1); scene.add(shade);
      const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 12), new THREE.MeshStandardMaterial({ color: '#000', emissive: '#fff0dc', emissiveIntensity: 8 })); bulb.position.set(0, lampY, -21.1); scene.add(bulb);
      const lamp = new THREE.PointLight('#ffe9cf', 40, 9, 1.4); lamp.position.set(0, lampY - 0.1, -21.1); scene.add(lamp);
      const hg = glowSprite('#ffe6c8', 3.2, 0.6); hg.position.copy(bulb.position); scene.add(hg);
      const P = PROPS.adult;
      const add = (bodies, x, z, h, seed, mirror = false) => {
        const f = new InkFigure(bodies, { height: h, seed, shadowAngle: 0.7, shadowLen: 0.6, mirror });
        f.group.position.set(x, 0, z); scene.add(f.group); set.figs.push(f); return f;
      };
      add([{ P, pose: poses.sitSide(1, { lean: 6, head: 4 }) }], -2.25, -21.1, 1.75, 71);
      add([{ P, pose: poses.sitSide(1, { lean: 6, head: 4 }) }], 2.25, -21.1, 1.68, 72, true);
      add([{ P: PROPS.kid, pose: poses.sitFront({ reach: true }) }], -0.75, -21.95, 1.18, 73);
      add([{ P, pose: poses.sitFront({ lean: 2 }) }], 0.75, -21.95, 1.66, 74);
      const tShatter = wordTime(T.time, '还给') - 0.15;
      const back = glowSprite('#9b7bff', 60, 0); back.position.set(0, 12, -46); scene.add(back);
      set.upd.push((t) => { ck.userData.update(t, tShatter); back.material.opacity = 0.3 * seg(t, tShatter, tShatter + 1.2); });
      set.cam = { pos: [3.4, 2.4, -7.0], look: [0, 6.5, -30] };
      set.camLate = { at: tShatter - 0.3, pos: [2.6, 1.5, -12.4], look: [0, 0.5, -24] };
    }
  }

  const look = new THREE.Vector3(), tmp = new THREE.Vector3();
  const api = { scene: sets[0].scene, camera, update };

  function update(t) {
    let bi = beats.findIndex((b) => t >= b.cut && t < b.end);
    if (bi < 0) bi = t < beats[0].cut ? 0 : beats.length - 1;
    const b = beats[bi], set = sets[bi];
    api.scene = set.scene;

    // wall fall (accelerating, small settle bounce)
    const fu = seg(t, b.fall, b.impact);
    let ang = -Math.PI / 2 * easeInCubic(fu);
    if (t > b.impact) ang = -Math.PI / 2 + Math.abs(Math.sin((t - b.impact) * 14)) * 0.035 * Math.exp(-(t - b.impact) * 5);
    set.wall.rotation.x = ang;
    // once down, the slab sinks into the floor under the dust so it never blocks the reveal
    set.wall.position.y = -1.7 * easeInOutCubic(seg(t, b.impact + 0.25, b.impact + 1.2));
    const lf = 1 - seg(t, b.impact - 0.15, b.impact + 0.35);
    set.wall.userData.labels.forEach((m) => { m.material.opacity = lf; m.visible = lf > 0.001; });
    set.burst.userData.update(t - b.impact);
    set.upd.forEach((f) => f(t, b));

    // camera: hold on the wall, then glide through to the vignette
    const pre = seg(t, b.cut, b.fall + 0.6);
    const p0 = tmp.set(lerp(3.2, 2.6, pre), lerp(1.3, 1.5, pre), lerp(31, 28, pre));
    const l0 = new THREE.Vector3(0, lerp(8.2, 8.6, pre), 0);
    const mv = easeInOutCubic(seg(t, b.impact - 0.35, b.impact + 2.2));
    let cp = set.cam.pos, cl = set.cam.look;
    camera.position.set(lerp(p0.x, cp[0], mv), lerp(p0.y, cp[1], mv), lerp(p0.z, cp[2], mv));
    look.set(lerp(l0.x, cl[0], mv), lerp(l0.y, cl[1], mv), lerp(l0.z, cl[2], mv));
    if (set.camLate) {
      const k = easeInOutCubic(seg(t, set.camLate.at, set.camLate.at + 2.0));
      camera.position.lerp(tmp.set(...set.camLate.pos), k);
      look.lerp(new THREE.Vector3(...set.camLate.look), k);
    }
    const drift = (t - b.cut) * 0.12;
    camera.position.z -= drift;
    const shake = t > b.impact ? Math.exp(-(t - b.impact) * 4.5) : 0;
    camera.position.x += noise1(t * 11, bi) * 0.28 * shake + noise1(t * 0.5, 9 + bi) * 0.05;
    camera.position.y += noise1(t * 11, bi + 3) * 0.22 * shake + noise1(t * 0.45, 19 + bi) * 0.04;
    camera.lookAt(look);
    set.figs.forEach((f) => f.face(camera));
    // the observer in front of the wall steps out of frame once the camera starts moving through
    set.figs[0].group.visible = t < b.impact + 0.5;

    // overlay: kicker, key figure, then two waves of captions / data / photos
    const o = [];
    const k = easeOutCubic(seg(t, b.cut + 0.05, b.cut + 0.5));
    o.push({ id: 'wk-bar', html: '<div style="width:96px;height:12px;background:#5B2EFF"></div>', x: 76, y: 204, opacity: k });
    o.push({ id: 'wk', x: 72, y: 234, size: 64, weight: 900, color: '#15121b', lh: 1.1, shadow: '0 0 22px rgba(246,243,238,.95)',
      html: revealHTML([`<span class="num" style="color:#5B2EFF">0${bi + 1}</span>&nbsp; ${b.word}`], [k]) });
    const tA = b.impact + 0.15, tB = b.id === 'time' ? wordTime(b.L, '还给') - 0.1 : b.id === 'dream' ? b.impact + 2.7 : b.L.start + 3.9;
    const A = easeOutCubic(seg(t, tA, tA + 0.45)), Aout = 1 - seg(t, tB - 0.3, tB);
    const Bv = easeOutCubic(seg(t, tB, tB + 0.45));
    const big = (id, lines, size = 150) => ({ id, x: 72, y: 336, size, weight: 900, color: '#15121b', lh: 1.04, shadow: '0 0 30px rgba(246,243,238,.95)',
      html: revealHTML(lines, lines.map((_, j) => easeOutCubic(seg(t, tA + j * 0.12, tA + 0.45 + j * 0.12)))), opacity: A > 0 ? 1 : 0 });
    const card = (id, html, a, extra = {}) => capBox(id, html, { y: 1180, a, size: 54, ...extra });
    const panel = (id, inner, a, y = 700, w = 940, rot = -1) => ({ id, x: 540, y, ax: 0.5, opacity: a > 0 ? Math.min(1, a * 1.6) : 0, scale: 0.92 + 0.08 * a, ty: (1 - a) * 40,
      html: `<div class="cap" style="background:#F6F3EE;box-shadow:14px 14px 0 #5B2EFF;transform:rotate(${rot}deg);width:${w}px;box-sizing:border-box;padding:30px 20px 24px">${inner}</div>` });
    if (b.id === 'disease') {
      o.push(big('wp', ['<span class="num">100</span> 年医学进步', '<span style="color:#5B2EFF">→</span> 压缩进 <span class="num p">10</span> 年'], 124));
      o.push(card('c1', '今天：一款新药要 <span class="num">10</span> 年、<span class="num">10</span> 亿美元——<span class="p">90%</span> 会失败。', A * Aout));
      o.push(photo('ph', '/assets/img/retina.png', { x: 72, y: 640, w: 400, h: 400, rot: -3, a: Bv, tag: 'AI 读眼底照片 · 筛查糖网病' }));
      o.push(card('c2', '<span class="num">2018</span> 年，FDA 批准了第一个<span class="p">不需要医生读片</span>的 AI 诊断系统。', Bv, { rot: 1.2 }));
    } else if (b.id === 'life') {
      o.push(big('wp', ['<span class="num">32</span> 岁 <span style="color:#5B2EFF">→</span> <span class="num p">73</span> 岁'], 150));
      o.push(panel('chart', `<div style="font-size:36px;font-weight:900;margin:0 0 10px 22px">全球人均寿命 · 1900 → 2023</div>${lifeChart(seg(t, tA + 0.2, tA + 2.2), 880, 380)}`, A * Aout, 620));
      o.push(card('c2', '下一次翻倍，可能靠 AI。多出来的，是还能<span class="p">抱起孙子</span>的那些年。', Bv, { rot: -1.2, y: 560 }));
      o.push({ id: 'ecg', x: 0, y: 860, opacity: Bv * 0.95, html: ecgLine(t - tB, 1080, 170) });
    } else if (b.id === 'origin') {
      o.push(big('wp', ['超过 <span class="num p">98%</span>'], 170));
      o.push(panel('bell', `<div style="font-size:36px;font-weight:900;margin:0 0 6px 22px">布鲁姆「2σ 问题」· 1984</div>${bellCurves(seg(t, tA + 0.3, tA + 1.8), 880, 330)}`, A * Aout, 640));
      o.push(card('c1', '一对一辅导的学生，成绩超过 <span class="p">98%</span> 的同龄人。可全世界，没有那么多好老师。', A * Aout));
      o.push(card('c2', '现在，<span class="p">大山里的孩子</span>，也能拥有全世界最好的老师。', Bv, { rot: 1.2, y: 1430 }));
    } else if (b.id === 'dream') {
      o.push({ ...big('wp', ['<span class="num p">1</span> 个人', '＝ <span class="num p">1</span> 家公司'], 150), opacity: (A > 0 ? 1 : 0) * (1 - seg(t, tB, tB + 0.3)) });
      o.push(card('c1', '<span class="num">2012</span> 年，Instagram 卖了 <span class="num">10</span> 亿美元——全公司只有 <span class="num p">13</span> 个人。', A * Aout, { y: 740 }));
      o.push(photo('ph1', '/assets/img/rocket.png', { x: 610, y: 640, w: 360, h: 460, rot: 3.5, a: Bv, tag: 'SpaceX · 猎鹰 9 号' }));
      o.push(photo('ph2', '/assets/img/astronaut.png', { x: 100, y: 690, w: 320, h: 380, rot: -4, a: easeOutCubic(seg(t, tB + 0.2, tB + 0.65)), tag: 'NASA 宇航员', shadow: '#15121b' }));
      o.push(card('c2', '下一个奇迹，可能只需要 <span class="num p">1</span> 个敢想的人。', easeOutCubic(seg(t, tB + 0.3, tB + 0.75)), { y: 330, rot: -1.2 }));
    } else if (b.id === 'time') {
      o.push(big('wp', ['<span class="num p" style="font-size:1.7em">93%</span>'], 150));
      o.push(panel('dots', `<div style="display:flex;align-items:center;gap:26px;padding:0 12px">${dotsGrid(seg(t, tA + 0.2, tA + 1.8), 360)}
        <div style="font-size:44px;font-weight:900;line-height:1.3;white-space:normal">一格 = 1%<br><span style="color:#5B2EFF">只剩 7 格</span></div></div>`, A * Aout, 640, 760, 1.2));
      o.push(card('c1', '<span class="num">18</span> 岁离家时，你这辈子陪父母的时间，已经用掉了 <span class="p">93%</span>。', A * Aout));
      o.push(card('c2', 'AI 接手重复的工作，<br>把时间，<span class="p">还给最爱的人</span>。', Bv, { rot: 1.2, y: 1430 }));
    }

    const flash = bi > 0 ? 1 - seg(t, b.cut, b.cut + 0.18) : 1 - seg(t, b.cut, b.cut + 0.3);
    const out = seg(t, end - 0.3, end);
    return {
      overlay: o, theme: 'light', noSubs: true, bloom: [0.6, 0.55, 1.9], ink: 0.6, tone: 0.24, streak: 0.3,
      speed: t > b.impact ? 0.8 * Math.exp(-(t - b.impact) * 3.0) : 0, speedC: [0.5, 0.6], speedColor: '#15121b',
      fade: out > 0 ? ['#F6F3EE', easeOutCubic(out)] : ['#F6F3EE', flash * 0.85],
      vignette: 0.42, grain: 0.03, ca: 0.6,
    };
  }
  return api;
}
