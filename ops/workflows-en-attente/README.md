# Workflows en attente — du travail prêt qui ne peut pas partir par git

**Pourquoi ce dossier.** Le 28/10, la poussée de `.github/workflows/deploy-dmoptic.yml` est refusée :
*« refusing to allow a GitHub App to create or update workflow … without `workflows` permission »*,
et l'API répond 403. Le fichier restait donc **modifié dans l'arbre de travail** à chaque session.

**Pourquoi ça gênait vraiment.** `tools/graphify/build_full_graph.py` lit les fichiers **suivis**
(`git ls-files`), y compris les `.yml` : un workflow modifié mais jamais commité change la carte de
plusieurs nœuds. Résultat, la porte `La machine` → « La carte du dépôt se rejoue à l'identique »
échouait à **chaque** poussée, pour une raison qui n'avait rien à voir avec le contenu livré
(28/10 : 58 lignes d'écart, puis 6). Un fichier sale en permanence rendait le vert impossible.

**Ce qui est ici.** `deploy-dmoptic.pending.yml` : la version voulue de
`.github/workflows/deploy-dmoptic.yml`, à savoir
1. la porte SEO locale dans le job `gate` (`audit_seo_local.py --self-test`, puis `--strict`) ;
2. l'étape **IndexNow** après publication, qui prévient Bing, Yandex, Seznam et Naver
   (`continue-on-error: true` : le silence d'un moteur ne retient jamais un site déjà en ligne).

**Comment l'appliquer** (deux chemins, aucun ne passe par une poussée de ma part) :

```bash
# a) dès que l'application GitHub a la permission `workflows`
cp ops/workflows-en-attente/deploy-dmoptic.pending.yml .github/workflows/deploy-dmoptic.yml
git add .github/workflows/deploy-dmoptic.yml && git commit -m "CI : portique SEO + IndexNow"
git push

# b) sinon, copier le contenu du fichier dans l'éditeur web de GitHub
#    (github.com/AKWOKING/AMK/edit/main/.github/workflows/deploy-dmoptic.yml)
```

**Ce qui tourne aujourd'hui, et ce qui ne tourne pas.** Le déploiement Cloudflare tourne (workflow
`deploy` déjà sur `main`). Le portique SEO local **ne tourne pas** dans la CI, et **IndexNow n'est pas
appelé automatiquement** : les deux pings du 28/10 ont été lancés à la main. Le site se publie
normalement sans ces deux étapes ; il ne se vérifie pas et ne prévient pas Bing.

**Le jour où c'est appliqué**, supprimer ce dossier et sa ligne dans `ops/REPO-MAP.md` se refait tout
seul (`python3 tools/graphify/build_full_graph.py`).
