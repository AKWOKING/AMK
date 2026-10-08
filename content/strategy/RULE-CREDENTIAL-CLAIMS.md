# RÈGLE PERMANENTE — aucune mention de diplôme/qualification sur un site client sans source au repo

> Ruling King 08/10/2026. S'applique à toute page, annonce, message ou vidéo qui affirme une
> qualité professionnelle d'un client (diplôme, titre, certification, ancienneté, agrément).

**Règle :** **aucun claim de credential sur un site client sans une source traçable au repo pour CE
credential précis.** Pas de source = pas de mention. Un fait voisin n'autorise pas le claim (une
inscription à l'Ordre ne prouve pas un diplôme ; un numéro d'inscription ne prouve pas une durée
d'exercice).

## Application immédiate (DM Optique)

| Claim | Source au repo | Statut |
|---|---|---|
| « Inscrit à l'ONOC » | registre ONOC, annuaire Littoral, ligne 102 : inscription 021/2016, arrêté 0382, titulaire M. Domche Noumbi (`clients/dm-optic/build-notes.md` l.54) | ✅ **autorisé** (trust bar du site) |
| « Opticien diplômé » | **aucune** | ⛔ **retiré** de `SPEC-PAGES-v1` (seule occurrence au repo) |

## Ruling 08/10 — balayage repo entier, remplacement partout (King)

**Le suffixe « /2016 » du registre est un numéro de décret (arrêté 0382, 021/2016), pas une durée
d'exercice. Ne jamais sourcer des « années de pratique » depuis un numéro de document.** Formulation
autorisée : « **Inscrit à l'ONOC** ». Le balayage est désormais une **tâche permanente, à l'échelle du dépôt**.

### Fait (08/10) — copie à venir réécrite, « depuis 2016 » → « Inscrit à l'ONOC »
Docs DM Optique (build-notes, content-plan, posting-calendar, carousels, ugc-script, README, SETUP-FB/TikTok/
Google, DEMO-SCRIPT, research ×2, website ×3), **HTML** (gabarit, concept, aperçu — FR+EN, schéma),
`build_dmoptic.py` + **og.jpg regénéré**, `CARTE-SIGNATURE-TABLEAU-VISION.html`, **carrousel C1 slides 1–2 re-rendues**.
La phrase W1-A (« exerce depuis 2016 ») est déjà réécrite (7 fichiers + lien WhatsApp).

### Non réécrit, annoté (enregistrements historiques — réécrire falsifierait ce qui a été dit/préparé)
`sales/Activity-Log.md` · `leads/records/dm-optique.md` · `sales/Send-BATCH-2026-09-24-Opticiens-4.md` ·
`clients/_uniqueness-registry.md` — bannière « non sourcé, NE PAS RÉUTILISER ».

### Encore périmé — dépend d'un outil absent
`clients/dm-optic/onboarding/print/CARTE-SIGNATURE-TABLEAU-VISION-A6.pdf` et `brand/…-preview.png` : générés
depuis le HTML (corrigé), **aucun moteur de rendu navigateur dans le bac** → PDF/PNG portent encore « depuis
2016 ». Carte retirée du print (ruling) ; à re-rendre avant tout usage à l'écran.
**Aussi :** la page déjà **déployée** (dmoptic-2.vercel.app) et son og.jpg en ligne portent encore l'ancienne
phrase — le dépôt est corrigé, le déploiement = un redéploiement à décider (King).

