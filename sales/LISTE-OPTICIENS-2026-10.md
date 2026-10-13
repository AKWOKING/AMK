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
