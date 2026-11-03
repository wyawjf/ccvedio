// Look-dev stills for THE LAST ELEMENT (static proofs, not the film renderer).
//   python3 -I f2/concepts/idea/kit/prep.py
//   node f2/concepts/idea/kit/render.mjs [f01 c1 ...]      -> f2/concepts/idea/proof/raw/*.png
//   then the finishing pass (grain / halation / vignette) with f2/film.py --still and kit/look.json
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../../../../server.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../../../..');
const OUT = path.resolve(HERE, '../proof/raw');
const ALL = ['f01', 'f03', 'f04', 'f05a', 'f05', 'f06', 'f07', 'f08a', 'f08', 'f09', 'f10', 'f11', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'];
const frames = process.argv.slice(2).length ? process.argv.slice(2) : ALL;
const server = await startServer(ROOT);
const port = server.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none'] });
fs.mkdirSync(OUT, { recursive: true });
for (const f of frames) {
  const page = await browser.newPage({ viewport: { width: 1080, height: f.startsWith('c') ? 1440 : 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.log('[pageerror]', f, e.message));
  await page.goto(`http://127.0.0.1:${port}/f2/concepts/idea/kit/lookdev.html?f=${f}`);
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(OUT, `${f}.png`) });
  await page.close();
  console.log('still', f);
}
await browser.close();
server.close();
