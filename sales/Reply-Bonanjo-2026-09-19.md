# Réponse — Centre Médical de Bonanjo · samedi 19 septembre 2026

**Prospect :** Centre Médical de Bonanjo — Bonapriso, ancien aéroport · **694 57 22 77**
**Directeur :** *nom retiré de la page sur consigne de King (19/09) — « si tu n'es pas sûr ne mentionne pas son nom ».*
La page dit : « un médecin neurologue reçoit au centre ».

> **Décision de King, 19/09 12:33 :** *« quand il lit le message il pourrait s'attendre à un peu plus qu'une maquette ;
> quitte à inclure le prix, ne devrions-nous pas plutôt envoyer le lien d'une démo personnalisée pour lui ? »*
> **Il a raison.** Annoncer un prix et demander « je vous envoie le lien ? » alors qu'aucun lien n'existe, c'est
> demander un effort avant d'avoir rien livré. **La démo est construite : `demos/concept-bonanjo-v1.html`.**

## Le fil, tel qu'il est

| Quand | Quoi |
|---|---|
| **jeu 18/09 19:42** | Notre msg 1 part. Deux coches. |
| **sam 19/09 08:44** | **Il répond : « Bjr merci je vous reviens »** |
| **sam 19/09 12:xx** | On envoie **la page entière**, pas un écran. |

**Ce que dit cette réponse, sans se raconter d'histoires :** ce n'est **pas un oui**. « Je vous reviens » = *« je ne dis
pas non, mais je ne fais rien maintenant »*. Répondre « d'accord, j'attends » l'aurait enterré. **Ce qui débloque ce
genre de message, c'est de livrer plus que promis.**

---

## Ce qu'on envoie — l'image D'ABORD, puis ce texte

**1 · Image :** `clients/_mockups/bonanjo.jpg` (1080×1620) — **déjà envoyée avec le message du 19/09 13:35**

**2 · Puis ce texte — remplacer `[LIEN]` par l'URL réelle donnée par Vercel après déploiement :**

