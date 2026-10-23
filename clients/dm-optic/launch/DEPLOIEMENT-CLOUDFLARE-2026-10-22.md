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

> **État au 22/10, 18 h : ✅ PUBLIÉ.** Le dépôt est connecté (`AKWOKING/AMK`), la branche de production
> est `arena/2fffee3b-amk`, Build command vide, Deploy command `npx wrangler deploy`, racine `/`.
> **Build vert** — `Success: Build completed`, version `f3288fc2`, 39 s de déploiement.
> Deux corrections ont été nécessaires pour y arriver : `name = "dmoptiquesarl"` (commit `9f5c26c`) et le
> retrait de `_redirects` (commit `617eea1`).


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

### ✅ Déployé et vérifié en ligne (22/10, commit `617eea1`)

| Vérification, faite sur le site public | Résultat |
|---|---|
| `https://dmoptiquesarl.com/en/` | **la page d'accueil anglaise**, titre « DM OPTIQUE SARL — Optometrist optician in Douala » |
| `https://dmoptiquesarl.com/en/montures/femmes/f01-ovale-doree/` | « F01 · Oval, gold », texte EN complet |
| `https://dmoptiquesarl.com/montures/femmes/f01-ovale-doree/` | « Vous aimerez aussi » traduit, textes EN dans le DOM |
| `https://dmoptiquesarl.com/sitemap.xml` | **96 URL** (48 françaises + 48 anglaises), `lastmod` au 21/10 |

Le build est donc vert, et le site publie bien le `srcset`, le miroir `/en/`, les descriptions uniques et
le schéma enrichi. **Workers Builds fait désormais son travail à chaque envoi sur la branche.**

---

## 3 ter · La redirection www → apex : **feu vert** (22/10, 18 h 20)

L'échec sur l'apex était bien un **état périmé**. Les deux sitemaps sont maintenant au vert :

| Sitemap soumis | Statut | Dernière lecture | Pages |
|---|---|---|---|
| `https://dmoptiquesarl.com/sitemap.xml` | **Success** | 21 oct. 2026 | **96** |
| `https://www.dmoptiquesarl.com/sitemap.xml` | **Success** | 21 oct. 2026 | **96** |

**96 pages découvertes, deux fois.** La découverte est faite et le sitemap ne bloque plus rien. La
redirection peut donc être posée — elle envoie désormais Google d'une adresse lue vers une adresse lue.

### Les 4 gestes

1. Cloudflare → zone **`dmoptiquesarl.com`** → *Rules* → **Redirect Rules**.
2. **Create new Single Redirect** → carte **« Redirect from WWW to root »** → **Create from template**.
3. Le modèle se remplit tout seul — **ne change rien**, c'est bon :

   | Champ | Valeur posée par le modèle |
   |---|---|
   | Rule name | `Redirect from WWW to root [Template]` |
   | Type | **Wildcard pattern** |
   | Request URL | `https://www.*` |
   | Target URL | `https://${1}` |
   | Status code | **301 - Permanent Redirect** |

   `*` capture tout ce qui suit `www.` — donc `dmoptiquesarl.com` **et** le chemin. `${1}` le remet dans
   la cible : `https://www.dmoptiquesarl.com/en/montures/` → `https://dmoptiquesarl.com/en/montures/`.
   Aucune boucle possible : la cible ne contient plus `www`.

4. **Deploy** (bouton en bas de la page).

> **Ne touche pas** à la carte existante « Redirect from HTTP to HTTPS » : elle fait un autre travail
> (le http → https) et la supprimer casserait le site.

### ✅ Vérifié le 22/10 : la redirection fonctionne

`https://www.dmoptiquesarl.com/` → `https://dmoptiquesarl.com/`. Constaté dans le navigateur, pas déduit.

**L'avertissement « This rule may not apply to your traffic » était un faux positif.** Cloudflare le
déclenche quand il ne reconnaît pas l'enregistrement `www` comme proxifié. Ici `www` et l'apex résolvent
vers **les mêmes IP Cloudflare** (`2606:4700:3036::6815:1623`, `…3037::ac43:ca3b`, v4 `104.21.22.35`) :
le trafic passait bien par le proxy, la règle s'applique.

> **Ce qu'il ne fallait pas faire :** cocher « Create a new proxied DNS record ». Ce choix ajoute un
> enregistrement au lieu de constater celui qui existe — doublon DNS, `www` hors service. On l'a écarté,
> et il n'y a rien à réparer côté DNS.

### Search Console : l'entrée `www` peut rester

**Décision : on garde les deux entrées.** Aucun risque, aucun nettoyage à faire :

