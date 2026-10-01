# FEUILLE D'ENVOI · UNIVERS OPTIQUE (Bépanda, Douala) — mardi 22/09/2026, matin
**Objet : la direction demandée est faite. Le fichier est à toi, pas un lien.**

---

## 1 · Ce qui est envoyé

| Fichier |_octets_ | sha256 (16 premiers) | À quoi ça sert |
|---|---|---|---|
| `demos/concept-univers-optique-v2.html` | **734 727** (718 Ko) | `ca52d3c5f6ccb7ec` | **la v2 « GRANDE PHOTO »** — la version à envoyer |
| `demos/concept-univers-optique-v2-sobre.html` | **81 565** (80 Ko) | `6a07f2c4aee18b77` | repli si WhatsApp refuse la pièce jointe (même copie, 0 visuel) |
| `demos/concept-univers-optique-v1.html` | 740 056 (722 Ko) | `719f8b60283184b6` | le dossier v1 — **à ne plus envoyer**, gardé pour la comparaison |

**Contrôles passés sur la v2** (avant écriture, dans le générateur) : 74 lignes, **0 faute** —
`audit_html.py` **0 constat confirmé** sur 470 portées de texte (desktop et mobile) ·
`check_inline_js.py` **0 faute sur 4 blocs** `<script>` (JSON-LD validé à part) · `diff` démo ↔
aperçu `/univers/` = **0 ligne** · dimensions des quatre visuels revérifiées à `identify` ·
**huit mutations** de contrôle rejetées (`rc=1`, livrable intact).

## 2 · Le chemin réel du fichier (à télécharger ici, pas à déployer)

```
/home/user/AMK/demos/concept-univers-optique-v2.html
```

`amk-cm.vercel.app/univers/` répond **404** tant que TU ne déploies pas : n'envoie **aucun lien**,
envoie **le fichier**. Il s'ouvre dans n'importe quel navigateur, téléphone ou ordinateur, sans réseau
pour les images (elles sont embarquées), **sans JavaScript pour se peindre** (le JS ne fait qu'animer
les trois étapes et basculer FR/EN).

**Si le client ouvre le fichier et voit une page vide ou coupée** : ce n'est pas le design, c'est un
téléchargement tronqué — vérifier les **734 727 octets** et le début du sha256 `ca52d3c5…` avant de
répondre à la remarque. La version du 21 au soir, elle, avait un vrai défaut (le contenu n'apparaissait
que si le JavaScript s'exécutait) : corrigé à la source, règle consignée dans `design/WORKFLOW.md`
étape 8 et `design/LESSONS.md`.

## 3 · Message à coller (FR, WhatsApp)

> Bonjour, votre aperçu est prêt, en pièce jointe (un seul fichier HTML, à ouvrir dans un navigateur).
> Vous verrez d'abord la salle de vente, puis les trois étapes — mesurer, poser un créneau, poser les
> verres —, le face-à-face « votre fiche d'aujourd'hui / ce que la page ajoute », vos six avis tels
> qu'ils sont, et la liste des six points que vous seul pouvez trancher.
> Rien de ce qui est écrit n'a été inventé : chaque ligne est lue à une adresse précise (fiche Google,
> archives du web, annuaire de l'Ordre), et ce que je n'ai pas pu vérifier est posé comme question, pas
> comme argument. Les images sont des rendus de concept, ils disent « votre photo le remplacera ».
> Il y a une version française et une anglaise dans le même fichier, avec un bouton FR/EN.
> Si la direction vous va, je la décline sur les pages internes ; si elle ne vous va pas, dites ce qui
> cloche et je la refais — c'est un aperçu, pas un devis engagé.

**À ne pas écrire** : « absent du web » (faux — il y a eu un site, mort le 9 janv. 2024), « 15 % »
comme une offre (elle existe sans date de fin, c'est UNE QUESTION), un prix (100 000 FCFA = la réponse
déjà faite à sa question du 21/09 18:08, à maintenir, pas à réécrire ici), un témoignage ou une note
moyenne en étoiles.

## 4 · Ce que la v2 change par rapport à la v1 (à dire si on demande)

| | v1 « le dossier » | **v2 « la grande photo »** |
|---|---|---|
| Registre | dossier de reprise, filets, densité 5 | cabinet, photo, air, densité 3 |
| Ouverture | carte d'état + six constats | **photo pleine largeur + titre serif, un mot en italique** |
| Services | tableau de dix lignes à filets | **trois paquets, une raison par paquet (dix lignes couvertes)** |
| Preuve | tableau, notes de bas de page | **face-à-face 8 lignes, colonne de droite surlignée** |
| Images | 3 rendus | **4 rendus**, tous relus un à un, zéro lettrage inventé |
| Rendez-vous | boutons WhatsApp | **pastilles de créneaux dans le hero, liens réels, marche sans JavaScript** |
| Pied de page | bloc court | **écran de conversion complet (4 blocs) + barre collée au pouce** |

Faits, chiffres, sources, six questions, horaires, NAP : **identiques** entre les deux. Seul le langage
visuel a été refait, sur tes quatre captures (gabarit « Grande Photo · Propre · Moderne » + trois écrans
Function). Overrides de loi **assumés et écrits** : crème+terracotta et la pilule du hero viennent de la
référence (design/STYLE-TOKENS.md, ligne du 22/09), pas d'un réflexe.

## 5 · Ce qui reste dû, dans l'ordre

1. **Sa réponse à lui** sur la direction (v2) et sur les six questions — rien n'est publiable sans ça.
2. **LE CRISTALLIN** : sa réponse **A / B** (page seule 100 000 · page + page Facebook 50 000) — relance
   prévue 23/09, et lui renvoyer `demos/concept-le-cristallin-v1.html` (620 492 octets), sa copie du
   dimanche étant cassée.
3. **Envoi** : je ne touche à aucun compte. Les messages sont prêts ci-dessus, le déclencheur reste à toi.
