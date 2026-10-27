/**
 * ─────────────────────────────────────────────────────────────────────────────
 * Vérifier la réservation DANS un DOM — trois états, deux langues
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Les portiques du site (`tests/logic.test.mjs`) tournent sans dépendance : ils
 * prouvent la logique, pas le rendu. Ce script prouve le rendu, sans navigateur :
 * il assemble `js/app.js` avec esbuild, l'exécute dans jsdom, et lit ce que la
 * page affiche dans trois états de configuration.
 *
 *   node tools/qa/verify_booking_dom.mjs
 *
 * Dépendances installées HORS du dépôt (le site reste sans dépendance, c'est
 * une promesse testée) :
 *
 *   mkdir -p /tmp/amk-dom && cd /tmp/amk-dom && npm init -y && npm i jsdom esbuild
 *   NODE_PATH=/tmp/amk-dom/node_modules node tools/qa/verify_booking_dom.mjs
 *
 * Ce qu'il refuse de laisser passer : un bouton visible sans lien ; un lien sans
 * `href` ; la phrase « aucune connexion à un agenda » affichée alors qu'un lien
 * existe ; l'inverse ; un bouton sur un lieu qui n'a pas de page ; et un message
 * WhatsApp promis alors qu'aucun numéro n'est publié.
 */
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createRequire } from "node:module";

const SITE = path.resolve(process.argv[2] || "hosting/previews/dr-ophtalmo");
const GLOBAL_URL = "https://calendar.app.google/essai-general";
const LOCAL_URL = "https://calendar.app.google/essai-douala";

let JSDOM;
let esbuild;
try {
  const require = createRequire(import.meta.url);
  ({ JSDOM } = require("jsdom"));
  esbuild = require("esbuild");
} catch {
  console.error(
    "jsdom et esbuild sont absents. Installez-les hors du dépôt :\n" +
      "  mkdir -p /tmp/amk-dom && cd /tmp/amk-dom && npm init -y && npm i jsdom esbuild\n" +
      "  NODE_PATH=/tmp/amk-dom/node_modules node tools/qa/verify_booking_dom.mjs",
  );
  process.exit(2);
}

/** Une copie du site dans /tmp, avec les liens forcés. Le dépôt n'est pas touché. */
function copie({ globalUrl = "", localUrl = "" } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "amk-booking-"));
  fs.cpSync(SITE, dir, { recursive: true, filter: (src) => !src.includes("/tests") });
  const config = path.join(dir, "js/config/doctor.js");
  let code = fs.readFileSync(config, "utf8");

  if (globalUrl) {
    const avant = code;
    code = code.replace('const BOOKING_URL = "";', `const BOOKING_URL = ${JSON.stringify(globalUrl)};`);
    if (code === avant) throw new Error("constante BOOKING_URL introuvable");
  }
  if (localUrl) {
    const avant = code;
    code = code.replace(
      /(id: "africa-medical",\s*\n\s*bookingUrl: )""/,
      `$1${JSON.stringify(localUrl)}`,
    );
    if (code === avant) throw new Error("bookingUrl du lieu africa-medical introuvable");
  }
  fs.writeFileSync(config, code);
  return path.join(dir, "js/app.js");
}

/** Le bundle, exécuté dans jsdom ; on lit ensuite l'état réel de la page. */
function rendre(entree, { choisirLieu } = {}) {
  const bundle = esbuild.buildSync({
    entryPoints: [entree],
    bundle: true,
    format: "iife",
    write: false,
    logLevel: "silent",
  }).outputFiles[0].text;

  const html = fs
    .readFileSync(path.join(SITE, "index.html"), "utf8")
    .replace(/<script[^>]*type="module"[^>]*><\/script>/, "");

  const dom = new JSDOM(html, { runScripts: "dangerously", pretendToBeVisual: true, url: "https://exemple.test/" });
  const { window } = dom;
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  window.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
  const script = window.document.createElement("script");
  script.textContent = bundle;
  window.document.body.append(script);
  window.document.dispatchEvent(new window.Event("DOMContentLoaded"));

  if (choisirLieu) {
    const select = window.document.querySelector("[data-location-select]");
    select.value = choisirLieu;
    select.dispatchEvent(new window.Event("change", { bubbles: true }));
  }

  const q = (s) => window.document.querySelector(s);
  const texte = (s) => (q(s) ? q(s).textContent.trim() : "");
  const visible = (s) => (q(s) ? !q(s).hidden : false);
  const semaine = [...window.document.querySelectorAll("[data-schedule-note] p")].find((n) =>
    /agenda|calendar/i.test(n.textContent),
  );
  const ligneInfo = [...window.document.querySelectorAll("[data-info-list] li")].find((li) =>
    /Réservation en ligne|Online booking/.test(li.textContent),
  );

  const etat = {
    lieu: choisirLieu || "(aucun)",
    bouton: visible("[data-booking]"),
    lien: q("[data-booking-link]")?.getAttribute("href") ?? null,
    // Le bouton WhatsApp d'après réservation ne doit apparaître que si le lieu a
    // un créneau ET qu'un numéro est publié.
    wa: q("[data-booking-wa]")?.getAttribute("href") ?? null,
    phrase: texte('[data-i18n="appointment.liveNote"]'),
    partiel: visible("[data-booking-partial]") ? texte("[data-booking-partial]") : null,
    semaine: semaine ? semaine.textContent.trim() : "(absente)",
    panneau: ligneInfo ? (ligneInfo.dataset.known === "true" ? "renseigné" : "à renseigner") : "(absent)",
  };

  const en = window.document.querySelector('[data-lang="en"]');
  if (en) en.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  etat.phraseEn = texte('[data-i18n="appointment.liveNote"]');
  etat.partielEn = visible("[data-booking-partial]") ? texte("[data-booking-partial]") : null;

  return etat;
}

