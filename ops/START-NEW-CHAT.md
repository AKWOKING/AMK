# Démarrer la session suivante

> À coller tel quel dans le premier message d'une nouvelle session. Le dépôt porte tout le reste.

> **Mise à jour du 24/10/2026 — l'ordre de démarrage n'est plus un texte, c'est une commande :**
> `bash tools/ops/machine.sh` (carte : `ops/MACHINE.md`), puis `bash tools/ops/provision.sh` sur une
> session neuve. Le message ci-dessous reste utile pour **le contexte métier daté du 22/10** — les
> trois chantiers qu'il liste ont été traités ou requalifiés depuis ; l'état vrai est au handoff le
> plus récent, pas ici.

---

## Le message à copier

```
Lis AGENTS.md, puis ops/HANDOFF-2026-10-22.md. Commence par lancer `python3 tools/ops/wake.py`
avant de lire ou de mesurer quoi que ce soit — le dépôt local peut être périmé.

Contexte : on continue le travail d'AMK (Douala). Premier client payant DM Optique SARL, et notre
propre présence à remettre à niveau.

Le dépôt est fusionné dans main. Trois choses à faire, dans cet ordre :
1. DM Optique — écrire la pièce du jeudi 30/10 (« pourquoi on revient » : une monture réglée en
   janvier ne l'est plus en juin), sous la direction de marque v2.
2. AMK — appliquer les 5 corrections du site puis déployer (site/OPTIMISATION-2026-10-22.md).
3. AMK — les comptes : vérifier si la page facebook.com/amkweb existe avant d'en créer une.

Règles qui ne se discutent pas : aucun montant publié, aucun nombre de montures nulle part, aucun
visage de patient, aucun délai promis. Avant tout contenu client : relire
clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md. Avant de publier : `bash tools/ops/gate-dm.sh`.
```

---

## Ce que la nouvelle session doit savoir en premier

| # | Point | Où |
|---|---|---|
| 1 | **L'arbre peut être faux.** Le local revient au commit de début de session. `wake.py` répare. | `AGENTS.md` §1–2, `ops/GIT-STABILITY-NOTE.md` |
| 2 | **On pousse après chaque lot.** Un commit local peut disparaître, un commit poussé non. | `AGENTS.md` §2 |
| 3 | **La direction de marque DM est arrêtée** : A moteur, B preuve, C limite. | `clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md` |
| 4 | **Le produit n'est pas le sujet** — on vend l'expertise, la confiance, l'expérience. | idem, §5–7 |
| 5 | **`ugc-03` est mort** (MP4 périmé, carte fautive). Ne pas le republier. | `content/month1/w1/ugc-03.md` |
| 6 | **`tiktok-01-v2` part mardi 27/10 à 19 h** ; à relire sur téléphone avant. | `content/month1/w1/tiktok-01-v2-20-20-20.md` |
| 7 | **Pas de navigateur ni de ffmpeg ici** : ce qui doit être vu se fait relire par King. | `AGENTS.md` §5 |
| 8 | **La mesure, ce sont les conversations WhatsApp**, pas les vues. | `ops/HANDOFF-2026-10-22.md` §11 |

---

## Après chaque session

Mettre à jour `ops/HANDOFF-2026-10-22.md` (ou en créer un nouveau daté) : état, décisions, chantiers
ouverts, prochaine action, questions en attente. Puis committer et pousser — sinon le travail de la
session n'existe pas pour la suivante.
