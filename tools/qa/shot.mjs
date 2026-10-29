#!/usr/bin/env node
/**
 * AMK — vérification de design dans un VRAI navigateur (Chromium + Puppeteer).
 *
 * C'est l'étape 4 du skill `pro-design` : ouvrir la page, capturer, contrôler, corriger.
 * Il remplace l'aveu « URL live inaccessible » par un outil qui mesure.
 *
 * Ce qu'il fait, dans cet ordre :
 *   1. ouvre la page (fichier local, ou URL si le réseau la laisse passer)
 *   2. capture à 1440 px et à 390 px → <out>/desktop.png, <out>/mobile.png
 *   3. mesure : débordement horizontal, texte coupé, images cassées, contraste AA,
 *      erreurs console, focus clavier visible, héro visible dans le premier écran
 *   4. écrit <out>/rapport.json + un résumé lisible, code de sortie 1 si un P1 est trouvé
 *
 * Usage :
 *   bash tools/video/install.sh                        # une fois par session
 *   python3 tools/qa/shot.py <fichier.html|URL> [--out /tmp/shot] [--strict]
 *
 * Prérequis dans la session shell (relancés par shot.py lui-même) :
 *   LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib   FONTCONFIG_PATH=/tmp/amk-video/fonts
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { pathToFileURL } from 'url';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const require = createRequire(import.meta.url);
const puppeteer = require(path.join(RT, 'node_modules', 'puppeteer-core'));
const { default: chromium } = await import(
  pathToFileURL(path.join(RT, 'node_modules', '@sparticuz', 'chromium', 'build', 'index.js')).href);

const args = {};
for (let i = 2; i < process.argv.length; i += 2) {
  if (process.argv[i].startsWith('--') === false) continue;
  if (process.argv[i + 1] === undefined || process.argv[i + 1].startsWith('--')) { args[process.argv[i].slice(2)] = true; i -= 1; continue; }
  args[process.argv[i].slice(2)] = process.argv[i + 1];
}

const target = args.url || process.argv[2];
if (!target) { console.error('usage : node shot.mjs --url <fichier|URL> [--out dir] [--strict]'); process.exit(2); }
const OUT = args.out || '/tmp/amk-shot';
const STRICT = Boolean(args.strict);
fs.mkdirSync(OUT, { recursive: true });

const url = /^https?:\/\//.test(target) ? target : pathToFileURL(path.resolve(target)).href;

const executablePath = await chromium.executablePath();
const browser = await puppeteer.launch({
  executablePath,
  args: [...chromium.args, '--no-sandbox', '--font-render-hinting=none'],
  headless: 'shell',
});

const findings = [];
const add = (level, code, msg, where) => findings.push({ level, code, msg, ...(where ? { where } : {}) });

/** contraste WCAG AA : ratio entre deux couleurs rgb */
const lum = ([r, g, b]) => {
  const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); const [hi, lo] = l1 > l2 ? [l1, l2] : [l2, l1]; return (hi + 0.05) / (lo + 0.05); };
const parseRGB = s => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null; const p = m[1].split(',').map(Number); return { rgb: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 }; };

