# LES 33 RAPPORTS DE VIDÉO, EN UNE PAGE — ce qui reste quand on a tout lu

**24/10/2026.** Ce document remplace la lecture de 29 rapports bruts (11–12/10/2026, 33 vidéos au total sur les neuf lots) : il dit **ce qui a
changé dans le dépôt**, **ce qui a été refusé et pourquoi**, et **ce qui reste ouvert**. Les rapports
eux-mêmes sont archivés — intacts, jamais supprimés — dans `archive/2026-10/youtube-lessons/`.
Le détail vidéo par vidéo reste dans `research/YouTube-Lessons.md`, lots [36] à [44].

## 0 · La méthode, qui est le vrai acquis

Chaque vidéo a suivi la même passe en six temps : capture de la source → audit des affirmations
(VERIFIED / UNVERIFIED / FALSE / **VENDOR SELF-REPORT**) → audit des outils → ce qui manquait → ce qu'on
adopte (avec sa destination) → résumé. Deux règles en sont sorties, et elles valent plus que n'importe
quelle leçon de contenu :

1. **Une affirmation sans source primaire n'entre pas.** Une vidéo sponsorisée est un tunnel de vente :
   ses chiffres sont classés `VENDOR SELF-REPORT`, jamais cités à un prospect.
2. **On n'adopte jamais une vidéo, on adopte une phrase et on la range.** Chaque adoption ci-dessous a
   une destination dans le dépôt ; ce qui n'en avait pas a été refusé.

## 1 · Ce qui a changé dans le dépôt

