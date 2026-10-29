# L'avis Google : ce qui est sur le site, et la carte du comptoir

```text
ÉTAPE 0    carte lue le 29/10 (14 311 nœuds), §0 → §3 bis · ask « avis google reviews site opticien »
DOCUMENTS  AMK-DESIGN-SKILLS.md lu en entier (§1 à §40) avant d'écrire une ligne, comme demandé ·
           §3.3 (lois 03 et 06), §8 (boutons), §9 (motion), §13 (pré-vol), §27 (a11y AA), §40 (perception)
LEÇON      les guidelines review snippet du 24/07/2026 déclarent inéligibles aux étoiles les pages
           LocalBusiness ou Organization qui affichent des avis contrôlés par l'entité elle-même,
           widgets d'avis Google ou Facebook compris. On n'affiche donc aucun avis. On demande.
```

## 1 · Ce qui a été posé sur le site

Une seule ligne, en bas de `/contact/` et de `/en/contact/` : **« Vous êtes venu au cabinet ? Votre
avis sur Google aide les patients qui cherchent un opticien à Bonabéri. »**, suivie d'un lien
**« Laisser un avis sur Google »** vers
`https://search.google.com/local/writereview?placeid=ChIJjdfYfQwXYRARAdi9mPLHGjY`.

Le `place_id` est celui que le cabinet a relevé lui-même le 21/10 : le lien ouvre **sa** fiche, pas une
liste de résultats où il faudrait la retrouver.

### Pourquoi ce n'est pas un encart

La loi 03 de §40 (banner blindness) est explicite : l'œil saute ce qui a la forme d'une publicité. Une
pastille bordée avec une icône d'étoile est exactement cette forme. Le bloc est donc **du texte**, un
filet de 1 px au-dessus, un lien **souligné** : c'est la correction déjà appliquée le 28/10 à la source
d'une fiche monture (§40.2, loi 03).

### Ce qu'il ne dit pas, et c'est le point

Aucune étoile. Aucune incitation. Aucune condition de satisfaction. La phrase demande **un avis**, pas
**une bonne note**. Un « laissez-nous 5 étoiles et vous aurez une remise » serait une violation des
règles Google **et** de la règle maison du 21/10.

## 2 · La carte du comptoir, prête à imprimer

| Fichier | Ce que c'est | Usage |
|---|---|---|
| `carte-avis-a6.pdf` | la carte complète, **A6, 300 dpi** | c'est ce fichier qu'on envoie à l'impression |
| `carte-avis-a6.png` | la même, 1240 × 1748 | aperçu, envoi WhatsApp |
| `qr-avis-google.svg` | le QR seul, **vectoriel** | imprimeur, autre support, écran |
| `qr-avis-google.png` | le QR seul, 1200 px | post, écran du comptoir |

**Trois choix qui ne sont pas décoratifs.**

1. **Correction d'erreur H (30 %).** Le QR doit survivre à une impression bon marché, à un comptoir
   humide et à un téléphone qui vise mal. Un QR « propre » à 7 % ne survit à rien de tout ça.
2. **Une adresse de repli en clair** : « ou cherchez DM OPTIQUE SARL sur Google ». Un QR est une
   commodité, jamais une condition. Le jour où le lien casse, la carte reste utile.
3. **Aucun texte qui promette une note, un avantage ou un délai.** Le pied de carte porte l'adresse et
   le téléphone : ce qu'on imprime reste un objet du cabinet, pas un coupon.

### Vérifié, pas supposé

```bash
python3 tools/ops/make_qr_avis.py --check
# QR version 8 · 49 modules · correction H (30 %)
#   qr-avis-google.png : IDENTIQUE
#   carte-avis-a6.png  : IDENTIQUE   ← la carte s'est relue, pas seulement le PNG du QR
```

`opencv-python-headless` relit le QR **imprimé dans la carte**, pas seulement l'image du QR. C'est la
carte qu'on imprime : c'est donc elle qui doit se relire.

### Le jour où le `place_id` change

```bash
python3 tools/ops/make_qr_avis.py          # régénère les 4 fichiers à partir de la constante PLACE_ID
```

Le script existe pour cette raison : un QR contient une URL, une URL se périme, et une image posée à
la main en 2026 ne dit plus à personne ce qu'elle pointe.

## 3 · Le piège trouvé en écrivant la carte, et corrigé

`str.split()` coupe sur **tout** espace, y compris l'espace insécable. La première épreuve affichait
donc :

```text
Scannez avec l'appareil photo, ou cherchez « DM OPTIQUE SARL
» sur Google.
```

Le guillemet fermant partait seul à la ligne, et le nom de marque se coupait en deux. Corrigé dans
`wrap()` du script (les insécables sont respectées) **et** dans le texte lui-même : le nom complet est
collé. Une épreuve se regarde, elle ne se suppose pas.

## 4 · Les portes, après le changement

| Porte | Résultat |
|---|---|
| `audit_seo_local.py --strict` | 0 faute · 0 avertissement |
| `audit_delivery.py --strict` | 0 P1 · 0 P2 · 1 P3 connu |
| `audit_laws.py` (six lois) | 0 faute · 0 avertissement |
| `audit_aeo.py` | aucune faute sur 103 pages |
| `audit_a11y.py --strict` sur `/contact/` FR et EN | 0 faute A/AA |
| `test_dmoptic_page.mjs` | 71 verts, 0 échec |
| `shot.py` sur `/contact/`, `/en/contact/` et l'accueil | **VERT** 0 P1 · 0 P2 · 0 P3 |

**Un faux positif corrigé au passage.** `shot.py` a d'abord signalé un P2 « texte coupé » sur
`<span>(nouvel onglet) (new tab)</span>` : la précision destinée aux lecteurs d'écran (`.v2-sr`,
1 px par 1 px, `clip`) était comptée comme un débordement. Un texte masqué aux yeux mais pas aux
lecteurs d'écran n'est pas un texte coupé. `shot.mjs` l'ignore désormais, et la capture est repassée
au vert **sans toucher au site** : c'est l'outil qui était faux.

## 5 · Ce qui reste, et à qui

| # | Geste | Qui |
|---|---|---|
| 1 | Soumettre `https://dmoptiquesarl.com/sitemap.xml` dans la propriété **Domaine** | King |
| 2 | Imprimer `carte-avis-a6.pdf` en A6, poser la carte au comptoir, à hauteur d'œil | King |
| 3 | Demander l'avis **après** le service, jamais avant, jamais en échange de quoi que ce soit. Le texte est déjà écrit et approuvé : `launch/MESSAGE-AVIS-GOOGLE-2026-10.md` | le cabinet |
| 4 | Répondre à chaque avis, factuellement, sans claim | le cabinet |
| 5 | Vérifier au 16/11 que des avis **récents** arrivent (la vélocité sur 90 jours pèse plus que le total) | nous |

**Ce qu'on ne promet pas** : qu'un avis arrive, ni qu'il fasse monter la fiche. On a rendu le geste
possible ; le reste appartient aux patients.
