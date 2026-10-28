# LA FABRICATION DE « LA MONTURE CHERCHE SON NOM » (épisode 1, H08) — tout ce qui a été traversé

```
Pièce      clients/dm-optic/content/month1/w3/assets/monture-01-h08-voix.mp4 — 29,53 s, 1080×1920
Publiée    mardi 27/10/2026 à 17 h 48 — Facebook et TikTok (King)
Tours      194 → 200, six tours de fabrication, une publication
Portes     audit_story · audit_hook · audit_video_motion (--calme) · audit_post_dm · banc 35/35
Ce doc     pourquoi il existe : King, 27/10 — « document all we went through to make this video so
           that we don't repeat these errors ». C'est un registre d'erreurs, pas un récit de réussite.
Écrit      27/10/2026, après publication
```

## 0 · En trente secondes

**Vingt et une erreurs**, dont **onze** ont coûté un rendu complet (≈ 30 s de machine chacune, mais surtout
un tour de plus), et **cinq** auraient pu partir en publication sans qu'on les voie si aucune porte ne les
avait attrapées. Elles se rangent en quatre familles, et c'est la famille qui se corrige, pas l'erreur :

| Famille | Combien | Ce qu'elle coûte | Ce qui la prévient aujourd'hui |
|---|---|---|---|
| **Matière fausse ou incomplète** (capture avec raccord, compteur de filtre pris pour un total, 65 au lieu de 40) | 4 | un plan refait, un chiffre faux évité de justesse | `trim_seam()` automatique · le chiffre se **compte** dans `hosting/previews/dmoptic/montures/` |
| **Durées non mesurées** (durées de repli périmées, cache de clips, silences de 1 s, `ease` en fin de plan) | 5 | 6 rendus, un film à 33 s au lieu de 29 | la voix mesure, la porte `--calme` mesure, `measure_clips()` rogne les respirations |
| **Texte posé sur l'interface** (bandeau sur le bouton vert, bandeau translucide sur du blanc, carton de vote illisible) | 4 | 3 rendus, des dizaines d'images de contrôle | `fiche_card()` (page posée dans le cadre) · bandeau opaque · cartons dessinés |
| **Règles maison non lues avant d'écrire** (« suivez la page », « abonnez-vous », CTA sans récompense, série sans boucle) | 4 | 4 reprises de kit | les portes refusent, et elles citent la règle (`abonnement-mendicite`, `cta-sans-recompense`, `serie-sans-boucle`) |
| **Outillage supposé présent** (PIL, numpy, ffmpeg, Chromium) | 4 | une session sans portes, deux relances | `bash tools/video/install.sh` · venv · **ne jamais supposer** |

## 1 · La chronologie, tour par tour

