
> **05/10 :** dans un tableau de prix, « — » = inclus sans surcoût, jamais « incluse » répété.

## Addendum Lot [44] — checklist de spec design en 6 tokens (12/10)

Source : `research/youtube-lessons/2026-10-12-batch-final/video-31-vibe-coding-design.md`
(Meng To / The Next Wave). Règle : **plus jamais d'adjectif (« beautiful », « moderne ») dans une
spec de page générée** — « beautiful » produit le générique entraîné (dégradé violet, bold par
défaut). Toute spec nomme ses 6 tokens :

1. **Layout** : hero / cards / liste / bento / browser-frame — nommé, pas décrit vaguement.
2. **Styling** : flat / outline / minimalist / glass / iOS / material — un seul choix.
3. **Couleurs** : accent = couleur de marque (AMK : vert) ; **fond = accent désaturé** (règle de
   construction, pas un hasard).
4. **Ombres** : none / small / large / « beautiful shadow » (sans border, inner shadow) — nommé.
5. **Typo** : famille + **graisse du heading = personnalité** + tracking resserré sur les grands
   titres.
6. **Pairing** : serif en titre + sans en corps (lisibilité du corps non négociable).

Complément : **un ingrédient signature par page** suffit à sortir du générique (pas d'effet
partout). Standard single-file confirmé en externe (chap. 05:32 de la vidéo). Spline (3D gratuit)
= backlog si besoin futur.

## Addendum 23/10 — le héros en couches, et le match cut entre sections

Source : trois captures TikTok montrées par King (comptes `weblove` et un carrousel de gabarits
d'anatomie de page). Ce qu'on en garde, ce qu'on refuse.

### 1 · Le gabarit du héros, en couches

Les schémas montrés décomposent tous la même chose, et c'est exactement ce qui manque à nos pages
quand elles « sonnent génériques » : **un héros n'est pas un bloc, c'est un empilement dont on doit
pouvoir nommer chaque couche.**

| Couche | Ce qu'elle porte | Le test |
|---|---|---|
| **0 — fond** | une forme large (arc, vague, aplat découpé), jamais un dégradé par défaut | si on la supprime, la page doit tenir debout |
| **1 — objet** | **un seul** objet héro, détouré, posé sur l'axe | s'il y en a deux, il n'y en a aucun |
| **2 — texte** | titre + sous-titre + CTA, groupés à **une** position | le titre doit se lire même sans l'objet |
| **3 — barre** | logo · navigation · CTA — alignés sur la même grille que le texte | c'est la couche qui casse en premier sur mobile |
| **4 — appui** | chiffre, mention, preuve discrète (ONOC, horaires, note) | elle doit pouvoir disparaître sans perte |

**La règle de composition :** l'objet héro reste **au même endroit** d'une section à l'autre
(`left: 50%`, `translateX(-50%)`) pendant que le texte et le fond changent. C'est ça qui donne
l'impression que la page est un seul film — pas un empilement de cartes.

### 2 · Le match cut : chaque section finit sur ce que la suivante commence

Deuxième capture (`weblove`, site de café) : *« this site feels like one shot, not 5 sections »*. Sept
gestes, tous réutilisables pour un cabinet d'optique — et tous gratuits en performance :

1. **Raconter la page comme une histoire** : *entrer → mesurer → choisir → régler → sortir*.
2. **L'objet héro fixe** (`left: 50%`, `translateX(-50%)`) : l'œil ne saute jamais.
3. **Un fil qui relie** : une ligne de 4 px au centre, `scaleY(progress)`, `transform-origin: top`.
4. **Même angle et même lumière** sur toutes les photos — pour nos photos réelles, ça veut dire **une
   seule séance, une seule fenêtre, un seul réglage**.
5. **Fondu croisé sur les 20 derniers pour cent** de chaque section : l'élément suivant est déjà là
   quand le précédent part.
6. **Une ligne de donnée par étape** — chez nous : `8h30–13h00`, `21/2016`, `656 122 239`. Un chiffre
   par section fait lire comme un métier, pas comme une décoration.
7. **Finir sur des cartes produit** qui réutilisent l'objet du récit — chez nous : la monture qui revient
   en dernier plan après l'examen.

### 3 · Ce qu'on refuse : le « 3D website » et le WebGL

La première capture vend un site en 3D (objet qui flotte, profondeur réelle). **On ne le fait pas** :
un mobile à Douala sur 3G n'a pas la puissance pour un rendu WebGL, et un héros qui met quatre secondes
à apparaître coûte plus que l'effet ne rapporte (`audit_delivery.py` le refuserait : LCP).

**Ce qu'on fait à la place, pour la même sensation :** la profondeur se fabrique en **CSS seul** —
c'est ce que les schémas en couches montrent déjà.
- objet à `scale(1.04)` avec ombre portée douce et un léger `translateZ` simulé par le flou du fond ;
- fond à `blur(24px)` + `scale(1.1)` (une seule couche, un seul filtre) ;
- parallaxe de 12 px maximum au défilement, désactivée sous `prefers-reduced-motion` ;
- aucun `<canvas>`, aucun `<script>` 3D, aucun appel réseau supplémentaire. **Coût : 0 Ko.**

**La loi qui tranche :** un effet qui coûte plus de 100 ms de LCP ne va pas dans un site client — même
gratuit, même beau. La profondeur est une affaire de superposition et de lumière, pas de moteur 3D.
