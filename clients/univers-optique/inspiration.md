# Univers Optique — inspiration (21 Sep 2026, 21:15 → 22:40)

**Commande de King :** « *build the website following our pipeline … this time make sure you dig deep and
find out everything : all his social and google business reviews everything.* » → le brief n'est pas
« faire joli », c'est **prouver qu'on a lu**. Deux recherches ne suffisaient pas chez ce prospect, et mon
message du 21/09 17:50 le disait à l'envers (voir la correction plus bas).

---

## 1 · Le portail a été fait — six sources, pas deux

| # | Source, lue en entier | Ce qu'elle a donné |
|---|---|---|
| 1 | **Le nom de domaine lui-même** : `getent hosts univers-optique.com` + `universoptique.cm` + `curl -I` | **aucun enregistrement DNS, HTTP 000** → le site est mort, ce n'est pas une impression |
| 2 | **Wayback Machine** : API `availability` puis deux captures lues (`…/20231102113017/` et `…/20240109220045/`) | **10 captures, 06/01/2018 → 09/01/2024** ; dernière page vivante = WordPress 3 cartes ; la capture suivante = un **répertoire Apache vide** → date de mort : janvier 2024 |
| 3 | **Fiche Google Maps**, reprise intégralement par le miroir `docteur.go.yo.fr/univers-optique/` | **3,3 / 5 · 6 avis** · catégorie Opticien · horaires lun–ven 8h–18h, sam 8h–13h, dim fermé · plus code **3P3G+JCG** · « entre pharmacie Sass et Express Union » · **champ site VIDÉ** · **aucun réseau social relié** · place id + coordonnées geo relevés |
| 4 | **Annuaire Maligah**, fiche `ETS UNIVERS OPTIQUE` | raison sociale · **BP 4680** · **trois lignes téléphoniques** · « Produits et soins oculaires » · champs **e-mail / langues / moyens de paiement non renseignés** |
| 5 | **Annonce kerawa.com** (2009→2022), support retiré depuis, texte encore indexé | **début d'activité le 01/08/2009** · liste des services dont **prothèses oculaires** et **verres de sécurité** · `universoptique@yahoo.fr` · horaires conformes à Google |
| 6 | **Recherche des homonymes et des réseaux** : Facebook / Instagram / TikTok, avis « Univers Optique », ONOC | page `universmedicale` = « Univers Optique · 508 likes · **Global trade invesment** » → **homonyme, métier différent, NON revendiquée** ; « Univers Optique Hagondange » (Moselle) **4,9/5 · 9 avis** → un homonyme français mieux noté que lui, qui passe avant lui ; **aucun** compte Instagram/TikTok rattachable trouvé |

**Ce que la fouille a trouvé que deux recherches n'auraient pas trouvé :** sur sa propre page de 2023,
au paragraphe « Verres et montures », il est écrit « **Chez Gweleo**, vous pouvez désormais adapter des
nouveaux verres correcteurs… ». Le nom d'une enseigne étrangère est resté collé dans son texte. Ses trois
cartes « NOS SERVICES » pointent **toutes vers `/examen-de-vue/`**. Et une bannière « **15 % de réduction** »
est restée en ligne sans promotion derrière.

## 2 · La correction de mon message du 21/09 17:50 (loi maison : une divergence s'examine sur les deux supports)

J'ai écrit au prospect qu'il était « **absent du web** ». **C'est faux**, et la fouille le prouve : il a une
fiche Google notée, un nom de domaine enregistré (mort), une fiche annuaire à son nom légal, une annonce
qui date de 2009. **Le vrai constat, et il est plus fort :**

> Ce n'est pas qu'il est absent du web. **C'est que sa seule page vivante est celle d'un autre.**
> Depuis janvier 2024, l'adresse qui parle de lui est un miroir tenu par un tiers : il y publie ses
> horaires, son adresse, sa note de 3,3/5 sur 6 avis — et le champ « site web » y est vide.

Ce cadrage est dans la page (section *Le dossier*, six constatations) et dans la feuille d'envoi. Le
message WhatsApp déjà parti n'est **pas** corrigé en public : on n'engueule pas le client (loi des
contenus, 19/09 19:40) — mais on ne le répète pas.

## 3 · Ce qui est publié sur la page, et ce qui ne l'est PAS

**Publié (parce que lu) :** la note 3,3/5 avec ses 6 avis · les horaires Google · l'adresse, le plus code
et le repère « entre pharmacie Sass et Express Union » · le BP 4680 · les trois lignes téléphoniques ·
les deux e-mails publics · les dix actes listés dans l'annonce et l'archive · la date de création 2009 ·
le fait que le domaine ne répond plus · le fait que Gweleo traîne dans son texte.

**Retenu, et c'est délibéré :**
- **aucun prix affiché** — il n'en a publié nulle part, et AMK ne met pas un prix dans la bouche d'un
  prospect (loi maison : pas de prix au message 1 ; ici, pas de prix du tout dans sa copie) ;
- **le « 15 % » n'est PAS repris comme une offre** : il devient la question n° 2 à trancher ;
- **aucun `aggregateRating`** dans le JSON-LD : baliser 3,3/5 sur 6 avis, c'est servir une étoile pâle dans
  les résultats. Visible sur la page, marqué pour Google : non, pas encore ;
- **aucun `sameAs`** : aucune page sociale ne lui est rattachée avec certitude ; la page à 508 likes est
  un homonyme ;
- **le numéro fixe n'est PAS affiché en clair** : les deux supports du client l'écrivent différemment
  (« +237 33 18 33 08 » ailleurs / « 243 18 33 08 » sur son pied de page 2023). Une divergence entre deux
  supports du client = une **question**, jamais une correction publiée, et jamais un numéro deviné.
- **`tel1` est vide dans la copie** et la page le dit dans ses questions ouvertes.

**Les six questions à trancher par lui** sont une section de la page (et non une note interne) : un
aperçu qui ne montre que ce qui brille est un catalogue.

## 4 · Ce que la fouille a donné comme argument de vente, sans rien inventer

1. **La rareté réelle** : prothèses oculaires + verres de sécurité en atelier + formations. Personne
   dans le quartier ne peut disputer ça, et ce n'est écrit nulle part sous son nom.
2. **L'ambiguïté du nom** : taper « Univers Optique avis » renvoie d'abord à un opticien de Moselle noté
   4,9. La réponse n'est pas un logo, c'est **le quartier dans le titre** (« Univers Optique Bépanda —
   opticien à Douala »), dans le JSON-LD, dans les légendes.
3. **Les champs vides** : langues parlées, moyens de paiement, e-mail — un acheteur institutionnel
   (RH, mutuelle, école) remplit sa shortlist avec ça. Trente minutes de travail, zéro budget.
4. **La fiche Google d'abord** : c'est son premier visiteur. Récupérer l'accès, répondre aux six avis,
   relier le site → c'est l'étape 0 du devis, écrite dans la page.

## 5 · Ce qui reste à obtenir (et qui n'est pas négociable avant publication)

Accès à la fiche Google Business · propriété du domaine `univers-optique.com` (le relancer ou non) ·
le bon numéro fixe · un seul e-mail à afficher · l'ordre des trois lignes · l'existence éventuelle d'une
page Facebook à son nom · **les photos réelles** (devanture, comptoir, une mesure chez le client).
Les visuels de la page sont **étiquetés « Rendu de concept — votre photo le remplacera »**, en FR et EN,
sur chaque image (consigne du 21/09, 20:20 : générer est autorisé, faire croire que c'est son magasin ne
l'est pas).