async function audit(width, height, label, fullPage) {
  const page = await browser.newPage();
  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => consoleErrors.push('pageerror: ' + String(e).slice(0, 200)));
  const failedReq = [];
  page.on('requestfailed', r => failedReq.push(r.url().slice(0, 120)));

  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  try {
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  } catch (e) {
    add('P1', 'LOAD', `la page ne charge pas : ${e.message.slice(0, 160)}`, label);
  }
  await new Promise(r => setTimeout(r, 400));

  // Défilement complet AVANT toute mesure : sans ça, les révélations au scroll
  // (IntersectionObserver) ne se déclenchent jamais et la page paraît vide.
  // Deux passes, hauteur relue à chaque pas (elle grandit quand le contenu se révèle) :
  // une seule passe rapide produit des faux positifs, et un outil qui crie au loup ne sert à rien.
  const scrollAll = async (pause) => page.evaluate(async (ms) => {
    const sleep = t => new Promise(r => setTimeout(r, t));
    // `scroll-behavior:smooth` fait durer le retour en haut : on le neutralise le temps du test,
    // sinon la capture « premier écran » est prise à mi-défilement (faux positif de h1 absent).
    const de = document.documentElement;
    const smooth = de.style.scrollBehavior;
    de.style.scrollBehavior = 'auto';
    for (let pass = 0; pass < 2; pass++) {
      let y = 0;
      while (y < document.documentElement.scrollHeight - 4) {
        window.scrollTo(0, y);
        await sleep(ms);
        y += Math.max(220, Math.round(window.innerHeight * 0.6));
      }
    }
    window.scrollTo(0, 0);
    await sleep(350);
    de.style.scrollBehavior = smooth;
  }, pause);
  await scrollAll(140);
  await new Promise(r => setTimeout(r, 300));

  const m = await page.evaluate(() => {
    // helpers recréés ici : cette fonction s'exécute dans le navigateur, pas dans Node
    const lum = ([r, g, b]) => {
      const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); const [hi, lo] = l1 > l2 ? [l1, l2] : [l2, l1]; return (hi + 0.05) / (lo + 0.05); };
    const parseRGB = s => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null; const p = m[1].split(',').map(Number); return { rgb: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 }; };

    const de = document.documentElement;
    const overflowX = Math.max(de.scrollWidth, document.body ? document.body.scrollWidth : 0) - de.clientWidth;

    // éléments qui dépassent la fenêtre — SAUF ceux d'un carrousel horizontal :
    // une carte hors écran à droite est le principe du carrousel, pas un défaut.
    const inScroller = el => {
      let n = el.parentElement;
      while (n && n !== document.body) {
        if (/auto|scroll/.test(getComputedStyle(n).overflowX)) return true;
        n = n.parentElement;
      }
      return false;
    };
    // Un tiroir fermé n'est pas un défaut de mise en page : ses liens attendent hors cadre derrière
    // le bouton menu (details non [open], aria-hidden, inert). On ne les compte ni ici ni au contraste.
    const inClosedPanel = el => Boolean(el.closest('details:not([open]), [aria-hidden="true"], [inert]'));
    const wide = [];
    document.querySelectorAll('body *').forEach(el => {
      if (inClosedPanel(el)) return;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      if (r.right > de.clientWidth + 2 || r.left < -2) {
        const cs = getComputedStyle(el);
        if (cs.position === 'fixed' || cs.visibility === 'hidden' || cs.display === 'none') return;
        if (inScroller(el)) return;
        wide.push({ tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 40), left: Math.round(r.left), right: Math.round(r.right) });
      }
    });

    // texte coupé : scrollHeight > clientHeight sur un conteneur à hauteur fixe / overflow hidden
    const clipped = [];
    document.querySelectorAll('h1,h2,h3,p,li,a,button,span').forEach(el => {
      const cs = getComputedStyle(el);
      // 29/10 : un texte masqué aux yeux mais pas aux lecteurs d'écran (.v2-sr, .sr, clip rect)
      // n'est PAS un texte coupé. Le compter comme tel produisait un faux P2 à chaque ajout
      // d'une précision accessible, et un faux positif coûte plus qu'un défaut manqué (§27.5).
      if (cs.width.match(/^(0|1)(\.\d+)?px$/) || cs.height.match(/^(0|1)(\.\d+)?px$/)) return;
      if (cs.overflow === 'hidden' && el.scrollHeight > el.clientHeight + 2 && el.clientHeight > 0) {
        clipped.push({ tag: el.tagName.toLowerCase(), text: (el.textContent || '').trim().slice(0, 50) });
      }
    });

    // images cassées
    const brokenImgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.currentSrc || i.src).slice(0, 10);

    // contraste sur les textes visibles
    const lowContrast = [];
    const bodyBg = getComputedStyle(document.body || de).backgroundColor;
    const seen = new Set();
    document.querySelectorAll('h1,h2,h3,h4,p,li,a,button,label,span,strong,em,td,th').forEach(el => {
      if (!el.textContent || !el.textContent.trim()) return;
      if (inClosedPanel(el)) return;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.6) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (r.top > de.clientHeight * 6) return;
      const fg = parseRGB(cs.color);
      let bg = parseRGB(cs.backgroundColor);
      let node = el;
      while ((!bg || bg.a === 0) && node && node !== document.documentElement) { node = node.parentElement; if (node) bg = parseRGB(getComputedStyle(node).backgroundColor); }
      if (!bg || bg.a === 0) bg = parseRGB(bodyBg) || { rgb: [255, 255, 255], a: 1 };
      if (!fg) return;
      const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10) || 400;
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const need = large ? 3 : 4.5;
      const cr = ratio(fg.rgb, bg.rgb);
      const key = cs.color + '|' + size + '|' + (el.tagName);
      if (cr < need && !seen.has(key)) {
        seen.add(key);
        lowContrast.push({ tag: el.tagName.toLowerCase(), text: (el.textContent || '').trim().slice(0, 40), ratio: Math.round(cr * 100) / 100, need, size, color: cs.color, bg: `rgb(${bg.rgb.join(',')})` });
      }
    });

    // héro visible dans le premier écran : un h1 lisible sans défiler
    const h1 = document.querySelector('h1');
    const h1Rect = h1 ? h1.getBoundingClientRect() : null;
    const heroVisible = Boolean(h1Rect && h1Rect.top < de.clientHeight * 0.9 && h1Rect.bottom > 0 && h1Rect.height > 0);
    const heroText = h1 ? (h1.textContent || '').trim().slice(0, 80) : null;

    // focus visible : on cible le premier élément interactif et on regarde son outline
    let focusVisible = null;
    const first = document.querySelector('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])');
    if (first) {
      first.focus();
      const cs = getComputedStyle(first);
      focusVisible = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== 'none';
      // on rend le focus au document : sinon la capture montre le liseré du curseur clavier
      // (par exemple le lien « Aller au contenu ») que le visiteur, lui, ne voit pas.
      first.blur();
    }

    // contenu qui n'apparaît qu'après une animation : opacité 0 / visibilité cachée
    const hidden = [];
    document.querySelectorAll('section, article, div, figure, ul').forEach(el => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      if (r.height < 120 || r.width < 200) return;
      if (parseFloat(cs.opacity) < 0.15) hidden.push({ tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 40), why: 'opacity ' + cs.opacity });
      else if (cs.visibility === 'hidden') hidden.push({ tag: el.tagName.toLowerCase(), cls: (el.className || '').toString().slice(0, 40), why: 'visibility hidden' });
    });

    // zones vides dans la page : grands blocs sans texte visible
    let blank = 0;
    document.querySelectorAll('body > section, body > div, main > section').forEach(el => {
      const r = el.getBoundingClientRect();
      const txt = (el.innerText || '').trim();
      if (r.height > 200 && txt.length === 0) blank += 1;
    });

    return { overflowX, wide: wide.slice(0, 8), clipped: clipped.slice(0, 8), brokenImgs, lowContrast: lowContrast.slice(0, 10), heroVisible, heroText, focusVisible, hidden: hidden.slice(0, 6), blank, title: document.title, height: de.scrollHeight };
  });

  if (m.overflowX > 2) add('P1', 'OVERFLOW', `débordement horizontal de ${m.overflowX} px`, `${label} · ${m.wide.map(w => `<${w.tag}> ${w.cls}`).join(' | ') || 'cause non isolée'}`);
  else if (m.wide.length) add('P3', 'WIDE', `${m.wide.length} élément(s) hors cadre sans débordement de page`, `${label} · ${m.wide.map(w => `<${w.tag}> ${w.cls}`).join(' | ')}`);
  if (m.clipped.length) add('P2', 'CLIPPED', `texte coupé dans ${m.clipped.length} élément(s)`, `${label} · ${m.clipped.map(c => `<${c.tag}> "${c.text}"`).join(' | ')}`);
  if (m.brokenImgs.length) add('P1', 'IMG', `${m.brokenImgs.length} image(s) cassée(s)`, `${label} · ${m.brokenImgs.join(' | ')}`);
  if (m.lowContrast.length) add('P2', 'CONTRAST', `${m.lowContrast.length} texte(s) sous WCAG AA`, `${label} · ${m.lowContrast.map(c => `"${c.text}" ${c.ratio}:1 (il faut ${c.need}) ${c.color} sur ${c.bg}`).join(' | ')}`);
  if (!m.heroVisible) add('P2', 'HERO', 'aucun h1 visible dans le premier écran', label);
  if (m.focusVisible === false) add('P2', 'FOCUS', 'le premier élément interactif n\'a pas de focus visible', label);
  if (m.focusVisible === null) add('P3', 'FOCUS', 'aucun élément interactif à cibler', label);
  if (m.hidden.length) add('P2', 'HIDDEN', `${m.hidden.length} bloc(s) restent invisibles après défilement`, `${label} · ${m.hidden.map(h => `<${h.tag}> ${h.cls} (${h.why})`).join(' | ')}`);
  if (m.blank) add('P2', 'BLANK', `${m.blank} grand(s) bloc(s) sans aucun texte visible`, label);
  if (consoleErrors.length) add('P1', 'CONSOLE', `${consoleErrors.length} erreur(s) console`, `${label} · ${consoleErrors.slice(0, 4).join(' | ')}`);
  if (failedReq.length) add('P2', 'NETWORK', `${failedReq.length} requête(s) échouée(s)`, `${label} · ${failedReq.slice(0, 4).join(' | ')}`);

  // ── RÈGLES §13 / §3 / §5 / §7 que le rendu seul peut vérifier (une fois, sur le desktop) ───────────
  if (label === 'desktop') {
    const r = await page.evaluate(() => {
      const txt = el => (el.textContent || '').replace(/\s+/g, ' ').trim();
      const css = [];
      for (const sh of Array.from(document.styleSheets)) {
        try { for (const rule of Array.from(sh.cssRules)) css.push(rule.cssText); } catch (e) { /* feuille cross-origin */ }
      }
      const CSS = css.join('\n');

      // 1 · bilinguisme : chaque texte doit exister dans les deux langues (data-en / data-fr)
      const en = document.querySelectorAll('[data-en]').length;
      const fr = document.querySelectorAll('[data-fr]').length;
      const orphan = document.querySelectorAll('[data-en]:not([data-fr]), [data-fr]:not([data-en])').length;

      // 2 · le premier écran : combien de blocs de texte y vivent réellement
      const h1 = document.querySelector('h1');
      let heroLeaves = 0, h1Lines = 0, heroHost = null;
      if (h1) {
        heroHost = h1.closest('section, header, [class*="hero"]') || h1.parentElement;
        const leaves = Array.from(heroHost.querySelectorAll('*')).filter(el => {
          if (el.closest('svg')) return false;
          // §3.3 : une colonne qui porte un vrai élément (carte, table, figure) n'est pas une pile de
          // texte. On mesure la pile, et le widget compte pour un : c'est la lecture du §7.
          if (el.closest('figure, table, dl, form')) return false;
          // 28/10 · deux fausses alertes : la mesure comptait (a) les blocs SOUS la ligne de flottaison
          // — une galerie de 24 fiches annonçait « 150 blocs » — et (b) chaque puce d'une liste répétée,
          // alors que la loi de proximité les lit comme UNE rangée. On mesure le premier écran, et une
          // liste de 2+ éléments vaut pour un bloc.
          // Un composant RÉPÉTÉ (trois portes de catalogue, trois boutons d'action) est un widget,
          // pas trois paragraphes de héro : dès que deux frères partagent tag+classe, on ne compte pas.
          const inRepetition = (() => {
            let n = el.parentElement;
            while (n && n !== heroHost) {
              const p = n.parentElement;
              if (p) {
                const key = n.tagName + '|' + (n.className || '').toString();
                const sibs = Array.from(p.children).filter(c => c.tagName + '|' + (c.className || '').toString() === key);
                if (sibs.length > 1) return true;
              }
              n = n.parentElement;
            }
            return false;
          })();
          if (inRepetition) return false;
          // 28/10 · troisième fausse alerte : le site est bilingue, donc chaque libellé existe deux fois
          // (bouton > span.fr-only). On ne compte que la feuille la plus profonde, sinon chaque phrase
          // vaut deux blocs. Les fils d'Ariane (nav) ne sont pas de la copie de premier écran.
          if (el !== h1 && el.closest('nav')) return false;
          const own = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
          if (own && Array.from(el.querySelectorAll('*')).some(d => Array.from(d.childNodes).some(n => n.nodeType === 3 && n.textContent.trim()))) return false;
          const cs = getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          const onFirstScreen = rect.top < window.innerHeight && rect.bottom > 0;
          return own && onFirstScreen && cs.display !== 'none' && cs.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
        });
        heroLeaves = leaves.length;
        const lh = parseFloat(getComputedStyle(h1).lineHeight) || 1;
        h1Lines = Math.round(h1.getBoundingClientRect().height / lh);
      }

      // 3 · navigation : hauteur et nombre d'entrées
      const nav = document.querySelector('header, nav');
      const navH = nav ? Math.round(nav.getBoundingClientRect().height) : 0;
      const navLinks = nav ? nav.querySelectorAll('nav a, a').length : 0;

      // 4 · sourcils : combien, pour combien de sections
      const sections = document.querySelectorAll('section').length;
      const eyebrows = document.querySelectorAll('.kicker, .eyebrow, [class*="kicker"], [class*="eyebrow"]').length;

      // 5 · liens morts et liens de contact
      const dead = Array.from(document.querySelectorAll('a[href="#"], a[href=""]')).length;
      const contact = Array.from(document.querySelectorAll('a[href^="tel:"], a[href*="wa.me"], a[href^="mailto:"]'))
        .map(a => a.getAttribute('href'));

      // 6 · images : alternative, chargement différé
      const imgs = Array.from(document.querySelectorAll('img'));
      const noAlt = imgs.filter(i => !i.hasAttribute('alt')).length;
      const lazy = imgs.filter(i => i.getAttribute('loading') === 'lazy').length;

      // 7 · données structurées
      let jsonldBad = 0, jsonldBlocks = 0;
      document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
        jsonldBlocks += 1;
        try { JSON.parse(s.textContent); } catch (e) { jsonldBad += 1; }
      });

      // 8 · échelle typographique
      const sizes = new Set();
      const sizeWhere = {};
      document.querySelectorAll('h1,h2,h3,h4,p,li,a,span,button,small,blockquote,td,th,label,summary,div').forEach(el => {
        const t = txt(el);
        if (!t || el.children.length > 2) return;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        const px = Math.round(parseFloat(cs.fontSize) * 10) / 10;
        sizes.add(px);
        if (!sizeWhere[px]) {
          const cls = (el.className || '').toString().trim().split(/\s+/)[0];
          sizeWhere[px] = el.tagName.toLowerCase() + (cls ? '.' + cls : '');
        }
      });

      // 9 · mouvement : les interdits mécaniques du §13
      const transitionAll = (CSS.match(/transition\s*:\s*all\b/gi) || []).length;
      const reducedMotion = /@media[^{]*prefers-reduced-motion/i.test(CSS);
      const focusVisible = /:focus-visible/.test(CSS);
      const slow = (CSS.match(/transition[^;}]*?(\d{3,})ms/g) || [])
        .map(s => Number((/(\d+)ms/.exec(s) || [0, 0])[1])).filter(ms => ms > 700).length;

      return {
        bi: { en, fr, orphan }, heroLeaves, h1Lines, navH, navLinks, sections, eyebrows,
        dead, contact, imgs: imgs.length, noAlt, lazy, jsonldBlocks, jsonldBad,
        sizes: Array.from(sizes).sort((a, b) => a - b), sizeWhere, transitionAll, reducedMotion, focusVisible, slow,
      };
    });

    if (r.bi.orphan) add('P1', 'BILINGUE', `${r.bi.orphan} élément(s) sans la paire data-en/data-fr`, `${r.bi.en} data-en · ${r.bi.fr} data-fr · §13/§20.8`);
    if (r.h1Lines > 2) add('P2', 'H1', `le h1 fait ${r.h1Lines} lignes en 1440 px`, 'le plafond est 2, §7');
    if (r.navH > 80) add('P2', 'NAV', `la navigation mesure ${r.navH} px de haut`, 'plafond 80 px, §7');
    if (r.heroLeaves > 6) add('P2', 'HERO', `le premier écran porte ${r.heroLeaves} blocs de texte`, 'repère §7 : 4 (sourcil + titre + sous-texte + boutons)');
    if (r.eyebrows > Math.ceil(r.sections / 3)) add('P3', 'EYEBROW', `${r.eyebrows} sourcils pour ${r.sections} sections`, 'plafond ceil(sections/3), §3.4');
    if (r.dead) add('P2', 'LINK', `${r.dead} lien(s) mort(s) (# ou vide)`, '§13');
    if (r.noAlt) add('P2', 'ALT', `${r.noAlt} image(s) sans attribut alt`, '§13');
    if (r.jsonldBad) add('P2', 'JSONLD', `${r.jsonldBad} bloc(s) JSON-LD illisible(s)`, `${r.jsonldBlocks} bloc(s) au total, §13`);
    if (r.sizes.length > 6) add('P3', 'TYPE', `${r.sizes.length} tailles de texte distinctes`, `plafond 6, §5 · ${r.sizes.join(' / ')} px`);
    if (r.transitionAll) add('P2', 'MOTION', `${r.transitionAll} \`transition: all\``, 'interdit, §13');
    if (!r.reducedMotion) add('P2', 'MOTION', 'aucun bloc `prefers-reduced-motion`', '§13');
    if (!r.focusVisible) add('P2', 'FOCUS', 'aucune règle `:focus-visible` dans la feuille', '§13');
    if (r.slow) add('P3', 'MOTION', `${r.slow} transition(s) au-delà de 700 ms`, 'révélations ≤ 700 ms, §13');
    rulesReport = r;
  }

  const file = path.join(OUT, `${label}.png`);
  await page.screenshot({ path: file, fullPage });
  await page.close();
  return { label, width, height, screenshot: file, title: m.title, pageHeight: m.height, heroText: m.heroText };
}

