# Décision — faut-il ajouter la voix aux sites AMK, et faut-il passer au mensuel ?

**Date :** 18 Sep 2026 · **Origine :** vidéo [20] (`research/YouTube-Lessons.md`) · **Statut : TRANCHÉ PAR KING — 18 Sep 2026**

> **① Prototype voix :** « on teste sur le site de AMK, that's better right » → **construit et testé sur `site/index.html`**
> (`tools/qa/test_voice_widget.mjs`, 24/24). Le site est à nous : le pire cas, c'est un bug trouvé par nous.
> **② Modèle :** « I'm more inclined to 100,000 FCFA then 15,000 monthly » → **retenu**, et `research/Pricing-Model-Cameroon-2026-09-18.md`
> confirme que le marché local va dans ce sens (installation 100 000 = entrée de marché ; maintenance 20 000–50 000 FCFA/mois
> chez les agences → **15 000 est sous le marché, volontairement**). Le mensuel est **optionnel et post-lancement**,
> jamais une condition de la vente. **La règle 43 n'est pas touchée : 100 000, 50/50, jamais de rabais.**

---

## 1 · La question, en une phrase

La vidéo n'apprend pas une fonctionnalité, elle apprend **un modèle d'affaire** : un site qui produit
des rendez-vous se facture **au mois**, pas au fichier livré. Est-ce qu'on garde 100 000 FCFA une fois,
ou est-ce qu'on ouvre une ligne mensuelle ?

| Option | Ce que ça donne | Ce que ça coûte |
|---|---|---|
| **A · On garde 100 000 FCFA, une fois** (règle 43 actuelle) | Simple, encaissable tout de suite, aucune infrastructure à tenir. 0 FCFA change de main tant que personne n'a dit oui. | On reconstruit le même mois à zéro. C'est exactement l'erreur que la vidéo décrit : « if you have to restart every single month, it's not a real business ». |
| **B · 100 000 FCFA + un mensuel (ex. 15 000–25 000 FCFA/mois)** | Le site devient un service : hébergement, modifications, assistant, suivi des clics WhatsApp. Revenu qui s'accumule. | Il faut tenir une promesse chaque mois — donc du temps — et le client peut arrêter. |
| **C · Mensuel seulement, pas d'installations** | Le plus attractif à l'entrée pour un petit labo. | Sans acompte, on travaille avant d'être payé, et un mois d'arrêt efface tout. |

**Mon avis : B, avec un plancher.** L'acompte 50/50 de la règle 43 n'est pas un problème de prix, c'est
une protection : il oblige le client à s'engager avant qu'on construise. Le mensuel s'ajoute **par-dessus**,
il ne remplace pas. Mais **je ne touche pas à la règle 43 sans ton accord explicite** — c'est ta grille,
et elle a tenu 5 jours sans un seul rabais.

**Ce que je n'adopte pas de la vidéo, quoi qu'il arrive :** 500 $/mois. Ici, un labo qui paie 25 000 FCFA/mois
paie déjà l'équivalent d'un quart de son site chaque trimestre. Le bon chiffre se mesure sur le premier client,
pas sur une vidéo américaine.

---

## 2 · La partie technique, elle, ne demande pas ton accord pour être vraie

| Palier | Quoi | Coût | Délai | Verdict |
|---|---|---|---|---|
| **Tier 0** | Voix par-dessus l'assistant scripté qu'on a **déjà** (OraCare v1/v3) — Chrome lit la réponse, écoute la question, renvoie vers WhatsApp si elle ne sait pas | **0 FCFA**, aucune clé, aucun serveur, reste un fichier unique | ~1 h par site | **Faisable aujourd'hui** |
| **Tier 1** | Vraie IA (clé API + fonction serverless) | quelques centimes par conversation + une clé | 1 journée | Seulement quand un client paie |
| **Tier 2** | Plateforme d'agent vocal (Retell/Vapi/ElevenLabs/GoHighLevel) | 97–297 $/mois, carte étrangère | — | **Parqué** |

**La limite honnête :** la reconnaissance vocale du navigateur ne fonctionne **que sur Chrome/Edge** —
**jamais sur Firefox**, partiellement sur iPhone. Et **personne ne peut dire** si elle comprend un accent
cam erounais sans l'essayer sur un vrai téléphone. **Ça se teste en 5 minutes :** un fichier, un lien,
le téléphone de King, la phrase « est-ce que je dois être à jeun ? ». Tant que ce test n'existe pas,
on ne promet rien à personne.

---

## 3 · Ce qu'on prend de la vidéo même si la voix ne se fait jamais

**Le ciblage par la publicité.** La vidéo cherche les prospects qui **paient déjà pour du trafic**
(Google Ads Transparency Center, Facebook Ads Library). Notre sourçage actuel = présence dans un annuaire
+ clics WhatsApp mesurés. **Un patron qui paie déjà pour être vu est strictement plus chaud que celui qui
est seulement listé** — il a déjà admis que l'acquisition se paie. C'est gratuit, public, et on ne l'a
jamais utilisé. **C'est la tactique la plus rentable de cette vidéo, et elle ne dépend d'aucune décision.**

**Le face-à-face plutôt que l'argument.** « Run it side by side » : on ne discute pas, on montre.
On construit déjà le concept gratuitement avant le oui. Il manque la moitié qui transforme un cadeau en
démonstration : **mesurer avant/après** (clics WhatsApp, appels) et le montrer.

---

## 4 · Ce que je demande à King — deux décisions

1. **Le prototype Tier 0 :** je construis un fichier de test (UNI-LABO, le plus utile : la préparation
   des analyses) que tu ouvres sur ton téléphone → tu parles → tu entends la réponse → ça finit sur WhatsApp.
   ~1 h, 0 FCFA, aucun risque, et ça répond une fois pour toutes à « est-ce que ça comprend un accent camerounais ».
2. **Le modèle d'offre :** A / B / C ci-dessus. Tant que tu ne tranches pas, **la règle 43 reste intacte** —
   100 000 FCFA, 50/50, jamais de rabais, et je ne facture rien au mois.

**Tant que ces deux réponses ne sont pas là : rien ne change dans le pipeline.** Aucun prospect n'entend
parler de voix ni de mensuel.
