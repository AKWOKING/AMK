# hyperframes (heygen-com/hyperframes) — le moteur vidéo d'AMK, auditée sur preuves

**Problème nommé (audit demandé par King le 20/10) :** rendre des vidéos d'annonce
(livrables clients) depuis du HTML réel, en local, sans frais par rendu.
**Licence : Apache-2.0** (vérifiée deux fois : dépôt amont au 19/10, champ `license` du paquet
npm installé au 20/10). **Version installée : CLI 0.8.177** (`--version` exécuté).

## Verdict de l'audit (20/10)

- **Flux de travail : OUI — c'est déjà notre moteur.** Hyperframes est le maillon de rendu de la
  chaîne brag (§1f②) : `check` (lint + layout + contraste WCAG AA) → `snapshot` (relue à l'œil)
  → `render`. Preuves d'usage réel : **19/10** vidéo de démonstration de bout en bout ; **20/10**
  le brag de livraison DM Optique — check 0 erreur / 0 warning, contraste **10/10 WCAG AA**,
  3 débordements volontaires déclarés `data-layout-allow-overflow`, rendu 20 s en ~58 s
  (`screenshot` mode, GPU logiciel — lenteur attendue en sandbox), portique mouvement OK après
  un blocage corrigé.
- **Vendable comme service : OUI.** Apache-2.0 = usage commercial et dérivés autorisés ; rendu
  **local = 0 FCFA par vidéo** (l'hébergé du même éditeur et letsbrag.app facturent ~19 $/vidéo).
  L'offre « vidéo d'annonce de livraison » tient debout : captures réelles du site livré,
  identité du client, musique générée/licenciée, 15–25 s vertical pour statut WhatsApp.
  **Le tarif est une décision de King** — jamais fixé par l'orchestrateur.
- **Conditions qui restent :** que du vrai à l'écran (captures réelles, pas de fausses
  statistiques) ; musique = nappe générée ou licenciée (piste embarquée ende.app interdite) ;
  rien d'envoyé sans validation de King (règle 3).

## Installation — UNE SEULE VOIE (ne jamais en empiler deux)

Hyperframes est installé **par `bash tools/brag/install.sh`** (la chaîne brag installe le CLI
npm, le wrapper Chrome et les skills) : même runtime, même pin, mêmes parades sandbox.
**Ne pas créer un second installeur sur la même cible** (leçon ECC). Sur la machine de King,
le même installeur télécharge Chrome lui-même.

```bash
bash tools/brag/install.sh            # installe la chaîne complète, Hyperframes inclus
export PATH="$HOME/.local/bin:$PATH"                                # ffmpeg (imageio) + ffprobe (npm)
export HYPERFRAMES_BROWSER_PATH=/tmp/amk-brag/chrome-wrapper.sh     # Chrome @sparticuz en sandbox
export HYPERFRAMES_SKIP_SKILLS=1
/tmp/amk-brag/node_modules/.bin/hyperframes check | snapshot | render
```

Détail des parades sandbox (Chrome bloqué, GSAP local, ffmpeg/ffprobe) : `tools/brag/README.md`.

## Règle de livraison vidéo (amendée par ruling King du 20/10)

Par défaut, les mp4 restent **hors Git** (régénérables) et les artefacts légers (plan, share-copy,
poster) entrent dans `clients/<client>/brag/`. **Exception posée par King le 20/10 :** le
`brag.mp4` de DM Optique est **versionné dans le dépôt** (`clients/dm-optic/brag/brag.mp4`,
`git add -f` — la règle globale `*.mp4` du `.gitignore` reste en place pour tout le reste).
Tout futur mp4 versionné = décision explicite de King, fichier par fichier.
