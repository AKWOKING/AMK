/**
 * test_laligne_page.mjs — rejoue le VRAI JavaScript de `demos/concept-laligne-v1.html` hors navigateur,
 * avec le DOM minuscule du dépôt (`fake_dom.mjs`) : pas de jsdom, pas de dépendance à installer.
 *
 * Ce qu'il protège, dans l'ordre :
 *   suite 0 · le contrat que la PAGE doit au JavaScript : identifiants, numéro unique, deux langues,
 *             données structurées et AEO — **et deux interdits propres à cette page** : aucune
 *             photographie (le cabinet n'en a publié aucune), et le numéro d'inscription à l'Ordre
 *             n'existe QUE dans les données structurées, jamais dans le texte visible ;
 *   suite 1 · la bascule FR|EN : langue, boutons, les douze messages WhatsApp ;
 *   suite 2 · le mouvement : rien ne reste invisible si le script plante ou si l'observateur manque ;
 *   suite 3 · les deux utilitaires du bloc contact : copier le numéro, enregistrer la fiche .vcf.
 *
 * Usage :  node tools/qa/test_laligne_page.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { el, doc, localStorageStub, scriptAfter, waMessage, ok } from "./fake_dom.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PAGE = path.join(ROOT, "demos", "concept-laligne-v1.html");
const html = fs.readFileSync(PAGE, "utf8");

const WA = "https://wa.me/237683651108?text=";
const NUM = "+237683651108";

/* Les DOUZE messages, dans l'ORDRE DU DOCUMENT : en-tête, premier écran, les quatre gestes, les cinq
   formes de visage (chacune son message, avec la forme nommée), les quatre choses qui se règlent en une
   réponse, le contact, le pied, la barre du bas. */
const RDV = ["Bonjour La Ligne Optic, je voudrais venir au cabinet. Comment se passe une visite ?",
             "Hello La Ligne Optic, I would like to come to the practice. How does a visit work?"];
const HRS = ["Bonjour La Ligne Optic, je voudrais passer au cabinet. Quels sont vos horaires aujourd'hui ?",
             "Hello La Ligne Optic, I would like to come to the practice. What are your opening hours today?"];
const MESURE = ["Bonjour La Ligne Optic, je voudrais prendre rendez-vous pour une mesure de ma vue.",
                "Hello La Ligne Optic, I would like to book a sight measurement."];
const SHAPE = [
  ["Bonjour La Ligne Optic, voici la photo de mon visage — je pense avoir un visage ovale. Quelle monture me conseillez-vous ?",
   "Hello La Ligne Optic, here is the photo of my face — I think it is oval. Which frame would you recommend?"],
  ["Bonjour La Ligne Optic, voici la photo de mon visage — je pense avoir un visage rond. Quelle monture me conseillez-vous ?",
   "Hello La Ligne Optic, here is the photo of my face — I think it is round. Which frame would you recommend?"],
  ["Bonjour La Ligne Optic, voici la photo de mon visage — je pense avoir un visage carré. Quelle monture me conseillez-vous ?",
   "Hello La Ligne Optic, here is the photo of my face — I think it is square. Which frame would you recommend?"],
  ["Bonjour La Ligne Optic, voici la photo de mon visage — je pense avoir un visage en cœur. Quelle monture me conseillez-vous ?",
   "Hello La Ligne Optic, here is the photo of my face — I think it is heart-shaped. Which frame would you recommend?"],
  ["Bonjour La Ligne Optic, voici la photo de mon visage — je pense avoir un visage oblong. Quelle monture me conseillez-vous ?",
   "Hello La Ligne Optic, here is the photo of my face — I think it is oblong. Which frame would you recommend?"],
];
const QUESTION = ["Bonjour La Ligne Optic, j'ai une question avant de venir : ",
                  "Hello La Ligne Optic, I have a question before coming: "];
