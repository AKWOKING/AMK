# AUDIT DES FICHIERS — ce qui est mort, ce qui est en double, ce qui coûte

```text
Généré par tools/ops/audit_files.py — 2026-10-24
1613 fichiers · 137.2 Mo · dont 23.0 Mo dans des fichiers > 5 Mo
Aucune suppression automatique : les décisions sont listées, pas prises.
```

## 1 · Ce qui se supprime sans réflexion

| Classe | Fichiers | Poids | Action |
|---|---|---|---|
| caches (`__pycache__`, `*.pyc`) | 0 | 0 o | `python3 tools/ops/audit_files.py --clean-cache` |

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

60 fichiers, 3.5 Mo. **Piste, pas preuve** : un manifeste, un CSS ou un `JSON` peut les appeler autrement.

| Dossier | Fichiers | Poids | Exemples |
|---|---|---|---|
| `clients/_mockups/bonanjo-img/` | 3 | 526.1 Ko | imagerie.jpg, maternite.jpg, neuro.jpg |
| `clients/dm-optic/launch/facebook-assets/posters/` | 3 | 437.5 Ko | poster-01-garcon-vert.jpeg, poster-02-fille-verte.jpeg, poster-03-fille-bleue.jpeg |
| `clients/_mockups/` | 2 | 408.9 Ko | EXEMPLE-college-telephone.jpg, EXEMPLE-dentaire-2devices.jpg |
| `content/Avatar/` | 3 | 359.8 Ko | E.jpeg, I.jpeg, K.jpeg |
| `content/carousels/c03-avant-de-payer/` | 3 | 320.5 Ko | slide-2.png, slide-3.png, slide-4.png |
| `hosting/previews/dmoptic/montures/` | 7 | 290.2 Ko | monture-e14-3.jpg, monture-f01-2.jpg, monture-f08-3.jpg |
| `content/pipeline/post01/vo/v5-sentences/` | 14 | 276.8 Ko | s07.mp3, s08.mp3, s09.mp3 |
| `content/carousels/c01-vous-etes-ouverts/` | 3 | 177.3 Ko | slide-2.png, slide-3.png, slide-4.png |
| `content/pipeline/post01/vo/` | 9 | 176.9 Ko | vo-b4.mp3, vo-b4a.mp3, vo-b4b.mp3 |
| `content/carousels/c02-test-des-10-secondes/` | 3 | 165.6 Ko | slide-2.png, slide-3.png, slide-4.png |
| `clients/dm-optic/content/month1/c1-render/` | 3 | 117.8 Ko | slide-2.png, slide-3.png, slide-4.png |
| `sales/social/videos/` | 1 | 97.3 Ko | school-founding-fr-cover.jpg |
| `content/videos/v06-facebook-no-booking/narration/` | 2 | 86.4 Ko | n4.mp3, n5.mp3 |
| `clients/dm-optic/website/logo/` | 1 | 79.2 Ko | source-extrait-du-pdf-1240x992.jpg |
| `clients/dm-optic/brand/` | 1 | 70.1 Ko | CARTE-SIGNATURE-TABLEAU-VISION-preview.png |
| `content/videos/v07-stock-invisible/assets/` | 2 | 38.0 Ko | maquette-ui-1.png, maquette-ui-2.png |

*Les photos de `clients/dm-optic/photoshoot/` ne sont PAS une rafale : c'est le **catalogue montures** du client — 160 photos, une par monture (156 montures + 4 vues du cabinet), 395 Mo. Elles sont listées parce qu'elles pèsent, pas parce qu'elles sont mortes : `sales/Activity-Log.md` (19/10) en garde **84 en réserve** pour le lot 2 du catalogue. Les supprimer effacerait la source d'un livrable à venir. Ce qui se discute ici, c'est de les sortir de git (stockage externe), pas de les effacer.*

## 4 · Documents

- **390 documents sans citation entrante** — à relire ou à archiver (voir `ops/REPO-MAP.md` §3 bis).
- **1 documents marqués périmés par leur propre texte** — détection lexicale, à vérifier un par un.

