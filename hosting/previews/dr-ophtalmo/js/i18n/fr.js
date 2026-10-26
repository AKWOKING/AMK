/**
 * FRANÇAIS — la langue de départ.
 * Écrit pour des patients au Cameroun : phrases courtes, pas de jargon
 * administratif, et on dit franchement ce qu'on ne sait pas encore.
 */
export const fr = {
  meta: {
    lang: "fr",
    title: "Médecine ophtalmologique au Cameroun — consultations à Mbouda, Bafoussam, Douala et Bonabéri",
    description:
      "Site professionnel d’un médecin ophtalmologue itinérant au Cameroun : lieux et jours de consultation, demande de rendez-vous par WhatsApp ou téléphone.",
  },

  common: {
    skip: "Aller au contenu",
    brand: "Médecine ophtalmologique",
    brandSub: "Cameroun",
    doctorFallback: "le médecin",
    unknown: "À confirmer",
    reported: "Communiqué",
    confirmed: "Confirmé",
    close: "Fermer",
    menu: "Menu",
    openMenu: "Ouvrir le menu",
    closeMenu: "Fermer le menu",
    language: "Langue",
    switchTo: "Passer en anglais",
    required: "obligatoire",
    optional: "facultatif",
    backToTop: "Revenir en haut",
    emDash: "—",
    today: "Aujourd’hui",
  },

  nav: {
    label: "Navigation principale",
    home: "Accueil",
    doctor: "Le médecin",
    consultations: "Consultations",
    appointments: "Rendez-vous",
  },

  hero: {
    eyebrow: "MÉDECINE OPHTALMOLOGIQUE · CAMEROUN",
    h1: ["VOTRE", "VISION,", "MA PRIORITÉ."],
    lead:
      "«Un médecin ophtalmologue à votre écoute, avec des consultations dans plusieurs villes et structures médicales au Cameroun.»",
    ctaPrimary: "Trouver un lieu de consultation",
    ctaSecondary: "Découvrir le médecin",
    placesLabel: "Lieux de consultation",
    places: "Mbouda · Bafoussam · Douala · Bonabéri",
    placesNote:
      "Ces villes sont des lieux de consultation. Elles ne veulent pas dire que le médecin consulte chaque jour dans chacune.",
    portraitCaption:
      "Portrait d’illustration (image générée) — il sera remplacé par la photographie du médecin.",
    statusLine: "Informations communiquées le 26 octobre 2026 — à reconfirmer avant tout déplacement.",
  },

  parcours: {
    kicker: "À PROPOS DU MÉDECIN",
    title: "«Une expertise médicale, plusieurs lieux de consultation.»",
    p1:
      "«Parce que l’accès aux soins visuels ne se limite pas à une seule adresse, le Dr [NOM DU MÉDECIN] propose des consultations dans plusieurs villes et structures médicales, selon un calendrier défini.»",
    p2:
      "«Ce site rassemble les informations essentielles pour vous aider à identifier le lieu de consultation adapté, à préparer votre visite et à contacter le bon interlocuteur.»",
    profileTitle: "Fiche professionnelle",
    profileNote:
      "Seules les informations communiquées par le médecin figurent ici. Aucun diplôme, aucune inscription, aucune expérience n’est inventée pour remplir la page.",
    labels: {
      name: "Nom et titre professionnels",
      specialty: "Spécialité",
      qualifications: "Formation et diplômes",
      registration: "Inscription professionnelle",
      languages: "Langues parlées",
      interests: "Intérêts cliniques",
      bio: "Biographie",
      services: "Prestations",
    },
    placeholders: {
      name: "Nom du médecin à publier",
      qualifications: "Diplômes à publier après vérification",
      registration: "Numéro d’inscription à publier après vérification",
      languages: "Langues à communiquer",
      interests: "Intérêts cliniques à communiquer",
      bio: "Biographie à recevoir du médecin",
    },
    servicesNotice:
      "La liste des actes pratiqués sera publiée après confirmation du médecin. En cas de doute, posez la question au moment de la prise de rendez-vous.",
    examinationCaption:
      "Examen de la vue en salle de consultation — photographie d’illustration (image générée), sans lien avec une structure partenaire en particulier.",
    equipmentCaption:
      "Lampe à fente et fauteuil d’examen — photographie d’illustration (image générée).",
    photoNote:
      "Les photographies de cette page sont des illustrations générées. Elles ne montrent ni le médecin, ni un lieu partenaire précis.",
  },

  consultations: {
    kicker: "LIEUX ET JOURS DE CONSULTATION",
    title: "«Où consulter le médecin ?»",
    lead:
      "«Retrouvez les lieux de consultation et les jours de présence du médecin. Vérifiez les informations avant votre déplacement et demandez un rendez-vous pour la structure concernée.»",
    selectLabel: "Choisir un lieu",
    selected: "Lieu sélectionné",
    requestCta: "Demander un rendez-vous",
    directions: "Ouvrir l’itinéraire",
    labels: {
      city: "Ville",
      facility: "Structure",
      address: "Adresse",
      days: "Jours de consultation",
      hours: "Horaires",
      phone: "Téléphone sur place",
    },
    notPublished: "Non communiqué",
    facilityPlaceholder: "Structure d’accueil à préciser",
    facilityNote:
      "Le médecin consulte dans cette structure. Le site ne dit ni qu’il la dirige, ni qu’il y est installé de façon permanente.",
    scheduleTitle: "La semaine de consultation",
    scheduleLead: "Une ligne par jour. Le lieu indiqué est celui communiqué par le médecin.",
    scheduleUnverified:
      "«Les jours et horaires de consultation sont à confirmer. Contactez-nous avant de vous déplacer.»",
    scheduleHoursMissing: "Horaires à confirmer",
    scheduleDayEmpty: "Pas de consultation annoncée",
    scheduleNote:
      "Aucune synchronisation avec un agenda n’existe : cette page est mise à jour à la main, et les horaires peuvent changer d’une semaine à l’autre.",
    scheduleAsOf: "Informations communiquées le {date}.",
    scheduleAction: "Rendez-vous",
    sourceLabel: "Source",
    sourcePrefix: "Communiqué par le médecin",
    statusHint: {
      confirmed: "Confirmé par le médecin",
      reported: "Communiqué par le médecin, confirmation à venir",
      unknown: "Pas encore communiqué",
    },
  },

  weekdays: {
    mon: "Lundi",
    tue: "Mardi",
    wed: "Mercredi",
    thu: "Jeudi",
    fri: "Vendredi",
    sat: "Samedi",
    sun: "Dimanche",
  },
  weekdaysShort: { mon: "Lun", tue: "Mar", wed: "Mer", thu: "Jeu", fri: "Ven", sat: "Sam", sun: "Dim" },

  appointment: {
    kicker: "RENDEZ-VOUS",
    title: "«Prenons soin de votre vision.»",
    lead:
      "«Choisissez votre lieu de consultation et contactez-nous pour demander un rendez-vous. Notre équipe pourra vous confirmer les modalités de consultation.»",
    formTitle: "Demande de rendez-vous",
    formNote:
      "Ne transmettez pas d’informations médicales ici : ni ordonnance, ni photo, ni diagnostic. Le médecin les demandera si nécessaire.",
    labels: {
      fullName: "Nom complet",
      contactMethod: "Moyen de contact préféré",
      contact: "Téléphone ou e-mail",
      contactPhone: "Numéro de téléphone",
      contactEmail: "Adresse e-mail",
      locationId: "Ville ou structure souhaitée",
      preferredDate: "Date souhaitée",
      preferredTime: "Heure souhaitée",
      note: "Message (facultatif)",
    },
    hints: {
      contact: "Le numéro ou l’adresse où l’on peut vous répondre.",
      preferredDate: "Si vous n’avez pas de préférence, laissez vide.",
      note: "Une phrase suffit : par exemple, la contrainte qui vous oblige à venir tel jour.",
    },
    methods: { whatsapp: "WhatsApp", phone: "Téléphone", email: "E-mail" },
    placeholders: {
      fullName: "Votre nom",
      contactPhone: "+237 6 00 00 00 00",
      contactEmail: "vous@exemple.com",
      note: "Votre message",
      choose: "Choisir…",
    },
    errors: {
      fullName: "Indiquez votre nom (2 caractères au moins).",
      contactRequired: "Indiquez un moyen de vous joindre.",
      contactPhone: "Ce numéro ne semble pas complet : indiquez au moins 8 chiffres.",
      contactEmail: "Cette adresse e-mail ne semble pas valide.",
      locationId: "Choisissez un lieu de consultation.",
      datePast: "Choisissez une date à venir.",
      dateFar: "Choisissez une date dans les six prochains mois.",
      noteLong: "Votre message dépasse {max} caractères.",
      summary: "Vérifiez les champs signalés.",
    },
    submit: "Préparer ma demande",
    whatsapp: "Envoyer ma demande sur WhatsApp",
    review: "Relire avant l’envoi",
    copy: "Copier le message",
    copied: "Message copié",
    copyFailed: "La copie a échoué — sélectionnez le texte et copiez-le.",
    preparedTitle: "Votre message est prêt",
    preparedNote:
      "Rien n’est envoyé depuis cette page. Copiez ce message et envoyez-le vous-même : c’est vous qui décidez.",
    noNumberTitle: "Le numéro officiel n’est pas encore publié",
    noNumberBody:
      "Le médecin n’a pas encore communiqué de numéro de rendez-vous vérifié. Le message ci-dessous est prêt : il partira dès que le numéro sera publié ici. En attendant, demandez-le à l’accueil de la structure où vous souhaitez consulter.",
    disclaimer:
      "Une demande n’est pas un rendez-vous confirmé. Attendez la confirmation du médecin ou de la structure avant de vous déplacer.",
    liveNote: "Ce site n’affiche pas de disponibilités en temps réel : aucune connexion à un agenda n’existe.",
    reset: "Recommencer",
    summaryTitle: "Votre demande",
  },

  wa: {
    greeting: "Bonjour, je souhaite demander un rendez-vous avec {doctor}.",
    place: "Lieu souhaité : {place}",
    date: "Date souhaitée : {date}",
    time: "Heure souhaitée : {time}",
    name: "Nom : {name}",
    contact: "Contact : {contact}",
    closing: "Merci de me confirmer les disponibilités.",
  },

  footer: {
    title: "Site professionnel",
    line: "Un médecin ophtalmologue, plusieurs lieux de consultation au Cameroun.",
    consultations: "Consultations",
    contact: "Contact",
    contactMissing: "Coordonnées à publier",
    contactMissingNote:
      "Le médecin n’a pas encore communiqué de numéro vérifié. Aucun numéro n’est affiché plutôt qu’un numéro approximatif.",
    legal: "Informations",
    legalLine:
      "Les jours, horaires et adresses sont ceux communiqués par le médecin et restent à confirmer avant un déplacement. Aucune donnée n’est collectée par ce site : le formulaire ne fait que préparer un message.",
    imagesLine: "Photographies : images générées, utilisées comme illustrations. Aucune ne montre le médecin réel.",
    editLink: "Informations à publier",
    editTitle: "Ce qu’il reste à publier",
    editIntro:
      "Liste tirée de la configuration du site. Chaque ligne vide s’affiche « à confirmer » sur la page : rien n’est inventé pour la remplir.",
    editHint: "À renseigner dans js/config/doctor.js, puis à confirmer avec le médecin.",
    backToTop: "Haut de page",
    rights: "Site professionnel — Cameroun",
  },
};
