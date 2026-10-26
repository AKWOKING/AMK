/**
 * ─────────────────────────────────────────────────────────────────────────────
 * RENDEZ-VOUS — champs, limites, modèles de message
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Ce formulaire ne collecte AUCUNE donnée clinique : ni antécédent, ni
 * ordonnance, ni photo d'œil, ni diagnostic. C'est une demande de rendez-vous,
 * pas un dossier médical. La liste ci-dessous est aussi la liste des champs
 * transmis au message WhatsApp : ce qui n'y est pas ne peut pas fuir.
 */

export const contactMethods = ["whatsapp", "phone", "email"];

export const limits = {
  name: 80,
  contact: 120,
  message: 400,
  /** Une demande ne se prend pas pour aujourd'hui : le médecin doit confirmer. */
  minLeadDays: 0,
  maxLeadDays: 180,
};

export const fields = [
  { name: "fullName", required: true, autocomplete: "name" },
  { name: "contactMethod", required: true, type: "radio" },
  { name: "contact", required: true, autocomplete: "tel" },
  { name: "locationId", required: true, type: "select" },
  { name: "preferredDate", required: false, type: "date" },
  { name: "preferredTime", required: false, type: "time" },
  { name: "note", required: false, type: "textarea" },
];

/**
 * Le message WhatsApp. Il ne contient que ce que le visiteur a choisi de
 * donner. Les valeurs absentes disparaissent au lieu de laisser « : — ».
 * Aucun envoi automatique : le lien ouvre WhatsApp, et l'humain appuie.
 */
export function whatsappMessage({ t, values, locationLabel, doctorName }) {
  const lines = [
    t("wa.greeting", { doctor: doctorName || t("common.doctorFallback") }),
    t("wa.place", { place: locationLabel }),
  ];
  if (values.preferredDate) lines.push(t("wa.date", { date: formatDate(values.preferredDate) }));
  if (values.preferredTime) lines.push(t("wa.time", { time: values.preferredTime }));
  if (values.fullName) lines.push(t("wa.name", { name: values.fullName.trim() }));
  if (values.contact) lines.push(t("wa.contact", { contact: values.contact.trim() }));
  lines.push(t("wa.closing"));
  return lines.join("\n");
}

/** 2026-10-28 → « 28 octobre 2026 » (ou « 28 October 2026 »), pour une date d'information. */
export function formatDateOnly(iso, lang = "fr") {
  const [y, m, d] = String(iso).split("-").map(Number);
  if (!y || !m || !d) return iso;
  return new Intl.DateTimeFormat(lang === "en" ? "en-GB" : "fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(Date.UTC(y, m - 1, d)));
}

/** 2026-10-28 → « mercredi 28 octobre 2026 » (ou « Wednesday 28 October 2026 »). */
export function formatDate(iso, lang = "fr") {
  const [y, m, d] = String(iso).split("-").map(Number);
  if (!y || !m || !d) return iso;
  const date = new Date(Date.UTC(y, m - 1, d));
  return new Intl.DateTimeFormat(lang === "en" ? "en-GB" : "fr-FR", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

/** Lien WhatsApp conforme : https://wa.me/<chiffres>?text=<encodé>. */
export function buildWhatsappUrl(number, message) {
  const digits = String(number || "").replace(/\D/g, "");
  if (!digits) return "";
  return `https://wa.me/${digits}?text=${encodeURIComponent(message)}`;
}
