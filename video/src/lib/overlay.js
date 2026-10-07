// DOM text layer composited over the WebGL canvas; each frame the active shot returns a list of items.
export class Overlay {
  constructor(root) { this.root = root; this.els = new Map(); }

  render(items) {
    const seen = new Set();
    for (const it of items) {
      if (!it || (it.opacity ?? 1) <= 0.002) continue;
      seen.add(it.id);
      let el = this.els.get(it.id);
      if (!el) {
        el = document.createElement('div');
        el.className = 'ov';
        this.root.appendChild(el);
        this.els.set(it.id, el);
      }
      if (el._html !== it.html) { el.innerHTML = it.html; el._html = it.html; }
      const s = el.style, ax = it.ax ?? 0, ay = it.ay ?? 0;
      s.display = 'block';
      s.left = `${it.x ?? 0}px`;
      s.top = `${it.y ?? 0}px`;
      s.fontSize = `${it.size ?? 60}px`;
      s.fontWeight = it.weight ?? 900;
      s.fontFamily = it.font ?? "'Noto Sans SC', sans-serif";
      s.color = it.color ?? '#141218';
      s.lineHeight = it.lh ?? 1.14;
      s.letterSpacing = `${it.ls ?? 0}em`;
      s.textAlign = it.align ?? 'left';
      s.opacity = it.opacity ?? 1;
      s.zIndex = it.z ?? 10;
      s.transformOrigin = `${ax * 100}% ${ay * 100}%`;
      s.transform = `translate(${-ax * 100}%, ${-ay * 100}%) translate(${it.tx ?? 0}px, ${it.ty ?? 0}px) scale(${it.scale ?? 1})`;
      s.filter = it.blur ? `blur(${it.blur}px)` : 'none';
      s.textShadow = it.shadow ?? 'none';
      s.width = it.width ? `${it.width}px` : 'auto';
      s.whiteSpace = it.width ? 'normal' : 'nowrap';
      s.textWrapStyle = it.wrap === 'balance' ? 'balance' : 'auto';
    }
    for (const [id, el] of this.els) if (!seen.has(id)) el.style.display = 'none';
  }
}

// Thin annotation leader lines drawn in one full-frame SVG item.
export function leaderSVG(id, lines) {
  const body = lines.filter((l) => l.a > 0).map((l) => {
    const len = Math.hypot(l.x2 - l.x1, l.y2 - l.y1);
    return `<line x1="${l.x1}" y1="${l.y1}" x2="${l.x2}" y2="${l.y2}" stroke="${l.color || '#15121b'}" stroke-width="${l.w || 2}"
      stroke-dasharray="${len}" stroke-dashoffset="${len * (1 - l.a)}"/><circle cx="${l.x2}" cy="${l.y2}" r="${6 * l.a}" fill="${l.dot || '#5B2EFF'}"/>`;
  }).join('');
  return { id, x: 0, y: 0, html: `<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="display:block">${body}</svg>` };
}

// Lines that slide up out of a mask, the editorial "reveal" used for every headline.
export function revealHTML(lines, progs) {
  return lines.map((h, i) => {
    const p = progs[i] ?? progs[progs.length - 1];
    return `<span class="ln"><span style="transform:translateY(${((1 - p) * 108).toFixed(2)}%)">${h}</span></span>`;
  }).join('');
}

// Comic caption box (paper card, ink border, hard offset shadow) that pops in with `a` in 0..1.
export function capBox(id, html, { x = 72, y = 1180, w = 936, a = 1, size = 54, rot = -1.0, shadow = '#15121b', bg = '#F6F3EE',
  color = '#15121b', ax = 0, ay = 0, weight = 900 } = {}) {
  const k = Math.max(0, Math.min(1, a));
  return {
    id, x, y, ax, ay, size, weight, color, lh: 1.34, width: w, opacity: k > 0 ? Math.min(1, k * 1.6) : 0,
    scale: 0.9 + 0.1 * k, ty: (1 - k) * 40,
    html: `<div class="cap" style="transform:rotate(${rot}deg);background:${bg};box-shadow:14px 14px 0 ${shadow}">${html}</div>`,
  };
}

// Real photo as a taped comic panel with an ink tag underneath.
export function photo(id, src, { x, y, w, h, a = 1, rot = 2, tag = '', ax = 0, ay = 0, shadow = '#5B2EFF', zoom = 1 } = {}) {
  const k = Math.max(0, Math.min(1, a));
  return {
    id, x, y, ax, ay, opacity: k > 0 ? Math.min(1, k * 1.8) : 0, scale: 0.86 + 0.14 * k, ty: (1 - k) * 60,
    html: `<div class="ph" style="width:${w}px;height:${h}px;transform:rotate(${rot}deg);box-shadow:16px 16px 0 ${shadow};overflow:visible">
      <div style="width:${w}px;height:${h}px;overflow:hidden"><img src="${src}" style="width:${w}px;height:${h}px;object-fit:cover;transform:scale(${zoom.toFixed(4)})"></div>
      <div class="tape"></div>${tag ? `<div class="tag">${tag}</div>` : ''}</div>`,
  };
}
