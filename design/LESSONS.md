# Leçons de métier — design, fabrication, contrôle

*Ajoutées le même jour que le travail qui les a produites (PRE-FLIGHT §4). Ne jamais effacer une leçon :
ajouter, annoter, ou versionner. Celles-ci viennent du build Le Cristallin (21/09/2026) — le premier concept
livré sur un prospect qui a répondu, donc le premier où un défaut de fabrication aurait été vu par le client,
pas par nous.*

---

## 21 Sep 2026 · Le Cristallin (`demos/build_le_cristallin.py`) — trois défauts passés au contrôle automatique, trouvés à la main

**Ce qui s'est passé.** `tools/qa/audit_html.py` est vert (`TOTAL confirmed findings: 0`, 385 runs, desktop et
mobile) sur une page où, coup sur coup : (1) le CTA WhatsApp du hero n'avait **pas de `href`** — il n'existait que
par JavaScript ; (2) l'URL `wa.me` portait le numéro **tel que le publie le flyer** (`699 90 55 77`) : le navigateur
tronque l'attribut au premier espace, donc le lien s'ouvrait sur `wa.me/699` **sans message pré-rempli** — la
fonctionnalité entière du concept ; (3) **7 eyebrows pour 8 sections** (la règle maison dit 1 par 3 sections) :
compté par le script, **pas ressorti en finding**.

**Les règles, maintenant mécaniques.** Elles sont écrites en assertions **dans le générateur**, pas dans l'espoir
d'une relecture :

```python
WA = re.sub(r"\D", "", C["wa"])                 # href → chiffres seuls ; l'AFFICHAGE garde les espaces
assert len(WA) == 9 and WA.startswith("6")
_nohref = re.findall(r'<a(?![^>]*href=)[^>]*>', PAGE); assert not _nohref
_nsec = PAGE.count("<section"); _neyb = PAGE.count('class="eyebrow"')
assert _neyb <= -(-_nsec // 3)                   # ceil(n/3) — pas n//3 + 1
if n_fr != n_en: raise SystemExit("… rien n'est écrit")   # équilibre de langue AVANT l'écriture
```

**Quatre règles de fabrication qui en sortent, valables pour tous les concepts :**

1. **Un bouton n'existe que s'il a une URL dans le HTML.** Un lien que le JavaScript fabrique au chargement est
   mort sur le téléphone qui charge mal — et c'est exactement le téléphone du patient de Douala. Le JS ne fait que
   **re-traduire** un `href` déjà réel. Vérification : `grep -o '<a[^>]*>' file | grep -v href` doit être vide.
2. **Numéro affiché ≠ numéro dans une URL.** `wa.me`/`tel:` prennent les chiffres seuls ; l'espace est une
   convenance de lecture. Le même champ JSON sert aux deux, normalisé à la source et **assertionné à trois
   chiffres près** — sinon le bug est invisible jusqu'à ce qu'un client appelle pour dire que ça ne marche pas.
3. **Le plafond d'eyebrows doit être `ceil(n/3)`**, et l'assertion doit être testée **en la cassant** : ma première
   version (`n//3` avec un « +1 si reste » dans le message) refusait une page conforme à 3/8. Les assertions qui
   ne sont jamais mutées ne protègent rien.
4. **Un fichier d'audit écrit avant les contrôles est un fichier fautif sur le disque.** L'équilibre FR|EN était
   vérifié *après* `write_text` ; la page cassée restait livrable. Ordre canonique : **contrôler → écrire**.

**Bonus, côté CRM (le même soir, même cause racine).** La correction du lead `le-cristallin` (réponse « Ok »,
site existant, prochaine action) était dans le code, rebuild « ✓ », et **absente du CSV** : deux passes
d'écrasement. (a) une clé hors schéma (`Website_status` au lieu de `Website status`) faisait `sys.exit` en fin de
script — donc le CSV que je relisais était celui **de la fois d'avant**, et j'ai lu des chiffres périmés trois
fois de suite en croyant que le builder mentait ; (b) la passe KEYMAP « la forme longue gagne » écrasait le
patch explicite du registre. Leçon : **après un rebuild, vérifier d'abord que la sortie dit `✓` ET que le
`mtime` du CSV a bougé**, puis relire le champ, jamais l'écran d'hier. Le garde-fou « clé hors schéma » est
excellent — c'est le silence du lecteur qui était nul.

