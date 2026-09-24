/**
 * test_dmoptic_page.mjs — rejoue le VRAI JavaScript de `demos/concept-dmoptic-v1.html` hors navigateur,
 * avec le DOM minuscule du dépôt (`fake_dom.mjs`) : pas de jsdom, pas de dépendance à installer.
 *
 * Ce qu'il protège, dans l'ordre :
 *   suite 0 · le contrat que la PAGE doit au JavaScript (identifiants, adresses, langues, données) ;
 *   suite 1 · la bascule FR|EN : langue, boutons, message WhatsApp, texte de remplacement des images ;
 *   suite 2 · le mouvement : si le script plante ou si l'API manque, RIEN ne reste invisible ;
 *   suite 3 · les deux utilitaires du bloc contact : copier le numéro, enregistrer la fiche .vcf.
 *
 * Ce que ça n'est pas : un test de rendu. La mise en page et l'œil restent à King (le bac n'a pas de
 * navigateur — c'est écrit tel quel dans les notes de livraison).
 *
 * Usage :  node tools/qa/test_dmoptic_page.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { el, doc, localStorageStub, scriptAfter, waMessage, ok } from "./fake_dom.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PAGE = path.join(ROOT, "demos", "concept-dmoptic-v1.html");
const html = fs.readFileSync(PAGE, "utf8");

const WA = "https://wa.me/237656122239?text=";
const NUM = "+237656122239";
const langSrc = scriptAfter(html, "LES DEUX LANGUES, LES ADRESSES WHATSAPP, ET CE QUE LA PAGE DIT");
/* Le marqueur doit être UNIQUE : « LE MOUVEMENT » vit aussi dans une règle CSS, plus haut —
   et `scriptAfter` remontait alors jusqu'au script de la langue (piège attrapé en écrivant ceci). */
const revealSrc = scriptAfter(html, "IntersectionObserver, jamais d'écouteur de défilement");

/* ═════════════ 0 · le contrat que la page doit au JavaScript ═════════════ */
console.log("═══ 0 · le contrat page ⇄ JavaScript ═══");

const IDS = ["btn-fr", "btn-en", "say", "copy2", "vcard", "main", "top", "h-hero",
             "constat", "actes", "titulaire", "completer", "contact"];
const missing = IDS.filter((id) => !html.includes('id="' + id + '"'));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));

const waTags = [...html.matchAll(/<a class="[^"]*\bwa\b[^"]*"[^>]*>/g)].map((m) => m[0]);
ok(`les ${waTags.length} liens WhatsApp portent data-fr ET data-en`,
   waTags.length >= 4 && waTags.every((t) => t.includes("data-fr=") && t.includes("data-en=")));

/* L'ADRESSE ÉCRITE DANS LE HTML DOIT ÊTRE CELLE QUE LE JAVASCRIPT FABRIQUERA.
   C'est ici que se cache l'écart entre `quote()` de Python et `encodeURIComponent()`. */
const badStatic = waTags.filter((t) => {
  const href = (t.match(/href="([^"]+)"/) || [])[1];
  const fr = (t.match(/data-fr="([^"]*)"/) || [])[1];
  return href !== WA + encodeURIComponent(fr);
});
ok("chaque adresse statique = le texte français encodé par le JavaScript (au caractère près)",
   badStatic.length === 0, badStatic.slice(0, 1).join(""));

ok("un seul numéro dans toute la page : celui du cabinet, avec l'indicatif",
   (html.match(/\+237656122239/g) || []).length >= 3 &&
   !/wa\.me\/(?!237656122239)/.test(html) && !/tel:\+(?!237656122239)/.test(html));

const imgs = [...html.matchAll(/<img[^>]*data-alt-fr[^>]*>/g)].map((m) => m[0]);
ok(`les ${imgs.length} images portent data-alt-fr ET data-alt-en`,
   imgs.length === 2 && imgs.every((t) => t.includes("data-alt-en=") && !/alt=""/.test(t)));

const structural = ["summary", "legend", "option", "title", "caption", "details"];
const onStructural = structural.filter((t) => new RegExp("<" + t + "[^>]*class=\"[^\"]*(fr-only|en-only)").test(html));
ok("aucune classe de langue sur un élément STRUCTUREL (§20.11)", onStructural.length === 0, onStructural.join(", "));

