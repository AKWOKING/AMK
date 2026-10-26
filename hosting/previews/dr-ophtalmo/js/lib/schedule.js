/**
 * La semaine se DÉDUIT de la configuration : un jour n'est jamais écrit deux
 * fois. Ajouter un lieu dans doctor.js suffit pour qu'il apparaisse ici, dans
 * le sélecteur et dans le formulaire.
 */
import { doctorConfig } from "../config/doctor.js";

export const WEEK = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];

/**
 * Les horaires peuvent être une chaîne (« 8 h – 15 h ») ou un objet bilingue
 * ({ fr, en }) quand le texte n'est pas une heure mais une modalité —
 * « Sur rendez-vous ». Cette fonction rend toujours une chaîne affichable.
 */
export const hoursText = (hours, lang = "fr") => {
  if (!hours) return "";
  if (typeof hours === "string") return hours.trim();
  return (hours[lang] || hours.fr || "").trim();
};

/**
 * @returns {Array<{day: string, entries: Array<{
 *   locationId: string, city: string, facility: string,
 *   hours: string, status: string, asOf: string
 * }>}>}
 */
export function buildWeek(config = doctorConfig) {
  const byDay = new Map(WEEK.map((day) => [day, []]));
  for (const location of config.locations) {
    for (const day of location.days || []) {
      if (!byDay.has(day)) continue;
      byDay.get(day).push({
        locationId: location.id,
        city: location.city,
        facility: location.facility,
        hours: location.hours || "",
        status: location.status || "unknown",
        asOf: location.asOf || "",
      });
    }
  }
  return WEEK.map((day) => ({ day, entries: byDay.get(day) }));
}

/** Un jour est « renseigné » dès qu'au moins un lieu y consulte. */
export const hasAnySchedule = (config = doctorConfig) =>
  config.locations.some((location) => (location.days || []).length > 0);

/** Y a-t-il au moins une heure connue ? Sinon on l'écrit, au lieu de laisser vide. */
export const hasAnyHours = (config = doctorConfig) =>
  config.locations.some((location) => Boolean(hoursText(location.hours)));

/** Le libellé d'un lieu, sans jamais afficher «  » ou « undefined ». */
export function locationLabel(location, t) {
  if (!location) return "";
  const parts = [location.facility, location.city].filter((part) => part && String(part).trim());
  if (parts.length === 0) return location.id;
  return parts.join(" · ");
}

/** Jours d'un lieu, déjà traduits, dans l'ordre de la semaine. */
export function locationDays(location, t) {
  if (!location || !location.days || location.days.length === 0) return "";
  return WEEK.filter((day) => location.days.includes(day))
    .map((day) => t(`weekdays.${day}`))
    .join(" · ");
}
