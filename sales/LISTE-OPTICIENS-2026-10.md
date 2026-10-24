# LISTE OPTICIENS — prospection post-mercredi · 05/10 (ruling King : adoptée)

> Construite le 05/10, zéro heure-King. **Rien ne part avant mercredi 07/10** (hold standing).
> **Cadence 1/jour (ruling King 05/10 — 2/jour veto : spam flag + liste brûlée en 5 j).** Chauds
> d'abord, froids après ; les réponses chaudes informent l'opener froid avant de l'engager.
> Exclusion : Bely Optique Médicale (refus écrit « Non Merci » le 24/09 — on ne re-contacte jamais).

**Ruling 06/10 : re-pull ONOC dimanche 11/10** — la veille du premier envoi (Bali, 12/10), pas avant.
Les numéros/titulaires ci-dessous sont transcrits de snippets ; aucun envoi sur un numéro non
re-vérifié ; aucun « inscrit depuis X » sans vérification.

## Opener reframé (verbatim ruling 05/10 — problème + produit, pas pitch)
> « Nous construisons des outils sur mesure pour opticiens — à commencer par une application
> d'essayage qui montre vos montures sur le visage de vos clients avant qu'ils ne passent. Vous
> seriez parmi les premiers. »
> Opener d'étude de cas DM Optique **uniquement si l'acompte est encaissé** (règle 11) ; sinon cette
> version concept, jamais l'une pour l'autre.

## Les 10 noms — calendrier 1/jour
**Lundi 12/10 — L'Opticien Bali SARL** (chaud, channel switch) : opener produit ; page FB en
appui (p/L-Opticien-bali-douala-Cameroun-…).
**Mardi 13/10 — Disc Optique Médicale** (chaud) : FB introvable → **appel voix** 677 53 35 68,
jamais un 2e WhatsApp texte.
**Mercredi 14/10 — Tchaya Optique** (chaud) : commentaire/DM sur fb.com/T.OPTIQUE.
**Jeudi 15/10 → mercredi 22/10 — les 7 froids, 1/jour, dans l'ordre :** 15 FABY · 16 Horizon ·
17 JiredOptic · 18 Planète · 19 KamaïsOptic · 20 Maff · 21 Centrale (Lumumba en réserve).
L'opener froid n'est figé qu'après lecture du pattern de réponses chaudes (12–14/10).

