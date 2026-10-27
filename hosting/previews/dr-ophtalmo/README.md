# Médecine ophtalmologique — site professionnel d'un médecin itinérant

**Statut : aperçu, non publié.** Aucune donnée de contact réelle n'est affichée, parce qu'aucune n'a été
communiquée par le médecin. Le site fonctionne malgré tout de bout en bout : c'est un site complet dont
les champs manquants s'écrivent « à confirmer » au lieu d'être remplis au hasard.

> Trois sections : **Hero · Parcours · Consultations**, la demande de rendez-vous étant l'ancre
> `#appointments` **à l'intérieur** de Consultations. Un médecin, plusieurs lieux, un seul endroit fiable
> pour savoir où et quel jour.

---

## 1 · Lancer le site

```bash
cd hosting/previews/dr-ophtalmo
python3 -m http.server 8099 --bind 0.0.0.0     # puis http://localhost:8099/
```

Aucune compilation, aucune dépendance : le site est servi tel quel. Les modules ES exigent HTTP (pas
`file://`), d'où le serveur.

**Tests qui tournent sans navigateur :**

```bash
node tests/logic.test.mjs     # 40 vérifications : configuration, semaine, FR/EN, validation, WhatsApp
```

---

## 2 · Ce qui est publié, et ce qui ne l'est pas

Chaque ligne du site vient de `js/config/doctor.js`. Statuts employés : **Confirmé** (le médecin a validé),
**Communiqué** (il l'a dit, la confirmation manque), **À confirmer** (rien n'a été dit).

| Information | État | Où la saisir |
|---|---|---|
| Spécialité : médecine ophtalmologique | Communiqué (26/10) | `specialty` |
| Mbouda — lundi, mardi | Communiqué (26/10) | `locations[0].days` |
| Bafoussam — mercredi, jeudi | Communiqué (26/10) | `locations[1].days` |
| Africa Médical, Douala — vendredi, samedi | Communiqué (26/10) | `locations[2].days` |
| Hôpital Charity, Bonabéri — Grand Hangar, Bloc 7 | Communiqué (26/10) — **aucun jour annoncé** | `locations[3].address`, `.days` |
| Nom, titre, diplômes, inscription à l'Ordre, langues, bio | **À confirmer** | `name`, `title`, `profile.*` |
| Horaires de consultation | **À confirmer** | `locations[].hours` |
| Téléphone / WhatsApp de rendez-vous | **À confirmer** | `contact.whatsapp`, `contact.phone` |
| Itinéraires (liens de carte) | **À confirmer** | `locations[].mapUrl` |

Rien n'est inventé : ni diplôme, ni ancienneté, ni titre hospitalier, ni adresse exacte, ni numéro, ni avis
patient, ni tarif. Le site ne dit jamais qu'il dirige une structure : chaque lieu porte la mention
« Le médecin consulte dans cette structure ».

**Pourquoi les jours de Mbouda, Bafoussam et Douala sont « Communiqué » et non « Confirmé »** : ils
viennent d'un message du médecin du 26/10/2026 à 17:53, repris mot pour mot dans `source`. C'est une
source unique. Le jour où le médecin confirme, passer `status` à `"confirmed"` et `asOf` à la date.

**Hôpital Charity n'a aucun jour** : la phrase du médecin dit qu'on y prend rendez-vous, elle ne dit pas
qu'il y consulte. Le site affiche donc « jours à confirmer » plutôt que de deviner le dimanche.

---

## 3 · Activer WhatsApp (une ligne)

```js
// js/config/doctor.js
contact: {
  whatsapp: "2376XXXXXXXX",   // chiffres seulement, format international, sans « + »
  ...
}
```

Dès que ce champ est rempli, **le bouton WhatsApp apparaît** dans le formulaire, le pied de page et les
modèles de message. Tant qu'il est vide, le site n'affiche aucun numéro : le formulaire prépare le message
et propose de le copier, en disant pourquoi il n'y a pas de bouton. Le message n'est **jamais** envoyé par
le site — c'est le visiteur qui appuie sur « Envoyer » dans WhatsApp.

---

## 4 · Changer un jour de consultation

Une seule édition, dans `js/config/doctor.js` :

```js
{
  id: "mbouda",
  days: ["mon", "tue"],        // mon tue wed thu fri sat sun
  hours: "08:00 – 14:00",      // vide = « horaires à confirmer »
  status: "confirmed",
  asOf: "2026-11-02",
  source: "Confirmation du médecin, 02/11/2026.",
}
```

La semaine, le sélecteur, le formulaire et le pied de page se mettent à jour ensemble : ils lisent tous ce
fichier. Rien n'est écrit deux fois.

---

## 4 bis · Activer la réservation en ligne (route A) — une ligne, quand les horaires existeront

Le site sait déjà recevoir un lien de réservation Google Agenda. Il ne l'affiche pas tant que le champ
est vide :

```js
// js/config/doctor.js
const BOOKING_URL = "";   // ← coller ici l'URL de la page de réservation
```

Dès qu'elle est remplie, **trois choses basculent ensemble** — c'est le même calcul (`js/booking.js`) :

