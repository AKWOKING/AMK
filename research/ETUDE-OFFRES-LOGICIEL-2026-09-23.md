# ÉTUDE — LES OFFRES « LOGICIEL DE GESTION », UNE PAR UNE
**23/09/2026** · suite de `research/ERPNext-AUDIT-2026-09-23.md` · pour chaque offre : le problème, **ce qui
existe déjà au Cameroun et dans la région**, comment ça se vend, ce que ça coûte, **ce que ça peut rapporter**,
et un verdict. Les prix que je propose sont des **propositions à valider** — aucun n'est posé à un client.

---

## 0 · Ce que cette étude change (trois corrections à mon audit précédent)

1. **Mon offre A (caisse + factures + stock à 250 000 + 25 000/mois) ne tient pas.** Le marché camerounais est
   **déjà servi, à 0 à 25 000 FCFA/mois**, par des logiciels locaux conformes OHADA, dont certains incluent déjà
   le Mobile Money, la paie CNPS et la DSF. Nous ne sommes pas seulement plus chers : nous serions **le prix le
   plus élevé du marché pour la même fonction**. Détail §2.
2. **Le Mobile Money n'est pas un trou, c'est un branchement.** Je disais « aucune passerelle Mobile Money » :
   c'est vrai pour ERPNext, **faux pour le Cameroun**. CamPay, Fapshi, Notch Pay, MMGate, Simiz, Monetbil,
   Diool encaissent MTN et Orange, avec une API, **pour 2 à 3 % par transaction**. Ce qui coûte 5 à 15 millions
   FCFA, c'est l'intégration **directe** chez les opérateurs — et là, on ne joue pas. Détail §1.2.
3. **L'offre B (labo/clinique) est la seule où notre prix tient — mais nous n'avons aucune référence en santé,
   et les concurrents en ont des dizaines** (65 cliniques au Bénin pour Medica, un laboratoire primé à Yaoundé
   pour BoxyLab). Donc : **pilote à périmètre étroit**, pas une offre lancée. Détail §3.

Et une découverte qui va compter dans 12 mois : **la facture électronique obligatoire (loi de finances 2026)**
— §1.3 et §8.

---

## 1 · Le contexte qui décide de tout

### 1.1 Ce que les PME camerounaises paient déjà (relevé du 23/09/2026)

| Solution | Origine | Prix affiché | Ce qui est inclus |
|---|---|---|---|
| **zBilling** | 🇨🇲 Cameroun (ICT4U SARL), 158 entreprises en 5 ans | **10 000 FCFA HT/mois** (2 utilisateurs) · 20 000 (5 util.) · essai 7 j | ventes, facturation, finances, stocks, livraisons, **SMS clients**, helpdesk |
| **Nkap Control** | 🇨🇲 | **gratuit** (20 factures/mois) · **3 000/mois** (Pro) · 10 000 (Max) | TVA **19,25 %** automatique, stock, trésorerie, rapports TVA/IS, **MTN MoMo + Orange Money intégrés**, liens de paiement, multi-boutiques |
| **GesCab Africa** | Afrique | **6 500 à 12 000 FCFA/mois** | comptabilité **SYSCOHADA**, facturation, stock, achats, trésorerie, **paie CNPS**, **DSF au format DGI** |
| **Omamori** | 🇨🇲 (omamori.cm) | 15 000/mois (1 util.) · 25 000 (5 util.) | gestion + **paie normes camerounaises + DIPE magnétique CNPS** |
| **Duka360** | Afrique | 11 150 FCFA/mois, tout inclus | caisse, stock, facturation, RH, comptabilité |
| **CloudFacile / Optisales / Mobility Cloud / GestionsPro** | 🇨🇲 + Afrique | sur devis · à partir de 3 000/mois (GestionsPro) | gestion commerciale, paie CNPS (CloudFacile), pipeline commercial (Optisales, LocalHost Digital) |
| **Invexcam** | 🇨🇲 Douala | sur devis, **démo publique en ligne** | **Dolibarr** paramétré FCFA + OHADA — exactement l'idée « ERP open source adapté » que j'avais proposée |
| **MediConnect Africa** | panafricain | **250 000 FCFA + 10 000/mois** par profil | clinique, **laboratoire**, imagerie, **cabinet optique**, pharmacie, assurance : chacun son outil, tous reliés |
| **Medica (CICASYS)** | 🇧🇯 Bénin, **65 cliniques** | **2 500 000 FCFA** licence à vie (10 postes) · maintenance **100 000/trimestre** · poste sup. 25 000 · module seul dès 400 000 | dossier patient, laboratoire, facturation, stock |
| **Clinicaa** | Afrique | **5 500 000 FCFA** licence à vie **ou 500 000 FCFA en abonnement** · maintenance **600 000/an** | ERP de centre de santé, 7 modules, marche **avec ou sans connexion** |
| **BoxyLab** | 🇹🇳 Tunisie → vend au Cameroun | sur devis (configurateur en ligne) | SIL/LIMS laboratoire, conformité ISO 15189 ; **Laboratoire Prima (Yaoundé) primé** avec cet outil |
| **Labores** | 🇨🇲 (Michel Ndeme, IAI) | non publié | rendu informatisé des résultats ; déployé à l'hôpital **Ad Lucem Obobogo** depuis déc. 2018 |
| **OpenELIS Global / LabBook** | international, **open source** | **0 FCFA de licence** | SIL/LIMS ; OpenELIS **déployé en Côte d'Ivoire (étude sur 21 labos)**, LabBook conçu pour les labos des pays à faibles ressources |
| **Camerbiz** (agence) | 🇨🇲 | site vitrine **100 000** · dynamique **200 000** · hébergement **35 000/an** | repère de prix pour notre propre métier : **nous sommes déjà au-dessus du marché avec 150 000** |
| **ECS Informatique** | 🇨🇲 | hébergement 3 900 / 6 900 / 13 800 / 25 000 FCFA/mois | l'hébergement local se paie en FCFA, sans carte étrangère — **ça répond à la question du serveur** |

