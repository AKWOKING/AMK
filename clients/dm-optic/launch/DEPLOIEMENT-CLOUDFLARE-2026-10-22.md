# Cloudflare — publication automatique du site DM OPTIQUE

> **Version du 22/10/2026.** Remplace définitivement l'envoi manuel par le tableau de bord
> (« Upload static files to update your Worker »), qui plante sur 183 fichiers sans afficher d'erreur.

---

## 0 · Ce que ton site demande, en chiffres

| | Site | Limite Cloudflare Workers |
|---|---|---|
| Fichiers | **183** | 20 000 |
| Fichier le plus lourd | **266 Ko** | 25 Mo |
| Poids total | **9 Mo** | — |

**Nom du Worker (relevé au tableau de bord le 22/10) : `dmoptiquesarl`.** C'est cette chaîne, exacte,
qui doit figurer en `name` dans `wrangler.toml` — un tiret de différence et `wrangler` crée un second
Worker, pendant que le domaine continue de pointer l'ancien.

Le site n'a jamais été le problème. L'outil d'envoi du tableau de bord, si : il annonce 184 fichiers,
ne montre aucune progression, et son propre bandeau précise qu'il ne gère que HTML/CSS/JS.

---

## 1 · La règle à comprendre avant tout : la branche n'est **pas** dans `wrangler.toml`

C'est le point qui bloque aujourd'hui, et il faut être clair : **`wrangler.toml` ne contient pas de
branche, et Cloudflare ne lit aucune branche dedans.** Le fichier dit *quel dossier publier* et *quelle
page servir en 404* — rien d'autre :

```toml
name = "dm-optique-sarl"                 # le nom du Worker (à recopier à l'identique)
[assets]
directory = "./hosting/previews/dmoptic" # le seul dossier publié
not_found_handling = "404-page"
```

La branche, elle, se règle à **deux endroits possibles**, et c'est ce choix qui décide de ce que tu
auras à faire à chaque nouveau chat :

| | Qui décide de la branche | Ce que ça coûte à chaque nouveau chat |
|---|---|---|
| **Workers Builds** (tableau de bord) | un réglage dans *Settings → Build* de Cloudflare | **tu changes le nom de la branche à la main** (30 s) |
| **GitHub Actions** (workflow) | le fichier `.github/workflows/deploy-dmoptic.yml`, avec `branches: ['arena/**']` | **rien** — toute branche `arena/…` publie |

Une ligne du type `branch = "arena/2fffee3b-amk"` écrite dans `wrangler.toml` **ne serait pas lue** :
ce n'est pas un champ reconnu. Le texte aurait l'air de faire le travail, et ne le ferait pas. C'est
pour cette raison que la solution durable est le workflow, pas le fichier de configuration.

---

## 2 · Le problème des branches qui changent