| Point | Pourquoi ce n'est pas un problème |
|---|---|
| Duplicata | Le site déclare `canonical` en apex sur les 96 pages, et `www` redirige en 301. Google consolide tout seul. |
| Découverte | Le sitemap n'est qu'une **aide** à la découverte. Les 96 URL sont déjà connues, deux fois. |
| Statut | Elle peut passer au rouge (« redirect ») — c'est **cosmétique**. Un sitemap en erreur ne pénalise pas le site. |

**Ne pas la supprimer n'apporte rien ; la supprimer non plus.** Si un jour elle s'affiche en erreur,
c'est attendu : **on ne la traite pas**, on ne la resoumettra pas, on ne la supprime pas non plus.

### Pourquoi cette redirection, au fond

Le site déclare déjà `canonical` en apex sur ses 96 pages. La redirection aligne le comportement sur ce
que le site dit déjà : **une seule adresse**. Sans elle, les liens partagés en `www` (les anciens, ceux
que les clients copient) mènent à une seconde adresse que Google doit réconcilier — avec elle, il n'y a
plus qu'une porte.

## 3 quater · Filtrer Workers Builds sur le dossier du site (King, 23/10)

> **King, 23/10 : « filtre les Workers Builds Cloudflare sur `hosting/previews/dmoptic/*`. »**

**Le problème, mesuré :** chaque envoi sur une branche de conversation déclenche une construction du
Worker `dmoptiquesarl` — **même quand pas un seul fichier du site n'est touché** (cas du 23/10 : une PR de
41 fichiers, aucun dans `hosting/previews/dmoptic`, et le contrôle « Workers Builds: dmoptiquesarl »
passe au rouge). Ça salit chaque PR et ça donne l'impression d'un site cassé qui ne l'est pas.

**Pourquoi je ne peux pas le faire moi-même, et c'est à dire :** ce réglage vit dans le tableau de bord
Cloudflare (*Settings → Build → Build watch paths*), **pas** dans `wrangler.toml` — le fichier ne connaît
pas ce champ, et l'y écrire donnerait l'illusion d'un réglage appliqué. Je n'ai **aucun accès API à
Cloudflare** dans cet environnement (ni jeton, ni connecteur). C'est donc **deux champs à remplir par King**,
et c'est fait en 60 secondes.

**La marche exacte :**

1. Cloudflare → **Workers & Pages** → **`dmoptiquesarl`** → onglet **Settings** ;
2. section **Build** → **Build watch paths** (parfois nommé *Path(s)* sous *Build*) ;
3. coller, **une ligne par chemin** :

```
hosting/previews/dmoptic/*
wrangler.toml
```

4. **Save**. Le déclencheur ne se réveille plus que si l'un de ces deux chemins bouge.

**Les deux autres champs à vérifier dans le même écran, tant qu'on y est :**

| Champ | Valeur attendue | Pourquoi |
|---|---|---|
| **Production branch** | la branche de la conversation en cours | Workers Builds publie **cette** branche ; si elle est périmée, le site ne se met plus à jour (déjà arrivé le 22/10) |
| **Deploy command** | `npx wrangler deploy` | c'est ce qui publie les assets ; sans lui, build vert et site inchangé |

**Après le réglage — le contrôle qui prouve que ça marche :** pousser un commit **hors** du dossier du site
(par exemple dans `knowledge/`) et vérifier que **aucune** construction Workers ne démarre. Un réglage qu'on
n'a pas vu refuser un build n'est pas un réglage : c'est une case cochée.

**Ce qui reste vrai sans ce réglage :** le workflow GitHub Actions (`.github/workflows/deploy-dmoptic.yml`)
est déjà filtré sur `paths:` et ne publie que si le dossier change — **lui fait déjà le travail.** Le filtre
Workers Builds sert à supprimer le bruit, pas à publier.

---

## 3 quinquies · Le jeton API reste **hors du dépôt**

**Décision (King, 22/10) :** le jeton n'est pas révoqué, il est simplement **gardé local**. Il ne doit
jamais entrer dans le dépôt — ni dans un fichier, ni dans un commit, ni dans un message.

**Où il va, et où il ne va pas :**

| Endroit | Autorisé ? |
|---|---|
| Un gestionnaire de mots de passe (le tien) | ✅ |
| GitHub → *Settings → Secrets and variables → Actions* | ✅ (chiffré, jamais réaffiché) |
| Un fichier local ignoré par git (`.dev.vars`, `.env`) | ✅ — **et il reste sur ta machine** |
| Un fichier suivi par git, un commit, un message de chat | ❌ |

**État vérifié le 22/10 :** le dépôt ne contient **aucun jeton complet** (une recherche `git log -S`
sur le préfixe des jetons Cloudflare ne remonte rien) ; le fragment qui figurait dans une note interne de
ce document a été retiré. Le `.gitignore` refuse désormais `.dev.vars`, `.env*`, `*.token` et `CLOUDFLARE_*`, pour
qu'un fichier oublié sur le bureau ne parte jamais avec un `git add -A`.

