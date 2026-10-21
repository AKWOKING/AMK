# Création de contenu — ce que le dépôt sait faire, au 22/10/2026

```
Statut   base de connaissance + mode d'emploi de l'outillage installé le 22/10
Sources  research/youtube-lessons/2026-10-22-eyecare-marketing/SYNTHESE.md
         research/youtube-lessons/2026-10-22-brand-strategy/SYNTHESE.md
         retour d'expérience du montage de la V2 (clients/dm-optic/content/month1/w1/)
Usage    toute production vidéo/sociale commence ici (PRE-FLIGHT §1g)
```

---

## 1 · La chaîne de production, telle qu'elle existe maintenant

```
photos réelles (dépôt)  →  moteur de rendu PIL  →  ffmpeg (imageio-ffmpeg)  →  portique mouvement  →  livraison
                                  ↑                        ↑
                            polices du site        voix (generate_speech)
```

| Maillon | Outil | État |
|---|---|---|
| Rendu des cartons et composition | **Pillow** | installé (13.0.0) |
| Encodage vidéo | **imageio-ffmpeg** (ffmpeg 7.0.2 statique) | installé — `apt` n'a pas accès aux dépôts |
| Polices | Schibsted Grotesk 500/700 + IBM Plex Sans, converties `woff2` → `ttf` par **fontTools + brotli** | dans `clients/dm-optic/content/month1/w1/assets/fonts/` |
| Moteur DM Optique | `tools/record/make_dmoptic_tiktok.py` | écrit le 22/10 |
| Portique qualité | `tools/qa/audit_video_motion.py` | **bloquant** |

**Commande d'installation** (à refaire si le sandbox est neuf) :
```bash
pip install --user --break-system-packages pillow imageio-ffmpeg numpy fonttools brotli
```

---

## 2 · Les règles de fabrication (payées par l'expérience)

1. **Chaque plan doit bouger.** Le portique bloque toute fenêtre de 2 s figée. Un carton « stable 3 s »
   échoue : il faut un zoom lent ou une apparition de texte.
2. **Zoom très lent = 2 à 6 %** sur la durée du plan. Au-delà, ça tremble et ça fait diaporama.
3. **Jamais d'agrandissement au-delà de 1,4×.** Une photo de 1400 px dans du 1920 devient molle.
4. **Produit sur fond uni** : on **échantillonne** la couleur des bords et on l'étend au 9:16. Ce n'est pas
   retoucher la photo, c'est changer le cadre — la monture reste intacte.
5. **Sous-titres incrustés**, jamais les automatiques de la plateforme : ce que le spectateur voit doit
   être exactement ce qu'on a écrit.
6. **Cartons : 0,3 s par mot**, minimum 0,8 s, deux lignes maximum à l'écran (réduire la police, pas le
   texte).
7. **Audio dans le fichier.** Un son ajouté dans l'application ne compte pas : le fichier livré porte la
   voix.
8. **Aucune musique commerciale.** Silence + voix, ou piste libre de droits documentée.
9. **Export** : 1080×1920, 30 fps, H.264, CRF ~20, `+faststart`, audio 128 kb/s. Sous 25 Mo.

---

## 3 · La structure d'un script court (5 temps)

Celle qui traverse toutes les sources et qu'on applique :

| # | Temps | Rôle | Interdit |
|---|---|---|---|
| 1 | **Le cas** | une situation vécue, à la 2ᵉ personne, dans les 3 premières secondes | se présenter, vanter le cabinet |
| 2 | **Le miroir** | ce que ça coûte, sans diagnostic | nommer un symptôme, promettre une guérison |
| 3 | **Le réel** | un objet du cabinet, un seul axe | empiler les arguments |
| 4 | **La preuve** | un fait vérifiable, une fois | « meilleur », « n°1 », « unique » |
| 5 | **La sortie** | un seul CTA + l'honnêteté (« si vous voyez bien, ne venez pas ») | deux CTA, urgence artificielle |

**Longueur** : 21–34 s. **Densité** : 2,5 à 3 mots par seconde lus à voix haute.

---

## 4 · Les quatre piliers de contenu (modèle DM Optique, transposable)

| Pilier | Ce que c'est | Preuve mobilisée |
|---|---|---|
| **Le geste utile** | une chose faisable dans les 30 secondes (20/20/20, entretien des verres) | aucune promesse — l'utilité |
| **La monture réelle** | une monture du stock, photographiée au cabinet, nommée | « montrer avant » |
| **La coulisse** | ce qui se passe entre la porte et la sortie | « mesurer, pas deviner » |
| **La sortie honnête** | ce qu'on refuse de faire, à qui on dit non | « dire quand on n'a pas besoin » |