const frN = (html.match(/class="[^"]*\bfr-only\b/g) || []).length;
const enN = (html.match(/class="[^"]*\ben-only\b/g) || []).length;
ok(`autant de .fr-only que de .en-only (${frN} / ${enN})`, frN === enN && frN > 30);

const ld = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
const opticien = ld["@graph"].find((g) => g["@type"] === "Optician");
ok("le schéma décrit bien le cabinet (type Optician, téléphone, ville, inscription)",
   !!opticien && opticien.telephone === NUM && opticien.address.addressLocality === "Douala" &&
   opticien.identifier.value === "021/2016");
ok("aucune note, aucun avis, aucun horaire inventé dans le schéma",
   !/aggregateRating|ratingValue|openingHours/.test(html));
ok("aucun lien mort : pas un seul href=\"#\"", !/href="#"/.test(html));
ok("aucun prix dans le texte visible",
   !/\b\d{2,3}\s?\d{3}\s?(FCFA|XAF|fcfa)\b/i.test(html) && !/priceRange/.test(html));

/* ═════════════ 1 · la bascule FR | EN ═════════════ */
console.log("\n═══ 1 · la bascule, et ce qu'elle change vraiment ═══");

const MESSAGES = [
  ["Bonjour DM OPTIC, je cherche un opticien à Douala.", "Hello DM OPTIC, I am looking for an optician in Douala."],
  ["Bonjour DM OPTIC, je voudrais un renseignement avant de passer.", "Hello DM OPTIC, I would like some information before coming."],
  ["Bonjour DM OPTIC, je voudrais passer vous voir. Quels sont vos horaires ?", "Hello DM OPTIC, I would like to come and see you. What are your opening hours?"],
];
const ALT = ["Une paire de lunettes de vue posée sur une surface claire, lumière douce.",
             "A pair of prescription glasses resting on a pale surface in soft light."];

function run(lang, stored) {
  const store = localStorageStub();
  if (stored) store.setItem("dmoptic-lang", stored);
  const anchors = MESSAGES.map(([fr]) => {
    const a = el("a");
    a.setAttribute("data-fr", fr);
    a.setAttribute("href", WA + encodeURIComponent(fr));
    return a;
  });
  MESSAGES.forEach(([, en], i) => anchors[i].setAttribute("data-en", en));
  const image = el("img");
  image.setAttribute("data-alt-fr", ALT[0]);
  image.setAttribute("data-alt-en", ALT[1]);
  const buttons = { "btn-fr": el("button"), "btn-en": el("button") };
  const say = el("p");
  const registry = Object.assign({
    say,
    "QA:a.wa": anchors,
    "QA:img[data-alt-fr]": [image],
    "QA:[data-say-fr]": [],
    "QA:a.wa,a[href^=\"tel:\"]": anchors,
    "QA:.hero .btn": [],
  }, buttons);
  const document = doc(registry, lang);
  new Function("document", "window", "localStorage", "navigator", langSrc)(
    document, { matchMedia: () => ({ matches: false }) }, store, {});
  return { document, anchors, image, say, buttons, store };
}

let r = run("fr");
ok("départ en français : la page se déclare en français",
   r.document.documentElement.getAttribute("data-lang") === "fr" && r.document.documentElement.lang === "fr");
ok("départ en français : FR est enfoncé, EN ne l'est pas",
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-en"].getAttribute("aria-pressed") === "false");
ok("départ en français : les messages WhatsApp restent français",
   r.anchors.every((a) => waMessage(a.getAttribute("href")).indexOf("Bonjour DM OPTIC") === 0) &&
   waMessage(r.anchors[2].getAttribute("href")) === MESSAGES[2][0]);
ok("départ en français : le texte de remplacement des images est français",
   r.image.getAttribute("alt") === ALT[0]);

r.buttons["btn-en"].fire("click");
ok("clic sur EN : la page bascule et se déclare en anglais",
   r.document.documentElement.getAttribute("data-lang") === "en" && r.document.documentElement.lang === "en");
ok("clic sur EN : les deux boutons disent leur état (aria-pressed)",
   r.buttons["btn-en"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "false");
ok("clic sur EN : les 3 messages WhatsApp passent en anglais, numéro inchangé",
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][1]) &&
   r.anchors.every((a) => a.getAttribute("href").indexOf(WA) === 0));
