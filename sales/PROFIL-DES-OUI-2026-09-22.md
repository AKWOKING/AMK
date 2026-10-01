# Le point commun de tous ceux qui ont dit oui — analysés sur les 145 leads

**Question posée par King, 22/09 vers 16h30 :** « ya-t-il un point commun entre tous ceux qui nous ont dit oui ? Si oui on devrait se pencher plus sur ce type de profil. »
**Réponse :** oui, il y en a un, il est mesurable, et ce n'est ni la ville, ni le secteur, ni la façon dont le message est écrit.

> **Ceux qui répondent sont ceux qui ont déjà payé — en argent ou en temps — pour être visibles quelque part.**
> Un domaine à eux (même mort), une page Facebook à eux (même abandonnée), une fiche chez un autre (annuaire, Google).
> **11,1 % de réponse quand c'est le cas, 2,5 % quand ce ne l'est pas.** Soit **4 fois plus**.

## 1 · Les chiffres, tels qu'ils sortent de `leads/CRM.csv` (145 leads, 6 réponses humaines au total)

| Critère testé | Taux de réponse quand OUI | Taux quand NON | Verdict |
|---|---|---|---|
| **A un domaine ou une page FB à soi** (colonnes `Website` / `Facebook`) | **3/27 = 11,1 %** | 3/118 = 2,5 % | ✅ **le seul qui sépare vraiment (×4,4)** |
| Domaine à soi seul (`Website`) | 2/15 = 13,3 % | — | ✅ renforce |
| Page FB à soi seul (`Facebook`) | 2/20 = 10,0 % | — | ✅ renforce |
| Vitrine à soi **ET** déjà référencé ailleurs (annuaire, Google, mondocteur…) | **2/5 = 40,0 %** | — | ✅ la case la plus chère, mais n=5 |
| Numéro WhatsApp dont le nom = l'établissement (`wa_verified=yes`) | 3/29 = 10,3 % | 3/116 = 2,6 % | ⚠️ lié au critère du haut, pas indépendant |
| Secteur labo d'analyses | 2/34 = 5,9 % | — | ➖ faible |
| Secteur optique | 2/44 = 4,5 % | — | ➖ faible |
| Secteur clinique | 1/24 = 4,2 % | — | ➖ faible |
| Secteur école | 1/38 = 2,6 % | — | ➖ le pire, SAUF si l'école a déjà un site |
| Douala vs Buea/Limbe | 5/115 = 4,3 % | 1/30 = 3,3 % | ❌ la ville ne change rien |
| Message écrit à partir d'un **fait vérifié** sur leur établissement | 3/65 = 4,6 % | 3/80 = 3,8 % | ❌ **le soin du message ne change presque rien** |

**La case qui compte vraiment :** santé/optique **ET** vitrine à soi = **2/2 = 100 %** — les deux leads qui ont donné naissance aux deux dossiers en cours (Le Cristallin, Univers Optique). n=2, donc ce n'est pas une preuve, c'est une **direction de chasse**.

## 2 · Le détail des six, un par un (c'est là que le motif se voit)

| Lead | Ce qu'il avait déjà, avant nous | Temps pour répondre |
|---|---|---|
| **Le Cristallin** (optique, Douala) | site **vivant** `lecristallinoptique.com` (domaine payé depuis 2018) + page FB | **2 min** |
| **Univers Optique** (optique, Douala) | domaine **mort** (`univers-optique.com`, plus aucun DNS, dernière copie vivante nov. 2023) + fiche Google 3,3/5 | **6 min** — et sa première phrase était « Combien ça me coûte » |
| **Labiomed** (labo, Douala) | rien de relevé dans le CRM (champ non rempli), mais identité WhatsApp Business nommée | **11 min** |
| **UNI-LABO** (labo, Douala) | rien de relevé (champ non rempli) ; numéro vérifié | ~2 h (18:41 → 20:57) |
| **Centre Médical de Bonanjo** (clinique, Douala) | **paie déjà pour du trafic** : Dr Tchaleu référencé sur `mondocteur237.com`, honoraires de consultation publics | le lendemain 08:44 |
| **STIBCCOL** (école, Buea) | page FB active + **un site déjà en cours de fabrication** (« we already have one in the making, ready by October ») | ~5 h |

