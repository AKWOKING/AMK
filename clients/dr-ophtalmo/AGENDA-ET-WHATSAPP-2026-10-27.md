# Réserver, puis prévenir le médecin — ce que Google fait, ce qu'il ne fait pas

```text
ÉTAPE 0   graphe rejoué 27/10 (13 643 nœuds) · ask « google calendar booking link rendez-vous »
PRE-FLIGHT §00, §0, §0b, §0c, §0c bis, §0e, §0f · knowledge 4 (LANDING-FUNNEL §2/§6)
DEMANDE   King, 27/10 : « une fois qu'un patient réserve, est-ce que c'est enregistré dans Google
          Calendar avec un rappel, et est-ce que le médecin reçoit une notification WhatsApp comme si
          la personne lui avait écrit directement ? »
SOURCES   documentation Google (support.google.com/calendar/answer/10729749), comparatifs relevés le
          27/10 (cal.id, meetergo, lilachbullock, twizzlo, beside, apptoto) ; documentation Meta
          (developers.facebook.com/…/business-phone-numbers), coexistence (whautomate, 2026), tarifs
          WhatsApp (sendseven, chatmitra, myoperator — relevés le 27/10).
```

## 1 · La réponse courte

| Ce que tu demandes | Possible ? | Par quel moyen | Coût |
|---|---|---|---|
| Le rendez-vous **s'inscrit dans Google Agenda** | ✅ oui, nativement | page « Créneaux de rendez-vous » de Google | 0 |
| Le patient reçoit une **confirmation** | ✅ oui, nativement | Google envoie l'e-mail de confirmation | 0 |
| Le patient reçoit un **rappel avant** | ⚠️ **non** sur un compte personnel gratuit | rappel automatique = option payante (Google One Premium / Workspace Business Standard) | ~payant |
| Le **médecin** est prévenu à l'instant sur son téléphone | ✅ oui, par l'**appli Google Agenda** (notification de l'événement) | aucune configuration : c'est le comportement normal d'un agenda | 0 |
| Le médecin reçoit un **WhatsApp automatique** qui ressemble à un message du patient | ⚠️ pas tel quel — trois chemins, aucun gratuit ni invisible | voir §3 | de 0 à payant |

**En une phrase.** Google fait très bien la moitié « agenda » ; il ne fait **ni SMS ni WhatsApp** — sa
documentation ne propose que l'e-mail. Et aucune des routes WhatsApp automatiques ne peut se brancher
sur le numéro que le Dr Fogue utilise déjà pour parler à ses patients, sans une migration ou une
coexistence qui change sa façon de travailler.

## 2 · Ce que Google fait, exactement

- La page de réservation écrit l'événement **dans l'agenda du médecin** dès la réservation. C'est le
  comportement de base, gratuit, sur un compte personnel.
- **Confirmation** : le patient reçoit un e-mail de confirmation, et peut recevoir des **rappels
  e-mail** — jusqu'à cinq par rendez-vous, avec un texte que Google ne laisse pas modifier.
- **Les rappels automatiques sont une option payante** : absents sur un compte Google personnel gratuit,
  présents sur Google One Premium ou Workspace Business Standard et au-dessus. Sur l'offre gratuite, la
  parade documentée est de mettre les détails utiles **dans la description** de l'événement, qui
  apparaît dans l'e-mail de confirmation.
- **Aucun rappel par SMS ni par WhatsApp.** Ce n'est pas une option à activer : ça n'existe pas chez
  Google. Il faut un outil tiers.
- **Côté médecin**, l'application Google Agenda sur son téléphone notifie l'événement comme n'importe
  quel rendez-vous. C'est gratuit, immédiat, et cela **ne demande aucune ligne de code** de notre côté.

## 3 · Le WhatsApp : trois chemins, et ce qu'ils coûtent vraiment

### A · Le bouton d'après réservation — **livré ce tour, 0 FCFA**

Après le clic « Choisir un créneau », la page propose « Prévenir le Dr Fogue sur WhatsApp » : un lien
`wa.me` **prérempli** avec le lieu et l'heure. Le message part du **numéro du patient** ; le médecin le
reçoit donc dans sa conversation, exactement comme si la personne lui avait écrit — parce que c'est le
cas.

- **Force** : gratuit, zéro dépendance, aucune donnée de patient ne transite par un tiers, et cela
  respecte la promesse du site (aucun appel externe chargé par la page).
- **Limite, dite franchement** : c'est **facultatif**. Si le patient ne clique pas, le médecin n'a que
  la notification de son agenda. Un automatisme, ça ne s'oublie pas ; un bouton, si.

### B · Un outil d'automatisation (Zapier, Make) branché sur l'agenda

Un déclencheur « nouvel événement » envoie un WhatsApp. Mais WhatsApp ne s'envoie pas sans passer par
l'API officielle de Meta — donc les mêmes prérequis que la route C, **plus** un intermédiaire
américain qui voit le nom du patient et son heure de rendez-vous. Pour une clinique, c'est une question
de traitement de données de santé, pas seulement d'abonnement.

### C · L'API WhatsApp de Meta, en direct

- **Le numéro ne peut pas être sur les deux plateformes.** Un numéro actif sur l'application WhatsApp
  (ou WhatsApp Business) ne peut pas être enregistré sur l'API sans en être retiré. Le 691 280 237 est
  le numéro avec lequel le Dr Fogue parle à ses patients depuis son téléphone : le basculer sur l'API le
  lui retire de son appli, sauf à passer par la **coexistence** — qui exige l'application WhatsApp
  Business (≥ 2.24.17) et un numéro déjà utilisé dessus depuis au moins sept jours.
- **Depuis le 1ᵉʳ octobre 2026, les messages de service sont facturés** au-delà de 1 000 par numéro et
  par mois (ils étaient gratuits auparavant). Les modèles « utilitaire » sont facturés à l'unité, selon
  le pays du destinataire.
- **Ce qu'il faut en plus** : un compte Meta Business, un compte WhatsApp Business (WABA), un numéro
  dédié, un webhook et une fonction serverless pour déclencher l'envoi à chaque réservation.
- **Ce que je n'ai pas chiffré** : le tarif exact par message pour le Cameroun. Il est dans la grille
  tarifaire de Meta, par pays ; je ne l'ai pas lue dans cette session, et je ne l'invente pas.

## 4 · Ce que je recommande, dans l'ordre

1. **Aujourd'hui** : le bouton d'après réservation (§3 A), tel qu'il est construit. Zéro coût, zéro
   dépendance, et il produit exactement l'effet demandé — un message du patient dans la conversation du
   médecin — chaque fois que le patient l'utilise.
2. **Quand le médecin aura ses horaires** : une page de réservation **par lieu** (Africa Médical en
   premier, le vendredi), avec les détails utiles dans la description de l'événement. Le médecin reçoit
   la notification sur son téléphone ; le patient reçoit la confirmation Google.
3. **Le rappel automatique au patient** : si le taux d'absence devient un problème mesuré, un abonnement
   Google One Premium ou Workspace suffit — sans une ligne de code. À décider sur des chiffres, pas par
   principe.
4. **L'automatisation WhatsApp complète** : seulement si le médecin accepte de faire migrer son numéro
   ou d'activer la coexistence, **et** si quelqu'un maintient le webhook. Ce n'est pas une décision de
   design, c'est une décision d'exploitation — elle doit être chiffrée et assumée avant d'être promise.

## 5 · Ce que le site ne dira jamais

- « Vous recevrez un rappel par WhatsApp » — Google n'en envoie pas, et notre bouton est facultatif.
- « Vous recevrez un rappel » tout court, tant que l'offre gratuite ne le permet pas.
- « Votre rendez-vous est confirmé » — il est **réservé chez Google** ; le site le dit ainsi, et le
  formulaire de demande garde sa phrase (« une demande n'est pas un rendez-vous confirmé »).

Un test le vérifie : aucune phrase des dictionnaires ne promet un rappel WhatsApp ou SMS.
