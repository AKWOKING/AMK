#!/usr/bin/env node
/**
 * AMK — DESIGN.md depuis une page réelle, sans extension Chrome.
 *
 * `bergside/design-md-chrome` extrait la typographie, les couleurs, les espacements, les rayons, les
 * ombres et les durées d'animation d'un onglet, puis écrit un `DESIGN.md`. C'est exactement l'outil
 * qu'il nous faut pour **codifier** un système de design — le nôtre ou celui d'une référence — mais
 * il ne s'installe que dans Chrome, à la main, onglet par onglet.
 *
 * Ici : on injecte le **même** `content-script.js` (amont intact) dans le Chromium embarqué, on
 * récupère sa charge utile par le même canal de message (un `chrome.runtime` factice), puis on
 * appelle les **mêmes** générateurs (`lib/normalize.mjs`, `lib/generate-design-md.mjs`).
 * Résultat : deux fichiers, `DESIGN.md` et `SKILL.md`, reproductibles en une commande.
 *
 * Usage : node tools/design-md/extract.mjs <url> [--out /tmp/design] [--name "DM OPTIQUE"]
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const EXT = process.env.AMK_DESIGNMD_SRC || '/tmp/amk-designmd/src';
const require = createRequire(import.meta.url);
const puppeteer = require(path.join(RT, 'node_modules', 'puppeteer-core'));
const { default: chromium } = await import(
  pathToFileURL(path.join(RT, 'node_modules', '@sparticuz', 'chromium', 'build', 'index.js')).href
);

const args = process.argv.slice(2);
const url = args.find((a) => !a.startsWith('--'));
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : fallback;
};
const OUT = opt('out', '/tmp/designmd');
const NAME = opt('name', '');
if (!url) {
  console.error('usage : node tools/design-md/extract.mjs <url> [--out /tmp/design] [--name "…"]');
  process.exit(2);
}
fs.mkdirSync(OUT, { recursive: true });

const source = fs.readFileSync(path.join(EXT, 'content-script.js'), 'utf8');
const browser = await puppeteer.launch({
  args: [...chromium.args, '--no-sandbox'],
  executablePath: await chromium.executablePath(),
  headless: 'shell',
});
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900 });
await page.goto(url, { waitUntil: 'load', timeout: 60000 });
await new Promise((r) => setTimeout(r, 1200)); // laisse les révélations au scroll se faire

// Le script amont s'accroche à `chrome.runtime.onMessage` : on lui donne ce qu'il attend, et on
// garde le callback pour lui poser la question nous-mêmes. Le code amont n'est pas modifié.
const payload = await page.evaluate(async (src) => {
  let listener = null;
  const chromeShim = { runtime: { onMessage: { addListener: (cb) => { listener = cb; } } } };
  new Function('chrome', src)(chromeShim);
  if (!listener) throw new Error("le script amont n'a pas posé d'écouteur");
  return await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("pas de réponse de l'extracteur")), 20000);
    listener({ type: 'TYPEUI_EXTRACT_STYLES' }, null, (r) => {
      clearTimeout(timer);
      r && r.ok ? resolve(r.payload) : reject(new Error(r && r.error ? r.error : 'extraction vide'));
    });
  });
}, source);
await browser.close();

const { normalizeExtractedStyles } = await import(pathToFileURL(path.join(EXT, 'lib', 'normalize.mjs')).href);
const { generateDesignMarkdown } = await import(pathToFileURL(path.join(EXT, 'lib', 'generate-design-md.mjs')).href);
const { generateSkillMarkdown } = await import(pathToFileURL(path.join(EXT, 'lib', 'generate-skill-md.mjs')).href);
const { validateMarkdownOutput } = await import(pathToFileURL(path.join(EXT, 'lib', 'validate.mjs')).href);

const normalized = normalizeExtractedStyles(payload);
const metadata = { brand: NAME || undefined, systemName: NAME || undefined, extractionUrl: url };
const designMd = generateDesignMarkdown({ normalized, metadata });
const skillMd = generateSkillMarkdown({ normalized, metadata });

const files = [['DESIGN.md', designMd], ['SKILL.md', skillMd]];
for (const [name, md] of files) {
  const mode = name === 'DESIGN.md' ? 'design' : 'skill';
  let verdict;
  try {
    verdict = validateMarkdownOutput(mode, md);
  } catch (e) {
    verdict = { ok: false, error: String(e) };
  }
  fs.writeFileSync(path.join(OUT, name), md, 'utf8');
  console.log(`${name.padEnd(10)} ${String(md.split('\n').length).padStart(4)} lignes · validation ${
    verdict && (verdict.ok || verdict.valid) ? 'OK' : JSON.stringify(verdict)
  }`);
}
console.log(`source     ${url}`);
console.log(`sortie     ${OUT}`);
