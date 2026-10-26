# BRAINSTORM — « LE SCRIPT » : ce que le dépôt sait, ce qu'il ne vérifie pas, et ce qu'on fait ce soir

```
Étape 0   graphe rejoué le 26/10 à 00:03 → 12 527 nœuds · 15 875 arêtes (ops/REPO-MAP.md)
          ask « roast du script EP01, réécriture, storytelling et copywriting » → 56 documents, 6 retenus
          ask « roast me critique script storytelling copywriting » → 51 documents
Puis      PRE-FLIGHT.md lu · §0b sans objet · §0c knowledge/ (HOOKS, CONTENT-CREATION, HOUSE §8, VIDEOS)
Skill     tools/superpowers/skills/brainstorming/SKILL.md (tracé dans ~/.amk-provisioned/usage.log)
Roast     knowledge/ROAST-2026-10-26-SCRIPT-EP01.md — verdict C (8,1 / 10), trois conditions écrites
But       choisir ce qu'on construit AVANT de le construire — et le dire en une page
```

## 1 · Ce que le graphe dit qu'on sait déjà écrire (et qui n'est pas utilisé)

Le dépôt contient **quatre couches d'écriture**, et elles ne se parlent pas :

| Couche | Ce qu'elle dit | Où | Utilisée par |
|---|---|---|---|
| **Les 5 temps** | cas → miroir → réel → preuve → sortie, avec un **interdit** par temps | `CONTENT-CREATION` §3 | à la main, jamais vérifiée |
| **Le squelette Kallaway** | hook → lock-in → corps → **rehook** → corps → CTA aligné | `CONTENT-CREATION` §3 bis | jamais vérifiée |
| **La copie** | PAS/PASTOR, 5 composants de l'offre, 0,3 s par mot, falaise à 0:02 | `HOUSE-KNOWLEDGE-BASE` §8 | en vente, pas en vidéo |
| **L'accroche** | 6 mots de puissance, échelle 1–5, grille 331 | `HOOKS-2026-10-25.md` | **porte** : `audit_hook` |

**Le constat qui compte** : l'accroche a une porte, la forme a une porte, le rôle a une porte, l'idée a
une porte. **L'histoire n'en a aucune.** Les trois documents qui décrivent la structure d'un script ne
sont vérifiés par **rien** — et c'est exactement pourquoi la v4 peut passer quatre portes vertes avec un
défaut que trois sièges du conseil voient en dix secondes.

> **Règle maison : une règle sans porte = un trou.** Le trou du soir, c'est la structure narrative.

## 2 · Ce que le graphe dit qu'on n'a pas

1. **Aucune porte de récit** : lock-in, rehook, preuve dite, CTA aligné — tout est écrit, rien n'est
   refusé. Un script sans rehook passe.
2. **Aucune donnée** : la grille a neuf cases et zéro chiffre. Le conseil l'a dit sans détour (Buffett) :
   la v5 est un pari, pas une mesure.
3. **La preuve visuelle n'est jamais sonore** : on a la capture (12 avis) et on ne la prononce pas. Le
   format actuel traite l'image et la voix comme deux canaux indépendants, alors que la doctrine Kallaway
   les ordonne (**visuel > écrit > parlé**).
4. **Le cadeau arrive trop tard** : « dix minutes, c'est gratuit » est le meilleur argument de la pièce
   et il tombe à 21 s sur 24,5.

## 3 · Trois approches (trois paris différents)

### A · Réécrire EP01 à la main, une fois
Une pièce, un soir, à l'oreille.
- **Coût** : ~1 h. **Ce que ça prouve** : que le texte peut être meilleur.
- **Le risque** : on refait exactement ce qu'on a fait quatre fois. La cinquième version sera jugée par
  la même personne qui a écrit les quatre précédentes — et **sans règle**, elle ne sait pas ce qui lui
  manquait. C'est le scénario que Buffett a voté contre.

