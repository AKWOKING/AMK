# DM OPTIQUE SARL — audit contre `AMK-DESIGN-SKILLS.md`, et ce qu'il a changé

**Date** : 28/10/2026 · **Périmètre** : `hosting/previews/dmoptic/` (97 pages, FR + miroir EN)
**Méthode** : les portiques de `tools/qa/` d'abord, l'œil ensuite, dans cet ordre. Le navigateur tourne
enfin dans cette session (`bash tools/video/install.sh`, qui installe désormais aussi Pillow, numpy et
Playwright), donc tout ce qui se mesure sur un rendu a été mesuré sur un rendu : Chromium 153,
captures 1440×900 et 390×844. **Aucune ligne de ce rapport ne dit « non mesurable ici ».**

**Verdict avant** : la page d'accueil passait les portiques de contraste et d'accessibilité, et **échouait
sur six règles du livre** — dont deux que personne n'avait vues parce que rien ne les mesurait.

---

## 1 · Les instruments, et ce que chacun a le droit de dire

| Instrument | Ce qu'il a dit, avant | Après |
|---|---|---|
| `audit_html.py` (contraste AA, 2 contextes) | 0 constat sur 317 passages | **0 constat sur 306** |
| `audit_a11y.py` (WCAG 2.2 A/AA) | 0 faute | 0 faute |
| `audit_page.py` (hiérarchie, densité) | 1 constat : **9 tailles de texte** | **0 constat** |
| `audit_hero.py` (premier écran) | 0 faute | 0 faute |
| `audit_reveal.py` (le bug des 142 blocs) | **2 fautes** | **0 faute**, sur les 97 pages |
| `audit_images.py` | 0 sur 6 images | 0 |
| `audit_claims.py` (verrous client) | 0 infraction | 0 |
| `check_inline_js.py` | 5 blocs compilés | 5 blocs, 0 faute |
| `shot.py` (Chromium réel) | VERT, 4 P3 | **VERT, 0 P1 · 0 P2 · 4 P3** |
| `audit_palette.py` (60-30-10, nouveau) | **marque à 0,07 %** de la page | **76 / 21 / 1,3 — 0 faute** |
| `test_dmoptic_page.mjs` (comportement) | 4 assertions cassées | **toutes passent** |

---

## 2 · Ce qui violait le livre, et ce qui a été fait

### 2.1 §13 — la porte de révélation (`audit_reveal.py`, 2 fautes)

`html.js .rv{opacity:0}` masquait `.rv.in{opacity:1}` par spécificité. C'est exactement le bug qui a rendu
**142 blocs invisibles le 23/10** : la classe était bien ajoutée, rien ne s'affichait, et aucune erreur en
console. Le JavaScript n'avait qu'un `catch` — pas de filet en cas d'observateur muet.

**Fait** : règle de base en `html.js .rv:not(.in)`, `revealAll()` appelée explicitement, **minuteur de
secours à 2,5 s**, et repli `@media (scripting:none)`. Sur les 97 pages : **836 blocs, 0 faute**.

### 2.2 §7 — le premier écran portait 23 blocs de texte

Le plafond du livre est **4** (sourcil + titre + sous-texte + boutons, une carte comptant pour un).
La page avait, sous les boutons, une **table de trois faits** (Où / Sur WhatsApp / Opticien) qui
**doublonnait mot pour mot la carte d'identité** déjà posée à droite. Personne ne l'avait vu : elle était
jolie, alignée, et redondante.

**Fait** : `dl.facts` retirée (HTML + CSS). Mesure après : **6 blocs** (sourcil, titre, ville, chapeau,
deux boutons, la carte). Le portique `shot.py` compte désormais ce chiffre à chaque passage.

### 2.3 §5 — douze tailles de texte pour une page

Mesuré : 13, 14, 15, 16, 16,3, 17, 17,6, 18,9, 19,2, 26, 36,8, 52 px. Le repère du livre est **6**.

**Fait** : les jetons absorbent les valeurs orphelines (`--fs-sm` 15, `--fs-xs` 13, `--fs-lead` = base),
et les cinq tailles écrites à la main (`1.2rem`, `1.1rem`, `1.06rem`, `1.02rem`, `.94rem`, `.5em`)
retournent sur l'échelle. Résultat : **52 / 36,8 / 19,2 / 17 / 15 / 13 — six tailles**.

### 2.4 §6.1 — la couleur du cabinet était invisible à l'échelle du document

C'est le constat que **seul** `audit_palette.py` pouvait faire : sur la page entière, le bleu de marque
`#1A3F86` occupait **0,07 %** des pixels identifiés. Le cabinet a une couleur, la page ne la montrait pas.
La bande sombre, elle, portait **19 %** de la surface en quasi-noir `#0A1220`.

