# CAMPAGNE VOLUME — le protocole des 20 à 50 messages par jour (26/10/2026)

```text
DÉCISION King, 26/10 : « we can't be sending just 1 message per day, we send between 20-50 ».
Ce document dit comment on tient cette cadence sans perdre le numéro, ce que la fabrique garantit,
et ce que King fait chaque matin en 25 minutes.
Deux fichiers, 35 messages écrits et mesurés le 26/10, tous à 0 bloquant 0 avertissement :
         sales/LOT-1-2026-10-27.md (5 à la main, tous à 3/3, version v4 du 26/10)
         sales/ENVOI-VOLUME-2026-10-27.md (30 par la fabrique, partis en 13 puis 17)
La vague 2 est retirée : sales/retires/ENVOI-VAGUE-2-2026-10-26.md (doublon du LOT 1 + deux messages
non réécrits : Free Optic et Capelli passent au LOT 2).
Le troisième lot du matin est retiré : sales/retires/ENVOI-VAGUE-3-2026-10-26.md (12 cibles mortes
ou déjà pourvues d'un site, 4 doublons).
```

## 1 · La montée, jour par jour

Un pic de 1 à 40 messages en une nuit est **le** signal qu'utilise WhatsApp pour repérer un compte
compromis (ask4lead, 24/07/2026). On monte donc par paliers, et le palier ne s'ouvre que si le
précédent n'a produit aucun blocage.

| Jour | Messages | D'où ils viennent | Ce qui doit être vrai la veille |
|---|---|---|---|
| **lun. 27/10** | **20** | les **7** écrits à la main (3/3, en tête) + **13** du lot volume | — |
| **mar. 28/10** | **17** | fin du lot volume, opticiens d'abord | 0 blocage, 0 signalement le 27 |
| **mer. 29/10** | **0** | plus une seule ligne composable | **journée de sourcing, pas d'envoi** |
| jeu. 30/10 | 20 | **nouveau stock obligatoire** (§4) | 0 blocage le 28 |
| ven. 31/10 | — | rien : paiement DM Optique, on ne mélange pas | — |
| lun. 02/11 | 20–30 | nouveau stock + les dates de la porte B | ratio de blocages < 1 % |

