# Où sont les vidéos — état au 22/10/2026

```
Question de King : « je ne trouve pas ugc-03.mp4 sur github » · « where is post 1 ?? »
Réponse : ils y sont maintenant, dans ce dossier. Chemins exacts au §1.
```

---

## 1 · Les fichiers, droit devant

| Post | Fichier vidéo | Couverture | Sous-titres | Durée · poids |
|---|---|---|---|---|
| **1 — 20/20/20** | **`tiktok-01-v2.mp4`** | `tiktok-01-v2-cover.jpg` | `tiktok-01-v2.fr.srt` | 23,00 s · 4,8 Mo |
| **2 — UGC « on montre avant de vendre »** | **`ugc-03.mp4`** | `ugc-03-cover.jpg` | — (sous-titres incrustés) | 22,30 s · 6,8 Mo |

Chemin complet depuis la racine du dépôt :

```
clients/dm-optic/content/month1/w1/tiktok-01-v2.mp4
clients/dm-optic/content/month1/w1/ugc-03.mp4
```

Les deux passent le portique (`tools/qa/audit_video_motion.py`) : **0 fenêtre figée**.
Les voix séparées (`assets/voix-v2.mp3`, `assets/ugc-03-voix.mp3`) restent hors dépôt — elles se
régénèrent en une commande (§3).

## 2 · Pourquoi ça n'y était pas, et ce qui a changé

Le dépôt excluait **tous** les `.mp4` et `.mp3` par `.gitignore` (règle du 23/09 : « le repo n'est pas un
disque dur »). Conséquence que je n'avais pas rendue assez visible : un fichier ignoré est **invisible sur
GitHub** et **hors de toute sauvegarde** — quand l'espace de travail a été remis à zéro, les deux vidéos
ont disparu du disque, et aucun `git checkout` ne pouvait les ramener.

**Ce qui a changé le 22/10** — sur ta demande explicite, deux exceptions **nommées** dans `.gitignore` :

```gitconfig
!clients/dm-optic/content/month1/w1/tiktok-01-v2.mp4
!clients/dm-optic/content/month1/w1/ugc-03.mp4
```

Le reste de la règle tient toujours : **brouillons, `.silent.mp4`, rushs et voix restent hors dépôt**.
Ce qui entre, c'est uniquement **la vidéo finie telle qu'elle part en publication**.

> ⚠️ **Coût assumé** : ~11,6 Mo de plus dans l'historique git. Si tu préfères revenir à la règle du 23/09,
> il suffit de retirer ces deux lignes et les deux fichiers — dis-le et je le fais.

> ⚠️ **La release GitHub n'a pas pu être utilisée** : l'envoi de pièces jointes passe par
> `uploads.github.com`, **injoignable depuis cet espace de travail** (testé : code 000). La mise en dépôt
> directe est donc le seul chemin qui existe ici — et c'est aussi le plus simple pour toi.

## 3 · Les reproduire (si un fichier disparaît encore)

```bash
W=clients/dm-optic/content/month1/w1

# post 1 — 20/20/20 (moteur dédié, calé sur le script approuvé)
python3 tools/record/make_dmoptic_tiktok.py --out $W/tiktok-01-v2.mp4 --voice $W/assets/voix-v2.mp3
python3 tools/record/make_dmoptic_tiktok.py --cover $W/tiktok-01-v2-cover.jpg   # couverture, séparément

# post 2 — UGC sans visage (moteur storyboard)
python3 tools/ugc/ugc.py render $W/ugc-03.json --out $W/ugc-03.mp4 \
        --cover $W/ugc-03-cover.jpg --qc
```

**Les voix** se régénèrent avec `voice-00` et le texte exact : `tiktok-01-v2.fr.srt` (post 1),
`ugc-03.md` §1 (post 2). Aucune dépendance payante.

## 4 · La règle debout qui en sort

**Toute vidéo finie livrée à un client entre dans le dépôt, et son nom est écrit dans ce fichier.**
L'arborescence porte le storyboard, le script et le mode d'emploi — ce qui se relit et se corrige — et
maintenant aussi le binaire — ce qui se regarde. Les brouillons, eux, restent dehors.
