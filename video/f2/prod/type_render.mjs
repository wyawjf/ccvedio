// Render every unique type state of a timeline JSON to a transparent PNG (one file per state key).
//   node f2/prod/type_render.mjs --data build/f2/type_film.json --out build/f2/type [--parts 3] [--force]
// With --parts N it forks N browsers and splits the states between them.
import { chromium } from 'playwright-core';
import { fork } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../../server.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i < 0 ? d : (argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : true); };
const dataPath = arg('data', 'build/f2/type_film.json');
const outDir = path.resolve(ROOT, arg('out', 'build/f2/type'));
const parts = Number(arg('parts', 1));
const part = arg('part', null);
const force = !!arg('force', false);
const only = arg('only', null);   // comma list of state indices (debug)

const data = JSON.parse(fs.readFileSync(path.resolve(ROOT, dataPath), 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

if (parts > 1 && part === null) {
  const kids = [];
  for (let p = 0; p < parts; p++) {
    kids.push(new Promise((res, rej) => {
      const c = fork(fileURLToPath(import.meta.url), [...argv, '--part', String(p)], { stdio: 'inherit' });
      c.on('exit', (code) => (code === 0 ? res() : rej(new Error('part ' + p + ' failed'))));
    }));
  }
  await Promise.all(kids);
  process.exit(0);
}

const server = await startServer(ROOT);
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium',
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--font-render-hinting=none', '--disable-lcd-text', '--force-color-profile=srgb'],
});
const page = await browser.newPage({ viewport: { width: data.w, height: data.h }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.log('[pageerror]', e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/f2/prod/type.html?data=/${dataPath}`);
await page.waitForFunction('window.__ready === true', null, { timeout: 300000 });
const err = await page.evaluate('window.__error || null');
if (err) { console.error('type page error:', err); process.exit(2); }
const report = await page.evaluate('window.__fontReport');
const p = part === null ? 0 : Number(part);
if (p === 0) console.log('fonts:', JSON.stringify(report));

let todo = data.states.map((s, i) => i).filter((i) => i % parts === p);
if (only) todo = String(only).split(',').map(Number);
let done = 0;
const t0 = Date.now();
for (const i of todo) {
  const file = path.join(outDir, data.states[i].key + '.png');
  if (!force && fs.existsSync(file)) continue;
  await page.evaluate((k) => window.renderState(k), i);
  const buf = await page.screenshot({ type: 'png', omitBackground: true, animations: 'disabled' });
  fs.writeFileSync(file, buf);
  done++;
  if (done % 100 === 0) console.log(`type part ${p}: ${done}/${todo.length} (${((Date.now() - t0) / done).toFixed(0)} ms/state)`);
}
console.log(`type part ${p}: rendered ${done} states in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
await browser.close();
server.close();
