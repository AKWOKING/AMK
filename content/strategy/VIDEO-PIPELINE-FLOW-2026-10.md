# Pipeline vidéo Flow + ChatGPT — octobre 2026

Statut : **v1, brouillon de travail.** Remplace `render.mjs` pour toutes les nouvelles vidéos. `render.mjs` reste le plan de secours uniquement.
Date : 13/10/2026. Propriétaire : King (exécute et publie). Rôle de l'agent : ORCHESTRATEUR (script, prompts, contrôle).

Légende : **[V]** vérifié contre une source · **[NV]** non vérifié, à tester sur l'outil avant de s'y fier.

---

## 1. Vue d'ensemble

- Chaîne : script FR à la première personne (45–60 s) → prompt Flow par plan → génération des clips dans Google Flow → assemblage (ChatGPT donne le prompt ou le plan de montage) → contrôle qualité → publication par King.
- Principe de King : **on livre, on observe, on affine.** Une vidéo imparfaite est acceptable. La dérive d'environnement et de logo entre plans est connue et acceptée.
- Le protagoniste est l'avatar animé dans Google Flow. Il ne change pas d'une vidéo à l'autre sans décision de King.

## 2. Rôle des outils

| Outil | Rôle | Statut |
|---|---|---|
| Agent (orchestrateur) | Script FR, prompt par plan, prompt d'assemblage, grille QC | Ce document |
| Google Flow (Veo 3.1) | Génération des plans vidéo, avatar | Crédits [V], voir §9 |
| ChatGPT | Prompt d'assemblage et ordre de montage | Rôle [NV] pour l'assemblage réel |
| `render.mjs` (dépôt) | **Secours uniquement** si Flow échoue durablement | Existant |

## 3. Système à trois ingrédients

1. **Avatar de référence** : une image fixe de l'avatar, utilisée pour garder le même visage et les mêmes vêtements. [NV] nombre d'emplacements de référence (le brief indique 3 ; à tester).
2. **Décor de référence** : une image du lieu (clinique, boutique, écran de téléphone) pour limiter la dérive d'environnement.
3. **Logo / carte d'identité** : fourni comme image ou ajouté en montage, jamais généré de mémoire par le modèle. Le logo DM Optique est dans `clients/dm-optic/website/logo/`.

## 4. Enchaînement des plans (frame chaining)

- Méthode visée : la dernière image d'un plan sert de première image du plan suivant pour garder la continuité. **[NV]** La méthode exacte dans Flow (image de départ, extension, ou export manuel) doit être confirmée sur l'outil.
- Si l'enchaînement échoue : chaque plan est généré à partir des trois ingrédients (§3) et la continuité se règle au montage.

## 5. Modèles de prompt Flow

### 5a. Prompt par plan (modèle)

```
Plan {n}/{N}. Durée visée : {d} s.
Personnage : l'avatar de la référence 1, même visage, même tenue (blouse blanche ou tenue du décor).
Décor : {description du lieu}, correspondant à la référence 2.
Action : {une action simple, un seul geste}.
Cadrage : {plan moyen / gros plan}, caméra fixe, lumière naturelle de jour.
Voix : français, ton calme et direct, à la première personne. Réplique : « {phrase du script} ».
Ne pas : changer le visage, ajouter du texte à l'écran, inventer une marque ou un logo.
```

### 5b. Prompt d'extension (Extend) — [NV]

Le brief indique qu'Extend prolonge un plan jusqu'à 148 s. **Non vérifié.** À n'utiliser qu'après test :

```
Prolonge le plan précédent de {d} s. Même personnage, même décor, même lumière.
Action suivante : {une action}. Réplique : « {phrase} ».
```

## 6. Modèles de prompt ChatGPT (assemblage)

```
Voici {N} plans vidéo en MP4 et le script FR ci-joint. Propose :
1. l'ordre de montage, plan par plan, avec l'heure de début et de fin ;
2. les coupes à faire si un plan dérive (visage ou décor) ;
3. où placer le logo / la carte d'identité (fin, 2 s) ;
4. la durée totale, qui doit rester entre 45 et 60 s.
Ne modifie pas le script. Réponds en français, en liste courte.
```

## 7. Contrôle qualité avant publication (grille King)

- [ ] Le visage de l'avatar est le même d'un plan à l'autre (sinon couper ou régénérer le plan).
- [ ] Le décor ne change pas sans raison.
- [ ] Aucun texte généré dans l'image (fautes, faux chiffres).
- [ ] Aucun logo ou marque inventée ; le logo réel est ajouté en montage.
- [ ] Phrases du script audibles, sans bruit ni coupure.
- [ ] Durée 45–60 s.
- [ ] Aucun chiffre, prix ou promesse qui n'a pas été validé par King.
- [ ] Le fichier final est celui qui sera publié (nom de fichier vérifié).

## 8. Échecs connus et récupération

| Échec | Récupération |
|---|---|
| Visage qui change entre plans | Régénérer le plan avec la référence 1 ; sinon couper |
| Décor qui dérive | Accepter si la dérive est légère (on livre) ; sinon régénérer avec la référence 2 |
| Texte illisible généré dans l'image | Régénérer sans texte dans le prompt ; ajouter le texte en montage |
| Génération échouée | Non facturée [V] ; relancer |
| Quota du jour épuisé | Attendre le lendemain (pas de report) [V] ; réduire le nombre de plans |
| Flow indisponible ou non accessible sur le compte | Plan de secours : `render.mjs` (dépôt) |

## 9. Budget de crédits par vidéo

Sources : [V] `promoclock.co/en/tools/google-flow/` et `saascrmreview.com/google-flow-pricing/`, consultés le 13/10/2026.

- Crédits gratuits : **50 par jour, sans report** [V].
- Coût par génération : Veo 3.1 Lite **10**, Fast **20**, Quality **100** [V]. Ultra divise par deux Lite et Fast [V]. Facturé par génération, pas par prompt [V]. Génération échouée non facturée [V].
- Budget calculé :
  - 6 clips Lite = 60 crédits (1 à 2 jours de crédits gratuits) [V, calcul].
  - 6 clips Fast = 120 crédits (plus de 2 jours) [V, calcul].
  - 1 clip Quality = 100 crédits [V, calcul].
- **Accès gratuit à Flow :** confirmé fonctionnel sur les comptes de King le 13/10 (déclaration de King, non vérifiée de source).
- **Non vérifié** : bonus de 100 crédits à l'inscription ; durée de 10 s par clip.

## 10. Extend ou 6 clips ?

- Option A, 6 clips de 8–10 s assemblés : plus fiable, plus de crédits (60 en Lite), plus de montage.
- Option B, Extend : moins de montage si l'outil tient la continuité. **Non vérifié** (limite de 148 s, continuité). À tester sur une vidéo de test avant toute publication.
- Recommandation provisoire : Option A en Lite pour la première vidéo, Option B testée à part sur un plan.

---

## Décisions et points ouverts

- **Vidéo publiée (POST-01) :** version Flow, hors dépôt (téléphone de King). Le `render.mjs` est la version antérieure.
- **Archivage :** seulement si POST-01 performe (rétention 3 s > 60 %, commentaires positifs), dans `content/pipeline/`.
- **Chiffres réels :** King les fournira après la séance de cohérence du 14/10. Restent [NV] : bonus de 100 crédits, clips de 10 s, chaîne Extend, limite de 3 références.
- **Validation :** le document reste non commité jusqu'à la confirmation de King après la séance du 14/10.
