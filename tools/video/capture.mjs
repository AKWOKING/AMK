#!/usr/bin/env node
/**
 * AMK — capture de page réelle (Chromium headless + Puppeteer).
 *
 * Produit de la MATIÈRE PREMIÈRE EN MOUVEMENT : le défilement réel d'une page,
 * image par image, à cadence fixe. C'est ce qui manquait à toutes nos vidéos
 * (voir content/lessons/CONTENT-LESSONS.md §13 : nos vidéos étaient des diaporamas).
 *
 * Modes :
 *   scroll  images successives du défilement (défaut) → <out>/frames/f00001.jpg
 *   full    une capture pleine page (pour maquettes/aperçus)  → <out>/full.png
 *   hero    une capture du premier écran                     → <out>/hero.png
 *
 * Exemples :
 *   node tools/video/capture.mjs --url file:///home/user/AMK/hosting/previews/demo/x.html \
 *        --out /tmp/cap --mode scroll --duration 12
 *   node tools/video/capture.mjs --url https://exemple.cm --out /tmp/cap --mode full
 *
 * Prérequis : bash tools/video/install.sh, puis dans la session shell :
 *   export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib
 *   export FONTCONFIG_PATH=/tmp/amk-video/fonts
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const require = createRequire(import.meta.url);
// puppeteer-core se charge en CJS ; @sparticuz/chromium est ESM-only (v153)
const puppeteer = require(path.join(RT, 'node_modules', 'puppeteer-core'));
const { default: chromium } = await import(
  pathToFileURL(path.join(RT, 'node_modules', '@sparticuz', 'chromium', 'build', 'index.js')).href);

const args = {};
for (let i = 2; i < process.argv.length; i += 2) {
  if (process.argv[i] === '--json') { args.json = true; i -= 1; continue; }
  args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
}

// 540×960 CSS px à DSF 2 = exactement 1080×1920 (9:16) — la page est rendue
// en mise en page mobile, comme ce que verra un patient/élève sur son téléphone.
const W = parseInt(args.width || '540', 10);
const H = parseInt(args.height || '960', 10);
const DSF = parseFloat(args.dsf || '2');
const FPS = parseInt(args.fps || '30', 10);
const MODE = args.mode || 'scroll';
const OUT = args.out || '/tmp/amk-capture';
const HOLD_START = parseFloat(args['hold-start'] || '0.8');
const HOLD_END = parseFloat(args['hold-end'] || '1.2');
const MAX_SPEED = parseFloat(args['max-speed'] || '700'); // px CSS/s — lisible
const WAIT = parseInt(args.wait || '1400', 10);
const FROM_FRAC = parseFloat(args['from-frac'] ?? '0');
const TO_FRAC = parseFloat(args['to-frac'] ?? '1');
const SETTLE = parseInt(args.settle || '170', 10);   // laisse les révélations au scroll se terminer
const QUALITY = parseInt(args.quality || '92', 10);

if (!args.url) { console.error('✗ --url obligatoire'); process.exit(2); }
fs.mkdirSync(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: await chromium.executablePath(),
  args: [...chromium.args, '--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--hide-scrollbars'],
  headless: chromium.headless ?? 'shell',
  defaultViewport: null,
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: DSF });
  await page.goto(args.url, { waitUntil: 'load', timeout: 60000 });
  await page.evaluate(() => Promise.race([
    Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))),
    new Promise(r => setTimeout(r, 8000)),
  ]));
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await new Promise(r => setTimeout(r, WAIT));

  if (MODE === 'full' || MODE === 'hero') {
    const file = path.join(OUT, MODE === 'full' ? 'full.png' : 'hero.png');
    await page.screenshot({ path: file, fullPage: MODE === 'full' });
    const dims = await page.evaluate(() => ({ w: document.scrollingElement.scrollWidth, h: document.scrollingElement.scrollHeight }));
    console.log(`✓ ${MODE} → ${file}  (page ${dims.w}×${dims.h} CSS px)`);
  } else {
    const pageScroll = await page.evaluate(() =>
      Math.max(0, (document.scrollingElement.scrollHeight - window.innerHeight)));
    // plage : on peut ne filmer qu'une section (ex. --from-frac 0.05 --to-frac 0.45)
    const yStart = Math.round(pageScroll * Math.min(Math.max(FROM_FRAC, 0), 1));
    const yEnd = Math.round(pageScroll * Math.min(Math.max(TO_FRAC, 0), 1));
    const maxScroll = Math.max(0, yEnd - yStart);
    if (maxScroll < 40) { console.error('✗ plage vide'); process.exit(3); }
    if (maxScroll < 40) {
      console.error('✗ page non défilable (hauteur utile ' + maxScroll + ' px) — rien à capturer en mouvement');
      process.exit(3);
    }
    // durée : imposée (--duration) sinon déduite de la vitesse maximale lisible.
    // GARDE-FOU : si la durée imposée pousse la vitesse au-delà de --max-speed, on allonge
    // (un défilement trop rapide rend le texte illisible — mesuré : 1511 px/s était trop vite).
    let travel = args.duration
      ? Math.max(1.5, parseFloat(args.duration) - HOLD_START - HOLD_END)
      : maxScroll / MAX_SPEED;
    if (maxScroll / travel > MAX_SPEED) {
      travel = maxScroll / MAX_SPEED;
      console.log(`  ⚠ durée allongée : ${maxScroll} px ÷ ${MAX_SPEED} px/s → +${travel.toFixed(1)} s (lisibilité)`);
    }
    const duration = HOLD_START + travel + HOLD_END;
    const frames = Math.max(2, Math.round(duration * FPS));
    const dir = path.join(OUT, 'frames');
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });

    const easeInOut = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    for (let i = 0; i < frames; i++) {
      const t = i / FPS;
      const p = Math.min(1, Math.max(0, (t - HOLD_START) / travel));
      const y = yStart + Math.round(easeInOut(p) * maxScroll);
      await page.evaluate(_y => window.scrollTo(0, _y), y);
      if (SETTLE > 0) await new Promise(r => setTimeout(r, SETTLE));
      await page.screenshot({ path: path.join(dir, 'f' + String(i + 1).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: QUALITY });
    }
    const manifest = {
      url: args.url, mode: 'scroll', cssViewport: [W, H], deviceScaleFactor: DSF,
      output: [W * DSF, H * DSF], fps: FPS, frames, duration: +duration.toFixed(2),
      maxScrollCssPx: maxScroll, pixelsPerSecond: Math.round(maxScroll / travel),
      framesDir: dir,
    };
    fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 2));
    console.log(`✓ scroll → ${dir}  ·  ${frames} images  ·  ${duration.toFixed(1)} s  ·  ${Math.round(maxScroll / travel)} px/s  ·  sortie ${W * DSF}×${H * DSF}`);
    if (args.json) console.log(JSON.stringify(manifest));
  }
} finally {
  await browser.close();
}
