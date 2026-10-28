# La carte de rendez-vous, dans ses trois états — 27 octobre 2026

Captures **réelles** : Chromium headless (`tools/video/install.sh`), page servie en local, carte
`#appointments` cadrée, en-tête masquée pour la lisibilité.

| Fichier | État | Ce qu'on doit y voir |
|---|---|---|
| `carte-eteinte-1440.jpg` | `bookingUrl` vide partout (aujourd'hui) | aucun bouton de réservation, la carte commence au formulaire |
| `carte-allumee-1440.jpg` | page générale remplie (essai local, non publié) | « Choisir un créneau », la phrase des créneaux, **« Prévenir le Dr Fogue sur WhatsApp »**, puis « Ou préparez une demande » |
| `carte-allumee-390.jpg` | même état, 390 px | les deux boutons tiennent sur toute la largeur, aucun débordement |
| `carte-partielle-1440.jpg` | une page pour Africa Médical seulement, lieu = Mbouda | **pas de bouton** ; une phrase encadrée dit que ce lieu ne réserve pas en ligne et renvoie au formulaire |

Mesures relevées par le même script : hauteur du bouton **47 px** (1440) et **42 px** (390), **0 erreur
console**, **0 débordement horizontal**. La flèche « nouvel onglet » est un SVG inline : le glyphe `↗` ne
se rend pas dans toutes les polices, et une icône manquante laisserait un bouton muet.

Pour rejouer : `tools/qa/verify_booking_dom.mjs` (DOM simulé, quatre états, hors dépôt) et les captures
ci-dessus.
