# L'ORDRE DES OFFRES, EXPLIQUÉ — **quel problème on règle, à chaque étape**

**23/09/2026** · complément à `research/ETUDE-OFFRES-LOGICIEL-2026-09-23.md` §9 · la question de King :
« je voudrais plus d'explication sur l'ordre que tu recommandes — **which problem are we solving ?** »

---

## 0 · La réponse en une phrase

**Nous ne réglons pas d'abord le problème du client. Nous réglons d'abord le nôtre — et nous ne touchons au
problème du client que là où il paie déjà pour le résoudre.**

Notre problème n° 1 est simple et il est mesurable : **nous vendons 150 000 FCFA une fois, puis nous
travaillons gratuitement.** Tant que ça n'est pas corrigé, tout ce qu'on ajoute (un ERP, un logiciel labo,
un site modifiable) **aggrave le problème** : plus d'outils à installer, plus de clients à dépanner, toujours
un seul paiement à l'entrée.

L'ordre C → D/E → B → A1 → A2 → F/G est donc un ordre **de coût croissant et de risque croissant**, où
chaque étape **finance et rend crédible** la suivante. Ce n'est pas un menu.

---

## 1 · Les quatre problèmes, à ne pas confondre

Chaque offre mélange en réalité quatre problèmes différents. Les confondre, c'est exactement ce qui fait
qu'on se retrouve à vendre un ERP à un opticien.

| # | Le problème | Qui le subit | Ce qui le règle | Quand |
|---|---|---|---|---|
| **P1** | **Pas de revenu qui revient.** Un client payé une fois est un client terminé ; il faut démarcher à nouveau pour le mois suivant | **Nous** | L'abonnement (offre C) | **maintenant** |
| **P2** | **Le travail d'après n'est pas payé.** Chaque page livrée crée du support gratuit à vie | **Nous** | L'abonnement + le périmètre écrit (C, puis B) | **maintenant** |
| **P3** | **Le client ne sait pas** : ce qui est en stock, qui lui doit de l'argent, où est le résultat d'analyse | **Le client** | Un outil de gestion — **que nous n'avons pas à construire** (A1, A2, B) | quand il paie déjà pour ça |
| **P4** | **Le client n'est pas trouvé** | **Le client** | La page — **notre produit actuel, déjà vendu deux fois** | déjà en cours |

**Ce que dit ce tableau :** P1 et P2 sont **nos** problèmes et ils se règlent **cette semaine**, sans
technologie. P3 est le problème du client, et il se règle **avec l'argent qu'il dépense déjà** — pas avec
nos économies. P4 est notre porte d'entrée : c'est la seule chose que nous savons vendre aujourd'hui, et
c'est par elle que passent les trois autres.

---

## 2 · Le filtre qui donne l'ordre

Chaque offre est passée au même crible. Quatre questions, dans cet ordre :

