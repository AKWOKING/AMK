# IDEAS — les lots de recherche d'idées

Ici vivent les **lots d'idées**, un fichier par quinzaine : `SHORTLIST-YYYY-MM-DD.md` — et la
**grille 331** (`GRID-331-2026-10-25.md` : 3 sujets × 3 formats, plus la dixième qui attend la donnée).
La doctrine est `knowledge/IDEA-PIPES-2026-10-25.md` ; la porte est **`tools/qa/audit_ideas.py`**.

```bash
python3 tools/qa/audit_ideas.py content/ideas/SHORTLIST-2026-10-25.md
python3 tools/qa/audit_hook.py --grid content/ideas/GRID-331-2026-10-25.md
```

## Le format, et pourquoi il est aussi contraint

Un lot est lu par une machine, donc il n'est pas de la prose libre. Une idée = un bloc `## IDEA-xx` et
huit lignes :

```
## IDEA-02 · Les trois niveaux de fiche Google
- pipe: 3
- topic: la fiche Google d'un opticien, en trois niveaux
- seed: Trois niveaux de fiche : celle qui fait appeler, celle qu'on survole, celle qui fait passer
- substance: trois fiches réelles de Douala comparées champ par champ
- cible: opticien de Douala, 35–54 ans, fiche existante
- preuve: format emprunté à la source du 25/10 (« the 3 levels of toothpaste »), aucune métrique à nous
- briques_constantes: ouverture, arc 6 beats, hook, mise en page, mascotte, voix, CTA, durée ≤ 25 s
- briques_changees: seed, substance
```

`outliers_validés: N` en tête de fichier : ce que la watchlist a **réellement** produit. Il reste à `0`
tant que personne n'a regardé les plateformes — c'est ce qui empêche un lot de se croire validé.

**Ce que la porte refuse** : un tuyau hors 1–6 · un champ manquant · `[NEEDS DATA]` dans la preuve · un
seed de moins de cinq mots ou identique au topic · une cible de moins de quatre mots · un tuyau 1 ou 2
sans **chiffre de performance** (une date et un timecode ne comptent pas) · plus de trois briques changées.

**Ce qu'elle avertit seulement** : tuyau 3 sans métrique · tuyau 5 (non-outlier) · original sans aucun
outlier sur la chaîne · peu de constantes · un lot où **aucune** idée n'a de donnée.

## Les deux règles qui valent plus que le format

1. **Aucun chiffre inventé.** Une preuve est un lien daté, une capture, ou le mot « aucune donnée ». Un
   lot qui n'a rien trouvé se dit vide — c'est le cas du lot du 25/10, et c'est écrit dans son en-tête.
2. **Aucune pièce ne se produit sans ligne de lot.** L'ordre est : idée → rôle (`audit_trust.py`) →
   forme (`audit_reel.py`). Trois portes, dans cet ordre.