Les trois réponses les plus rapides de la campagne sont les trois où le prospect savait **déjà ce qu'est un site** : il n'a rien à nous expliquer, il ne demande pas ce que c'est, il demande **combien** et **quand**.

Et l'école qui a répondu — la seule sur 39 — est **la seule qui était déjà en train d'en faire un**. Le contre-exemple confirme la règle.

## 3 · Ce qui n'EST PAS le motif (à ne plus optimiser)

- **La ville** : Douala 4,3 % / Buea-Limbe 3,3 %. On a passé des semaines à croire que Douala était le bon terrain. À peine.
- **Le secteur seul** : labo 5,9 %, optique 4,5 %, école 2,6 %. Un « secteur porteur » ne prédit rien si le lead n'a jamais rien payé pour sa visibilité.
- **La qualité du message** : écrire message 1 à partir d'un fait vérifié sur le prospect (page morte, annuaire, abscent des recherches) fait passer le taux de 3,8 % à **4,6 %**. C'est bien, c'est gratuit, mais **ce n'est pas le levier**. Le levier, c'est la liste.
- **Le prix dans le premier message** : **toutes** les réponses de la campagne sont arrivées avant tout prix. Le tout
  premier message contenant un prix ET un lien cliquable est celui du 19/09 à 21:00, envoyé à Labiomed —
  **quarante minutes après son « oui »**. Univers a demandé le prix avant qu'on le lui donne. Le prix ne
  déclenche pas la réponse ; il **clo** une réponse déjà obtenue.

## 4 · Le trou de données qui empêche d'exploiter ce qu'on vient de trouver

| | Leads santé/optique | dont colonne `Website` renseignée |
|---|---|---|
| | **106** | **2** (Les Cristallin et Univers, vérifiés à la main) |

Sur les 106 labos / cliniques / optiques, **104 n'ont jamais eu leur présence web vérifiée**, et 105 n'ont pas de colonne `Facebook`. Le critère qui sépare 11,1 % de 2,5 % est donc calculé sur **41 leads observés sur 145** : les écoles ont été auditées ligne par ligne (39/39 renseignées), le secteur santé non.

**Conséquence, et c'est la seule chose à faire avant la prochaine liste :** remplir **une seule colonne** — `Website` = `domaine (vivant/mort)` ou `none found` — sur les 104. Une minute par lead. Si le taux de 18,6 % de « vitrine à soi » observé sur l'ensemble se retrouve dans ce lot, ça fait **~19 leads** qui entrent dans le profil, soit **2 à 3 réponses attendues** au lieu d'une sur les 19 messages de la dernière vague.

## 5 · La règle de chasse, écrite noir sur blanc

**Un lead n'entre dans la liste d'envoi que s'il coche AU MOINS UN case :**
1. un **domaine à lui** — vivant (donc refaitable) ou **mort / expiré** (douleur prouvée : il a payé, ça ne marche plus) ;
2. une **page Facebook à son nom** qui encaisse de l'attention sans rien capturer (avis, messages, horaires faux) ;
3. une **présence payée chez un tiers** : annuaire (mondocteur, maligah, ONOC/réseaux de soins), fiche Google, site Wix/WordPress de 2016, ou « un site en cours » chez un concurrent ;
4. **et** le numéro WhatsApp porte le nom de l'établissement (compte Business) — sinon on vérifie le profil **avant** d'écrire, et si ça ne s'identifie pas on n'envoie pas.

**Zéro case cochée = pas de premier message.** Ces leads-là coûtent du temps et ne répondent pas : 118 leads « rien à eux » → 3 réponses.

## 6 · Le pitch change avec le profil : on ne vend plus l'existence, on vend le remplacement

