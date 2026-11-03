// Tiny static server (fonts from project node_modules, everything else from this folder) + Playwright screenshots.
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
import { chromium } from '/home/user/ccvedio/video/node_modules/playwright-core/index.mjs';
const HERE = path.dirname(new URL(import.meta.url).pathname);
const NM = '/home/user/ccvedio/video/node_modules';
const T = {'.html':'text/html','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.png':'image/png','.jpg':'image/jpeg','.js':'text/javascript'};
const srv = http.createServer((q, r) => {
  const u = decodeURIComponent(new URL(q.url, 'http://x').pathname);
  const f = u.startsWith('/nm/') ? path.join(NM, u.slice(4)) : path.join(HERE, u);
  if (!(f.startsWith(NM) || f.startsWith(HERE))) { r.writeHead(403).end(); return; }
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404).end(); return; } r.writeHead(200, {'content-type': T[path.extname(f)] || 'application/octet-stream'}); r.end(d); });
});
await new Promise(res => srv.listen(0, '127.0.0.1', res));
const port = srv.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const jobs = JSON.parse(process.argv[2]);
for (const [frame, w, h, out] of jobs) {
  const p = await browser.newPage({ viewport: { width: w, height: h } });
  await p.goto(`http://127.0.0.1:${port}/lookdev.html?f=${frame}`);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(HERE, out) });
  await p.close();
  console.log('shot', frame, out);
}
await browser.close(); srv.close();
