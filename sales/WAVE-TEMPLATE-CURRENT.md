# Template de vague en vigueur — version du lundi 12/10/2026 (CONTRÔLE de l'A/B)

> Fichier créé le 13/10/2026 pour que le test A/B ait un contrôle documenté. Règle : **chaque version de template de vague a son fichier**, plus seulement l'historique de chat.
> Statut : **version réellement envoyée le 12/10** (reconstruite). Ce fichier n'est pas une règle ; il documente ce qui est parti.

## 1 · Texte (contrôle, bras A)

```
Bonjour M./Mme [Nom] — [cabinet], [quartier].
Je m'appelle King, je fais des sites pour opticiens.
Je peux vous préparer un aperçu de votre présence en ligne, avec un bouton WhatsApp en un clic.
Vous voulez le voir ?
```

## 2 · Preuve de l'envoi (sources)

| Envoi | Date / heure | Source | Niveau de preuve |
|---|---|---|---|
| Planète Optique, M. Jean Dury | 12/10/2026 11:34 | Capture WhatsApp fournie par King (13/10) | **Vérifié** (capture) |
| JiredOptic Med, Mme Pierrette (LIPOTH) | 12/10/2026 11:37 | Capture WhatsApp fournie par King (13/10, 14:33) | **Vérifié** (capture) |

Texte tel qu'il apparaît sur la capture (même schéma que le contrôle, nom et cabinet remplis) :

> Bonjour M. Jean Dury — Planète Optique. Je m'appelle King, je fais des sites pour opticiens. Je peux vous préparer un aperçu de votre présence en ligne, avec un bouton WhatsApp en un clic. Vous voulez le voir ?

## 3 · Points non vérifiés

- **JiredOptic Med (Douala) :** **vérifié par capture (13/10).** Envoi le 12/10 à 11:37 ; réponse du client « non » à 11:47, puis « bonjour monsieur » à 11:47 ; accusé de réception de King à 11:53 (« C'est noté, je ne vous dérange pas davantage… »). **Écart avec le texte de contrôle :** la salutation utilise le prénom (« Mme Pierrette ») et non « M./Mme [Nom] ». CRM (`crm.py`, ligne JiredOptic) : **corrigé le 13/10** — `contacted=Yes`, `reply=Yes`, `stage=parked`, `last_send_state=delivered`, journal 12/10 11:37 ajouté (commit 71851af).
- **Réponse négative enregistrée :** le client a dit « non ». Aucune relance. Le message de clôture de King est un **message de traitement de réponse**, pas un élément du test A/B.
- **Autres envois du 12/10 :** non recensés. La liste complète des destinataires du lundi n'est pas dans le dépôt. Les deux envois vérifiés sont Planète Optique et JiredOptic Med.

## 4 · Ce que ce fichier n'est pas

- Ce n'est pas le template v2 (voir `sales/CLIENT-MESSAGING-RULES.md` §12).
- Ce n'est pas une règle en vigueur. Le texte ci-dessus documente l'envoi, il ne le recommande pas.

## 5 · Amélioration (règle)

Chaque version de template de vague est versionnée dans un fichier daté (`sales/WAVE-TEMPLATE-<version>-<date>.md`), avec : texte exact, date d'envoi, destinataires, source de preuve. Le template v2 aura le sien à sa première utilisation.