| Ce qu'on a retenu | D'où | Où ça vit maintenant |
|---|---|---|
| Cibler par **signal** (avis Google, activité FB/IG, travaux, changement de direction), pas par liste | v12–v13 (GTM) | `sales/RESEARCH-STANDARD.md` |
| **Rétro-ingénierie des deals gagnés** avant d'inventer un play : on n'automatise que ce qu'une transaction réelle confirme | v15 (Crawford) | `sales/RESEARCH-STANDARD.md` |
| « Pas de signaux sur étagère » — cohérent avec le biais gratuit | v15 | `ops/TOOL-SCAN.md` |
| Checklist SEO TikTok (10 gestes) | v3 (HubSpot) | `content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md` |
| **Le hook = la pensée non dite de l'audience**, jamais « voici comment on a corrigé » | v22–v25 (hooks) | `content/pipeline/TIKTOK-POST-01-BUG-LOGO.md` |
| **Pas de logo dans les 3 premières secondes** ; la marque arrive à la signature | v25 | idem |
| **Test du son coupé** : le clip doit se comprendre sans audio | v23 | idem (critère de gate) |
| **3 ouvertures candidates** avant render, une seule retenue | v23 | idem |
| Le format AMK est confirmé : **2D motion code→vidéo**, déterministe, rééditable | v16–v17, v26–v29 | pipeline POST-01…09, inchangé |
| Checklist de **6 tokens de design** (layout, styling, accent, ombres, typo, pairing) | v21, v31 | `AMK-DESIGN-SKILLS.md` |
| Checklist des **défauts de rendu** (texte sur fond de même luminance, texte coupé, chevauchement) | v26 | spec POST-01 |
| Feedback daté **par beat/seconde** (« à 10 s, le bandeau n'est pas lisible ») | v26 | méthode d'aller-retour avec King |
| **3 règles de closing WhatsApp** : nommer le problème dans leurs mots · prix en un message puis attente · cadrage revenu-pas-dépense | v32 | fichiers de vague `sales/` |
| Plancher du marché CM camerounais : **50 000 FCFA/mois** = le prix à ne pas casser | v33 (FR, Cameroun) | `sales/` (intelligence prix) |
| Ligne de service : **contenu premium au livrable**, jamais de retainer CM tout-venant | v33 | brief d'établissement |

## 2 · Ce qui a été refusé, nommément

Un refus nommé vaut une adoption : il empêche de reposer la question dans deux mois.

- **Le format stickman** (v28, v30) — anti-positionnement : c'est un template d'usine pour l'économie
  RPM, pas une preuve de compétence. Refusé deux fois, sur deux échantillons.
- **La manipulation** en vente (v32, la moitié « dark ») : douleur amplifiée, urgence fabriquée, ego
  coincé. Sur un marché méfiant, la confiance est l'actif n°1 — la première moitié (Cialdini sain) est
  gardée, la seconde est refusée.
- **Les agrégateurs « gratuits illimités »** (v19, et son doublon v18) : « free & unlimited » est un
  signal d'alarme, pas une offre. Seuls les free tiers officiels (Google Vids, Adobe Firefly) sont notés.
- **Les stacks payants** Clay / Salesforge / Apollo / Instantly / Midjourney / Veo (v12–v15, v27–v29) :
  aucun profit ne les justifie à notre échelle, et le biais est gratuit/open-source.
- **Les agents IA d'outbound** (v14, « Agent Frank ») : notre première ligne est humaine et vérifiée.
- **Le blogging automatisé** (v20) : heurte de front nos règles sur le contenu produit en série.
- **Les transcripts fictifs** comme méthode de test (v15) : une affirmation non vérifiée ne doit jamais
  entrer au CRM ni dans un message. On garde la méthode de Crawford, pas son raccourci.

## 3 · Ce qui reste ouvert

1. **Cadence TikTok** : la recommandation lue est 3–5/semaine ; notre cadence de test est plus basse.
   Revue prévue à J14, pas avant.
2. **Le trigger « avis Google »** est déjà dans notre détection de fuites : le formaliser comme *signal*
   change-t-il le scoring, ou seulement le vocabulaire ?
3. **Vendre aux CM et agences sous-équipés** (canal B2B2C, v33) : à tester seulement après les premiers
   clients directs.
4. **L'autopsie des deals perdus** (COMOBIL…) sans rouvrir le fil client : format interne à définir.
5. **Temps de render réel** d'un slide motion 1080×1350 dans notre environnement : non mesuré.

## 4 · Et deux trous, nommés

- **v20 (« Easy MCP / WordPress ») n'a pas de vidéo vérifiable** : le titre exact n'existe pas tel quel
  sur YouTube après cinq recherches. L'audit a été fait sur la documentation publique du produit, et
  c'est écrit dans le rapport. Si King tient à cette vidéo, il envoie l'URL ; sinon l'entrée reste sans
  source, ce qui est exactement ce qu'elle mérite.
- **v18 est un doublon de v11** (même vidéo, autre libellé). Traité en renvoi, pas rejoué. La leçon de
  process est dans le rapport : vérifier les identifiants de la file contre les lots déjà traités.

## 5 · Ce que ces vidéos disent de travers, et qu'il faut savoir

Trois familles d'affirmations reviennent sans preuve, et elles sont désormais **classées** :

| Type d'affirmation | Fréquence | Ce qu'on en fait |
|---|---|---|
| « X vues en Y jours » sur un compte neuf | très fréquent (v2, v10, v28, v30) | jamais cité à un prospect : un compte neuf peut être poussé par l'algorithme de test |
| « 100 % gratuit » / « illimité » | v11, v19, v28, v30 | traité comme un signal d'alarme ; on vérifie le free tier officiel |
| Chiffres de productivité d'un vendor (« 1 = 5 SDR ») | v13, v14 | `VENDOR SELF-REPORT`, jamais un argument de vente |

Aucun de ces chiffres n'entre dans une proposition commerciale. C'est la règle §1g, et ces 33 vidéos
sont exactement le genre de source qui l'aurait violée sans elle.

## 6 · Ce qui n'a pas été archivé, et pourquoi

Archiver n'est pas « ranger tout ce qui traîne » : c'est retirer ce dont la conclusion est déjà
ailleurs. Cinq fichiers restent donc en place, et pour une raison chacun :

- les **quatre index des lots [36] à [39]** — `research/youtube-lessons/2026-10-11-batch-1/INDEX.md`,
  `…batch-2/INDEX.md`, `…batch-3/INDEX.md`, `…batch-4/INDEX.md`. Leurs rapports vidéo sont encore cités
  par des documents vivants (`AMK-DESIGN-SKILLS.md`, `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md`,
  `content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md`) : archiver l'index aurait coupé l'entrée de ces
  dossiers, pas fermé une porte inutile ;
- `research/youtube-lessons/2026-10-22-brand-strategy/SYNTHESE.md` — ce n'est pas une récolte mais **déjà
  une synthèse** (positionnement, Warby Parker, vente optique), et elle alimente un document client
  vivant : `clients/dm-optic/brand/BRAND-STRATEGY-2026-10-22.md`. Elle reste, et ce document la cite.

---

**Archivé le 24/10/2026** : les 29 rapports bruts et leurs 9 index, dans
`archive/2026-10/youtube-lessons/`. Rien n'est perdu : `git log --follow` les retrouve, et ce document
dit où mène chacune de leurs conclusions.
