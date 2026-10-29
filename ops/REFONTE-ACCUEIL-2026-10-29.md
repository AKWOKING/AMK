# L'accueil AMK — la passe du 29/10, et les trois directions d'où elle vient

```
Objet     refonte de l'accueil de amk-cm.vercel.app, à partir d'une référence envoyée par King
Référence capture « NEXORA » (barre claire, héros photo, titre 3 lignes, rangée de 4 preuves)
            + l'affiche AMK (« Turn Your Ideas », encre + ambre)
Règle     la grammaire de la référence, NOS couleurs (encre #0F172A, ambre #F59E0B, papier #F7F6F2)
État      construit, mesuré, non déployé. La production attend le feu vert de King.
```

---

## 0 · Ce que King a demandé, dans ses mots

> « the AMK website, I want something like what is in the screenshot but still with our brand colors »

La référence est une page d'agence : barre de navigation claire, grand héros sur une photo de
paysage, un titre en trois lignes dont la dernière partie porte l'accent, un bouton, puis une rangée
de quatre preuves sous le pli. **Ce qui suit reprend cette grammaire et rien d'autre** : ni la palette
bleu-gris, ni le nom, ni la photo.

Ce qui n'était pas dans la demande et qui a été tranché ici, parce qu'il fallait bien :

| Question | Réponse retenue | Pourquoi |
|---|---|---|
| Garder le bilingue par bouton (`data-en`), ou deux pages ? | **deux pages** : `/` et `/en/` | une page dont le texte dépend de `localStorage` n'est pas indexable en anglais ; la version `/en/` existait déjà et servait un HTML français |
| Garder le sélecteur de niche du héros (« Patients » / « Écoles ») ? | **retiré** | le titre visible changeait selon l'onglet actif : sans JS, la moitié des visiteurs lisait un titre qui ne les concernait pas |
| Garder la bande de chiffres (24 h · 100 % · 6 concepts) ? | **retirée** | trois de ces quatre chiffres ne prouvaient rien, et « 100 % à vous » se dit mieux dans la liste des livrables |
| Garder le bandeau défilant ambre ? | **retiré** | c'est un signe de site généré, et il ne vendait rien |
| Changer la police (Outfit) ? | **non** | c'est la police maison, et elle ne se chargeait même pas (voir §2) |

---

## 1 · Les trois directions, avant de construire

`AMK-DESIGN-SKILLS.md` §19.3 impose d'explorer trois directions avant tout build, et de n'en garder
qu'une. Les trois ont été écrites, la troisième a été choisie.

### A · « Le dossier de presse » — éditorial, papier, colonnes
Un accueil qui ressemble à un journal d'entreprise : grand titre serif, filets, deux colonnes, la
preuve en pleine largeur. **Ce qu'il aurait donné** : une allure très différente des concepts clients,
donc une démonstration de craft. **Ce qu'il coûtait** : l'audience est un gérant de cabinet ou de
boutique qui lit sur un téléphone en 3G ; un serif éditorial fin sur 390 px se lit mal, et le dépôt
interdit le serif par défaut. **Écarté.**

### B · « L'affiche » — encre et ambre, comme le post Facebook
L'accueil reprend l'affiche que King a déjà en main : fond encre, titre énorme en deux couleurs,
quatre pictogrammes, bandeau « Let's build something great ». **Ce qu'il aurait donné** : une
cohérence immédiate entre le post et le site. **Ce qu'il coûtait** : l'affiche est un format
publicitaire (un cadre, une accroche, un CTA), pas une page qui doit répondre à « combien », « en
combien de temps », « qui d'autre ». Et un héros en encre pleine largeur fait tomber le dominant à
plus de 85 % sur le premier écran. **Écarté**, mais sa palette est gardée.

