# Socle de démonstration — clinique / cabinet

Une page, construite pour être **recopiée cinq fois** avec trois changements. Elle applique
`sales/AMK-DESIGN-SKILLS.md` (addendum du 23/10) et `sales/LISTE-OPTICIENS-2026-10.md` §6-§7.

## Ce qu'elle démontre

| Règle de l'addendum | Où c'est appliqué |
|---|---|
| Héros en 5 couches, chaque couche nommée | commentaire `<!-- ⓠ couche 0..4 -->` + classes `.hero-arc` `.obj` `.hero-copy` `.bar` `.appui` |
| L'objet ne bouge pas d'un écran à l'autre | `.obj{position:sticky}` colonne de droite — mesuré à `top:88px` sur deux positions de défilement |
| Un fil relie les étapes | `.thread` 4 px, `scaleY(var(--p))`, `transform-origin:top`, avançant de 0 à 1 |
| Une ligne de donnée par étape | `.data` en mono : `8h30 — 17h00`, `4 étapes`, `3 familles`, `devis écrit`, `6 jours sur 7` |
| Fondu croisé | `IntersectionObserver` → `.step.in`, pas de sortie |
| Finir sur des cartes qui reprennent l'objet | `.cards` (détartrage, conservateur, prothèse) |
| **Refus du 3D/WebGL** | aucun `<canvas>`, aucun `<script src>`, aucune librairie. Profondeur = `blur(22px)` + `drop-shadow` + `scale(1.04)`. **0 Ko de réseau pour l'effet** |
| « un effet qui coûte > 100 ms de LCP ne passe pas » | LCP = le titre. Les deux seules polices critiques sont préchargées par le CSS, `font-display:swap` |
| Mobile d'abord | sous 860 px : l'objet ouvre le récit (124 px), le fil disparaît, les étapes portent la continuité |

## Ce que ça coûte à recopier pour un prospect

Trois changements, pas un de plus :

1. **l'objet** — remplacer le `<svg>` de `.obj` (dent → œil → monture → sourire). Même `viewBox`,
   même place, même ombre. C'est la signature : elle ne change pas de place, elle change de sujet.
2. **la couleur de marque** — `--brand` (vert `#0B5D4E` ici). L'accent `--accent` reste le même partout,
   c'est lui qui fait la maison.
3. **le texte** — les cinq étapes et les trois cartes. Le reste (barre, contact, pied) est identique.

## Ce qui n'est **pas** dedans, volontairement

- **aucun prix**, aucune marque de matériel, aucun avis client recopié ;
- **aucune photo empruntée** : les blocs `.photo` / `.ph` disent « votre photo ici ». Une image de
  banque dans une démo de cabinet dentaire est un mensonge qui se voit à la première question ;
- **aucun faux numéro actif** : le `+237 6 00 00 00 00` est un emplacement, jamais un vrai numéro
  au hasard (on ferait sonner quelqu'un d'autre).

## Vérification avant de montrer le lien

```bash
python3 tools/qa/shot.py hosting/previews/demo-clinique/index.html --out /tmp/shot-demo
# → VERT · 0 P1 · 0 P2 · 0 P3 (23/10, 1440 px et 390 px, contraste AA compris)
```

Le portique mesure le contraste, le débordement, le texte coupé, les images cassées, le focus
clavier et la présence du héro dans le premier écran. **Il passe avant l'envoi du lien, pas après.**
