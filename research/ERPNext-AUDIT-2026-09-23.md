# AUDIT — **Frappe / ERPNext** (le dépôt que King a envoyé)

**23/09/2026** · `github.com/frappe/erpnext` — lu **en clone filtré du dépôt réel** (5 611 fichiers), pas résumé
depuis une page marketing. Les chiffres de ce document sont mesurés, les licences sont lues dans les dépôts,
et tout ce que je n'ai pas vérifié est signalé comme tel (§9).

---

## 0 · La réponse en six lignes, pour King pressé

1. **C'est un vrai ERP, gratuit, mature et vivant** : 39 500 ★, dernière version stable **v16.35.0 le 15/09/2026**,
   549 types de documents, 186 rapports prêts, 77 modèles d'impression. Rien à voir avec un gadget.
2. **Mais ce n'est pas un outil pour nos 47 leads actuels.** Un opticien qui paie 150 000 FCFA pour être trouvé
   n'a pas besoin d'une comptabilité analytique multi-sociétés. Lui vendre ça aujourd'hui, c'est le perdre.
3. **Le Cameroun est déjà prévu, et c'est le point qui change tout** : le **plan comptable SYSCOHADA camerounais
   (1 329 comptes, avec codes) est dans le dépôt**, et l'assistant d'installation applique la **TVA 19,25 %**.
   Un comptable de Douala reconnaît ses comptes. Ce n'est pas nous qui l'avons écrit, c'est offert.
4. **Ce qui manque décide de tout** : **aucun Mobile Money** (ni MTN MoMo, ni Orange Money, ni CinetPay/Flutterwave),
   **aucun WhatsApp natif**, un hébergement **sur serveur** (pas Vercel), et une interface française à **~50 %**.
5. **Ce n'est donc pas un « produit » à vendre, c'est un métier à ajouter** — un back-office (caisse, stock,
   factures, dossier patient) pour un **autre profil de client** que celui d'aujourd'hui : 10 à 30 employés,
   multi-site, qui facture tous les jours. Prix : **250 000 à 600 000 FCFA de mise en service + un abonnement
   mensuel**, pas 150 000 une fois.
6. **Trois choses à garder même si on ne vend rien** : le **modèle économique** (héberger et entretenir =
   revenu récurrent, c'est exactement ce que nous cherchions), le **PDF de facture à notre marque**, et
   l'idée **« le lien de facture qui s'ouvre dans WhatsApp »**. Détail §7.

---

## 1 · Ce que j'ai réellement lu (preuves)

| Mesure | Valeur | Comment je l'ai obtenue |
|---|---|---|
| Étoiles / activité | **39 496 ★** · dernier commit **le jour même** | API GitHub |
| Version lue | `17.0.0-dev` (branche `develop`) | `erpnext/__init__.py` du clone |
| Versions stables | **16.35.0** (15/09/2026) · **15.121.3** (15/09/2026) | releases GitHub + branches `version-15/16` |
| Volume | 5 611 fichiers · ~157 000 lignes de Python · ~85 000 de JS | `git ls-tree` + `wc -l` |
| Types de documents (doctypes) | **549** — comptes 195 · stock 82 · fabrication 50 · paramétrage 43 · CRM 28 · ventes 22 · achats 20 | comptage des `doctype/*.json` |
| Rapports prêts à l'emploi | **186** | arborescence `*/report/` |
| Modèles d'impression | **77** | arborescence `print_format/` |
| Langues | **39** fichiers de traduction ; **FR : 47 % (ERPNext)** et **73 % (framework)** | `locale/fr.po`, comptage des `msgstr` vides |
| Python requis (branche develop) | **≥ 3.14** — signe qu'il ne faut **pas** déployer `develop` | `pyproject.toml` |

**Ce que je n'ai pas fait :** je n'ai **pas installé** l'application (le bac à sable a 3 Go de RAM, pas de
MariaDB, pas de Docker — et une démo installée ici disparaîtrait avec le bac). Ma conclusion sur la difficulté
d'installation vient de la documentation et du déploiement officiel, pas d'un essai (§9).

---

## 2 · Les licences — c'est ça qui décide de ce qu'on peut vendre

Lues dans les dépôts, une par une :

