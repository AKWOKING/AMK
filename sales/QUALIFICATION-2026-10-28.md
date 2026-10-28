# La porte d'entrée — qualifier avant d'écrire (28/10/2026)

```text
ÉTAPE 0   graphe rejoué 28/10 (13 900 nœuds) · ask « qualification prospect ICP acheteur »
RULING    King, 28/10 : « Pour éviter de retomber sur ce genre de cas we need a clear qualification
          process… Dr Fogue n'est pas dirigeant (decision taker), il est consultant itinérant. »
LIT AVANT D'ÉCRIRE : sales/RESEARCH-STANDARD.md §4-5-8b-8c · sales/SOCIAL-ACQUISITION-PLAYBOOK §1.2
                     sales/CLIENT-MESSAGING-RULES §9 · sales/MQL-Qualification-2026-09-18.md
PORTE     tools/qa/audit_qualification.py leads/CRM.csv   (mécanique, ce qu'on peut prouver)
ÉTAT      191 lignes au CRM · 9 en `qualifying` ou au-delà · 1 cas d'école (Dr FOGUE)
```

---

## 0 · Pourquoi ce document existe

Le 26/10, un message a été écrit à un **ophtalmologue itinérant** comme s'il était un **opticien
propriétaire**. Il a répondu en cinq minutes : « **je ne suis pas opticien patron** ». Trois jours plus
tard il disait « ok allez y », puis « pourquoi une somme pareil », et le fil s'est arrêté.

Il n'a pas échoué sur le prix, ni sur la formulation. Il a échoué **avant la première ligne** : on a écrit
à quelqu'un qui n'a **pas d'actif à équiper** et **pas d'autorité pour acheter**. Nos règles existaient —
`RESEARCH-STANDARD` §8b (« type d'acheteur »), `MQL` porte M4 (« décideur identifiable »), le playbook ICP
§1.2. Elles étaient **écrites et non exécutées**, parce qu'elles se vérifiaient « à la main, avant
l'écriture », et qu'à la main, un nom dans une case suffisait à croire le travail fait.

**Une règle sans porte est un trou.** C'est la phrase de la maison, et ce document est la porte.

---

## 1 · Les cinq questions — trois éliminatoires, sans exception

Chaque question a **une preuve exigée**, une **source**, et **une date**. Sans les trois, la réponse est
`?` — et un `?` ne vaut jamais « oui ».

### **Q1 · L'ACHETEUR — éliminatoire** 🔴

> **Existe-t-il une personne qui peut dire oui, et qui possède ce qu'on vend ?**

Personne ne vend un site de cabinet à quelqu'un qui **consulte dans le cabinet des autres**. La question
n'est pas « a-t-on un nom ? » — c'est « ce nom **possède-t-il** l'enseigne, le local, la fiche Google, le
nom de domaine ? ».

| Rôle | Ce que ça veut dire | Verdict |
|---|---|---|
| **PROPRIÉTAIRE** | Il possède l'enseigne et le lieu. Il signe. | ✅ qualifie |
| **MANDATÉ** | Un salarié, un gérant, un associé qui **décide** — et on connaît le nom du signataire au-dessus. | ✅ qualifie, avec le nom du signataire écrit |
| **SANS AUTORITÉ** | Consultant itinérant, praticien vacataire, médecin qui tourne entre plusieurs structures, réceptionniste, community manager, « le neveu qui gère Facebook ». | ❌ **disqualifie** |
| **INCONNU** | On n'a pas cherché. | ❌ **ne s'écrit pas** |

**Preuve exigée :** `contact_name` **+** `contact_role` **+** `authority` **+** la source datée.
⚠️ **La personne qui répond n'est pas forcément l'acheteur.** C'est le cœur du cas Fogue : le CRM portait
« MINTEU NZONGA Eric Aimé » comme **titulaire ONOC** — un nom d'annuaire, pas la personne qui a répondu,
et pas forcément celle qui signe.

**Le test en une phrase** (à se poser avant chaque envoi) : *« le site s'afficherait au nom de qui ? »*
Si la réponse est « au nom d'une structure qui ne lui appartient pas », il n'y a rien à vendre ici.

### **Q2 · L'ACTIF — éliminatoire** 🔴

> **Y a-t-il quelque chose à équiper ?**

Un nom (enseigne), un lieu (adresse, même approximative), une présence publique (fiche Google ou page
Facebook) à laquelle accrocher le site.

Sans les trois, on ne vend pas un site : on vend une **identité** à quelqu'un qui n'en a pas encore, et ce
n'est ni notre produit, ni notre prix, ni notre délai. Un praticien itinérant peut vouloir une page
personnelle ; c'est un **autre objet**, qui n'existe dans aucun palier de `knowledge/PRIX-2026-10-24.md`.

### **Q3 · LE MÉTIER — éliminatoire pour l'envoi** 🟠

> **Est-il dans l'ICP du mois ?**

`sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md` §1.2 : **A** l'opticien indépendant (gérant
propriétaire, 1-2 points de vente) · **B** le cabinet de quartier (1-3 praticiens, 5-20 employés) · **C**
l'école privée bilingue. Un seul ICP par mois.

