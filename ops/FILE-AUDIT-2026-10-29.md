# AUDIT DES FICHIERS — ce qui est mort, ce qui est en double, ce qui coûte

```text
Généré par tools/ops/audit_files.py — 2026-10-29
1962 fichiers · 173.9 Mo · dont 23.0 Mo dans des fichiers > 5 Mo
Aucune suppression automatique : les décisions sont listées, pas prises.
```

## 1 · Ce qui se supprime sans réflexion

| Classe | Fichiers | Poids | Action |
|---|---|---|---|
| caches (`__pycache__`, `*.pyc`) | 0 | 0 o | `python3 tools/ops/audit_files.py --clean-cache` |

## 2 · Doublons exacts — octet pour octet

### Doublons dans le **même** projet — ceux qu'on peut retirer

| Copie gardée | Doublon(s) | Taille unitaire |
|---|---|---|
| `content/reels/ep01/frames/v6-1700_release2.jpg` | `content/reels/ep01/frames/v6-xtra_release2.jpg` | 29.2 Ko |

**Gain : 29.2 Ko.**

### Paires source / déploiement — à garder, mais à surveiller

33 groupes. Le concept vit dans `demos/`, la copie déployée dans `hosting/previews/`. **Ce n'est pas du gras** : supprimer la copie déployée casse un site. Le risque réel est la **dérive** — deux copies qui divergent sans qu'on le sache.

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

138 fichiers, 12.4 Mo. **Piste, pas preuve** : un manifeste, un CSS ou un `JSON` peut les appeler autrement. Les rapports `ops/FILE-AUDIT-*.md` sont hors corpus : sans cela, l'audit se citerait lui-même et le chiffre changerait à chaque exécution.

| Dossier | Fichiers | Poids | Exemples |
|---|---|---|---|
| `tryon-camera/apercus/` | 3 | 2.0 Mo | apercu-interface.png, apercu-inventaire.png, exemples-6-montures.png |
| `mockups/` | 3 | 1.8 Mo | amk-phone.png, concept-phone.png, oracare-phone.png |
| `clients/dm-optic/launch/revue-2026-10-24/` | 9 | 1.1 Mo | 05-desktop-apres.jpg, 07-anneau-autour-carte-1024.jpg, 08-avant-apres-1440.jpg |
| `clients/_mockups/` | 5 | 983.3 Ko | EXEMPLE-clinique.jpg, EXEMPLE-college-2devices.jpg, EXEMPLE-college-portable.jpg |
| `content/Avatar/` | 6 | 769.8 Ko | E.jpeg, I.jpeg, K.jpeg |
| `clients/_mockups/labs/` | 3 | 647.2 Ko | 2k-labo.jpg, interlabo.jpg, meka.jpg |
| `content/reels/ep01/frames/` | 24 | 563.4 Ko | 0000015.jpg, 0000051.jpg, 0000070.jpg |
| `clients/_mockups/bonanjo-img/` | 3 | 526.1 Ko | imagerie.jpg, maternite.jpg, neuro.jpg |
| `clients/dm-optic/launch/facebook-assets/posters/` | 3 | 437.5 Ko | poster-01-garcon-vert.jpeg, poster-02-fille-verte.jpeg, poster-03-fille-bleue.jpeg |
| `content/carousels/c03-avant-de-payer/` | 5 | 416.7 Ko | slide-2.png, slide-3.png, slide-4.png |
| `hosting/previews/dmoptic/montures/` | 10 | 408.0 Ko | monture-e14-3.jpg, monture-f01-2.jpg, monture-f04-3.jpg |
| `content/carousels/c01-vous-etes-ouverts/` | 5 | 397.1 Ko | slide-2.png, slide-3.png, slide-4.png |
| `sales/social/videos/` | 4 | 355.1 Ko | clinic-founding-en-cover.jpg, clinic-founding-fr-cover.jpg, school-founding-en-cover.jpg |
| `content/pipeline/post01/vo/v5-sentences/` | 17 | 322.1 Ko | s04.mp3, s05.mp3, s06.mp3 |
| `content/carousels/c02-test-des-10-secondes/` | 5 | 284.6 Ko | slide-2.png, slide-3.png, slide-4.png |
| `content/videos/v06-facebook-no-booking/narration/` | 5 | 241.9 Ko | n1.mp3, n2.mp3, n3.mp3 |
| `content/pipeline/post01/vo/` | 12 | 226.5 Ko | vo-b1.mp3, vo-b2.mp3, vo-b3.mp3 |
| `sales/` | 1 | 226.3 Ko | AMK-5-Stage-Funnel.png |
| `brand/v1-green/` | 1 | 225.4 Ko | funnel-v1-green.png |
| `clients/dm-optic/content/month1/c1-render/` | 5 | 196.6 Ko | slide-2.png, slide-3.png, slide-4.png |