| Application | Licence | Ce qu'on peut en faire |
|---|---|---|
| **ERPNext** (le cœur ERP) | **GPL-3.0** | L'utiliser, le modifier, l'héberger pour un client. Si on **distribue** une version modifiée, on doit fournir le code source. |
| **Frappe Framework** (le moteur) | **MIT** | Presque tout, y compris le fermé. C'est la brique « libre ». |
| **Frappe Builder** (constructeur de sites) / **Payments** / **frappe_docker** | **MIT** | Idem — utilisables librement. |
| **Frappe CRM**, **Helpdesk**, **Books**, **Insights**, **LMS**, **Print Designer** | **AGPL-3.0** | Attention : voir ci-dessous. |
| **Frappe HR** (RH + paie) | **GPL-3.0** | Utilisable ; aucune paie camerounaise intégrée (§5). |
| **Marley / « healthcare »** (dossier patient, labo) | **GPL-3.0** (Earthians, actif) | Utilisable pour un client clinique/labo. |

**La clause qui compte : AGPL §13.** Si on **modifie** une app AGPL et qu'on la fait tourner **pour des
utilisateurs qui y accèdent par le réseau**, on doit leur **offrir le code source correspondant**. Traduit en
règle pour nous, sans jargon :

- **Une instance par client, chez le client** → aucun problème. C'est son outil, s'il demande les sources, on
  les lui donne (elles sont publiques de toute façon).
- **Un service multi-clients où plusieurs clients accèdent à la même instance modifiée** → tout utilisateur
  peut demander nos modifications. Autrement dit : **on ne garde pas de « recette secrète » dans du AGPL.**
  Ce qu'on vend, ce n'est pas le code : c'est l'installation, les réglages, la formation et l'entretien.
- **On ne promet jamais à un client un logiciel « fermé, à nous »** construit sur du AGPL. Si un jour un client
  veut absolument du fermé, on écrit ce bout-là **au-dessus de l'API** (nos pages, nos scripts) — pas dedans.

