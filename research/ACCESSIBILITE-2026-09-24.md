# Accessibilité — ce qu'on promet, ce qu'on a vérifié, ce qui reste à l'œil

**24 septembre 2026 · lot [27] · déclencheur : « start with accessibility, I guess you will do research
online, I'll add what I can find »**

Ce document est le compte rendu lisible du lot. La doctrine est en **§27** de `AMK-DESIGN-SKILLS.md`, le
détail des sources en **lot [27]** de `research/YouTube-Lessons.md`, l'outil est
**`tools/qa/audit_a11y.py`** (testé par `tools/qa/test_audit_a11y.py`).

---

## 1 · Le niveau qu'on vise, et pourquoi pas plus haut

**WCAG 2.2, niveau AA.** Un **standard et un niveau** — jamais l'adjectif seul.

Silktide nomme les niveaux comme un client les entend : **A = « must do »**, **AA = « should do »**,
**AAA = « reaching for the stars »** (vidéo en langue des signes, contraste 7:1 partout, cibles 44 px
partout). AAA n'est pas tenable sur une page commerciale, et aucun laboratoire ni aucune école d'ici ne
paierait pour ça. **AA est le niveau qu'un appel d'offres ou un ministère exige.** C'est donc celui-là, et
on dit lequel.

**Ce qu'on ne dira jamais : « certifiée ».** Personne ne certifie rien ici ; nous mesurons, et nous disons
sur quels critères.

## 2 · L'outil

```
python3 tools/qa/audit_a11y.py site/*.html demos/concept-*.html    # le rapport, critère par critère
python3 tools/qa/audit_a11y.py --strict <fichier>                 # rc=1 dès une faute de niveau A ou AA
python3 tools/qa/test_audit_a11y.py                               # l'outil est-il fiable ? (12 défauts, 1 page saine)
```

Chaque constat porte **le numéro du critère** (`[1.1.1]`, `[2.4.7]`, `[3.3.2]`…) : c'est ainsi qu'un audit
se lit et se conteste. Et l'outil **dit aussi ce qui est conforme** — un rapport qui ne liste que des
fautes ne peut pas être signé par celui qui doit le signer.

L'outil est branché sur la **route « website build »** du `PRE-FLIGHT.md` et sur la **porte technique §1b**.
Toute page qu'on livre passe par là.

## 3 · Résultats sur nos pages (24/09, après corrections)

| page | repères | images / alts | titres | champs étiquetés | focus | langue | noms des boutons | contraste (`audit_html`) | faute A/AA |
|---|---|---|---|---|---|---|---|---|
| `site/index.html` (site AMK) | **main + nav + header + footer + lien d'évitement** | 6 / 6 | 1 seul `h1`, plus de saut | 2 / 2 | défini | `lang` suit le commutateur | 15 / 15 | **269 textes**, desktop + mobile | **0** |
| `site/creation-site-web-clinique-cameroun.html` | **main + nav + header + footer + lien d'évitement** | 2 / 2 | 1 seul `h1` | — | défini | `fr` | 2 / 2 | 122 textes | **0** |
| `site/creation-site-web-ecole-cameroun.html` | **main + nav + header + footer + lien d'évitement** | 3 / 3 | 1 seul `h1` | — | défini | `fr` | 2 / 2 | **128 textes** | **0** |
| `demos/concept-unilabo-v2.html` | **main + nav + header + footer + lien d'évitement + 2 groupes nommés** | 5 / 5 | 1 seul `h1`, pied de page réparé | **25 / 25** | défini | `fr`, suit le commutateur | 2 / 2 | 385 textes | **0** |
| `demos/concept-univers-optique-v2.html` *(gelé)* | — | 4 / 4 | saut `h1`→`h3` **noté** | — | défini | `fr` | 2 / 2 | 594 textes | **0** |
| `demos/concept-le-cristallin-v1.html` *(gelé)* | — | 3 / 3 | 1 seul `h1` | 1 / 1 | défini | `fr` | 2 / 2 | 484 textes | **0** |

Contrôles complémentaires, tous verts : `audit_page --strict` rc=0 · `check_inline_js` 9 blocs / 0 faute ·
harnais UNI-LABO **42/42** · `audit_html` 0 constat partout (structure **et** contraste).

## 4 · Les défauts trouvés **sur nos propres pages**, et réparés

Un contrôle d'accessibilité qui ne trouve rien sur ce qu'on a déjà livré ne valait pas la peine d'être
écrit. Trois de ces défauts étaient invisibles à l'œil nu.

