# AMK — optimisation du site `amk-cm.vercel.app`

```
Exécuté  22/10/2026 (soir) — corrections appliquées dans site/, déploiement NON fait (voir §7)
Relevé   22/10/2026, sur le site EN LIGNE (pas sur le dossier local — les deux diffèrent)
Constat  la passe SEO du 08/10/2026 n'a jamais été déployée. Le public voit encore la v01.
Principe ce qui se corrige ici ne coûte rien : que du texte et des attributs.
```

---

## 1 · Les cinq erreurs visibles par un visiteur

| # | Ce qu'on lit en ligne | Pourquoi c'est faux | Correction |
|---|---|---|---|
| 1 | « **En ligne en 3–5 jours** » — **8 occurrences** | on ne l'a pas tenu : DM Optique a pris un mois. C'est l'engagement le plus vérifiable de la page, et c'en est le plus fragile | retirer le chiffre, dire **« un site livré, pas un site promis »**, et laisser la date au devis |
| 2 | « En ligne en **5–7 jours** » (offre Croissance) | même problème, en plus long | idem |
| 3 | **Compteurs à 0** : « 0 langues », « 0 sites concepts », « 0h » | le chiffre s'anime en JS ; si le script ne tourne pas (réseau lent, aperçu Facebook, lecteur d'écran) le visiteur lit **zéro**. Un zéro est pire que pas de compteur | **écrire les chiffres en dur** dans le HTML ; l'animation devient un bonus |
| 4 | « **Quatre** concepts… trois pour les écoles » | **six** sont listés juste en dessous | corriger le cardinal, il se voit à l'œil nu |
| 5 | « Aperçu **24 h** » sur le bouton et dans trois réponses | nous nous sommes donné la règle : build ≤ 15 min, relecture ≤ 1 h. « 24 h » promet plus que ce qu'on veut tenir | « aperçu **le jour même**, sur WhatsApp » |

**Le point 3 est le plus coûteux, et le moins cher à réparer.** Un aperçu de lien Facebook ou WhatsApp affiche souvent la page sans exécuter le JavaScript animé : nos propres partages donnent donc l'image d'une agence à zéro partout.

---

## 2 · Ce qui est déjà bon — ne pas y toucher

Vérifié dans le HTML : `lang="fr"` · titre de 63 caractères · description de 139 caractères · images en **WebP** · **un seul bloc JSON-LD** (pas de doublon) · `og:image` et `og:url` remplis avec le bon domaine · page `mitoc` en `noindex` · 3 liens `wa.me` avec message pré-rempli · formulaire qui **ouvre WhatsApp** sans envoyer de données.

C'est au-dessus de la moyenne locale. Le problème n'est pas la base, c'est **la version en ligne**.

---

## 3 · Ce qui manque, par ordre de rendement

| Priorité | Manque | Effet | Effort |
|---|---|---|---|
| **1** | **Déployer** la version corrigée | tout le reste est théorique sans ça | 10 min |
| **2** | **Aucun lien vers nos réseaux sociaux** dans le pied de page | nos visiteurs ne peuvent pas nous suivre ; on vient d'ajouter ces liens à **97 pages** de DM Optique et pas à la nôtre | 15 min |
| **3** | **L'anglais n'est pas indexable** — pas « il manque des `hreflang` » | ⚠️ **correction du 22/10 : la première rédaction de cette ligne était fausse.** Il n'y a **pas deux URL** FR et EN mais **une seule**, dont le texte anglais vit dans des attributs `data-en` que Google n'exécute pas. Des `hreflang` n'auraient donc rien à déclarer. Conséquence réelle : le site est vu **en français seulement** par les moteurs, alors que les écoles et cliniques du Nord-Ouest et du Sud-Ouest cherchent en anglais. Le vrai correctif est un miroir `/en/` avec de vraies URL (c'est ce qui a été fait pour DM Optique : 48 pages + `hreflang`). **Coût réel : plusieurs heures, pas 20 minutes** | à planifier |
| **4** | Accueil = **écoles + cliniques seulement** | c'est **voulu** (décision du 08/10 : pas d'opticiens dans le titre tant que DM Optique n'est pas approuvé). Une page **opticiens** se crée après | après DM Optique |
| **5** | **Fiche Google** AMK | impossible à vérifier d'ici — à faire par King sur place | 30 min |
| **6** | Adresse **Gmail** comme contact | contredit la promesse (voir `brand/AMK-PRESENCE-2026-10-22.md` §3) | à décider |

