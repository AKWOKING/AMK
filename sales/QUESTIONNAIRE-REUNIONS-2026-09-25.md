# QUESTIONNAIRE DES RENDEZ-VOUS DU 25/09 — personnalisation, autres services, relation longue

**24/09/2026 · lot [32]** · demande de King : *« on doit préparer un questionnaire pour nos réunions de
vendredi — 1. pour la personnalisation du site, 2. d'autres services qu'ils aimeraient qu'AMK provide (une
automatisation, logiciel, contenu animé), 3. toute autre information pertinente pour une collaboration
réussie et longue, ce projet et les suivants »*.

**Ce document sert à deux choses** : §1 à §4 sont pour nous (le guide et les questions), **l'Annexe A est la
feuille qu'on laisse au client**. Les six points factuels d'Univers Optique vivent déjà dans
`sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md` §2 — on ne les redouble pas ici, on les complète.

---

## 0 · Les quatre règles qui rendent un questionnaire utile

1. **Une question ne se pose que si sa réponse change un fichier.** La page, le contrat, le CRM, la ligne
   d'abonnement, la fiche Google — ou rien. Une question dont la réponse ne change rien coûte du temps et
   de la bonne volonté, et elle donne l'impression qu'on remplit un formulaire au lieu de construire un
   site. Chaque question ci-dessous porte donc sa destination (`→`).
2. **Huit minutes en séance, pas trente.** Les deux rendez-vous ont un ordre du jour serré (Univers : les
   six points, la signature, les 50 000 ; UNI-LABO : la démonstration, les corrections, le contrat, les
   75 000, l'abonnement). Le bloc long part sur **la feuille de l'Annexe A**, que le client remplit quand il
   veut et renvoie par WhatsApp.
3. **On interroge les problèmes, jamais les outils.** *« Voulez-vous de l'intelligence artificielle ? »*
   conduit à un « oui » qu'on ne peut pas honorer — et notre grille s'est déjà fait prendre une fois avec
   « propulsées par l'IA ». On demande où le temps se perd, ce qui se perd, et ce que les clients
   demandent : les outils, c'est notre travail, pas le sien.
4. **Si la question appelle un prix, la réponse s'écrit après.** *« Je vous l'écris et je vous l'envoie »*
   — jamais un chiffre improvisé en séance (règle du 24/09, `sales/PRIX-ET-RECURRENCE-2026-09-24.md` §6).

---

## 1 · Personnalisation du site — le bloc de séance (5 minutes)

À poser **dans cet ordre**, et à noter mot à mot : ce sont les réponses qui rendent la page *à eux* au lieu
d'une page bien faite.

| # | La question, telle qu'on la pose | Ce que la réponse change |
|---|---|---|
| **A1** | *« Avez-vous déjà des photos du laboratoire / du magasin — et si oui, est-ce que je peux les voir ? »* Puis, seulement s'il n'y en a pas : *« je peux prendre cinq photos de votre paillasse avant de partir, aucun patient, aucun nom, aucun écran. »* | `img/` : vraies photos au lieu des « mise en situation » → `research/PHOTO-LABO-PIXEL-8A-2026-09-24.md` ; vérification par `tools/qa/audit_images.py` |
| **A2** | *(UNI-LABO)* *« Avez-vous une autorisation du ministère de la Santé, et êtes-vous inscrits à un contrôle de qualité externe ? »* | une **bande de crédibilité en haut de page**, ou rien — la plupart des laboratoires du quartier ne l'affichent pas |
| **A3** | *(Univers)* *« La réduction de 15 % que vous aviez en 2023 — elle existe encore ? »* | la page et la fiche Google : **rien ne part sans son accord écrit** |
| **A4** | *« Si un client ne retient qu'une phrase de votre page, ce serait laquelle ? »* | le titre, l'accroche, la première ligne — écrit **dans ses mots**, pas dans les nôtres |
| **A5** | *« Quelles sont les trois questions qu'on vous pose le plus au comptoir ou au téléphone ? »* | la FAQ : les **vraies** questions, avec ses vraies réponses (elles existent déjà chez UNI-LABO : à jeun, urines, hormones…) |
| **A6** | *« Y a-t-il quelque chose que vous ne voulez **pas** voir publié — un ancien nom, une adresse, un prix ? »* | les exclusions écrites de la page (et une ligne dans le contrat, § « Description du projet ») |
| **A7** | *« On écrit « vous » ou « nous » ? Et l'anglais, à côté du français ou pas du tout ? »* | le ton et la bascule FR\|EN |
| **A8** | *« Quand un patient hésite, qu'est-ce qui le rassure — la propreté, le résultat rapide, le prix, le personnel ? »* | l'ordre des arguments dans la page (la demande précède la réponse) |

**Rappel** : les six points factuels d'Univers (préfixe du fixe, ordre des trois lignes, nom du titulaire,
adresse e-mail, fiche Google) se posent **avant** ce bloc — ils sont déjà sur sa page, une réponse par
ligne. Ce bloc-ci vient après, quand les faits sont propres.

---

