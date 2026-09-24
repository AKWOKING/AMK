/**
 * test_cinqsens_page.mjs — rejoue le VRAI JavaScript de `demos/concept-cinqsens-v1.html` hors navigateur,
 * avec le DOM minuscule du dépôt (`fake_dom.mjs`) : pas de jsdom, pas de dépendance à installer.
 *
 * Ce qu'il protège, dans l'ordre :
 *   suite 0 · le contrat que la PAGE doit au JavaScript (identifiants, numéros, deux langues, données, AEO) ;
 *   suite 1 · la bascule FR|EN : langue, boutons, les huit messages WhatsApp, texte de remplacement des images ;
 *   suite 2 · le mouvement : rien ne reste invisible si le script plante, et la bande d'arrivage s'arrête
 *             quand le visiteur le demande ;
 *   suite 3 · les deux utilitaires du bloc contact : copier le numéro, enregistrer la fiche .vcf.
 *
 * Usage :  node tools/qa/test_cinqsens_page.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { el, doc, localStorageStub, scriptAfter, waMessage, ok } from "./fake_dom.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PAGE = path.join(ROOT, "demos", "concept-cinqsens-v1.html");
const html = fs.readFileSync(PAGE, "utf8");

const WA = "https://wa.me/237696698136?text=";
const NUM = "+237696698136";

/* Les deux raccourcis de carte servent DEUX fois : au contrôle du balisage (plus bas) et à la
   simulation de la bascule de langue. Ils sont donc déclarés ici, avant tout usage. */
const ORD = ["Bonjour Cinq Sens, voici la photo de mon ordonnance pour des lunettes de vue.",
             "Hello Cinq Sens, here is the photo of my prescription for spectacles."];
const PROTH = ["Bonjour Cinq Sens, je voudrais des informations sur les prothèses oculaires.",
               "Hello Cinq Sens, I would like information about ocular prostheses."];
const langSrc = scriptAfter(html, "LES DEUX LANGUES, LES ADRESSES WHATSAPP, ET CE QUE LA PAGE DIT");
/* L'autre script de langue : celui du `<head>`, qui remet la langue choisie AVANT le premier rendu. Un
   vrai navigateur l'exécute en premier — le test doit faire pareil, sinon « la page se rouvre en
   anglais » ne serait vérifié nulle part. */
const bootSrc = scriptAfter(html, "Avant le premier rendu");
/* Le marqueur doit être UNIQUE : « LE MOUVEMENT » vit aussi dans un commentaire CSS, plus haut — et
   `scriptAfter` remonterait alors jusqu'au script de la langue (piège attrapé le 24/09 sur DM OPTIC). */
const revealSrc = scriptAfter(html, "IntersectionObserver, jamais d'écouteur de défilement");
/* Le TEXTE seul : le base64 des photos contient n'importe quelle suite de lettres, et une recherche
   naïve sur le fichier entier trouve « zEIss » dans une image (piège attrapé le 24/09). */
const text = html.replace(/data:image\/[a-z+]+;base64,[^"]+/gi, "«img»")
                 .replace(/<script[\s\S]*?<\/script>/g, "")
                 .replace(/<!--[\s\S]*?-->/g, "");

/* ═════════════ 0 · le contrat que la page doit au JavaScript ═════════════ */
console.log("═══ 0 · le contrat page ⇄ JavaScript ═══");

const IDS = ["btn-fr", "btn-en", "say", "copy2", "vcard", "main", "top", "h-hero",
             "services", "arrivages", "cabinets", "questions", "contact"];
const missing = IDS.filter((id) => !html.includes('id="' + id + '"'));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));

const waTags = [...html.matchAll(/<a class="[^"]*\bwa\b[^"]*"[^>]*>/g)].map((m) => m[0]);
ok(`les ${waTags.length} liens WhatsApp portent data-fr ET data-en`,
   waTags.length >= 7 && waTags.every((t) => t.includes("data-fr=") && t.includes("data-en=")));

/* L'ADRESSE ÉCRITE DANS LE HTML DOIT ÊTRE CELLE QUE LE JAVASCRIPT FABRIQUERA. */
const badStatic = waTags.filter((t) => {
  const href = (t.match(/href="([^"]+)"/) || [])[1];
  const fr = (t.match(/data-fr="([^"]*)"/) || [])[1];
  return href !== WA + encodeURIComponent(fr);
});
ok("chaque adresse statique = le texte français encodé par le JavaScript (au caractère près)",
   badStatic.length === 0, badStatic.slice(0, 1).join(""));

ok("un seul numéro WhatsApp dans toute la page : le 696 698 136",
   (html.match(/\+237696698136/g) || []).length >= 3 &&
   !/wa\.me\/(?!237696698136)/.test(html));
