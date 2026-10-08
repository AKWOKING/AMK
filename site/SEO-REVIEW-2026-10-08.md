# AMK site (`amk-cm.vercel.app`) — revue de performance de recherche · export Search Console du 08/10/2026

Source : `https___amk-cm.vercel.app_-Performance-on-Search-2026-10-08/` (7 CSV, filtre « Web · 7 derniers jours »).
Relu contre : `site/` (dépôt), la page **en ligne** (robots, sitemap, accueil, 2 morceaux), `AMK-SEO-PLAYBOOK.md`,
`content/pipeline/KEYWORDS-2026-09-22.md`, `research/Google-Presence-AMK-2026-09-19.md`.
**Statut : suggestions uniquement — aucun fichier du site n'a été modifié.**

## 1 · Ce que l'export dit — et ne dit pas

| Mesure (29/09 → 05/10) | Valeur |
|---|---|
| Clics · impressions · CTR · position | **1 · 1 · 100 % · 3,0** (le 02/10) |
| Page | accueil `/` seule (les deux pages de service `index,follow` : **0 impression**) |
| Pays · appareil | Cameroun · mobile |
| Requêtes | **fichier vide** |

- **Un échantillon de 1 ne permet aucune conclusion.** Ni « le titre marche », ni « le SEO ne marche pas ».
- **Requêtes vides = normal ici** : Google masque les requêtes rares (anonymisées) ; elles comptent dans les totaux, pas dans le tableau.
- **Les données s'arrêtent au 05/10** (délai habituel de Search Console) : 06–08/10 absents.
- **On ne peut pas séparer les recherches de King** de celles d'un inconnu.
- **Repère du 19/09 :** 6 impressions en 3 mois · 0 clic · position 2,3. **Aujourd'hui :** 1 impression / 1 clic en 7 jours →
  **premier clic enregistré**, rythme ≈ 1 impression par semaine, soit ≈ 4–5 par mois.
