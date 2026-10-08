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
| `dmoptic-2.vercel.app` | ⚠️ « depuis 2016 » ×3 (FR+EN) — page v2.1, en retard sur le dépôt → redéploiement King |
| `dmoptic.vercel.app` | 404 (aucun déploiement) |
| `lecristallin-concept.vercel.app` | non relu (gel ; mots du client) |
| `uni-labo.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun « depuis / since / certifié » ; nomme « Dr Tientcheu Philomène, Biologiste » (nom + titre, à relier à la source du dossier) — 2ᵉ moitié non lue |
| `cavisa.vercel.app` | 1ʳᵉ moitié lue (chunk 1/2) : aucun claim d'année ni de diplôme ; adresse/horaires « à confirmer » — 2ᵉ moitié non lue |
| `mitoc-concept.vercel.app` | page entière lue : aucun claim d'année ni de diplôme (« Independent optician » seulement) ; page marquée démo |
| `amk-cm.vercel.app` (+ `/mitoc.html`, `/clinic-bonaberi.html`, `/creation-site-web-*.html`) | **non balayé** — à faire au scan du dimanche 11/10 |

*Limite assumée : `fetch_page` rend la page par morceaux ; un « aucun hit » ne vaut que pour la partie lue (colonne Résultat).*