ok("clic sur EN : le texte de remplacement de l'image passe en anglais",
   r.image.getAttribute("alt") === ALT[1]);
ok("clic sur EN : le choix est retenu (localStorage), pas seulement affiché",
   r.store.getItem("dmoptic-lang") === "en");
ok("clic sur EN : la région vive l'annonce (role=status)", /English/.test(r.say.textContent));

r = run("fr", "en");
ok("un visiteur qui revient en anglais : la page se rouvre en anglais, sans clic",
   r.document.documentElement.getAttribute("data-lang") === "en" &&
   waMessage(r.anchors[0].getAttribute("href")).indexOf("Hello") === 0);

/* ═════════════ 2 · le mouvement ne doit jamais cacher la page ═════════════ */
console.log("\n═══ 2 · le mouvement, et le droit de ne rien voir ═══");

function runReveal(globals) {
  const items = [el("li"), el("div"), el("section")];
  const document = doc({ "QA:.rv": items });
  const fn = new Function("document", "window", "IntersectionObserver", revealSrc);
  fn(document, globals.window, globals.IO);
  return items;
}

const noApi = runReveal({ window: { matchMedia: () => ({ matches: false }) }, IO: undefined });
ok("sans IntersectionObserver : les 3 blocs sont affichés", noApi.every((n) => n.classList.contains("in")));

const crash = runReveal({ window: undefined, IO: undefined });
ok("si le script de mouvement plante : les 3 blocs sont affichés quand même",
   crash.every((n) => n.classList.contains("in")));

let seen = [];
class IO {
  constructor(cb) { this.cb = cb; }
  observe(node) { seen.push(node); }
  unobserve() {}
}

const calm = runReveal({ window: { matchMedia: () => ({ matches: true }), IntersectionObserver: IO }, IO });
ok("mouvement réduit demandé par le visiteur : affichage immédiat, aucune animation",
   calm.every((n) => n.classList.contains("in")));

seen = [];
const live = runReveal({ window: { matchMedia: () => ({ matches: false }), IntersectionObserver: IO }, IO });
ok("sinon : les blocs sont confiés à l'observateur, pas allumés d'avance",
   live.every((n) => !n.classList.contains("in")) && seen.length === 3);

/* ═════════════ 3 · les deux utilitaires : copier, enregistrer ═════════════ */
console.log("\n═══ 3 · copier le numéro, enregistrer le contact ═══");

function runTools() {
  const copied = [];
  const say = el("p");
  const buttons = { "btn-fr": el("button"), "btn-en": el("button"), copy2: el("button"), vcard: el("button") };
  const document = doc(Object.assign({ say, "QA:a.wa": [], "QA:img[data-alt-fr]": [],
    "QA:[data-say-fr]": [], "QA:a.wa,a[href^=\"tel:\"]": [], "QA:.hero .btn": [] }, buttons));
  document.createElement = (tag) => el(tag);
  const body = el("body");
  body.appendChild = () => {}; body.removeChild = () => {};
  document.body = body;
  const navigator = { clipboard: { writeText: (t) => { copied.push(t); return Promise.resolve(); } } };
  new Function("document", "window", "localStorage", "navigator", langSrc)(
    document, { matchMedia: () => ({ matches: false }) }, localStorageStub(), navigator);
  return { buttons, say, copied };
}

const t = runTools();
t.buttons.copy2.fire("click");
setTimeout(() => {
  ok("copier le numéro : le presse-papier reçoit le numéro du cabinet, avec l'indicatif",
     t.copied.length === 1 && t.copied[0] === NUM, "reçu : " + JSON.stringify(t.copied));
  ok("copier le numéro : la page le dit dans la région vive", /656 122 239/.test(t.say.textContent));

  let crashed = false;
  try { t.buttons.vcard.fire("click"); } catch (e) { crashed = true; }
  ok("enregistrer le contact : le clic ne casse rien, même dans un DOM qui n'a ni Blob ni téléchargement",
     crashed === false);
  ok("enregistrer le contact : la page annonce quelque chose au visiteur",
     t.say.textContent.length > 10, "dit : " + t.say.textContent);
  console.log("\n" + (process.exitCode ? "✗ au moins une assertion a échoué" : "✓ toutes les assertions passent"));
}, 0);
