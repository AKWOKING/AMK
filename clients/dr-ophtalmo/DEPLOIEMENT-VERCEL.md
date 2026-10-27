# Déployer l'aperçu Dr Fogue à la main (27/10/2026)

Le fichier à télécharger : **`dr-ophtalmo-site-2026-10-27.zip`** (à la racine du dépôt, 572 Ko).
Il contient le site exactement tel qu'il doit être servi, dans un dossier `dr-ophtalmo-site/`.

## Ce qu'il y a dans l'archive, et ce qui n'y est pas

| Dedans (30 fichiers) | Dehors, et pourquoi |
|---|---|
| `index.html`, `css/`, `js/` (config, i18n, lib) | `tests/` — les 45 vérifications servent au développement, pas au visiteur |
| `assets/img/` — 8 WebP du Dr Fogue, `og.jpg`, `favicon.svg` | `assets/src/` — **7 Mo d'images générées** (portrait, examen, équipement) : elles ne sont plus chargées par la page, et les laisser dans un déploiement public rendrait téléchargeables des visages qui n'existent pas |
| `assets/fonts/` — 6 fichiers WOFF2 | |
| `robots.txt`, `llms.txt`, `_headers` | |

Contrôle avant emballage : les **12 références locales** de `index.html` et du CSS, plus les 10 chemins
d'images écrits dans `js/config/doctor.js`, sont tous présents dans l'archive. Servi depuis le dossier
dézippé, les 12 fichiers testés répondent **200**, la page affiche « Dr Fogue » 5 fois et ne contient
plus ni `portrait-960`, ni `examination-960`, ni `equipment-960`, ni `[NOM DU MÉDECIN]`.

## Route A — la CLI, sur le projet existant (recommandé)

```bash
unzip dr-ophtalmo-site-2026-10-27.zip
cd dr-ophtalmo-site
vercel link            # team AMK (amk-5d61) → projet dr-ophtalmo-preview
vercel deploy --prod
```

L'alias `dr-ophtalmo-preview.vercel.app` bascule sur cette version. Si la CLI refuse à cause du
*Root Directory* du projet (`hosting/previews/dr-ophtalmo`, réglé pour l'intégration Git), deux options :
`vercel deploy --prod --yes` depuis le dossier, ou la route B.

## Route B — un nouveau projet, sans toucher à l'existant

```bash
cd dr-ophtalmo-site
vercel deploy --prod        # répond « Link to existing project? » → No
```

Le site part sur une URL neuve, l'ancienne production reste en place : c'est la route sans risque si
tu veux comparer les deux versions côte à côte.

## Route C — le dashboard

**Add New → Project**, puis glisser le dossier `dr-ophtalmo-site` (dézippé) dans la zone d'import.
Si le glisser-déposer ne prend pas un dossier sans `package.json`, la CLI de la route A fait le travail.

## Quota

Le blocage que j'ai rencontré venait de l'API (`POST /v13/deployments`, 100 créations par jour en offre
gratuite). Une promotion d'un déploiement **existant** ne consomme rien : *Deployments → ⋯ → Promote to
Production* sur celui du commit `9930a44` suffit, et c'est plus rapide que tout ce qui précède.

## Deux choses à savoir après le dépôt

1. **`_headers` n'est pas lu par Vercel** (c'est une convention Netlify / Cloudflare Pages). Les en-têtes
   de sécurité ne s'appliquent donc pas. Si tu les veux sur Vercel, il faut un `vercel.json` — je ne l'ai
   **pas** mis dans l'archive : sa CSP (`style-src 'self'`, `form-action 'none'`) n'a jamais été testée
   dans un vrai navigateur, et l'ajouter sans mesure risquerait de casser la page qu'on vient de finir.
   À faire un jour, avec un rendu sous les yeux.
2. **`noindex` est actif**, et c'est voulu : `robots.txt` fermé, `<meta name="robots">` dans le `<head>`.
   Le jour où le Dr Fogue valide le site comme son vrai site, ces deux verrous s'ouvrent **avant** la mise
   en ligne — sinon il n'apparaîtra jamais sur Google, même avec le bon contenu.

## Refonte du 27 octobre 2026 (premier écran)

Deuxième dépôt de la même journée : le hero refait (photo de la salle d'examen en fond plein cadre,
dégradé navy à gauche, bande d'équipe à la place du portrait isolé). L'archive
`dr-ophtalmo-site-2026-10-27.zip` à la racine du dépôt a été **régénérée** : 32 fichiers, 703 Ko,
17 références vérifiées présentes. Si le glisser-déposer est utilisé, c'est cette version-là qu'il faut.

## Après le déploiement

Me le dire : je relis la page en production et je confirme point par point ce qui est passé — le nom,
les trois photographies, les quatre lieux, le samedi à l'Hôpital Charity, le JSON-LD `Physician`, et
l'absence de toute mention « image générée ».
