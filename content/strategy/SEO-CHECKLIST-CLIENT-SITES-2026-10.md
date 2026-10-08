# SEO — liste de contrôle pour les sites clients (tirée de amk-cm, 08/10/2026)

> **Origine.** King (08/10) : « fais tout ce qu'il faut pour améliorer notre site ; prends ça comme un apprentissage
> pour ce qu'on fera pour nos clients », avec le *SEO Starter Guide* de Google Search Central. Ce fichier range
> ce que le guide dit, ce qu'on a vérifié sur `amk-cm`, ce qu'on a changé, et **ce qu'on refait sur chaque site
> client**. Journal complet : `site/SEO-REVIEW-2026-10-08.md` §8. Outils : `tools/seo/`, `tools/qa/`.

## 0 · Ce qu'on peut promettre à un client, et ce qu'on ne peut pas

Le guide le dit lui-même : *aucun secret ne place un site premier*, un changement met de quelques heures à plusieurs
mois, il faut attendre **quelques semaines** avant de juger. Donc, dans une offre : « nous préparons le site pour
qu'il soit **trouvable et compris** par Google ; nous mesurons avec Search Console ». **Jamais** « première page »,
jamais un volume de recherche, jamais un délai de classement. (Même règle que `RULE-CREDENTIAL-CLAIMS` : pas de
chiffre sans source.)

## 1 · Ce que le guide demande → ce qu'on vérifie → verdict amk-cm au 08/10

| Le guide dit | On vérifie (commande ou geste) | amk-cm avant → après |
|---|---|---|
| Google doit voir la page comme l'utilisateur | `view-source` : le texte important est dans le HTML servi, pas seulement après JS ; CSS/JS non bloqués ; **Inspection d'URL** (Search Console) | HTML mélangé EN/FR → **français cohérent dans le HTML statique** (outil `bake_default_lang.py`) |
| Titres de page : uniques, clairs, concis, avec marque et lieu | longueur ≤ ~65 car., un titre par page, même langue que le corps | 96 car. (liste de villes, à tronquer) → 64 car. : « Création de site web école & clinique, Cameroun \| AMK Douala » |
| Meta description : courte, unique, les points utiles | ≤ ~155 car., même langue que la page, pas de liste de villes | 288 car., français + une phrase en anglais, quatre villes → 139 car., une seule langue |
| URLs descriptives | mots lisibles dans le chemin | déjà bon (`creation-site-web-ecole-cameroun.html`) |
| Dupliqués : une page = une URL canonique | `<link rel="canonical">` sur chaque page | présent partout |
| Images : de qualité, près du texte, **alt descriptif** | `audit_images`, `alt` sur toutes les images, poids | alt présents mais **en anglais sur une page française** et jamais traduits → FR + traduits par le JS ; **2,28 Mo de PNG → 0,47 Mo de WebP** |
| Données structurées valides | JSON-LD qui se parse, noms **identiques** partout | **trois noms d'entreprise différents** → un seul, identique à la fiche Google, `sameAs` + `hasMap` vers elle ; `WebSite` ajouté (nom du site dans les résultats) |
| Sitemap : seulement les URLs qu'on veut | pas de page `noindex` dans le sitemap ; `lastmod` vrai ou absent | 2 pages `noindex` volontairement hors sitemap ; `lastmod` seulement là où le contenu a changé |
| Ne pas laisser dans Google ce qui ne doit pas y être | `noindex` sur les pages de travail et **toute page qui porte le nom d'un prospect** | `mitoc.html` (nom d'un vrai prospect, indexable) → `noindex,nofollow` |
| Fiche Google / promotion | profil rempli, avis réels, URL du site dans la fiche | profil lié et vérifié (lien Maps lu), **0 avis**, description à réécrire (voir §4) |
| Search Console | propriété vérifiée, sitemap soumis, export suivi | vérifiée (fichier `google…html`, **à ne jamais retirer du déploiement**) ; export chaque dimanche |

## 2 · Ce que le guide dit de NE PAS faire — on n'y perd pas de temps

