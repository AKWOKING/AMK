/**
 * FRANÇAIS — la langue de départ.
 * Écrit pour des patients au Cameroun : phrases courtes, pas de jargon
 * administratif, et on dit franchement ce qu'on ne sait pas encore.
 */
export const fr = {
  meta: {
    lang: "fr",
    title: "Dr Fogue, ophtalmologue — consultations à Mbouda, Bafoussam et Douala",
    description:
      "Le Dr Fogue, ophtalmologue, consulte à Mbouda, Bafoussam, Douala (Africa Médical) et Bonabéri (Hôpital Charity). Jours de consultation et contact direct par WhatsApp ou téléphone.",
  },

  common: {
    skip: "Aller au contenu",
    brand: "Dr Fogue",
    brandSub: "Ophtalmologue",
    doctorFallback: "le Dr Fogue",
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
    eyebrow: "OPHTALMOLOGIE · CAMEROUN",
    h1: ["VOTRE VISION,", "MA PRIORITÉ."],
    lead:
      "Le Dr Fogue vous accompagne dans la santé de vos yeux. Retrouvez les informations sur ses consultations et contactez-le pour préparer votre rendez-vous.",
    ctaPrimary: "Prendre rendez-vous",
    ctaSecondary: "Voir les lieux de consultation",
    whatsappCta: "Écrire sur WhatsApp",
    identityPending: "Nom et spécialité à confirmer",
    placesLabel: "Lieux de consultation",
    places: "Mbouda · Bafoussam · Douala · Bonabéri",
    placesNote:
      "Les jours changent d’un lieu à l’autre : la semaine complète est un peu plus bas, lieu par lieu.",
    statusLine: "Jours communiqués par le Dr Fogue le 26 octobre 2026 — à reconfirmer avant tout déplacement.",
  },

  parcours: {
    kicker: "LE MÉDECIN",
    title: "«Votre spécialiste de la vue.»",
    p1:
      "«Le Dr Fogue vous accompagne dans la prise en charge de votre santé visuelle à travers des consultations organisées dans plusieurs lieux au Cameroun.»",
    p2:
      "«Retrouvez ici les informations pratiques pour préparer votre consultation et contacter son équipe : les jours de présence lieu par lieu, l’adresse quand elle est connue, et le numéro à joindre.»",
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
      "Le Dr Fogue en consultation. Photographie transmise par le médecin, 26 octobre 2026.",
    equipmentCaption:
      "Le Dr Fogue en consultation. Affiche du cabinet, recadrée — 26 octobre 2026.",
    photoNote:
      "Les photographies de cette page sont celles du Dr Fogue, transmises par lui le 26 octobre 2026. Aucune image générée ne figure sur le site.",
  },

  consultations: {
    kicker: "LIEUX ET JOURS DE CONSULTATION",
    title: "«Où consulter le Dr Fogue ?»",
    lead:
      "«Quatre lieux de consultation, et des jours différents selon le lieu. Vérifiez l’information avant de vous déplacer, puis demandez un rendez-vous pour la structure concernée.»",
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
    scheduleTitle: "La semaine du Dr Fogue",
    scheduleLead: "Une ligne par jour. Le lieu indiqué est celui communiqué par le médecin.",
    scheduleUnverified:
      "«Les jours et horaires de consultation sont à confirmer. Veuillez contacter le Dr Fogue avant de vous déplacer.»",
    scheduleHoursMissing: "Horaires à confirmer",
    scheduleDayEmpty: "Pas de consultation annoncée",
    scheduleNote:
      "Aucune synchronisation avec un agenda n’existe : cette page est mise à jour à la main, et les horaires peuvent changer d’une semaine à l’autre.",
    scheduleNoteWhenBooked:
      "Les jours de présence ci-dessus sont mis à jour à la main : ils peuvent changer d’une semaine à l’autre. Les créneaux libres, eux, se réservent dans l’agenda du Dr Fogue — le bouton est plus bas, dans la section rendez-vous.",
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
      "«Choisissez votre lieu de consultation, puis préparez votre message : il part sur WhatsApp, et c’est vous qui l’envoyez. Le Dr Fogue ou son équipe vous répond pour confirmer le créneau.»",
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
    // Trois variantes, jamais deux à la fois (js/booking.js, `liveNoteKey`) :
    // aucune page de réservation, ce lieu en a une, ou un autre lieu en a une.
    liveNoteWhenBooked:
      "Cette page n’affiche pas de disponibilités en temps réel. Les créneaux libres se voient sur la page de réservation du Dr Fogue, reliée à son agenda ; le bouton est juste au-dessus du formulaire.",
    liveNotePartial:
      "Pour ce lieu, les créneaux ne se réservent pas encore en ligne : préparez une demande ci-dessous. La réservation en ligne existe pour les autres lieux de consultation, un peu plus haut dans la page.",
    reset: "Recommencer",
    summaryTitle: "Votre demande",
  },

  booking: {
    cta: "Choisir un créneau",
    opensNewTab: "s’ouvre dans un nouvel onglet",
    note: "Vous choisissez l’heure dans l’agenda du Dr Fogue : le rendez-vous s’inscrit aussitôt dans son agenda et vous recevez la confirmation de Google. Si aucune heure ne vous convient, préparez une demande ci-dessous.",
    or: "Ou préparez une demande",
    label: "Réservation en ligne",
    notForPlace:
      "Ce lieu ne propose pas encore de réservation en ligne. Préparez une demande ci-dessous : elle part sur WhatsApp, et le Dr Fogue vous répond pour fixer l’heure.",
    // Le message part du numéro du patient : le médecin le reçoit comme un
    // message ordinaire, dans la conversation. Rien n’est envoyé par le site.
    waCta: "Prévenir le Dr Fogue sur WhatsApp",
    waNote:
      "Facultatif : ce message part de votre propre numéro, avec le lieu et l’heure que vous venez de réserver. Vous pouvez le modifier avant de l’envoyer.",
    waMessage:
      "Bonjour {doctor}, je viens de réserver un créneau sur votre page de réservation — lieu : {place}. Pouvez-vous me confirmer que le rendez-vous est bien noté ? Merci.",
  },

  wa: {
    direct:
      "Bonjour Docteur Fogue, je souhaiterais obtenir des informations sur vos consultations ophtalmologiques et connaître le prochain créneau disponible. Merci.",
    greeting: "Bonjour, je souhaite demander un rendez-vous avec {doctor}.",
    place: "Lieu souhaité : {place}",
    date: "Date souhaitée : {date}",
    time: "Heure souhaitée : {time}",
    name: "Nom : {name}",
    contact: "Contact : {contact}",
    closing: "Merci de me confirmer les disponibilités.",
  },

  footer: {
    title: "Dr Fogue · Ophtalmologie",
    line: "Un ophtalmologue, quatre lieux de consultation au Cameroun.",
    consultations: "Consultations",
    contact: "Contact",
    contactMissing: "Coordonnées à publier",
    contactMissingNote:
      "Le médecin n’a pas encore communiqué de numéro vérifié. Aucun numéro n’est affiché plutôt qu’un numéro approximatif.",
    legal: "Informations",
    legalLine:
      "Les jours, horaires et adresses sont ceux communiqués par le Dr Fogue et restent à confirmer avant un déplacement. Aucune donnée n’est collectée par ce site : le formulaire ne fait que préparer un message.",
    imagesLine:
      "Photographies du Dr Fogue, transmises par le médecin le 26 octobre 2026. La photographie d’équipe n’est pas publiée : son lieu n’est pas confirmé.",
    questionsTitle: "Questions à confirmer avec le Dr Fogue",
    editLink: "Informations à publier",
    editTitle: "Ce qu’il reste à publier",
    editIntro:
      "Liste tirée de la configuration du site. Chaque ligne vide s’affiche « à confirmer » sur la page : rien n’est inventé pour la remplir.",
    editHint: "À renseigner dans js/config/doctor.js, puis à confirmer avec le médecin.",
    backToTop: "Haut de page",
    rights: "Dr Fogue · Ophtalmologie — Cameroun",
    credit: "Aperçu AMK, non publié — à valider par le Dr Fogue avant publication.",
  },
};
