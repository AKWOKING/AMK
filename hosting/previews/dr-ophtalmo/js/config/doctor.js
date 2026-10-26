/**
 * ─────────────────────────────────────────────────────────────────────────────
 * SOURCE UNIQUE — identité et lieux de consultation
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * RÈGLE DU FICHIER : une chaîne vide veut dire « information non communiquée ».
 * Elle ne veut JAMAIS dire « à remplacer par une valeur plausible ». Le site
 * affiche « à confirmer » et n'invente rien : ni jour, ni adresse, ni diplôme,
 * ni numéro, ni année d'expérience, ni titre hospitalier.
 *
 * Deux champs de statut, et ils ne veulent pas dire la même chose :
 *   status: "confirmed" → le médecin a confirmé, à la date `asOf`
 *   status: "reported"  → le médecin l'a communiqué, mais la confirmation manque
 *   status: "unknown"   → rien n'a été communiqué
 *
 * La provenance de chaque information est écrite dans `source`. Un lecteur du
 * dépôt doit pouvoir remonter d'une ligne affichée à la phrase qui l'a produite.
 */

export const doctorConfig = {
  /* ── Identité professionnelle ───────────────────────────────────────────── */
  // Nom complet et titre : non communiqués à ce jour.
  name: "",
  title: "",
  specialty: "Médecine ophtalmologique",
  specialtyStatus: "reported", // donné dans la demande de King, 26/10

  // Rien de ce qui suit n'a été communiqué : qualifications, inscription à
  // l'Ordre, années d'exercice, biographie, intérêts cliniques, langues.
  profile: {
    qualifications: [], // ex. ["Doctorat en médecine, Faculté de médecine …"]
    registration: "", // ex. « N° 000/2019 — Ordre national des médecins du Cameroun »
    languages: [],
    interests: [],
    bio: "",
    portrait: {
      src: "assets/img/portrait-960.webp",
      srcset:
        "assets/img/portrait-640.webp 640w, assets/img/portrait-960.webp 960w, assets/img/portrait-1440.webp 1440w",
      alt: {
        fr: "Portrait d’illustration : une ophtalmologue en blouse blanche dans une salle de consultation lumineuse.",
        en: "Illustrative portrait: an ophthalmologist in a white coat in a bright consultation room.",
      },
      // Cette image est générée. Elle ne doit jamais être présentée comme la
      // photo du médecin : la légende le dit à l'écran, et `isRealPhoto`
      // commande la mention.
      isRealPhoto: false,
      caption: {
        fr: "Portrait d’illustration (image générée) — il sera remplacé par la photographie du médecin.",
        en: "Illustrative portrait (generated image) — to be replaced by the doctor’s own photograph.",
      },
    },
  },

  /* ── Contact ────────────────────────────────────────────────────────────── */
  // Aucun numéro vérifié à ce jour. Le numéro de la boutique « Africa Optic »
  // qui a transmis le message n'est PAS le numéro du médecin : il n'entre pas ici.
  contact: {
    // Format international pour wa.me : chiffres seulement, sans « + » (237…).
    whatsapp: "",
    phone: "",
    email: "",
    coordinatorName: "", // « secrétariat / coordinateur de rendez-vous », si connu
    status: "unknown",
    asOf: "",
    source: "",
  },

  /* ── Quatre lieux de consultation ────────────────────────────────────────
   * `days` et `hours` viennent de la phrase du médecin du 26/10, citée dans
   * `source`. Elle ne dit pas d'heures, et elle ne donne pas de jour pour
   * l'hôpital Charity : les deux restent vides, et l'écran le dit.
   */
  locations: [
    {
      id: "mbouda",
      order: "01",
      city: "Mbouda",
      facility: "",
      address: "",
      mapUrl: "",
      contactPhone: "",
      days: ["mon", "tue"],
      hours: "",
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « je consulte à mbouda le lundi mardi ».",
      schedule: [],
    },
    {
      id: "bafoussam",
      order: "02",
      city: "Bafoussam",
      facility: "",
      address: "",
      mapUrl: "",
      contactPhone: "",
      days: ["wed", "thu"],
      hours: "",
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « bafoussam mercredi jeudi ».",
      schedule: [],
    },
    {
      id: "africa-medical",
      order: "03",
      city: "Douala",
      facility: "Africa Médical",
      address: "Ancien dépôt Guinness, Douala",
      mapUrl: "",
      contactPhone: "",
      days: ["fri", "sat"],
      hours: "",
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « africa médical situé à l’ancien dépôt guinness et douala vendredi samedi ».",
      schedule: [],
    },
    {
      id: "hopital-charity",
      order: "04",
      city: "Bonabéri, Douala",
      facility: "Hôpital Charity",
      address: "Grand Hangar, Bloc 7, Bonabéri",
      mapUrl: "",
      contactPhone: "",
      days: [], // non communiqués
      hours: "",
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « rendez-vous à l’hôpital charity médical assurance center situé à bonaberie grand hagard bloc7 ». Aucun jour n’y est attaché : le message ne dit pas si le médecin y consulte, ou si on y prend seulement les rendez-vous.",
      schedule: [],
    },
  ],

  /* ── Méta ───────────────────────────────────────────────────────────────── */
  meta: {
    // Date de la dernière information entrée dans ce fichier. Affichée sous le
    // tableau des jours : « informations communiquées le … — à reconfirmer ».
    infoAsOf: "2026-10-26",
    infoSource: "Message du médecin, 26/10/2026 17:53 (WhatsApp).",
    // Le site ne prétend pas être branché sur un agenda : aucune synchronisation
    // n'existe. Ce champ l'écrit en clair, pour que l'écran ne l'oublie pas.
    liveSync: false,
  },
};

/* ── Petits lecteurs, utilisés partout ───────────────────────────────────── */

/** Une valeur est « connue » si c'est une chaîne non vide (ou une liste non vide). */
export const isKnown = (value) =>
  Array.isArray(value) ? value.length > 0 : typeof value === "string" && value.trim() !== "";

/** Nom affichable, ou null si le nom n'a pas été communiqué. */
export const doctorDisplayName = (config = doctorConfig) =>
  isKnown(config.name) ? [config.title, config.name].filter(isKnown).join(" ") : null;

/** Numéro WhatsApp utilisable : chiffres seulement, 8 à 15 (format wa.me). */
export const whatsappNumber = (config = doctorConfig) =>
  String(config.contact.whatsapp || "").replace(/\D/g, "");
