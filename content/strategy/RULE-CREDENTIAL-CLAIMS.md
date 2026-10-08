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
- **W1-B « Dix ans d'expérience. Zéro résultat sur Internet. »** (`ads/variant-messages.md` l.39,
  `content/month1/w1/ugc-script.md` l.41 et 129) : « dix ans » est **dérivé de 2016** — années de pratique tirées
  d'un numéro de document, exactement ce que le ruling interdit. Variante non recommandée, non diffusée ;
  candidat à retrait ou réécriture sur un mot de King.
- `research/domche-noumbi.md` l.81, `market-analysis.md` l.139 : « Décembre 2019 : près de sept ans » — source
  distincte (mention presse), **à vérifier avant tout usage public**, pas de claim publié aujourd'hui.

### Autres clients — trouvailles du balayage (NON modifiées : hors ruling nommé, à trancher)
- **La Ligne :** « inscrite depuis 2017 » (`dossier.md`, `build-notes.md`, `concept-laligne-v1.html`) — dérivé
  de **025/2017** : même défaut que 2016. Candidat au remplacement identique.
- **Univers Optique :** « depuis 2009 » / `foundingDate 2009-08-01` — source présente (annonce kerawa.com,
  « début d'activité le 01/08/2009 ») : sourcé, **tenu**.
- **Le Cristallin :** « depuis 2010 », « 24/32 ans d'expérience » — **leurs propres mots**, déjà « à valider par lui ».
- **Cinq Sens :** « diplômés en optique lunetterie » — **leurs mots**, marqués comme tels au dossier.
- Non-claims écartés : Salvation (résultats 2016), `douala.cm` enregistré 2016, base64, « 16h00 » encodé.

### Commande de rebalayage (repo entier)
`grep -rIn "2016" . --exclude-dir=.git | grep -v "021/2016"` puis `grep -rIniE "depuis (20[0-2][0-9])|since 20[0-2][0-9]|exerce depuis|diplômé|certifié|agréé" . --exclude-dir=.git`
