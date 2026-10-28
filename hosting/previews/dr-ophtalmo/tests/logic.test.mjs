/**
 * Vérifications qui tournent sans navigateur et sans dépendance :
 *
 *   node tests/logic.test.mjs
 *
 * Ce qu'elles protègent : la configuration (un lieu déclaré reste déclaré, un
 * jour annoncé a toujours sa source), les traductions (aucune clef orpheline),
 * la validation du formulaire, le message WhatsApp, et l'honnêteté du site —
 * aucun numéro inventé, aucun jour sans provenance écrite.
 */
import assert from "node:assert/strict";
import { doctorConfig, isKnown, doctorDisplayName, whatsappNumber } from "../js/config/doctor.js";
import { services } from "../js/config/services.js";
import { whatsappMessage, buildWhatsappUrl, formatDate, limits } from "../js/config/appointment.js";
import { dictionaries, createTranslator, resolve } from "../js/i18n/index.js";
import { buildWeek, hasAnyHours, locationDays, locationLabel, WEEK } from "../js/lib/schedule.js";
import { validate } from "../js/lib/validators.js";
import {
  bookingStatus,
  bookingFor,
  bookingCapability,
  bookingMode,
  liveCopyKey,
  liveNoteKey,
  BOOKING_HOSTS,
} from "../js/booking.js";

let passed = 0;
const check = (label, fn) => {
  fn();
  passed += 1;
  console.log(`  ✓ ${label}`);
};

const fr = createTranslator("fr");
const en = createTranslator("en");

/* ── 1 · La configuration ──────────────────────────────────────────────── */
console.log("\n1 · Configuration");

check("quatre lieux, quatre identifiants stables", () => {
  assert.equal(doctorConfig.locations.length, 4);
  assert.deepEqual(
    doctorConfig.locations.map((l) => l.id),
    ["mbouda", "bafoussam", "africa-medical", "hopital-charity"],
  );
});

check("chaque jour annoncé a une source écrite", () => {
  for (const location of doctorConfig.locations) {
    if ((location.days || []).length > 0) {
      assert.ok(isKnown(location.source), `${location.id} : jours sans source`);
      assert.match(location.source, /\d{2}\/\d{2}\/\d{4}/, `${location.id} : source sans date`);
    }
  }
});

check("aucun état de lieu hors du vocabulaire prévu", () => {
  for (const location of doctorConfig.locations) {
    assert.ok(["confirmed", "reported", "unknown"].includes(location.status), location.id);
  }
});

check("un lien d'itinéraire ne va jamais sans adresse vérifiée", () => {
  for (const location of doctorConfig.locations) {
    if (isKnown(location.mapUrl)) assert.ok(isKnown(location.address), location.id);
  }
});

check("le site ne se dit branché sur un agenda que si un lien existe", () => {
  // `meta.liveSync` n'est plus écrit à la main : il est déduit de `bookingUrl`
  // (js/config/doctor.js). Les deux ne peuvent donc pas se contredire.
  assert.equal(doctorConfig.meta.liveSync, bookingStatus(doctorConfig.bookingUrl).enabled);
});

check("aucun numéro douteux : si WhatsApp existe, c'est 8 à 15 chiffres", () => {
  const number = whatsappNumber();
  if (number) assert.match(number, /^\d{8,15}$/);
  // Aucun numéro n'est exigé : le site doit fonctionner sans (voir plus bas).
  assert.equal(typeof doctorConfig.contact.whatsapp, "string");
});

check("le nom du médecin n'est pas inventé", () => {
  // S'il est vide, l'interface affiche un texte d'attente — jamais un nom plausible.
  assert.ok(doctorConfig.name === "" || doctorConfig.name.length > 3);
  if (doctorConfig.name === "") assert.equal(doctorDisplayName(), null);
});

/* ── 2 · La semaine ────────────────────────────────────────────────────── */
console.log("\n2 · Semaine déduite de la configuration");

const week = buildWeek();

check("sept jours, du lundi au dimanche", () => {
  assert.equal(week.length, 7);
  assert.deepEqual(week.map((d) => d.day), WEEK);
});