**Le métier se lit dans la source, pas dans le nom du fichier.** L'annuaire de l'Ordre des opticiens
(ONOC) contient des opticiens, **mais aussi des ophtalmologues, des gérants et des associés**. Le champ
`org_type` du CRM ne le dit pas : il vaut `other` pour les opticiens comme pour les ophtalmologues, ce qui
est un défaut du schéma connu — ne pas s'y fier.

⚠️ **Écart à trancher par King** : le ruling du 28/10 dit « cliniques privées **1-10 employés** » ; le
playbook écrit « **5 à 20** ». Tant que le playbook n'est pas réécrit, **c'est lui qui fait foi**.

### **Q4 · LE CANAL — éliminatoire** 🔴

> **Le numéro est-il sur WhatsApp, vérifié par le profil vu ?**

Ruling 12/10 (`CLIENT-MESSAGING-RULES` §10) : pas de WhatsApp, pas de prospect. Ruling 25/10 : un numéro
**testé et introuvable** est `disqualified` avec motif daté. `wa_verified = unknown` veut dire « **jamais
vérifié** » — et un numéro jamais vérifié ne s'écrit pas.

### **Q5 · LE MANQUE — éliminatoire** 🔴

> **Qu'est-ce qui manque, et l'a-t-on vérifié ce matin ?**

`RESEARCH-STANDARD` §8c : le deep check a lieu **avant** le brouillon. Un site dédié vivant = hors cible
(`disqualified`, motif daté) — on ne revient jamais avec « il vous manque une page ». Tout fait du message
porte sa date de vérification ; le `SITE-CHECK` se refait **le jour de l'envoi**.

**Et une règle de forme qui vient du même endroit** : chaque affirmation du message est adossée à une
source. Un fait **inventé** coûte plus qu'un fait manquant — « votre emplacement principal à Akwa » a
obligé le client à nous corriger sur son propre cabinet.

---

## 2 · Trois niveaux d'exigence — parce qu'on ne peut pas tout savoir avant d'écrire

La même porte ne demande pas la même preuve à un premier message et à un devis. Confondre les deux
donne soit un blocage total (personne n'est jamais qualifié), soit le laisser-aller du 26/10. Trois
niveaux, et **Q1 ne recule à aucun** :

| Niveau | Quand | Ce que Q1 exige | Ce qui est interdit |
|---|---|---|---|
| **N1 · premier contact froid** | on écrit à un cabinet d'un ICP connu, avant toute réponse | le **rôle ciblé** est écrit (`propriétaire` ou `gérant`, déduit du type d'ICP), Q2 ✅ Q3 ✅ Q4 ✅ Q5 ✅ | pas de prix, pas d'offre, pas d'aperçu *promis* comme déjà fait, pas de visite |
| **N2 · première réponse** | dès que la personne parle | on **établit qui c'est** : nom + rôle + `authority`, et on pose la question « qui décide de ce qui s'affiche sur le site ? » | pas de prix, pas de devis, pas de déplacement |
| **N3 · prix, devis, visite** | avant tout chiffre et tout déplacement | `authority` = **proprietaire** ou **mandate** avec le signataire nommé | tout le reste attend |

**La règle qui rend N1 acceptable** : un message N1 ne promet rien et ne coûte rien au prospect — il pose
une question fermée. C'est ce qui autorise à écrire sans savoir encore qui signe. **Le 26/10, on a sauté
de N1 à N3 en trois messages** : prix par écrit, puis « avant qu'on ne fixe une date ». C'est ça, le
faux pas, plus que le message lui-même.

