# Le flux de prospection — quatre étapes, et le vertical qui rapporte le plus vite (24/10/2026)

> Note de conception écrite après `superpowers/brainstorming`, et après l'accord de King sur la
> recommandation **A + B** (concept par métier d'abord, personnalisation après la première réponse).
> Elle ne construit rien : elle fixe ce qu'on construit, et ce que chaque étape doit produire pour que
> la suivante ait le droit de commencer. **Rien ne se code avant l'approbation de King.**

```
Décidé     : A (concept par métier) + B (site personnalisé dans les 24 h après une réponse)
Ouvert     : le vertical — recommandation ci-dessous, à confirmer
Remplace   : rien. Complète PRE-FLIGHT §1c/§1h, RESEARCH-STANDARD §8b/§8c, LIFECYCLE §1
```

---

## 1 · Le flux, et ce qui ferme chaque étape

| # | Étape | Qui | Sortie (fichier ou geste) | La porte qui ferme l'étape |
|---|---|---|---|---|
| 1 | **Scout** | moi | `leads/records/<slug>.md` + une ligne CRM par le générateur (`leads/build/crm.py`) | aucune : on ne descend pas une piste sans fiche |
| 2 | **Vérifier** | moi, puis **King** pour le numéro | la fiche porte **sept verdicts** : besoin, signal, service, pourquoi maintenant, chiffre vérifié, canal, type d'acheteur | **§8b trois portes** (A joignabilité WhatsApp · B intention numérique · C acheteur) **et §8c** (un verdict écrit par affirmation) |
| 3 | **Construire** | moi | **un concept par métier** (dentaire, laboratoire, clinique) — nom fictif, `noindex`, publié une fois sur Vercel | portiques §1b + `audit_delivery --strict` + étiquette de fiction |
| 4 | **Écrire** | moi, **King** envoie | le message à coller + **une capture** du concept portant les faits publics du prospect | `tools/qa/audit_outreach.py` = 0 bloquant, puis `gate-dm.sh` |
| 5 | **Personnaliser** *(déclenché par une réponse)* | moi | le site du prospect avec ses vrais faits, **dans les 24 h** | portiques §1b, revue de King, puis §1f③ (Vercel) |

**Ce que l'étape 3 ne fait pas** : elle ne construit pas le site d'un prospect. Le concept est
**générique par métier** ; ce que le prospect reçoit dans le message, c'est une **capture annotée avec
ses faits à lui** — l'objet est montré, le nom n'est pas publié (ruling King du 17/09 : pas de nom réel
sans autorisation écrite, et les concepts nommés ne sont jamais liés publiquement).

**Ce que l'étape 5 achète** : la personnalisation au moment où elle a de la valeur — quand le
prospect a déjà répondu — et au moment où elle coûte le moins, parce qu'on ne construit que pour des
gens qui écoutent. C'est aussi la promesse publique du site AMK : *« l'aperçu est dans votre téléphone
sous 24 heures après votre premier message »*.

---

## 2 · Le vertical : ce que les données du dépôt disent

### 2.1 · Le comptage (CRM, 163 lignes, comptées et non estimées)

| Vertical | Base | Contactés | Réponses | **dont humaines** | Taux humain | IC 95 % (Jeffreys) |
|---|---|---|---|---|---|---|
| **Opticien** | 58 | 25 | 7 | **7** | **28,0 %** | [14,3 ; 47,6] |
| Clinique | 27 | 15 | 1 | 0 | **0 %** | [0,0 ; 20,4] |
| Laboratoire | 37 | 22 | 1 | 1 | 4,5 % | [0,8 ; 21,8] |
| École | 38 | 0 | 0 | 0 | — | — |

Test exact de Fisher, opticiens 7/25 contre cliniques 0/15 : **p = 0,033**. Contre laboratoires 1/22 :
p = 0,052. Un seul client signé à ce jour — **DM Optique, opticien**.

### 2.2 · Le modèle (Monte-Carlo, 20 000 tirages, loi bêta de Jeffreys)

Deux étages : réponse au message, puis signature après réponse (**1 signature sur 7 réponses
humaines** — c'est le chiffre le plus fragile du modèle, et l'intervalle le dit). Cadence : **1 message
par jour** (ruling 05/10).

| Vertical | Signature par message (médiane) | 80 % | P(≥ 1 client en 20 messages) | 5 clients : médiane |
|---|---|---|---|---|
| **Opticien** | **4,36 %** | [1,08 ; 11,11] % | **67 %** | **108 jours** (80 % : 35–365) |
| Clinique | 0,19 % | [0,01 ; 1,61] % | 11 % | jamais atteint en un an dans 86 % des tirages |
| Laboratoire | 0,74 % | [0,11 ; 2,95] % | 22 % | jamais atteint dans 66 % des tirages |

**Ce que « 0/15 » vaut exactement, en probabilité :** après 15 cliniques contactées sans une seule
réponse humaine, la probabilité que le taux réel des cliniques soit **aussi élevé que celui des
opticiens (28 %) est de 0,17 %**. Qu'il soit **au moins 10 %** : **7,4 %**. Autrement dit : les
cliniques ne sont pas prouvées mortes, elles sont prouvées **différentes** — et une seule vague de 15
messages ne suffirait pas à les condamner.

### 2.3 · Le confondant, dit franchement

Les opticiens ont reçu **plusieurs vagues** (12, 15 et 22/10) et les textes les plus récents ; les
cliniques ont reçu les messages de la mi-septembre, écrits avant la structure en quatre temps. Une
partie de l'écart est donc **de la copie, pas du métier**. Deux choses limitent ce confondant :
les cliniques ont reçu **plus de relances par piste** (0,27 contre 0,08) — et sont restées muettes — et
les six messages du 26/10, réécrits et passés à la porte, contiennent **cinq cliniques** : c'est
justement le test propre qui manque.

### 2.4 · Le marché, compté à la source

- **Opticien : 75 cabinets à Douala**, tous avec un numéro publié — annuaire officiel de l'ONOC,
  région Littoral, lignes 85 à 159, relu aujourd'hui (`onocameroun.com/annuaire-des-opticiens-par-region/`).
- **Le CRM ne couvre pas ce marché** : 58 lignes optiques, 25 contactées, **33 non contactées — dont
  une seule porte un numéro**. La matière première existe donc (75), elle n'est simplement pas saisie.
- Clinique : aucun registre public dans le dépôt ; 27 identifiées, aucune borne de marché. Le vivier
  est plus grand, ce n'est pas la contrainte.

### 2.5 · La décision recommandée

**Les opticiens d'abord, comme verticale de prospection froide** — pour quatre raisons qui se
cumulent, et une seule d'entre elles serait suffisante :

1. **Le taux de réponse** : 28 % (7 sur 25) contre 0 % (0 sur 15), et un p de 0,033 (§2.3, Fisher
   exact) qui, malgré le confondant, ne se
   retourne pas.
2. **Le seul euro encaissé** est un opticien (DM Optique) — et les trois fils les plus avancés aussi
   (Univers, Cavisa, Cristallin).
3. **Le marché est fini et connu** : 75, tous joignables, dont ~50 jamais touchés. On peut compter ce
   qui reste, ce qu'on ne peut pas faire avec les cliniques.
4. **Le produit se réutilise** : le catalogue de 40 montures (`build_dmoptic_montures.py`) et le
   gabarit DM sont déjà écrits ; l'extension try-on (900 000) ne s'adresse qu'à eux.

**Les cliniques ne sont pas fermées** : elles deviennent le **bras de contrôle** du lot du 26/10 —
cinq messages, texte neuf, même porte. Si le taux de réponse reste sous 10 % (seuil posé ici — non revérifié, il ne vient d'aucune source) sur ces cinq, le vertical
froid se ferme pour de bon, chiffre en main ; s'il monte, la thèse « c'était la copie » gagne et on
rouvre.

---

## 3 · Ce que le flux ne fait pas

- **Pas de site par prospect avant la réponse.** Quinze aperçus nommés ont été construits entre le 14
  et le 24/09 pour **un seul client payant** ; ils ont été retirés du dépôt le 24/10.
- **Pas de nom de prospect sur une page publique** sans autorisation écrite (ruling 17/09).
- **Pas de service qui dépend d'un tiers** dans l'offre de tête : ni WhatsApp Business API, ni
  revendication de fiche Google, ni page Facebook « garantie ». On les **accompagne**, on ne les
  promet pas — c'est déjà écrit dans le dossier Univers.
- **Pas de message sans les trois portes.** Un numéro non vérifié sur WhatsApp ne part pas.

---

## 4 · Les trous connus, à traiter dans le plan

1. **La porte A** : les six numéros du lot du 26/10 ne sont pas vérifiés. Rien ne part avant.
2. **Le CRM ne stocke pas les numéros** des opticiens non contactés (1 sur 33). L'étape 1 doit les
   saisir depuis l'ONOC, par le générateur, jamais à la main.
3. **Aucun fichier de métriques** : le tracker vit dans le document d'envoi. Un fichier en propre est
   un **fichier debout neuf** → confirmation de King (§4b).
4. **Le taux de signature (1/7) repose sur un seul client.** Les trois prochaines réponses valent
   plus, pour ce modèle, que n'importe quelle nouvelle statistique.
5. **Les cinq concepts à construire** (dentaire, laboratoire, clinique) : aucun n'existe, et le
   registre d'unicité doit être lu avant le premier (trois familles déjà prises : dentaire, labo,
   clinique).

---

## 6 · Réutiliser les designs dentaire et labo — la réponse, avec le prix réel

King : *« we can reuse the designs for dentaire and labo since no client has bought it yet, what do you
think ? »* **Oui, et c'est même la meilleure nouvelle du week-end** — mais pas en l'état : les six pages
récupérables portent l'identité complète de leurs anciens prospects.

### 6.1 · Elles sont récupérables, et je l'ai vérifié

Le bac était un clone **shallow** (`git rev-list --all` = 2 commits) : l'historique a été récupéré
(`git fetch --unshallow`, 730 commits), et chaque fichier supprimé le 24/10 a été retrouvé à son commit
d'origine (`54d962cb` pour cinq d'entre eux, `38b7f06c` pour JEMPO et Béthanie).