- **Contrôle à 30 jours du playbook (≈ 21/10) : ≥ 20 impressions, ≥ 2 clics.** Au rythme actuel, **le seuil d'impressions ne sera pas atteint** — ce serait un manque de pages indexables (une page sert une poignée de requêtes), pas la preuve d'un mauvais titre. Le signe qui compte reste : **une requête tapée par un inconnu** (aujourd'hui, aucune visible).

## 2 · La trouvaille principale : ce que Google voit ≠ le dépôt

| | Titre |
|---|---|
| **En ligne (ce que Google indexe)** | Création de site web pour écoles & cliniques au Cameroun \| AMK · Douala · Yaoundé · Buea · Limbé (96 car.) |
| **Dépôt `site/index.html` (05/10, jamais déployé)** | Création de site web pour écoles & outils digitaux pour opticiens du Cameroun \| AMK – Douala (92 car.) |

1. **Le repositionnement du 05/10 (opticiens) n'est pas en ligne.** Il n'a touché que le `<title>`, la description et le JSON-LD ; le corps de la page parle toujours d'écoles et de cliniques (le mot « opticien » : **1 occurrence sur ~2 300 mots**).
2. **La meta description du dépôt est corrompue** (381 car., commence par « Création de Nous construisons les outils… », phrase anglaise **en double**) ; la description JSON-LD aussi (« Création de Web et solutions digitales… »). Cause probable : un remplacement de texte qui a collé deux formulations (commit `0a03e5d`). **Un déploiement du dépôt publierait ce texte tel quel.**
3. **Le site en ligne est EN AVANCE sur le dépôt** : l'accueil en ligne liste les concepts 05 (`sample-polyclinic.html`) et 06 (`sample-maternity.html`) — **absents du dépôt** (aucun fichier, aucune mention). `site/DEPLOY.md` décrit un déploiement par `amk-site.zip` : **le redéployer écraserait ces deux pages** (même piège que Le Cristallin, `hosting/previews/README.md`).
   → **Aucun redéploiement d'`amk-cm` avant d'avoir rapatrié ces deux pages dans le dépôt** (King les exporte depuis Vercel : l'orchestrateur ne peut pas les relire en HTML complet).

## 3 · Ce qu'un visiteur qui clique rencontre (même page en ligne et dans le dépôt)

| # | Constat | Gravité |
|---|---|---|
| a | **Prix périmé.** Page : « Starter — Founding **100,000 FCFA** · 2 FOUNDING SLOTS · option mensuelle **15,000 FCFA** · prix identique pour tous ». JSON-LD : `price` 100000 ×3 + `priceRange`. **Grille v3 du 05/10 : 200 000 install. + 50 000/mois, fondateurs clos.** Un inconnu arrivé de Google lit un prix que nous ne tenons plus. | **Haute** |
| b | **Affirmations sans trace au dépôt.** FAQ : « We have projects under way with institutions in Douala, Buea and Limbe, and we also work with schools in Yaoundé, Bafoussam and Bamenda » ; « Secure SSL hosting, **99.9% uptime** ». CRM : **aucun client payant** (DM Optique et Le Cristallin = « closing », acompte vide). Règle credentials (`RULE-CREDENTIAL-CLAIMS.md`) : pas de claim sans source. | **Haute** (page publique) |
| c | **Mismatch de public.** Les prospects opticiens que nous contactons arrivent sur une page écoles/cliniques ; la preuve opticien (page DM Optique) n'est pas en ligne. | Moyenne |
| d | **Langues mêlées.** `<html lang="en">` ; titre et H1 en français, neuf H2 sur onze en anglais ; la bascule EN/FR est du JavaScript sur une seule URL (aucun `hreflang`) : Google n'indexe que le texte statique. Le playbook (§7) dit que le marché cherche en français avec la ville. | Moyenne |
| e | Compte incohérent : « **Four** complete concepts » (H2) · « **six** complete concepts » (FAQ) · six cartes. | Faible |

## 4 · Suggestions, par rendement

**P0 — avant TOUT déploiement d'`amk-cm`**
1. Rapatrier `sample-polyclinic.html` et `sample-maternity.html` dans `site/` (+ `sitemap.xml`), puis comparer en ligne ↔ dépôt.
2. Remplacer la meta description et la description JSON-LD corrompues (propositions ci-dessous).
3. Aligner le bloc prix (page, FAQ « How much… », JSON-LD) sur la grille v3 — **décision de King** (on affiche ou non un prix ; les fondateurs sont clos).
4. Supprimer ou sourcer les affirmations du 3-b (je propose de les retirer ; « 99.9 % uptime » → retirer ou citer l'engagement de l'hébergeur).

**P1 — cohérence (un titre, un H1, un corps qui disent la même chose)**
5. **Titre/description : choisir UN métier par page.** Pour la page telle qu'elle est (corps écoles/cliniques) :
   - Titre (60) : `Création de site web école & clinique, Cameroun | AMK Douala`
   - Description (139) : `Votre école ou clinique est jugée sur Google avant qu'on vous appelle. Site bilingue FR|EN, rendez-vous WhatsApp, aperçu gratuit sous 24 h.`
   - Pour opticiens, **sur une page dédiée** (règle 3 du playbook), titre (56) : `Site web pour opticiens au Cameroun, avec WhatsApp | AMK` — description (138) : `Un catalogue de montures qui s'ouvre sur WhatsApp, en français et en anglais. Sites pour opticiens du Cameroun : aperçu gratuit sous 24 h.`
   - **Ne pas mettre « opticiens » dans le titre de l'accueil tant que le corps n'en parle pas** : Google réécrit les titres qui ne correspondent pas à la page, et le visiteur rebondit.
6. Langue : `lang="fr"` par défaut, H2 en français (le H1 l'est déjà) ; l'anglais reste la bascule. La niche anglophone (Buea/Limbé, playbook P2) demande **une URL distincte + `hreflang`** — plus tard.

**P2 — mesure (Search Console)**
7. Soumettre `sitemap.xml` ; **Inspection d'URL → « Demander l'indexation »** pour les deux pages de service (0 impression : à vérifier si indexées).
8. Lire les requêtes sur **3 mois / 16 mois**, pas 7 jours.
9. **Ajouter à la tâche du dimanche 20h00** : export Search Console (même format), rangé sous `research/gsc/AAAA-MM-JJ/` ; une ligne dans `ops/TOOL-SCAN.md`.

**P3 — croissance (playbook, dans cet ordre)**
10. **Une page « opticiens »** (`creation-site-web-opticien-cameroun.html`) **seulement quand la page DM Optique est en ligne et approuvée par le client** : sans preuve, c'est « mille pages vides » (règle de sûreté du playbook §7).
11. **Rétrolien utile et bon marché :** une mention « Site par AMK » dans le pied de page des sites clients (aucune n'existe aujourd'hui) — **à valider avec chaque client à la livraison** (le pied de page est déjà un point de la phase build).
12. **Profil Google d'AMK** (playbook : action 2, ~32 % du classement local ; avis ~20 %) — état **non vérifiable d'ici**, King confirme.
13. Hygiène du sitemap : `mitoc.html` (page de concept portant le nom d'un prospect) n'y est pas ; les pages modèles (« Template ») y sont à 0,6 — à décider avec le point 1.

## 5 · À trancher par King
1. Exporter les deux pages « live-only » (point 1) ? 2. Prix : afficher la grille v3, ou aucun prix sur la page ? 3. Retirer les affirmations du 3-b ? 4. Quel est le métier de l'accueil (écoles/cliniques seulement, ou accueil large + trois pages métier) ? 5. Profil Google AMK : ouvert, complet ?

## 6 · À ne PAS faire
- Promettre un volume de recherche (aucun outil de volume ici — `KEYWORDS-2026-09-22.md`).
- Créer des pages quartier/ville « pour le SEO » sans un fait vrai à y mettre (playbook §7).
- Viser « création site web Douala » en tête-à-tête avec quatre agences : le playbook l'a déjà écarté ; l'angle gagnable est le **problème vécu** (« ma page Facebook ne prend pas de rendez-vous »).
- Redéployer `amk-cm` depuis le dépôt tel quel (points 2.2, 2.3, 3-a, 3-b).

---

## 7 · Suivi du 08/10 (soir) — après l'export de King et ses réponses

**Le dépôt = le site en ligne.** King a exporté `site/` depuis Vercel (PR #5, `8ecb97d`). La copie du dépôt qui portait le repositionnement du 05/10 (titre « opticiens », description) a été remplacée ; elle survit dans l'historique git (`0a03e5d`, `afc7d52`). Elle n'a **pas** été réappliquée : la vocation de l'accueil n'est pas tranchée (question 4).

**Ce qui devient sans objet dans les §2–§3 ci-dessus**
- 2.1 « la page en ligne est en avance sur le dépôt » : résolu, les deux sont identiques.
- 2.2 « description corrompue dans le dépôt » : la corruption n'existait que dans l'ancienne copie du dépôt ; la description en ligne, relue dans l'export, est propre.
- 2.3 (pages `polyclinic` et `maternity` absentes du dépôt) : elles y sont désormais.

**Ce qui reste valable :** le §1 (n = 1, aucune conclusion), l'écart d'indexation (~1 impression par semaine), les candidats de balises T-A2 / D-A (aucun appliqué), les affirmations non sourcées du 3-b, `lang="en"` sur une page à titre français, et l'absence de la balise `google-site-verification` dans `index.html` (le fichier `google08d73756faeade69.html` assure la vérification ; il doit rester déployé).

**Rulings de King (7e message)**
- **Question 2, prix : AUCUN prix sur amk-cm.** Raison : les clients demandent des choses différentes, le prix suit le périmètre. **Fait dans le dépôt, non déployé** : voir `sales/Activity-Log.md` (08/10) pour la liste. Conséquence SEO à savoir : l'angle « prix site internet Cameroun » de `content/pipeline/KEYWORDS-2026-09-22.md` supposait qu'AMK était seul à afficher un chiffre ; il tombe. La FAQ « Combien coûte la création d'un site web au Cameroun ? » reste, avec une réponse sans chiffre (périmètre, devis écrit avant de commencer, aperçu gratuit).
- **Question 5, profil Google : ouvert.** « Complet » et l'adresse du profil restent à fournir (pour `sameAs` du JSON-LD, aujourd'hui vide).
- **Questions 3 et 4 : sans réponse.** Affirmations non sourcées (« projets en cours à Douala, Buea, Limbé », « écoles à Yaoundé, Bafoussam, Bamenda », « 99,9 % de disponibilité ») : NON modifiées. Vocation de l'accueil : NON tranchée.

**Constaté en retirant les prix** : à l'étape 5 de la page d'accueil, la version française portait une copie obsolète de la réponse de FAQ (avec le tarif mensuel) au lieu de traduire l'anglais ; remplacée par la traduction fidèle. Les pages `sample-polyclinic.html` et `sample-maternity.html` sont en `noindex,nofollow` : **volontairement non ajoutées au sitemap** (Search Console signalerait « URL soumise marquée noindex »). Si King veut les faire indexer : retirer le `noindex` ET les ajouter au sitemap, ensemble.

**Ne pas redéployer** tant que la question 3 (affirmations) n'a pas de réponse ; les prix retirés partiront avec ce même redéploiement.

