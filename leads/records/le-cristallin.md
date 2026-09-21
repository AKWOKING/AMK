# Le Cristallin

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-09-21. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | le-cristallin |
| Type | other |
| Ville | Douala |
| Langue de contact | FR |
| Étape | closing |
| WhatsApp | 699 90 55 77 |
| Numéro vérifié | unknown |
| Contact | MESSOUE LONTE Serge Nazaire — ASCOMA écrit « MESSOUA » : DEUX graphies connues, à caler sur sa pièce d'identité, jamais tranchées par nous |
| Canal | WhatsApp |
| Contacté | Yes |
| Réponse | YES lun 21/09 17:53 « Ok » (2 min) puis 18:01 note VOCALE : il a un site ET une page Facebook, et il DEMANDE si on veut bien lui en créer une autre = signal d'achat. |
| Maquette / site | Yes |
| Relances envoyées | 0 |
| Source | directory |
| Détail source | Annuaire officiel ONOC + Maligah |

## Contradiction résolue (M2)

- **Ce qui se contredisait :** Ma note d'annuaire (21/09) affirmait « Aucun site trouvé » et j'ai écrit le message 1 dessus. Son propre flyer, lu plus tard, portait l'adresse du cabinet.
- **Retenu :** lecristallinoptique.com est EN LIGNE et a été lu EN ENTIER le 21/09 (roi : « Le cristallin a déjà un site »), et IL A AUSSI UNE PAGE FACEBOOK — dite par lui dans sa note vocale de 18:01, absente de ma fiche : je n'avais pas cherché là où il me pointait.
- **Écarté :** l'argument « introuvable » retiré de la ligne ; le lead passe en REFONTE + création/reprise de page FB (sa demande, 18:01) ; les claims non contrôlés sont rétrogradés en QUESTIONS posées sur la page : les 12 assureurs (jamais vus sur la page d'accueil) et « 24 ans d'expérience ».

## Notes

| CONTRADICTION RÉSOLUE (M2) — retenu : lecristallinoptique.com est EN LIGNE et a été lu EN ENTIER le 21/09 (roi : « Le cristallin a déjà un site »), et IL A AUSSI UNE PAGE FACEBOOK — dite par lui dans sa note vocale de 18:01, absente de ma fiche : je n'avais pas cherché là où il me pointait. · FB : 515 likes · 44 en parlent · 98 y étaient (lus le 21/09 dans des annuaires publics, affichés sans enjoliver sur la maquette) · avis Google : 3 avis, note 3,0. ENVOI : envoyer LE FICHIER `demos/concept-le-cristallin-v1.html` (592 Ko, ≤ budget WhatsApp 1 100 Ko), PAS un lien — `amk-cm.vercel.app/cristallin/` répond 404 tant que rien n'est déployé. BLOQUÉ par UNE réponse de King : est-ce qu'AMK reprend la page Facebook du cabinet, et à 50 000 FCFA ? Réponse « A » (page seule) ou « B » (page + FB) → le message part. Feuille prête : `sales/Send-LE-CRISTALLIN-2026-09-21-Soir.md` (A sans prix / B : refonte 100 000 FCFA + reprise page FB 50 000 FCFA, 50/50, rien dû avant accord). S'il marchande : on ajuste le PÉRIMÈTRE, on ne baisse jamais les 100 000 FCFA. ADRESSE CLOSE à trois sources (site + flyer + annuaire ASCOMA) : Akwa, boulevard de la République, carrefour TIF, face ancien COMECI · 242 65 12 65 / 699 90 55 77 / 679 63 20 12 · contact@lecristallinoptique.com. MON « Bonapriso / CTFIC Mballa 2 » d'hier soir ne figurait dans AUCUNE des trois : retiré. La maquette ne corrige plus, elle DEMANDE s'il existe un second local.

## Prochaine action

**Répondre dans l'heure.** Une réponse humaine est en attente : c'est la priorité absolue (règle des 90 secondes).

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 49 ligne(s).*

