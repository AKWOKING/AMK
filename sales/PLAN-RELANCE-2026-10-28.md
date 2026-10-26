# Plan de relance — mercredi 28/10/2026 (écrit le 26/10, 16 h 40)

```text
ÉTAPE 0   graphe rejoué 26/10 16:25 (13 320 nœuds) · carte lue §0/§6/§2/§3/§1/§3 bis · ask « CRM à jour
          après les trois lots du 26/10, fin de l'outreach, relance mercredi 28/10 » → lus :
          knowledge/OUTREACH-MESSAGING-2026-10-22.md, sales/CLIENT-MESSAGING-RULES.md §3/§13,
          leads/CRM.csv, sales/CAMPAGNE-VOLUME-2026-10-26.md §5, tools/superpowers/skills/brainstorming
PRE-FLIGHT : outreach / clôture de journée → PRE-FLIGHT.md lu (§00, §0, §0b, §0c), MACHINE.md lu
PORTE     les trois modèles vivent dans `sales/RELANCE-2026-10-28.md`, pas ici — un plan qui cite des
          messages non mesurables est un plan sans porte.
          python3 tools/qa/audit_outreach.py sales/RELANCE-2026-10-28.md --strict
          → 0 bloquant, 0 avertissement (53 / 70 / 67 mots, 3 et 4 phrases, 1 question)
ÉTAT      15 messages partis le 26/10 · 1 réponse (ISEE « Bonjour », 15:41) · 0 conversation engagée
          · 1 fil fermé par King (16:04) · 14 suivis ouverts au 28/10
```

## 1 · Ce que la pré-vol a donné, et qui change le plan

Trois choses, lues et non supposées :

1. **La règle écrite dit J+7, pas J+2.** `sales/CAMPAGNE-VOLUME-2026-10-26.md` §5 étape 5 : « pas de
   relance avant J+7, une seule ». Mercredi 28/10, c'est **J+2**. Ce n'est donc pas une relance ordinaire :
   c'est une **exception datée**, et elle doit être écrite comme telle — sinon la règle suivante ne vaudra
   plus rien non plus.
2. **Le CRM ne savait rien de la journée.** Les 15 lignes étaient encore en `prospecting`, `last_send_state`
   vide, aucune date de suivi. Corrigé : `sent`, `stage_since=2026-10-26`, `Follow-up date=2026-10-28`
   partout, sauf ISEE (`parked`, aucune relance).
3. **Le seul chiffre vivant est 1 / 15**, et il est arrivé sur un message faux. Un taux de réponse à J+1 ne
   dit rien : il faut attendre 48 h avant de conclure quoi que ce soit sur la formulation.

## 2 · Ce que je sais, et ce qui n'est pas décidé (brainstorming)

Ce que King a demandé, dans ses mots : *« Sent all the messages for today so we can end outreach for today,
and follow up on Wednesday »*. Donc : arrêt aujourd'hui, reprise mercredi. Ce qui n'est **pas** dit, et qui
change tout ce qu'on écrit mercredi :

| Question ouverte | Pourquoi elle décide du contenu |
|---|---|
| **Relance-t-on ceux qui n'ont jamais ouvert ?** | Une relance sur un message que personne n'a ouvert ne convertit rien : elle ajoute un deuxième non-lu. Elle ne coûte que du temps — mais elle coûte aussi une des deux cartouches (on n'a droit qu'à une relance). |
| **Que dit une relance à qui n'a pas répondu du tout ?** | Trois formes possibles : un **second fait** sur sa fiche, une **demande plus petite** (« oui ou non, un mot »), ou une **sortie propre** (« je clos, revenez quand vous voulez »). |
| **Combien de messages mercredi ?** | La cadence du §2 est 20–50/jour. On n'a que 14 suivis. Faut-il compléter avec un lot neuf, ou la journée est-elle aux relances ? |

## 3 · Trois approches — et celle que je recommande

**A · Relancer les 14, mercredi matin, avec un second fait.**
Simple, complet, et ça remplit la matinée. Coût : on brûle la cartouche unique de relance sur des gens qui
n'ont peut-être rien lu ; et 14 messages identiques dans la forme, ça se voit.

**B · Regarder les accusés de lecture mercredi matin, et ne relancer que ceux qui ont lu sans répondre.**
Une relance sert à transformer un « lu et oublié » en réponse ; elle ne sert à rien sur un « jamais ouvert ».
Coût : dépend des réglages WhatsApp du destinataire — un message lu sans accusé est invisible, et on
relancerait alors trop peu.

**C · Ne pas relancer mercredi : envoyer 5 nouveaux, et relancer les 14 le 02/11 (J+7).**
Respecte la règle écrite, garde du volume, et laisse 48 h de plus à une réponse spontanée. Coût : les 14
restent muets une semaine, et King a demandé mercredi.

