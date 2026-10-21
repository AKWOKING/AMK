# Les URL à faire indexer aujourd'hui — 21/10/2026

**Objectif du jour :** que Google connaisse les **10 pages qui travaillent**, pas les 48.
Les 38 autres suivront seules par le sitemap — on ne gaspille pas le quota du jour sur une fiche F60.

**Ce qu'est « demander l'indexation » :** une file d'attente prioritaire, pas une garantie. Google passe
en général sous **24–72 h** ; le compteur de demandes est limité à ~10–12 par jour et par propriété.

---

## 1 · Les 3 gestes, dans cet ordre

### Geste 1 — le sitemap (une fois, 30 secondes)

Search Console → propriété **`dmoptiquesarl.com`** (type Domaine) → menu **Sitemaps** → saisir
`sitemap.xml` → **Envoyer**.

Il doit afficher **Réussite** et **48 URL détectées**. S'il est déjà envoyé : vérifier simplement que la
date de dernière lecture est récente. **Ne pas renvoyer 10 fois** — ça ne rend pas Google plus rapide.

### Geste 2 — les 10 URL prioritaires (aujourd'hui)

Pour chacune : coller l'URL dans la **barre de recherche en haut de Search Console** → attendre le test →
bouton **« Demander l'indexation »**. Une par une, dans cet ordre :

| # | URL | Pourquoi elle passe en premier |
|---|---|---|
| 1 | `https://dmoptiquesarl.com/` | la porte d'entrée, le nom du cabinet |
| 2 | `https://dmoptiquesarl.com/montures/` | le hub, lien de tous les posts |
| 3 | `https://dmoptiquesarl.com/examen-de-vue/` | **le service qui fait venir** · cible du post Google du 27/10 |
| 4 | `https://dmoptiquesarl.com/contact/` | adresse + horaires + WhatsApp · cible du post du 17/11 |
| 5 | `https://dmoptiquesarl.com/le-cabinet/` | la preuve (photos réelles, ONOC) |
| 6 | `https://dmoptiquesarl.com/montures/femmes/` | catégorie la plus fournie (24 montures) |
| 7 | `https://dmoptiquesarl.com/montures/hommes/` | catégorie homme |
| 8 | `https://dmoptiquesarl.com/montures/enfants/` | **cible du post Google du 10/11** |
| 9 | `https://dmoptiquesarl.com/montures/femmes/f01-ovale-doree/` | monture du **carrousel Facebook n°1** |
| 10 | `https://dmoptiquesarl.com/montures/hommes/h08-double-pont-aviateur-noir-et-dore/` | monture du **carrousel n°2** |

### Geste 3 — demain et après-demain : les 2 montures restantes des posts, puis le reste

| Jour | URL |
|---|---|
| demain | `https://dmoptiquesarl.com/montures/enfants/e16-carree-bleue/` (carrousel n°3) |
| demain | `https://dmoptiquesarl.com/montures/femmes/f24-carree-ecaille/` (monture du TikTok n°1) |
| ensuite | les 36 autres fiches, **sans intervention** : elles sont dans le sitemap et toutes liées depuis leur catégorie |

---

## 2 · Ce qu'il faut regarder après, et quand

| Quand | Où | Ce qu'on attend |
|---|---|---|
| **24–72 h** | Search Console → **Indexation → Pages** | les 10 URL passent de « Détectée, non indexée » à **« Indexée »** |
| **7 jours** | Google, en navigation privée : `site:dmoptiquesarl.com` | le nombre de pages listées monte (c'est indicatif, pas une mesure) |
| **7 jours** | Search Console → **Performances → Requêtes** | premières requêtes réelles : « dm optique », « opticien bonaberi »… |
| **4 semaines** | même écran | c'est là qu'on saura si le travail paie — pas avant |

**Ne pas s'inquiéter si une URL reste « Détectée, non indexée » une semaine.** Sur un domaine neuf,
Google indexe par vagues. Ce qui le décide : le contenu, les liens entrants (posts Facebook, fiche
Google, TikTok) et le temps.

---

## 3 · Deux précautions

1. **Ne pas demander l'indexation deux fois la même URL le même jour** — le quota est consommé pour rien.
2. **Ne pas envoyer d'URL avec un `?` ou un `#`** : uniquement les adresses ci-dessus, telles quelles.
   Une URL avec paramètre crée une page en double dans l'index.

> Rappel : la balise canonique est correcte sur les 49 pages (audit du jour), donc même si Google découvre
> une variante, il saura laquelle garder. C'est déjà fait — c'est ce qui rend cette étape simple.

---

## 8 · Le sitemap renvoie 403 à Google — diagnostic (22/10)

Capture du 21/10 : *Sitemap could not be read · General HTTP error · HTTP Error: 403*, 1 instance.
Le fichier **existe** (il s'ouvre normalement dans un navigateur, 48 URL, et il en comptera 96 après le
prochain envoi). Un 403 n'est donc pas un fichier manquant : **quelqu'un refuse l'accès au robot.**

**Par ordre de probabilité :**

1. **La protection anti-robots de Cloudflare.** C'est le cas le plus fréquent depuis que Cloudflare
   bloque les robots par défaut. À vérifier : *Security → Bots* (Bot Fight Mode / « Block AI bots ») et
   *Security → WAF → Custom rules*. Googlebot doit être autorisé ; « verified bots » = allow.
2. **L'adresse soumise n'est pas la bonne.** Search Console accepte `https://www.dmoptiquesarl.com/...`
   et `https://dmoptiquesarl.com/...` comme deux adresses différentes. La bonne est **sans `www`** :
   `https://dmoptiquesarl.com/sitemap.xml`. Si une entrée `www` traîne, la supprimer avant de resentir.
3. **Une redirection sur le chemin.** Si Cloudflare redirige (`www` → apex, ou http → https) sur
   `/sitemap.xml`, Google lit la redirection comme une erreur. Le fichier doit répondre **200 en direct**.

**Les 4 gestes, dans l'ordre :**
1. Cloudflare → *Security → Bots* : autoriser les robots vérifiés (Googlebot en fait partie).
2. Search Console → *Sitemaps* : supprimer l'entrée existante, puis soumettre **`sitemap.xml`** (sans
   `https://`, sans `www`, le domaine étant déjà celui de la propriété).
3. Cliquer **OPEN SITEMAP** : si la page s'ouvre, le fichier est bon côté serveur — le refus est donc
   côté protection, et l'étape 1 le corrige.
4. Revenir 24 h plus tard : le statut doit passer de *Couldn't fetch* à *Success*.

**Ce qu'on ne fait pas :** redemander l'indexation des 10 URL pour « forcer ». Le sitemap est le seul
point bloquant ; tant qu'il renvoie 403, aucune demande manuelle ne compense. Et une fois le sitemap lu,
les 96 URL (48 françaises + 48 anglaises) se découvrent **toutes seules** — les demandes manuelles ne
servent plus qu'à accélérer les pages qui comptent.