1. **Est-ce que ça règle P1 ou P2 ?** (Si non → ce n'est pas prioritaire, quel que soit le marché.)
2. **Est-ce qu'on peut le vendre cette semaine, avec ce qu'on a ?** (Sinon → ça attend.)
3. **Combien ça nous coûte en jours, en argent et en risque ?**
4. **Est-ce que ça produit une référence qui rend la suite plus facile ?**

| Offre | Règle P1/P2 ? | Vendable cette semaine ? | Coût pour nous | Produit une référence ? | Rang |
|---|---|---|---|---|---|
| **C** Entretien mensuel | **Oui — les deux** | **Oui** (sur les affaires déjà sur la table) | ~0 FCFA, 1-2 h/mois par client | Non, mais **rend tout vendable** | **1** |
| **D/E** Devis PDF + lien facture | Non directement, mais **rend C possible** | Oui | 2-4 jours, une fois | Non | **2** |
| **B** Labo / clinique | **Oui** (abonnement 35 000/mois) | Non — visite + périmètre écrit d'abord | 6-8 jours, risque réel | **Oui — la référence santé** | **3** |
| **A1** Revendre zBilling / MediConnect | **Oui, faiblement** | Oui (un appel) | 20 minutes | Non | **4** |
| **A2** Hors-standard (multi-dépôts) | Oui | Non — il faut qu'un tel client se présente | 5-10 jours par projet | Oui, mais tardive | **5** |
| **F** Site modifiable par le client | Non — **il détruit P2** | Oui, mais cher | 2-3 jours | Non | **6** |
| **G** Facture électronique | Non, pas encore | **Impossible** (specs non publiées) | 30 min/mois de veille | Non | **veille** |

---

## 3 · Étape par étape : quel problème, et pourquoi ici

### ① C — le contrat d'entretien · **le problème P1, notre survie**

**Le problème réglé :** nous n'avons pas de rentrée d'argent qui se répète. Aujourd'hui, un client satisfait
est un client **terminé**.

**Pourquoi en premier :** c'est la seule offre qui ① se vend **sur des affaires déjà sur la table** (aucune
prospection, aucun lead nouveau), ② ne coûte **rien** en développement, ③ **le marché paie déjà** (les
éditeurs santé facturent 400 000 à 600 000 FCFA/an de maintenance ; l'hébergement local va de 3 900 à
25 000 FCFA/mois), et ④ **corrige la cause** de notre fatigue, pas la conséquence.

**Le chiffre directement disponible, sans démarcher :**

| Client déjà sur la table | Abonnement proposé | Par an |
|---|---|---|
| Le Cristallin (150 000 payés en cours) | 10 000/mois | 120 000 |
| Univers Optique (100 000, RDV vendredi) | 10 000/mois | 120 000 |
| UNI-LABO (150 000, RDV vendredi) | 10 000 → 25 000/mois si l'instance héberge les résultats | 120 000 → 300 000 |
| **Total prudent** | **30 000/mois** | **360 000 FCFA/an** |

**Ce qui doit être vrai pour que ça marche :** on livre réellement les 2 h/mois **et les sauvegardes
vérifiées**. Un abonnement non tenu est pire qu'un abonnement vendu — il transforme un client content en
client qui parle mal de nous.

**Signal d'échec :** au bout de 3 mois, si on n'a pas livré les 2 h promises, on **réduit le périmètre
écrit** (et on baisse le prix) — on ne fait pas semblant.

**Ce qui ne change pas :** le prix de la page reste **100 000 / 150 000**, jamais remisé. L'abonnement est
**une ligne de plus**, pas une réduction déguisée.

---

### ② D + E — notre outillage (devis PDF, lien de facture WhatsApp) · **le problème P2, côté crédibilité**

**Le problème réglé :** on ne peut pas vendre un abonnement avec un devis écrit dans WhatsApp. Un
prélèvement mensuel exige **un document** : un devis qui montre la ligne mensuelle, un reçu pour chaque
paiement MoMo, et une façon de l'envoyer qui ne ressemble pas à une faveur.

**Pourquoi juste après C :** parce que **C est impossible à tenir sans ça**. C'est l'infrastructure de C,
pas un projet séparé. Et ça se fait **une fois** pour tous les clients.

**Coût :** 2 à 4 jours, 0 FCFA de logiciel. **Rapport :** immédiat sur notre crédibilité, et ça se revend en
option (15 000-25 000 FCFA) à un client qui veut ses factures à son logo.

**Signal d'échec :** aucun — c'est du travail interne, il faut juste le faire.

---

### ③ B — le pilote laboratoire · **le problème P3 du client, là où notre prix tient**

**Le problème réglé (chez le client) :** un laboratoire de Douala travaille sur des fiches pré-imprimées et
des carnets. Le résultat se perd, l'échantillon ne se retrouve pas, personne ne sait ce que les clients
entreprises doivent, et tout ce qui prouverait une démarche qualité est en papier.

