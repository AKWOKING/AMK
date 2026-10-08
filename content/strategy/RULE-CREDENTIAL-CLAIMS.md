# RÈGLE PERMANENTE — aucune mention de diplôme/qualification sur un site client sans source au repo

> Ruling King 08/10/2026. S'applique à toute page, annonce, message ou vidéo qui affirme une
> qualité professionnelle d'un client (diplôme, titre, certification, ancienneté, agrément).

**Règle :** **aucun claim de credential sur un site client sans une source traçable au repo pour CE
credential précis.** Pas de source = pas de mention. Un fait voisin n'autorise pas le claim (une
inscription à l'Ordre ne prouve pas un diplôme ; un numéro d'inscription ne prouve pas une durée
d'exercice).

## Application immédiate (DM Optique)

| Claim | Source au repo | Statut |
|---|---|---|
| « Inscrit à l'ONOC » | registre ONOC, annuaire Littoral, ligne 102 : inscription 021/2016, arrêté 0382, titulaire M. Domche Noumbi (`clients/dm-optic/build-notes.md` l.54) | ✅ **autorisé** (trust bar du site) |
| « Opticien diplômé » | **aucune** | ⛔ **retiré** de `SPEC-PAGES-v1` (seule occurrence au repo) |

## Ruling 08/10 — W1-A réécrit, et règle de source

**Le suffixe « /2016 » du registre est un numéro de décret (arrêté 0382, 021/2016), pas une durée
d'exercice. Ne jamais sourcer des « années de pratique » depuis un numéro de document.**

- **FAIT :** « Cet opticien exerce depuis 2016 » → « **Cet opticien est inscrit à l'ONOC** » (source :
  registre, ligne 102, 021/2016), sur les 7 fichiers où la phrase exacte apparaissait (campagne,
  variantes + lien WhatsApp ré-encodé, README C1, script UGC, carrousels.md, SETUP-TIKTOK, script
  démo).

## Balayage du repo (08/10) — reste à ranger par King (ruling non étendu)

« **inscrit depuis 2016** » / « le registre vous connaît depuis 2016 » (≈25 occurrences) dérive du
même suffixe de décret. Le ruling couvre W1-A ; **je ne l'étends pas sans mot.** Exposition :
`build-notes.md` + prototype montré au client · `launch/SETUP-FACEBOOK|TIKTOK|GOOGLE-BUSINESS.md`
(bios, avant go-live) · `posting-calendar.md` · `content-plan-month1.md` · `carousels.md` slides +
**PNG rendus `c1-render/slide-*.png` (texte figé dans l'image)** · `ugc-script.md` · `research/*` ·
`website/brief.md`, `inspiration.md`. Question à King : « inscrit depuis 2016 » = acceptable (année
d'inscription) ou à remplacer par « Inscrit à l'ONOC » partout ?
