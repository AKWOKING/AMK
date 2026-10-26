# TIKTOK + INSTAGRAM — les deux légendes d'EP01 v6, et la réponse sur le montage

```text
Statut     prêt à coller. Facebook part à 12 h (§PUBLICATION-2026-10-26) ; ce fichier couvre TikTok et Instagram.
Question   King, 26/10 : « hashtags (if needed) and caption for tiktok and for instagram separately adapted
           to the respective social medias — or do you think we should tweak the videos for specific platforms »
Réponse    Légendes : oui, deux, et elles ne se ressemblent pas (ci-dessous). Montage : pas aujourd'hui,
           une coupe TikTok de 16 s pour la pièce suivante. Trois raisons mesurées au §1, aucune au goût.
Porte      python3 tools/qa/audit_platform.py content/reels/ep01/PUBLICATION-TIKTOK-INSTAGRAM-2026-10-26.md \
                                             content/reels/ep01/ep01-v6.mp4   → doit finir « OK »
```

> **Ce que ce document ne promet pas** : aucune portée, aucun taux, aucun « hashtag magique ». Le dépôt a
> **une** mesure par plateforme, elle est datée, et elle ne dit rien du nombre de hashtags (§4).

---

## 1 · Faut-il retoucher la vidéo pour chaque plateforme ? — la réponse, avec les chiffres

**Non pour aujourd'hui. Oui pour la pièce suivante.** Voici ce qui a été mesuré sur le master, pas ce qui
se dit.

| Ce qu'on vérifie | Mesure sur `ep01-v6.mp4` | Verdict |
|---|---|---|
| Format | **1080 × 1920**, 30 fps, H.264 + AAC | ✅ natif vertical, les deux plateformes |
| Durée | **23,71 s** | ⚠️ la grille maison du 23/10 dit **12–16 s** sur TikTok, **16–22 s** sur Facebook (`CONTENT-CREATION` §5 quater) |
| Texte critique (labels + titres) | à **y = 12 % → 53 %** de la hauteur | ✅ hors de la zone que TikTok et Instagram recouvrent (bas et droite) |
| Bas de l'image | 3 à 9 % libres — c'est la **mascotte** et la **barre de progression** (décor) | ✅ ce qui est recouvert n'est pas du texte |
| Droite de l'image | 19 à 46 % libres selon le beat | ✅ les icônes TikTok/IG tombent sur du vide |
| Filigrane | **aucun** | ✅ un master propre se réemploie ; un export TikTok filigrané, non |
| Sous-titres | le texte à l'écran est du **dessin**, pas le verbatim de la voix | ⚠️ TikTok exige des **sous-titres manuels** (ruling 11/10) : ils se tapent dans l'app (§2.3) |

**Ce qui a été écarté, et pourquoi :** refaire le master en trois formats. Un montage différent par
plateforme était le ruling du 23/10 — il parle d'un **tournage large** remonté deux fois, pas d'une
re-synthèse de la voix. Or ici la voix décide de la durée (`build_timing.py`) : une coupe TikTok à 16 s
oblige à **réécrire et re-synthétiser** les beats, ce qui prend 40 minutes et change le texte que King
vient de valider. À **une heure de la publication**, c'est un mauvais échange.

**Donc :**
- **aujourd'hui** : le même master sur les trois plateformes, trois légendes différentes (c'est là que
  se joue l'adaptation, pas dans le fichier) ;
- **pour EP02** : une coupe **TikTok 16 s** (hook, spike1, release1, CTA) et le master long pour
  Facebook / Instagram. La règle existe déjà ; on l'applique à la pièce suivante, pas à celle-ci.

---

## 2 · TIKTOK — la légende, les sous-titres, les réglages

### 2.1 La légende (français, deux lignes — la grille maison)

```text
Votre patient tape « opticien Akwa ». Il appelle l'autre.
Sa fiche a douze avis, la vôtre n'a qu'un nom. Écrivez APERÇU sur WhatsApp : 677 78 96 31.

#Douala #Cameroun #opticien #opticienDouala #lunettesDouala #AMKweb
```

**Pourquoi celle-là et pas la légende Facebook** : sur TikTok, le premier mot-clé doit tomber dans les
**premiers caractères** parce que la recherche lit la légende (`TIKTOK-SEO-CHECKLIST` §C). « opticien
Akwa » est déjà dans la première ligne — c'est le mot que le patient tape. Sur Facebook, la légende se
lit (6–10 lignes) ; ici, deux lignes et un mot-clé.