> **Correction du 24/09 — à lire d'abord.** La première version de ce rapport annonçait « deux boutons
> sans aucun nom, leur texte étant écrit par le JavaScript ». **C'était faux.** C'était un faux positif de
> la première version de mon outil, qui lisait le contenu des boutons sans regarder leur `aria-label`, et
> qui ignorait le `<span>` lisible du bouton micro (« Tap to speak »). Pire : la « correction » sortie de
> cette fausse alerte a remplacé un nom bilingue qui **suivait la langue du visiteur** par un nom figé dans
> les deux langues — elle a été **annulée**. **Huit défauts réels restent : six sur le site, deux sur
> UNI-LABO.** Le faux positif, lui, s'est corrigé dans l'outil. Détail en **§6**.

**Site AMK (`site/index.html`) — 6 corrections réelles**

1. **Deux champs du formulaire dont l'étiquette n'était pas attachée** au champ (un `<label>` voisin, sans
   `for=`) : un lecteur d'écran annonçait « champ de texte » sans dire lequel (3.3.2) — plus deux
   `autocomplete`, pour que le téléphone aide au lieu de faire taper.
2. **Le formulaire ne disait pas ce qui se passe après le clic** : il écrit maintenant sa réponse dans une
   zone vivante (`role="status"`), et **rattrape une fenêtre bloquée** en emmenant lui-même le visiteur
   vers WhatsApp (3.3.1 — c'est la leçon d'UX du lot [22], côté accessibilité).
3. **Des sauts de niveau dans les titres** : `h2`→`h4` puis `h2`→`h5` (1.3.1). La liste des titres est le
   sommaire du document pour qui navigue de titre en titre.
4. **Dix icônes décoratives** non marquées `aria-hidden` : le lecteur d'écran annonçait « image » avant
   chaque lien (1.1.1).
5. **Le menu mobile ne disait pas qu'il s'ouvrait** : pas d'`aria-expanded`, et la touche **Échap** ne le
   fermait pas.
