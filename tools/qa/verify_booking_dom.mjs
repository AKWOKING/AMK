/**
 * ─────────────────────────────────────────────────────────────────────────────
 * Vérifier le bouton de réservation DANS un DOM — éteint, puis allumé
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Les portiques du site (`tests/logic.test.mjs`) tournent sans dépendance : ils
 * prouvent la logique, pas le rendu. Ce script prouve le rendu, sans navigateur :
 * il assemble `js/app.js` avec esbuild, l'exécute dans jsdom, et lit ce que la
 * page affiche dans les deux états de `bookingUrl`.
 *
 *   node tools/qa/verify_booking_dom.mjs
 *
 * Il a besoin de deux paquets, installés HORS du dépôt (le site reste sans
 * dépendance, c'est une promesse testée) :
 *
 *   mkdir -p /tmp/amk-dom && cd /tmp/amk-dom && npm init -y && npm i jsdom esbuild
 *   NODE_PATH=/tmp/amk-dom/node_modules node tools/qa/verify_booking_dom.mjs
 *
 * Ce qu'il refuse de laisser passer : un bouton visible sans lien, un lien sans
 * `href`, une phrase « aucune connexion à un agenda » qui reste affichée alors
 * que le bouton existe, et l'inverse.
 */
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";

const SITE = path.resolve(process.argv[2] || "hosting/previews/dr-ophtalmo");
const FAKE_URL = "https://calendar.app.google/essai-local-non-publie";

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

/** Une copie du site dans /tmp, avec `bookingUrl` forcé. Le dépôt n'est pas touché. */
function copieAvec(url) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "amk-booking-"));
  fs.cpSync(SITE, dir, { recursive: true, filter: (src) => !src.includes("/tests") });
  const config = path.join(dir, "js/config/doctor.js");
  const avant = fs.readFileSync(config, "utf8");
  const apres = url ? avant.replace('const BOOKING_URL = "";', `const BOOKING_URL = ${JSON.stringify(url)};`) : avant;
  if (url && apres === avant) throw new Error("la constante BOOKING_URL n'a pas été trouvée dans doctor.js");
  fs.writeFileSync(config, apres);
  return { dir, entree: path.join(dir, "js/app.js") };
}

/** Le bundle, exécuté dans jsdom ; on lit ensuite l'état réel de la page. */
function rendre(entree) {
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
  // jsdom a déjà passé DOMContentLoaded quand on ajoute le script : on le rejoue.
  window.document.dispatchEvent(new window.Event("DOMContentLoaded"));

  const q = (s) => window.document.querySelector(s);
  const texte = (s) => (q(s) ? q(s).textContent.trim() : "");
  const semaine = [...window.document.querySelectorAll("[data-schedule-note] p")].find((n) =>
    /agenda|calendar/i.test(n.textContent),
  );
  const ligneInfo = [...window.document.querySelectorAll("[data-info-list] li")].find((li) =>
    /Réservation en ligne|Online booking/.test(li.textContent),
  );

  const etat = {
    boutonVisible: q("[data-booking]") ? !q("[data-booking]").hidden : false,
    lien: q("[data-booking-link]")?.getAttribute("href") ?? null,
    nouvelOnglet: q("[data-booking-link]")?.getAttribute("target") ?? null,
    // Les textes sont gardés entiers : c'est l'affichage qui les coupe, pas les contrôles.
    phraseRendezVous: texte('[data-i18n="appointment.liveNote"]'),
    phraseSemaine: semaine ? semaine.textContent.trim() : "(absente)",
    panneauInfo: ligneInfo ? `${ligneInfo.dataset.known === "true" ? "renseigné" : "à renseigner"}` : "(absent)",
  };

  // Et la même chose après un clic sur le sélecteur de langue.
  const en = window.document.querySelector('[data-lang="en"]');
  if (en) en.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  etat.phraseRendezVousEn = texte('[data-i18n="appointment.liveNote"]');
  etat.phraseSemaineEn = (
    [...window.document.querySelectorAll("[data-schedule-note] p")].find((n) => /agenda|calendar/i.test(n.textContent))
      ?.textContent || "(absente)"
  ).trim();

  return etat;
}

const eteint = rendre(copieAvec("").entree);
const allume = rendre(copieAvec(FAKE_URL).entree);

console.log("\nÉTEINT (bookingUrl vide)");
for (const [k, v] of Object.entries(eteint)) console.log(`  ${k.padEnd(20)} ${String(v).slice(0, 96)}`);
console.log("\nALLUMÉ (lien collé)");
for (const [k, v] of Object.entries(allume)) console.log(`  ${k.padEnd(20)} ${String(v).slice(0, 96)}`);

const fautes = [];
const attendu = (condition, message) => {
  if (!condition) fautes.push(message);
};

attendu(eteint.boutonVisible === false, "éteint : le bouton est visible sans lien");
attendu(eteint.lien === null, "éteint : le bouton porte un href");
attendu(/aucune connexion à un agenda/i.test(eteint.phraseRendezVous), "éteint : la phrase des rendez-vous ne nie plus l'agenda");
attendu(/aucune synchronisation avec un agenda/i.test(eteint.phraseSemaine), "éteint : la phrase de la semaine ne nie plus l'agenda");
attendu(eteint.panneauInfo === "à renseigner", "éteint : le panneau « à publier » ne réclame pas le lien");

attendu(allume.boutonVisible === true, "allumé : le bouton n'apparaît pas");
attendu(allume.lien === FAKE_URL, "allumé : le bouton ne pointe pas sur le lien configuré");
attendu(allume.nouvelOnglet === "_blank", "allumé : le lien ne s'ouvre pas dans un nouvel onglet");
attendu(!/aucune connexion à un agenda/i.test(allume.phraseRendezVous), "allumé : la phrase nie encore tout agenda");
attendu(!/aucune synchronisation avec un agenda/i.test(allume.phraseSemaine), "allumé : la semaine nie encore tout agenda");
attendu(/agenda/i.test(allume.phraseSemaine), "allumé : la semaine ne dit pas d'où viennent les créneaux");
attendu(/no connection to any calendar/i.test(eteint.phraseRendezVousEn), "éteint (EN) : phrase fausse");
attendu(/booking page/i.test(allume.phraseRendezVousEn), "allumé (EN) : la phrase anglaise n'a pas basculé");
attendu(/calendar/i.test(allume.phraseSemaineEn), "allumé (EN) : la note de semaine n'a pas basculé");

if (fautes.length) {
  console.error(`\n${fautes.length} faute(s) :`);
  for (const f of fautes) console.error(`  ✗ ${f}`);
  process.exit(1);
}
console.log("\n0 faute — le bouton et les deux phrases basculent ensemble, dans les deux langues.");
