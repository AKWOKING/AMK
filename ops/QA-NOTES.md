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

---

## 11/10/2026 — balayage des pages publiques (fait avec `fetch_page`, pas `curl`)

> **Méthode :** `curl` est bloqué sur `*.vercel.app` depuis le bac à sable (HTTP 000, `SSL_ERROR_SYSCALL`),
> mais **`fetch_page` atteint les pages servies**. Le re-pull ONOC du même jour l'avait prouvé sur
> `onocameroun.com`. La règle permanente du 08/10 (« la même grille s'applique à l'URL publique ») est donc
> **exécutable ici** — voir `ops/INFERENCE-ERRORS.md` entrée 09.
> **Limite honnête :** `fetch_page` rend la page en markdown — **le `<head>` n'est pas lisible** (ni `og:url`,
> ni `og:image`, ni `robots`) et les images sont retirées. Tout ce qui concerne l'en-tête reste à vérifier
> autrement (Sharing Debugger, ou `view-source` sur la machine de King).

| Page | Résultat du 11/10 |
|---|---|
| **`dm-optique-sarl.vercel.app`** (page entière, 2 morceaux) | ✅ **Le redéploiement de King est en ligne.** « DM OPTIQUE SARL » dans les **six** messages WhatsApp pré-remplis (ruling 10/10 tenu) · les **trois cartes « Nos montures » sont bien des CTA WhatsApp** distincts (Option B, ruling 08/10) · ✅ aucun « depuis / since / 2016 », aucun diplôme, aucun avis, aucune note · « inscrit à l'ONOC » / « registered with the ONOC » seulement · ✅ **aucun prix** : la FAQ « Combien coûte une paire de lunettes ? » répond « le prix dépend de vos verres et de la monture… posez la question sur WhatsApp » — conforme à l'exigence du client (brief §4) · ✅ horaires du 08/10 (8h30–13h00 / 8h30–17h30), **aucun jour affirmé**, et la FAQ ajoute « écrivez sur WhatsApp pour confirmer le jour qui vous arrange » · ✅ adresse West Hotel, 1ᵉʳ étage, dernière porte à droite · ✅ titulaire M. Domche Noumbi (sourcé : annuaire ONOC #102) · ✅ illustrations légendées « Photo d'illustration » · ✅ **aucun placeholder social** (ruling 10/10). **Non vérifié :** l'en-tête (`og:image`, `noindex`) et le rendu du logo — `fetch_page` ne lit pas le `<head>`. C'est précisément ce que le Sharing Debugger tranchera (vignette absente deux fois le 10/10). |
| **`amk-cm.vercel.app`** (accueil, 2 morceaux sur 3) | ⚠️ **CORRECTION : la passe SEO du 08/10 EST déployée.** Les lignes ci-dessus (« non déployée », « en attente de déploiement ») sont **périmées**. Preuves lues en ligne : la phrase réécrite du 08/10 y est mot pour mot — « **Notre équipe travaille à distance avec des entreprises partout au Cameroun.** » — et la FAQ « hors de Douala ? » répond « nous travaillons à distance, partout au Cameroun ». **Les 3 affirmations sans trace ont disparu** : plus de « projects under way… Douala, Buea, Limbe », plus de « schools in Yaoundé, Bafoussam, Bamenda », **plus de « 99.9% uptime »**. ✅ **Aucun prix affiché** : « Starter — sur devis », « Croissance — sur demande », FAQ « le prix suit le périmètre… devis écrit ». ✅ « nous ne montrons jamais le site d'un client sans son accord écrit ». **Ce qui reste à regarder :** (1) promesses de délai en ligne — « En ligne en 3–5 jours », « 5–7 jours », « aperçu en 24h », « 1 mois de support gratuit » : ce sont des engagements, pas des claims de credential, mais un prospect peut nous les opposer ; (2) l'accueil vise toujours **écoles + cliniques** et ne parle **ni des opticiens ni de l'app d'essayage** — c'est la décision consignée (`CALENDRIER-4-SEMAINES` l.88 : l'accueil bouge quand DM Optique est en ligne et approuvé), pas un oubli ; (3) 3ᵉ morceau et **sous-pages non lues** (`sample-*.html`, `clinic-bonaberi.html`, les 2 pages service). |
| **`uni-labo.vercel.app`** | ❌ **NON balayé ce tour.** Le flag du 08/10 reste ouvert : « Dr Tientcheu Philomène, Biologiste » toujours non tracé à une source de dossier. À faire. |
| **`cavisa.vercel.app`** | ❌ **NON balayé ce tour** (2ᵉ moitié toujours non lue). |
| **`dmoptic-2.vercel.app`** | Hors périmètre (abandonnée, King 08/10 ; « on oublie », 10/10). Risque résiduel inchangé : page publique avec « depuis 2016 », et l'outil de suppression n'est pas à notre portée. |

