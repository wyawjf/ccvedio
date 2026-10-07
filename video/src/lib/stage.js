// Shared look: paper studio environment, brand materials, fake volumetrics and atmosphere.
import * as THREE from 'three';
import { rng } from './util.js';

export const C = {
  paper: '#ECE8E1', paperHi: '#F6F3EE', ink: '#15121b',
  violet: '#5B2EFF', violetHi: '#8B66FF', violetDeep: '#24106E', night: '#07050D',
};

export const mats = {
  violet: () => new THREE.MeshPhysicalMaterial({
    color: C.violet, roughness: 0.34, metalness: 0.0, clearcoat: 0.7, clearcoatRoughness: 0.22,
    emissive: '#3a17c9', emissiveIntensity: 0.18, envMapIntensity: 0.9,
  }),
  violetMatte: () => new THREE.MeshStandardMaterial({ color: C.violet, roughness: 0.62, emissive: '#2a0fa0', emissiveIntensity: 0.12 }),
  glow: (i = 4) => new THREE.MeshStandardMaterial({ color: '#000000', emissive: C.violetHi, emissiveIntensity: i, toneMapped: true }),
  clay: (c = '#F1EEE8') => new THREE.MeshStandardMaterial({ color: c, roughness: 0.92, metalness: 0 }),
  ink: () => new THREE.MeshStandardMaterial({ color: C.ink, roughness: 0.75 }),
};

// Vertical gradient sky dome; horizon color should match the fog color for a seamless horizon.
export function skyDome(top, horizon, bottom = horizon, radius = 900) {
  const geo = new THREE.SphereGeometry(radius, 48, 24);
  const mat = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: { top: { value: new THREE.Color(top) }, horizon: { value: new THREE.Color(horizon) }, bottom: { value: new THREE.Color(bottom) } },
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
    fragmentShader: `uniform vec3 top; uniform vec3 horizon; uniform vec3 bottom; varying vec3 vP;
      void main(){ float h = vP.y; vec3 c = h > 0.0 ? mix(horizon, top, pow(smoothstep(0.0, 0.85, h), 0.8)) : mix(horizon, bottom, smoothstep(0.0, -0.2, h));
      gl_FragColor = vec4(c, 1.0); }`,
  });
  const m = new THREE.Mesh(geo, mat);
  m.renderOrder = -10;
  m.frustumCulled = false;
  return m;
}

function paperTexture(seed = 3) {
  const cv = document.createElement('canvas'); cv.width = cv.height = 256;
  const g = cv.getContext('2d'), r = rng(seed), img = g.createImageData(256, 256);
  for (let i = 0; i < 256 * 256; i++) {
    const v = 236 + (r() - 0.5) * 14;
    img.data[i * 4] = v; img.data[i * 4 + 1] = v - 2; img.data[i * 4 + 2] = v - 6; img.data[i * 4 + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(cv);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(220, 220); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

// The "infinite paper studio": sky, fog, ground, key/fill lights.
export function studio(scene, env, o = {}) {
  const dark = !!o.dark;
  const horizon = o.horizon || (dark ? '#0b0814' : C.paper);
  scene.background = new THREE.Color(horizon);
  scene.fog = new THREE.Fog(horizon, o.fogNear ?? 40, o.fogFar ?? 220);
  scene.add(skyDome(o.top || (dark ? '#040308' : '#C9C1DE'), horizon, o.bottom || horizon));
  scene.environment = env;
  scene.environmentIntensity = o.envIntensity ?? (dark ? 0.25 : 0.45);

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(3000, 3000),
    dark
      ? new THREE.MeshStandardMaterial({ color: '#0d0a16', roughness: 0.78, metalness: 0.0 })
      : new THREE.MeshStandardMaterial({ color: o.ground || '#E6E1D8', roughness: 0.96, map: paperTexture() }),
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  const hemi = new THREE.HemisphereLight(dark ? '#5a46a8' : '#f4f2ff', dark ? '#080610' : '#b9ae9e', o.hemi ?? (dark ? 0.35 : 0.62));
  scene.add(hemi);

  const key = new THREE.DirectionalLight(o.keyColor || '#fff6ea', o.key ?? (dark ? 0.6 : 2.9));
  key.position.set(...(o.keyPos || [-30, 55, 25]));
  key.castShadow = o.shadows !== false;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.03;
  key.shadow.radius = 3;
  const sc = key.shadow.camera, ext = o.shadowExtent ?? 40;
  sc.left = -ext; sc.right = ext; sc.top = ext; sc.bottom = -ext; sc.near = 1; sc.far = 260;
  scene.add(key, key.target);
  return { ground, hemi, key };
}

// Point the key light + its shadow frustum at a region (used when a shot moves between sets).
export function aimKey(key, center, offset = [-30, 55, 25]) {
  key.target.position.set(center[0], center[1], center[2]);
  key.position.set(center[0] + offset[0], center[1] + offset[1], center[2] + offset[2]);
  key.target.updateMatrixWorld();
}

const radialCache = new Map();
export function radialTexture(inner = 'rgba(0,0,0,0.55)', outer = 'rgba(0,0,0,0)', size = 256) {
  const k = inner + outer + size;
  if (radialCache.has(k)) return radialCache.get(k);
  const cv = document.createElement('canvas'); cv.width = cv.height = size;
  const g = cv.getContext('2d'), gr = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gr.addColorStop(0, inner); gr.addColorStop(1, outer);
  g.fillStyle = gr; g.fillRect(0, 0, size, size);
  const t = new THREE.CanvasTexture(cv);
  radialCache.set(k, t);
  return t;
}

// Soft dark blob on the ground: cheap ambient occlusion under objects.
export function contactShadow(w, d, opacity = 0.5) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({
    map: radialTexture('rgba(20,14,30,1)', 'rgba(20,14,30,0)'), transparent: true, opacity, depthWrite: false, toneMapped: false,
  }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.015; m.renderOrder = 1;
  return m;
}

// Glow sprite (additive) for light sources and halos.
export function glowSprite(color = '#8B66FF', size = 4, opacity = 1) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({
    map: radialTexture('rgba(255,255,255,1)', 'rgba(255,255,255,0)'), color, transparent: true, opacity,
    blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false, fog: false,
  }));
  s.scale.set(size, size, 1);
  return s;
}

// Volumetric-looking light cone: open cylinder with a shader fading along length and toward the rim.
export function lightCone({ rTop = 0.5, rBottom = 6, height = 30, color = '#8B66FF', opacity = 0.5, additive = false, bottomFade = 0.86 } = {}) {
  const geo = new THREE.CylinderGeometry(rTop, rBottom, height, 64, 1, true);
  geo.translate(0, -height / 2, 0);
  const mat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, side: THREE.DoubleSide, fog: false,
    blending: additive ? THREE.AdditiveBlending : THREE.NormalBlending,
    uniforms: { color: { value: new THREE.Color(color) }, opacity: { value: opacity }, height: { value: height }, bottomFade: { value: bottomFade } },
    vertexShader: `varying float vY; varying vec3 vN; varying vec3 vV;
      void main(){ vY = position.y; vec4 mv = modelViewMatrix * vec4(position,1.0);
      vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform vec3 color; uniform float opacity; uniform float height; uniform float bottomFade; varying float vY; varying vec3 vN; varying vec3 vV;
      void main(){ float along = clamp(-vY / height, 0.0, 1.0);
        float rim = pow(abs(dot(normalize(vN), normalize(vV))), 1.6);
        float a = opacity * rim * (0.35 + 0.65 * along) * smoothstep(0.0, 0.08, along) * smoothstep(1.0, bottomFade, along);
        gl_FragColor = vec4(color, a); }`,
  });
  const m = new THREE.Mesh(geo, mat);
  m.renderOrder = 5;
  return m;
}

