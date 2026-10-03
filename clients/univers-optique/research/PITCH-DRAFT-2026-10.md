# PITCH DRAFT — Univers Optique (virtual try-on) · v2 du 03/10 · RIEN NE PART AVANT : mercredi passé + revue King + réponse collaborateurs

> **Ruling King 03/10 — architecture LOCAL-ONLY.** Le client veut l'outil **uniquement sur son téléphone
> et ceux de ses collaborateurs** : rien d'hébergé sur le web, rien qu'un concurrent puisse parcourir —
> son catalogue est son avantage compétitif. Notre recommandation « web beats app » (recherche §3) est
> **battue par son exigence** : exigence client > recommandation (règle générale 03/10, playbook).
> **Pricing 03/10 :** pilote **900 000 FCFA** (450/450 ; pushback → 300/300/300, jamais moins) ·
> standard **1 400 000 FCFA** · mensuel **30 000 FCFA** (endpoint sync si utilisé, maintenance, ≤ 4 h/mois).
> Recherche complète + décision local-only : `try-on-options-2026-10.md` §3 (note ruling) et §8.

## Brouillon EN (verbatim ruling 03/10 — sa langue au rdv)

```
Good morning! I've priced the try-on tool exactly as you described it: one photo of the client, then
your frames on their face, swiped one by one. Installed only on your phone and your collaborators'
phones — nothing on the web, nothing a competitor can browse. Your catalogue stays yours. As our
pilot, with the right to publish the result as a case study once it's live: 900 000 FCFA, split
450 000 to start and 450 000 on delivery. The standard price for any other optician will be
1 400 000. The written scope is ready whenever you want to see it.
```

FR sur demande. Pas de bullet, pas de signature (standard maison).

## Cadrage (ne pas dévier)
- **Le 900k ne s'excuse pas.** Ce n'est pas un premium d'exclusivité : c'est le coût honnête d'un build
  local-only (packaging Android/sideload, tests devices, permissions, stockage offline, flow de mise à
  jour). Le 750k antérieur datait de la version web — celle qu'il ne voulait pas. Le dire tel quel.
- **Pushback → phaser le split 300/300/300.** Jamais réduire le total. Jamais trader le scope.
- **« your collaborators' phones » ne commit à aucun nombre.** Le scope exact attend la réponse :
  lui + 1–2 = APK sideloadé + reinstall au update (MVP) ; équipe de comptoir multi-shifts = catalogue
  partagé + mécanisme de mise à jour, voire endpoint sync privé device-ID-gated. La question est posée
  à King (puis au client après mercredi) — voir le suivi.
  **Réponse King 03/10 : inconnu.** Le pitch part **tel quel** (« your collaborators' phones ») après mercredi ET après revue ; le scope du build se fixe à la réponse du client, jamais avant.
- Le PDF de scope (`try-on-options-2026-10.md` §8) part **seulement s'il le demande**.
