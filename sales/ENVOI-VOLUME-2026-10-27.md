# ENVOI — LA VAGUE VOLUME (27 et 28 octobre 2026)

```text
DÉCISION King, 26/10 : « we can't be sending just 1 message per day, we send between 20-50,
in cold messaging volume counts ». La règle du 1/jour (ruling 05/10) est donc révisée, pas oubliée :
ce qui la fondait — le texte identique répété — reste interdit, et la porte le vérifie désormais.
CADENCE  J1 mardi 27/10 : 20 messages · J2 mercredi 28/10 : 29. Le ⑦ de la vague 2 (Capelli) glisse au
         29/10 si King n'a pas envoyé les sept avant — jamais deux fois le même cabinet.
PORTE    python3 tools/qa/audit_outreach.py sales/ENVOI-VOLUME-2026-10-27.md --strict
         → 0 bloquant, 0 avertissement. 49 messages, aucun ne partage douze mots avec un autre.
```

## Ce que ce lot est, et ce qu'il n'est pas

**Ce qu'il est** : la première vague écrite par une fabrique (`tools/outreach/compose.py`), parce que
quarante-neuf messages à la main, c'est trois jours de travail pour un résultat qui se ressemble.

**Ce qu'il n'est pas** : personnalisé au fait près. Deux angles seulement, et ils disent la vérité :

| Angle | Ce qu'il affirme | Sa preuve | Combien ici |
|---|---|---|---|
| **le nom** | le profil WhatsApp ne porte pas le nom de l'établissement | capture du 25/10 (§8b porte A) | **2** |
| **l'offre** | une page existe déjà dans le métier du destinataire — opticien, clinique, école, laboratoire | `dmoptiquesarl.com` (client payant) · `hosting/samples/clinic-bonaberi.html` · `hosting/samples/mitoc.html` · `hosting/previews/labiomed/` | **47** |

L'angle « offre » ne dit **rien** sur le prospect : ni qu'il n'a pas de site, ni que sa fiche est vide.
Nous ne l'avons pas vérifié pour ces 47 lignes, et le §8c interdit de l'affirmer. La question finale
demande une action et rien d'autre.

## Ce que King fait, dans cet ordre

1. **Vérifier que le numéro joint WhatsApp** avant d'écrire — 8 secondes par ligne, 20 lignes ≈ 3 min.
   Un numéro mort ne se remplace pas par un SMS (ruling 25/10 : « pas sur WhatsApp = mort »).
2. **Envoyer dans l'ordre.** L'ordre du fichier est l'ordre d'envoi : opticiens d'abord.
3. **Répondre dans l'heure** à qui répond (§7 de `CLIENT-MESSAGING-RULES`).
4. **Cocher le tracker** (`sales/CAMPAGNE-VOLUME-2026-10-26.md` §5) : envoyé / lu / répondu.

## Les messages

> Généré par `tools/outreach/compose.py` depuis `leads/CRM.csv` (lecture seule).
> Chaque message ne dit que ce que sa ligne prouve. Porte : `audit_outreach.py --strict`.


## Jour 1

**#1 Optique Pro — Douala — 690 03 48 18**
> Bonjour, à Douala le nom sur votre profil est « Laury Ntemtsa » seul.
> Le tableau de l'Ordre dit « Optique Pro ».
> Deux noms, et ce n'est pas votre faute.
> Dites-moi, en un mot : lequel vos patients utilisent ?

**#2 Africa Optic — Douala — 691 28 02 37**
> Bonjour, à Douala vous êtes Africa Optic, et je passais par là.
> J'ai fait la page d'un opticien de Douala.
> Je peux vous envoyer le lien, sans rien préparer.
> Dites-moi en un mot : je vous l'envoie ?

**#3 Alpha Optic — Douala — 699 57 34 57**
> Bonjour, vous êtes Alpha Optic à Douala, si je ne me trompe.
> Cette page d'un opticien de Douala tourne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#4 Caprice Optique — Douala — 675 06 16 23**
> Bonjour, Caprice Optique : à Douala, j'ai quelque chose à vous montrer.
> Voilà la page d'un opticien de Douala, en ligne.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#5 Class-Optic — Douala — 691 17 18 17**
> Bonjour, Class-Optic : à Douala, deux minutes de votre temps suffisent.
> Et la page d'un opticien de Douala existe.
> Le lien part quand vous voulez, sans condition.
> Vous me dites un mot : je vous le partage ?

