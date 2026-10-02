# DM OPTIQUE · Correspondance variantes → messages pré-remplis

```
Status: PRÊT — attribution par variante                     ·  Updated: 2026-10-02
Règle : chaque variante a SON message pré-rempli, et donc SON chiffre.
Lecture : coût par message = dépense de la variante ÷ messages reçus pour cette variante.
⛔ Rien de ceci n'est public avant l'encaissement de l'acompte (§14, décision du 21/09).
```

## 0 · Pourquoi ce fichier existe

King, 02/10/2026 : *« Log the variant-to-message mapping in `clients/dm-optic/ads/variant-messages.md`
so that cost-per-message per variant is readable at a glance. »*

**Le problème qu'il règle :** sans message pré-rempli propre à chaque variante, un message WhatsApp qui
arrive est **anonyme** — impossible de dire quelle accroche l'a produit, donc impossible de calculer un
coût par message par variante. Avec un message pré-rempli, **l'attribution est dans la conversation
elle-même** : le client cite l'accroche qu'il a vue. Zéro devinette.

**Règles debout :**
- **Chaque CTA aboutit sur WhatsApp.** Jamais sur le site, jamais en commentaire.
- **Un message = une variante = un numéro de suivi.** Une variante EN publiée plus tard reçoit **sa
  propre ligne** (attribution = variante × langue).
- **La règle des 3 000 FCFA est exécutée, pas suggérée** : au-dessus de 3 000 FCFA par message, on coupe
  la variante — et on note le chiffre quand même (`README.md` §5).
- Le message pré-rempli est **celui que le spectateur envoie** — il cite l'accroche, il ne fait aucune
  allégation médicale. C'est sa phrase, pas la nôtre.

**Format du lien :** `https://wa.me/237656122239?text=<message encodé>` — le numéro est le WhatsApp du
cabinet (656 122 239). Ne jamais changer le numéro dans un lien sans vérifier `dossier.md`.

---

## 1 · La table des 12 — 10 actives, 2 gelées

| # | Statut | Accroche (vidéo) | Message pré-rempli (ce que le spectateur envoie) | Lien WhatsApp |
|---|---|---|---|---|
| **W1-A** | ✅ recommandée | « Cet opticien exerce depuis 2016. Personne ne le trouvait. » | Bonjour ! J'ai vu votre vidéo : « Cet opticien exerce depuis 2016. Personne ne le trouvait. » Où êtes-vous exactement à Bonabéri ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%20%21%20J%27ai%20vu%20votre%20vid%C3%A9o%20%3A%20%C2%AB%20Cet%20opticien%20exerce%20depuis%202016.%20Personne%20ne%20le%20trouvait.%20%C2%BB%20O%C3%B9%20%C3%AAtes-vous%20exactement%20%C3%A0%20Bonab%C3%A9ri%20%3F) |
| **W1-B** | variante | « Dix ans d'expérience. Zéro résultat sur Internet. » | Bonjour, j'ai vu la vidéo « Dix ans d'expérience, zéro résultat sur Internet ». C'est bien vous ? Où vous trouver ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20la%20vid%C3%A9o%20%C2%AB%20Dix%20ans%20d%27exp%C3%A9rience%2C%20z%C3%A9ro%20r%C3%A9sultat%20sur%20Internet%20%C2%BB.%20C%27est%20bien%20vous%20%3F%20O%C3%B9%20vous%20trouver%20%3F) |
| **W1-C** | variante | « Vous ne savez pas à qui confier vos yeux ? » | Bonjour, je cherche un opticien de confiance à Douala. Pouvez-vous m'aider ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20je%20cherche%20un%20opticien%20de%20confiance%20%C3%A0%20Douala.%20Pouvez-vous%20m%27aider%20%3F) |
| **W2-A** | ✅ recommandée | « Vous plissez les yeux en fin de journée ? » | Bonjour, j'ai vu votre vidéo. Je plisse les yeux en fin de journée — est-ce que je peux passer pour un examen de vue ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20votre%20vid%C3%A9o.%20Je%20plisse%20les%20yeux%20en%20fin%20de%20journ%C3%A9e%20%E2%80%94%20est-ce%20que%20je%20peux%20passer%20pour%20un%20examen%20de%20vue%20%3F) |
| **W2-B** | variante ⚠️ faible | « Trois signes que vos yeux fatiguent. » | Bonjour, j'ai vu la vidéo « Trois signes que vos yeux fatiguent ». Je peux passer pour un examen de vue ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20la%20vid%C3%A9o%20%C2%AB%20Trois%20signes%20que%20vos%20yeux%20fatiguent%20%C2%BB.%20Je%20peux%20passer%20pour%20un%20examen%20de%20vue%20%3F) |
| **W3-A** | ✅ recommandée | « Vous avez trois paires. Vous n'en portez aucune. » | Bonjour ! « Vous avez trois paires, vous n'en portez aucune » — c'est moi. Je peux passer essayer des montures au cabinet ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%20%21%20%C2%AB%20Vous%20avez%20trois%20paires%2C%20vous%20n%27en%20portez%20aucune%20%C2%BB%20%E2%80%94%20c%27est%20moi.%20Je%20peux%20passer%20essayer%20des%20montures%20au%20cabinet%20%3F) |
| **W3-B** | variante | « Cette paire vous plaisait en boutique. Plus maintenant. » | Bonjour, j'ai vu votre vidéo. J'ai des lunettes que je ne porte plus. Vous pouvez m'aider à choisir une monture ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20votre%20vid%C3%A9o.%20J%27ai%20des%20lunettes%20que%20je%20ne%20porte%20plus.%20Vous%20pouvez%20m%27aider%20%C3%A0%20choisir%20une%20monture%20%3F) |
| **W3-C** | variante | « Une monture, ça ne s'achète pas. Ça s'essaie. » | Bonjour, votre vidéo dit qu'une monture, ça s'essaie. Je peux passer essayer au cabinet ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20votre%20vid%C3%A9o%20dit%20qu%27une%20monture%2C%20%C3%A7a%20s%27essaie.%20Je%20peux%20passer%20essayer%20au%20cabinet%20%3F) |
| **W4-A** | variante | « Huit heures d'écran. Vos yeux le sentent. » | Bonjour, j'ai vu votre vidéo. Je passe huit heures par jour sur un écran — quels verres me conseillez-vous ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20votre%20vid%C3%A9o.%20Je%20passe%20huit%20heures%20par%20jour%20sur%20un%20%C3%A9cran%20%E2%80%94%20quels%20verres%20me%20conseillez-vous%20%3F) |
| **W4-B** | ✅ recommandée | « Quatre situations où vos yeux travaillent. » | Bonjour, j'ai vu la vidéo « Quatre situations où vos yeux travaillent ». Écran, route, lecture, soleil : vous avez des verres pour ça ? | [ouvrir](https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20la%20vid%C3%A9o%20%C2%AB%20Quatre%20situations%20o%C3%B9%20vos%20yeux%20travaillent%20%C2%BB.%20%C3%89cran%2C%20route%2C%20lecture%2C%20soleil%20%3A%20vous%20avez%20des%20verres%20pour%20%C3%A7a%20%3F) |