**Recommandation : B, avec C en repli.** Raison : mercredi matin, King a une information que je n'ai pas —
les ticks. Si la majorité a lu sans répondre, on relance (forme 1 : second fait). Si presque rien n'est lu,
on ne relance pas : on part sur un lot neuf, et les 14 repartent au 02/11. **A n'est bon que si King veut du
volume mercredi quoi qu'il arrive** — dans ce cas il faut l'assumer comme une exception, pas la présenter
comme une règle.

## 4 · Le déroulé du 28/10, si B est choisi

| Heure | Geste | Sortie attendue |
|---|---|---|
| 08 h 30 | Ouvrir les 14 fils, noter **lu / non lu** dans le tracker §5 (colonne « Lu ») | une liste de 0 à 14 noms |
| 08 h 45 | Remplir le CRM : `last_send_state=delivered_unread` ou `read`, jamais deviné | 14 lignes justes |
| 09 h 00 | Écrire les relances **des seuls lus**, sur le modèle du §5, avec leur propre fait | 0 à 14 messages |
| 09 h 30 | `audit_outreach.py --strict` sur le fichier du jour → 0 / 0 exigé | porte |
| 10 h 00 | Envoyer, une heure d'écart minimum entre deux, noter l'heure | tracker |
| 14 h 00 | Si moins de 3 relances sont parties : **lot neuf de 5** (recherche d'abord, §5 du playbook) | volume |
| 17 h 00 | Clôture : compter `réponses < 48 h`, écrire une ligne dans l'Activity-Log | chiffre |

## 5 · Les trois modèles de relance — dans un fichier à part, et mesurés

Copie lisible ci-dessous ; **la version vérifiée est `sales/RELANCE-2026-10-28.md`** (c'est elle que la
porte mesure, 53 / 70 / 67 mots, 0 / 0). Ce ne sont pas des gabarits à copier tels quels : chacun est lié à
**son** fait, et le fait doit être revérifié le matin même avant l'envoi.

**Modèle 1 — la relance douce, sans second fait (LOT 1)**
> Bonjour, inattendu de revenir à Douala, et une seule fois : lundi je proposais un aperçu de site, sans réponse ; si le moment est mauvais, un mot et je clos.
> Je fais les sites pour les opticiens de Douala : horaires, examens et un bouton qui écrit.
> Voulez-vous que je vous envoie l'aperçu du site ?

**Modèle 2 — le second fait, revérifié le matin (LOT 2)**
> Bonjour, sans doute inutile de revenir à Bonamoussadi, mais j'ai revérifié l'annuaire ce matin : deux adresses y figurent toujours, et aucun plan.
> Sur la fiche, un patient doit encore choisir entre deux repères, sans carte pour l'aider.
> Je fais les sites pour les opticiens de Douala : le plan, les horaires et vos montures au même endroit ; un mot, et le vôtre existe.
> Voulez-vous que je vous envoie l'aperçu du site ?

**Modèle 3 — le fait qui a bougé (LOT 3)**
> Bonjour, inattendu de revenir à Akwa, et une seule fois : le lien annoncé sur votre page Facebook ne répond toujours pas, je viens de réessayer.
> Le patient qui clique dessus tombe sur une page vide, et rappelle l'annuaire.
> Je fais les sites pour les opticiens de Douala : horaires, montures et un bouton qui écrit ; un mot suffit pour clore.
> Voulez-vous que je vous envoie l'aperçu du site ?

## 6 · Les portes, avant tout envoi du 28/10

```bash
python3 tools/qa/audit_outreach.py sales/RELANCE-2026-10-28.md --strict   # 0 bloquant exigé
python3 tools/qa/audit_claims.py  sales/RELANCE-2026-10-28.md             # VERDICT : OK
python3 tools/ops/machine.py --check                                      # portes dures ouvertes
```

Et deux règles qui ne se mesurent pas : **un second fait se revérifie le matin même** (un horaire peut
changer en 48 h), et **une relance ne repitch jamais le site à qui en a un** — ISEE a payé pour l'apprendre.

## 7 · Ce que ce plan ne prouve pas

- **Que la relance marche.** Aucun taux camerounais ; les 15–20 % des messages documentés viennent de
  sources tierces de 2026, pas de Douala.
- **Que l'arrêt d'aujourd'hui était le bon moment.** 15 messages le même jour, c'est le haut de la cadence
  §2 ; la réponse viendra ou non dans les 48 h.
- **Que B soit meilleur que A.** La différence se mesurera mercredi soir : nombre de lus, nombre de
  relances parties, nombre de réponses.

## 8 · La seule question qui me bloque

**Mercredi matin, je relance les 14 — ou je pars sur cinq nouveaux et je laisse les 14 au 02/11 ?**
Réponds « relance » ou « lot neuf », et le plan s'exécute sans autre arbitrage.
