# REELS — le studio explainer AMK (format « post-it animé »)

> **Réponse à King, 25/10 (tour 144)** : *« I want content like these, can you do it ?? yes or no »* →
> **OUI.** Ce dossier contient le moteur, un épisode complet rendu, et le mode d'emploi. Les trois
> captures de référence (`/tmp/arena-coding-uploads/Screenshot_20261024-*.png`) ne sont pas copiées :
> la grammaire est reprise (fond crème, trame de points, titres noir + accent orange, cartes punaisées
> avec 0 visiteurs, pastille bicolore à côté d'un personnage qui désigne), pas les images.

## 1 · Ce qu'il y a ici

| Fichier | Rôle |
|---|---|
| `reelkit.py` | le moteur : scènes, fond, cartes, pastilles, mascotte, barre de progression, encodage |
| `ep01/make_ep01.py` | l'épisode 01 : **6 beats, arc moderne, 24,3 s** — le scénario est **dans le code**, et la pièce déclare son **accroche** (`HOOK`) et son **jeu** (`TRUST`) |
| `ep01/ep01-v5.mp4` | **le master courant** : 1080×1920, 30 fps, H.264 + AAC, **24,80 s, avec voix, script conforme à la porte du récit** |
| `ep01/ep01-v4.mp4` | la v4 (24,50 s) — **le filet** : si la v5 déplaît à l'oreille, on republie celle-là |
| `ep01/ep01-v4-silent.mp4` | la même image sans son (pour reposer une autre voix sans refaire le rendu) |
| `ep01/ep01-v3.mp4` | la v3 (23,76 s, conseil gratuit, accroche « Votre cabinet existe ») — conservée comme trace |
| `ep01/ep01-v2.mp4` | la v2 (23,4 s, trois cimes, un souffle en `release2`) — conservée comme trace |
| `ep01/ep01-v1.mp4` | la v1 (21,4 s, sans voix, **arc classique**) — conservée comme trace, **ne pas publier** |
| `ep01/voice/` | les 6 clips de voix + `timing.json` (les durées réelles) + `build_timing.py` (la porte audio) |
| `ep01/voice.json` | le texte de la voix, beat par beat |
| `tools/qa/audit_reel.py` | **la porte de l'arc** — refuse un réel mal formé avant le rendu |
| `tools/qa/audit_trust.py` | **la porte du jeu** — refuse une pièce dont le rôle ne tient pas le score (`CONTENT-GAMES`, §3) |
| `tools/qa/audit_hook.py` | **la porte de l'accroche** — quatre mots obligatoires, échelle, pas de peur ni de promesse (`HOOKS`, §1–2) ; `--grid` vérifie la grille 331 |
| `tools/qa/audit_story.py` | **la porte du récit** — la scène, le lock-in, la preuve **prononcée**, le rehook, le CTA aligné (`CONTENT-CREATION` §3/§3 bis) |
| `ep01/poster.jpg` | la couverture — frame **2,2 s du master v4** pour la vignette |
| `ep01/frames/` | les captures de contrôle (inspection avant diffusion) — `v3-*` sont les six beats du master courant |
| `ep01/assets/mascot.png` | la mascotte — illustration générée, fond retiré par diffusion |

## 2 · Lancer

```bash
# deux dépendances seulement, sans apt (le paquet du bac est réinitialisé entre les sessions) :
pip install --break-system-packages pillow imageio-ffmpeg   # imageio-ffmpeg fournit le binaire ffmpeg

cd /home/user/AMK
python3 tools/qa/audit_reel.py content/reels/ep01/make_ep01.py            # ① la porte AVANT le rendu
python3 content/reels/ep01/voice/build_timing.py                          # ② mesurer la voix
python3 tools/qa/audit_hook.py content/reels/ep01/make_ep01.py            # ① l'accroche (4 mots, niveau)
python3 tools/qa/audit_trust.py content/reels/ep01/make_ep01.py           # ② la porte du jeu
python3 content/reels/ep01/make_ep01.py content/reels/ep01/ep01-v4.mp4    # ③ ≈ 30 s de rendu
python3 tools/ops/projection.py                                            # ④ la salle : http://0.0.0.0:8000/
```

**L'ordre n'est pas décoratif** : la porte lit `BEATS`, construit depuis `voice/timing.json`. Une voix trop
longue fait donc échouer la porte **avant** de brûler un rendu — et `build_timing.py` refuse une synthèse
muette (voir §4).

Si `ffmpeg` est déjà sur le `PATH`, il est utilisé ; sinon `imageio_ffmpeg.get_ffmpeg_exe()`.

## 3 · Le style, en six règles tenues par le code

| # | Règle | Où c'est codé |
|---|---|---|
| 1 | **Un beat = un mouvement de l'arc**, 6 beats, ≤ 25 s (règle V8 + `knowledge/STORY-ARC-2026-10-25.md`) | `build()` / `BEATS` |
| 2 | Fond **crème + trame de points**, jamais de photo | `Kit._base()` |
| 3 | **Titre noir, dernier mot orange** — un seul accent par écran | `headline()` / `s1_hook` |
| 4 | Cartes type **post-it punaisé**, une couleur par idée, entrée décalée de 0,25 s | `rounded_card()` |
| 5 | **Pastille bicolore** à côté de la mascotte : `cherchez vous-même`, `les trois manquent` | `pill()` |
| 6 | Mascotte **en bas, jamais au-dessus d'un texte** ; elle respire (± 6 px) et s'incline quand elle « parle » | `Mascot.draw()` |
| 7 | **L'arc moderne** : départ à 70, secousse entre 5 et 10 s, ≥ 3 cimes, un relâchement entre deux cimes, CTA = dernière cime (`knowledge/STORY-ARC-2026-10-25.md`) | `BEATS` + `tools/qa/audit_reel.py` |
| 8 | **Aucun glyphe hors Montserrat** : `✓` sort une boîte vide → la coche est **dessinée** | `draw_check()` |

⚠️ **Piège du dépôt, corrigé** : les quatre fichiers `content/assets/fonts/Montserrat-*.ttf` sont **le même
fichier variable** (744 936 octets chacun). Sans `set_variation_by_name`, PIL rend l'instance par défaut —
**Thin**. Le premier rendu sortait donc en maigre alors que le code demandait `ExtraBold`.
`reelkit.font()` demande l'axe ; ne pas le retirer.

## 4 · L'épisode 01 — « Votre patient tape opticien Akwa. » (v5, 24,80 s)

> **Reconstruit le 26/10 (tour 150)** après le **Roast Room** (`knowledge/ROAST-2026-10-26-SCRIPT-EP01.md`,
> verdict C, 8,1/10) et **sous la nouvelle porte du récit** (`tools/qa/audit_story.py`). La v4 était une
> bonne pièce **mal ordonnée** : elle ouvrait sur une consigne, ne relançait jamais au milieu, montrait
> « 12 avis » sans le prononcer, et donnait son meilleur cadeau à 18 s. La v5 corrige les quatre, et rien
> d'autre. **le lien : https://github.com/AKWOKING/AMK/blob/main/content/reels/ep01/ep01-v5.mp4**
> La v4 reste dans le dépôt (`ep01-v4.mp4`) comme filet — la condition de Buffett.

| Beat | Durée | La voix dit | L'écran montre | La cime | Rôle déclaré |
|---|---|---|---|---|---|
| **hook** | 0,00–5,00 | « Votre patient tape opticien Akwa. Il appelle l'un des deux. Pas vous. » | la recherche, **deux** résultats (coche verte / croix orange), puis la scène en trois lignes | 70 | `cas` |
| **spike1** | 5,00–9,67 | « Sa fiche : un site, douze avis. La vôtre : un nom. » | deux cartes : `SON SITE · 6 photos`, `SES AVIS · douze` — puis « La vôtre : **un nom.** » | **92** | `lockin+preuve` |
| **release1** | 9,67–13,33 | « Horaires et fiche : dix minutes, gratuit. » | « Dix minutes. **Gratuit.** » et la coche | 58 | `corps` |
| **spike2** | 13,33–16,53 | « Ce n'est pas le site. Il veut venir ce soir. » | « Ce n'est pas **le site.** » barré, puis « Il veut venir **ce soir.** » et le sceau « 22 h · le cabinet est fermé » | **88** | `rehook+corps` |
| **release2** | 16,53–21,61 | « Un site répond à 22 heures. Horaires, adresse, WhatsApp. » | « **à 22 h 00.** » puis la carte verte, la coche et « Une seule page. Une seule réponse. » | 60 | `corps` |
| **cta** | 21,61–24,80 | « Écrivez APERÇU sur WhatsApp. » | `APERÇU` en grand, le numéro, « 10 minutes cette semaine » | **95** | `sortie` |

**Les quatre portes, et ce qu'elles disent de la v5** : `✓ récit · 24,8 s · 6 beats` (cas, lock-in,
preuve dite, rehook, sortie alignée — **zéro avertissement**) · `✓ accroche niveau 3 · 4/4 mots · 12 mots`
(⚠ `sans-intrigue`) · `✓ rôle 24,8 s · 20/125 · plancher 12` · `✓ arc 6 beats · 3 cimes`.

