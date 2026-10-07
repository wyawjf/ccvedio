// Data graphics drawn as SVG strings for the overlay (all inputs are real figures; see README sources).
import { clamp, easeOutCubic, seg } from './util.js';

const INK = '#15121b', VIO = '#5B2EFF', PAPER = '#F6F3EE';
let life = null, ecg = null;
export async function loadData() {
  life = await (await fetch('/assets/img/life.json')).json();
  ecg = (await (await fetch('/assets/img/ecg.json')).json()).values;
}

const svg = (w, h, body) => `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" style="display:block;overflow:visible">${body}</svg>`;

// Global life expectancy 1900 -> 2023, drawn progressively.
export function lifeChart(p, w = 900, h = 400) {
  const x = (yr) => 40 + ((yr - 1900) / (2023 - 1900)) * (w - 120), y = (v) => h - 40 - ((v - 25) / (80 - 25)) * (h - 80);
  const pts = life.map(([yr, v]) => [x(yr), y(v)]);
  let len = 0; for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
  const d = pts.map((q, i) => `${i ? 'L' : 'M'}${q[0].toFixed(1)},${q[1].toFixed(1)}`).join('');
  const k = easeOutCubic(clamp(p));
  const endI = Math.min(pts.length - 1, Math.floor(k * (pts.length - 1) + 0.0001));
  const last = pts[pts.length - 1];
  return svg(w, h, `
    <line x1="40" y1="${h - 40}" x2="${w - 60}" y2="${h - 40}" stroke="${INK}" stroke-width="4"/>
    <text x="40" y="${h}" font-family="Anton" font-size="34" fill="${INK}">1900</text>
    <text x="${w - 60}" y="${h}" font-family="Anton" font-size="34" fill="${INK}" text-anchor="end">2023</text>
    <path d="${d} L${last[0]},${h - 40} L${pts[0][0]},${h - 40} Z" fill="${VIO}" opacity="${0.14 * k}"/>
    <path d="${d}" fill="none" stroke="${VIO}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="${len}" stroke-dashoffset="${len * (1 - k)}"/>
    <circle cx="${pts[0][0]}" cy="${pts[0][1]}" r="12" fill="${INK}"/>
    <text x="${pts[0][0] + 6}" y="${pts[0][1] - 26}" font-family="Anton" font-size="64" fill="${INK}">32</text>
    <circle cx="${pts[endI][0]}" cy="${pts[endI][1]}" r="${14 * (k > 0.98 ? 1.2 : 1)}" fill="${VIO}" stroke="${PAPER}" stroke-width="5"/>
    <text x="${last[0] - 10}" y="${last[1] - 30}" font-family="Anton" font-size="86" fill="${VIO}" text-anchor="end" opacity="${seg(k, 0.85, 1)}">73</text>`);
}

// Bloom's 2-sigma result: the tutored distribution sits two standard deviations to the right.
export function bellCurves(p, w = 900, h = 360) {
  const k = easeOutCubic(clamp(p)), sx = (z) => 60 + ((z + 3.2) / 8.4) * (w - 120), sy = (v) => h - 50 - v * (h - 110) / 0.4;
  const g = (z, m) => Math.exp(-0.5 * (z - m) * (z - m)) / Math.sqrt(2 * Math.PI);
  const curve = (m) => { let s = ''; for (let z = -3.2; z <= 5.2; z += 0.1) s += `${s ? 'L' : 'M'}${sx(z).toFixed(1)},${sy(g(z, m)).toFixed(1)}`; return s; };
  const shift = 2 * k;
  return svg(w, h, `
    <line x1="40" y1="${h - 50}" x2="${w - 40}" y2="${h - 50}" stroke="${INK}" stroke-width="4"/>
    <path d="${curve(0)}" fill="none" stroke="${INK}" stroke-width="6"/>
    <path d="${curve(shift)} L${sx(5.2)},${h - 50} L${sx(-3.2)},${h - 50} Z" fill="${VIO}" opacity="0.22"/>
    <path d="${curve(shift)}" fill="none" stroke="${VIO}" stroke-width="8"/>
    <line x1="${sx(0)}" y1="${sy(0.4) - 10}" x2="${sx(0)}" y2="${h - 50}" stroke="${INK}" stroke-width="3" stroke-dasharray="10 8"/>
    <line x1="${sx(shift)}" y1="${sy(0.4) - 10}" x2="${sx(shift)}" y2="${h - 50}" stroke="${VIO}" stroke-width="3" stroke-dasharray="10 8"/>
    <text x="${sx(0)}" y="${h - 8}" font-family="Noto Sans SC" font-weight="900" font-size="30" fill="${INK}" text-anchor="middle">普通课堂</text>
    <text x="${sx(shift)}" y="${h - 8}" font-family="Noto Sans SC" font-weight="900" font-size="30" fill="${VIO}" text-anchor="middle" opacity="${k}">一对一辅导</text>
    <text x="${sx(shift) + 60}" y="${sy(0.3)}" font-family="Anton" font-size="58" fill="${VIO}" opacity="${seg(k, 0.5, 1)}">+2σ</text>`);
}

// 100 dots: 93 already spent, 7 left (Tim Urban, "The Tail End").
export function dotsGrid(p, w = 560) {
  const n = Math.floor(93 * easeOutCubic(clamp(p))), cell = w / 10, r = cell * 0.36;
  let body = '';
  for (let i = 0; i < 100; i++) {
    const cx = (i % 10) * cell + cell / 2, cy = Math.floor(i / 10) * cell + cell / 2;
    const used = i < n, left = i >= 93;
    body += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${left ? VIO : used ? INK : 'none'}" stroke="${left ? VIO : INK}" stroke-width="3" opacity="${left ? 0.55 + 0.45 * clamp(p * 2 - 1) : 1}"/>`;
  }
  return svg(w, w, body);
}

// Real ECG (MIT-BIH record 208) scrolling like a bedside monitor.
export function ecgLine(t, w = 1080, h = 200, speed = 0.9) {
  const n = ecg.length, span = Math.floor(n * 0.55), off = Math.floor((t * speed * n / 5) % n);
  let d = '';
  for (let i = 0; i < span; i++) {
    const v = ecg[(off + i) % n];
    d += `${i ? 'L' : 'M'}${((i / span) * w).toFixed(1)},${(h / 2 - v * h * 0.42).toFixed(1)}`;
  }
  return svg(w, h, `<path d="${d}" fill="none" stroke="${VIO}" stroke-width="12" opacity="0.25" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="${VIO}" stroke-width="5" stroke-linejoin="round"/>`);
}

// Researchers needed to double chip density: early 1970s = 1, today = 18 (Bloom et al., 2020).
export function bars18(p, w = 900) {
  const k = easeOutCubic(clamp(p)), unit = (w - 220) / 18;
  return svg(w, 230, `
    <text x="0" y="62" font-family="Noto Sans SC" font-weight="900" font-size="40" fill="${INK}">1971</text>
    <rect x="200" y="22" width="${unit}" height="56" fill="${INK}"/>
    <text x="0" y="172" font-family="Noto Sans SC" font-weight="900" font-size="40" fill="${VIO}">今天</text>
    <rect x="200" y="132" width="${unit * 18 * k}" height="56" fill="${VIO}"/>
    ${Array.from({ length: Math.floor(18 * k) }, (_, i) => `<line x1="${200 + unit * (i + 1)}" y1="132" x2="${200 + unit * (i + 1)}" y2="188" stroke="${PAPER}" stroke-width="3"/>`).join('')}`);
}
