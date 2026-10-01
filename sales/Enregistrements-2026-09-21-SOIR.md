# SOIR 21/09 — enregistrements d'envois, 3 de MES erreurs corrigées, et le texte Bonanjo réécrit

Heure de rédaction : ~18:20 (les écrans de King portent 17:39 → 17:51). Je ne suis pas le canal : ici je
**enregistre** ce qui est parti, je **corrige** ce que le CRM racontait faux, et je **réécris** un message
que j'avais mal tourné. Tout est appliqué dans `leads/build/crm.py` + `views.py` puis régénéré.

---

## ① ⚡ LA DÉCOUVERTE LA PLUS UTILE DE LA SOIRÉE — `« je vous reviens » n'est pas un accord`

**Ta correction :** *« Centre Médical de Bonanjo didn't really confirm they wanted to work with us — the
message makes it seem like they had already seen the demo and agreed. »*

Tu as raison, et le fil le prouve tout seul :
- ven 18/09 **19:37** — message 1, une coche.
- sam 19/09 **08:44** — « **Bjr merci je vous reviens** ». C'est un **report poli**. Pas un « oui », pas un
  feu vert, pas une demande de lien.
- sam 19/09 **13:35** — la page entière + **le prix** (100 000 · 50 000/50 000), envoyés sur la foi de ce
  « je vous reviens » lu comme un accord. Deux coches, plus rien depuis.

Mon brouillon de 17:00 continuait dans la même faute : « je ne vous relance pas pour le prix — **j'attends
votre feu vert** » + « je les écris noir sur blanc sur la page ». Ces deux phrases supposent qu'il a accepté.
**Elles sont jetées.** Un prospect à qui on prête un accord qu'il n'a pas donné perd le goût de répondre :
c'est la mécanique exacte qui explique qu'un fil à 2 coches depuis 29 heures ne dise rien.

### Le texte à envoyer (remplace mon brouillon de 17:00)