### Même classe, DM Optique — trouvé au rebalayage, NON modifié (hors ruling nommé)
- **W1-B « Dix ans d'expérience. Zéro résultat sur Internet. » — RETIRÉE 08/10 (ruling King), SANS remplacement.**
  « Dix ans » était dérivé de 2016 (années de pratique tirées d'un numéro de document). Lignes supprimées de
  `ads/variant-messages.md` (table + suivi), `content/month1/w1/ugc-script.md` (accroche B + variante B du
  pré-rempli) et `content/month1/README.md` (pré-rempli W1-B) ; compte de variantes 12 → 11 ; lettres W1-A et
  W1-C conservées. Historique git : `c6aaf87` et avant.
- `research/domche-noumbi.md` l.81, `market-analysis.md` l.139 : « Décembre 2019 : près de sept ans » — source
  distincte (mention presse), **à vérifier avant tout usage public**, pas de claim publié aujourd'hui.

### Autres clients — trouvailles du balayage (NON modifiées : hors ruling nommé, à trancher)
- **La Ligne :** « inscrite depuis 2017 » — **TRAITÉ 08/10 (ruling King)** : remplacé par **« Inscrite à
  l'ONOC »** dans `dossier.md`, `build-notes.md`, `a-completer.md`, `laligne-v1.tpl.html`,
  `concept-laligne-v1.html`, `hosting/previews/laligne/index.html` (FR + EN). `025/2017` reste comme simple
  numéro (JSON-LD). Aucune image cuite ne portait l'année (`og.jpg` vérifié).
- **Univers Optique :** « depuis 2009 » / `foundingDate 2009-08-01` — **TENU, requalifié 08/10 (ruling King)** :
  les documents disent **« annoncé depuis 2009 (source : annonce kerawa.com — support retiré, URL non conservée
  au dépôt) »**, **jamais** une affirmation client-facing sans vérification directe auprès d'Univers.
  **MISE À JOUR 08/10 (ruling King, ultérieur) :** « depuis 2009 » et `foundingDate` **RETIRÉS de la page démo
  du site** (`demos/univers-optique-site-v2.html`, `-sobre.html`, `hosting/previews/univers/index.html` : 11 → 0
  occurrence, JSON-LD valide, audit 0). Motif de King : le gel du 23/09 couvrait le contenu de pitch, pas les
  claims de fait non sourcés sur une page publique. **Non touchés (contenu de pitch, gel maintenu) :**
  `concept-univers-optique-v1/v2*.html`, `hosting/previews/univers-note/`, `univers-v1/`, les builders et
  `univers_optique_content.*` — ils portent encore 2009 (dont la phrase adressée à lui, « Depuis le
  1er août 2009, vous examinez… »). ⚠️ **Piège de reconstruction :** relancer `build_univers_optique_v2.py`
  réintroduirait 2009 dans la page du site (patch direct des fichiers construits, builder gelé). Remplacement
  de King « Opticien à Akwa, Douala » **non appliqué tel quel** : Akwa n'est pas au dépôt pour Univers (CRM :
  « Douala » ; page et dossier : **Bépanda**) ; le texte retiré n'a pas été remplacé, la page dit déjà
  « Opticien à Bépanda, Douala ». Restauration si Univers confirme la date par document.
- **uni-labo (flag 08/10, ruling King : signaler, ne pas agir) :** « Dr Tientcheu Philomène, Biologiste »
  sur la page publique `uni-labo.vercel.app` — nom et titre **non reliés à une source de dossier** (seule
  mention au dépôt : `clients/uni-labo/AUDIT-2026-09-23.md`). Ajouté à la liste du scan du dimanche 11/10 ; si
  non tracé : « Notre biologiste » ou les mots du client au go-live.
- **Le Cristallin :** « depuis 2010 », « 24/32 ans d'expérience » — **leurs propres mots**, déjà « à valider par lui ».
- **Cinq Sens :** « diplômés en optique lunetterie » — **leurs mots**, marqués comme tels au dossier.
- Non-claims écartés : Salvation (résultats 2016), `douala.cm` enregistré 2016, base64, « 16h00 » encodé.

### Commande de rebalayage (repo entier) — NON FILTRÉE (08/10 : un `grep -v "021/2016"` avait masqué des lignes mêlant numéro de décret ET claim)
`grep -rIn "2016" . --exclude-dir=.git` et `grep -rIn "2017" . --exclude-dir=.git` — lire chaque ligne (les numéros de décret 021/2016, 025/2017 sont des numéros, pas des années d'exercice) puis `grep -rIniE "depuis (20[0-2][0-9])|since 20[0-2][0-9]|exerce depuis|diplômé|certifié|agréé" . --exclude-dir=.git`.
**Page déployée :** la même grille s'applique à l'URL **publique** (lecture de la page servie), pas seulement au dépôt — voir `ops/TOOL-SCAN.md` (tâche hebdomadaire) et `ops/QA-NOTES.md` (avant tout partage d'URL).