**#6 Cristalys Optic — Douala — 690 94 51 50**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> Cette page d'un opticien de Douala est ici.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Répondez par un mot : je vous le transmets ?

**#7 Dumbu Lunetterie — Douala — 690 11 43 23**
> Bonjour, Dumbu Lunetterie : à Douala, deux minutes de votre temps suffisent.
> J'ai fait la page d'un opticien de Douala.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#8 Emeraude Optique Sarl — Douala — 699 90 99 60**
> Bonjour, à Douala je vois Emeraude Optique Sarl dans l'annuaire des pros.
> Une page d'un opticien de Douala tourne aussi.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot : je vous montre le lien ?

**#9 Espace Vision — Douala — 677 33 94 24**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> C'est la page d'un cabinet de Douala, prête.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#10 Express Optic — Douala — 675 77 61 25**
> Bonjour, à Douala vous êtes Express Optic, et je passais par là.
> Voilà la page d'un opticien de Douala, en ligne.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Vous me dites un mot : je vous le partage ?

**#11 Gift Optical — Douala — 673 52 17 35**
> Bonjour, vous êtes Gift Optical à Douala, si je ne me trompe.
> Et la page d'un opticien de Douala existe.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot : je vous montre le lien ?

**#12 Gilles-André Vision — Douala — 699 88 31 78**
> Bonjour, à Douala, Gilles-André Vision — je passais par votre nom ce matin.
> Une page d'un cabinet de Douala tourne aussi.
> Cinq minutes sur votre téléphone, et vous verrez.
> Répondez par un mot : je vous le transmets ?

**#13 Grâce Vision — Douala — 691 39 28 78**
> Bonjour, vous êtes Grâce Vision à Douala, si je ne me trompe.
> J'ai fait la page d'un cabinet de Douala.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot, un seul : vous voulez voir ?

**#14 Jucia Optics — Akwa — 653 449 349**
> Bonjour, à Akwa, Jucia Optics — je passais par votre nom ce matin.
> Cette page d'un opticien de Douala tourne.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#15 L'Opticien SARL — Douala — 694 33 65 82**
> Bonjour, L'Opticien SARL : à Douala, j'ai quelque chose à vous montrer.
> C'est la page d'un opticien de Douala, prête.
> Cinq minutes sur votre téléphone, et vous verrez.
> Vous me dites un mot : je vous le partage ?

**#16 La Fierté de l'Optique — Douala — 695 17 90 57**
> Bonjour, à Douala je vois La Fierté de l'Optique dans l'annuaire des pros.
> Cette page d'un opticien de Douala tourne.
> Le lien part quand vous voulez, sans condition.
> Un mot, un seul : vous voulez voir ?

**#17 La Lunetterie Médicale El Shadai — Douala — 696 89 64 11**
> Bonjour, La Lunetterie Médicale El Shadai : à Douala, j'ai quelque chose à vous montrer.
> Cette page d'un opticien de Douala est ici.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Dites-moi en un mot : je vous l'envoie ?

**#18 Le Samaritain Optique — Douala — 670 19 74 51**
> Bonjour, Le Samaritain Optique : à Douala, deux minutes de votre temps suffisent.
> Voilà la page d'un opticien de Douala, en ligne.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot : je vous montre le lien ?

**#19 Light Optique — Douala — 677 64 87 90**
> Bonjour, à Douala je vois Light Optique dans l'annuaire des pros.
> Et la page d'un opticien de Douala existe.
> Je vous le transmets, vous comparez avec la vôtre.
> Répondez par un mot : je vous le transmets ?

**#20 London Vision — Douala — 696 76 81 16**
> Bonjour, à Douala vous êtes London Vision, et je passais par là.
> Cette page d'un cabinet de Douala est ici.
> Vous regardez tranquillement, quand vous avez le temps.
> Dites-moi juste un mot : je l'envoie ce soir ?


