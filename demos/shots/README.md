# demos/shots/ — captures et maquettes d'envoi

**Règle** (`AMK-DESIGN-SKILLS.md` §13 et le Concept Production Standard) : chaque page envoyée à un
prospect reçoit une capture hero 1280×800 (après le reveal), une capture mobile 390 px, et une
maquette ordinateur + téléphone quand on envoie. Usage public de captures nommées seulement après
accord du client ; tant qu'il n'y a pas d'accord, le contenu public reste **nameless** (Nova /
Little Oaks / Crestwood).

**État au 24/10/2026 — le dossier est vide de captures, volontairement.** Les maquettes et captures
des prospects retirés (`mockup-secondary`, `mockup-clinic`, `mockup-mitoc`, `mockup-skye`,
`mockup-yaks`, `mockup-opticien`, `mockup-afriquelabo`, `mockup-jempo`, `mockup-labethanie`,
`oracare-*`) ont été retirées avec leurs dossiers clients. Ce qui reste ici : cette règle, et les
prochaines captures.

**Ramener une capture :** `git log --oneline -- demos/shots/` puis
`git checkout <commit>^ -- demos/shots/<fichier>`.

## Format et nommage

| Fichier | Usage |
|---|---|
| `<slug>-concept.png` | master 1280×800, après reveal |
| `<slug>-mobile.png` | 390 px de large |
| `<slug>-wa.jpg` | copie d'envoi WhatsApp, 1600×900, Lanczos, q88 — elle passe la recompression de WhatsApp, le master reste pour l'impression |

Regénérer une copie WA depuis le master :

```bash
convert <slug>-concept.png -resize 1600x900^ -gravity center -extent 1600x900 -quality 88 <slug>-wa.jpg
```

## Comment capturer

`tools/shots/` porte la chaîne (Chromium embarqué via `@sparticuz/chromium`), `tools/video/capture.mjs`
la commande. Envoi : **l'image d'abord**, le texte ensuite, jamais les deux dans le même message.

## À faire

Aucune capture n'est due pour un prospect. La prochaine est due pour **DM Optique** si King veut une
maquette d'envoi de la page en production, et pour **Le Cristallin** quand le gel sera levé
(`hosting/previews/README.md`).
