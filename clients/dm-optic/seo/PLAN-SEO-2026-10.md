# DM OPTIQUE — plan SEO et mise en ligne (15/10/2026)

> Statuts : **VÉRIFIÉ** = lu dans la source officielle (URL et date). **PARTIEL** = source secondaire ou section non lue.
> **NON VÉRIFIÉ** = pas encore cherché. Aucun chiffre de volume de recherche sans source.
> Rendez-vous client : **vendredi 16/10/2026** (et non 17/10, qui est un samedi).

## 0 · Ordre des opérations (dépend du domaine final)

1. Décision du domaine final et de l'hébergement (King) → déploiement sur Cloudflare (King, manuel).
2. Retirer Vercel **seulement après** confirmation que le domaine final répond (King).
3. Search Console, sitemap, Google Business Profile → après le déploiement final (le domaine doit exister).
4. `noindex` levé **au lancement seulement** (checklist 10.1).

Point d'attention : le message du 10/10 dit au client que l'ancien lien « ne sera plus actif ». Tout changement d'adresse doit être annoncé au client, par King.

## 1 · Les 13 points

| # | Point | Statut | Ce que la source dit | Décision |
|---|---|---|---|---|
| 1 | Google Search Console | VÉRIFIÉ (starter guide, mis à jour 10/12/2025) | « Setting up a Search Console account helps you monitor and optimize how your website performs on Google Search. » | À faire après déploiement final. Compte au nom du cabinet, King en administrateur. |
| 2 | Sitemap | NON VÉRIFIÉ | Doc « sitemaps » non ouverte | À vérifier avant de le créer. Une seule page : sitemap court, une URL. |
| 3 | Google Analytics | **BLOQUÉ** | AI features (10/12/2025) : analytics optionnel (« you could also track conversions… in other tools such as Google Analytics ») | **Collecte de données : avocat d'abord** (règle King, loi 2024/017). Search Console suffit au départ. |
| 4 | Google Business Profile | PARTIEL | AI features renvoie à « establish-business-details » ; fiche déjà rédigée (`SETUP-GOOGLE-BUSINESS.md`) | King crée avec le client (vérification sur son téléphone). Horaires : lundi à samedi, 8h30–13h00 et 8h30–17h30. |
| 5 | Concurrents locaux et étrangers, mots-clés | NON VÉRIFIÉ | Pas de source lue | Recherche manuelle sur les résultats (Bonabéri, Douala, opticien). L'outil open-seo (point 12) n'est pas une source de volume de recherche. Aucun volume chiffré sans source. |
| 6 | Ville dans le titre | VÉRIFIÉ (starter guide, section « Keywords in the domain name or URL path » ; spam policies, « keyword stuffing ») | Les mots-clés dans le domaine ont « hardly any effect » ; **listes de villes = bourrage de mots-clés** | Mettre **un** « Bonabéri » naturel dans le titre et la description. Pas de liste de quartiers. Titre actuel : « …à Douala » seulement. |
| 7 | Meta descriptions | PARTIEL | Section « Control your snippets » non lue | Une description par page, en phrase naturelle, sans liste de mots-clés. À confirmer dans la section. |
| 8 | Liens internes | VÉRIFIÉ (AI features, 10/12/2025) | « Making your content easily findable through internal links » | Lier les sections (montures, examen, contact) depuis l'accueil. Pertinent quand les pages existent. |
| 9 | Backlinks | VÉRIFIÉ (spam policies, 28/08/2026) | Interdits : acheter ou vendre des liens, échanges de liens, **liens dans les pieds de page de nombreux sites**, annuaires de faible qualité | **Pas de liens achetés, pas d'annuaires en masse.** Liens légitimes : fiche Google, partenaires locaux réels, presse locale. |
| 10 | llms.txt | PARTIEL | AI features (10/12/2025) : « no additional technical requirements ». La phrase explicite sur llms.txt est dans un guide plus récent que je n'ai pas pu ouvrir ; les sources secondaires la citent | **Ne pas faire** pour Google. Sans effet démontré. |
| 11 | Miroirs en Markdown | PARTIEL | Idem point 10. Source secondaire : un responsable Google aurait qualifié ces pages pour bots d'« idée stupide » | **Ne pas faire.** |
| 12 | open-seo (every-app) | PARTIEL | Dépôt lu en page d'accueil : « Open source alternative to Semrush and Ahrefs », 780 commits, activité au 14/10/2026. Les « principes de copie et workflow » n'ont pas été lus | Outil, pas une source de règles. À évaluer plus tard, avec ses données. Pas de clé ni de compte créés par nous. |
| 13 | Liste de backlinks Medium | VÉRIFIÉ (auteur, 23/05/2025) | L'auteur dit lui-même que la plupart des liens sont « spammy, no-follow, or expired » ; 48 liens fonctionnels sur 3 000 ; beaucoup de sites sans rapport (Giphy, Zazzle, Redbubble…) | **Ne pas utiliser.** Recoupe la règle de liens de spam (point 9). |

## 2 · Ce qui relève du client ou de King (pas d'Arena)

- Création des comptes Google, Search Console, Google Business Profile, Facebook et TikTok : King, avec le client présent (code sur son téléphone).
- Domaine, DNS, Cloudflare, Vercel : King.
- Décision sur les analytics : avocat d'abord.
- Photos, point de repère, position GPS : client, vendredi 16/10.

## 3 · Ce qui reste à faire côté site (Arena)

- Le montage `/montures` code en dur l'adresse Vercel dans son `canonical` et son `og:url`. Il faut la lire depuis `--url`, comme la page d'accueil, avant tout changement d'hébergement.
- Le texte pour le client sur les paiements (espèces, Mobile Money, paiement en plusieurs fois) : approuvé par le client sur WhatsApp, 15/10 17:54. À ajouter sur la page.
- Message WhatsApp sur les heures de service (le cabinet n'est pas ouvert 24h/24).
