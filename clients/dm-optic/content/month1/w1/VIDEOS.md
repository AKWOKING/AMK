# Où sont les vidéos — et pourquoi elles ne sont pas dans l'arborescence

```
Updated 2026-10-21 (soir)
Question de King : « je ne trouve pas ugc-03.mp4 sur github » · « where is post 1?? »
Réponse courte : les .mp4 ne sont pas versionnés (règle du dépôt), ils sont dans la RELEASE.
```

---

## 1 · La raison, en une ligne

Le dépôt **ignore les fichiers vidéo et audio par construction** :

```gitconfig
# .gitignore, ligne 13-20
# ── MÉDIAS LOURDS (règle du 23/09/2026, demande de King : « retire les vidéos précédentes,
#    elles rendent le repo lourd inutilement »). Le dépôt n'est pas un disque dur…
*.mp4
*.webm
*.mov
*.mkv
*.mp3
*.wav
```

**C'est ta règle, et elle est bonne** : 71 Mo avaient été retirés le 23/09 pour cette raison. Le corollaire
que je n'avais pas assez dit : **un fichier ignoré n'apparaît jamais sur GitHub**, et il **ne survit pas**
non plus à une remise à zéro de l'espace de travail. C'est exactement ce qui s'est passé cette nuit — les
deux vidéos et leurs voix ont disparu du disque, elles ont été **remontées et revérifiées** (voir §3).

## 2 · Où les prendre, maintenant

**Release GitHub** (téléchargement direct, aucun poids dans l'arborescence) :

> **`https://github.com/AKWOKING/AMK/releases/tag/dm-optique-videos-2026-10-22`**

| Fichier joint | Quoi |
|---|---|
| `tiktok-01-v2.mp4` | **le post 1** — 23,00 s, 1080×1920, voix incluse |
| `tiktok-01-v2-cover.jpg` | sa couverture 1080×1920 |
| `tiktok-01-v2.fr.srt` | ses sous-titres (7 blocs) |
| `ugc-03.mp4` | **le post 2** — 22,30 s, sans visage, « on montre avant de vendre » |
| `ugc-03-cover.jpg` | sa couverture |
| `ugc-03-voix.mp3` · `voix-v2.mp3` | les deux voix, séparées (si tu veux remonter à ta façon) |

La release est **permanente** : c'est elle, désormais, la copie de référence. Télécharge les fichiers sur
ton téléphone ou ton disque — l'espace de travail, lui, peut être remis à zéro.

## 3 · État au 2026-10-21, après remontage

| Fichier | Durée | Poids | Portique |
|---|---|---|---|
| `tiktok-01-v2.mp4` | 23,00 s | 4,8 Mo | **OK** (min 2,72/255 sur 20-22 s) |
| `ugc-03.mp4` | 22,30 s | 6,8 Mo | **OK** (min 1,78/255 sur 20-22 s) |

## 4 · Les reproduire (si un fichier disparaît encore)

```bash
W=clients/dm-optic/content/month1/w1

# post 1 — 20/20/20 (moteur dédié, calé sur le script approuvé)
python3 tools/record/make_dmoptic_tiktok.py --out $W/tiktok-01-v2.mp4 --voice $W/assets/voix-v2.mp3
python3 tools/record/make_dmoptic_tiktok.py --cover $W/tiktok-01-v2-cover.jpg   # la couverture, à part

# post 2 — UGC sans visage (moteur storyboard)
python3 tools/ugc/ugc.py render $W/ugc-03.json --out $W/ugc-03.mp4 \
        --cover $W/ugc-03-cover.jpg --qc
```

Les **voix** se régénèrent avec `tools/record/` et la voix de la maison (`voice-00`) : le texte exact est
dans `tiktok-01-v2.fr.srt` (post 1) et dans `ugc-03.md` §1 (post 2). Aucune dépendance à un service payant.

## 5 · La règle qui en sort (proposition, ruling à toi)

**Tout fichier vidéo livré est déposé en release le jour même, et son nom est écrit dans ce fichier.**
L'arborescence garde le storyboard, le script et le mode d'emploi — ce qui se relit et se corrige — et la
release garde le binaire, ce qui se regarde. Si tu préfères l'inverse (les `.mp4` dans l'arborescence), il
suffit d'une ligne dans `.gitignore` ; dis-le et je l'ajoute.
