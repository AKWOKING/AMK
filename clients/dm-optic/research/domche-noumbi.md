# Recherche — M. Domche Noumbi & DM OPTIQUE

> **Objet : ce qui existe en ligne, avec un niveau de confiance par ligne.** Rien ici n'entre sur un
> support public sans être confirmé. Une page de santé qui invente une adresse ou un horaire coûte un
> patient, puis la confiance.
>
> Recherches d'origine : **24/09/2026** (contrôle approfondi, six recherches — voir
> `clients/dm-optic/inspiration.md` et `clients/dm-optic/build-notes.md` §2). Complété le **01/10/2026**
> à partir de la synthèse de King.
>
> ⚠️ **Ce fichier corrige la synthèse du 01/10 sur un point. Voir §2.**

---

## 1 · Échelle de confiance utilisée

| Niveau | Sens | Usage autorisé |
|---|---|---|
| **A — confirmé** | Document officiel, ou fait vu directement par King | Publiable |
| **B — attesté** | Source publique datée et attribuée, non contredite | Publiable **avec la source et la date** |
| **C — plausible** | Indice non recoupé | **Interdit** en public ; usage interne seulement, signalé |
| **D — écarté** | Contredit, ou sans lien établi | Ne jamais réutiliser |

---

## 2 · ⚠️ Correction : il existe **deux** traces publiques, pas une

La synthèse du 01/10 indique : *« aucune trace publique de M. Domche Noumbi ou DM OPTIQUE en ligne,
hormis une petite annonce afribobo de 2019 non confirmée. »*

**Le dépôt contredit cette synthèse.** Le contrôle du 24/09 a trouvé une **seconde trace, de niveau B**,
et elle est **déjà publiée sur l'aperçu du site** (section *Le titulaire*) :

> **« Son nom apparaît en mars 2023 dans la liste des opticiens de Douala citée par la presse »**
> — *Echos Santé*, article sur l'**Ordre national des opticiens du Cameroun**.
> Provenance consignée : `clients/dm-optic/build-notes.md` §2 (tableau de provenance) et
> `clients/dm-optic/inspiration.md` § « le contrôle approfondi », point 4.

**Pourquoi c'est important, et pas anecdotique :**

- C'est le **seul actif de crédibilité vérifiable** du cabinet, avec son inscription à l'Ordre.
- C'est précisément l'angle que la stratégie veut exploiter : **inscrit vs informel** (voir
  `market-analysis.md` §4). Une mention dans la presse professionnelle sur l'Ordre national **est** la
  preuve publique de cet angle.
- Elle est **publiable** (niveau B : publique, datée, attribuée) — à condition de citer *Echos Santé*
  et **mars 2023**.
- Si ce fichier disait « aucune trace », **la page construite se contredirait elle-même.**

**Décision proposée :** conserver la mention de mars 2023 comme preuve, avec sa source et sa date.
À faire confirmer par King, qui a mené la recherche — **le document papier ou l'URL de l'article n'est
pas archivé dans le dépôt**, et c'est une faiblesse : une preuve citée sans pièce jointe est une
preuve qu'on ne peut pas re-vérifier. → **Action : retrouver et archiver l'article** (ou sa capture)
avant le lancement.

---

## 3 · Inventaire des traces

| # | Trace | Détail | Confiance | Usage |
|---|---|---|---|---|
| 1 | **Registre ONOC** | Littoral, **ligne 102** · inscription **021/2016** · arrêté ministériel **0382** · titulaire **M. Domche Noumbi** · téléphone **656 122 239** · Douala | **A** | Publiable. C'est la carte d'identité du premier écran |
| 2 | **Mention presse, mars 2023** | *Echos Santé* — liste des opticiens de Douala, article sur l'Ordre national des opticiens du Cameroun | **B** | Publiable **avec source + date**. À archiver |
| 3 | **Profil WhatsApp** | Nom affiché **« DM OPTIC »**, numéro vérifié à l'écran par King | **A** | Utilisé comme nom d'usage |
| 4 | **Annonce afribobo, déc. 2019** | « **DM optometrie** » · **2 500 F** · publiée par un **particulier nommé Samuel** | **C** | ⛔ **Écartée.** Voir §4 |
| 5 | Domaines `dmoptique.com`, `dmoptic.com` | **Existent mais ne servent rien** (réponse vide) | **A** (constat) | Aucune page à eux. Voir §5 |
| 6 | Domaines `.cm` | `dmoptique.cm`, `dmoptic.cm`, `dm-optique.cm` : **inexistants** | **A** | Le `.cm` est libre — à réserver au nom du client |

---

