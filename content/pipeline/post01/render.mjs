#!/usr/bin/env node
/**
 * AMK POST-01 — rendu frame-par-frame (déterministe) → MP4 silencieux 1080×1920.
 *
 * Méthode (ruling King 12/10 « build spec ») : Chromium headless (moteur /tmp/amk-video,
 * installé par tools/video/install.sh) pose chaque frame via window.seek(t) sur
 * content/pipeline/post01/POST-01.html, screenshot 540×960 @ DSF 2 → 1080×1920, puis
 * ffmpeg (imageio-ffmpeg) encode en H.264 yuv420p, SANS piste audio (-an).
 *
 * Usage :
 *   export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts
 *   node content/pipeline/post01/render.mjs --duration 3  --out content/pipeline/POST-01-DUMMY-2026-10-12.mp4
 *   node content/pipeline/post01/render.mjs --duration 45 --out content/pipeline/POST-01-BUG-LOGO-2026-10-12.mp4
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';
import { execFileSync, spawnSync } from 'child_process';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const require = createRequire(import.meta.url);
const puppeteer = require(path.join(RT, 'node_modules', 'puppeteer-core'));
const { default: chromium } = await import(
  pathToFileURL(path.join(RT, 'node_modules', '@sparticuz', 'chromium', 'build', 'index.js')).href);

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
const DURATION = parseFloat(args.duration || '45');
const FPS = parseInt(args.fps || '30', 10);
const OUT = args.out || '/tmp/post01.mp4';
const HTML = path.resolve(path.dirname(new URL(import.meta.url).pathname), 'POST-01.html');
const FRAMES = args.frames || '/tmp/post01-frames';

// ffmpeg depuis imageio-ffmpeg (pip) — même source que tools/video/install.sh
const FFMPEG = args.ffmpeg || execFileSync('python3',
  ['-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'], { encoding: 'utf8' }).trim();

fs.rmSync(FRAMES, { recursive: true, force: true });
fs.mkdirSync(FRAMES, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: await chromium.executablePath(),
  args: chromium.args,
  headless: true,
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 540, height: 960, deviceScaleFactor: 2 });
  await page.goto(pathToFileURL(HTML).href, { waitUntil: 'load' });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

  const n = Math.round(DURATION * FPS);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.seek(t), i / FPS);
    await page.screenshot({
      path: path.join(FRAMES, `f${String(i + 1).padStart(5, '0')}.jpg`),
      type: 'jpeg', quality: 92,
    });
    if (i % 150 === 0) console.log(`frame ${i + 1}/${n}`);
  }
  if (errors.length) { console.error('✗ erreurs console (§13 : 0 attendu) :', errors); process.exit(3); }
} finally { await browser.close(); }

const r = spawnSync(FFMPEG, ['-y', '-framerate', String(FPS), '-i', path.join(FRAMES, 'f%05d.jpg'),
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
  '-movflags', '+faststart', '-an', OUT], { stdio: 'inherit' });
if (r.status !== 0) { console.error('✗ ffmpeg a échoué'); process.exit(r.status ?? 1); }
console.log(`✓ ${OUT} (${DURATION}s @ ${FPS}fps, silencieux)`);
