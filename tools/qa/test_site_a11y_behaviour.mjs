#!/usr/bin/env node
/**
 * AMK — test de COMPORTEMENT d'accessibilité du site (site/index.html), lot [27].
 *
 * POURQUOI CE TEST EXISTE. La passe d'accessibilité du 24/09 a corrigé des états qui ne se voient
 * qu'à l'exécution : un menu qui annonce son ouverture (`aria-expanded`), des boutons de langue qui
 * disent lequel est actif (`aria-pressed`), un formulaire qui écrit sa réponse après le clic
 * (`role="status"`). `audit_a11y.py` lit le HTML au repos et ne peut pas les vérifier ; le test au
 * navigateur (`test_voice_widget.mjs`) ne tourne plus dans ce bac à sable, faute de bibliothèques
 * système. Ce test-ci exécute VRAIMENT le JavaScript de la page dans un DOM (jsdom), sans navigateur.
 *
 * Il ne remplace pas le test au navigateur : il vérifie les ÉTATS, pas le rendu.
 *
 * Usage : node tools/qa/test_site_a11y_behaviour.mjs
 *   prérequis (hors dépôt, non persisté) : npm i jsdom  (dans /tmp/amk-video, ou AMK_VIDEO_RUNTIME)
 */
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';

const RT = process.env.AMK_VIDEO_RUNTIME || '/tmp/amk-video';
const require = createRequire(import.meta.url);
const { JSDOM } = require(path.join(RT, 'node_modules', 'jsdom'));

const FILE = process.env.SITE_FILE || '/home/user/AMK/site/index.html';
let fails = 0;
const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails++; };

const html = fs.readFileSync(FILE, 'utf8');
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  url: 'https://amk.example/',
  beforeParse(w) {
    w.matchMedia = w.matchMedia || (() => ({ matches: false, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }));
    w.open = () => ({ closed: false, focus() {} });      // la fenêtre WhatsApp ne s'ouvre pas ici
  },
});
const w = dom.window, d = w.document;

// le script de la page tourne à la fin du corps : on lui laisse un tour de boucle
await new Promise(r => setTimeout(r, 50));

console.log('═══ le menu mobile annonce son état (WCAG 4.1.2) ═══');
const btn = d.getElementById('m-btn'), nav = d.getElementById('m-nav');
ok(!!btn && !!nav, 'le bouton et le panneau existent');
ok(btn.getAttribute('aria-expanded') === 'false', 'au repos : aria-expanded="false"');
ok(btn.getAttribute('aria-controls') === 'm-nav', 'le bouton dit quel élément il commande');
w.openM();
ok(nav.classList.contains('open') && btn.getAttribute('aria-expanded') === 'true', 'après openM() : ouvert ET annoncé');
w.closeM();
ok(!nav.classList.contains('open') && btn.getAttribute('aria-expanded') === 'false', 'après closeM() : fermé ET annoncé');
ok(typeof w.openM === 'function' && typeof w.closeM === 'function', 'les fonctions existent (le onclick du HTML les appelle)');

console.log('\n═══ les boutons de langue disent lequel est actif (WCAG 4.1.2) ═══');
const en = d.getElementById('btn-en'), fr = d.getElementById('btn-fr');
ok(en.getAttribute('aria-pressed') === 'true' && fr.getAttribute('aria-pressed') === 'false', 'au départ : EN actif, annoncé');
w.setLang('fr');
ok(d.documentElement.lang === 'fr', 'setLang("fr") change la langue du document (WCAG 3.1.1)');
ok(fr.getAttribute('aria-pressed') === 'true' && en.getAttribute('aria-pressed') === 'false', 'après bascule : FR actif, annoncé');
w.setLang('en');
ok(fr.getAttribute('aria-pressed') === 'false' && en.getAttribute('aria-pressed') === 'true', 'et retour : EN actif, annoncé');

console.log('\n═══ le formulaire répond après le clic (WCAG 3.3.1) ═══');
const status = d.getElementById('f-status');
ok(!!status && status.getAttribute('role') === 'status' && status.getAttribute('aria-live') === 'polite',
   'une zone vivante existe, vide au repos');
ok(status && status.textContent.trim() === '', 'elle ne dit rien tant que rien ne s\'est passé');
d.getElementById('f-school').value = 'Institut Test';
d.getElementById('f-phone').value = '600000000';
const e = { preventDefault() {} };
w.sendAudit(e);
ok(status.textContent.trim().length > 10, 'après envoi : la zone vivante écrit ce qui vient de se passer');
ok(/WhatsApp/i.test(status.textContent), 'et elle nomme WhatsApp, pas un mot technique');

console.log('\n═══ les étiquettes de champs sont attachées (WCAG 3.3.2) ═══');
for (const id of ['f-school', 'f-phone']) {
  const lab = d.querySelector('label[for="' + id + '"]');
  ok(!!lab && lab.textContent.trim().length > 2, 'le champ #' + id + ' a une étiquette qui lui est LIÉE : « ' + (lab ? lab.textContent.trim() : '') + ' »');
}

console.log('\n═══ les noms accessibles (WCAG 4.1.2) ═══');
// Un nom vient d'un aria-label OU du texte visible — vérifier seulement l'attribut produit de faux
// diagnostics : c'est exactement l'erreur qu'a faite la première version d'audit_a11y.py (deux
// boutons déclarés « sans nom » alors que leur nom était dans un attribut, et un icône-bouton qui
// portait un <span> lisible). On mesure le nom, pas l'attribut.
const nom = el => ((el.getAttribute('aria-label') || '') + ' ' + (el.textContent || '')).trim();
for (const [id, quoi] of [['vx-fab', 'le bouton du widget vocal'], ['vx-mic', 'le bouton micro'], ['m-btn', 'le bouton de menu']]) {
  const el = d.getElementById(id);
  ok(!!el && nom(el).length > 2, quoi + ' porte un nom accessible : « ' + (el ? nom(el).slice(0, 40) : '') + ' »');
}
// et aucun bouton de la page n'est sans nom, à l'exécution
// « EN » et « FR » sont des noms parfaitement valides (deux lettres) : le seul cas fautif est un
// bouton dont le nom est VIDE. Un seuil de longueur invente des fautes.
const sansNom = [...d.querySelectorAll('button')].filter(b => nom(b).trim() === '');
ok(sansNom.length === 0, 'aucun bouton sans nom sur la page (' + d.querySelectorAll('button').length + ' boutons)');

console.log();
if (fails) { console.log('ÉCHECS : ' + fails); process.exit(1); }
console.log('Tout est vert — les états d\'accessibilité du site sont réels à l\'exécution, pas seulement dans le HTML.');
