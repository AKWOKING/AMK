# ENVOI — LE LOT VOLUME (28 et 29 octobre 2026) · 30 messages

```text
PORTE    python3 tools/qa/audit_outreach.py sales/ENVOI-VOLUME-2026-10-27.md --strict
         → 0 bloquant, 0 avertissement sur 30 messages.
SOURCE   tools/outreach/compose.py batch --limit 30 --deja ENVOI-VAGUE-2 ENVOI-VAGUE-3
         (le lot du matin — 49 messages sur les mêmes lignes — a été refait : il contenait des
          villes qui étaient des noms de personnes, et neuf cabinets qui n'ont pas la porte B)
ORDRE    deux passes : les opticiens d'abord (28 % de réponses mesurées), le reste ensuite.
```

## Ce que ce lot est

**30 messages, écrits par la fabrique, jugés par la porte.** Chaque message nomme l'établissement, son
quartier, et offre une page qui **existe** dans son métier : `dmoptiquesarl.com` pour un opticien,
`hosting/samples/clinic-bonaberi.html` pour une clinique, `hosting/samples/mitoc.html` pour une école,
`hosting/previews/labiomed/` pour un laboratoire. Aucun ne dit « vous n'avez pas de site » : nous ne
l'avons pas vérifié (§8c).

**Ce qu'ils ne sont pas** : du sur-mesure. C'est le palier 2 de la recherche — nom, quartier, métier —
mesuré à 4,4 % de réponses, contre 11,2 % pour une ligne vraiment recherchée. À 40 messages par jour,
ce palier produit plus de réponses que dix messages parfaits ; c'est le calcul qui autorise la cadence,
et il est écrit dans `ops/BRAINSTORM-VOLUME-2026-10-26.md` §1.

## Ce que ce lot n'est pas : un lot d'envoi

**Aucune de ces trente lignes n'a été ouverte sur WhatsApp par King.** Le geste de huit secondes reste
obligatoire avant chaque envoi : ouvrir le profil, vérifier que le numéro vit et que c'est un cabinet.
Les cabinets qui échouent se **barrent** — pas de SMS, pas d'appel (ruling 25/10).

**Et le stock s'arrête là.** 52 lignes composables au total, 53 messages écrits avec la vague 2 : à
20 par jour, **deux jours et demi** puis plus rien. `supply.py plan` le dit avant l'envoi, et c'est le
vrai sujet de la semaine — pas la cadence.

## Les messages

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

**#6 Cristalys Optic — Douala — 690945150**
> Bonjour, Cristalys Optic à Douala : deux lignes, et je vous laisse juge.
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

**#12 L'Opticien SARL — Douala — 694336582**
> Bonjour, à Douala votre nom est L'Opticien SARL, je crois.
> Une page d'un opticien tourne déjà, du même genre.
> Cinq minutes sur votre téléphone, et vous verrez.
> Vous me dites un mot : je partage le lien ?

**#13 La Fierté de l'Optique — Douala — 695179057**
> Bonjour, La Fierté de l'Optique à Douala : deux lignes, et je vous laisse juge.
> Une page d'un opticien tourne déjà, du même genre.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Dites-moi en un mot : je vous l'envoie ?

**#14 La Lunetterie Médicale El Shadai — Douala — 696896411**
> Bonjour, à Douala je passais par votre nom ce matin, La Lunetterie Médicale El Shadai.
> Une page d'un opticien tourne déjà, du même genre.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot suffit : vous voulez que je l'envoie ?

**#15 Le Samaritain Optique — Douala — 670197451**
> Bonjour, à Douala vous êtes Le Samaritain Optique.
> Cette page d'un opticien existe : elle est en ligne.
> Le lien part quand vous voulez, sans condition.
> Un mot : je vous montre le lien ?

**#16 Light Optique — Douala — 677648790**
> Bonjour, à Douala je vois Light Optique dans l'annuaire.
> Cette page d'un opticien existe : elle est en ligne.
> Vous l'ouvrez, et vous jugez vous-même.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#17 London Vision — Douala — 696768116**
> Bonjour, à Douala vous êtes London Vision.
> Une page d'un opticien est en ligne, montrable en cinq minutes.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot, un seul : vous voulez voir ?

**#18 Lux Optique — Douala — 655040549**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> Cette page d'un opticien existe : elle est en ligne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi en un mot : je vous l'envoie ?

**#19 LyfyOptic — Douala — 699980666**
> Bonjour, à Douala je vois LyfyOptic dans l'annuaire.
> Une page d'un opticien est en ligne, montrable en cinq minutes.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Un mot : je vous montre le lien ?

**#20 Maranatha Optics — Douala — 658163190**
> Bonjour, Maranatha Optics à Douala : deux lignes, et je vous laisse juge.
> Cette page d'un opticien existe : elle est en ligne.
> Je peux vous envoyer le lien, sans rien préparer.
> Répondez par un mot : je vous le transmets ?

**#21 Mel's Optic — Douala — 690988518**
> Bonjour, Mel's Optic : à Douala, j'ai quelque chose à montrer.
> Cette page d'un opticien existe : elle est en ligne.
> Je vous le transmets, vous comparez avec la vôtre.
> Vous me dites un mot : je partage le lien ?

**#22 Mouscou Optique Médicale — Douala — 696654164**
> Bonjour, à Douala vous êtes Mouscou Optique Médicale.
> Voilà la page d'un opticien, prête, avec les horaires.
> Vous l'ouvrez, et vous jugez vous-même.
> Vous me dites un mot : je partage le lien ?

**#23 OMB Optique — Douala — 699770234**
> Bonjour, à Douala je vois OMB Optique dans l'annuaire.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi en un mot : je vous l'envoie ?

**#24 Optic Laser Médical — Douala — 677827434**
> Bonjour, Optic Laser Médical : à Douala, j'ai quelque chose à montrer.
> Voilà la page d'un opticien, prête, avec les horaires.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot suffit : vous voulez que je l'envoie ?

**#25 OpticPlus — Douala — 699379150**
> Bonjour, à Douala je travaille avec les opticiens d'ici.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous donne l'adresse, vous ouvrez quand vous voulez.
> Répondez par un mot : je vous le transmets ?

**#26 Pagrot Optique — Douala — 699904691**
> Bonjour, à Douala votre nom est Pagrot Optique, je crois.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot, un seul : vous voulez voir ?

**#27 Saoudia Optique — Douala — 696040413**
> Bonjour, Saoudia Optique à Douala : deux lignes, et je vous laisse juge.
> Voilà la page d'un opticien, prête, avec les horaires.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot : je vous montre le lien ?

**#28 Win Optic Plus — Douala — 699125906**
> Bonjour, à Douala je passais par votre nom ce matin, Win Optic Plus.
> Voilà la page d'un opticien, prête, avec les horaires.
> Le lien part quand vous voulez, sans condition.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#29 World Vision — Douala — 656032172**
> Bonjour, à Douala vous êtes World Vision.
> Et la page d'un opticien existe, avec ce qu'on vient chercher.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot suffit : vous voulez que je l'envoie ?

**#30 Blessed Group of Schools (BGS / Blessed Anglo-Saxon) — Simbock — 680139453**
> Bonjour, à Simbock je vois Blessed Group of Schools (BGS / Blessed Anglo-Saxon) dans l'annuaire.
> Et la page d'une école existe, avec ce qu'on vient chercher.
> Cinq minutes sur votre téléphone, et vous verrez.
> Répondez par un mot : je vous le transmets ?
