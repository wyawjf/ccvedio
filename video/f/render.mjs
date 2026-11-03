// Render the F (Nadella) stills.
//   node f/render.mjs carousel   -> build/f/carousel/NN.png   (1080x1440 image post)
//   node f/render.mjs cards      -> build/f/cards/*.png       (1080x1920 video cards, bumpers, clip frames)
//   node f/render.mjs subs       -> build/f/subs/*.png        (subtitle strips listed in f/edl.json)
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../server.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const what = process.argv.slice(2);
const want = (k) => what.length === 0 || what.includes(k);
const slides = JSON.parse(fs.readFileSync(path.join(ROOT, 'f/slides.json'), 'utf8')).slides;
const edl = JSON.parse(fs.readFileSync(path.join(ROOT, 'f/edl.json'), 'utf8'));

const server = await startServer(ROOT);
const port = server.address().port;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });

async function shot(query, w, h, out, transparent = false) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto(`http://127.0.0.1:${port}/f/slides.html?${query}`);
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(250);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await page.screenshot({ path: out, type: 'png', omitBackground: transparent });
  await page.close();
}

if (want('carousel')) {
  for (let i = 0; i < slides.length; i++) {
    await shot(`i=${i}&h=1440`, 1080, 1440, path.join(ROOT, `build/f/carousel/${String(i + 1).padStart(2, '0')}.png`));
  }
  console.log(`carousel: ${slides.length} images`);
}

if (want('cards')) {
  for (let i = 0; i < slides.length; i++) {
    await shot(`i=${i}&h=1920`, 1080, 1920, path.join(ROOT, `build/f/cards/slide${i}.png`));
    if (slides[i].type === 'point') {
      await shot(`i=${i}&h=1920&mode=bump`, 1080, 1920, path.join(ROOT, `build/f/cards/bump${i}.png`));
      await shot(`i=${i}&h=1920&mode=frame`, 1080, 1920, path.join(ROOT, `build/f/cards/frame${i}.png`));
      await shot(`i=${i}&h=1920&mode=frametop`, 1080, 1920, path.join(ROOT, `build/f/cards/frametop${i}.png`), true);
    }
  }
  console.log('cards done');
}

if (want('subs')) {
  let k = 0;
  for (const item of edl.items) {
    if (item.type !== 'clip') continue;
    for (const [j, s] of item.subs.entries()) {
      const q = new URLSearchParams({ mode: 'sub', h: '380', zh: s.zh, en: s.en || '', draft: s.draft ? '1' : '0' });
      await shot(q.toString(), 1080, 380, path.join(ROOT, `build/f/subs/${item.id}_${j}.png`), true);
      k++;
    }
  }
  console.log(`subs: ${k} strips`);
}

await browser.close();
server.close();
