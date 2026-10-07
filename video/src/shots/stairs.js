// Shot 2 — four monumental steps: food, force, information... and intelligence (a glowing cube).
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { studio, mats, contactShadow, glowSprite, dust, C } from '../lib/stage.js';
import { InkFigure, PROPS, poses } from '../lib/figure.js';
import { revealHTML, leaderSVG } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutCubic, easeInOutSine, noise1, wordTime } from '../lib/util.js';

export const text = '人类的四次「批量生产」食物力气信息智慧01020304FOODFORCEINFORMATIONINTELLIGENCE';

export function wheat(mat) {
  const r = rng(11), parts = [], grain = new THREE.SphereGeometry(1, 10, 8);
  for (let i = 0; i < 13; i++) {
    const a = (i / 13) * Math.PI * 2 + r() * 0.4;
    const B = new THREE.Vector3(Math.cos(a) * 0.38, 0, Math.sin(a) * 0.38);
    const M = new THREE.Vector3(Math.cos(a) * 0.07, 1.05, Math.sin(a) * 0.07);
    const top = 2.4 + r() * 0.5, spread = 0.55 + r() * 0.35;
    const Tp = new THREE.Vector3(-Math.cos(a) * spread, top, -Math.sin(a) * spread);
    const curve = new THREE.CatmullRomCurve3([B, M, Tp]);
    parts.push(new THREE.TubeGeometry(curve, 24, 0.028, 6));
    const dir = curve.getTangent(1).normalize();
    const side = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 0, 1)).normalize();
    for (let k = 0; k < 16; k++) {
      const g = grain.clone();
      g.scale(0.07, 0.13, 0.07);
      const along = 0.08 + k * 0.045, off = (k % 2 ? 1 : -1) * 0.05;
      const p = Tp.clone().add(dir.clone().multiplyScalar(along)).add(side.clone().multiplyScalar(off));
      const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().add(side.clone().multiplyScalar(off * 4)).normalize());
      g.applyQuaternion(q); g.translate(p.x, p.y, p.z);
      parts.push(g);
    }
  }
  const band = new THREE.TorusGeometry(0.17, 0.05, 8, 24); band.rotateX(Math.PI / 2); band.translate(0, 1.0, 0);
  parts.push(band);
  return new THREE.Mesh(mergeGeometries(parts), mat);
}

export function gearGeometry(teeth, R, root, hole, depth) {
  const sh = new THREE.Shape();
  const n = teeth * 4;
  for (let i = 0; i <= n; i++) {
    const a = (i / n) * Math.PI * 2, phase = i % 4;
    const rr = phase === 1 || phase === 2 ? R : root;
    const p = [Math.cos(a) * rr, Math.sin(a) * rr];
    i === 0 ? sh.moveTo(...p) : sh.lineTo(...p);
  }
  const h = new THREE.Path(); h.absarc(0, 0, hole, 0, Math.PI * 2, true); sh.holes.push(h);
  for (let k = 0; k < 6; k++) {
    const a = (k / 6) * Math.PI * 2, c = [Math.cos(a) * (root * 0.6), Math.sin(a) * (root * 0.6)];
    const hp = new THREE.Path(); hp.absarc(c[0], c[1], root * 0.16, 0, Math.PI * 2, true); sh.holes.push(hp);
  }
  const g = new THREE.ExtrudeGeometry(sh, { depth, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.04, bevelSegments: 2, curveSegments: 24 });
  g.translate(0, 0, -depth / 2);
  return g;
}

function chipTexture() {
  const cv = document.createElement('canvas'); cv.width = cv.height = 512;
  const g = cv.getContext('2d'), r = rng(5);
  g.fillStyle = '#000'; g.fillRect(0, 0, 512, 512);
  g.strokeStyle = '#b49cff'; g.lineWidth = 3; g.lineCap = 'round';
  for (let i = 0; i < 46; i++) {
    let x = 256 + (r() - 0.5) * 120, y = 256 + (r() - 0.5) * 120;
    g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 4; k++) { if (k % 2) x += (r() - 0.5) * 300; else y += (r() - 0.5) * 300; g.lineTo(x, y); }
    g.stroke();
    g.fillStyle = '#d8ccff'; g.beginPath(); g.arc(x, y, 5, 0, Math.PI * 2); g.fill();
  }
  g.fillStyle = '#e9e1ff'; g.fillRect(196, 196, 120, 120);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function chip() {
  const grp = new THREE.Group();
  const body = new THREE.Mesh(new THREE.BoxGeometry(2.6, 2.6, 0.32), new THREE.MeshPhysicalMaterial({ color: '#1d1046', roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.15 }));
  grp.add(body);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 2.3), new THREE.MeshStandardMaterial({ color: '#000', emissive: '#ffffff', emissiveMap: chipTexture(), emissiveIntensity: 2.2, roughness: 0.4 }));
  face.position.z = 0.165; grp.add(face);
  const pinG = [], pin = new THREE.BoxGeometry(0.1, 0.34, 0.06);
  for (let s = 0; s < 4; s++) for (let i = 0; i < 9; i++) {
    const g = pin.clone(), off = (i - 4) * 0.26;
    if (s < 2) g.translate(off, (s ? 1 : -1) * 1.45, 0); else { g.rotateZ(Math.PI / 2); g.translate((s === 3 ? 1 : -1) * 1.45, off, 0); }
    pinG.push(g);
  }
  grp.add(new THREE.Mesh(mergeGeometries(pinG), new THREE.MeshStandardMaterial({ color: '#cfc8e8', metalness: 0.9, roughness: 0.25 })));
  grp.traverse((o) => { if (o.isMesh) o.castShadow = true; });
  return grp;
}