> **À savoir :** le jeton n'est **pas nécessaire** à Workers Builds, qui publie avec l'autorisation GitHub
> déjà donnée. Il ne sert qu'à la route GitHub Actions (§4) — donc, tant que ce n'est pas fait, tu peux
> le garder localement sans rien perdre.

## 3 sexies · ⚠️ Ne jamais « Retry » un ancien build

**Ce qui s'est passé le 22/10 à 17 h 00** (capture du tableau de bord) : le build relancé portait le
commit **`1dfee35`** — celui d'**avant** le retrait de `_redirects`. Il a donc échoué exactement comme la
première fois, avec le même message. Ce n'est pas une régression : c'est le même commit, relancé.

| Bouton | Ce qu'il fait | À utiliser ? |
|---|---|---|
| **Retry build** (sur un build rouge) | rejoue **le commit de ce build-là**, à l'identique | ❌ jamais sur un ancien commit |
| **New deployment** (en haut à droite) | construit **la tête de la branche** (dernier commit) | ✅ |
| Rien | un `push` sur la branche déclenche un build neuf | ✅ (c'est le fonctionnement normal) |

**Comment savoir quel commit un build construit :** la ligne sous le titre, à côté du nom de la branche
(`arena/2fffee3b-amk  ·  1dfee35  ·  Manually deployed`). Si ce n'est pas le dernier commit poussé,
c'est un build périmé — on ne le relance pas, on en crée un nouveau.

**Le site en ligne, lui, était déjà bon.** Le déploiement du commit `617eea1` avait abouti (vérifié :
`/en/` en anglais, sitemap à 96 URL). Un build rouge sur un commit périmé ne défait pas un déploiement
réussi — il occupe seulement le badge « Latest build failed ».

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
3. Search Console → **Sitemaps** : l'entrée de l'apex doit être **Success, 96 pages**. L'entrée `www`
   disparaît après la mise en place de la redirection (§3 ter). Détail : `../seo/URLS-INDEXATION-2026-10-21.md` §9.

---

## 7 · Ce qu'il faut retenir

- **Le site est largement dans les limites** : 183 fichiers sur 20 000.
- **La branche ne se configure pas dans `wrangler.toml`.** Elle se règle dans Cloudflare (Workers
  Builds) ou dans le workflow GitHub. Écrire une branche dans le `.toml` donnerait l'illusion d'un
  réglage — et c'est précisément le piège à éviter.
- **`_headers` est pris en charge** par les Workers avec assets. **`_redirects` aussi — mais uniquement
  avec des chemins relatifs** : aucune redirection d'hôte ne peut y être écrite.
- **La redirection `www` → apex se pose maintenant** (§3 ter) : les deux sitemaps sont au vert, 96 pages
  chacun. Une seule entrée à garder ensuite dans Search Console : celle de l'apex.
- **`wrangler` publie en une commande et dit ce qui ne va pas**, là où l'écran d'upload tournait sans
  rien dire.

---

## 6 · 23/10/2026 — « j'ai changé la branche, rien ne s'est passé »

**Ce qui s'est réellement passé, minute par minute** (relevé sur les *check runs* GitHub, app
`cloudflare-workers-and-pages`, projet `dmoptiquesarl`, compte `fa5fe266d7198ea5dc98567329d932fd`) :

| Heure UTC | Commit | Résultat |
|---|---|---|
| 04:34–04:36 | `b68239e`, `489340f`, `479b508` | échec (avant le changement de branche : rien à publier) |
| **04:48:25** | **`e30dadb`** | **succès — Version ID `79223b1f-1d52-4fba-9b36-07899017b26b`** |
| 04:50:01 | `69e196b` | échec |
| 04:53:19 | `788199b` | échec |

**Changer la branche ne déclenche aucun build** : Cloudflare publie à chaque **envoi** sur la branche
de production. Le premier envoi après le réglage a donc été le vrai déclencheur — et il a réussi. Le
site en ligne porte bien les correctifs du 23/10 : `https://dmoptiquesarl.com/llms.txt` contient
désormais la section `## English pages` (47 URL), qui date du même commit que le menu mobile, les
icônes et les cartes JPEG.

**Les builds suivants, eux, échouent en une seconde**, sans version produite et sans annotation : le
rapport GitHub ne contient que le *Build ID*, pas la sortie du build. Deux symptômes, une cause
probable : la commande de déploiement est `npx wrangler deploy`, et `npx` demande confirmation avant
d'installer un paquet absent — dans un runner non interactif, il s'arrête aussitôt. D'où l'échec
instantané.

**Correctif (un champ, 30 secondes)** : Workers & Pages → `dmoptiquesarl` → **Settings → Build →
Deploy command** :

