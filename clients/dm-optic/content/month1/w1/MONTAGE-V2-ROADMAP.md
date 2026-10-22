# Montage de la V2 — plan de travail (22/10, soir)

**Objectif** : une vidéo de 23 s, 1080×1920, prête à publier, montée **ce soir**, sans tournage et sans
visage — à partir des photos réelles du dépôt.

> **État, 22/10 18 h 55 : MONTÉE.** `tiktok-01-v2.mp4` — 23,00 s, 1080×1920, 30 fps, H.264 + AAC,
> **4,3 Mo**, voix incluse. Portique mouvement : **OK**, aucune fenêtre figée (min 2,16/255 sur 4-6 s).
> Ce qui a changé par rapport au plan est consigné en §7 — pas effacé.

**Ce que ce document est** : le plan, écrit **avant** de commencer, avec les outils, les décisions
techniques et les contrôles. Il est daté pour qu'on puisse dire plus tard ce qui a été prévu et ce qui a
changé en route.

---

## 1 · Les faits de départ

| Élément | État vérifié le 22/10 |
|---|---|
| Script | `tiktok-01-v2-20-20-20.md` — 6 beats, 23 s, 60 mots |
| Sous-titres | `tiktok-01-v2.fr.srt` — 7 blocs, écrits à la main |
| Photos disponibles | 65 images de montures (1600×1200) + 8 photos du cabinet |
| Typographie | **Schibsted Grotesk** (500/700) + IBM Plex Sans — les polices du site, en `woff2` |
| Couleurs | `--brand #1A3F86` · `--ink #0C1524` · `--paper #EEF1F5` · `--wa #0B7A3E` |
| Outils installés | ❌ aucun : ni ffmpeg, ni PIL, ni police, ni brotli |
| Portique | `tools/qa/audit_video_motion.py` — **bloquant** : aucune fenêtre de 2 s figée |

---

## 2 · Ce qui doit être installé, et pourquoi

| Paquet | Rôle | Pourquoi lui |
|---|---|---|
| `pillow` | rendu des cartons et composition des images | pas de navigateur dans le sandbox (Chromium bloqué) |
| `imageio-ffmpeg` | **binaire ffmpeg statique** | `apt` n'a pas accès aux dépôts ; ce paquet embarque ffmpeg 7.0.2 |
| `numpy` | portique mouvement (déjà requis par l'outil QA) | |
| `fonttools` + `brotli` | conversion `woff2` → `ttf` | PIL ne lit pas le `woff2` ; sans brotli, fontTools refuse |

**Installation** : `pip install --user --break-system-packages pillow imageio-ffmpeg numpy fonttools brotli`
— c'est la commande déjà utilisée dans ce dépôt (`tools/record/make_video.py` s'appuie sur le même
binaire ffmpeg).

---

## 3 · Les décisions de fabrication

### 3.1 Les images : trois traitements, pas un

| Type | Source | Traitement 9:16 |
|---|---|---|
| **Monture** (f01, f24, e16) | 1600×1200, fond crème uni | fond **échantillonné** aux bords et étendu — la monture reste intacte, **aucune retouche du produit** |
| **Intérieur** (cabinet-interieur) | 1400×926 | recadrage vertical + **panoramique lent** sur le mur de montures |
| **Carton** (fin) | aucun | fond bleu de marque + logo + texte, zoom lent |

Le fond crème de la F24 est uni : l'étendre n'est pas retoucher la photo, c'est **changer le cadre**.
Règle maison respectée : la monture, elle, n'est pas touchée.

### 3.2 Le mouvement : obligatoire partout

Le portique bloque toute fenêtre de 2 s figée. Donc **chaque plan bouge** : zoom lent (2 à 6 % sur la
durée du plan), panoramique horizontal pour l'intérieur, et apparition progressive des cartons
(opacité + 12 px de translation). Le carton final, prévu « stable 3 s » dans le script, devient
**zoom lent + texte qui se pose** — sinon il échouerait au portique.

### 3.3 La voix

`generate_speech` exige une voix **choisie par King** (`add_voice`). Deux voix françaises sont proposées
à l'écoute ; le montage final utilise celle qu'il retient. **La vidéo ne part pas sans audio dans le
fichier** (règle maison) — d'où deux versions produites : une version **muette de contrôle** (pour valider
l'image tout de suite) et la **version finale avec voix**.

### 3.4 Les sous-titres

Les 7 blocs du `.srt` sont **incrustés** dans l'image (pas seulement en piste). TikTok affiche ses propres
sous-titres automatiques si on les laisse faire — on ne les utilise pas. Incrustés = ce que le spectateur
voit est exactement ce qu'on a écrit.

---

## 4 · L'ordre d'exécution