const MESSAGES = [RDV, RDV, MESURE, ...SHAPE, QUESTION, HRS, HRS, HRS];

const langSrc = scriptAfter(html, "LES DEUX LANGUES, LES ADRESSES WHATSAPP, ET CE QUE LA PAGE DIT");
const bootSrc = scriptAfter(html, "Avant le premier rendu");
const revealSrc = scriptAfter(html, "IntersectionObserver, jamais d'écouteur de défilement");

/* Le TEXTE seul : ni les scripts, ni les commentaires, ni (au cas où) un quelconque base64 — une
   recherche naïve sur le fichier entier trouve n'importe quelle suite de lettres dans une image. */
const text = html.replace(/data:image\/[a-z+]+;base64,[^"]+/gi, "«img»")
                 .replace(/<script[\s\S]*?<\/script>/g, "")
                 .replace(/<!--[\s\S]*?-->/g, "");
const ld0 = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
const cabinet = ld0["@graph"].find((g) => g["@type"] === "Optician");
const faq = ld0["@graph"].find((g) => g["@type"] === "FAQPage").mainEntity;

/* ═════════════ 0 · le contrat page ⇄ JavaScript ═════════════ */
console.log("═══ 0 · le contrat page ⇄ JavaScript ═══");

const IDS = ["btn-fr", "btn-en", "say", "copy2", "vcard", "main", "top", "h-hero",
             "services", "visagiste", "passage", "reponses", "questions", "contact"];
const missing = IDS.filter((id) => !html.includes('id="' + id + '"'));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));

const waTags = [...html.matchAll(/<a class="[^"]*\bwa\b[^"]*"[^>]*>/g)].map((m) => m[0]);
ok(`les ${waTags.length} liens WhatsApp portent data-fr ET data-en`,
   waTags.length === 12 && waTags.every((t) => t.includes("data-fr=") && t.includes("data-en=")));

/* L'ADRESSE ÉCRITE DANS LE HTML DOIT ÊTRE CELLE QUE LE JAVASCRIPT FABRIQUERA. */
const badStatic = waTags.filter((t) => {
  const href = (t.match(/href="([^"]+)"/) || [])[1];
  const fr = (t.match(/data-fr="([^"]*)"/) || [])[1];
  return href !== WA + encodeURIComponent(fr);
});
ok("chaque adresse statique = le texte français encodé par le JavaScript (au caractère près)",
   badStatic.length === 0, badStatic.slice(0, 1).join("").slice(0, 120));

ok("un seul numéro WhatsApp dans toute la page : le 683 651 108",
   (html.match(/\+237683651108/g) || []).length >= 3 && !/wa\.me\/(?!237683651108)/.test(html));
ok("un seul numéro appelable, et c'est le même",
   (html.match(/tel:\+237(\d+)/g) || []).every((t) => t === "tel:+237683651108"));

/* ── LA SIGNATURE DE CETTE PAGE : elle est DESSINÉE ─────────────────────────────────────────────── */
ok("aucune photographie : la page n'a pas un seul <img>, et rien en base64",
   !/<img\b/i.test(html) && !/data:image/i.test(html));
const svgs = [...html.matchAll(/<svg\b[^>]*>/g)].map((m) => m[0]);
ok(`les ${svgs.length} dessins sont décoratifs et annoncés comme tels (aria-hidden)`,
   svgs.length >= 12 && svgs.every((s) => s.includes('aria-hidden="true"') && s.includes('focusable="false"')));

