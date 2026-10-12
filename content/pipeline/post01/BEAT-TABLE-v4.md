# POST-01 v4 — Avatar motion-comic · table des beats (31 s)

Source de rendu : `content/pipeline/post01/index-v4.html` · composites figés : `content/Avatar/_composites/composite-<état>.png` (1080×1920, approuvés King).
Registre : motion-comic. Pas d'animation de personnage (clignement, lèvres, respiration) : chaque changement d'état est un **changement de composite** (fondu enchaîné 250 ms, §9 : 200–320 ms). Pas de zoom, pas de panoramique.

| Beat | Temps | Composite | Overlay (gras, zone 0–340 css) | Légende (petite) | Transition | Ligne VO |
|---|---|---|---|---|---|---|
| B1 | 0–3,2 s | IDLE (0–2,2 s) → SURPRISED (2,2–3,2 s) | « Le logo du site a disparu. » (0–2,2) · « Un nouveau logo. » (2,2–3,2) · hook « Tu vois pourquoi ? » (1–3,2) | — | coupe sur SURPRISED à « disparu » (2,2 s ; le mot démarre à 2,03 s dans la VO calée à 0,2 s), fondu 250 ms | « Le logo du site a disparu. » |
| B2 | 3,2–7 s | TALKING | « On l'intègre. Et là… rien. » (3,2–7) | « 2 jours bloqué sur ça. » (3,2–7) | fondu 250 ms à 3,2 s | « 2 jours bloqué sur ça. » |
| B3 | 7–12 s | THINKING | « On enlève le masque. » (7–9) → « Faux. » (9–12) | « C'est pas le rognage. » (7–12) | fondu 250 ms à 7,0 s | « C'est pas le rognage. » |
| B4 | 12–21 s | SURPRISED (12–15 s) → APPROVING (15–21 s) | « Un disque invisible. » (12–21) | « L'anneau était un disque plein. Peint par-dessus. » (12–21) | fondus 250 ms à 12,0 s et 15,0 s | « L'anneau était un disque plein. Peint par-dessus. » |
| B5 | 21–27 s | POINTING | « Le fix : creuser l'anneau. » (21–27) | « Un vrai anneau. Logo au-dessus. » (21–27) | fondu 250 ms à 21,0 s | « Un vrai anneau. Logo au-dessus. » |
| B6 | 27–31 s | APPROVING | « Le détail qu'on voit pas, c'est celui qui casse tout. » (27–31) | — | fondu 250 ms à 27,0 s | « Le détail qu'on voit pas, c'est celui qui casse tout. » |

## Règles
- **Texte :** entrée 200 ms, opacité + translateY 18 px → 0 (ease-out). Aucun texte n'entre depuis scale(0).
- **VO :** la ligne VO de chaque beat est la légende du beat ; à défaut de légende, l'overlay. Les overlays sans légende (« Un nouveau logo. », « On enlève le masque. », « Faux. », « Un disque invisible. », « Le fix : creuser l'anneau. ») restent à l'écran, non lus.
- **Calage VO (voice-04) :** B1 à 0,2 s (durée 2,93 s) · B2 à 3,2 s (1,78 s) · B3 à 7,2 s (1,57 s) · B4 à 12,2 s (4,26 s) · B5 à 21,2 s (3,03 s) · B6 à 27,2 s (3,53 s). Chaque clip finit dans son beat. Le mot « disparu » est repéré par détection de silence (début ≈ 2,03 s dans le clip), pas par alignement mot à mot : à réécouter.
- **Bouclage :** B6 finit sur APPROVING ; pas de logo de marque à l'écran dans cette version (aucun nom n'est affiché).
- **Hors v4 :** pas de rendu vidéo complet, pas de publication avant validation King.
