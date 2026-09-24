# Cavisa Optique — notes de construction

**Qui** : Cavisa Optique, Douala · **M. DONGMO Jean René** · WhatsApp **+237 699 95 90 52** (vérifié par King le 24/09, profil « CAVISA OPTIQUE »).
**Pourquoi maintenant** : King a écrit le 24/09 à 12:16 — *« Je finalise l'aperçu interactif spécialement adapté à Cavisa Optique… lien d'accès direct ici sur WhatsApp d'ici 1h »*. M. Dongmo a répondu « Ok » à 12:23.
**Fichiers** : `demos/cavisa-v1.tpl.html` (le gabarit) → `demos/build_cavisa.py` → **`demos/concept-cavisa-v1.html`** + **`hosting/previews/cavisa/`** (`index.html` + `og.jpg`).
**Références et Design Read** : `clients/cavisa/inspiration.md` (à lire avant de retoucher la page).

---

## 1 · Les décisions, et pourquoi

### Dials
**VARIANCE 5 · MOTION 4 · DENSITY 4.** Le marché est un téléphone, souvent en 3G ; le patient hésite à pousser la porte. Décalage mesuré, rien de cinématique, une idée par écran.

### La couleur — Black & Tan (§6.2, famille du pool rotation, **jamais utilisée dans la registre**)
| Rôle | Valeur | Contraste mesuré |
|---|---|---|
| Sol (nuit chaude) | `#14100D` | — |
| Bande / cartes | `#1C1611` · `#221A13` | — |
| Texte | `#F7EDE1` | **15,9:1** sur le sol |
| Texte secondaire | `#E6D6C5` / `#C3AE9A` | 8,6:1 et plus |
| **Accent unique** (filets, numéros, italiques) | `#E9A544` | **8,9:1** sur le sol |
| **Vert WhatsApp**, réservé aux envois | `#0C7F41` (blanc dessus : **5,1:1**) | AA ✓ |

Aucune ligne opticien de la registre n'est sombre et chaude (Univers = papier chaud clair, Cristallin = papier froid, L'Opticien = crème). Le sombre n'est pas un caprice : c'est **le comptoir éclairé vu du trottoir**, et ça se justifie dans `inspiration.md` §3 (à Douala, les opticiens en ligne sont des cartes de visite claires).

### La typographie — l'en-tête d'abord (§23.4)
**Instrument Serif** (display, 400 + italique, tenu serré) sur **Karla** (corps 400/500/700). Aucun opticien de la registre n'utilise ce couple. Chargement : `Instrument+Serif:ital@0;1` + `Karla:wght@400;500;700`, `display=swap`, chaîne de repli identique à la maison (Georgia / system-ui).

### La mise en page — « la promenade au comptoir »
hero (texte + **panneau-verre**) → 4 cartes (montures · verres sur ordonnance · réparation & ajustage · lunettes de soleil) → **parcours en 4 étapes numérotées** sur bande surélevée → ordonnance + « ce qu'on vous demandera d'apporter » → **encadré « Aucune surprise avant de vous déplacer »** → **carte claire « Deux lignes, et la page est complète »** → 4 accordéons → la porte WhatsApp → pied de page §20 (4 blocs + bandeau) + **barre du bas sur téléphone**.

Transpositions assumées (détaillées dans `inspiration.md`) : la structure *promesse → preuves → chemin → réponse au coût → FAQ* vient de Superpower, **avec zéro chiffre** ; le « What to expect » de Warby Parker devient **« ce qu'on vous demandera d'apporter »** ; le bloc de paiement devient **« aucune surprise »**.

