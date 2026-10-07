// 2.5D ink figures: a parametric 2D skeleton drawn into a canvas in an editorial ink style,
// mounted on a camera-facing plane with a soft projected ground shadow.
import * as THREE from 'three';
import { rng } from './util.js';

const DEG = Math.PI / 180;
export const INK = '#15121b';
const PAPER_LINE = 'rgba(238,234,226,';

const ADULT = {
  headRx: 0.43, headRy: 0.53, neck: 0.3, torso: 2.8, shoulderW: 0.78, hipW: 0.38, neckR: 0.2,
  upperArm: 1.42, foreArm: 1.28, handL: 0.46, thigh: 2.0, shin: 1.9, footL: 0.82,
  armR: [0.2, 0.15, 0.1], legR: [0.36, 0.24, 0.13], chest: 0.55,
};
const KID = {
  headRx: 0.42, headRy: 0.5, neck: 0.22, torso: 1.6, shoulderW: 0.58, hipW: 0.28, neckR: 0.14,
  upperArm: 0.88, foreArm: 0.78, handL: 0.3, thigh: 1.1, shin: 1.0, footL: 0.5,
  armR: [0.15, 0.12, 0.09], legR: [0.21, 0.17, 0.1], chest: 0.38,
};
export const PROPS = { adult: ADULT, kid: KID };

const add = (a, b, k = 1) => [a[0] + b[0] * k, a[1] + b[1] * k];
const D = (a) => [Math.sin(a * DEG), -Math.cos(a * DEG)]; // angle measured from straight down, + toward +x
const Uv = (a) => [Math.sin(a * DEG), Math.cos(a * DEG)]; // angle measured from straight up

export function joints(P, pose) {
  const tor = pose.torso || 0, up = Uv(tor), perp = [up[1], -up[0]];
  const hip = pose.origin || [0, 0];
  const neck = add(hip, up, P.torso);
  const shC = add(neck, up, -0.36 * (P.torso / ADULT.torso));
  const head = add(neck, Uv(tor + (pose.head || 0)), P.neck + P.headRy * 0.8);
  const front = pose.view !== 'side';
  const shL = front ? add(shC, perp, -P.shoulderW) : add(shC, perp, -0.05);
  const shR = front ? add(shC, perp, P.shoulderW) : add(shC, perp, 0.05);
  const hpL = front ? add(hip, perp, -P.hipW) : hip;
  const hpR = front ? add(hip, perp, P.hipW) : hip;
  const arm = (sh, a) => {
    const el = add(sh, D(a.s), P.upperArm);
    const ha = add(el, D(a.e), P.foreArm);
    return { sh, el, ha, end: add(ha, D(a.h ?? a.e), P.handL) };
  };
  const leg = (hp, l) => {
    const kn = add(hp, D(l.h), P.thigh);
    const an = add(kn, D(l.k), P.shin);
    const toe = front ? add(an, D(l.k), P.legR[2] * 1.6) : add(an, D((l.f ?? 90) * (pose.facing || 1)), P.footL);
    return { hp, kn, an, toe };
  };
  return {
    P, pose, up, perp, hip, neck, shC, head, front,
    armL: arm(shL, pose.armL), armR: arm(shR, pose.armR),
    legL: leg(hpL, pose.legL), legR: leg(hpR, pose.legR),
  };
}

function bounds(J, out) {
  const pts = [J.head, J.neck, J.hip, J.armL.end, J.armR.end, J.armL.el, J.armR.el,
    J.legL.toe, J.legR.toe, J.legL.an, J.legR.an, J.legL.kn, J.legR.kn];
  for (const p of pts) {
    out.minX = Math.min(out.minX, p[0]); out.maxX = Math.max(out.maxX, p[0]);
    out.minY = Math.min(out.minY, p[1]); out.maxY = Math.max(out.maxY, p[1]);
  }
  out.maxY = Math.max(out.maxY, J.head[1] + J.P.headRy * 1.1);
  return out;
}

