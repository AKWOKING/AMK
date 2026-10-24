# design-md — codifier un système de design depuis une page réelle

> Amont : `bergside/design-md-chrome` (MIT, pin **`8e07614`**), installé le 23/10/2026 dans
> `tools/design-md/`. Le dépôt n'en garde rien : la source vit dans `/tmp/amk-designmd/src`.

## 1 · Pourquoi on l'a pris, et ce qu'on n'a pas pris

L'amont est une **extension Chrome** : on ouvre un onglet, on clique, elle lit les styles calculés
(typographie, couleurs, espacements, rayons, ombres, durées) et écrit un `DESIGN.md`. C'est exactement
ce qui manquait : une façon de **codifier** un système plutôt que de le décrire de mémoire.

On n'a pas installé l'extension — on a réutilisé son **extracteur** (`content-script.js`) et ses
**générateurs** (`lib/`), sans modifier une ligne d'amont. `extract.mjs` injecte le script dans le
Chromium embarqué, lui fournit un `chrome.runtime` factice, récupère la charge utile par le même
canal de message que l'extension, puis appelle `normalize` → `generateDesignMarkdown` →
`validateMarkdownOutput`.

## 2 · Usage

```bash
bash tools/video/install.sh                    # Chromium (une fois par session)
bash tools/design-md/install.sh                # source amont épinglée
python3 tools/design-md/extract.py hosting/previews/dmoptic --name "DM OPTIQUE SARL"
#  → /tmp/designmd/DESIGN.md + SKILL.md, les deux validés (14 contrôles chacun)
```

Un dossier, un fichier `.html`, ou une URL. Un dossier est servi en HTTP local (les pages du dépôt
utilisent des chemins absolus : en `file://` tout casse).

## 3 · Ce que l'extraction du site DM a donné (23/10)

Les jetons réels, lus dans le navigateur — pas déduits du CSS à la main :

| Famille | Valeurs extraites |
|---|---|
| Police | `IBM Plex Sans`, base **17 px**, graisse 400, interligne 27,5 px |
| Échelle | 13 · 14 · 15 · 16 · 17 · 17,6 · 18,9 px |
| Couleurs | texte `#0c1524` / `#43506a`, surface `#101b2e`, accent `#0b7a3e` |
| Rayons | 14 px · 20 px · 999 px (pastille) |
| Ombres | `rgba(12,21,36,.1) 0 14px 34px` |
| Mouvement | 160 · 180 · 280 · 380 ms |

**Ce qui est faux et qu'il faut corriger à la main :** le générateur devine l'audience et la surface
(« e-commerce storefront »). Pour un cabinet d'optique, c'est à réécrire. Le document est un
**brouillon de système**, pas une vérité : on garde les jetons, on réécrit la prose.

## 4 · Où ça s'arrête

- Il lit ce que le navigateur calcule : une page vide (chargement bloqué, JS cassé) donne un système vide.
- Il ne juge pas : un contraste faible est extrait fidèlement. Le jugement reste à `tools/qa/shot.py`
  (contraste AA) et à `audit_delivery.py`.
- Il ne remplace pas `pro-design` : celui-ci **construit**, celui-là **relève**.
