/**
 * ENGLISH — a complete alternative, not a shortened one.
 * Same facts, same honesty about what is still unconfirmed. Facility names
 * (Africa Médical, Hôpital Charity) stay as they are: they are proper names.
 */
export const en = {
  meta: {
    lang: "en",
    title: "Ophthalmology in Cameroon — consultations in Mbouda, Bafoussam, Douala and Bonabéri",
    description:
      "Professional website of an itinerant ophthalmologist in Cameroon: consultation locations, weekly days, and appointment requests by WhatsApp or phone.",
  },

  common: {
    skip: "Skip to content",
    brand: "Ophthalmology",
    brandSub: "Cameroon",
    doctorFallback: "the doctor",
    unknown: "To be confirmed",
    reported: "Reported",
    confirmed: "Confirmed",
    close: "Close",
    menu: "Menu",
    openMenu: "Open menu",
    closeMenu: "Close menu",
    language: "Language",
    switchTo: "Switch to French",
    required: "required",
    optional: "optional",
    backToTop: "Back to top",
    emDash: "—",
    today: "Today",
  },

  nav: {
    label: "Main navigation",
    home: "Home",
    doctor: "The doctor",
    consultations: "Consultations",
    appointments: "Appointments",
  },

  hero: {
    eyebrow: "OPHTHALMOLOGY · CAMEROON",
    h1: ["YOUR", "VISION,", "MY PRIORITY."],
    lead:
      "“An ophthalmologist who listens, consulting in several cities and medical facilities across Cameroon.”",
    ctaPrimary: "Find a consultation location",
    ctaSecondary: "Meet the doctor",
    placesLabel: "Consultation locations",
    places: "Mbouda · Bafoussam · Douala · Bonabéri",
    placesNote:
      "These cities are consultation locations. They do not mean the doctor consults in each of them every day.",
    portraitCaption:
      "Illustrative portrait (generated image) — to be replaced by the doctor’s own photograph.",
    statusLine: "Information reported on 26 October 2026 — reconfirm before travelling.",
  },

  parcours: {
    kicker: "ABOUT THE DOCTOR",
    title: "“Medical expertise, several consultation locations.”",
    p1:
      "“Because access to eye care is not limited to a single address, Dr [DOCTOR NAME] consults in several cities and medical facilities, on a defined schedule.”",
    p2:
      "“This website gathers the essential information to help you identify the right consultation location, prepare your visit, and reach the right person.”",
    profileTitle: "Professional details",
    profileNote:
      "Only information provided by the doctor appears here. No degree, registration or experience is invented to fill the page.",
    labels: {
      name: "Professional name and title",
      specialty: "Specialty",
      qualifications: "Training and qualifications",
      registration: "Professional registration",
      languages: "Languages spoken",
      interests: "Clinical interests",
      bio: "Biography",
      services: "Services",
    },
    placeholders: {
      name: "Doctor’s name to be published",
      qualifications: "Qualifications to be published once verified",
      registration: "Registration number to be published once verified",
      languages: "Languages to be provided",
      interests: "Clinical interests to be provided",
      bio: "Biography to be received from the doctor",
    },
    servicesNotice:
      "The list of services performed will be published once the doctor confirms it. If in doubt, ask when you request an appointment.",
    examinationCaption:
      "Eye examination in a consultation room — illustrative photograph (generated image), not tied to any particular partner facility.",
    equipmentCaption: "Slit lamp and examination chair — illustrative photograph (generated image).",
    photoNote:
      "The photographs on this page are generated illustrations. They show neither the doctor nor a specific partner location.",
  },

  consultations: {
    kicker: "LOCATIONS AND CONSULTATION DAYS",
    title: "“Where can you see the doctor?”",
    lead:
      "“Find the consultation locations and the days the doctor is present. Check the information before travelling, and request an appointment for the relevant facility.”",
    selectLabel: "Choose a location",
    selected: "Selected location",
    requestCta: "Request an appointment",
    directions: "Open directions",
    labels: {
      city: "City",
      facility: "Facility",
      address: "Address",
      days: "Consultation days",
      hours: "Hours",
      phone: "Phone on site",
    },
    notPublished: "Not provided",
    facilityPlaceholder: "Host facility to be specified",
    facilityNote:
      "The doctor consults at this facility. This site does not claim he runs it, nor that he is based there permanently.",
    scheduleTitle: "The consultation week",
    scheduleLead: "One row per day. The location shown is the one reported by the doctor.",
    scheduleUnverified:
      "“Consultation days and hours are to be confirmed. Contact us before travelling.”",
    scheduleHoursMissing: "Hours to be confirmed",
    scheduleDayEmpty: "No consultation announced",
    scheduleNote:
      "Nothing is synced to a calendar: this page is updated by hand, and hours may change from one week to the next.",
    scheduleAsOf: "Information reported on {date}.",
    scheduleAction: "Appointment",
    sourceLabel: "Source",
    sourcePrefix: "Reported by the doctor",
    statusHint: {
      confirmed: "Confirmed by the doctor",
      reported: "Reported by the doctor, confirmation pending",
      unknown: "Not provided yet",
    },
  },

  weekdays: {
    mon: "Monday",
    tue: "Tuesday",
    wed: "Wednesday",
    thu: "Thursday",
    fri: "Friday",
    sat: "Saturday",
    sun: "Sunday",
  },
  weekdaysShort: { mon: "Mon", tue: "Tue", wed: "Wed", thu: "Thu", fri: "Fri", sat: "Sat", sun: "Sun" },

  appointment: {
    kicker: "APPOINTMENTS",
    title: "“Let’s take care of your vision.”",
    lead:
      "“Choose your consultation location and contact us to request an appointment. Our team will confirm the consultation arrangements.”",
    formTitle: "Appointment request",
    formNote:
      "Please do not send medical information here: no prescription, no photograph, no diagnosis. The doctor will ask if needed.",
    labels: {
      fullName: "Full name",
      contactMethod: "Preferred contact method",
      contact: "Phone or e-mail",
      contactPhone: "Phone number",
      contactEmail: "E-mail address",
      locationId: "Preferred city or facility",
      preferredDate: "Preferred date",
      preferredTime: "Preferred time",
      note: "Message (optional)",
    },
    hints: {
      contact: "The number or address where we can reach you.",
      preferredDate: "If you have no preference, leave it empty.",
      note: "One line is enough: for example, the constraint that makes a given day easier.",
    },
    methods: { whatsapp: "WhatsApp", phone: "Phone", email: "E-mail" },
    placeholders: {
      fullName: "Your name",
      contactPhone: "+237 6 00 00 00 00",
      contactEmail: "you@example.com",
      note: "Your message",
      choose: "Choose…",
    },
    errors: {
      fullName: "Please give your name (at least 2 characters).",
      contactRequired: "Please give a way to reach you.",
      contactPhone: "This number looks incomplete: at least 8 digits.",
      contactEmail: "This e-mail address does not look valid.",
      locationId: "Please choose a consultation location.",
      datePast: "Please choose a future date.",
      dateFar: "Please choose a date within the next six months.",
      noteLong: "Your message is over {max} characters.",
      summary: "Please check the highlighted fields.",
    },
    submit: "Prepare my request",
    whatsapp: "Send my request on WhatsApp",
    review: "Review before sending",
    copy: "Copy the message",
    copied: "Message copied",
    copyFailed: "Copy failed — select the text and copy it.",
    preparedTitle: "Your message is ready",
    preparedNote:
      "Nothing is sent from this page. Copy the message and send it yourself: you decide.",
    noNumberTitle: "The official number is not published yet",
    noNumberBody:
      "The doctor has not yet provided a verified appointment number. The message below is ready and will go out as soon as the number is published here. Meanwhile, ask at the reception of the facility where you wish to consult.",
    disclaimer:
      "A request is not a confirmed appointment. Wait for confirmation from the doctor or the facility before travelling.",
    liveNote: "This site shows no real-time availability: there is no connection to any calendar.",
    reset: "Start again",
    summaryTitle: "Your request",
  },

  wa: {
    greeting: "Hello, I would like to request an appointment with {doctor}.",
    place: "Preferred location: {place}",
    date: "Preferred date: {date}",
    time: "Preferred time: {time}",
    name: "Name: {name}",
    contact: "Contact: {contact}",
    closing: "Please confirm availability. Thank you.",
  },

  footer: {
    title: "Professional website",
    line: "One ophthalmologist, several consultation locations in Cameroon.",
    consultations: "Consultations",
    contact: "Contact",
    contactMissing: "Contact details to be published",
    contactMissingNote:
      "The doctor has not yet provided a verified number. No number is shown rather than an approximate one.",
    legal: "Information",
    legalLine:
      "Days, hours and addresses are those reported by the doctor and remain to be confirmed before travelling. This site collects no data: the form only prepares a message.",
    imagesLine: "Photography: generated images used as illustrations. None of them shows the real doctor.",
    editLink: "Information to publish",
    editTitle: "What still has to be published",
    editIntro:
      "List built from the site configuration. Every empty line shows “to be confirmed” on the page: nothing is invented to fill it.",
    editHint: "Fill in js/config/doctor.js, then have the doctor confirm each line.",
    backToTop: "Top of page",
    rights: "Professional website — Cameroon",
  },
};
