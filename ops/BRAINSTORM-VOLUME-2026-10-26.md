# BRAINSTORM — 26/10/2026 (tour 155) · la cadence : 1, 20 ou 50 messages par jour ?

```text
Étape 0  graphe rejoué 26/10 10:42 (12 856 nœuds) · carte lue §0/§6/§2/§3
Demande  King : « we can't be sending just 1 message per day, we send between 20-50, in cold messaging
         volume counts, you can do research on it » + une vidéo : value-first, mockup gratuit, preuve.
Ruling   le 1/jour du 05/10 est **révisé** — pas oublié. Ce qui le fondait reste vrai, et c'est ce qui
         fixe la nouvelle règle : ce n'est pas le nombre qui fait bannir, c'est le **motif** et le **ratio**.
```

## 1 · Ce que le dépôt disait, et pourquoi il disait 1

| Source interne | Ce qu'elle dit | État |
|---|---|---|
| `sales/LISTE-OPTICIENS-2026-10.md` §1 | « cadence 1/jour — ruling 05/10 : 2/jour veto, spam flag + liste brûlée en 5 j » | **révisé aujourd'hui** |
| `sales/Playbook-Addendum-4` (15/09) §blasts | « au-delà de ~15 nouvelles conversations/jour, c'est une décision **WhatsApp Business API**, pas un bricolage sur une ligne personnelle » | **c'est exactement le seuil franchi** |
| `sales/AMK-Facebook-Page-Setup.md` §spam | « 3 nouvelles conversations/jour la première semaine » — pour une **page Facebook neuve** | hors sujet ici (WhatsApp, numéro établi) |

Le 05/10, la règle a été écrite après un **drapeau**. Le numéro avait alors quelques semaines et le lot
partait avec des textes proches. Les deux conditions ont changé : le numéro a trois mois de conversations
réelles, et la fabrique garantit aujourd'hui qu'aucun message ne partage douze mots avec un autre.

## 2 · La recherche — ce qui est vérifiable, et ce qui ne l'est pas

**Sur WhatsApp, personne ne publie de plafond.** Meta ne documente que l'API. Pour l'application
gratuite, les chiffres qui circulent sont des observations de praticiens, pas des règles :

| Affirmation | Source, date | Ce qu'on en retient |
|---|---|---|
| 20–50 messages/jour les 3 premiers jours pour un numéro neuf, montée jusqu'à 200/jour en trois semaines ; **sous 200/jour par numéro** est le plafond observé | whapi.cloud, 11/09/2026 — « community-tested », pas officiel | **20–50 n'est pas un seuil de danger**, c'est le haut du démarrage |
| Le déclencheur n°1 est le **ratio de blocages et de signalements**, pas le volume : « dix blocages sur cinquante envois est bien pire qu'un sur mille » | leadsflyer, 18/10/2026 | le nombre de messages ne tue pas ; le **contenu qui agace** tue |
| Un taux de signalement de **2 à 3 %** suffit à déclencher une restriction | ask4lead, 24/07/2026 | c'est notre unique métrique d'arrêt |
| Un **pic soudain** (20 → 2 000 en une nuit) est lu comme un compte compromis | ask4lead, 24/07/2026 | d'où la montée progressive, pas 1 → 40 |
| API : 250/jour non vérifié, 1 000 après vérification, limites **par portefeuille** depuis octobre 2025 | chatarmin, 01/09/2026 ; rmdialer, 20/08/2026 | l'API existe si on veut 200+/jour avec opt-in |

**Sur le courriel froid**, où les chiffres sont mesurés, la réponse est plus intéressante encore :

| Approche | Envois/jour | Taux de réponse | Réponses/jour | Temps par message |
|---|---|---|---|---|
| Blast générique | 200 | 2 % | **4,0** | 30 s |
| Personnalisation basique | 100 | 4 % | 4,0 | 1 min |
| Personnalisation forte | 30 | 12 % | **3,6** | 5 min |
| Hyper-personnalisation | 10 | 20 % | 2,0 | 15 min |

