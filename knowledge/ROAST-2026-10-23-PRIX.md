# Roast Room — séance du 23/10/2026 · « faut-il afficher un prix sur le site AMK ? »

> **Comment cette séance a été tenue, dit franchement.** Le protocole est celui du skill `roast-room`
> (nateherkai/roast-room, épinglé `e40f406`, **licence MIT** vérifiée ce jour) : `SKILL.md`,
> `references/round-prompts.md`, `references/scoring.md`, et les fiches `_hot.md` des sièges lues dans
> `~/.roast-room/.claude/skills/roast-room/brains/`. **Ce n'est pas le rendu de l'application** : elle
> demande Claude Code et un accès modèle (`api.anthropic.com` bloqué dans le bac). Les sièges ont donc
> été tenus par l'agent, en suivant les mêmes fiches et la même arithmétique — c'est un conseil
> conforme au protocole, pas une session sub-agent.

## Le brief

AMK vend des sites à des écoles privées et des cliniques au Cameroun. La page d'accueil affiche
aujourd'hui « Sur devis, selon votre besoin ». La grille d'Arthur (`knowledge/LANDING-FUNNEL-2026-10-23.md`)
dit que le prix est un **filtre**, et que le visiteur suppose toujours le pire (« ça doit coûter cinq
chiffres »). Contrainte : nous n'avons qu'un client réel et aucune donnée de conversion.

**Options** — A. Garder « sur devis » seul. B. Publier **un point d'entrée** (« à partir de … FCFA »)
avec ce qu'il inclut. C. Publier **trois formules** à prix fixes.

**Sièges et poids** — Hormozi (offres et prix) ×3 · Graham (produit et demande) ×2 · Buffett (argent et
risque) ×2. Total 7.

## Tour 1 — position d'ouverture

**HORMOZI — Conditional yes (B)** · scores A 2 / B 8 / C 6
« Le devis est un mur. Tu demandes au prospect de travailler pour découvrir le prix. Une fourchette
basse avec une pile de livrables nommés fait le tri à ta place. Trois formules fixes, pas encore : sans
preuve client, un prix fixe est une affirmation non étayée. Je ne remise jamais, je change les termes —
donc l'ancre doit être un **plancher** que tu livres toujours. »

**GRAHAM — Yes (B)** · scores A 4 / B 7 / C 6
« Publier un prix, c'est lancer plus vite. Chaque conversation qui n'arrive pas est une chose que tu
n'apprends pas. Mais commence étroit : une ancre, une promesse, un public. Trois formules avant d'avoir
vendu dix fois, c'est de l'optimisation prématurée. »

**BUFFETT — Conditional yes (B)** · scores A 5 / B 7 / C 4
« Le devis protège ta marge : c'est son seul mérite. Une ancre publique la plafonne. Si tu l'écris,
écris un prix que tu peux tenir **même dans le pire des cas** : un site complexe, un client qui change
d'avis trois fois. Trois formules fixes sur une capacité que tu n'as pas encore mesurée, c'est du risqué
pour un gain d'affichage. »

## Tour 2 — le débat

- **Hormozi attaque Buffett** : « Ta marge ne meurt pas d'une ancre, elle meurt d'un périmètre flou.
  Une ancre + une page "ce qui fait monter le prix" protège les deux. »
- **Buffett concède** : « Alors la liste du périmètre n'est pas une option, c'est la condition. »
- **Graham attaque Hormozi** : « Trois formules, c'est déjà vouloir paraître gros. Une seule ancre dit la
  vérité d'aujourd'hui et se change en une heure. »
- **Hormozi concède** : « Une ancre suffit pour ce trimestre ; les trois formules attendent dix ventes. »
- **Le siège le plus à risque (Buffett) est invité à défendre A à pleine force** : « Si tu n'as pas
  encore livré deux fois le même type de site, publier un prix est une prédiction, pas une offre. »
  Graham répond : « Une prédiction qu'on peut défaire en une heure n'est pas un pari, c'est un test. »

## Tour 3 — vote et scores finaux

| Siège | Poids | A « sur devis » | B « ancre » | C « trois formules » |
|---|---|---|---|---|
| Hormozi | 3 | 2 | **8** | 5 |
| Graham | 2 | 4 | **7** | 6 |
| Buffett | 2 | 5 | **7** | 4 |

**Arithmétique** (moyenne pondérée, `scoring.md`) :

- A : (3×2 + 2×4 + 2×5) / 7 = 24 / 7 = **3,4**
- B : (3×8 + 2×7 + 2×7) / 7 = 52 / 7 = **7,4**
- C : (3×5 + 2×6 + 2×4) / 7 = 43 / 7 = **6,1**

**Écart** (spread) sur B : 8 − 7 = 1. **Confiance** : (7 + 7 + 7)/3 × 2 ≈ 14 → ramenée à **10/10** par
le protocole (plafond), à lire comme « le conseil est d'accord, ce qui ne veut pas dire qu'il a raison ».

**Verdict : GO WITH CONDITIONS** — option **B**, score **7,4** (bande 6,0–7,4).
Aucun siège en `RUIN RISK: likely` : le plafond « risque de ruine » ne s'applique pas. Aucune porte à
sens unique : un prix affiché se retire en une heure, le plafond « one-way door » ne s'applique pas non
plus.

## La résolution, telle que le conseil l'endosse

1. Une seule ligne d'ancre : **« à partir de … FCFA »**, un montant que nous tenons **même** sur le
   projet le plus lourd déjà livré (condition Buffett).
2. **La pile de livrables nommés** sous l'ancre : pages, bilingue FR/EN, WhatsApp prérempli, mise en
   ligne (condition Hormozi).
3. **« Ce qui fait monter le prix »** : trois lignes maximum (nombre de pages, photos à produire,
   délais). C'est la protection du périmètre, et la réponse honnête au « je ne sais pas ce que je paie ».
4. **Pas de remise** : si le budget est plus bas, on **change les termes** (périmètre), jamais l'ancre.
5. **Trois formules : après dix ventes**, pas avant. La question revient au conseil à ce moment-là.

## Dissent, à conserver

**Buffett** : « Tu publies un prix sans avoir mesuré ton coût réel de livraison sur trois projets
semblables. L'ancre est un engagement ; les conditions ci-dessus la rendent tenable, mais si le
quatrième projet dépasse de 40 %, c'est toi qui paies la différence. »

## Prochaine étape (une seule)

Écrire la ligne d'ancre et la pile de livrables dans la section `#pricing` de `site/index.html`, avec la
liste « ce qui fait monter le prix » — puis repasser `bash tools/ops/gate-amk.sh` (le P3 F6 doit tomber).