### C · « La référence, avec nos couleurs » — **retenue**
La grammaire de la capture, peinte avec les jetons AMK : barre de papier, héros photographique,
titre en trois lignes, un bouton ambre, une rangée de quatre preuves, puis le corps de page tel quel.
**Pourquoi celle-là** : c'est la direction que King a nommée, elle tient sur 390 px sans effort, elle
laisse la preuve (DM OPTIQUE, les six concepts) au centre, et elle corrige au passage les trois
défauts mesurés du premier écran (§2).

**La règle 60-30-10, mesurée après coup** (`tools/qa/audit_palette.py`, capture 1440) :

| Écran | Dominant | Secondaire | Accent | Verdict |
|---|---|---|---|---|
| Héros (photo + voile encre) | 74,4 % | 22,2 % | 3,4 % (bouton) | ✓ |
| Bande des quatre preuves | papier clair | fiches | ambre des icônes | ✓ |

---

## 2 · L'audit d'avant, mesuré et non raconté

`python3 tools/qa/shot.py site/index.html` sur l'accueil du 29/10 au matin :

```
TOTAL 4 P1 · 11 P2 · 6 P3 — ROUGE
```

| Défaut | Ce que ça donnait | Correction |
|---|---|---|
| **P1 console + P2 réseau** : Google Fonts injoignable | Outfit ne se chargeait pas : la page s'affichait dans la police système, et chaque audit comptait une requête tierce en échec | **Outfit servi depuis `site/fonts/`** (5 fichiers woff2, 71 Ko au total, `font-display:swap`) |
| **Le `<h1>` mesurait 18 px** | `.seo-h1` était le vrai titre ; le titre visible était un `<h2>` de panneau, caché pour qui n'ouvrait pas le bon onglet | **un seul `<h1>`**, 62 px, une phrase, jamais caché |
| **La barre de navigation n'avait pas de fond** | Sur le corps crème, la marque et les liens restaient blancs et gris clair : illisible dès qu'on quittait le héros | barre de **papier** avec filet, encre sur papier, `position:sticky` |
| **1 × P2 contraste** : la pastille « FR » | encre sur encre, 1:1 mesuré | pastille ambre, encre dessus |
| **Le `<h1>` passait sur trois lignes** | plafond du §7 : deux lignes | titre raccourci et taille ramenée à 62 px : **deux lignes** |

Après la passe, toujours `shot.py` :

```
TOTAL 0 P1 · 0 P2 · 6 P3 — VERT
```

