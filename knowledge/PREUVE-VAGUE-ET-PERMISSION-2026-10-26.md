# La preuve vague, et le droit de ne pas construire d'avance (26/10/2026)

```text
SOURCE ①  King, 26/10/2026, deux rulings en une phrase :
          « ask him before mentioning, but that isn't important for now — let's just keep it vague and
            say "je fais les sites pour les opticiens de Douala" if it is an optician »
          « you said the owner will say no, that means our closing rate is low right — using that same
            POV, optimise the messages once more »
SOURCE ②  Recherche en ligne du 26/10 (tier C — témoignages, agrégateurs, aucun chiffre camerounais)
PORTE     tools/qa/audit_outreach.py · PREUVE élargi · banc 26/26
USAGE     tous les messages froids vers un opticien, à Douala et ailleurs
```

---

## 1 · Ce que le ruling change dans la phrase de preuve

| Avant (v4) | Après (v5) |
|---|---|
| « J'ai fait le site **d'un opticien d'ici**, il est en ligne. » | « **Je fais les sites pour les opticiens de Douala**, et l'un des leurs est en ligne. » |
| suppose un client nommable, et « d'ici » ne dit ni métier ni ville | dit le **métier** et la **ville**, jamais le client |
| cinq variantes de la même phrase dans le lot | cinq formulations différentes, même contenu |

**Pourquoi c'est un progrès et pas un recul.** Nommer DM Optique aurait été la preuve la plus forte —
et c'est **son** accord qu'il faut, pas notre envie. King a tranché : on demande d'abord, on reste vague
en attendant. Une preuve vague **ne se dément pas** ; une preuve nominative envoyée sans accord peut
coûter le client, pas seulement le prospect.

**La ligne rouge, écrite ici pour qu'elle ne glisse pas** : « je fais les sites pour les opticiens de
Douala » est une **catégorie de métier**, pas un compteur. Ça devient faux le jour où l'on écrit « la
plupart », « plusieurs » ou un chiffre. Aucun de ces mots n'entre dans un message.

## 2 · Ce que la porte a dû apprendre

`PREUVE` ne connaissait que « j'ai fait », « un opticien d'ici », « en ligne ». La nouvelle preuve
existait donc et la porte ne la voyait pas — exactement le défaut de `CAUSE` au pluriel, la veille.
Trois motifs ajoutés (`les sites pour les opticiens`, `sites pour les opticiens`, `site pour un
opticien`), **un cas de banc ajouté** (la preuve vague passe sans avertissement), banc **26/26**.

Le message d'avertissement ne dit plus « DM Optique, en ligne » : il dit « dire le métier et la ville, et
qu'un site tourne déjà ». Une porte qui cite un client dans son propre code finit par le citer dans un
message.

## 3 · Ce que la recherche en ligne dit — et ce qu'elle ne dit pas

| Source (26/10/2026) | Ce qu'elle donne | Ce qu'elle ne donne pas |
|---|---|---|
| **sbl.so**, guide WhatsApp froid 2026 | **3–5 %** de réponses en première touche froide ; **15–20 %** quand le message est vraiment documenté | rien sur le Cameroun ; l'écart 3–5 / 15–20 est déclaratif |
| **Overloop**, longueur 2026 | **50–125 mots** = meilleure bande (8,2 %) ; **sous 25 mots**, 4,1 % | nos messages à 58–69 mots sont **dans** la bande : raccourcir serait un recul |
| **b2bleadfinder**, agences web 2026 | nommer un manque **vérifiable** : 15–20 % contre 1–3 % générique | un article de vendeur, sans échantillon publié |
| **prospeo**, Loom froid 2026 | **demander la permission d'abord** : 15–22 % ; envoyer la vidéo non sollicitée : 3–4 % | chiffres de praticiens, pas d'étude contrôlée |
| **buzzlead** + r/b2b_sales | on n'enregistre **que pour ceux qui ont répondu** ; l'audit gratuit de 3 h ne se lit pas | aucun test sur un marché francophone |

**Ce que ça change, et c'est un aveu.** La veille, j'avais recommandé de **construire un aperçu par
prospect** (10 minutes, 50 minutes pour cinq). La recherche du 26/10 dit l'inverse : ce qui bat
l'envoi non sollicité, c'est de **demander d'abord**, puis de construire pour ceux qui ont dit oui. La
v5 est donc écrite pour que **l'aperçu se construise après le oui** — et le Roast Room a ajouté une
seule exception : l'aperçu de ①, construit **avant**, pour que la promesse de ce message-là ne soit pas
une promesse (voir `knowledge/ROAST-2026-10-26-LOT-1-V5.md`, verdict B).

## 4 · Ce qui reste non vérifié, et qui doit le rester dans les messages

- **Aucun taux de réponse camerounais n'existe** : tout chiffre écrit dans un message serait inventé.
- **L'hypothèse « preuve vague = crédible »** n'est mesurée nulle part. Elle protège le client ; elle
  peut coûter des réponses. On ne le saura qu'après les cinq.
- **La permission d'abord** suppose qu'il répond « oui » — donc que le message tienne sans objet montré.
  C'est précisément ce que la v5 parie.