## Jour 2

**#21 Lux Optique — Douala — 655 04 05 49**
> Bonjour, à Douala je vois Lux Optique dans l'annuaire des pros.
> J'ai fait la page d'un opticien de Douala.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#22 LyfyOptic — Douala — 699 98 06 66**
> Bonjour, vous êtes LyfyOptic à Douala, si je ne me trompe.
> Voilà la page d'un opticien de Douala, en ligne.
> Vous regardez tranquillement, quand vous avez le temps.
> Répondez par un mot : je vous le transmets ?

**#23 Maison Optique — Douala — 657 73 70 45**
> Bonjour, à Douala vous êtes Maison Optique, et je passais par là.
> C'est la page d'un opticien de Douala, prête.
> Le lien part quand vous voulez, sans condition.
> Un mot : je vous montre le lien ?

**#24 Maranatha Optics — Douala — 658 16 31 90**
> Bonjour, à Douala, Maranatha Optics — je passais par votre nom ce matin.
> Et la page d'un opticien de Douala existe.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Dites-moi en un mot : je vous l'envoie ?

**#25 Mel's Optic — Douala — 690 98 85 18**
> Bonjour, Mel's Optic : à Douala, j'ai quelque chose à vous montrer.
> Une page d'un opticien de Douala tourne aussi.
> Je peux vous envoyer le lien, sans rien préparer.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#26 Mouscou Optique Médicale — Douala — 696 65 41 64**
> Bonjour, Mouscou Optique Médicale : à Douala, deux minutes de votre temps suffisent.
> Cette page d'un opticien de Douala est ici.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot, un seul : vous voulez voir ?

**#27 OMB Optique — Douala — 699 77 02 34**
> Bonjour, à Douala, OMB Optique — je passais par votre nom ce matin.
> J'ai fait la page d'un opticien de Douala.
> Vous regardez tranquillement, quand vous avez le temps.
> Vous me dites un mot : je vous le partage ?

**#28 Optic Laser Médical — Douala — 677 82 74 34**
> Bonjour, Optic Laser Médical : à Douala, deux minutes de votre temps suffisent.
> C'est la page d'un opticien de Douala, prête.
> Je peux vous envoyer le lien, sans rien préparer.
> Répondez par un mot : je vous le transmets ?

**#29 OpticPlus — Douala — 699 37 91 50**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> Et la page d'un opticien de Douala existe.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#30 Pagrot Optique — Douala — 699 90 46 91**
> Bonjour, à Douala je vois Pagrot Optique dans l'annuaire des pros.
> Voilà la page d'un opticien de Douala, en ligne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi en un mot : je vous l'envoie ?

**#31 Royal Optic — Bali — 676 250 409**
> Bonjour, à Bali vous êtes Royal Optic, et je passais par là.
> Une page d'un opticien de Douala tourne aussi.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot, un seul : vous voulez voir ?

**#32 Saoudia Optique — Douala — 696 04 04 13**
> Bonjour, à Douala vous êtes Saoudia Optique, et je passais par là.
> Cette page d'un opticien de Douala tourne.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Répondez par un mot : je vous le transmets ?

**#33 Win Optic Plus — Douala — 699 12 59 06**
> Bonjour, vous êtes Win Optic Plus à Douala, si je ne me trompe.
> C'est la page d'un opticien de Douala, prête.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi en un mot : je vous l'envoie ?

**#34 World Vision — Douala — 656 03 21 72**
> Bonjour, vous êtes World Vision à Douala, si je ne me trompe.
> Cette page d'un cabinet de Douala est ici.
> Le lien part quand vous voulez, sans condition.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#35 Divine Success Comprehensive College (DSCC) — Ngodi — 696023696**
> Bonjour, à Ngodi je lis « Kingdom Family Int'l » sur votre compte pro.
> Le tableau vous nomme « Divine Success Comprehensive College (DSCC) », pas autrement.
> Aucun reproche : ce n'est pas votre page.
> Dites-moi en un mot : lequel vos clients prononcent ?

