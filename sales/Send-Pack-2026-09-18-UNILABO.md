# UNI-LABO — réponse à chaud · 18 Sep 2026 (21:54 WAT)

**Contexte :** UNI-LABO a répondu **« Bsr »** le **18/09 à 20:57** au msg1 du soir
(« Je vous prépare un aperçu gratuit de votre accueil ? Un « oui » suffit. »).
C'est la **2ᵉ réponse humaine de la campagne** (après St. Theresa le 15/09).
**PRR : 2/31 = 6,5 %.**

**Décision de King (18/09) :** « il n'y a pas de lien de l'aperçu… c'est à toi de créer
le site web unique de UNI-LABO **sur mesure** » → construit, audité, à déployer par King,
puis lien envoyé. C'est l'exception à la règle *(ff) : ne pas construire avant un « oui »*,
parce que le « oui » de King vaut commande.

---

## Ce qui est prêt

| Élément | État |
|---|---|
| Source canonique | `demos/concept-unilabo-v1.html` (44 Ko, fichier unique, 0 asset externe) |
| Bundle de déploiement | `hosting/previews/unilabo/index.html` (= copie à l'octet) |
| Maquette envoyée plus tôt | `clients/douala-cliniques/07-unilabo.jpg` |
| **Gate `audit_html.py`** | ✅ **0 finding** — 285 passages de texte (desktop **et** mobile) |
| Parité FR/EN | ✅ 126 / 126 nœuds |
| Liens | 11 × `wa.me/237696139819` · 7 × `tel:` — **aucun prix affiché** |
| Indexation | `noindex` + JSON-LD `MedicalBusiness` |

**Faits sourcés qui sont dans la page** (aucune invention) : Dr Tientcheu Philomène,
biologiste · Bonamoussadi, **Carrefour Etoo**, Rue 5N441 BP 2592 · **696 13 98 19** (WhatsApp)
· 233 47 00 68 · **Lun–Ven 07h–19h, Sam 07h–13h** · espèces · FR + EN.
Les deux points que les sources se contredisaient (18h vs 19h ; Rue 5N121 vs 5N441) ont été
tranchés en faveur de la source la plus spécifique — **et la page demande au labo de corriger**.

---

## 1 · Déploiement — King (≈ 2 minutes)

1. vercel.com → **Add New → Project**
2. glisser le dossier `hosting/previews/unilabo/` (il contient `index.html`)
3. nom du projet : **`unilabo-concept`** → Deploy
4. lien attendu : **https://unilabo-concept.vercel.app**

> ⚠️ **Vérifiez le lien une fois avant de l'envoyer** (page complète, les 3 boutons du hero
> cliquables). Le lien est déjà écrit dans le message ci-dessous : s'il diffère, corrigez-le.

---

## 2 · Message à envoyer — à chaud, sur le fil existant

**Numéro : 696 13 98 19 · douala → FRANÇAIS**

```
Bonsoir. Akwo King, AMK — Douala. Vous m'avez écrit ce soir, alors je vous réponds avec l'aperçu plutôt qu'avec un discours.

https://unilabo-concept.vercel.app

Il est fait pour UNI-LABO : vrais horaires, préparation des examens, itinéraire Carrefour Etoo, en français et en anglais.
Dites-moi si les horaires et la liste des analyses sont exacts — je corrige tout de suite. Un « oui » suffit.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Si l'envoi part après 06h00 samedi →** remplacer « Bonsoir » par « Bonjour » et
« ce soir » par « hier soir ». Rien d'autre ne change.

**Pourquoi ces choix :**
- **Ligne 1 = raison d'ouvrir**, pas de signature ni de réassurance (règle 48).
- **Aucun prix dans le message** : le prix se pose avec la preuve qu'il achète (règle 48).
- La question finale est un **« oui » / « non »** et elle sert le client :
  il valide ses propres horaires (règle 45).
- Pas de « je prends ça pour un accord » : un « Bsr » n'est pas un accord (leçon 69).

---

## 3 · Relances prévues

| Quand | Angle |
|---|---|
| **M+2 — dim 20/09** | « Vous avez pu ouvrir ? » + **une seule** correction faite à la main devant lui (rapidité = preuve) |
| **M+4 — mar 22/09** | la question des **horaires du samedi** : c'est un samedi qu'il perd des patients |
| **M+7 — ven 25/09** | dernier : prix 100 000 FCFA 50/50, **une fois**, jamais de remise → puis `parked` |

Après la 3ᵉ relance sans réponse : **`parked`**, pas de 4ᵉ.

---

## 4 · Ce que dit ce fil (pour le CRM)

- **2 réponses humaines sur 31 fils ouverts.** Le message du soir a produit une réponse
  **en 35 minutes**, après 5 jours de campagne. À noter pour le prochain lot :
  c'est le **premier message d'un fil** qui a fait répondre, pas une relance.
- **UNI-LABO = le lead le mieux documenté de la campagne** (3 sources recoupées, nom du
  biologiste, deux numéros, deux horaires) → c'est ce niveau de recherche qui a permis de
  construire la page en 1 h 30 sans jamais inventer une ligne.
