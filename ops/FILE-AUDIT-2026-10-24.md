# AUDIT DES FICHIERS — ce qui est mort, ce qui est en double, ce qui coûte

```text
Généré par tools/ops/audit_files.py — 2026-10-24
1638 fichiers · 188.5 Mo · dont 66.2 Mo dans des fichiers > 5 Mo
Aucune suppression automatique : les décisions sont listées, pas prises.
```

## 1 · Ce qui se supprime sans réflexion

| Classe | Fichiers | Poids | Action |
|---|---|---|---|
| caches (`__pycache__`, `*.pyc`) | 2 | 144.0 Ko | `python3 tools/ops/audit_files.py --clean-cache` |

## 2 · Doublons exacts — octet pour octet

Aucun doublon à l'intérieur d'un même projet.

### Paires source / déploiement — à garder, mais à surveiller

32 groupes. Le concept vit dans `demos/`, la copie déployée dans `hosting/previews/`. **Ce n'est pas du gras** : supprimer la copie déployée casse un site. Le risque réel est la **dérive** — deux copies qui divergent sans qu'on le sache.

| Source | Déploiement | Taille |
|---|---|---|
| `demos/concept-le-cristallin-v1.html` | `hosting/previews/cristallin/index.html` | 608.7 Ko |
| `hosting/samples/img/nova.png` | `site/img/nova.png` | 232.4 Ko |
| `hosting/samples/img/littleoaks.png` | `site/img/littleoaks.png` | 219.3 Ko |
| `clients/_mockups/labs/labiomed.jpg` | `hosting/previews/labiomed/og.jpg` | 212.2 Ko |
| `hosting/samples/img/mmc-consult.jpg` | `site/assets/mockup-clinique.jpg`, `site/img/mmc-consult.jpg` | 192.7 Ko |
| `hosting/samples/img/mmc-maternity.jpg` | `site/img/mmc-maternity.jpg` | 169.2 Ko |
| `hosting/samples/img/sec-campus.jpg` | `site/img/sec-campus.jpg` | 156.0 Ko |
| `hosting/samples/img/mmc-hero.jpg` | `site/img/mmc-hero.jpg` | 144.0 Ko |
| `hosting/samples/img/mmc-lab.jpg` | `site/img/mmc-lab.jpg` | 125.5 Ko |
| `hosting/samples/img/mit-wall.jpg` | `site/img/mit-wall.jpg` | 109.7 Ko |
| `hosting/samples/img/sec-hero.jpg` | `site/img/sec-hero.jpg` | 103.4 Ko |
| `hosting/samples/img/sec-class.jpg` | `site/assets/mockup-college.jpg`, `site/img/sec-class.jpg` | 88.5 Ko |
| `hosting/samples/build_sample_secondary.py` | `site/build_sample_secondary.py` | 73.3 Ko |
| `hosting/samples/img/sec-dorm.jpg` | `site/img/sec-dorm.jpg` | 66.6 Ko |
| `hosting/samples/img/sec-awards.jpg` | `site/img/sec-awards.jpg` | 66.3 Ko |
| `hosting/samples/img/mit-hero.jpg` | `site/img/mit-hero.jpg` | 62.3 Ko |
| `hosting/samples/build_sample_clinic.py` | `site/build_sample_clinic.py` | 58.6 Ko |
| `hosting/samples/img/sec-sports.jpg` | `site/img/sec-sports.jpg` | 58.3 Ko |
| `hosting/samples/img/sec-lab.jpg` | `site/img/sec-lab.jpg` | 57.9 Ko |
| `hosting/samples/build_sample_mitoc.py` | `site/build_sample_mitoc.py` | 54.4 Ko |


## 3 · Médias sans aucune référence par leur nom

87 fichiers, 12.0 Mo. **Piste, pas preuve** : un manifeste, un CSS ou un `JSON` peut les appeler autrement.

