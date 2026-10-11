# VIRTUAL TRY-ON — options réalistes pour AMK (02/10)

> Commande de King (02/10) : Univers Optique veut « une app où le client prend UNE photo (sans
> lunettes) puis swipe des montures sur son visage ». **Recherche d'abord, aucun contact, aucun build,
> aucun pitch avant lecture de King.** Statut : livrable de décision, pas un devis.

## 1 · Ce qu'est l'essayage virtuel en 2026 — quatre catégories, et ce qui marche vraiment

| Catégorie | Principe | État réel en 2026 |
|---|---|---|
| **AR temps réel (caméra)** | la caméra filme le visage, un moteur de face-tracking pose les montures en direct | **C'est le standard marchand.** Banuba [1](https://www.banuba.com/glasses-virtual-try-on), Fittingbox, Jeeliz le font tourner en navigateur, y compris sur mobiles modestes. C'est du produit, pas de la démo. |
| **Photo-based (landmarks + overlay 2D)** | une photo uploadée → détection des points du visage → montures PNG alignées sur les yeux, qu'on fait défiler | **Marche très bien pour CHOISIR** (pas pour « se voir en vidéo »). C'est exactement le geste décrit par Univers Optique : photo → swipe. Le moins cher, le plus robuste sur vieux téléphones. |
| **Photo-based génératif (IA)** | une photo + une monture → image régénérée par diffusion | Qualité inégale sur les lunettes (géométrie des branches, reflets) ; coûteux par image ; **c'est un outil de shooting produit, pas d'essayage client** [2](https://www.photta.app/blog/best-ai-eyewear-virtual-try-on-tools). Intéressant pour les visuels du catalogue, pas pour le swipe. |
| **3D complet (modèles par monture)** | chaque monture scannée/modélisée en 3D, rendu PBR | Le rendu premium des gros (Fittingbox 195 000+ montures pré-digitizées [3](https://auglio.com/en/best-virtual-try-on-eyewear-2026)). **Irréaliste à notre échelle** : digitizer le stock d'un opticien = coût par monture + délais, sans base préexistante. |

Verdict : **le besoin d'Univers Optique est la catégorie 2** (photo → swipe), éventuellement habillée en
catégorie 1 plus tard. Pas la 3 (trop cher), pas la 4 (trop lourd).

## 2 · Les options réalistes pour AMK, classées coût/complexité

### Option A — Photo + landmarks + overlay (recommandée pour le MVP)
- Moteur : **MediaPipe FaceLandmarker** (Google, open source, Apache-2.0, 468 points du visage, tourne
  dans le navigateur, gratuit) — la pile de référence existe déjà en MIT : MediaPipe + Three.js,
  landmarks + occlusion [4](https://github.com/alperenuzun/basic-virtual-tryon-glasses).
- Pipeline montures : photo frontale de chaque monture sur support, fond retiré une fois, PNG calibré.
  Zéro coût par monture après l'outillage (une séance photo au téléphone, qu'on sait faire).
- Coût récurrent : **0 FCFA** (tout tourne sur le téléphone du client).
- Complexité : moyenne-faible. C'est du web mobile-first, notre cœur.
- Compatibilité Cameroun : excellente — pas de vidéo temps réel, pas de WebGL lourd ; une photo suffit.

### Option B — Widget AR temps réel open source
- **Jeeliz VTO Widget** : JavaScript/WebGL, « photo-realistic real-time glasses try-on directly in the
  browser », repo public [5](https://github.com/jeeliz) ; gratuit en self-hosted (licence à vérifier au
  moment de l'adoption — le cœur est open, jeeliz.com vend le service managé).
- Alternatives gratuites : **TensorFlow.js face-landmarks-detection** (open source), le même MediaPipe.
- Coût : 0 FCFA de licence ; complexité moyenne (caméra + HTTPS + perf sur Android modestes à tester
  sur place — c'est LE point à vérifier en conditions réelles Cameroun).

### Option C — SDK commerciaux (Banuba, Fittingbox, DeepAR, Auglio)
- Banuba : widget self-serve **$49/mois pour 1 000 essayages**, $99 (3 500), $349 (15 000) ; app Shopify
  $319–1 599/mois [1](https://www.banuba.com/glasses-virtual-try-on)[6](https://www.banuba.com/blog/best-virtual-try-on-platforms-eyewear-brands). ≈ 30 000–210 000 FCFA/mois **de licence seule**.
- Fittingbox ≈ $59/mois entrée [2](https://www.photta.app/blog/best-ai-eyewear-virtual-try-on-tools) ; Auglio dès $119/mois [3](https://auglio.com/en/best-virtual-try-on-eyewear-2026) ; Perfect Corp $379/mois [6](https://www.banuba.com/blog/best-virtual-try-on-platforms-eyewear-brands). DeepAR : abonnement, prix non revérifié cette passe.
- Verdict : **trop cher pour un opticien de Douala** (la licence mange le mensuel AMK entier), et on
  devient revendeur d'un SDK qu'on ne contrôle pas. À garder en mémoire si un gros client émerge.

### Option D — Essayage génératif par image
- Coût par image en 2026 : $0.003–0.03 selon modèle/hébergeur (FLUX schnell ≈ $0.003, SD 3.5 ≈
  $0.008–0.012) [7](https://www.digitalapplied.com/blog/ai-image-generation-api-pricing-comparison-2026)[8](https://modelslab.com/cheapest-ai-image-api) ≈ 2–18 FCFA l'image.
- Mais : la qualité « monture sur VOTRE photo » reste inégale, latence + dépendance API + coût qui scale
  avec l'usage. **À réserver à la production de visuels catalogue**, pas à l'outil client.

## 3 · App vs web — trancher la question d'Univers Optique

Il a dit « app ». **Le web gagne, de loin, pour le Cameroun :**
- Aucun téléchargement (16 Go de stockage, données coûteuses), aucun store, aucune mise à jour à pousser.
- Un lien WhatsApp ouvre l'outil : c'est déjà le canal de vente de l'opticien.
- « App » perçue = PWA ajoutée à l'écran d'accueil : icône, plein écran, même geste — sans les coûts.
- Maintenance : une seule base de code, hébergée avec nos sites existants.
Le cas pour une vraie app n'existe que si l'outil doit tourner **hors ligne en boutique sur un terminal
dédié** — ce n'est pas le besoin exprimé (c'est LE client qui essaie, sur SON téléphone).

## 4 · Le MVP — la plus petite chose qui livre la valeur

Geste cible, tel que demandé par Univers Optique : **photo → essaye → choisis → WhatsApp**.
1. Page mobile : « prenez ou chargez une photo, sans lunettes, de face ».
2. Landmarks MediaPipe côté téléphone ; estimation de l'écart pupillaire apparent pour l'échelle.
3. Galerie swipe de N montures (PNG calibrés) posées sur la photo ; rotation/inclinaison auto douce.
4. Bouton « demander ce modèle » → WhatsApp pré-rempli avec le nom de la monture (standard maison).
5. Back-office minimal pour l'opticien : ajouter/retirer des montures (photo + nom + prix).
**Pas** de stock en ligne, pas de paiement, pas de PD médical, pas de 3D. La douleur « remonter les
montures après chaque client » est couverte : la vitrine devient la photo, pas le mur.

## 5 · Effort, prix, et la question stratégique

- Effort estimé : moteur photo/landmarks 15–20 h · pipeline montures + back-office 10–15 h · UI mobile +
  WhatsApp 10–15 h · QA sur téléphones réels (Android modestes inclus) 8–10 h → **45–60 h**.
- Prix : c'est une **ligne de service séparée**, pas le pack site à 150 000. Suggestion à discuter avec
  King : pilote **900 000–1 500 000 FCFA** (build + digitisation de 20–30 montures) + **30 000–50 000
  FCFA/mois** (hébergement, ajout de montures, évolutions) — soit 6 à 10× le site, cohérent avec un outil
  qui touche au chiffre d'affaires, pas à la vitrine.
- **La question stratégique : oui, c'est répétable.** Le moteur est construit une fois ; par opticien
  suivant, il ne reste que la séance photo des montures + l'intégration (≈ 8–12 h). Si le pilote
  Univers Optique tourne, c'est une ligne produit « essayage virtuel pour opticiens du Cameroun » —
  exactement le « something + website » que le marché demande (§3.9 KB). Univers Optique = client
  pilote, pas client gratuit : le prix pilote reste un prix.

## 6 · Ouverts (à trancher avant tout build)
- Licence exacte du widget Jeeliz si on le touche (le cœur open source suffit probablement).
- Test terrain : MediaPipe sur un Android 2019 moyen de Douala, en 3G — le vrai juge de paix.
- Le geste « photo du client par le vendeur en boutique » (sa variante à lui) vs « photo chez le client »
  (notre variante) : mêmes briques, deux UI — commencer par celle du client.
- Consentement photo : une phrase claire avant upload (photo traitée sur SON téléphone, pas envoyée).

---
Sources vérifiées le 02/10 depuis le sandbox : Banuba pricing [1][6] · Photta/Auglio comparatifs 2026
[2][3] · repo MIT MediaPipe+Three.js [4] · GitHub Jeeliz [5] · pricing APIs image 2026 [7][8].

## 7 · Ruling pricing (King, 02/10) — remplace la fourchette du §5
- **Pilote Univers Optique : 750 000 FCFA**, conditionné aux droits d'étude de cas tier-1 (nom,
  captures, métriques avant/après anonymisées, contenu public une fois livré). Le prix pilote est
  discounté parce qu'on **achète l'étude de cas**, pas seulement parce qu'on vend l'outil.
- **Standard opticien 2+ : 1 200 000 FCFA**, sans discount, scope complet.
- **Mensuel : 30 000 FCFA** — hébergement, maintenance, ≤ 4 h de modifications/mois.
- **S'il pousse sur 750k : ne jamais descendre.** Proposer le split 400k au départ / 350k à la
  livraison — même total. Jamais de remise ; on trade le scope ou le timing, jamais le prix.
- Brouillon du message : `PITCH-DRAFT-2026-10.md` — rien ne part avant mercredi ET avant revue de King.

## 7b · Note ruling 03/10 sur le §3 (« app vs web »)
Le §3 argumente que le web gagne — **c'est notre recommandation générale, et elle reste vraie en
général** (pas de téléchargement, pas de store, lien WhatsApp). **Pour CE client, elle est battue :**
il a posé une exigence qui prime — son catalogue ne doit être consultable par personne d'autre, donc
rien d'hébergé publiquement. Règle née le 03/10 (King) : **quand un client pose une exigence,
l'exigence gagne sur notre recommandation ; si on n'est pas d'accord, on le dit explicitement et on
demande un ruling — on ne pitche jamais en douce contre l'exigence.** (Même classe de bug qu'OraCare :
habiller une préférence interne en décision client.)

## 8 · RULING 03/10 — architecture LOCAL-ONLY on-device
- **Android, sideloadé (APK), PAS de Play Store** (public) · wrapper **Capacitor** pour garder une
  base HTML maintenable.
- Photos des montures **stockées localement** sur l'appareil ; aucun endpoint parcourable.
- Landmarks visage **on-device** (MediaPipe FaceLandmarker, gratuit, tourne local) ; photo du client
  prise dans l'app, compositing local, **rien n'est uploadé**.
- Mise à jour du catalogue : **MVP = reinstall** à chaque update ; plus tard, sync privé
  device-ID-gated (le mensuel 30k couvre « l'endpoint sync SI utilisé »).
- Distribution : son téléphone + ceux de ses collaborateurs — **nombre exact INCONNU** (question
  ouverte : lui + 1–2 = simple ; comptoir multi-shifts = catalogue partagé + mécanisme de maj).
  Le pitch ne commit à aucun nombre tant que la réponse n'est pas là.
- **Pricing ruling :** pilote 900 000 (450/450 ; pushback → 300/300/300) · standard 1 400 000 ·
  mensuel 30 000. Le 900k = coût honnête du local-only (packaging, tests devices, permissions,
  offline, flow update) — pas un premium, pas d'excuse.
- Pour les sessions futures : le §2 (option A photo+landmarks) reste le MOTEUR technique — seul le
  SHELL change (web → APK Capacitor). La recherche web/SDK garde sa valeur pour tout client qui, lui,
  accepte le web.

## 8b · Révision pricing 03/10 v3 — même montant, nouvelle forme (ruling King)
Recherche : 900k est **sous le marché** du dev custom au Cameroun (apps simples ≈ 2M FCFA+ ; dev senior
Douala 200–350k/jour) — le problème n'était pas le montant mais le **one-time** : en PME, une grosse
demande initiale déclenche un process d'achat au lieu d'un oui. Nouvelle structure : **300k signature ·
300k livraison MVP · 300k J+30 post-lancement**, droits d'étude de cas inclus dans les trois tranches.
Fallback si l'entrée 300k bloque : **200k/350k/350k**, même total, jamais sous 900k. Standard 1.4M
inchangé. (Le v2 450/450 et le v1 400/350 sont caducs.)
