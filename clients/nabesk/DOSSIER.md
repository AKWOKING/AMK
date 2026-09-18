# NABESK Comprehensive College — Bonduma, Buea

**MQL 6/6 · FROID — jamais approché · aucun numéro WhatsApp connu**
Statut corrigé le 18/09 : **aucune carte scellée n'a été déposée**. Ce prospect n'a jamais été contacté. Il n'y a pas de canal : sans numéro trouvé, il n'est pas joignable aujourd'hui.

---

## 1 · Faits vérifiés

| Fait | Source |
|---|---|
| **Deux numéros de centre GCE** : **11853** (niveau A) et **22197** (technique & commercial) | `camgceb.org` — PDF de résultats officiels 2022/2023/2024 ; `concourscameroon.com` |
| **Centre d'accueil GCE**, quartier **Bonduma-Buea** | PDF « Practical Accommodation Centres » 2021 ; jointure NABESK-Junction |
| A-Level 2020 : **128 inscrits, 106 reçus → 83,46 %** | `concourscameroon.com`, résultats GCE A-Level 2020 |
| TVEE A-Level 2024 : **30 inscrits, 19 reçus → 63,33 %** | `camgceb.org` — 2024 TVEE Advanced Level Results |
| TVEE A-Level 2023 : 26 inscrits, 16 reçus → 61,54 % | `camgceb.org` — 2023 TVEE Advanced Level Results |
| A-Level 2017 : 134 inscrits, 29 reçus → 21,64 % *(année faible, publique)* | résultats GCE 2017 |
| **Aucun site web.** Les résultats ne vivent que dans des PDF de 300 pages | `sales/Walk-In-Deep-Dives-2026-09-15.md` |

> **Correction d'exactitude.** Le fichier interne disait « 83,5 % au O-Level ». Vérification faite : c'est **83,46 % au A-Level 2020**. Le chiffre est juste, son étiquette ne l'était pas. Corrigé ici et dans le CRM.

## 2 · Douleur

1. **Ils publient des résultats et personne ne les voit.** Les PDF du GCE Board sont des documents de plusieurs centaines de pages, sans nom d'école lisible, où NABESK est une ligne parmi des centaines.
2. **Un parent ne peut pas répondre à la seule question qui compte** — « est-ce que mon enfant y réussit ? » — sans télécharger un PDF de 300 pages et compter lui-même.
3. **Aucun site, aucune page d'admission, aucune grille de frais.**
4. Leur série technique et commerciale est un vrai différenciateur local (peu d'écoles ont deux centres) et **elle est invisible**.

**L'accroche est là, prête :** « vos résultats sont publics — mais habillés en tableur ».

## 3 · Direction artistique

**Style : `geometric` + `professional`** · **Palette : Monochrome + une seule couleur saturée** (§6.2 rotation)
**Dial : VARIANCE 6 · MOTION 3 · DENSITY 5** — densité au-dessus du preset écoles : cette école vend des **chiffres**. Le mouvement est réduit au minimum : on lit, on ne contemple pas.

| Rôle | Valeur |
|---|---|
| Marque | `#0E7490` cyan profond (l'unique couleur saturée) |
| Secondaire dérivé | `#57A0B5` (éclairci à 30 %) |
| Fond | `#F7F6F3` — neutre froid, **jamais** blanc pur |
| Encre | `#16191D` — **jamais** noir pur |
| Règle | Le cyan *uniquement* sur chiffres, filets et CTA — le reste en monochrome |

**Pourquoi ce choix :** le monochrome lit « document, rigueur, chiffre » ; la couleur unique désigne exactement ce qu'on veut faire regarder. C'est l'inverse du cobalt institutionnel de Summerset : ici, on ne vend pas de la tradition, on vend de la **transparence chiffrée**.

## 4 · Maquette — ⚠️ À REFAIRE EN ANGLAIS

**Défaut signalé par King le 18/09 : cette maquette a été produite en français alors que Buea est anglophone.** Elle ne doit pas être envoyée telle quelle. La commande ci-dessous est conservée telle quelle ; la corriger = passer les jetons en anglais (`--h1 --sub --svc`, et le libellé `--line`).

```bash
python3 tools/outreach/mockup.py --vertical college \
  --name "NABESK Comprehensive College" \
  --specialty "Collège polyvalent · Bonduma, Buea" \
  --color "#0E7490" \
  --h1 "Des résultats|publiés noir sur blanc" \
  --sub "Général, technique et commercial, à Bonduma. Centre d'examen GCE 11853 et 22197." \
  --svc "Général,Technique,Commercial" \
  --out clients/nabesk/maquette-nabesk.jpg
```

*Aucun chiffre de réussite n'entre dans la maquette : afficher 83,46 % (2020) dans un aperçu de 2026 ferait naître la question « et les années suivantes ? ». Le chiffre se dit en conversation, avec la bonne étiquette.*

## 5 · Texte à envoyer quand ils demandent l'aperçu

> Bonjour Monsieur le Principal 👋
> Je suis Akwo King, je fais les sites des écoles à Buea.
> J'ai préparé l'aperçu de NABESK : vos sections général, technique et commercial, et vos résultats GCE présentés de façon lisible plutôt qu'en PDF.
> (La maquette est jointe — c'est un aperçu, rien n'est en ligne.)
> Je vous montre la suite ?

## 6 · Ce qu'on ne fait pas

- ❌ Jamais citer l'année 2017 (21,64 %) : c'est public, mais le rappeler gratuitement, c'est se faire fermer la porte.
- ❌ Jamais présenter 83,46 % comme le résultat courant de l'école. On dit toujours **l'année** avec le chiffre.
- ❌ Aucun numéro non vérifié.
