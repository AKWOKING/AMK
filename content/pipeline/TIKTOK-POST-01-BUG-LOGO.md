# TikTok AMK — POST 01 (v3 — version silencieuse, ruling King 12/10 « build spec » — NE PAS PUBLIER)

**Pilier :** **debug-in-public** (série nommée — ruling King 12/10 ; ex « build-in-public »).
**Angle :** **le résultat d'abord, le bug comme moteur.** Le premier plan montre le cercle propre ;
le titre reste honnête sur le processus.
**Titre / accroche :** « Un bug d'affichage qu'on a mis 2 jours à comprendre. »
**Format :** screen-led, esthétique Kamo (fond sombre, texte court en gras, mock terminal), **FR**,
**38,5 s**, **1080×1920**, pas de visage, **VO voice-00 + SFX synthétisés maison** (aucune musique
dans le fichier — King peut ajouter un son platform-native au téléversement TikTok, zéro licence).
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
5. **Rendu :** Chromium headless (moteur `tools/video/`) → frames → **ffmpeg** → MP4 H.264,
   1080×1920, 30 fps. **Audio (ruling 12/10 v4) :** VO = 6 clips `voice-00` (plateforme, choix King)
   posés à beat+0,15 s ; SFX synthétisés en sandbox (whoosh de slide à chaque transition, impact
   « ball drop » quand le disque tombe, pop au démasquage, blip au fix, carillon signature, ticks de
   frappe pendant le code) ; mix → AAC muxé. **Test-first : dummy 3 s validé par King avant le complet.**
6. **QA avant rendu final :** `AMK-DESIGN-SKILLS.md` §9 (motion : transform/opacity uniquement,
   easings maison, jamais d'entrée depuis scale(0)) + §13 (console 0 erreur, contraste) +
   `tools/qa/audit_video_motion.py` sur le MP4.

## Script — beat / écran / overlay (gras) / caption (petit)
| Beat | Écran (page de test AMK, rendu) | Overlay (gras) | Caption (narrative) |
|---|---|---|---|
| 0–5,5s | Hero, **cercle propre** (logo AMK dans l'anneau) | « Ce logo paraît normal. » | « Ce logo, il paraît normal. Il nous a pris deux jours. » |
| 5,5–10,5s | État `broken` : cercle = anneau seul, intérieur vide | « Jour 1 : le logo invisible. » | « Au départ, le cercle était vide. Le logo ne s'affichait pas. » |
| 10,5–16,5s | État `repro` : `contain`, sans masque → le logo AMK revient | « Hypothèse 1 : le rognage. Faux. » | « On enlève le masque : le logo revient. Donc ce n'était pas le rognage. » |
| 16,5–25s | Le `::before` mis en évidence : un **disque** plein sur le logo + panneau de code (frappe) | « Hypothèse 2 : un disque peint par-dessus. » | « L'« anneau » était en fait un disque plein, peint au-dessus du logo. » |
| 25–33,5s | Le fix : anneau en bordure, logo au-dessus → cercle propre + panneau de code (frappe du fix) | « Le fix : creuser l'anneau. » | « On creuse l'anneau, le logo passe au-dessus. Résultat : propre. » |
| 33,5–38,5s | Retour hero propre + signature | « AMK — on construit, on casse, on comprend. » | « C'est ça, faire un site sérieux. » |

**Texte à l'écran : overlay en gras + caption narrative.** Les captions sont **manuels**
(règle 11/10 : jamais d'auto-générés) — ce sont les lignes ci-dessus, mot pour mot ; la **VO voice-00
lit exactement ces lignes** (ruling v4 12/10).
**Contrôle avant export (ruling 12/10) : aucune URL, aucun domaine, aucun monogramme client dans le
cadre — que du AMK.** **Pas de prix, pas de nom.**

## Variante rejetée (pour mémoire)
Ouvrir sur le bug (« le logo était cassé ») sans montrer d'abord le résultat : moins fort — le viewer
doit voir la preuve (le cercle propre) **avant** d'accepter l'histoire. On garde le résultat en premier
plan.

---

## Statut de production / publication (rulings King 12/10)

- **v2 confirmée par King** ; v3 = mise au format captions seules ; **v4 (ruling 12/10 nuit) = retour
  de la voix (voice-00) + SFX synthétisés** ; musique toujours absente du fichier (King au téléversement).
- La section « PORTE DE CONSENTEMENT » (11/10) reste **supprimée** — sans objet.
- **Fichiers :** dummy `content/pipeline/POST-01-DUMMY-2026-10-12.mp4` (test pipeline 3 s, à valider
  par King) puis complet `content/pipeline/POST-01-BUG-LOGO-2026-10-12.mp4`.
- **NE PAS PUBLIER** — approbation King requise sur le MP4 final. Publication visée : mardi 13/10.

---

## PARKÉ 12/10 nuit — RÉÉCRITURE À VENIR (framework Lot [42])

Le v4 final est un **asset de test** du nouveau framework, pas le post (ruling King 12/10 nuit :
3 défauts — pas de hook 0–3 s, pas de cadre narratif, ouverture « tuto design »). Mapping de
réécriture adopté (sources : `research/youtube-lessons/2026-10-12-batch-hooks/` rapports 22–25 §5,
consolidation `research/YouTube-Lessons.md` Lot [42]) :

- **NOUVEAU beat 0 (3–4 s) « contexte »** : la requête en une phrase — « Un site pour une clinique
  d'optique. Le logo fourni : un PDF. » (vidéo 24, set up the past).
- **B1 réécrit « désir + obstacle »** : en mots d'opticien, hook = pensée non dite (« il est beau…
  jusqu'au jour où on clique »), **zéro logo/marque en 0–3 s** (vidéos 23 + 25). 3 ouvertures
  candidates en at-bats → King tranche avant render.
- **B2/B4 : coût du problème avant la solution** : « 2 jours de recherche. Sur un site réel : un
  client clique et rien ne se passe. » (vidéo 25).
- **B5/B6 : transformation want ≠ need** : on voulait un logo propre, on repart avec une règle
  (`vector-effect`) (vidéo 24). Marque et signature **seulement en B6**, répétées identiques à
  chaque post (vidéos 22 + 23).
- **Gate ajouté : test du son coupé** — le clip doit se comprendre sans audio (vidéo 23).
- **Pari nommé du post (vidéo 25)** : « Nous croyons que montrer un vrai bug résolu installe la
  compétence perçue ; nous parions ce post sur des questions WhatsApp d'opticiens. » Outcome à
  logger : questions reçues (jamais « on a posté »).

Réécriture = prochaine tâche, sur ordre de King. Le MP4 v4 reste en place comme référence.
