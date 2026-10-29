# Checklist Google : DM OPTIQUE SARL, 29/10/2026

```text
ÉTAPE 0    carte lue le 29/10 12 h 01 (14 296 nœuds, 871 documents), §0 → §3 bis, sans reconstruction
           ask « avis google reviews site opticien » → SETUP-GOOGLE-BUSINESS, MARKETING-OPTICAL, PLAN-SEO
PRE-FLIGHT lu · §0b dossier client (dossier.md, a-completer.md) · §0c knowledge (MARKETING-OPTICAL-2026-10-22)
DOCUMENTS  seo/DIAGNOSTIC-INDEXATION-2026-10-26.md · seo/RUNBOOK-403-2026-10-26.md ·
           seo/PLAN-SEO-2026-10.md · launch/SETUP-GOOGLE-BUSINESS.md · pre-launch-checklist.md
MÉTHODE    les chiffres de Google d'abord (export du 23/10), puis nos relevés d'aujourd'hui, puis les
           actions classées par qui les fait. Aucun délai promis : Google n'en publie aucun, et une
           semaine sur un domaine de trois semaines ne prouve rien.
LIMITE     cet environnement n'ouvre pas de socket vers dmoptiquesarl.com (curl : SSL refusé, vérifié
           aujourd'hui). Les pages en ligne sont lues par proxy (fetch_page). Un 200 vu par un proxy
           n'est pas ce que Googlebot reçoit : les vérifications qui engagent Google se font dans
           Search Console, à la main, par King.
```

## 0 · Trois questions, trois chantiers

« Le site n'apparaît pas sur Google » mélange trois choses qui n'ont ni le même délai, ni le même
propriétaire. Tant qu'on les traite ensemble, on attend un miracle au lieu de faire trois gestes.

| La question | Ce qui la règle | Qui | Délai |
|---|---|---|---|
| **Est-il dans l'index ?** | Search Console : propriété juste, sitemap soumis, erreurs à zéro | King | jours à semaines, sans garantie |
| **Est-il sur la carte ?** | Fiche Google : catégorie, adresse, horaires, photos, avis | King + client | immédiat à visible, mais dépend de la fiche |
| **Mérite-t-il d'être cité ?** | Les pages, leur contenu, leurs réponses | nous (fait) | au rythme des mises à jour |

Aujourd'hui, le chantier 3 est fait, le chantier 1 est à moitié fait, et le chantier 2 n'est plus un
inconnu. **État de la fiche au 29/10** (captures dans `preuves-2026-10-29/`) : revendiquée et gérée
(« You manage this Business Profile »), profil « Complete info », nom, adresse et téléphone identiques
au site, catégorie « Opticien » rendue en français, **7 avis à 4,9** (4 avis à 5,0 le 23/10). Un seul
écart : la fiche ferme à 17h00, le site dit 17h30. C1, C2, C3, C4, C6 et C8 passent au vert ; C5 attend
un arbitrage du cabinet.

## 1 · Ce que Google a dans les mains, mesuré

### 1.1 · L'export du 23/10 (Search Console, chiffres de Google)

| Raison | Pages | Lecture |
|---|---|---|
| Blocked due to access forbidden (403) | 8 | **4 pages vues sous 3 variantes** d'URL (`www`, `http`, sans barre finale), crawlées le 20/10, avant la mise en ligne du 22/10 |
| Redirect error | 2 | propriété en `www` alors que le site canonise l'apex |
| Discovered, not indexed | 89 | Google connaît les URL et n'est pas venu : budget de crawl minuscule sur un domaine neuf |
| Crawled, not indexed | 3 | venu, lu, pas retenu |
| **Indexées** | **4 / 106** | impressions : 0 à 11 par jour |

### 1.2 · Ce qui a changé depuis, et ce qui est vérifié aujourd'hui

