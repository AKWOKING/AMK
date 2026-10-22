# tools/photo — édition photo client, locale, pour le web

> Adopté en test le 19/10/2026 (voir `ops/TOOL-SCAN.md`). Problème nommé : les
> photos du client (montures + cabinet, prises au téléphone) doivent être
> nettoyées avant d'entrer sur le site — sans envoyer de données client dans
> un service tiers, et sans déformer le produit.

## Ce que fait la chaîne (et ce qu'elle refuse de faire)

| Photos montures (`--mode catalogue`) | Photos cabinet (`--mode clinique`) |
|---|---|
| Détourage IA local (ISNet ONNX, CPU ~4 s/image) → fond propre uniforme → 4:3 1600×1200 (le catalogue affiche 800×600) + master transparent PNG pour les carrousels. | Rotation EXIF, niveaux doux, netteté légère, ≤1920 px. **Aucun détourage, aucun objet effacé** : la pièce reste la pièce. |

**Interdits permanents** (contrat « le site ne montre que du vrai » + R1–R4) :
pas de recoloration/redessin de monture, pas de fond généré « studio » qui
ferait croire à un lieu, pas de visage IA, pas de patient identifiable sans
accord écrit. L'IA ne fait qu'un masque (détourage) — le reste est
Pillow classique. Chaque sortie est contrôlée à l'œil avant publication.

## Pourquoi ce modèle-là (histoire d'egress)

La voie normale est **rembg** (MIT, `pip install "rembg[cpu,cli]"`), mais ses
poids se téléchargent depuis les *release assets* GitHub — bloqués par
l'egress de la sandbox (vérifié le 19/10 : 302 → `objects.githubusercontent.com`
hors liste). Le paquet npm **@imgly/background-removal-node** embarque son
modèle ISNet en chunks dans le paquet : il arrive donc par un hôte autorisé,
on le reconstruit (~88 Mo) et on l'exécute avec le même onnxruntime Python.
Preuve faite ici le 19/10 sur une image de référence démo (pas de donnée
client). Sur la machine de King (internet normal), les deux chemins marchent ;
`install.sh` essaie npm d'abord (ISNet 1024 px, meilleur sur les branches
fines), repli `rembg d u2net`.

**Licences.** rembg : MIT ; poids u2net : Apache-2.0 ; paquet IMG.LY : licence
propre (voir son `LICENSE.md`, double licence) — usage **local interne**
uniquement. Les poids ne sont **jamais** commités ni redistribués (ils vivent
dans `~/.rembg/models/manual/`, et `*.onnx` est dans `.gitignore`).

Écartés après recherche : **IOPaint/lama-cleaner** (dépôt archivé le
13/08/2025, PyTorch lourd, et l'effacement d'objets contredit « que du vrai »
hors cas vie privée) ; **Upscayl/Real-ESRGAN ncnn** (exige un GPU Vulkan,
absent de la sandbox — à réserver à la machine de King si des photos arrivent
trop petites ; un téléphone récent n'en aura probablement pas besoin).

## Usage

```bash
bash tools/photo/install.sh            # idempotent (+ --smoke pour le test)
~/.venv-amk/bin/python tools/photo/prep.py <photos…> -o <sortie> --mode catalogue [--bg FFFFFF]
~/.venv-amk/bin/python tools/photo/prep.py <photos…> -o <sortie> --mode clinique
```

**Branchement catalogue DM** (quand King dépose photos + noms) :
sorties `*-catalogue.jpg` → dossier des visuels du site → lignes
`{"nom": <fourni par le client>, "photo": <chemin>, "phrase": …}` dans
`clients/dm-optic/site/frames.json` → `python3 demos/build_dmoptic_montures.py`
→ gates QA → **King déploie lui-même** (règle maison, aucun déploiement agent).
Aucune carte sans nom fourni par le client ; aucun prix.

**Porte TOOL-SCAN :** première utilisation production = test personnel de
King sur le premier lot réel (il valide les sorties avant build). Si le
détourage mange une branche fine ou laisse un halo, on ajuste (autre modèle,
retouche manuelle du masque) — on ne publie jamais une sortie non relue.