| Périmé (d'après lui-même) | Cité par |
|---|---|
| `sales/Walk-In-Batch-2026-09-15.md` | 3× |

⚠️ **Ni l'orphelin ni le « périmé » ne se supprime automatiquement.** Le 24/10, `AMK-DESIGN-SKILLS.md` était signalé « remplacé par Activity-Log » — c'est faux, et une suppression sur cette base aurait effacé 1 400 lignes de règles de design.

## 4 bis · Les orphelins datés — ce que personne ne cite, et qui ne peut pas expirer

**390 orphelins** au total, mais **60 seulement à traiter** : les autres sont normaux (164 imports tiers, 116 fiches CRM reliées par la base, 50 README d'outils installés).

- **41 n'ont aucune date**, ni dans leur chemin, ni dans leurs douze premières lignes : un document sans date ne peut pas expirer, donc il ne meurt jamais.
- Les 19 autres s'étalent du **2026-09-21** au **2026-10-24**.

| Famille | Orphelins | Le plus ancien | Verdict proposé |
|---|---|---|---|
| `clients/dm-optic` | 15 | 2026-10-07 | à décider |
| `content/videos` | 7 | 2026-10-22 | archiver avec le lot du mois |
| `ops/` | 7 | 2026-10-07 | à décider |
| `content/scripts` | 4 | sans date | à décider |
| `content/pipeline` | 3 | 2026-10-05 | à décider |
| `hosting/samples` | 3 | sans date | à décider |
| `ops/templates` | 3 | sans date | citer depuis la machine |
| `research/youtube-lessons` | 3 | 2026-10-11 | archiver après synthèse |
| `sales/` | 3 | 2026-09-21 | à décider |
| `content/assets` | 2 | sans date | à décider |
| `content/Avatar` | 1 | sans date | à décider |
| `content/` | 1 | sans date | citer (point d'entrée d'un dossier vivant) |
| `content/studio` | 1 | sans date | citer (point d'entrée d'un dossier vivant) |
| `demos/img` | 1 | sans date | à décider |
| `design/` | 1 | sans date | citer (point d'entrée d'un dossier vivant) |
| `hosting/previews` | 1 | sans date | à décider |
| `leads/` | 1 | sans date | à décider |
| `sales/VAGUE-2026-10-12` | 1 | 2026-10-12 | archiver |
| `site/` | 1 | 2026-10-23 | à décider |
| `site/img` | 1 | sans date | à décider |

*Le verdict est une **proposition**, pas une décision : archiver = `git mv` vers `archive/`, jamais supprimer. `archive/` sort du corpus (ni carte, ni portes, ni audit) mais reste dans git.*

**Les documents sans date** (à dater ou à archiver) :

- `clients/dm-optic/brag/MEDIA.md`
- `clients/dm-optic/content/month1/c1-render/README.md`
- `clients/dm-optic/content/month1/w2/etapes-01-validation-client.md`
- `clients/dm-optic/content/month1/w2/etapes-01.md`
- `clients/dm-optic/content/month1/w2/facebook-post-enfants.md`
- `clients/dm-optic/launch/facebook-assets/MEDIA.md`
- `clients/dm-optic/onboarding/VISIT-FALLBACKS.md`
- `clients/dm-optic/onboarding/VOICE-NOTE-MARDI-06-10.md`
- `clients/dm-optic/photoshoot/others/MEDIA.md`
- `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/MEDIA.md`
- `content/Avatar/_composites/busts-694/MEDIA.md`
- `content/README.md`
- `content/assets/ASSETS.md`
- `content/assets/fonts/MEDIA.md`
- `content/pipeline/post01/SENTENCE-TIMING-v5d.md`
- `content/pipeline/post01/layers/MEDIA.md`
- `content/scripts/v01-instagram-vs-website.md`
- `content/scripts/v02-five-website-answers.md`
- `content/scripts/v03-part2-three-reasons.md`
- `content/scripts/v04-before-whatsapp.md`
- `content/studio/README.md`
- `content/videos/v02-five-website-answers/STATUS.md`
- `content/videos/v03-part2-three-reasons/STATUS.md`
- `content/videos/v04-before-whatsapp/STATUS.md`
- `content/videos/v05-schools/STATUS.md`
- `content/videos/v06-facebook-no-booking/MEDIA.md`
- `demos/img/MEDIA.md`
- `design/README.md`
- `hosting/previews/dmoptic/montures/MEDIA.md`
- `hosting/samples/DEPLOY.md`
- `hosting/samples/design-research.md`
- `hosting/samples/img/MEDIA.md`
- `leads/M1-EXTRACTION-REPORT.md`
- `ops/CHANGELOG-VENDREDI.md`
- `ops/CHECKPOINT-MARDI-06-10-20H.md`
- `ops/FIRST-CLIENT-PRE-MORTEM.md`
- `ops/POST-WEDNESDAY-2026-10.md`
- `ops/templates/TASK-TEMPLATE-CARROUSEL.md`
- `ops/templates/TASK-TEMPLATE-SITE-BUILD.md`
- `ops/templates/TASK-TEMPLATE-UGC-SCRIPT.md`
- `site/img/MEDIA.md`

## 5 · Archives et artefacts

| Archive | Taille | Fabriquée par | Contenu |
|---|---|---|---|
| `dmopticsarl-2026-10-21.zip` | 4.6 Mo | `tools/ops/release.sh` | 182 fichier(s), plus récent 2026-10-21 |

## 6 · Les 20 plus gros fichiers — ce qui pèse dans l'historique

| Fichier | Taille |
|---|---|
| `clients/dm-optic/brag/brag.mp4` | 14.6 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_132758528.MP.jpg` | 8.4 Mo |
| `dmopticsarl-2026-10-21.zip` | 4.6 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking_VOIX.mp4` | 4.1 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking.mp4` | 3.2 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_131635710.MP.jpg` | 3.0 Mo |
| `tryon-camera/V2 Try-On Camera.html` | 2.9 Mo |
| `demos/img/le-cristallin-lab.png` | 2.6 Mo |
| `demos/img/le-cristallin-hero.png` | 2.5 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B1-entree-cabinet.png` | 2.4 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C1-mains-qui-ajustent.png` | 2.4 Mo |
| `demos/img/le-cristallin-tryon.png` | 2.3 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B2-salle-examen.png` | 2.2 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C2-monture-tenue-hauteur.png` | 2.2 Mo |
| `mockups/oracare-phone.png` | 1.6 Mo |
| `content/assets/host/s1_hook.png` | 1.2 Mo |
| `brand/avatar-amk.png` | 1.1 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/A3-profil-branches.png` | 1.1 Mo |
| `tryon-camera/apercus/exemples-6-montures.png` | 1009.3 Ko |
| `content/pipeline/post01/vo/vo-master-v5d.mp3` | 992.9 Ko |

⚠️ **Le `.git` ne perd rien quand on supprime un fichier.** Un binaire retiré reste dans l'historique ; seul un `git filter-repo` (réécriture + force-push) le retire vraiment. Tant que ce n'est pas fait, supprimer un gros média allège le disque, pas le dépôt.

---

*Rejouable : `python3 tools/ops/audit_files.py`. Rapport précédent à comparer : 1613 fichiers, 137.2 Mo.*