const draws = [...html.matchAll(/data-draw="1"/g)].length;
ok(`la ligne du premier écran se TRACE (${draws} traits), et le tracé passe par stroke-dashoffset`,
   draws >= 5 && /@keyframes drawline\{to\{stroke-dashoffset:0\}\}/.test(html) &&
   /html\.js \.draw \[data-draw\]\{stroke-dasharray/.test(html));
ok("les dessins ne s'animent que si le JavaScript est là",
   /html\.js \.draw\.is-on \[data-draw\]\{animation/.test(html) &&
   !/^\.draw \[data-draw\]\{animation/m.test(html));

const radios = [...html.matchAll(/<input class="fh" type="radio" name="face" id="f-[a-z]+"/g)].map((m) => m[0]);
const labels = [...html.matchAll(/<label for="f-[a-z]+">/g)].map((m) => m[0]);
const panels = [...html.matchAll(/<article class="panel p-[a-z]+">/g)].map((m) => m[0]);
ok("cinq formes de visage : cinq boutons radio, cinq étiquettes, cinq panneaux",
   radios.length === 5 && labels.length === 5 && panels.length === 5);
ok("chaque panneau a SON titre et SON dessin",
   (html.match(/<article class="panel[^"]*">[\s\S]*?<\/article>/g) || []).every((p) => (p.match(/<h3>/g) || []).length === 1 && p.includes("<svg")));

/* ── les faits qu'on s'interdit d'inventer ─────────────────────────────────────────────────────── */
ok("les quatre gestes du cabinet sont ceux qu'il annonce, mot pour mot",
   ["Consultation", "Réfraction", "Visagiste", "Conseil"].every((s) => html.includes(s)));
ok("aucun repère inventé : pas un seul lieu nommé que le cabinet n'a pas écrit",
   !/Collège|Kokotier|consulat|face à l'immeuble|Carrefour/i.test(text));
ok("l'adresse écrite est celle que le cabinet publie, et rien de plus",
   /boulevard de la Liberté/.test(html) && !/Rue King Akwa/.test(html));
ok("aucun horaire annoncé (« horaires annoncés », openingHours) : ils sont inconnus",
   !/Horaires annoncés/i.test(text) && !/openingHours/.test(html) &&
   /horaires du jour/.test(text));
ok("aucun prix dans le texte visible", !/\b\d{2,3}\s?\d{3}\s?(FCFA|XAF|fcfa)\b/i.test(text) && !/priceRange/.test(text));
ok("aucune marque de monture nommée (le cabinet n'en publie aucune)",
   !/Ray-Ban|Oakley|Gucci|Tom Ford|Zenni|Essilor|Zeiss|Luxottica|Caddis|Felix Gray/i.test(text));
ok("aucun avis, aucune note dans le schéma (§31 AEO)",
   !/aggregateRating|ratingValue|"Review"/.test(JSON.stringify(ld0)));
ok("le conseil de visagiste est écrit comme du STYLE, jamais comme un examen",
   /conseil de style/i.test(text) && /pas un examen/i.test(text));
ok("le cabinet ne s'attribue aucun acte médical : l'examen des yeux est renvoyé à l'ophtalmologue",
   /reste le travail de votre ophtalmologue/i.test(text));
ok("la photo du visage : ce qu'elle devient est écrit noir sur blanc",
   /reste dans la conversation WhatsApp/i.test(text) && /goes nowhere else/i.test(html));
ok("le numéro d'inscription à l'Ordre n'est PAS dans le texte visible — seulement dans le schéma",
   !/025\/2017/.test(text) && /025\/2017/.test(JSON.stringify(cabinet)));
ok("la titulaire est nommée UNE fois par langue, en pied de page, avec sa qualité",
   (text.match(/Joungo/g) || []).length === 2 &&
   (html.match(/<span class="fr-only" lang="fr">Mme Joungo Line Chantale, opticienne/g) || []).length === 1 &&
   cabinet.founder.name === "Line Chantale Joungo");
ok("aucun lien mort : pas un seul href=\"#\"", !/href="#"/.test(html));
ok("aucun emoji dans le texte (icônes = SVG, jamais des grappes d'emojis)",
   !/[\u{1F300}-\u{1FAFF}\u{2700}-\u{27BF}]/u.test(html));

/* ── différenciation : cette page ne doit pas être la précédente ────────────────────────────────── */
ok("la page ne reprend ni les polices ni les motifs de la vague précédente",
   /Fraunces/.test(html) && /Archivo/.test(html) &&
   !/Anton|Space Mono|Schibsted|Instrument Serif/.test(html) &&
   !/class="ticker"/.test(html) && !/class="rail"/.test(html));

/* ── le mouvement doit pouvoir s'arrêter ───────────────────────────────────────────────────────── */
const calmBlock = (html.match(/@media \(prefers-reduced-motion:reduce\)\{[\s\S]*?\n\}/) || [""])[0];
ok("le bloc `prefers-reduced-motion` arrête les révélations ET le tracé des dessins",
   calmBlock.includes(".rv") && calmBlock.includes("[data-draw]"), calmBlock.slice(0, 60));

/* ── AEO (§31.3) : six questions visibles, six questions dans le schéma, mot pour mot ──────────── */
const details = [...html.matchAll(/<details>[\s\S]*?<\/details>/g)].map((m) => m[0]);
ok(`les ${details.length} accordéons ont UN seul <summary> chacun (§20.11)`,
   details.length === 6 && details.every((d) => (d.match(/<summary[\s>]/g) || []).length === 1));
ok("chaque <summary> porte ses DEUX langues à l'intérieur (jamais la classe de langue sur lui)",
   details.every((d) => {
     const s = (d.match(/<summary>[\s\S]*?<\/summary>/) || [""])[0];
     return s.includes("fr-only") && s.includes("en-only");
   }));

const plain = (x) => x.replace(/<[^>]+>/g, " ").replace(/&nbsp;|\u00a0/g, " ").replace(/\u2019/g, "'").replace(/\s+/g, " ").trim();
const qVisible = [...html.matchAll(/<summary><span><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
const aVisible = [...html.matchAll(/<\/summary>\s*<p><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
ok(`les ${faq.length} questions du schéma sont mot pour mot celles de la page`,
   faq.length === 6 && faq.every((q, i) => plain(q.name) === qVisible[i]), "vues : " + qVisible.length);
ok("les réponses du schéma sont mot pour mot celles de la page",
   faq.every((q, i) => plain(q.acceptedAnswer.text) === aVisible[i]),
   faq.map((q, i) => plain(q.acceptedAnswer.text) === aVisible[i] ? "" : "n°" + (i + 1)).join(" "));
ok("le schéma décrit le cabinet (nom, téléphone, boulevard, ville) — l'écriture « riche en entités » de l'AEO",
   cabinet.telephone === NUM && cabinet.address.addressLocality === "Douala" &&
   cabinet.address.streetAddress === "Boulevard de la Liberté");
ok("la page reste une page de travail : noindex présent, et c'est voulu",
   /<meta name="robots" content="noindex,nofollow">/.test(html));

/* ── la langue, dans le balisage ───────────────────────────────────────────────────────────────── */
const frN = (html.match(/class="[^"]*\bfr-only\b/g) || []).length;
const enN = (html.match(/class="[^"]*\ben-only\b/g) || []).length;
ok(`autant de .fr-only que de .en-only (${frN} / ${enN})`, frN === enN && frN > 60);
const structural = ["summary", "legend", "option", "title", "caption", "details"];
const onStructural = structural.filter((t) => new RegExp("<" + t + "[^>]*class=\"[^\"]*(fr-only|en-only)").test(html));
ok("aucune classe de langue sur un élément STRUCTUREL (§20.11)", onStructural.length === 0, onStructural.join(", "));

/* ═════════════ 1 · la bascule FR | EN ═════════════ */
console.log("\n═══ 1 · la bascule, et ce qu'elle change vraiment ═══");

function run(lang, stored) {
  const store = localStorageStub();
  if (stored) store.setItem("laligne-lang", stored);
  const anchors = MESSAGES.map(([fr]) => {
    const a = el("a");
    a.setAttribute("data-fr", fr);
    a.setAttribute("href", WA + encodeURIComponent(fr));
    return a;
  });
  MESSAGES.forEach(([, en], i) => anchors[i].setAttribute("data-en", en));
  const buttons = { "btn-fr": el("button"), "btn-en": el("button") };
  const say = el("p");
  const registry = Object.assign({ say, "QA:a.wa": anchors }, buttons);
  const document = doc(registry, "fr");
  const win = { matchMedia: () => ({ matches: false }) };
  new Function("document", "window", "localStorage", bootSrc)(document, win, store);
  new Function("document", "window", "localStorage", "navigator", langSrc)(document, win, store, {});
  return { document, anchors, say, buttons, store };
}

let r = run("fr");
ok("départ en français : la page se déclare en français",
   r.document.documentElement.getAttribute("data-lang") === "fr" && r.document.documentElement.lang === "fr");
ok("départ en français : FR est enfoncé, EN ne l'est pas",
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-en"].getAttribute("aria-pressed") === "false");
ok(`départ en français : les ${MESSAGES.length} messages WhatsApp restent français`,
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][0]));

r.buttons["btn-en"].fire("click");
ok("clic sur EN : la page bascule et se déclare en anglais",
   r.document.documentElement.getAttribute("data-lang") === "en" && r.document.documentElement.lang === "en");
ok("clic sur EN : les deux boutons disent leur état (aria-pressed)",
   r.buttons["btn-en"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "false");
ok(`clic sur EN : les ${MESSAGES.length} messages WhatsApp passent en anglais, numéro inchangé`,
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][1]) &&
   r.anchors.every((a) => a.getAttribute("href").indexOf(WA) === 0));
ok("clic sur EN : le choix est retenu (localStorage), pas seulement affiché",
   r.store.getItem("laligne-lang") === "en");
ok("clic sur EN : la région vive l'annonce (role=status)", /English/.test(r.say.textContent));

r = run("fr", "en");
ok("un visiteur qui revient en anglais : la page se rouvre en anglais, sans clic",
   r.document.documentElement.getAttribute("data-lang") === "en" &&
   waMessage(r.anchors[0].getAttribute("href")).indexOf("Hello") === 0);

/* ═════════════ 2 · le mouvement ne doit jamais cacher la page ═════════════ */
console.log("\n═══ 2 · le mouvement, et le droit de ne rien voir ═══");

function runReveal(globals) {
  const items = [el("li"), el("div"), el("section")];
  const document = doc({ "QA:.rv": items, "QA:.draw": [el("svg")] });
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
   live.every((n) => !n.classList.contains("in")) && seen.length === 4);

/* ═════════════ 3 · les deux utilitaires : copier, enregistrer ═════════════ */
console.log("\n═══ 3 · copier le numéro, enregistrer le contact ═══");

function runTools() {
  const copied = [];
  const say = el("p");
  const buttons = { "btn-fr": el("button"), "btn-en": el("button"), copy2: el("button"), vcard: el("button") };
  const document = doc(Object.assign({ say, "QA:a.wa": [] }, buttons));
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
  ok("copier le numéro : le presse-papier reçoit le numéro WhatsApp du cabinet, avec l'indicatif",
     t.copied.length === 1 && t.copied[0] === NUM, "reçu : " + JSON.stringify(t.copied));
  ok("copier le numéro : la page le dit dans la région vive", /683 651 108/.test(t.say.textContent));

  let crashed = false;
  try { t.buttons.vcard.fire("click"); } catch (e) { crashed = true; }
  ok("enregistrer le contact : le clic ne casse rien, même dans un DOM qui n'a ni Blob ni téléchargement",
     crashed === false);
  ok("enregistrer le contact : la page annonce quelque chose au visiteur",
     t.say.textContent.length > 10, "dit : " + t.say.textContent);
  console.log("\n" + (process.exitCode ? "✗ au moins une assertion a échoué" : "✓ toutes les assertions passent"));
}, 0);