---

## 3 · Le verdict, et où il s'écrit

| Verdict | Condition | Ce qui se passe |
|---|---|---|
| **QUALIFIÉ** | Q1 ✅ **et** Q2 ✅ **et** Q3 ✅ **et** Q4 ✅ **et** Q5 ✅ | le message peut être écrit |
| **À VÉRIFIER** | une seule réponse `?` | on va chercher la preuve, **on n'écrit pas** |
| **DISQUALIFIÉ** | une éliminatoire est ❌ | `disqualified` + **code** + motif daté, et on n'y revient pas par message |
| **PARQUÉ** | disqualification **réversible** (canal absent, hors ICP du mois, moment) | `parked` + **condition de réouverture datée** |

**Codes de motif** (ils entrent dans `disqualification_reason`, en tête, avant le récit) :

```
Q1_pas_acheteur      il consulte / travaille chez les autres, ou personne ne signe
Q2_pas_actif         aucune enseigne, aucun lieu, aucune présence publique à équiper
Q3_hors_icp          le métier n'est pas dans l'ICP du mois
Q4_pas_de_canal      numéro absent de WhatsApp (testé) — ruling 25/10
Q5_site_vivant       un site dédié vivant existe — autre offre, autre jour
Q5_fait_non_verifie  le fait du message n'est pas daté du jour
```

**Deux champs ajoutés au CRM** (`leads/build/crm.py`, `NEW_FIELDS`) : `authority` (proprietaire /
mandate / sans-autorite / inconnu) et `qualification` (Q-OK / code). Une ligne sans ces deux champs
n'est pas qualifiée, quel que soit son `stage`.

⚠️ **`leads/CRM.csv` n'est pas reconstruit par ce document.** Le CSV porte aujourd'hui de l'état que le
générateur ne connaît pas (18 lignes divergentes, mesuré le 28/10). Tant que ce décalage n'est pas réparé,
on écrit les codes dans le CSV **après** décision, jamais par un rebuild.

---

## 4 · Les deux règles de gouvernance

### ① La personne qui répond n'est pas l'acheteur — et ça se vérifie **avant** de vendre

Quand un fil démarre, la **première** chose qu'on établit n'est pas le besoin : c'est **qui signe**. Une
seule question suffit, et elle n'est pas commerciale :

> « Qui décide de ce qui s'affiche sur le site de [structure] — vous, ou la direction ? »

Trois réponses possibles, trois suites :

| Réponse | Suite |
|---|---|
| « moi » | Q1 ✅ — on continue |
| « la direction, c'est X » | on demande à rencontrer **X**, et le fil actuel devient une **porte** |
| « je ne sais pas / personne » | **on arrête de vendre.** On ne vend pas à quelqu'un qui n'a pas d'actif |

⚠️ **Ce qui est exclu, dans tous les cas** : proposer le prix à quelqu'un qui n'a pas l'autorité. Un prix
posé devant un non-décideur ne remonte pas — il **fuit**, et il revient par un confrère, plus bas.

### ② Un non-ICP qui lève la main ne s'achète pas avec une remise

Si un prospect hors ICP (ou sans autorité) dit « oui » :

1. **on ne baisse pas le prix** — `PRIX-2026-10-24` §7.4, et une remise accordée à un non-ICP devient le
   prix de tous les suivants ;
2. **on ne construit pas d'offre sur mesure dans le fil** — une offre qui n'existe dans aucun palier est
   une décision de King, pas une improvisation ;
3. **on écrit le cas, on le date, et on demande un ruling.** C'est ce qui s'est passé le 28/10 avec le
   Dr Fogue : `parked`, motif `Q1_pas_acheteur`, et une question ouverte (« un praticien itinérant
   multi-sites est-il une cible, et à quel prix ? »).

---

## 5 · Le cas d'école, écrit une fois

**Dr FOGUE — `africa-optic` — 691 28 02 37.**