```
npx --yes wrangler@4.152.0 deploy
```

Puis **New deployment** (ou *Retry* sur le build rouge). Si l'échec persiste, la ligne rouge du build
dit laquelle des causes restantes s'applique : jeton absent, nom de Worker différent, dossier
introuvable, quota de builds. **Cette ligne, je ne peux pas la lire d'ici** : le tableau de bord
Cloudflare demande une session, et le sandbox n'a ni jeton ni accès réseau à `api.cloudflare.com`.

**Et le correctif durable**, celui qui rend la question sans objet : le workflow
`.github/workflows/deploy-dmoptic.yml` (versionné dans `tools/deploy/workflow-deploy-dmoptic.yml`,
parce qu'un GitHub App sans permission `workflows` ne peut pas le pousser). Il vise `arena/**`, lance
la porte de livraison **avant** la publication et épingle `wranglerVersion: 4.152.0`. Il demande deux
secrets (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` = `fa5fe266d7198ea5dc98567329d932fd`) et un
copier-coller dans `main`.

### 6 ter · 23/10, 06:21 — la chaîne automatique est en place, et elle est verte

Commit `591a0ce` sur `main` (le workflow enfin au bon chemin) → **run `39905310242`** :

| Job | Durée | Résultat |
|---|---|---|
| Porte de livraison (--strict) | 25 s | ✅ (témoin 15/15 + `audit_delivery.py --strict` rc=0) |
| deploy (`cloudflare/wrangler-action@v3`, wrangler 4.152.0) | 37 s | ✅ — `wrangler deploy` sort en 0, le site est publié |

**Le rouge qui reste n'est pas cette chaîne.** C'est l'ancienne intégration **Workers Builds**, qui part
sur le même envoi, vers le même Worker, et échoue **en 0 seconde** : elle n'a pas le temps de compiler
quoi que ce soit, elle se heurte au déploiement déjà en cours (`Build ID l46404e7-154f-41d2-a517-a706c7e677ae`,
aucune version produite).

**À faire une fois (10 s)** : Workers & Pages → `dmoptiquesarl` → **Settings → Build → Disable builds**
(la bascule déjà visible sur la capture). À partir de là :

- un seul mécanisme publie ;
- plus de croix rouge sur chaque envoi ;
- plus de nom de branche à tenue à jour ;
- **aucun P1/P2 ne peut partir en production** : la porte s'exécute avant `wrangler deploy`, dans le
  même workflow.

Alternative si King préfère garder Workers Builds : remplacer sa Deploy command par
`npx --yes wrangler@4.152.0 deploy` **et** couper les envois automatiques du workflow (`on: workflow_dispatch`
seulement) — deux mécanismes qui publient en même temps se disputeront toujours le même Worker.

---

## 7 · Ce que la nuit du 23/10 a appris sur la chaîne de déploiement

``` 
Constat   un déploiement a bien eu lieu à 04:48 UTC ; les trois pushes suivants ont échoué en ~60 s.
Preuve    curl -sI https://dmoptiquesarl.com/dm-logo.webp
          → cache-control: public, max-age=31536000, immutable · cf-cache-status: HIT
          curl -s https://dmoptiquesarl.com/404.html | grep -c 'class="mnav'
          → 1  (le menu mobile n'est dans aucun build antérieur au 23/10)
```

**Le piège de l'interface.** Changer la *branche de production* (Settings → Builds & deployments)
**ne déclenche aucun déploiement** : c'est le **push** qui déclenche. Un déploiement lancé à 04:45
pour tester la branche, trois minutes avant le push décisif de 04:48, montre donc l'ancien site — et
on croit que « rien ne s'est passé ».

**La panne suivante, probable et non prouvée.** Après 04:48, chaque push échoue en ~60 s, sans
message dans le check GitHub ; l'erreur n'est visible que dans `dash.cloudflare.com`. Le suspect n° 1
est l'installation non interactive de `npx wrangler` (la commande de déploiement tire la dernière
version à chaque build) :

```
Deploy command : npx --yes wrangler@4.152.0 deploy
```

**La sortie durable** : `tools/deploy/workflow-deploy-dmoptic.yml`, un workflow GitHub Actions
(`workflow_dispatch` + push sur `main`, limites de concurrence, portique de livraison avant le
déploiement, vérification `curl` du `cache-control` après). Il n'est **pas** dans `.github/workflows/`
parce que l'App GitHub utilisée ici n'a pas la permission `workflows` : deux tentatives (git push,
API `contents`) ont répondu **403**. Il doit être collé par King sur `main`, avec les secrets
`CLOUDFLARE_API_TOKEN` et `CLOUDFLARE_ACCOUNT_ID` (`fa5fe266d7198ea5dc98567329d932fd`).