*(inboxkit, 06/09/2026 — tableau de benchmark, données d'éditeur.)*

**Le tableau dit deux choses à la fois.** 30 messages très personnalisés rapportent **presque autant**
que 200 génériques — mais coûtent **2 h 30** contre 1 h 40. Et 20–49 envois par boîte obtiennent un taux
**supérieur de 27 %** à la moyenne (5,7 % contre 4,5 %, Hunter.io, 2026).

**Donc King a raison sur le chiffre, et le chiffre exact est 20–50, pas plus.** Ce n'est pas le volume
qui est puni : c'est le volume **sans personnalisation**. Les paliers mesurés (Gangly, 500 courriels,
T1 2026) :

| Palier | Taux de réponse |
|---|---|
| 0 — blast | 2,1 % |
| 1 — prénom seul | 2,6 % |
| **2 — nom + entreprise + rôle** | **4,4 %** |
| 3 — une ligne vraiment recherchée | 7,8 % |
| 4 — déclencheur réel (événement, signal) | 11,2 % |

À 40 messages par jour au palier 2 : **1,8 réponse/jour**. À 8 messages au palier 4 : 0,9. **Le volume
gagne — à condition de ne pas descendre au palier 1.** C'est toute la conception de la fabrique.

## 3 · Ce que la vidéo ajoute, et ce qu'elle ne peut pas nous faire faire

La vidéo propose quatre choses. Trois sont déjà dans nos règles ; une est **refusée**, et il faut dire
pourquoi.

| Proposition | Notre état | Verdict |
|---|---|---|
| **Valeur d'abord** : ne pas ouvrir sur le prix ni sur un argumentaire | `PLAYBOOK` §0 ligne 5 : le prix vient quand il est demandé | **déjà la règle** |
| **Personnaliser** : citer un détail réel, pas un prénom | `RESEARCH-STANDARD` §8c : une preuve datée par affirmation | **déjà la règle**, c'est ce qui coûte |
| **Sa propre vitrine comme preuve** | notre site existe ; il est le même pour tous | **à montrer**, pas à raconter : c'est l'objet de l'offre |
| **Maquette gratuite par prospect** | **refusée le 24/10** : 15 aperçus construits pour 1 client payant, retirés le même jour | **remplacée**, voir §4 |
| Vidéo explicative de 5 minutes après intérêt | nous avons 20–30 s de reel, aucun expliquer de 5 min | **dette** (§6) |

**Le refus, en une phrase** : une maquette *par prospect* est un travail non payé dont le taux de
conversion est inconnu ; quatre maquettes **par métier**, déjà construites et réutilisables, donnent la
même preuve pour un coût marginal nul.

## 4 · L'offre qui rend 40 messages possibles : la page qui existe déjà

La personnalisation coûte cher parce qu'elle demande un **fait par prospect**. Nous avons exactement
**19 profils WhatsApp vus** (porte A, capture du 25/10) pour 71 lignes envoyables. Impossible de tenir
40/jour avec ça.

La fabrique contourne le problème sans mentir : elle n'affirme **rien** sur le prospect et offre une
**page réelle, par métier**, déjà dans le dépôt.

| Métier | La page offerte | Ce qu'elle est |
|---|---|---|
| opticien | `dmoptiquesarl.com` | **client payant**, en production |
| clinique | `hosting/samples/clinic-bonaberi.html` | échantillon interne, jamais envoyé |
| école | `hosting/samples/mitoc.html` | échantillon interne |
| laboratoire | `hosting/previews/labiomed/` | aperçu envoyé le 19/09, fil en « report motivé » |

Le message ne dit pas « j'ai un client dans votre métier » — il dit « j'ai fait la page d'un opticien de
Douala » (vrai) ou « d'une école de Douala » (vrai) et propose d'envoyer le lien. **Zéro affirmation sur
le prospect, donc zéro risque de la phrase fausse** qui a coûté le 24/09.

