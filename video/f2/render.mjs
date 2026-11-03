// Drive a render page in headless Chromium and stream frames into ffmpeg (or write stills).
//
//   node f2/render.mjs --page f2/film.html --stills 1.2,5,9.5 --out build/f2/stills
//   node f2/render.mjs --page f2/film.html --from 0 --to 12 --out build/f2/seg/a.mp4
//   node f2/render.mjs --page f2/post.html --w 1080 --h 1440 --frames 0,1,2 --out build/f2/carousel
// The page must define window.__ready, window.__duration and window.renderAt(t | frameIndex).
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../server.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, all) => {
  if (a.startsWith('--')) acc.push([a.slice(2), all[i + 1]?.startsWith('--') ? true : all[i + 1] ?? true]);
  return acc;
}, []));
const W = Number(args.w || 1080), H = Number(args.h || 1920);
const fps = Number(args.fps || 30);

const server = await startServer(ROOT);
const port = server.address().port;
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium',
  args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
    '--disable-gpu-sandbox', '--enable-webgl', '--disable-dev-shm-usage', '--font-render-hinting=none'],
});
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('[page]', m.text()); });
page.on('pageerror', (e) => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${port}/${args.page}${args.query ? '?' + args.query : ''}`);
await page.waitForFunction('window.__ready === true', null, { timeout: 300000 });
const duration = await page.evaluate('window.__duration || 0');

async function frameAt(t, type = 'jpeg') {
  await page.evaluate((tt) => window.renderAt(tt), t);
  return page.screenshot({ type, quality: type === 'jpeg' ? 95 : undefined, animations: 'disabled' });
}

if (args.stills || args.frames) {
  fs.mkdirSync(args.out, { recursive: true });
  const list = String(args.stills || args.frames).split(',');
  for (const s of list) {
    const t0 = Date.now();
    const buf = await frameAt(Number(s), 'png');
    const name = args.frames ? `${String(Number(s) + 1).padStart(2, '0')}.png` : `t${Number(s).toFixed(2).padStart(6, '0')}.png`;
    const f = path.join(args.out, name);
    fs.writeFileSync(f, buf);
    console.log(`still ${s} -> ${f} (${Date.now() - t0} ms)`);
  }
} else {
  const from = Number(args.from || 0), to = Math.min(Number(args.to ?? duration), duration);
  const f0 = Math.round(from * fps), f1 = Math.round(to * fps);
  fs.mkdirSync(path.dirname(args.out), { recursive: true });
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps),
    '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p',
    '-r', String(fps), args.out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const tStart = Date.now();
  for (let f = f0; f < f1; f++) {
    const buf = await frameAt(f / fps);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if ((f - f0) % 60 === 0) {
      const done = f - f0 + 1, el = (Date.now() - tStart) / 1000;
      console.log(`${args.out}: frame ${f}/${f1} (${(el / done).toFixed(2)} s/frame)`);
    }
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  console.log('done', args.out, ((Date.now() - tStart) / 1000).toFixed(1) + 's');
}
await browser.close();
server.close();
