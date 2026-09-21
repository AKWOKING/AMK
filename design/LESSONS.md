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