**Ce que ce tableau dit, en une phrase :** sur la gestion pure (factures, stock, caisse), **le Cameroun a déjà ses
éditeurs, ses prix bas et ses démos en ligne**. Notre entrée ne peut pas être « un logiciel » — elle doit être
**autre chose** : la présence, la configuration métier, l'intégration avec la vitrine, l'accompagnement.

### 1.2 Le Mobile Money est un branchement, pas un mur

| Voie | Coût | Délai réaliste |
|---|---|---|
| **Agrégateur local** (CamPay **2 %/encaissement**, Fapshi **3 %**, MMGate, Notch Pay, Monetbil, Diool, **Simiz 1,8-2,5 %**) | **0 FCFA d'installation**, commission par transaction | **2 à 5 jours** d'intégration |
| **Intégration directe MTN / Orange** | **5 à 15 millions FCFA** (développement, tests, certification) | **3 à 7 mois** |

Conséquence pratique : si un client veut « le paiement MoMo sur sa facture », **on passe par CamPay ou Fapshi**,
jamais par l'opérateur. Et pour un simple encaissement noté dans la comptabilité (ce dont 90 % des commerces ont
besoin), on crée deux modes de paiement « MTN MoMo » et « Orange Money » avec la **référence du SMS** : zéro
commission, zéro intégration.

### 1.3 La vague qui arrive : la facture électronique obligatoire

La **loi de finances 2026** camerounaise instaure la facturation électronique, d'abord sur les transactions
soumises à la TVA (**B2B en priorité**), sur un modèle de **contrôle continu en temps réel**. Le texte prévoit que
les entreprises utilisent **« exclusivement des équipements, logiciels ou dispositifs électroniques agréés par
l'administration fiscale »**, qu'elles assurent **la transmission instantanée et continue** des données de
facturation, et **l'intégrité et la conservation** des informations. La loi de finances 2024 avait déjà imposé un
suivi électronique à certains contribuables, et la DGI exploite déjà une plateforme de collecte de données (E-BILLING).

**Ce qui est certain aujourd'hui :** le cadre est voté, la direction est claire (tout passe par des plateformes
agréées), et **les détails techniques et la liste des prestataires agréés ne sont pas encore publiés**.

**Ce qu'on en fait :** ① **on ne promet jamais « conforme DGI »** — personne ne peut le promettre aujourd'hui ;
② on **prépare un actif** (un diagnostic de conformité + un partenariat avec une plateforme agréée dès la
publication) — c'est une vague qui forcera des milliers d'entreprises à changer ou adapter leur outil de
facturation, et **c'est exactement le genre de bascule où un petit acteur local peut se placer**. Détail §8.

