# LA LIGNE OPTIC — notes de construction (24/09/2026, nuit)

**Client** : **La Ligne Optic** — opticienne à **Akwa, boulevard de la Liberté**, Douala.
Répond **« Ok merci beaucoup vyni »** à 21:04 au message du lot 4 ; King annonce le lien à 21:35.
**Aperçu** : `demos/concept-laligne-v1.html` ← gabarit `demos/laligne-v1.tpl.html` + `demos/build_laligne.py`
→ déployable dans `hosting/previews/laligne/` (`index.html` + `og.jpg`).
**Contrôle approfondi** : `clients/la-ligne/dossier.md` · **inspiration** : `clients/la-ligne/inspiration.md`.

---

## 1 · Le Design Read, et la décision qui commande tout le reste

> Reading this as: a **drawn page for a face-first practice** — chalk paper, graphite ink, one laque red —
> where **nothing is photographed**, because the practice has never published a photograph and we will not
> fake one. Every image is a line drawing, and the drawing *is* the service (leur mot : **visagiste**).

**Dials** : VARIANCE **6** · MOTION **5** · DENSITY **4** — l'atelier calme, l'exact contraire de la page
Cinq Sens construite la veille (affiche, magasin, cinq couleurs qui crient). C'est assumé et écrit au
registre d'unicité.

## 2 · Ce qui a décidé de la forme de la page

| Fait du contrôle | Conséquence de construction |
|---|---|
| 4 services publiés, et rien d'autre : consultation · réfraction · visagiste · conseil | la section 01 prend **ces quatre mots**, dans cet ordre, et explique chacun au patient |
| « **Visagiste** » est le seul mot qui les distingue | le service devient **une expérience** : cinq formes de visage, cinq lignes de monture, chacune son message WhatsApp |
| **Aucune photo** publiée | la page est **dessinée** (SVG) — et la vignette du lien est un dessin, elle aussi |
| **Aucun horaire**, aucun prix, aucune marque, aucun avis | section 04 : « quatre choses qui se règlent en une réponse » — l'honnêteté devient la preuve |
| Titulaire **JOUNGO Line Chantale**, inscription **025/2017** | nommée **une fois**, en pied de page, avec sa qualité ; le numéro d'inscription reste **dans les données structurées** (règle DM OPTIC) |
| Opticien ≠ ophtalmologue | la FAQ l'écrit : la réfraction est un acte d'opticien, l'examen des yeux reste le travail de l'ophtalmologue |

## 3 · Écran par écran

1. **Le premier écran** — « Votre visage d'abord. La monture ensuite. » À droite, un **dessin qui se
   trace** : la règle du regard, un visage, la monture par-dessus (SVG, `stroke-dashoffset`, 5 traits).
   Trois faits sous le texte : opticienne inscrite depuis 2017 · le conseil de visagiste · Akwa.
2. **Les quatre gestes** — une liste à filets (pas des cartes) : chacun dit ce qu'il veut dire **et ce que
   vous pouvez dire en arrivant**.
3. **Le visage d'abord** — cinq onglets radio (ovale, rond, carré, cœur, oblong), **sans JavaScript** :
   `:checked` fait tout. Chaque panneau : le visage dessiné, la ligne conseillée, l'explication, ce qu'on
   évite, et **son** message WhatsApp (la forme est nommée dans le message — la visagiste sait à quoi elle
   répond). Deux notes ferment la section : c'est du **style**, pas un examen ; la photo **reste dans la
   conversation**.
4. **Comment ça se passe** — quatre temps, de « vous écrivez » à « vous repartez avec la suite claire ».
   Aucun délai promis, aucun prix annoncé.
5. **Quatre choses qui se règlent en une réponse** — tarif, marques, horaires, votre monture actuelle :
   on explique **pourquoi** elles ne sont pas sur la page, et on renvoie au WhatsApp. C'est la bande de
   preuves de Felix Gray, retournée : ici la preuve, c'est de ne rien affirmer qu'on ne sache.
6. **Six questions** (`FAQPage`, mot pour mot) · **deux gestes** (WhatsApp, appel) · copier le numéro ·
   fiche `.vcf` · barre d'action fixe sur téléphone.

## 4 · Mouvement (budget §9)

Trois mouvements, pas un de plus : le **tracé** des dessins du premier écran, les **révélations** au
défilement (IntersectionObserver, **jamais** d'écouteur de défilement), et les transitions d'onglets du
navigateur. Un `@media (prefers-reduced-motion:reduce)` arrête les deux premiers ; sans JavaScript, la
ligne est **entière** et tout le contenu est visible.

## 5 · Les contrôles

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** sur **314 passages** de texte (desktop et mobile) |
| `audit_a11y.py --strict` | **0 faute, 0 avertissement** — il a attrapé un saut de niveau **h2 → h4** en pied de page (corrigé en `h3`) |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `check_inline_js.py` | **rc 0** — 4 blocs compilés |
| `audit_aeo.py` | ✓ `Optician` + `FAQPage` (6 questions, mot pour mot) · `noindex` voulu |
| `audit_images.py` | 0 faute — 0 image, et c'est le sujet |
| `node tools/qa/test_laligne_page.mjs` | **52/52** |
| Poids | **79 Ko**, douze liens WhatsApp, **zéro image à charger** |

**Trois choses que le test protège et qu'aucun audit ne voit** : la page n'a **pas un seul `<img>`** ;
le numéro d'inscription à l'Ordre n'existe **que** dans les données structurées ; la titulaire est nommée
**une fois par langue** (le premier jet de l'assertion comptait une seule fois pour les deux langues — le
test avait raison, la page aussi).

**Un bug attrapé par le test, pas par les audits** : la région vive annonçait « la page est maintenant en
français » **au moment de passer en anglais** (arguments inversés dans `setLang`). Invisible à l'œil,
invisible aux audits — visible pour un lecteur d'écran.

## 6 · Ce qu'on ne dit pas, et pourquoi

- **Aucun horaire** : aucun annuaire ne les donne. La page dit où les trouver (la conversation).
- **Aucune photo, aucune marque, aucun prix, aucun avis** : rien n'a été publié.
- **Aucun repère de quartier** inventé (« en face de… », « à côté de… ») : nous n'en avons trouvé aucun.
- **Aucun acte médical** attribué au cabinet, jamais.
- **Aucune promesse** de délai, de classement ou de résultat.

## 7 · Avant d'envoyer le lien (dans cet ordre)

1. **Déployer** `hosting/previews/laligne/` — **le dossier entier** (`index.html` **et** `og.jpg`) ;
2. `python3 demos/build_laligne.py --url https://<adresse>` puis **redéployer** : `og:url` et `og:image`
   se remplissent là, pas avant ;
3. **ouvrir sur un téléphone** : FR par défaut, bascule EN, le dessin qui se trace, les cinq onglets qui
   changent de panneau **sans JavaScript**, un vrai WhatsApp pré-rempli (683 651 108), aucun débordement ;
4. envoyer le message de `sales/Send-LA-LIGNE-2026-09-24.md` §1, après la carte du lien.