## 2 · Les autres services — le bloc de séance (3 minutes, tourné vers les problèmes)

On ne propose **rien** à ce moment-là. On écoute, on note, et on range chaque réponse dans une offre qui
existe déjà ou dans « recherche à faire » (l'ordre des offres : C → D/E → B → A1 → A2 → F, `ORDRE-DES-OFFRES`).

| # | La question | Ce qu'on écoute, et où ça va |
|---|---|---|
| **B1** | *« Dans une journée normale, qu'est-ce qui vous prend le plus de temps — et qu'est-ce que vous aimeriez ne plus faire vous-même ? »* | un problème de **temps** → entretien/abonnement (C), ou un morceau de travail précis |
| **B2** | *« Qu'est-ce qui se perd, chez vous ? Un résultat qu'on ne retrouve pas, une commande qu'on attend, un client qui ne revient pas, une facture qu'on oublie ? »* *(labo : résultats, échantillons, comptes des entreprises ; optique : commandes de verres, montages, échéances)* | un problème **perdu/tracé** → pilote labo (B, 400 000 + 35 000/mois), ou hors-standard (A2), ou devis/facture (D/E) |
| **B3** | *« Vos clients vous demandent-ils des choses qu'aujourd'hui vous ne pouvez pas leur donner — un rendez-vous en ligne, une facture propre, un suivi par WhatsApp ? »* | les **services futurs** : on note le besoin, on ne promet ni prix ni délai ; l'assistant automatique et le contenu vidéo sont des lignes **à part**, sur devis, et jamais « compris » |

**Ce qu'on ne fait pas dans ce bloc** : dire « oui » à l'automatisation, citer un prix, ou promettre de
l'IA. Et **« contenu animé »** (vidéo, animation) : ce n'est pas dans nos offres aujourd'hui — si le
besoin sort de leur bouche, il se note comme un **sujet de recherche**, pas comme une ligne vendable. Ce
qu'on sait faire aujourd'hui : la page, les textes, les photos, la fiche Google, l'entretien mensuel.

---

## 3 · Pour que ça marche longtemps — la relation, pas le logiciel

| # | La question | Ce que ça change |
|---|---|---|
| **C1** | *« Pour les textes et les corrections, qui décide, vous ou quelqu'un d'autre ? »* (associé, conjoint, direction — le « zombie check » du playbook) | qui on appelle, qui signe ; évite un « laisse-moi en parler à… » à la livraison |
| **C2** | *« La fiche Google — qui a le mot de passe du compte ? »* | `sales/FICHE-GOOGLE-PROFILE.md` : sans la main sur la fiche, la marche à suivre prend 3 jours de demande d'accès |
| **C3** | *« Votre nom de domaine, et votre hébergement — qui paie, à quel nom, et il expire quand ? »* (Univers : LWS ; Le Cristallin : 13/06/2027) — ⚠️ **à UNI-LABO, cette question passe AVANT l'abonnement : c'est elle qui choisit le palier** (ni l'un ni l'autre → Standard 30 000 ; les deux → Essentiel 12 000 — décision de King, 24/09) | la clause domaine/DNS, la ligne d'abonnement, et **le prix annoncé demain** |
| **C4** | *« Pour une correction, je vous écris sur ce numéro — et sous quel délai une correction vous suffit-elle ? »* | le canal et le délai réels de l'abonnement (nous promettons 24 h ouvrées) |
| **C5** | *« Qu'est-ce qui vous ferait arrêter ? Qu'est-ce qui serait inacceptable pour vous ? »* | notre **signal d'échec** : c'est la seule question qui nous dit où nous allons décevoir — et elle se pose sans défense |
| **C6** | *« Comment vos patients vous trouvent-ils aujourd'hui — bouche-à-oreille, Facebook, Google, quelqu'un qui passe devant ? »* | ce que la page et la fiche doivent remplacer ; et la question d'attribution du 24/09 (« comment nous avez-vous connus ? ») appliquée à **leur** clientèle |
| **C7** | *« Si quelqu'un vous demandait un site comme celui-ci, vous nous enverriez à qui ? »* | le parrainage : **un mois d'abonnement offert au parrain**, prix normal pour le filleul — on demande, on ne quémande pas |
| **C8** | *« Après la livraison, est-ce que je peux montrer votre site comme exemple — ou vous préférez attendre ? »* | le droit de portfolio (il est déjà au contrat), et un témoignage **libre, jamais acheté** |

---

## 4 · Ce qu'on ne demande pas — et pourquoi

| On ne demande pas | Parce que |
|---|---|
| « Voulez-vous de l'IA / un assistant automatique ? » | ça produit un « oui » qu'on ne peut pas honorer ; l'assistant est un service **futur**, écrit à part |
| « Ça vaut combien pour vous ? » / leur chiffre d'affaires | on ne vend pas un pourcentage de leur poche ; le prix se pose, il ne se négocie pas contre une remise |
| Un prix pour un service qui n'a pas de grille | la réponse se rédige après : *« je vous l'écris »* |
| Un témoignage contre quelque chose | un témoignage ne s'achète pas (le piège du contrat « Fondateur » : « en échange d'un tarif préférentiel ») |
| Des documents personnels, des registres, des dossiers patients | jamais dans un cadre photo, jamais dans un dossier — et on ne les demande pas |
| « Est-ce que vous voulez une vidéo ? » | même piège que l'IA : on demande le **besoin**, pas le format |
| Une promesse de classement Google | on ne promet jamais de position ni de citation (`sales/FICHE-GOOGLE-PROFILE.md`, `research/AEO-2026-09-24.md`) |