## 5 · Les trois options

| | **A — 40/jour tout de suite** | **B — 20 puis +10/jour** | **C — rester à 10/jour** |
|---|---|---|---|
| Ce qu'on gagne | le volume maximal dès demain | 200 messages en 8 jours, sans pic | zéro risque de drapeau |
| Ce qu'on perd | un pic 1 → 40 est **le** signal de compte compromis | trois jours avant le plein régime | la seule variable qui compte : le nombre de tentatives |
| Le risque | le numéro, c'est-à-dire tout le canal | faible | un lot de 71 lignes épuisé en 7 jours, puis plus rien |

## 6 · Recommandation — **B**, avec la porte qui manquait

1. **Montée en cinq jours** : 20 (27/10) → 30 (28/10) → 40 (29/10) → 40 (30/10) → 50 (31/10) si le
   ratio de blocages reste **sous 1 %**. Un pic vers 40 le premier jour est précisément ce que la
   recherche cite comme déclencheur.
2. **Interrupteur** : un seul blocage signalé → on s'arrête pour la journée, on relit les trois derniers
   messages, on reprend à −50 %. À 2 % de signalements sur 24 h → arrêt, et on rouvre avec un texte neuf.
3. **Aucun texte identique** — c'est désormais une porte : `audit_outreach` §10 bloque toute séquence de
   douze mots répétée dans trois messages, et la fabrique **refuse d'écrire** un lot qui la contient.
4. **La contrainte réelle n'est pas la cadence, c'est le stock** : 71 lignes envoyables aujourd'hui,
   soit **1,8 jour à 40/jour**. Le gisement ONOC est épuisé (28 testés, 0 restant). Il faut **200 numéros
   par semaine** pour tenir — et nous n'avons aucun outil qui les trouve sans réseau (§7).
5. **Ce qui reste interdit, volume ou pas** : affirmer un fait non vérifié ; écrire deux fois au même
   numéro (le CRM contient **3 doublons de numéro**, la fabrique les écarte) ; promettre une fiche Google
   validée ; construire une page par prospect avant son accord.

## 7 · Ce qui manque, et qui ne s'invente pas ici

- **Aucun accès réseau aux annuaires** dans cet environnement (seuls GitHub, npm et PyPI sortent). La
  fabrique ne peut donc pas trouver de nouveaux numéros : elle ne peut que **composer** sur le stock.
- **Le CRM n'a pas de clé** : 152 lignes sur 190 n'ont pas d'`ID`. Tout ce qui compte les envois
  (relances, doublons, tracker) repose sur une identité qui n'existe pas — c'est réparé côté outils
  (clé = `slug`), pas côté données.
- **La vidéo de 5 minutes n'existe pas.** Nous avons des reels de 20–30 s. C'est une dette datée, pas
  un oubli : elle ne se produit pas avant EP02.

## 8 · Ce que la journée a appris en écrivant — la contrainte n'est pas la cadence, c'est la preuve

Le §6 recommandait 20 → 30 → 40 → 40 → 50. Trois heures plus tard, en construisant de quoi le tenir,
trois chiffres ont changé la recommandation.

**① Le stock n'est pas de 71 lignes, il est de 52 messages.** Mesuré par la fabrique, pas estimé : sur
190 lignes du CRM, 78 ont un numéro joignable et ne sont pas contactées ; 52 seulement ont un numéro, un
métier avec une page qui existe, et un **lieu sûr**. Seize lignes ont une ville qui est un nom de
personne (« Madam Namondo Alexander ») : écrire « à Madam Namondo Alexander vous êtes… » serait la faute
la plus visible du lot. On ne les écrit pas — on les compte comme dette de données.

