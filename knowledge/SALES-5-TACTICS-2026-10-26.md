# LES CINQ TACTIQUES DE VENTE — ce qui tient dans 25 secondes, ce qui n'y tient pas

```
Statut    doctrine de levier, opposable (portes : tools/qa/audit_story.py, audit_hook.py)
Source    King, 26/10/2026 — texte transmis : 5 tactiques tirées de Cialdini (Influence), Kahneman
          (Thinking, Fast and Slow), Iannarino (The Lost Art of Closing), Berger (Contagious) et
          Keenan (Gap Selling). Aucune URL, aucune page, aucun chiffre fourni : les livres sont
          nommés, pas cités. **Tier C** — on retient les mécanismes, jamais une statistique.
Étend     sales/AMK-Sales-Playbook-v2.md PART B (Erhart, 10 tactiques — le même terrain, autre école)
Relie     sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md (le chemin de conversion, §4)
          sales/MESSAGES-2026-09-23-PERSUASION.md §8 (les trois phrases plates)
          content/reels/ep01/ (EP01 v6 — la première pièce qui en applique trois)
Écrit     26/10/2026, tour 151
```

---

## 1 · Les cinq, telles que la source les pose

| # | Tactique | Le mécanisme, en une phrase | L'exemple de la source |
|---|---|---|---|
| 1 | **Réciprocité** — « The Unfair Favor » | donner d'abord, sans rien attendre, crée une dette psychologique | un rapport de marché gratuit avant de demander du temps |
| 2 | **Rareté** — « The Closing Window » | la peur de perdre pèse plus que l'envie de gagner | « ces tarifs jusqu'à la prochaine revue », pas « achetez » |
| 3 | **Cohérence** — « Micro Commitment » | trois ou quatre petits oui rendent le grand oui logique | de petits accords sur des points sans enjeu |
| 4 | **Preuve sociale** — « Neighborhood Consensus » | on choisit ce que nos pairs ont déjà validé | « la plupart des familles de ce quartier prennent cette option » |
| 5 | **Autorité** — « Expert Frame » | on ne vend plus, on conseille | « il n'y a que deux options qui tiennent pour vous ; reste à choisir » |

**Ce que les cinq ont en commun** : aucune ne demande de *convaincre*. Elles changent ce que le client
croit savoir sur la situation. C'est pour ça qu'elles voyagent mal en 25 secondes : une vidéo courte ne
peut pas installer une dette, un quartier ou une autorité — elle peut seulement **montrer un fait que le
client n'avait pas** et **rendre le premier pas déraisonnablement petit**.

## 2 · Le crible : format court, tiers froid, aucun suivi

Trois contraintes décident, et elles viennent du dépôt, pas de moi :

| Contrainte | La règle | Ce qu'elle élimine |
|---|---|---|
| **25 s, 50 mots** | `audit_reel` (plafond 25 s) + débit mesuré à ~0,45 s/mot | toute tactique qui demande du temps de mise en place |
| **Premier contact** | la grille 331 case 3 = TOFU ; le spectateur ne nous connaît pas | la rareté et l'autorité **revendiquées** (on n'est personne pour lui, encore) |
| **Zéro peur, zéro promesse** | ruling 25/10, codé dans `audit_hook` (lexique `PEUR`, `PROMESSE`) | la rareté artificielle, l'urgence, la garantie de résultat |

## 3 · Le verdict, tactique par tactique

### ① Réciprocité — **OUI, et c'est la plus forte**
Le dépôt la pratiquait déjà sans la nommer : « dix minutes, gratuit » (v5). Le défaut n'était pas la
tactique, c'était **le cadeau flou** : dix minutes *de quoi* ? Corrigé en v6 : « Les horaires, ça se
change en dix minutes. Sans moi. » — un cadeau **utilisable sans nous**, vérifiable, et qui coûte
réellement quelque chose à donner (on renonce à le facturer).
**Où ça vit** : beat 3 (≈ 9,5 s), jamais après 70 % de la pièce (avertissement `cadeau-tardif`).

### ② Rareté — **NON dans cette pièce, OUI plus tard, et seulement si elle est vraie**
La source dit « jusqu'à la prochaine revue ». Chez nous, la seule rareté **vraie** est la capacité :
un opérateur, deux aperçus par semaine (`PLAYBOOK` §3, ligne B5 : « Deux places »).
Mais sur un **premier contact**, la rareté se lit comme une pression et **grille le crédit** qu'on est en
train d'acheter avec la réciprocité. Ruling : **interdite en TOFU**, autorisée en **BOFU** (B5, 07/11),
à une condition : le chiffre doit être la capacité réelle de la semaine, décidée par King, jamais un
chiffre de théâtre. `audit_story` refusera `urgence` si la formulation glisse vers la peur.
**Effet secondaire mesurable** : elle donne aussi une raison de répondre maintenant, ce qui manque à
tout notre tunnel.

