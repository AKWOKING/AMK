/**
 * test_cavisa_page.mjs — rejoue le VRAI JavaScript de `demos/concept-cavisa-v1.html` hors navigateur,
 * avec le DOM minuscule du dépôt (`fake_dom.mjs`) : pas de jsdom, pas de dépendance à installer.
 *
 * Pourquoi ce fichier existe : les deux défauts qui nous ont coûté le plus cher ne se voient PAS en
 * lisant la page — une FAQ vide en anglais (19/09 : une classe de langue posée sur `<summary>`, §20.11)
 * et un lien WhatsApp qui ne parlait pas la langue du visiteur. Les deux se reproduisent ici.
 *
 * Ce qu'il protège, dans l'ordre :
 *   suite 0 · le contrat que la PAGE doit au JavaScript (identifiants, attributs, adresses statiques) ;
 *   suite 1 · la bascule FR|EN : langue, boutons, message WhatsApp, texte de remplacement des images ;
 *   suite 2 · le mouvement : si le script plante ou si l'API manque, RIEN ne reste invisible.
 *
 * Ce que ça n'est pas : un test de rendu. La mise en page et l'œil restent à King (le bac n'a pas de
 * navigateur — écrit tel quel dans les notes de livraison).
 *
 * Usage :  node tools/qa/test_cavisa_page.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { el, doc, localStorageStub, scriptAfter, waMessage, ok } from "./fake_dom.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PAGE = path.join(ROOT, "demos", "concept-cavisa-v1.html");
const html = fs.readFileSync(PAGE, "utf8");

const WA = "https://wa.me/237699959052?text=";
const langSrc = scriptAfter(html, "LES DEUX LANGUES, LES ADRESSES WHATSAPP");
const revealSrc = scriptAfter(html, "LE MOUVEMENT");

/* ═════════════ 0 · le contrat que la page doit au JavaScript ═════════════ */
console.log("═══ 0 · le contrat page ⇄ JavaScript ═══");

const IDS = ["btn-fr", "btn-en", "say", "contenu", "top", "h-hero", "montures", "parcours",
             "ordonnance", "sans-surprise", "completer", "questions", "contact"];
const missing = IDS.filter((id) => !html.includes('id="' + id + '"'));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));

const waTags = [...html.matchAll(/<a class="[^"]*\bwa\b[^"]*"[^>]*>/g)].map((m) => m[0]);
ok(`les ${waTags.length} liens WhatsApp portent data-fr ET data-en`,
   waTags.length >= 9 && waTags.every((t) => t.includes("data-fr=") && t.includes("data-en=")));

/* L'ADRESSE ÉCRITE DANS LE HTML DOIT ÊTRE CELLE QUE LE JAVASCRIPT FABRIQUERA.
   C'est ici que se serait caché l'écart entre le `quote()` de Python et `encodeURIComponent()`. */
const badStatic = waTags.filter((t) => {
  const href = (t.match(/href="([^"]+)"/) || [])[1];
  const fr = (t.match(/data-fr="([^"]*)"/) || [])[1];
  return href !== WA + encodeURIComponent(fr);
});
ok("chaque adresse statique = le texte français encodé par le JavaScript (au caractère près)",
   badStatic.length === 0, badStatic.slice(0, 1).join(""));

const imgs = [...html.matchAll(/<img[^>]*data-alt-fr[^>]*>/g)].map((m) => m[0]);
ok(`les ${imgs.length} images portent data-alt-fr ET data-alt-en`,
   imgs.length === 2 && imgs.every((t) => t.includes("data-alt-en=") && !/alt=""/.test(t)));

const details = [...html.matchAll(/<details>[\s\S]*?<\/details>/g)].map((m) => m[0]);
const summaries = details.map((d) => (d.match(/<summary[\s>]/g) || []).length);
ok(`les ${details.length} accordéons ont UN seul <summary> chacun (§20.11)`,
   details.length === 4 && summaries.every((n) => n === 1), "summary par bloc : " + summaries.join(", "));
ok("chaque <summary> porte ses DEUX langues à l'intérieur (jamais la classe de langue sur lui)",
   details.every((d) => {
     const s = (d.match(/<summary>[\s\S]*?<\/summary>/) || [""])[0];
     return s.includes("fr-only") && s.includes("en-only");
   }));

const structural = ["summary", "legend", "option", "title", "caption"];
const onStructural = structural.filter((t) => new RegExp("<" + t + "[^>]*class=\"[^\"]*(fr-only|en-only)").test(html));
ok("aucune classe de langue sur un élément STRUCTUREL", onStructural.length === 0, onStructural.join(", "));

const frN = (html.match(/class="[^"]*\bfr-only\b/g) || []).length;
const enN = (html.match(/class="[^"]*\ben-only\b/g) || []).length;
ok(`autant de .fr-only que de .en-only (${frN} / ${enN})`, frN === enN && frN > 30);

ok("le numéro de la boutique est celui de Cavisa, avec l'indicatif, partout",
   (html.match(/\+237699959052/g) || []).length >= 2 && !/wa\.me\/(?!237699959052)/.test(html));