**Pourquoi ici et pas avant :** c'est **la seule offre dont notre prix tient** (les concurrents vont de
250 000 FCFA + 10 000/mois à 5 500 000 FCFA), mais c'est aussi **la plus lente et la plus risquée** :
① nous n'avons **aucune référence santé**, ② il faut une visite, un cahier des charges écrit et des
sauvegardes vérifiées **avant** la mise en service (si l'outil tombe, le laboratoire s'arrête), ③ un échec
ici brûle un prospect qu'on ne remplacera pas.

**Pourquoi il vient après C et D/E :** ① on a besoin de la machine à facturer un abonnement pour le vendre
proprement, ② il arrive **par la porte de la page** (plusieurs de nos labos ont reçu ou acheté une page :
UNI-LABO est en ligne), ③ et surtout il **produit la référence** qui rendra le deuxième labo et la première
clinique deux fois plus faciles à convaincre.

**Coût :** 6 à 8 jours + un serveur plus solide (10 000-15 000/mois). **Proposition :** 400 000 + 35 000/mois
(périmètre écrit : résultats + factures + encaissements MoMo, 2 postes, 3 h de formation). Ce n'est pas une
remise, c'est **un périmètre plus petit**.

**Signal d'échec :** pendant l'essai, si personne au laboratoire ne saisit, ou si la connexion tombe trois
fois par semaine, **on s'arrête avant la mise en service complète**. On ne prend pas un client dans un
bâtiment qu'il ne peut pas tenir.

---

### ④ A1 — revendre zBilling / MediConnect · **le problème P3, sans le construire**

**Le problème réglé :** un commerçant nous demande « et la caisse, et le stock ? » — et la réponse honnête
aujourd'hui est : **ce marché est déjà servi, moins cher que nous** (Nkap Control est gratuit puis 3 000/mois
avec le Mobile Money inclus, zBilling est à 10 000/mois). On ne construit pas là-dedans : **on prend une
commission sur quelqu'un qui l'a déjà fait**.

**Pourquoi quatrième :** c'est une **décision de 20 minutes pour un gain faible** (10-25 % d'un abonnement de
10 000 = 1 000 à 2 500 FCFA/mois par client). Ça vaut le coup si c'est gratuit et rapide ; ça ne vaut pas une
journée de travail.

**Signal d'échec :** si la commission proposée est sous 10 % **et** sans support de leur part, on laisse
tomber — le temps de vente dépasserait le gain.

---

### ⑤ A2 — le hors-standard · **le problème P3, quand le standard casse**

**Le problème réglé :** multi-dépôts, ventes à crédit avec échéanciers, commissions des commerciaux,
tournées d'encaissement. Là, les SaaS locaux cèdent — et là, **notre prix se défend**
(200 000-400 000 + 20 000-35 000/mois).

**Pourquoi cinquième :** on **ne prospecte pas pour cette offre**. Elle n'existe que si un distributeur, un
grossiste ou une quincaillerie se présente avec ces symptômes. Sinon c'est un devis à rédiger pour rien.

---

### ⑥ F — le site que le client modifie lui-même · **à ne pas faire maintenant**

**Le problème réglé (chez le client) :** il veut changer un prix sans nous appeler.

**Le problème créé (chez nous) :** le jour où il modifie tout seul, **il ne nous appelle plus** — on perd les
retouches **et** on garde le support quand il casse la mise en page. C'est la seule offre de la liste qui
**détruit P2**, c'est-à-dire la raison d'être de l'abonnement.

**Verdict :** uniquement **premium** (300 000 FCFA et plus, avec formation), et **plus tard**. Notre revenu
futur, c'est l'abonnement, pas l'autonomie du client.

---

### ⑦ G — la facture électronique · **la veille, pas l'offre**

**Le problème réglé :** il n'existe pas encore aujourd'hui. La loi de finances 2026 impose la facture
électronique (modèle temps réel, plateformes agréées, transmission continue), mais **les spécifications et
la liste des prestataires agréés ne sont pas publiées**.