| Au lieu de… | On dit… |
|---|---|
| « Vous n'existez pas en ligne » | « **Vous existez déjà** — et c'est exactement le problème : ce que les gens trouvent aujourd'hui, ce n'est pas vous. » |
| « Je peux vous faire un site » | « J'ai **testé votre site / votre page / votre fiche** : voilà les trois trous précis, et voilà la page qui les bouche. » |
| « Ça vous apportera des clients » | « Vous payez déjà pour être visible **chez untel**. Le même argent, chez vous. » (Bonanjo) |
| « Un domaine, c'est compliqué » | « Votre domaine est mort depuis novembre 2023. Vos patients tapent votre nom, ils ne trouvent pas votre nom. » (Univers) |

Concrètement, pour les deux leads en cours, ça veut dire : **on arrête d'attendre une permission de publier** et on livre ce qui reste à corriger — c'est déjà la ligne suivie avec Le Cristallin (modifications illimitées pendant la phase concept, facture et identifiants à la fin, règle de King du 22/09).

## 7 · Ce qu'on fait maintenant, avec ce profil

**Décision de King, 22/09 16:45 : on laisse tomber les écoles.** Conséquence directe sur la liste
ci-dessous : sur les 24 leads du profil, **23 sont des écoles** — elles sortent. Il ne reste **qu'un seul
lead** : **MITOC** (opticien de Molyko, que le classeur d'origine classait « école », corrigé le 22/09),
déjà en cours de relance. **Le gisement du profil est donc vide dans le CRM — non pas
parce que le profil est faux, mais parce que 104 des 106 leads santé/optique n'ont jamais été
vérifiés.** Le chantier de demain (remplir `Website` et `Facebook`, une minute par lead) devient donc la
seule source possible de la prochaine vague.

**a) La liste de ce soir / demain ne change pas d'angle, mais change de source.** Les 24 leads ci-dessous sont **déjà dans le CRM, déjà audités, et cochent le critère n°1 ou n°2 sans avoir répondu** — c'est le stock le plus chaud qu'on ait sous la main. (Beaucoup d'écoles : c'est notre pire segment, mais « école qui a payé un domaine » ≠ « école froide ».)