### B · Construire la porte qui manque, puis réécrire sous elle *(recommandée)*
Écrire `tools/qa/audit_story.py` : la **porte du récit**. Elle lit le module de la pièce et refuse :
- `pas-de-cas` — pas de situation vécue dans le premier beat ;
- `pas-de-lockin` — rien n'annonce pourquoi rester après le hook ;
- `pas-de-rehook` — aucun beat de relance entre les deux corps ;
- `preuve-muette` — une preuve existe à l'écran mais aucun chiffre/fait n'est **prononcé** ;
- `cta-non-aligne` — le CTA ne reprend pas le mot de la promesse ;
- `deux-cta`, `urgence`, `liste-sans-axe` (trois arguments empilés dans un même beat).
Puis réécrire EP01 v5 **sous cette porte**, et s'en servir pour les huit cases restantes de la grille.

- **Coût** : ~1 h 30 (porte + banc + réécriture + rendu).
- **Ce que ça prouve** : que la leçon de la v4 devient une règle exécutable, pas une anecdote.
- **Le risque** : une porte trop stricte **tue l'écriture**. Garde-fou : elle **refuse** six choses
  mesurables et **avertit** sur le reste. Aucun jugement de goût.

### C · Produire les huit cases d'abord, juger à l'audience
Remplir la grille, publier, laisser les vues trancher.
- **Coût** : 8 jours. **Ce que ça prouve** : la cadence.
- **Le risque, déjà mesuré** : **zéro donnée** au 26/10, aucune fenêtre d'observation. On produirait huit
  pièces avec le même défaut de structure, et on n'aurait toujours rien pour trancher.

**Recommandation : B, puis A sous B.** On construit la porte, on réécrit EP01 v5 dessous ce soir, et la
porte sert les huit autres cases. C attend la donnée, qui n'existe pas encore.

## 4 · Ce que je ne peux pas décider seul

Une seule question, et elle change la livraison de mardi :

> **Si la v5 est bonne à l'oreille mais que la v4 reste meilleure pour toi, laquelle part mardi ?**

Le conseil a tranché : **le filet reste** (v4 conservée) et **c'est ton oreille qui départage**, pas la
porte. Si tu ne veux pas arbitrer, la règle par défaut est : **v5 si elle passe les quatre portes et
qu'aucun beat n'est plus faible que dans la v4 ; sinon v4.**

## 5 · Propositions

| # | Proposition | Coût | Ce qu'elle règle |
|---|---|---|---|
| 1 | **`tools/qa/audit_story.py`** + banc — la porte du récit (5 temps, lock-in, rehook, preuve dite, CTA aligné) | ~45 min | la règle sans porte |
| 2 | **EP01 v5** réécrite sous la porte : scène en ouverture, chiffre prononcé, rehook au milieu, cadeau avant le CTA | ~30 min + rendu | le défaut que le roast a trouvé |
| 3 | **Chaîne à cinq portes** : idée → accroche → **récit** → rôle → forme | 10 min de docs | l'ordre qui manquait |
| 4 | **La v4 reste sur le disque** et sur `main` | 0 | la condition de Buffett |
| 5 | Publier **mardi**, quoi qu'il arrive | 0 | la seule façon d'avoir une donnée un jour |

## 6 · Audit de ce document

- **Mesuré** : les 12 527 nœuds, les 56 documents retrouvés par `ask`, les six défauts du roast (chacun
  adossé à une règle nommée), les durées de la v4 (timing.json).
- **Jugement** : le classement B > A > C est une opinion argumentée, **pas une mesure**. Elle repose sur
  une hypothèse non vérifiée : qu'une porte de récit produise de meilleurs scripts. Ce soir, elle en
  produira **un** — et c'est tout ce qu'on pourra dire.
- **Absent** : aucune vue, aucun taux de rétention, aucune donnée de publication. Tout ce qui concerne
  « est-ce que ça marche » reste ouvert, et le restera jusqu'à mardi.
