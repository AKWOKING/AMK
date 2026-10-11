/**
 * test_amkcm_lang.mjs — la bascule FR|EN de `site/index.html`, rejouée hors navigateur (pas de dépendance).
 *
 * Ce qu'il protège (ajouté le 08/10/2026, passe SEO « langue par défaut = FR dans le HTML statique ») :
 *   1 · le vrai `setLang` de la page, extrait du fichier, est exécuté sur CHAQUE élément `data-en|data-fr` ;
 *   2 · après setLang("en") puis setLang("fr"), chaque élément porte exactement le texte de son attribut ;
 *   3 · les placeholders (`data-ph-*`) et les alt (`data-alt-*`) suivent la langue ;
 *   4 · le bouton « Parler à ce site » ne porte PLUS data-en (sinon le clic EN|FR efface l'icône micro) ;
 *   5 · l'état statique : <html lang="fr">, FR « on » et aria-pressed vrai, EN faux (desktop et mobile).
 * Limite assumée : ce n'est pas un navigateur. Il prouve la logique des attributs, pas le rendu.
 *
 * Usage :  node tools/qa/test_amkcm_lang.mjs [site/index.html]
 */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const FILE = process.argv[2] || path.join(ROOT, "site", "index.html");
const html = fs.readFileSync(FILE, "utf8").replace(/\r\n/g, "\n");
let fails = 0;
const ok = (label, cond, detail = "") => { console.log(`${cond ? "ok  " : "FAIL"} ${label}${cond ? "" : "  → " + detail}`); if (!cond) fails++; };
const unesc = (s) => s.replace(/&nbsp;/g, "\u00a0").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">");

/* éléments simulés : une entrée par balise ouvrante portant l'attribut cherché */
function collect(attr) {
  const out = [];
  /* un « > » peut se trouver DANS une valeur d'attribut (data-fr="<b>Gratuit.</b> …") : on lit les valeurs entre guillemets */
  const re = new RegExp(`<([a-z0-9]+)((?:[^>"]|"[^"]*")*\\s${attr}="[^"]*"(?:[^>"]|"[^"]*")*)>`, "g");
  let m;
  while ((m = re.exec(html))) {
    const attrs = {};
    for (const a of m[2].matchAll(/\s([a-z\-]+)="([^"]*)"/g)) attrs[a[1]] = unesc(a[2]);
    out.push({ tag: m[1], attrs, innerHTML: null, classList: { toggle() {} }, getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }, setAttribute(k, v) { this.attrs[k] = v; } });
  }
  return out;
}
const dataEn = collect("data-en"), phEls = collect("data-ph-en"), altEls = collect("data-alt-en");

const src = html.slice(html.indexOf("function setLang(l)"));
const fn = src.slice(0, src.indexOf("\ndocument.addEventListener(\"keydown\""));
const store = {};
const sel = { "[data-en]": dataEn, "[data-ph-en]": phEls, "[data-alt-en]": altEls };
const buttons = {};
const ctx = {
  document: { documentElement: { lang: "fr" }, querySelectorAll: (q) => sel[q] || [], getElementById: (id) => (buttons[id] ||= { classList: { toggle() {} }, setAttribute() {} }) },
  localStorage: { setItem: (k, v) => (store[k] = v) }, wireWaLinks() {},
};
vm.createContext(ctx);
vm.runInContext(fn, ctx);

ok("setLang trouvé dans la page", typeof ctx.setLang === "function");
ok("éléments bilingues trouvés", dataEn.length > 200, String(dataEn.length));

for (const lang of ["en", "fr", "en", "fr"]) {
  ctx.setLang(lang);
  const bad = dataEn.filter((e) => e.innerHTML !== e.attrs["data-" + lang]);
  ok(`setLang("${lang}") : ${dataEn.length} textes = leur attribut`, bad.length === 0 && ctx.document.documentElement.lang === lang, bad.slice(0, 2).map((b) => b.tag).join(","));
  ok(`setLang("${lang}") : ${phEls.length} placeholder(s) et ${altEls.length} alt suivent`,
     phEls.every((e) => e.attrs.placeholder === e.attrs["data-ph-" + lang]) && altEls.every((e) => e.attrs.alt === e.attrs["data-alt-" + lang]));
}
ok("préférence mémorisée (amk-lang)", store["amk-lang"] === "fr");

const fab = html.match(/<button class="vx-fab"[^>]*>/)[0];
ok("bouton « Parler à ce site » sans data-en (l'icône survit à la bascule)", !/data-en/.test(fab), fab);

/* état statique du HTML servi */
ok('<html lang="fr">', /<html lang="fr">/.test(html));
for (const id of ["btn-fr", "btn-fr-m"]) { const t = html.match(new RegExp(`<button id="${id}"[^>]*>`))[0]; ok(`${id} actif`, /class="on"/.test(t) && /aria-pressed="true"/.test(t), t); }
for (const id of ["btn-en", "btn-en-m"]) { const t = html.match(new RegExp(`<button id="${id}"[^>]*>`))[0]; ok(`${id} inactif`, !/class="on"/.test(t) && /aria-pressed="false"/.test(t), t); }

console.log(fails ? `\n${fails} échec(s)` : "\ntout est vert");
process.exit(fails ? 1 : 0);