let rulesReport = null;
const shots = [];
shots.push(await audit(1440, 900, 'desktop', true));
shots.push(await audit(390, 844, 'mobile', true));
// le premier écran seul (ce que voit le visiteur avant de défiler)
shots.push(await audit(1440, 900, 'desktop-hero', false));
shots.push(await audit(390, 844, 'mobile-hero', false));

await browser.close();

const count = lvl => findings.filter(f => f.level === lvl).length;
const verdict = count('P1') > 0 || (STRICT && count('P2') > 0) ? 'ROUGE' : (count('P2') > 0 ? 'ORANGE' : 'VERT');

const report = { url, out: OUT, screenshots: shots, findings, rules: rulesReport, totals: { p1: count('P1'), p2: count('P2'), p3: count('P3') }, verdict };
fs.writeFileSync(path.join(OUT, 'rapport.json'), JSON.stringify(report, null, 2));

console.log(`\nVÉRIFICATION DE DESIGN — ${target}`);
console.log(`  ${shots.length} captures : ${shots.map(s => `${s.label} (${s.width}px)`).join(' · ')}`);
for (const s of shots) console.log(`  ${s.label.padEnd(12)} ${String(s.width).padStart(4)}px  ${s.screenshot}`);
console.log('');
if (!findings.length) console.log('  aucun défaut trouvé.');
for (const f of findings) console.log(`  [${f.level}] ${f.code.padEnd(9)} ${f.msg}\n        ${f.where || ''}`);
console.log(`\n  TOTAL ${count('P1')} P1 · ${count('P2')} P2 · ${count('P3')} P3 — ${verdict}`);
console.log(`  rapport : ${path.join(OUT, 'rapport.json')}\n`);
process.exit(verdict === 'ROUGE' ? 1 : 0);