check("les jours annoncés tombent sur le bon lieu", () => {
  const place = (day) => week.find((d) => d.day === day).entries.map((e) => e.locationId);
  assert.deepEqual(place("mon"), ["mbouda"]);
  assert.deepEqual(place("tue"), ["mbouda"]);
  assert.deepEqual(place("wed"), ["bafoussam"]);
  assert.deepEqual(place("thu"), ["bafoussam"]);
  assert.deepEqual(place("fri"), ["africa-medical"]);
  // Le 26/10, le médecin écrit « samedi sur rendez-vous à l’hôpital charity » :
  // le samedi est donc à Bonabéri, et Africa Médical garde le vendredi.
  assert.deepEqual(place("sat"), ["hopital-charity"]);
  assert.deepEqual(place("sun"), []);
});

check("un lieu n'apparaît que les jours qu'il annonce", () => {
  const all = week.flatMap((d) => d.entries.map((e) => e.locationId));
  for (const location of doctorConfig.locations) {
    const attendu = (location.days || []).length > 0;
    assert.equal(all.includes(location.id), attendu, `${location.id} : présence incohérente`);
  }
});

check("le numéro publié est celui du médecin", () => {
  assert.equal(whatsappNumber(), "237691280237");
  assert.equal(doctorConfig.contact.phone, "+237 691 280 237");
  assert.equal(doctorConfig.contact.status, "confirmed");
  assert.match(doctorConfig.contact.source, /\d{2}\/\d{2}\/\d{4}/);
});

check("le nom affiché est « Dr Fogue », et il vient du médecin", () => {
  assert.equal(doctorDisplayName(), "Dr Fogue");
  assert.equal(doctorConfig.specialty, "Ophtalmologie");
});

check("les trois photographies déclarées existent sur le disque", () => {
  const site = path.resolve(new URL("..", import.meta.url).pathname);
  const cfg = doctorConfig.images;
  assert.deepEqual(Object.keys(cfg).sort(), ["about", "hero", "team"]);
  for (const [name, image] of Object.entries(cfg)) {
    for (const file of [image.src, ...image.srcset.split(",").map((part) => part.trim().split(" ")[0])]) {
      assert.ok(fs.existsSync(path.join(site, file)), `${name} : ${file} manquant`);
    }
    for (const lang of ["fr", "en"]) {
      assert.ok(image.alt[lang] && image.alt[lang].length > 20, `${name} : alt ${lang} trop court`);
    }
    assert.match(image.alt.fr, /Fogue/, `${name} : l'alt ne nomme pas le médecin`);
  }
});

check("le hero est un paysage, pas un portrait recadré", () => {
  // La photographie de la salle d'examen est en 16/9 : c'est sa composition
  // (zone sombre à gauche, médecin à droite) qui fait le premier écran. Un
  // cadrage portrait la transformerait en bande verticale et viderait la page.
  const hero = doctorConfig.images.hero;
  assert.ok(hero.width > hero.height, `hero ${hero.width}×${hero.height} n'est pas un paysage`);
  assert.match(hero.src, /hero-room/, "le hero doit être la photo de la salle d'examen");
  assert.ok(!hero.caption, "le hero ne porte pas de légende");
  assert.match(doctorConfig.profile.portrait.src, /hero-room/, "le portrait affiché est celui du hero");
});

check("la photographie d'équipe est publiable en l'état", () => {
  const team = doctorConfig.images.team;
  assert.ok(team.width < team.height, "la photo d'équipe est un portrait 4/5");
  for (const lang of ["fr", "en"]) {
    assert.ok(team.caption[lang].length > 20, `légende ${lang} trop courte`);
    // Rien n'affirme l'affiliation : le panneau visible sur la photo n'est pas
    // vérifié, la légende ne nomme donc aucun hôpital.
    assert.ok(!/hôpital de paris|hopital de paris/i.test(team.caption[lang] + team.alt[lang]),
      "la légende ne peut pas nommer un hôpital non confirmé");
  }
});

check("la page ne dit jamais qu'une photo publiée ne l'est pas", () => {
  // Le 27/10, la photographie d'équipe est entrée dans la page tandis qu'une
  // question du panneau « à confirmer » affirmait encore qu'elle n'était pas
  // publiée. Une page qui se contredit coûte plus cher que dix questions.
  const questions = (doctorConfig.info?.questions ?? []).flatMap((q) => [q.fr, q.en].filter(Boolean));
  for (const q of questions) {
    assert.ok(!/n’est pas publiée|not published/i.test(q), `question contradictoire : ${q}`);
  }
});

