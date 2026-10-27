/**
 * ─────────────────────────────────────────────────────────────────────────────
 * Réservation en ligne — la route A, et rien de plus
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Un seul lien : la page de réservation du médecin (Google Agenda → « Créneaux
 * de rendez-vous »). Aucun script, aucune iframe, aucun cookie — le site
 * n'apprend rien du visiteur, et Google ne voit que ceux qui cliquent.
 *
 * Pourquoi pas une intégration : une iframe Google poserait ses cookies dès
 * l'affichage et ferait tomber trois promesses tenues par les tests du site
 * (« aucune ressource d'un domaine tiers », « aucun cookie », « aucune mesure
 * d'audience »). Une vraie synchronisation (OAuth + fonction serverless + jetons
 * à rafraîchir) coûterait plus de pièces mobiles que de bénéfice pour un
 * médecin qui veut surtout qu'on le joigne.
 *
 * Deux règles, et elles se testent sans navigateur :
 *   ① tant que `bookingUrl` est vide, le bouton n'existe pas et la page dit
 *      qu'aucune connexion à un agenda n'existe ;
 *   ② un lien qui n'est pas en https, ou qui ne pointe pas vers un service de
 *      réservation connu, est refusé en silence — on n'envoie pas un patient
 *      vers une adresse qu'on n'a pas vérifiée.
 */

/** Les hôtes acceptés. Ajouter un outil de réservation = une ligne ici, à découvert. */
export const BOOKING_HOSTS = ["calendar.app.google", "calendar.google.com"];

/**
 * L'état du lien de réservation.
 *
 * @param {string} url            la valeur de `bookingUrl` dans la configuration
 * @param {string[]} hosts        les hôtes acceptés (paramètre pour les tests)
 * @returns {{enabled: boolean, href: string, reason: string, host: string}}
 *   `reason` vaut "empty" · "malformed" · "insecure" · "host" · "ok".
 *   Un refus ne casse pas la page : il rend simplement le bouton absent.
 */
export function bookingStatus(url, hosts = BOOKING_HOSTS) {
  const raw = typeof url === "string" ? url.trim() : "";
  const off = (reason, host = "") => ({ enabled: false, href: "", reason, host });

  if (!raw) return off("empty");

  let parsed;
  try {
    parsed = new URL(raw);
  } catch {
    return off("malformed");
  }

  // http:// enverrait le visiteur vers une page en clair, et le lien serait
  // réécrit par le navigateur : on refuse plutôt que de corriger en silence.
  if (parsed.protocol !== "https:") return off("insecure", parsed.hostname);
  if (!hosts.includes(parsed.hostname)) return off("host", parsed.hostname);

  return { enabled: true, href: parsed.href, reason: "ok", host: parsed.hostname };
}

/** Le raccourci que le rendu utilise. */
export const bookingEnabled = (url, hosts) => bookingStatus(url, hosts).enabled;

/**
 * La bascule de la copie.
 *
 * Deux phrases de la page affirment aujourd'hui qu'aucune connexion à un agenda
 * n'existe. Le jour où le lien est là, elles deviennent fausses — et une page
 * qui se contredit coûte plus cher qu'une page muette. Une seule fonction
 * choisit donc la variante, pour les deux phrases à la fois : impossible
 * d'avoir le bouton sans la copie, ou l'inverse.
 *
 * @param {string} baseKey  la clef de la phrase sans réservation
 * @param {boolean} enabled l'état du lien
 * @returns {string} `baseKey` ou `baseKey + "WhenBooked"`
 */
export function liveCopyKey(baseKey, enabled) {
  return enabled ? `${baseKey}WhenBooked` : baseKey;
}
