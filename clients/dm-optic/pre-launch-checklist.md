# Checklist de pré-lancement — DM OPTIQUE SARL

> **Dix items. Dix portes. Le lancement n'a lieu que lorsque les dix sont vertes.**
> **Le portique est l'item 1 : tant que l'acompte n'est pas encaissé, aucun des neuf autres n'est
> autorisé à bouger.** Ni site, ni page, ni fiche, ni contenu, ni compte créé.
>
> Écrit le **01/10/2026**. État : **0/10**.

---

## Item 1 · L'acompte est encaissé 🔴 **LE PORTIQUE**

| | |
|---|---|
| **Critère** | **75 000 FCFA** réellement **encaissés** sur le compte — pas annoncés, pas « en cours », pas promis |
| **Vérification** | Relevé bancaire. Une capture de conversation WhatsApp ne vaut pas encaissement |
| **Si non** | ⛔ **Tout s'arrête ici.** Les items 2 à 10 ne sont pas entamés |
| **État** | ☐ |

> **Pourquoi c'est le portique et pas une formalité.** L'accord est **verbal**. Rien d'écrit n'engage
> le paiement. Produire avant l'encaissement, c'est travailler à perte sur une promesse.

---

## Item 2 · Nous sommes un émetteur identifiable 🔴

| | |
|---|---|
| **Critère** | **RIB + NIU AMK** disponibles, au **nom exact** qui figurera sur la proforma |
| **Vérification** | La proforma émise porte notre raison sociale, notre NIU, notre RIB |
| **⚠️ État réel** | ⛔ **Le dépôt ne contient ni RIB ni NIU pour AMK.** C'est un bloquant **de notre côté**, pas du sien |
| **Pourquoi** | Une SARL sous contrôle fiscal ne peut pas classer une facture dont l'émetteur n'est pas identifiable. Sans cela, **la proforma ne déclenche aucun virement** |
| **État** | ☐ |

---

## Item 3 · Le NIU et l'adresse fiscale du client sont reçus 🔴

| | |
|---|---|
| **Critère** | **NIU** + **adresse fiscale** de DM OPTIQUE SARL, écrits |
| **Vérification** | Reportés sur la proforma, identiques à ses documents |
| **Où** | Promis par le client le 01/10 pour le 02/10 ; question 1.1–1.2 du questionnaire |
| **État** | ☐ |

---

## Item 4 · Les comptes sont au nom du client 🔴

| | |
|---|---|
| **Critère** | Facebook et TikTok **créés au nom du client**, e-mail et numéro de récupération **à lui**, nous en **administrateur** — pas propriétaire |
| **Vérification** | L'e-mail propriétaire est le sien ; notre accès est révocable par lui |
| **⚠️ Ordre** | **Avant toute création.** Un compte créé sur nos identifiants est très difficile à rétrocéder |
| **Décision** | Verrouillée par King — `dossier.md` §3.1 |
| **État** | ☐ |

---

## Item 5 · Les jours d'ouverture sont confirmés

| | |
|---|---|
| **Critère** | Les **jours**, écrits. Les heures sont déjà connues (8h00–17h30, consultation 8h30–13h30) |
| **Vérification** | Aucun jour n'est affiché sur le site ou dans le contenu sans avoir été donné |
| **Pourquoi** | Bloque la section Examen de vue, le pied de page, **et la semaine 2 du plan de contenu** |
| **État** | ☐ |

---

## Item 6 · L'adresse est complète et repérable

| | |
|---|---|
| **Critère** | Adresse validée **et** un **repère physique** (« en face de… », « à côté de… »), **et** l'étage |
| **Vérification** | Le repère a été relu par le client |
| **Pourquoi** | À Bonabéri, on arrive en taxi. Un repère convertit mieux qu'un plan |
| **État** | ☐ |

---

## Item 7 · Les photos réelles sont reçues **et archivées dans le dépôt** 🔴

