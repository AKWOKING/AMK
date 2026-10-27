# La carte de rendez-vous, dans les deux états — 27 octobre 2026

Ces trois images sont des **captures réelles** : Chromium headless (`tools/video/install.sh`), page servie en
local, carte `#appointments` cadrée. Ce ne sont pas des reconstitutions, contrairement aux aperçus du hero.

| Fichier | État | Ce qu'on doit y voir |
|---|---|---|
| `carte-eteinte-1440.jpg` | `bookingUrl = ""` (aujourd'hui) | aucun bouton de réservation, la carte commence au formulaire |
| `carte-allumee-1440.jpg` | `bookingUrl` rempli (essai local, non publié) | le bouton « Choisir un créneau », la phrase des créneaux, puis « Ou préparez une demande » |
| `carte-allumee-390.jpg` | même état, 390 px | le bouton tient sur toute la largeur, aucun débordement, la flèche se rend |

Mesures relevées par le même script : hauteur du bouton **47 px** (1440) et **42 px** (390), **0 erreur
console**, **0 débordement horizontal**. La flèche « nouvel onglet » est un SVG inline : le glyphe `↗` ne se
rend pas dans toutes les polices, et une icône manquante laisserait un bouton muet.

Pour rejouer : `tools/qa/verify_booking_dom.mjs` (DOM simulé, hors dépôt) et les deux captures ci-dessus.
