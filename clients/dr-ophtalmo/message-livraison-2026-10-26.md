# Message de présentation à King — Aperçu Dr Ophtalmo (26/10/2026)

**Ce que ce message accompagne :** le lien d'aperçu `https://dr-ophtalmo-preview.vercel.app`
(noindex, non publié) et la vidéo de lancement brag de 20 s
(`/home/user/brag-output-dr-ophtalmo/brag-whatsapp.mp4` 2,28 Mo · `brag.mp4` 10,4 Mo · `poster.jpg`).
**Rien ne part au médecin avant la réponse de King** : la vidéo reste un brouillon (§1f②) et le lien
n'est pas publié.

---

## Le message (WhatsApp, à copier tel quel)

> Le site est prêt, King : https://dr-ophtalmo-preview.vercel.app — quatre lieux, les jours que le
> médecin a donnés, et « à confirmer » partout où il n'a rien envoyé.
> Deux vidéos l'accompagnent : 20 secondes pour son statut WhatsApp (2,3 Mo), et la version pleine
> (10,4 Mo).
> Trois décisions t'attendent, et elles ne sont pas les miennes : son nom, ses horaires, son numéro.
> Tu veux que je corrige quoi avant que ça parte au médecin ?

---

## Ce que le message ne dit pas, volontairement

- **Aucun horaire précis, aucun numéro, aucun nom** : ils ne sont pas dans la configuration, donc ils ne
  sont pas dans le message non plus. Un message qui annonce ce que le site n'a pas encore se retourne
  contre nous au premier clic.
- **Aucune promesse sur l'envoi au médecin** : le lien et la vidéo vont d'abord à King, le fil client ne
  s'ouvre qu'après son oui.
- **Aucune statistique** : il n'y a pas encore une seule visite mesurée — le site n'a **aucune** mesure
  d'audience, c'est un choix (test §7 : ni `fetch`, ni cookie, ni analytics).

## Portes passées avant écriture

| Porte | Résultat |
|---|---|
| `audit_outreach.py --strict` (motif §13, ≤ 70 mots, ≤ 4 phrases) | **non applicable, et dit comme tel** : c'est une porte de **message froid**, et elle bloque tout « lien cliquable dans un premier message ». Ici le lien **est** le livrable, et le destinataire est King, pas un prospect. La mesure utile est passée quand même : **69 mots, 4 phrases, 1 question** — dans les limites. Contorsionner le message pour satisfaire une porte faite pour un autre destinataire aurait produit un message faux ; la porte qui fait foi ici est celle de livraison, juste en dessous. |
| `audit_delivery.py hosting/previews/dr-ophtalmo --strict` | **VERT** — 0 P1 · 1 P2 · 1 P3, assumés (voir build-notes §5) |
| `node tests/logic.test.mjs` | **40/40** |
| `hyperframes check` + `audit_video_motion.py` | 0 issue, 19/19 AA · **OK** sur les deux fichiers |
| Lecture externe du lien (`fetch_page`) | page servie + `robots.txt` servi |