// Tapered capsule between two points.
function capsule(g, a, b, r1, r2) {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  g.beginPath();
  g.arc(a[0], a[1], r1, ang + Math.PI / 2, ang + Math.PI * 1.5);
  g.arc(b[0], b[1], r2, ang - Math.PI / 2, ang + Math.PI / 2);
  g.closePath();
  g.fill();
}

function smoothClosed(g, pts) {
  g.beginPath();
  const n = pts.length;
  const mid = (i) => [(pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2];
  const m0 = mid(n - 1);
  g.moveTo(m0[0], m0[1]);
  for (let i = 0; i < n; i++) { const m = mid(i); g.quadraticCurveTo(pts[i][0], pts[i][1], m[0], m[1]); }
  g.closePath();
  g.fill();
}

// Draw one skeleton. `X` maps skeleton space (y up) to canvas pixels.
function drawBody(g, J, X, s, ink, far) {
  const P = J.P;
  const px = (p) => X(p);
  const torsoPts = () => {
    const at = (f, off) => { const c = add(J.hip, J.up, P.torso * f); return px(add(c, J.perp, off)); };
    if (J.front) {
      const hipHalf = P.hipW + P.legR[0] * 0.9, sh = P.shoulderW + P.armR[0] * 0.9;
      return [at(-0.14, -hipHalf * 1.02), at(0.36, -hipHalf * 0.86), at(0.7, -sh * 0.93), at(0.86, -sh * 1.02), at(0.95, -sh * 0.62),
        at(1.01, -P.neckR * 1.25), at(1.01, P.neckR * 1.25), at(0.95, sh * 0.62), at(0.86, sh * 1.02), at(0.7, sh * 0.93),
        at(0.36, hipHalf * 0.86), at(-0.14, hipHalf * 1.02)];
    }
    const c = P.chest, f = J.pose.facing || 1;
    return [at(-0.08, -c * 0.95 * f), at(0.4, -c * 0.78 * f), at(0.75, -c * 0.92 * f), at(0.97, -c * 0.62 * f),
      at(1.0, P.neckR * f), at(0.8, c * 1.05 * f), at(0.45, c * 0.85 * f), at(-0.08, c * 0.9 * f)];
  };
  const limbArm = (A, col) => {
    g.fillStyle = col;
    capsule(g, px(A.sh), px(A.el), P.armR[0] * s, P.armR[1] * s);
    capsule(g, px(A.el), px(A.ha), P.armR[1] * s, P.armR[2] * s);
    capsule(g, px(A.ha), px(A.end), P.armR[2] * s * 1.15, P.armR[2] * s * 0.8);
  };
  const limbLeg = (L, col) => {
    g.fillStyle = col;
    capsule(g, px(L.hp), px(L.kn), P.legR[0] * s, P.legR[1] * s);
    capsule(g, px(L.kn), px(L.an), P.legR[1] * s, P.legR[2] * s);
    capsule(g, px(L.an), px(L.toe), P.legR[2] * s * 1.15, P.legR[2] * s * 0.9);
    if (J.front) { const a = px(L.an); g.beginPath(); g.ellipse(a[0], a[1] + P.legR[2] * s * 0.9, P.legR[2] * s * 1.25, P.legR[2] * s * 0.75, 0, 0, Math.PI * 2); g.fill(); }
  };
  const farInk = far || ink;
  if (J.front) {
    limbLeg(J.legL, ink); limbLeg(J.legR, ink);
    g.fillStyle = ink; smoothClosed(g, torsoPts());
    limbArm(J.armL, ink); limbArm(J.armR, ink);
  } else {
    limbArm(J.armL, farInk); limbLeg(J.legL, farInk);
    g.fillStyle = ink; smoothClosed(g, torsoPts());
    limbLeg(J.legR, ink); limbArm(J.armR, ink);
  }
  // neck + head
  g.fillStyle = ink;
  capsule(g, px(J.neck), px(add(J.neck, Uv((J.pose.torso || 0) + (J.pose.head || 0)), P.neck)), P.neckR * s, P.neckR * s);
  const h = px(J.head), rot = ((J.pose.torso || 0) + (J.pose.head || 0)) * DEG;
  g.beginPath();
  g.ellipse(h[0], h[1], P.headRx * s, P.headRy * s, rot, 0, Math.PI * 2);
  g.fill();
  // hair volume: a little higher and wider at the crown, slightly toward the back in profile
  const back = J.front ? 0 : -(J.pose.facing || 1) * 0.08 * s;
  g.beginPath();
  g.ellipse(h[0] + back, h[1] - P.headRy * 0.22 * s, P.headRx * 1.07 * s, P.headRy * 0.82 * s, rot, Math.PI * 0.95, Math.PI * 2.05);
  g.fill();
}

// Fine paper-colored strokes that read as hand-drawn hatching and garment folds.
function drawDetails(g, J, X, s, seed) {
  const P = J.P, r = rng(seed);
  g.save();
  g.globalCompositeOperation = 'source-atop';
  g.lineCap = 'round';
  const line = (a, b, w, alpha) => {
    const A = X(a), B = X(b);
    g.strokeStyle = PAPER_LINE + alpha + ')';
    g.lineWidth = w * s;
    g.beginPath(); g.moveTo(A[0], A[1]); g.lineTo(B[0], B[1]); g.stroke();
  };
  // trouser creases
  for (const L of [J.legL, J.legR]) {
    line(add(L.hp, L.kn, 0), [L.kn[0] * 0.55 + L.hp[0] * 0.45, L.kn[1] * 0.55 + L.hp[1] * 0.45], 0.035, 0.28);
    line([L.kn[0], L.kn[1] - 0.1], [L.an[0] * 0.7 + L.kn[0] * 0.3, L.an[1] * 0.7 + L.kn[1] * 0.3], 0.03, 0.22);
  }
  // belt / jacket hem
  const hem = add(J.hip, J.up, P.torso * 0.05);
  line(add(hem, J.perp, -P.hipW - P.legR[0] * 0.6), add(hem, J.perp, P.hipW + P.legR[0] * 0.6), 0.03, J.front ? 0.3 : 0.18);
  // spine / back seam
  if (J.front) line(add(J.hip, J.up, P.torso * 0.12), add(J.hip, J.up, P.torso * 0.85), 0.025, 0.2);
  // sleeve folds
  for (const A of [J.armL, J.armR]) {
    for (let k = 0; k < 2; k++) {
      const f = 0.35 + k * 0.25, c = [A.sh[0] + (A.el[0] - A.sh[0]) * f, A.sh[1] + (A.el[1] - A.sh[1]) * f];
      const d = [A.el[1] - A.sh[1], -(A.el[0] - A.sh[0])], n = Math.hypot(d[0], d[1]) || 1;
      line(add(c, d, -0.12 / n), add(c, d, 0.12 / n), 0.025, 0.22);
    }
  }
  // diagonal hatching on the lit side
  const b = { minX: 1e9, maxX: -1e9, minY: 1e9, maxY: -1e9 };
  bounds(J, b);
  const cx = (b.minX + b.maxX) / 2;
  for (let i = 0; i < 70; i++) {
    const y = b.minY + (b.maxY - b.minY) * r();
    const x = cx + (b.maxX - cx) * (0.15 + r() * 0.9);
    const len = 0.25 + r() * 0.35;
    line([x, y], [x + len * 0.55, y + len], 0.018, 0.12 + r() * 0.12);
  }
  g.restore();
}

// Render a figure (optionally with extra props) into a canvas.
// `bodies` is a list of {P, pose}; the first one defines the ground line.
export function drawFigureCanvas(bodies, { pxPerUnit = 64, margin = 0.6, seed = 1, ink = INK, extra = null, box = null } = {}) {
  const Js = bodies.map((b) => joints(b.P, b.pose));
  const bb = box ? { ...box } : { minX: 1e9, maxX: -1e9, minY: 1e9, maxY: -1e9 };
  if (!box) Js.forEach((J) => bounds(J, bb));
  const minY = Math.min(...Js.map((J) => Math.min(J.legL.toe[1], J.legR.toe[1], J.legL.an[1], J.legR.an[1]) - J.P.legR[2]));
  bb.minY = box ? box.minY : minY;
  const s = pxPerUnit;
  const w = Math.ceil((bb.maxX - bb.minX + margin * 2) * s), h = Math.ceil((bb.maxY - bb.minY + margin * 2) * s);
  const cv = document.createElement('canvas');
  cv.width = w; cv.height = h;
  const g = cv.getContext('2d');
  const X = (p) => [(p[0] - bb.minX + margin) * s, h - (p[1] - bb.minY + margin) * s];
  for (const J of Js) {
    drawBody(g, J, X, s, ink, '#2c2733');
    drawDetails(g, J, X, s, seed++);
  }
  if (extra) extra(g, X, s, Js);
  roughen(cv, seed);
  // ground anchor in canvas pixels (x of first hip, y of the ground line)
  const anchor = X([Js[0].hip[0], bb.minY]);
  return { canvas: cv, anchor, unitsW: w / s, unitsH: h / s, box: bb, joints: Js };
}

// Re-stamp the drawing with sub-pixel jitter so edges read as ink rather than vector fills.
function roughen(cv, seed) {
  const r = rng(seed * 31 + 7), copy = document.createElement('canvas');
  copy.width = cv.width; copy.height = cv.height;
  copy.getContext('2d').drawImage(cv, 0, 0);
  const g = cv.getContext('2d');
  for (let i = 0; i < 4; i++) {
    g.globalAlpha = 0.35;
    g.drawImage(copy, (r() - 0.5) * 2.2, (r() - 0.5) * 2.2);
  }
  g.globalAlpha = 1;
}

function blurredCopy(src, px) {
  const c = document.createElement('canvas');
  c.width = src.width; c.height = src.height;
  const g = c.getContext('2d');
  g.filter = `blur(${px}px)`;
  g.drawImage(src, 0, 0);
  return c;
}

// A figure mounted in 3D: camera-facing plane + ground shadow. Height is in world units (meters).
export class InkFigure {
  constructor(bodies, {
    height = 1.75, kid = false, pxPerUnit = 64, seed = 1, shadow = true, shadowAngle = 0.6,
    shadowLen = 0.9, shadowOpacity = 0.28, extra = null, box = null, ink = INK, mirror = false,
  } = {}) {
    this.opts = { pxPerUnit, seed, extra, box, ink };
    const P = bodies[0].P;
    const unitsTall = P.torso + P.neck + P.headRy * 1.8 + P.thigh + P.shin + P.legR[2];
    this.mPerUnit = height / unitsTall;
    this.group = new THREE.Group();
    this.mirror = mirror;
    const fig = drawFigureCanvas(bodies, this.opts);
    this.fig = fig;
    this.tex = new THREE.CanvasTexture(fig.canvas);
    this.tex.colorSpace = THREE.SRGBColorSpace;
    this.tex.anisotropy = 4;
    const geo = this._planeGeo(fig);
    this.mat = new THREE.MeshBasicMaterial({ map: this.tex, transparent: true, alphaTest: 0.03, toneMapped: false, fog: true, side: THREE.DoubleSide });
    this.mesh = new THREE.Mesh(geo, this.mat);
    this.mesh.renderOrder = 2;
    this.holder = new THREE.Group();
    this.holder.add(this.mesh);
    this.group.add(this.holder);
    if (shadow) {
      this.shadowTex = new THREE.CanvasTexture(blurredCopy(fig.canvas, Math.max(2, pxPerUnit * 0.08)));
      this.shadowMat = new THREE.MeshBasicMaterial({ color: 0x000000, map: this.shadowTex, transparent: true, opacity: shadowOpacity, depthWrite: false, toneMapped: false });
      this.shadow = new THREE.Mesh(geo.clone(), this.shadowMat);
      this.shadow.rotation.x = -Math.PI / 2;
      this.shadow.scale.set(1, shadowLen, 1);
      this.shadowHolder = new THREE.Group();
      this.shadowHolder.rotation.y = shadowAngle;
      this.shadowHolder.position.y = 0.012;
      this.shadowHolder.add(this.shadow);
      this.group.add(this.shadowHolder);
    }
  }

  _planeGeo(fig) {
    const w = fig.unitsW * this.mPerUnit, h = fig.unitsH * this.mPerUnit;
    const geo = new THREE.PlaneGeometry(w, h);
    const ax = fig.anchor[0] / fig.canvas.width, ay = fig.anchor[1] / fig.canvas.height;
    geo.translate(w * (0.5 - ax), h * (0.5 - (1 - ay)) + 0.0, 0);
    geo.translate(0, 0, 0);
    if (this.mirror) geo.scale(-1, 1, 1);
    return geo;
  }

  // Redraw with a new pose (same canvas box so the anchor stays fixed).
  setBodies(bodies) {
    const fig = drawFigureCanvas(bodies, { ...this.opts, box: this.fig.box });
    const g = this.fig.canvas.getContext('2d');
    g.clearRect(0, 0, this.fig.canvas.width, this.fig.canvas.height);
    g.drawImage(fig.canvas, 0, 0);
    this.tex.needsUpdate = true;
  }

  face(camera) {
    const p = new THREE.Vector3();
    this.group.getWorldPosition(p);
    this.holder.rotation.y = Math.atan2(camera.position.x - p.x, camera.position.z - p.z) - this.group.rotation.y;
  }
}

// ---- pose library -------------------------------------------------------------------------
export const poses = {
  standBack: (o = {}) => ({ view: 'front', torso: 2, head: o.head || 0,
    armL: { s: -9, e: -14 }, armR: { s: 6, e: 2 }, legL: { h: -7, k: -12 }, legR: { h: 3, k: 2 } }),
  lookUp: () => ({ view: 'front', torso: -2.5, head: 0,
    armL: { s: -7, e: 0 }, armR: { s: 10, e: 17 }, legL: { h: -3, k: -2 }, legR: { h: 7, k: 13 } }),
  armRaised: () => ({ view: 'front', torso: 0,
    armL: { s: -10, e: -6 }, armR: { s: 158, e: 170 }, legL: { h: -5, k: -3 }, legR: { h: 4, k: 2 } }),
  armsOpen: () => ({ view: 'front', torso: 0,
    armL: { s: -48, e: -62 }, armR: { s: 48, e: 62 }, legL: { h: -6, k: -4 }, legR: { h: 6, k: 4 } }),
  lift: () => ({ view: 'front', torso: 0, head: 0,
    armL: { s: -176, e: 166 }, armR: { s: 176, e: -166 }, legL: { h: -8, k: -5 }, legR: { h: 9, k: 6 } }),
  kidUp: (origin) => ({ view: 'front', torso: 0, origin,
    armL: { s: -128, e: -150 }, armR: { s: 128, e: 150 }, legL: { h: -16, k: -4 }, legR: { h: 20, k: 34 } }),
  walk: (ph, facing = 1) => {
    const a = Math.sin(ph * Math.PI * 2), b = Math.cos(ph * Math.PI * 2);
    const knee = (x) => Math.max(0, x);
    return {
      view: 'side', facing, torso: 4 * facing, head: -2 * facing,
      armL: { s: 22 * a * facing, e: (22 * a + 14) * facing }, armR: { s: -22 * a * facing, e: (-22 * a + 14) * facing },
      legL: { h: -24 * a * facing, k: (-24 * a - 26 * knee(-b)) * facing, f: 90 },
      legR: { h: 24 * a * facing, k: (24 * a - 26 * knee(b)) * facing, f: 90 },
    };
  },
  sitSide: (facing = 1, o = {}) => ({ view: 'side', facing, torso: (o.lean ?? 8) * facing, head: (o.head ?? 6) * facing,
    armL: { s: 38 * facing, e: 86 * facing }, armR: { s: 44 * facing, e: 92 * facing },
    legL: { h: 88 * facing, k: 4 * facing, f: 90 }, legR: { h: 84 * facing, k: 0, f: 90 } }),
  sitFront: (o = {}) => ({ view: 'front', torso: o.lean || 0, head: o.head || 0,
    armL: { s: -14, e: o.reach ? 40 : 28 }, armR: { s: 14, e: o.reach ? -40 : -28 },
    legL: { h: -10, k: -4 }, legR: { h: 10, k: 4 } }),
};