| Métier | Page | Taille | Ce qu'elle contient comme design |
|---|---|---|---|
| **Dentaire** | `concept-yaks-v1.html` | 616 Ko | roue des spécialités, bande de preuve, bento services |
| **Dentaire** | `concept-oracare-v3.html` | 1,1 Mo | bento + cartes de prix + hero photo, EN d'abord |
| **Laboratoire** | `concept-unilabo-v2.html` | 84 Ko | **la fiche de prélèvement comme unique motif**, fiche vivante |
| **Laboratoire** | `concept-afriquelabo-v1.html` | 296 Ko | console d'analyses, catalogue consultable, mono numéroté |
| Clinique (bonus) | `concept-labethanie-v1.html` | 260 Ko | dépliant de soins, liste cochable → un message WhatsApp |
| Clinique (bonus) | `concept-jempo-v1.html` | 164 Ko | quatre portes (spécialité → praticien → rendez-vous) |

### 6.2 · Ce qui bloque la réutilisation telle quelle

Le contrôle de fuite sur les six, fait ce soir :

| Fichier | Ce qui reste dedans |
|---|---|
| yaks | `YAKS`, `Skye`, `Logbessou` |
| oracare | `OraCare`, `Skye`, `Molyko` |
| unilabo | `UNI-LABO`, `Bonamoussadi`, `Bonabéri` |
| afriquelabo | `AFRIQUE LABO`, `Bessengue`, **numéro `690 54 70 93`** |
| labethanie | `La Béthanie`, `Bonabéri`, **deux numéros** |
| jempo | `JEMPO`, `Deido`, `Bessengue` |