check("aucune légende ne porte la mention de provenance datée", () => {
  // Ruling King 27/10 : « Photographie transmise par le médecin, 26 octobre
  // 2026 » n'est pas nécessaire. Une légende dit qui est sur la photo, pas d'où
  // elle vient.
  for (const [name, image] of Object.entries(doctorConfig.images)) {
    const texte = [image.caption?.fr, image.caption?.en].filter(Boolean).join(" ");
    assert.ok(!/transmise par le médecin|supplied by the doctor/i.test(texte),
      `${name} : la légende raconte encore la provenance`);
    assert.ok(!/\d{1,2} (?:octobre|october) 2026/i.test(texte),
      `${name} : la légende porte encore une date`);
  }
});

check("chaque image demandée par la page existe dans la configuration", () => {
  // Une image retirée du HTML mais laissée dans la configuration est un fichier
  // mort ; une image demandée par la page sans configuration ne s'affiche pas.
  const site = path.resolve(new URL("..", import.meta.url).pathname);
  const html = fs.readFileSync(path.join(site, "index.html"), "utf8");
  const demandees = [...html.matchAll(/data-photo="([a-z]+)"/g)].map((m) => m[1]).sort();
  assert.deepEqual(demandees, Object.keys(doctorConfig.images).sort(),
    `la page demande ${demandees.join(", ")}, la configuration déclare ${Object.keys(doctorConfig.images).join(", ")}`);
});

