# Prospect n°2 — CLINIQUE LA BÉTHANIE (Bonabéri, Douala)

*Ouvert le 17 Sep 2026 en fin d'après-midi, après l'envoi d'Afrique Labo (prospect n°1) et la finalisation de L'Opticien.*
**Statut : concept construit et audité — en attente du déploiement + de l'envoi par King.**

## 1 · Trois portes (§8b) — VERDICT : 3/3 ✅
| Porte | Verdict | Preuve |
|---|---|---|
| **A · Joignabilité** | ✅ **PASS (King, 17 Sep)** | **677 76 07 82** confirmé sur WhatsApp (capture de King « +237 77760782 » = même ligne en format 8 chiffres). C'est la ligne câblée dans les 6 boutons WhatsApp du concept. |
| **B · Intention digitale** | ✅ PASS | **210 clics WhatsApp** via DoualaTour ; présence active dans les annuaires santé (Medicoor, Maligah, réseau ASCOMA) : les patients les cherchent déjà par téléphone. **Aucun site propre trouvé** → leur crédibilité visible dépend d'annuaires tiers qu'ils ne contrôlent pas. |
| **C · Acheteur** | ✅ PASS | Clinique privée dirigée par **Dr Richard PETIEU** (chirurgien) — propriétaire-décideur nommé. |
**Score 3/3 → on construit et on envoie.**

## 2 · Ce que les sources disent (re-vérifié le 17 Sep)
- Raison sociale publiée : **« Clinique La Béthanie-Ginteam »**, **Ancienne Route Bonabéri**, **Rue Mpondo**, BP 4 916 Douala.
- **Dr Richard Petieu**, chirurgien — annuaire du **réseau de soins ASCOMA** (édition 2021), fiches Medicoor / Maligah.
- ⚠️ Deux entrées d'annuaire coexistent (« CENTRE MEDICALE LA BETHANIE » / « Clinique La Bethanie-Ginteam ») et les informations datent de **2021** → c'est exactement le problème : leurs données publiques sont périmées et dispersées.

## 3 · Ce que la clinique a livré elle-même (uploads King, 17 Sep)
- **Dépliant « Service de gynécologie »** (`clients/la-bethanie/Clinique La Béthanie (Bonabéri).jpg`) : « Votre santé intime, notre priorité » ; six prestations ; **683 76 74 13 / 699 73 15 48** ; « BONABÉRI – RUE MPONDO (ANCIENNE ROUTE), DOUALA » ; **OUVERT 24H/24 · 7J/7** ; palette bleu royal + vert feuille ; typographie Montserrat.
- **Photo de l'entrée** (`entrance … .jpg`) : bâtiment jaune, grille verte, enseigne blanche « LA BETHANIE — Centre Médico-Chirurgical, Maternité », Tél. **677 76 07 82 / 683 … 74 13** ; bloc « NOS SPÉCIALITÉS » (gynécologie-obstétrique, médecine générale, chirurgie générale lisibles — le reste est trop flou pour être utilisé).
- **Conséquence de méthode :** le concept est bâti **sur leur propre matière** (dépliant + photo réelle), pas sur des suppositions.

## 4 · Concept livré — « LA CONSULTATION »
`demos/concept-labethanie-v1.html` (257 KB, single-file, base64, FR|EN) · builder `demos/build_labethanie.py` (paramétrable `--wa/--out`) · mockup `demos/shots/mockup-labethanie-wa.jpg` (191 KB) · preview `hosting/previews/labethanie/`.
**Déployé le 17/09 par King : https://labethanie-concept.vercel.app** (vérifié : page complète, 6 liens WhatsApp vers la ligne réelle).
Sections : hero (photo réelle de l'entrée + « Votre santé intime, notre priorité ») · **urgences 24h/24 · 7j/7** (appel + WhatsApp) · **service de gynécologie** avec les 6 prestations du dépliant en **liste à cocher → un seul message WhatsApp discret** (rien n'est stocké sur la page) · « une première consultation, comment ça se passe » · **chirurgie** (centre médico-chirurgical, direction Dr Petieu) · **nous trouver** (Rue Mpondo / Ancienne Route, repère « bâtiment jaune, grille verte », plan schématique, photo de l'enseigne) · FAQ (5) · contact + sticky WhatsApp/appel · **aucun prix** (aucun n'est publié) · **aucun nom de patient, aucun témoignage**.
Audit : `python3 tools/qa/audit_html.py` → **0 finding** (222 runs, desktop + mobile). Détail des décisions : `clients/la-bethanie/build-notes.md` · références live : `clients/la-bethanie/inspiration.md`.

## 5 · Prochaines étapes
1. **King** : déployer `hosting/previews/` → l'aperçu `/labethanie/` · QA téléphone · **envoyer image d'abord** (§2e du Send-Sheet 17/09).
2. Réponse « oui » → lien + 2 questions (photos/vraie ligne ; qui décide ?) puis collecte : logo, photos (accueil, salle d'accouchement, bloc, labo), liste exacte des services, numéro WhatsApp définitif.
3. À faire confirmer par la clinique : quel numéro est **le** WhatsApp (677 76 07 82 supposé) et si **683 76 74 13 / 699 73 15 48** sont toujours actifs ; la liste de chirurgie ; l'accord pour nommer le Dr Petieu.
4. Relances : **à poser le jour de l'envoi** (M+2 · M+4 · M+7, max 3).