**Nuance importante pour nos clients actuels :** un opticien ou un petit commerce hors TVA (chiffre d'affaires
sous le seuil du régime du réel) n'est pas concerné au départ. **On ne leur vend donc rien sur ce sujet** — on le
garde pour les PME au réel, les cliniques, les laboratoires, les distributeurs.

---

## 2 · OFFRE A — La caisse, les factures et le stock

**Le problème réel.** Le commerçant tient un cahier, un carnet de reçus, un fichier Excel. Il ne sait pas ce qu'il
a en stock, il ne sait pas qui lui doit de l'argent, et le soir il recompte la caisse à l'aveugle. Quand il grandit
(un deuxième point de vente, un employé qui encaisse), il perd le contrôle — et c'est là qu'il cherche un outil.

**Qui le fait déjà au Cameroun.** Tout le monde (§1.1) : zBilling (10 000/mois), Nkap Control (gratuit à
10 000/mois, MoMo inclus), GesCab (6 500-12 000/mois, DSF + paie), Omamori (15 000-25 000/mois, CNPS/DIPE),
Duka360 (11 150/mois), CloudFacile, Optisales, Mobility Cloud, GestionsPro, et Invexcam avec une démo Dolibarr
paramétrée OHADA. **Il n'existe pas de trou de marché ici.**

**Comment ils vendent.** Prix affiché, en FCFA, sans engagement, avec **essai gratuit de 7 jours**, formation
initiale incluse, support par WhatsApp, et un discours unique : « sans engagement, facturé en FCFA, conforme
OHADA ». Certains ciblent explicitement la paie CNPS pour verrouiller l'adoption.

**Ce que ça nous coûterait.** 3 à 5 jours de travail + un serveur (~5 000-8 000 FCFA/mois) + la traduction +
le support. Notre prix proposé était 250 000 + 25 000/mois — **soit 2 à 8 fois le prix du marché sur la même
fonction, avec un outil plus lourd et un support que personne d'autre ne réclame.**

**Verdict : on ne lance pas l'offre A telle quelle.** Trois repositionnements possibles, par ordre de solidité :

- **A1 — Revendre plutôt que construire (le plus rapide).** Prendre contact avec **zBilling (Cameroun)** ou
  **MediConnect Africa**, et demander un **programme de revendeur/intégrateur** : commission sur la mise en
  service et sur l'abonnement. Profit : faible par client (10-25 % de 10 000/mois = 1 000-2 500/mois), mais
  **zéro coût, zéro risque, et ça se vend en même temps que la page**. Notre valeur ajoutée : la configuration,
  la formation sur place, le suivi — pas le logiciel.
- **A2 — Le cas hors standard (là où le SaaS local casse).** Multi-dépôts, ventes à crédit avec échéanciers,
  commissions commerciales, tournées d'encaissement. C'est là qu'un ERPNext/Dolibarr se justifie, et là que le
  prix peut être défendu : **mise en service 200 000-400 000 + 20 000-35 000/mois**, avec un cahier des charges
  écrit **avant** le devis. Cible : pas un opticien, un **distributeur, une quincaillerie, un grossiste**.
- **A3 — Ne rien vendre, mais armer la page.** Pour nos 47 leads : la page web reste le produit. **La caisse
  n'entre pas dans la conversation.**

---

## 3 · OFFRE B — Le dossier, les résultats et les factures (laboratoire / clinique)

**Le problème réel.** Un laboratoire de Douala fait tout à la main : la fiche pré-imprimée remplie au stylo, le
résultat écrit dans le carnet du patient, la secrétaire qui ressaisit pour l'édition, l'échantillon qu'on ne
retrouve pas, la facture sur un carnet à souche. Quand un médecin demande un résultat de la semaine dernière, ça
prend une heure. Quand un client entreprise demande « combien je vous dois », personne ne sait. Et pour un
laboratoire qui vise une **accréditation ISO 15189**, tout ce qui prouve la traçabilité est en papier.