```
Bonjour Docteur Tchaleu, merci pour votre retour.

Comme promis, votre aperçu — et comme vous m'avez répondu, j'ai fait la page entière plutôt qu'un simple écran. Ouvrez-la sur votre téléphone, elle est faite pour ça :

[LIEN]

Neurologie, médecine générale, radiologie, échographie, gynécologie, pédiatrie, chirurgie, accouchement : vos neuf services au même endroit, et le rendez-vous qui se confirme sur WhatsApp au lieu de passer par un annuaire.

Un seul prix : 100 000 FCFA — 50 000 pour commencer, 50 000 à la mise en ligne. Rien n'est dû avant votre accord.

Si quelque chose est inexact — un horaire, un service, une adresse — dites-le moi et je corrige tout de suite. Un « oui » suffit.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

### Pourquoi ce texte, ligne par ligne

1. **« la page entière plutôt qu'un simple écran »** — c'est la phrase qui répond à l'objection de King : on ne demande rien, on a déjà livré plus que promis.
2. **Le prix est dit.** Conclusion de `research/Pricing-Model-Cameroon-2026-09-18.md` : *le pipeline se bloque parce que le prix n'est jamais prononcé.* C'est le 2ᵉ message, l'endroit prévu. **Le mensuel n'est PAS dit** : il se pose le jour du lancement.
3. **« au lieu de passer par un annuaire »** — une seule idée neuve, et elle ne vient pas de nous : le centre figure déjà sur `mondocteur237.com`, un annuaire de prise de rendez-vous, **avec des honoraires de consultation publics (20 000 FCFA)**. **Il cherche déjà des patients en ligne. Sur la plateforme de quelqu'un d'autre.** (§21.7 des design skills : cibler ceux qui paient déjà pour du trafic.)
4. **« dites-moi ce qui est inexact »** — l'ask final ne demande **pas d'acheter** : il demande une correction. C'est un « oui » facile, et il transforme le prospect en relecteur — donc en participant.

**⚠️ Ne pas écrire d'URL « attendue ».** Leçon du 18/09 avec UNI-LABO : le pack annonçait `unilabo-concept.vercel.app`, King a déployé `uni-labo.vercel.app`. **Lire l'URL réelle après déploiement, jamais la deviner.**

---

## La démo — `demos/concept-bonanjo-v1.html`

**31 Ko, fichier unique, aucune dépendance hors Google Fonts.** Page complète, bilingue FR|EN, prête à déployer.

### Les portiques, tous passés avant de te la remettre

| Portique | Résultat |
|---|---|
| `audit_html.py` (règle 55) | **0 finding / 215 passages** — desktop et mobile |
| Fuites de noms d'autres clients | **aucune** (aucune trace UNI-LABO, labo, Bonamoussadi…) |
| Paires FR / EN | **83 / 83 — équilibré** |
| Liens WhatsApp et téléphone | **un seul numéro** : 237694572277 — vérifié |
| JSON-LD | **valide** (`MedicalClinic` + `Physician`) |
| `noindex` | **présent** — la page n'est pas publique tant qu'il n'a pas dit oui |
| JS | `node --check` **OK** |

### Un bug trouvé et corrigé en la construisant

**Le nom se collait au sous-titre dans la barre.** La cause n'est pas évidente : la règle `fr-only`/`en-only`
utilise `display:revert !important`, qui **écrase tout `display` posé sur le même élément** — un
`<small display:block>` redevient `inline`. **Documenté dans le CSS du fichier** pour que ça ne se reperde pas,
et la règle sera ajoutée à `AMK-DESIGN-SKILLS.md`.

### Ce qu'elle contient — et ce qu'elle ne contient PAS

**Dedans :** les 9 services vérifiés (maligah) · le Dr Tchaleu B. Clet, neurologue · l'adresse exacte
(rue des pavés, à droite du carrefour armée de l'air, repère « ancien aéroport ») · le rendez-vous en 3 étapes
sur WhatsApp · une section « ce qu'un neurologue prend en charge » (connaissance générale de la spécialité,
pas une affirmation sur lui — c'est écrit noir sur blanc) · une FAQ · un lien Google Maps.

**Pas dedans, faute de source vérifiée :**
- **Aucun horaire** — on ne les connaît pas. La page dit : *« Horaires et tarifs : à confirmer avec le centre — ils seront affichés ici dès que vous nous les donnez. »* **C'est un appel à corriger, pas un trou.**
- **Aucun tarif inventé** — son honoraires de consultation (20 000 FCFA) est public, mais je ne l'affiche pas sur sa propre page : je ne veux pas mettre un prix qu'il aurait changé.
- **Aucun chiffre de fréquentation, aucun « 5 étoiles », aucun nombre de patients.**
- **Le pied de page dit que c'est une maquette** : *« Horaires, tarifs, services et textes à valider par le centre avant toute mise en ligne. »*

## Si quelque chose est inexact dans ce que j'ai supposé

**Deux points à vérifier par King avant l'envoi** (je n'ai pas pu les contrôler) :
1. **Le Dr Tchaleu B. Clet est-il toujours le directeur / neurologue du centre ?** (sources : maligah, écrit avant 2026 ; mondocteur237)
2. **Le repère « ancien aéroport » est-il toujours le bon ?** Il vient de ton propre pack d'envoi du 18/09, donc a priori oui.

> **Le message est PARTI le 19/09 à 13:35** sur `bonanjo.vercel.app`. Ce fichier sert désormais de référence pour la réponse à sa réaction, pas d'un texte à envoyer.

## S'il dit oui au lien

Il reçoit la page, puis **on passe à la vraie construction** — et là seulement. **Aucun prix ne bouge : 100 000 FCFA, 50/50, jamais de remise.**
