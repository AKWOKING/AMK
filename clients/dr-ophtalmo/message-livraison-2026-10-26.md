# Message de présentation à King — Aperçu Dr Ophtalmo (26/10/2026)

**Ce que ce message accompagne :** le lien d'aperçu `https://dr-ophtalmo-preview.vercel.app`
(noindex, non publié) et la vidéo de lancement brag de 20 s — **désormais dans le dépôt**, demande de
King du 26/10 (« push the brag video to github ») :

| Fichier | Lien | Poids |
|---|---|---|
| `brag.mp4` (lecture) | `https://github.com/AKWOKING/AMK/raw/main/clients/dr-ophtalmo/brag/brag.mp4` | **4,1 Mo** |
| `brag-whatsapp.mp4` (statut WhatsApp) | `https://github.com/AKWOKING/AMK/raw/main/clients/dr-ophtalmo/brag/brag-whatsapp.mp4` | **2,5 Mo** |
| `poster.jpg` (affiche) | `https://github.com/AKWOKING/AMK/raw/main/clients/dr-ophtalmo/brag/poster.jpg` | 67 Ko |

**Rien ne part au médecin avant la réponse de King** : la vidéo reste un brouillon (§1f②) et le lien
n'est pas publié. Les liens ci-dessus fonctionnent dès la fusion sur `main` ; sur une branche, remplacer
`main` par le nom de la branche.

---

## Le message (WhatsApp, à copier tel quel)

> Le site est prêt, King : https://dr-ophtalmo-preview.vercel.app — quatre lieux, les jours que le
> médecin a donnés, et « à confirmer » partout où il n'a rien envoyé.
> La vidéo de 20 s est sur GitHub, cette fois par un lien qui ne meurt pas : la version statut
> WhatsApp pèse 2,5 Mo, la version de lecture 4,1 Mo.
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

## Ce qui a changé le 26/10 au soir — la leçon du chemin qui meurt

La veille, les deux vidéos n'existaient que dans `/home/user/brag-output-dr-ophtalmo/`. Au redémarrage
de l'environnement, **le dossier n'existait plus** : la vidéo était « prête » et introuvable. King a dû
demander « push the brag video to github ». Les fichiers sont donc **rendus à nouveau** (captures réelles,
`check` 0 erreur / 19-19 AA, `audit_video_motion` OK) et **versionnés dans le dépôt**, sous
`clients/dr-ophtalmo/brag/`, avec une exception datée dans `.gitignore` — 6,7 Mo en tout, le master de
14 Mo restant dehors.

Deux corrections ont été trouvées en regardant les images rendues, pas en lisant le code : le panoramique
à 1,14 d'échelle **rognage le texte du site sur les côtés** (ramené à 1 → 1,02) et la carte de légende
laissait **traverser le texte de la page** (fond opaque, pastille « Horaires à confirmer » déplacée dans
la carte). Le premier rendu a aussi été **bloqué par `audit_video_motion`** — fenêtre 18–20 s figée à 1,39
— réglé par un troisième halo et un fond qui avance vers la caméra sur les 20 s.