**Et la leçon de fond, qui n'est pas un bug.** Ce client avait **déjà un site** et ma fiche CRM disait « aucun
site trouvé » : j'avais recopié une note d'annuaire sans contrôler le domaine, et j'avais construit le message 1
dessus. Avant de maquetter un prospect, `fetch_page` sur son URL — si elle existe — **puis** choisir la douleur.
Un site qui existe mais qui ne convertit pas (formulaire Nom/Email comme seul contact, carrousels dupliqués ×3,
flyer qui contredit le site) se vend mieux en refonte qu'en création : c'était le seul « Ok » de la soirée, et
il est venu d'un message faux.

## 21 Sep 2026 (soir) · Le contrôle n'existe que si le tube ne ment pas

`bash leads/build/rebuild.sh | grep -E "..."` renvoie le code de **`grep`**, jamais celui du builder. Un build
mort en fin de script (« ✗ clé(s) inconnue(s) ») passait donc pour un succès, et j'ai lu trois fois de suite un
CSV **périmé** en accusant mes champs d'être « perdus ». `leads/build/rebuild.sh` porte maintenant la correction :
chaque étape est exécutée par une fonction qui capture le code de retour, imprime `✗ ÉCHEC — <étape>` avec le
`mtime` du CSV quand rien n'a été écrit, et le script sort en `1`. Contre-épreuve faite en **cassant** le schéma
(une clé inconnue posée sur la ligne `le-cristallin`) : rc = 1, message lu, CSV intact ; après revert, rc = 0.

**Règle tenue, sans script :** après toute reconstruction, lire la **dernière** ligne du journal (le tampon
`tail -n`, pas un `grep` filtrant) ou vérifier le `mtime` de la cible. Un `grep` est un filtre, pas un test.

**Le même soir, troisième forme du même défaut (et la plus embarrassante).** Dans `build-notes.md`, la ligne
§13 du CTA collant portait « ✓ identiques au hero » — **c'était faux** : le hero disait « Réserver un examen de
vue », le rail « Réserver sur WhatsApp ». Réglé par le code, pas par la bonne intention : le libellé du rail est
**dérivé** de `hero.book` dans le JSON (une seule source), et le générateur assert que les deux `<span>` du hero
et du rail sont égaux. Leçon tenue : **dans une check-list, un point sans machine derrière est une opinion.**

