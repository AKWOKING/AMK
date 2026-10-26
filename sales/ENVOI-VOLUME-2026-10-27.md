# ENVOI — LE LOT VOLUME (27 et 28 octobre 2026) · 30 messages

```text
PORTE    python3 tools/qa/audit_outreach.py sales/ENVOI-VOLUME-2026-10-27.md --strict
         → 0 bloquant, 0 avertissement sur 30 messages.
SOURCE   tools/outreach/compose.py batch --limit 40 --deja ENVOI-VAGUE-2 --ecarter VERIF-2026-10-27
         → 30 messages écrits, **16 lignes écartées** : numéro mort ou cabinet ayant déjà un site.
ORDRE    les sept cabinets à 3/3 sont SORTIS de ce lot : ils ont leur fichier, écrit à la main
         (sales/ENVOI-VAGUE-2-2026-10-26.md). Ici, le reste.
```

## Ce que ce lot est

**30 messages, dont 14 à 2/3 et 16 à 1/3** — mesuré, numéro par numéro, contre `leads/VERIF-2026-10-27.md`.

**16 lignes ont été écartées avant d'écrire**, et c'est la seule chose qui compte dans cette phrase :
`--ecarter` a retiré les numéros que King a vus **morts** le 25/10, et les cabinets qui ont **déjà un site
dédié** (Cristalys, LyfyOptic, Royal Optic, Win Optic Plus, Biolex, Biomedicam…). Écrire à ceux-là aurait
été une faute : on ne dit pas « il vous manque une page » à quelqu'un qui en a une (§8c).

**Ce qu'ils disent** : le nom de l'établissement, son quartier, et l'offre du lien d'une page qui **existe
déjà** dans le métier du destinataire — `dmoptiquesarl.com` pour un opticien, la clinique de Bonabéri,
MITOC pour une école, Labiomed pour un laboratoire. Rien sur le prospect : ni « vous n'avez pas de site »,
ni « votre fiche est vide ».

**Ce qu'ils ne sont pas** : du sur-mesure. C'est le palier 2 de la recherche — nom, quartier, métier —
mesuré à 4,4 % de réponses contre 11,2 % pour une ligne vraiment recherchée (`ops/BRAINSTORM-VOLUME` §8).

## La porte A se ferme au moment de l'envoi

| Verdict du vérificateur | Combien | Ce que ça veut dire pour King |
|---|---|---|
| **3/3 → envoi direct** | **0** | les sept 3/3 sont dans `sales/ENVOI-VAGUE-2-2026-10-26.md` |
| **2/3 → King tranche** | **14** | profil Business vu + titulaire nommé ; **la preuve numérique manque** |
| **1/3 → aucune porte franchie** | **16** | numéro jamais ouvert sur WhatsApp |
| numéro mort ou site existant | **0** | écartés à l'écriture, pas à l'envoi |

**Ce fichier est une file d'attente de vérification, pas un lot d'envoi.** Ce qui le transforme en lot,
c'est le geste de King : ouvrir chaque numéro, huit secondes, barrer ce qui n'est pas un cabinet. Les 14
à 2/3 n'ont besoin que d'une date (`sales/SWEEP-PORTE-B-2026-10-27.md`) ; les 16 à 1/3 ont besoin des
trois choses, et c'est le même geste qui les donne.

**Pourquoi on les écrit d'avance** : le message ne dépend pas de ce que la vérification trouvera — il ne
dit rien du prospect. Écrire d'avance ne coûte que du temps machine ; vérifier d'abord coûterait un jour.

## Ce que King fait, dans cet ordre

1. **Vérifier le numéro** sur WhatsApp (8 s) ; barrer les morts plutôt que les composer.
2. **Envoyer dans l'ordre du fichier** — les portes déjà franchies sont devant.
3. **Répondre dans l'heure** à qui répond.
4. **Cocher le tracker** le soir (`sales/CAMPAGNE-VOLUME-2026-10-26.md` §5).

