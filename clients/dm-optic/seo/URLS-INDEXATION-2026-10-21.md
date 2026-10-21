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

## 8 · Le sitemap renvoie 403 à Google — diagnostic corrigé (22/10)

Capture Search Console du 21/10 : *Sitemap could not be read · General HTTP error · 403*, **1 instance**.
Le fichier existe : il s'ouvre normalement dans un navigateur et je viens de le lire en ligne (48 URL).

**Ma première hypothèse était fausse.** J'avais mis en tête de liste la protection anti-robots de
Cloudflare. La capture *Security Overview* du 22/10 la contredit :

| Ce que montre l'écran | Lecture |
|---|---|
| **Bot traffic : 0/1 running** | Aucune protection anti-robots n'est active. Bot Fight Mode est **éteint** → il n'a pas pu bloquer Googlebot. |
| Mitigated **0,91 %** sur 4 310 requêtes | Cloudflare bloque très peu de choses — rien qui ressemble à un refus systématique. |
| DDoS, API abuse, Web app exploits : *All running* | Ce sont les protections qui ne gênent jamais un robot de moteur. |
| *AI Labyrinth*, *security.txt* : simples **suggestions** | Rien d'appliqué. |

**Donc le 403 ne vient probablement pas de Cloudflare.** Deux explications tiennent, dans cet ordre :

1. **Une seule instance, à un moment précis.** Une erreur unique sur une lecture, ce n'est pas une
   règle : c'est un hoquet (propagation DNS au lancement du 21/10, ou coupure d'une seconde).
   **La réponse est de resoumettre et de regarder 24 h plus tard** — pas de changer la configuration.
2. **Le mauvais hôte.** `www.dmoptiquesarl.com` et `dmoptiquesarl.com` répondent **tous les deux** le
   site complet (vérifié le 22/10 : `robots.txt` identique sur les deux, canonical vers l'apex). Si le
   sitemap a été soumis sur `www` alors que ses 48 URL pointent l'apex, Google lit un fichier qui
   déclare un autre domaine que celui de la propriété. C'est une cause classique d'erreur de lecture.

**Ce qui a été corrigé côté site (22/10, puis corrigé une seconde fois) :** un fichier `_redirects`
renvoyant `www` → apex avait été ajouté au build. **Il a fait échouer le déploiement Cloudflare**
(`Only relative URLs are allowed`, code 100324) : les Workers n'acceptent que des chemins relatifs dans
ce fichier, et `_redirects` ne compare jamais les hôtes. Le fichier est **retiré**. La redirection se
fait dans la zone : **Cloudflare → Rules → Redirect Rules** (modèle « Redirect from WWW to root »),
voir `launch/DEPLOIEMENT-CLOUDFLARE-2026-10-22.md` §3 ter. Le `canonical` de chaque page pointe déjà
l'apex, donc les moteurs consolident même sans cette règle.

### Où cliquer, dans l'ordre (10 minutes)

1. **Cloudflare → Workers & Pages → projet du site → Create deployment → upload** : déposer
   `dmopticsarl.zip` (182 entrées). C'est ce qui met en ligne `/en/` et le `srcset`.
2. Vérifier ensuite `https://dmoptiquesarl.com/en/` (doit afficher l'anglais) et
   `https://www.dmoptiquesarl.com/` (doit **rediriger** vers l'apex).
3. **Search Console → Sitemaps** : supprimer l'entrée en erreur, puis saisir **`sitemap.xml`**
   (sans `https://`, sans `www`) — la propriété doit être celle du domaine **sans www**.
4. Si la propriété existante est en `https://www…` : ajouter une **propriété de domaine**
   (*Ajouter une propriété → Domaine → `dmoptiquesarl.com`*), validée par un enregistrement TXT chez
   Cloudflare. Elle couvre **www et apex d'un coup**, et c'est la seule forme qui ne se trompe jamais
   d'hôte. Le sitemap s'y soumet ensuite en deux clics.
5. **Revenir dans 24 h.** Statut attendu : *Success*. Si c'est encore *Couldn't fetch* :
   **Cloudflare → Security → Events**, filtrer sur le chemin `sitemap` — l'événement nomme le service
   qui a bloqué, s'il y en a un.

### Ce qu'on ne fait pas

- **Redemander l'indexation des 10 URL pour « forcer ».** Tant que le sitemap n'est pas lu, les
  demandes manuelles ne compensent rien ; après, les 96 URL se découvrent seules.
- **Toucher aux règles de sécurité Cloudflare.** Rien n'est actif, il n'y a rien à désactiver — et
  désactiver une protection qui n'existe pas ne répare pas un 403.
- **Renommer ou déplacer le sitemap.** Il est à sa place, à la racine, déclaré dans `robots.txt`.
