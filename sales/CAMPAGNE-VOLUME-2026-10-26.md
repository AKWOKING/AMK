# CAMPAGNE VOLUME — le protocole des 20 à 50 messages par jour (26/10/2026)

```text
DÉCISION King, 26/10 : « we can't be sending just 1 message per day, we send between 20-50 ».
Ce document dit comment on tient cette cadence sans perdre le numéro, ce que la fabrique garantit,
et ce que King fait chaque matin en 25 minutes.
Trois fichiers, 53 messages écrits et mesurés le 26/10, tous à 0 bloquant 0 avertissement :
         sales/ENVOI-VAGUE-2-2026-10-26.md (7 à la main, tous à 3/3)
         sales/ENVOI-VAGUE-3-2026-10-26.md (16 par la fabrique, 13 partent le 27)
         sales/ENVOI-VOLUME-2026-10-27.md (30 par la fabrique, 28 et 29/10)
```

## 1 · La montée, jour par jour

Un pic de 1 à 40 messages en une nuit est **le** signal qu'utilise WhatsApp pour repérer un compte
compromis (ask4lead, 24/07/2026). On monte donc par paliers, et le palier ne s'ouvre que si le
précédent n'a produit aucun blocage.

| Jour | Messages | D'où ils viennent | Ce qui doit être vrai la veille |
|---|---|---|---|
| **lun. 27/10** | **20** | les **7** écrits à la main (3/3, en tête) + **13** de la vague 3 | — |
| **mar. 28/10** | **22** | lot volume, opticiens d'abord | 0 blocage, 0 signalement le 27 |
| **mer. 29/10** | **11** | fin du lot volume + les **3** restants de la vague 3 | 0 blocage le 28 |
| jeu. 30/10 | **0** | plus une ligne composable | **journée de sourcing, pas d'envoi** |
| sam. 31/10 | — | rien : paiement DM Optique, on ne mélange pas | — |
| lun. 02/11 | 40–50 | **nouveau stock obligatoire** (≈ 200 numéros/semaine, §4) | ratio de blocages < 1 % |

**Ce que la table dit vraiment** : la cadence de 20–50 tient **deux jours et demi**, puis elle bute sur
le stock. 52 lignes sont composables au total ; 53 messages sont écrits. Et la moitié de ces 52 n'a
jamais été ouverte sur WhatsApp : la vérification de huit secondes décidera de leur sort.

**Le vrai chiffre du jour** : assez de texte pour trois jours, assez de numéros **prouvés pour un** (les
sept). `tools/outreach/supply.py plan` rend ce tableau et refuse d'en promettre un plus flatteur : il
compte les **pistes** que voit le vérificateur (77) et les **messages** que la fabrique peut écrire (52),
et il dit l'écart — 53 messages écrits pour 52 lignes, donc **un** message sans ligne. Le reste
du plan dépend d'une seule chose — ouvrir des annuaires — et c'est le §4.

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
répéter un motif. Étendre la réserve (8ᵉ et 9ᵉ variantes par phrase) est un travail de 20 minutes qui
ouvre un lot de 81.

## 4 · Le stock — la contrainte que la cadence révèle

| Gisement | Ce qu'il reste | Pourquoi |
|---|---|---|
| Opticiens ONOC | **0** | 28 testés le 25/10, 22 joignables, **0 restant** |
| Annuaire (137 lignes) | ~70 jamais contactées | dont **17** avec un profil vu le 25/10 — les autres sont des numéros non prouvés |
| Cliniques, labos, écoles | ~36 | verticales mesurées à **0/15** de réponses : à ne rouvrir qu'avec l'offre, pas avec l'angle « nom » |
| **Total envoyable** | **78** | 1,9 jour à 40/jour — **49 déjà écrites**, donc 29 en réserve |

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

## 5 · Le tracker — une ligne par message, cinq colonnes

À tenir dans `leads/Daily Ops.csv` (jamais à la main dans le CRM : `leads/build/crm.py`).

| # | Cabinet | Envoyé | Lu | Répondu | Bloqué |
|---|---|---|---|---|---|
| 1 | Ets Espace Médical · 655 04 95 29 | ☐ | ☐ | ☐ | ☐ |
| 2 | ASS pour RRPHDD · 675 39 90 23 | ☐ | ☐ | ☐ | ☐ |
| 3 | ISEE · 656 97 80 43 | ☐ | ☐ | ☐ | ☐ |
| … | les 7 de la vague 2, puis 13 de la vague 3, puis le lot volume | ☐ | ☐ | ☐ | ☐ |

**Ce qui compte n'est pas « envoyé » mais « répondu »** — et le seul chiffre qui décide de la suite est
`réponses < 48 h`. Aujourd'hui il vaut **0**.

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