## Les messages

## Jour 1 — mardi 27/10 · 13 messages

**#1 Optique Pro — Douala — 690034818**
> Bonjour, à Douala votre compte s'appelle « Laury Ntemtsa ».
> Les tableaux de l'Ordre portent « Optique Pro ».
> Ce n'est pas votre faute : deux noms, deux recherches.
> Dites-moi en un mot : lequel vos patients prononcent ?

**#2 Africa Optic — Douala — 691280237**
> Bonjour, Africa Optic à Douala : deux lignes, et je vous laisse juge.
> Et la page d'un opticien existe, avec ce qu'on vient chercher.
> Le lien part quand vous voulez, sans condition.
> Vous me dites un mot : je partage le lien ?

**#3 Alpha Optic — Douala — 699573457**
> Bonjour, Alpha Optic : à Douala, j'ai quelque chose à montrer.
> J'ai fait la page d'un opticien d'ici, en ligne et publique.
> Le lien part quand vous voulez, sans condition.
> Répondez par un mot : je vous le transmets ?

**#4 Caprice Optique — Douala — 675061623**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> J'ai fait la page d'un opticien d'ici, en ligne et publique.
> Vous l'ouvrez, et vous jugez vous-même.
> Un mot, un seul : vous voulez voir ?

**#5 Class-Optic — Douala — 691171817**
> Bonjour, à Douala je passais par votre nom ce matin, Class-Optic.
> Et la page d'un opticien existe, avec ce qu'on vient chercher.
> Vous l'ouvrez, et vous jugez vous-même.
> Dites-moi en un mot : je vous l'envoie ?

**#6 Dumbu Lunetterie — Douala — 690114323**
> Bonjour, Dumbu Lunetterie à Douala : deux lignes, et je vous laisse juge.
> J'ai fait la page d'un opticien d'ici, en ligne et publique.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#7 Emeraude Optique Sarl — Douala — 699909960**
> Bonjour, à Douala vous êtes Emeraude Optique Sarl.
> J'ai fait la page d'un opticien d'ici, en ligne et publique.
> Je peux vous envoyer le lien, sans rien préparer.
> Dites-moi en un mot : je vous l'envoie ?

**#8 Espace Vision — Douala — 677339424**
> Bonjour, à Douala vous êtes Espace Vision.
> Une page d'un opticien tourne déjà, du même genre.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Répondez par un mot : je vous le transmets ?

**#9 Express Optic — Douala — 675776125**
> Bonjour, à Douala je vois Express Optic dans l'annuaire.
> Une page d'un opticien tourne déjà, du même genre.
> Le lien part quand vous voulez, sans condition.
> Un mot, un seul : vous voulez voir ?

**#10 Gift Optical — Douala — 673521735**
> Bonjour, Gift Optical : à Douala, j'ai quelque chose à montrer.
> Une page d'un opticien tourne déjà, du même genre.
> Vous l'ouvrez, et vous jugez vous-même.
> Un mot : je vous montre le lien ?

**#11 Gilles-André Vision — Douala — 699883178**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> Une page d'un opticien tourne déjà, du même genre.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#12 Grâce Vision — Douala — 691392878**
> Bonjour, à Douala votre nom est Grâce Vision, je crois.
> Une page d'un opticien tourne déjà, du même genre.
> Cinq minutes sur votre téléphone, et vous verrez.
> Vous me dites un mot : je partage le lien ?

**#13 Jucia Optics — Akwa — 653449349**
> Bonjour, Jucia Optics à Akwa : deux lignes, et je vous laisse juge.
> Une page d'un opticien tourne déjà, du même genre.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Dites-moi en un mot : je vous l'envoie ?

## Jour 2 — mercredi 28/10 · 17 messages

**#14 L'Opticien SARL — Douala — 694336582**
> Bonjour, à Douala je passais par votre nom ce matin, L'Opticien SARL.
> Une page d'un opticien tourne déjà, du même genre.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot suffit : vous voulez que je l'envoie ?

