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
 * Le lien qui s'applique à un lieu donné.
 *
 * Deux niveaux, dans cet ordre : le lieu, puis la page générale. C'est ce qui
 * permet le seul montage gratuit honnête — une page de réservation pour Africa
 * Médical (le vendredi), et la demande écrite pour les trois autres lieux,
 * qu'une page unique ne saurait pas distinguer.
 *
 * @param {object} config      `doctorConfig`
 * @param {string} locationId  le lieu choisi (vide = aucun)
 * @returns {{enabled:boolean, href:string, reason:string, host:string, scope:"location"|"global"|"none"}}
 */
export function bookingFor(config, locationId) {
  const locations = Array.isArray(config?.locations) ? config.locations : [];
  const location = locations.find((item) => item && item.id === locationId);
  const local = bookingStatus(location?.bookingUrl);
  if (local.enabled) return { ...local, scope: "location" };

  const global = bookingStatus(config?.bookingUrl);
  if (global.enabled) return { ...global, scope: "global" };

  // Aucun lien : on rend le refus du lieu s'il y en a un (utile aux tests et au
  // diagnostic), sinon celui de la page générale.
  const reason = local.reason !== "empty" ? local.reason : global.reason;
  return { enabled: false, href: "", host: "", reason, scope: "none" };
}

/** Vrai dès qu'une page de réservation existe, où que ce soit. Pilote la copie. */
export function bookingCapability(config) {
  const urls = [config?.bookingUrl, ...(Array.isArray(config?.locations) ? config.locations : []).map((l) => l?.bookingUrl)];
  return urls.some((url) => bookingStatus(url).enabled);
}

/**
 * L'état de la carte de rendez-vous, en trois valeurs — et pas deux :
 *
 *   "off"     aucun lien nulle part       → le site nie tout agenda (aujourd'hui)
 *   "on"      ce lieu a un créneau        → bouton + phrase de réservation
 *   "partial" des liens existent ailleurs → surtout pas le bouton (on enverrait
 *                                          un patient de Mbouda réserver un
 *                                          créneau à Douala), et une phrase qui
 *                                          dit quoi faire pour ce lieu-ci
 *
 * @returns {"off"|"on"|"partial"}
 */
export function bookingMode(config, locationId) {
  if (!bookingCapability(config)) return "off";
  return bookingFor(config, locationId).enabled ? "on" : "partial";
}

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

/**
 * La clef de la phrase des rendez-vous, pour les trois états.
 * Une seule fonction, pour que le bouton et la phrase ne puissent pas diverger.
 */
export function liveNoteKey(mode) {
  if (mode === "on") return "appointment.liveNoteWhenBooked";
  if (mode === "partial") return "appointment.liveNotePartial";
  return "appointment.liveNote";
}