### 2.2 Halte aux hashtags : combien, lesquels, et ce qu'ils ne font pas

**La règle maison** (`TIKTOK-SEO-CHECKLIST` §C) : **3 à 8**, dont 2–3 larges ou locaux + 2–3 de niche +
1 de marque. **Six**, ci-dessus :

| Rôle | Hashtag | Pourquoi |
|---|---|---|
| large | `#Cameroun` | le pays ; c'est là que vit la recherche locale |
| local | `#Douala` | la ville de l'opticien — la seule géographie qui compte |
| niche | `#opticien` | le métier, en français (la cible lit français) |
| niche | `#opticienDouala` | métier + ville : le croisement, celui qu'on veut gagner |
| niche | `#lunettesDouala` | le mot que le **patient** tape, pas celui du gérant |
| marque | `#AMKweb` | un seul, toujours le même, pour que la série se retrouve |

**Ce qu'ils ne font pas** : ils ne créent pas de portée. Notre seule mesure TikTok dit que le levier est le
**pourcentage de lecture** (26 % sur la vidéo de DM Optique), pas le nombre d'étiquettes. Six hashtags
suffisent à dire à TikTok de quoi parle la vidéo ; au-delà, on dilue la légende sans rien gagner.

**Ce qu'on n'écrit jamais** : `#fyp`, `#pourtoi`, `#viral`, `#follow` — ils ne classent rien, ils signalent
un compte qui cherche des vues. Et un hashtag de ville **inventé** (une ville où le client n'est pas) est
une promesse fausse.

### 2.3 Les sous-titres — manuels, jamais automatiques (ruling 11/10)

L'automatique ne tient pas sur un accent camerounais en français. On tape donc ces six lignes dans
l'éditeur TikTok, **mot pour mot**, et King les relit avant publication :

```text
0,0 – 5,0 s    Votre patient tape opticien Akwa. Il appelle l'autre, pas vous.
5,0 – 8,8 s    Sa fiche a douze avis. La vôtre n'a qu'un nom.
8,8 – 12,2 s   Les horaires, ça se change en dix minutes. Sans moi.
12,2 – 16,3 s  Le soir, il veut venir. Et personne ne répond.
16,3 – 19,5 s  Une page avec vos horaires répond à votre place.
19,5 – 23,7 s  Écrivez APERÇU. Voyez votre page avant de payer.
```

**Où les placer** : au **tiers supérieur** de l'écran, pas en bas — le bas est recouvert par l'interface.

### 2.4 Les réglages de publication

| Réglage | Valeur | Pourquoi |
|---|---|---|
| Son | **la voix du master, aucun son tendance ajouté** | mesure du 17/09 : narration **6,2 s** de lecture moyenne contre **3,8 s** avec un son tendance — le son couvre la voix, il ne l'aide pas |
| Qui peut regarder | **Tout le monde** | un opticien qui ne nous connaît pas doit pouvoir tomber dessus |
| Commentaires | **autorisés** | c'est là que la conversation commence ; on répond dans l'heure |
| Duet / Stitch | **autorisés** | un stitch est une recommandation gratuite |
| Téléchargement | **autorisé** | un opticien qui renvoie la vidéo à son associé, c'est un partage |
| Couverture | frame de **spike1** (les deux fiches, 6,0 s) | TikTok n'a pas de vignette personnalisée : on choisit la frame, pas une image |
| Nom du fichier | `ep01-opticien-douala-apercu.mp4` | la checklist demande un nom descriptif avant l'upload |

### 2.5 Le commentaire épinglé (à poster dans les 5 minutes)

```text
677 78 96 31 — écrivez APERÇU. Je regarde votre fiche, et vous voyez votre page avant de payer.
```

---

## 3 · INSTAGRAM — la légende en anglais, le reste en français

### 3.1 Pourquoi l'anglais ici et pas ailleurs

`brand/AMK-PRESENCE-2026-10-22.md` §2, correction n° 5 : **« FR à l'écran, EN en légende »**. Instagram est
le seul de nos trois comptes dont l'audience historique est anglophone (bio « english only », relevé du
08/10, **6 abonnés**, 122 vues sur 30 jours). On applique la règle : la vidéo reste en français (c'est la
langue de l'opticien d'Akwa), la légende parle anglais — et elle porte **le mot à écrire**, qui ne se
traduit pas.

