// Shot 5 — humanity's long walk, a monumental door opens ("毕业"), and the final question.
import * as THREE from 'three';
import { studio, mats, contactShadow, glowSprite, dust, radialTexture, C } from '../lib/stage.js';
import { InkFigure, PROPS, poses, drawFigureCanvas } from '../lib/figure.js';
import { revealHTML, capBox } from '../lib/overlay.js';
import { rng, seg, lerp, easeOutCubic, easeInOutCubic, easeInOutSine, noise1, wordTime } from '../lib/util.js';

export const text = '人类花了几十万年学会活下去毕业剩下的问题，只有一个：你，敢不敢想？当智慧像电一样便宜AI继续发展下去人类会得到什么Coo-Coo出海Ai实验室都在学一件事可能让我们第一次从「活下去」哈勃极深场每一个光点，都是一个星系图片公有领域美国海军眼底照片细胞显微心电数据数据来源';

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
  const lightMat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffffff'), toneMapped: false, fog: false,
    map: radialTexture('rgba(255,255,255,1)', 'rgba(150,120,255,1)', 512) });
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
  const tWhite = G.end - 0.1;
  const tOutro = D.end + 0.9;
  const look = new THREE.Vector3();

  function update(t) {
    // camera: a long, slow push toward the door
    const u = easeInOutSine(seg(t, shotStart, tWhite));
    camera.position.set(lerp(3.0, 0.6, u) + noise1(t * 0.4, 3) * 0.06, lerp(1.6, 1.15, u) + noise1(t * 0.35, 4) * 0.04, lerp(34, 13, u));
    look.set(lerp(-0.5, 0, u), lerp(12.5, 13.5, u), DZ);
    camera.lookAt(look);
    hero.face(camera);

    const open = easeInOutCubic(seg(t, tOpen, tOpen + 1.8));
    hingeL.rotation.y = open * 1.45; hingeR.rotation.y = -open * 1.45;
    const glow = easeOutCubic(seg(t, tOpen - 0.1, tOpen + 1.2));
    const more = seg(t, tOpen + 0.8, tWhite);
    lightMat.color.set('#e4dbff').multiplyScalar(2.2 + glow * 1.6 + more * 1.2);
    carpet.material.opacity = 0.35 * glow;
    doorLight.intensity = 420 * glow;
    halo.material.opacity = 0.35 * glow;
    hero.shadowMat.opacity = 0.55 * glow;
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
    const sIn = easeOutCubic(seg(t, S.start - 0.05, S.start + 0.45));
    const sOut = 1 - seg(t, tOpen - 0.5, tOpen - 0.1);
    o.push({ id: 'ds', x: 72, y: 214, size: 112, weight: 900, color: '#15121b', lh: 1.1, opacity: sOut, shadow: '0 0 30px rgba(246,243,238,.95)',
      html: revealHTML(['几十万年，', '人类都在学一件事：', '<span class="p" style="font-size:1.35em">活下去。</span>'],
        [sIn, easeOutCubic(seg(t, S.start + 0.25, S.start + 0.7)), easeOutCubic(seg(t, wordTime(S, '学会'), wordTime(S, '学会') + 0.45))]) });
    const gIn = easeOutCubic(seg(t, tOpen, tOpen + 0.5));
    const gOut = 1 - seg(t, tWhite - 0.1, tWhite + 0.1);
    o.push({ id: 'dg', x: 540, y: 210, ax: 0.5, size: 320, weight: 900, color: '#15121b', ls: 0.06, opacity: gOut,
      html: revealHTML(['毕业'], [gIn]), shadow: '0 0 50px rgba(246,243,238,.95)' });
    o.push(capBox('dg2', 'AI，可能让我们第一次，从「活下去」这门课<span class="p">毕业</span>。',
      { y: 1170, a: easeOutCubic(seg(t, tOpen + 0.5, tOpen + 0.9)) * gOut, size: 56, rot: -1.2, shadow: '#5B2EFF' }));
    // the Hubble eXtreme Deep Field (NASA, public domain) as the final backdrop
    const hub = seg(t, tWhite + 0.05, tWhite + 0.5) * (1 - seg(t, tOutro - 0.3, tOutro + 0.2));
    const zoom = 1.0 + 0.16 * seg(t, tWhite, tOutro + 0.5);
    o.push({ id: 'hubble', x: 0, y: 0, opacity: hub, z: 2,
      html: `<div style="width:1080px;height:1920px;overflow:hidden;background:#07050d"><img src="/assets/img/hubble_deep_field.png" style="width:1080px;height:1920px;display:block;transform:scale(${zoom.toFixed(4)});transform-origin:55% 45%"></div>` });
    o.push(capBox('htag', '哈勃极深场（NASA）：每一个光点，都是一个星系。', { x: 64, y: 210, w: 800, size: 38, a: easeOutCubic(seg(t, Q.start - 0.1, Q.start + 0.3)) * (1 - seg(t, tOutro - 0.3, tOutro)),
      bg: '#15121b', color: '#F6F3EE', shadow: '#5B2EFF', rot: -1.2 }));
    const qIn = easeOutCubic(seg(t, Q.start + 0.2, Q.start + 0.6)), qOut = 1 - seg(t, D.start - 0.15, D.start + 0.05);
    o.push({ id: 'dq', x: 540, y: 820, ax: 0.5, ay: 0.5, size: 104, weight: 900, color: '#F6F3EE', opacity: qOut, align: 'center', lh: 1.2, shadow: '0 4px 40px rgba(0,0,0,.6)',
      html: revealHTML(['剩下的问题，', '只有一个：'], [qIn, easeOutCubic(seg(t, Q.start + 0.5, Q.start + 0.95))]) });
    const dIn = easeOutCubic(seg(t, D.start, D.start + 0.4));
    const dOut = 1 - seg(t, tOutro - 0.35, tOutro);
    o.push({ id: 'dd', x: 540, y: 860, ax: 0.5, ay: 0.5, size: 196, weight: 900, color: '#F6F3EE', align: 'center', lh: 1.1, opacity: dOut,
      scale: 1 + 0.05 * seg(t, D.start, tOutro), shadow: '0 6px 50px rgba(0,0,0,.65)',
      html: revealHTML(['你，', '<span style="color:#B69CFF;text-shadow:0 0 40px rgba(120,80,255,.9)">敢</span>不敢想？'], [dIn, easeOutCubic(seg(t, D.start + 0.25, D.start + 0.7))]) });
    // end card
    const e0 = seg(t, tOutro - 0.2, tOutro + 0.3);
    o.push({ id: 'e-bg', x: 0, y: 0, opacity: e0, z: 20, html: '<div style="width:1080px;height:1920px;background:#F2EEE7"></div>' });
    const e1 = easeOutCubic(seg(t, tOutro, tOutro + 0.6)), e2 = easeOutCubic(seg(t, tOutro + 0.3, tOutro + 0.9)), e3 = easeOutCubic(seg(t, tOutro + 0.6, tOutro + 1.2));
    o.push({ z: 30, id: 'e-bar', html: '<div style="width:96px;height:12px;background:#5B2EFF"></div>', x: 76, y: 560, opacity: e1 });
    o.push({ z: 30, id: 'e1', x: 72, y: 600, size: 132, weight: 900, color: '#15121b', lh: 1.08, opacity: e1 > 0 ? 1 : 0,
      html: revealHTML(['当<span class="p">智慧</span>', '像电一样便宜'], [e1, e2]) });
    o.push({ z: 30, id: 'e2', x: 76, y: 910, size: 46, weight: 700, color: 'rgba(21,18,27,.7)', opacity: e2, html: 'AI 继续发展下去，人类会得到什么？' });
    o.push({ z: 30, id: 'e3', x: 76, y: 1080, size: 40, weight: 900, color: '#15121b', ls: 0.04, opacity: e3,
      html: '<span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:#5B2EFF;margin-right:14px;vertical-align:middle"></span>Coo-Coo出海Ai实验室' });
    o.push({ z: 30, id: 'e4', x: 76, y: 1560, width: 930, size: 24, weight: 500, color: 'rgba(21,18,27,.55)', lh: 1.55, opacity: e3,
      html: '图片：NASA、SpaceX（公有领域）· Grace Hopper（美国海军，公有领域）· 眼底照片、细胞显微（CC0）· 心电数据 MIT-BIH（ODC-By）<br>数据：AlphaFold DB · Bloom et al. 2020 · Our World in Data · Bloom 1984 · Tim Urban · Dario Amodei' });

    const white = easeOutCubic(seg(t, tWhite, tWhite + 0.35));
    return {
      overlay: o, theme: 'light', noSubs: true, ink: 0.55, tone: 0.22, streak: glow * 0.9,
      speed: t > tOpen ? 0.7 * Math.exp(-(t - tOpen) * 2.2) : 0, speedC: [0.5, 0.45], speedColor: '#15121b',
      bloom: [0.5 - glow * 0.2, 0.3, 2.2],
      fade: ['#F6F3EE', white],
      vignette: 0.42, grain: 0.03, ca: 0.6,
    };
  }
  return { scene, camera, update };
}