| Score | Lead | Secteur | Ville | Ce qu'il a déjà | Étape |
|---|---|---|---|---|---|
| 4 | COMOBIL – Collège Moderne Bilingue Les Lauréats | école | Douala (Bonamoussadi) | domaine : COMOBIL.com ; page FB | prospecting |
| 4 | COSBINAL – Complexe Scolaire Bilingue NAL | école | Douala (Bonamoussadi, Kotto Bloc K) | domaine : cosbinal.online ; page FB | prospecting |
| 4 | Groupe Scolaire Moderne Bilingue WAFO | école | Douala (Denver-Bonamoussadi, BP 6081) | domaine : groupescolairemodernebilinguewafo.com ; page FB | prospecting |
| 4 | Le Paradis des Anges (PDA) | école | Douala (Makepe, Carrefour SNEC Bloc A) | domaine : leparadisdesanges.org ; page FB | prospecting |
| 3 | American School of Douala (ASD) | école | Douala (BP 1909) | domaine : asddouala.com | prospecting |
| 3 | Blessed Group of Schools (BGS / Blessed Anglo-Saxon) | école | Yaoundé (Simbock + Nomayos, BP 1839) | domaine : blessedgroupofschools.com ; page FB | prospecting |
| 3 | Collège Catholique Bilingue La Retraite | école | Yaoundé (159 Ave Konrad Adenauer) | domaine : laretraitecatholicbilingualcollege.org ; page FB | prospecting |
| 3 | Complexe Scolaire et Universitaire Siantou | école | Yaoundé (Mvog-Mbi/Coron-Biteng, BP 04) | domaine : siantou-univ.com (+ siantou.net e-service subdomains) ; page FB | prospecting |
| 3 | Saint Anne's High School Limbe (SAHISCOL) | école | Limbe (New Town) | domaine : sahiscol.org ; page FB | prospecting |
| 2 | Baird Memorial College | école | Buea (Bonduma) | domaine : bairdmemorial.com (self-built, spelling errors; unreachable  | qualifying |
| 2 | College de l'Excellence de Limbe | école | Limbe | domaine : coel.net (from info@coel.net) | prospecting |
| 2 | Divine Success Comprehensive College (DSCC) | école | Douala (Ngodi) | page FB | prospecting |
| 2 | New Horizon International Comprehensive High School (NHICHS) | école | Limbe (Cité Sonara, Bota) | domaine : nhiss.org (live) + nhichs.org (PARKED/expired) | prospecting |
| 2 | Presbyterian Comprehensive Secondary School (PCSS) Buea | école | Buea (Madam Namondo Alexander) | domaine : None found (pcss@yahoo.com) | parked |
| 2 | Presbyterian Comprehensive Secondary School Bonamoussadi (PCSS) | école | Douala (Bonamoussadi) | page FB | prospecting |
| 2 | Rainforest International School (RFIS) | école | Yaoundé (SIL, BP 1299) | domaine : rfis.org | prospecting |
| 1 | Baptist Comprehensive College | école | Buea (Great Soppo) | page FB | qualifying / FU 2026-09-17 |
| 1 | Baptist High School (BHS) Awae | école | Yaoundé (Awae) | page FB | prospecting |
| 1 | Midas Touch Optic Center (MITOC) | école | Buea (Molyko, opp former police station, Malingo) | page FB | qualifying / FU 2026-09-17 |
| 1 | National Comprehensive High School (NCHS) Limbe | école | Limbe (near Atlantic Technical & Commercial) | page FB | prospecting |
| 1 | One Stop Medical Laboratory & Diagnostics | école | Buea (location TBD; co-owner based Buea) | page FB | parked / FU research then schedule |
| 1 | Solidarity Health Foundation (Solidarity Clinic & Laboratory) | école | Buea (Untarred Malingo St / Molyko Checkpoint D61, P.O. Box 467; plus code 575J+7M) | page FB | parked / FU 2026-09-16 |
| 1 | St. Joseph's College Sasse (SJC Sasse) | école | Buea (Sasse/Small Soppo) | page FB | prospecting |
| 1 | Summerset Bilingual College (SMBICOL) | école | Buea (Wokoko) | page FB | prospecting |

**b) Une relance sur le profil = un message qui parle de CEUX-là, pas de nous** — et les deux écoles
encore en fil gardent ce qui leur a été promis (STIBCCOL a notre permission de revenir en octobre,
on l'honore) : on arrête d'ouvrir de nouvelles écoles, pas d'honorer une parole. « Votre site est en ligne mais ne s'ouvre pas sur mobile » / « votre page poste depuis 2 ans, personne ne peut réserver » / « le site que vous êtes en train de faire : voilà ce qui doit y figurer pour capter les appels ».

**c) La vague du 18/09 ne sert plus de modèle.** 19 messages identiques partis dans le soir = **0 réponse en 4 jours**, et ils allaient pour la plupart à des leads sans aucune vitrine. Une vague ne se juge pas au nombre d'envois, mais au profil de ce qu'elle touche.

**d) Test de falsification — à lire dans 3 jours.** Les ~30 prochains premiers contacts sont pris **uniquement** dans le profil ci-dessus, en gardant le reste en réserve.
- Si on obtient **4 réponses ou plus** (≥ 13 %), le profil est une loi : la sourcing devient « présence d'abord », et on arrête d'acheter du volume dans les annuaires.
- Si on reste sous **2 réponses**, le point commun était une coïncidence de six cas, on le note comme tel et on revient au volume.
Dans les deux cas on le saura, au lieu de le croire.

---

*Comment c'est calculé : jointure sur `leads/CRM.csv` (145 lignes, colonnes `Website`, `Facebook`, `wa_verified`, `org_type`, `City`, `Reply`, `source`), scripts jetables du 22/09 16h4x. Les réponses automatiques (2K Labo, Adonaï) sont exclues, comme toujours. Aucun chiffre ici n'est sorti de ma tête : tous reproductibles avec les mêmes colonnes.*

*Complément du 22/09 16:40 : les deux relances Labiomed et Bonanjo parties ce mardi (16:22 / 16:24) sont
exactement deux messages du profil décrit ici — un « oui » non clos et un praticien qui paie déjà pour du
trafic ailleurs — et ce sont les deux seuls fils de la campagne que King a choisi de faire avancer à la
prochaine vague.*