// Floating dust motes, deterministic in time.
export function dust({ count = 600, box = [40, 20, 40], center = [0, 10, 0], size = 0.06, color = '#ffffff', opacity = 0.6, seed = 9, additive = true } = {}) {
  const r = rng(seed), pos = new Float32Array(count * 3), base = new Float32Array(count * 3), ph = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    base[i * 3] = center[0] + (r() - 0.5) * box[0];
    base[i * 3 + 1] = center[1] + (r() - 0.5) * box[1];
    base[i * 3 + 2] = center[2] + (r() - 0.5) * box[2];
    ph[i] = r() * 100;
  }
  pos.set(base);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({
    size, color, transparent: true, opacity, depthWrite: false, sizeAttenuation: true,
    map: radialTexture('rgba(255,255,255,1)', 'rgba(255,255,255,0)', 64),
    blending: additive ? THREE.AdditiveBlending : THREE.NormalBlending, toneMapped: false,
  });
  const pts = new THREE.Points(geo, mat);
  pts.frustumCulled = false;
  pts.userData.update = (t) => {
    for (let i = 0; i < count; i++) {
      pos[i * 3] = base[i * 3] + Math.sin(t * 0.21 + ph[i]) * 0.6;
      pos[i * 3 + 1] = base[i * 3 + 1] + Math.sin(t * 0.17 + ph[i] * 1.3) * 0.5 + t * 0.08;
      pos[i * 3 + 2] = base[i * 3 + 2] + Math.cos(t * 0.19 + ph[i]) * 0.6;
    }
    geo.attributes.position.needsUpdate = true;
  };
  return pts;
}

// Large flat text rendered into a texture (for words carved into 3D surfaces).
export function textPlane(text, {
  font = "900 400px 'Noto Sans SC'", color = '#15121b', width = 10, height = 5, canvasW = 2048, canvasH = 1024,
  align = 'center', vertical = false, lineGap = 1.0, opacity = 1, ls = 0,
} = {}) {
  const cv = document.createElement('canvas'); cv.width = canvasW; cv.height = canvasH;
  const g = cv.getContext('2d');
  g.font = font; g.fillStyle = color; g.textBaseline = 'middle'; g.textAlign = align;
  if (ls) g.letterSpacing = `${ls}px`;
  if (vertical) {
    const chars = [...text], size = parseFloat(font.match(/(\d+)px/)[1]) * lineGap;
    chars.forEach((ch, i) => g.fillText(ch, canvasW / 2, canvasH / 2 + (i - (chars.length - 1) / 2) * size));
  } else {
    const lines = text.split('\n'), size = parseFloat(font.match(/(\d+)px/)[1]) * lineGap;
    const x = align === 'left' ? 0 : align === 'right' ? canvasW : canvasW / 2;
    lines.forEach((l, i) => g.fillText(l, x, canvasH / 2 + (i - (lines.length - 1) / 2) * size));
  }
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(width, height), new THREE.MeshBasicMaterial({
    map: tex, transparent: true, opacity, depthWrite: false, toneMapped: false, polygonOffset: true, polygonOffsetFactor: -2,
  }));
  return m;
}