ok("aucun lien mort : pas un seul href=\"#\"", !/href="#"/.test(html));
ok("aucun prix, aucun délai chiffré, aucune note, aucun avis dans le texte visible",
   !/\b\d{2,3}\s?\d{3}\s?(FCFA|XAF|fcfa)\b/i.test(html) && !/aggregateRating|ratingValue/.test(html));

/* ═════════════ 1 · la bascule FR | EN ═════════════ */
console.log("\n═══ 1 · la bascule, et ce qu'elle change vraiment ═══");

const MESSAGES = [
  ["Bonjour Cavisa Optique, je cherche des lunettes.", "Hello Cavisa Optique, I am looking for glasses."],
  ["Bonjour Cavisa Optique, je voudrais voir les montures que vous avez dans la boutique.",
   "Hello Cavisa Optique, I would like to see the frames you have in the shop."],
  ["Bonjour Cavisa Optique, j’ai une ordonnance et je voudrais des verres.",
   "Hello Cavisa Optique, I have a prescription and I would like lenses."],
  ["Bonjour Cavisa Optique, je voudrais un renseignement avant de passer.",
   "Hello Cavisa Optique, I would like some information before coming."],
];
const ALT = ["Une cliente essaie une monture devant le miroir du comptoir, un opticien en blouse blanche à côté d'elle.",
             "A customer tries on frames at the counter mirror, an optician in a white coat beside her."];

function run(lang, stored) {
  const store = localStorageStub();
  if (stored) store.setItem("cavisa-lang", stored);
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
  const registry = {
    "btn-fr": el("button"), "btn-en": el("button"), "say": el("p"),
    "QA:a.wa": anchors, "QA:img[data-alt-fr]": [image],
  };
  const document = doc(registry, lang);
  new Function("document", "window", "localStorage", langSrc)(
    document, { matchMedia: () => ({ matches: false }) }, store);
  return { document, anchors, image, store };
}

let r = run("fr");
ok("départ en français : la page se déclare en français",
   r.document.documentElement.getAttribute("data-lang") === "fr" && r.document.documentElement.lang === "fr");
ok("départ en français : FR est enfoncé, EN ne l'est pas",
   r.document.getElementById("btn-fr").getAttribute("aria-pressed") === "true" &&
   r.document.getElementById("btn-en").getAttribute("aria-pressed") === "false");
ok("départ en français : le message WhatsApp reste français",
   r.anchors.every((a) => waMessage(a.getAttribute("href")).indexOf("Bonjour Cavisa Optique") === 0) &&
   waMessage(r.anchors[3].getAttribute("href")) === MESSAGES[3][0]);
ok("départ en français : le texte de remplacement des images est français",
   r.image.getAttribute("alt") === ALT[0]);

r.document.getElementById("btn-en").fire("click");
ok("clic sur EN : la page bascule et se déclare en anglais",
   r.document.documentElement.getAttribute("data-lang") === "en" && r.document.documentElement.lang === "en");
ok("clic sur EN : les deux boutons disent leur état (aria-pressed)",
   r.document.getElementById("btn-en").getAttribute("aria-pressed") === "true" &&
   r.document.getElementById("btn-fr").getAttribute("aria-pressed") === "false");
ok("clic sur EN : les 4 messages WhatsApp passent en anglais, numéro inchangé",
   r.anchors.every((a, i) => waMessage(a.getAttribute("href")) === MESSAGES[i][1]) &&
   r.anchors.every((a) => a.getAttribute("href").indexOf(WA) === 0));
ok("clic sur EN : le texte de remplacement de l'image passe en anglais",
   r.image.getAttribute("alt") === ALT[1]);
ok("clic sur EN : le choix est retenu (localStorage), pas seulement affiché",
   r.store.getItem("cavisa-lang") === "en");
ok("clic sur EN : la région vive l'annonce (role=status)",
   /English/.test(r.document.getElementById("say").textContent));

r = run("fr", "en");
ok("un visiteur qui revient en anglais : la page se rouvre en anglais, sans clic",
   r.document.documentElement.getAttribute("data-lang") === "en" &&
   waMessage(r.anchors[0].getAttribute("href")).indexOf("Hello") === 0);

/* ═════════════ 2 · le mouvement ne doit jamais cacher la page ═════════════ */
console.log("\n═══ 2 · le mouvement, et le droit de ne rien voir ═══");

function runReveal(globals) {
  const items = [el("li"), el("li"), el("div")];
  const registry = { "QA:.rv": items };
  const document = doc(registry);
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
/* Le script teste `'IntersectionObserver' in window` avant de s'en servir : le faux `window` doit donc
   porter l'API, sinon on ne teste pas le chemin réel (piège attrapé le 24/09 en écrivant ce fichier). */
const calm = runReveal({ window: { matchMedia: () => ({ matches: true }), IntersectionObserver: IO }, IO });
ok("mouvement réduit demandé par le visiteur : affichage immédiat, aucune animation",
   calm.every((n) => n.classList.contains("in")));

seen = [];
const live = runReveal({ window: { matchMedia: () => ({ matches: false }), IntersectionObserver: IO }, IO });
ok("sinon : les blocs sont confiés à l'observateur, pas allumés d'avance",
   live.every((n) => !n.classList.contains("in")) && seen.length === 3);

console.log(process.exitCode ? "\nDES ÉCHECS — voir ci-dessus." : "\nTout est vert.");