| Tour | Ce que King a demandé | Ce qui a été livré | Ce qui a été appris |
|---|---|---|---|
| **194** | « une série sans le docteur, sans visage » | muet 14,20 s, monture + cartes | la matière est **déjà au dépôt** : une photo de monture et les fiches du site suffisent |
| **195** | « add voice » | parlé 19,87 s, `voice-05` | **la voix ne se comprime pas** : c'est le montage qui se cale sur les durées mesurées |
| **196** | « une histoire derrière le nommage, des jeux, des sondages » | v3, 6 beats, jeu en 3 manches | une pièce peut passer **quatre portes** et rester faible : il manquait la porte du **récit** |
| **197** | « votre monture n'est pas la leur » + trois scripts | v4, vote A/B, cadence mardi/vendredi | les trois scripts de King échouent aux **quatre mêmes** points : c'est une lacune de **structure** |
| **198** | « ajoute des images » | v5 : catalogue, visage généré, fiche | une capture pleine page **n'est pas une image** (raccord) ; `--mode scroll` est un piège |
| **199** | « humanizer + roast room, remove all the motion design » | v6 : film calme, texte humanisé | la porte du mouvement mesurait le **mouvement**, pas le **rythme** |
| **200** | « final script » | v7 : le sien, appliqué | sa condition (« 40 montures seulement si c'est dit ») était **la bonne règle** |

## 2 · Le registre des erreurs — les onze qui ont coûté un rendu

| # | L'erreur | Comment on l'a vue | Le correctif | Ce qui l'empêche de revenir |
|---|---|---|---|---|
| 1 | **« 65 montures »** alors que le site en publie **40** (65 = nombre de photos dans le dossier) | comptage des fiches dans `hosting/previews/dmoptic/montures/` avant rendu | « 40 montures, 40 codes » | le chiffre se compte, il ne s'estime pas ; `audit_story` exige une preuve **prononcée** |
| 2 | **Un carton unique tenu 6,7 s** sur une macro : fenêtre figée à 9–10 s | `audit_video_motion --window 1` | beat long découpé en 2–3 plans | règle écrite dans le moteur : *un beat long se découpe toujours* |
| 3 | **Capture pleine page avec raccord** : Chromium réimprime le haut de la page (8 190 px catalogue, 2 225 px fiche) | comparaison de la bande du haut avec le reste de l'image | coupe **avant** le raccord | `trim_seam()` le détecte et le dit à chaque rendu |
| 4 | **Défilement en `ease` pur** : la page ralentit et s'arrête en fin de plan (fenêtre 22–23 s figée) | même porte, fenêtre 1 s | **55 % ease + 45 % linéaire** | la fonction le dit : *une page qui ralentit s'arrête* |
| 5 | **Bandeau de texte sur le bouton vert** de la fiche (fond clair + bandeau translucide) | images de contrôle, relues une par une | la fiche est **posée dans le cadre**, sur le marine ; bandeau opaque à 248/255 | `fiche_card()` : le texte ne marche jamais sur un bouton |
| 6 | **Durées de repli périmées** dans la version muette : une image tenait 3,2 s | `audit_video_motion --calme` (bloquant) | les durées de repli **sont** les durées mesurées de la voix | une version muette n'est pas une version sans montage |
| 7 | **Cache `.net.wav`** : les durées mesurées venaient des anciens clips | incohérence entre le texte et la durée du beat | `rm -f /tmp/voixI/*.net.wav` avant chaque mesure | noté dans les deux documents de tour |
| 8 | **Silences internes de 1 s** chez `voice-06` : le même texte donnait 33 s | mesure des trous dans le clip (analyse PCM 100 ms) | respirations ramenées à **0,20 s** (montage radio, débit intact) | `measure_clips()` filtre les silences internes |
| 9 | **Trou noir de 0,28 s entre deux beats** (coupe sur le noir) | relecture des images de contrôle | l'image du dernier plan tient pendant la respiration | `frame()` garde le plan précédent |
| 10 | **Aucune image générée autorisée**, puis **une** autorisée | règle maison (`BRAND` §8/§12) | exception écrite, datée, bornée, **et finalement non utilisée** au tour 200 | une exception s'écrit ; elle ne se pratique pas en silence |
| 11 | **`--mode scroll` impose sa durée** (4 455 px ÷ 700 px/s = 7,4 s) : 221 images ingérables | essai, puis abandon | capture `--mode full` + fenêtre programmatique | la bonne matière est **une** image, pas un rush |

## 3 · Les cinq que les portes ont attrapées — et qui seraient parties sans elles

| # | Ce qui allait sortir | La porte | Ce qu'elle a dit |
|---|---|---|---|
| 12 | « Suivez DM Optique », « Abonnez-vous », « Suis la page » | `audit_post_dm` / doctrine | `abonnement-mendicite` : **demander un abonné n'en produit pas** — c'est une raison de revenir qui en produit un |
| 13 | Un CTA qui nomme l'action sans dire ce qu'on reçoit | `audit_story` | `cta-sans-recompense` : ajouter ce que le spectateur obtient |
| 14 | Un kit qui déclare une série **sans promettre de suite** (ma légende raccourcie avait coupé « la suite ») | `audit_post_dm` | `serie-sans-boucle` : sans boucle ouverte, une série ne fait pas revenir |
| 15 | L'accroche de King sans sujet, action, objectif, contraste | `audit_hook` | `mots-manquants` : 4 mots obligatoires |
| 16 | Une preuve **montrée** (le catalogue) mais **jamais prononcée** | `audit_story` | `preuve-muette` : un fait qu'on ne dit pas n'existe pas pour qui écoute au volant |

## 4 · Les quatre erreurs d'outillage, et ce qu'elles ont coûté

| # | L'erreur | Coût | La règle |
|---|---|---|---|
| 17 | `capture.mjs --mode full` qui échoue **juste après** un autre appel Chromium (`FileNotFoundError`) | deux relances, deux fausses alertes « page cassée » | relancer **seule**, une fois, avant de conclure |
| 18 | un helper inexistant appelé dans le moteur (`beat_page_key`) | un rendu perdu | ne jamais citer une fonction qu'on n'a pas lue |
| 19 | `/tmp` vidé entre deux sessions : Chromium, PIL, numpy, ffmpeg disparus | une session sans portes (ce tour-ci) | `bash tools/video/install.sh` + venv Python, **au début** de chaque session de vidéo |
| 20 | 10 clips de synthèse par tour, plafond atteint | une phrase **coupée** en cours de route (« quarante codes » dite, « H02, H04, H05 » perdue) | compter les clips **avant** d'écrire les phrases ; une phrase = un clip court |
| 21 | le bandeau `header` du site collé en haut de chaque capture | une image de contrôle trompeuse | masquer `header`/`dock` **avant** la capture, jamais après |

## 5 · Ce que la chaîne de portes a changé, au fond

Trois portes ont été **complétées** pendant cette série, jamais désarmées :

1. **`audit_video_motion --calme`** (tour 199). L'ancienne règle — « une fenêtre figée = diaporama » —
   bloquait un film volontairement immobile (9 fenêtres à 1 s). La nouvelle règle du mode calme est une
   règle de **tenue** : *aucune image ne tient plus de 2,6 s sans un changement*. Résultat mesuré sur les
   deux fichiers : **2,33 s max, 19 changements**.
2. **`trim_seam()`** (tour 201, ce tour). Ce qui était une mesure manuelle (8 150 px, 2 200 px) est devenu
   une détection automatique, qui **imprime** le raccord trouvé. Le jour où une capture changera, on le
   saura au lieu de le découvrir en publication.
3. **`measure_clips()`** (tour 199). Il ne rogne plus seulement la tête et la queue : il ramène les
   respirations internes à 0,20 s. Le débit ne change pas — les trous, si.

## 6 · Le coût réel, pour la prochaine fois

| Poste | Quantité | Remarque |
|---|---|---|
| Rendus vidéo complets | **21** (6 en 197–198, 5 en 199, 10 en 200) | 4 seulement étaient des livrables ; **17** étaient des corrections |
| Clips de synthèse | **16** (6 `voice-05`, 6 `voice-06`, 4 refaits) + **2 auditions** | dont 3 refaits pour une seule phrase trop longue |
| Captures de site | 6 (catalogue ×3, fiche ×2, héros ×1) | 2 ont fini au film |
| Images générées | 1 (`visage-h08.jpg`) | **non utilisée** dans la version publiée |
| Documents produits | 1 script, 1 kit, 2 séances/docs de leçon, 2 entrées de journal | — |

**La leçon de coût** : sur 21 rendus, **17** viennent de trois causes seulement — durées non mesurées,
texte posé sur de l'interface claire, matière non vérifiée. Ce sont les trois choses qu'une **relecture
d'images de contrôle avant le rendu** attrape en 30 secondes.

## 7 · La liste de contrôle, avant de rendre (à appliquer telle quelle à l'épisode 2)

1. **Les chiffres** : chacun est compté dans `hosting/previews/dmoptic/montures/`, pas estimé.
2. **Les captures** : `header`/`dock` masqués ; `trim_seam` a imprimé son raccord (ou son absence).
3. **Le texte** : aucun carton ne tombe sur un bouton, un prix ou un lien de la page capturée.
4. **Les durées** : la version muette utilise **les durées mesurées**, pas les valeurs de repli.
5. **Les respirations** : aucun silence interne de plus de 0,3 s ; aucun trou noir entre deux beats.
6. **Les clips** : moins de 10 par tour, une phrase courte par clip.
7. **Le mouvement** : `--calme` avant de rendre, pas après.
8. **Les portes** : `audit_story`, `audit_hook`, `audit_post_dm`, banc — dans cet ordre, et **avant** le kit.
9. **Le kit** : le tableau « ce qui a bougé et pourquoi » est rempli (§10 du kit).
10. **Les images de contrôle** : 12 à 15 images relues **une par une**, pas une planche d'un coup d'œil.

## 8 · Ce qui n'a jamais été vérifié, et qui reste au-dessus de cette série

- **La H08 est-elle encore au cabinet ?** Le site la publie ; personne ne l'a confirmée cette semaine.
- **Les horaires** (8h30–13h00, lundi–samedi) : publiés par le cabinet, non reconfirmés.
- **La cadence** suppose que King publie mardi et vendredi. Le vendredi 30/10 n'a **pas** de pièce prête.
- **Aucun chiffre de performance n'existe encore** : la vidéo est en ligne depuis 17 h 48. Tout ce que le
  dépôt dit de son effet est une **cible**, pas une mesure.