**Qui le fait déjà, ici et dans la région** — c'est le point dur :
- **MediConnect Africa (panafricain)** : labo, clinique, imagerie, **cabinet optique**, pharmacie — **250 000
  FCFA de mise en service + 10 000/mois**. C'est notre concurrent frontal le plus cher en crédibilité.
- **Medica / CICASYS (Bénin, 65 cliniques équipées)** : **2 500 000 FCFA** licence à vie, maintenance
  **100 000/trimestre**. Il vend au prix d'un vrai logiciel métier, avec des références.
- **Clinicaa** : 5 500 000 FCFA à vie ou **500 000 en abonnement**, maintenance 600 000/an. Fonctionne **avec ou
  sans connexion** — argument décisif ici, que nous n'avons pas.
- **BoxyLab (Tunisie)** : SIL/LIMS vendu en Afrique francophone, conforme ISO 15189, avec un **laboratoire
  camerounais primé** comme référence affichée.
- **Labores (Camerounais)** : déployé depuis 2018 (Hôpital Ad Lucem Obobogo).
- **OpenELIS Global** et **LabBook** : **open source, 0 FCFA de licence** — OpenELIS tourne déjà sur un réseau de
  21 laboratoires en Côte d'Ivoire et est soutenu par une université américaine (DIGI/UW).

**Comment ça se vend dans ce métier.** Démonstration sur les données du client (pas une démo générique),
**formation sur place par poste**, engagement sur le paramétrage des analyses du client, et **références
nominatives**. Le prix se compose toujours en trois blocs : mise en service (une fois), abonnement ou
maintenance (par an ou par trimestre), postes supplémentaires. Les concurrents affichent ces trois lignes —
c'est ce que le client compare.

**Ce que ça nous coûterait.** 5 à 10 jours de travail pour un périmètre labo complet (dossier, échantillons,
résultats, facturation), un serveur plus solide (~10 000-15 000 FCFA/mois), et **un risque réel : nous n'avons
aucune référence en santé**. Le module qualité (procédures, non-conformités, revues) serait un **différenciateur
fort** face à la paperasse d'accréditation — mais il ne se vend pas au premier rendez-vous.

**Proposition (à valider) :** **pilote à périmètre étroit — 400 000 FCFA de mise en service + 35 000 FCFA/mois**,
sur **un seul laboratoire**, avec un périmètre écrit noir sur blanc : *résultats + factures + encaissements MoMo,
2 postes, 3 h de formation, 2 types d'examens paramétrés*. Le dossier patient complet et le module qualité
s'ajoutent **après** le premier mois payé. **Ce n'est pas une remise, c'est un périmètre plus petit** (règle AMK).

**Le calcul, honnêtement.** 400 000 à l'entrée + 35 000 × 12 = **820 000 FCFA la première année**, pour 6 à 8
jours de travail et un serveur à 12 000/mois. Marge brute ≈ 60-70 %. Mais le vrai gain n'est pas là : c'est la
**première référence santé**, qui rend le deuxième client deux fois plus facile. Et le risque à couvrir : **si le
logiciel tombe, un laboratoire s'arrête** → sauvegardes vérifiées et procédure de secours écrites, dès le jour 1.

**Verdict :** c'est **la seule offre où notre prix tient**. À mener **en pilote**, sur un labo de notre liste
(UNI-LABO, Labiomed, ScientiLabo, KYLAYA, Bioscan, Pathcare), **après** avoir vérifié trois choses sur place :
qui saisit, quelle connexion, et quel est le circuit réel des résultats.

---

## 4 · OFFRE C — Le contrat d'entretien mensuel (le vrai revenu)

**Le problème réel — et cette fois c'est le nôtre.** Nous vendons une page 150 000 FCFA **une fois**, puis nous
la corrigeons gratuitement quand le client appelle. Chaque client gagné augmente notre charge de travail sans
augmenter nos revenus. C'est le modèle qui nous a menés à « le contenu ne nous a donné aucun lead ».

**Ce que le marché paie déjà pour ça.** Le concepteur de Clinicaa propose une **maintenance à 600 000 FCFA/an** ;
Medica facture **100 000 FCFA/trimestre** (400 000/an) ; l'hébergement local se paie **3 900 à 25 000 FCFA/mois**
chez ECS Informatique ; l'étude de marché agence web Douala 2026 identifie la **maintenance et l'hébergement comme
« le revenu récurrent n°1 »** du métier avec une **marge de 50-70 %**. *⚠️ Cette étude affiche des unités
incohérentes (« 80-500 FCFA/mois/site ») : je n'en retiens que la tendance, pas les chiffres.*

