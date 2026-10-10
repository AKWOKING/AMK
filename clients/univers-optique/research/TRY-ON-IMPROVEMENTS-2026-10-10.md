# Essayage Univers Optique — pistes d'amélioration, après recherche (10/10/2026, 20:50)

> **PROPOSITION. Aucune ligne de code modifiée.** King a testé `uo-essayage-camera.vercel.app` sur son téléphone : **« ça marche »** (verbatim 10/10). **La source de l'app n'est PAS dans le dépôt** : je n'ai pu lire que le texte de la page en ligne (titre « UO · Essayage en direct (caméra) · prototype J2 », caméra, mode photo, visages d'exemple, 6 montures, bouton « + » pour ajouter ses montures, détourage automatique du fond clair, message « internet nécessaire au premier lancement »). Je ne sais donc **pas** si l'overlay est en 2D (PNG) ou en 3D, ni comment l'échelle est calculée : chaque piste ci-dessous dit ce qu'elle suppose. Cadre : `SCOPE-2026-10.md` (900 000 FCFA, ≤3 appareils, ≤30 montures, APK local, garantie 30 j) et ruling « rien ne se finalise sans la validation du client ».

## Ce que disent les sources (trouvées le 10/10)
| Sujet | Constat | Source |
|---|---|---|
| **Échelle** | Un visage vu par caméra n'a pas de taille absolue : avec une distance inter-pupillaire moyenne supposée (63 mm), les lunettes sont **fausses de ±15 %** selon le visage. Meilleure référence : le **diamètre de l'iris (≈11,7 mm)**, ou une carte bancaire | KhalidAb7/VTO (« Known limitations » + « Recommended next improvements »), rohitjaiswal2001/Eye-Glass-Track-on |
| **Branches / occlusion** | Les branches doivent **disparaître derrière l'oreille et la tête** quand on tourne ; solution : maillage du visage + proxy de la tête, invisibles, qui n'écrivent que la profondeur | Eye-Glass-Track-on, alperenuzun/basic-virtual-tryon-glasses |
| **Stabilité** | Lissage (filtre « One-Euro » ou exponentiel) pour que la monture ne tremble pas ; la forme du visage est mesurée seulement en vue de face pour que l'ajustement ne dérive pas quand on tourne | Eye-Glass-Track-on, basic-virtual-tryon-glasses |
| **Performance (mobiles modestes)** | Délégué GPU d'abord, repli CPU ; détection **seulement quand une nouvelle image arrive** ; moteur de visage dans un **Web Worker** pour ne pas bloquer l'affichage ; chargement différé | KhalidAb7/VTO (« Performance notes ») |
| **Perte du visage** | MediaPipe perd le visage au-delà de ≈65° de rotation : les lunettes se cachent jusqu'à ce qu'il soit retrouvé | Eye-Glass-Track-on |
| **Précision publiée** | Un article universitaire (MediaPipe + Three.js) rapporte **IoU 85 %, erreur de largeur 4–5 %** — c'est leur système, pas le nôtre | nepjol.info (A Web-Based AR-Powered Virtual Eyewear Try-On System) |
| **Calibrage par monture** | Chaque produit se cale une fois (décalage vertical = centre des verres sur les pupilles ; profondeur = pont sur le nez ; échelle) puis l'enregistre | KhalidAb7/VTO §9 |

## Pistes classées (valeur pour un opticien ÷ effort ; mon jugement, pas une mesure)
1. **Test sur le terrain AVANT toute amélioration** (effort : 1 h de King). Trois téléphones Android modestes, lumière de boutique, lunettes déjà portées, cheveux longs, tête tournée à 45°. C'est la phrase de notre propre note du 02/10 : « LE point à vérifier en conditions réelles ». Sans ça, on améliore au hasard.
2. **Taille réelle de chaque monture** (effort : faible si l'app a déjà un champ par monture). L'opticien connaît la largeur réelle (le calibre est gravé à l'intérieur de la branche) : la saisir à l'ajout d'une monture, et prendre l'iris comme référence de visage, rend la **taille crédible** — c'est ce qu'un patient compare. *Suppose que l'échelle actuelle repose sur une moyenne : à confirmer dans la source.*
3. **Branches derrière l'oreille** (effort : moyen). Le défaut le plus visible dès que le client tourne la tête. *Suppose un overlay 3D ou un masque par monture ; en 2D pur, limiter la rotation autorisée et le dire.*
4. **Lissage + « visage perdu »** (effort : faible). Message clair (« replacez le visage ») au lieu d'une monture qui saute.
5. **Moteur dans un Web Worker, GPU puis CPU** (effort : moyen), seulement si le test 1 montre des saccades.
6. **Fonctionner sans internet après le premier lancement** (effort : faible). Le texte de la page dit que internet est nécessaire au premier lancement ; l'APK local du périmètre doit embarquer le moteur de visage. À vérifier à la livraison, pas avant.
7. **Ajout de monture** : le détourage « fond clair automatique » est annoncé ; un détourage automatique rate les montures claires ou transparentes. Prévoir un aperçu avant de valider l'ajout et conseiller le PNG détouré. *Je n'ai pas testé ce bouton.*
8. **Idée à moi, aucune source :** envoyer la capture par WhatsApp (partage du navigateur) pour que le client la montre à un proche. Hypothèse de vente, pas une exigence du client.

## Ce qui n'est PAS recommandé
- Passer au 3D complet par monture (30 montures, pas de numérisation : coût hors périmètre, cf. note du 02/10).
- Promettre une précision en millimètres : même les sources parlent de ±15 % sans calibrage.
- Ajouter des fonctions avant le retour du client (« rien ne se finalise sans votre validation »).

## Ce qu'il me faut de King
1. **La source de l'app** (dépôt, dossier ou zip) : sans elle je ne peux rien modifier. Elle devrait vivre dans `clients/univers-optique/app/`.
2. Le résultat du test terrain (piste 1), même informel : sur quel téléphone, et ce qui a cloché.