| Point | État au 29/10 | Preuve |
|---|---|---|
| Surface d'indexation | **22 URL** (11 FR + 11 EN), **80 fiches en `noindex,follow`** | `python3 tools/ops/dm_index_surface.py --check` |
| Sitemap en ligne | **22 URL**, `lastmod` 2026-10-28 | `fetch_page` 29/10 |
| `robots.txt` en ligne | `Allow: /` + sitemap déclaré, aucun robot bloqué, **y compris les robots d'assistants** | `fetch_page` 29/10 |
| Canonical / hreflang | 51 paires réciproques, 0 problème | `audit_seo.py` |
| Portique SEO local | **0 faute · 0 avertissement** | `audit_seo_local.py --strict` |
| Porte de livraison | 0 P1 · 0 P2 · 1 P3 connu (images d'aperçu partagées) | `audit_delivery.py --strict` |
| `http://` toujours servi en 200 | **corrigé le 26/10** (Always Use HTTPS = ON, déclaré par King) | `RUNBOOK-403` § « ce qui est prouvé » |
| Validation du 403 lancée | **oui, 26/10** (8 en attente, 0 en échec) | idem |
| Sitemap soumis dans la propriété Domaine | **Dernier geste non fait au 26/10** | `RUNBOOK-403` geste 3 |

**Conclusion de cette section : il n'y a plus rien à corriger dans le HTML.** Le site demande 22 URL
propres, liées, canoniques, bilingues. Ce qui reste se passe dans deux tableaux de bord.

## 2 · Côté site : ce qui est fait, et ce qu'on peut encore faire

Rien ici n'attend King. Ces lignes se vérifient par commande.

| # | Point | Comment on vérifie | C'est fait quand |
|---|---|---|---|
| A1 | La surface indexée est celle qu'on veut | `python3 tools/ops/dm_index_surface.py --check` | `pages cœur indexables : 22 · fiches noindex : 80 · OK` |
| A2 | Le sitemap ne demande pas l'index d'une page qui le refuse | `audit_delivery.py --strict` (D9) | 0 P1, 0 P2 |
| A3 | Aucune page orpheline, aucun titre en double | `audit_seo_local.py --strict` | 0 faute, 0 avertissement |
| A4 | Les robots d'assistants ne sont pas bloqués | lire `robots.txt` en ligne | `Allow: /`, aucun `Disallow` |
| A5 | Les fiches montures restent accessibles sans polluer l'index (`noindex,follow`) | `dm_index_surface.py --check` | 80 fiches `noindex`, 0 dans le sitemap |
| A6 | Chaque question fréquente a sa réponse en page | `node tools/qa/test_dmoptic_page.mjs` | 71 verts, 0 échec |
| A7 | **Le site renvoie vers la fiche** (itinéraire, ouverture) | chercher `place_id` dans l'accueil et `/contact/` | 2 occurrences par page (fait) |
| A8 | **Le site invite à laisser un avis** | chercher `writereview` | ⛔ **absent aujourd'hui** : voir §5 |

## 3 · Côté Search Console : six gestes, tous de King

Aucun ne demande de code. Tous se font dans l'interface, avec le compte du cabinet.

| # | Geste | Où, exactement | C'est fait quand |
|---|---|---|---|
| B1 | **La propriété suivie est « Domaine »**, pas `www` | Search Console → sélecteur de propriété → `dmoptiquesarl.com` (type Domaine) | ✅ **fait** : les deux hôtes dans un même panneau Sitemaps ne peuvent exister que là |
| B2 | **Soumettre le sitemap** dans cette propriété | Indexation → Sitemaps → ajouter `sitemap.xml` | ✅ **fait** : soumis le 26/10, lu le 29/10, **Success, 22 pages** |
| B3 | **Valider le correctif du 403** | Indexation → Pages → « Blocked due to access forbidden (403) » → Valider le correctif | l'état passe de « En attente » à « Réussi » (peut prendre des semaines) |
| B4 | **Valider le correctif « Redirect error »** | même écran, motif « Redirect error » | idem |
| B5 | **Inspecter l'URL d'accueil et `/questions/`** | barre de recherche en haut → coller l'URL → « Demander l'indexation » | « URL dans l'index de Google » ou demande enregistrée |
| B6 | **Retirer le sitemap `www` en double** (le 29/10, deux lignes au tableau) | Sitemaps → les 3 points au bout de la ligne www → **Remove sitemap** | une seule ligne reste, celle de l'apex |

**Ce qui ne sert à rien, et qu'il faut s'épargner** : redemander l'indexation tous les jours (Google
limite le nombre de demandes), rouvrir les cinq contrôles WAF du 26/10 (faits, rien trouvé), et
soumettre le sitemap depuis deux propriétés à la fois. Le doublon `www` constaté le 29/10 est un reste
du 21/10, quand les deux hôtes servaient encore le site : `www` redirige en 301 vers l'apex depuis le
22/10, vérifié en ligne le 29/10. Retirer la ligne ne retire aucune URL de l'index.

