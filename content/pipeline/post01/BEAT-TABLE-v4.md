# POST-01 v4 — Avatar motion-comic · table des beats (31 s)

Source de rendu : `content/pipeline/post01/index-v4.html` · composites figés : `content/Avatar/_composites/composite-<état>.png` (1080×1920, approuvés King).
Registre : motion-comic. Pas d'animation de personnage (clignement, lèvres, respiration) : chaque changement d'état est un **changement de composite** (fondu enchaîné 250 ms, §9 : 200–320 ms). Pas de zoom, pas de panoramique.

| Beat | Temps | Composite | Overlay (gras, zone 0–340 css) | Légende (petite) | Transition | Ligne VO |
|---|---|---|---|---|---|---|
| B1 | 0–3,2 s | IDLE (0–2,2 s) → SURPRISED (2,2–3,2 s) | « Tu vois pourquoi ? » (0–2,2) · « Un nouveau logo. » (2,2–3,2) | « Le logo du site a disparu. » (0–3,2) | coupe sur SURPRISED à « disparu » (2,2 s ; le mot démarre à 2,03 s dans la VO calée à 0,2 s), fondu 250 ms | « Le logo du site a disparu. » |
| B2 | 3,2–7 s | TALKING | « On l'intègre. Et là… rien. » (3,2–7) | « 2 jours bloqué sur ça. » (3,2–7) | fondu 250 ms à 3,2 s | « 2 jours bloqué sur ça. » |
| B3 | 7–12 s | THINKING | « On enlève le masque. » (7–9) → « Faux. » (9–12) | « C'est pas le rognage. » (7–12) | fondu 250 ms à 7,0 s | « C'est pas le rognage. » |
| B4 | 12–21 s | SURPRISED (12–15 s) → APPROVING (15–21 s) | « Un disque invisible. » (12–21) | « L'anneau était un disque plein. Peint par-dessus. » (12–21) | fondus 250 ms à 12,0 s et 15,0 s | « L'anneau était un disque plein. Peint par-dessus. » |
| B5 | 21–27 s | POINTING | « Le fix : creuser l'anneau. » (21–27) | « Un vrai anneau. Logo au-dessus. » (21–27) | fondu 250 ms à 21,0 s | « Un vrai anneau. Logo au-dessus. » |
| B6 | 27–31 s | APPROVING | — | « Le détail qu'on voit pas, c'est celui qui casse tout. » (27–31) | fondu 250 ms à 27,0 s | « Le détail qu'on voit pas, c'est celui qui casse tout. » |

## Règle de légende / VO (option A, appliquée)
La légende est exactement la ligne VO, mot pour mot. L'overlay est à l'écran seulement, jamais lu.

## Ambiance (ruling King)
Vapeur (3 traits, opacité seule, cycle 3 s) et lueur (opacité 0,97–1,00, cycle 5 s) pilotées par `seek(t)`, calque au-dessus du personnage. Limite constatée : la vapeur est crème sur chemise crème, presque invisible ; elle ne suffit pas à passer la porte de mouvement.

## Règles
- **Texte :** entrée 200 ms, opacité + translateY 18 px → 0 (ease-out). Aucun texte n'entre depuis scale(0).
- **VO :** la ligne VO de chaque beat est la légende du beat ; à défaut de légende, l'overlay. Les overlays sans légende (« Un nouveau logo. », « On enlève le masque. », « Faux. », « Un disque invisible. », « Le fix : creuser l'anneau. ») restent à l'écran, non lus.
- **Calage VO (voice-04) :** B1 à 0,2 s (durée 2,93 s) · B2 à 3,2 s (1,78 s) · B3 à 7,2 s (1,57 s) · B4 à 12,2 s (4,26 s) · B5 à 21,2 s (3,03 s) · B6 à 27,2 s (3,53 s). Chaque clip finit dans son beat. Le mot « disparu » est repéré par détection de silence (début ≈ 2,03 s dans le clip), pas par alignement mot à mot : à réécouter.
- **Bouclage :** B6 finit sur APPROVING ; pas de logo de marque à l'écran dans cette version (aucun nom n'est affiché).
- **Hors v4 :** pas de rendu vidéo complet, pas de publication avant validation King.

## Mise à jour — passage de la porte de mouvement (version finale)
- **Légendes = VO mot pour mot, découpées au temps de la VO :** B1 « Le logo du site a disparu. » (0–3,2 s) · B2 « 2 jours bloqué sur ça. » (3,2–7 s) · B3 « C'est pas le rognage. » (7–12 s) · B4 « L'anneau était un disque plein. » (12–16 s) puis « Peint par-dessus. » (16–21 s) · B5 « Un vrai anneau. » (21–24 s) puis « Logo au-dessus. » (24–27,2 s) · B6 « Le détail qu'on voit pas, » (27,2–28,4 s) puis « c'est celui qui casse tout. » (28,4–31 s).
- **Overlays = titres de chapitre, à l'écran seulement :** « Tu vois pourquoi ? » · « Un nouveau logo. » · « On l'intègre. » · « Et là… rien. » · « On enlève le masque. » · « Faux. » · « Un disque invisible. » (12–14,5 s, puis 18,5–21 s) · « Le fix : creuser l'anneau. » (21–23 s).
- **Pauses VO :** B4, B5 et B6 sont générées en deux morceaux (voice-04), recollés avec silence au calage ci-dessus. Les mots sont inchangés.
- **Vie continue (porte de mouvement) :** grain de pellicule recalculé à chaque image (blocs 4×4 px, opacité 5 %) · vapeur gris #6E6E6E · lueur 0,94–1,00 (cycle 5 s) · 9 particules de poussière (opacité 15–18 %, dérive 10–12 s) · respiration 3 px, vers le bas seulement (le bas du buste reste sous le bureau).
- **Légende :** 36 px (lisibilité 1080×1920).
- **Porte de mouvement :** 15/15 fenêtres OK (plus petite valeur max 1,65 à 10–12 s).