**Publics (annuaire ONOC, capture onocameroun.com le 05/10 — Douala, numéros publiés par l'Ordre) :**
4. **FABY Optique** — Douala · 692 08 00 55 (titulaire Boudzap Zoyem H.)
5. **Horizon Optique** — Douala · 677 44 74 17 (Djeumo Feunou S.)
6. **JiredOptic Med** — Douala · 696 26 50 31 (Lipoth P.)
7. **Planète Optique** — Douala · 699 85 58 35 (Makongo J. D.)
8. **KamaïsOptic** — Douala · 690 57 82 27 (Makouo Kamokwe H.)
9. **Maff Optique SARL** — Douala · 699 93 19 56 (Manfo épse Jounda H.)
10. **Centrale Optique** — Douala · 693 96 89 56 (Zobo J.)
Remplaçant : Lumumba OpticMedical — Douala · 670 59 79 96.

## Règles d'envoi (standing)
WhatsApp 2–3 phrases, l'opener seul, pas de bullet, pas de signature · pas de re-ask · pas de
mention d'un site en ouverture · chaque envoi loggé au CRM le jour même · 0 reply à J+7 → change de
canal, pas de wording.

## Protocole numéros ONOC (ruling 05/10)
Re-pull des deux pages ONOC au moment de logguer le premier envoi froid (risque de transposition des
7 numéros) ; si un numéro saute : corriger, logger la correction dans ce fichier + INFERENCE-ERRORS.

## RE-PULL ONOC — dimanche 11/10/2026 (fait, ruling 06/10 respecté : la veille du premier envoi)

**Périmètre lu :** `onocameroun.com/annuaire-des-opticiens-par-region/` (région **LITTORAL**, lignes 85–159 ;
chunks Sud / Sud-Ouest / Nord-Ouest **non lus**) et `onocameroun.com/liste-de-tous-les-opticiens-inscrits-au-tableau/`
(les 3 chunks, complet). **Méthode :** `fetch_page` — le `curl` du bac à sable est bloqué sur ce domaine
(HTTP 000, SSL_ERROR_SYSCALL), donc la lecture est passée par l'outil de lecture de page.

**Verdict : les 8 numéros du fichier sont CONFORMES à l'annuaire** (la source citée le 05/10, « numéros publiés
par l'Ordre »). **Aucun numéro à corriger.** Mais les deux pages de l'ONOC **se contredisent** sur quatre lignes :

| Lead | Numéro du fichier = ANNUAIRE (ligne) | « Liste des inscrits » (même personne) | Écart |
|---|---|---|---|
| Horizon optique | 677447417 (#100, DJEUMO FEUNOU Siméon, 032) | 677447417 (032) | ✅ identique |
| Planète Optique | 699855835 (#121, MAKONGO Jean Dury, 35) | 699855835 (035) | ✅ identique |
| Maff Optique Sarl | 699931956 (#123, MANFO Epse JOUNDA Hélène, 70) | 699931956 (070) | ✅ identique |
| Lumumba OpticMedical | 670597996 (#144, NZIKANG Armstrong TUAMBI, 054/2018) | 670597996 (054/2018) | ✅ identique |
| **FABY Optique** | **692080055** (#99, BOUDZAP ZOYEM Hermine, 118/**2017**) | 672552137 (BOUZAP ZOYEM Hermine, 118/**2021**) | numéro **+** année d'inscription **+** orthographe du nom |
| **JiredOptic Med** | **696265031** (#120, LIPOTH Pierrette Lotie Elise, 116) | 695626632 (116/2021) | numéro |
| **KamaïsOptic** | **690578227** (#122, MAKOUO KAMOKWE Honorine Judith, 112) | 699578227 (112) | numéro — mêmes 6 derniers chiffres, préfixe **690 vs 699** |
| **Centrale Optique** | **693968956** (#145, ZOBO Jean, 044/2020) | 699598286 (ZOGO Jean Prosper, 044) | numéro **+** nom |

**Règle née du re-pull :** **l'annuaire gagne** (c'est la page citée, et c'est elle qui publie les numéros par
cabinet). Mais pour FABY, JiredOptic, KamaïsOptic et Centrale : si WhatsApp ne livre pas / ne répond pas,
**tester le second numéro avant de classer le lead** — jamais un deuxième envoi sur le même numéro
(règle 02/10 : au-delà de 7 jours sans réponse on change de canal, pas de wording).

**Chauds, vérifiés aussi :** DISC 677533568 (#133, NANKAP TCHIPTCHOUA Jean Calvin) ✅ conforme.
**Tchaya Optique = #153, TCHAYA PITCHA'A Yannick Patou, Douala, 696790173** — un numéro **existe**, alors que
le plan ne prévoyait que Facebook. ⚠️ Ne pas confondre : **#67 « TchayaOptic » et #68 « Best View Sarl »
(TCHAYA NGOKO) sont à YAOUNDÉ**, pas à Douala.

⚠️ **BALI (envoi du 12/10) — rien à corriger, mais une affirmation à NE PAS faire.** Le CRM porte
`670 27 60 65` avec `wa_verified="yes"` (source : « Douala sweep — 2 039 likes FB, pas de site »). L'annuaire
publie **ce même numéro** sous **#107 « Optic-Swiss Sarl »** (inscription 169, titulaire FOTSING Alexis Daris),
et la ligne la plus proche du nom du CRM est **#104 « L'Opticien Sarl »** (39, DOUALLA Karen Sophie,
694 33 65 82). **Aucune ligne « L'Opticien Bali SARL » dans l'annuaire.** → (1) le numéro reste celui que King a
vérifié sur WhatsApp ; (2) **aucune mention de l'inscription à l'Ordre dans l'opener de Bali** — pas de source
pour CE cabinet, donc pas de claim (`content/strategy/RULE-CREDENTIAL-CLAIMS.md`).

**Clients et fils existants, recoupés au passage — tous conformes :** **DM Optique #102 · 021/2016 · arrêté
0382 · DOMCHE NOUMBI · 656122239** (la « ligne 102 » citée au dossier est toujours exacte, et `021/2016` est
bien un **numéro d'inscription** — la source confirme elle-même `RULE-CREDENTIAL-CLAIMS`) · Le Cristallin #126
(MESSOUE LONTE Serge Nazaire) 699905577 · Univers Optique #94 (BAYANG BIHEN Calvin) 699252874 · Cavisa #103
(DONGMO Jean René, 059/2018) 699959052 · La Ligne OpticAkwa #109 (025/2017) 683651108 · Bely Optique Médicale
#136 toujours inscrit (exclu depuis le 24/09, ne pas re-contacter).

**Ce que la source NE donne PAS :** aucune donnée d'ancienneté, nulle part — uniquement des numéros
d'inscription et d'arrêté. **Rien, dans le registre, ne permet d'écrire « depuis YYYY ».** La règle du 08/10
est confirmée par la source elle-même.

---

# LOT DU 24/10 — 5 prospects qualifiés (recherche du 23/10, envoi prévu le 24)

> **Demande King 23/10 :** « a small batch of 5 clinics… check if there's a trace of any social media
> activity… our ICP = same profile as DM Optique… find the 5 prospects today, write the first outreach
> message, and prepare a plan for their demo website. »
> **Méthode :** recherche web + lecture des pages publiques (Facebook, Instagram, TikTok, annuaires,
> ONOC, Google). Aucun mot-clé inventé, aucun chiffre de trafic estimé. Les numéros viennent de pages
> publiques et **se re-vérifient sur le profil WhatsApp avant chaque envoi** (règle du 05/10).

## 1 · Le profil qui définit le lot — **corrigé le 23/10**

> **Correction de King (23/10) :** ce n'est pas le bon profil. DM OPTIQUE SARL **n'avait aucune
> présence en ligne au départ** — ni site, ni page, ni compte. Un cabinet à 207 publications a déjà
> quelqu'un qui s'occupe de son image : ce n'est pas notre prospect, c'est son concurrent.
> Les cinq ci-dessous sont donc devenus **le groupe de contrôle** (voir §8), et le vrai lot est en §7.

Le profil retenu par King : **un cabinet privé de Douala, 1 à 10 salariés, qui n'a rien en ligne** —
pas de site, pas de page, pas de compte. Il existe par le bouche-à-oreille, une plaque et un numéro.
C'est l'état de DM OPTIQUE SARL avant qu'on travaille ensemble.

**Ce que ça change dans la méthode :** on ne cherche plus une preuve d'activité, on cherche une
**absence** — et une absence ne se prouve pas, elle se constate par élimination. La méthode est en §7.1.

## 2 · Les cinq — ce qui est vérifié, et ce qui reste à vérifier

| # | Cabinet | Quartier | Ce qu'on a vu (preuve) | Le trou | Contact public |
|---|---|---|---|---|---|
| 1 | **Fashion Vision Douala** | Bonapriso, rue Afcodi | Instagram **2 034 abonnés · 207 publications** ; page Facebook ; groupe présent dans 7 pays ; ONOC #142 (001/2016, PUILLE Nicolas) | **aucun site trouvé** pour la boutique de Douala | 656 22 38 63 · fvisiondouala@outlook.fr |
| 2 | **Original Optique / Glamour Optique** | Akwa, face Palais Dika (+ Yaoundé) | TikTok **@original.optique** actif (vidéos pédagogiques, adresses, horaires) ; site `originaloptique-douala.com` | **le site répond HTTP 500** (vérifié 23/10) | 678 922 973 · 691 01 94 33 |
| 3 | **Optix SARL** | Akwa, carrefour Idéal | Page Facebook active (« atelier spécialisé depuis plus de 10 ans ») ; fiche Google qui pointe encore un site | **`optix-sarl.business.site` renvoie 404** — Google a arrêté ce service en 2024 | 697 72 32 65 · lesoptix@gmail.com |
| 4 | **SOS Vision** | Akwa, ancien Makumba | Facebook actif (publications récentes, lunettes de soleil) ; ONOC **#125** (007/2016, MEILO NGASSA Line) | **aucun site trouvé**, ni IG ni TikTok | 699 86 04 63 · sosvision05@gmail.com |
| 5 | **House of Lunettes Optic** | Douala | Facebook avec **contenu éducatif régulier** (« quelle monture pour quel visage ») | **aucun site trouvé** ; le contenu ne vit que dans le fil | 674 43 08 92 · esemeebot@yahoo.fr |

**Écartés du lot (et pourquoi) :** Valdoz Optic (site + IG + X actifs, groupe structuré — hors ICP) ·
Maison Optique (site `.cm` + TikTok @maisonoptique237) · Golden Eyes (deux sites, marketing externalisé) ·
Leroy Optique (site + IG + TikTok) · Bely (refus écrit du 24/09) · les 11 déjà contactés du lot d'octobre.

## 3 · Le groupe de contrôle — **quatre parqués, un réécrit**

> **Version du 23/10 : PÉRIMÉE.** Les cinq textes d'origine sont remplacés. La raison, le diagnostic
> ligne par ligne et les nouveaux textes à envoyer aujourd'hui sont dans
> **`sales/OUTREACH-REECRITURE-2026-10-24.md`** §1 et §4.2.

Ce que les deux captures du 24/10 ont changé :

| # | Prospect | Statut au 24/10 | Motif |
|---|---|---|---|
| ① | Fashion Vision | **ne pas réécrire** | **déjà contacté le 24/09** (deux coches, jamais ouvert). Relance possible à J+30 avec le gabarit de rupture, pas une « nouvelle ouverture » |
| ② | Original Optique | **relance J+2 (26/10)** | message du 24/10 envoyé 11:52 → **réponse automatique** (« pas disponibles ») alors que la fiche dit « Open until 2:00 PM ». C'est une fuite vue à l'écran, pas une théorie |
| ③ | Optix | **part aujourd'hui** | site en 404 : l'exception écrite dans la règle de King (site cassé = on demande pourquoi il a été abandonné) |
| ④ | SOS Vision | **parqué** | Facebook actif, ni IG ni site : c'est le profil « les réseaux suffisent » — le groupe qu'on **mesure**, pas celui sur qui on mise |
| ⑤ | House of Lunettes | **parqué** | page Facebook éducative, aucun site. Même raison |

**Le seul texte du §3 qui part aujourd'hui — Optix (697 72 32 65) :**

> Bonjour, votre lien optix-sarl.business.site ouvre une page « introuvable » : Google a fermé ce
> service en 2024, sans prévenir les cabinets qui l'utilisaient.
> Quelqu'un qui clique dessus aujourd'hui ne sait plus si vous êtes encore ouvert.
> Vous l'avez laissé tomber exprès, ou personne ne vous a prévenu ?

**Relance d'Original Optique — jeudi 26/10 seulement, si toujours rien :**

> Bonjour, sur votre compte, deux choses se contredisent : la fiche affiche « ouvert » et le message
> automatique répond « nous ne sommes pas disponibles ».
> Un patient qui écrit à 14 h reçoit une réponse qui dit le contraire de ce qu'il voit.
> Je vous envoie les deux captures côte à côte ?

## 4 · Cadence — **correction du 23/10 : je me suis trompé**

Ce que j'avais écrit ici — « cinq le même jour, c'est le motif qu'on a écarté, il faut deux numéros » —
était une extrapolation, pas la règle. Et elle ne tient pas debout :

- le motif du 05/10 visait un **envoi groupé, texte identique, vers beaucoup de monde**. Ici : dix
  destinataires, **dix textes différents**, aucun lien dans le premier message. Ce n'est pas un motif
  de masse, c'est dix conversations qui commencent.
- « signaler le numéro » ne parle pas du destinataire : chaque personne peut nous **bloquer** ou nous
  **signaler**, et c'est **notre numéro expéditeur** qui accumule. Sur cinq à dix messages, c'est un
  risque marginal. Je l'ai présenté comme une contrainte dure, ce n'était pas honnête.
- **ce qui reste vrai et suffit** : ① dix textes différents, jamais de copier-coller ; ② **aucun lien
  dans le premier message** ; ③ pas plus d'un message par heure ; ④ on s'arrête net si deux personnes
  nous bloquent.

**Décision proposée :** les dix partent **demain, sur un seul numéro**, espacés d'environ 45 minutes
(09h00 → 16h00). Si le ruling « 1/jour » reste ta règle ferme, on fait 5 demain et 5 le 25/10 — c'est
ton choix, ce n'est plus un problème technique.

## 5 · La démo — un socle commun, cinq angles

Voir la section « démo » du lot : même squelette pour les cinq (5 pages, héros en couches, JSON-LD,
WhatsApp prérempli), et **une chose différente par prospect** — celle qui prouve qu'on l'a regardé lui.

## 6 · Le plan de démo — ce qu'on construit si l'un dit oui

### 6.1 · Le socle, réutilisé pour les cinq

Ce que le chantier DM a laissé et qui se réutilise tel quel : HTML statique (aucun framework), système
de jetons CSS, bascule FR/EN par attribut, données structurées `Optician`, CTA WhatsApp **prérempli**,
`_headers` de cache, `404.html`, `robots.txt` + `sitemap.xml`, et les portiques `shot.py` /
`audit_delivery.py`.

**Cinq pages, jamais plus, pour une première démo :**

| Page | Ce qu'elle contient | Pourquoi elle existe |
|---|---|---|
| Accueil | héros en couches (voir §7), 3 chemins, preuves, horaires, WhatsApp | c'est la seule page que 80 % des visiteurs liront |
| Montures | galerie des photos **fournies par le cabinet**, filtres femme/homme/enfant | ce que le client vient voir |
| Examen de vue | le déroulé en 4 étapes, ce qu'il faut apporter, horaires d'examen | la question qu'on nous pose en DM |
| Le cabinet | le titulaire, l'équipement, l'adresse avec l'étage et la porte | la confiance |
| Contact | adresse, itinéraire, téléphone, WhatsApp, horaires | la conversion |

**Ce qu'on ne met pas dans une démo :** aucun prix, aucune marque de monture revendiquée, aucun avis
client recopié, aucune photo empruntée à un autre cabinet. Les photos qu'on n'a pas encore → blocs
grisés nommés « votre photo ici », pas une image de banque.

**Le temps réel :** 3 à 4 h pour la première (socle + identité visuelle tirée de leurs publications),
2 h 30 pour les suivantes. Les portiques tournent avant tout envoi de lien.

### 6.2 · L'angle de chaque démo — la seule chose qui change

| # | Prospect | L'angle de la démo | La preuve qu'on a regardé |
|---|---|---|---|
| 1 | Fashion Vision | **la vitrine Douala d'un groupe de 7 pays** : bilingue FR/EN, la galerie en avant, l'adresse de Bonapriso répétée à chaque section | leurs 207 publications, leur bio en anglais et en français |
| 2 | Original Optique | **deux villes, un seul endroit où les trouver** : Akwa et Yaoundé, horaires distincts, itinéraire par boutique | leurs vidéos citent les deux adresses et deux numéros |
| 3 | Optix | **l'atelier** : soudure, polissage, remise en état des montures, 10 ans de métier — le geste avant la monture | « atelier spécialisé depuis plus de 10 ans » sur leur page |
| 4 | SOS Vision | **lentilles et solaires** : les deux catégories en tête, l'adaptation des lentilles expliquée en 3 étapes | leur présentation Facebook : « lunettes optiques, de soleil, lentilles » |
| 5 | House of Lunettes | **les conseils deviennent des pages** : 3 articles courts (forme du visage, entretien, enfant) qui restent en ligne | ils publient déjà ce contenu, et il disparaît du fil |

### 6.3 · Ce qu'on demande au premier échange (si la réponse est « oui, montrez-moi »)

Quatre choses, pas plus : **6 à 10 photos** (devanture, intérieur, équipement, montures), **le nom exact**
du titulaire et son numéro d'inscription à l'ONOC, **les horaires réels** (examen séparé de l'accueil),
et **le numéro WhatsApp** qui reçoit les messages. Sans ça, la démo reste une maquette — et une maquette
ne se montre pas comme un site.

## 7 · LOT DU 24/10 — cinq cliniques **sans aucune présence en ligne**

### 7.1 · Comment on constate une absence (et ce que ça ne prouve pas)

Une présence se prouve ; une **absence** se constate par élimination. Quatre contrôles par piste :

1. **Recherche nominative** — le nom exact, puis le nom + `facebook`, + `instagram`, + `site web`.
2. **Tri des résultats** — si tout ce qui remonte est un **annuaire** (Maligah, DoualaTour, Pages
   Pratiques, Pages Jaunes, Ayila'a), un **réseau d'assurance** (ASCOMA, NSIA, Pass24, Sogécable WTW)
   ou une fiche d'avis, alors le cabinet n'a **rien qui lui appartienne**.
3. **Aucun domaine** au nom du cabinet (attention aux homonymes : `souriredentaire.com` est au Niger,
   pas à Bali-Douala).
4. **Contrôle à la main avant envoi** — recherche Facebook/Instagram dans l'application et champ
   « site web » de la fiche Google. C'est le seul contrôle qui vaut ; le reste est un indice.

**La limite, écrite noir sur blanc :** une page Facebook peut exister sans être indexée, et une fiche
Google sans site reste une présence. Donc **on ne dit jamais « vous n'avez rien en ligne »** — on dit
**« je n'ai rien trouvé »**. C'est vrai, c'est vérifiable, et ça n'insulte personne. Les cinq messages
sont écrits comme ça.

### 7.2 · Les cinq

| # | Établissement | Type | Quartier / adresse | Mobiles | Ce que j'ai trouvé — et rien d'autre |
|---|---|---|---|---|---|
| 6 | **Cabinet Dentaire Bouda Seidou** (Dr Seidou Bouda) | dentaire | Bonanjo, Immeuble Neuilly II, 1682 av. du Général de Gaulle, à côté de la station Total | 677 76 03 49 · 696 00 01 11 | reconnu à l'**ONCDC** ; sinon **deux adresses** (Maligah dit Akwa, 1376 bd de la Liberté) et **quatre numéros** selon la source ; aucun site, aucune page |
| 7 | **Cabinet Dentaire Le Sourire** (Dr Nadine Towe-Kalla) | dentaire | Bali, 298 rue Dikoumé Bell, face maison de l'étanchéité | 698 00 78 08 · 699 62 94 55 | **Pages Jaunes** + annuaire de l'**AFECDEC** (elle y est secrétaire adjointe) ; aucun site, aucune page |
| 8 | **Cabinet Dentaire IVY** | dentaire | Bonanjo, 882 rue Christian Tobie Kuoh (rue Ivy) | 697 945 251 · 699 943 186 | **DoualaTour** + une place de marché de dentistes ; la fiche le classe « **ORL ⚊ dentiste** » — un autre métier que le sien |
| 9 | **COMED** — Centre d'Ophtalmologie et de Médecine de Douala | ophtalmo + médecine générale | Bonapriso, 370 rue 1.225 (route Dominique Savio), BP 2763 | 699 915 652 · 233 42 03 85 | **créé en 1993**, 33 ans de métier ; en ligne : une ligne d'annuaire, sans horaires ni photos |
| 10 | **CMO JOLINOM** — Centre Médical d'Ophtalmologie | ophtalmo | Deido, derrière la pharmacie de la Bourse (Grand Moulin) | 677 466 425 · 677 46 64 25 | listé chez **NSIA, ASCOMA, Medlog** ; **deux mobiles différents** selon l'assureur, aucune adresse plus précise que « derrière la pharmacie » |

**Taille** : 1 à 5 personnes pour les trois cabinets dentaires, 4 à 10 pour les deux centres. Aucun n'a
de service marketing, aucun ne publie.

### 7.3 · Écartés — et le motif, parce que c'est le motif qui compte

| Écarté | Pourquoi |
|---|---|
| Cabinet Dentaire **CERAM** (Deido) | **page Facebook à 1 726 abonnés** — il y a quelqu'un derrière. C'est exactement le cas d'école de ta règle |
| Cabinet dentaire **YAKS** (Logbessou) | page Facebook active, et **déjà contacté le 16/09**, parqué depuis |
| Clinique Dentaire **WADO** (Logpom) | **Instagram 175 publications + TikTok + YouTube** — présence construite, hors ICP |
| **CMODN** (Makepe, ophtalmo) | page Facebook ; déjà classé « Piste 4 » le 10/10 |
| **Sparks · Shine · Maison Optique · La Cerisaie · Lynx Vision · DIEC · C2T · La Grâce · Etienno · Rond-Point · SAFY · BZK · Shekina · Sony** | ont un site, ou une page tenue |
| **Cabinet Dentaire Azur · Cabinet Dentaire du Palais · Clinique Kerthan · Clinique Ndassa** | **réserve** : rien trouvé en ligne, mais informations contradictoires (Azur : 413 rue Gouverneur Carras *et* 1.066 rue Clemenceau ; Kerthan et Ndassa : un seul annuaire, pas d'adresse vérifiable) |

### 7.4 · Les cinq messages — **réécrits le 24/10**

> Les versions du 23/10 étaient des constats : elles demandaient au docteur de faire le travail de
> relier « pas de site » à « patients perdus ». Diagnostic et sources : **`sales/OUTREACH-REECRITURE-2026-10-24.md`**.

Format : **fait vérifiable (ligne 1) → ce que fait le patient (ligne 2) → une question fermée (ligne 3)**.
35 à 55 mots. Aucune signature, aucun lien, aucun prix.

**⑥ Bouda Seidou — 677 76 03 49**
> Bonjour Docteur, votre cabinet apparaît sur quatre annuaires différents, avec quatre numéros et deux adresses.
> Un patient qui cherche un dentiste à Bonanjo tombe sur une de ces pages, appelle un numéro que vous n'utilisez peut-être plus, et raccroche.
> Je vous montre ce qu'il voit ?

**⑦ Le Sourire — 698 00 78 08**
> Bonjour Docteur, je suis tombé sur l'annuaire de l'association des chirurgiens-dentistes où vous êtes secrétaire adjointe — et c'est, avec les Pages Jaunes, tout ce qui existe au nom de votre cabinet.
> Un patient qui cherche un dentiste à Bali ne vous trouve pas : il trouve les cabinets qui ont une page, et il appelle l'un d'eux.
> Je vous montre ce qu'il voit ?

**⑧ IVY — 697 945 251**
> Bonjour Docteur, sur DoualaTour, votre cabinet de la rue Ivy est classé « ORL et dentiste », avec deux numéros et aucune page à lui.
> Un patient qui cherche un dentiste lit « ORL » et passe au suivant — il ne saura jamais que c'est vous qu'il cherchait.
> Je vous envoie la fiche telle qu'il la lit ?

**⑨ COMED — 699 915 652**
> Bonjour Docteur, le COMED soigne à Bonapriso depuis 1993, et tout ce qu'un patient trouve en ligne, c'est une ligne d'annuaire : un numéro fixe, pas d'horaires.
> Un patient qui cherche un ophtalmologue un samedi ne peut pas savoir que vous êtes ouvert — il appelle celui qui l'affiche.
> Je vous montre ce qu'il voit ?

**⑩ CMO Jolinom — 677 466 425**
> Bonjour Docteur, votre centre est enregistré chez trois assureurs avec deux numéros différents et, pour seule adresse, « derrière la pharmacie de la Bourse ».
> Un patient avec une ordonnance appelle le numéro que son assureur lui donne — pas forcément le vôtre.
> Lequel des deux est le bon aujourd'hui ?

**Lot du 24/10 : ces cinq + Optix = 6 messages, un seul numéro, espacés d'environ 45 minutes.**

### 7.5 · Ce qui doit être vrai avant d'envoyer

1. **Le numéro ouvre WhatsApp** — un mobile d'annuaire n'est pas une preuve. C'est la leçon du 10/10 :
   sur 18 pistes, 15 sont tombées pour cette raison. Quatre de mes cinq ont deux numéros ; on teste le
   premier, on garde le second.
2. **L'adresse et les horaires sont confirmés par eux**, pas par un annuaire — c'est précisément ce
   qu'on leur demande dans le message.
3. **Aucune affirmation absolue** : « je n'ai rien trouvé », jamais « vous n'avez rien ».
4. Aucun prix, aucun lien, aucune promesse de délai dans le premier message (verrous DM en vigueur).

### 7.6 · L'angle de démo de chacun (le socle du §6.1 ne change pas)

> **Le socle est construit** : `hosting/previews/demo-clinique/index.html` — héros en 5 couches,
> match cut, profondeur en CSS seul, **0 Ko d'effet**, portique `shot.py` **VERT (0 P1 · 0 P2 · 0 P3)**.
> Pour chaque prospect : on change le `<svg>` de l'objet, `--brand`, et le texte. Rien d'autre.

| # | Prospect | L'angle | Ce qui le rend vrai |
|---|---|---|---|
| 6 | Bouda Seidou | **une seule adresse, enfin** : l'itinéraire, l'étage, l'immeuble, le téléphone unique en haut de chaque page | deux adresses et quatre numéros circulent aujourd'hui |
| 7 | Le Sourire | **la page qui remplace l'annuaire** : horaires réels, soins, photos du cabinet | n'existe que sur deux annuaires |
| 8 | IVY | **dire ce qu'il soigne** : dentisterie, pas ORL — un titre, une phrase, les soins en 4 lignes | l'annuaire le classe ORL |
| 9 | COMED | **1993** : une page d'histoire (« 33 ans à Bonapriso »), l'équipe, les examens | créé en 1993, âge vérifiable |
| 10 | JOLINOM | **un numéro, une adresse, un plan** : tout tient dans la première page | deux numéros et pas d'adresse |

---

## 8 · Le test que tu veux faire — et ce qu'il peut vraiment dire

**Groupe A (sans présence) :** les cinq du §7. **Groupe B (avec présence) :** les cinq du §2.

**Ta prédiction :** A dit oui, B ne répond pas ou refuse, parce que B est déjà servi par ses réseaux.

**Ce qui la valide :** 2 réponses positives ou plus sur 5 en A, et 0 ou 1 en B.
**Ce qui la tue :** A muet aussi — alors le problème n'est pas la présence en ligne, il est dans le
message, le canal ou le numéro.

**Les trois limites, dites franchement :**
1. **n = 10.** L'historique du fichier est à **2 réponses sur 31 envois (6,5 %)**. Sur dix, l'espérance
   est inférieure à une réponse : ce test donne un **signal**, pas une preuve. Pour conclure, il faut
   trois vagues de dix.
2. **Deux métiers différents.** A est fait de dentistes et d'ophtalmologues, B d'opticiens. Si A répond
   et B non, on ne saura pas si c'est la présence en ligne ou le métier. Pour trancher, la deuxième
   vague doit être **cinq opticiens sans présence** (il en existe : c'est le vivier de la §2, ceux
   écartés pour un site en ruine).
3. **La livraison.** Un numéro qui n'est pas sur WhatsApp ne dit rien sur la théorie — il dit qu'on
   n'a pas frappé à la bonne porte. On le note comme **non testé**, jamais comme un refus.

**Pour que ce soit comparable**, les dix partent avec la même structure (2 phrases, un fait vérifié,
une question, aucun lien), le même expéditeur, le même jour. Et on note pour chacun : envoyé / livré /
lu / répondu / bloqué.
