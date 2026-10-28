# Brainstorm — brancher un agenda sur le site du Dr Fogue, ou pas

```text
ÉTAPE 0   graphe rejoué 27/10 10 h 21 (13 643 nœuds) · carte lue §0/§6/§2/§3/§1/§3 bis
          ask « google calendar booking link rendez-vous réservation dr fogue » → 64 documents,
          dont clients/dm-optic/launch/SETUP-GOOGLE-BUSINESS.md et sales/FICHE-GOOGLE-PROFILE.md
PRE-FLIGHT  §00, §0, §0b, §0c, §0c bis, §0e, §0f, §1i, §1i bis, §5
KNOWLEDGE   knowledge 4 (LANDING-FUNNEL-2026-10-23 §2, §6, §10 : conversion, formulaire, porte technique)
DOSSIER     clients/dr-ophtalmo/build-notes.md (§6–§8), DEPLOIEMENT-VERCEL.md,
            hosting/previews/dr-ophtalmo/{js/app.js, js/config/doctor.js, tests/logic.test.mjs}
DEMANDE     King, 27/10 : « prépare la route A dès maintenant derrière une configuration éteinte »
MÉTHODE     brainstorming (superpowers) : les faits d'abord, trois routes à part, puis trancher
ÉTAT        proposition ci-dessous, et le code écrit ce tour — rien n'est visible en ligne
```

## 1 · Ce que le pré-vol a mesuré, et qui contraint la décision

| Fait | Le chiffre | La source, datée |
|---|---|---|
| Lieux de consultation | **4** (Mbouda, Bafoussam, Africa Médical · Douala, Hôpital Charity · Bonabéri) | `js/config/doctor.js`, `locations` |
| Horaires communiqués | **0 sur 4** — « horaires à confirmer » partout | même fichier, `hours: ""` |
| Jours communiqués | **6 sur 7** (lundi → samedi), avec **un conflit** le vendredi | message du médecin 26/10 17:53 contre l'affiche du cabinet |
| Pages de réservation gratuites sur un compte Google personnel | **1** | documentation Google, relevée 27/10 |
| Ressources d'un domaine tiers chargées par le site | **0** — c'est un test (`logique.test.mjs` §7) | `tests/logic.test.mjs` |
| Cookies, mesure d'audience, `fetch` | **0** — c'est un test | même fichier |
| Promesse affichée sous le formulaire | « une demande n'est pas un rendez-vous confirmé » | `appointment.disclaimer`, FR et EN |

**La contrainte dure, en une phrase :** nous savons déjà poser un bouton qui réserve, mais nous ne
savons pas encore **quelles heures** il pourrait proposer — et une page de réservation se construit
précisément sur ces heures.

## 2 · Trois routes, et ce que chacune coûte

### Route A — un lien de réservation, pas une intégration

Un bouton sortant vers la page Google Agenda du médecin. Le patient choisit un créneau, il est réservé
dans l'agenda du médecin ; le site, lui, ne charge rien et n'apprend rien.

- **Coût** : une constante dans `js/config/doctor.js`.
- **Ce que ça casse** : deux phrases (« aucune connexion à un agenda », « aucune synchronisation ») et un
  champ (`meta.liveSync`). Tout le reste tient.
- **Limite honnête** : sur l'offre gratuite, **une seule** page de réservation — donc un seul jeu de
  plages horaires. Avec quatre lieux, cette page ne peut pas dire « lundi Mbouda, mercredi Bafoussam ».
  Une page par lieu demande Google One Premium ou un Workspace payant.

### Route B — la page de réservation dans une iframe

- **Ce que ça casse** : trois tests rouges le jour même (domaine tiers, cookies, `liveSync`), la
  promesse « aucun appel à un tiers » du `llms.txt`, et la CSP de `_headers` (`default-src 'self'`).
- **Ce que ça n'apporte pas** : le patient ne quitte pas la page — c'est le seul gain, et il se paie
  d'un cookie Google posé sans consentement. **Écartée.**

### Route C — une vraie synchronisation (OAuth + fonction serverless)

Créneaux libres affichés sur la page, réservation sur place.

- **Ce que ça exige** : un compte de service ou un OAuth avec jeton à rafraîchir, une fonction Vercel, un
  secret, une gestion d'erreur quand Google tombe, et une politique de confidentialité (on manipule
  alors la disponibilité d'un médecin).
- **Ce que ça apporte en plus de A** : le créneau se voit **sans quitter la page**. Pour un patient
  camerounais qui consulte sur téléphone, ce gain est réel mais faible : le lien Google s'ouvre dans le
  même navigateur, en deux secondes.
- **Verdict** : disproportionnée **maintenant**. À rouvrir si le médecin ouvre la réservation à plusieurs
  structures avec des agendas distincts.

## 3 · Ce qu'on construit ce tour (A, éteinte)

| Élément | Où | Comportement |
|---|---|---|
| `bookingUrl: ""` | `js/config/doctor.js` | vide = rien n'est branché |
| Validation du lien | `js/booking.js` (nouveau) | `https` obligatoire, hôte dans `BOOKING_HOSTS`, sinon bouton absent |
| `meta.liveSync` | `js/config/doctor.js` | **déduit** de `bookingUrl`, plus jamais écrit à la main |
| Le bouton | `index.html` + `renderBooking()` | bloc `hidden` en dur, **sans href** avant JS : aucun bouton mort |
| Les deux phrases | `liveCopyKey()` | une seule fonction choisit les variantes, pour les deux à la fois |
| Le panneau « à publier » | `renderInfoDialog()` | ligne « Réservation en ligne » cochée ou non |
| Les tests | `tests/logic.test.mjs` §9 | 7 vérifications neuves (59 au total) |

**Décision de conception, écrite pour ne pas être rouverte :** le lien est un `<a target="_blank"
rel="noopener noreferrer">`, jamais une iframe, jamais un script. Le jour où quelqu'un voudra
« intégrer » l'agenda, un test tombera avant la page.

**Ce que je n'ai pas fait, exprès :** remplacer le CTA du hero par le lien de réservation. Tant que le
patient peut arriver sur `#appointments` et y trouver les deux chemins (créneau ou demande), le hero
n'a pas à changer de destination — et changer sa cible en JavaScript ajouterait une dépendance à JS sur
le geste le plus important de la page.

## 4 · Ce que le tour laisse ouvert, et à qui

1. **Les horaires** — les quatre lieux, et le vendredi tranché. Rien ne se branche avant. *Le médecin.*
2. **Une page par lieu, ou une seule ?** — dépend de son abonnement Google et de son organisation. *Le
   médecin, à qui la question doit être posée en même temps que les horaires.*
3. **La promesse du créneau.** Une page de réservation transforme une demande en engagement. Si le
   médecin ne tient pas ses créneaux, la page fait plus de dégâts que WhatsApp. *Décision de King, à
   prendre avec lui, pas pour lui.*