**Ce qui a changé entre les trois versions** — et pourquoi :

| | v1 (20:25) | v2 (21:45) | v3 (22:35) | v4 (23:40) | **v5 (26/10)** |
|---|---|---|---|---|
| ouverture | carton de titre, **à zéro** | on est **déjà** dans l'écran de recherche | idem | idem, **deux** résultats — le contraste est montré |
| accroche | carton | « Votre cabinet existe. Votre site, non. » | idem | **« Tapez votre nom sur Google : il appelle les autres, pas vous. »** |
| mots de puissance | — | 2 / 4 (sujet, contraste) | 2 / 4 | **4 / 4** |
| échelle | — | niveau 1 (Reporter) | niveau 1 | **niveau 3** (Fortuneteller) |
| pics | **un seul** (le CTA final) | **trois** (5,0 · 12,7 · 20,2 s) | trois, resserrés par la voix | trois (5,00 · 12,81 · 20,68 s) |
| voix | aucune | 6 clips | `release2` n'est plus muet | 6 clips, accroche re-synthétisée **trois fois** pour tenir en 5 s |
| `release2` | décorative | **souffle** muet | **le conseil gratuit** | inchangé |
| utilité (jeu 5) | 2 | 3 | 4 | 4 |
| durée | 21,4 s | 23,4 s | 23,76 s | **24,76 s** |
| vérification | aucune | `audit_reel` | + `audit_trust` (20/125) | + `audit_hook` (4/4) | **+ `audit_story`** (la porte du récit) |
| ouverture | carton | recherche | un résultat | **deux** résultats + consigne | **une scène : le patient tape** |
| rehook | — | — | — | — | **oui (« ce n'est pas le site »)** |
| preuve dite | — | — | — | non (à l'écran seulement) | **« douze avis »** |
| cadeau | — | — | 18 s | 18 s | **9,7 s** |

**La voix** : `voice-03` (masculine, registre publicitaire), français, synthèse du 25/10. Les six clips sont
dans `ep01/voice/`, les durées mesurées dans `timing.json`. **Le beat s'allonge jusqu'à la voix, jamais
l'inverse** — et si le total dépasse 25 s, `build_timing.py` ferme la porte en nommant le beat à
raccourcir.

**Pourquoi `release2` est passé du souffle au conseil** : le jeu 5 paie la **confiance**, et la formule est
`minutes × pertinence × utilité` (`knowledge/CONTENT-GAMES-2026-10-25.md`, §3). Un relâchement muet laisse
la pertinence intacte mais **l'utilité à zéro** : le spectateur n'a rien emporté. Trois lignes vraies — les
horaires se publient en dix minutes, la fiche se réclame, l'avis ne se fabrique pas — suffisent à ce qu'il
reparte avec quelque chose, et à ce que la seule ligne qui reste à acheter soit la nôtre.

### Un défaut trouvé en vérifiant, et ce qu'il a appris

Le premier clip de `release2` (« Un aperçu, à votre nom. ») a été **généré sans erreur** — 9 549 octets,
2,33 s — et il est **muet** : RMS 0,003 au lieu de 0,096 pour les cinq autres. Un fichier qui existe n'est
pas un fichier qui parle. `build_timing.py` mesure donc le **niveau** de chaque clip et refuse la synthèse
muette ; en v2, `release2` est devenu un **souffle déclaré** (`SOUFFLE = {"release2"}`), c'est-à-dire un
silence **voulu** et non un trou.

**En v3, le silence a été supprimé, pas toléré** : `SOUFFLE` est vide, les six beats parlent. Un silence
déclaré est une dette de contenu — il occupe 2,3 s de l'attention et ne rend rien. La règle reste :
*un beat muet est un choix à justifier par écrit, et le meilleur choix est de lui écrire une phrase*.

### Ce que l'épisode ne fait pas — et c'est volontaire

- **Aucun chiffre de résultat** : pas de « +X % d'appels », pas de « 3× plus de visites ». Le seul chiffre
  est `677 78 96 31`, notre numéro.
- **Aucun nom de client**, aucun nom de concurrent : les neuf fiches sont génériques.
- **Aucune promesse de mesure** (ruling 142) : on ne dit pas ce que la fiche laisse filer, on montre ce
  qu'elle **n'a pas**.
- **Aucune mention d'IA** (ruling King 11/10) : l'épisode ne raconte pas comment il est fait.
- **Pas de visage, pas de sous-titre automatique** : la voix est **synthétique** (`voice-03`) et le texte
  est **écrit** (ruling 11/10). Aucune image de King, aucune personne réelle à l'écran.
- **Aucune demande de vues** : la pièce est une **porte** (score 20/125). Elle n'essaie pas d'être
  partagée, elle essaie d'être comprise par l'opticien de Douala qui la voit une fois.

**Pourquoi le script a été reconstruit (v5)** : la v4 passait quatre portes et restait faible à
l'oreille — King l'a dit avant les portes. Le Roast Room a nommé les quatre causes, chacune adossée à
une règle que le dépôt **écrivait déjà sans la vérifier** : pas de scène (`CONTENT-CREATION` §3, temps 1),
pas de rehook (§3 bis), preuve montrée mais jamais dite (temps 4), cadeau enterré (§3 bis, principe 4).
`tools/qa/audit_story.py` transforme ces quatre règles en refus. Une règle sans porte = un trou.

**Pourquoi l'accroche a été refaite (v4)** : `knowledge/HOOKS-2026-10-25.md` §1 dit qu'un hook porte
quatre mots obligatoires — sujet, action, objectif, contraste. La v3 en avait deux : elle **constatait**
(« votre site, non ») sans donner ni geste ni résultat. Le spectateur ne pouvait rien en faire. La v4
ouvre sur un geste de dix secondes qu'il peut exécuter immédiatement (« tapez votre nom »), sur un
résultat annoncé (« il appelle les autres ») et sur le contraste qui le concerne (« pas vous »).

**Et la contrainte qui a décidé de la formulation** : l'arc plafonne le contexte à **5 s**
(`audit_reel.py`). Une première version en 23 mots durait **8,03 s** ; une deuxième en 15 mots, **5,27 s** ;
la version retenue fait **5,00 s pile**. On a raccourci **le texte trois fois** — jamais la voix, jamais
le plafond. Le résultat est plus dur : huit mots utiles au lieu de vingt-trois.

## 5 · La file d'attente (même arc, même moteur, même voix)

| # | Sujet (playbook §2) | Accroche | État |
|---|---|---|---|
| EP01 | **T2** | « Tapez votre nom sur Google : il appelle les autres, pas vous. » | ✅ **v4 rendue — accroche 4/4, niveau 3, porte 20/125, case 3 de la grille 331** |
| EP02 | **B1** | « Une fiche Google complète, à quoi ça ressemble » — la fiche DM Optique, trois captures | à écrire |
| EP03 | **M5** | « 3 questions avant de payer un site » | à écrire |
| EP04 | **T7** | « Deux accueils, même cabinet » — deux écrans côte à côte | à écrire |
| EP05 | **B5** | « J'ouvre deux aperçus cette semaine » | à écrire |

Un épisode = un fichier `epNN/make_epNN.py` de 150 lignes, cinq fonctions `s1..s5`. Aucun montage, aucune
timeline à maintenir : **le code est le montage**.

## 6 · Porte avant diffusion (§7 du playbook, version vidéo)

- [ ] `python3 tools/qa/audit_story.py content/reels/epNN/make_epNN.py` → **✓** (scène, lock-in, preuve dite, rehook, CTA aligné)
- [ ] `python3 tools/qa/audit_hook.py content/reels/epNN/make_epNN.py` → **✓** (4 mots obligatoires, échelle déclarée)
- [ ] `python3 tools/qa/audit_hook.py --grid content/ideas/GRID-331-*.md` → **✓** (la case existe dans la grille)
- [ ] `python3 tools/qa/audit_ideas.py content/ideas/SHORTLIST-YYYY-MM-DD.md` → **✓** (la pièce a une
      ligne de lot : tuyau, preuve, cible, briques — `knowledge/IDEA-PIPES-2026-10-25.md`)
- [ ] `python3 tools/qa/audit_trust.py content/reels/epNN/make_epNN.py` → **✓** (le rôle tient son plancher)
- [ ] `python3 tools/qa/audit_reel.py content/reels/epNN/make_epNN.py` → **✓** (6 règles de l'arc)
- [ ] durée ≤ 25 s et lisible **sans son** (le texte porte l'histoire, la voix la double)
- [ ] un seul accent orange par écran, aucun texte sous 30 px
- [ ] aucun chiffre qui ne soit pas daté et sourcé dans ce README
- [ ] aucun nom de client sans accord écrit
- [ ] le master est inspecté en captures (`frames/`), pas seulement en lecture rapide
- [ ] la voix est **audible là où elle doit l'être** : RMS mesuré par beat (`build_timing.py`)
- [ ] le tuyau de l'idée est **écrit** : un original (tuyau 6) se déclare, il ne se déguise pas en outlier
- [ ] King publie — l'agent ne publie jamais
