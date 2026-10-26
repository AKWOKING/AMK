# RÉPONSE « OUI » — ce qui se passe dans les 24 heures (26/10/2026)

```text
Déclencheur : un des sept du lot `sales/ENVOI-VAGUE-2-2026-10-26.md` répond oui, ou demande « montre-moi ».
Promesse     : la page à son nom, dans son téléphone, sous 24 h — c'est la promesse publique du site AMK.
Portes       : les six qui existent déjà + la porte de livraison `audit_delivery.py` + le deploy gate téléphone.
Interdit     : publier son nom en clair sur une page publique · promettre une fiche Google validée · annoncer un prix
               qu'il n'a pas demandé.
```

> **Ce document ne construit rien.** Il dit **quoi construire, dans quel ordre, et ce qui ferme chaque
> étape** — pour que la réponse à un « oui » ne dépende pas de ma mémoire à 23 h. Il applique le flux du
> 24/10 (`docs/superpowers/specs/2026-10-24-flux-prospection-design.md` §1, étape 5) : la
> personnalisation arrive **après** la réponse, jamais avant.

---

## 1 · Les huit gestes, dans l'ordre, avec le temps de chacun

| # | Geste | Temps | Sortie | La porte |
|---|---|---|---|---|
| 1 | **Répondre oui, en trois lignes**, avec l'heure de livraison nommée | 2 min | un message daté (« demain 10 h ») | §4 du kit de publication : une heure, jamais « bientôt » |
| 2 | **Récolter ses faits** — nom exact, quartier, horaires, WhatsApp, spécialités, photos | 15 min | `clients/<slug>/facts-<date>.md`, **chaque ligne avec sa source** | §8c : une preuve par affirmation. Aucun fait inventé n'entre dans la page |
| 3 | **Réserver le design** — lire `clients/_uniqueness-registry.md` et s'y inscrire | 5 min | une ligne au registre (archétype, palette, typo, ton) | `AMK-DESIGN-SKILLS` §17 : jamais deux fois le même design |
| 4 | **Construire** depuis le gabarit DM (`demos/dmoptic-v1.tpl.html`) en un seul fichier | 2 h | `hosting/previews/<slug>/index.html` | §1b (portiques) + `audit_hero.py` + `audit_page.py` |
| 5 | **Passer les portes mécaniques** | 15 min | six lignes vertes | `audit_a11y.py` · `audit_delivery.py --strict` · `audit_claims.py` · `audit_images.py` · `audit_html.py` · `test_amkcm_lang.mjs` |
| 6 | **Étiqueter la fiction** : `noindex,nofollow`, et tout chiffre non vérifié porte sa mention | 2 min | balise + mention visible | `hosting/build_previews.py` réinjecte `noindex` ; la mention est écrite à la main |
| 7 | **Déployer sur Vercel** dans **son** projet | 10 min | une URL `*.vercel.app` | §1f③ · jamais le domaine du client avant signature |
| 8 | **Le deploy gate téléphone** — 6 points, sur son téléphone à lui | 10 min | ✅ ou on corrige | `hosting/previews/README.md` §deploy gate : non vérifié sur téléphone = non envoyé |

**Total : 3 h de travail réel sur les 24 h.** Le reste du temps est de l'attente — et c'est bien ainsi :
la promesse est une **borne**, pas une performance.

---

## 2 · Le message à envoyer une fois la page prête

**Image d'abord, texte ensuite** — jamais les deux dans le même message (`hosting/previews/README.md`
§règles d'envoi).

> Bonjour, voilà votre page : [lien].
> Vos horaires, votre adresse et votre WhatsApp y sont — le numéro ouvre directement la conversation.
> Ouvrez-la sur votre téléphone, pas sur un ordinateur. Dites-moi ce qui ne va pas : je corrige aujourd'hui.

**Trois règles de ce message** : le lien est **cliquable et seul** · aucun prix · aucune demande
d'engagement. Le prix se dit **quand il le demande**, jamais avant (`PLAYBOOK` §0 ligne 5).

---

## 3 · Ce que la page ne fait jamais, même sur un « oui »

| Interdit | Pourquoi |
|---|---|
| **Son nom en clair sur une page publique** | ruling du 17/09 : un aperçu partagé un-à-un n'est jamais public. `noindex,nofollow` **et** un slug neutre |
| **Une fiche Google « créée » ou « validée »** | la validation dépend de Google. On **regarde** sa fiche, on **l'accompagne** ; on ne promet pas |
| **Un chiffre qui n'est pas le sien** | chaque prix, chaque horaire, chaque compteur est tracé à une source, ou étiqueté « exemple » |
| **Un témoignage ou un avis emprunté** | on n'a qu'un client, et ses avis ne sont pas transférables |
| **Une mesure d'appels** | nous n'avons aucun accès à ses appels (ruling 142) |
| **Un domaine à notre nom** | le domaine s'enregistre **à son nom**, dans son dossier (conditions d'intervention, 07/10) |

---

## 4 · Les huit points du deploy gate, à cocher avant d'envoyer le lien

Sur **son** téléphone, la nuit si possible (`AMK-DESIGN-SKILLS` §24.3.5) :

- [ ] la page démarre en **FR**, le basculeur EN|FR change tout, dans les deux sens ;
- [ ] un **pré-remplissage WhatsApp ouvert depuis un bouton** — bon numéro, bon texte, encodage correct ;
- [ ] le bouton mobile fixe est visible et cliquable ; la navigation tient sur une ligne ; aucun
      débordement horizontal ;
- [ ] **ses** faits réels s'affichent ; tout chiffre qui n'est pas le sien porte son étiquette ;
- [ ] la **passe de provenance** est faite : chaque prix, horaire, compteur a sa source ;
- [ ] `noindex,nofollow` est bien dans le HTML servi (pas seulement dans le fichier local) ;
- [ ] après un correctif, la vérification se refait **sur l'URL en ligne** ;
- [ ] la page s'ouvre en moins de 5 s en 4G, et les images ne dépassent pas 250 Ko chacune.

---

## 5 · Si le oui n'arrive jamais — la règle de sortie

Un message froid qui reste sans réponse **n'est pas un refus** : c'est un silence. La règle du dépôt
(`CLIENT-MESSAGING-RULES` §13) :

- **coches grises** (livré, jamais ouvert) → `parked`, raison datée, **aucune relance** ; le fil ne rouvre
  que si le cabinet écrit ;
- **deux coches bleues** (lu) → **une** relance de rupture à J+7, une seule fois, et elle ne vend rien.

Et la décision qui compte, si les sept restent muets : elle ne se prend **pas** sur ce lot. Elle se prend
sur la question du brainstorming — *le message est-il le bon, ou l'offre ?* — avec les sept lignes du
tracker en main, pas avec une impression.
