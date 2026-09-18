# Summerset Bilingual College (SMBICOL) — Wokoko, Buea

**MQL 6/6 · FROID — jamais approché · aucun numéro WhatsApp connu**
Statut corrigé le 18/09 : **aucune carte scellée n'a été déposée**. Ce prospect n'a jamais été contacté. Il n'y a pas de canal : sans numéro trouvé, il n'est pas joignable aujourd'hui.

---

## 1 · Faits vérifiés

| Fait | Source |
|---|---|
| **Principal : Yerima Samson Tata** (nommé publiquement) | *Cameroon Tribune*, 2 juin 2026 — « Locked Gates, High Stakes » |
| Leur **centre d'accueil a reçu ≈ 1 350 candidats** au GCE de juin 2026, sections **grammaire, technique et commerciale**, sous surveillance policière permanente | idem |
| Adresse : **Check Point Wokoko**, Buea — en face de la pharmacie ENAMEN | `sales/Walk-In-Batch-2026-09-15.md` |
| Fondé en **2000**, ≈ **1 000 élèves**, ≈ **80 enseignants** | recherche dépôt, 14/09 |
| **Aucun site web.** Page Facebook **inactive depuis décembre 2015** ; l'adresse mail qu'elle porte appartient à un tiers | `sales/Invitation-First-Replan-2026-09-15.md` |
| Boîtes mail déclarées : smbicol@yahoo.com (faible) | idem |
| Présent dans les annuaires scolaires (inovedu.net) — mais **sans fiche à eux** | inovedu.net |
| Enseignants de longue date (un professeur y est depuis 2013) → institution stable | LinkedIn, profil public |

**Le chiffre qui compte : 1 350 candidats.** Un centre qui accueille 1 350 candidats au GCE est une institution connue de toute la région — et qui n'existe pas en ligne. C'est la contradiction qui vend.

## 2 · Douleur

1. **Aucune page à eux.** Leur présence en ligne se résume à une page Facebook morte depuis 2015 et à des fiches d'annuaire.
2. **Un parent qui cherche « Summerset Bilingual College Buea »** tombe sur des annuaires, pas sur l'école.
3. **Leur principal événement de l'année — le GCE — a été rapporté par la presse nationale, pas par eux.** La preuve de sérieux existe ; elle n'est nulle part chez eux.
4. Aucune procédure d'admission en ligne, aucune grille de frais consultable.

## 3 · Direction artistique

**Style : `professional` + accents `editorial`** · **Palette : Cobalt + Cream** (§6.2 rotation — jamais la famille du projet précédent)
**Dial : VARIANCE 5 · MOTION 4 · DENSITY 4** — sous les presets écoles (6/4/4) : une institution de 2000 avec 1 350 candidats veut de l'autorité et de l'ordre, pas de la fantaisie.

| Rôle | Valeur |
|---|---|
| Marque | `#1B3F8F` cobalt profond |
| Secondaire dérivé | `#5A78BE` (éclairci à 30 %) |
| Fond | `#F6F1E7` crème — **jamais** `#FFFFFF` pur (§3.1) |
| Encre | `#141A24` — **jamais** `#000000` pur |
| Accent rare | Le cobalt ne couvre que CTA + filets (règle 60-30-10, §6.1) |

**Pourquoi ce choix :** le cobalt est la couleur de l'institution académique classique ; posé sur crème il lit « sérieux, bilingue, établi ». Il se distingue nettement des deux autres prospects du lot (cyan technique pour NABESK, brique pour Saint Bernard), donc aucun des trois ne ressemble aux autres.

## 4 · Maquette — ⚠️ À REFAIRE EN ANGLAIS

**Défaut signalé par King le 18/09 : cette maquette a été produite en français alors que Buea est anglophone.** Elle ne doit pas être envoyée telle quelle. La commande ci-dessous est conservée telle quelle ; la corriger = passer les jetons en anglais (`--h1 --sub --svc`, et le libellé `--line`).

```bash
python3 tools/outreach/mockup.py --vertical college \
  --name "Summerset Bilingual College" \
  --specialty "Collège bilingue · Wokoko, Buea" \
  --color "#1B3F8F" \
  --h1 "Bilingue,|de la 6e à la Terminale" \
  --sub "Fondé en 2000 à Wokoko. Plus de 1 300 candidats ont composé au GCE dans notre centre en juin 2026." \
  --svc "Général,Technique,Commercial" \
  --out clients/summerset/maquette-summerset.jpg
```

*Aucun numéro WhatsApp n'est injecté : nous n'en avons pas de vérifié. Ne jamais en inventer un.*

## 5 · Texte à envoyer quand ils demandent l'aperçu

> Bonjour Monsieur le Principal 👋
> Je suis Akwo King, je fais les sites des écoles à Buea.
> J'ai préparé l'aperçu de Summerset : général, technique et commercial, avec l'admission et les frais lisibles sur téléphone.
> (La maquette est jointe — c'est un aperçu, rien n'est en ligne.)
> Je vous montre la suite ?

**Si on nous demande comment on a su :** le GCE de juin 2026 — leur centre d'accueil a retenu l'attention de la presse nationale. On le dit tel quel, sans flatterie.

## 6 · Ce qu'on ne fait pas

- ❌ Chercher à les joindre par un numéro non vérifié — la carte scellée est le seul canal, et il est déjà ouvert.
- ❌ Citer le chiffre de 1 350 comme s'il était officiel : la presse écrit « roughly 1,350 ». On dit **« plus de 1 300 »**.
- ❌ Critique de leur page Facebook morte — on pose la question, on ne la juge pas.