**Ce que la table dit vraiment** : la cadence de 20–50 tient **deux jours**, puis elle bute sur le stock.
52 lignes sont composables au total, **16 sont écartées** (numéro mort ou cabinet déjà pourvu d'un site),
**36 restent** — et **37 messages sont écrits** : il n'y a plus une seule ligne libre.

**Le vrai chiffre du jour** : assez de texte pour deux jours, assez de numéros **prouvés pour sept** (les
3/3 de la vague 2), et **30 messages dont 14 seulement ont deux portes sur trois**. `supply.py plan` rend
un tableau plus flatteur (20 / 22 / 36) parce qu'il compte les **pistes** ; la fabrique, elle, ne peut
écrire que ce que la ligne prouve. L'écart entre les deux est exactement le sujet du §4.

## 2 · L'interrupteur — la seule métrique qui arrête la campagne

Le volume ne fait pas bannir ; le **ratio de blocages** le fait — dix blocages sur cinquante envois est
bien pire qu'un sur mille (leadsflyer, 18/10/2026), et 2 à 3 % de signalements suffisent (ask4lead).

| Ce qu'on voit | Ce qu'on fait |
|---|---|
| **0 blocage** sur la journée | on monte d'un palier le lendemain |
| **1 blocage** | on s'arrête pour la journée ; on relit les trois derniers messages ; on reprend à −50 % |
| **2 % de signalements sur 24 h** | arrêt complet ; on ne reprend qu'avec un texte neuf et un angle différent |
| **un « stop » explicite** | ce numéro ne reçoit plus jamais rien, définitivement — et le CRM le note |

**Comment on le mesure sans outil** : WhatsApp Business affiche les messages bloqués dans
`Paramètres → Confidentialité`; le tracker (§5) porte une colonne `bloqué` que King coche. **Une case
cochée = un blocage.** Pas de mesure automatique : nous n'avons pas d'accès à son compte.

## 3 · Ce que la fabrique garantit, et ce qu'elle ne garantit pas

`tools/outreach/compose.py` écrit les messages ; `tools/qa/audit_outreach.py` les juge.

| Garanti par l'outil | Non garanti — et ça reste humain |
|---|---|
| aucun message ne partage **douze mots** avec un autre du lot (§10) | que le fait soit vrai : la fabrique ne dit que ce que la ligne prouve, elle ne prouve rien |
| 35 à 55 mots, une seule question, une question qui **demande une action** | que le numéro **joigne WhatsApp** : c'est la porte A, et c'est le geste de King |
| aucun lien, aucun prix, aucune signature, aucun emoji | que le message tombe juste — un message qui passe la porte peut rester plat |
| aucun doublon de numéro dans le lot — **mesuré le 26/10** : 3 numéros du CRM vivent sur deux lignes, il n'en reste **qu'un** dans le stock envoyable (CEMECES ↔ INSES, 674 93 66 04), et la fabrique garde la première | le bon moment de la journée |
| l'objet de l'offre correspond au **métier** (une école n'entend pas parler d'opticien) | que l'interlocuteur soit le décideur (porte C) |

**Réserve** : la fabrique plafonne à **49 messages par lot** — au-delà, elle refuse plutôt que de
répéter un motif. Ce n'est pas la limite du jour : **le stock s'épuise avant les variantes** (37 écrits,
0 ligne libre). Étendre les variantes n'ouvrirait rien tant que le §4 n'est pas fait.

## 4 · Le stock — la contrainte que la cadence révèle

| Gisement | Ce qu'il reste | Pourquoi |
|---|---|---|
| Opticiens ONOC | **0** | 28 testés le 25/10, 22 joignables, **0 restant** |
| Annuaire (137 lignes) | ~70 jamais contactées | dont **17** avec un profil vu le 25/10 — les autres sont des numéros non prouvés |
| Cliniques, labos, écoles | ~36 | verticales mesurées à **0/15** de réponses : à ne rouvrir qu'avec l'offre, pas avec l'angle « nom » |
| **Total envoyable** | **78** | mais **41 sans message écrit** : ni métier avec une page, ni lieu sûr — c'est le stock à sourcer, pas à composer |

**Ce qu'il faut** : environ **200 numéros par semaine** pour tenir 40/jour. Le mode d'emploi complet —
quatre sources nommées, vingt minutes de gestes, ce qu'on écarte — est dans `sales/SOURCING-2026-10-27.md`.
Trois sources, dans l'ordre de rendement observé :

1. **Les annuaires de Douala** (pagespratiquescm, maligah, doualazoom) — 68 % des numéros y joignent
   WhatsApp (leçon du 19/09). **King seul peut les ouvrir** : cet environnement n'a pas de réseau vers
   les annuaires. Il colle ce qu'il trouve, et `supply.py ingest` nettoie :
   `python3 tools/outreach/supply.py ingest --in ~/annuaire.csv --source annuaire --vu 2026-10-27`
   → neuf chiffres exigés, préfixes `+237`/`00237` ramenés à neuf, doublons du CRM et doublons internes
   écartés, un **fichier de transit** (`leads/STAGING-<date>.csv`), jamais le CRM directement.
   Plus rapide encore quand la source est une page web : il la **colle** et laisse l'extracteur sortir
   les numéros — `python3 tools/outreach/supply.py extract --in /tmp/p.txt --source facebook`.
2. **Les pages Facebook professionnelles** — elles donnent le nom, le quartier et souvent le numéro.
3. **Le passage** — une affiche relevée en boutique vaut trois numéros d'annuaire (une seule ligne du
   CRM vient de là, et c'est la mieux renseignée).

## 5 · Le tracker — quinze messages partis le 26/10, relance le 28/10

| # | Lot | Cabinet | Envoyé | Lu | Répondu | Relance |
|---|---|---|---|---|---|---|
| 1 | 1 | Ets Espace Médical · 655 04 95 29 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 2 | 1 | ASS pour RRPHDD · 675 39 90 23 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 3 | 1 | ISEE · 656 97 80 43 | **☑ 26/10 15:15** | **☑ 15:41** | **☑ « Bonjour » 15:41** | **aucune — clos 16:04** |
| 4 | 1 | Bellevue Optique · 694 89 26 96 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 5 | 1 | S.O.S Vision · 699 86 04 63 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 6 | 2 | Capelli Optique Médicale · 675 26 89 81 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 7 | 2 | Saoudia Optique · 696 04 04 13 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 8 | 2 | Pagrot Optique · 699 90 46 91 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 9 | 2 | Light Optique · 677 64 87 90 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 10 | 2 | Optique Pro · 690 03 48 18 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 11 | 3 | Free Optic · 679 11 37 60 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 12 | 3 | London Vision · 696 76 81 16 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 13 | 3 | Maranatha Optics · 658 16 31 90 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 14 | 3 | Africa Optic · 691 28 02 37 | **☑ 26/10** | ☐ | ☐ | 28/10 |
| 15 | 3 | Alpha Optic · 699 57 34 57 | **☑ 26/10** | ☐ | ☐ | 28/10 |

**État au 26/10, 16 h 30.** Quinze messages partis, **une réponse** (ISEE, 26 minutes, sur un message faux),
**zéro conversation engagée**, un fil fermé par King lui-même. Les quinze lignes sont dans `leads/CRM.csv`
avec `last_send_state=sent`, `stage_since=2026-10-26`, `Follow-up date=2026-10-28` — sauf ISEE, `parked`,
sans date de relance.

**Les colonnes « Lu » et « Répondu » ne se remplissent qu'avec une capture.** Un accusé de lecture n'est
pas une réponse, et l'absence d'accusé ne prouve pas que le message n'a pas été lu : sur WhatsApp Business,
les ticks bleus dépendent des réglages du destinataire.

**Le chiffre qui décide de la suite** reste `réponses < 48 h` : **1 / 15** à cette heure, et elle est
arrivée sur un message faux. Aucun taux camerounais n'existe encore dans nos sources.

**Le plan de relance est écrit** : `sales/PLAN-RELANCE-2026-10-28.md` — qui relancer, avec quel second
fait, et pourquoi la relance du 28/10 est **une exception datée** à la règle du J+7.


### 5 bis · LOT 3 — cinq lignes ouvertes, aucune cochée

| # | Cabinet | Envoyé | Lu | Répondu | Bloqué |
|---|---|---|---|---|---|
| 11 | Free Optic · 679 11 37 60 | ☐ | ☐ | ☐ | ☐ |
| 12 | Tchaya Optique Akwa · 699 98 87 24 | ☐ (contrôle 60 s) | ☐ | ☐ | ☐ |
| 13 | Star Optic · 654 04 68 45 | ☐ (contrôle 60 s) | ☐ | ☐ | ☐ |
| 14 | Cabinet d'Optique la Rétine · 695 47 43 64 | ☐ (contrôle 60 s) | ☐ | ☐ | ☐ |
| 15 | Kamaïs Optic · 678 43 54 60 | ☐ (ruling : 2ᵉ approche) | ☐ | ☐ | ☐ |

**ISEE (n° 3) est clos le 26/10 à 16 h 04** : King a fermé la conversation lui-même (« autant pour moi, je
n'avais pas vu votre site… bonne continuation »). Aucune relance après un mot pareil — le dossier reste
chaud pour dans six mois, pas pour cette semaine.

## 6 · Les 25 minutes du matin

| Minute | Geste |
|---|---|
| 0–5 | ouvrir les 20 numéros du jour sur WhatsApp, vérifier qu'ils **joignent** ; barrer les morts. C'est aussi là que la porte B apparaît : un profil Business vu, et la ligne passe de 2/3 à 3/3 |
| 5–25 | envoyer, dans l'ordre du fichier, **un par un** — jamais un copier-coller groupé. Un « stop » = plus jamais, et on le note |
| à tout moment | la première réponse se traite **dans l'heure** (§7 `CLIENT-MESSAGING-RULES`) : c'est la seule fenêtre où le prospect est devant son écran |

**Le soir, 5 minutes** : cocher le tracker. Ce qui n'est pas coché le soir n'existe pas le lendemain.

## 7 · Ce qui reste interdit, volume ou pas

- Affirmer un fait non vérifié — « vous n'avez pas de site » sans capture datée (§8c).
- Écrire deux fois au même numéro — la fabrique écarte les doublons, King ne les rajoute pas à la main.
- Promettre une fiche Google « validée » ou un chiffre de patients.
- Construire une page **par prospect** avant son accord (ruling 24/10) : l'offre porte sur les pages qui
  existent déjà, une par métier.
- Envoyer du même texte à plusieurs — la porte le bloque, et c'est la seule chose qui protège le numéro.
