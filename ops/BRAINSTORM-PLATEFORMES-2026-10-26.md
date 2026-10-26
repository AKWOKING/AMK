# Brainstorm — 26/10/2026 (tour 153, 11 h) · une légende par plateforme, ou un montage par plateforme ?

```text
Question   King : « hashtags and caption for tiktok and for instagram separately adapted to the respective
           social medias — or do you think we should tweak the videos for specific platforms »
Contexte   Facebook part à 12 h. Il reste une heure. Le master v6 est validé (23,71 s, 4 portes vertes).
Méthode    graphify (12 730 nœuds) → preflight.sh → PRE-FLIGHT.md §00 → superpowers/brainstorming
```

## Ce que le dépôt savait déjà (et qui tranche avant l'opinion)

| Fait | Source | Conséquence |
|---|---|---|
| **Un tournage, deux montages** — TikTok 12–16 s, Facebook 16–22 s | `CONTENT-CREATION` §5 quater (ruling King 23/10) | la question de King a **déjà** une réponse écrite : oui, mais par le montage |
| **TikTok note le film, Facebook le distribue** (26 % vs 12 % de lecture moyenne sur la même vidéo) | idem, tableau du 23/10 | ce qui se joue sur TikTok, c'est la rétention des deux premières secondes |
| **3 à 8 hashtags : local + niche + marque** | `TIKTOK-SEO-CHECKLIST` §C | la forme des hashtags est écrite ; le nombre n'a pas de preuve, c'est une règle |
| **Sous-titres manuels, jamais automatiques** | ruling King 11/10 | l'automatique ne tient pas sur un accent camerounais |
| **FR à l'écran, EN en légende** | `brand/AMK-PRESENCE` §2, correction 5 | l'adaptation Instagram est **déjà tranchée** : la langue de la légende |
| **Narration 6,2 s de lecture vs 3,8 s avec son tendance** | `ANALYTICS-LOG` 17/09 | on n'ajoute pas de son tendance par-dessus la voix |

## Les trois options

| | **A — mêmes masters, trois légendes** | **B — coupe TikTok 16 s aujourd'hui** | **C — version anglaise pour Instagram** |
|---|---|---|---|
| Ce qu'on gagne | la pièce sort à 12 h sur les trois réseaux | la grille du 23/10 est tenue | l'anglophone entend la pièce, pas seulement la légende |
| Ce qu'on perd | la grille TikTok (23,7 s au lieu de 12–16) | 40 min de re-synthèse + re-rendu, et le texte validé par King change | 1 h (6 clips EN), et la cible Instagram a **6 abonnés** |
| Le risque | un TikTok long, faiblement poussé | publier en retard sur les trois réseaux | dépenser une heure sur le plus petit des trois comptes |

## Recommandation : **A aujourd'hui, B pour EP02, C refusé**

**A** — parce que l'adaptation qui change le résultat à une heure de la publication est **la légende**, pas
le fichier : le master est en 1080×1920, sans filigrane, et son texte utile est entre 12 % et 53 % de la
hauteur (mesuré, §1 du kit), donc hors des zones que TikTok et Instagram recouvrent.

**B pour EP02** — la règle du 23/10 est bonne et n'est pas appliquée ici pour une seule raison : l'heure.
Elle se décide **avant** d'écrire le prochain script, pas après le rendu.

**C refusé** — le dépôt a déjà tranché : FR à l'écran, EN en légende. Une seconde voix anglaise doublerait
le travail de relecture de King pour un compte à 6 abonnés. Le jour où l'anglophone devient une cible
mesurée, on rouvre.

## La porte

`tools/qa/audit_platform.py` (+ `test_audit_platform.py`, **16/16**) vérifie trois règles qui n'étaient
vérifiées par rien : le nombre et la nature des hashtags, les sous-titres manuels, et la langue de la
légende Instagram. Elle **avertit** (`coupe-tiktok-manquante`) quand le master dépasse 16 s — un
avertissement, pas un refus : la pièce longue a le droit de sortir, mais on doit le savoir.
