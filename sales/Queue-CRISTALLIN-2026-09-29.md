# LE CRISTALLIN — **le message de santé du lundi 29/09**, à envoyer par King

**Écrit le 24/09/2026 (lot [33])** · **rien ne part sans King** (`prep/queue only`).

---

## 0 · Ce qui s'est passé aujourd'hui, en deux lignes

Lundi 24/09, **10:10** : *« Bonjour je vais te revenir »*. **10:11** : *« Je suis malade »*. **10:13**, King
a répondu — et la réponse est la bonne, mot pour mot :

> « Bonjour Monsieur Messoua, Navré d'apprendre cela. Je vous souhaite un prompt rétablissement ! Prenez
> tout le temps de vous reposer, la santé passe avant tout. Le projet attendra votre retour en forme. Bon
> courage et à très bientôt ! »

**Aucune question, aucun prix, aucune date.** C'est exactement ce qu'il fallait : la balle est chez lui, et
le projet n'a pas besoin d'être rappelé à quelqu'un qui est au lit.

---

## 1 · La décision, écrite pour ne pas être réinventée dans trois jours

**On ne relance pas un malade.** Le prochain message — un seul — part **lundi 29/09**, et il parle de sa
santé **avant** le projet. Il ne repose pas le prix (il est posé depuis le 23/09 et n'a été ni accepté ni
refusé), il ne demande pas de nouvelles du site, et il n'ajoute aucune échéance.

**Et si lundi il ne répond pas ?** On ne relance pas non plus : on attend son retour. La seule exception —
dans deux semaines, le 8/10 — serait un message court du même genre, santé d'abord, sans un mot du projet.
Au-delà, on ne fait plus rien : un client qui a un devis en main, un aperçu en ligne et une raison humaine
de ne pas répondre **n'a pas besoin qu'on lui rappelle qu'on existe**.

**Ce qui ne bouge pas d'ici là :**

- **la page ne se touche pas** — `lecristallin-concept.vercel.app` reste telle quelle (gel de King : « on
  ne touche plus rien jusqu'à ce que les prospects deviennent des clients payants ») ; son *« ne change
  encore rien sans mon ok »* du 22/09 tient toujours, et il est malade : ce serait le pire moment pour
  changer quelque chose ;
- **le prix ne bouge pas** : 150 000 FCFA, 50/50, acompte 75 000, jamais de remise ;
- **aucune compensation ne se met en route** : les trois du §4 de `REVUE-CONTRATS-GRILLE-2026-09-23.md`
  (WhatsApp Business configuré, domaine 2027, fiche Google) s'appliquent **à la livraison payée**, pas
  avant — et elles ne se mentionnent pas dans un message de santé ;
- **l'abonnement** ne se propose qu'à la livraison payée (règle du 23/09).

---

## 2 · Le message de lundi 29/09 — la version à envoyer

> Bonjour Monsieur Messoua,
>
> J'espère que vous allez mieux et que le repos fait son effet.
>
> Aucune urgence de mon côté : tout est en ordre et rien ne presse. Reposez-vous bien, on reparlera du
> projet quand vous serez d'aplomb — et s'il y a quoi que ce soit de plus simple pour vous, dites-le-moi.
>
> Bon rétablissement, à bientôt.

**Pourquoi cette version et pas une autre :**

| Choix | Raison |
|---|---|
| **Pas de prix, pas de « où en est-on »** | il est malade : la seule information utile pour lui, c'est qu'on ne lui court pas après |
| **« tout est en ordre »** | c'est vrai (l'aperçu est en ligne, rien n'est cassé) et ça le rassure sans rien demander |
| **« dites-le-moi »** | laisse une porte s'il veut, lui, accélérer — la balle reste chez lui |
| **Pas de « je vous rappelle la semaine prochaine »** | c'est une promesse de relance déguisée : s'il va mieux, il écrira. C'est lui qui a dit « je vais te revenir » |

**Ce qu'on n'envoie pas :** ni le lien de l'aperçu (il l'a), ni la grille, ni « le site est prêt à partir en
ligne », ni un point d'étape. Un message = une intention.

---

## 3 · S'il répond « ça va mieux, on avance »

C'est le scénario normal, et il est déjà préparé : le prix est posé (150 000, 50/50), le contrat Standard
est prêt, et les trois compensations remplacent les deux promesses sans objet de son message du 23/09
(« hébergement 1 an » alors que son domaine LWS court jusqu'au 13/06/2027 et que son hébergement existe).
La feuille de route est dans `REVUE-CONTRATS-GRILLE-2026-09-23.md` §4 et §6.

**Dans ce cas, la première chose à dire n'est pas le prix** — c'est : *« tout est prêt, on part quand vous
voulez, 3 à 5 jours après l'acompte. »*

---

## 4 · S'il demande une remise (parce qu'il est malade, parce que c'est dur, parce que…)

La réponse est la même qu'avant, et elle est écrite d'avance : **on ne remise pas, on ajuste le périmètre.**
Si le budget de démarrage est le problème, l'option honnête est **la moitié du périmètre** (par exemple la
page sans la refonte de la fiche Google et sans la configuration WhatsApp Business, ou un démarrage à
75 000 avec la suite plus tard) — **jamais 150 000 → 120 000**. La différence est tout sauf cosmétique : une
remise faite à un client malade se retrouve dans le fil du client suivant.

---

## 5 · Le suivi, dans le dépôt

L'échange d'aujourd'hui et la décision sont **dans le générateur** (`leads/build/crm.py`, bloc `FIL_2409`) :
`stage=closing` inchangé, `Follow-up date = 2026-09-29`, le verbatim des trois messages, et le renvoi vers
ce document. Le CRM a été reconstruit et reverrouillé — une prochaine exécution de `rebuild.sh` ne peut plus
effacer la date.
