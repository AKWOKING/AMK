# Brainstorm — tenir 15 à 20 messages demain (27/10/2026), avec le stock qui existe

```text
ÉTAPE 0   graphe rejoué 26/10 18 h 59 (13 519 nœuds) · carte lue §0/§6/§2/§3/§1/§3 bis
PRE-FLIGHT  §00, §0, §0b, §0c, §0c bis · knowledge outreach (22/10, 26/10) · CLIENT-MESSAGING-RULES
            §13 → §13 sexies · tools/qa/audit_outreach.py (constantes) · tools/outreach/verify.py
DEMANDE   King, 26/10 : « prepare the outreach batch for tomorrow about 15-20 leads »
MÉTHODE   brainstorming (superpowers) : les faits d'abord, trois approches à part, puis trancher
ÉTAT      proposition — rien n'est envoyé, rien n'est écrit dans un lot tant que ce choix n'est pas fait
```

## 1 · Ce que le pré-vol a mesuré, et qu'on ne peut pas contourner

| Fait | Le chiffre | La source, datée |
|---|---|---|
| Numéros dont King a **vu** le profil WhatsApp et qui n'ont **jamais** reçu de message | **6** | `leads/CRM.csv` (`wa_verified=yes`, `Contacted=No`, `stage=prospecting`), capture du **25/10** dans `sales/PORTE-A-2026-10-25.md` §1–§2 |
| Messages déjà partis le 26/10 | **15** | `sales/CAMPAGNE-VOLUME-2026-10-26.md` §5 |
| Stock jamais contacté | **62** | `python3 tools/outreach/supply.py plan` (26/10) |
| Messages que la fabrique peut écrire | **22** — après correction du filtre ce soir (**38** avant, voir §1 bis) | `python3 tools/outreach/supply.py plan` (26/10, après le correctif) |
| Opticiens réellement composables et jamais approchés | **17** | 22 composables − 4 déjà vérifiés − 1 école |
| Numéros que King a testés et trouvés morts | 6 sur 28 (**21 %**) | `sales/PORTE-A-2026-10-25.md` §4 |
| Réponse mesurée sur les messages déjà partis | **1 / 15** (ISEE, sur un message faux) | `CAMPAGNE-VOLUME` §5 |

**La contrainte dure, en une phrase : nous savons écrire quinze messages, mais nous ne savons en
envoyer que six sans que King ait ouvert WhatsApp.** La porte A n'est pas une formalité de style : sur
28 numéros testés, 6 étaient morts, et deux « vivants » étaient des lignes personnelles (IVY, El Shadai).
Écrire « votre cabinet » à une ligne personnelle, c'est la faute d'ISEE en plus discret.

### 1 bis · Ce que la fabrique promettait de trop — corrigé ce soir

Les 38 « composables » mesurés au premier passage étaient un surcompte, recroisé ligne à ligne au CRM
et **corrigé dans le code** (`tools/outreach/compose.py`, deux refus ajoutés : `wa_verified=no` et site
vivant/déclaré). Le compte honnête est **22**. Ce que le filtre écarte désormais tout seul :

| Ligne comptée par la fabrique | Pourquoi elle n'est pas composable | Source |
|---|---|---|
| **Royal Optic** · 676 250 409 | WhatsApp a refusé le numéro le 24/09 | Notes CRM (`LOT 3`) |
| **Win Optic Plus** · 699 12 59 06 | **pas sur WhatsApp**, vérifié par King le 24/09 | Notes CRM (`LOT 4`) |
| **Cristalys Optic** · 690 94 51 50 | `cristalysoptic.com` **vivant** (24/09) : lui vendre un site est la faute du 24/09 | `Website` au CRM |
| **LyfyOptic** · 699 98 06 66 | `lyfyoptic.com` vivant (gabarit inachevé, mais c'est le sien) | `Website` au CRM |
| **Gift Optical** · 673 52 17 35 | site déclaré sur sa propre fiche, **en attente d'arbitrage** depuis le 24/09 | `Website` au CRM |
| **Maison Optique** · 657 73 70 45 | homonyme d'un `maison-optique.cm` déjà identifié sur un **autre** numéro — à ne pas confondre | `LOT-3` §0 |

Le gisement honnête est donc **32 messages possibles, dont 22 seulement sur des opticiens** — et parmi
ces 22, **6 ont un profil vu** (4 opticiens + COMED et IVY, cliniques). Pour quinze, il manque **neuf
ouvertures de WhatsApp**. Ce n'est pas un problème d'écriture, c'est un problème de geste humain.

## 2 · Trois approches, à part, sans les mélanger

### Approche A — « Les six d'abord » (le minimum vrai)

On écrit les six numéros dont la porte A est déjà capturée, on les envoie demain, et on garde les neuf
autres pour le 28.

- **Ce que ça donne demain** : 6 messages, 0 contrôle, 0 risque de numéro mort.
- **Ce que ça coûte** : la demande n'est pas tenue (6 pour 15–20), et six messages ne font pas un jour
  de campagne — le ruling « volume » du 26/10 reste sans effet.
- **Où ça casse** : à la deuxième journée, on aura consommé le stock vérifié et on se reposera la même
  question avec **zéro** numéro d'avance au lieu de neuf.
- **Verdict** : c'est le plancher, pas une stratégie. On le garde comme repli si King n'ouvre pas
  WhatsApp demain matin.

### Approche B — « Quinze écrits, neuf contrôles de soixante secondes » (recommandée)

On écrit **quinze messages ce soir**, en **trois sous-lots de cinq** (contrainte 169 non révoquée) :

- **sous-lot 1** : les 5 dont la porte A est déjà franchie et capturée (4 opticiens + COMED) → **partir
  sans contrôle** ;
- **sous-lot 2** : IVY (numéro vérifié, profil personnel — à confirmer) + 4 opticiens dont le numéro
  vient du tableau de l'Ordre ;
- **sous-lot 3** : 5 opticiens, même provenance.

Les neuf numéros du sous-lot 2 et 3 passent par le geste que le protocole prévoit déjà — **minutes 0 à 5
des « 25 minutes du matin »** (`CAMPAGNE-VOLUME` §6) : ouvrir, regarder le nom affiché, barrer les morts.
Chaque message porte son fait daté et sa source, donc un numéro qui saute ne laisse pas de trou : il
laisse une ligne barrée et un message reporté.

- **Ce que ça donne demain** : **15 messages prêts**, dont **5 partent sans rien attendre**, 10 après un
  contrôle de 5 minutes au total. Si 3 numéros sur 10 sont morts (le taux mesuré est 21 %), il en reste
  **12** — au-dessus du plancher de 15 moins l'usure, et on le sait d'avance.
- **Ce que ça coûte** : 5 minutes de King le matin, et l'honnêteté d'écrire « à confirmer » sur 9 lignes
  au lieu de faire semblant.
- **Où ça casse** : si le profil affiché sur un des neuf contredit le nom du message (leçon
  d'Ets Espace Médical → Optic Medical Favour and Joy), **on ne l'envoie pas** et le lot part à douze.
  C'est prévu, pas subi.
- **Variante haute** : King ouvre 15 numéros au lieu de 9 → on monte à 20 en ajoutant les cinq
  composables suivants (Caprice, Le Samaritain, Express, Mouscou déjà écrit, + 4). Le fichier est écrit
  pour que l'ajout soit une ligne, pas une réécriture.

### Approche C — « Vingt par la fabrique » (`compose.py batch --limit 20`)

On laisse l'atelier produire vingt messages d'un coup : il assemble depuis des réservoirs de phrases,
fait tourner la porte lui-même et refuse les lots qui se ressemblent.

- **Ce que ça donne demain** : 20 messages, 0 bloquant 0 avertissement **par construction**.
- **Où ça casse, et c'est mesuré** : la fabrique comptait **38** lignes dont **6 fausses** (§1 bis,
  corrigé depuis : 22) ; elle écrit sur l'angle « offre » avec un fait unique et générique (« les
  annuaires recopient votre fiche »)
  répété d'un message à l'autre — c'est exactement le motif que le §10 sanctionne, et le fichier
  `ENVOI-VOLUME-2026-10-27.md` en est déjà la démonstration : 30 messages, 9 doublons du tracker, une
  trame reconnaissable. Elle ne connaît pas non plus les six profils vus, qui sont notre meilleure matière.