### 3.2 La légende (anglais, cinq lignes)

```text
Your patient Googles « opticien Akwa ». He calls the other guy.
Their listing has twelve reviews. Yours has a name.

Hours. Address. WhatsApp. A page in your name answers at 10pm, when the cabinet is closed.

Write APERÇU on WhatsApp: +237 677 78 96 31. You see your page before you pay.

#Douala #Cameroon #Optician #Optometry #Eyewear #SmallBusinessCameroon #AMKweb
```

**Ce que la version anglaise ne fait pas** : elle ne traduit pas mot pour mot. « douze avis » devient
« twelve reviews » ; « répond à votre place » devient « answers at 10pm », parce qu'un anglophone de
Douala ou de la diaspora n'entend pas « à votre place » comme un opticien francophone.

**Alt text** (obligatoire chez nous — `AMK-DESIGN-SKILLS` §27, accessibilité) :

```text
Reel de 24 s, fond crème. Texte : « Votre patient tape opticien Akwa. Il appelle l'autre, pas vous. » puis
« Sa fiche a douze avis. La vôtre n'a qu'un nom. » Un personnage illustré désigne les deux fiches.
```

### 3.3 Les réglages

| Réglage | Valeur | Pourquoi |
|---|---|---|
| Format | **Reel** (pas un post vidéo) | seul format poussé hors abonnés |
| Partager dans le fil | **oui** | double la surface sans second envoi |
| Partager sur Facebook | **non** | le reel part déjà sur la page à 12 h ; deux envois = deux mesures brouillées |
| Lieu | **Douala, Cameroun** | la seule géographie de la cible |
| Hashtags | **7** dans la légende (§3.2) | Instagram les lit comme des sujets de classement ; au-delà de 10, ils ne font rien de plus |
| Lien | **aucun** dans la légende (il n'est pas cliquable) — le numéro est écrit, et le lien est dans la bio | ne jamais écrire « lien en bio » sans que la bio ait le bon lien |
| Son | la voix du master | idem TikTok |

### 3.4 Le premier commentaire (à poster tout de suite)

```text
Si vous préférez le français : écrivez APERÇU sur WhatsApp — 677 78 96 31. Vous voyez votre page avant de payer.
```

---

## 4 · Ce que ces légendes ne prétendent pas

- **Aucun taux, aucune portée.** La seule mesure Instagram est datée du 08/10 : 6 abonnés, 122 vues en
  30 jours, un post à 45 vues (le meilleur) et un à 6. La seule mesure TikTok : 156 et 121 vues, 26 % de
  lecture moyenne. Aucune ne dit ce que fera ce reel.
- **Aucun hashtag « qui marche ».** On applique la règle de la checklist (3–8, local + niche + marque)
  parce qu'elle est écrite, pas parce qu'elle est prouvée.
- **Aucun contenu vanité.** Si ce reel ne produit aucun message sur aucune des trois plateformes, le
  §6.3 du `PLAYBOOK` s'applique : on ne refait pas une saison sans chiffre.

---

## 5 · Le compteur, plateforme par plateforme (à remplir le soir et à J+1)

**Le seul chiffre qui décide est la dernière colonne, toutes plateformes confondues.**

| Plateforme | Vues | Lecture moyenne | % complètes | Partages | Enregistrements | Commentaires | Messages reçus | dont **APERÇU** |
|---|---|---|---|---|---|---|---|---|
| Facebook (12 h) | | | | | — | | | |
| TikTok | | | | | | | | |
| Instagram | | | | | | | | |
| **Total** | | | | | | | | |

**Ce qui ne se compare pas** : une vue TikTok et une vue Facebook ne veulent pas dire la même chose (TikTok
note le film, Facebook le distribue — `CONTENT-CREATION` §5 quater). On ne fait jamais la moyenne des trois.

---

## 6 · Ce qui reste à King

1. **TikTok** : légende §2.1 · sous-titres §2.3 tapés à la main · six réglages §2.4 · commentaire épinglé §2.5.
2. **Instagram** : légende §3.2 · alt text · lieu · premier commentaire §3.4.
3. **La décision de la coupe 16 s** pour EP02 : elle se prend **avant** d'écrire le script suivant, pas
   après le rendu — sinon on refait le même arbitrage dans l'urgence.