**Fait** : la bande passe au bleu du cabinet (`--night` `#0B2450`, `--night-2` `#0E2C60`). Le commentaire
du fichier disait déjà « encre marine » : le code ne le faisait pas. Mesure après : **dominant 76,4 % ·
marque 20,6 % · accent 1,3 % — 0 faute, 0 avertissement**. Le bleu entre aussi dans le premier écran
(sourcil, bouton d'appel, filet de la carte) : 0,01 % → 0,25 %.

### 2.5 §3.3 — trois cartes égales

La vitrine était `repeat(3, 1fr)` : le défaut que le livre nomme en premier. **Fait** :
`1.35fr 1fr 1fr`. Asymétrie réelle, pas décorative : la première monture est la photo la plus parlante.

### 2.6 La dérive : du code vivant absent du gabarit

Le constructeur a **refusé** de reconstruire : la page en place portait `.mnav`, `.mnav-panel`, `.psrc`
— un menu mobile `<details>` (23/10) et un lien « source préférée Google » (20/10) **jamais reportés dans
`demos/dmoptic-v1.tpl.html`**. Reconstruire les aurait effacés.

**Fait** : les trois blocs (CSS, HTML, JS) sont portés dans le gabarit, puis la page est reconstruite.
C'est la règle du dépôt qui a parlé : *une page en place n'est pas une source*.

### 2.7 Les tests qui parlaient d'une page qui n'existe plus

`test_dmoptic_page.mjs` comptait **4** liens vers `/montures/` (le menu mobile en ajoute un cinquième) et
scannait les `<details>` **dans les commentaires CSS** (le commentaire du menu en cite un). Deux assertions
tombaient sur du vrai. **Fait** : le balayage ignore commentaires, `<style>` et `<script>`, et se limite à
la section des questions ; le compte des liens dit 5 et nomme les cinq.

---

## 3 · Ce qui reste ouvert, et pourquoi

| # | Constat | Pages | Pourquoi ce n'est pas fait |
|---|---|---|---|
| 1 | « la page ne dit pas ce qui se passe après le clic » | 13 (accueil exclu) : `examen-de-vue`, `le-cabinet`, `montures` + 3 catégories, `404`, et leurs miroirs EN | la phrase est une **promesse au client** (« réponse en X ») : elle se demande, elle ne s'invente pas. §34 : aucune promesse |
| 2 | champs sans état d'erreur repérable | 6 (`montures/{hommes,femmes,enfants}` FR + EN) | ce sont les **filtres de catalogue** ; un état d'erreur sur un filtre n'a de sens qu'avec un moteur de recherche, que le ruling D3 (20/10) refuse |
| 3 | une action principale par section (§19.1) | accueil | la vitrine porte **trois** boutons WhatsApp, un par famille. Défendable (chacun part avec son message), mais c'est un arbitrage : à trancher par King |
| 4 | la photo du premier écran est très lavée | accueil | §25 : une photo doit porter **un** sens. Le voile sert la lisibilité du texte ; l'alléger demande de retoucher la photo, pas le CSS |
| 5 | 4 P3 « éléments hors cadre » | accueil | `.wash`, l'anneau SVG et un cercle décoratif débordent sans provoquer de défilement. Sans conséquence, listé pour mémoire |

---

## 4 · Ce que cet audit dit du livre, et pas seulement de la page

1. **Une règle non mesurée n'est pas une règle.** Les six constats ci-dessus étaient tous dans le livre
   depuis septembre, et aucun portique ne les regardait — parce que la proportion, le nombre de blocs du
   premier écran et le compte de tailles n'étaient vérifiés par rien. `shot.py` les mesure maintenant.
2. **Le gabarit est la seule source.** Trois mois de correctifs appliqués à la page construite ont produit
   une page en place que son propre constructeur refuse d'écraser. Le refus a bien fonctionné ; c'est la
   dérive qu'il faut interdire, pas le refus.
3. **Un test qui compte des occurrences compte aussi les commentaires.** Deux assertions « cassées » ne
   l'étaient pas : c'est le test qui regardait au mauvais endroit.

---

## 5 · Reproduire

```bash
bash tools/video/install.sh                       # une fois par session : Chromium + libs + polices + Pillow/numpy/playwright
python3 demos/build_dmoptic.py --production --url https://dmoptiquesarl.com/ --force-rebuild
python3 demos/build_dmoptic_montures.py           # les 47 sous-pages + le miroir EN
python3 tools/qa/shot.py hosting/previews/dmoptic/index.html --out /tmp/dm
python3 tools/qa/audit_palette.py --image /tmp/dm/desktop.png \
    --palette "#EEF1F5=surface,#FFFFFF=surface,#0B2450=brand,#1A3F86=brand,#0B7A3E=accent,#E0703A=semantic"
python3 tools/qa/audit_reveal.py hosting/previews/dmoptic/*/index.html
node tools/qa/test_dmoptic_page.mjs
```
