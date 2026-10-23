# Badge « source préférée sur Google » — recherche et mise en œuvre, 23 octobre 2026

## 1 · Ce que la fonction est réellement

Un lecteur **connecté à son compte Google** peut désigner des sites comme ses *sources préférées*.
Quand un de ces sites remonte dans **Top Stories**, **AI Overviews** ou **AI Mode**, son lien porte un
badge « preferred ». C'est un **signal personnel** : il ne change rien pour ceux qui ne nous ont pas
choisis, et il ne remplace ni la pertinence ni la fraîcheur.

| Date | Ce qui change | Source |
|---|---|---|
| 02/09/2025 | lancement de Preferred Sources dans Top Stories | blog.google |
| 30/04/2026 | disponibilité **mondiale, toutes langues** | Search Console changelog / SEJournal |
| 27/05/2026 | extension à **AI Overviews et AI Mode** ; Google annonce 345 000 sources choisies | blog.google |
| 20/08/2026 | **bouton intégrable** (2 lignes de HTML) + > 600 000 sources | Search Central, annonce Google |

Ce que Google dit du gain : *les lecteurs cliquent environ **deux fois plus** vers une source
préférée*. C'est une affirmation de Google, pas une mesure indépendante — elle est citée comme telle.

## 2 · Les conditions d'éligibilité (la partie que la plupart des articles sautent)

1. **Domaine ou sous-domaine uniquement**, jamais un sous-dossier : `example.com` et
   `code.example.com` sont éligibles, `example.com/blog` ne l'est pas. → `amk-cm.vercel.app` et
   `dmoptiquesarl.com` sont donc éligibles **par construction**.
2. Le site doit **apparaître dans l'outil de préférences** (`google.com/preferences/source`). Google
   dit de le tester en tapant son domaine dans la recherche de l'outil — **impossible à faire d'ici**
   (il faut une session Google et une interaction).
3. Pour le badge dans **AI Overviews / AI Mode**, le site doit en plus être **inclus dans les
   fonctionnalités d'IA générative de Search Console**.

## 3 · Les trois implémentations possibles

| Méthode | Ce qu'elle fait | Coût réel |
|---|---|---|
| **JavaScript standard** (recommandée par Google) | `<script src="news.google.com/swg/js/v1/publisher.js">` + `<div google-add-preferred-source-btn>` : bouton officiel, traduit, et **retour direct à la page** après le clic | **une iframe `news.google.com` par bouton, chargée à chaque vue** (mesuré par un tiers le 21/08/2026), donc un appel tiers sur nos pages — contraire à notre promesse « rapide en 3G » et à notre absence de trackers |
| **JavaScript avancé** | même SDK, rendu maison, `preferred-sources-control="manual"` + file `PREFERRED_SOURCE` | même appel tiers, plus de code |
| **Deeplink** | un simple lien vers `google.com/preferences/source?q=<domaine>` | **zéro script, zéro iframe, fonctionne sans JavaScript** ; le lecteur confirme sur la page Google (un clic de plus) |

Google autorise explicitement le badge maison : *« You may use your own design or download the Google
button assets »*.

## 4 · Ce qui a été livré, et pourquoi ce choix

**Choix : deeplink + badge maison** (étoile dessinée par nous, aucun logo Google reproduit, textes dans
la langue de la page). Motif : nos deux sites promettent une page légère sur un téléphone en 3G ; un
script et une iframe tiers à chaque vue sont un coût permanent pour un geste de fidélité.

| Site | Portée | Domaine dans le lien |
|---|---|---|
| **AMK** | 3 pages réelles (`index`, `école`, `clinique`) | `amk-cm.vercel.app` (canonique actuel) |
| **DM Optique** | **97 pages** (toutes, FR et EN, y compris les fiches de montures) | `dmoptiquesarl.com` (canonique du site) |

Détails techniques :

- **Une seule source** : `tools/site/add_amk_social.py` (`PREF_DOMAIN`) et
  `tools/site/add_social_footer.py` (`PREF_DOMAIN`) — le jour du passage au domaine propre, **une
  ligne change** et l'outil est relancé ; les 3 + 97 pages suivent.
- **Accessibilité** : lien avec texte visible (pas d'icône seule), cible ≥ **44 px**, `:focus-visible`
  à 2 px, contraste vérifié (`audit_html` : 0 finding sur les deux pages testées).
- **Bilingue** : AMK par `data-en`/`data-fr` ; DM par `.fr-only`/`.en-only` sur les pages FR **et** EN.
- **Idempotence** : les deux outils portent un marqueur (`class="amk-psrc"`, `class="psrc"`) et un
  `--check` ; relancer ne duplique rien (vérifié : « 97 pages · 0 à corriger »).

## 5 · Ce que ce badge ne fera pas — à dire à King

1. **Ce n'est pas un levier de classement.** Il ne touche que les lecteurs qui nous ont déjà choisis.
2. **Top Stories est un produit d'actualité.** Une école, une clinique ou un studio web n'y apparaît
   presque jamais : l'effet attendu chez nous est **faible**, et il porte surtout sur AI Overviews/AI
   Mode (où il faut l'inclusion Search Console).
3. **Le lien peut tomber sur un domaine absent de l'outil.** Si `amk-cm.vercel.app` n'y figure pas, le
   lecteur arrive sur une recherche sans résultat. **À vérifier par King en un clic** (voir §6).
4. Le jour où le site AMK passe sur son domaine, le lien du badge **doit** suivre — sinon il désigne
   un domaine de test.

## 6 · À faire par King, deux minutes

1. Ouvrir `https://www.google.com/preferences/source?q=amk-cm.vercel.app` **connecté** à un compte
   Google : le site apparaît-il dans les résultats ? Si non : le sous-domaine n'est pas encore retenu
   par Google — le badge reste en place mais ne sert à rien tant que le domaine propre n'existe pas.
2. Refaire le test avec `https://www.google.com/preferences/source?q=dmoptiquesarl.com`.

## 7 · Sources

- Search Central — *Help your readers find your site through preferred sources* (maj 18/09/2026) :
  <https://developers.google.com/search/docs/appearance/preferred-sources>
- Blog Google — *Preferred sources now in AI Mode and AI Overviews* (27/05/2026)
- Search Engine Land — disponibilité globale (30/04/2026) ; Search Engine Roundtable — bouton mis à
  jour et retour à la page (20/08/2026)