| Dossier | Fichiers | Poids | Exemples |
|---|---|---|---|
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/` | 2 | 2.1 Mo | A1-monture-face-catalogue.png, A3-profil-branches.png |
| `tryon-camera/apercus/` | 3 | 2.0 Mo | apercu-interface.png, apercu-inventaire.png, exemples-6-montures.png |
| `mockups/` | 3 | 1.8 Mo | amk-phone.png, concept-phone.png, oracare-phone.png |
| `content/Avatar/_composites/busts-694/` | 3 | 1.1 Mo | avatar-approving-694.png, avatar-idle-694.png, avatar-pointing-694.png |
| `hosting/previews/dmoptic/montures/` | 22 | 1013.6 Ko | monture-e14-2.jpg, monture-e14-3.jpg, monture-e19-2.jpg |
| `clients/_mockups/labs/` | 3 | 647.2 Ko | 2k-labo.jpg, interlabo.jpg, meka.jpg |
| `clients/_mockups/` | 3 | 574.4 Ko | EXEMPLE-clinique.jpg, EXEMPLE-college-2devices.jpg, EXEMPLE-college-portable.jpg |
| `demos/img/` | 2 | 436.4 Ko | dmoptic-enfants.jpg, dmoptic-montures.jpg |
| `content/Avatar/` | 3 | 410.1 Ko | M.jpeg, N.jpeg, WhatsApp Image 2026-10-12 at 18.34.29.jpeg |
| `sales/social/videos/` | 3 | 257.8 Ko | clinic-founding-en-cover.jpg, clinic-founding-fr-cover.jpg, school-founding-en-cover.jpg |
| `content/pipeline/post01/vo/v5-sentences/` | 14 | 256.4 Ko | s04.mp3, s05.mp3, s06.mp3 |
| `sales/` | 1 | 226.3 Ko | AMK-5-Stage-Funnel.png |
| `brand/v1-green/` | 1 | 225.4 Ko | funnel-v1-green.png |
| `content/carousels/c01-vous-etes-ouverts/` | 2 | 219.8 Ko | slide-5.png, slide-6.png |
| `clients/_mockups/labs/img/` | 1 | 174.2 Ko | hero-lab.jpg |
| `content/pipeline/post01/vo/` | 9 | 163.4 Ko | vo-b1.mp3, vo-b2.mp3, vo-b3.mp3 |
| `content/videos/v06-facebook-no-booking/narration/` | 3 | 155.6 Ko | n1.mp3, n2.mp3, n3.mp3 |
| `content/carousels/c02-test-des-10-secondes/` | 2 | 119.0 Ko | slide-5.png, slide-6.png |
| `content/carousels/c03-avant-de-payer/` | 2 | 96.2 Ko | slide-5.png, slide-6.png |
| `tryon-camera/` | 1 | 79.9 Ko | og-uo-camera.jpg |

*Les photos de `clients/dm-optic/photoshoot/` ne sont PAS une rafale : c'est le **catalogue montures** du client — 160 photos, une par monture (156 montures + 4 vues du cabinet), 395 Mo. Elles sont listées parce qu'elles pèsent, pas parce qu'elles sont mortes : `sales/Activity-Log.md` (19/10) en garde **84 en réserve** pour le lot 2 du catalogue. Les supprimer effacerait la source d'un livrable à venir. Ce qui se discute ici, c'est de les sortir de git (stockage externe), pas de les effacer.*

## 4 · Documents

- **412 documents sans citation entrante** — à relire ou à archiver (voir `ops/REPO-MAP.md` §3 bis).
- **1 documents marqués périmés par leur propre texte** — détection lexicale, à vérifier un par un.

| Périmé (d'après lui-même) | Cité par |
|---|---|
| `sales/Walk-In-Batch-2026-09-15.md` | 3× |

⚠️ **Ni l'orphelin ni le « périmé » ne se supprime automatiquement.** Le 24/10, `AMK-DESIGN-SKILLS.md` était signalé « remplacé par Activity-Log » — c'est faux, et une suppression sur cette base aurait effacé 1 400 lignes de règles de design.

## 5 · Archives et artefacts

| Archive | Taille | Fabriquée par | Contenu |
|---|---|---|---|
| `amk-factures-pwa-v2.zip` | 86.1 Ko | — | 6 fichier(s), plus récent 2026-10-23 |
| `amk-factures-pwa.zip` | 85.8 Ko | — | 6 fichier(s), plus récent 2026-10-23 |
| `dmopticsarl.zip` | 4.6 Mo | `demos/pack_dmoptic.py` | 182 fichier(s), plus récent 2026-10-21 |

## 6 · Les 20 plus gros fichiers — ce qui pèse dans l'historique

| Fichier | Taille |
|---|---|
| `clients/dm-optic/brag/brag.mp4` | 14.6 Mo |
| `clients/dm-optic/content/month1/w1/spot-03.mp4` | 13.6 Mo |
| `clients/dm-optic/content/month1/w1/spot-02.mp4` | 12.1 Mo |
| `clients/dm-optic/content/month1/w2/etapes-01.mp4` | 11.1 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_132758528.MP.jpg` | 8.4 Mo |
| `clients/dm-optic/content/month1/w1/ugc-03.mp4` | 6.5 Mo |
| `dmopticsarl.zip` | 4.6 Mo |
| `clients/dm-optic/content/month1/w1/tiktok-01-v2.mp4` | 4.5 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking_VOIX.mp4` | 4.1 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking.mp4` | 3.2 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_131635710.MP.jpg` | 3.0 Mo |
| `tryon-camera/V2 Try-On Camera.html` | 2.9 Mo |
| `tryon-camera/archive/V1 Try-On Camera.html` | 2.9 Mo |
| `demos/img/le-cristallin-lab.png` | 2.6 Mo |
| `demos/img/le-cristallin-hero.png` | 2.5 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B1-entree-cabinet.png` | 2.4 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C1-mains-qui-ajustent.png` | 2.4 Mo |
| `demos/img/le-cristallin-tryon.png` | 2.3 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B2-salle-examen.png` | 2.2 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C2-monture-tenue-hauteur.png` | 2.2 Mo |

⚠️ **Le `.git` ne perd rien quand on supprime un fichier.** Un binaire retiré reste dans l'historique ; seul un `git filter-repo` (réécriture + force-push) le retire vraiment. Tant que ce n'est pas fait, supprimer un gros média allège le disque, pas le dépôt.

---

*Rejouable : `python3 tools/ops/audit_files.py`. Rapport précédent à comparer : 1638 fichiers, 188.5 Mo.*
