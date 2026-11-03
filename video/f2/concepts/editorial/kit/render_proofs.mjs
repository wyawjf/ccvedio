// Proof frames for the PUBLIC DOMAIN concept (static layout proofs, not the film renderer).
//   python3 -I f2/concepts/editorial/kit/prep.py
//   node f2/concepts/editorial/kit/render_proofs.mjs            -> f2/concepts/editorial/proof/*.png
//   node f2/concepts/editorial/kit/render_proofs.mjs f1 c1       -> just those frames
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../../../../server.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../../../..');
const OUT = path.resolve(HERE, '../proof');
const ALL = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f11a', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'];
const frames = process.argv.slice(2).length ? process.argv.slice(2) : ALL;

const server = await startServer(ROOT);
const port = server.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox', '--force-color-profile=srgb'] });
fs.mkdirSync(OUT, { recursive: true });
for (const f of frames) {
  const page = await browser.newPage({ viewport: { width: 1080, height: f.startsWith('c') ? 1440 : 1920 } });
  await page.goto(`http://127.0.0.1:${port}/f2/concepts/editorial/kit/proof.html?f=${f}`);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, `${f.startsWith('c') ? 'carousel' : 'film'}_${f}.png`) });
  await page.close();
}
await browser.close();
server.close();
console.log(`proofs: ${frames.length} -> ${OUT}`);