Chaque conversation ouvre une branche neuve (`arena/2fffee3b-amk` aujourd'hui, autre chose demain).
Deux conséquences :

1. **Un réglage « branche de production » dans Cloudflare devient faux à chaque nouveau chat.** Il faut
   le rouvrir et le changer — sinon le site cesse d'être mis à jour, silencieusement.
2. **Un fichier de workflow, lui, peut viser un motif** : `arena/**` couvre toutes les branches du
   genre, présentes et futures. C'est exactement le cas d'usage.

**Donc :** on démarre en Workers Builds pour publier **aujourd'hui** (§3), puis on installe le workflow
(§4) pour ne plus jamais toucher au tableau de bord. Les deux peuvent cohabiter : le même contenu
déployé deux fois ne casse rien. Quand le workflow aura publié une fois, tu peux déconnecter Workers
Builds si tu veux un seul mécanisme.

---

## 3 · Aujourd'hui : publier en 5 clics (Workers Builds)

> **État au 22/10 : ✅ FAIT.** Le dépôt est connecté (`AKWOKING/AMK`), la branche de production est
> `arena/2fffee3b-amk`, Build command vide, Deploy command `npx wrangler deploy`, racine `/`.
> Le premier build a été déclenché par le commit `9f5c26c`, qui corrige `name` en `dmoptiquesarl`.


1. **Cloudflare → Workers & Pages →** ouvre le projet du site.
2. Onglet **Settings** → section **Build** → **Connect** (ou *Connect Git repository*).
3. **GitHub** → autorise → dépôt **`AKWOKING/AMK`**.
4. **Production branch** : `arena/2fffee3b-amk` *(la branche de la conversation en cours)*.
5. **Build command** : *(vide — le site est déjà construit dans le dépôt)*
   **Deploy command** : `npx wrangler deploy`  ·  **Root directory** : `/`
6. **Save**. Le premier déploiement part dans la minute.

### Vérifier dans les 2 minutes

| À ouvrir | Attendu |
|---|---|
| `https://dmoptiquesarl.com/en/` | l'accueil **en anglais** (nouveau) |
| `https://www.dmoptiquesarl.com/` | **redirige** vers l'adresse sans `www` |
| `https://dmoptiquesarl.com/montures/` | la page montures, rapide |

Si `/en/` répond 404 : le déploiement n'a pas pris, va voir l'onglet **Deployments** du projet — le
journal y est lisible, contrairement à l'écran d'upload manuel.

---

## 3 bis · Le premier build n'a pas pris — que regarder (22/10, après 6 min)

**Constat mesuré :** `https://dmoptiquesarl.com/en/` répond encore la page **404**. Le site en ligne est
donc toujours l'ancienne version : **aucun déploiement n'a abouti**, ni réussi. Ce n'est pas une
hypothèse, c'est le test.

**Où lire la réponse, en 30 secondes :** Cloudflare → Workers & Pages → **dmoptiquesarl** → onglet
**Deployments** (à côté de *Metrics*). Chaque ligne porte un statut ; un échec ouvre un journal où la
cause est écrite en clair. **C'est ce journal qu'il faut copier** — l'écran d'envoi manuel, lui, ne
disait rien ; celui-ci parle.

Les quatre causes possibles, dans l'ordre de probabilité, et leur correction :

| # | Ce que dit le journal | Cause | Correction |
|---|---|---|---|
| 1 | **aucune ligne de build** (onglet vide) | Le `push` n'a déclenché personne : *Build watch paths* ne correspond pas au chemin modifié, ou la branche de production n'est pas `arena/2fffee3b-amk`. | *Settings → Build* : vérifier la branche, **vider Build watch paths** (ou y mettre `hosting/previews/dmoptic/**`), puis **Retry deployment**. |
| 2 | `Could not resolve ... wrangler` / `npx` introuvable | Aucun `package.json` à la racine : `npx` tente de résoudre le paquet et échoue selon la version de Node de l'image. | Mettre **Deploy command** = `npx --yes wrangler@latest deploy`. |
| 3 | `Authentication error` / `not authorized` | L'intégration GitHub n'a pas les droits sur le compte Workers. | *Settings → Build → Manage* (ou *Disconnect* puis *Connect*), réautoriser en cochant **tous les dépôts** et les droits Workers. |
| 4 | `name` / `worker not found` / un second Worker apparaît | `name` dans `wrangler.toml` ≠ nom du Worker. | Il vaut `dmoptiquesarl` depuis le commit `9f5c26c` ; si un Worker en double est apparu, supprimer le doublon, pas l'original. |

**Dans tous les cas :** après correction, *Deployments → **Retry deployment*** relance sans nouveau
commit. Et si le tableau de bord refuse encore, la route C (§ route C, `npx wrangler deploy` depuis un
ordinateur) publie le même dossier avec le même fichier de configuration — c'est le même travail, fait
hors du navigateur.

## 4 · Une fois pour toutes : le workflow `arena/**`

Le fichier ci-dessous est aussi dans le dépôt (`tools/deploy/workflow-deploy-dmoptic.yml`). Il doit
vivre dans **`.github/workflows/deploy-dmoptic.yml`** et, pour être hérité par les prochaines branches,
il doit exister dans **`main`** — puisque chaque nouvelle conversation coupe sa branche depuis `main`.

### 4.1 · Créer un jeton Cloudflare (2 min)

**Réponse à la question posée le 22/10 — modèle ou jeton personnalisé ?**
👉 **Le modèle « Edit Cloudflare Workers ».** Ne prends pas *Create Custom Token*.

Pourquoi : le modèle contient exactement les trois droits nécessaires, déjà réglés —
`Account → Workers Scripts → Edit`, `Account → Account Settings → Read`, `Zone → Workers Routes → Edit`.
Un jeton personnalisé obligerait à retrouver ces trois permissions à la main ; en oublier une donne un
échec « Authentication error » au moment du déploiement, sans dire laquelle manque.

**Le chemin exact :** *My Profile → API Tokens → Create Token* → dans la liste **API token templates**,
ligne **Edit Cloudflare Workers** → **Use template** → puis :

| Champ | Valeur |
|---|---|
| Token name | `deploy-dmoptique-github` |
| Account resources | ton compte (`Akwo.king.dev@gmail.com's Account`) |
| Zone resources | **Include → Specific zone → `dmoptiquesarl.com`** |
| TTL / IP filtering | laisser vide |

→ **Continue to summary** → **Create token** → **copie-le immédiatement** (il ne s'affiche qu'une fois).

Note aussi l'**Account ID** : Workers & Pages → colonne de droite de la page d'accueil.

> **Ce jeton n'est PAS nécessaire si tu t'arrêtes à l'étape 3.** Workers Builds publie sans jeton, avec
> l'autorisation GitHub déjà donnée. Le jeton ne sert qu'à la publication depuis GitHub Actions (§4),
> c'est-à-dire à la seule méthode qui survit à un changement de branche.

### 4.2 · Poser les deux secrets dans GitHub (1 min)

Dépôt AMK → **Settings → Secrets and variables → Actions → New repository secret** :

| Nom | Valeur |
|---|---|
| `CLOUDFLARE_API_TOKEN` | le jeton de 4.1 |
| `CLOUDFLARE_ACCOUNT_ID` | l'identifiant de compte |

### 4.3 · Créer le fichier dans `main` (1 min)

GitHub → dépôt → **Add file → Create new file** →
nom : `.github/workflows/deploy-dmoptic.yml` → **branche : `main`** → colle le contenu de
`tools/deploy/workflow-deploy-dmoptic.yml` → **Commit changes**.

> C'est le seul geste que je ne peux pas faire à ta place : GitHub refuse qu'un outil automatique
> dépose un fichier de workflow (c'est une protection contre les scripts qui modifieraient la chaîne
> de publication). Le fichier est prêt, il ne reste qu'à le coller.

### 4.4 · Fusionner la PR n°9

La PR #9 apporte `wrangler.toml` et le site (183 fichiers) dans `main`. Sans elle, les prochaines
branches n'auront pas la configuration, et le workflow échouera à la première exécution.

### 4.5 · Vérifier

Onglet **Actions** du dépôt → « Déployer DM Optique sur Cloudflare » → la dernière exécution doit être
**verte**. En cas de rouge, le journal nomme la cause en une ligne (jeton absent, nom de Worker
incorrect, dossier introuvable).

---

## 5 · À chaque nouveau chat — 30 secondes

| Si tu utilises… | Ce que tu fais |
|---|---|
| **le workflow** (§4) | **rien.** La nouvelle branche publie d'elle-même au premier envoi. |
| **Workers Builds seul** (§3) | Cloudflare → projet → *Settings → Build* → remplace la branche par celle de la conversation. |

C'est la seule différence entre les deux méthodes, et elle vaut les 4 minutes du §4.

---

## 6 · Après chaque publication — les 3 vérifications

1. `https://dmoptiquesarl.com/en/` → l'anglais.
2. `https://www.dmoptiquesarl.com/` → redirection vers l'apex.
3. Search Console → **Sitemaps** → `sitemap.xml` doit passer à *Success* (une fois la redirection en
   place, le 403 du 21/10 n'a plus de raison d'être). Détail : `../seo/URLS-INDEXATION-2026-10-21.md` §8.

---

## 7 · Ce qu'il faut retenir

- **Le site est largement dans les limites** : 183 fichiers sur 20 000.
- **La branche ne se configure pas dans `wrangler.toml`.** Elle se règle dans Cloudflare (Workers
  Builds) ou dans le workflow GitHub. Écrire une branche dans le `.toml` donnerait l'illusion d'un
  réglage — et c'est précisément le piège à éviter.
- **`_redirects` et `_headers` sont pris en charge** par les Workers avec assets (2 000 redirections,
  100 règles d'en-têtes) : la redirection `www` → apex survivra.
- **`wrangler` publie en une commande et dit ce qui ne va pas**, là où l'écran d'upload tournait sans
  rien dire.
