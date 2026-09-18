# Maquette instantanée AMK — mode d'emploi

**Décision de King (18 Sep 2026) :** on ne construit plus un site complet avant le « oui »
du prospect. Avant le « oui » → une **maquette légère mais personnalisée**, qui donne envie
de demander l'aperçu. Le site complet n'est construit qu'après un accord explicite.

Coût : **~2 minutes par prospect** (contre plusieurs heures pour un site complet).
Aucun réseau nécessaire : le modèle est dans le dépôt.

---

## 1 · Prérequis (une fois par session — `/tmp` est effacé à chaque redémarrage)

```bash
bash tools/video/install.sh
export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib
export FONTCONFIG_PATH=/tmp/amk-video/fonts
```

## 2 · Commande type

```bash
python3 tools/outreach/mockup.py \
  --vertical clinique \
  --name "Cabinet Dentaire YAKS" \
  --specialty "Cabinet dentaire · Logbessou, Douala" \
  --color "#0E7A5C" \
  --whatsapp 672702078 \
  --h1 "Des soins dentaires|sans surprise" \
  --sub "Urgences, détartrage et blanchiment. Rendez-vous confirmé sur WhatsApp." \
  --svc "Urgences,Détartrage,Blanchiment" \
  --out clients/_mockups/yaks.jpg
```

`--vertical clinique|college` choisit seulement la **photo par défaut** et les libellés
d'action neutres. Tout le reste vient du prospect.

Sortie : image **1080×1620** (~225 Ko) — la même page montrée sur **ordinateur portable
et sur téléphone**. Choisir le format avec `--devices both` (défaut), `phone` ou `laptop`
(dans ce cas la sortie est en 1080×1350).

| `--devices` | Sortie | Usage |
|---|---|---|
| `both` (défaut) | 1080×1620 | l'envoi habituel : on voit la page sur ordinateur **et** sur téléphone |
| `phone` | 1080×1350 | quand on ne veut montrer que le téléphone |
| `laptop` | 1080×1350 | quand on ne veut montrer que l'ordinateur |

Le modèle `site/mockup-hero.html` est **responsive** : la même page est capturée en
390×844 (téléphone) et en 1280×800 (ordinateur). Les deux rendus sont donc réellement
la même page, à deux largeurs — la maquette ne triche pas.

## 3 · Où trouver les mots à mettre dans la maquette

Les jetons `--h1 --sub --svc` doivent être les **mots du prospect**, pas les nôtres.
Sources, dans cet ordre :

1. sa page Facebook / sa bio Instagram (souvent la seule vitrine) ;
2. sa fiche Google Business (horaires, services cités) ;
3. son numéro WhatsApp, statut et catalogue ;
4. les photos de sa devanture (nom exact, quartier, repères).

## 4 · Loi d'exactitude — ce qui n'entre JAMAIS dans une maquette

- aucun **prix**, aucune **durée d'attente**, aucun **chiffre** que le prospect n'a pas publié ;
- aucun **témoignage**, aucun **nombre de patients / d'élèves** ;
- aucune promesse de résultat, aucun rang, aucun classement ;
- jamais « le site de X » : toujours « une maquette, pas encore en ligne ».

La maquette porte deux étiquettes d'honnêteté : le bandeau interne
« MAQUETTE AMK · PAS ENCORE EN LIGNE » et la pastille externe
« MAQUETTE PERSONNALISÉE · PAS LE SITE FINAL ».

## 5 · Options

| Option | Rôle |
|---|---|
| `--whatsapp` | injecte le numéro du prospect dans la barre du bas (sa page, son numéro) |
| `--photo` | remplace la photo par défaut (chemin local) |
| `--cta1/--cta2` | libellés des deux boutons |
| `--badge` | pastille posée sur la photo |
| `--bar` / `--bar-sub` | barre d'action du bas |
| `--kicker` | sur-titre de la carte (« Aperçu gratuit · 1 page d'accueil ») |
| `--line` | phrase de pied de carte |
| `--devices` | `both` (défaut) · `phone` · `laptop` |
| `--height` | hauteur de la carte (1620 pour deux appareils, 1350 pour un seul) |

## 6 · Fichiers

| Fichier | Rôle |
|---|---|
| `site/mockup-hero.html` | **modèle unique à jetons** — tous les mots sont des `{{TOKENS}}` |
| `site/assets/mockup-clinique.jpg` | photo par défaut santé |
| `site/assets/mockup-college.jpg` | photo par défaut école |
| `tools/outreach/mockup.py` | remplissage + capture + composition |
| `clients/_mockups/` | sorties (exemples : `EXEMPLE-dentaire.jpg`, `EXEMPLE-college.jpg`) |

## 7 · Étapes suivantes du mode d'emploi

1. Rechercher le prospect (3 portes, §8b).
2. Remplir la maquette avec ses mots.
3. Envoyer : image d'abord, texte en légende — un seul message.
4. Si « oui » → **c'est là seulement** qu'on construit le site complet.