ok("la seconde ligne 655 163 365 est appelable, mais n'ouvre JAMAIS WhatsApp",
   /tel:\+237655163365/.test(html) && !/wa\.me\/237655163365/.test(html));

const imgs = [...html.matchAll(/<img[^>]*data-alt-fr[^>]*>/g)].map((m) => m[0]);
ok(`les ${imgs.length} images portent data-alt-fr ET data-alt-en`,
   imgs.length === 3 && imgs.every((t) => t.includes("data-alt-en=") && !/alt=""/.test(t)));

const frN = (html.match(/class="[^"]*\bfr-only\b/g) || []).length;
const enN = (html.match(/class="[^"]*\ben-only\b/g) || []).length;
ok(`autant de .fr-only que de .en-only (${frN} / ${enN})`, frN === enN && frN > 50);

const structural = ["summary", "legend", "option", "title", "caption", "details"];
const onStructural = structural.filter((t) => new RegExp("<" + t + "[^>]*class=\"[^\"]*(fr-only|en-only)").test(html));
ok("aucune classe de langue sur un élément STRUCTUREL (§20.11)", onStructural.length === 0, onStructural.join(", "));

/* ── la signature : le rail des cinq sens, la bande d'arrivage, la vitrine ─────────────────────── */
const railCount = (html.match(/<div class="rail" aria-hidden="true"><i><\/i><i><\/i><i><\/i><i><\/i><i><\/i><\/div>/) || []).length;
ok("le rail des cinq sens est là, exactement cinq teintes, et décoratif", railCount === 1);

const ticker = (html.match(/<div class="ticker" aria-hidden="true">[\s\S]*?<\/div>\s*<\/div>/) || [""])[0];
ok("la bande qui défile est décorative (aria-hidden) et son contenu est doublé (défilement sans couture)",
   ticker.includes('aria-hidden="true"') && (ticker.match(/class="tick-set"/g) || []).length === 2);

