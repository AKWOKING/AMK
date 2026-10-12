# TikTok AMK — POST 01 (v3 — version silencieuse, ruling King 12/10 « build spec » — NE PAS PUBLIER)

**Pilier :** **debug-in-public** (série nommée — ruling King 12/10 ; ex « build-in-public »).
**Angle :** **le résultat d'abord, le bug comme moteur.** Le premier plan montre le cercle propre ;
le titre reste honnête sur le processus.
**Titre / accroche :** « Un bug d'affichage qu'on a mis 2 jours à comprendre. »
**Format :** screen-led, esthétique Kamo (fond sombre, texte court en gras, mock terminal), **FR**,
**~45 s**, **1080×1920**, pas de visage, **fichier silencieux** (aucune piste son dans le MP4 ;
la musique est ajoutée par King au téléversement TikTok — platform-native, zéro licence).
**Zéro référence client (ruling King 12/10) :** aucun nom, aucune URL, aucun domaine, aucun
monogramme client. Tout est construit sur une **page de test AMK** avec le **logo AMK**. Le travail
client qui a inspiré le bug **ne fait pas partie de l'histoire** — la vidéo dit « voici un bug qu'on
a résolu », point.
**Règle debout respectée :** on raconte **notre raisonnement**, jamais « l'IA a fait » (problème →
raisonnement → décision → résultat).

## Pourquoi CE post en premier
- L'histoire est réelle et documentée en interne (`content/pipeline/VIDEO-12-CANDIDAT-BUG-AFFICHAGE.md`,
  commits `ffe789b`/`33628b6`) — mais **à l'écran tout est reconstruit sur la page de test AMK** :
  aucun artefact client n'apparaît jamais.
- Prouve la compétence sans vendre : on montre qu'on **casse, comprend, répare** — crédibilité, pas pitch.
- Concret et falsifiable (§3.8 copy gate) : le bug se voit, le fix se voit. Pas d'adjectif orphelin.
- Zéro risque : pas de prix, pas de cadre client, rien d'identifiable → aucune porte de consentement.

## Méthode de production (ruling King 12/10 — orchestrator de bout en bout, PAS de screen recording)
1. **Page HTML** avec les trois états CSS du cas-test : `broken` (disque plein peint sur le logo) ·
   `repro` (`contain`, sans masque) · `clean` (fix : anneau en bordure, logo au-dessus).
2. **Transitions minutées** entre états, calées sur les six beats du tableau ci-dessous.
3. **Panneau de code animé** : frappe animée du `::before` fautif puis du fix, lisible (gros
   caractères, contraste AA).
4. **Deux couches de texte par beat :** overlay **gras** (Kamo, toujours à l'écran) + **caption**
   narrative en dessous, minutée sur le beat.
5. **Rendu :** Chromium headless (moteur `tools/video/`) → frames → **ffmpeg** → MP4 silencieux
   H.264, 1080×1920, 30 fps. **Test-first : dummy 3 s validé par King avant le rendu complet.**
6. **QA avant rendu final :** `AMK-DESIGN-SKILLS.md` §9 (motion : transform/opacity uniquement,
   easings maison, jamais d'entrée depuis scale(0)) + §13 (console 0 erreur, contraste) +
   `tools/qa/audit_video_motion.py` sur le MP4.

## Script — beat / écran / overlay (gras) / caption (petit)
| Beat | Écran (page de test AMK, rendu) | Overlay (gras) | Caption (narrative) |
|---|---|---|---|
| 0–4s | Hero, **cercle propre** (logo AMK dans l'anneau) | « Ce logo paraît normal. » | « Ce logo, il paraît normal. Il nous a pris deux jours. » |
| 4–11s | État `broken` : cercle = anneau seul, intérieur vide | « Jour 1 : le logo invisible. » | « Au départ, le cercle était vide. Le logo ne s'affichait pas. » |
| 11–19s | État `repro` : `contain`, sans masque → le logo AMK revient | « Hypothèse 1 : le rognage. Faux. » | « On enlève le masque : le logo revient. Donc ce n'était pas le rognage. » |
| 19–30s | Le `::before` mis en évidence : un **disque** plein sur le logo + panneau de code (frappe) | « Hypothèse 2 : un disque peint par-dessus. » | « L'« anneau » était en fait un disque plein, peint au-dessus du logo. » |
| 30–40s | Le fix : anneau en bordure, logo au-dessus → cercle propre + panneau de code (frappe du fix) | « Le fix : creuser l'anneau. » | « On creuse l'anneau, le logo passe au-dessus. Résultat : propre. » |
| 40–45s | Retour hero propre + signature | « AMK — on construit, on casse, on comprend. » | « C'est ça, faire un site sérieux. » |

**Texte à l'écran uniquement. Overlay en gras + caption narrative. Aucun son dans le fichier.**
Les captions sont **manuels** (règle 11/10 : jamais d'auto-générés) — ce sont les lignes ci-dessus,
mot pour mot.
**Contrôle avant export (ruling 12/10) : aucune URL, aucun domaine, aucun monogramme client dans le
cadre — que du AMK.** **Pas de prix, pas de nom.**

## Variante rejetée (pour mémoire)
Ouvrir sur le bug (« le logo était cassé ») sans montrer d'abord le résultat : moins fort — le viewer
doit voir la preuve (le cercle propre) **avant** d'accepter l'histoire. On garde le résultat en premier
plan.

---

## Statut de production / publication (rulings King 12/10)

- **v2 confirmée par King** (ruling « v2 script — CONFIRMED ») ; la v3 n'est que la mise au format
  silencieux ordonnée par le build spec (VO → captions, aucune piste son, musique laissée à King).
- La section « PORTE DE CONSENTEMENT » (11/10) reste **supprimée** — sans objet.
- **Fichiers :** dummy `content/pipeline/POST-01-DUMMY-2026-10-12.mp4` (test pipeline 3 s, à valider
  par King) puis complet `content/pipeline/POST-01-BUG-LOGO-2026-10-12.mp4`.
- **NE PAS PUBLIER** — approbation King requise sur le MP4 final. Publication visée : mardi 13/10.