| Ce qui change | Éteint (aujourd'hui) | Allumé |
|---|---|---|
| Le bouton dans la section rendez-vous | absent (bloc `hidden`, sans même un `href`) | « Choisir un créneau » → nouvel onglet |
| La phrase des rendez-vous | « aucune connexion à un agenda n'existe » | « les créneaux libres se voient sur la page de réservation » |
| La phrase de la semaine | « aucune synchronisation avec un agenda » | « les créneaux libres se réservent dans l'agenda du médecin » |
| `meta.liveSync` | `false` | `true` |
| Le panneau « Informations à publier » | « Réservation en ligne — à renseigner » | la ligne est cochée |

Ce que le lien n'est **pas** : une iframe, un script, un cookie. C'est un `<a target="_blank"
rel="noopener noreferrer">`. Le site reste à zéro requête tierce, et Google ne voit que ceux qui cliquent.

Ce qui est refusé sans le dire : un lien qui n'est pas en `https`, ou qui ne pointe pas vers
`calendar.app.google` / `calendar.google.com` (`BOOKING_HOSTS` dans `js/booking.js`). Le bouton
n'apparaît simplement pas — on n'ouvre pas une erreur devant un patient.

**Ce qu'il faut avant de le brancher, et qui manque encore :** des horaires. Une page de réservation se
construit sur des plages horaires hebdomadaires ; aucun des quatre lieux n'a d'heure communiquée, et le
vendredi est en conflit (affiche du cabinet contre message du médecin). Programmer une récurrence sur
une information contradictoire serait pire que pas de réservation du tout.

---

## 5 · Ce que le site ne fait pas — et le dit

- **Pas de réservation en ligne tant que le lien est vide.** Aucun rendez-vous n'est créé, aucune place
  n'est réservée : le site prépare un message, et le rappelle sous le formulaire (« Une demande n'est pas
  un rendez-vous confirmé »). Dès que `bookingUrl` est renseigné, le créneau se réserve **chez Google**,
  pas ici — et les deux phrases qui parlaient d'agenda basculent (voir §4 bis).
- **Pas de disponibilités en temps réel.** Aucun agenda n'est branché tant que `bookingUrl` est vide
  (`meta.liveSync`, déduit du champ, jamais écrit à la main), et la page l'écrit.
- **Pas de collecte de données.** Aucun formulaire ne part vers un serveur : il n'y a ni backend, ni
  cookie, ni mesure d'audience. Le formulaire refuse explicitement les informations médicales.
- **Pas de faux avis.** Aucun témoignage, aucune note, aucun compteur.
- **Photographies réelles, et attribuées.** Les trois images du médecin viennent de lui (27/10/2026) ;
  aucune n'est générée, aucune ne porte de légende de provenance (ruling King du 27/10). La légende de la
  photo d'équipe ne nomme aucune affiliation : le panneau visible sur l'image n'est pas vérifié.

---

## 6 · Structure

```text
index.html                 la page ; aucun texte en dur, seulement des clefs data-i18n
css/styles.css             jetons, grille 12 colonnes, responsive, impression, mouvement réduit
js/config/doctor.js        identité, contact, quatre lieux  ← le seul fichier à éditer
js/config/services.js      prestations (une seule, déductible ; le reste à confirmer)
js/config/appointment.js   champs, limites, modèle du message WhatsApp, liens wa.me
js/i18n/fr.js · en.js      dictionnaires complets ; js/i18n/index.js résout et interpole
js/lib/schedule.js         la semaine se déduit des lieux
js/lib/validators.js       validation + messages localisés
js/app.js                  rendu et interactions (le seul fichier qui touche au DOM)
assets/                    3 images en 3 largeurs (webp), 6 fichiers de police locaux
tests/logic.test.mjs       40 vérifications sans navigateur
```

---

## 7 · Ce qui a été vérifié

- **40 vérifications de logique** (`tests/logic.test.mjs`) : quatre lieux, semaine déduite, jours
  traduits, parité stricte des clefs FR/EN, validation (nom, téléphone, e-mail, date passée, date trop
  lointaine, message trop long), message WhatsApp (lieu, date en clair, aucun `undefined`), encodage
  `wa.me` sans `+`, absence de lien quand aucun numéro n'est configuré.
- **46 vérifications de rendu** dans un DOM simulé (jsdom, hors dépôt) : trois sections, ancres exactes,
  H1 en trois lignes, quatre lieux dans le sélecteur et dans le formulaire, sept jours dont le dimanche
  vide, bascule FR↔EN qui conserve le lieu choisi et la saisie en cours, erreurs de formulaire annoncées
  avec `aria-invalid`, message préparé nommant le lieu choisi, aucun `undefined` affiché.
- **Mesuré dans un vrai Chromium** (26/10, après `bash tools/video/install.sh`), aux largeurs
  1440 · 1024 · 768 · 390 · 320 : **0 débordement horizontal**, **0 image cassée**, **0 erreur console**,
  aucun texte sous 12 px (10,2 px avant correction), anneau de focus 3 px, en-tête à 60 px en 320 px,
  H1 sur trois lignes, `document.fonts.status === "loaded"`.
- **Non vérifié** : le rendu sur un vrai téléphone en 3G, l'aperçu d'un lien collé dans une vraie
  conversation WhatsApp, et les polices sur un Android ancien. La page est déployée en aperçu privé
  (`dr-ophtalmo-preview.vercel.app`, `noindex`) précisément pour ce contrôle-là.

---

## 8 · Accessibilité et poids

- Navigation clavier complète, lien d'évitement, `aria-expanded` sur le menu mobile, anneaux de focus
  visibles, `aria-invalid` + messages liés par `aria-describedby`, annonces `aria-live`.
- Aucun état ne repose sur la couleur seule : chaque lieu porte un point **et** un mot (« Communiqué »,
  « À confirmer »).
- `prefers-reduced-motion` coupe les apparitions ; sans JavaScript, rien n'est masqué (les animations ne
  s'activent qu'une fois l'observateur posé).
- Poids total : ~300 Ko d'images (trois formats chacune), ~150 Ko de polices locales, zéro appel tiers.
  Les images sont en `loading="lazy"` sauf le portrait du hero.
