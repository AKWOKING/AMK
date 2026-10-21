# Vidéo 01 — « Ce que voit quelqu'un qui n'est jamais venu »

```
Fichier   etapes-01.mp4 · 31,0 s · 1080×1920 · 30 fps · 11,6 Mo
Voix      voice-01 (narration FR), 8 phrases posées à la seconde
Montage   tools/record/make_dmoptic_etapes.py
Images    vraies photos du cabinet + 4 visuels d'étape générés (mention « illustration »)
Portiques mouvement OK · affirmations OK
```

---

## 1 · Ce que ce film applique

Chaque choix renvoie à une règle écrite, pas à un goût.

| Choix | Règle d'origine |
|---|---|
| **Une seule idée** : l'examen se fait en quatre étapes, dans cet ordre | Kallaway — une vidéo = une idée ; capture IG — cesser d'être connu pour douze choses |
| **8 plans au lieu de 15**, chacun tenu 3,4 à 5,4 s | Kallaway — le texte doit rester ≥ 3 s à l'écran |
| **Texte découplé de l'image** : le carton ne disparaît plus avec le plan | Diagnostic des trois rendus précédents (`HOOKS-ET-VIRALITE` §2) |
| **Le flou se résout sur le plan 1** | Hook visuel, catégorie ② (pattern interrupt) — le *freeze* d'ouverture |
| **Le visuel rompt, le texte nomme, la voix ajoute la cause** | Kallaway — triple hook aligné |
| **Le lock-in pose la preuve** (quatre étapes, praticien unique) | Kallaway — *trust anchor* dans les 5–10 s qui suivent le hook |
| **Sous-titres brûlés** | Masterclass Ocuco — les clips doivent fonctionner sans son |
| **Une demande unique, sans prix** (WhatsApp) | Contrainte 2 du dossier + capture IG (« demander ») |
| **Paiement en plusieurs fois + livraison** en carte de fin | Autorisation explicite du client, 21/10 |
| **« simulation approximative » / « illustration »** à l'écran | Règle d'honnêteté du §11 bis |

---

## 2 · La structure

| Temps | Rôle | Image | Texte | Voix |
|---|---|---|---|---|
| 0–3,4 | Hook | intérieur réel, **flou → net** | Ce n'est pas / une photo floue. | « C'est ce que voit quelqu'un qui n'a jamais fait mesurer ses yeux. » |
| 3,4–6,8 | Lock-in | macro du phoroptère | Quatre étapes. / Aucune ne se saute. | « Ça ne se règle pas tout seul. Ça se mesure. » |
| 6,8–10,4 | Étape 1 | *illustration* : le bureau, l'écoute | **1 · On écoute** / ce que vous n'arrivez plus à voir | « D'abord : ce que vous n'arrivez plus à voir. » |
| 10,4–14,0 | Étape 2 | *illustration* : l'autoréfractomètre | **2 · On mesure** / le bilan optique | « Ensuite, le bilan optique. » |
| 14,0–17,6 | Étape 3 | *illustration* : l'échelle, le cache-œil | **3 · On lit** / les acuités, œil par œil | « Puis les acuités, un œil après l'autre. » |
| 17,6–21,2 | Étape 4 | *illustration* : la monture d'essai | **4 · On réfracte** / la correction qui en sort | « Enfin la réfraction : elle donne la correction. » |
| 21,2–25,6 | Preuve | **vraie photo** : le praticien au travail | C'est lui / qui fait l'examen. / Laquintinie · Kumba · Bethesda | « C'est le même praticien, du début à la fin. » |
| 25,6–31,0 | Demande | carte de fin, vitrine entière | Écrivez-nous / avant de venir. + WhatsApp + paiement échelonné | « Écrivez-nous avant de venir. » |

**La preuve est placée après les quatre étapes, pas avant.** Le spectateur a d'abord vu ce qu'est l'examen ; il apprend ensuite qui le fait. L'inverse aurait été une accréditation sans contenu.

---

## 3 · Ce que le film ne fait pas

- aucun prix, aucune remise, aucun cadeau ;
- aucun nombre de montures en stock ;
- aucun témoignage, aucun avis, aucune note ;
- aucune statistique de résultat, aucune promesse de guérison ;
- aucun concurrent nommé ;
- aucun visage de patient identifiable — les visuels d'étape sont cadrés pour cela.

---

## 4 · Contrôles passés

```
python3 tools/qa/audit_video_motion.py …/etapes-01.mp4
  → VERDICT : OK — mouvement présent dans chaque fenêtre (0 fenêtre figée)

python3 tools/qa/audit_claims.py …/w2
  → VERDICT : OK

Audio : 31,0 s · crête −2,0 dBFS · voix continue de 0 à 28 s
```

---

## 5 · Publication

**Où** : TikTok (`@dmoptique.bonaberi237`) et Facebook. Puis en **Statut WhatsApp**, qui est le vrai canal de conversion ici — mais il ne touche que les contacts qui ont enregistré le numéro.

**Légende proposée** (à valider) :

> Ce n'est pas une photo floue. C'est ce que voit quelqu'un qui n'a jamais fait mesurer ses yeux.
>
> L'examen se fait en quatre temps : on écoute, on mesure, on lit les acuités œil par œil, on réfracte. Et c'est le même praticien du début à la fin.
>
> Écrivez-nous sur WhatsApp avant de venir, on vous dit quoi prévoir.
>
> *Simulation approximative. Visuels d'étape : illustration.*

**Réponse-type aux commentaires** (« combien ? », « c'est où ? ») : renvoyer vers WhatsApp, ne jamais chiffrer en public. Une réponse courte, toujours la même, pour que le compte reste prévisible.

**Les quatre nombres à relever à 48 h** : vues à 3 s · rétention à 10 s · conversations WhatsApp ouvertes · contacts ayant enregistré le numéro.

---

## 6 · Ce qui reste ouvert

1. **Le rendu des visuels générés.** Ils sont cohérents entre eux mais plus lumineux que les vraies photos. Si le client préfère, on refait les quatre plans d'étape avec ses propres prises de vue — le montage ne change pas.
2. **Le plan « preuve »** coupe le haut du crâne du praticien : c'est dans la photo d'origine, pas un choix de cadrage.
3. **La série.** Ce film est le numéro 1 d'un format répétable : même ouverture (une image qui se résout), même promesse (quatre étapes), même demande. Le numéro 2 peut prendre n'importe quel symptôme — les phares la nuit (H5), le tableau au fond de la classe, l'écran à 40 cm (H10).
