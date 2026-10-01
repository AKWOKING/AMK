/**
 * test_unilabo_page.mjs — rejoue le VRAI JavaScript de `demos/concept-unilabo-v2.html` hors navigateur.
 *
 * Deux suites, celles qui protègent les deux seules choses dynamiques de la page :
 *   1. LE FORMULAIRE ET LA FICHE VIVANTE — six états (vide, partiel, complet FR, complet EN,
 *      refus expliqué, bascule de langue), avec lecture du message WhatsApp généré mot pour mot.
 *   2. L'ÉTAT D'OUVERTURE — cinq horloges (lundi 10 h, lundi 22 h, samedi 10 h, samedi 15 h,
 *      dimanche 11 h) et les deux langues, parce que la page affirme un état au visiteur.
 *
 * Ce que ça n'est pas : un test de rendu. Le CSS, la mise en page et l'œil restent à King.
 * Voir `design/LESSONS.md` (un compilateur voit ce qu'un auditeur de contraste ne voit pas).
 *
 * 24/09 — LA REFONTE. La page a été réécrite de zéro (mobile d'abord, cinq photographies au lieu de
 * quinze, texte plus jamais posé sur une image). Les deux blocs de JavaScript qui portent le formulaire et
 * l'état d'ouverture sont repris MOT POUR MOT de la version précédente : ce sont eux qui portent la fiche vivante et l'état d'ouverture, et ce
 * sont eux que ce fichier protège. Le contrat qu'ils exigent de la page — dix-huit identifiants, la classe
 * `.chips`, les attributs `data-fr`/`data-en`/`data-prep`, les images `data-alt-fr` — est vérifié par la
 * SUITE 0 de ce fichier, contre le HTML lui-même — auquel s'ajoute un troisième bloc, ÉCRIT pour la
 * refonte (les liens WhatsApp statiques qui prennent la langue du visiteur, suite 3). Si un test tombe ici,
 * c'est la page qui a bougé, pas le test.
 *
 * Usage :  node tools/qa/test_unilabo_page.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { el, doc, localStorageStub, fixedClock, scriptAfter, waMessage, ok } from "./fake_dom.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const PAGE = path.join(ROOT, "demos", "concept-unilabo-v2.html");
const html = fs.readFileSync(PAGE, "utf8");
const formSrc = scriptAfter(html, "LA FICHE VIVANTE");
const linksSrc = scriptAfter(html, "LES LIENS WHATSAPP QUI PARLENT LA LANGUE");
/* Le marqueur du bloc principal : la page commence par un micro-script qui retire `no-js` ; viser
   « (function(){ » tomberait dessus depuis la refonte. On vise un commentaire propre au bloc. */
const mainSrc = scriptAfter(html, "L'ÉTAT RÉEL DU LABORATOIRE");

/* ───────────────────────────── suite 0 · le contrat page ⇄ JavaScript ─────────────────────────────
   Les blocs ci-dessus ne parlent à la page que par des identifiants, des classes et quelques attributs.
   Ces quelques lignes refusent une page qui ne les porte plus : sans elles, une refonte peut être
   parfaitement valide et laisser la fiche vivante muette — l'écran ne le montrerait qu'au visiteur. */
console.log("═══ 0 · le contrat que la page doit au JavaScript ═══");

const IDS = ["rdv", "rdv-go", "rdv-said", "fiche-state", "fiche-nom", "fiche-tests", "fiche-prep",
             "fiche-moment", "fiche-foot", "btn-fr", "btn-en", "open-state", "wa-said",
             "rdv-g1", "rdv-g2", "rdv-g3", "rdv-nom", "rdv-note"];
const missing = IDS.filter((id) => !html.includes(`id="${id}"`));
ok(`les ${IDS.length} identifiants attendus sont dans la page`, missing.length === 0, "manquants : " + missing.join(", "));
ok("le groupe de préparation porte la classe .chips (son étiquette de langue)",
   /class="[^"]*\bchips\b/.test(html));
ok("la bande de retour est marquée [data-wa-bar]", html.includes("data-wa-bar"));

const boxes = [...html.matchAll(/<input type="checkbox"[^>]*>/g)].map((m) => m[0]);
ok(`les ${boxes.length} cases à cocher portent data-fr ET data-en`,
   boxes.length > 0 && boxes.every((b) => b.includes("data-fr=") && b.includes("data-en=")));