| Question | Réponse | Preuve |
|---|---|---|
| **Q1 acheteur** | ❌ **SANS AUTORITÉ** | il le dit lui-même le 26/10 à 17 h 24 : « **je ne suis pas opticien patron** », « par contre je suis ophtalmologue ». Il consulte **dans** Africa Médical et l'Hôpital Charity, il n'en est pas le dirigeant. Aucun local, aucune enseigne à lui. |
| **Q2 actif** | ❌ | pas de cabinet, pas d'enseigne, pas de fiche à lui. Le site aurait affiché un nom de personne sur des lieux qui appartiennent à d'autres. |
| **Q3 métier** | ❌ | ni A (opticien gérant), ni B (cabinet), ni C (école). |
| **Q4 canal** | ✅ | numéro vivant, il a répondu en 5 minutes. |
| **Q5 manque** | ✅ | rien de vivant à son nom — mais ça ne sert à rien si Q1 et Q2 échouent. |

**Verdict : `parked`, `Q1_pas_acheteur` + `Q2_pas_actif`.** Pas de relance commerciale, pas de visite, pas
d'offre, **pas de remise**. Si le fil revient de lui-même, la seule réponse est celle qui protège la
relation : il n'y a rien à vendre aujourd'hui, et on le dit.

**Ce que ça corrige dans nos propres écrits** : le 28/10 au matin, l'analyse et la séance du Roast Room
recommandaient **d'aller le voir** (option B, 8,0/10). **C'était faux** : on ne se déplace pas pour
qualifier quelqu'un qui n'a pas l'autorité d'acheter, et un déplacement ne crée pas un dirigeant. Les deux
documents portent la correction.

**Ce que le cas a réellement produit** : une question d'offre qui n'a pas de réponse dans le dépôt — *un
praticien itinérant multi-sites est-il une cible, et avec quel objet, à quel prix ?* Elle est **ouverte**,
et elle n'appartient qu'à King.

---

## 6 · Ce qu'elle donne sur le lot du 28/10

Le CRM porte **13 relances datées du 28/10** (le lot du 26/10). Passées à la porte :

| Contrôle | Résultat |
|---|---|
| **Q4 canal** | **12 / 13** ont un WhatsApp vérifié (`wa_verified = yes`). **London Vision** est `unknown` → **pas de relance** (ruling 12/10) |
| **Q5 manque** | **13 / 13** sans site vivant enregistré → à reconfirmer le jour de l'envoi (`SITE-CHECK`) |
| **Q3 métier** | 12 opticiens (ICP A) → dans l'ICP. `ASS pour RRPHDD` est le nom de l'Ordre ; le nom commercial vu sur WhatsApp est **Ambassador Vision** |
| **Q1 acheteur** | **0 / 13** n'a de rôle écrit. Au niveau **N1**, le rôle ciblé (gérant propriétaire) suffit ; au niveau **N2**, il faudra l'établir dès la première réponse |
| **Q2 actif** | 13 / 13 ont une ville et une enseigne |

**Conclusion opérationnelle : 12 relances peuvent partir aujourd'hui, une seule est exclue.** Et la
question « qui décide ? » entre dans le premier échange de chaque fil qui répond — elle ne coûte pas un
message de plus si elle remplace une phrase de vente.

---

## 7 · Ce que la porte mécanise, et ce qu'elle ne peut pas

`tools/qa/audit_qualification.py` lit le CRM et applique ce qui se prouve par les champs :

| Contrôle | Ce qu'il regarde | Ce qu'il ne peut pas savoir |
|---|---|---|
| **Q1** | `contact_name` + `contact_role` + `authority` présents, et `authority` ≠ `sans-autorite`/`inconnu` | si la personne dit la vérité sur son rôle |
| **Q2** | une ville + un nom d'organisation renseignés | si le lieu existe vraiment |
| **Q3** | `qualification` ne porte pas `Q3_hors_icp` | quel ICP est celui du mois (c'est dans le playbook) |
| **Q4** | `wa_verified == yes` pour tout lead engagé | si le profil a été vu aujourd'hui |
| **Q5** | `site_url` vide **ou** `site_checked_on` récent | si le site est vivant — ça se teste |

Il **refuse** (`code 1`) un lead en `qualifying`/`demo`/`offer`/`closing` qui n'a pas ses preuves, et il
**signale** ceux en `prospecting` qui partent en envoi sans Q1 ni Q4.

**Ce qu'il ne fera jamais** : décider qu'un métier est dans l'ICP, ni qu'un homme est propriétaire. Une
porte mécanique attrape l'oubli, **pas le mensonge** — et c'est écrit ici pour que personne ne croie que
le vert du script vaut qualification.
