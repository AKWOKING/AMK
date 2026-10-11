# TikTok AMK — POST 01 (recommandé, pour revue King — NE PAS PUBLIER)

**Pilier :** build-in-public (variante « avant/après » des titres approuvés).
**Angle (mon choix, ruling King ouvert) :** **le résultat d'abord, le bug comme moteur.** Le premier
plan montre le cercle propre ; le titre reste honnête sur le processus.
**Titre / accroche :** « Un bug d'affichage qu'on a mis 2 jours à comprendre. »
**Format :** screen-led, esthétique Kamo (fond sombre, texte court en gras, mock terminal), **FR**,
**sous-titres manuels** (règle 11/10 : jamais d'auto-générés), **30–45 s**, pas de visage.
**Client : non nommé** (« un opticien de Douala ») — nommer exige consentement (`RULE-CREDENTIAL-CLAIMS`).
**Règle debout respectée :** on raconte **notre raisonnement**, jamais « l'IA a fait » (problème →
raisonnement → décision → résultat).

## Pourquoi CE post en premier
- C'est le seul des 9 titres dont l'**artefact réel est prêt maintenant** : toute l'histoire est
  documentée (`content/pipeline/VIDEO-12-CANDIDAT-BUG-AFFICHAGE.md`, commits `ffe789b`/`33628b6`).
- Prouve la compétence sans vendre : on montre qu'on **casse, comprend, répare** — crédibilité, pas pitch.
- Concret et falsifiable (§3.8 copy gate) : le bug se voit, le fix se voit. Pas d'adjectif orphelin.
- Évite les deux pièges : pas de liste de prix, pas de cadre client sans consentement.

## Script + shot list (beat / plan / overlay / voix)
| Beat | Plan (screen record) | Overlay (gras, court) | Voix off (FR) |
|---|---|---|---|
| 0–4s | Hero live, **cercle propre** (logo dans l'anneau) | « Ce logo paraît normal. » | « Ce logo, il paraît normal. Il nous a pris deux jours. » |
| 4–11s | État cassé : cercle = anneau seul, intérieur vide | « Jour 1 : le logo invisible. » | « Au départ, le cercle était vide. Le logo ne s'affichait pas. » |
| 11–19s | Repro minimal : `contain`, sans masque → le logo revient | « Hypothèse 1 : le rognage. Faux. » | « On enlève le masque : le logo revient. Donc ce n'était pas le rognage. » |
| 19–30s | Le `::before` mis en évidence : un **disque** plein sur le logo | « Hypothèse 2 : un disque peint par-dessus. » | « L'« anneau » était en fait un disque plein, peint **au-dessus** du logo. » |
| 30–40s | Le fix : anneau en bordure, logo au-dessus → cercle propre | « Le fix : creuser l'anneau. » | « On creuse l'anneau, le logo passe au-dessus. Résultat : propre. » |
| 40–45s | Retour hero propre + signature | « AMK — on construit, on casse, on comprend. » | « C'est ça, faire un site sérieux. » |

**Sous-titres manuels FR** sur chaque beat, mot à mot ce que dit la VO.
**À screen-recorder :** hero live propre · capture de l'état cassé · le snippet CSS du `::before` · le
snippet du fix (deux fonds padding-box/border-box) · retour hero propre.
**Pas de musique sous la voix** si elle couvre la VO ; sinon nappe discrète. **Pas de prix, pas de nom.**

## Variante rejetée (pour mémoire)
Ouvrir sur le bug (« le logo était cassé ») sans montrer d'abord le résultat : moins fort — le viewer
doit voir la preuve (le cercle propre) **avant** d'accepter l'histoire. On garde le résultat en premier
plan.

---

## PORTE DE CONSENTEMENT (ruling King, 11/10) — avant publication mardi

Le texte dit « un opticien de Douala » (anonyme) mais les beats avant/après montrent le site live de
DM Optique : **le visuel est identifiable même si le texte ne l'est pas**. Avant publication mardi,
King envoie **lundi** une ligne WhatsApp à M. Domche :

> « Bonjour Monsieur, j'aimerais publier un court post sur la correction du logo — votre site reste
> anonyme dans la vidéo. D'accord ? »

**Gate opérationnelle :** accord explicite OU silence sans objection d'ici mardi matin → publier.
**Objection → aucun plan du site dans la vidéo** : remplacer les beats site par un mock anonymisé
(reconstruire les états cassé/propre sur un domaine fictif). Le site reste live quoi qu'il arrive —
le message est une courtoisie, pas une condition de mise en ligne.
