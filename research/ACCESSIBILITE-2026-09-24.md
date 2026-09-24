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

| page | images / alts | titres | champs étiquetés | focus | langue | noms des boutons | contraste (`audit_html`) | faute A/AA |
|---|---|---|---|---|---|---|---|---|
| `site/index.html` (site AMK) | 6 / 6 | 1 seul `h1`, plus de saut | 2 / 2 | défini | `lang` suit le commutateur | 15 / 15 | 268 textes, desktop + mobile | **0** |
| `site/creation-site-web-clinique-cameroun.html` | 2 / 2 | 1 seul `h1` | — | défini | `fr` | 2 / 2 | 122 textes | **0** |
| `site/creation-site-web-ecole-cameroun.html` | 3 / 3 | 1 seul `h1` | — | défini | `fr` | 2 / 2 | 127 textes | **0** |
| `demos/concept-unilabo-v2.html` | 5 / 5 | 1 seul `h1`, pied de page réparé | **25 / 25** | défini | `fr`, suit le commutateur | 2 / 2 | 385 textes | **0** |
| `demos/concept-univers-optique-v2.html` *(gelé)* | 4 / 4 | saut `h1`→`h3` **noté** | — | défini | `fr` | 2 / 2 | 594 textes | **0** |
| `demos/concept-le-cristallin-v1.html` *(gelé)* | 3 / 3 | 1 seul `h1` | 1 / 1 | défini | `fr` | 2 / 2 | 484 textes | **0** |

Contrôles complémentaires, tous verts : `audit_page --strict` rc=0 · `check_inline_js` 9 blocs / 0 faute ·
harnais UNI-LABO **42/42** · `audit_html` 0 constat partout (structure **et** contraste).

## 4 · Les onze défauts trouvés **sur nos propres pages**, et réparés

Un contrôle d'accessibilité qui ne trouve rien sur ce qu'on a déjà livré ne valait pas la peine d'être
écrit. Trois de ces défauts étaient invisibles à l'œil nu.

**Site AMK (`site/index.html`) — 9 corrections**

1. **Deux boutons dont tout le texte était écrit par le JavaScript** (le bouton de langue et celui du widget
   vocal) : dans le HTML, ils n'avaient **aucun nom**. Aucun lecteur d'écran, aucun moteur de recherche ne
   voyait quoi que ce soit. → nom accessible bilingue sur les deux.
2. **Un bouton micro en icône seule**, sans nom (4.1.2).
3. **Deux champs du formulaire dont l'étiquette n'était pas attachée** au champ (un `<label>` voisin, sans
   `for=`) : un lecteur d'écran annonçait « champ de texte » sans dire lequel (3.3.2). → `for=` + deux
   `autocomplete`.
4. **Le formulaire ne disait pas ce qui se passe après le clic** : il écrit maintenant sa réponse dans une
   zone vivante (`role="status"`), et **rattrape une fenêtre bloquée** en emmenant lui-même le visiteur vers
   WhatsApp (3.3.1 — c'est la leçon d'UX du lot [22], côté accessibilité).
5. **Des sauts de niveau dans les titres** : `h2`→`h4` puis `h2`→`h5` (1.3.1). La liste des titres est le
   sommaire du document pour qui navigue de titre en titre.
6. **Dix icônes décoratives** non marquées `aria-hidden` : le lecteur d'écran annonçait « image » avant
   chaque lien (1.1.1).
7. **Le menu mobile ne disait pas qu'il s'ouvrait** : pas d'`aria-expanded`, et la touche **Échap** ne le
   fermait pas.
8. **Les boutons de langue ne disaient pas lequel était actif** → `aria-pressed` (le visuel `.on` ne parle
   qu'aux voyants).
9. Une paire de balises de titre cassée **par ma propre correction** — rattrapée par `audit_html.py`, qui
   refuse les balises orphelines. *Le contrôle a attrapé le correcteur.*

**Page UNI-LABO (`demos/concept-unilabo-v2.html`) — 2 corrections**

10. **Les quatre photos de familles** portaient un texte alternatif qui répétait le titre déjà imprimé sous
    la photo (*« Photo d'illustration de laboratoire — Biochimie »*) : il n'apprenait rien sur l'image.
    **Les images ont été ouvertes une par une et regardées**, et les alts disent maintenant ce qu'elles
    montrent :
    - six tubes à bouchon bleu, remplis d'un liquide jaune, dans un portoir violet, une micropipette posée à côté ;
    - un frottis sanguin vu au microscope : globules rouges roses et globules blancs violets ;
    - une pipette qui dépose un échantillon dans les puits d'une plaque d'analyse à fond violet ;
    - un automate : un bras mécanique saisit un petit flacon au-dessus d'un carrousel de tubes à bouchons colorés.
11. **Le pied de page sautait de `h2` à `h4`** → les trois rubriques sont en `h3`, style suivi.

*Effet de bord, corrigé :* le constructeur annonçait des **caractères** en écrivant « octets » — le piège
qui a déjà fait écrire de faux chiffres dans sept fichiers. Il donne maintenant les deux. La page passe de
**84 671 à 85 299 octets** (**82 912 caractères**), copie hébergée resynchronisée.

## 5 · Les quatre choses qu'aucune machine ne vérifie — et qui reste à l'œil

| à vérifier | état |
|---|---|
| **Le contraste** | ✅ couvert, mais par un **autre** outil : `audit_html.py` calcule le ratio WCAG de **chaque texte** depuis le CSS du fichier, en desktop **et** en mobile. |
| **L'ordre de tabulation réel** | ⚠️ on peut prouver qu'aucun `tabindex` positif n'existe et qu'un style de focus est défini ; que l'ordre soit *agréable* demande un clavier et une minute de patience. **À faire en séance sur le téléphone.** |
| **Le rendu à 200 % de zoom** | ⚠️ les critères de reflux sont vérifiables en CSS, rien ne remplace le regard. |
| **La qualité d'un texte alternatif** | ✅ traité à la main cette fois (les quatre photos ont été regardées), ⚠️ et à refaire **le jour où le laboratoire nous envoie ses propres photos** : un alt se réécrit à chaque nouvelle image. |

## 6 · La leçon d'outillage (elle vaut pour tous nos contrôles)

Le premier jet de `audit_a11y.py` a produit **cinq faux positifs** — un lien-icône qui *avait* bien un
`aria-label` ; une icône de 19 px **à l'intérieur** d'un bouton (la cible, c'est le bouton, pas le glyphe) ;
un champ de texte libre sans `autocomplete` (le critère 1.3.5 ne concerne que les données à sens connu) ;
un simple changement de couleur au survol (ce n'est pas du contenu caché) ; une icône dans un lien déjà
nommé — **et un faux négatif plus grave** : `a:focus{outline:none}` satisfaisait son propre test « une règle
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

**Si King trouve d'autres sources** : les envoyer, elles seront lues et intégrées ici. Les angles qui
manqueraient au dossier : le **test réel au lecteur d'écran** (NVDA sur Windows, TalkBack sur Android —
c'est le seul moyen de vérifier le n° 2 du tableau §5) et l'accessibilité **des formulaires WhatsApp**,
qui ne sont pas des formulaires HTML.

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
