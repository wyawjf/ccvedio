// Shot 5 — humanity's long walk, a monumental door opens ("毕业"), and the final question.
import * as THREE from 'three';
import { studio, mats, contactShadow, glowSprite, dust, radialTexture, C } from '../lib/stage.js';
import { InkFigure, PROPS, poses, drawFigureCanvas } from '../lib/figure.js';
import { revealHTML } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutCubic, easeInOutSine, noise1, wordTime } from '../lib/util.js';

export const text = '人类花了几十万年学会活下去毕业剩下的问题，只有一个：你，敢不敢想？当智慧像电一样便宜AI继续发展下去人类会得到什么Coo-Coo出海Ai实验室';

const WALK_BOX = { minX: -2.5, maxX: 2.5, minY: -4.05, maxY: 4.2 };

export default function make({ env, T, shotStart, DURATION }) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1080 / 1920, 0.1, 2000);
  const { key, hemi } = studio(scene, env, { fogNear: 60, fogFar: 260, keyPos: [-30, 30, 40], shadowExtent: 40, top: '#BDB3D8' });
  key.target.position.set(0, 0, -25);

  // the door
  const DZ = -46;
  const pillarG = new THREE.BoxGeometry(3.4, 30, 3.4);
  const clay = mats.clay('#F2EEE7');
  const pl = new THREE.Mesh(pillarG, clay), pr = new THREE.Mesh(pillarG, clay);
  pl.position.set(-8.7, 15, DZ); pr.position.set(8.7, 15, DZ);
  const lintel = new THREE.Mesh(new THREE.BoxGeometry(20.8, 3.4, 3.4), clay); lintel.position.set(0, 31.7, DZ);
  [pl, pr, lintel].forEach((m) => { m.castShadow = true; m.receiveShadow = true; scene.add(m); });
  const leafG = new THREE.BoxGeometry(6.85, 30, 0.7);
  const leafMat = mats.clay('#EAE5DD');
  const hingeL = new THREE.Group(), hingeR = new THREE.Group();
  hingeL.position.set(-7.0, 0, DZ + 1.2); hingeR.position.set(7.0, 0, DZ + 1.2);
  const leafL = new THREE.Mesh(leafG, leafMat), leafR = new THREE.Mesh(leafG, leafMat);
  leafL.position.set(3.425, 15, 0); leafR.position.set(-3.425, 15, 0);
  leafL.castShadow = leafR.castShadow = true;
  hingeL.add(leafL); hingeR.add(leafR);
  scene.add(hingeL, hingeR);
  const lightMat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffffff'), toneMapped: false, fog: false });
  const portal = new THREE.Mesh(new THREE.PlaneGeometry(14, 30), lightMat); portal.position.set(0, 15, DZ - 0.4); scene.add(portal);
  const carpet = new THREE.Mesh(new THREE.PlaneGeometry(16, 60), new THREE.MeshBasicMaterial({
    map: (() => { const cv = document.createElement('canvas'); cv.width = 64; cv.height = 512; const g = cv.getContext('2d');
      const gr = g.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 512);
      const t = new THREE.CanvasTexture(cv); return t; })(),
    color: new THREE.Color('#b9a2ff'), transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, fog: false,
  }));
  carpet.rotation.x = -Math.PI / 2; carpet.position.set(0, 0.03, DZ + 30); scene.add(carpet);
  const doorLight = new THREE.SpotLight('#efe6ff', 0, 120, 0.55, 0.7, 1.0);
  doorLight.position.set(0, 14, DZ - 2); doorLight.target.position.set(0, 0, 0); scene.add(doorLight, doorLight.target);
  const halo = glowSprite('#a68bff', 70, 0); halo.position.set(0, 16, DZ - 1); scene.add(halo);
  scene.add(contactShadow(28, 8, 0.3).translateZ(DZ));

  // the hero
  const hero = new InkFigure([{ P: PROPS.adult, pose: poses.standBack() }], { height: 1.75, seed: 81, shadowAngle: Math.PI, shadowLen: 1.0, shadowOpacity: 0.0 });
  hero.group.position.set(0.2, 0, -14);
  scene.add(hero.group);

  // the procession: humanity walking across the plain
  const atlas = Array.from({ length: 12 }, (_, i) => {
    const f = drawFigureCanvas([{ P: PROPS.adult, pose: poses.walk(i / 12, 1) }], { box: WALK_BOX, pxPerUnit: 40, seed: 90 + i });
    const t = new THREE.CanvasTexture(f.canvas); t.colorSpace = THREE.SRGBColorSpace; return t;
  });
  const tmpl = new InkFigure([{ P: PROPS.adult, pose: poses.walk(0, 1) }], { box: WALK_BOX, pxPerUnit: 40, seed: 90, shadow: false });
  const r = rng(5), walkers = [];
  for (let i = 0; i < 42; i++) {
    const lane = i % 3;
    const m = new THREE.Mesh(tmpl.mesh.geometry, new THREE.MeshBasicMaterial({ map: atlas[0], transparent: true, alphaTest: 0.03, toneMapped: false, fog: true }));
    const grp = new THREE.Group(); grp.add(m); scene.add(grp);
    const s = 0.9 + r() * 0.18;
    grp.scale.setScalar(s);
    walkers.push({ grp, m, x0: -70 + i * 3.4 + r() * 1.5, z: -24 - lane * 3.2 - r(), v: 1.25 + r() * 0.2, ph: r() });
  }
  const motes = dust({ count: 300, box: [40, 30, 60], center: [0, 12, -25], size: 0.07, color: '#ffffff', opacity: 0.6 });
  scene.add(motes);

  const S = T.survive, G = T.graduate, Q = T.question, D = T.dare;
  const tOpen = wordTime(G, '毕业') - 0.2;
  const tWhite = D.start - 0.25;
  const tOutro = D.end + 0.9;
  const look = new THREE.Vector3();

  function update(t) {
    // camera: a long, slow push toward the door
    const u = easeInOutSine(seg(t, shotStart, tWhite));
    camera.position.set(lerp(3.0, 0.6, u) + noise1(t * 0.4, 3) * 0.06, lerp(1.6, 1.35, u) + noise1(t * 0.35, 4) * 0.04, lerp(34, 0, u));
    look.set(lerp(-0.5, 0, u), lerp(12.5, 13.5, u), DZ);
    camera.lookAt(look);
    hero.face(camera);

    const open = easeInOutCubic(seg(t, tOpen, tOpen + 1.8));
    hingeL.rotation.y = open * 1.45; hingeR.rotation.y = -open * 1.45;
    const glow = easeOutCubic(seg(t, tOpen - 0.1, tOpen + 1.2));
    const more = seg(t, Q.start, tWhite);
    lightMat.color.set('#c9b6ff').multiplyScalar(4 + glow * 8 + more * 6);
    carpet.material.opacity = 0.85 * glow;
    doorLight.intensity = 2600 * glow;
    halo.material.opacity = 0.35 * glow;
    hero.shadowMat.opacity = 0.42 * glow;
    hero.shadow.scale.y = 1 + glow * 3.5;
    hemi.intensity = 0.62 - 0.12 * glow;

    walkers.forEach((w) => {
      const x = w.x0 + w.v * (t - shotStart);
      w.grp.position.set(x, 0, w.z);
      const ph = ((x / 1.55) + w.ph) % 1;
      w.m.material.map = atlas[Math.floor(((ph % 1) + 1) % 1 * 12) % 12];
      w.grp.rotation.y = Math.atan2(camera.position.x - x, camera.position.z - w.z);
      w.m.material.opacity = 1 - 0.85 * glow;
    });
    motes.userData.update(t);

    // overlay
    const o = [];
    const sIn = easeOutCubic(seg(t, S.start - 0.05, S.start + 0.5));
    const sOut = 1 - seg(t, tOpen - 0.5, tOpen - 0.1);
    o.push({ id: 'ds', x: 72, y: 220, size: 112, weight: 900, color: '#15121b', lh: 1.1, opacity: sOut,
      html: revealHTML(['几十万年，', '学会<span class="p">活下去</span>。'], [sIn, easeOutCubic(seg(t, wordTime(S, '学会') - 0.1, wordTime(S, '学会') + 0.4))]) });
    const gIn = easeOutCubic(seg(t, tOpen, tOpen + 0.55));
    const gOut = 1 - seg(t, Q.start - 0.2, Q.start + 0.1);
    o.push({ id: 'dg', x: 540, y: 230, ax: 0.5, size: 300, weight: 900, color: '#15121b', ls: 0.06, opacity: gOut,
      html: revealHTML(['毕业'], [gIn]), shadow: '0 0 50px rgba(246,243,238,.95)' });
    const qIn = easeOutCubic(seg(t, Q.start - 0.05, Q.start + 0.5));
    o.push({ id: 'dq', x: 540, y: 300, ax: 0.5, size: 76, weight: 900, color: '#15121b', opacity: 1 - seg(t, tWhite - 0.1, tWhite + 0.1),
      html: revealHTML(['剩下的问题，', '只有一个：'], [qIn, easeOutCubic(seg(t, Q.start + 0.35, Q.start + 0.85))]), align: 'center', lh: 1.2 });
    const dIn = easeOutCubic(seg(t, D.start - 0.05, D.start + 0.45));
    const dOut = 1 - seg(t, tOutro - 0.35, tOutro);
    o.push({ id: 'dd', x: 540, y: 760, ax: 0.5, ay: 0.5, size: 168, weight: 900, color: '#15121b', align: 'center', lh: 1.12, opacity: dOut,
      scale: 1 + 0.04 * seg(t, D.start, tOutro), html: revealHTML(['你，', '<span class="p">敢</span>不敢想？'], [dIn, easeOutCubic(seg(t, D.start + 0.25, D.start + 0.75))]) });
    // end card
    const e1 = easeOutCubic(seg(t, tOutro, tOutro + 0.6)), e2 = easeOutCubic(seg(t, tOutro + 0.3, tOutro + 0.9)), e3 = easeOutCubic(seg(t, tOutro + 0.7, tOutro + 1.3));
    o.push({ id: 'e-bar', html: '<div style="width:84px;height:10px;background:#5B2EFF"></div>', x: 76, y: 640, opacity: e1 });
    o.push({ id: 'e1', x: 72, y: 680, size: 118, weight: 900, color: '#15121b', lh: 1.1, opacity: e1 > 0 ? 1 : 0,
      html: revealHTML(['当<span class="p">智慧</span>', '像电一样便宜'], [e1, e2]) });
    o.push({ id: 'e2', x: 76, y: 970, size: 40, weight: 500, color: 'rgba(21,18,27,.66)', ls: 0.04, opacity: e2, html: 'AI 继续发展下去，人类会得到什么？' });
    o.push({ id: 'e3', x: 76, y: 1700, size: 34, weight: 700, color: '#15121b', ls: 0.06, opacity: e3,
      html: '<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#5B2EFF;margin-right:14px;vertical-align:middle"></span>Coo-Coo出海Ai实验室' });

    const white = easeOutCubic(seg(t, tWhite, tWhite + 0.35));
    return {
      overlay: o, theme: 'light', noSubs: t > Q.start - 0.1,
      bloom: [0.7 + glow * 0.5, 0.65, 1.9 - glow * 0.3],
      fade: ['#F6F3EE', white * (t > tOutro ? lerp(1, 0.86, seg(t, tOutro, tOutro + 1.5)) : 1)],
      vignette: 0.42, grain: 0.03, ca: 0.6,
    };
  }
  return { scene, camera, update };
}