## 4 · Côté fiche Google : le vrai levier du pack local

C'est ici que se joue « apparaître quand quelqu'un cherche un opticien à Bonabéri ». Les facteurs
locaux se répartissent, selon les relevés 2026, en proximité (≈ 55 %, non contrôlable), signaux de
fiche (≈ 32 %) et avis (16 à 20 %). **On ne contrôle que les deux derniers.**

| # | Point | Comment on vérifie | C'est fait quand |
|---|---|---|---|
| C1 | **La fiche existe et elle est revendiquée** | Maps → `place_id` `ChIJjdfYfQwXYRARAdi9mPLHGjY` → « Revendiquer cette fiche » | ✅ **fait** le 29/10 : « You manage this Business Profile », profil « Complete info » |
| C2 | **Nom identique partout** : `DM OPTIQUE SARL` | comparer fiche, site, Facebook, TikTok | quatre fois le même nom, à la lettre |
| C3 | **Adresse identique** : Ndobo Mayor, immeuble West Hotel, 1er étage, dernière porte à droite | comparer à `/contact/` | même rue, même étage, même repère |
| C4 | **Téléphone identique** : 656 122 239 | comparer | un seul numéro, partout |
| C5 | **Horaires exacts** : lun. au sam., examen 8h30 à 13h00, autres besoins 8h30 à 17h30 | comparer à `/contact/` | ⚠️ **écart trouvé le 29/10** : la fiche dit « Closes 5pm » (17h00), le site dit 17h30. À trancher par le cabinet, voir `RELEVE-FICHE-2026-10-29.md` §4 |
| C6 | **Catégories** | Modifier le profil → Catégorie | ✅ **tranché par l'écran le 29/10** : « Opticien » est en place et Google la rend en français. On la garde. Seule question restante, bonus : une secondaire d'optométrie, si le sélecteur la propose |
| C7 | **Photos réelles, 2 à 4 par mois** | ajouter des photos du cabinet | au moins 10 photos au départ, puis un ajout mensuel |
| C8 | **Avis : demander, sans trier ni inciter** | lien `writereview` + QR au comptoir | ✅ **ça marche** : 4 avis à 5,0 le 23/10 → **7 avis à 4,9 le 29/10** (+3 en six jours). Le lien est en ligne sur `/contact/`, la carte A6 est prête |

### C6 · L'arbitrage de catégorie, tranché par l'écran le 29/10

**Réponse, 29/10** : la fiche affiche « **Opticien** in Bonabéri », rendue en français sur une recherche
francophone au Cameroun. La catégorie est en place, elle correspond au titre légal du cabinet, et on
n'y touche pas. Le débat ci-dessous reste écrit parce qu'il explique la décision, pas parce qu'il est
encore ouvert.

Deux positions existaient dans nos documents, et elles ne disaient pas la même chose :

- `launch/SETUP-GOOGLE-BUSINESS.md` (21/10) : **catégorie principale « Opticien »**, au motif que la
  catégorie existe au Cameroun, et « ne pas la changer » ;
- les relevés externes 2026 recommandent **« Optometrist »** en principale, la catégorie large diluant
  l'intention.

**Ce qui départageait, et c'était bien à l'écran** : ouvrir le sélecteur et regarder ce que Google
propose réellement pour le Cameroun. L'écran a répondu avant le sélecteur, puisque la catégorie
principale est visible sur la fiche publique. **« Opticien » gagne, et on ne force rien.**

Il reste une seule question, et c'est un bonus, pas une correction : **si** le sélecteur propose une
catégorie secondaire d'optométrie ou d'examen de la vue, l'ajouter en secondaire est cohérent avec
« opticien optométriste ». À regarder une fois, sans changer la principale.

## 5 · Ce que le site peut faire en plus, et que je peux livrer

Une seule chose, et elle vaut plus que tout le reste côté code : **inverser le sens du flux**. Le site
n'affiche pas les avis (voir §6), mais il peut **alimenter** la fiche. C'est là que se gagne la
vélocité sur 90 jours, qui pèse plus que le total.