Aucune n'est réutilisable en l'état : publier la page d'un ancien prospect sous un nom fictif, avec son
numéro dedans, c'est exactement ce que `tools/video/anonymise.py` a été écrit pour empêcher (son contrôle
fort avait trouvé **21 fuites** que l'ancien test laissait passer).

### 6.3 · Ce que je recommande

**Réutiliser la direction, pas le fichier** — trois raisons :

1. **Le registre d'unicité garde déjà l'essentiel** (`clients/_uniqueness-registry.md`) : archétype,
   palette, typographie, ton de chaque page. C'est ça qui coûte cher à inventer, et c'est déjà écrit.
2. **Les fichiers sont lourds** (616 Ko à 1,1 Mo, images en base64, polices embarquées) : repartir d'eux
   pour en faire une page générique coûte plus qu'un build neuf sur le gabarit DM, plus léger et déjà
   outillé (`demos/dmoptic-v1.tpl.html` + builder).
3. **La règle du 20/10** — le site ne montre que du vrai : une page de concept ne peut pas hériter des
   photos d'un cabinet qui n'a pas signé.

**Donc : deux concepts neufs (dentaire, laboratoire), construits sur le gabarit DM, avec les directions
déjà tirées** — « roue des spécialités » pour le dentaire, « la fiche de prélèvement » pour le labo — et
**le contrôle de fuite en porte de sortie**, pas en option. Les anciens fichiers restent dans l'historique
git comme référence visuelle : on les ouvre, on ne les publie pas.