**Marque (TRADEMARK_POLICY.md, lu dans le dépôt) :** « ERPNext » et son logo appartiennent à Frappe
Technologies. On **peut** écrire « nous installons et configurons ERPNext » ; on **ne peut pas** mettre
« ERPNext » dans un nom d'entreprise, de produit ou de domaine, ni dans de la publicité. Concrètement : **notre
offre a son propre nom, et ERPNext est la technologie en dessous.** (C'est aussi mieux commercialement.)

---

## 3 · Le Cameroun est déjà prévu — le point qui change la donne

C'est la découverte de cet audit, et elle n'est pas dans les pages de vente :

| Ce que j'ai trouvé dans le dépôt | Preuve | Pourquoi ça compte |
|---|---|---|
| **`cm_plan_comptable` + `cm_plan_comptable_avec_code`** — plan comptable **SYSCOHADA du Cameroun**, dossier `verified/` | 1 329 numéros de comptes ; arborescence « Comptes de ressources durables », « Comptes de tiers », « Comptes de trésorerie », « Comptes de charges/produits des activités ordinaires » | Un comptable de Douala lit directement ses comptes SYSCOHADA. **Aucun développement, aucun mapping à inventer.** |
| **TVA camerounaise pré-remplie** : `{"Cameroon Tax": {"account_name": "VAT", "tax_rate": 19.25}}` | `setup/setup_wizard/data/country_wise_tax.json` (170 pays) | Le bon taux, dès l'installation. C'est le chiffre que tout le monde se trompe à saisir. |
| **Comptes de TVA dans le plan** (« TVA facturée sur ventes », « TVA récupérable sur achats »…) | fichier du plan camerounais | La déclaration de TVA sort de la comptabilité, sans tableur parallèle. |
| **Toute la zone CEMAC est couverte** : Cameroun, **Tchad, Gabon, Congo, RCA, Guinée équatoriale** (plus Bénin, Togo, Mali, Niger, Burkina, Sénégal, Côte d'Ivoire, RDC, Comores) | dossiers `chart_of_accounts/verified/` | La même installation sert pour un client qui a une filiale à Libreville ou N'Djamena. Argument de vente rare ici. |
| **Interface française : ERPNext 47 %, framework 73 %** | comptage des chaînes des `fr.po` | ⚠️ **Les revendeurs qui écrivent « entièrement traduit en français » exagèrent.** Le vrai travail de traduction d'une quinzaine d'écrans métier (facture, caisse, stock, patient) **est un service qu'on peut facturer** — et il reste utile au client, pas à nous. |

**Ce qui n'existe pas :** la **paie camerounaise** (CNPS, IRPP, DIPE, DSF). Aucun module. Un concurrent de Douala
(Y-Note) l'a développé **sur Odoo**, ce qui prouve à la fois que le besoin est réel et que c'est un métier à
part entière, avec de la responsabilité légale. **On ne vend pas la paie.**

---

## 4 · Ce qui existe, et le problème réel que ça règle chez un client

Traduction : la colonne de gauche est dans la boîte, la colonne du milieu est le problème, la colonne de droite
est un client ou un prospect **déjà dans notre CRM**.

| Ce que ça fait | Le problème réel à Douala | Pour qui, chez nous |
|---|---|---|
| **Devis → facture → acompte → solde → reçu** | Le carnet, les photos de reçus, « je te paie la semaine prochaine » | L'Opticien, Le Cristallin, Univers Optique, MITOC, Skye, YAKS |
| **Caisse (POS) + clôture de caisse** | La caisse du soir qu'on recompte à l'aveugle ; les écarts | Commerces, opticiens, pharmacies |
| **Stock + lots + dates de péremption + numéros de série** | Les réactifs périmés au fond du frigo ; les montures qu'on croit avoir | **Labiomed, ScientiLabo, KYLAYA, Bioscan, Biodiagnostics, Interlabo** (labos du CRM), pharmacies |
| **Achats + fournisseurs + commandes** | Les commandes passées par WhatsApp et perdues dans le fil | Labs, cliniques, distributeurs |
| **Abonnements + relances d'impayés (`subscription`, `dunning`)** | Les clients mensuels qui oublient, et les appels gênants | Notre propre abonnement d'hébergement · un labo qui facture une entreprise chaque mois |
| **Contrats d'entretien + SLA + réclamations (`Issue`, `Service Level Agreement`, `Warranty Claim`)** | « Le client appelle trois fois et personne ne note » | Nous — et tout prestataire qui a du matériel chez le client |
| **Qualité : non-conformités, procédures, revues (`quality_management`, 16 documents)** | La démarche d'accréditation d'un laboratoire, tenue dans des classeurs Word | Un labo qui vise une accréditation (argument fort, mais pas un premier achat) |
| **Immobilisations + entretien du matériel** | La machine à échographie dont personne ne sait quand elle a été révisée | Cliniques, labs, tout client avec du matériel |
| **Portail client + formulaires web** | Le client qui veut « juste son relevé » et qui dérange la secrétaire | Labs et cliniques avec des clients entreprises |
| **186 rapports prêts** (ventes, stock, TVA, créances, caisse) | Le gérant qui ne sait pas combien il a vendu hier | Tous — c'est souvent le déclencheur d'achat |
| **Dossier patient / examens / échantillons / résultats** — app **Marley**, 137 documents : `patient`, `appointment`, `lab_test`, `lab_test_sample`, `observation`, `observation_reference_range`, `drug_prescription`… | Le dossier papier qu'on ne retrouve pas ; le résultat envoyé par photo | **UNI-LABO, Labiomed, Pathcare Diagnostics, Bonanjo, OraCare, Polyclinique Innova, CMODN** |

---

## 5 · Ce qui n'est PAS dans la boîte (à ne jamais promettre)

C'est la partie qui évite de perdre un client et notre réputation.

**① Aucun Mobile Money.**
Les passerelles réellement supportées sont : Razorpay, Stripe, PayPal, Braintree, GoCardless, **M-Pesa (Kenya,
en shillings)**, Paytm, Paymob. **Pas de MTN MoMo, pas d'Orange Money, pas de CinetPay, PayDunya ni
Flutterwave.** Donc : on n'annonce **jamais** « vos clients paient en ligne ». Ce qu'on fait à la place, et qui
couvre 80 % du besoin réel : on crée deux **modes de paiement « MTN MoMo » et « Orange Money »**, on y saisit
la **référence de la transaction** (celle du SMS), et l'encaissement est juste dans la comptabilité. Le client
arrête de chercher dans WhatsApp qui a payé quoi.

**② Aucun WhatsApp natif.**
ERPNext ne stocke le WhatsApp que comme un **champ** (« WhatsApp No ») sur les fiches. L'envoi réel passe par
l'app communautaire **`frappe_whatsapp`** (Meta Cloud API), que le CRM officiel de Frappe utilise aussi. Mais
côté client ça impose : **un numéro dédié** (donc pas le numéro actuel du cabinet), une **vérification Meta**,
des **modèles de messages à faire approuver**, et un **coût par conversation**.
→ **Pour nos clients actuels : non.** Notre force, `wa.me` avec un texte prérempli, reste meilleure et gratuite.
→ **Pour un gros client** (clinique multi-sites, distributeur) : oui, **en option payante**, et c'est un vrai
projet à part (2 à 5 jours), pas un réglage.

**③ La caisse hors ligne : attention au piège.**
Le POS standard **a besoin d'internet pour se charger** (« il est rapide, mais pas *vraiment* hors ligne » —
c'est écrit noir sur blanc dans leur forum). Le vrai hors-ligne existe dans des apps communautaires
(**POSNext**, **POS Awesome**). On ne vend donc **pas** « la caisse marche sans réseau » sans tester la
connexion du client d'abord. C'est exactement le genre de promesse qui se paie en appel téléphonique.

**④ L'hébergement : un serveur, pas Vercel.**
Il faut un VPS (2 cœurs / 4 Go confortable) avec MariaDB et Redis, soit géré par nous (**4 à 10 h/mois de
travail réel**, de l'aveu même du marché), soit chez **Frappe Cloud** (à partir de **5 $/site/mois**, puis
10/25/50 $ selon la charge — sources tierces, à revérifier). Deux questions à trancher **avant** de vendre :
**qui paie ce serveur, et avec quel moyen de paiement** (une carte étrangère ; MoMo ne paie pas un VPS).

**⑤ L'interface n'est française qu'à moitié** (mesuré : 47 % / 73 %) — et un ERP à moitié anglais, pour une
secrétaire de quartier, c'est un refus d'usage. Seule réponse honnête : **on traduit les écrans qui servent**,
pour ce client, avant de former.

**⑥ Le vrai risque : ce n'est pas un site.** Un ERP mal cadré = le gérant qui appelle tous les jours. Notre
forfait page (100 000-150 000 FCFA) **ne couvre pas** ce travail, et une remise là-dessus nous tuerait (§6).

---

## 6 · Ce qu'on peut vendre — trois offres, dans l'ordre, avec les vrais chiffres

> ⚠️ **Aucun prix n'est posé à un client sans ton accord** (règle en vigueur). Les montants ci-dessous sont des
> **propositions argumentées**, calculées à partir du coût réel et de la concurrence locale, à valider par toi.

**D'abord, la vérité sur le marché :** le Cameroun a des intégrateurs ERP installés (**IPLANS** à Douala,
**LocalHost Digital** et **E-Business Cameroun** sur **Odoo**, **Y-Note** avec ses modules CNPS/DIPE/DSF). Ils
vendent à des **entreprises**, pas à des boutiques. **Aucun de ces concurrents ne vend une page web à
150 000 FCFA.** Nous, oui — et c'est notre porte d'entrée : on connaît déjà le quartier, le client, et sa
vitrine. **La page reste le produit d'appel ; le back-office est la suite.**

### Offre A — « La caisse, les factures et le stock » (commerce / opticien, 3 à 8 employés)
- **Pour qui** : un opticien ou une boutique qui vend déjà tous les jours, encaisse en espèces et MoMo, et tient
  son stock de tête. *(Candidats déjà dans le CRM : MITOC, L'Opticien, Skye, YAKS — et Le Cristallin, Univers
  Optique **seulement après** leur premier paiement, une fois le gel levé.)*
- **Ce qu'on livre** : installation, plan comptable **SYSCOHADA Cameroun**, TVA 19,25 %, ses articles et ses
  montures, **2 modes de paiement MoMo/Orange**, une caisse (1 poste), la facture à son logo, **2 h de
  formation**, et les sauvegardes.
- **Ce que ça nous coûte** : 3 à 5 jours de travail, un VPS (≈ **6 000 à 12 000 FCFA/mois**).
- **Proposition** : **250 000 FCFA** de mise en service (50 % d'acompte, comme toujours) + **25 000 FCFA/mois**
  (hébergement, sauvegardes, mises à jour, 1 h d'aide).
- **Ce qui tue l'affaire** : un client qui n'a pas d'ordinateur, ni de connexion le soir, ni quelqu'un capable
  de saisir deux lignes. **À vérifier en visite avant de proposer quoi que ce soit.**

### Offre B — « Le dossier, les résultats et les factures » (laboratoire / clinique, 10 à 30 employés)
- **Pour qui** : un laboratoire privé ou une clinique **avec 2 sites ou plusieurs praticiens** — la paperasse y
  coûte déjà plus cher qu'un abonnement. *(Candidats dans le CRM : UNI-LABO, Labiomed, ScientiLabo, KYLAYA,
  Bioscan, Pathcare Diagnostics, Bonanjo, OraCare, Polyclinique Innova, CMODN.)*
- **Ce qu'on livre** : **Marley** (dossier patient, examens, échantillons, résultats, prescriptions) **+ ERPNext**
  (facturation, encaissements, stock et lots de réactifs, rapports), écrans traduits, **formation par poste**.
- **Ce que ça nous coûte** : 5 à 10 jours, et un vrai risque d'appels. Un VPS plus gros (≈ 12 000-20 000 FCFA/mois).
- **Proposition** : **450 000 à 600 000 FCFA** de mise en service + **40 000 FCFA/mois**.
- **Pourquoi ça peut marcher ici** : c'est le seul segment où le client **facture tous les jours** et où la
  « qualité » (§4) est un argument, pas un luxe.
- **Pourquoi je ne le mettrais pas en premier** : c'est un métier de santé. Si le dossier patient est mal
  installé et qu'un résultat se perd, ce n'est plus une histoire de site web.

### Offre C — « L'entretien mensuel » (le vrai revenu, quel que soit le client)
Hébergement + sauvegardes vérifiées + mises à jour + 1 h d'aide par mois + **contrat d'entretien daté**.
**25 000 à 40 000 FCFA/mois.** C'est **ça** qu'on garde : dix clients entretien = 250 000 à 400 000 FCFA/mois
qui rentrent sans démarcher. C'est la première fois qu'on a un modèle de revenu **récurrent** crédible — et il
s'applique **aussi** aux pages qu'on vend déjà (hébergement de la page + corrections, 10 000-15 000 FCFA/mois).

### Et pour nos 47 leads actuels ? **Rien de tout ça.**
Un opticien qui cherche à être trouvé achète **une page**. Lui proposer un ERP, c'est le confondre avec son
fournisseur. **La séquence correcte est : la page d'abord, le back-office six mois plus tard, quand il a
quelqu'un pour le tenir.** On ne mélange pas les deux dans le même message.

---

## 7 · Ce qu'on garde pour nous — même si on ne vend rien (le plus rentable de cet audit)

1. **Le modèle économique.** Frappe ne vend pas de licences : elle vend **l'hébergement, les sauvegardes et les
   mises à jour**, tous les mois. Exactement ce qui manquait à AMK. **À copier tel quel** : nos pages, puis nos
   outils, vendus avec un abonnement d'entretien (§6-C).
2. **Le PDF de facture / devis / reçu à notre marque.** Le **Print Designer** permet de dessiner un modèle
   propre (logo AMK, mentions, acompte). Aujourd'hui nos devis sont du **texte** dans WhatsApp. Un PDF à notre
   nom, joint au message, change la perception de l'agence **dès le prochain client**, et c'est aussi un petit
   service vendable (25 000 FCFA) à un client qui veut ses factures à son logo.
3. **« Le lien de facture qui s'ouvre dans WhatsApp »** — notre idée à nous, pas celle de Frappe : la facture
   est **hébergée** par le système, le message WhatsApp contient un lien `wa.me` prérempli, le client clique,
   voit la facture, la télécharge. Pas besoin de l'API Meta, pas de coût par message, et ça marche **avec le
   numéro que le client a déjà**. C'est notre signature technique (comme la page avant le paiement) et ça se
   vend à tous les métiers qui facturent.
4. **Le pattern « réglages pays en données »** (`country_wise_tax.json`) : les règles locales (taux, comptes,
   mentions) vivent dans un fichier, pas dans du code. À reprendre pour nos propres outils — un jour, « AMK
   Cameroun preset » pour n'importe quel logiciel qu'on installe.
5. **Frappe Builder (MIT)** : un constructeur de sites visuel. Si un jour un client veut **modifier son site
   lui-même**, c'est la brique à poser — et ça ne nous coûte rien en licence.
6. **`frappe_docker`** : la façon propre de déployer un outil chez un client (une commande, des sauvegardes,
   une mise à jour). C'est le squelette de l'offre C.

---

## 8 · Les trois décisions que je te demande

1. **On ouvre ce chantier, oui ou non — et jusqu'où ?**
   (a) **Non** : je clos le sujet, on garde seulement les idées du §7. (b) **Une démo** : je monte une instance
   publique avec des **données inventées** d'opticien ou de labo, pour la montrer en rendez-vous — c'est un
   VPS de 5 $/mois et 2 heures de travail. (c) **Un pilote** sur un vrai client, à prix réduit mais **pas
   gratuit** — jamais gratuit : un pilote gratuit s'arrête quand on s'en lasse.
2. **Qui paie le serveur, et avec quoi ?** Frappe Cloud ou un VPS ne se règlent pas en Mobile Money. Si tu as un
   moyen de payer en devises, c'est réglé ; sinon, il faut trouver un hébergeur local, et je te dirai franchement
   que ça complique tout.
3. **Quel profil pour la démo — labo/clinique ou commerce ?** Je ne peux pas faire les deux. Le **labo** est plus
   impressionnant (dossier patient + résultats), le **commerce** est plus facile à vendre et à tenir.

---

## 9 · Annexe — la recette technique (si tu dis oui) et ce que je n'ai PAS vérifié

**La recette, en clair** (pour un VPS Debian/Ubuntu, 2 cœurs et 4 Go de RAM) :
`docker` + `frappe_docker` → site neuf → **version stable 16** (jamais `develop`) → assistant : **pays = Cameroun**
→ **plan comptable : `cm_plan_comptable_avec_code`** (SYSCOHADA, 1 329 comptes) → vérifier la **TVA 19,25 %** →
créer les modes de paiement **MTN MoMo** et **Orange Money** → traduire les écrans qui serviront → former.
Ordre de grandeur : une demi-journée pour une instance propre et sauvegardée, hors personnalisation client.

**Ce que je n'ai pas vérifié, et qu'il faudra vérifier avant de promettre :**
- je n'ai **pas installé** l'application (bac à sable : 3 Go de RAM, ni MariaDB ni Docker) — donc « une
  demi-journée » est une estimation de documentation, pas un essai ;
- les **prix de Frappe Cloud** viennent de pages tierces (5 $/10 $/25 $/50 $ par site et par mois) : à confirmer
  sur `frappe.io` avant d'écrire un chiffre à un client ;
- **Marley** (santé) : dépôt actif (dernière mise à jour le 22/09/2026) et compatible « Frappe/ERPNext », mais je
  **n'ai pas testé l'installation** ni la compatibilité exacte avec la version 16 ;
- le **coût réel de l'API WhatsApp de Meta** (par message, par conversation) en FCFA : non vérifié ;
- les **tarifs des intégrateurs de Douala** : je n'ai lu que leurs pages publiques, aucune offre chiffrée.

**Sources principales :** le dépôt `frappe/erpnext` cloné (branche `develop`, 23/09/2026) ; les dépôts
`frappe/{frappe,crm,helpdesk,hrms,books,builder,insights,lms,payments,print_designer,frappe_docker}` et
`earthians/marley` (licences et métadonnées lues via l'API GitHub) ; la documentation de l'app Payments ; les
forums Frappe (POS hors ligne, WhatsApp) ; pages publiques d'intégrateurs ERP au Cameroun.
