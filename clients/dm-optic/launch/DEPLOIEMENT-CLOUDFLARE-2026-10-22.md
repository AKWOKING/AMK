# Déployer le site sur Cloudflare — 22/10/2026

> **Le problème, en une phrase.** Le site n'est pas trop gros pour Cloudflare : **183 fichiers, 9 Mo**,
> alors que la limite d'un Worker est de **20 000 fichiers et 25 Mo par fichier**. Ce qui bloque, c'est
> **l'outil d'envoi du tableau de bord** (« Upload static files to update your Worker ») : il n'affiche
> ni progression ni erreur, et il reste planté. On arrête donc de passer par lui.

---

## 1 · Ce que montre ta capture

| Ce que tu vois | Ce que ça dit |
|---|---|
| *Upload static files to update your Worker* | Tu es dans l'édition **manuelle des assets** d'un Worker — un outil prévu pour quelques fichiers de test, pas pour un site entier. |
| *This uploader currently only supports static assets (HTML, CSS, and JS files)* | Le bandeau avertit lui-même : **ce n'est pas l'outil normal**. Il ignore ou avale mal les images, les polices, le sitemap. |
| *Uploading 184 total file(s)* · aucune progression | Le compteur est faux dès le départ (**183 fichiers** dans le zip) : il compte un dossier ou un fichier fantôme. Signe que la liste est mal construite côté navigateur. |
| dossiers `en` 3 Mo · `montures` 5 Mo | C'est ici que ça coince : deux gros dossiers, beaucoup de fichiers, un envoi qui n'avance plus. |

**Conclusion :** ce n'est pas le site qu'il faut alléger, c'est la méthode d'envoi qu'il faut changer.
Un site statique de cette taille se publie **depuis le dépôt**, pas à la main.

---

## 2 · La bonne façon : Cloudflare construit lui-même depuis GitHub

Une fois branché, **chaque fusion dans `main` met le site en ligne tout seul** — plus de zip, plus de
glisser-déposer, plus de plantage. C'est exactement ce qu'il faut pour un site qu'on fait évoluer.

Tout est déjà préparé dans le dépôt :

| Fichier | Rôle |
|---|---|
| `wrangler.toml` | dit à Cloudflare **quel dossier** publier (`hosting/previews/dmoptic`) et **quelle page** servir sur une adresse inconnue (`404.html`) |

*(Le fichier de workflow GitHub Actions n'est pas dans le dépôt : l'outil qui pousse ce dépôt n'a pas le
droit d'y déposer des workflows. Si tu choisis la route B, le fichier est fourni en clair au § B, à
coller depuis l'interface GitHub.)*

### Route A — Workers Builds : recommandée, aucun mot de passe à créer

1. **Cloudflare → Workers & Pages →** ouvre le projet du site (celui dont le nom est en haut de la page).
2. Onglet **Settings** → section **Build** → **Connect** (ou *Connect Git repository*).
3. Choisis **GitHub** → autorise → dépôt **`AKWOKING/AMK`** → branche **`main`**.
4. Réglages de build :
   - **Build command** : *(vide)* — le site est déjà construit dans le dépôt ;
   - **Deploy command** : `npx wrangler deploy` *(c'est la valeur par défaut)* ;
   - **Root directory** : `/`.
5. **Save**. Cloudflare lance un premier déploiement dans la minute.

À partir de là : **fusion dans `main` = site à jour.** Rien d'autre à faire.

> **Pourquoi c'est la bonne route :** le nom du Worker est déjà le bon, puisque tu le connectes depuis
> la page du Worker existant. Avec la route B (ci-dessous), il faut recopier ce nom dans `wrangler.toml`
> — et se tromper créerait un **second** Worker, le domaine continuant de pointer l'ancien.

### Route B — depuis GitHub (si tu préfères tout piloter dans GitHub)

1. Cloudflare → **My Profile → API Tokens → Create Token** → modèle **« Edit Cloudflare Workers »** →
   *Continue* → *Create*. Copie le jeton (il ne s'affiche qu'une fois).
2. Récupère l'**Account ID** : Cloudflare → Workers & Pages → colonne de droite de la page d'accueil.
3. GitHub → dépôt AMK → **Settings → Secrets and variables → Actions → New repository secret** :
   - `CLOUDFLARE_API_TOKEN` = le jeton ;
   - `CLOUDFLARE_ACCOUNT_ID` = l'identifiant.
4. Vérifie que `wrangler.toml` porte **exactement** le nom du Worker existant (première ligne).
5. GitHub → **Add file → Create new file** → nom du fichier : `.github/workflows/deploy-dmoptic.yml`
   → colle exactement ceci, puis **Commit** :

```yaml
name: Déployer DM Optique sur Cloudflare

on:
  push:
    branches: [main]
    paths:
      - "hosting/previews/dmoptic/**"
      - "wrangler.toml"
  workflow_dispatch: {}

permissions:
  contents: read

concurrency:
  group: deploy-dmoptic
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Vérifier le site avant publication
        run: |
          set -e
          test -f hosting/previews/dmoptic/index.html
          test -f hosting/previews/dmoptic/sitemap.xml
          test -f hosting/previews/dmoptic/_redirects
      - name: Publier sur Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: deploy
```

6. Onglet **Actions → « Déployer DM Optique sur Cloudflare » → Run workflow**.

### Route C — depuis un ordinateur avec un terminal (3 commandes)

```bash
git clone https://github.com/AKWOKING/AMK && cd AMK
export CLOUDFLARE_API_TOKEN=...        # le même jeton qu'à la route B
npx wrangler deploy
```

`wrangler` envoie les 183 fichiers, applique `_redirects` (www → apex) et `_headers`, et ne laisse
aucune place à un plantage d'interface.

---

## 3 · Si tu veux quand même réessayer le tableau de bord

Deux erreurs possibles, dans l'ordre :

1. **Tu as déposé le dossier parent au lieu du site.** Le bon dossier est celui qui **contient
   `index.html`** — pas celui qui contient le zip, ni un dossier « dmoptic ». C'est ce qui explique le
   **184ᵉ fichier** : il y en a un de trop.
2. **Tu as déposé le `.zip`.** Cet outil-là attend des fichiers, pas une archive : le zip n'est lu
   comme un dossier par aucun navigateur.

Et si l'envoi reste planté malgré tout : **ferme l'onglet, vide le cache du navigateur, réessaie en
navigation privée**. C'est un défaut connu de cet écran, pas de ton site.

---

## 4 · Après le déploiement — les 3 vérifications

| À vérifier | Attendu |
|---|---|
| `https://dmoptiquesarl.com/en/` | la page d'accueil **en anglais** (nouveauté du 22/10) |
| `https://www.dmoptiquesarl.com/` | **redirige** vers l'adresse sans `www` |
| `https://dmoptiquesarl.com/montures/femmes/f01-ovale-doree/` | s'affiche, et la photo arrive vite (image allégée) |

Puis Search Console → **Sitemaps** : supprimer l'entrée en erreur, ressaisir **`sitemap.xml`**.
Détail : `../seo/URLS-INDEXATION-2026-10-21.md` §8.

---

## 5 · Ce qu'il faut retenir

- **Le site est dans les limites de Cloudflare**, largement : 183 fichiers sur 20 000.
- **`_redirects` et `_headers` sont pris en charge** par les Workers avec assets — c'est documenté par
  Cloudflare. La redirection www → apex fonctionnera donc dès que le site sera publié par `wrangler`.
- **Le tableau de bord n'est pas un outil de publication.** Il l'a prouvé deux fois.
