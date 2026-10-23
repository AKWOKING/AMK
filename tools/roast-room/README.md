# roast-room — le conseil d'administration qui débat (installé le 23/10/2026, demande King)

Amont : <https://github.com/nateherkai/roast-room> · **licence à vérifier** (`NOASSERTION` : le fichier
LICENSE amont n'est pas une licence SPDX reconnue) · épinglé
`e40f40652d5690c4d9f928c4794c673a99f2cd0e` (22/10/2026) · 1 004 ★.

## Ce que c'est

Sept (puis douze) conseillers construits sur les écrits **publics** de Bezos, Paul Graham, Hormozi,
Gary Vee, Dan Martell, Gino Wickman, Buffett, Naval, Codie Sanchez, Leila Hormozi, Sara Blakely… Ils
débattent une décision dans Claude Code, avec un verdict noté et un PDF. Une petite app locale
(`app/server.mjs`, Node ≥ 20) montre la table. `/newroaster <nom>` fabrique un siège de plus.

## Ce qui est installé

Le skill `roast-room` et les agents `council-*.md` dans `~/.claude`, miroir `~/.agents/skills`. Le
clone reste dans `~/.roast-room` pour le lanceur. **Aucune dépendance npm** (le `package.json` n'en
déclare aucune), `node --check app/server.mjs` passe. L'app n'est **pas** démarrée par l'installeur.

## Le point de licence, dit franchement

`NOASSERTION` signifie que GitHub n'a pas reconnu la licence. Le fichier existe (1 220 octets) mais il
faut le lire avant tout usage qui sorte de la maison. **Décision par défaut prise ici : usage interne
AMK uniquement, aucune redistribution, aucun livrable client qui en dépende.** Si King veut s'en servir
en production, lire `LICENSE` d'abord (5 minutes).

## Ce que ça apporte à AMK

Un **second avis structuré** sur les décisions qui coûtent cher : prix, positionnement, niche, embauche.
Ce n'est pas un oracle : c'est un rituel qui force à écrire la question et à entendre un désaccord.
L'usage le plus juste chez nous : trancher une question de positionnement (école vs clinique, forfait
vs projet) avant une réunion, jamais pour remplacer le ruling de King.

## Limites

Nécessite Claude Code et une clé Anthropic (absente ici). Le verdict est généré : **aucun chiffre qui
en sort n'est une donnée** — il ne se cite pas dans un livrable client.

Réinstallation : `bash tools/roast-room/install.sh`.

## ⚠️ L'installation ne survit pas à la session (constaté le 23/10, 06:40)

Entre deux tours, `~/.roast-room`, `~/.claude/skills/roast-room` et les douze agents **avaient
disparu** : seuls `tools/roast-room/README.md` et `install.sh` (dans le dépôt) avaient survécu. Le
clone et les skills vivent hors de ce qui est versionné.

**Donc, au début de toute session où l'on veut s'en servir** :

```bash
bash tools/roast-room/install.sh     # ~1 s, idempotent, épinglé e40f406
```

Vérifié le 23/10 après relance : clone présent, `SKILL.md` présent, 12 agents (`council-bezos.md` …),
`node --check app/server.mjs` passe. Si la commande échoue, c'est le réseau GitHub, pas le dépôt.