**Règle de contenu qui en découle (loi maison §13, côté copie) :** une divergence relevée entre deux supports du
client doit être **lue sur les deux supports**, pas dans mes notes de tri. Ce que j'avais écrit — « son flyer donne
une adresse que son site ne donne pas » — sortait de MON inventaire : sur l'image, le flyer porte la MÊME adresse.
Une note d'audit recopiée sans relecture est devenue une ligne visible de la page, donc **une correction publique
du client par nous**. Forme définitive dans la maquette : on ne corrige pas, on **demande** (« si un second local
existe, écrivez-le moi — une page ne porte qu'une adresse validée par vous »). Deux autres lignes suivent la même
règle (horaire du samedi, liste des assureurs) : **question explicite + conditionnel**, jamais affirmation.

## 21 Sep 2026 · 20:20 · `audit_html.py` est un filet, pas un juge (défaut consigné, patch remisé)

Deux défauts **mesurés** dans l'outil ce soir : `match_compound` ne sait pas lire un sélecteur **composé**
(`.a.b` est testé comme un seul nom de classe → jamais égal), et `effective_bg` lit la propriété `background`
sans exiger le point-virgule, donc il attrape parfois la couleur d'une **bordure** comme fond. Conséquence
concrète : il a signalé un faux 1,38:1 sur un lien d'en-tête bien contrasté, et il n'a rien vu pendant qu'un
jeton `@@TOKEN@@`全文 sautait à l'œil dans la page.

**J'ai patché le matching — et je l'ai remisé dans la minute** : la correction fait apparaître **des régressions
sur 6 concepts déjà livrés** (jusqu'à 32 findings sur `concept-oracare-v1`). Un outil de contrôle ne se corrige pas
en même temps qu'une livraison : d'abord la liste des pages à re-valider, ensuite le patch, avec le temps de
relire chaque finding. Écrit ici pour que le prochain qui « optimise » l'auditeur sache dans quoi il met les mains.

**Ce que ça change à ma discipline, dès demain :** un `TOTAL confirmed findings: 0` ne prouve que ce que l'outil
sait voir. Les cinq assertions **dans le générateur** (jetons survivants · `<a>` sans `href` · espaces dans une
URL `wa.me` · plafond d'eyebrows · paires de langue équilibrées · étiquette obligatoire sur chaque visuel ·
poids ≤ 1 100 Ko) sont ce qui protège vraiment, parce qu'elles échouent **bruyamment** et qu'elles sont
individuellement **testées en les cassant**. Règle tenue : *une vérification qui n'a jamais été vue en échec
n'est pas une vérification, c'est un rituel.*
## 21 Sep 2026 · 23:20 · Univers Optique — trois lois sorties d'un build « propre » (CRM, SEO, images)

**1. Une sortie ne se corrige jamais à la main — et un tableau de bord muet est pire qu'absent.**
Deux ratages du même soir : (a) l'état de Le Cristallin (`closing`, page FB à 515, date de relance, verbatim
de la vocale) vivait **dans `leads/CRM.csv`** ; `rebuild.sh` l'a effacé **en silence** ; (b) `stage="closing"`
n'existait **ni dans `STAGE_ORDER` ni dans `STAGE_LABEL`** de `views.py`, donc nos deux fils les plus avancés
n'apparaissaient dans **aucune** vue — le compteur n'était pas faux, il taisait le seul chiffre qui compte.
**Règle :** tout fait d'échange (qui a répondu, quoi, à quelle heure, avec quelle URL lue) s'écrit **dans le
générateur**, et **toute valeur d'énumération doit être couverte par une assertion** — « aucun stage du CSV
hors de la vue », « aucune clé hors des colonnes canoniques », « un slug inconnu fait avorter ». Le garde-fou
a mordu dans la minute : `bamfam_*`, `Last FB post`, `first_touched` refusés ; mutation du faux slug → `rc=1`,
CSV intact ; **deux rebuilds → CSV identique**.

**2. « Dig deep » veut dire : lire ce que le prospect ne sait pas avoir publié.** Le domaine **ne résout
pas** (DNS + `curl 000`), mais il **existe** ; Wayback donne **10 captures** et la date de mort (**09/01/2024**,
répertoire Apache vide) ; la fiche Google porte **3,3/5 · 6 avis · champ site vide · aucun réseau** ;
l'annuaire Maligah porte **BP 4680 + trois lignes + trois champs vides** ; une annonce retirée (kerawa) date
l'activité au **01/08/2009** et nomme **prothèses oculaires** et **verres de sécurité**. Résultat concret :
ma phrase du 17:50 (« absent du web ») était **fausse**, et le vrai constat est **plus fort** — « sa seule page
vivante est celle d'un autre ». **Une affirmation sur la présence en ligne d'un prospect porte une source et
une date, ou ne part pas.** Ne jamais publier une correction du client : ses contradictions (deux versions de
son fixe, un « 15 % » sans offre) deviennent **des questions dans la page**.

**3. Un rendu n'est jamais une photo, et un badge ne se décrète pas : il s'assemble.** Les trois visuels
(dévoré par `generate_image`, compressés en JPEG 74–80) portent l'étiquette FR **et** EN ; la contrainte est
vérifiée par assertion (`badge in PAGE` × langues) **et** par un budget (≤ 260 Ko/visuel, ≤ 1 100 Ko/page)
parce que le livrable est **une pièce jointe WhatsApp**, pas une URL. D'où le **repli `--sobre`** généré par
le même gabarit (83 Ko, 0 visuel, dit dans la page, audit 0 finding) : une promesse d'envoi doit rester tenable
si le canal refuse le poids. **Jamais** un lien de preview inventé (`amk-cm.vercel.app/univers/` = 404 tant que
King ne déploie pas). Et **jamais** de balisage `aggregateRating` sur une base de 6 avis, **jamais** de
`sameAs` deviné : ce qui n'est pas lu n'est pas écrit — ni sur la page, ni dans le code.
## 21 Sep 2026 · 23:55 · Un fichier peut être « conforme » et cassé (Univers Optique, repasse qualité)

Deux défauts trouvés **après** un `audit_html.py` à 0 finding : (1) le pied de page avait 5 blocs dans une
grille déclarée à 4 colonnes — le CTA tombait seul sur une ligne de décalée ; (2) la règle
`.cta.small{display:none}` était **orpheline** : le bouton n'avait jamais été posé dans le `<header>`, donc
sur desktop (rail mobile masqué) **il n'existait plus aucun chemin vers WhatsApp entre le hero et le pied de
page**. Le premier se voyait dans le navigateur, le second dans le comportement d'un visiteur — **aucun des
deux n'est un contraste**, et c'est exactement ce que notre auditeur mesure.

**Règle :** après l'auditeur, trois contrôles **de géométrie sur le fichier généré**, écrits dans le
générateur : (a) **aucune règle CSS orpheline** (toute classe stylée doit exister dans le DOM, sauf celles
posées par le JS) ; (b) **enfants directs = colonnes déclarées** pour toute grille, en parsant le HTML, pas
en comptant à l'œil ; (c) **au moins un chemin de conversion visible hors du hero et hors du rail mobile**.
Chacun **muté une fois pour vérifier qu'il échoue** (rc=1 sur `.orphantest`, sur le 5ᵉ bloc du footer).
**Corollaire honnête, à écrire dans les notes de livraison : sans navigateur dans le bac, la densité et les
débordements fins ne sont PAS vérifiés — on le dit, on ne le prétend pas « passé à l'œil ».**

## 2026-09-21 23:59 · un rendu généré porte la **norme**, pas le réel — et jamais un nom inventé

**Ce qui s'est passé (UNIVERS OPTIQUE) :** j'avais briefé les images en « *documentary realism, Bépanda
neighbourhood, natural daylight* ». Résultat : trois rendus **techniquement** et **commercialement faux** —
un local aux murs fatigués, des présentoirs vides. Le roi a refusé : « *je n'aime pas les images generer, ça ne
représente pas une clinique moderne* ». Sa règle comparative (« *the demo has to look BETTER than his actual
website* ») s'applique **aux pixels autant qu'au code** : un audit à 0 finding sur une page qui montre une
boutique délabrée ne vaut rien, parce que le client, lui, lit d'abord l'image.

**Deuxième défaut du même lot, trouvé en relisant les fichiers avant câblage :** les rendus portaient **du
lettrage inventé** — « VISION CLAIRE OPTIQUE » sur un mur, « OPTICAL SERVICES DOUALA » sur une blouse, et chez
Le Cristallin une plaque de verre avec du **texte miroité sans sens**. Une maquette n'a pas le droit d'écrire un
nom que le client n'a pas : c'est une info fausse en image, et le hasard peut en faire un concurrent.

**Règle 1 — brief d'image pour tout commerce (clinique, école, optique) :** *moderne, tenu, équipé* —
menuiserie claire + sombre, **présentoirs rétroéclairés**, comptoir vitré, **appareils de mesure réels et
propres**, personnel en tenue soignée, lumière équatoriale ; **négatifs écrits dans le prompt** : pas de
peinture qui pèle, pas d'encombrement, pas de néon, pas de halo bleu/violet « IA », pas de verre givré décoratif,
pas de texte incrusté. **Le réalisme local se met dehors** (rue, palmiers, mobilité visible derrière la vitre),
jamais dans la dégradation de l'intérieur.

**Règle 2 — aucune image n'est câblée sans relecture humaine enregistrée :** on **ouvre** chaque rendu, on
vérifie (a) niveau de finition, (b) **zéro lettrage**, (c) mains/visages/ombres plausibles, (d) **aucun contexte
médical chirurgical**. Le bac n'a pas d'OCR : le **contrôle est manuel mais rendu obligatoire par la machine** —
ici une fiche `IMG_REVIEW` par visuel, sans quoi le générateur sort `rc=1`. Un point de relecture sans contrôle
derrière est une opinion.

**Règle 3 — la légende décrit son image.** Quand le rendu change de sujet, le texte qui le présente change dans
le même commit (« La devanture » → « **La salle de vente** »), et dit ce qui restera vrai à la livraison :
*cette image est un rendu de concept, la vôtre la remplacera, devanture et enseigne comprises*.