**#36 American School of Douala (ASD) — BP 1909 — 677717083**
> Bonjour, à BP 1909 je travaille pour les opticiens de la ville.
> Cette page d'une école de Douala tourne.
> Je vous le transmets, vous comparez avec la vôtre.
> Vous me dites un mot : je vous le partage ?

**#37 Aube Labo — Akwa II — 693 06 81 84**
> Bonjour, à Akwa II je travaille pour les opticiens de la ville.
> J'ai fait la page d'un laboratoire de Douala.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot : je vous montre le lien ?

**#38 Baptist High School (BHS) Awae — Awae — 677647802**
> Bonjour, Baptist High School (BHS) Awae : à Awae, j'ai quelque chose à vous montrer.
> Cette page d'une école de Douala tourne.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot : je vous montre le lien ?

**#39 Biolex Labo — Deido — 697 78 00 05**
> Bonjour, à Deido, Biolex Labo — je passais par votre nom ce matin.
> Voilà la page d'un laboratoire de Douala, en ligne.
> Le lien part quand vous voulez, sans condition.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#40 Laboratoire Biomedicam — Bonapriso — 699 00 32 07**
> Bonjour, Laboratoire Biomedicam : à Bonapriso, deux minutes de votre temps suffisent.
> Une page d'un laboratoire de Douala tourne aussi.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#41 Bioscan — New Bell — 680 06 03 94**
> Bonjour, à New Bell je vois Bioscan dans l'annuaire des pros.
> Cette page d'un cabinet de Douala est ici.
> Je peux vous envoyer le lien, sans rien préparer.
> Vous me dites un mot : je vous le partage ?

**#42 Bishop Jules Peters Memorial College — Bokwaongo — 683348856**
> Bonjour, Bishop Jules Peters Memorial College : à Bokwaongo, j'ai quelque chose à vous montrer.
> Et la page d'une école de Douala existe.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot, un seul : vous voulez voir ?

**#43 Blessed Group of Schools (BGS / Blessed Anglo-Saxon) — Simbock — 680139453**
> Bonjour, Blessed Group of Schools (BGS / Blessed Anglo-Saxon) : à Simbock, j'ai quelque chose à vous montrer.
> J'ai fait la page d'une école de Douala.
> Le lien part quand vous voulez, sans condition.
> Répondez par un mot : je vous le transmets ?

**#44 Clinique Médico-Chirurgicale de L'Espoir (CEMECES) — Bonabéri Sodiko — 674 93 66 04**
> Bonjour, Clinique Médico-Chirurgicale de L'Espoir (CEMECES) : à Bonabéri Sodiko, deux minutes de votre temps suffisent.
> Cette page d'une clinique de Douala tourne.
> Vous regardez tranquillement, quand vous avez le temps.
> Dites-moi en un mot : je vous l'envoie ?

**#45 Centre Médical Saint Luc — Rond-point Deido — 699 08 67 11**
> Bonjour, à Rond-point Deido je vois Centre Médical Saint Luc dans l'annuaire des pros.
> C'est la page d'une clinique de Douala, prête.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#46 Clinique des Cités — Makepe — 699 22 62 74**
> Bonjour, à Makepe je travaille pour les opticiens de la ville.
> Voilà la page d'une clinique de Douala, en ligne.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot, un seul : vous voulez voir ?

**#47 Centre Médical d'Ophtalmologie de Douala-Nord (CMODN) — Makepe — 698 00 68 98**
> Bonjour, à Makepe vous êtes Centre Médical d'Ophtalmologie de Douala-Nord (CMODN), et je passais par là.
> Et la page d'une clinique de Douala existe.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#48 COMED — Bonapriso — 699 91 56 52**
> Bonjour, vous êtes COMED à Bonapriso, si je ne me trompe.
> Une page d'un cabinet de Douala tourne aussi.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Vous me dites un mot : je vous le partage ?

**#49 Complexe Scolaire et Universitaire Siantou — Mvog-Mbi — 668556755**
> Bonjour, à Mvog-Mbi, Complexe Scolaire et Universitaire Siantou — je passais par votre nom ce matin.
> Cette page d'une école de Douala est ici.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot : je vous montre le lien ?