### Le « star of the show » et sa rime (§23.3)
**Le verre** : la photo du hero est encadrée comme un verre (anneau ambre + reflet en biais + halo chaud). Un composant de ce verre **revient à trois endroits** : la puce du hero, les numéros d'étape, et — en pointillé — la carte claire. C'est l'objet du métier : rien de décoratif n'a été ajouté (aucun point d'état, aucune pastille, cf. §3.4).

### La copie — quatre engagements, aucun chiffre
La page promet ce qu'une boutique peut tenir : **le prix, le délai, la réparabilité et la liste de ce qu'il faut apporter sont donnés dans la conversation WhatsApp, avant le déplacement**. Elle ne promet **aucun examen de la vue** (non vérifié), **aucun prix affiché**, **aucun délai affiché**, **aucune note**, **aucun avis**, **aucune adresse**, **aucun horaire**. L'ordonnance est traitée comme un fait de parcours (« les verres se montent dessus »), pas comme un acte médical.

---

## 2 · Les contrôles, et leurs résultats exacts (24/09)

| Porte | Commande | Résultat |
|---|---|---|
| Contraste / structure | `python3 tools/qa/audit_html.py demos/concept-cavisa-v1.html` | **0 faute** sur 208 passages de texte (desktop **et** mobile) |
| Accessibilité | `python3 tools/qa/audit_a11y.py --strict …` | **rc=0**, 0 faute A/AA, 0 avertissement (INFO : barre fixe → rien ne passe dessous, vérifié par le `padding-bottom` du `body`) |
| Images | `python3 tools/qa/audit_images.py …` | rc=0 — *0 image externe : les deux photos sont embarquées en base64*, et **aucune métadonnée** (vérifié : `-strip`, pas d'EXIF, donc pas de GPS) |
| JavaScript inline | `python3 tools/qa/check_inline_js.py …` | **rc=0**, 4 blocs compilés |
| Contrat de page | `python3 tools/qa/audit_page.py …` | **0 constat, 0 bloquant** |
| Hero | `python3 tools/qa/audit_hero.py …` | 0 faute, 0 avertissement |
| AEO / données structurées | `python3 tools/qa/audit_aeo.py …` | 0 faute (`Optician`, `FAQPage`, `PostalAddress`, `ContactPoint`, `City`) |
| **Comportement (le vrai JavaScript)** | `node tools/qa/test_cavisa_page.mjs` | **28 assertions vertes** — bascule FR/EN, `aria-pressed`, messages WhatsApp dans la bonne langue, `alt` des images, `localStorage`, région vive, et **3 chemins de secours du mouvement** (API absente / script qui plante / mouvement réduit) |
| Balayage mécanique (`design/MOTION.md` §6) | greps | `transition:all` 0 · `ease-in` 0 · `scale(0)` 0 · `animation:` 0 · animations de `gap` retirées · hover derrière `(hover:hover) and (pointer:fine)` ×2 · `.btn`/`.lang`/`.cardlink` ont leur `:active` |
| Em-dash | grep | **0** dans les chaînes anglaises |

**Poids** : page **216 Ko** (dont 162 Ko de base64 pour les deux photos : 77 Ko et 44 Ko avant encodage) — un concept « ~1 Mo acceptable » (§13), mais la moitié est ici, pour un téléphone en 3G.

### Les photographies — refaites le 24/09 après le verdict de King
**Verdict :** *« elles font beaucoup année 90, Douala est bcp plus moderne »*. Les deux images ont été
régénérées en direction 2026 : **boutique contemporaine** (étagères chêne + noir mat, éclairage LED encastré,
comptoir en verre, sol béton ciré, grandes vitrines, plantes) et **salle d'examen à équipement numérique**
(réfracteur avec écran, panneau lumineux, mur chêne). Le hero est un plan taille **au miroir** : la cliente
essaie une monture, l'opticien guide — le cercle du miroir double le motif du verre de la page.
Ce qui a changé dans le builder (`demos/build_cavisa.py`) : **recadrage au centre** (`-resize ^ -gravity
center -extent`) au lieu des décalages écrits en dur — une photo se suit, l'autre casse.
Rappel : ce sont **des mises en situation générées**, écrit sous chacune, à remplacer par les vraies photos
de la boutique dès que M. Dongmo en fournit.

### Ce qui n'a PAS pu être fait dans le bac — écrit tel quel, jamais coché à tort (§13)
- **Console navigateur sans erreur (Chromium, EN/FR, 390 px)** : **NON EXÉCUTÉ** — pas de navigateur dans le bac. Substitut : `check_inline_js` (les 4 scripts compilent) + `test_cavisa_page.mjs` (28 assertions sur le vrai JavaScript).
- **Capture 1280×800 du hero → `demos/shots/`** : **NON EXÉCUTÉE** (pas de navigateur). À faire sur la machine de King : `node tools/video/capture.mjs --mode hero` puis recadrer en 1200×630 si l'on veut une vignette *de la page* au lieu de la photo du hero.
- **Maquette laptop + téléphone** : **NON EXÉCUTÉE**, même raison.
- **Débordement horizontal à 390/360 px** : **NON MESURÉ** (pas de navigateur). Ce qui est en place : colonne unique sous 860 px, `img{max-width:100%}`, `flex-wrap` sur les rangées de boutons et de puces.
- **Lecteur d'écran (NVDA/TalkBack) et zoom 200 %** : **NON EXÉCUTÉS** — protocole prêt dans `tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`, à passer sur un vrai téléphone.
- **Goût, hiérarchie réelle, « squint test » visuel** : **NON MESURÉS**. Deux marches-personas écrites, à revalider à l'œil :
  - *parent à l'étranger* qui paie des lunettes pour un proche → un bouton vert, un message déjà écrit, page en anglais s'il le souhaite ;
  - *patient anxieux et économe* → l'encadré « aucune surprise » répond avant le déplacement ; aucune promesse de prix sur la page.
- **Photos** : générées (mises en situation) puis **relues à l'œil** — pas de texte, pas de logo, pas de filigrane lisible, aucun visage caricatural. Ce sont **des illustrations** : la légende sous chacune le dit, et invite à les remplacer par les vraies photos de la boutique.

---

## 3 · Déployer, et envoyer

```bash
python3 demos/build_cavisa.py     # regénère la page ET le dossier de déploiement
```
Le dossier **`hosting/previews/cavisa/`** contient `index.html` (autonome, 279 Ko) et `og.jpg` (1200×630). Il se déploie tel quel (Netlify Drop, Vercel, n'importe quel hébergeur statique).

1. Déployer → relever l'adresse réelle.
0. **DÉCISION DE KING (24/09) : on ne redéploie pas maintenant.** Le redéploiement se fera **une seule
   fois**, quand M. Dongmo aura dit **les changements qu'il veut**. Ce redéploiement-là emportera tout d'un
   coup : ses informations (adresse, horaires, photos), la vignette du lien (`og:image`) et les photos 2026.
   Conséquence à assumer : tant que ce déploiement n'a pas eu lieu, le lien déjà envoyé s'affiche **sans
   vignette** — c'est le prix d'un seul redéploiement au lieu de deux.

2. **Décommenter le bloc `og:image` / `og:url`** en tête de `demos/cavisa-v1.tpl.html`, y coller l'adresse, relancer le builder **et redéployer** — sinon le lien s'affiche chez Cavisa comme une carte grise sans vignette (§20.7). *(Les deux balises sont commentées volontairement : WhatsApp ne résout pas les URL relatives, on ne peut donc pas les écrire avant de connaître l'adresse.)*
3. Ouvrir le lien **sur un téléphone**, la nuit et en plein soleil (§24.3.5), puis envoyer **le lien seul**, sans pièce jointe, à M. Dongmo — c'est King qui envoie, jamais nous.

**Quand il répondra « c'est bien »**, les trois choses à demander, dans cet ordre :
1. **ses horaires d'ouverture** et **son adresse exacte** (la carte « à compléter » de la page les attend) ;
2. **ses vraies photos** (elles remplacent les deux illustrations) — et **pas** avant qu'il les propose : on ne réclame pas un document qu'on n'a pas ;
3. **trois vérifications de contenu** : fait-il des contrôles de la vue ? annonce-t-il le prix dans la conversation WhatsApp ? a-t-il des lunettes de soleil en boutique ?

**À la mise en ligne chez lui** (le jour où ce n'est plus une maquette) : retirer `noindex,nofollow`, écrire `og:url`/`og:image`, et remplacer la ligne « Maquette préparée par AMK… » du bandeau par la vraie signature. **Rien d'autre ne change** : la page est déjà bilingue, accessible AA, et ne contient pas un seul chiffre inventé.