**Comment ça se vend.** Jamais seul : **attaché au livrable**, annoncé dès le devis, avec trois choses nommées —
① hébergement et nom de domaine, ② **sauvegardes vérifiées tous les mois**, ③ **2 h de modifications par mois**
(le client comprend « je peux t'appeler deux fois par mois sans négocier »). Engagement **annuel**, payé
**trimestriellement par MoMo** (là encore : CamPay/Notch Pay peuvent encaisser automatiquement, ou un simple
rappel WhatsApp).

**Proposition (à valider) :** **10 000 FCFA/mois** pour une page hébergée (ou **100 000 FCFA/an payé d'avance**),
**25 000-35 000/mois** pour une instance qui contient des données (labo/clinique).

**Ce que ça coûte :** serveur 5 000-8 000/mois par client (mutualisé au-delà de 3 clients), **1 à 2 h/mois**, et
un vrai risque : un abonnement non tenu est pire qu'un abonnement vendu. Marge brute > 70 %.

**Le calcul qui compte :** **10 clients à 10 000/mois = 100 000 FCFA/mois qui rentrent sans démarcher**, soit
notre prix d'une page complète **chaque mois et demi**, sans vente nouvelle. Vingt clients = 200 000/mois, notre
année de pages actuelles.

**Verdict : à lancer immédiatement**, à l'occasion du prochain paiement client (Le Cristallin, Univers Optique
— **une fois le gel levé et le prix encaissé**), et systématiquement **dans chaque devis futur**.

---

## 5 · OFFRE D — Le devis / la facture PDF à notre marque

**Le problème.** Aujourd'hui nos devis sont du **texte dans WhatsApp**. Le client ne garde rien, ne peut rien
montrer à un comptable, et notre agence ressemble à un indépendant qui travaille depuis son téléphone.

**Qui le fait déjà.** Tous les logiciels de gestion du tableau §1.1 produisent des factures PDF avec logo — ce
n'est **pas un produit vendable seul**. Côté agences camerounaises, **je n'ai trouvé aucune offre ni prix standardisé de devis PDF** — je ne peux
donc pas affirmer que c'est rare, seulement que ce n'est pas ce qui se vend en ligne.

**Ce que ça coûte / rapporte.** 2 à 3 h de travail, **0 FCFA de logiciel** (modèle d'impression maison, ou le
Print Designer si on monte un ERPNext plus tard). En **interne** : effet immédiat sur la crédibilité, et c'est
la pièce qui rend possible **le passage à l'offre C** (« voici votre devis, l'hébergement est en bas, en
abonnement »). En **externe** : option à **15 000-25 000 FCFA** dans un devis de page, pour un client qui veut
ses factures à son logo.

**Verdict : on le fait pour nous, cette semaine. On le vend en option, jamais seul.**

---

## 6 · OFFRE E — Le lien de facture qui s'ouvre dans WhatsApp

**Le problème.** Envoyer une facture par WhatsApp se fait aujourd'hui en photo floue ou en PDF lourd ; le client
ne la retrouve plus trois semaines après, et chacun redemande une copie.

**Qui le fait déjà.** Les liens de paiement existent chez **CamPay, Notch Pay, MMGate** ; Nkap Control inclut des
liens de paiement ; MediConnect et Medica ont des portails. **La version « message WhatsApp prérempli + lien vers
la facture hébergée » n'est pas standard ici** — et elle ne dépend d'aucun accord avec Meta : on utilise
**le numéro que le client a déjà**.

**Ce que ça coûte.** 1 à 2 jours de développement **une seule fois**, réutilisable pour tous nos clients : la
facture est générée en PDF, hébergée à une adresse secrète, et le message WhatsApp contient
`« Votre facture n°X : [lien] »`. Aucun coût par message.

**Ce que ça rapporte.** Ce n'est pas un produit : c'est **l'argument qui fait signer l'offre A2 ou B** (« votre
client reçoit sa facture en un clic, et il la retrouve toujours »). Et ça marche aussi **pour nous** : nos devis,
nos reçus d'acompte MoMo.

