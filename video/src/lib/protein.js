// Procedural protein "cartoon" geometry: alpha-helix ribbons, beta-strand arrows and coil loops.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

// Sweep an elliptical cross-section along points. widthDir(i) gives the ribbon's broad axis.
function sweep(points, widthDir, halfW, halfH, radial) {
  const n = points.length, pos = [], idx = [];
  for (let i = 0; i < n; i++) {
    const p = points[i];
    const tan = points[Math.min(n - 1, i + 1)].clone().sub(points[Math.max(0, i - 1)]).normalize();
    let w = widthDir(i, tan).clone();
    w.sub(tan.clone().multiplyScalar(w.dot(tan))).normalize();
    const b = new THREE.Vector3().crossVectors(tan, w).normalize();
    const hw = typeof halfW === 'function' ? halfW(i / (n - 1)) : halfW;
    const hh = typeof halfH === 'function' ? halfH(i / (n - 1)) : halfH;
    for (let k = 0; k < radial; k++) {
      const a = (k / radial) * Math.PI * 2;
      const o = w.clone().multiplyScalar(Math.cos(a) * hw).add(b.clone().multiplyScalar(Math.sin(a) * hh));
      pos.push(p.x + o.x, p.y + o.y, p.z + o.z);
    }
  }
  for (let i = 0; i < n - 1; i++) {
    for (let k = 0; k < radial; k++) {
      const a = i * radial + k, b2 = i * radial + ((k + 1) % radial), c = a + radial, d = b2 + radial;
      idx.push(a, c, b2, b2, c, d);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

function anyPerp(v) {
  const a = Math.abs(v.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0);
  return new THREE.Vector3().crossVectors(v, a).normalize();
}

export function proteinGeometry(rand, { segments = 5, detail = 1 } = {}) {
  const radial = detail > 0.7 ? 10 : 6;
  const step = detail > 0.7 ? 1 : 2;
  const parts = [];
  let cur = new THREE.Vector3(0, 0, 0);
  let dir = new THREE.Vector3(rand() - 0.5, rand() - 0.5, rand() - 0.5).normalize();
  const rv = () => new THREE.Vector3(rand() - 0.5, rand() - 0.5, rand() - 0.5);

  for (let s = 0; s < segments; s++) {
    const kind = rand() < 0.62 ? 'helix' : 'strand';
    dir = dir.clone().add(rv().multiplyScalar(1.6)).normalize();
    if (kind === 'helix') {
      const L = 1.3 + rand() * 1.4, R = 0.23, pitch = 0.54;
      const turns = L / pitch, N = Math.floor((turns * 18) / step);
      const u = anyPerp(dir), v = new THREE.Vector3().crossVectors(dir, u);
      const pts = [];
      for (let i = 0; i <= N; i++) {
        const t = i / N, ang = t * turns * Math.PI * 2;
        pts.push(cur.clone().add(dir.clone().multiplyScalar(t * L))
          .add(u.clone().multiplyScalar(Math.cos(ang) * R)).add(v.clone().multiplyScalar(Math.sin(ang) * R)));
      }
      const axis = dir.clone();
      parts.push(sweep(pts, () => axis, (f) => 0.2 * Math.min(1, f * 8, (1 - f) * 8) + 0.04, 0.06, radial));
      cur = pts[pts.length - 1].clone();
    } else {
      const L = 1.0 + rand() * 0.9, N = Math.floor(14 / step), pts = [];
      for (let i = 0; i <= N; i++) {
        const t = i / N;
        pts.push(cur.clone().add(dir.clone().multiplyScalar(t * L)).add(anyPerp(dir).multiplyScalar(Math.sin(t * Math.PI * 3) * 0.04)));
      }
      const wdir = anyPerp(dir);
      parts.push(sweep(pts, () => wdir, (f) => (f < 0.72 ? 0.17 : 0.32 * (1 - (f - 0.72) / 0.28) + 0.02), 0.05, Math.max(4, radial - 2)));
      cur = pts[pts.length - 1].clone();
    }
    // coil loop to the next element
    if (s < segments - 1) {
      const a = cur.clone(), d = a.clone().add(dir.clone().multiplyScalar(0.35)).add(rv().multiplyScalar(0.7));
      const e = d.clone().add(rv().multiplyScalar(0.6)).add(dir.clone().multiplyScalar(-0.5));
      const curve = new THREE.CatmullRomCurve3([a, d, e]);
      const pts = curve.getPoints(Math.floor(16 / step));
      parts.push(sweep(pts, (i, tan) => anyPerp(tan), 0.065, 0.065, Math.max(5, radial - 4)));
      cur = e.clone();
    }
  }
  const g = mergeGeometries(parts);
  g.computeBoundingSphere();
  const c = g.boundingSphere.center;
  g.translate(-c.x, -c.y, -c.z);
  g.scale(1 / g.boundingSphere.radius, 1 / g.boundingSphere.radius, 1 / g.boundingSphere.radius);
  g.computeBoundingSphere();
  return g;
}