export function brainCube() {
  const grp = new THREE.Group();
  const core = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.25, 1.25), mats.glow(5));
  const shell = new THREE.Mesh(new THREE.BoxGeometry(2.1, 2.1, 2.1), new THREE.MeshPhysicalMaterial({
    color: C.violet, roughness: 0.12, transparent: true, opacity: 0.38, clearcoat: 1, envMapIntensity: 1.4, emissive: '#3b18d6', emissiveIntensity: 0.25,
  }));
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(2.12, 2.12, 2.12)), new THREE.LineBasicMaterial({ color: '#c7b6ff', toneMapped: false }));
  const ringMat = new THREE.MeshStandardMaterial({ color: '#000', emissive: C.violetHi, emissiveIntensity: 2.5 });
  const r1 = new THREE.Mesh(new THREE.TorusGeometry(2.0, 0.025, 8, 128), ringMat);
  const r2 = new THREE.Mesh(new THREE.TorusGeometry(2.45, 0.02, 8, 128), ringMat);
  const halo = glowSprite('#7b55ff', 9, 0.5);
  grp.add(core, shell, edges, r1, r2, halo);
  grp.userData = { core, shell, r1, r2, halo };
  grp.userData.animate = (t, power = 1) => {
    shell.rotation.set(t * 0.35, t * 0.5, 0); edges.rotation.copy(shell.rotation); core.rotation.set(-t * 0.4, t * 0.3, 0);
    r1.rotation.set(1.2 + t * 0.6, 0.3, t * 0.2); r2.rotation.set(0.4, 1.1 + t * 0.45, -t * 0.3);
    core.material.emissiveIntensity = 4 * power;
    halo.material.opacity = 0.45 * power; halo.scale.setScalar(9 * (0.8 + 0.2 * power));
  };
  return grp;
}