Balise meta *keywords* (Google ne l'utilise pas) · bourrage de mots-clés (contraire aux règles de spam) · mots-clés
dans le nom de domaine (effet quasi nul) · **longueur minimale ou maximale du texte** (il n'y en a pas) · ordre ou
nombre de titres `h1…h6` (bon pour les lecteurs d'écran, sans effet sur le classement) · « pénalité de contenu
dupliqué » (inefficace, pas une sanction) · **E-E-A-T n'est pas un facteur de classement** · PageRank seul. Donc :
on ne vend pas « optimisation des balises keywords » à un client, et on ne réécrit pas un site pour « avoir 1 500 mots ».

## 3 · La liste, dans l'ordre, pour un site client bilingue (à faire avant la livraison)

1. **Une langue par défaut, écrite dans le HTML.** Choisir avec le client la langue des gens qui cherchent (au
   Cameroun : souvent le français ; Buea/Limbé : souvent l'anglais). `python3 tools/seo/bake_default_lang.py page.html fr`
   puis, à la main : `<html lang>`, boutons FR|EN (`class="on"`, `aria-pressed`), titre, description, `og:*`.
   Test : `node tools/qa/test_amkcm_lang.mjs page.html`. **Limite connue** : une page à bascule JS n'a qu'une URL ; pour
   se classer aussi **en anglais**, il faut une vraie URL `/en/` (voir §5).
2. **Titre et description** écrits à la main, dans la langue du corps (§1).
3. **Un nom d'entreprise, partout identique** : site, JSON-LD, fiche Google, pied de page. Le copier de la fiche.
4. **JSON-LD** : `ProfessionalService`/`LocalBusiness` + `@id`, `sameAs` (fiche Google, Facebook…), `hasMap`,
   `areaServed` (seulement ce qu'on dessert **vraiment**), `WebSite`. Pas de `price`/`priceRange` si le site ne
   montre pas de prix. Pas d'`openingHours` ni d'`aggregateRating` sans données réelles.
5. **Images** : WebP (`Pillow`, qualité ~80), `alt` descriptif dans la langue de la page, héros avec
   `fetchpriority="high"`, le reste `loading="lazy"`.
6. **Pages de travail et pages de prospects** : `noindex,nofollow` ; hors sitemap.
7. **Sitemap + robots.txt** ; le fichier de vérification Search Console **dans le paquet de déploiement**
   (`hosting/build_site_zip.py` l'inclut — une ancienne liste l'aurait oublié).
8. **Affirmations** : chaque chiffre, ville de projets, ancienneté ou disponibilité (« 99,9 % ») doit avoir une
   source au dépôt (`RULE-CREDENTIAL-CLAIMS.md`). Une zone *desservie* (à distance) n'est pas une zone *où l'on a des clients* : ne pas écrire l'une pour l'autre.
9. **Contrôles** : `audit_html`, `audit_a11y --strict`, `check_inline_js`, test de bascule, puis `view-source` sur la page EN LIGNE.
10. **Après mise en ligne** : Inspection d'URL → « Demander une indexation » pour chaque page changée ; sitemap
    soumis ; une note datée dans le journal ; **jugement à 30 jours**, pas avant.

## 4 · Fiche Google (Business Profile) — ce qu'on fait pour AMK, et pour chaque client

- Relever la fiche **telle que Google la montre** (nom, catégorie, site, téléphone, horaires, avis) et la comparer au site.
- **Aucune superlative non prouvée** dans la description (« premier », « meilleur ») : même règle que pour le site.
- **Avis : seulement de vrais clients, avec leur accord.** Zéro avis aujourd'hui sur la fiche AMK ; le premier doit
  venir du premier site livré. Jamais d'avis de complaisance (règle de Google, et risque de suppression de la fiche).
- Remplir : services, horaires **réels** (tous les jours, pas seulement un), lien de réservation = WhatsApp, photos
  de travaux réels (avec accord du client), publications régulières.
- Le lien **site → fiche** (`sameAs`, `hasMap`) et **fiche → site** doit exister dans les deux sens.

## 5 · Ce qui reste, et que le HTML seul ne règle pas

- **Contenu** : le guide le dit — c'est le facteur n° 1. Les pages métier (école, clinique) sont les seules qui ciblent une
  intention précise. Une page de plus n'a de sens que s'il y a **un fait vrai à y mettre** (pas de pages « quartier » en
  série). Candidat : une page opticiens, **quand** la vocation de l'accueil est tranchée.
- **Anglais** : vraies URLs `/en/` + `hreflang` = seule façon sérieuse de servir « website design Buea ».
- **Liens entrants** : « Site par AMK » dans le pied de page des sites clients (accord du client), annuaires, fiche Google.
- **Prix** : retirer le prix retire aussi l'angle « prix site internet Cameroun » (`KEYWORDS-2026-09-22.md` supposait qu'AMK était seul à afficher un chiffre). La FAQ « Combien coûte… » reste, avec une réponse sans chiffre.
- **Mesure** : 1 impression sur les 7 derniers jours (export chaque dimanche, `ops/TOOL-SCAN.md`). Aucune conclusion avant ~21/10 (seuil du contrôle à 30 jours : ≥ 20 impressions et ≥ 2 clics).