```
Bonjour Docteur. Rien à valider, rien à décider : juste votre avis.
Vous avez pu ouvrir la page ? Qu'est-ce qui vous paraît juste, et qu'est-ce qui ne vous ressemble pas ?
Si c'est « pas maintenant », dites-le-moi en deux mots, je ne vous réécrirai pas.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi celui-là :** quatre lignes, **zéro** mot qui suppose un accord (pas « votre feu vert », pas
« comme convenu », pas « je corrige »), une seule chose demandée — **un avis** — et une porte de sortie qui
coûte deux mots à dire. Le prix n'est pas rappelé : il est déjà chez lui depuis le 19/09, le répéter
transformerait une question d'avis en relance commerciale.

**Après :** s'il décrit un défaut (horaire, service, adresse), la correction part dans l'heure et **c'est
là** que le créneau se propose. S'il ne répond pas : `presented` reste, **FU2 (M+4) mar 22/09**, puis parked
le 26/09 — on ne transforme pas un « je vous reviens » en cinq messages.

---

## ② LES ENVOIS DU SOIR, TELS QUE VUS SUR TES ÉCRANS

| # | Lead | Fait enregistré | Ce que ça change au CRM |
|---|---|---|---|
| 1 | **AFRIQUE LABO** (690 54 70 93) · 17:39, **édité**, une coche | FU2 envoyée (angle : les résultats) | `follow_ups_sent` **1 → 2** · `last_send_state=delivered` · FU3 **mer 23/09** au plus tard · `qualified` (pas `presented` : voir ③) |
| 2 | **OraCare** (672 52 66 86) · 17:43, une coche | le message de **clôture** est parti : « last note from me, then I stop » | **`parked` le 21/09**, `follow_ups_sent=3`, plus AUCUNE relance. Sorti de `RELANCE_A_JOUR` : une date de relance sur un fil fermé est une invitation à se griller |
| 3 | **Baird** (677 87 53 95) · 17:30 (et **FU1 jeu 17/09 13:48**) | 3 messages sur le fil, 0 réponse | `follow_ups_sent` **1 → 2** · FU3 **mer 23/09 = la dernière** · en file : « PROGRAMMÉE — ne rien faire avant » |
| 4 | **Le Cristallin** 17:51 · **Univers Optique** 17:50 · **Disc Optique Médicale** 17:48 · **Tchaya Optique** 17:47 | message 1 parti, **une coche** (livré non lu) sur les quatre | les 4 lignes : `prospect → qualified` · `first_touched=2026-09-21` · `Contacted=Yes` · `variante_envoi` (A/C) gravé · `profile_name_seen` = le titulaire public |
| 5 | **Bely Optique Médicale** 696 85 52 42 | **pas sur WhatsApp** | `wa_verified=no` · `Contacted=No` · `disqualification_reason=Canal injoignable` · la ligne **reste sans envoi** : un numéro qui ne reçoit rien n'est pas une relance ratée |
| 6 | **Médina Optic** 699 93 93 34 | absent des envois du soir | **rien de décidé** : `prospect`, 0 envoi, aucune date. **Question ouverte (⑤)** |

**Compteur après la soirée :** 145 lignes · **49 contactées** · 3 réponses humaines · **PRR 6,1 %** ·
`closing 2 · presented 1 · qualified 42 · prospect 1 · parked 8 · lost 10` · **0 client · 0 FCFA · 9 jours.**
La vague 1 est ouverte : 4 opticiens sur le fil, 1 numéro hors service, 33 encore à écrire.

---

## ③ TROIS ERREURS À MOI, TROIS CORRECTIONS DANS LA DONNÉE

**1 · J'avais « découvert » un doublon qui n'existait pas.** À 17:30 j'ai écrit qu'AFRIQUE LABO **n'était pas
dans le CRM** et j'ai ajouté une ligne. **FAUX** : la ligne existait déjà, sous `afrique-labo-douala` (et
c'est même elle qui portait la note « FU1 envoyée le 19/09, FU2 = lun 21 »). Cause exacte : j'ai cherché le
mot « AFRIQUE LABO » dans `crm.py` au lieu de chercher le **numéro** dans le CSV généré, et la ligne
s'appelait « Afrique Labo SARL ». Résultat : 146 lignes, le même numéro deux fois, deux cadencements qui
tournent à double sur la même docteure. **La ligne dupliquée est supprimée** et un **garde-fou permanent**
est entré dans `crm.py` : deux lignes portant le même numéro = **le build échoue**. (Il a hurlé dès la
première seconde d'après : `674 93 66 04` était déjà sur deux lignes — CEMECES et INSES. Voir 3.)

**2 · Un lead parqué ressortait « à relancer ».** `views.py` demandait d'abord sa table de dates, avant
l'étape du lead : OraCare, parqué à 18:20, est apparu en « **Relance 4/3** » dans la file du jour. Corrigé :
un `parked`/`lost` n'est **jamais** dû, quel que soit le calendrier. Et la règle du palier tient
désormais dans le code, pas dans ma bonne intention.

**3 · Le classeur disait plus de choses que je ne le lisais.** La cellule `Contacted` de la ligne 31 du
classeur portait, en toutes lettres : *« YES 15 Sep 14:41 WA (mockup image + msg 1; one tick) »*. Comme la
valeur n'était pas exactement « Yes », le traitement la lisait comme **non contactée** et l'écrivait telle
quelle dans une colonne booléenne. Corrigé : `Contacted` est normalisé, **et la preuve d'envoi descend dans
`Notes`** au lieu d'être écrasée. Leçon écrite : *une colonne qui ne ressemble pas à son type n'est pas du
bruit, c'est souvent le seul endroit où un fait a été noté.*

---

## ④ CEMECES : le numéro retiré, pas bricolé

Le garde-fou a trouvé `674 93 66 04` sur **deux** lignes : INSES (l'école) et CEMECES (la clinique). C'est
l'erreur de ma fiche du 18/09 — j'avais attribué le mobile de l'école à la clinique ; ta capture l'avait déjà
dit le jour même. La correction choisie n'est **pas** une exception dans le garde-fou : **le numéro est
retiré de la ligne CEMECES**, `wa_verified=no`, `Contacted=No`, et la raison est écrite dans la donnée.
Une ligne sans numéro est une tâche ; une ligne avec le numéro du voisin est un message au mauvais
destinataire. La clinique reste **à prendre par sa page Facebook** (la page, pas l'affiche), quand tu veux
ouvrir ce dossier.

---

## ⑤ CE QUE JE TE DEMANDE — trois mots chacun

1. **Médina Optic** : numéro hors WhatsApp, ou ton choix de ne pas l'écrire ? (ça décide `parked` avec
   gâchette, ou 5ᵉ envoi du lot 2.)
2. **Bonanjo** : le texte §① est prêt. Tu l'envoies ce soir (≤ 21:00, il n'est pas froid : il a un fil
   ouvert), ou demain 09:00 ?
3. **AFRIQUE LABO** : le message de 17:39 contenait une phrase de TROP, écrite par moi — « cette étape [les
   résultats] est écrite noir sur blanc » alors que le concept dit « **retrait sur place**, envoi sur demande
   au guichet ». Si la docteure répond, **on rétablit la vérité dans la minute** ; je ne corrige rien par un
   nouveau message aujourd'hui (le palier des 3 est atteint). Dis-moi si tu préfères que la correction parte
   avec la FU3 de mercredi.

**Et une chose que je ne ferai pas sans toi :** quatre messages en 4 minutes (17:47 → 17:51) au lieu des
~10 min prescrites, à des confrères du même ordre. Pour l'instant aucun retour négatif. Noté dans `crm.py`.
Si le lot 2 part ce soir, je les espace — la réputation dans une petite profession vaut plus que quatre
envois gagnés en cinq minutes.

---

## ⑥ L'ÉTAT DES FILS À 18:25 — ce qui n'a PAS bougé aujourd'hui, écrit sans l'habiller

| Lead | Dernier fait enregistré | Ce que ça veut dire |
|---|---|---|
| **L'Opticien Bali** (670 27 60 65) | msg 1 jeu 17/09 · **aucune relance envoyée** (le fichier du 16:00 en promettait une dim 20/09) | 3/3 aux trois portes, **4 jours sans rien**. Le seul prospect optique déjà validé. Texte prêt : `Send-Pack-2026-09-21-1600.md` §7. |
| **MITOC** (678 90 89 62) | FU1 jeu 17/09 · **FU2 du 21/09 non envoyée** (la page live `mitoc-concept.vercel.app` tourne toujours en démo vers TOI) | Le bouton WhatsApp d'un prospect affiche le numéro d'AMK depuis 5 jours : c'est le seul message qui **mérite** d'être envoyé en premier demain matin. |
| **Labiomed** (699 98 54 66) | « je vous reviens » 19/09 21:16 · 🙏 21:27 · lu 21:40 · **FU1 (M+2) non envoyée** | Le premier oui de la campagne, et le CRM ne dit plus « Relance 2/3 » mais « M+2 — il a dit qu'il reviendrait quand il serait disponible ». Fenêtre : **20:00 ce soir**, sinon demain 09:00. |
| **UNI-LABO** | RDV fixé par eux **ven 25/09**, heure manquante | Neuf jours de marge, mais **rien n'est confirmé** : une ligne de confirmation + leurs horaires réels (notre page les affiche, écrits par nous). |
| **Skye · YAKS** | parqués 18:20, deux fils ✓✓ non lus / transférés | Aucune relance. Réveil = leur lecture, pas notre calendrier. |

**Une phrase à ne plus écrire, venue de moi et partie par ta main :** « last note from me, then I stop »
(OraCare 17:43) et « je ne vous écrirai plus » (brouillon Bali) sont des **promesses de silence**. Si demain
un prospect ouvre le lien et que nous réécrivons, nous aurons menti sur la seule chose qu'un opticien ou un
dentiste peut vérifier : notre parole. **Formulation à retenir pour la reprise** : « je ne vous relancerai
plus sur ce dossier — si un jour vous voulez la page, ce fil suffit ». Le palier des 3 messages reste, la
promesse absolue sort des textes.