`L837` · - `Le Cristallin` 17:51 · `Univers Optique` 17:50 · `Disc Optique Médicale` 17:48 · `Tchaya Optique` 17:47 :
`L881` · ## Lundi 21/09/2026 — 18:20 → 19:15 · « Ok » de Le Cristallin : le premier aperçu demandé, construit et branché sur le CRM
`L887` · > « Le cristallin a déjà un site : https://lecristallinoptique.com/ … notre but, puisqu'il a eu la gentillesse
`L890` · **Ma faute, écrite ici noir sur blanc :** la ligne `le-cristallin` du CRM portait ma note « **Aucun site trouvé** »,
`L896` · dans `clients/le-cristallin/inspiration.md`.
`L920` · `(+237) 242 65 12 65 / 699 90 55 77 / 679 63 20 12` · `contact@lecristallinoptique.com` · Akwa, face COMECI SA.
`L930` · 699 90 55 77. C'est là que se trouve la valeur de la refonte, et c'est ce que la maquette démontre.
`L934` · - `demos/build_le_cristallin.py` + **`demos/le_cristallin_content.json`** (toute la copie FR|EN vit dans le JSON ;
`L936` · la leçon est devenue architecture) → `demos/concept-le-cristallin-v1.html` · **58 KB** · **zéro image** · une
`L947` · sur le demo **et** sur `hosting/previews/cristallin/index.html` — et **diff démo ↔ aperçu = 0 ligne** (contrôlé
`L954` · que le re-traduire ; (2) l'URL WhatsApp portait le numéro **tel que l'écrit le flyer** (`699 90 55 77`) → le
`L966` · - **Dossier créé : `clients/le-cristallin/{inspiration,build-notes}.md`** + ligne au registre d'unicité +
`L968` · - `hosting/build_previews.py` → **`/cristallin/`** ajouté aux aperçus privés.
`L985` · La maquette existe ; **le lien n'existe pas** — `amk-cm.vercel.app/cristallin/` répondra 404 tant que King n'aura
`L1005` · posée sur la ligne `le-cristallin`) : rc = 1, message lu, CSV intact ; après revert, rc = 0.
`L1018` · `hosting/previews/`, `/cristallin/` = 59 888 octets) — visible par King dans son navigateur de préview, **jamais
`L1054` · **172 FR / 172 EN** · 3 eyebrows / 8 sections · 0 `<a>` sans `href` · `wa.me/699905577` chiffres seuls · rail
`L1070` · quoi vous voulez seulement cree une autre » + **l'URL de sa page Facebook** (`https://www.facebook.com/lecristallinoptique/`,
`L1086` · l'enseigne « LE CRISTALLIN » posée sur le vert du flyer, tailluse en marche avec praticienne en blouse et
`L1099` · En cherchant sa page FB, l'annuaire du **réseau de soins ASCOMA** renvoie sa fiche : « LE CRISTALLIN · Optique
`L1100` · Médicale · M. Serge Nazaire **MESSOUA** · 222 65 12 65 / 699 90 55 77 · Akwa · Boulevard de la République,
`L1126` · sur `hosting/previews/cristallin/index.html`, `diff` entre les deux = **0 ligne** · **218 FR / 218 EN** · 9 sections
`L1128` · sans `href` · 0 ancre morte · `wa.me/699905577` (chiffres seuls, **son** numéro, jamais le nôtre) · JSON-LD décodé
`L1130` · **HTTP 200** sur `/cristallin/`.
`L1132` · **Écrit dans les fichiers :** `demos/le_cristallin_content.json` (comparatif, social, photos), `demos/build_le_cristallin.py`
`L1133` · (images + assertions), `demos/img/le-cristallin-{hero,lab,tryon}.{png,jpg}`, `clients/le-cristallin/build-notes.md`
`L1134` · (bloc V2, y compris mes cassages), `clients/le-cristallin/inspiration.md` (4ᵉ source), `design/LESSONS.md`
`L1136` · deux graphies du nom, `closing`), `sales/Send-LE-CRISTALLIN-2026-09-21-Soir.md` (versions A/B réécrites sur les
`L1185` · et la grille de réticule décorative sont **bannis**, donc la « planche d'acuité » du Cristallin ne pouvait
`L1218` · **(a) `bash leads/build/rebuild.sh` a EFFACÉ l'état de Le Cristallin.** En ajoutant la ligne Univers, le
`L1235` · « **④ Prix posé, en négociation — 2** » (Le Cristallin, Univers Optique) · 47 contactés · **4 réponses
`L1242` · Le Cristallin (« A » page seule / « B » page + Facebook, 50 000 FCFA) ; les six questions qu'Univers doit
`L1260` · et `/cristallin/` = 200. **Loi nouvelle, dans `design/LESSONS.md` : « conforme » ≠ « bon » — après
`L1264` · ## 2026-09-21 · 23:59 → 00:20 · **UNIVERS OPTIQUE (et LE CRISTALLIN) — le roi refuse les images, on refait les visuels**
`L1271` · peint sur un mur (« VISION CLAIRE OPTIQUE »), une marque brodée sur une blouse, et chez Le Cristallin
`L1279` · lettering, no signage**) et le réalisme douala gardé **par la rue visible derrière la vitre**. **LE CRISTALLIN**
`L1294` · repli sobre **84 Ko**, démo Cristallin **605 Ko** · `audit_html.py` = **TOTAL confirmed findings: 0** sur les
`L1296` · `:4173/univers/` et `:4173/cristallin/` = **200** · feuilles d'envoi actualisées (poids, mention du changement
`L1305` · et `le-cristallin` repassés de `closing` à `prospecting`, relance du 22/09 effacée, note vocale du
`L1306` · Cristallin envolée, et les fiches `leads/records/*.md` reconstruites sans mes blocs du journal. **Aucune
`L1328` · pour l'envoi de 09:00, et Le Cristallin choisit A ou B ? » a été posée à King ; **pas de réponse avant la coupure
`L1331` · avec) ; la relance du Cristallin reste datée au 23/09. Une demande de validation qui dort n'est pas un feu vert,
`L1336` · puisque c'est eux qui ont été refusés ; et **LE CRISTALLIN** attend toujours sa réponse **A (page seule) /
`L1340` · ## 2026-09-22 · 08:05 → 08:55 · UNIVERS OPTIQUE + LE CRISTALLIN — « ce site est moche et n'a pas d'image » : c'était une panne, pas un goût
`L1357` · **LE CRISTALLIN — défaut 2, plus grave : son `<script>` ne compilait pas depuis dimanche.** Quatre phrases de
`L1373` · (`clients/univers-optique/`, `clients/le-cristallin/`).
`L1376` · **86 954** (`1ff52ae6be71dc4d…`) · Le Cristallin **620 492** (`625ce76a78f9b341…`) · `audit_html.py`
`L1378` · `diff` démo ↔ aperçu = **0 ligne** aux deux clients · `:4173/univers/` et `:4173/cristallin/` = **200**.
`L1383` · par mes soins.** La promesse tient : aperçu UNIVERS OPTIQUE **avant 09:00** ; LE CRISTALLIN attend toujours sa

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
