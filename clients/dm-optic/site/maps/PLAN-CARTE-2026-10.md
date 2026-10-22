# La carte et l'itinéraire — ce qu'on installe, ce qu'on n'installe pas

> **21/10/2026.** King a envoyé la capture + le code « Quick Builder » de Google (Locator Plus) et le
> code copié. Ce document tranche : ce qu'on prend du code, ce qu'on n'installe pas, et pourquoi.
> **La carte du cabinet existe — mais elle n'a pas besoin d'une clé API pour nous servir.**

---

## 1 · Ce que le code contient, vérifié ligne à ligne

| Élément | Valeur réelle |
|---|---|
| Nom | `DM OPTIQUE SARL` |
| Adresse | Ndobo Mayor, Immeuble West Hotel, 1er étage, dernière porte à droite, Bonabéri |
| Ville | Douala, Cameroun |
| **`placeId`** | **`ChIJjdfYfQwXYRARAdi9mPLHGjY`** |
| Coordonnées | **4.1010324, 9.6323773** |
| Composant | `<gmpx-store-locator>` (Extended Component Library **0.6.15**) |
| Clé API | **`YOUR_API_KEY_HERE`** — deux fois, donc **aucune** |
| `mapId` | `""` dans la config, `DEMO_MAP_ID` dans la balise — **incohérent** |
| Bandeau de la capture | « **Finish account setup** to add to your site » |

**Le code collé, tel quel, ne fonctionne pas** : sans clé, le composant reste vide ; et le compte Google
Cloud n'est pas terminé (pas de facturation, pas d'API activée). Ce n'est pas un défaut du travail de
King — c'est l'écran où Quick Builder s'arrête tant que la clé n'existe pas.

**Ce que le passage a quand même donné, et qui vaut de l'or :** l'**identifiant canonique de la fiche**
(`place_id`) et ses coordonnées exactes. C'est la seule chose qu'on ne pouvait pas deviner, et elle ne
demande ni clé, ni facturation, ni JavaScript.

---

## 2 · Verdict sur le Locator Plus : **non, pas maintenant**

| Raison | Détail |
|---|---|
| **Un locator pour un seul lieu** | L'écran affiche « All locations (1) ». L'outil est fait pour les chaînes : il ajoute un panneau de recherche et une liste… à un endroit unique |
| **Clé + facturation** | Google Maps Platform exige un compte de facturation actif. La clé doit être restreinte par **référent HTTP** (`dmoptiquesarl.com`), sinon elle est pillable |
| **Un script Google en plus** | Le composant charge `ajax.googleapis.com` sur **chaque** visite. Le site est aujourd'hui sans script tiers, sans cookie, sans traceur — c'est un argument commercial, pas un détail |
| **Deux langues, deux systèmes** | Les libellés du widget viennent de Google, pas de notre bascule FR/EN |
| **Le vrai besoin est l'itinéraire** | Le client veut « comment j'y vais / est-ce que c'est bien là », pas explorer une carte |

**Si King veut un jour la carte intégrée**, les conditions sont écrites ici pour ne pas les réinventer :
clé créée dans un projet Google Cloud **au nom du cabinet**, API **Maps JavaScript** seulement, clé
restreinte par référent HTTP (`https://dmoptiquesarl.com/*`, `http://localhost:*`), **alerte de budget**
(le risque n'est pas la clé volée, c'est la facture), `mapId` cohérent, et un bandeau de consentement si
un cookie Google apparaît. Rien de tout ça n'est fait aujourd'hui.

---

## 3 · Ce qu'on a fait à la place — zéro clé, zéro facture

Les **trois liens officiels** de Google Maps (API « Maps URLs »), qui ne demandent aucune clé :

| Usage | Lien |
|---|---|
| **Itinéraire** (bouton de l'accueil) | `https://www.google.com/maps/dir/?api=1&destination=DM%20OPTIQUE%20SARL&destination_place_id=ChIJjdfYfQwXYRARAdi9mPLHGjY` |
| **Ouvrir la fiche** (page contact) | `https://www.google.com/maps/search/?api=1&query=DM%20OPTIQUE%20SARL&query_place_id=ChIJjdfYfQwXYRARAdi9mPLHGjY` |
| **Laisser un avis** (option, à valider) | `https://search.google.com/local/writereview?placeid=ChIJjdfYfQwXYRARAdi9mPLHGjY` |

**Pourquoi c'est mieux qu'avant :** le lien « Ouvrir dans Maps » cherchait le cabinet par son **nom** —
Google pouvait afficher une liste, ou un homonyme. Avec `place_id`, il ouvre **la** fiche. Le bouton
« Itinéraire » de l'accueil existait dans le code mais restait **caché** (`MAP_URL` vide) : il est
maintenant actif.

---

## 4 · État du dépôt après le changement

| | |
|---|---|
| `demos/dmoptic-v1.tpl.html` | `MAP_URL` renseigné (itinéraire par `place_id`) |
| `demos/build_dmoptic_montures.py` | `PLACE_ID` en constante ; lien contact par `query_place_id` |
| Build | `build_dmoptic.py --production` + `build_dmoptic_montures.py` — 47 pages + sitemap 48 |
| Portiques | `audit_html` **49/49** · `audit_a11y --strict` **rc 0 sur 49** · `check_inline_js` **49/49** · `audit_images` 0 · `test_dmoptic_page.mjs` vert |
| `dmopticsarl.zip` | reconstruit, **132 fichiers**, `testzip` OK |
| Déploiement | **non fait ce tour** : le bac n'a ni jeton Vercel ni projet lié, et `api.vercel.com` n'est pas joignable. Le zip est prêt pour l'upload Cloudflare (geste de King) |

---

## 5 · Sources

- Code et capture : Google Maps Platform → **Quick Builder** → *Locator Plus*, export du 21/10/2026 (archivé à côté, `google-quick-builder-locator.html`).
- Formats de liens : documentation Google Maps URLs (`maps/dir/`, `maps/search/` avec `destination_place_id` / `query_place_id`).
- Contraintes de clé : documentation Google Maps Platform — « API security best practices » (restriction par référent HTTP), facturation obligatoire.
