# Le Cristallin — notes de build (21 Sep 2026, 18:45)

## Fichier
- `demos/build_le_cristallin.py` (le gabarit, aucun jeton non remplacé à la sortie)
- `demos/le_cristallin_content.json` (**toute la copie FR|EN vit ici**) — le générateur ne contient
  pas une seule phrase : le premier jet du fichier cassait sur les apostrophes françaises dans un f-string,
  la leçon est gravée dans l'architecture, pas dans un commentaire.
- sortie : `demos/concept-le-cristallin-v1.html` (58 KB · une seule copie de la page, **sans photo : donc
  sans les 1 à 3 Mo d'images base64 de nos autres concepts**) + `hosting/previews/cristallin/`.

## Design Read (§1) et dials (§2)
> « Lecture : une refonte-conversion pour les patients de Douala et les services RH qui paient des lunettes,
> dans une langue de cabinet d'optique (mesure, papier, horaires), penchée vers une planche d'acuité
> éditoriale — pas une boutique. »

VARIANCE **6** (asymétrie posée : trois portes de tailles inégales, tableau à filets, bandeau sombre) ·
MOTION **4** (révélation IO + survols uniquement ; `prefers-reduced-motion` honnoré en CSS **et** en JS) ·
DENSITY **4**. Preset maison « School/clinic concept (conversion) », volontairement pas celui d'un e-commerce.

## Direction : « PLANCHE D'ACUITÉ »
L'objet même du métier — la table Snellen — devient l'ouverture **et** le sommaire des services : cinq lignes
de lettres de plus en plus petites, chacune = un acte du cabinet, chacune = un message WhatsApp pré-rempli
qui nomme cet acte. Ce n'est pas de la décoration : le visiteur choisit sa prestation en lisant, et le
fichier n'a plus besoin d'un menu de services. Zéro concept de nos autres builds ne fait ça.

**Différenciation sur 6 axes (minimum 4 exigé par PRE-FLIGHT §2.6) :**
| Axe | Ici | Ce que ça écarte au registre |
|---|---|---|
| Layout | planche d'acuité = navigation ; tableau à 10 lignes ; sélecteur d'assureur | `concept-opticien-v1` (cabine d'essayage, monture qui tourne) |
| Palette | papier froid `#EFF2F1` + vert du flyer `#0D5A41` + encre `#0B1613`, **un seul accent, aucun ambre, aucune crème** | `concept-opticien-v1` (ink-teal + amber + clay sur crème) · OraCare (cream/sand + gold) |
| Typo | **Archivo** (display) + Instrument Sans (texte) + JetBrains Mono (uniquement les libellés de mesure) | `concept-opticien-v1` (Fraunces + Inter) · afriquelabo (Space Grotesk + Inter + mono partout) |
| Traitement image | **aucune photo** : trois cadres dessinés, étiquetés « à remplacer par vos photos » | tous les autres builds (photos base64) |
| Ordre des sections | portes (patient / assuré / employeur) AVANT les prestations | tout le reste de nos concepts, qui ouvre sur les services |
| Ton | « Vous lisez la dernière ligne ? » — la preuve par la mesure, pas la séduction | « Voir net. Se voir bien. » (opticien v1) |

## Choix de contenu, et pourquoi
1. **La porte « entreprises et institutions » est posée en large**, pas en troisième carte identique : les
   douze assureurs et la prestation de formation du personnel sont la partie du chiffre que le site actuel
   cache dans un bloc de texte. C'est aussi la seule porte que leurs concurrents d'annuaire ne peuvent pas
   copier en un week-end.
2. **Le sélecteur d'assurance** (12 noms → message WhatsApp pré-rempli avec le nom de l'assureur) est la
   fonctionnalité nouvelle. Elle ne demande aucune donnée que nous devrions inventer : elle utilise la liste
   qu'ils publient déjà, et elle remplace un formulaire Nom/Email/Objet/Message.
3. **Les logos des marques de montures ne sont pas repris.** Leur site actuel affiche des photos de
   produits Ray-Ban, Dior, Emporio Armani… Nous ne les copions pas : droits de tiers, et rien à gagner à
   montrer un catalogue dont nous n'avons aucune photo vraie. À la place : trois cadres à remplir par le
   cabinet (devanture, laboratoire, monture portée), dessinés et **étiquetés comme tels**. Un propriétaire
   qui voit un cadre vide avec son nom dessus comprend ce qu'on attend de lui ; un propriétaire qui voit une
   photo volée croit que le site est déjà fini.
4. **Aucun prix inventé.** Leur site n'en affiche pas, donc la FAQ répond « pourquoi il n'y en a pas » et
   envoie vers WhatsApp pour un devis. (Nos concepts qui affichent des prix le font parce que LE lead les a
   donnés : Afrique Labo sa grille, MITOC ses montures. Ici, rien.)
5. **Aucun avis, aucune note, aucun compteur.** Bandeau de preuve = les trois papiers seulement, avec un
   doute affiché sur la version de l'ISO.
6. **Les quatre divergences site/flyer sont ÉCRITES SUR LA PAGE**, dans une section « Avant de publier » du
   pied : samedi, les deux lignes de téléphone du flyer, les deux adresses, la date de fin du kit offert, la
   version du certificat. C'est la première fois qu'un de nos concepts montre au propriétaire sa propre
   besogne — et c'est exactement ce qu'une refonte honnête doit faire. Un prospect qui lit « à trancher avant
   publication » sait qu'il n'a pas affaire à un moule.

## Contrôles passés
- `python3 tools/qa/audit_html.py demos/concept-le-cristallin-v1.html` → **TOTAL confirmed findings: 0**
  (385 runs, desktop 385 / mobile 385) — passé sur le démo ET sur l'aperçu, avec `diff = 0 ligne` entre les deux. Deux défauts avaient été trouvés et corrigés avant : le lien
  téléphone du bandeau sombre et l'eyebrow du bandeau de preuve étaient en `--deep` sur fond noir (2,25:1).
- Paires de langue : **170 FR / 170 EN**, compte égal, contrôlé par une assertion dans le générateur
  **avant** l'écriture (un fichier déséquilibré ne touche plus le disque).
- 0 lien mort, 0 `href="#"`, **0 `<a>` sans `href`**, toutes les ancres existent ; dans les URL, `wa.me` pointe
  sur **699905577** (chiffres seuls — un espace dans un `href` tronque le lien et tue le message pré-rempli),
  l'affichage garde **699 90 55 77** ; le numéro du propriétaire uniquement (jamais le nôtre) ; `tel:` 242 65 12 65 et 679 63 20 12 ; un seul `mailto`.
- Em-dash : **0 dans les 170 chaînes anglaises** (autorisées en français : 6 là-bas).
- JSON-LD `Optician` : décodé et validé localement ; horaires = ceux du SITE (lun-ven 08:30–18:30), le
  samedi du flyer n'est PAS dans les données structurées tant qu'il n'est pas confirmé.
- `robots: noindex,nofollow` présent (concept nommé = privé, règle du 17/09).

## À FAIRE avant l'envoi à M. Messoue (bloquant, pas fait ici)
1. **Capture 1280×800** → `demos/shots/le-cristallin-concept.png` + mockup ordinateur/téléphone :
   `playwright` est absent du bac. À lancer sur la machine de King, ou me redonner un bac avec le navigateur.
2. **Le lien.** `amk-cm.vercel.app/cristallin/` répondra 404 tant que le dossier n'est pas déployé sur Vercel
   (le projet Vercel est le tien) — **ne jamais deviner l'URL**. Alternative sans dépendance : envoyer le
   fichier lui-même (58 KB, s'ouvre dans un navigateur de téléphone) ou une capture d'écran.
3. **Relire la lede du hero à voix haute** avec lui : « Vous lisez la dernière ligne ? » est une
   accroche, pas une promesse médicale.
4. Roi : si tu veux que la page devienne une proposition commerciale, le prix n'y va pas — la page est la
   preuve, l'offre se fait dans le fil (100 000 FCFA, 50/50, comme les deux autres fils à `closing`).

## Relecture §13 — passée le 21/09 au soir, et ce qu'elle a trouvé que le script ne trouve pas

| Point | État |
|---|---|
| `alert/confirm/prompt` | aucun |
| transition globale sur `body` | aucune (uniquement sur les cibles `.btn`, `.row`, `.door`, `.tag`) |
| `html{scroll-behavior:auto}` sous `prefers-reduced-motion` | ✓ (+ IO court-circuitée en JS) |
| `::selection` | ✓ posé |
| bandeau de preuve | **sans eyebrow** — le bandeau sombre se lit déjà comme un bloc à part (la règle « 1 eyebrow par 3 sections » est une assertion du générateur, plafond `ceil(8/3)=3`) |
| CTA mobile collant | **`Réserver un examen de vue` / `Book an eye exam` — mot pour mot le CTA du hero, même href, même message pré-rempli** ; à-côté = `Appeler` (`tel:`). Cette ligne a été **vérifiée par une assertion du générateur**, pas par mes yeux : ma première note affirmait « ✓ identiques » alors que le hero disait « Réserver un examen de vue » et le rail « Réserver sur WhatsApp ». Un point de relecture qui n'est pas une assertion est une opinion. |
| zones tactiles | mesuré dans le CSS : rail mobile `padding:12px` + `0.9rem` ≈ **42–44 px** de cible, rangées de la planche `padding:13px 16px` ≈ **45 px**, boutons du hero `13px 18px`. Sous le seuil de 44 px pour le rail de 1–2 px : **À CONFIRMER SUR UN VRAI TÉLÉPHONE** (dernier point non vérifiable dans ce bac, pas de navigateur ici) — si ça tape court, on passe le padding du rail à 14px, pas la police |
| zéro chaîne en double, pas de `lorem` | ✓ (aucun texte non rempli, 0 jeton survivant — assertion) |
| aucun lien mort | 0 `<a>` sans `href`, 0 `href="#"`, toutes les ancres résolues |
| URLs WhatsApp | `wa.me/699905577` — **chiffres seuls** ; l'affichage garde `699 90 55 77`. Le numéro du propriétaire uniquement (jamais le nôtre) |
| `noindex` + JSON-LD `Optician` décodé | ✓ · horaires = ceux du SITE (lun–ven 8h30–18h30), le samedi du flyer n'entre pas dans les données structurées avant confirmation |
| équilibre FR\|EN | **170 / 170**, contrôlé AVANT écriture (un fichier déséquilibré ne touche plus le disque) |
| 5 mutations d'automate testées | numéro espacé · ancre sans href · 4 eyebrows sur 8 sections · déséquilibre de langue · libellé du rail différent du hero → **toutes bloquées par le générateur** |
| aperçu publié = démo | `hosting/previews/cristallin/index.html` à `demos/concept-le-cristallin-v1.html` : **diff = 0 ligne** (contrôlé par `difflib`) |

Contrôles : `python3 tools/qa/audit_html.py` → `TOTAL confirmed findings: 0` (385 runs, desktop 385 / mobile 385)
sur le démo **et** sur l'aperçu. Les leçons mécaniques de cette relecture sont versées dans
`design/LESSONS.md` (21/09) — elles valent pour les prochains concepts, pas seulement pour celui-ci.

## Correction de 19:40 — la note vocale était une question d'achat, et une de mes « divergences » était la mienne

**Ce que la transcription de King a changé (vocale de 18:01, 10 s) :** le cabinet a **déjà une page Facebook** en
plus du site, et M. Messoue a demandé **si nous voulions bien lui en créer une autre**. Ce n'est plus un fil « on
vous livre un aperçu », c'est un fil « on nous demande une prestation » → étape `closing`, et le prix peut sortir
d'un message 1 (la règle est consommée : message 1 envoyé, lu, répondu). La feuille d'envoi porte maintenant deux
versions, A sans prix / B chiffrée, **B n'est envoyable qu'après que King a validé qu'AMK fait la page FB**.

**Deux lignes de la maquette réécrites à la source (JSON), une retirée :**
1. `contact.addrFlag` — j'affirmais que son flyer donnait une **adresse différente** (Bonapriso / CTFIC Mballa 2)
   de celle du site (Akwa / FODEC / COMECI). Sur l'image visible à l'écran, **le flyer porte lui aussi Akwa /
   FODEC / COMECI** : l'écart est peut-être de mon côté (j'avais lu le « Bonapriso CTFIC » dans mes propres notes
   d'inventaire, pas dans sa bouche). La page ne corrige plus le client, elle **demande** : « si une deuxième
   adresse existe, écrivez-la moi ».
2. `contact.hoursFlag` — « le flyer ajoute le samedi 8h30–13h30 » est **maintenu** (c'est lisible sur l'image),
   mais reformulé en choix à trancher : *un seul des deux horaires peut être publié*.
3. **Ajout de la ligne « Votre page Facebook »** dans *Nous joindre* : nommée, **pas liée** — son URL nous est
   inconnue et un lien deviné part chez un homonyme. Le lien réel arrive par sa réponse → ici + dans `sameAs`.

**Contrôles rejoués après édition :** `audit_html.py` → **0 finding** (389 runs, desktop 389 / mobile 389) ·
**172 FR / 172 EN** · 0 jeton survivant · 0 `<a>` sans `href` · 3 eyebrows / 8 sections · rail mobile = libellé
du hero · `wa.me/699905577`. `diff` démo ↔ `hosting/previews/cristallin/index.html` = 0 ligne.

**Et la leçon de méthode, pour les prochains dossiers :** une divergence relevée entre deux supports du client
doit être **lue sur les deux supports**, pas sur mes notes. Je l'avais inscrite comme un fait de SON inventaire
alors qu'elle sortait de MON traitement — et elle était devenue une ligne visible de la page, donc une correction
publique du client par nous. Trois libellés de la maquette portent maintenant un conditionnel, pas une accusation.

---

# V2 — 21/09 · 20:15 · « la démo doit être MEILLEURE que son site, pour qu'il compare » (consigne du roi)

## Ce qui a changé, et pourquoi la v1 ne suffisait plus

La v1 était une **lettre d'intention** : belle, sobre, honnête — mais sans une seule image, et sans dire
explicitement en quoi elle bat le site existant. Pour un prospect qui a déjà un site et qui demande « vous avez
consulté mon site ? », ce n'est pas assez : **il compare, donc nous devons comparer avec lui**. Trois ajouts :

1. **Section `#comparatif` — 8 lignes, deux colonnes légendées** (« Votre site actuel » / « Version modernisée »).
   Chaque ligne de gauche est **lue sur sa page ou son flyer**, ce n'est pas un argumentaire : formulaire Nom/Email
   comme seul chemin · bloc des 8 partenaires écrit **trois fois** · « ACTIVA Assurances » **deux fois avec deux
   logos** · samedi absent du site · page Facebook non reliée · FR seul · les trois papiers noyés dans un paragraphe ·
   poids. Pied de section : *« Huit lignes, huit lectures de VOTRE page. Si l'une est fausse, dites-la : je la
   corrige avant même de parler de la suite. »* → c'est une **preuve de travail**, pas un pitch.
2. **Trois visuels générés, inlinés en base64** (166 + 126 + 108 Ko de JPEG, 391 Ko embarqués) : devanture avec
   l'enseigne « LE CRISTALLIN » sur le vert du flyer, tailluse en marche avec praticienne en blouse et lunettes de
   protection, monture sur un visage. Règle tenue : **chacun porte l'étiquette** « Visuel de concept — à remplacer
   par vos photos » en FR **et** EN, et le générateur le vérifie par assertion (`badge.fr in PAGE and badge.en in PAGE`)
   — un rendu qui ne se dit pas devient une fausse photo du client (loi §15).
3. **Sa page Facebook, RELIÉE** (il en a donné l'URL) : dans l'en-tête, dans le bloc contact avec ses chiffres
   publics (515 likes · 44 en parlent · 98 y étaient) et dans `sameAs` du JSON-LD. Les **avis Google — 3 avis,
   note 3,0** — sont affichés tels quels, avec le chantier proposé (répondre aux trois, en demander d'autres à la
   remise du matériel) : ni inventés, ni enjolivés, ni cachés.

## Ce que la V2 a cassé en route (utile pour les prochains builds)

- **Un jeton non remplacé n'était pas un crash.** Le premier essai produisait un HTML de 166 Ko (le gabarit nu)
  et l'audit passait : seule la relecture à l'œil a vu les `@@TOKEN@@` qui sautaient aux yeux. Depuis, le
  générateur refuse d'écrire si un seul jeton survit.
- **Collision de classes, trouvée par l'auditeur — mais par accident.** J'avais nommé `.cmp` à la fois la grille
  du comparatif (`border + background:var(--line)`) et le lien de l'en-tête : le lien héritait du **fond** du
  conteneur. Renommées `.cmpgrid` / `.tocmp`. Leçon de nommage : un jeton de rendu et un nom de classe ne doivent
  jamais partager une racine.
- **`tools/qa/audit_html.py` a un défaut connu, consigné, NON corrigé ce soir** : son `match_compound` ne gère pas
  les sélecteurs composés (`.a.b` → testé comme un seul nom de classe, donc jamais égal), et `effective_bg` lit
  `background:` en attrapant la valeur de `border:`. Résultat : il peut signaler un faux défaut (texte blanc sur
  la couleur d'une bordure) et en rater de vrais. J'ai patché le matching — **régression immédiate sur 6 concepts
  (jusqu'à 32 findings sur `concept-oracare-v1`)** — donc j'ai **remisé le patch** (`git checkout`) et laissé
  l'outil tel quel : corriger l'auditeur exige de rejouer les 11 concepts un par un, ce n'est pas la tâche de
  ce soir, et une correction d'outil qui casse 6 pages livrées est une régression. À ouvrir en ticket
  d'ingénierie séparé, avec la liste des concepts à re-valider.

## État des contrôles, V2

`audit_html.py` → **0 finding** (484 runs, desktop 484 / mobile 484) sur le démo **et** sur l'aperçu publié,
avec `diff démo ↔ aperçu = 0 ligne` · **218 FR / 218 EN** · 9 sections pour 2 eyebrows (plafond `ceil(9/3)=3`) ·
3 `<img>` toutes en `loading="lazy"` + `alt` + `width`/`height` (aucun saut de mise en page) · 0 `alt=""` ·
0 `<a>` sans `href`, 0 ancre morte · `wa.me/699905577` (chiffres seuls) vers **son** numéro, `tel:` 242 65 12 65
et 679 63 20 12 · JSON-LD `Optician` décodé avec les deux URL en `sameAs` · 0 em-dash dans les 218 chaînes
anglaises · **poids 592 Ko** sous le budget d'envoi WhatsApp de 1 100 Ko (assertion).

En-tête mobile : les deux CTA portent `.small` et disparaissent sous 900 px — sur un téléphone, l'action reste
dans le rail collant ; deux CTA dans une barre de 390 px, c'est un bouton sur deux non touchable.

## Reste à faire, et c'est court

Envoyer **le fichier** (pas de lien : rien n'est déployé, et je n'invente pas une URL Vercel) + les 5 lignes de
`sales/Send-LE-CRISTALLIN-2026-09-21-Soir.md`. La seule question encore ouverte côté contenu : **les 12
assureurs** — la page les affiche avec la mention « à faire valider » ; s'il les confirme, ils sortent du
conditionnel ; s'il n'en reconnaît que neuf, on retire les trois autres. Capture mockup non produite (`playwright`
absent du bac) : sur son téléphone, la page se suffit à elle-même.

---

## 22/09 08:3x · le fichier envoyé dimanche contenait un `<script>` en SyntaxError (trouvé en compilant, pas en regardant)

`build_le_cristallin.py` injectait quatre phrases de statut du sélecteur d'assurance avec
`json.dumps(...)[1:-1]` : les **guillemets sautés**, donc le moteur JS lisait `Sélectionnez une assurance`
comme trois identifiants. `Unexpected identifier 'une'` → toute l'IIFE mourait : bascule FR|EN, message
WhatsApp construit à la volée, état du sélecteur, reveals. Comme le reveal portait un `opacity:0` **non gardé**
sur 24 blocs, la page pouvait se présenter **vide sous l'en-tête** chez un lecteur dont le JS ne tournait pas —
le symptôme exact que King a photographié chez le voisin d'Univers Optique le même matin.

**Trois corrections, écrites dans le générateur :** (1) les phrases sont injectées **avec** leurs guillemets
(`json.dumps` garde l'échappement) ; (2) l'état caché n'existe que sous **`html.js`** posé inline dans le
`<head>`, la révélation a son propre `<script>` et son `try/catch` (`show()` en cas de pépin), le budget
tombé à **2 blocs sur 12** (`chart` + `cmpgrid`, le moment écrit de cette page : la lecture comparée) ;
(3) `tools/qa/check_inline_js.py` compile le JS embarqué **avant** écriture — `rc=1`, rien sur le disque.

**Pour l'envoi :** le fichier du dimanche est à remplacer. Version d'aujourd'hui : **620 492 octets**,
sha256 `625ce76a78f9b341…`, 484 runs de texte, 0 finding de contraste, aperçu identique au octale près
(`diff` = 0 ligne). Le message A/B du 21/09 reste valable tel quel : la panne était technique, pas
commerciale — mais il faut **redonner le fichier**, sinon c'est la version cassée qu'il ouvrira.
## 22/09 · 14:35 · audit de la page en ligne (?v=7) — quatre défauts trouvés chez le client, et l'hébergement tranché par le RDAP

**Ce qui a été relu, pas reçu en résumé.** La page `https://lecristallin-concept.vercel.app/?v=7` a été
ouverte et lue en entier (les deux moitiés), et `http://lecristallinoptique.com/` aussi. Le RDAP du domaine
a été interrogé. Trois sources, aucune supposition.

**La source de cette v7 n'est pas dans ce dépôt.** `demos/build_le_cristallin.py` et
`concept-le-cristallin-v1.html` existent ici, mais aucun marqueur de la v7 (« OFFSHORE », « SUNU »,
« 32 ans », « Grandes entreprises & sociétés », `?v=7`) n'y figure : la page publiée a été construite
dans l'autre session. La règle de la maison tient ici : **pas de seconde source reconstituée à
l'aveugle** — on livre la liste exacte des corrections, ou on reçoit le chemin du fichier et on applique
avec les contrôles.

**1 · Le mur des assurances compte faux, dans les deux sens.** La page affiche dix-sept badges et la FAQ
répète « 17 partner insurers ». En face, ce que le client a écrit : 15 sociétés le 21/09 (dont « G.M.C.
ASCOMA CAMEROUN » = UNE société) + 4 nouvelles le 22/09 = **19 distinctes**, deux noms orthographiés par
lui-même (ROYAL ONYX, EXCA) étant des rectifications, pas des ajouts. Sur la page : `G.M.C.` et
`Ascoma Cameroun` sont deux badges (doublon compté deux fois) et **SAAR, ALPHA, L.D.A. manquent**. Le
chiffre 17 est donc exact par accident. À corriger : 19 badges, 19 dans la phrase de FAQ.

**2 · Un bloc imprimé deux fois.** « ### Grandes entreprises & sociétés » + la ligne « 32 ans d'expérience…
» apparaissent en double dans le HTML rendu ; la seconde occurrence n'a pas les quatre badges (CAMRAIL,
SOCAPALM, SAFACAM, P.A.D.). Effet de bord visible sur mobile.

**3 · Horaires : la page contredit son propre flyer.** Publié : `Lun–Ven 8h30–18h30 · Sam 8h30–13h30`.
Flyer envoyé par lui le 21/09 à 18:02 : **09h30–19h30 / 09h30–13h30**. Une heure d'écart sur toute la
semaine, sur le champ le plus consulté d'un site d'opticien. Le 21/09 à 20:10, le message d'envoi
annonçait déjà « 8h30–13h30 » au client : l'erreur est antérieure à la v7, elle n'a jamais été
corrigée depuis. Ce n'est pas à nous de trancher — une ligne à lui envoyer, et la réponse devient la
source unique (tableau + `openingHoursSpecification` + bandeau, avec un contrôle qui refuse toute heure
publiée qui la contredit, comme chez Univers).

**4 · Trois âges qui ne s'accordent pas.** Sa page actuelle : « installé au Cameroun depuis 2010 » et
« 24 ans d'expérience ». Son message du 21/09 21:13 : « 32 Ans d'expérience. ». La v7 : « 32 ans » dans
le corps, « depuis 2010 » dans la description partagée. Formulation qui tient sans inventer, à valider
par lui : « Cabinet installé à Douala depuis 2010, une équipe qui cumule 32 ans d'expérience en
opticien-lunetterie. »

**Les logos ne sont pas à attendre : ils sont déjà publiés par lui.** `http://lecristallinoptique.com/img/clients/`
→ c1 MUTUELLES DES BRASSERIES · c2 (répété) · c3 GRAS SAVOYE · c4 ALPHA · c5 SAHAM · c6 CHANAS ·
c7 + c13 ACTIVA (**doublon chez lui aussi**) · c8 BENEFICIAL GENERAL · c9 SAAR · c11 ZENITHE ·
c12 SAMARITAN · c14 ASCOMA. Quatre de ces noms n'ont jamais été cités dans la conversation : les reprendre
tels quels publierait des partenaires non validés → on lui demande lesquels il garde, en une ligne.

**Hébergement et domaine : la question posée par King a une réponse écrite dans le registre, pas dans un
devis.** `lecristallinoptique.com` — enregistré **13/06/2018**, expire **13/06/2027**, registrar **LWS
(Ligne Web Services, IANA 1630)**, statut `clientTransferProhibited`, nameservers `ns1/ns2.lws-hosting.net`
+ `ns3/ns4.lwsdns.com`. Donc : domaine payé neuf ans d'avance, hébergement mutualisé LWS déjà en place
(gestionnaire de fichiers / FTP), et **rien à acheter ni à facturer des deux côtés**. La route sûre est de
**poser le fichier sur SON hébergement** et de ne pas toucher au DNS : son adresse
`contact@lecristallinoptique.com` vit sur ce domaine et une bascule de nameservers l'emporterait (les MX
aussi). Si on préfère garder l'hébergeur du concept (Vercel, TLS automatique — la page actuelle appelle
toutes ses images en `http://` absolu, donc mixed content dès qu'on passe en https), on ne change qu'un
`A`/`CNAME`, jamais les `NS`, et avec son accord écrit.

**Ce qui se facture, et ce qui ne se facture pas.** Le travail : page, contenus, corrections jusqu'à
validation, mise en ligne (forfait annoncé 100 000 FCFA, 50/50). L'option page/animation Facebook
(+50 000). Éventuellement une maintenance (mises à jour, sauvegarde, surveillance du certificat) — le
seul récurrent honnête ici. Pas d'hébergement, pas de domaine. Et la demande du client « où est
l'assistant pour faire des modifications » (21/09 21:13) doit être répondue avant toute facture : il croit
que le widget est un éditeur. Ce n'en est pas un ; s'il veut s'éditer lui-même, c'est un chantier à part,
donc un prix à part — jamais dans le forfait.
