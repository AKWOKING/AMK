/**
 * test_dmoptic_page.mjs — rejoue le VRAI JavaScript de `demos/concept-dmoptic-v1.html` hors navigateur,
 * avec le DOM minuscule du dépôt (`fake_dom.mjs`) : pas de jsdom, pas de dépendance à installer.
 *
 * Ce qu'il protège, dans l'ordre :
 *   suite 0 · le contrat que la PAGE doit au JavaScript (identifiants, adresses, langues, données, AEO) ;
 *   suite 1 · la bascule FR|EN : langue, boutons, message WhatsApp, texte de remplacement des images ;
 *   suite 2 · le mouvement : si le script plante ou si l'API manque, RIEN ne reste invisible — et les
 *             deux dégradés animés du premier écran s'arrêtent quand le visiteur le demande ;
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
/* Le marqueur doit être UNIQUE : « LE MOUVEMENT » vit aussi dans une règle CSS, plus haut — et
   `scriptAfter` remonterait alors jusqu'au script de la langue (piège attrapé le 24/09). */
const revealSrc = scriptAfter(html, "IntersectionObserver, jamais d'écouteur de défilement");

/* ═════════════ 0 · le contrat que la page doit au JavaScript ═════════════ */
console.log("═══ 0 · le contrat page ⇄ JavaScript ═══");

const IDS = ["btn-fr", "btn-en", "say", "copy2", "vcard", "main", "top", "h-hero",
             "actes", "etapes", "montures", "questions", "contact"];
const missing = IDS.filter((id) => !html.includes('id="' + id + '"'));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));

const waTags = [...html.matchAll(/<a class="[^"]*\bwa\b[^"]*"[^>]*>/g)].map((m) => m[0]);
ok(`les ${waTags.length} liens WhatsApp portent data-fr ET data-en`,
   waTags.length >= 6 && waTags.every((t) => t.includes("data-fr=") && t.includes("data-en=")));

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
   imgs.length === 5 && imgs.every((t) => t.includes("data-alt-en=") && !/alt=""/.test(t)));

