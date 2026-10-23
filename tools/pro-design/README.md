# pro-design — le skill de construction de pages (installé le 23/10/2026)

```
Source     tools/pro-design/SKILL.md — la source est DANS le dépôt (fournie par King, 23/10)
Install    bash tools/pro-design/install.sh  → ~/.agents/skills/pro-design/ + ~/.claude/skills/pro-design/
Nature     markdown pur : aucun binaire, aucun réseau, aucun sudo
Portée     construire, redessiner ou relire un site, une landing page, une UI
```

## Ce qu'il apporte, en quatre temps

| # | Étape | Ce qu'elle impose | Ce que ça remplace dans notre façon de faire |
|---|---|---|---|
| 1 | **Marque d'abord** | lire les fichiers de marque, sinon écrire une fiche (4–6 couleurs nommées, deux typographies avec un rôle, une voix, un élément signature) et la faire confirmer ; **tout en variables CSS** | nos allers-retours sur la palette arrivaient souvent après la première maquette |
| 2 | **Bibliothèque de motifs** | choisir un motif **par section** et dire pourquoi ; n'utiliser des étapes numérotées que si c'est une vraie séquence ; étudier 2–3 sites du même métier ; **refuser six tics visuels nommés** | la « belle page » sans argument devient traçable : chaque section a sa raison |
| 3 | **Mouvement** | **un** moment orchestré ; le reste répond à une action ; 150–250 ms pour l'interface, 600–900 ms pour la séquence ; `prefers-reduced-motion` ; jamais de contenu caché qui attend une animation | c'est exactement la règle maison `AMK-DESIGN-SKILLS` §9 + `design/MOTION.md`, ici en version courte et opposable |
| 4 | **Boucle de vérification** | construire **tout**, puis ouvrir dans un vrai navigateur, captures **1440** et **390**, contrôler débordement / texte coupé / contraste / images cassées / console / focus clavier / héro dans le premier écran, **corriger en un seul lot**, **deux tours maximum, puis stop** | c'est notre §1b, mais avec une limite explicite : **on arrête de polir** |

**Et la phrase qui compte le plus, à la fin du skill :** *« Maximum two rounds. Do not keep polishing. »*
Un audit qui tourne en boucle coûte plus qu'il ne rapporte — c'est la même règle que `§3 sexies` du
déploiement Cloudflare (« ne jamais retry un ancien build ») appliquée au design.

## Hiérarchie en cas de conflit — les lois maison gagnent

| Le skill dit | La maison dit | Qui gagne |
|---|---|---|
| écrire une fiche de marque si aucune n'existe | `clients/<client>/brand/` contient déjà une direction figée (DM : `DIRECTION-MARQUE-v2-2026-10-22.md`, identité verrouillée) | **la maison** : on ne réécrit pas une marque validée par le client |
| étudier des sites du même métier | protocole d'unicité `AMK-DESIGN-SKILLS` §2 + `clients/_uniqueness-registry.md` (on ne copie pas, on s'en écarte volontairement) | **la maison** |
| ses six tics refusés | `AMK-DESIGN-SKILLS` §3 (anti-slop) en liste plus longue | **la maison**, le skill s'y ajoute |
| captures 1440 / 390 | portiques `tools/qa/audit_*.py` + `audit_delivery.py --strict` + `gate-amk.sh` | **les portiques** : ils bloquent, le skill ne fait que constater |
| « deux tours maximum » | aucune règle maison ne dit le contraire | **le skill** |

## Comment il se branche sur ce qu'on a déjà

```
pro-design §1  →  clients/<client>/brand/  +  design/STYLE-TOKENS.md
pro-design §2  →  AMK-DESIGN-SKILLS.md (§7 mise en page, §14 menu de styles, §17 motifs)
pro-design §3  →  design/MOTION.md + tools/design-motion-principles (le skill détaillé, pour l'audit)
pro-design §4  →  tools/qa/ (les portiques) + une capture réelle
```

**Le seul endroit où il faut être honnête :** l'étape 4 demande « Playwright ou Claude in Chrome ».
Dans la sandbox, **une URL live est inaccessible au Chromium** (l'egress est fermé — constaté le 20/10) ;
ce qui marche, c'est **un fichier local** servi par un petit serveur, avec le Chromium de la chaîne vidéo :

```bash
bash tools/video/install.sh
CHROME_PATH=/tmp/amk-video/chrome-wrapper.sh   # recette : tools/taste-skill/README.md
```

Si la jonction casse, le rapport **le dit** et seuls `lint.mjs` + les portiques §1b font foi — jamais une
capture inventée.

## Vérifier / réinstaller

```bash
bash tools/pro-design/install.sh     # idempotent, hors réseau
grep -c '^## ' ~/.agents/skills/pro-design/SKILL.md   # attendu : 4 sections + quality floor + hand-off
```

L'environnement ne survit pas entre sessions : **le script se relance**, et c'est pour ça que la source est
dans le dépôt et pas seulement dans `~/.agents/`.

## Décision d'usage (ruling proposé, à confirmer par King)

**pro-design devient la porte d'entrée de toute page neuve ; taste-skill reste l'outil de tirage de
direction quand le style n'est pas encore fixé.** Les deux ne se lancent pas en même temps sur la même
page : pro-design pour **structurer et vérifier**, taste-skill pour **chercher une direction** quand la
marque n'en a pas. Un seul des deux par page, et on le dit dans l'en-tête pré-vol.