---

## 2026-10-11 · DM Optique — vérification live (protocole Task B)

**État : EN ATTENTE du signal « deployed » de King.** Aucune vérification finale faite ce soir —
le protocole se déclenche sur le signal, pas avant.

**Baseline (fetch `dm-optique-sarl.vercel.app`, 11/10 au soir, AVANT signal) :**
- `<title>` live : « Opticien à Douala — DM OPTIQUE SARL : vue, verres, montures ».
- Le bloc ONOC du corps affiche bien **deux lignes** : « DM OPTIQUE SARL / Douala ».
- **Non confirmable par fetch :** le logo du hero (image base64 retirée par l'outil) et le
  `<head>`/`og:title` (le markdown ne rend pas les balises meta). → la vérif finale doit inspecter le
  HTML brut (hero `.herologo`/`--logo` et og:title deux lignes) sur le signal « deployed ».
- Donc : si King a déjà déployé, ceci est peut-être la nouvelle version ; la vérif formelle reste à
  faire sur signal.

**Protocole (à exécuter dans les 5 min du signal « deployed ») :**
1. Ouvrir `dm-optique-sarl.vercel.app`.
2. Tagline = deux lignes « DM OPTIQUE SARL / DOUALA », PAS la forme virgule.
3. Logo présent dans le hero (ancien : cercle bleu-rose).
4. `<head>` propre : title + og:title en forme deux lignes, pas de version ancienne en cache.
5. Reporter ici **LIVE VERIFIED** ou **LIVE MISMATCH** + détails.

## 2026-10-11 · Hero DM Optique — diagnostic lisibilité (Task 2, ruling King : Option 3)

**Deux problèmes distincts, tranchés par la mesure :**
- **A — chevauchement (le vrai problème).** `.herologo` right-anchored derrière `.hero-grid` ; sous
  980px (une colonne) la colonne de texte passe SOUS le badge. Mesure (bord droit texte vs bord gauche
  logo) : 640 → −241 · 768 → −241 · 900 → −353 (chevauchement) · 1024 → +149 · 1200 → +264 (sûr).
  **Breakpoint mesuré = 980px** (= le passage de la grille en deux colonnes ; premier viewport où
  écart ≥ 40px). Correctif : emblème de coin 220px (right:-88, top:-32) sous 980 ; badge 405px
  (right:-24, top:16) à ≥980. Scope = bug fix (restaure la composition d'origine, l'anneau était
  hors-cadre en mobile) — pas de sign-off client.
- **B — contraste (n'était PAS le problème).** Audit WCAG depuis les tokens réels : H1 `--ink #0C1524`
  = 16,1:1 sur papier / 11,4:1 sur le wash le plus sombre ; corps `.lede --ink-2 #43506A` = 7,2:1 /
  5,1:1 → **AA conforme**. Donc aucune couleur de texte à changer ; la question « dégradé vs couleur
  unique » se dissout une fois le chevauchement corrigé.
- **Couleur :** pas de texte dégradé (§3.1 interdit le gradient text sur grands titres + §6.1 un seul
  accent ; l'extrémité claire #7FA6E8 échouerait AA). Si jamais une couleur unique était voulue :
  bleu profond #2A5CB8 (5,6:1) conforme ; sky blue non. **Décision : aucune modification de couleur.**
À retenir pour tout futur hero : mesurer le chevauchement AVANT de toucher la couleur ; le contraste
se vérifie depuis les tokens, pas à l'œil.