**② La preuve est encore plus rare que le stock : 7 lignes sur 77 sont à 3/3.** Le vérificateur du matin
l'a dit (`leads/VERIF-2026-10-26.md`) : sept ENVOYER, neuf KING-TRANCHE, soixante et une sans aucune
porte franchie. Autrement dit, **la contrainte de la semaine n'est pas « combien on envoie par jour »,
c'est « combien de profils King ouvre le matin »**. À huit secondes par ligne, ouvrir quarante profils
coûte cinq minutes — c'est faisable, et c'est le seul chemin vers 40 par jour.

**③ Un texte propre n'est pas un message qu'on a le droit d'envoyer.** Le lot de 49 messages du matin
passait la porte avec **0 bloquant** — et contenait **neuf cabinets à 2/3** et **un à 1/3**, dont sa
première ligne. La porte mesure le texte ; le vérificateur mesure le droit d'écrire. Il fallait les deux,
et c'est désormais écrit dans le lot lui-même (`sales/ENVOI-VOLUME-2026-10-27.md`, section du compte).

### La table qui remplace le plan de montée

| Jour | Envois | D'où | Réserve après |
|---|---|---|---|
| **lun. 27/10** | **20** | 7 écrits à la main (3/3) + 13 de la vague 3 | 33 |
| **mar. 28/10** | **22** | lot volume, opticiens d'abord | 11 |
| **mer. 29/10** | **11** | fin du lot volume + les 3 restants de la vague 3 | **0** |
| jeu. 30/10 | **0** | plus une ligne composable : journée de **sourcing**, pas d'envoi | 0 |

C'est moins glorieux que 50, et c'est vrai. `python3 tools/outreach/supply.py plan` rend ce tableau et
**refuse** de promettre davantage : il compare, jour par jour, ce que la cadence demande et ce que le
stock prouve.

### Ce que la recherche dit du palier où nous sommes

Les messages de ces trois lots sont au **palier 2** — nom de l'établissement, quartier, métier, page du
métier. Ce n'est pas de la personnalisation profonde, et il faut le dire : sur 500 courriels mesurés en
2026, ce palier rend **4,4 %** de réponses, quand une ligne vraiment recherchée en rend **7,8 %** et un
déclencheur réel **11,2 %** (Gangly). À 20 par jour, cela vaut **0,9 réponse par jour** ; à 7 par jour
en personnalisation profonde, **0,8**. Le volume gagne donc — mais de peu, et seulement tant qu'on ne
descend pas au palier 1 (prénom seul) ni au palier 0 (publipostage).

**Conséquence pratique** : le prochain euro de qualité ne s'investit pas dans plus de phrases, il
s'investit dans **une ligne de fait par prospect** — c'est-à-dire dans les profils que King ouvre.

### Ce qui a été construit pour tenir, et ce qui manque encore

| Pièce | Ce qu'elle fait | Ce qu'elle refuse |
|---|---|---|
| `tools/outreach/compose.py batch` | écrit la journée (7 variantes × 3 phrases, charnière `(a, b, a+b)`), une page par métier | d'écrire un lot où une phrase atteint douze mots hors nom propre, ou deux messages partagent une séquence |
| `tools/outreach/supply.py plan` | dit ce que la cadence demande et ce que le stock tient | de promettre plus de messages qu'il n'y a de lignes |
| `tools/outreach/supply.py ingest` | valide une liste collée (annuaire, page Facebook, passage) : neuf chiffres, doublons écartés | d'écrire dans le CRM — il ne produit qu'un fichier de transit |
| `tools/outreach/scout.py verify` | applique les trois portes et nomme les contradictions | d'inventer une porte : sans capture datée, elle reste `inconnue` |

**Ce qui manque, et qui ne s'invente pas dimanche soir** : les numéros. Il en faut **200 par semaine**
pour tenir 40/jour, et cet environnement n'a de réseau que vers GitHub, npm et PyPI — aucun annuaire.
La seule voie est celle du §7 : King ouvre les annuaires et les pages Facebook, `supply.py ingest`
nettoie ce qu'il colle, `scout.py verify` dit ce qui a le droit de partir.