### Les deux gelées — pas de lien tant que la décision n'est pas prise

| # | Statut | Accroche | Raison · décision requise |
|---|---|---|---|
| **W2-C** | ⛔ **frozen — gelée indéfiniment** (King, 02/10) | « Vos yeux fatiguent. Ce n'est peut-être pas seulement l'écran. » | « ce n'est peut-être pas seulement l'écran » sous-entend une **cause médicale**. Règle R1 du 02/10. Conservée au fichier avec sa raison, sans lien. |
| **W4-C** | ⛔ **frozen — awaiting King ruling** | « Le soleil de Douala. Vos yeux le paient. » | « le paient » sous-entend un **dommage**. Test de King : si peur du coût de la négligence → reste gelée ; si simple énoncé tarifaire → dégel. Pas un énoncé tarifaire à ce stade. Pas de lien tant que gelée. |

---

## 2 · Le tableau de mesure — remplir pendant le mois 1

| Variante | Dépense (FCFA) | Messages reçus | Coût / message | Décision (≥ 3 000 = couper) |
|---|---|---|---|---|
| W1-A |  |  |  |  |
| W1-B |  |  |  |  |
| W1-C |  |  |  |  |
| W2-A |  |  |  |  |
| W2-B |  |  |  |  |
| W3-A |  |  |  |  |
| W3-B |  |  |  |  |
| W3-C |  |  |  |  |
| W4-A |  |  |  |  |
| W4-B |  |  |  |  |

**Rappel du seuil :** budget d'essai 5 000 FCFA, concentré en **un seul test S2**. À 3 000 FCFA le
message, 5 000 FCFA = **1,67 message** — c'est le seuil de lisibilité, pas un objectif (`content-plan-month1.md`).

**Un message reçu ≠ une demande.** §3 : compter les **conversations**, pas les clics. Un message
pré-rempli reçu = une conversation ouverte.

---

## 3 · Règle d'usage sur place

- Le lien se met **dans la légende et en commentaire épinglé** de chaque vidéo publiée — jamais seulement
  dans la bio.
- **Une variante = une publication.** Deux variantes ne partagent jamais un lien.
- Si une variante EN est produite : **nouvelle ligne** `W1-A-EN`, nouveau lien, nouveau chiffre.
- À la fin de chaque semaine : reporter dépense et messages dans le tableau §2.