---

## 4 · Le détail qu'on ne voit pas mais qui compte

Le site contient **`img/nova.webp`** et **`og-cover.jpg`** dans ses concepts. Or **`nova` est le nom d'une école fictive** utilisée comme démonstration : c'est bien, et c'est étiqueté. Le risque n'est pas là.

Le risque est ailleurs : **un concept fictif présenté comme un client**. La page dit « noms fictifs, nous ne montrons jamais le site d'un client sans accord écrit » — **cette phrase doit rester**, c'est elle qui protège. Ne jamais la raccourcir au moment de gagner de la place.

---

## 7 · Journal d'exécution — 22/10 (soir)

| # | Correction | État |
|---|---|---|
| 1 | Promesse « 3–5 jours » / « 5–7 jours » / « en une semaine » | ✅ **retirée partout** — `index.html`, les deux pages métier, la page concept maternelle, et jusqu'aux `og:`/`twitter:` et au JSON-LD (c'est là que Google la lisait) |
| 2 | Compteurs à 0 (« 0 langues », « 0 sites concepts ») | ✅ **le chiffre est dans le HTML** ; l'animation ne fait plus que le rejouer. Un aperçu de lien ou un lecteur d'écran lit désormais 24 h / 2 langues / 6 concepts |
| 3 | « Quatre concepts » alors que six sont montrés | ✅ **« Six concepts »**, et « trois pour les écoles, **trois** pour les cliniques » (FR et EN) |
| 4 | Carte de statistique qui promettait « 3–5 jours » | ✅ remplacée par **« 100 % — à vous : domaine, fichiers, hébergement »**, vrai et vérifiable sur la page |
| 5 | Réponse FAQ « combien de temps ? » | ✅ réécrite : « Nous ne donnons pas de date avant de connaître le périmètre. L'aperçu est dans votre téléphone sous 24 heures ; la mise en ligne suit vos validations. » |
| 6 | `amk-site.zip` périmé | ✅ reconstruit (`hosting/build_site_zip.py`), 4,0 Mo, cohérent avec `site/` |

**Vérifications passées** : `audit_seo` et `audit_html` verts sur les 4 pages modifiées (sauf
`sample-nursery.html`, qui porte **5 contrastes insuffisants préexistants** — non touchés, c'est un
choix de design de la démo).

**⚠️ Ce qui n'est pas fait : le déploiement.** Voir le §5 ci-dessous — il reste à la main de King.

---

## 5 · Le plan de déploiement, sans risque

1. **Comparer** le dossier `site/` et `amk-site.zip` (22/10 14:16, 4,0 Mo, 28 fichiers, dont 6 `img/*.webp`) : publier **le plus récent**, pas les deux.
2. **Déployer en prévisualisation** d'abord (`vercel deploy` sans `--prod`) et relire la page sur téléphone.
3. Vérifier les cinq points du §1 **sur l'URL de prévisualisation**, pas dans l'éditeur.
4. Passer en production.
5. **Redemander l'indexation** dans la Search Console, et repasser le partage dans le *Facebook Sharing Debugger* (le cache Open Graph garde l'ancienne image plusieurs jours).

**Ne pas publier depuis un dossier dont on n'est pas sûr** : c'est comme ça qu'on écrase une correction par une version plus ancienne.

---

## 6 · Ce que je ne peux pas faire d'ici — vérifié le 22/10 au soir

- **Déployer.** Le connecteur Vercel atteint bien l'équipe (`amk-5d61`) et le projet `dm-optique-sarl`,
  mais **aucun projet `amk-cm` n'est visible** : ni par identifiant, ni par recherche. Je ne peux donc
  pas publier ce que je viens de corriger. **Il reste 2 minutes de travail pour King** (voir §8).