**#15 La Fierté de l'Optique — Douala — 695179057**
> Bonjour, à Douala vous êtes La Fierté de l'Optique.
> Cette page d'un opticien existe : elle est en ligne.
> Le lien part quand vous voulez, sans condition.
> Un mot : je vous montre le lien ?

**#16 La Lunetterie Médicale El Shadai — Douala — 696896411**
> Bonjour, à Douala je vois La Lunetterie Médicale El Shadai dans l'annuaire.
> Cette page d'un opticien existe : elle est en ligne.
> Vous l'ouvrez, et vous jugez vous-même.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#17 Le Samaritain Optique — Douala — 670197451**
> Bonjour, à Douala vous êtes Le Samaritain Optique.
> Une page d'un opticien est en ligne, montrable en cinq minutes.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot, un seul : vous voulez voir ?

**#18 Light Optique — Douala — 677648790**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> Cette page d'un opticien existe : elle est en ligne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi en un mot : je vous l'envoie ?

**#19 London Vision — Douala — 696768116**
> Bonjour, à Douala je vois London Vision dans l'annuaire.
> Une page d'un opticien est en ligne, montrable en cinq minutes.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Un mot : je vous montre le lien ?

**#20 Lux Optique — Douala — 655040549**
> Bonjour, Lux Optique à Douala : deux lignes, et je vous laisse juge.
> Cette page d'un opticien existe : elle est en ligne.
> Je peux vous envoyer le lien, sans rien préparer.
> Répondez par un mot : je vous le transmets ?


**#21 Maison Optique — Douala — 657737045**
> Bonjour, Maison Optique : à Douala, j'ai quelque chose à montrer.
> Cette page d'un opticien existe : elle est en ligne.
> Je vous le transmets, vous comparez avec la vôtre.
> Vous me dites un mot : je partage le lien ?

**#22 Maranatha Optics — Douala — 658163190**
> Bonjour, à Douala vous êtes Maranatha Optics.
> Voilà la page d'un opticien, prête, avec les horaires.
> Vous l'ouvrez, et vous jugez vous-même.
> Vous me dites un mot : je partage le lien ?

**#23 Mel's Optic — Douala — 690988518**
> Bonjour, à Douala je vois Mel's Optic dans l'annuaire.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi en un mot : je vous l'envoie ?

**#24 Mouscou Optique Médicale — Douala — 696654164**
> Bonjour, Mouscou Optique Médicale : à Douala, j'ai quelque chose à montrer.
> Voilà la page d'un opticien, prête, avec les horaires.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot suffit : vous voulez que je l'envoie ?

**#25 OMB Optique — Douala — 699770234**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Répondez par un mot : je vous le transmets ?

**#26 Optic Laser Médical — Douala — 677827434**
> Bonjour, à Douala votre nom est Optic Laser Médical, je crois.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot, un seul : vous voulez voir ?

**#27 OpticPlus — Douala — 699379150**
> Bonjour, OpticPlus à Douala : deux lignes, et je vous laisse juge.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot : je vous montre le lien ?

**#28 Pagrot Optique — Douala — 699904691**
> Bonjour, à Douala je passais par votre nom ce matin, Pagrot Optique.
> Voilà la page d'un opticien, prête, avec les horaires.
> Le lien part quand vous voulez, sans condition.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#29 Saoudia Optique — Douala — 696040413**
> Bonjour, à Douala vous êtes Saoudia Optique.
> Et la page d'un opticien existe, avec ce qu'on vient chercher.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot suffit : vous voulez que je l'envoie ?

**#30 World Vision — Douala — 656032172**
> Bonjour, à Douala je vois World Vision dans l'annuaire.
> Et la page d'un opticien existe, avec ce qu'on vient chercher.
> Cinq minutes sur votre téléphone, et vous verrez.
> Répondez par un mot : je vous le transmets ?
