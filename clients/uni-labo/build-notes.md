# UNI-LABO — notes de construction

**Client :** UNI-LABO, laboratoire d'analyses de biologie médicale — Carrefour Etoo, Bonamoussadi (Makepe
Bloc L), Douala · Rue 5N441 · BP 2592 · 07h–19h (sam. 13h) · WhatsApp 696 13 98 19.
**Fichiers :** `demos/concept-unilabo-v1.html` (canonique) → `hosting/previews/unilabo/index.html`
(+ `og.jpg`, + `img/` : les quatre photos) → **racine du projet Vercel `uni-labo.vercel.app`**.
**État :** page retravaillée le 23/09 au soir (audit `AUDIT-2026-09-23.md` → passe §8). Rendez-vous de
clôture **vendredi 25/09 à 13 h**, à leur laboratoire. Prix posé : 150 000 FCFA (acompte 75 000).

## 1 · La lecture

Un laboratoire ne vend pas des analyses, il vend **la certitude que le prélèvement sera utilisable**.
Tout se joue **avant** l'arrivée : une analyse mal préparée, c'est un déplacement perdu et une piqûre pour
rien. Leur page en ligne le sait déjà (cinq panneaux de préparation) mais le dit **en paragraphes** ; nous
le disons **avec l'objet** : la fiche de prélèvement. Le visiteur est un patient pressé, souvent envoyé par
un médecin, parfois à jeun depuis le matin, qui veut trois choses — suis-je au bon endroit, que dois-je
faire avant, comment je prends rendez-vous. La page répond dans cet ordre.

## 2 · Les molettes (§2)

| VARIANCE | MOTION | DENSITY |
|---|---|---|
| **6** — la fiche est un objet qu'aucun autre site de labo ne porte ; la frise passe en bandeau à quatre colonnes | **3** — un seul mouvement signé (l'appui à 140 ms) et l'état d'ouverture qui se calcule ; aucune entrée animée, rien qui cache du contenu | **7** — beaucoup de matière (préparation, familles, retrait, FAQ), mais portée par des filets et des listes, jamais par six cartes égales |

## 3 · La différence (§19, registre)

| Axe | UNI-LABO | Le voisin le plus proche |
|---|---|---|
| Objet dominant | **la fiche de prélèvement**, en trois états | Afrique Labo : console de tarifs ; Cristallin : échelle d'acuité |
| Palette | papier froid `#F4F5F7` + **un seul violet `#5B21B6`** (+ vert WhatsApp pour les seules actions d'envoi) | Afrique Labo : cyan poster + navy ; OraCare : crème/or |
| Typographie | **Sora** (display) + **Public Sans** (texte) | Afrique Labo : Space Grotesk ; Univers : Bricolage Grotesque |
| Rythme | frise à quatre colonnes sous le hero, puis bandeaux photo + fiches | Afrique Labo : sections numérotées ; Cristallin : lignes décroissantes |
| Signature | **la fiche vivante du formulaire** qui se remplit, et la ligne « Préparation » déduite de leurs propres textes | aucune ailleurs |
| Ton | « voici ce qu'il faut faire avant de venir », tutoiement de guichet → vouvoiement | Afrique Labo : réponses de guichet |

## 4 · Les règles appliquées, et où

- **§15.bis** : quatre photos générées, relues, légendées « Mise en situation… » ; fichiers séparés (§15.6).
  **La préparation a été regénérée le 23/09 sur correction de King** (« no one lives in that type of
  house ») : la première version montrait une maison de village, la version retenue un intérieur de ville
  (carrelage, cuisine à gaz, réfrigérateur, ventilateur sur pied). Le décor doit être celui du patient, pas
  celui qu'on imagine pour lui.
- **§13** : `prefers-reduced-motion`, focus visible sur tout le focusable, cibles 44 px, contraste AA
  (mesuré : encre/papier 16,7 · blanc/violet 8,98 · blanc/vert WhatsApp 5,43).
- **§3.4** : trois étiquettes en casse de phrase au total, aucune numérotée, aucun point d'état décoratif
  (le point de la barre du haut est **calculé** à l'heure de Douala).
- **§20.8** : chaque phrase existe en trois endroits (`data-fr`, `data-en`, le nœud visible) — les
  remplissages du formulaire sont écrits dans les deux langues dans le JavaScript, pas dans le HTML.
- **§21/09** : « un bouton n'existe que s'il a une URL dans le HTML » — l'envoi du formulaire est un `<a
  href>` réel, que le JavaScript enrichit ; incomplet, il garde le message générique.
- **Honesteté** : aucun prix, aucun avis, aucun `aggregateRating`, aucun `sameAs`, aucune photo présentée
  comme la leur, aucune donnée stockée (le message part du téléphone du patient).

## 5 · Ce qui reste, et ce qui n'est pas à nous

1. **Redéploiement** du dossier `hosting/previews/unilabo/` (King — Vercel, glisser-déposer).
2. **Photos définitives** : le jour de la livraison, trois clichés au laboratoire (accueil, paillasse,
   salle de prélèvement) — la page porte déjà les emplacements et les légendes.
3. **`noindex,nofollow`** à retirer le jour où c'est LEUR site sur LEUR domaine.
4. Couleurs, si le client veut les siennes : la famille violette vient de l'aperçu du 18/09, elle n'est pas
   un choix de leur charte.