6. **Les boutons de langue ne disaient pas lequel était actif** → `aria-pressed` (le visuel `.on` ne parle
   qu'aux voyants).

**…et deux défauts que j'ai introduits moi-même en corrigeant** — la ligne la plus utile de tout le lot :

8. Une paire de balises de titre **cassée par ma propre correction**, rattrapée par `audit_html.py` (qui
   refuse les balises orphelines) ;
9. une **zone de statut sans `id`** : le JavaScript la cherchait par son identifiant, ne la trouvait pas, et
   n'écrivait donc jamais rien — une correction d'accessibilité qui ne faisait rien, sans le moindre
   message d'erreur. Rattrapée par le **test de comportement** écrit dans la foulée
   (`tools/qa/test_site_a11y_behaviour.mjs`), qui exécute vraiment le JavaScript de la page dans un DOM.

*Le contrôle a attrapé le correcteur — deux fois.* C'est pour ça que la règle « on corrige la page, jamais
l'assertion » a une sœur : **une correction non exécutée n'est pas une correction.**

**Page UNI-LABO (`demos/concept-unilabo-v2.html`) — 2 corrections (7 et 8)**

7. **Les quatre photos de familles** portaient un texte alternatif qui répétait le titre déjà imprimé sous
    la photo (*« Photo d'illustration de laboratoire — Biochimie »*) : il n'apprenait rien sur l'image.
    **Les images ont été ouvertes une par une et regardées**, et les alts disent maintenant ce qu'elles
    montrent :
    - six tubes à bouchon bleu, remplis d'un liquide jaune, dans un portoir violet, une micropipette posée à côté ;
    - un frottis sanguin vu au microscope : globules rouges roses et globules blancs violets ;
    - une pipette qui dépose un échantillon dans les puits d'une plaque d'analyse à fond violet ;
    - un automate : un bras mécanique saisit un petit flacon au-dessus d'un carrousel de tubes à bouchons colorés.
8. **Le pied de page sautait de `h2` à `h4`** → les trois rubriques sont en `h3`, style suivi.

*Effet de bord, corrigé :* le constructeur annonçait des **caractères** en écrivant « octets » — le piège
qui a déjà fait écrire de faux chiffres dans sept fichiers. Il donne maintenant les deux. La page passe de
**84 671 à 85 299 octets** (**82 912 caractères**), copie hébergée resynchronisée.

## 4 bis · Deuxième passe, le même jour (lot [28]) — 4 défauts de plus, dont un de niveau A

King a envoyé quatre sources supplémentaires, qui tombaient pile sur les deux trous annoncés : **le test réel
au lecteur d'écran** et **les formulaires**. Ce qu'elles ont fait sortir :

1. **Les trois pages du site n'avaient AUCUN repère `<main>`.** C'est le tout premier constat du tutoriel NVDA :
   sans repère principal, le lecteur annonce l'en-tête, le menu, le pied de page… et **« page blank »** au
   milieu d'une page pleine. Corrigé (`<main id="contenu">` sur les trois, plus `main{display:block}`).
2. **Deux de ces pages n'avaient pas de lien d'évitement** « Aller au contenu » — critère **2.4.1, niveau A**.
   Corrigé : le lien est la première chose qu'un `Tab` atteint.
3. **Le formulaire du site échouait en SILENCE.** `if (!biz) return false;` : un clic sans nom ne produisait
   rien — pas de message, pas de focus, aucune annonce. C'est mot pour mot le défaut que le tutoriel NVDA
   décrit et que tout l'article de Kortic traite. Cas vicieux en prime : un champ rempli d'**espaces** passe la
   validation native du navigateur, donc ce JavaScript était le seul filet, et il se taisait. Corrigé : la zone
   vivante annonce ce qui manque, le champ passe en `aria-invalid`, et **le focus l'atteint**.
4. **Un astérisque d'obligation que rien n'expliquait** (« Nom de l'école ou de la clinique \* »). Un astérisque
   ne se vocalise pas et son sens doit être donné *avant* le formulaire — ce qui n'était fait nulle part.
   Appliqué la règle de Kortic : on marque le **facultatif**, pas l'obligatoire.

**Deux contrôles neufs dans l'outil**, nés des mêmes sources : **2.4.1 les repères** (sans `<main>`, la page
est signalée) et **1.3.1 les groupes nommés** (un `<fieldset>` sans `<legend>` ne nomme rien : le lecteur
annonce des cases isolées). Et **3.1.2** passe d'un doute à une vérification : il regarde maintenant *comment*
la page bilingue cache l'autre langue — `display:none` la retire de l'arbre d'accessibilité, `opacity:0` la
laisse dedans et le lecteur annonce **les deux langues**. UNI-LABO : `display:none` ✅. Site : une seule langue
dans le document à la fois ✅.

**Le total honnête : 12 défauts réels** (8 du lot [27] + 4 du lot [28]), **2 défauts que j'ai causés moi-même
en corrigeant**, et **1 fausse alerte** que j'ai dû retirer. Les trois catégories sont dans ce rapport.

---

## 5 · Les quatre choses qu'aucune machine ne vérifie — et qui reste à l'œil

| à vérifier | état |
|---|---|
| **Le contraste** | ✅ couvert, mais par un **autre** outil : `audit_html.py` calcule le ratio WCAG de **chaque texte** depuis le CSS du fichier, en desktop **et** en mobile. |
| **L'ordre de tabulation réel** et **ce que ça donne à l'oreille** | ⚠️ on peut prouver qu'aucun `tabindex` positif n'existe et qu'un style de focus est défini ; le reste demande un clavier, un lecteur d'écran et cinq minutes. **La procédure existe maintenant** : `tools/qa/PROTOCOLE-LECTEUR-ECRAN.md` (huit touches, gestes TalkBack, et ce qu'on doit entendre sur NOS pages — 44 titres et 42 liens sur le site, « *1 · Vos analyses, groupe de cases à cocher, 1 sur 19* » sur UNI-LABO). À faire par King, ou en séance. |
| **Le rendu à 200 % de zoom** | ⚠️ les critères de reflux sont vérifiables en CSS, rien ne remplace le regard. |
| **La qualité d'un texte alternatif** | ✅ traité à la main cette fois (les quatre photos ont été regardées), ⚠️ et à refaire **le jour où le laboratoire nous envoie ses propres photos** : un alt se réécrit à chaque nouvelle image. |

## 6 · La leçon d'outillage (elle vaut pour tous nos contrôles)

Le premier jet de `audit_a11y.py` a produit **six faux positifs** — un lien-icône qui *avait* bien un
`aria-label` ; une icône de 19 px **à l'intérieur** d'un bouton (la cible, c'est le bouton, pas le glyphe) ;
un champ de texte libre sans `autocomplete` (le critère 1.3.5 ne concerne que les données à sens connu) ;
un simple changement de couleur au survol (ce n'est pas du contenu caché) ; une icône dans un lien déjà
nommé ; et **deux boutons du site déclarés « sans nom » alors que le nom était là** — dans un attribut
`aria-label` pour l'un, dans un `<span>` visible pour l'autre (c'est le faux positif qui a fait écrire une
fausse correction dans la première version de ce rapport) — **et un faux négatif plus grave** : `a:focus{outline:none}` satisfaisait son propre test « une règle
de focus existe », c'est-à-dire que l'outil validait exactement la règle qui supprime le repère de focus.

Tout a été corrigé **dans l'outil**, jamais toléré. D'où la règle écrite dans son test : *un contrôle n'est
digne de confiance qu'après avoir refusé une page cassée exprès, accepté une page saine, et tourné sans se
plaindre sur nos propres pages.* Même leçon qu'au lot [26], où deux vidéos sur cinq étaient muettes :
**vérifier l'instrument avant de croire la mesure.**

## 7 · Ce qui n'a pas été touché

**Le Cristallin et Univers Optique restent gelés** (consigne : on ne touche plus rien avant qu'ils paient).
Leurs constats sont **notés dans le test du contrôle**, pas corrigés : un saut `h1`→`h3` sur Univers, et un
lien portant une icône sans nom explicite sur le Cristallin. Le jour où ils paient, c'est deux minutes.

## 8 · Les sources lues

Envoyées par King : **Silktide** (`youtu.be/5H1JGdqLrWo`, 1:50 — les trois niveaux) et le cours d'audit
d'**Accessible Web** (playlist `PLqQI0lmiVs1jhQQNAprIPCjFUYVBB7tY8`, **55 vidéos, une par critère**).
Cherchées aux endroits qui font foi : **W3C** — `TR/WCAG21` et le quickref de la **WCAG 2.2** (la plus
récente ; 2.1 et 2.0 restent valides) — et **MDN** : *Understanding WCAG*, *Keyboard accessible*, *Text
labels and names*.

Écarté volontairement : l'extension et l'offre payante du formateur (c'est du marketing, pas de la
documentation), les critères de niveau AAA (hors périmètre annoncé), et les vidéos sans parole — règle du
lot [26].

**Deuxième tour, ajouté par King le 24/09 (lot [28])** — et il tombait exactement sur les deux angles qui
manquaient :

- **`youtu.be/aAh1PFsgcBY`** — *NVDA Screen Reader Tutorial: How to Use It for Accessibility Testing*
  (Software Testing 101). Lu en entier. C'est le mode d'emploi du test à l'oreille, et sa meilleure idée est
  une comparaison : **le même formulaire, fautif puis irréprochable** — d'un côté « page blank » sur une page
  pleine, des cases annoncées sans leur groupe, aucune erreur annoncée ; de l'autre, chez Apple, tout est dit.
- **`kortic.com/formulaires-et-messages-d-erreurs-accessibles.html`** (Anthony Ladeuil, FR, CC BY-NC-SA) —
  le traitement le plus complet qu'on ait trouvé de la partie que tout le monde saute : **les erreurs**. On
  en a pris la doctrine des champs obligatoires (marquer le **facultatif**), la règle du `fieldset`/`legend`,
  le patron du **résumé d'erreurs** (un conteneur focalisé, chaque erreur étant un bouton qui mène au champ et
  le marque `aria-invalid`), et une phrase qui vaut à elle seule l'article : une date au format `jj/mm/aaaa`
  se vocalise « *gigi barre oblique aime aime barre oblique ah ah ah ah* ».
- **`github.com/videvelopers/TalkBack-Sound-effect-for-NVDA-`** — un module NVDA (Python, MIT, 2023) qui
  imite les sons de TalkBack. L'intérêt n'est pas le module mais ce qu'il imite : **sur Android on explore
  élément par élément, un son par objet.** Ce qui n'est pas atteignable au balayage n'existe pas — et c'est le
  téléphone que nos clients ont.
- **`faq.whatsapp.com/3614672068767202`** (Android, fr_FR) — ❓ **PAGE NON LUE.** Elle répond **403** à notre
  outil de récupération (quatre tentatives : URL d'origine, sans paramètres, `fr_FR`, `en_US`) et le bac à
  sable n'a **aucun réseau en ligne de commande**. Je ne résume pas ce que je n'ai pas lu. **Coller le texte
  ici suffit** et son contenu entre dans le dossier comme les autres.

**Ce que le dossier ne peut pas encore prouver, et qu'on dit plutôt que de le maquiller :** ni NVDA ni
TalkBack ne tournent dans ce bac à sable (pas de Windows, pas d'Android, pas de navigateur installable).
Le protocole existe, il est écrit pour être exécuté par un humain — **et la première exécution reste à faire**.

## 9 · Ce que ça vaut pour un client, en un paragraphe honnête

Aucune loi camerounaise n'oblige aujourd'hui un laboratoire ou une école à être accessible : **la raison de
le faire n'est pas la loi, c'est le visiteur.** Le même travail dont un patient aveugle a besoin — du vrai
texte plutôt que du texte dans une image, des étiquettes attachées aux champs, une page qui survit à un zoom
de 200 %, des cibles assez grandes pour un pouce, du texte lisible en plein soleil sur un écran bon
marché — est exactement ce dont tout le monde a besoin sur un téléphone en 3G à Bonamoussadi. C'est aussi
la différence visible entre notre page à 150 000 FCFA et un gabarit, et elle ne coûte rien de plus à
garder. Pour l'école d'octobre, ça devient un argument : une école qui reçoit des parents handicapés n'est
pas servie par un site que ces parents ne peuvent pas utiliser.

**En séance, si la question vient** — et seulement si elle vient — la phrase est : *« la page est
construite pour être lisible par tous, y compris les visiteurs qui utilisent un lecteur d'écran : c'est
vérifié critère par critère. »* Pas « certifiée ».
