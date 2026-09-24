# Réponse — CAVISA OPTIQUE a regardé l'aperçu · 24/09/2026, 13:16

**Ce qu'il a écrit, mot pour mot :** *« Beaucoup de manquement mais c'est appréciable. »*
**Avant, à 13:09, King a envoyé** le lien `https://cavisa.vercel.app/` (carte de lien affichée : titre + description ; **sans vignette** — `og:image` était encore commenté, corrigé depuis, redéploiement nécessaire).

---

## 1 · Comment on lit cette phrase

**Ce n'est pas un refus.** Trois signes : il a **ouvert** la page, il l'a **jugée** (« appréciable »), et il **demande le reste**. Un homme qui refuse écrit « merci » et se tait.

**« Manquement » veut dire : ce qui manque.** Et ce qui manque, on le sait en partie sans lui : la page laisse **volontairement** deux lignes vides — son **adresse exacte** et ses **horaires** — parce qu'on n'invente jamais une information sur une page qui porte son nom. Elles affichent « à confirmer », et c'est visible.

**Et il y a une cause qu'il faut regarder en face.** Le message d'envoi de 13:09 promettait *« vos informations et votre localisation à Douala »* et *« la présentation de vos services et horaires »*. La page, elle, dit « à confirmer » sur les deux. **Un client qui lit la promesse puis la page appelle ça un manquement — et il a raison.** La leçon est écrite dans `sales/MESSAGES-2026-09-23-PERSUASION.md` §2.

**Donc la réponse n'est pas de nous justifier.** C'est de lui demander ses quatre informations, dans un message qui rend la chose facile : il envoie, on complète.

---

## 2 · LE MESSAGE À ENVOYER (FR, prêt à copier)

> **Avant de l'envoyer : redéployer `hosting/previews/cavisa/`** (dossier entier). Le lien portera alors sa vignette, et la page en ligne sera à coup sûr la version du jour — photos comprises.

```
Merci d'avoir pris le temps de regarder, et merci pour le compliment.

Vous avez raison, il manque des choses — et c'est normal : ce sont vos
informations, pas les miennes. Je n'ai pas voulu les inventer.

Pour compléter, il me faut de vous :
• votre adresse exacte, avec un repère (« en face de… », « à côté de… »)
  — le plus simple : envoyez-moi votre position WhatsApp, un appui suffit
• vos horaires d'ouverture
• ce que je n'ai pas listé : vos marques, les lunettes de soleil, les
  montures enfants, ce que vous réparez sur place
• 2 ou 3 photos de la boutique prises avec votre téléphone — la devanture,
  le comptoir, vos montures

Et une question : vous voulez afficher vos prix sur la page, ou les garder
pour la conversation ?

Envoyez-moi tout ce que vous avez, même en vrac. Dès que je les ai, je
complète et je vous renvoie la page à jour.

— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ce message est écrit ainsi** (règles maison) : première ligne **pour lui**, nom et titre **à la fin** (`sales/MESSAGES-2026-09-23-PERSUASION.md` §1) · **aucun prix** · **une seule question** posée · rien qu'on ne puisse tenir (« dès que je les ai », pas « dans l'heure ») · aucune promesse de classement, aucun nom d'un autre opticien, aucune allusion au registre.

**Variante courte** (s'il répond par note vocale ou s'il est pressé) :

```
Merci d'avoir regardé. Vous avez raison : il manque votre adresse et vos
horaires — je ne les ai pas inventés exprès. Envoyez-moi ça, plus 2-3 photos
de la boutique, et je complète aujourd'hui.
— Akwo King / AMK
```

---

## 3 · Ce que chaque réponse change dans la page (écrit d'avance, pour ne pas improviser)

| Ce qu'il envoie | Ce qu'on fait dans `demos/concept-cavisa-v1.html` |
|---|---|
| Adresse + repère (ou position WhatsApp) | La carte claire « à compléter » devient un bloc **Nous trouver** : adresse écrite, repère, et un lien **Itinéraire** (`google.com/maps/search/?api=1&query=…`) — aucun besoin d'une fiche Google pour que le lien fonctionne. |
| Horaires | Ils apparaissent dans la **barre du haut**, dans la section contact, et alimentent le bandeau « ouvert / fermé » calculé à l'heure de Douala (le même mécanisme qu'UNI-LABO, honnête parce que les horaires sont les siens). |
| Marques, solaires, enfants, réparations | La grille « Au comptoir » s'étend — **ses** mots, pas les nôtres. |
| 2-3 photos | Elles remplacent les deux illustrations, et la légende « mise en situation » disparaît. Sa devanture passe en hero. |
| « Oui, affichez les prix » | Une section prix avec **ses** chiffres. Nous ne proposons jamais un prix à sa place. |
| « Non, gardez-les en conversation » | La page ne change pas d'un mot : elle promet déjà l'annonce du prix sur WhatsApp. |

**Et une chose qu'on ne fait pas maintenant** : lui offrir la création de sa **fiche Google** (il n'en a pas — `google.com/maps/search/Cavisa+Optique+Douala` répond « Google Maps can't find… »). C'est un **projet séparé**, pas un cadeau de finition. On le garde pour la conversation de clôture, après qu'il ait vu la page complétée.

---

## 4 · Ce qu'on ne fait pas

- **Aucune relance** tant qu'il n'a pas répondu : c'est lui qui doit la balle.
- **Aucun prix inventé**, aucun délai inventé, aucun avis, aucune note : la règle n'a pas bougé.
- **On ne redéploie pas deux fois pour rien** : un redéploiement maintenant (vignette + photos + état du jour), un autre quand ses informations arrivent.
- **On ne réécrit pas son message** dans nos mots pour lui faire dire mieux que ce qu'il a dit.

---

## 5 · Après son envoi

1. Compléter la page (tableau §3), relancer `python3 demos/build_cavisa.py` + les six portes + `node tools/qa/test_cavisa_page.mjs` (28/28).
2. Redéployer, puis **lui renvoyer le lien** : c'est le moment où il voit ses photos et son adresse à leur place.
3. Journaliser chaque fait dans `sales/Activity-Log.md` (heure + mot exact), et mettre le CRM à jour dans `leads/build/crm.py` — **jamais à la main dans le CSV**.
4. La conversation de clôture vient **après** qu'il ait dit « c'est bien » — pas avant.
