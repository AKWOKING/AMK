# TikTok AMK — POST 01 (v2 — ruling King 12/10 « script reframe » — pour confirmation finale, NE PAS PUBLIER)

**Pilier :** **debug-in-public** (série nommée — ruling King 12/10 ; ex « build-in-public »).
**Angle :** **le résultat d'abord, le bug comme moteur.** Le premier plan montre le cercle propre ;
le titre reste honnête sur le processus.
**Titre / accroche :** « Un bug d'affichage qu'on a mis 2 jours à comprendre. »
**Format :** screen-led, esthétique Kamo (fond sombre, texte court en gras, mock terminal), **FR**,
**sous-titres manuels** (règle 11/10 : jamais d'auto-générés), **30–45 s**, pas de visage.
**Zéro référence client (ruling King 12/10) :** aucun nom, aucune URL, aucun domaine, aucun
monogramme client. Tout est reconstruit sur une **page de test AMK** avec le **logo AMK**. Le travail
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

## À construire avant l'enregistrement (nouveau — v2)
**Page de test AMK** reproduisant le bug à l'identique : le `::before` en **disque plein** peint
au-dessus du logo AMK placé dans l'anneau. Trois états sur la page : cassé (logo invisible) · repro
minimal (`contain`, sans masque) · propre (fix anneau en bordure). Domaine AMK ou fictif — **jamais
un domaine client dans le cadre ni dans la barre d'adresse.**

## Script + shot list (beat / plan / overlay / voix)
| Beat | Plan (screen record — page de test AMK) | Overlay (gras, court) | Voix off (FR) |
|---|---|---|---|
| 0–4s | Hero de la page de test, **cercle propre** (logo AMK dans l'anneau) | « Ce logo paraît normal. » | « Ce logo, il paraît normal. Il nous a pris deux jours. » |
| 4–11s | État cassé : cercle = anneau seul, intérieur vide (logo AMK invisible) | « Jour 1 : le logo invisible. » | « Au départ, le cercle était vide. Le logo ne s'affichait pas. » |
| 11–19s | Repro minimal : `contain`, sans masque → le logo AMK revient | « Hypothèse 1 : le rognage. Faux. » | « On enlève le masque : le logo revient. Donc ce n'était pas le rognage. » |
| 19–30s | Le `::before` mis en évidence : un **disque** plein sur le logo | « Hypothèse 2 : un disque peint par-dessus. » | « L'« anneau » était en fait un disque plein, peint **au-dessus** du logo. » |
| 30–40s | Le fix : anneau en bordure, logo au-dessus → cercle propre | « Le fix : creuser l'anneau. » | « On creuse l'anneau, le logo passe au-dessus. Résultat : propre. » |
| 40–45s | Retour hero propre + signature | « AMK — on construit, on casse, on comprend. » | « C'est ça, faire un site sérieux. » |

**Sous-titres manuels FR** sur chaque beat, mot à mot ce que dit la VO.
**À screen-recorder :** hero propre de la page de test AMK · capture de l'état cassé · le snippet
CSS du `::before` · le snippet du fix (deux fonds padding-box/border-box) · retour hero propre.
**Contrôle avant export (ruling 12/10) : aucune URL, aucun domaine, aucun monogramme client dans le
cadre — que du AMK.** **Pas de musique sous la voix** si elle couvre la VO ; sinon nappe discrète.
**Pas de prix, pas de nom.**

## Variante rejetée (pour mémoire)
Ouvrir sur le bug (« le logo était cassé ») sans montrer d'abord le résultat : moins fort — le viewer
doit voir la preuve (le cercle propre) **avant** d'accepter l'histoire. On garde le résultat en premier
plan.

---

## Statut de publication (ruling King 12/10)

La section « PORTE DE CONSENTEMENT » (11/10) est **supprimée** — sans objet : plus rien
d'identifiable n'apparaît dans la vidéo (logo AMK sur page AMK). **Publiable mardi 13/10 — après la
confirmation finale de King sur cette v2. Ne pas publier avant.**