Les six P3 restants sont trois constats structurels qui existaient avant et qui ne se corrigent pas
en une passe : 13 sourcils pour 11 sections, 31 tailles de texte distinctes (le site entier, pas
l'accueil), et le lien d'évitement qui vit hors cadre (c'est son métier).

---

## 3 · Ce qui a changé, fichier par fichier

| Fichier | Ce qui y est |
|---|---|
| `site/index.html` | en-tête refait, héros remplacé, rangée de quatre preuves ajoutée, bande de chiffres + marquee + « défilé » retirés, flèches et coches dessinées en SVG, liens de police locaux |
| `site/accueil-2026-10-29.css` **(neuf)** | la passe entière : jetons, barre, héros, bande, corps de page, petits écrans, `prefers-reduced-motion` |
| `site/fonts/*.woff2` **(neuf)** | Outfit 400/500/600/700/800, latin, servi par le site |
| `site/img/hero-douala-dusk-1600.webp` · `-860.webp` **(neuf)** | le fond du héros : le Wouri au crépuscule, 58 Ko et 23 Ko |
| `site/img/og-cover.jpg` | **re-capturé** : l'aperçu de partage montre le nouveau premier écran, pas l'ancien |
| `site/en/index.html` | **régénéré** : c'était un HTML français avec un `lang="en"` |
| `tools/site/build_en_page.py` **(neuf)** | le générateur de la page anglaise (§4) |
| `site/sitemap.xml` | `lastmod` du 29/10 sur `/` et `/en/` |

### Ce qui a été retiré, et pourquoi c'est un gain

1. **La bande de chiffres** (`24 h`, `100 %`, `2`, `6`) : quatre nombres qui ressemblent à des
   preuves. Trois ne prouvaient rien de vérifiable, et le quatrième se dit mieux dans la fiche client.
2. **Le bandeau défilant** (`Écoles · Cliniques · Bilingue · …`) : de la décoration qui bouge.
3. **Le « défilé » et ses trois pastilles flottantes** (`EN|FR`, `WhatsApp d'abord`, `Rapide en 3G`) :
   trois animations en boucle sur le premier écran, pour trois mots déjà écrits dans la rangée de
   preuves.
4. **Les deux onglets de niche** : voir §0.
5. **Le dégradé radial** du héros : il ne servait qu'à meubler le vide à côté d'une capture.

Aucun de ces cinq blocs ne portait une information qu'on ne retrouve pas ailleurs sur la page, en
mieux. C'est le critère : **on ne retire pas pour alléger, on retire parce que la version d'après dit
la même chose plus vite.**

---

## 4 · La page anglaise est maintenant vraiment anglaise

`site/en/index.html` était un export du français : `lang="en"`, un titre anglais, et 1 700 lignes de
texte français. Google recevait donc une page anglaise qui parle français, et le `hreflang` promettait
une version qui n'existait pas.

`python3 tools/site/build_en_page.py` la reconstruit depuis la page française :

1. **chaque nœud visible est remplacé par son `data-en`** — 301 paires, aucune traduction à la main ;
2. le `<head>` est réécrit (titre, description, og, canonical, hreflang, locale) ;
3. le bloc des trois étapes de paiement, qui n'avait pas de paire, est écrit en anglais dans le script ;
4. le sélecteur de langue devient **deux liens** (`EN` / `FR`) : changer de langue change de page ;
5. la **FAQ structurée est reconstruite depuis les `summary` anglais** de la page, pas recopiée du
   français ;
6. les `data-en` / `data-fr` sont retirés : la page n'a plus de bascule, et laisser les paires ferait
   croire le contraire.

Le script **refuse de finir si du français reste dans le corps** (code de sortie 1). Il est
rejouable : la page anglaise se régénère en une seconde après tout changement de la page française.

---

## 5 · Les portes, et ce qu'elles disent

| Porte | Avant | Après |
|---|---|---|
| `shot.py` (1440 + 390, console, contraste, débordement) | 4 P1 · 11 P2 · 6 P3 | **0 P1 · 0 P2 · 6 P3** |
| `audit_funnel.py` | 0 P1 (mesuré sur copie) | **0 P1 · 0 P2 · 1 P3** (« pick up the phone » n'est pas dans sa liste de mots de résultat : c'est un mot de résultat, la liste est plus courte que le français) |
| `audit_hero.py` | ✓ | ✓ (h1 dans le premier écran, premier écran porté par le texte) |
| `audit_a11y.py` | 0 faute A/AA | 0 faute A/AA |
| `audit_html.py` | 0 constat | 0 constat |
| `audit_aeo.py` · `audit_seo.py` | OK | OK |
| `audit_site_amk.py` | **1 ✗** : le nœud du refus n°1 annonçait « 150 000 » là où `data-fr` annonce les trois prix | **0 ✗** |
| `audit_delivery.py site/` | 0 P1 | 0 P1 · 1 P2 (les 8 pages sans ancre mobile, préexistant) |
| `audit_palette.py` | — | héros **60-30-10 ✓** |

La porte de livraison n'était pas verte pour autant : elle gardait un P2 qui ne venait pas du héros, mais
de sept pages de démonstration. Le §7 le traite, et la porte finit à **0 P1 · 0 P2 · 0 P3**.

---

## 6 · Ce qui reste ouvert

| # | Question | Qui tranche |
|---|---|---|
| 1 | **Déployer ou non** : la passe est dans `site/`, la production n'a pas bougé | King, après avoir regardé sur son téléphone |
| 2 | **Un seul libellé de CTA par intention.** Relevé sur la page : « Aperçu gratuit » (2), « Recevoir mon aperçu gratuit » (5), « Recevoir mon aperçu gratuit sur WhatsApp » (1) pour **une seule** intention ; puis un libellé différent par offre (« Ouvrir un site concept », « Ouvrir le site concept », « Parler d'un catalogue », « Prendre le forfait Suivi », « Parler du forfait Croissance »). La loi §4.5 demande un libellé par intention : ici, la même intention porte trois mots. Une ligne de texte à trancher, pas un prix | King, avec la grille des prix sous les yeux |
| 3 | **Trois des six vignettes de concepts datent de septembre** : elles montrent des pages qui ont pu changer depuis. Ce n'est pas faux, c'est vieux | prochain tour, si King veut des vignettes fraîches |
| 4 | **La photo du héros est générée, pas prise à Douala.** Elle ne montre ni client ni personne, donc elle n'invente rien de vérifiable ; reste à décider si on la remplace par une vraie photo de la ville, un soir où quelqu'un est sur le pont | King |
| 5 | **Les six P3 structurels** (sourcils, échelle de texte, crédit « Site par AMK ») se traitent page par page, pas dans une passe de héros | prochain tour |

---

## 7 · La porte de livraison, fermée pour de vrai

`python3 tools/qa/audit_delivery.py site/` refusait de passer sous `--strict` avant cette passe :

```
[P2] D1 · 8 page(s)  sous 641/861/900 px, les liens de section disparaissent sans bouton de menu
[P3] D2 · _headers   aucun fichier `_headers` : ni cache, ni en-tête de sécurité
[P3] D6 · 9 page(s)  `og:image` sans dimensions ni type
```

**D1 — la navigation au téléphone.** Sept pages de démonstration (`clinic-bonaberi`, `mitoc`,
`sample-*`) cachaient leur `.nav-links` sous 640 px **sans rien mettre à la place**. Un prospect qui
ouvre un concept depuis WhatsApp sur son téléphone ne pouvait plus sauter à « Tarifs » ni à « Visite ».
La correction ne demande pas de JavaScript : **les ancres restent visibles, sur une rangée qui défile**,
sous la marque. Coût mesuré : 27 px de hauteur d'en-tête, zéro script, zéro état de focus à gérer — un
menu hamburger aurait demandé les trois.

| Page | Ancre visible à 390 px | En-tête mobile | Débordement |
|---|---|---|---|
| `clinic-bonaberi` · `en/clinic-bonaberi` | 4 / 4 | 80 · 83 px | 0 |
| `mitoc` · `en/mitoc` | 4 / 4 | 91 · 91 px | 0 |
| `sample-secondary` | 6 / 6 | 91 px | 0 |
| `sample-school` | 5 / 5 | 131 px | 0 |
| `sample-maternity` · `sample-polyclinic` | 4 / 4 | 127 · 90 px | 0 |
| `sample-nursery` | 4 / 4 | 93 px | 0 |

Trois détails trouvés en mesurant, et corrigés dans la même passe :

1. **Le crédit « site concept par AMK » du bandeau** sortait de la ligne et poussait la marque à la ligne
   suivante : l'en-tête passait de 80 à 115 px. Il est retiré sous 640 px — le bandeau DEMO du haut porte
   déjà la mention.
2. **`sample-nursery` défilait de 90 px horizontalement au bureau** : `.hero` avait bien `overflow:hidden`,
   mais n'était pas positionné, donc une pastille `right:-90px` prenait la fenêtre pour bloc conteneur.
   `position:relative` suffit. Constat antérieur à la passe, jamais vu parce qu'aucune porte ne mesurait
   ce fichier.
3. **`mockup-hero.html`** est un gabarit à jetons `{{…}}`, en `noindex`, sans lien entrant : il est
   maintenant exclu du contrôle de navigation avec **la même définition de « gabarit » que `audit_aeo`**
   (jetons non remplis, ou `mockup` dans le nom), pour que les deux portes ne se contredisent pas.

**D2 — cache et en-têtes.** `site/vercel.json` : HSTS un an, `nosniff`, politique de référent, permissions
restreintes, et un cache d'une semaine sur images et polices. Rien pour le HTML : Vercel le sert déjà en
revalidation. **À prouver après déploiement** par `curl -I` sur une image et sur l'accueil — un fichier de
configuration n'est pas une mesure.

**D6 — l'aperçu de partage.** Neuf pages déclaraient `og:image` sans dimensions ni type : WhatsApp et
Facebook doivent télécharger l'image avant de savoir la réserver sa place. Les trois balises sont
maintenant écrites avec **les dimensions réelles du fichier** (1200×630 pour les couvertures, 1280×800
pour les captures), lues par Pillow, pas recopiées.

### Les deux erreurs d'instrument de la journée

La porte a accusé deux fois sa propre correction, et les deux fois le défaut était dans l'instrument :

- **Un commentaire CSS n'est pas une règle.** La note qui expliquait la correction
  (« Avant : `.nav-links{display:none}` ») a rallumé le constat qu'elle décrivait. `audit_delivery` retire
  désormais les commentaires avant d'analyser.
- **Une règle de pseudo-élément ne cache pas l'élément.** `.nav-links::-webkit-scrollbar{display:none}`
  (masquer la barre de défilement de la rangée) se lisait comme « la nav est cachée ».

Leçon commune : **un texte de contrôle qui lit du CSS doit distinguer le code du propos sur le code.**

---

## 8 · Le paquet de déploiement

`python3 hosting/build_site_zip.py` → **`amk-site.zip`, 42 fichiers, 5,2 Mo** (7,05 Mo décompressés).

Ce n'est plus une liste écrite à la main. Le script lit chaque page, chaque feuille qu'elle charge, et
chaque `srcset`, puis emporte ce qu'elles référencent. Trois conséquences vérifiables :

| Ce qui manquait au zip du 08/10 | Pourquoi c'était grave |
|---|---|
| `accueil-2026-10-29.css` | un accueil sans feuille de style |
| `fonts/*.woff2` (5 fichiers) | une page en police système |
| `img/hero-douala-dusk-1600.webp` | un héros vide |
| `site/vercel.json` | ni HSTS, ni cache des assets |

Le contrôle, fait **sur le zip décompressé**, pas sur `site/` :

- **42 / 42** fichiers servis en HTTP 200 par un serveur local ;
- **176** références locales (liens, images, `srcset`, `og:image`, `url()` des feuilles) résolues,
  **0 manquante** ;
- accueil, `/en/`, `clinic-bonaberi.html` et `en/mitoc.html` rendus à 390 et 1440 : **Outfit chargée
  depuis le paquet** (4 graisses), `h1` à 62 px puis 36 px, **0 réponse 4xx, 0 erreur console,
  0 débordement**.

### Une dépendance de moins

Cinq pages de démonstration (`clinic-bonaberi`, `mitoc`, `sample-secondary` et leurs jumelles
anglaises) tiraient **Outfit depuis `fonts.googleapis.com`** alors que la police est dans le paquet
depuis cette passe. Elles portent maintenant les mêmes `@font-face` que l'accueil. Sur les six pages
mesurées, plus une seule requête vers un CDN de polices : c'est une panne tierce en moins, et la même
graisse de marque partout.

Restent trois concepts à typefaces propres (Nunito, Montserrat, Archivo + Inter) qui chargent encore
depuis Google Fonts : ce sont des maquettes, elles changent de police **exprès**, et les rapatrier
coûterait 15 fichiers et ~250 Ko. À faire le jour où King les montre dans un réseau qui filtre Google.

**Écart assumé** : le zip ne contient ni `DEPLOY.md`, ni les notes de recherche, ni `mockup-hero.html`
(gabarit à jetons, `noindex`, sans lien entrant) — il contient ce qui doit être servi, rien d'autre.
