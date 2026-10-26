/**
 * ─────────────────────────────────────────────────────────────────────────────
 * SOURCE UNIQUE — identité, photographies et lieux de consultation
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
 *
 * MISE À JOUR DU 26/10/2026 (soir) — le médecin a été identifié et a parlé :
 *   · il est le Dr FOGUE, ophtalmologue (message WhatsApp du 26/10, 17:26 :
 *     « je ne suis pas opticien patron », « par contre je suis ophtalmologue ») ;
 *   · son numéro est le 691 280 237, donné sur son affiche et dans la
 *     conversation — c'est le numéro du médecin, pas celui d'un opticien ;
 *   · ses jours de consultation sont dans sa phrase du 26/10, 17:53, citée
 *     sous chaque lieu. Aucune heure n'y figure : elles restent vides.
 */

const WHATSAPP = "237691280237";
const PHONE = "+237 691 280 237";

export const doctorConfig = {
  /* ── Identité professionnelle ───────────────────────────────────────────── */
  name: "Fogue",
  title: "Dr",
  specialty: "Ophtalmologie",
  specialtyStatus: "confirmed", // « par contre je suis ophtalmologue », 26/10 17:26

  // Rien de ce qui suit n'a été communiqué : qualifications, inscription à
  // l'Ordre, années d'exercice, biographie, intérêts cliniques, langues.
  profile: {
    qualifications: [],
    registration: "",
    languages: [],
    interests: [],
    bio: "",
    portrait: {
      // La photographie réelle du médecin, transmise par lui le 26/10/2026.
      src: "assets/img/dr-fogue-hero-960.webp",
      srcset:
        "assets/img/dr-fogue-hero-640.webp 640w, assets/img/dr-fogue-hero-960.webp 960w, assets/img/dr-fogue-hero-1440.webp 1440w",
      width: 960,
      height: 1474,
      alt: {
        fr: "Le Dr Fogue, ophtalmologue, en blouse blanche sur fond bleu.",
        en: "Dr Fogue, ophthalmologist, in a white coat against a blue background.",
      },
      isRealPhoto: true,
      caption: {
        fr: "Le Dr Fogue, ophtalmologue. Photographie transmise par le médecin, 26 octobre 2026.",
        en: "Dr Fogue, ophthalmologist. Photograph supplied by the doctor, 26 October 2026.",
      },
    },
  },

  /**
   * Les trois photographies du médecin, chacune à sa place.
   * Aucune image générée ne subsiste sur le site : ce que le visiteur voit,
   * c'est le médecin lui-même.
   */
  images: {
    hero: {
      src: "assets/img/dr-fogue-hero-960.webp",
      srcset:
        "assets/img/dr-fogue-hero-640.webp 640w, assets/img/dr-fogue-hero-960.webp 960w, assets/img/dr-fogue-hero-1440.webp 1440w",
      width: 960,
      height: 1474,
      alt: {
        fr: "Portrait du Dr Fogue, ophtalmologue, en blouse blanche et lunettes, sur fond bleu.",
        en: "Portrait of Dr Fogue, ophthalmologist, wearing glasses and a white coat against a blue background.",
      },
    },
    about: {
      src: "assets/img/dr-fogue-cabinet-960.webp",
      srcset:
        "assets/img/dr-fogue-cabinet-640.webp 640w, assets/img/dr-fogue-cabinet-960.webp 960w, assets/img/dr-fogue-cabinet-1440.webp 1440w",
      width: 960,
      height: 812,
      alt: {
        fr: "Le Dr Fogue en blouse blanche et stéthoscope, devant un mur turquoise, lors d’une consultation.",
        en: "Dr Fogue in a white coat with a stethoscope, in front of a turquoise wall, during a consultation.",
      },
      caption: {
        fr: "Le Dr Fogue en consultation. Photographie transmise par le médecin, 26 octobre 2026.",
        en: "Dr Fogue during a consultation. Photograph supplied by the doctor, 26 October 2026.",
      },
    },
    consultation: {
      src: "assets/img/dr-fogue-consultation-720.webp",
      srcset:
        "assets/img/dr-fogue-consultation-480.webp 480w, assets/img/dr-fogue-consultation-720.webp 720w",
      width: 720,
      height: 1400,
      alt: {
        fr: "Le Dr Fogue en tenue de consultation bleue, souriant, dans une salle d’examen.",
        en: "Dr Fogue in blue clinical scrubs, smiling, in an examination room.",
      },
      caption: {
        fr: "Le Dr Fogue en consultation. Affiche du cabinet, recadrée — 26 octobre 2026.",
        en: "Dr Fogue in consultation. Practice poster, cropped — 26 October 2026.",
      },
    },
  },

  /* ── Contact ────────────────────────────────────────────────────────────── */
  contact: {
    // Format international pour wa.me : chiffres seulement, sans « + » (237…).
    whatsapp: WHATSAPP,
    phone: PHONE,
    email: "",
    coordinatorName: "",
    status: "confirmed",
    asOf: "2026-10-26",
    source:
      "Affiche du cabinet (« Contact: 691280237 ») et conversation WhatsApp du 26/10/2026 — numéro donné par le médecin lui-même.",
  },

  /* ── Quatre lieux de consultation ────────────────────────────────────────
   * Les jours viennent de la phrase du médecin du 26/10, citée dans `source`.
   * Elle ne donne AUCUNE heure : `hours` reste vide et l'écran le dit.
   * Le samedi est noté « sur rendez-vous » parce que c'est sa formulation
   * exacte — pas une heure d'ouverture inventée.
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
      days: ["fri"],
      hours: "",
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « africa médical situé à l’ancien dépôt guinès et douala vendredi samedi sur rendez-vous à l’hôpital charity … ».",
      schedule: [],
    },
    {
      id: "hopital-charity",
      order: "04",
      city: "Bonabéri, Douala",
      facility: "Hôpital Charity — Medical Assurance Center",
      address: "Grand Hangar, Bloc 7, Bonabéri",
      mapUrl: "",
      contactPhone: "",
      days: ["sat"],
      hours: {
        fr: "Sur rendez-vous",
        en: "By appointment",
      },
      status: "reported",
      asOf: "2026-10-26",
      source:
        "Message du médecin, 26/10/2026 17:53 — « samedi sur rendez-vous à l’hôpital charity médical assurance center situé à bonaberie grand hagard bloc7 ». L’heure d’ouverture n’est pas communiquée.",
      schedule: [],
    },
  ],

  /* ── Méta ───────────────────────────────────────────────────────────────── */
  meta: {
    // Date de la dernière information entrée dans ce fichier. Affichée sous le
    // tableau des jours : « informations communiquées le … — à reconfirmer ».
    infoAsOf: "2026-10-26",
    infoSource: "Message du médecin, 26/10/2026 17:53 (WhatsApp) + affiche du cabinet.",
    // Le site ne prétend pas être branché sur un agenda : aucune synchronisation
    // n'existe. Ce champ l'écrit en clair, pour que l'écran ne l'oublie pas.
    liveSync: false,
    /**
     * Les questions à poser au médecin avant de publier le site pour de bon.
     * Elles s'affichent dans le panneau « Informations à publier », et aucune
     * n'est résolue en silence : ce qui n'est pas répondu reste « à confirmer ».
     */
    questions: [
      {
        fr: "L’affiche du cabinet annonce « vendredi, Douala, Bonabéri Grand Hangar Bloc 7, 8 h à 15 h », alors que votre message place le vendredi à Africa Médical et le samedi à l’hôpital Charity. Laquelle des deux est la bonne ?",
        en: "The practice poster says “Friday, Douala, Bonabéri Grand Hangar Bloc 7, 8 am to 3 pm”, while your message puts Friday at Africa Médical and Saturday at Hôpital Charity. Which one is right?",
      },
      {
        fr: "Les horaires d’ouverture des quatre lieux (aucun n’a été communiqué).",
        en: "Opening hours for the four locations (none has been provided).",
      },
      {
        fr: "L’adresse exacte à Mbouda et à Bafoussam (la ville seule est connue).",
        en: "The exact address in Mbouda and Bafoussam (only the city is known).",
      },
      {
        fr: "Le nom à publier : « Dr Fogue » suffit-il, ou faut-il le nom complet ?",
        en: "The name to publish: is “Dr Fogue” enough, or should the full name appear?",
      },
      {
        fr: "L’inscription à l’Ordre national des médecins du Cameroun, si vous souhaitez la publier.",
        en: "Registration with the National Order of Physicians of Cameroon, if you want it published.",
      },
      {
        fr: "Les langues de consultation (français, anglais, autres).",
        en: "Consultation languages (French, English, others).",
      },
      {
        fr: "La photographie d’équipe transmise porte un panneau « Hôpital de Paris » : elle n’est pas publiée tant que son origine n’est pas confirmée par vous.",
        en: "The team photograph supplied shows an “Hôpital de Paris” sign: it is not published until you confirm where it was taken.",
      },
    ],
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