**Verdict : à construire une fois, à utiliser partout.**

---

## 7 · OFFRE F — Le site que le client modifie lui-même

**Le problème (pour le client).** Il veut changer un prix, ajouter une photo, et il doit appeler.

**Qui le fait déjà.** Le marché camerounais du site vitrine est **dominé par WordPress** (et les prix sont bas :
**100 000 FCFA** chez Camerbiz pour un vitrine, hébergement 35 000/an). Frappe Builder est techniquement propre
(licence MIT), Dolibarr a aussi un CMS.

**Le piège, et il est gros.** Notre page à 150 000 FCFA se défend parce qu'elle est **faite pour le client**.
Le jour où il peut tout modifier seul, il ne nous appelle plus — et s'il casse la mise en page, il nous appelle
quand même. **On perd le revenu de retouches et on garde le support.**

**Verdict : à ne proposer que premium** — « site + accès de modification » à **300 000 FCFA et plus**, avec
formation, jamais en standard. Et **à ne pas lancer maintenant** : notre revenu futur, c'est l'abonnement de
l'offre C, pas l'autonomie du client.

---

## 8 · OFFRE G (nouvelle) — L'accompagnement « facture électronique »

**Ce que c'est.** La LF 2026 impose la facture électronique (modèle temps réel, plateformes agréées), sans avoir
publié ni les spécifications techniques ni la liste des prestataires agréés. **Toute entreprise au régime du réel
concernée devra changer ou adapter son outil de facturation.**

**Qui le fera.** Les éditeurs qui seront agréés (les locaux : zBilling, GesCab, Omamori… et les gros : Sage,
Odoo). **Nous ne serons pas un éditeur agréé** — pas les moyens, pas le métier.

**Ce qu'on peut être :** le **technicien de quartier** qui, quand la liste sortira, **branche** les PME de Douala
sur la plateforme agréée de leur choix : diagnostic, choix, paramétrage du logiciel existant, mise en conformité
des mentions, formation, vérification. C'est un métier d'intégration — celui qu'on sait faire.

**Ce que ça coûte aujourd'hui : 0 FCFA.** Ce que ça demande : **une veille mensuelle** (publications DGI,
arrêtés, plateformes agréées) et **deux pages de méthode préparées d'avance** (diagnostic + checklist).

**Ce que ça peut rapporter :** chez nos concurrents, une mise en conformité se facture comme une mise en service
(plusieurs centaines de milliers de FCFA) ; sur 20 clients concernés, c'est un chiffre d'affaires à six chiffres
sans prospection nouvelle. **Mais aujourd'hui, on ne vend rien et on ne promet rien.**

**Verdict : un actif de veille, pas une offre.** Première revue le **23/10/2026**.

---

## 9 · Tableau de synthèse et l'ordre que je recommande

| | Offre | Existe déjà ? | Prix du marché | Notre prix possible | Marge | Verdict |
|---|---|---|---|---|---|---|
| **A** | Caisse + factures + stock | **Oui, partout** (10 éditeurs) | 0 à 25 000/mois | 200 000-400 000 + 20 000-35 000/mois **uniquement hors standard (A2)** | 50-60 % | ⛔ **Pas telle quelle** — revendre (A1) ou viser le hors-standard (A2) |
| **B** | Labo / clinique | **Oui** (Medica 65 cliniques, MediConnect, BoxyLab, Labores, OpenELIS) | 250 000 + 10 000/mois → 5 500 000 + 600 000/an | **400 000 + 35 000/mois (pilote)** | 60-70 % | 🟡 **Pilote sur 1 labo**, périmètre écrit, après visite |
| **C** | Contrat d'entretien | **Oui**, c'est le modèle du métier | 400 000-600 000/an (éditeurs santé) · hébergement 3 900-25 000/mois | **10 000/mois (page)** · **25 000-35 000/mois (instance)** | > 70 % | ✅ **À lancer maintenant**, dans chaque devis |
| **D** | Devis/facture PDF | Oui, inclus partout | — | 15 000-25 000 en option | — | ✅ **Pour nous d'abord**, vendu en option |
| **E** | Lien de facture WhatsApp | Les liens de paiement existent ; **le lien-facture prérempli non** | — | Inclus dans A2/B | — | ✅ **À construire une fois** |
| **F** | Site modifiable par le client | Oui (WordPress domine, 100 000) | 100 000-200 000 | 300 000+ (premium) | 50 % | ⚠️ **Plus tard**, et cher — sinon ça détruit l'offre C |
| **G** | Facture électronique (LF 2026) | Personne encore (specs non publiées) | inconnu | mise en conformité (à chiffrer) | ? | 🔭 **Veille**, revue le 23/10 |