const scenarios = {
  "① aucun lien (aujourd'hui)": rendre(copie()),
  "② page générale, lien collé": rendre(copie({ globalUrl: GLOBAL_URL }), { choisirLieu: "mbouda" }),
  "③ page pour Africa Médical seulement · lieu Mbouda": rendre(copie({ localUrl: LOCAL_URL }), {
    choisirLieu: "mbouda",
  }),
  "④ même configuration · lieu Africa Médical": rendre(copie({ localUrl: LOCAL_URL }), {
    choisirLieu: "africa-medical",
  }),
};

for (const [nom, etat] of Object.entries(scenarios)) {
  console.log(`\n── ${nom}`);
  for (const [k, v] of Object.entries(etat)) {
    console.log(`   ${k.padEnd(9)} ${String(v ?? "—").slice(0, 104)}`);
  }
}

const fautes = [];
const attendu = (condition, message) => {
  if (!condition) fautes.push(message);
};

const [un, deux, trois, quatre] = Object.values(scenarios);

// ① rien n'est branché : le site d'aujourd'hui, à la lettre.
attendu(un.bouton === false, "① le bouton est visible sans lien");
attendu(un.lien === null, "① le bouton porte un href");
attendu(/aucune connexion à un agenda/i.test(un.phrase), "① la phrase ne nie plus l'agenda");
attendu(/aucune synchronisation avec un agenda/i.test(un.semaine), "① la semaine nie l'agenda");
attendu(un.partiel === null, "① une phrase « réservable ailleurs » s'affiche sans réservation nulle part");
attendu(un.panneau === "à renseigner", "① le panneau « à publier » ne réclame pas le lien");
attendu(un.wa === null, "① un bouton WhatsApp apparaît sans réservation");

// ② page générale : le bouton existe pour n'importe quel lieu.
attendu(deux.bouton === true, "② le bouton n'apparaît pas");
attendu(deux.lien === GLOBAL_URL, "② le bouton ne pointe pas sur la page générale");
attendu(!/aucune connexion à un agenda/i.test(deux.phrase), "② la phrase nie encore tout agenda");
attendu(/agenda|calendar/i.test(deux.semaine) && !/aucune synchronisation/i.test(deux.semaine), "② la semaine nie encore l'agenda");
attendu(deux.partiel === null, "② une phrase « réservable ailleurs » s'affiche alors que le lieu a une page");
attendu(/wa\.me\/237691280237/.test(deux.wa || ""), "② le bouton WhatsApp ne pointe pas sur le numéro publié");
attendu(decodeURIComponent(deux.wa || "").includes("Mbouda"), "② le message WhatsApp ne nomme pas le lieu");

// ③ une page pour un seul lieu : surtout pas de bouton ailleurs.
attendu(trois.bouton === false, "③ le bouton apparaît sur un lieu qui n'a pas de page");
attendu(trois.lien === null, "③ un href traîne sur un lieu sans page");
attendu(trois.partiel !== null, "③ le lieu sans page ne s'explique pas");
attendu(trois.wa === null, "③ un bouton WhatsApp apparaît pour un lieu sans réservation");
attendu(/préparez une demande/i.test(trois.partiel || ""), "③ la phrase ne dit pas quoi faire");
attendu(trois.phraseEn.length > 0 && !/no connection to any calendar/i.test(trois.phraseEn), "③ la phrase anglaise nie l'agenda alors qu'une page existe");
attendu(decodeURIComponent(trois.semaine).includes("créneaux") || /calendar/i.test(decodeURIComponent(trois.semaine)), "③ la semaine ne mentionne pas la réservation");

// ④ le bon lieu : bouton, message, et pas de phrase partielle.
attendu(quatre.bouton === true, "④ le bouton manque sur le lieu qui a une page");
attendu(quatre.lien === LOCAL_URL, "④ le bouton ne pointe pas sur la page du lieu");
attendu(quatre.partiel === null, "④ la phrase partielle s'affiche sur le lieu qui a une page");
attendu(decodeURIComponent(quatre.wa || "").includes("Africa Médical"), "④ le message WhatsApp ne nomme pas le lieu");
attendu(/Math\.|undefined|\[object/i.test(quatre.phrase) === false, "④ une valeur brute s'affiche dans la phrase");

if (fautes.length) {
  console.error(`\n${fautes.length} faute(s) :`);
  for (const f of fautes) console.error(`  ✗ ${f}`);
  process.exit(1);
}
console.log("\n0 faute — les quatre états tiennent, dans les deux langues.");
