/**
 * Validation du formulaire. Les messages viennent du dictionnaire : une erreur
 * s'écrit dans la langue affichée, et change de langue avec la page.
 */
import { limits } from "../config/appointment.js";

const phoneDigits = (value) => String(value || "").replace(/[^\d]/g, "");

/** Volontairement souple : on vérifie qu'un humain peut rappeler, pas un format. */
export const isValidPhone = (value) => {
  const digits = phoneDigits(value);
  return digits.length >= 8 && digits.length <= 15;
};

export const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(String(value || "").trim());

const todayISO = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(
    now.getDate(),
  ).padStart(2, "0")}`;
};

/** @returns {Record<string, string>} nom de champ → clef d'erreur (pas le texte). */
export function validate(values, { t } = {}) {
  const errors = {};

  if (!values.fullName || values.fullName.trim().length < 2) {
    errors.fullName = "fullName";
  }

  const contact = String(values.contact || "").trim();
  if (!contact) {
    errors.contact = "contactRequired";
  } else if (values.contactMethod === "email") {
    if (!isValidEmail(contact)) errors.contact = "contactEmail";
  } else if (!isValidPhone(contact)) {
    errors.contact = "contactPhone";
  }

  if (!values.locationId) errors.locationId = "locationId";

  if (values.preferredDate) {
    const today = todayISO();
    if (values.preferredDate < today) {
      errors.preferredDate = "datePast";
    } else {
      const limit = new Date();
      limit.setDate(limit.getDate() + limits.maxLeadDays);
      const limitISO = `${limit.getFullYear()}-${String(limit.getMonth() + 1).padStart(2, "0")}-${String(
        limit.getDate(),
      ).padStart(2, "0")}`;
      if (values.preferredDate > limitISO) errors.preferredDate = "dateFar";
    }
  }

  if (values.note && values.note.length > limits.message) {
    errors.note = "noteLong";
  }

  return errors;
}

/** Le texte affiché pour une erreur. */
export const errorText = (key, t) => {
  if (!key) return "";
  if (key === "noteLong") return t(`appointment.errors.${key}`, { max: limits.message });
  return t(`appointment.errors.${key}`);
};