- **Verdict** : bon outil de remplissage, mauvais plan de journée. À garder pour les jours sans matière.

## 3 · Comparaison, sur les seuls critères qui décident

| | A · six d'abord | **B · quinze, neuf contrôles** | C · vingt par la fabrique |
|---|---|---|---|
| Messages prêts ce soir | 6 | **15** | 20 (dont jusqu'à 6 lignes fausses avant le correctif) |
| Partent demain sans contrôle | 6 | **5** | 0 (numéros jamais testés) |
| Contrôles de King | 0 | **9 (≈ 5 min)** | 20 (≈ 15 min) |
| Fait daté + source par ligne | oui | **oui** | non (fait générique) |
| Risque §10 (ressemblance) | nul | **maîtrisé** (écriture à la main, 15 trames) | élevé (démontré le 26/10) |
| Risque d'écrire à un numéro mort | nul | **3 attendus sur 10, barrés avant l'envoi** | 4 attendus sur 20, découverts à l'envoi |
| Respecte 15–20 | non | **oui** | oui |

## 4 · Recommandation

**B.** Elle est la seule qui tienne la demande (15) sans inventer un seul fait, et elle transforme le
seul geste qui manque — ouvrir neuf profils — en cinq minutes déjà prévues par le protocole du matin.
Elle protège aussi la seule chose qui ne se rachète pas : un message envoyé à un numéro mort, ou à une
entreprise sous un nom qu'elle ne porte pas.

**Ce qui la rendrait fausse** : si King ne peut pas ouvrir WhatsApp demain matin, B retombe sur A (six
messages). Si King préfère ne rien envoyer tant que le client du site n'a pas répondu, B reste écrit et
attend — un lot écrit n'est jamais perdu, un lot envoyé l'est.

## 5 · Le plan d'exécution, si B est tranchée

1. **Écrire** `sales/LOT-2026-10-27.md` : trois sous-lots de cinq, quinze messages, un `FAIT` daté et
   sourcé sous chaque titre, une colonne « porte A » par ligne (✅ capturée le 25/10 / ⏳ à ouvrir).
2. **Passer la porte** : `python3 tools/qa/audit_outreach.py sales/LOT-2026-10-27.md --strict` jusqu'à
   **0 bloquant, 0 avertissement** — 35–70 mots, quatre phrases, une seule question, désarmement et
   preuve sociale compris, §10 vérifié entre les quinze.
3. **Écrire le protocole du matin** : les neuf numéros à ouvrir, dans l'ordre, avec ce qu'on regarde et
   ce qu'on fait si le nom ne correspond pas.
4. **Ne rien envoyer.** Le fichier part chez King ; l'envoi reste son geste, et le tracker
   (`CAMPAGNE-VOLUME` §5) ne se remplit qu'après.

**Ce que ce brainstorm ne fait pas** : il ne promet pas vingt messages sans le geste de King, il ne
rouvre pas les verticales mesurées à 0/15 de réponses (cliniques, labos, écoles) pour grossir un chiffre,
et il n'écrit pas un seul « vous n'avez pas de site » — la leçon d'ISEE du 26/10 tient toujours.