const rooms = [...html.matchAll(/<article class="room[^"]*">[\s\S]*?<\/article>/g)].map((m) => m[0]);
ok("les deux cabinets sont deux cartes distinctes, chacune avec SON message WhatsApp",
   rooms.length === 2 && rooms[0].includes("Akwa") && rooms[1].includes("Brazzaville") &&
   rooms[0].includes("data-fr=") && rooms[1].includes("data-fr=") &&
   (rooms[0].match(/data-fr="([^"]*)"/) || [])[1] !== (rooms[1].match(/data-fr="([^"]*)"/) || [])[1]);
ok("les repères des deux cabinets sont ceux de leurs propres publications",
   /Collège King Akwa/.test(html) && /Kokotier/.test(html) && /immeuble Michelin/.test(html) &&
   /Flore service/.test(html));
ok("la livraison à domicile et la prothèse oculaire sont annoncées (services revendiqués par le cabinet)",
   /Livraison à domicile/.test(html) && /Prothèses oculaires/.test(html));

/* ── les raccourcis de carte : un message écrit pour le geste qu'ils proposent ──────────────────── */
const shortcuts = [...html.matchAll(/<a class="cardwa wa"[^>]*data-fr="([^"]*)"[^>]*data-en="([^"]*)"/g)]
  .map((m) => [m[1], m[2]]);
ok("les deux raccourcis de carte portent leur propre message (ordonnance en photo, prothèses)",
   shortcuts.length === 2 && shortcuts[0][0] === ORD[0] && shortcuts[1][0] === PROTH[0] &&
   shortcuts[0][1] === ORD[1] && shortcuts[1][1] === PROTH[1]);
ok("le raccourci prothèses ne dit rien de clinique : il demande des informations, c'est tout",
   /informations sur les prothèses/.test(shortcuts[1][0]) &&
   !/mon cas|mon œil|je suis|perdu|accident/i.test(html));

/* ── les faits qu'on s'interdit d'inventer ─────────────────────────────────────────────────────── */
ok("aucun prix dans le texte visible",
   !/\b\d{2,3}\s?\d{3}\s?(FCFA|XAF|fcfa)\b/i.test(text) && !/priceRange/.test(text));
ok("aucune marque de monture nommée dans le texte (le cabinet n'a envoyé aucune liste)",
   !/Ray-Ban|Oakley|Gucci|Tom Ford|Zenni|Essilor|Zeiss|Luxottica/i.test(text));
const ld0 = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
ok("aucun avis, aucune note dans le schéma (§31 AEO)",
   !/aggregateRating|ratingValue|"Review"/.test(JSON.stringify(ld0)));
ok("les horaires sont affichés comme ANNONCÉS et absents du schéma (jamais un fait non vérifié)",
   /Horaires annoncés/.test(html) && !/openingHours/.test(html));
ok("les trois photos sont légendées comme des illustrations", (html.match(/Photo d'illustration/g) || []).length >= 3);
ok("aucun lien mort : pas un seul href=\"#\"", !/href="#"/.test(html));
ok("aucun emoji dans le texte (icônes = SVG, jamais des grappes d'emojis)",
   !/[\u{1F300}-\u{1FAFF}\u{2700}-\u{27BF}]/u.test(html));

/* ── AEO (§31.3) : six questions visibles, six questions dans le schéma, mot pour mot ──────────── */
const details = [...html.matchAll(/<details>[\s\S]*?<\/details>/g)].map((m) => m[0]);
const summaries = details.map((d) => (d.match(/<summary[\s>]/g) || []).length);
ok(`les ${details.length} accordéons ont UN seul <summary> chacun (§20.11)`,
   details.length === 6 && summaries.every((n) => n === 1), "summary par bloc : " + summaries.join(", "));
ok("chaque <summary> porte ses DEUX langues à l'intérieur (jamais la classe de langue sur lui)",
   details.every((d) => {
     const s = (d.match(/<summary>[\s\S]*?<\/summary>/) || [""])[0];
     return s.includes("fr-only") && s.includes("en-only");
   }));

const ld = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
const cabinet = ld["@graph"].find((g) => g["@type"] === "Optician");
ok("le schéma décrit le cabinet (nom, téléphone, rue, ville, deux lieux) — l'écriture « riche en entités » de l'AEO",
   !!cabinet && cabinet.telephone === NUM && cabinet.address.addressLocality === "Douala" &&
   cabinet.address.streetAddress === "Rue King Akwa" && cabinet.location.length === 2);
ok("le schéma porte le nom complet de la raison sociale ET l'enseigne",
   /Référence Optique Médicale Cinq Sens SARL/.test(cabinet.name) && cabinet.alternateName === "Cinq Sens");

ok("le schéma relie la page à leurs comptes RÉELS (blog, X, LinkedIn) et à eux seuls",
   Array.isArray(cabinet.sameAs) && cabinet.sameAs.length === 3 &&
   cabinet.sameAs.every((u) => /^https:\/\/(referenceoptiquemedicale\.blogspot\.com\/|x\.com\/MedicaleOptique|www\.linkedin\.com\/in\/)/.test(u)));

const faq = ld["@graph"].find((g) => g["@type"] === "FAQPage").mainEntity;
const plain = (x) => x.replace(/<[^>]+>/g, " ").replace(/&nbsp;|\u00a0/g, " ").replace(/\u2019/g, "'").replace(/\s+/g, " ").trim();
const qVisible = [...html.matchAll(/<summary><span><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
const aVisible = [...html.matchAll(/<\/summary>\s*<p><span class="fr-only"[^>]*>([\s\S]*?)<\/span>/g)].map((m) => plain(m[1]));
ok(`les ${faq.length} questions du schéma sont mot pour mot celles de la page`,
   faq.length === 6 && faq.every((q, i) => plain(q.name) === qVisible[i]), "vues : " + qVisible.length);
ok("les réponses du schéma sont mot pour mot celles de la page",
   faq.every((q, i) => plain(q.acceptedAnswer.text) === aVisible[i]),
   faq.map((q, i) => plain(q.acceptedAnswer.text) === aVisible[i] ? "" : "n°" + (i + 1)).join(" "));
ok("la page reste une page de travail : noindex présent, et c'est voulu",
   /<meta name="robots" content="noindex,nofollow">/.test(html));

/* ── le mouvement doit pouvoir s'arrêter ───────────────────────────────────────────────────────── */
const calmBlock = (html.match(/@media \(prefers-reduced-motion:reduce\)\{[\s\S]*?\n\}/) || [""])[0];
ok("le bloc `prefers-reduced-motion` arrête la bande, les révélations, la lueur ET le rail",
   [".tick-track", ".rv", ".wash", ".rail i"].every((k) => calmBlock.includes(k)),
   calmBlock.slice(0, 50));
ok("la bande ne bouge que par `transform`",
   /@keyframes tickmove\{[\s\S]*?translate3d/.test(html) && !/\.tick-track\{[^}]*left/.test(html));
ok("la lueur du premier écran est décorative : une seule, vide, et qui ne capte pas le clic",
   (html.match(/<div class="wash" aria-hidden="true"><\/div>/g) || []).length === 1 &&
   /\.wash\{[^}]*pointer-events:none/.test(html));
ok("la lueur et le rail ne s'animent que si le JavaScript est là, et en `transform` seul",
   /html\.js \.wash\{animation:washdrift/.test(html) && /html\.js \.rail i\{/.test(html) &&
   /@keyframes washdrift\{[\s\S]*?translate3d/.test(html));

/* ═════════════ 1 · la bascule FR | EN ═════════════ */
console.log("\n═══ 1 · la bascule, et ce qu'elle change vraiment ═══");

/* Les dix messages, dans l'ORDRE DU DOCUMENT (premier écran, raccourci ordonnance, raccourci prothèses,
   services, arrivages, Akwa, Brazzaville, contact, pied de page, barre du bas). */
const RDV = ["Bonjour Cinq Sens, je voudrais passer au cabinet. Quels sont vos horaires aujourd'hui ?",
             "Hello Cinq Sens, I would like to come to the practice. What are your opening hours today?"];
const MESSAGES = [
  RDV,
  ORD,
  PROTH,
  ["Bonjour Cinq Sens, j'ai une ordonnance à monter. Que faut-il apporter ?",
   "Hello Cinq Sens, I have a prescription to be made up. What should I bring?"],
  ["Bonjour Cinq Sens, je cherche une monture. Voici ce que j'aimerais : ",
   "Hello Cinq Sens, I am looking for a frame. This is what I would like: "],
  ["Bonjour Cinq Sens, je voudrais venir au cabinet d'Akwa. Envoyez-moi la localisation, s'il vous plaît.",
   "Hello Cinq Sens, I would like to come to the Akwa practice. Please send me the location."],
  ["Bonjour Cinq Sens, je voudrais venir à l'agence de Brazzaville. Envoyez-moi la localisation, s'il vous plaît.",
   "Hello Cinq Sens, I would like to come to the Brazzaville branch. Please send me the location."],
  RDV, RDV, RDV,
];
const ALT = ["Une trentaine de montures de couleur vive alignées sur un fond noir mat.",
             "About thirty brightly coloured frames lined up on a matte black background."];

function run(lang, stored) {
  const store = localStorageStub();
  if (stored) store.setItem("cinqsens-lang", stored);
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
  const document = doc(registry, "fr");          /* le balisage part toujours en français… */
  const win = { matchMedia: () => ({ matches: false }) };
  new Function("document", "window", "localStorage", bootSrc)(document, win, store);   /* …puis le <head> */
  new Function("document", "window", "localStorage", "navigator", langSrc)(document, win, store, {});
  return { document, anchors, image, say, buttons, store };
}

let r = run("fr");
ok("départ en français : la page se déclare en français",
   r.document.documentElement.getAttribute("data-lang") === "fr" && r.document.documentElement.lang === "fr");
ok("départ en français : FR est enfoncé, EN ne l'est pas",
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-en"].getAttribute("aria-pressed") === "false");
ok(`départ en français : les ${MESSAGES.length} messages WhatsApp restent français`,
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][0]));
ok("départ en français : le texte de remplacement des images est français",
   r.image.getAttribute("alt") === ALT[0]);

r.buttons["btn-en"].fire("click");
ok("clic sur EN : la page bascule et se déclare en anglais",
   r.document.documentElement.getAttribute("data-lang") === "en" && r.document.documentElement.lang === "en");
ok("clic sur EN : les deux boutons disent leur état (aria-pressed)",
   r.buttons["btn-en"].getAttribute("aria-pressed") === "true" &&
   r.buttons["btn-fr"].getAttribute("aria-pressed") === "false");
ok(`clic sur EN : les ${MESSAGES.length} messages WhatsApp passent en anglais, numéro inchangé`,
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][1]) &&
   r.anchors.every((a) => a.getAttribute("href").indexOf(WA) === 0));
ok("clic sur EN : le texte de remplacement de l'image passe en anglais",
   r.image.getAttribute("alt") === ALT[1]);
ok("clic sur EN : le choix est retenu (localStorage), pas seulement affiché",
   r.store.getItem("cinqsens-lang") === "en");
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
  ok("copier le numéro : le presse-papier reçoit le numéro WhatsApp du cabinet, avec l'indicatif",
     t.copied.length === 1 && t.copied[0] === NUM, "reçu : " + JSON.stringify(t.copied));
  ok("copier le numéro : la page le dit dans la région vive", /696 698 136/.test(t.say.textContent));

  let crashed = false;
  try { t.buttons.vcard.fire("click"); } catch (e) { crashed = true; }
  ok("enregistrer le contact : le clic ne casse rien, même dans un DOM qui n'a ni Blob ni téléchargement",
     crashed === false);
  ok("enregistrer le contact : la page annonce quelque chose au visiteur",
     t.say.textContent.length > 10, "dit : " + t.say.textContent);
  console.log("\n" + (process.exitCode ? "✗ au moins une assertion a échoué" : "✓ toutes les assertions passent"));
}, 0);
