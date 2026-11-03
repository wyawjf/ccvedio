// Static server (fonts + three from project node_modules under /nm/, everything else from this folder) + screenshots.
//   node video/f2/concepts/product/kit/shoot.mjs f01 f02 c01 ...      (no args = every frame)
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { chromium } from '/home/user/ccvedio/video/node_modules/playwright-core/index.mjs';
const HERE = path.dirname(new URL(import.meta.url).pathname);
const NM = '/home/user/ccvedio/video/node_modules';
const OUT = path.join(HERE, '..', 'proof', 'raw'); fs.mkdirSync(OUT, { recursive: true });
const T = { '.html': 'text/html', '.css': 'text/css', '.woff2': 'font/woff2', '.woff': 'font/woff', '.png': 'image/png', '.jpg': 'image/jpeg', '.js': 'text/javascript', '.mjs': 'text/javascript' };
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(new URL(q.url, 'http://x').pathname);
  const f = u.startsWith('/nm/') ? path.join(NM, u.slice(4)) : path.join(HERE, u);
  if (!(f.startsWith(NM) || f.startsWith(HERE))) { r.writeHead(403).end(); return; }
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404).end(); return; } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
});
await new Promise(res => srv.listen(0, '127.0.0.1', res));
const port = srv.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl', '--font-render-hinting=none'] });
const ALL = ['f01', 'f02', 'f03a', 'f03', 'f04', 'f05', 'f06', 'f06b', 'f07', 'f07b', 'f08', 'f09', 'f10', 'c01', 'c02', 'c05', 'c07'];
const list = process.argv.slice(2).length ? process.argv.slice(2) : ALL;
for (const f of list) {
  const h = f.startsWith('c') ? 1440 : 1920;
  const p = await browser.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('[pageerror]', f, e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('[console]', f, m.text()); });
  await p.goto(`http://127.0.0.1:${port}/proof.html?f=${f}`);
  await p.waitForFunction('window.__ready === true', null, { timeout: 120000 });
  await p.waitForTimeout(250);
  await p.screenshot({ path: path.join(OUT, `${f}.png`) });
  await p.close();
  console.log('shot', f);
}
await browser.close(); srv.close();
