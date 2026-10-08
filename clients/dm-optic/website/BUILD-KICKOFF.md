# BUILD KICKOFF — site DM OPTIQUE SARL · exécutable au déclencheur acompte

> Complète `website/brief.md` (le brief) : ce fichier est la **procédure de mise en ligne**, prête à
> tourner le jour où l'acompte est encaissé (portique `pre-launch-checklist.md` item 1). Écrit le 03/10.

## 1 · Décision d'architecture — recommandation : Chemin A
Le site v2.2 existe : une page, orienté patient, **38/38 assertions**, `noindex`, non publié.
- **Chemin A (recommandé) :** publier v2.2 tel quel au déclencheur ; lever `noindex` ; coller l'adresse
  réelle puis `python3 demos/build_dmoptic.py --url https://<adresse>` + redéployer (og:url/og:image).
- Chemin B (rebuild) : seulement si King tranche contre A — et alors, brief §2 s'applique, +1 semaine.
**À trancher par King avant mercredi** (cocher) : ☐ A ☐ B. Sans coche, A par défaut au déclencheur.

## 2 · Pages & sections (Chemin A = la page unique v2.2)
Premier écran : nom + ville + métier (« puis-je venir, et comment ? ») · preuve d'inscription ONOC +
titulaire nommé · services (vue · soleil · enfants) · où et quand (Ndobo Mayor, Douala IV · 8h00–17h30) ·
CTA WhatsApp omniprésent (wa.me/237656122239, message pré-rempli). Hors périmètre : boutique, paiement,
RDV en ligne, blog (brief §1).

## 3 · Spé bilingue
FR d'abord, EN complet (langue du visiteur de Bépanda/Bonabéri mixte) — v2.2 porte déjà les deux ;
vérifier au QA que le toggle ne casse aucun CTA pré-rempli (les chaînes WhatsApp restent FR).

## 4 · Stratégie de placeholders (le site ne montre que du vrai)
- **Photos :** illustrations légendées comme telles jusqu'à la séance (Pixel 8a, `photoshoot/`) ; chaque
  emplacement a sa spec de shoot — le swap se fait photo par photo, sans rebuild.
- **Horaires :** 8h00–17h30 tels que publiés par le cabinet (source datée) — pas « à confirmer ».
- **Prix :** aucun sur la page ; orientation WhatsApp (décision 24/09 Cavisa : la question se pose, ne
  s'invente pas).

## 5 · Cible de déploiement
Projet Vercel de King (drag-and-drop, `hosting/previews/README.md`) — **déployer LE DOSSIER ENTIER**
(`index.html` + `og.jpg`), puis rebuild og + redéployer. Jamais depuis une branche arena. `dmoptic.vercel.app`
(v1) morte : l'adresse du client est le nouveau projet.

## 6 · QA checklist avant de donner l'adresse au client
1. `tools/qa/audit_a11y.py` + `audit_hero.py` + `audit_images.py` verts sur la page servie.
2. Test lecteur-écran à l'oreille (`tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`).
3. Téléphone de King, plein jour, 3G : premier écran lisible, bouton WhatsApp ouvre le message pré-rempli,
   FR **et** EN.
4. Partager le lien dans WhatsApp à King : la carte porte titre + description + **vignette** (leçon og).
5. `noindex` levé **après** ces quatre portes, pas avant.

## 7 · Ruling King 03/10 — pas de versions alternatives avant acompte
*No alternative versions built before the deposit and the photoshoot. v2.2 is the recommendation.
Two mood boards on standby for a look pushback only. Real design work begins after deposit + shoot.*
Les deux mood boards (fallback, jamais en ouverture) : `design/moodboards/MOOD-BOARD-A.png` et
`MOOD-BOARD-B.png` — une direction esthétique chacun (palette, système typo, archétype de layout
différents). Règle standing 03/10 (playbook) : une seule recommandation forte ferme mieux que trois
options.
