# QA NOTES — journal tooling QA · créé le 05/10 (ruling King)

> Classe **distincte** d'`ops/INFERENCE-ERRORS.md` : ici les faux-zéros d'outil/QA, pas des
> jugements d'inférence. Ruling King 05/10 : la classe grep est QA/tooling, **pas** inférence.
> Règle miroir dans la checklist orchestrateur : `PRE-FLIGHT.md` §1d.

**Règle (ruling King 05/10) :** quand on grep un contenu qu'on vient d'insérer, la chaîne cherchée
est la **ligne source littérale, marqueurs markdown inclus** (`**gras**` compris). Un pattern
« propre » sans marqueurs produit un faux-zéro garanti sur du contenu boldé.

| Date | Faux-zéro | Cause | Tranché par |
|---|---|---|---|
| 05/10 | blocs (d)/(e) du doc conditions comptés 0 | pattern sans `**` alors que la source est boldée | lecture des lignes 13/16 |
| 05/10 | « enseigne » de la proforma v2 comptée 0 | pattern sans `**` alors que la source est `**Enseigne commerciale :** …` | lecture de la ligne 5 |

Le ruling King compte 3 occurrences de la classe au 05/10 ; « enseigne » (proforma v2) est la 4e.
Chaque occurrence a été tranchée par **lecture de ligne**, jamais réinterprétée depuis le zéro.

---

## Avant tout partage d'URL publique à un prospect (ruling King 08/10)

**Règle :** avant qu'une URL publique soit envoyée à un prospect, deux contrôles **contre la page EN LIGNE**
(pas contre le dépôt) : **(1)** le balayage crédentiels (`content/strategy/RULE-CREDENTIAL-CLAIMS.md`) ;
**(2)** le pré-flight de livraison `AMK-DESIGN-SKILLS.md` §13 (+ §18.4 échelle de vérification).
Un contrôle fait sur la copie locale ne compte pas : c'est la page servie que le client ouvre.

**Deux cas qui l'ont motivée :**
- **Labiomed (19/09)** — trouvé par King sur la page en ligne : la FAQ n'apparaissait pas en anglais
  (`<details>` avec classe de langue sur le `<summary>`) ; leçon `AMK-DESIGN-SKILLS.md` §20.11.
- **`dmoptic-2.vercel.app` (08/10)** — la page servie portait encore « depuis 2016 » (3 occurrences) alors
  que le dépôt avait été corrigé, et était en retard d'une version (v2.1 en ligne, adresse/horaires « à
  confirmer » ; dépôt = v2.2). Un redéploiement par King est requis.

