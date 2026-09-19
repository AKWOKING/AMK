# LABIOMED — le PREMIER « oui » de la campagne · samedi 19 septembre 2026

**Prospect :** LABIOMED — 104 Route Deido-Bassa, Deido, Douala · **+237 699 98 54 66**
**Le fil :** message envoyé **19:32** (2 coches, lu) → **« Oui » à 19:43 — 11 minutes plus tard.**
**Puis King a envoyé l'aperçu et le texte SANS le prix** (son choix : *« je veux que le prix soit accompagné d'un lien »*).
**Le lien existe maintenant.**

> **C'est le premier « oui » de la campagne.** 45 messages envoyés, 3 réponses humaines — et la première main levée.
> **Ce n'est pas un « je vous reviens ».** C'est une demande.

---

## État réel du fil, au 19/09 20:02

| Quand | Quoi | État |
|---|---|---|
| 19:32 | Notre msg 1 | **Lu (2 coches)** |
| 19:43 | Il répond **« Oui »** | — |
| 20:02 | Aperçu + texte (sans le prix, sur décision de King) | **1 coche — PAS ENCORE LU** |
| — | **Le lien de la démo** | **à envoyer** |

**`last seen today at 19:44`** — il a lu le « Oui » à 19:44 et **n'a pas encore ouvert le message de 20:02.**

---

## À envoyer — le lien ET le prix, ensemble

**Déployer d'abord :** `hosting/previews/labiomed/` (6 fichiers, ~530 Ko — `index.html` **+ le dossier `img/`**).
**Puis remplacer `[LIEN]` par l'URL réelle que Vercel donne. Ne jamais la deviner** (leçon UNI-LABO).

```
Docteur, voici la page complète :

[LIEN]

Ouvrez-la sur votre téléphone — elle est faite pour ça. Vous y verrez : ce qu'un
patient doit préparer avant de venir (à jeun ou pas, ce qu'il faut apporter), la
liste de vos examens, comment les résultats sont annoncés sur WhatsApp, et vos
deux adresses.

Rien n'est inventé : tout vient de vos informations publiques. C'est une maquette,
pas le site final — dites-moi ce qui est inexact et je corrige.

Le prix : 100 000 FCFA pour la page complète en français et en anglais, live en
3 à 5 jours. La moitié pour commencer, la moitié à la mise en ligne. Rien n'est dû
avant votre accord.

— Akwo King / AMK – Développement Web & Solutions Digitales
```

### Pourquoi le prix va avec le lien, et pourquoi il n'était pas dans le 1er message

**King a raison sur le principe :** *« le prix accompagné d'un lien »*. Un prix sans rien à voir est un chiffre abstrait ;
**un prix à côté d'une page qu'il peut ouvrir est un achat.** C'est exactement l'ordre : **la preuve, puis le prix.**

**Et le mensuel n'est toujours pas là.** Il se pose **le jour du lancement** — pas maintenant. Dire « 15 000 par mois »
à ce stade transforme un projet clair en abonnement, et **l'abonnement se refuse plus facilement que le projet.**
`100 000 FCFA, 50/50, jamais de remise.` La règle 43 ne bouge pas.

**Ce qui manque encore, et qui est volontaire :** la page dit *« Horaires : à confirmer »*. **C'est un appel à corriger, pas un trou.**
S'il répond avec ses horaires, il a déjà commencé à travailler avec nous.

---

## La démo — `hosting/previews/labiomed/`

**Ce qui a décidé du design : LE MARCHÉ, comme King l'a demandé.**

Les 5 laboratoires camerounais qui ont un site ont été **ouverts et lus** (ce sont ceux qu'on avait écartés du pack LABOS) :
`douala-labo.com` · `laboratoire-drouot.com` · `kylayalabo.com` · `scientilabo.com` · `lebondiagnostic.com`.

**Ce que le marché fait :** le laboratoire le plus établi de Douala — **Douala Labo, 35 ans d'existence** — utilise
un **hero en photo plein écran avec le texte par-dessus**, et une barre de trois accès rapides
(*Espace résultats · Nos spécialités · Unité COVID*). **C'est le standard du marché. La page le suit.**

**Ce que le marché ne fait pas, et qui fait la différence :**
- **Le voile dégradé sous le texte.** Leur photo est décorative ; ici elle est **lisible**. C'est ce qui a passé le portique contraste du premier coup.
- **Une page qui répond à la vraie question du patient** — « je dois venir à jeun ? » — au lieu d'un catalogue de spécialités.
- **Mobile d'abord.** Leur site est fait pour un ordinateur ; ici, le bouton WhatsApp est collé en bas de l'écran du téléphone.

**Les 6 photos :** le hero (prélèvement) a été **généré** avec exclusion explicite de tout texte, logo et panneau,
puis **relu à l'œil** ; les 4 autres viennent des visuels de laboratoire **déjà présents dans le dépôt**
(`labo-samples`, `labo-hero`, `labo-reception`) — King avait raison, ils étaient déjà là et ils sont bons.

**Portiques :** `audit_html.py` → **0 finding / 245 passages** (desktop et mobile) · **5 images, 0 cassée** ·
FR/EN équilibré · **un seul numéro partout** (237699985466) · `noindex` · JSON-LD `MedicalLaboratory`.

---

## Ce qui reste, dans l'ordre

1. **Déployer `hosting/previews/labiomed/`** et lire l'URL réelle.
2. **Envoyer le lien + le prix** (texte ci-dessus).
3. **S'il dit oui :** on construit pour de vrai, et **on demande les horaires** — c'est la première chose à corriger.
4. **S'il demande une remise :** la réponse est non, et c'est écrit d'avance. `100 000, 50/50, jamais de remise.`
