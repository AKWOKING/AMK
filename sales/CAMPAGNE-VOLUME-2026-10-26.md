# CAMPAGNE VOLUME — le protocole des 20 à 50 messages par jour (26/10/2026)

```text
DÉCISION King, 26/10 : « we can't be sending just 1 message per day, we send between 20-50 ».
Ce document dit comment on tient cette cadence sans perdre le numéro, ce que la fabrique garantit,
et ce que King fait chaque matin en 25 minutes.
Lot du jour : sales/ENVOI-VOLUME-2026-10-27.md — 49 messages, 0 bloquant, 0 avertissement.
```

## 1 · La montée, jour par jour

Un pic de 1 à 40 messages en une nuit est **le** signal qu'utilise WhatsApp pour repérer un compte
compromis (ask4lead, 24/07/2026). On monte donc par paliers, et le palier ne s'ouvre que si le
précédent n'a produit aucun blocage.

| Jour | Messages | Ce qui doit être vrai la veille | Lot |
|---|---|---|---|
| **mar. 27/10** | **20** | — | `ENVOI-VOLUME` J1 |
| **mer. 28/10** | **29** | 0 blocage, 0 signalement le 27 | `ENVOI-VOLUME` J2 |
| jeu. 29/10 | 30 | 0 blocage | **à composer** (stock 22) |
| ven. 30/10 | 40 | 0 blocage, ≥ 1 réponse humaine | **à composer** (stock épuisé) |
| sam. 31/10 | — | rien : journée de relance, pas d'envoi neuf | — |
| lun. 02/11 | 50 | ratio de blocages < 1 % | **nouveau stock obligatoire** |

**Ce que la table dit vraiment** : au-delà du 29/10, **nous n'avons plus de lignes**. 71 envoyables
aujourd'hui, 49 écrites. Les 22 restantes tiennent une journée. Le reste du plan dépend d'une seule
chose — trouver des numéros — et c'est le §4.

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
| aucun doublon de numéro dans le lot (3 existent au CRM, ils sont écartés) | le bon moment de la journée |
| l'objet de l'offre correspond au **métier** (une école n'entend pas parler d'opticien) | que l'interlocuteur soit le décideur (porte C) |

**Réserve** : la fabrique plafonne à **49 messages par lot** — au-delà, elle refuse plutôt que de
répéter un motif. Étendre la réserve (8ᵉ et 9ᵉ variantes par phrase) est un travail de 20 minutes qui
ouvre un lot de 81.

## 4 · Le stock — la contrainte que la cadence révèle

| Gisement | Ce qu'il reste | Pourquoi |
|---|---|---|
| Opticiens ONOC | **0** | 28 testés le 25/10, 22 joignables, **0 restant** |
| Annuaire (137 lignes) | ~70 jamais contactées | dont **19 seulement** avec un profil vu — les autres sont des numéros non prouvés |
| Cliniques, labos, écoles | ~36 | verticales mesurées à **0/15** de réponses : à ne rouvrir qu'avec l'offre, pas avec l'angle « nom » |
| **Total envoyable** | **71** | 1,8 jour à 40/jour |

**Ce qu'il faut** : environ **200 numéros par semaine** pour tenir 40/jour. Trois sources, dans l'ordre
de rendement observé :

1. **Les annuaires de Douala** (pagespratiquescm, maligah, doualazoom) — 68 % des numéros y joignent
   WhatsApp (leçon du 19/09). **King seul peut les ouvrir** : cet environnement n'a pas de réseau vers
   les annuaires.
2. **Les pages Facebook professionnelles** — elles donnent le nom, le quartier et souvent le numéro.
3. **Le passage** — une affiche relevée en boutique vaut trois numéros d'annuaire (une seule ligne du
   CRM vient de là, et c'est la mieux renseignée).

## 5 · Le tracker — une ligne par message, cinq colonnes

À tenir dans `leads/Daily Ops.csv` (jamais à la main dans le CRM : `leads/build/crm.py`).

| # | Cabinet | Envoyé | Lu | Répondu | Bloqué |
|---|---|---|---|---|---|
| 1 | Optique Pro · 690 03 48 18 | ☐ | ☐ | ☐ | ☐ |
| 2 | Africa Optic · 691 28 02 37 | ☐ | ☐ | ☐ | ☐ |

**Ce qui compte n'est pas « envoyé » mais « répondu »** — et le seul chiffre qui décide de la suite est
`réponses < 48 h`. Aujourd'hui il vaut **0**.

## 6 · Les 25 minutes du matin

| Minute | Geste |
|---|---|
| 0–5 | ouvrir les 20 numéros du jour sur WhatsApp, vérifier qu'ils **joignent** ; barrer les morts |
| 5–25 | envoyer, dans l'ordre du fichier, **un par un** — jamais un copier-coller groupé |
| à tout moment | la première réponse se traite **dans l'heure** (§7 `CLIENT-MESSAGING-RULES`) : c'est la seule fenêtre où le prospect est devant son écran |

**Le soir, 5 minutes** : cocher le tracker. Ce qui n'est pas coché le soir n'existe pas le lendemain.

## 7 · Ce qui reste interdit, volume ou pas

- Affirmer un fait non vérifié — « vous n'avez pas de site » sans capture datée (§8c).
- Écrire deux fois au même numéro — la fabrique écarte les doublons, King ne les rajoute pas à la main.
- Promettre une fiche Google « validée » ou un chiffre de patients.
- Construire une page **par prospect** avant son accord (ruling 24/10) : l'offre porte sur les pages qui
  existent déjà, une par métier.
- Envoyer du même texte à plusieurs — la porte le bloque, et c'est la seule chose qui protège le numéro.