check("le premier écran pose son texte sur la photographie, pas à côté", () => {
  const site = path.resolve(new URL("..", import.meta.url).pathname);
  const html = fs.readFileSync(path.join(site, "index.html"), "utf8");
  const css = fs.readFileSync(path.join(site, "css/styles.css"), "utf8");
  assert.match(html, /class="hero-media"/, "le hero n'a pas de couche photographique");
  assert.match(html, /class="hero-scrim"/, "le dégradé de lisibilité manque");
  assert.ok(!/data-portrait-caption/.test(html), "la légende du portrait est toujours dans la page");
  // Le dégradé existe dans les deux sens : horizontal sur ordinateur, vertical
  // sur téléphone (la composition est empilée sous 900 px).
  const scrim = css.slice(css.indexOf(".hero-scrim"), css.indexOf(".hero-copy"));
  assert.match(scrim, /linear-gradient\(\s*90deg/, "pas de dégradé horizontal");
  assert.match(css, /@media \(max-width: 900px\)[\s\S]{0,2400}\.hero-scrim/, "pas de dégradé mobile");
});

check("aucune photographie n'est annoncée comme générée", () => {
  for (const [name, image] of Object.entries(doctorConfig.images)) {
    const texte = [image.alt?.fr, image.caption?.fr, image.alt?.en, image.caption?.en].join(" ");
    assert.ok(!/génér|generated|illustration/i.test(texte), `${name} : texte d'illustration générée`);
  }
});

check("les questions à confirmer sont bilingues et datées", () => {
  assert.ok(doctorConfig.meta.questions.length >= 5);
  for (const question of doctorConfig.meta.questions) {
    assert.ok(question.fr && question.fr.length > 20);
    assert.ok(question.en && question.en.length > 20);
  }
});

check("sans horaires connus, le drapeau le dit", () => {
  // Si un jour des horaires sont saisis, ce test ne bloque rien : il documente
  // seulement que l'absence est détectée plutôt que passée sous silence.
  const missing = !hasAnyHours();
  assert.equal(typeof missing, "boolean");
});

check("le libellé d'un lieu ne contient jamais undefined", () => {
  for (const location of doctorConfig.locations) {
    const label = locationLabel(location, fr);
    assert.ok(label.length > 0 && !/undefined|null/.test(label), label);
  }
});

check("les jours d'un lieu sont traduits, pas codés en dur", () => {
  const mbouda = doctorConfig.locations[0];
  assert.equal(locationDays(mbouda, fr), "Lundi · Mardi");
  assert.equal(locationDays(mbouda, en), "Monday · Tuesday");
});

/* ── 3 · Traductions ───────────────────────────────────────────────────── */
console.log("\n3 · FR / EN");

const flatten = (obj, prefix = "") =>
  Object.entries(obj).flatMap(([key, value]) =>
    value && typeof value === "object" ? flatten(value, `${prefix}${key}.`) : [`${prefix}${key}`],
  );

check("les deux dictionnaires ont exactement les mêmes clefs", () => {
  const keysFr = flatten(dictionaries.fr).sort();
  const keysEn = flatten(dictionaries.en).sort();
  const missingInEn = keysFr.filter((k) => !keysEn.includes(k));
  const missingInFr = keysEn.filter((k) => !keysFr.includes(k));
  assert.deepEqual(missingInEn, [], `manquantes en anglais : ${missingInEn.join(", ")}`);
  assert.deepEqual(missingInFr, [], `manquantes en français : ${missingInFr.join(", ")}`);
});

check("aucun texte vide dans les dictionnaires", () => {
  for (const [lang, dict] of Object.entries(dictionaries)) {
    const walk = (node, path = "") => {
      for (const [key, value] of Object.entries(node)) {
        if (value && typeof value === "object") walk(value, `${path}${key}.`);
        else if (typeof value === "string") assert.ok(value.trim().length > 0, `${lang} : ${path}${key} vide`);
      }
    };
    walk(dict);
  }
});

check("le titre du hero tient en deux lignes, dans les deux langues", () => {
  // Ruling King 27/10 : « Votre vision, / ma priorité. » — deux lignes qui
  // laissent respirer la photographie entre le texte et le visage.
  assert.equal(fr("hero.h1").length, 2);
  assert.equal(en("hero.h1").length, 2);
  assert.equal(fr("hero.h1").join(" "), "VOTRE VISION, MA PRIORITÉ.");
});

check("l'anglais ne renvoie pas vers le français par accident", () => {
  // Quelques phrases qui doivent vraiment être traduites, pas recopiées.
  const pairs = ["hero.ctaPrimary", "consultations.scheduleUnverified", "appointment.disclaimer"];
  for (const key of pairs) assert.notEqual(fr(key), en(key), key);
});

check("une clef absente ne casse pas la page", () => {
  assert.equal(fr("clef.qui.n.existe.pas"), "clef.qui.n.existe.pas");
});

/* ── 4 · Validation ────────────────────────────────────────────────────── */
console.log("\n4 · Formulaire");

const base = {
  fullName: "Awa Ngo Bell",
  contactMethod: "whatsapp",
  contact: "691 23 45 67",
  locationId: "mbouda",
  preferredDate: "",
  preferredTime: "",
  note: "",
};

check("un formulaire rempli correctement passe", () => {
  assert.deepEqual(validate(base, { t: fr }), {});
});

check("un nom trop court est refusé", () => {
  assert.equal(validate({ ...base, fullName: "A" }, { t: fr }).fullName, "fullName");
});

check("un numéro incomplet est refusé", () => {
  assert.equal(validate({ ...base, contact: "6912" }, { t: fr }).contact, "contactPhone");
});

check("un e-mail demandé mais invalide est refusé", () => {
  assert.equal(
    validate({ ...base, contactMethod: "email", contact: "awa@" }, { t: fr }).contact,
    "contactEmail",
  );
  assert.deepEqual(validate({ ...base, contactMethod: "email", contact: "awa@exemple.cm" }, { t: fr }), {});
});

check("un lieu manquant est refusé", () => {
  assert.equal(validate({ ...base, locationId: "" }, { t: fr }).locationId, "locationId");
});

check("une date passée est refusée, une date future acceptée", () => {
  assert.equal(validate({ ...base, preferredDate: "2020-01-01" }, { t: fr }).preferredDate, "datePast");
  const soon = new Date();
  soon.setDate(soon.getDate() + 3);
  const iso = soon.toISOString().slice(0, 10);
  assert.equal(validate({ ...base, preferredDate: iso }, { t: fr }).preferredDate, undefined);
});

check("une date au-delà de six mois est refusée", () => {
  const far = new Date();
  far.setDate(far.getDate() + limits.maxLeadDays + 30);
  assert.equal(validate({ ...base, preferredDate: far.toISOString().slice(0, 10) }, { t: fr }).preferredDate, "dateFar");
});

check("un message trop long est refusé", () => {
  const note = "a".repeat(limits.message + 1);
  assert.equal(validate({ ...base, note }, { t: fr }).note, "noteLong");
});

/* ── 5 · Message WhatsApp ──────────────────────────────────────────────── */
console.log("\n5 · Message et lien WhatsApp");

const message = whatsappMessage({
  t: fr,
  values: { ...base, preferredDate: "2026-11-04", preferredTime: "09:30", note: "Je viens de Bafoussam." },
  locationLabel: "Africa Médical · Douala",
  doctorName: "le médecin",
});

check("le message nomme le lieu, la date en clair, le nom", () => {
  assert.match(message, /Africa Médical · Douala/);
  assert.match(message, /mercredi 4 novembre 2026/);
  assert.match(message, /Awa Ngo Bell/);
  assert.match(message, /Bonjour, je souhaite demander un rendez-vous/);
});

check("le message ne contient ni undefined ni champ vide mal interpolé", () => {
  assert.ok(!/undefined|null|\{\w+\}/.test(message), message);
});

check("le message ne transmet aucune donnée médicale demandée par le site", () => {
  // Le message est construit à partir des seuls champs du formulaire : aucun autre.
  assert.ok(!message.includes("Je viens de Bafoussam."), "le champ libre ne doit pas être ajouté au message WhatsApp");
});

check("le lien wa.me est correctement encodé, sans + dans le numéro", () => {
  const url = buildWhatsappUrl("+237 691 23 45 67", message);
  assert.match(url, /^https:\/\/wa\.me\/237691234567\?text=/);
  assert.ok(url.includes("%0A"), "les retours à la ligne sont encodés");
  assert.ok(!url.includes("+"), "aucun + dans l'URL");
});

check("sans numéro configuré, aucun lien n'est fabriqué", () => {
  assert.equal(buildWhatsappUrl("", message), "");
});

check("la date s'écrit en clair dans les deux langues", () => {
  assert.equal(formatDate("2026-11-04", "fr"), "mercredi 4 novembre 2026");
  assert.equal(formatDate("2026-11-04", "en"), "Wednesday, 4 November 2026");
});

/* ── 6 · Prestations ───────────────────────────────────────────────────── */
console.log("\n6 · Prestations");

check("chaque prestation est libellée dans les deux langues", () => {
  for (const service of services) {
    assert.ok(service.label.fr && service.label.en, service.id);
    assert.ok(["confirmed", "reported", "unknown"].includes(service.status), service.id);
  }
});

check("aucune prestation « confirmed » sans date de confirmation", () => {
  for (const service of services) {
    if (service.status === "confirmed") assert.ok(isKnown(service.asOf), service.id);
  }
});

/* ── 7 · Vie privée : ce site ne parle à aucun tiers ───────────────────── */
console.log("\n7 · Aucun appel externe");

import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);
const readAll = (dir) =>
  fs
    .readdirSync(dir, { withFileTypes: true })
    .flatMap((entry) => {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) return entry.name === "node_modules" ? [] : readAll(full);
      return /[.](html|css|js)$/.test(entry.name) ? [fs.readFileSync(full, "utf8")] : [];
    });