- **Créer ou vérifier la page Facebook** : `facebook.com/amkweb` répond **403** à toute requête
  automatique (Facebook ferme l'accès aux robots), et il n'y a pas de navigateur ici.
- **Vérifier la fiche Google** d'AMK.
- **Voir le site comme un visiteur** : je lis le HTML, je ne le regarde pas.

---

## 8 · Les 2 minutes de King — publier les corrections

Le dossier `site/` est à jour dans le dépôt ; le zip aussi. Au choix :

1. **Si le projet `amk-cm` est relié à GitHub** : fusionner la branche suffit, Vercel redéploie seul.
   Un commit vient de partir — vérifier dans Vercel qu'un déploiement apparaît pour ce projet.
2. **Sinon, à la main** : ouvrir le projet `amk-cm` dans Vercel → *Deployments* → glisser le contenu de
   `site/` (ou le `amk-site.zip` reconstruit) → publier.
3. **Puis, dans l'ordre** : ouvrir `amk-cm.vercel.app` sur téléphone et vérifier les quatre points —
   plus de « 3–5 jours », les compteurs affichent 24 / 2 / 6, « Six concepts », et la FAQ répond sans
   date. Enfin, repasser le lien dans le *Facebook Sharing Debugger* (le cache garde l'ancienne image).

Tout le reste du §2 et du §3 est faisable maintenant, dans le dépôt.

---

## 9 · Audit complet du 22/10 (tour 55) — design, SEO, storytelling

> **Commande de King :** « read all the design, SEO, storytelling then audit our website using all the tools
> and skills available ». Ce §9 est le rapport. Il ne remplace pas le §7 (les corrections du soir) : il **le
> vérifie**, et il ajoute ce que les portiques ont trouvé après le déploiement.
>
> **Le site est en ligne et à jour.** `fetch_page https://amk-cm.vercel.app/` (22/10) montre bien la version
> `e67402c` : délais retirés, « Six concepts », FAQ réécrite. **C'est King qui déploie désormais, à la main.**
> Les corrections ci-dessous sont dans le dépôt et dans `amk-site.zip` (3,9 Mo, reconstruit à 16 h 30) —
> **elles ne sont pas encore en ligne.**

### 9.1 · Ce qui a réellement tourné

| Outil | Sur quoi | Résultat |
|---|---|---|
| `tools/ops/wake.py` | état du dépôt | branche à jour, arbre = dépôt |
| `PRE-FLIGHT.md` | lu **en entier** (353 l.) | — |
| `impeccable detect --json` (0.1.16) | 3 pages réelles | **32 → 25 findings** |
| `tools/qa/audit_site_amk.py` *(écrit ce tour)* | 10 pages | **10 → 0** |
| `audit_html.py` | 12 pages | 3 pages réelles **0** ; 42 findings de contraste sur 6 démos |
| `audit_a11y.py --strict` | 6 pages | 3 pages réelles **0** ; 2 démos réparées (12 champs) |
| `audit_seo` · `audit_aeo` · `audit_hero` · `audit_images` · `check_inline_js` | 3 pages réelles | **0 faute partout, rc 0** |
| `audit_claims.py` | 3 pages + dossier DM | règle corrigée, **AMK 3/3 OK**, DM inchangé sur le fond |
| `test_amkcm_lang.mjs` | `index.html` | **tout est vert** (la bascule FR|EN ne perd plus d'attribut) |
| `gate-dm.sh` | porte du jour | **PORTE : OK**, 0 rendu périmé |
| `hosting/build_site_zip.py` | paquet de déploiement | zip reconstruit, 3,9 Mo |
| `fetch_page` | le site en ligne | à jour, mais révèle 7 phrases cassées (§9.2 n° 1) |
| Skills réinstallés | `taste-skill`, `ecc` (6), `ui-ux-pro-max`, `design-motion-principles`, `impeccable` | **le bac les efface à chaque session** — réinstallés avant l'audit |

### 9.2 · Ce que j'ai corrigé aujourd'hui (16 correctifs, tous vérifiés par un portique)

| # | Défaut trouvé | Trouvé par | Correction | Fichier(s) |
|---|---|---|---|---|
| 1 | **7 phrases cassées** laissées par mon remplacement en masse du 22/10 (« Site complet en ligne **en dès** votre validation », étape 5 finissant sur une virgule) | `fetch_page` du live | phrases reconstruites une par une | `index.html`, les 2 pages métier |
| 2 | **« En ligne en 3 à 5 jours après l'acompte » toujours en français**, alors que l'anglais disait déjà « as soon as you approve » — la promesse retirée au §7 survivait dans une seule langue, **en ligne** | nouveau contrôle §20.8ter | « En ligne dès votre validation » | 2 pages métier |
| 3 | « il is yours in **3 to 5 days after the deposit** » dans les pieds de page de 3 démos | `grep` ciblé après le n° 2 | « it is yours » | `clinic-bonaberi`, `mitoc`, `sample-secondary` |
| 4 | **Phrase française injectée dans une chaîne anglaise** : « One WhatsApp message starts the **24h après validation du brief** free preview » | nouveau contrôle §20.8ter | « … starts the free preview » | `sample-school` (×2) |
| 5 | Contraste **3,93:1** : le sous-titre héritait du slate `#64748B` sur le navy `#0B1120` (WCAG AA = 4,5:1), dans le hero **et** dans `.process` / `.audit` | `impeccable` (low-contrast) + calcul | `#CBD5E1` → **12,68:1** | `index.html` |
| 6 | Contraste **3,11:1** : le CTA ambre du menu mobile en gris `#5C5C5C` sur `#F59E0B` | `impeccable` (gray-on-color) | `#0F172A` → **8,31:1** | `index.html` |
| 7 | **41 blocs `opacity:0`** (`.rv`) : si le JS échoue, la page reste vide — aucun garde-fou | `audit_site_amk` §13 + `impeccable` (buried-raster) | `html.js .rv` + une ligne de JS dans le `<head>` | `index` + 5 démos |
| 8 | **Bascule FR qui efface les signatures de témoignages** : un élément bilingue dans un élément bilingue (`innerHTML` du parent) | nouveau contrôle §20.8bis | citation dans un `<span>` bilingue, signature hors du parent | `sample-school` (4 citations) |
| 9 | **12 champs de formulaire sans `<label for>`** (WCAG 3.3.2, niveau A) | `audit_a11y --strict` (rc=1) | `for="…"` sur les 12 | `sample-school` (7), `sample-nursery` (5) |
| 10 | `prefers-reduced-motion` **absent** alors que la page utilise `scroll-behavior:smooth` | `audit_site_amk` §13 | bloc ajouté | 2 pages métier |
| 11 | Mots bannis §11b dans le texte visible : **« Solutions Digitales »** (slogan : **36 occurrences dans 8 fichiers**, attributs et texte visible) et « world-class » | `audit_site_amk` §11b | « **Sites web pour écoles et cliniques** » / « Websites for schools and clinics » | 3 pages réelles + 5 démos |
| 12 | **Deux noms d'entreprise** dans le JSON-LD (`AMK` vs `AMK – Web Development & Digital Solutions`) | lecture du JSON-LD | un seul nom : **`AMK`** | 3 pages + démos |
| 13 | Pied de page de `sample-maternity` **sans aucun contact** (§20.6) | `audit_site_amk` §20.6 | ligne WhatsApp / téléphone | `sample-maternity` |
| 14 | Texte visible ≠ attribut : « corrections faites » / « **les** corrections faites », `Demo / concept:` vs `—` | `audit_site_amk` §20.8 | alignés | `école`, `clinic-bonaberi` |
| 15 | `sitemap.xml` : `lastmod` au **08/10** alors que le contenu a changé le 22/10 | lecture du sitemap | `2026-10-22` sur les 3 pages modifiées | `sitemap.xml` |
| 16 | Promesse de classement : « des sites de clinique qui **vous placent en premier** » | `grep` après la grille SEO §0 | « qu'on trouve quand on cherche votre spécialité » | `index.html` |

**Quatre de ces défauts (n° 2, 3, 4, 16) étaient invisibles aux portiques d'hier** : ils ne cassent pas le HTML,
ils ne cassent pas la mise en page — ils changent ce que le site **promet**. D'où les trois nouveaux contrôles
de `audit_site_amk.py` : §20.8bis (bilingue imbriqué), §20.8ter (parité des délais EN/FR), et le garde-fou
`html.js`.

### 9.3 · Design — ce qui reste, et mon avis

| Constat | Où | Gravité | Mon avis |
|---|---|---|---|
| `icon-tile-stack` ×3 : pastille d'icône au-dessus d'un `h3` | `index` (3 cartes « problème ») | slop, faible | Le motif est daté (2021). Le remplacer par l'icône **en ligne avec le titre** ou pas d'icône du tout. À faire avec une maquette, pas à l'aveugle. |
| `dark-glow` ×2 : halo ambre rayonnant | hero, section audit | slop, faible | **Assumé** : c'est le halo de marque, il porte la pastille WhatsApp et le hero. Je le garde, je le note. |
| `marquee` en boucle infinie | bande « sites vitrines » | gêne, moyen | Pause au survol et au focus déjà présente, `prefers-reduced-motion` respecté. Alternative : arrêter la boucle après un tour. **À trancher par goût, pas par règle.** |
| `codex-grid-background` : grille à deux axes | hero | slop, faible | Un seul endroit, très discret. Assumé. |
| `numbered-section-labels` ×6 (« 1 · Classes » … « 6 · WhatsApp ») | 2 pages métier | advisory | **Je les garde** : ils servent de sommaire sur une page à six étapes. La règle vise le décor qui remplace la structure ; ici la structure existe. |
| `tiny-text` 11,2 / 11,5 px | `index` (étiquettes de service, consentement du widget) | advisory | 11,2 px est au plancher. Le consentement à 11,5 px est du petit texte légal : acceptable. |
| `low-contrast` 3,6:1 `#64748B` sur `#131b2b` | `index` | **non localisé** | `impeccable` ne donne pas le sélecteur et il n'y a pas de navigateur ici. Le hero et les sections sombres sont corrigés (n° 5) ; reste un texte slate sur un fond qui n'existe nulle part tel quel dans la CSS (`#131b2b` ≈ navy4 + voile). **À revérifier à l'œil au prochain passage.** |
| **42 contrastes insuffisants dans les 6 démos** | `sample-school` 12, `sample-secondary` 13, `mitoc` 5, `sample-nursery` 5, `mockup-hero` 5, `clinic-bonaberi` 2 | réel | Ce sont les pages qu'on montre aux prospects. Chaque finding donne le sélecteur et le ratio (`audit_html`), donc c'est mécanique — mais c'est une passe de 2–3 h et elle touche à la palette de chaque démo. **Je ne l'ai pas faite à l'aveugle.** Exemple : `.facility .eyebrow` 4,09:1 (ambre sur vert), `.stat .demo` 3,54:1. |

### 9.4 · SEO — les 11 étapes de la liste maison, une par une

| # | Étape | État au 22/10 | Preuve / reste à faire |
|---|---|---|---|
| 1 | Une langue par défaut écrite dans le HTML | ✅ | `<html lang="fr">`, texte FR statique, `test_amkcm_lang.mjs` vert. **Limite connue : une seule URL.** |
| 2 | Titre + description écrits à la main | ✅ | `audit_seo` rc 0 sur les 3 pages ; titres ≤ 65 car., descriptions ≤ 155. |
| 3 | Un nom d'entreprise identique partout | ⚠️ corrigé **côté site** | JSON-LD unifié sur `AMK`. **Reste : le nom exact de la fiche Google** — je ne peux pas la lire d'ici. |
| 4 | JSON-LD valide, sans note inventée | ✅ | Aucun `aggregateRating` hors commentaire de consigne. 4,9/87 avait été retiré le 08/10. |
| 5 | Images WebP, `alt` descriptif, `fetchpriority` | ✅ | `audit_images` rc 0 (8 + 3 + 2 images). |
| 6 | Pages de travail et de prospects en `noindex` | ⚠️ **à trancher** | `mitoc`, `mockup-hero`, `sample-maternity`, `sample-polyclinic` : `noindex` ✅. **Mais `sample-school`, `sample-secondary`, `sample-nursery`, `clinic-bonaberi` sont indexables** — des établissements **fictifs** avec des témoignages inventés. Voir §9.7. |
| 7 | Sitemap + `robots.txt` + fichier Search Console | ✅ | 7 URLs, aucune page `noindex`, `lastmod` corrigé ce jour ; le fichier Google est dans le zip. |
| 8 | Chaque chiffre a une source | ✅ | `audit_claims` rc 0. |
| 9 | Portiques avant livraison | ✅ | `audit_html`, `audit_a11y --strict`, `check_inline_js`, test de bascule : tous verts sur les 3 pages réelles. |
| 10 | Si l'adresse change, reconstruire `og:`/`canonical` | — | Pas de changement d'adresse. |
| 11 | Après mise en ligne : demander l'indexation, juger à 30 jours | ⏳ **King** | « Demander une indexation » sur les 3 pages modifiées + `sitemap.xml`. |

**Le seul vrai manque structurel reste l'anglais.** Le texte anglais vit dans des attributs `data-en` que
Google n'exécute pas : le site ne peut pas se classer sur « website design Buea ». Le correctif est un miroir
`/en/` avec de vraies URLs et `hreflang` — exactement ce qu'on a fait pour DM (48 pages). C'est un chantier
d'une demi-journée, et il se vend.

### 9.5 · Storytelling — la grille StoryBrand (SB7), appliquée à l'accueil

| Élément | Présent ? | Où / ce qui manque |
|---|---|---|
| **Un personnage** (le directeur d'école, la gérante de clinique) | ✅ | « Votre école est jugée sur Google » — le héros est le client, pas AMK. |
| **Un problème** (externe, interne, philosophique) | ✅ | Externe : invisible sur Google. Interne : « ils s'arrêtent chez votre concurrent ». Philosophique : une école sérieuse ne devrait pas dépendre d'une page Facebook. |
| **Un guide** (empathie + autorité) | ⚠️ **moitié** | Empathie : oui (« les parents cherchent avant de visiter »). **Autorité : non** — 0 avis, 0 client livré, aucun prix, aucun nom de client. Les 6 concepts sont la seule preuve, et ils sont fictifs. **C'est le trou du récit, et il est normal : il se bouche avec le premier client, pas avec des adjectifs.** |
| **Un plan** | ✅ | 4 étapes + une section « processus » de 5 étapes. C'est la partie la plus solide de la page. |
| **Un appel à l'action** | ⚠️ | Un CTA clair et répété (« Recevoir mon aperçu gratuit »), **mais deux CTA dans le hero** : le second (« Ouvrir un site concept ») envoie le prospect ailleurs avant qu'il ait lu la promesse. |
| **L'échec évité** | ✅ | « ils s'arrêtent à la porte de votre concurrent ». |
| **Le succès** | ⚠️ | « 100 % à vous : domaine, fichiers, hébergement » — vrai mais **technique**. Le succès du client (plus d'appels, moins de questions répétées) n'est pas montré, faute de mesure réelle. |

Ce que j'en retiens, et qui n'est pas dans les portiques : **la page ne ment pas, et c'est sa force**. Elle
n'invente ni avis, ni nombre de clients, ni délai. Le prix à payer est un trou d'autorité au milieu du récit.
Deux façons honnêtes de le boucher : (a) le premier client, filmé et cité ; (b) un **avant/après** de la fiche
Google d'AMK elle-même, avec des captures de Search Console — la seule preuve qui ne demande personne.

### 9.6 · Ce que je n'ai pas pu exécuter — et qui ne doit pas être lu comme « fait »

- **Aucun navigateur dans le bac.** Donc : pas de capture d'écran, pas de test à 390 px et 360 px, pas de
  Lighthouse ni de Core Web Vitals sur le site en ligne, **et aucune vérification à l'œil de mes corrections
  CSS**. Je les ai prouvées par le calcul de contraste et par les portiques, pas par l'image.
- **`impeccable detect` en CLI seulement.** Les règles « URL » (rendu réel, débordements, cibles tactiles)
  n'ont pas tourné.
- **Search Console** : pas d'accès. Impossible de confirmer l'indexation des 3 pages ni de voir les requêtes.
- **La fiche Google** : pas lue. Le nom exact qu'elle porte n'est donc pas vérifié (cf. étape 3).
- **Facebook** : `403` comme d'habitude ; la vérification du §3bis reste un geste au téléphone.
- **Les 42 contrastes des démos** : mesurés, **non corrigés** (§9.3).

### 9.7 · Trois arbitrages pour King

1. **Les 4 démos indexables** (`sample-school`, `sample-secondary`, `sample-nursery`, `clinic-bonaberi`) portent
   des noms fictifs et des témoignages inventés. Une balise `Review` inventée met en cause tout le domaine ;
   ici il n'y a pas de balise, mais la page reste indexable. **Deux options :** les passer en `noindex` et les
   montrer uniquement par lien direct — ou les garder indexables en rendant le bandeau « démo » plus explicite
   pour un visiteur qui arrive de Google. *Mon avis : `noindex` sur les quatre, et le sitemap ne garde que
   l'accueil et les deux pages métier.*
2. ~~**Nos liens sociaux dans le pied de page** (Instagram / Facebook / TikTok)~~ — **fait le 23/10, tour 61.**
   Les trois pastilles (logos seuls, pas de texte, nom accessible au lecteur d'écran) sont posées sur les
   **trois pages réelles** par `tools/site/add_amk_social.py`, avec les trois adresses dans le `sameAs` du
   JSON-LD. Les neuf concepts (`sample-*`, `clinic-bonaberi`, `mitoc`) restent **sans** nos icônes : ce sont
   les identités de clients fictifs ou prospects, et la règle « le site ne montre que du vrai » s'y applique.
   Détail et arbitrages : `brand/AMK-PRESENCE-2026-10-22.md` §16.
3. **La ligne de crédit « Site par AMK »** : présente sur les démos, absente des 3 pages réelles (§20.4). Sur
   notre propre site elle n'apporte rien ; sur les sites **clients**, c'est le lien entrant de la liste SEO §5.
   *Mon avis : ne rien mettre sur AMK, l'inscrire au contrat client.*

### 9.8 · Les cinq problèmes de fond, au format §0e

| Problème | Correctif | Amélioration (durable) | Action |
|---|---|---|---|
| Une promesse retirée dans une langue survit dans l'autre | les 4 phrases corrigées ce jour | **contrôle `§20.8ter`** dans `audit_site_amk.py` : compare les durées EN/FR et échoue si une langue promet un délai que l'autre a perdu | orchestrateur (fait) |
| Une bascule `innerHTML` détruit le contenu imbriqué | `<span>` bilingue dans `sample-school` | **contrôle `§20.8bis`** : détecte les éléments bilingues imbriqués sur l'arbre HTML | orchestrateur (fait) |
| Le JS est une condition de visibilité | porte `html.js` sur 6 pages | même garde-fou à appliquer à **tout nouveau site client** : jamais d'`opacity:0` sans porte | orchestrateur (règle à écrire dans `AMK-DESIGN-SKILLS.md` §13) |
| Un faux positif de portique apprend à ignorer le portique | `audit_claims` : fenêtre limitée à la phrase, pluriels, exemption du dossier `site/` | test de régression à chaque modification d'une règle (`/tmp` : 5 violations toujours attrapées, 1 faux positif supprimé) | orchestrateur (fait) |
| L'anglais n'est pas indexable | rien fait (chantier) | miroir `/en/` + `hreflang`, gabarit réutilisable pour chaque client bilingue | **King décide**, orchestrateur exécute |

**Ce qui n'a pas changé et qui compte : le site ne promet rien qu'il ne puisse tenir.** Aucun avis inventé,
aucun nombre de clients, aucun délai de livraison, aucun prix public — la seule promesse chiffrée est
« aperçu sous 24 h », et elle est produite par la machine.

---

## 10 · La passe design du 23/10 — d'après deux prompts de structure

```
Entrées   deux prompts de sites fournis par King (23/10), tirés de websiteprompts.ai :
          « Nadia Okonjo » (marque personnelle) et « Compound Search » (agence SEO).
Demande   « adapt them and work on AMK website keeping of course our brand colors and text »
Résultat  le SYSTÈME est repris, l'identité ne bouge pas, et aucune preuve inventée n'entre.
```

### 10.1 · The Design Read (protocole §2, étape 5)

**Ce que ces deux prompts ont en commun, et qui manque à notre page** : une **voix technique**
(étiquettes en monospace, chiffres à chasse fixe, index numérotés), une **échelle typographique
franche** (le titre du premier écran occupe la place qu'il mérite), une **frise** qui rend le processus
lisible d'un coup d'œil, et une section de **refus** — dire ce qu'on ne vend pas, ce qui vaut mieux que
dire une fois de plus ce qu'on vend.

**Ce qu'ils ont et que nous ne pouvons pas avoir, sans mentir** : une courbe de trafic à 61 400 sessions,
« +412 % », « 1 840 mots-clés en top 3 », « 180 conférences », « 140 000 personnes dans la salle », des
citations de clients nommés, des tarifs au mois. **Nous n'avons aucun de ces chiffres, et en inventer un
seul détruirait la seule chose que ce site possède : il ne promet rien qu'il ne puisse tenir.**

### 10.2 · Ce qui est repris, et comment c'est adapté

| Emprunté | À qui | Comment c'est adapté à AMK | Où |
|---|---|---|---|
| **Étiquettes et données en monospace** | les deux | pile système (`ui-monospace…`), aucun téléchargement de police : le site reste rapide en 3G | `.kicker`, `.step small`, `.row-label`, `.f-grid h3`, `.amk-soc-lbl` |
| **Chiffres à chasse fixe** (`tabular-nums`) | Compound | les compteurs ne « sautent » plus pendant l'animation | `.stat .n` |
| **Échelle du titre du premier écran** | Nadia | `clamp(34px, 4.6vw, 64px)`, interligne 1.03, approche −0.03em — sans portrait : nous n'avons pas de visage à découper, et le protocole visages n'est pas tranché | `.punch` |
| **Frise de processus** | Compound | un seul filet ambre de 1 px au-dessus des cinq étapes, et un halo sur l'étape révélée | `.steps::before` (≥ 900 px) |
| **Section « ce qu'on ne fera pas »** | Compound | **quatre refus qui sont les nôtres** : prix affiché, délai sans condition, avis inventés, site qui reste chez nous | `#refus` |
| **Marquee** | Nadia | déjà présent sur la page ; on n'en ajoute pas un deuxième | existant |

### 10.3 · Ce qui est refusé, et pourquoi (à ne pas réintroduire)

| Refusé | Pourquoi |
|---|---|
| **La courbe de trafic animée** | elle raconte la croissance d'un client. Nous n'avons pas de données de client à montrer — et une courbe inventée serait exactement ce que la section « refus » condamne deux écrans plus bas |
| **« +412 % », « 1 840 mots-clés »** | chiffres de démonstration du prompt, pas des nôtres |
| **Les tarifs au mois** | un prix public est interdit par notre grille (§11b) et la fiche DM. Le devis se fait après le brief |
| **Les citations de clients nommés** | aucun client n'a encore accepté d'être cité |
| **Les portraits découpés** | politique visages non tranchée (§6 du socle) — et le site « ne montre que du vrai » |
| **Next.js / React / Framer Motion** | le site est un fichier HTML autonome, sans build ni dépendance : c'est ce qui le rend rapide en 3G et déployable par King en un glisser-déposer. Changer de pile pour une animation serait un coût sans bénéfice |

### 10.4 · Deux défauts trouvés en chemin, et corrigés

1. **Les sections vides (captures de King, 23/10).** Les 41 blocs `.rv` de l'accueil sont masqués par
   `html.js .rv{opacity:0}` et révélés par un `IntersectionObserver`. Si cet observateur ne se déclenche
   pas — JS partiellement bloqué, navigateur exotique, exception en amont — **la page reste blanche entre
   l'en-tête et le pied de page**, et la capture le montre. Correctif : la révélation est enveloppée dans
   `DOMContentLoaded`, `try/catch`, et **un minuteur force l'affichage après 1,2 s** quoi qu'il arrive.
   Règle : **aucune animation ne doit pouvoir cacher le contenu.** Ajout d'un `@media (scripting:none)`.
2. **Les logos sociaux n'étaient pas centrés dans leur rond.** Cause réelle : `footer a` et
   `.f-grid a` (spécificité 0,1,1) écrasaient `display:inline-flex` (0,1,0) — le lien retombait en
   `display:block` avec `padding:5px 0`, donc le glyphe partait en haut à gauche. Correctif : sélecteurs
   `.amk-soc a.amk-soc-a` (0,2,1), `padding:0`, `line-height:1`, `svg` à 18 px explicites.
   **Leçon** : un composant neuf hérite des règles `footer a` du site ; on écrit donc des sélecteurs à
   spécificité supérieure, et on **regarde** le résultat — un portique ne rend pas le CSS.

### 10.5 · Le troisième défaut, plus ancien, corrigé au passage

Le compteur du premier écran disait **« 24 h — d'aperçu gratuit de page d'accueil »**, c'est-à-dire **un
délai sans sa condition** — exactement ce que le §12.8 avait corrigé sur la carte de partage et le §14.5
sur les bios. Il dit maintenant **« 24 h — pour un aperçu gratuit, après validation du brief »**. C'était
la dernière promesse non conditionnée du site.