export default function make({ env, T, shotStart }) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1080 / 1920, 0.1, 2000);
  const { key } = studio(scene, env, { fogNear: 70, fogFar: 260, keyPos: [-34, 40, 22], shadowExtent: 34 });
  key.target.position.set(0, 4, -12);

  const H = [3, 6, 9, 12], D = 7, Wd = 7.4;
  const blocks = H.map((h, i) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(Wd, h, D), mats.clay('#F3F0EA'));
    m.position.set(0, h / 2, -i * D);
    m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
    const cs = contactShadow(Wd * 1.5, D * 1.4, 0.35); cs.position.set(0, 0.02, -i * D); scene.add(cs);
    return m;
  });
  const vm = mats.violet();
  const wh = wheat(vm); wh.scale.setScalar(1.15); wh.position.set(-1.6, H[0], 1.4); wh.castShadow = true; scene.add(wh);
  const g1 = new THREE.Mesh(gearGeometry(14, 1.55, 1.27, 0.45, 0.5), vm); g1.position.set(-1.0, H[1] + 1.6, -D + 1.0); g1.castShadow = true; scene.add(g1);
  const g2 = new THREE.Mesh(gearGeometry(9, 1.0, 0.78, 0.3, 0.42), vm); g2.position.set(1.55, H[1] + 1.05, -D + 1.2); g2.castShadow = true; scene.add(g2);
  const ch = chip(); ch.position.set(-0.6, H[2] + 1.55, -2 * D + 1.2); ch.rotation.set(-0.12, 0.35, 0.0); scene.add(ch);
  const cube = brainCube(); cube.position.set(0, H[3] + 2.9, -3 * D); scene.add(cube);
  const cubeLight = new THREE.PointLight('#8a63ff', 0, 40, 1.5); cubeLight.position.copy(cube.position); scene.add(cubeLight);

  const fig = new InkFigure([{ P: PROPS.adult, pose: poses.lookUp() }], { height: 1.75, seed: 21, shadowAngle: 0.75, shadowLen: 0.8 });
  fig.group.position.set(1.7, 0, 5.0);
  scene.add(fig.group);
  const motes = dust({ count: 380, box: [30, 26, 50], center: [0, 12, -10], size: 0.06, color: '#ffffff', opacity: 0.55 });
  scene.add(motes);

  const L = T.stairs, Wl = T.wisdom;
  const wt = [wordTime(L, '食物'), wordTime(L, '力气'), wordTime(L, '信息'), wordTime(Wl, '智慧')];
  const end = T.title.start - 0.28;
  const look = new THREE.Vector3(), v = new THREE.Vector3();
  const corner = (i) => new THREE.Vector3(-Wd / 2, H[i], -i * D + D / 2);

  // camera keyframes: [time, position, target]
  const keys = [
    [shotStart, [15.5, 2.2, 27], [-5.0, 4.6, -8]],
    [wt[2] + 0.3, [14.5, 6.5, 25], [-5.0, 7.6, -10]],
    [wt[3] - 0.7, [11.5, 11.5, 16], [-3.0, 12.6, -17]],
    [end, [5.5, 14.6, 4.0], [-1.0, 15.0, -21]],
  ];
  function camAt(t) {
    let i = 0;
    while (i < keys.length - 2 && t > keys[i + 1][0]) i++;
    const [t0, p0, q0] = keys[i], [t1, p1, q1] = keys[i + 1];
    const u = easeInOutSine(seg(t, t0, t1));
    camera.position.set(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), lerp(p0[2], p1[2], u));
    look.set(lerp(q0[0], q1[0], u), lerp(q0[1], q1[1], u), lerp(q0[2], q1[2], u));
  }

  function update(t) {
    camAt(t);
    camera.position.x += noise1(t * 0.5, 7) * 0.06; camera.position.y += noise1(t * 0.45, 8) * 0.05;
    camera.lookAt(look);
    fig.face(camera);
    g1.rotation.z = t * 0.35; g2.rotation.z = -t * 0.35 * (14 / 9) + 0.12;
    const ignite = easeOutCubic(seg(t, wt[3] - 0.15, wt[3] + 0.5));
    cube.userData.animate(t, 1 + ignite * 2.2);
    cube.position.y = H[3] + 2.9 + Math.sin(t * 1.3) * 0.12;
    cubeLight.intensity = 60 + ignite * 500;
    motes.userData.update(t);

    const o = [];
    const k = easeOutCubic(seg(t, shotStart + 0.25, shotStart + 0.9));
    o.push({ id: 'kick-bar', html: '<div style="width:84px;height:10px;background:#5B2EFF"></div>', x: 76, y: 212, opacity: k, tx: (1 - k) * -30 });
    o.push({ id: 'kick', html: revealHTML(['人类的四次', '「批量生产」'], [k, easeOutCubic(seg(t, shotStart + 0.4, shotStart + 1.05))]), x: 72, y: 246, size: 76, weight: 900, lh: 1.12, color: '#15121b' });
    const names = ['食物', '力气', '信息', '智慧'], en = ['FOOD', 'FORCE', 'INFORMATION', 'INTELLIGENCE'];
    const leaders = [];
    const rowY = [1240, 1040, 840, 600];
    names.forEach((n, i) => {
      v.copy(i === 3 ? cube.position : corner(i)).project(camera);
      const x = (v.x * 0.5 + 0.5) * 1080, y = (-v.y * 0.5 + 0.5) * 1920;
      const a = easeOutCubic(seg(t, wt[i] - 0.1, wt[i] + 0.35));
      const out = 1 - seg(t, wt[3] + 0.6, wt[3] + 1.0) * (i < 3 ? 1 : 0);
      const last = i === 3;
      o.push({ id: 'lab' + i, x: 72, y: rowY[i], ax: 0, ay: 1, opacity: (a > 0 ? 1 : 0) * out,
        html: `<div class="en" style="font-weight:800;font-size:21px;letter-spacing:.22em;color:${last ? '#6A3BFF' : 'rgba(21,18,27,.5)'};margin-bottom:8px">0${i + 1} · ${en[i]}</div>`
          + revealHTML([last ? `<span class="p">${n}</span>` : n], [a]),
        size: last ? 120 : 68, weight: 900, color: '#15121b', lh: 1.05 });
      const lx = 72 + (last ? 270 : 160);
      leaders.push({ x1: lx, y1: rowY[i] - 34, x2: x, y2: y, a: easeOutCubic(seg(t, wt[i] + 0.05, wt[i] + 0.55)) * out,
        color: last ? '#5B2EFF' : 'rgba(21,18,27,.55)', w: last ? 3 : 2 });
    });
    o.push({ ...leaderSVG('leaders', leaders), opacity: 1 });
    const fadeIn = 1 - seg(t, shotStart, shotStart + 0.4);
    const flash = seg(t, end - 0.25, end);
    return {
      overlay: o, theme: 'light',
      bloom: [0.5 + ignite * 0.7, 0.6, 1.9 - ignite * 0.6],
      fade: flash > 0 ? ['#F6F3EE', easeOutCubic(flash)] : ['#F6F3EE', easeOutCubic(fadeIn)],
      vignette: 0.42, grain: 0.03, ca: 0.6,
    };
  }
  return { scene, camera, update };
}