---

## 5 · Où va chaque réponse (le soir même, jamais « plus tard »)

| Réponse | Fichier | Qui l'écrit |
|---|---|---|
| Faits (téléphones, noms, horaires, adresses, e-mails) | la page + `leads/records/<client>.md` + `leads/CRM.csv` | nous, **le soir même** (règle M7 : la prose ne suffit pas, ce qui change un calcul va dans le générateur) |
| Ce qu'on peut publier / ne pas publier | contrat, § « Description du projet » (le champ le plus important, vide aujourd'hui) | nous, à faire signer |
| Photos | `img/` après vérification (`audit_images.py`) | nous |
| Fiche Google (qui a la main, autorisation) | `sales/FICHE-GOOGLE-PROFILE.md` + la fiche cliente | nous |
| Autres services entendus | `ORDRE-DES-OFFRES` (rang) ou une ligne « recherche à faire » | nous, sans réponse au client avant écrit |
| Abonnement choisi, domaine, délai de réponse | `sales/PRIX-ET-RECURRENCE-2026-09-24.md` (feuille unique) + le contrat | King tranche, nous écrivons |

---

## Annexe A — **la feuille à laisser au client** (à imprimer ou à envoyer sur WhatsApp)

> **AMK — quelques questions pour que votre site vous ressemble vraiment**
> *(Pas besoin de tout remplir d'un coup. Écrivez, photographiez la feuille, renvoyez-la sur WhatsApp —
> ou répondez de vive voix, c'est pareil.)*
>
> **Votre activité, telle que vous la racontez**
> 1. Si un client ne retenait qu'**une phrase** de votre site, ce serait laquelle ?
> 2. Quelles sont les **trois questions** qu'on vous pose le plus souvent au comptoir ou au téléphone ?
> 3. Qu'est-ce qui rassure un client qui hésite — la rapidité, la propreté, le prix, le personnel, autre chose ?
> 4. Y a-t-il quelque chose que vous **ne voulez pas** voir publié (un ancien nom, une adresse, un prix) ?
>
> **Vos clients**
> 5. Comment vous trouvent-ils aujourd'hui — bouche-à-oreille, Facebook, Google, la rue ?
> 6. Vos clients vous demandent-ils des choses que vous ne pouvez pas encore leur donner (rendez-vous en
>    ligne, facture, suivi par WhatsApp, autre) ?
>
> **Votre organisation**
> 7. Qui décide pour les textes et les corrections — vous, ou une autre personne avec vous ?
> 8. Qu'est-ce qui vous prend le plus de temps dans une journée, et que vous aimeriez ne plus faire
>    vous-même ?
> 9. Votre nom de domaine et votre hébergement : à quel nom, payés jusqu'à quand ?
> 10. La fiche Google de l'entreprise : est-ce vous qui avez le mot de passe du compte ?
>
> **Et pour la suite**
> 11. Qu'est-ce qui vous ferait arrêter de travailler avec nous — qu'est-ce qui serait inacceptable ?
> 12. Si quelqu'un vous demandait un site comme le vôtre, à qui nous enverriez-vous ?
>
> *(Une ligne par question suffit. Ce qui n'a pas de réponse aujourd'hui n'empêche rien : on le garde pour
> la prochaine fois.)*

---

## Annexe B — la feuille à garder (nous, pour la séance)

**Univers Optique — 10 h.** ① les six points factuels (préfixe du fixe · les 15 % · l'ordre des trois
lignes · le nom du titulaire · l'e-mail · la fiche Google) → ② signature et 50 000 → ③ **bloc A** (A1, A3,
A4, A5) → ④ **bloc B** en trois questions → ⑤ **bloc C** (C1, C3, C6) → ⑥ la feuille A, à laisser.

**UNI-LABO — 13 h.** ① la démonstration et les corrections → ② **A2** (autorisation, contrôle qualité) →
③ le contrat et les 75 000 → **④ LA QUESTION du domaine et de l'hébergement, PUIS l'abonnement** (Standard 30 000 s'il n'a rien, Essentiel 12 000 s'il a les deux — décision de King, 24/09), avec la phrase du dépassement : *ce qui dépasse attend le mois suivant* → ⑤ **A1** (leurs photos, sinon les quinze minutes) → ⑥ **bloc B** → ⑦ la feuille
A, à laisser.

**Ce qu'on emporte** : cette feuille, les deux numéros MoMo écrits à la main, et la règle qui ne bouge pas —
**aucun prix improvisé, aucune promesse de classement, aucun témoignage acheté.**