**Pourquoi en veille :** parce qu'on **ne promet jamais « conforme DGI »** sur un texte dont les modalités
techniques n'existent pas. On garde un œil (30 minutes par mois) et on prépare les deux pages de méthode —
le jour où la liste sort, des milliers d'entreprises au régime du réel devront changer d'outil de
facturation, et ce sera un métier d'intégration, celui qu'on sait faire.

**Rendez-vous : 23/10/2026.** Si rien n'est publié, on repousse d'un mois, sans forcer.

---

## 4 · Ce qu'on ne fait PAS — et pourquoi c'est ce qui protège l'ordre

| On ne fait pas | Parce que |
|---|---|
| **Lancer un produit logiciel** | On n'a ni les moyens d'un éditeur, ni l'envie de porter la responsabilité de la comptabilité de quelqu'un d'autre. On installe, on configure, on forme, on entretient. |
| **Prospecter pour vendre un ERP** | Un opticien qui cherche à être trouvé achète **une page**. Lui proposer un ERP, c'est le confondre avec son fournisseur. |
| **Toucher au Cristallin et à Univers** | **Gel décidé par King** : rien ne bouge avant le paiement. L'abonnement se proposera **au moment de la livraison payée**, pas avant — le client du Cristallin a dit « ne change rien sans mon ok ». |
| **Reprendre la production de contenu** | Décision de King : on ne poste plus. Les heures vont à la prospection et à l'encaissement. |
| **Baisser un prix pour gagner un client** | Règle AMK : jamais de remise, **on ajuste le périmètre**. |

---

## 5 · Le tunnel, en une image

```
   LA PAGE                     L'ABONNEMENT                 L'OUTIL
   (aujourd'hui)               (cette semaine)              (ce mois-ci)

   100 000 / 150 000     →     10 000 / mois           →    400 000 + 35 000/mois
   ouvre la porte              paie les factures            le métier suivant
   P4 : « on me trouve »       P1 + P2 : ça se répète       P3 : le client « sait »
```

**Pourquoi dans cet ordre, et jamais l'inverse :** la page est la **seule porte** que nous savons ouvrir (deux
rendez-vous vendredi, deux prix posés). L'abonnement est ce qui **transforme cette porte en rente**. L'outil
est ce qui **élargit le métier** — mais il ne peut s'ouvrir qu'une fois qu'on encaisse et qu'on facture
proprement. **Un labo achète plus volontiers un outil à quelqu'un qui a déjà livré sa page et qui lui envoie
une facture PDF.**

---

## 6 · Les trois dépendances qui peuvent casser l'ordre

1. **L'argent de vendredi doit rentrer.** Univers 10 h, UNI-LABO 14 h 30 : 250 000 FCFA sur la table. **Sans
   ça, tout ce document est de la théorie.** C'est la priorité absolue de la semaine.
2. **Le pilote B exige une visite**, pas un message WhatsApp. Tant que la visite n'est pas faite, je ne peux
   préparer qu'un cahier des charges, pas un devis.
3. **L'abonnement doit être livré**, mois après mois. C'est la seule chose qui, si elle est mal faite, nous
   coûte un client — et notre réputation se construit précisément sur le contraire.

---

## 7 · Ce que je propose comme prochaine action, de chaque côté

**King :** ① les deux rendez-vous de vendredi (Univers 10 h, UNI-LABO 14 h 30) et l'encaissement ;
② valider le principe de l'abonnement à 10 000/mois, pour qu'il soit proposé **au moment de la livraison
payée** — pas avant ; ③ me dire **quel laboratoire** je visite, et quand.

**Moi :** ① le modèle de devis/facture PDF à notre marque (D) ; ② le lien de facture WhatsApp (E) ;
③ le cahier des charges du pilote labo, prêt avant la visite ; ④ la veille facture électronique au 23/10.
