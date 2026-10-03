# GIT STABILITY NOTE · 03/10 · pattern récurrent du sandbox

- **Pattern :** le `.git` du sandbox revient par intermittence à un commit de base au cours des longs
  tours (7 fois cette semaine, dont 1 le 03/10 en plein ruling DM).
- **Symptômes :** `views.py` redevient une vieille version ; les ancres de recherche python ne matchent
  plus ; `ls-remote` diverge du `git log` local.
- **Tells :** la sortie de la file RELANCE contredit ce qui vient d'être écrit ; le guard passe mais le
  contenu est périmé (rc=0 ne prouve rien — règle 02/10).
- **Mitigation (appliquée à chaque tour) :** `git ls-remote origin` est la **seule source de vérité** ;
  ne jamais faire confiance au seul état local ; au début du rituel, fetch + reset --hard sur la ref
  distante ; après chaque rebuild, vérifier la sortie de la file ; sauvegarder les écritures du tour
  dans /tmp avant tout reset.
- **Implication mercredi 07/10 :** si un commit pré-visite a rollback pendant la nuit, **re-vérifier
  contre la remote avant de partir pour Bonabéri** — le bundle de démo, les PDF d'impression et la file
  RELANCE doivent être relus depuis `origin/arena/01a0f7ad-amk`, pas depuis le working tree local.