*Les photos de `clients/dm-optic/photoshoot/` ne sont PAS une rafale : c'est le **catalogue montures** du client — 160 photos, une par monture (156 montures + 4 vues du cabinet), 395 Mo. Elles sont listées parce qu'elles pèsent, pas parce qu'elles sont mortes : `sales/Activity-Log.md` (19/10) en garde **84 en réserve** pour le lot 2 du catalogue. Les supprimer effacerait la source d'un livrable à venir. Ce qui se discute ici, c'est de les sortir de git (stockage externe), pas de les effacer.*

## 4 · Documents

- **orphelins : NON MESURÉS** — le graphe des citations est absent (`graphify-out/graph.json`). Sans lui, tout document paraît orphelin : aucun chiffre ne veut dire quoi que ce soit. Remède : `python3 tools/graphify/build_full_graph.py`, puis rejouer cet audit.
- **0 documents marqués périmés par leur propre texte** — détection lexicale, à vérifier un par un.

| Périmé (d'après lui-même) | Cité par |
|---|---|

⚠️ **Ni l'orphelin ni le « périmé » ne se supprime automatiquement.** Le 24/10, `AMK-DESIGN-SKILLS.md` était signalé « remplacé par Activity-Log » — c'est faux, et une suppression sur cette base aurait effacé 1 400 lignes de règles de design.

## 4 bis · Les orphelins datés — ce que personne ne cite, et qui ne peut pas expirer

**Non mesurés.** Le graphe des citations est absent (`graphify-out/graph.json`) : sans lui, tout document paraît orphelin et aucun chiffre ne veut dire quoi que ce soit. Le reste de ce rapport (poids, doublons, médias) reste valable ; cette section, non.

```bash
python3 tools/graphify/build_full_graph.py && python3 tools/ops/audit_files.py
```

## 5 · Archives et artefacts

| Archive | Taille | Fabriquée par | Contenu |
|---|---|---|---|
| `dmopticsarl-2026-10-21.zip` | 4.6 Mo | `tools/ops/release.sh` | 182 fichier(s), plus récent 2026-10-21 |
| `dr-ophtalmo-site-2026-10-27.zip` | 710.4 Ko | — | 33 fichier(s), plus récent 2026-10-27 |

## 6 · Les 20 plus gros fichiers — ce qui pèse dans l'historique

| Fichier | Taille |
|---|---|
| `clients/dm-optic/brag/brag.mp4` | 14.6 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_132758528.MP.jpg` | 8.4 Mo |
| `dmopticsarl-2026-10-21.zip` | 4.6 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking_VOIX.mp4` | 4.1 Mo |
| `clients/dr-ophtalmo/brag/brag.mp4` | 4.1 Mo |
| `content/videos/v06-facebook-no-booking/Video_06_Facebook_No_Booking.mp4` | 3.2 Mo |
| `clients/dm-optic/photoshoot/others/PXL_20261016_131635710.MP.jpg` | 3.0 Mo |
| `tryon-camera/V2 Try-On Camera.html` | 2.9 Mo |
| `demos/img/le-cristallin-lab.png` | 2.6 Mo |
| `clients/dr-ophtalmo/brag/brag-whatsapp.mp4` | 2.5 Mo |
| `demos/img/le-cristallin-hero.png` | 2.5 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B1-entree-cabinet.png` | 2.4 Mo |
| `hosting/previews/dr-ophtalmo/assets/src/examination.png` | 2.4 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C1-mains-qui-ajustent.png` | 2.4 Mo |
| `hosting/previews/dr-ophtalmo/assets/src/portrait.png` | 2.3 Mo |
| `demos/img/le-cristallin-tryon.png` | 2.3 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/B2-salle-examen.png` | 2.2 Mo |
| `hosting/previews/dr-ophtalmo/assets/src/equipment.png` | 2.2 Mo |
| `clients/dm-optic/photoshoot/reference-composition-NE-PAS-PUBLIER/C2-monture-tenue-hauteur.png` | 2.2 Mo |
| `content/reels/ep01/ep01-v5.mp4` | 2.0 Mo |

⚠️ **Le `.git` ne perd rien quand on supprime un fichier.** Un binaire retiré reste dans l'historique ; seul un `git filter-repo` (réécriture + force-push) le retire vraiment. Tant que ce n'est pas fait, supprimer un gros média allège le disque, pas le dépôt.

---

*Rejouable : `python3 tools/ops/audit_files.py`. Rapport précédent à comparer : 1962 fichiers, 173.9 Mo.*