| # | Étape | Sortie | Contrôle |
|---|---|---|---|
| 1 | Installer les 5 paquets | — | `ffmpeg -version`, `PIL` importable |
| 2 | Convertir 4 polices `woff2` → `ttf` | `assets/fonts/*.ttf` | chaque fichier > 10 Ko, ouvert par PIL |
| 3 | Écrire le moteur de rendu | `tools/record/make_dmoptic_tiktok.py` | rendu image par image, 690 images |
| 4 | Versions muettes | `tiktok-01-v2-silent.mp4` | durée 23,0 s ± 0,2 |
| 5 | **Portique mouvement** | verdict | 0 fenêtre figée, code de sortie 0 |
| 6 | Contrôle visuel | 4 PNG extraits | je les ouvre et je les regarde |
| 7 | Voix (choix de King) | `voix.mp3` | durée ≈ 21 s |
| 8 | Montage final | `tiktok-01-v2.mp4` | audio présent, volume normalisé |
| 9 | Contrôle final | portique + ffprobe + 3 PNG | aucune régression |

---

## 5 · Ce qui peut échouer, et le repli prévu

| Risque | Repli |
|---|---|
| Une photo du cabinet contient un visage **non identifiable comme personnel** | on garde (King : les visages du personnel sont autorisés) ; sinon on passe au carton |
| Le panoramique sur l'intérieur est flou (photo 1400 px étirée en 1920) | on réduit le zoom et on garde le cadrage natif ; jamais d'agrandissement au-delà de 1,4× |
| La voix générée est trop rapide ou trop lente pour 23 s | on ajuste le texte, **pas** la vitesse de lecture à l'export (un débit accéléré s'entend) |
| Le portique signale une fenêtre figée | on ajoute du mouvement dans la fenêtre — jamais on ne baisse le seuil |
| Le rendu dépasse 25 Mo | on garde H.264, CRF 20, `faststart`, audio 128 kb/s |

---

## 6 · Ce qui n'est pas dans ce plan, volontairement

- **Aucune image IA.** Le mois est sans visage ; les photos réelles suffisent. La question des modèles
  UGC IA est traitée à part, avec ses conditions (`knowledge/CONTENT-CREATION-2026-10-22.md` §6).
- **Aucune musique commerciale.** Silence + voix, ou piste libre documentée.
- **Aucune retouche de produit.** Le cadrage change, la monture non.
- **Aucune publication.** Le fichier est livré ; c'est King qui publie (§ règle de maison).

---

## 7 · Journal de montage — ce qui a changé en route

| # | Décision du plan | Ce qui s'est passé | Correction |
|---|---|---|---|
| 1 | photos paysage posées sur un fond flou | ça donnait deux grandes zones grises mortes en haut et en bas | **recadrage couvrant** : la photo remplit tout le cadre, aucune bande |
| 2 | texte blanc avec ombre | illisible sur le sol clair et sur le fond crème | **bandeau marine plein cadre** sous le texte, avec filet orange qui grandit |
| 3 | première version du mouvement (« zoom 5 % ») | **portique BLOQUÉ** : 5 fenêtres figées sur 11 | amplitudes portées à 14–16 %, déplacement en x **et** en y, carton final rendu à 1,22× puis recadré |
| 4 | carton final « stable 3 s » | aurait échoué au portique | rendu plus grand puis **recadrage mouvant** : net *et* en mouvement |
| 5 | la 5ᵉ image : E16 (enfant) | une monture enfant sous un texte sur la vue = mauvais signal | **H08**, monture homme, plus neutre |
| 6 | photos du cabinet centrées | coupaient le poster « anatomie de l'œil » et laissaient un mur vide | **ancrage du recadrage à 30 %** (gauche) : on garde le mur de montures |
| 7 | voix posée puis `-shortest` | **la vidéo tombait à 21,2 s** : le carton WhatsApp était coupé | tempo doux (0,92) + silence de fin, **durée forcée à 23,00 s** |
| 8 | montage muet d'abord | utile pour valider l'image sans attendre la voix | gardé : c'est la version de contrôle |
| 9 | police du site en `woff2` | PIL ne lit pas le `woff2`, et fontTools exige `brotli` | conversion en `ttf` versionnée dans `assets/fonts/` |

**Ce qui n'a pas bougé** : aucune photo de produit retouchée · aucun visage · aucune image IA · aucune
musique · un seul CTA · la durée (23 s) · le texte des sous-titres.

---

## 8 · La couverture

Produite par le même moteur (`--cover`). 1080×1920, la F24 sur carte crème, l'accroche dans le **carré
central** — c'est ce carré que la grille de profil recadre, donc l'accroche reste lisible même réduite.
Pied de couverture : « Opticien optométriste · WhatsApp 656 122 239 ».