**Rythme** : 2 posts/semaine — un pilier 1 ou 4, un pilier 2 ou 3. C'est ce qui supprime la question
« que poster aujourd'hui ? ».

---

## 5 · Ce qui produit un résultat (et ce qui ne le produit pas)

| On mesure | On ne mesure pas |
|---|---|
| conversations WhatsApp avec le message pré-rempli propre à la vidéo | vues |
| avis Google gagnés | likes |
| itinéraires et appels depuis la fiche | abonnés |
| enregistrements et partages (pilier 1) | impressions |

**Le message pré-rempli est la seule attribution fiable** : chaque vidéo a son propre texte
(`wa.me/237…?text=…`), sinon une conversation ne dit pas d'où elle vient. Pas de cookies, pas d'UTM côté
WhatsApp.

---

## 6 · Visages, UGC et modèles IA — la position du dépôt

**Rappel des faits** : le client (King) et le docteur ont évoqué la possibilité de **modèles UGC
réalistes / influenceurs IA** si le mois 1 ne donne pas de résultats ; les visages **du personnel** sont
autorisés sur les photos.

### Ce qui est autorisé

- Les **photos réelles** du cabinet et des montures, y compris avec le personnel identifiable (accord du
  client, 22/10).
- Un **avatar IA présentateur** — quelqu'un qui *explique* ce qu'on lui fait dire — **à condition** d'être
  signalé comme généré par IA (voir ci-dessous).
- Les **témoignages réels**, avec autorisation écrite, sans détail de santé.

### Ce qui n'est pas autorisé, et ne le sera pas

| Interdit | Pourquoi |
|---|---|
| Un **faux patient** généré par IA qui dit « j'ai été soigné chez eux » | c'est un **faux témoignage** : tromperie, et dans beaucoup de pays une pratique commerciale illicite. Le gain à court terme coûte la crédibilité entière du cabinet |
| Un **professionnel de santé IA** présenté comme le praticien | même raison, aggravée : c'est un titre réglementé (ONOC) |
| Une **photo de produit** générée ou retouchée | règle de maison : les photos réelles sont la matière première |
| Un contenu IA **non signalé** | les plateformes exigent le signalement des médias synthétiques ; un compte qui se fait prendre perd sa portée |

### Les conditions pratiques, si on va vers l'avatar IA

1. **Étiqueter** : mention « contenu généré par IA » dans la légende, et l'étiquette native de la
   plateforme quand elle existe.
2. **Rôle limité** : présentateur / explicatif. Jamais un patient, jamais un soignant, jamais un
   témoignage.
3. **Aucune promesse médicale** dans la bouche de l'avatar — c'est nous qui parlons.
4. **Cohérence de marque** : même voix, même axe (« on montre avant de vendre »), même typographie.
5. **Le réel reste majoritaire** : au moins un contenu sur deux doit contenir une image réelle du
   cabinet ou d'une monture — sinon le compte devient une chaîne d'avatars et perd ce qui le distingue.
6. **Décision de King avant production**, et mention au dossier client.

### La voie préférée, dans l'ordre

1. **Photos réelles + cartons + voix** (ce qu'on fait ce soir) — zéro risque.
2. **King ou un membre du personnel à l'écran**, une session par mois — la recherche place les visages au
   premier rang ; c'est le meilleur rapport effort/effet.
3. **Avatar IA présentateur** — seulement si 1 et 2 ne suffisent pas, avec les six conditions ci-dessus.

---

## 7 · La règle de source (posée le 22/10)

> **Une statistique sans source primaire nommée n'entre pas dans une décision client.**

Les pages d'agences qui recyclent des chiffres sans les nommer produisent des stratégies sur du sable. Ce
qui est accepté : l'institution nommée (BrightLocal, Litmus, Stanford, Sprout Social, Omnisend), même si
le chiffre n'a pas été revérifié à la source — auquel cas il est **signalé comme non revérifié**.

---

## 8 · Les portes à franchir avant qu'une vidéo sorte

- [ ] Accroche ≤ 3 s, aucune auto-présentation
- [ ] Un seul axe de marque, une seule preuve
- [ ] Aucune promesse médicale, aucun symptôme nommé
- [ ] Aucun tiers nommé (concurrent, marque de monture ou de verre)
- [ ] Un seul CTA
- [ ] Sous-titres manuels relus
- [ ] **Audio dans le fichier**
- [ ] **Portique mouvement : 0 fenêtre figée**
- [ ] Relu par le client — rien n'est publié sans lui
