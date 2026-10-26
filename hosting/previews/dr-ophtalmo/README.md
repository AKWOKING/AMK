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
node tests/logic.test.mjs     # 34 vérifications : configuration, semaine, FR/EN, validation, WhatsApp
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

## 5 · Ce que le site ne fait pas — et le dit

- **Pas de réservation en ligne.** Aucun rendez-vous n'est créé, aucune place n'est réservée. Le site
  prépare un message, et le rappelle sous le formulaire (« Une demande n'est pas un rendez-vous confirmé »).
- **Pas de disponibilités en temps réel.** Aucun agenda n'est branché (`meta.liveSync = false`), et la
  page l'écrit.
- **Pas de collecte de données.** Aucun formulaire ne part vers un serveur : il n'y a ni backend, ni
  cookie, ni mesure d'audience. Le formulaire refuse explicitement les informations médicales.
- **Pas de faux avis.** Aucun témoignage, aucune note, aucun compteur.
- **Photographies générées.** Les trois images sont des illustrations produites pour cet aperçu ; deux
  légendes le disent à l'écran. Aucune ne montre le médecin réel : dès qu'il envoie sa photo, remplacer
  `profile.portrait.src`, `srcset`, `alt` et passer `isRealPhoto` à `true` (la légende disparaît).

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
tests/logic.test.mjs       34 vérifications sans navigateur
```

---

## 7 · Ce qui a été vérifié

- **34 vérifications de logique** (`tests/logic.test.mjs`) : quatre lieux, semaine déduite, jours
  traduits, parité stricte des clefs FR/EN, validation (nom, téléphone, e-mail, date passée, date trop
  lointaine, message trop long), message WhatsApp (lieu, date en clair, aucun `undefined`), encodage
  `wa.me` sans `+`, absence de lien quand aucun numéro n'est configuré.
- **46 vérifications de rendu** dans un DOM simulé (jsdom, hors dépôt) : trois sections, ancres exactes,
  H1 en trois lignes, quatre lieux dans le sélecteur et dans le formulaire, sept jours dont le dimanche
  vide, bascule FR↔EN qui conserve le lieu choisi et la saisie en cours, erreurs de formulaire annoncées
  avec `aria-invalid`, message préparé nommant le lieu choisi, aucun `undefined` affiché.
- **Non vérifié ici** : le rendu pixel d'un vrai navigateur (aucun Chromium disponible dans
  l'environnement de construction) et les mesures de contraste à l'écran. La page est ouverte en aperçu
  pour ce contrôle visuel ; les tailles de police, les points de rupture (1440 · 1024 · 768 · 390 · 320)
  et l'absence de débordement horizontal ont été traités dans la feuille de style, pas mesurés.

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