### ③ Cohérence (micro-engagement) — **OUI, mais pas comme en v4**
La v4 ouvrait sur « **Tapez** votre nom » : c'est un ordre, et un ordre n'est pas un micro-accord — il
demande au spectateur de obéir à un inconnu avant de lui avoir donné quoi que ce soit. Ce que la
tactique demande vraiment, c'est une **suite** de oui faciles. Notre échelle en compte quatre, et
**trois ne sont pas dans la vidéo** :

| Marche | Le oui demandé | Où |
|---|---|---|
| 1 | « oui, ça m'arrive de taper un nom sur Google » (mental, déclenché par la scène) | beat 1 |
| 2 | « oui, sa fiche a plus que la mienne » (constat, non menaçant) | beat 2 |
| 3 | « oui, les horaires je peux les changer » (capacité reconnue) | beat 3 |
| 4 | « ok, j'écris **un mot** » | CTA |

Écrire un mot n'est pas acheter : c'est le plus petit engagement possible, et c'est **pour ça** qu'il
marche. Le message d'accueil prend le relais avec deux questions (`PLAYBOOK` §4.2) — deux micro-accords
de plus, avant tout prix.

### ④ Preuve sociale — **PARTIELLE, et c'est celle qui coûte le plus cher à dire vrai**
Trois preuves possibles, et deux sont interdites :

| Preuve | Utilisable ? | Pourquoi |
|---|---|---|
| **Les douze avis de la fiche concurrente** | ✅ oui — c'est la capture datée du 24/10 | elle prouve que **les patients notent**, pas que nos clients sont contents |
| **DM Optique comme client** | ⛔ pas sans accord écrit pour un reel public | `clients/` n'est pas un argument de vente sans permission |
| « la plupart des opticiens de Douala… » | ⛔ **jamais** | aucune mesure ; ce serait un chiffre inventé (ruling 140) |

Donc en v6 : la preuve sociale reste **le fait des douze avis**, et elle est **prononcée** (elle était
muette en v4). La forme « consensus de quartier » de la source attend qu'on ait trois clients — pas un.

### ⑤ Autorité (expert frame) — **OUI, sous la forme du diagnostic, jamais du titre**
On ne peut pas dire « je suis l'expert » : on est inconnu, et le dépôt interdit de revendiquer ce qu'on
ne peut pas prouver (`RULE-CREDENTIAL-CLAIMS`). Mais l'autorité **se montre** par le diagnostic : nommer
le mécanisme que le client n'avait pas vu, puis **restreindre le choix**.
La source dit : « il n'y a que deux options qui tiennent pour vous ». Notre version en 25 s tient en une
phrase de mécanisme : « Une page avec vos horaires répond à votre place » — le diagnostic **est** l'avis
d'expert. La restriction du choix, elle, appartient à la conversation (deux options, jamais cinq), pas à
un reel de 25 s.

## 4 · Ce que Kahneman, Berger, Iannarino et Keenan ajoutent (et qu'on garde)

| Auteur | Le point qui change quelque chose chez nous | Où il atterrit |
|---|---|---|
| **Kahneman** | le Système 1 traite le concret, pas les nombres abstraits ; une perte pèse plus qu'un gain, **mais** la peur est exclue par ruling | on remplace le chiffre abstrait par une scène (« le soir, il veut venir, personne ne répond »), et la perte reste **factuelle** |
| **Berger** | valeur pratique + déclencheur : un contenu se partage quand il sert dans une situation précise | le déclencheur est « quand un patient tape ton nom », et le cadeau est actionnable en 10 minutes |
| **Iannarino** | on ne clôt pas une vente en 25 s, on obtient un **engagement** ; chaque engagement prépare le suivant | le CTA demande un mot, pas un achat ; le message d'accueil demande deux faits, pas un rendez-vous |
| **Keenan** | vendre l'écart entre l'état actuel et l'état futur, chiffré quand c'est possible | l'écart est montré deux fois : **douze avis vs un nom** (état actuel) et **personne ne répond le soir** (état futur) |

## 5 · Ce que la pièce ne fait pas, et qu'il faut dire

- **Aucun taux de conversion n'est mesuré.** Le dépôt n'a ni vue, ni clic, ni message compté pour EP01.
  Le Roast Room note un **potentiel** sur une grille (`knowledge/ROAST-2026-10-26-EP01-VENTE.md`), pas
  un pourcentage. Tout chiffre de conversion publié ce tour serait inventé.
- **La rareté n'est pas utilisée** dans cette pièce, volontairement, et elle reste disponible pour la
  pièce BOFU du 07/11 — à la condition d'être la capacité réelle.
- **La preuve sociale est faible** : un fait de fiche concurrente, zéro témoignage client. C'est l'état
  du dépôt, pas un choix esthétique.

## 6 · Provenance, et ce qu'on ne peut pas vérifier

King a transmis **le résumé** de cinq ouvrages, pas les ouvrages. Les cinq livres existent et les
mécanismes sont connus ; **aucune citation n'est vérifiée ici**, et **aucun chiffre** n'a été transmis.
On cite donc les livres comme **origine du mécanisme**, jamais comme preuve d'une affirmation. C'est la
règle du dépôt depuis le 24/10 : une source de seconde main se déclare.