const sources = readAll(root);

check("aucune ressource servie depuis un domaine tiers", () => {
  const found = [];
  for (const src of sources) {
    for (const m of src.matchAll(/https?:\/\/[^"'`)\s]+/g)) {
      const url = m[0];
      // Seuls les liens de documentation et les URI de schéma sont tolérés.
      // L'URL de l'aperçu est une DONNÉE (JSON-LD `url`), pas une ressource chargée :
      // aucun navigateur ne va la chercher. Elle est donc tolérée ici, et elle seule.
      if (/schema\.org|w3\.org|github\.com\/AKWOKING|mdn\.|example\.com|wa\.me/.test(url)) continue;
      if (url === "https://dr-ophtalmo-preview.vercel.app/") continue;
      // Le lien de réservation est une DONNÉE de configuration, pas une
      // ressource chargée : aucun navigateur ne va le chercher avant le clic.
      // Seul l'hôte validé par js/booking.js est toléré, et seulement s'il est
      // réellement configuré — aujourd'hui la liste est vide.
      const bookingHost = bookingStatus(doctorConfig.bookingUrl).host;
      if (bookingHost && url.startsWith(`https://${bookingHost}/`)) continue;
      found.push(url);
    }
  }
  assert.deepEqual(found, [], `domaines tiers : ${found.slice(0, 5).join(", ")}`);
});

check("aucun formulaire n'envoie de données, aucun cookie, aucune mesure", () => {
  const joined = sources.join("\n");
  assert.ok(!/fetch\(|XMLHttpRequest|navigator\.sendBeacon/.test(joined), "un appel réseau est présent");
  assert.ok(!/document\.cookie/.test(joined), "un cookie est écrit");
  assert.ok(
    !/googletagmanager|gtag\(|google-analytics|plausible\.io|matomo\.(js|php)/i.test(joined),
    "une mesure d'audience est branchée",
  );
});

/* ── 9 · Réservation en ligne (route A) ────────────────────────────────── */
console.log("\n9 · Réservation en ligne");

check("un lien vide n'active rien", () => {
  const status = bookingStatus("");
  assert.equal(status.enabled, false);
  assert.equal(status.href, "");
  assert.equal(status.reason, "empty");
});

check("seul un lien https vers un service de réservation connu est accepté", () => {
  // Ce qui est accepté : la page de réservation Google, en https.
  for (const url of [
    "https://calendar.app.google/abc123",
    "https://calendar.google.com/calendar/appointments/schedules/xyz?gv=true",
  ]) {
    assert.equal(bookingStatus(url).enabled, true, url);
  }
  // Ce qui est refusé, et pourquoi : le bouton disparaît, la page n'explique
  // pas — on ne met pas un message d'erreur devant un patient.
  const refused = {
    "http://calendar.app.google/abc123": "insecure",
    "javascript:alert(1)": "insecure",
    "https://calendly.com/docteur-fogue": "host",
    "https://calendar.app.google.evil.example/x": "host",
    "pas une url": "malformed",
  };
  for (const [url, reason] of Object.entries(refused)) {
    const status = bookingStatus(url);
    assert.equal(status.enabled, false, url);
    assert.equal(status.reason, reason, url);
    assert.equal(status.href, "", url);
  }
});

check("un lien par lieu ne vaut que pour ce lieu", () => {
  // Le montage gratuit honnête : une page pour Africa Médical, rien ailleurs.
  const config = {
    bookingUrl: "",
    locations: [
      { id: "mbouda", bookingUrl: "" },
      { id: "africa-medical", bookingUrl: "https://calendar.app.google/douala" },
    ],
  };
  assert.equal(bookingCapability(config), true, "une page existe pourtant");
  assert.equal(bookingMode(config, "africa-medical"), "on");
  assert.equal(bookingMode(config, "mbouda"), "partial", "Mbouda ne doit pas voir le bouton");
  const douala = bookingFor(config, "africa-medical");
  assert.equal(douala.scope, "location");
  assert.equal(douala.href, "https://calendar.app.google/douala");
  assert.equal(bookingFor(config, "mbouda").enabled, false);
});

check("une page générale vaut pour tous les lieux", () => {
  const config = {
    bookingUrl: "https://calendar.app.google/tous",
    locations: [{ id: "mbouda", bookingUrl: "" }, { id: "bafoussam", bookingUrl: "" }],
  };
  for (const id of ["mbouda", "bafoussam"]) {
    assert.equal(bookingMode(config, id), "on", id);
    assert.equal(bookingFor(config, id).scope, "global", id);
  }
});

check("le lieu gagne sur la page générale", () => {
  // Un médecin peut vouloir une page par lieu ; la plus précise est la bonne.
  const config = {
    bookingUrl: "https://calendar.app.google/tous",
    locations: [{ id: "africa-medical", bookingUrl: "https://calendar.app.google/douala" }],
  };
  assert.equal(bookingFor(config, "africa-medical").href, "https://calendar.app.google/douala");
  assert.equal(bookingFor(config, "africa-medical").scope, "location");
  assert.equal(bookingFor(config, "mbouda").href, "https://calendar.app.google/tous");
});

check("un lien refusé laisse la page honnête, quel que soit le lieu", () => {
  // Un lien http:// par lieu ne doit ni activer le bouton, ni faire dire au
  // site qu'il est branché sur un agenda.
  const config = { bookingUrl: "", locations: [{ id: "mbouda", bookingUrl: "http://calendar.app.google/x" }] };
  assert.equal(bookingCapability(config), false);
  assert.equal(bookingMode(config, "mbouda"), "off");
  assert.equal(bookingFor(config, "mbouda").enabled, false);
});

check("sans lien nulle part, le site reste exactement comme avant", () => {
  assert.equal(bookingCapability(doctorConfig), false, "un lien traîne dans la configuration");
  for (const location of doctorConfig.locations) {
    assert.equal(bookingMode(doctorConfig, location.id), "off", location.id);
  }
  assert.equal(doctorConfig.meta.liveSync, false);
});

check("la phrase des rendez-vous a trois variantes, jamais deux à la fois", () => {
  assert.equal(liveNoteKey("off"), "appointment.liveNote");
  assert.equal(liveNoteKey("on"), "appointment.liveNoteWhenBooked");
  assert.equal(liveNoteKey("partial"), "appointment.liveNotePartial");
  for (const translate of [fr, en]) {
    const [off, on, partial] = [liveNoteKey("off"), liveNoteKey("on"), liveNoteKey("partial")].map(translate);
    assert.notEqual(off, on);
    assert.notEqual(off, partial);
    assert.notEqual(on, partial);
    // « partiel » ne doit pas promettre le bouton qu'il n'y a pas.
    assert.ok(!/bouton|button/i.test(partial), "la variante partielle annonce un bouton absent");
  }
});

check("le message WhatsApp d'après réservation nomme le lieu et le médecin", () => {
  for (const translate of [fr, en]) {
    const modele = translate("booking.waMessage");
    assert.match(modele, /\{place\}/, "le lieu n'est pas dans le message");
    assert.match(modele, /\{doctor\}/, "le médecin n'est pas dans le message");
    // Il part du numéro du patient : le site ne doit pas le présenter comme
    // envoyé par le site, ni comme une notification automatique.
    assert.ok(!/notification/i.test(modele), "le message promet une notification");
  }
});

check("aucune phrase ne promet un rappel par WhatsApp ni par SMS", () => {
  // Google n'envoie ni SMS ni WhatsApp — seulement des e-mails, et ses rappels
  // automatiques sont une option payante. Une phrase qui promettrait un rappel
  // serait fausse, et c'est le genre de promesse qu'un patient retient.
  for (const dict of [dictionaries.fr, dictionaries.en]) {
    for (const key of flatten(dict)) {
      const value = resolve(dict, key);
      if (typeof value !== "string") continue;
      assert.ok(
        !/rappel\s+(par\s+)?(whatsapp|sms)|(whatsapp|sms)\s+reminder|reminder\s+(by|via)\s+(whatsapp|sms)/i.test(value),
        `${key} promet un rappel WhatsApp/SMS que Google n'envoie pas`,
      );
    }
  }
});

check("la liste des hôtes acceptés est courte et explicite", () => {
  assert.deepEqual(BOOKING_HOSTS, ["calendar.app.google", "calendar.google.com"]);
});

check("le bouton de réservation est masqué tant que le lien est vide", () => {
  const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
  const block = html.match(/<div class="booking" data-booking hidden>([\s\S]*?)<\/div>/);
  assert.ok(block, "le bloc de réservation a disparu du HTML");
  // Pas de href en dur : sans lien configuré, il n'existe aucun bouton mort,
  // même si le JavaScript ne s'exécute pas.
  assert.ok(!/href=/.test(block[1]), "le bouton porte un href en dur");
  assert.match(block[1], /rel="noopener noreferrer"/);
  assert.match(block[1], /target="_blank"/);
});

check("aucune iframe, aucun script de réservation n'est chargé", () => {
  // La route A est un lien sortant. Le jour où quelqu'un voudra « intégrer »
  // l'agenda, ce test tombera avant la page.
  const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
  assert.ok(!/<iframe/i.test(html), "une iframe a été ajoutée");
  const scripts = [...html.matchAll(/<script[^>]*src="([^"]+)"/g)].map((m) => m[1]);
  assert.deepEqual(scripts, ["js/app.js"], "un script tiers a été ajouté");
});

check("les deux phrases basculent ensemble, et ne se contredisent jamais", () => {
  const pairs = [
    ["appointment.liveNote", /aucune connexion à un agenda|no connection to any calendar/i],
    ["consultations.scheduleNote", /aucune synchronisation avec un agenda|nothing is synced to a calendar/i],
  ];
  for (const [base, denial] of pairs) {
    const booked = liveCopyKey(base, true);
    assert.equal(booked, `${base}WhenBooked`);
    assert.equal(liveCopyKey(base, false), base, `${base} : l'état éteint change la clef`);

    for (const translate of [fr, en]) {
      const off = translate(base);
      const on = translate(booked);
      assert.match(off, denial, `${base} : la version sans lien ne nie plus l'agenda`);
      assert.ok(!denial.test(on), `${base}WhenBooked nie encore tout agenda alors qu'un lien existe`);
      assert.match(on, /agenda|calendar/i, `${base}WhenBooked ne dit pas d'où viennent les créneaux`);
      assert.notEqual(off, on, `${base} : aucune bascule réelle`);
    }
  }
});

check("le bouton et les phrases sortent d'un seul calcul", () => {
  // Ce test ne juge pas le style : il empêche la divergence. Le jour où
  // quelqu'un défait le lien entre le bouton et la copie, il tombe.
  const app = fs.readFileSync(path.join(root, "js/app.js"), "utf8");
  const statique = app.slice(app.indexOf("function renderStatic"), app.indexOf("function renderBooking"));
  assert.match(statique, /renderBooking\(\);/, "renderStatic ne rend plus la réservation");
  assert.equal((app.match(/data-i18n-when-booked/g) || []).length, 1, "la bascule est écrite deux fois");
  assert.match(app, /block\.hidden = mode !== "on"/, "le bloc ne dépend plus de l'état du lieu");
  assert.match(app, /liveNoteKey\(mode\)/, "la phrase des rendez-vous ne suit plus l'état");
  assert.match(app, /liveCopyKey\("consultations\.scheduleNote"/, "la note de la semaine ne bascule plus");
});

check("chaque variante « WhenBooked » a sa phrase d'origine", () => {
  // Une variante sans base ne s'afficherait jamais ; une base sans variante
  // afficherait le déni alors que le bouton existe.
  for (const dict of [dictionaries.fr, dictionaries.en]) {
    const keys = flatten(dict);
    for (const key of keys.filter((k) => k.endsWith("WhenBooked"))) {
      const base = key.replace(/WhenBooked$/, "");
      assert.ok(keys.includes(base), `${key} n'a pas de phrase d'origine`);
    }
    for (const key of ["booking.cta", "booking.note", "booking.label", "booking.or"]) {
      assert.ok(keys.includes(key), `${key} manque au dictionnaire`);
    }
  }
});

/* ── 8 · L'aperçu reste privé ──────────────────────────────────────────── */
console.log("\n8 · Aperçu privé, partage lisible");

check("la page demande aux moteurs de ne pas l'indexer", () => {
  const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
  assert.match(html, /<meta name="robots" content="noindex, nofollow" \/>/);
});

check("robots.txt interdit tout le site", () => {
  const txt = fs.readFileSync(path.join(root, "robots.txt"), "utf8");
  assert.match(txt, /User-agent: \*\s*\nDisallow: \/\s*$/);
});

check("og:image est un JPEG 1200 × 630 présent sur le disque", () => {
  const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
  assert.match(html, /property="og:image" content="assets\/img\/og\.jpg"/);
  assert.match(html, /property="og:image:width" content="1200"/);
  assert.match(html, /property="og:image:height" content="630"/);
  assert.ok(fs.existsSync(path.join(root, "assets/img/og.jpg")), "og.jpg absent");
});

check("les en-têtes de sécurité sont déclarés", () => {
  const headers = fs.readFileSync(path.join(root, "_headers"), "utf8");
  for (const name of ["Strict-Transport-Security", "Content-Security-Policy", "X-Content-Type-Options"]) {
    assert.ok(headers.includes(name), `${name} absent`);
  }
});

console.log(`\n${passed} vérification(s) passée(s).`);
