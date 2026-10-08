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

## Balayage du repo (08/10) — à ranger par King, non modifié ici (hors périmètre du site)

- `clients/dm-optic/build-notes.md` (l.71, 75, 144, 239), `content-plan-month1.md` (l.40) :
  « Inscrit depuis 2016 », « le registre vous connaît depuis 2016 » — **« 2016 » est déduit du
  suffixe du numéro 021/2016** ; le repo ne contient pas la page d'annuaire datée. Source par
  inférence. Le re-pull ONOC du 11/10 peut vérifier la date.
- `clients/dm-optic/ads/campaign-brief.md` l.16, `ads/variant-messages.md` l.38 (W1-A) :
  « Cet opticien **exerce** depuis 2016 » — affirme l'**exercice**, le registre ne prouve que
  l'**inscription**. Claim plus fort que la source : candidat à correction avant toute diffusion.
