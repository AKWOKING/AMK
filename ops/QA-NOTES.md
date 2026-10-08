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
| `dmoptic-2.vercel.app` | ⚠️ **RISQUE TOUJOURS OUVERT (08/10 soir) : la nouvelle URL `dm-optique-sarl.vercel.app` est propre, l'ANCIENNE sert encore « depuis 2016 » — à rediriger/retirer par King APRÈS le redéploiement du og (le client a reçu cette adresse le 24/09 : rediriger, ne pas supprimer sans lui dire)** — état avant le 08/10 soir :  : « depuis 2016 » ×3 (FR+EN), page v2.1 (adresse/horaires « à confirmer ») — le dossier `hosting/previews/dmoptic/` est maintenant v2.3 (ONOC + nouvelles heures) ; à relire en ligne après le dépôt |
| `dmoptic.vercel.app` | 404 (aucun déploiement) |
| `lecristallin-concept.vercel.app` | non relu (gel ; mots du client) |
| `uni-labo.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun « depuis / since / certifié » ; ⚠️ **FLAG (08/10, ruling King) :** « Dr Tientcheu Philomène, Biologiste » non tracé à une source de dossier → liste du scan du **dimanche 11/10** ; remplacer par « Notre biologiste » au go-live si non tracé — **aucune modification maintenant** ; 2ᵉ moitié non lue |
| `cavisa.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun claim d'année ni de diplôme ; adresse/horaires « à confirmer » — 2ᵉ moitié non lue |
| `mitoc-concept.vercel.app` | page entière lue : aucun claim d'année ni de diplôme (« Independent optician » seulement) ; page marquée démo |
| `amk-cm.vercel.app` (accueil, 2 morceaux lus) | **balayé 08/10 : aucun « depuis / since » ni diplôme ; ⚠️ 3 affirmations sans trace** — « projects under way… Douala, Buea, Limbe », « we also work with schools in Yaoundé, Bafoussam, Bamenda », « 99.9% uptime » ; ✅ prix : RETIRÉS du dépôt le 08/10 (ruling King : aucun prix sur amk-cm), non déployés ; ✅ dépôt = export live depuis le 08/10 (PR #5). Détail : `site/SEO-REVIEW-2026-10-08.md`. **Aucune modification** ; décisions de King attendues. Sous-pages non balayées. |
| `amk-cm.vercel.app` — **passe SEO 08/10 (soir), dans `site/`, non déployée** | 3 affirmations retirées ; français par défaut cuit dans le HTML ; nom unifié = fiche Google ; WebP ; `mitoc.html` noindex ; promesses de prix périmées retirées ; contraste des boutons FR\|EN corrigé. **Contrôles :** `audit_html` 0 constat · `audit_a11y --strict` rc 0 · `check_inline_js` 0 faute · **`node tools/qa/test_amkcm_lang.mjs` vert** (nouveau, sans dépendance). **Non fait :** rendu visuel et tests puppeteer (absents du bac à sable). **Après déploiement :** balayage du site en ligne (§13) + `view-source`. Détail : `site/SEO-REVIEW-2026-10-08.md` §8. |
| `dm-optique-sarl.vercel.app` (08/10 soir) | **Nouvelle URL canonique (King). Lue en deux morceaux par l'orchestrateur :** « inscrit à l'ONOC » · horaires 8h30–13h00 / 8h30–17h30 · adresse West Hotel · aucun prix · aucun « depuis »/« since »/« 2016 » · FAQ prix sans chiffre. **Non vérifié :** l'en-tête HTML (`og:url`, `og:image`), qui d'après le dépôt pointait vers `dmoptic-2` ; la page ne s'est pas vue sur téléphone. **Fait :** `build_dmoptic.py --url https://dm-optique-sarl.vercel.app/` (diff = 2 lignes + l'étiquette d'URL de `og.jpg`). **À faire (King) :** redéployer le dossier `hosting/previews/dmoptic/` **puis** rediriger l'ancienne URL ; **ne jamais retirer `dmoptic-2` avant** (l'aperçu WhatsApp charge `og.jpg` depuis l'adresse écrite dans `og:image`). Vendredi : balayage §13 sur la nouvelle URL, comme prévu. |
| **Standing tool : SEO site client** | `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` — actif permanent (ruling King 08/10) : **chaque livraison de site client la passe.** Trouvailles de la passe `amk-cm` à ne pas refaire : (1) `aggregateRating` / `Event` inventés en JSON-LD d'un modèle indexable (`sample-school.html`, retirés) ; (2) og:url/og:image restés sur l'ancienne URL après un changement d'adresse ; (3) promesses de prix périmées après retrait des prix ; (4) CSS des boutons de langue liée à l'identifiant. |

*Limite assumée : `fetch_page` rend la page par morceaux ; un « aucun hit » ne vaut que pour la partie lue (colonne Résultat).*

*Univers Optique (08/10) : la page démo du site n'est plus « depuis 2009 » (fichiers construits patchés, builder gelé — piège de reconstruction noté dans `content/strategy/RULE-CREDENTIAL-CLAIMS.md`). URL publique Univers non répertoriée au dépôt : à confirmer par King.*