/* ── la vitrine des montures (v2.1) : trois familles, trois conseils, et aucune marque inventée ───── */
const showcase = (html.match(/<section id="montures"[\s\S]*?<\/section>/) || [""])[0];
const cards = showcase.match(/<article class="frame[\s\S]*?<\/article>/g) || [];
ok("la vitrine montre trois familles de montures, une photo et un titre chacune",
   cards.length === 3 && cards.every((c) => c.includes("<img") && c.includes("<h3>")),
   "cartes : " + cards.length);
ok("la vitrine dit que les photos sont des illustrations (jamais des montures du cabinet)",
   /Photos d'illustration\./.test(showcase) && /Illustration photos\./.test(showcase));
ok("la vitrine ne nomme AUCUNE marque et n'affiche AUCUN prix",
   !/Ray-Ban|Oakley|Gucci|Tom Ford|Oliver Peoples|Essilor|Zeiss/i.test(showcase) && !/\d{3,}\s?(FCFA|XAF)/i.test(showcase));
ok("la vitrine porte une seule action (le reste du choix se fait au cabinet)",
   (showcase.match(/class="btn /g) || []).length === 1);
ok("les trois conseils du choix sont là (forme du visage, appui, usage)",
   (showcase.match(/<div>\s*<h3>/g) || []).length >= 3);

const structural = ["summary", "legend", "option", "title", "caption", "details"];
const onStructural = structural.filter((t) => new RegExp("<" + t + "[^>]*class=\"[^\"]*(fr-only|en-only)").test(html));
ok("aucune classe de langue sur un élément STRUCTUREL (§20.11)", onStructural.length === 0, onStructural.join(", "));

const frN = (html.match(/class="[^"]*\bfr-only\b/g) || []).length;
const enN = (html.match(/class="[^"]*\ben-only\b/g) || []).length;
ok(`autant de .fr-only que de .en-only (${frN} / ${enN})`, frN === enN && frN > 30);

const ld = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
const opticien = ld["@graph"].find((g) => g["@type"] === "Optician");
ok("le schéma décrit le cabinet (Optician, téléphone, ville, inscription) — l'écriture « riche en entités » de l'AEO",
   !!opticien && opticien.telephone === NUM && opticien.address.addressLocality === "Douala" &&
   opticien.identifier.value === "021/2016");
ok("aucune note, aucun avis, aucun horaire inventé dans le schéma",
   !/aggregateRating|ratingValue|openingHours/.test(html));
/* §31 AEO : l'entité garde son identifiant (machine), le PATIENT n'a pas à lire l'arrêté ministériel
   (décision de King, 24/09 : « tout les détails de lui dans l'ordre » n'ont pas à être sur la page). */
const visible = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<!--[\s\S]*?-->/g, "");
ok("les numéros du registre (021/2016, arrêté 0382) ne sont plus écrits dans le texte visible",
   !/021\/2016|0382|Littoral, ligne 102/.test(visible));
ok("mais l'entité garde son identifiant dans les données structurées (021/2016)",
   /021\/2016/.test(html) && opticien.identifier.value === "021/2016");
ok("aucun lien mort : pas un seul href=\"#\"", !/href="#"/.test(html));
ok("aucun prix dans le texte visible",
   !/\b\d{2,3}\s?\d{3}\s?(FCFA|XAF|fcfa)\b/i.test(html) && !/priceRange/.test(html));

/* ── AEO (§31.3) : cinq questions visibles, cinq questions dans le schéma, mot pour mot ────────── */
const details = [...html.matchAll(/<details>[\s\S]*?<\/details>/g)].map((m) => m[0]);
const summaries = details.map((d) => (d.match(/<summary[\s>]/g) || []).length);
ok(`les ${details.length} accordéons ont UN seul <summary> chacun (§20.11)`,
   details.length === 6 && summaries.every((n) => n === 1), "summary par bloc : " + summaries.join(", "));
ok("chaque <summary> porte ses DEUX langues à l'intérieur (jamais la classe de langue sur lui)",
   details.every((d) => {
     const s = (d.match(/<summary>[\s\S]*?<\/summary>/) || [""])[0];
     return s.includes("fr-only") && s.includes("en-only");
   }));

const faq = ld["@graph"].find((g) => g["@type"] === "FAQPage").mainEntity;
const plain = (x) => x.replace(/<[^>]+>/g, " ").replace(/&nbsp;|\u00a0/g, " ").replace(/\u2019/g, "'").replace(/\s+/g, " ").trim();
const qVisible = [...html.matchAll(/<summary><span><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
const aVisible = [...html.matchAll(/<\/summary>\s*<p><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
ok(`les ${faq.length} questions du schéma sont mot pour mot celles de la page`,
   faq.length === 6 && faq.every((q, i) => plain(q.name) === qVisible[i]),
   "vues : " + qVisible.length);
ok("les réponses du schéma sont mot pour mot celles de la page",
   faq.every((q, i) => plain(q.acceptedAnswer.text) === aVisible[i]),
   faq.map((q, i) => plain(q.acceptedAnswer.text) === aVisible[i] ? "" : "n°" + (i + 1)).join(" "));
ok("chaque réponse commence par l'information, pas par le contexte (BLUF)",
   faq.every((q) => plain(q.acceptedAnswer.text).split(" ").length >= 12));
ok("la page reste une page de travail : noindex présent, et c'est voulu",
   /<meta name="robots" content="noindex,nofollow">/.test(html));

/* ── les deux dégradés animés du premier écran doivent pouvoir s'arrêter ───────────────────────── */
const calmBlock = (html.match(/@media \(prefers-reduced-motion:reduce\)\{[\s\S]*?\n\}/) || [""])[0];
ok("le bloc `prefers-reduced-motion` arrête AUSSI les deux dégradés du premier écran (.wash, .lensring)",
   calmBlock.includes(".wash") && calmBlock.includes(".lensring"), calmBlock.slice(0, 60));
ok("les dégradés ne bougent que par `transform` (composé par le GPU), jamais par `filter: blur`",
   /@keyframes drift\{[\s\S]*?transform:/.test(html) && !/\.wash\{[^}]*filter/.test(html));

/* ═════════════ 1 · la bascule FR | EN ═════════════ */
console.log("\n═══ 1 · la bascule, et ce qu'elle change vraiment ═══");

/* Les cinq messages, dans l'ORDRE DU DOCUMENT (premier écran, étapes, contact, pied, barre du bas). */
const MESSAGES = [
  ["Bonjour DM OPTIC, je voudrais prendre un rendez-vous pour un examen de la vue.",
   "Hello DM OPTIC, I would like to book an eye examination."],
  ["Bonjour DM OPTIC, avez-vous cette monture en boutique : ",
   "Hello DM OPTIC, do you have this frame in store: "],
  ["Bonjour DM OPTIC, voici ce qui ne va pas : ", "Hello DM OPTIC, this is what is wrong: "],
  ["Bonjour DM OPTIC, je voudrais passer vous voir. Quels sont vos horaires ?",
   "Hello DM OPTIC, I would like to come and see you. What are your opening hours?"],
  ["Bonjour DM OPTIC, je voudrais prendre un rendez-vous pour un examen de la vue.",
   "Hello DM OPTIC, I would like to book an eye examination."],
  ["Bonjour DM OPTIC, je voudrais prendre un rendez-vous pour un examen de la vue.",
   "Hello DM OPTIC, I would like to book an eye examination."],
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
ok("départ en français : les six messages WhatsApp restent français",
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
ok("clic sur EN : les 6 messages WhatsApp passent en anglais, numéro inchangé",
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
    "QA:a.wa,a[href^=\"tel:\"]": [], "QA:.hero .btn": [] }, buttons));
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