| # | Livrable | Effet | Coût |
|---|---|---|---|
| D1 | Lien « Vous êtes venu au cabinet ? Laissez un avis sur Google » sur `/contact/`, discret, une ligne | le patient qui sort de la page contact peut laisser un avis en un geste | ✅ **fait le 29/10** |
| D2 | QR code de ce même lien, prêt à imprimer pour le comptoir | la demande se fait au bon moment, dans la vraie vie | ✅ **fait le 29/10** : `launch/carte-avis-a6.pdf` |
| D3 | Message de demande d'avis, version courte FR + EN, à valider par King | sert sur WhatsApp après la visite, jamais avant | ⏳ restant |

**D1 et D2 sont livrés** : voir `clients/dm-optic/launch/AVIS-GOOGLE-2026-10-29.md` (le bloc, la carte
A6, la vérification de relecture du QR, et le faux positif corrigé dans `shot.mjs`). D3 reste ouvert :
le texte d'une demande d'avis se valide avant d'être envoyé, il ne s'écrit pas au passage.

## 6 · Ce qu'on ne fera pas, et la raison

| Refus | Pourquoi |
|---|---|
| **Recopier les avis Google sur le site** | Google déclare inéligibles aux étoiles les pages `LocalBusiness` ou `Organization` qui affichent des avis contrôlés par l'entité elle-même (guidelines review snippet, 24/07/2026), widgets inclus. Aucun gain, et un risque de mauvaise interprétation |
| Récupérer les avis autrement que par la Maps Platform | hors conditions d'utilisation, et nous n'avons ni clé ni budget API |
| Acheter ou échanger des avis | interdit, et détectable ; la règle maison date du 21/10 |
| Promettre une position ou un délai | Google écrit lui-même qu'aucun moyen ne permet de demander ni d'acheter un meilleur classement |
| Créer des pages « opticien à [quartier] » en série | doorway + scaled content, doc Google du 28/08/2026 |
| Redemander l'indexation chaque jour | la demande est limitée, et elle ne crée pas de budget de crawl |

## 7 · Le calendrier de lecture, sans promesse

Trois dates, trois lectures, et une seule règle : **on lit ce que Google dit, on ne l'interprète pas**.

| Date | Ce qu'on lit | Ce qui est normal | Ce qui ne l'est pas |
|---|---|---|---|
| **05/11** | Search Console → Pages | 403 en baisse, sitemap « Réussite », plus de 4 URL connues | un 403 **nouveau** après le 26/10 : rouvrir l'annexe du runbook |
| **16/11** | Pages + Performances | cible interne : **≥ 15 URL indexées sur 22**, 0 en 403, 0 redirect error, « Découvertes » en baisse | index stable à 4 : le problème n'est plus le site |
| **30/11** | Performances + fiche | premières impressions régulières, premiers avis récents | 0 impression et 0 avis : le sujet est la fiche, pas le site |

**Ces cibles sont internes. Elles ne sont promises ni au client, ni à personne.** Un domaine de trois
semaines sans lien externe peut rester des mois dans « Découvertes, non indexées » sans qu'aucune règle
ne soit enfreinte.

## 8 · La ligne du bas

| Fait, et vérifié | Reste à faire | Qui |
|---|---|---|
| HTML irréprochable, 22 URL, canonical, hreflang, robots, questions | suivre la validation du 403 et du redirect (B3, B4) | **King** |
| sitemap soumis dans la propriété Domaine, lu le 29/10, 22 pages (B2) | retirer le sitemap `www` en double (B6) | **King**, 2 minutes |
| fiche revendiquée, « Complete info », nom, adresse et téléphone identiques (C1 à C4) | trancher les horaires : la fiche dit 17h00, le site dit 17h30 (C5) | **King + cabinet** |
| catégorie « Opticien » en place, rendue en français (C6) | une secondaire d'optométrie, si le sélecteur la propose | **King**, à l'occasion |
| 7 avis à 4,9, dont 3 de plus en six jours (C8) | coller la capture « Pages » de Search Console au 05/11 | **King** |
| lien et QR « laisser un avis » livrés (D1, D2) | imprimer la carte A6 et la poser au comptoir | **King** |

Détail des captures, y compris ce qu'elles ne prouvent pas : `seo/RELEVE-FICHE-2026-10-29.md`.

**La phrase à retenir.** Le site n'est pas en retard : il est propre, et il attend deux gestes qui ne
sont pas dans le dépôt. Une semaine sans résultat n'est pas un signal, c'est la durée normale d'un
domaine neuf ; ce qui serait un signal, c'est le même chiffre au 16/11.
