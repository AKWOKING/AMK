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

## 3 bis · Le build tourne, et il échoue sur une seule ligne (22/10, journal de build)

**Ce que le journal montre, et qui est une bonne nouvelle :** le build se déclenche, `wrangler` s'installe,
les assets se téléversent (`180 already uploaded`, `+ /robots.txt`)… puis **la création de la version
échoue** :

```
Invalid _redirects configuration:
Line 1: Only relative URLs are allowed. [code: 100324]
Failed: error occurred while running deploy command
```

**Deux vérités que ça établit :**

1. Workers Builds **fonctionne** : dépôt, branche, build command, deploy command, tout est branché.
2. Le coupable est **mon `_redirects`**, pas ta configuration. Il contenait
   `https://www.dmoptiquesarl.com/* https://dmoptiquesarl.com/:splat 301` — or **Workers n'accepte que
   des chemins relatifs** dans ce fichier, et surtout **`_redirects` ne compare jamais les hôtes** : une
   redirection `www` → apex ne peut pas s'y écrire, quelle que soit la syntaxe. C'était une erreur de ma
   part, appuyée sur la documentation « Pages » et non sur celle des « Workers ».

**Corrigé (commit à venir) :** le fichier `_redirects` est **supprimé** du site et du générateur. Le
déploiement ne peut plus échouer pour cette raison. Le zip repasse à **182 entrées**.

> **Détail à garder en tête :** les assets avaient bien été téléversés avant l'échec (180 fichiers
> « already uploaded »), mais **la version n'a jamais été créée** — donc le site en ligne n'a pas bougé.
> C'est exactement ce qu'on observait : `/en/` en 404, `/montures/` à l'ancienne version.

---

## 3 ter · La redirection www → apex se fait dans Cloudflare, pas dans le site

`_redirects` ne peut pas la faire. La bonne place est la **zone**, et c'est trois clics :

1. Cloudflare → **dmoptiquesarl.com** → **Rules** → **Redirect Rules** → **Create rule**.
2. **When incoming requests match** → *Custom filter expression* :
   - Field **Hostname** · Operator **equals** · Value `www.dmoptiquesarl.com`
3. **Then** → Type **Static** · URL `https://dmoptiquesarl.com` · Status **301** ·
   cocher **Preserve query string** → **Deploy**.

Alternative en un clic : dans l'écran de création, l'onglet **Templates** propose
**« Redirect from WWW to root »** — c'est exactement cette règle.

**Si tu ne la fais pas :** le site reste accessible sur les deux adresses, et le `canonical` de chaque
page pointe déjà l'apex — Google consolide. Ce n'est donc **pas bloquant** ; c'est du confort et de la
propreté.

---

## 3 quater · 🔐 Le jeton API que tu as collé dans le chat est à remettre à zéro

Le jeton `cfut_HicH…` a été **copié en clair dans la conversation**. Un jeton vaut un mot de passe : il
donne le droit de publier sur le compte Workers.

**À faire maintenant, dans cet ordre :**

1. Cloudflare → **My Profile → API Tokens** → ligne `deploy-dmoptique-github` → **Roll** (ou *Delete*).
   Le jeton affiché devient inutilisable immédiatement.
2. **Create Token → Edit Cloudflare Workers** → *Use template* → même nom, mêmes ressources →
   **Create** → **ne le colle nulle part dans un chat**.
3. Il ne va qu'à **un seul endroit** : GitHub → dépôt AMK → *Settings → Secrets and variables → Actions*
   → `CLOUDFLARE_API_TOKEN`. GitHub le chiffre, et il n'est plus jamais réaffiché.

**Et rappelle-toi : ce jeton n'est pas nécessaire pour l'étape 3.** Workers Builds publie déjà sans lui.
Il ne servira qu'à la publication depuis GitHub Actions (§4).

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
- **`_headers` est pris en charge** par les Workers avec assets. **`_redirects` aussi — mais uniquement
  avec des chemins relatifs** : aucune redirection d'hôte ne peut y être écrite. La redirection
  `www` → apex se fait dans *Rules → Redirect Rules* (§3 ter).
- **`wrangler` publie en une commande et dit ce qui ne va pas**, là où l'écran d'upload tournait sans
  rien dire.