### Balayage des pages publiques (08/10, via lecture de la page servie)
| URL | Résultat |
|---|---|
| `dmoptic-2.vercel.app` | ⚠️ **RISQUE TOUJOURS OUVERT (08/10 soir) : la nouvelle URL `dm-optique-sarl.vercel.app` est propre, l'ANCIENNE sert encore « depuis 2016 » — **King l'abandonne (08/10, 2e message du soir) : hors périmètre des balayages, plus aucune référence client.** Reste une condition : redéployer `dm-optique-sarl` (og corrigé) AVANT de l'abandonner, et vérifier que le client a bien la nouvelle adresse** — état avant le 08/10 soir :  : « depuis 2016 » ×3 (FR+EN), page v2.1 (adresse/horaires « à confirmer ») — le dossier `hosting/previews/dmoptic/` est maintenant v2.3 (ONOC + nouvelles heures) ; à relire en ligne après le dépôt |
| `dmoptic.vercel.app` | 404 (aucun déploiement) |
| `lecristallin-concept.vercel.app` | non relu (gel ; mots du client) |
| `uni-labo.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun « depuis / since / certifié » ; ⚠️ **FLAG (08/10, ruling King) :** « Dr Tientcheu Philomène, Biologiste » non tracé à une source de dossier → liste du scan du **dimanche 11/10** ; remplacer par « Notre biologiste » au go-live si non tracé — **aucune modification maintenant** ; 2ᵉ moitié non lue |
| `cavisa.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun claim d'année ni de diplôme ; adresse/horaires « à confirmer » — 2ᵉ moitié non lue |
| `mitoc-concept.vercel.app` | page entière lue : aucun claim d'année ni de diplôme (« Independent optician » seulement) ; page marquée démo |
| `amk-cm.vercel.app` (accueil, 2 morceaux lus) | **balayé 08/10 : aucun « depuis / since » ni diplôme ; ⚠️ 3 affirmations sans trace** — « projects under way… Douala, Buea, Limbe », « we also work with schools in Yaoundé, Bafoussam, Bamenda », « 99.9% uptime » ; ✅ prix : RETIRÉS du dépôt le 08/10 (ruling King : aucun prix sur amk-cm), non déployés ; ✅ dépôt = export live depuis le 08/10 (PR #5). Détail : `site/SEO-REVIEW-2026-10-08.md`. **Aucune modification** ; décisions de King attendues. Sous-pages non balayées. |
| `amk-cm.vercel.app` — **passe SEO 08/10 (soir), dans `site/`, non déployée** | 3 affirmations retirées ; français par défaut cuit dans le HTML ; nom unifié = fiche Google ; WebP ; `mitoc.html` noindex ; promesses de prix périmées retirées ; contraste des boutons FR\|EN corrigé. **Contrôles :** `audit_html` 0 constat · `audit_a11y --strict` rc 0 · `check_inline_js` 0 faute · **`node tools/qa/test_amkcm_lang.mjs` vert** (nouveau, sans dépendance). **Non fait :** rendu visuel et tests puppeteer (absents du bac à sable). **Après déploiement :** balayage du site en ligne (§13) + `view-source`. Détail : `site/SEO-REVIEW-2026-10-08.md` §8. |
| `dm-optique-sarl.vercel.app` (08/10 soir) | **Nouvelle URL canonique (King). Lue en deux morceaux par l'orchestrateur :** « inscrit à l'ONOC » · horaires 8h30–13h00 / 8h30–17h30 · adresse West Hotel · aucun prix · aucun « depuis »/« since »/« 2016 » · FAQ prix sans chiffre. **Non vérifié :** l'en-tête HTML (`og:url`, `og:image`), qui d'après le dépôt pointait vers `dmoptic-2` ; la page ne s'est pas vue sur téléphone. **Fait :** `build_dmoptic.py --url https://dm-optique-sarl.vercel.app/` (diff = 2 lignes + l'étiquette d'URL de `og.jpg`). **À faire (King) :** redéployer le dossier `hosting/previews/dmoptic/` **puis** abandonner l'ancienne URL ; **ne pas l'abandonner avant** (l'aperçu WhatsApp charge `og.jpg` depuis l'adresse écrite dans `og:image`). Vendredi : balayage §13 sur la nouvelle URL, comme prévu. |
| **Vendredi 09/10 — séquence DM + amk-cm (ruling 08/10, 11ᵉ message)** | Verrouillée dans `hosting/previews/README.md` (6 étapes). **Constaté le 08/10 en préparant le masquage :** la page DM Optique du dépôt n'a **ni pills de catégorie, ni barre de recherche, ni filtre** (4 boutons : FR, EN, copier le numéro, enregistrer le contact) ; ces éléments n'existent que dans `SPEC-PAGES-v1.md` §2. Les trois cartes « Lunettes de vue / de soleil / Enfants » de la section `#montures` n'ont ni lien ni survol : c'est le seul élément qui ressemble à des catégories non cliquables. **Question posée à King** (laquelle masquer ?) avant de toucher à une page approuvée par le client le 25/09. La note de spec « pills et recherche cachées tant qu'aucune carte n'existe » est écrite. **Question sautée par King (08/10) → aucune modification de la page tant qu'il n'a pas choisi** : (A) masquer les trois cartes + le lien de navigation, (B) les garder avec un bouton WhatsApp par famille, (C) autre élément sur une page que le dépôt ne montre pas (capture demandée). Ordre d'envoi (étape 2 avant 3) : gardé tel que ruled, conflit signalé. |
| **08/10/2026 (12ᵉ message) — Option B appliquée à la page DM Optique** | **Ruling King :** les trois cartes de `#montures` deviennent des CTA WhatsApp (message par catégorie, FR + EN) ; pas de catalogue, filtres ni recherche. Ceci **clôt la question ouverte** de la ligne précédente (« laquelle masquer ? »). **Fait :** gabarit + reconstruction avec `--url https://dm-optique-sarl.vercel.app/` (`og` rebuilt dans le même geste) ; test de page **50/50** (+5 assertions Option B ; deux anciennes mises à jour : « six messages » → neuf, « une seule action » → quatre) ; `audit_html` 0 · `audit_a11y --strict` rc 0 · `audit_images` 0 · `check_inline_js` OK · `audit_hero` 0 · `audit_aeo` 0 ; `robots` = `noindex,nofollow` ✓ ; aucun `dmoptic-2`, aucun « DM OPTIC », aucun « depuis 2016 ». **Rendu réel (Chromium headless, 390 px, FR puis EN puis FR) :** trois liens, bons messages, bascule OK, aucun débordement horizontal. **À redéployer par King le 09/10.** Spec : `SPEC-PAGES-v1.md` (bannière + §1 + §2). |
| **08/10/2026 — salutation des cartes** | Les trois messages ruled disent « Bonjour DM **Optique** » ; les six autres messages de la page disent « DM **OPTIQUE SARL** » (nom donné par le client le 25/09). Texte de King gardé ; le test accepte exactement ces deux salutations. **À valider par King** (un changement de chaîne si « SARL » partout). |
| **08/10/2026 — séquence du vendredi corrigée** | Vérification en ligne **avant** que le client reçoive l'URL (King a permuté 2↔3). README, fichier d'envoi et cette table alignés. |
| **08/10/2026 — outillage : un navigateur existe** | « Pas de navigateur dans le bac » (affirmé jusqu'ici) était faux : `bash tools/video/install.sh` → Chromium headless dans `/tmp/amk-video`, puis `LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts`. Une vérification en ligne peut donc lire le DOM rendu, pas seulement le texte de `fetch_page` ; le portique « vérifié sur un téléphone, en plein jour » (King) **reste** — un rendu headless ne le remplace pas. |
| **Standing tool : SEO site client** | `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` — actif permanent (ruling King 08/10) : **chaque livraison de site client la passe.** Trouvailles de la passe `amk-cm` à ne pas refaire : (1) `aggregateRating` / `Event` inventés en JSON-LD d'un modèle indexable (`sample-school.html`, retirés) ; (2) og:url/og:image restés sur l'ancienne URL après un changement d'adresse ; (3) promesses de prix périmées après retrait des prix ; (4) CSS des boutons de langue liée à l'identifiant. |

*Limite assumée : `fetch_page` rend la page par morceaux ; un « aucun hit » ne vaut que pour la partie lue (colonne Résultat).*

*Univers Optique (08/10) : la page démo du site n'est plus « depuis 2009 » (fichiers construits patchés, builder gelé — piège de reconstruction noté dans `content/strategy/RULE-CREDENTIAL-CLAIMS.md`). URL publique Univers non répertoriée au dépôt : à confirmer par King.*