## 4 · Le drapeau afribobo 2019 — pourquoi il est écarté, et ce qu'il contamine

**Les faits.** Une petite annonce afribobo de **décembre 2019**, libellée **« DM optometrie »**, prix
**2 500 F**, publiée par un **particulier nommé Samuel**.

**Pourquoi elle est écartée (niveau C → D pour tout usage public) :**

1. **Le nom ne correspond pas.** « DM optometrie » ≠ « DM Optique ». L'optométrie et l'optique-lunetterie
   sont des métiers distincts ; rien n'établit qu'il s'agisse du même cabinet.
2. **L'émetteur ne correspond pas.** Publiée par un particulier (**Samuel**), pas par M. Domche Noumbi.
3. **Aucun recoupement.** Ni adresse, ni téléphone, ni autre point de contact commun.
4. **L'ancienneté.** Décembre 2019 : près de sept ans.

**Règle appliquée** (`build-notes.md` §2) : *« une valeur sans source n'entre pas dans une page de
santé »*. L'annonce n'apparaît **nulle part** sur la page, et ne doit apparaître sur aucun support.

### ⚠️ Effet de bord à signaler : l'ancrage de prix « 2 500 FCFA »

La synthèse du 01/10 retient comme ancrage de marché : *« les examens de vue à 2 500 FCFA
historiquement »*. Or **le seul « 2 500 F » documenté dans le dépôt est le prix de cette annonce
afribobo de décembre 2019** — celle-là même qu'on écarte comme non fiable et sans lien établi.

**Conséquence :** cet ancrage de prix repose sur (a) une source qu'on a jugée non pertinente pour ce
cabinet, (b) un prix vieux de près de sept ans, (c) une prestation non précisée. **Il ne peut pas
porter une décision de positionnement tarifaire.** Ce n'est pas une raison pour afficher un prix — le
dépôt n'en affiche aucun — mais c'est une raison de **ne pas construire la stratégie sur ce chiffre**.
→ **Action : établir l'ancrage réel sur le terrain lors de la visite des 07–08/10**, pas sur une
annonce de 2019. Détail dans `market-analysis.md` §5.

---

## 5 · Ce qui n'existe pas (constat négatif, vérifié le 24/09)

Aucun des canaux suivants n'a été trouvé. Un constat négatif est daté : il vaut **au 24/09/2026** et
doit être re-vérifié avant le lancement.

| Canal | État au 24/09 |
|---|---|
| Site web | aucun |
| Facebook | aucune page |
| TikTok | aucun compte |
| Instagram | aucun compte |
| YouTube | aucune chaîne |
| X / Twitter | aucun compte |
| Blogspot / WordPress | aucun |
| Google Business Profile | aucune fiche |
| Annuaire / répertoire | aucune entrée |

**Ce que ça veut dire commercialement.** « Vous n'êtes nulle part » est **vrai** — et c'est l'actif
narratif de la page : *le registre de l'Ordre le connaît depuis 2016, le web non.* Mais la réciproque
est vraie aussi : **il n'y a aucun avis, aucune photo, aucun contenu à reprendre.** Tout est à produire,
et **aucun témoignage ne peut être repris** puisqu'il n'en existe aucun.

**À re-vérifier avant lancement** (l'absence peut avoir changé) : page Facebook, fiche Google,
`dmoptique.com` / `dmoptic.com`.

---

## 6 · Ce qu'on ne sait toujours pas

| Inconnu | Pourquoi ça bloque |
|---|---|
| **Jours d'ouverture** | Les heures sont connues (8h00–17h30, consultation 8h30–13h30), **les jours non**. La page n'affirme aucun jour |
| **NIU + adresse fiscale** | Sans eux, pas de proforma conforme pour une SARL |
| **Marques de montures vendues** | La vitrine ne nomme **aucune** marque ; on n'invente pas de portefeuille |
| **Moyens de paiement** | Espèces, MTN MoMo, Orange Money ? Un patient qui vient sans pouvoir payer est un patient perdu |
| **Assurances / mutuelles** | Décide le patient assuré et distingue le cabinet |
| **Périmètre réel des six actes** | La page liste six services **types**, signalés comme tels. Un cabinet ne fait pas tout |
| **Photos réelles** | Les trois images de la vitrine sont des **illustrations**. Bloquant pour le site **et** les carrousels |
| **Un repère physique** | « en face de… », « à côté de… » — l'adresse seule ne suffit pas à Bonabéri, où l'on arrive en taxi |

→ Ces huit points sont repris, structurés et prêts à poser dans
**`clients/dm-optic/onboarding/intake-questionnaire.md`**.
