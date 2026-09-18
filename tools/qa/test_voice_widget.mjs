#!/usr/bin/env node
/**
 * AMK — test de la couche vocale Tier 0 (site/index.html), protocole §21.
 *
 * Vérifie que le widget RÉPOND vraiment, dans les deux langues, qu'il ne fabrique
 * rien quand il ne sait pas, et que le bouton WhatsApp reste la voie principale.
 * Ne teste pas le micro (impossible en headless) — c'est le test sur téléphone de King.
 *
 * Usage : node tools/qa/test_voice_widget.mjs
 */
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const require = createRequire(import.meta.url);
const puppeteer = require(path.join(RT, 'node_modules', 'puppeteer-core'));
const { default: chromium } = await import(
  pathToFileURL(path.join(RT, 'node_modules', '@sparticuz', 'chromium', 'build', 'index.js')).href);

const URL = process.env.VX_URL || 'file:///home/user/AMK/site/index.html';
let fails = 0;
const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails++; };

const browser = await puppeteer.launch({
  executablePath: await chromium.executablePath(),
  args: [...chromium.args, '--no-sandbox', '--disable-dev-shm-usage', '--hide-scrollbars'],
  headless: chromium.headless ?? 'shell',
});

try {
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(URL, { waitUntil: 'load' });

  console.log('\n1 · Le widget existe, et le WhatsApp reste la voie principale');
  ok(await page.$$eval('#vx-fab', e => e.length) === 1, 'bouton flottant présent');
  const hidden = await page.$eval('#vx-panel', e => e.hidden);
  ok(hidden === true, 'panneau fermé au chargement (aucun micro qui écoute tout seul)');
  const waLinks = await page.$$eval('a[href*="wa.me"]', e => e.length);
  const barHref = await page.$eval('#mbar-wa', e => e.getAttribute('href') || '');
  ok(waLinks >= 1 && /wa\.me\/237677789631/.test(barHref),
     `${waLinks} lien(s) statique(s) + barre mobile câblée (${barHref.slice(0, 28)}…) — le repli WhatsApp est intact`);

  console.log('\n2 · Ouverture + questions suggérées');
  await page.click('#vx-fab');
  ok(await page.$eval('#vx-panel', e => !e.hidden), 'panneau ouvert après clic');
  const chips = await page.$$eval('.vx-chip', e => e.length);
  ok(chips >= 3, `${chips} questions suggérées (utilisables sans micro)`);

  console.log('\n3 · Réponses — anglais (langue par défaut de la page)');
  const ask = (q) => page.evaluate(q => { window.__vx.ask(q, false); return document.getElementById('vx-ans').textContent; }, q);

  const rPrice = await ask('how much does it cost?');
  ok(/100,000 FCFA/.test(rPrice), 'prix : 100 000 FCFA répondu');

  const rMonthly = await ask('what happens after launch, is there a monthly plan?');
  ok(/15,000 FCFA per month/.test(rMonthly), 'mensuel : 15 000 FCFA/mois répondu');
  ok(/two updates a month/.test(rMonthly), 'périmètre du mensuel énoncé (2 modifications/mois)');
  ok(/no contract|stop any time/i.test(rMonthly), 'sans engagement dit au client');
  ok(/domain and files stay yours/i.test(rMonthly), 'domaine et fichiers restent au client');

  const rDelay = await ask('how long does it take');
  ok(/3 to 5 days/.test(rDelay), 'délai : 3 à 5 jours répondu');

  const rBi = await ask('is french and english included?');
  ok(/Bilingual EN\|FR/.test(rBi), 'bilingue inclus répondu');

  console.log('\n4 · Le repli honnête — aucune invention');
  const rJunk = await ask('do you sell motorcycle tyres in Yaoundé?');
  ok(/I do not know that one/.test(rJunk), 'question hors périmètre → « je ne sais pas »');
  ok(/WhatsApp/.test(rJunk), 'le repli renvoie vers WhatsApp');

  console.log('\n5 · Le français suit la langue du site');
  await page.evaluate(() => { if (typeof setLang === 'function') setLang('fr'); });
  ok(await page.evaluate(() => document.documentElement.lang) === 'fr', 'page passée en français');
  const rFr = await ask('combien ça coute ?');
  ok(/100 000 FCFA/.test(rFr), 'prix en français');
  const rFrM = await ask('et après le lancement ?');
  ok(/15 000 FCFA par mois/.test(rFrM), 'mensuel en français');
  const chip0 = (await page.$eval('.vx-chip', e => e.textContent)).trim();
  ok(!/How much|cost/i.test(chip0), `puces retraduites : « ${chip0} »`);

  console.log('\n6 · Le lien WhatsApp part avec la question du visiteur');
  const href = await page.$eval('#vx-wa', e => e.getAttribute('href'));
  ok(/wa\.me\/237677789631\?text=/.test(href), 'numéro AMK dans le lien');
  ok(/coute|lancement/.test(decodeURIComponent(href)), 'la question est pré-remplie dans le message');

  console.log('\n7 · Interface mobile 390×844');
  await page.evaluate(() => { if (typeof setLang === 'function') setLang('en'); });
  await page.evaluate(() => window.__vx.ask('what happens after launch?', false));
  await new Promise(r => setTimeout(r, 350));
  const box = await page.$eval('#vx-panel', e => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
  ok(box.x >= 0 && box.x + box.w <= 390, `panneau dans l'écran (x=${Math.round(box.x)}, largeur=${Math.round(box.w)})`);
  const fab = await page.$eval('#vx-fab', e => { const r = e.getBoundingClientRect(); return { y: r.y, b: r.bottom }; });
  ok(fab.y > 690 && fab.b <= 844, `bouton au-dessus de la barre mobile (bas=${Math.round(fab.b)})`);
  await page.screenshot({ path: '/tmp/vx-mobile.png' });

  console.log('\n8 · Zéro erreur JavaScript');
  ok(errors.length === 0, errors.length ? 'erreurs : ' + errors.join(' | ') : 'aucune erreur de page');
} finally {
  await browser.close();
}

console.log(fails === 0 ? '\n✅ TOUT PASSE' : `\n❌ ${fails} échec(s)`);
process.exit(fails === 0 ? 0 : 1);
