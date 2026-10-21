# UGC-03 · « On montre avant de vendre » — sans visage

```
Status: PRODUIT, NON PUBLIÉ   ·  Date: 22/10/2026   ·  Format: 9:16, 1080x1920, 30 fps
Fichier: ugc-03.mp4 (22,30 s, 6,8 Mo)   ·  Couverture: ugc-03-cover.jpg
Moteur: tools/ugc/ugc.py   ·  Storyboard: ugc-03.json   ·  Voix: assets/ugc-03-voix.mp3
Portique mouvement: OK (aucune fenêtre figée)   ·  Visages: ceux du personnel (autorisés, King 22/10)
```

**Rôle dans la série.** TikTok n°1 (V2) prouve *le cabinet et la monture*. UGC-03 prouve *la méthode* :
la transparence avant la vente — quarante montures photographiées, le prix affiché, l'examen le matin.
C'est le contenu qui transforme « joli cabinet » en « je peux vérifier avant de me déplacer ».

---

## 1 · Découpage (22,30 s)

| # | Temps | Plan | Sous-titre | Voix |
|---|---|---|---|---|
| 1 | 0,0–3,4 | autorefractor, personnel en blouse | Choisir des lunettes, ça commence par mesurer. | idem |
| 2 | 3,4–6,8 | carton sur le mur de montures | — | 40 modèles en ligne. |
| 3 | 6,8–10,8 | monture f24, carte crème | Celle-ci. Ce prix. En photo. | avec son prix. |
| 4 | 10,8–14,4 | monture h08, carte crème | Pas de surprise à la caisse. | — |
| 5 | 14,4–18,0 | intérieur, mur de montures | Examen 8h30–13h00 / Opticien inscrit ONOC. | L'examen, c'est le matin, avec un opticien inscrit à l'ONOC. |
| 6 | 18,0–22,3 | carton de fin sur l'enseigne | On montre avant de vendre. | On montre avant de vendre. WhatsApp : 656 122 239. |

**Texte de la voix (22,1 s, `voice-00`, la voix de la maison) :**

> Choisir des lunettes, ça commence par mesurer. Chez DM Optique, chaque monture est photographiée, avec
> son prix. Quarante modèles en ligne. L'examen, c'est le matin, avec un opticien inscrit à l'ONOC. On
> montre avant de vendre. WhatsApp : 656 122 239.

**Vérifications de contenu** : aucun prix affiché à l'écran (règle maison) · aucune allégation médicale ·
aucun témoignage · aucun concurrent nommé · « 40 montures » = 40 modèles publiés sur le site (comptage du
catalogue, pas une estimation) · « opticien inscrit ONOC » = registre Littoral l.102, inscription 021/2016.

---

## 2 · Ce qui est mesuré

```
ugc-03.mp4 · 22,3 s · fenêtre 2 s · seuil 1,5/255
0-2 14,43 · 2-4 94,54 · 4-6 2,00 · 6-8 88,21 · 8-10 2,86 · 10-12 43,65
12-14 2,22 · 14-16 101,13 · 16-18 13,70 · 18-20 105,18 · 20-22 2,62
VERDICT : OK — mouvement dans chaque fenêtre
```

Les trois fenêtres « calmes » (4-6, 8-10, 12-14) sont les cartons produit : le fond est fixe, c'est le
recadrage qui glisse. Elles passent, mais ce sont les endroits où le montage doit être le plus court.

---

## 3 · Ce qui manque, et qui ne s'invente pas

Aucun visage **généré** dans ce fichier. Les visages présents sont ceux du personnel, sur des photos
réelles. Pour un vrai plan d'influenceur IA : `tools/ugc/providers.py` + une clé (Veo 3.1, 0,96 $ le clip
de 8 s) — voir `research/ugc-video/2026-10-22-TOOLCHAIN-UGC.md` §3.

## 4 · Reproductible

```bash
python3 tools/ugc/ugc.py render clients/dm-optic/content/month1/w1/ugc-03.json \
        --out clients/dm-optic/content/month1/w1/ugc-03.mp4 \
        --cover clients/dm-optic/content/month1/w1/ugc-03-cover.jpg --qc
```

Le rendu prend ~100 s et le portique doit sortir en code 0. Toute différence de durée, de taille ou de
verdict est un **écart à expliquer avant publication**.