**L'ordre que je recommande :**
1. **C — le contrat d'entretien.** Disponible dès le prochain client payé, coût quasi nul, et c'est la seule ligne
   qui répond au problème « on travaille beaucoup et on encaisse une fois ».
2. **D + E — notre outillage.** Le devis PDF et le lien-facture : ça rend C crédible et ça nous sert tous les jours.
3. **B — un pilote labo.** Un seul, périmètre étroit, prix plein, et une référence à la sortie.
4. **A1 — un appel à zBilling et MediConnect** pour demander leurs conditions de revendeur. 20 minutes, zéro risque.
5. **A2** seulement si un distributeur hors-standard se présente (aucune prospection pour ça).
6. **F** : jamais en standard. **G** : veille le 23/10.

**Les trois questions qui me manquent, et que seul King peut trancher :**
① Pour l'offre C, on annonce **10 000/mois** (page) — c'est le chiffre que je mettrais devant Le Cristallin et
Univers Optique **quand le gel sera levé** : tu valides ?
② Pour le pilote B, on part sur **quel laboratoire** — j'en prépare la visite et le cahier des charges ?
③ Est-ce que j'écris à **zBilling** et **MediConnect** pour demander leurs conditions de revendeur (message que
tu enverras, pas moi) ?

---

## 10 · Sources et ce qui reste à vérifier

**Sources principales (relevé du 23/09/2026)** : pages publiques de **zBilling, Nkap Control, GesCab Africa,
Omamori, Duka360, Invexcam, MediConnect Africa, CICASYS/Medica, BoxyLab, Camerbiz, ECS Informatique** ;
**Agence Ecofin** et **francophonieinnovation** (Labores) ; **openelis-global.org** et **lab-book.org** ;
**scidev.net** (Clinicaa) ; **pasteur-yaounde.org** (accréditation ISO 15189 par le SOAC, renouvelée en 2026) ;
**edicomgroup.com** et le **projet de loi de finances 2026 camerounais (dgb.cm)** pour la facture électronique ;
**CamPay** (2 %), **Fapshi** (3 %), **simiz.io** et **mmgate.org** pour les frais Mobile Money ; **WeComm** et
l'étude de marché agence web Douala 2026 pour la maintenance.

**Liens vérifiables :** `campay.net` · `fapshi.com` · `notchpay.co` · `simiz.io/blog/guide-paiement-mobile-cameroun-2026` ·
`nkapcontrol.com` · `zBilling (alivaon.com/blog/meilleurs-logiciels-gestion-commerciale-cameroun)` ·
`gescab-africa.com` · `omamori.cm` · `duka360.africa` · `mediconnect4africa.cloud` · `cicasys.co/produits/medica` ·
`boxylab.net` · `openelis-global.org` · `lab-book.org` · `scidev.net` (Clinicaa) · `pasteur-yaounde.org` (ISO 15189,
SOAC) · `edicomgroup.com/fr/blog/facturation-electronique-obligatoire-au-cameroun` · `dgb.cm` (projet de loi de
finances 2026) · `camerbiz.com` et `ecsinformatique.com` (prix locaux) · `agenceecofin.com` (Labores).

**Ce qui reste à vérifier avant de mettre un chiffre devant un client :**
- les **frais réels CamPay / Notch Pay** après compte marchand (les 2-3 % sont les tarifs publics, hors
  négociation) et le délai de reversement ;
- le **prix réellement payé** par un laboratoire de Douala aujourd'hui (aucune source publique : ça se demande
  en visite — question à poser telle quelle : « vous utilisez quoi pour vos résultats en ce moment ? ») ;
- l'existence d'un **programme revendeur** chez zBilling / MediConnect (à demander directement) ;
- la **date et les spécifications** de la facture électronique — veille du 23/10.
