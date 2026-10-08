# VIDEO 7 — REPLAN (rulings King 06/10, diagnostic accepté)

> Diagnostic adopté : **(b)+(c) cause première** (falaise 0:02 produite par l'ouverture diaporama —
> #4 figé jusqu'à 4,78 s ; fond-EN sans narration au fichier), **(a) cause secondaire de conversion**
> (86–91 % de 18–34 ans face à un acheteur 35–55), **(d) données insuffisantes** (3 posts comparables
> à créneau fixe pour trancher). Sources : `pipeline/ANALYTICS-LOG.md`, `strategy/POSTING-CALENDAR.md`.

## Règles de production (1–7 acceptées + 8 ruling)

1. Premier mouvement ≤0,8 s ; gate **FFmpeg** sur le master avant publication (zéro fenêtre figée
   ≥1 s dans les 5 premières s).
2. Premier mot à l'écran à 0,3 s + voix **dans le fichier à 0 s** ; jamais son tendance seul.
3. Hook = problème de l'acheteur en 3 s, parlé + écrit (FR TikTok).
4. Sous-titres chaque frame parlée, lisibles à un bras.
5. ≤25 s ; CTA à ≤20 s, au milieu.
6. Double canal : TikTok + statut WhatsApp/FB pour les 35–55.
7. Gate de publication : lecture ≥12 s ou complétion ≥15 %, sinon on corrige, on ne reposte pas.
8. **Un variable par test (ruling King 06/10, option b adoptée) :** V7 ne change QUE les deux
   leviers principaux — **mouvement ≤0,8 s + voix dans le fichier à 0 s**. Le reste (sous-titres
   systématiques, CTA milieu, ≤25 s, double canal) est **tenu pour V8**. Trois cycles de test
   (V7, V8, V9) avant la kill rule **04/11**.

## Concept retenu : C1 « L'annuaire ne suffit pas » (C2/C3 écartés)

- Hook 3 s : « Vous êtes dans l'annuaire de l'Ordre. » + mouvement ≤0,8 s sur le **format** du
  répertoire ; voix 0 s.
- Problème → résolution → offer : 150+ noms, zéro monture visible avant d'entrer (fait CRM) → une
  page qui montre les montures + WhatsApp (maquette publique fictive, labellisée) → « Écrivez
  PREVIEW en message privé. »
- Footage : captures du **format** de l'annuaire ONOC (structure des champs + agrégat « 150+ noms » ;
  **aucune entrée individuelle réelle visible** — cadrage/flou sinon) + recherche Google réelle +
  scroll démo. Aucune UI d'app ; aucun travail DM Optique ; zéro stock. Signal dominant :
  opticien-facing.

### Modification 1 (ruling) — aucun nom réel d'opticien dans le hook
Montrer le **format** de l'annuaire et l'agrégat « 150+ noms », jamais une entrée individuelle réelle
(risque social : pair exposé en négatif sur un marché étroit). Si une entrée est nécessaire au
visuel : **échantillon fictif clairement labellisé**. **Ruling 06/10 (option 1) :** le hook C1 =
format + agrégat seulement ; le re-pull ONOC du 11/10 sert **uniquement la vague opticiens du 12/10**
(messages d'outreach), pas la vidéo — C1 ne dépend donc pas du 11/10, et le créneau conditionnel du
08/10 tient.

### Modification 2 (ruling) — workflow PREVIEW défini AVANT publication
« Écrivez PREVIEW » est une promesse ; le workflow est ci-dessous et doit exister avant que C1 parte.
Template : `ops/templates/PREVIEW-ONE-PAGE-OPTICIEN.md`.

## Workflow PREVIEW (ruling King 06/10)

- **Quoi :** maquette une page (PDF) générée depuis une capture d'annuaire + le nom du demandeur —
  hook du problème + aperçu de page (montures + WhatsApp), pas un site complet.
- **Délais (ruling King 08/10) :** build **≤15 min** (orchestrateur : PDF une page depuis la capture
  d'annuaire + nom du demandeur) · relecture King **≤1 h** après réception du PDF · **envoi le même
  jour ouvré si le DM arrive avant 15h WAT ; le lendemain matin si après.** Arithmétique : 15 min +
  1 h = 1 h 15 au pire — « sous l'heure » est une cible, la règle ferme est le jour même.
- **Canal :** **WhatsApp** (canal acheteur ; l'IG DM n'est pas celui des opticiens).
- **Qui :** l'orchestrateur génère (plafond ruled ≤15 min ; mon chiffre antérieur « <10 min » n'était
  pas testé — remplacé) ; **King relit et envoie**. Jamais d'envoi direct orchestrateur.
- **Promesse tenue :** un PREVIEW livré tard = pire que pas de PREVIEW.

## Timing de publication — REPLAN 08/10 (ruling King)

Le créneau jeudi 08/10 n'a pas tenu (pas de master, script en hold). **Nouveau : C1 publie vendredi
09/10, 18:00–20:00, TikTok FR, seulement si le master passe le gate FFmpeg.** Si le master échoue :
**C1 est tué pour ce cycle** — on ne publie pas un test cassé. La vague 12/10 part alors sans
warm-up : **soft miss, pas crise.** (a) workflow PREVIEW documenté ✓ (ce fichier) · (b) gate FFmpeg ·
(c) priorité v06 : voir collision ci-dessous.

⚠️ **COLLISION OUVERTE — vendredi 09/10 :** le ruling 05/10 (`CONTENT-PIPELINE.md` l.142) fixe
**v06 = mercredi 19h25 si dépôt encaissé, sinon vendredi 09/10.** Le dépôt n'est pas encaissé (King,
08/10) → v06 est dû vendredi 09/10, le même jour que C1. Deux publications, un seul créneau TikTok
fixe : **à arbitrer par King** (v06 inchangé vendredi + C1 glisse ; ou C1 vendredi 18:00–20:00 et v06
re-daté ; ou les deux, à des heures différentes — au prix de la comparabilité du créneau fixe).

## Script C1 — DÉLIVRÉ vendredi 09/10 matin (ruling King 08/10)

Toujours voulu. **Livraison : vendredi 09/10 au matin** (script verbatim + liste de captures,
téléphone, ~20 s). Contrainte réelle : script le matin → captures de King → master → gate FFmpeg
avant 18:00, une seule journée ; si ça ne tient pas, la règle de kill s'applique (pas de dérive de
créneau).

## Bookmark — « building in public » : CLOS pour maintenant

L'app est LLM-built : pas de sketches, pas de progrès filmables. L'angle meurt jusqu'à une beta avec
vraie UI ; il redevient viable en territoire Video-7-redo. (Ruling King 06/10.)
