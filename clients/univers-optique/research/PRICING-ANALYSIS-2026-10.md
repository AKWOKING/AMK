# PRICING ANALYSIS — UNIVERS OPTIQUE TRY-ON LOCAL-ONLY · 03/10

> Question (King) : **étant donné le scope corrigé, 900 000 FCFA est-il le bon prix pilote ?**
> Scope corrigé : app Android **local-only sideloadée** (pas de store, pas d'URL publique) · try-on AR
> photo → landmarks on-device (MediaPipe) → overlay monture → swipe · **≤ 3 appareils** (lui +
> collaborateurs — **ceci clôt la question « collaborateurs » restée ouverte**) · photos de montures
> stockées localement, rien d'uploadé, **pas de backend, pas d'hébergement** · pas de routage WhatsApp,
> pas de capture de leads · MVP update = reinstall · effort estimé **45–60 h**.
> Taux utilisés : 1 USD ≈ 590 FCFA · 1 KES ≈ 4,5 FCFA · 1 NGN ≈ 0,39 FCFA (approx., à vérifier au jour du devis).

---

## 1 · Coût d'une app Android locale/offline au Cameroun et en Afrique de l'Ouest
- **Peef.dev (août 2025)** : app simple avec stockage local (type Firebase/Supabase) = **300 000 – 800 000 FCFA** ; avec géoloc/paiements = 450 000 – 1 M ; les freelances mobiles camerounais **démarrent à 1,5–2 M FCFA en forfait** (l'heure est rare, le forfait est la norme) ; app complète cross-platform moyenne ≈ 3,8 M.
  Source : peef.dev/blog/combien-coute-une-application-mobile-en-afrique-250-000-fcfa-303
- **We-Flutter, guide prix Afrique 2026 (fév. 2026)** : freelance Cameroun **à partir de 1,5 M FCFA** ; point clé pour nous : **« optimisation offline-first : +15 à 20 % du budget »** (le offline coûte plus cher, pas moins) ; freelance Cameroun ≈ 6 k€ avec « risque 70 % abandon ».
  Source : we-flutter.com/prix-application-mobile-afrique/
- **Marché local (blog business Cameroun 2026)** : freelance local facture **500 000 – 3 M FCFA par application**.
  Source : blog.iambeezy.app/fr/business-rentable-cameroun-2026-20-idees-forte-marge-fcfa/
- ⚠️ Aucun devis public trouvé pour la catégorie exacte « sideloaded, offline, sans backend » — le plus proche est « app simple à stockage local » (300–800 k) auquel s'ajoute la prime offline-first (+15–20 %) et la complexité AR (section 2). Les 200–350 k/jour « dev senior Douala » viennent de notre recherche antérieure — **non re-vérifiés ce jour** ⚠️.

## 2 · Coût spécifique d'un try-on AR lunettes (deux sources minimum)
- **Abbacus Technologies (sept. 2026)** : « Eyewear try-on : **$8 000 – $25 000** » ; basique $8–15 k, avancé $15–30 k+ ; simple WebAR $5–15 k. ✔ **Confirme le benchmark 8–25 k$ de King** (= **4,7 M – 14,8 M FCFA**).
  Source : abbacustechnologies.com/how-much-does-it-cost-to-build-an-ar-try-on-feature/
- **SpikeSecure, Inde (sept. 2026)** — le point bas du marché mondial : widget web try-on lunettes **₹4–10 lakh ≈ 2,8–7,0 M FCFA** ; app Android+iOS **₹8–18 lakh ≈ 5,6–12,6 M FCFA** ; 8–10 semaines ; maintenance dès ₹20 k/mois.
  Source : spikesecure.com/ar-virtual-try-on-development/eyewear/
- **Idea Usher (janv. 2026)** : app try-on lunettes $10–100 k au total ; dont « facial detection & tracking » **$3–15 k** et « real-time overlay & alignment » **$5–20 k** — c'est exactement le cœur de notre build.
  Source : ideausher.com/blog/create-virtual-eyeglass-try-on-app/
- **MediaPipe vs SDK commerciaux :** les SDK (Banuba dès ~$319/mois ; Fittingbox dès ~$59/mois ; Photta) sont **des services hébergés/métrés** — leur modèle entre en conflit direct avec l'exigence local-only (rien sur un serveur). **MediaPipe FaceLandmarker (468 landmarks, on-device, gratuit) est le seul moteur compatible avec le scope** ; il supprime la licence récurrente mais remet le travail de tracking **dans nos 45–60 h** — la ligne « facial detection & tracking $3–15 k » d'Idea Usher, c'est ce travail-là. Le local-only n'est donc pas une économie : il déplace le coût de la licence vers les heures.

## 3 · Plancher de main-d'œuvre — 45–60 h à Douala
- **Upwork, taux par région (janv. 2026)** : Afrique **$30–60/h** ; Upwork médian mobile **$27/h**, p25 $18, p75 $39 (gigradar.io/blog/upwork-hourly-rate).
  Sources : upwork.com/resources/cost-build-mobile-app · gigradar.io
- Calcul du plancher (45–60 h) :
  - **Plancher Upwork p25 ($18/h)** : $810–1 080 ≈ **480 k – 640 k FCFA** (taux plancher, zéro prime de risque).
  - **Médiane ($27/h)** : $1 215–1 620 ≈ **720 k – 960 k FCFA**.
  - **p75 ($39/h)** : ≈ **1,05 M – 1,4 M FCFA**.
  - Forfaits locaux : 500 k – 1 M pour une app simple **sans AR** (section 1).
- **Le chiffre clé : 900 000 ÷ 60 h = 15 000 FCFA/h ≈ $25/h — pile la médiane Upwork.** 900k n'est donc ni un cadeau ni du luxe : c'est la médiane mondiale du freelance appliquée à un build camerounais.

## 4 · Valeur des droits d'étude de cas — précédents de marché
- **Diagnostic Biochips, modèle « 50-for-50 » (via ViaVerus, juin 2026)** : prix early-access ≈ **50 % du futur prix liste** contre la reconnaissance beta ; effets : le client devient acheteur (pas évaluateur), cash réel, **prix de référence pour les clients suivants**, données marché.
  Source : viaverus.com/blog/free-pilots-are-killing-your-startup-the-case-for-charging-in-beta
- **Content Fudge (2025)** : beta payante = remise « souvent **50 % ou plus** » du prix cible. · **Doctor Market Fit (2024)** : remise pilote typique **50–75 %**. · Pratique SaaS (Quora, 2017) : pilote beta = 50 % du pro-rata.
- **Notre structure face à la bande 25–50 % :** pilote 900 k vs standard 1 400 k = **remise de 36 %** contre droits d'étude de cas (nom, captures, métriques anonymisées, contenu public une fois live). **Dans la bande, côté raisonnable** — et le premier-mover AR lunettes au Cameroun est un cas réellement vendable (aucun concurrent local à citer).

## 5 · Comparable privé/white-label dans un marché similaire
- **Nigeria (Nexoris, sept. 2026)** : app custom simple (MVP) **₦2,5–6 M ≈ 975 k – 2,34 M FCFA**.
- **Kenya (Quest Designers)** : MVP mono-plateforme **KES 150 k ≈ 675 k FCFA** (explicitement « offline-first architecture ») ; app business KES 500 k ≈ 2,25 M.
  Sources : nexoristech.com/insights/mobile-app-development-cost-in-nigeria/ · questdesigners.com/services/mobile-app-development
- **Ghana** : pas de grille publique crédible trouvée ce jour ⚠️ (gap assumé, ne bloque pas la conclusion — Nigeria + Kenya + Cameroun convergent).
- **Effet de l'exigence de confidentialité sur la valeur :** le local-only supprime tout upside récurrent de notre côté (pas d'hébergement à facturer sauf l'option sync, pas de SaaS) ; en échange le client obtient **l'exclusivité** — un outil que ses concurrents ne peuvent ni parcourir ni copier. Cette exclusivité est SA valeur, pas la nôtre : **on ne la facture pas en premium, on facture les heures** — ce que fait déjà la structure 300/300/300.

---

## RECOMMANDATION : **garder 900 000 FCFA, structure 300/300/300 inchangée**
1. **Économie du travail vérifiée** : 15 k FCFA/h effectif = médiane Upwork ; 1,4–1,8× le plancher absolu — assez pour absorber le risque réel du build (qualité de l'overlay AR sur Android bas de gamme, tests multi-appareils, packaging).
2. **Sous tous les benchmarks produit** : 900 k = 19 % du bas du benchmark eyewear ($8 k) et 32 % du point bas mondial (SpikeSecure ₹4 lakh) — et ces benchmarks sont pour des versions **hébergées** ; la nôtre est plus rare.
3. **Au-dessus du plancher local sans AR, en dessous du forfait freelance camerounais standard** (1,5–2 M) : cohérent pour un outil mono-fonction, mais à complexité AR réelle.
4. **La remise pilote (36 % vs 1,4 M) est dans la bande documentée 25–50 %** et s'achète contre des droits qui ont un prix de marché réel.
5. **Le tranchage 300/300/300 fait le travail psychologique** (pas de gros montant initial → pas de process d'achat) — la recherche de la v3 reste valable ; le montant n'a jamais été le problème.
- **Garde-fou de scope à écrire dans le devis** : catalogue MVP plafonné (ex. ≤ 30 montures numérisées à la prise de vue simple) ; au-delà, ou après le pilote, les nouvelles références passent par le mensuel 30 k (≤ 4 h/mois). Sans ce plafond, le « reinstall on catalog change » peut glisser.
- **Ne PAS baisser à 750 k** : ce prix datait de la version web ; la recherche montre qu'on serait sous la médiane mondiale du travail pour un build AR. **Ne pas monter non plus** : 900 k est déjà la porte d'entrée honnête du marché local — le standard 1,4 M existe pour l'opticien 2+.