const PREPS = ["jeun", "urines", "hormones", "enfant", "suivi", "ordonnance", "autre"];
const badPrep = boxes.map((b) => (b.match(/data-prep="([^"]+)"/) || [])[1]).filter((v) => v && !PREPS.includes(v));
ok("chaque data-prep appartient au vocabulaire connu du formulaire", badPrep.length === 0, badPrep.join(", "));

const moments = [...html.matchAll(/<input type="radio" name="moment"[^>]*>/g)].map((m) => m[0]);
ok(`les ${moments.length} moments portent data-fr ET data-en`,
   moments.length === 4 && moments.every((m) => m.includes("data-fr=") && m.includes("data-en=")));

const altables = [...html.matchAll(/<img[^>]*data-alt-fr[^>]*>/g)].map((m) => m[0]);
ok(`les ${altables.length} photographies ont leur texte alternatif dans les deux langues`,
   altables.length > 0 && altables.every((i) => i.includes("data-alt-en=")));

const waLinks = [...html.matchAll(/https:\/\/wa\.me\/(\d+)/g)].map((m) => m[1]);
ok(`tous les liens WhatsApp pointent le numéro du laboratoire (${waLinks.length} liens)`,
   waLinks.length > 0 && waLinks.every((n) => n === "237696139819"));
ok("la page ne déclare qu'un seul titre de niveau 1", (html.match(/<h1[\s>]/g) || []).length === 1);

/* ── LA CLASSE DE BUG RELEVÉE DANS LA VERSION PRÉCÉDENTE ──────────────────────────────────────────────
   Ses liens « Demander le tarif » portaient une apostrophe encodée DEUX fois : l'URL disait d%26%23x27;,
   et WhatsApp affichait « le tarif d&#x27;… » au patient. Le constructeur encode désormais chaque message
   en un seul endroit, mais une régression silencieuse reste possible : on la refuse ici. */
const hrefs = [...html.matchAll(/href="([^"]*)"/g)].map((m) => m[1]);
const doubleEncoded = hrefs.filter((h) => /%26%23|&#x|&amp;#|%23x27/.test(h));
ok("aucun lien ne porte une apostrophe (ou une esperluette) encodée deux fois",
   doubleEncoded.length === 0, doubleEncoded.slice(0, 2).join(" | "));

const waStatic = [...html.matchAll(/<a[^>]*data-wa[^>]*>/g)].map((m) => m[0]);
ok(`les ${waStatic.length} liens WhatsApp statiques portent leur message DANS LES DEUX LANGUES`,
   waStatic.length >= 4 && waStatic.every((a) => a.includes("data-fr-text=") && a.includes("data-en-text=")),
   waStatic.filter((a) => !a.includes("data-en-text=")).length + " sans version anglaise");
ok("ces liens portent un href réel et utilisable SANS JavaScript (le français, langue du laboratoire)",
   waStatic.every((a) => /href="https:\/\/wa\.me\/237696139819\?text=.+"/.test(a)));

/* ── LE PLAN ─────────────────────────────────────────────────────────────────────────────────────────
   Un plan est du TEXTE dans un dessin : sur un téléphone de 360 px, un libellé de 11 unités dans un
   viewBox de 460 s'affiche à 9 px — illisible, alors que le plan sert justement à trouver le laboratoire.
   On refuse donc un plan dont un libellé passerait sous 12 unités, et un plan sans épingle ni nord. */
/* on vise LE plan (role="img" + son rapport largeur/hauteur), pas la première icône venue */
const svg = (html.match(/<svg viewBox="0 0 (\d+) (\d+)" role="img"[\s\S]*?<\/svg>/) || [])[0] || "";
const svgW = parseInt((svg.match(/viewBox="0 0 (\d+)/) || [])[1] || "0", 10);
const svgSizes = [...svg.matchAll(/font-size="(\d+)"/g)].map((m) => parseInt(m[1], 10));
ok(`le plan est dessiné (${svgSizes.length} libellés, viewBox ${svgW} unités de large)`, svgSizes.length >= 6 && svgW > 0);
ok("aucun libellé du plan ne passe sous 12 unités (≈ 13 px sur un téléphone)",
   svgSizes.every((n) => n >= 12), "minimum : " + Math.min(...svgSizes));
ok("le plan marque l'emplacement du laboratoire par une épingle, pas une tache",
   /d="M\d+ \d+c-[\d.]+ 0-/.test(svg) && svg.includes('fill="#5B21B6"'));
ok("le plan porte son nord", />N<|">N"</.test(svg));

/* ───────────────────────────── suite 1 · le formulaire et la fiche ───────────────────────────── */
const CHECKBOXES = [
  { "data-fr": "Glycémie (à jeun)", "data-en": "Glucose (fasting)", "data-prep": "jeun" },
  { "data-fr": "Analyse d'urines", "data-en": "Urine test", "data-prep": "urines" },
  { "data-fr": "TSH, T3, T4 (thyroïde)", "data-en": "TSH, T3, T4 (thyroid)", "data-prep": "hormones" },
  { "data-fr": "Hémogramme complet (NFS)", "data-en": "Complete blood count (CBC)" }, // sans consigne
  { "data-fr": "Autre analyse", "data-en": "Another test", "data-prep": "autre" },
];

function runForm(lang, state) {
  const boxes = CHECKBOXES.map((a) => { const e = el("input"); Object.entries(a).forEach(([k, v]) => e.setAttribute(k, v)); return e; });
  boxes.forEach((b, i) => { b.checked = state.checked.includes(i); });
  const moment = el("input");
  moment.setAttribute("data-fr", "Matin (7h–12h)");
  moment.setAttribute("data-en", "Morning (7am–12pm)");

  const form = el("form");
  const reg = {
    "rdv": form, "rdv-go": el("a"), "rdv-said": el("p"),
    "fiche-state": el("span"), "fiche-nom": el("dd"), "fiche-tests": el("dd"),
    "fiche-prep": el("dd"), "fiche-moment": el("dd"), "fiche-foot": el("p"),
    "btn-fr": el("button"), "btn-en": el("button"),
    "Q:#rdv-g1": el("fieldset"), "Q:#rdv-g2": el("div"), "Q:#rdv-g3": el("fieldset"),
    "Q:#rdv-nom": (() => { const e = el("input"); e.value = state.nom || ""; return e; })(),
    "Q:#rdv-note": (() => { const e = el("input"); e.value = state.note || ""; return e; })(),
    "Q:input[name=\"moment\"]": moment,
    "Q:input[name=\"moment\"]:checked": state.moment ? moment : null,
  };
  form.querySelectorAll = () => boxes.filter((b) => b.checked);
  form.querySelector = (sel) => (("Q:" + sel) in reg ? reg["Q:" + sel] : null);

  const document = doc(reg, lang);
  const window = { location: { href: "" } };
  new Function("document", "window", "localStorage", formSrc)(document, window, localStorageStub());
  return { reg, document, boxes, form };
}

console.log("═══ 1 · le formulaire et la fiche vivante ═══");

let r = runForm("fr", { checked: [0, 2], nom: "Alice Ndoumbé", moment: true });
let msg = waMessage(r.reg["rdv-go"].getAttribute("href"));
ok("complet FR — l'action est allumée", r.reg["rdv-go"].getAttribute("aria-disabled") === "false");
ok("complet FR — la fiche dit « prête à envoyer »", r.reg["fiche-state"].textContent === "prête à envoyer");
ok("complet FR — les analyses cochées sont écrites", r.reg["fiche-tests"].textContent.includes("Glycémie"));
ok("complet FR — la préparation est déduite du texte du laboratoire",
   r.reg["fiche-prep"].textContent.startsWith("À jeun 8 à 12 h"),
   r.reg["fiche-prep"].textContent);
ok("complet FR — le message nomme l'analyse ET la préparation",
   msg.includes("Nom : Alice Ndoumbé") && msg.includes("Préparation : À jeun 8 à 12 h"), msg.replace(/\n/g, " · "));

r = runForm("en", { checked: [0, 1], nom: "Alice Ndoumbé", moment: true });
msg = waMessage(r.reg["rdv-go"].getAttribute("href"));
ok("complet EN — la fiche suit la langue", r.reg["fiche-tests"].textContent === "Glucose (fasting) · Urine test");
ok("complet EN — le message part en anglais", msg.startsWith("Hello UNI-LABO") && msg.includes("Preparation: Fasting 8 to 12 h"));

r = runForm("fr", { checked: [3], nom: "", moment: false });
ok("incomplet — l'action est éteinte", r.reg["rdv-go"].getAttribute("aria-disabled") === "true");
ok("incomplet — l'action garde une URL générique (jamais un brouillon)",
   r.reg["rdv-go"].getAttribute("href") ===
   "https://wa.me/237696139819?text=" + encodeURIComponent("Bonjour UNI-LABO, je souhaite prendre rendez-vous."));
ok("sans consigne publiée — la page le DIT au lieu de l'inventer",
   r.reg["fiche-prep"].textContent === "Pas de consigne particulière publiée : nous confirmons par message",
   r.reg["fiche-prep"].textContent);

const prevented = r.reg["rdv-go"].fire("click");
ok("refus — le clic est empêché", prevented === true);
ok("refus — le groupe « moment » passe en erreur", r.reg["Q:#rdv-g3"].classList.contains("is-err"));
ok("refus — le nom porte aria-invalid", r.reg["Q:#rdv-nom"].getAttribute("aria-invalid") === "true");
ok("refus — la raison est écrite à l'écran", r.reg["rdv-said"].textContent.startsWith("Cochez au moins une analyse"));

r = runForm("fr", { checked: [0], nom: "Bob", moment: true });
ok("valide — le clic N'EST PAS empêché", r.reg["rdv-go"].fire("click") === false);

r = runForm("fr", { checked: [0], nom: "Bob", moment: true });
r.document.documentElement.setAttribute("data-lang", "en");
r.reg["btn-en"].fire("click");
await new Promise((res) => setTimeout(res, 5));
ok("bascule de langue — la fiche se réécrit en anglais",
   r.reg["fiche-tests"].textContent === "Glucose (fasting)" &&
   r.reg["fiche-prep"].textContent.startsWith("Fasting"), r.reg["fiche-prep"].textContent);

/* ───────────────────────────── suite 2 · l'état d'ouverture ───────────────────────────── */
console.log("\n═══ 2 · l'état d'ouverture, à l'heure de Douala ═══");

function runOpening(iso, lang) {
  const reg = { "btn-fr": el("button"), "btn-en": el("button"), "open-state": el("span"), "wa-said": el("p"),
                "Q:.chips": el("div"), "QA:.chip": [], "QA:.prep-panel": [], "QA:a[href]": [] };
  const im = el("img");
  im.setAttribute("data-alt-fr", "FR alt");
  im.setAttribute("data-alt-en", "EN alt");
  reg["QA:img[data-alt-fr]"] = [im];
  const document = doc(reg, lang);
  new Function("document", "window", "localStorage", "Date", "setTimeout", mainSrc)(
    document, { location: { href: "" } }, localStorageStub(), fixedClock(iso), () => {});
  return { reg, im };
}

const CASES = [
  ["2026-09-28T09:15:00Z", "fr", "lundi 10h15", /Ouvert maintenant, jusqu'à 19h/],
  ["2026-09-28T21:00:00Z", "fr", "lundi 22h", /Fermé, nous rouvrons demain à 7h/],
  ["2026-09-26T09:00:00Z", "fr", "samedi 10h", /Ouvert maintenant, jusqu'à 13h/],
  ["2026-09-26T14:00:00Z", "en", "samedi 15h", /Closed, we open Monday at 7am/],
  ["2026-09-27T10:00:00Z", "en", "dimanche 11h", /Closed, we open Monday at 7am/],
];
for (const [iso, lang, label, want] of CASES) {
  const { reg } = runOpening(iso, lang);
  ok(`${label} → ${lang}`, want.test(reg["open-state"].innerHTML), reg["open-state"].innerHTML.replace(/<[^>]+>/g, " ").trim());
}

const { reg: regEn, im } = runOpening("2026-09-28T09:15:00Z", "en");
ok("l'étiquette du groupe de puces suit la langue", regEn["Q:.chips"].getAttribute("aria-label") === "Preparation");
ok("le texte alternatif des photos suit la langue", im.getAttribute("alt") === "EN alt");

/* ───────────────────────── suite 3 · les liens WhatsApp suivent la langue ───────────────────────── */
console.log("\n═══ 3 · les liens WhatsApp, dans la langue du visiteur ═══");

function runLinks(lang) {
  const messages = [
    { fr: "Bonjour UNI-LABO, je voudrais connaître le tarif de cette analyse : ",
      en: "Hello UNI-LABO, I would like to know the price of this test: " },
    { fr: "Bonjour Dr Tientcheu, j'ai une question sur une analyse.",
      en: "Hello Dr Tientcheu, I have a question about a test." },
  ];
  const anchors = messages.map((m) => {
    const a = el("a");
    a.setAttribute("data-fr-text", m.fr);
    a.setAttribute("data-en-text", m.en);
    a.setAttribute("href", "https://wa.me/237696139819?text=" + encodeURIComponent(m.fr));
    return a;
  });
  const document = doc({ "QA:a[data-wa][data-fr-text]": anchors, "btn-fr": el("button"), "btn-en": el("button") }, lang);
  new Function("document", linksSrc)(document);
  return anchors;
}

let anchors = runLinks("fr");
ok("page en français — le lien reste français et la phrase est encodée UNE fois",
   waMessage(anchors[0].getAttribute("href")) === "Bonjour UNI-LABO, je voudrais connaître le tarif de cette analyse : ",
   waMessage(anchors[0].getAttribute("href")));
anchors = runLinks("en");
ok("page en anglais — le lien s'écrit en anglais (l'apostrophe revient en clair)",
   waMessage(anchors[1].getAttribute("href")) === "Hello Dr Tientcheu, I have a question about a test.",
   waMessage(anchors[1].getAttribute("href")));
ok("page en anglais — le numéro ne change jamais",
   anchors.every((a) => a.getAttribute("href").indexOf("https://wa.me/237696139819?text=") === 0));

console.log(process.exitCode ? "\nDES ÉCHECS — voir ci-dessus." : "\nTout est vert.");
