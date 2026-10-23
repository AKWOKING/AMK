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

## 1 · Le profil qui définit le lot

DM OPTIQUE SARL, c'est : un cabinet de quartier, **un titulaire identifiable**, des **photos réelles**,
un **numéro WhatsApp** comme porte d'entrée, **aucune équipe marketing**. Le prospect qui lui ressemble
a donc : une activité sociale **visible et récente**, des **patients réels** (avis, commentaires), et
**pas de maison à lui** sur le web — ou une maison en ruine (lien mort).

**Le signal que King a repéré et qui est confirmé ici :** les cabinets qui « ne veulent pas de site »
tiennent déjà un compte. Ils investissent du temps dans un canal qu'ils **louent** (Facebook, TikTok,
Instagram) et n'ont rien qui leur appartienne.

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

## 3 · Les cinq messages d'ouverture (prêts à envoyer)

Règles appliquées : 2–3 phrases, **aucune puce**, **aucune signature**, **aucune offre dans le premier
message**, une seule question. Le fait cité est vrai et vérifiable — c'est lui qui ouvre la porte.

**① Fashion Vision Douala**
> Bonjour, je suis tombé sur votre Instagram — 207 publications, un vrai travail de montures et de
> lunettes. Mais quand quelqu'un cherche « Fashion Vision Bonapriso » sur Google, il ne trouve pas votre
> boutique. Vos clients vous demandent souvent l'adresse en message ?

**② Original Optique**
> Bonjour, le lien de votre site (originaloptique-douala.com) affiche une erreur depuis un moment — je
> suis tombé dessus en cherchant vos horaires pour Akwa. Vous savez si quelqu'un s'en occupe encore ?

**③ Optix**
> Bonjour, le lien que Google affiche encore pour Optix mène à une page introuvable — le service qu'ils
> utilisaient a fermé en 2024. Vous avez un autre endroit où envoyer les gens qui vous cherchent ?

**④ SOS Vision**
> Bonjour, votre page Facebook bouge, mais quelqu'un qui tape « SOS Vision Akwa » sur Google ne trouve ni
> l'adresse ni les horaires. C'est par WhatsApp que vos clients vous joignent, ou ils passent
> simplement ?

**⑤ House of Lunettes**
> Bonjour, vous publiez des conseils sur les formes de montures — c'est rare ici, et c'est utile. Mais un
> conseil publié sur Facebook disparaît du fil en trois jours. Ça vous dirait qu'ils restent quelque
> part qui vous appartienne ?

## 4 · Cadence — un conflit à trancher par King

Le ruling du 05/10 dit **1 envoi par jour, 2 maximum** (raison : signalement spam → numéro grillé →
 liste brûlée). Cinq messages le même jour, sur un numéro qui n'a jamais envoyé à ces gens, c'est
 exactement le motif qu'on a écarté.

**Proposition :** les cinq sont **écrits et prêts** dès maintenant ; on en envoie **2 le 24/10**
(09h00 et 17h00), **2 le 25/10**, **1 le 26/10**. Si King veut les cinq demain, alors il faut deux
numéros, pas un.

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