| | |
|---|---|
| **Critère** | **3–4 photos du cabinet** · **6–8 photos de montures** par famille · 1–2 du geste (montage, ajustement) |
| **Vérification** | Les fichiers sont **dans le dépôt**, pas seulement en conversation |
| **⚠️ Antécédent** | Neuf photos avaient été envoyées puis **perdues** par le bac. **Cette fois, archivage immédiat** |
| **Pourquoi** | Bloque **les semaines 2, 3 et 4** du plan de contenu, et laisse trois illustrations sur le site |
| **État** | ☐ |

---

## Item 8 · Le périmètre des services est validé par le client

| | |
|---|---|
| **Critère** | Les six actes affichés sont **confirmés ou retirés un par un**, par écrit |
| **Vérification** | La page n'affiche aucun service que le cabinet ne rend pas |
| **Pourquoi** | La page liste aujourd'hui six services **types**, signalés comme tels. Un cabinet ne fait pas tout — ce qui est retiré disparaît |
| **État** | ☐ |

---

## Item 9 · La ligne de base est mesurée

| | |
|---|---|
| **Critère** | **Avant** tout lancement : patients par jour · appels ou messages entrants · provenance |
| **Vérification** | Les chiffres sont écrits **dans le dépôt**, datés |
| **Pourquoi** | Le client achète de la **traçabilité**. Un rapport de fin de mois sans point de départ est **invérifiable** — donc inutile à une SARL sous contrôle fiscal |
| **Coût** | Quatre questions pendant la visite |
| **État** | ☐ |

---

## Item 10 · Le site est publiable — et vérifié sur un téléphone 🔴

| | |
|---|---|
| **Critère** | Les **cinq** sous-points ci-dessous, tous verts |
| **État** | ☐ |

| Sous-point | Critère |
|---|---|
| **10.1** | Le **`noindex` est levé** — ⚠️ il est **voulu** sur la page de travail ; le lever est l'acte de publication, pas une formalité |
| **10.2** | L'**URL définitive est tranchée** : ⚠️ `dmoptic.vercel.app` et `dmoptic-2.vercel.app` sont toutes deux citées dans le dépôt. Une seule est réelle. Recoller avec `build_dmoptic.py --url`, puis redéployer **le dossier entier** (`index.html` + `og.jpg`) |
| **10.3** | Le **domaine est au nom du client** — jamais un domaine à nous. `dmoptique.cm` / `dmoptic.cm` sont **libres** |
| **10.4** | **Les contrôles passent** : `audit_a11y.py --strict` 0 faute · `audit_html.py` 0 constat · `audit_aeo.py` schéma complet · `node tools/qa/test_dmoptic_page.mjs` **38/38** |
| **10.5** | **Vérifié sur un téléphone, en plein jour** — FR par défaut, bascule EN qui change tout, un vrai WhatsApp pré-rempli qui s'ouvre, aucun débordement horizontal. **Portique : « Not verified on a phone = not sent. »** |

> **Note d'outillage.** `build-notes.md` dit « le bac n'a pas de navigateur » — **c'est dépassé** :
> Playwright est installé, les 14 fichiers de test passent. Les captures sont possibles. **Mais le
> portique du téléphone reste** : une capture dans un bac n'est pas une lecture en plein jour à Bonabéri.

---

## Récapitulatif

| # | Item | Bloquant ? | État |
|---|---|---|---|
| 1 | Acompte encaissé | 🔴 **portique** | ☐ |
| 2 | RIB + NIU AMK (émetteur identifiable) | 🔴 | ☐ |
| 3 | NIU + adresse fiscale du client | 🔴 | ☐ |
| 4 | Comptes au nom du client | 🔴 | ☐ |
| 5 | Jours d'ouverture | oui | ☐ |
| 6 | Adresse + repère | oui | ☐ |
| 7 | Photos réelles archivées | 🔴 | ☐ |
| 8 | Périmètre des services validé | oui | ☐ |
| 9 | Ligne de base mesurée | oui | ☐ |
| 10 | Site publiable + vérifié au téléphone | 🔴 | ☐ |

**0/10 vertes au 01/10/2026.**

**Les deux items qui dépendent de nous, pas du client : 2 et 10.** Les huit autres attendent le client
ou l'encaissement. **Le chemin critique passe donc par l'item 2** — sans nos identifiants de
facturation, la proforma ne part pas, l'acompte ne vient pas, et l'item 1 ne s'ouvre jamais.
