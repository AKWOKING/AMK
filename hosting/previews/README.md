# AMK — Client preview hosting (King self-hosts)

```text
État au 26/10/2026 — 4 aperçus, et rien d'autre.
dmoptic/      client payant, en production sur dmoptiquesarl.com
labiomed/     laboratoire de Deido-Bassa — aperçu envoyé, lien labiomed.vercel.app
cristallin/   opticien — refonte, aperçu construit, GELÉ (voir plus bas)
dr-ophtalmo/  médecin ophtalmologue itinérant — aperçu construit le 26/10, NON publié, aucune
              coordonnée réelle ; lien de travail dr-ophtalmo-preview.vercel.app (noindex)
```

**Décision King, 24/10 :** « cut the ones belonging to retired prospects and keep `dmoptic`,
`labiomed` and `cristallin` ». Les onze autres aperçus (`afriquelabo`, `bonanjo`, `cavisa`,
`cinqsens`, `demo`, `demo-clinique`, `laligne`, `mboacare-demo`, `opticien`, `skye`, `unilabo`,
`univers`, `univers-note`, `univers-v1`, `yaks`) sont **retirés du dépôt**, avec leurs pages
canoniques dans `demos/` et leurs builders.

**Pourquoi ce n'est pas une perte :** `clients/_uniqueness-registry.md` garde, pour chaque page
construite, l'empreinte de design — archétype de mise en page, famille de palette, système
typographique, ton. C'était la seule raison de conserver les fichiers (« ne pas refaire deux fois
le même design ») ; le registre la couvre mieux qu'un fichier HTML, parce qu'il se lit avant de
construire au lieu de se comparer après.

**Ramener un aperçu :** `git log --oneline -- hosting/previews/<slug>/`, puis
`git checkout <commit>^ -- hosting/previews/<slug>/ demos/`.

## Les trois aperçus, et ce qui les régit

| Slug | Source canonique | État |
|---|---|---|
| `dmoptic/` | `demos/concept-dmoptic-v1.html` ← `demos/dmoptic-v1.tpl.html` + `demos/build_dmoptic.py` (+ `build_dmoptic_montures.py` pour les 40 fiches) | **production** — `dmoptiquesarl.com`, déployé sur Cloudflare. C'est le seul aperçu qui se déploie encore depuis ce dépôt. |
| `labiomed/` | aucun builder dans le dépôt — le dossier est autonome (`index.html`, `og.jpg`, `img/`) | **envoyé** — `labiomed.vercel.app`, message du 19/09 avec le lien et le prix. Le fil est en « report motivé », pas en oui commercial. |
| `cristallin/` | `demos/concept-le-cristallin-v1.html` ← `demos/build_le_cristallin.py` + `demos/le_cristallin_content.json` | **gelé** — voir ci-dessous |
| `dr-ophtalmo/` | aucun builder — dossier autonome (HTML + CSS + modules ES + `js/config/doctor.js`) | **aperçu, non publié** — aucune donnée de contact réelle ; `node tests/logic.test.mjs` (40 vérifications) ; déployé pour lecture sur `dr-ophtalmo-preview.vercel.app` (projet Vercel `dr-ophtalmo-preview`, racine ce dossier, `noindex` + `robots.txt`) |

## ⛔ GEL — Le Cristallin (décision de King, 23/09/2026 au soir)

> **« Pour lecristallin et univers on ne touche plus rien jusqu'à ce que les prospects deviennent
> des clients payants. »** — Univers a été retiré du dépôt le 24/10 ; la règle reste entière pour
> Le Cristallin.

1. **Aucune modification** de `demos/concept-le-cristallin-v1.html`, de son builder ni du contenu
   JSON. Pas d'ajustement, pas de « petite retouche », pas de rebuild.
2. **Ne JAMAIS redéployer le Cristallin depuis ce dépôt.** La page en ligne
   (`lecristallin-concept.vercel.app`, projet Vercel de King) est **en avance sur notre copie** :
   elle porte déjà le slogan dans la barre, les textes d'origine sur les verres et l'adresse
   Ancien COMECI / ECOTEX, et ses liens WhatsApp sont en `wa.me/237699905577`. Un déploiement
   depuis le dépôt **écraserait le travail que le client regarde**.
3. La règle du client complète la nôtre, mot pour mot (21:58, 22/09) : « Pour le reste ne change
   encore rien puisque j'ai certains modifications que tu as apporté sans mon ok. »
4. **Ce qui reste permis** : le marquer comme client, encaisser, répondre à ses messages. **Rien
   d'autre** tant qu'il n'a pas payé.

## Reconstruire

```bash
python3 hosting/build_previews.py     # ne reconstruit plus que cristallin/ (SLUGS)
python3 demos/build_dmoptic.py        # dmoptic/ — écrit l'aperçu, og.jpg et les WebP
python3 demos/build_dmoptic_montures.py   # les fiches montures de dmoptic/
```

`build_previews.py` réinjecte `noindex,nofollow` sur chaque copie : un aperçu partagé un-à-un
n'est jamais public. **Ne pas le lancer sur `cristallin/`** tant que le gel tient : il réécrirait
la copie locale et l'écart avec la page en ligne deviendrait invisible.

`index.html` reste un marqueur privé, sans aucun lien.

## Deploy gate — avant d'envoyer un aperçu à un prospect

Sur un **téléphone**, pas sur l'aperçu du poste :

1. La page démarre en **FR**, le basculeur EN|FR change toute la page dans les deux sens.
2. **Un vrai pré-remplissage WhatsApp ouvert** depuis un bouton de la page — bon numéro, bon texte
   français, encodage URL correct.
3. Le bouton mobile fixe est visible et cliquable ; la navigation tient sur une ligne ; aucun
   débordement horizontal.
4. Les faits réels du prospect s'affichent ; tout chiffre qui n'en est pas un porte son étiquette
   de démonstration.
5. **Passe de provenance** (`AMK-DESIGN-SKILLS.md` §18.1) : chaque prix, horaire et compteur est
   tracé à une source, ou étiqueté comme exemple.
6. Après un correctif post-déploiement, revérifier **sur l'URL en ligne** — le fichier servi, pas
   la copie locale.

**« Sur un téléphone » veut dire** (`AMK-DESIGN-SKILLS.md` §24.3.5) : la nuit, en plein soleil,
sur Android **et** iOS. Non vérifié sur téléphone = non envoyé.

## Règles d'envoi

- Envoyer le **lien du sous-dossier** ou l'URL du projet, jamais l'URL GitHub brute.
- **Image d'abord, texte ensuite** — jamais les deux dans le même message.
- À la signature : le site part dans un dossier/projet **au nom du client**, le domaine enregistré
  **à son nom**.
- Chaque aperçu porte `noindex,nofollow` : rien de tout cela n'est public.
