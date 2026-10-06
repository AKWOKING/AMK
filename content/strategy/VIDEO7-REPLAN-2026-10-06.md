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
- Footage : captures ONOC (page publique) + recherche Google réelle + scroll démo. Aucune UI d'app ;
  aucun travail DM Optique ; zéro stock. Signal dominant : opticien-facing.

### Modification 1 (ruling) — aucun nom réel d'opticien dans le hook
Montrer le **format** de l'annuaire et l'agrégat « 150+ noms », jamais une entrée individuelle réelle
(risque social : pair exposé en négatif sur un marché étroit). Si une entrée est nécessaire au
visuel : **échantillon fictif clairement labellisé**. Le re-pull ONOC du 11/10 fournit l'agrégat,
pas la cible.

### Modification 2 (ruling) — workflow PREVIEW défini AVANT publication
« Écrivez PREVIEW » est une promesse ; le workflow est ci-dessous et doit exister avant que C1 parte.
Template : `ops/templates/PREVIEW-ONE-PAGE-OPTICIEN.md`.

## Workflow PREVIEW (ruling King 06/10)

- **Quoi :** maquette une page (PDF) générée depuis une capture d'annuaire + le nom du demandeur —
  hook du problème + aperçu de page (montures + WhatsApp), pas un site complet.
- **Turnaround :** ≤4 h ouvrées (09:00–18:00) ; demande après 18:00 → lendemain 10:00. (Mon
  paramètre, ajustable sur un mot.)
- **Canal :** **WhatsApp** (canal acheteur ; l'IG DM n'est pas celui des opticiens).
- **Qui :** l'orchestrateur génère en <10 min par demandeur ; **King relit et envoie**. Jamais
  d'envoi direct orchestrateur.
- **Promesse tenue :** un PREVIEW livré tard = pire que pas de PREVIEW.

## Timing de publication — conditionnel, pas fixe

C1 publie **jeudi 08/10, 18:00–20:00** seulement si : (a) workflow PREVIEW documenté ✓ (ce
fichier) · (b) master passe le gate FFmpeg · (c) DM Optique n'a pas déclenché la priorité v06
(acompte encaissé mercredi). Sinon C1 glisse à la semaine suivante et la vague 12/10 part sans
warm-up — **soft miss, pas crise**.

## Script C1 — HOLD

Pas livré ce jour. Livraison **mercredi 07/10 matin, après la visite DM** : l'issue de mercredi
décide si C1 ou v06 est la prochaine production ; écrire avant = risque de travail mort.

## Bookmark — « building in public » : CLOS pour maintenant

L'app est LLM-built : pas de sketches, pas de progrès filmables. L'angle meurt jusqu'à une beta avec
vraie UI ; il redevient viable en territoire Video-7-redo. (Ruling King 06/10.)
