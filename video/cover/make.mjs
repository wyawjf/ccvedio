// Render a clean frame as the cover background, then lay the cover type over it.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer } from '../server.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const t = Number(process.argv[2] || 18.6);
const server = await startServer(ROOT);
const port = server.address().port;
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
});
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(`http://127.0.0.1:${port}/src/index.html?clean=1`);
await page.waitForFunction('window.__ready === true', null, { timeout: 180000 });
await page.evaluate((tt) => window.renderAt(tt), t);
fs.writeFileSync(path.join(ROOT, 'build/cover-bg.png'), await page.screenshot({ type: 'png' }));
const cover = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
await cover.goto(`http://127.0.0.1:${port}/cover/cover.html`);
await cover.evaluate(() => document.fonts.ready);
await cover.waitForTimeout(500);
await cover.screenshot({ path: path.join(ROOT, 'build/cover.jpg'), type: 'jpeg', quality: 92 });
await browser.close();
server.close();
console.log('cover written');
