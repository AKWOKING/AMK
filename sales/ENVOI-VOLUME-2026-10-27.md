# ENVOI — LA VAGUE VOLUME (27, 28 et 29 octobre 2026)

```text
DÉCISION King, 26/10 : « we can't be sending just 1 message per day, we send between 20-50,
in cold messaging volume counts ».
PORTE    python3 tools/qa/audit_outreach.py sales/ENVOI-VOLUME-2026-10-27.md --strict
         → 0 bloquant, 0 avertissement. 42 messages sur trois jours, aucun ne partage douze mots
         avec un autre — ni avec les sept de la vague 2.
ORDRE    les sept cabinets à 3/3 sont SORTIS de ce lot — ils ont leur propre fichier, écrit à la main :
         sales/ENVOI-VAGUE-2-2026-10-26.md. Ici, le reste : ordre de preuve, portes d'abord.
```

## Ce que ce lot est, et ce qu'il n'est pas

**Ce qu'il est** : la première vague écrite par une fabrique (`tools/outreach/compose.py`), parce que
quarante-deux messages à la main, c'est trois jours de travail pour un résultat qui se ressemble.

**Ce qu'il n'est pas** : personnalisé au fait près. Deux angles, et ils ne mentent pas :

| Angle | Ce qu'il affirme | Sa preuve | Combien ici |
|---|---|---|---|
| **le nom** | le profil WhatsApp ne porte pas le nom de l'établissement | capture du 25/10 (porte A) | **0** — les deux cas restants ont leur message écrit à la main |
| **l'offre** | une page existe déjà dans le métier du destinataire | opticien : `dmoptiquesarl.com` (client payant) · clinique : `hosting/samples/clinic-bonaberi.html` · école : `hosting/samples/mitoc.html` · laboratoire : `hosting/previews/labiomed/` | **42** |

**L'angle « offre » ne dit rien sur le prospect** : ni qu'il n'a pas de site, ni que sa fiche est vide.
Nous ne l'avons pas vérifié pour ces lignes, et le §8c interdit de l'affirmer. La question finale demande
une action, et rien d'autre.

## La porte A se ferme au moment de l'envoi — et voici le compte

Mesuré le 26/10 sur ce fichier, numéro par numéro, contre `leads/VERIF-2026-10-26.md` :

| Verdict du vérificateur | Combien | Ce que ça veut dire pour King |
|---|---|---|
| **3/3 → envoi direct** | **0** | les sept 3/3 sont dans `sales/ENVOI-VAGUE-2-2026-10-26.md`, pas ici |
| **2/3 → King tranche** | **9** | profil Business vu, acheteur identifié, **la preuve numérique manque** |
| **1/3 → jamais écrit à l'aveugle** | **33** | numéro jamais ouvert sur WhatsApp : aucune porte n'est prouvée |
| numéro mort (⛔) | **0** | aucun, et c'est la première fois |

Ces 42 lignes ne sont pas les mêmes que celles du matin : les sept à 3/3 en ont été **sorties** (elles
ont leur propre fichier, écrit à la main, mot pour mot). Sur les 42, la fabrique n'a jamais réécrit un
des sept messages de la vague 2 — `--deja` le lui interdit.

**Donc ce fichier n'est pas encore un lot d'envoi : c'est une file d'attente de vérification.** Ce qui
le transforme en lot, c'est le geste de King : ouvrir les 42 profils, huit secondes chacun, et laisser
tomber tout ce qui n'est pas un cabinet. Les 9 à 2/3 n'ont besoin que d'une capture ; les 33 à 1/3 ont
besoin de trois choses à la fois, et c'est le même geste qui les donne.

**Conséquence assumée** : le plancher de 20 n'est pas garanti par ce fichier. Il est garanti par le
temps que King passe sur WhatsApp — et c'est précisément le goulot que le ruling du 26/10 désigne.
Les 42 messages existent pour qu'aucune minute de vérification ne se perde en rédaction.

## Ce que King fait, dans cet ordre

1. **Vérifier le numéro** sur WhatsApp (8 s) ; barrer les morts plutôt que les composer.
2. **Envoyer dans l'ordre du fichier** — les portes franches sont devant.
3. **Répondre dans l'heure** à qui répond.
4. **Cocher le tracker** le soir (`sales/CAMPAGNE-VOLUME-2026-10-26.md` §5).

## Les messages

**#1 Optique Pro — Douala — 690 03 48 18**
> Bonjour, à Douala le nom sur votre profil est « Laury Ntemtsa » seul.
> Le tableau de l'Ordre dit « Optique Pro ».
> Deux noms, et ce n'est pas votre faute.
> Dites-moi, en un mot : lequel vos patients utilisent ?

**#2 Alpha Optic — Douala — 699 57 34 57**
> Bonjour, à Douala vous êtes Alpha Optic, et je passais par là.
> J'ai fait la page d'un opticien de Douala.
> Je peux vous envoyer le lien, sans rien préparer.
> Dites-moi en un mot : je vous l'envoie ?

**#3 Emeraude Optique Sarl — Douala — 699 90 99 60**
> Bonjour, vous êtes Emeraude Optique Sarl à Douala, si je ne me trompe.
> Cette page d'un opticien de Douala tourne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#4 La Fierté de l'Optique — Douala — 695 17 90 57**
> Bonjour, La Fierté de l'Optique : à Douala, j'ai quelque chose à vous montrer.
> Voilà la page d'un opticien de Douala, en ligne.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#5 Light Optique — Douala — 677 64 87 90**
> Bonjour, Light Optique : à Douala, deux minutes de votre temps suffisent.
> Et la page d'un opticien de Douala existe.
> Le lien part quand vous voulez, sans condition.
> Vous me dites un mot : je vous le partage ?

**#6 Maranatha Optics — Douala — 658 16 31 90**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> Cette page d'un opticien de Douala est ici.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Répondez par un mot : je vous le transmets ?

**#7 Pagrot Optique — Douala — 699 90 46 91**
> Bonjour, Pagrot Optique : à Douala, deux minutes de votre temps suffisent.
> J'ai fait la page d'un opticien de Douala.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#8 Saoudia Optique — Douala — 696 04 04 13**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> C'est la page d'un opticien de Douala, prête.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#9 World Vision — Douala — 656 03 21 72**
> Bonjour, à Douala vous êtes World Vision, et je passais par là.
> Voilà la page d'un cabinet de Douala, en ligne.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Vous me dites un mot : je vous le partage ?

**#10 Africa Optic — Douala — 691 28 02 37**
> Bonjour, vous êtes Africa Optic à Douala, si je ne me trompe.
> Et la page d'un opticien de Douala existe.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot : je vous montre le lien ?

**#11 Caprice Optique — Douala — 675 06 16 23**
> Bonjour, à Douala, Caprice Optique — je passais par votre nom ce matin.
> Une page d'un opticien de Douala tourne aussi.
> Cinq minutes sur votre téléphone, et vous verrez.
> Répondez par un mot : je vous le transmets ?

**#12 Class-Optic — Douala — 691 17 18 17**
> Bonjour, à Douala, Class-Optic — je passais par votre nom ce matin.
> Cette page d'un opticien de Douala tourne.
> Je peux vous envoyer le lien, sans rien préparer.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#13 Cristalys Optic — Douala — 690 94 51 50**
> Bonjour, vous êtes Cristalys Optic à Douala, si je ne me trompe.
> J'ai fait la page d'un opticien de Douala.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot, un seul : vous voulez voir ?


## Jour 2 — mardi 28/10 · 22 messages

**#14 Espace Vision — Douala — 677 33 94 24**
> Bonjour, Espace Vision : à Douala, j'ai quelque chose à vous montrer.
> C'est la page d'un cabinet de Douala, prête.
> Cinq minutes sur votre téléphone, et vous verrez.
> Vous me dites un mot : je vous le partage ?

**#15 Express Optic — Douala — 675 77 61 25**
> Bonjour, Express Optic : à Douala, deux minutes de votre temps suffisent.
> Voilà la page d'un opticien de Douala, en ligne.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot : je vous montre le lien ?

**#16 Gift Optical — Douala — 673 52 17 35**
> Bonjour, à Douala je vois Gift Optical dans l'annuaire des pros.
> Et la page d'un opticien de Douala existe.
> Je vous le transmets, vous comparez avec la vôtre.
> Répondez par un mot : je vous le transmets ?

**#17 Gilles-André Vision — Douala — 699 88 31 78**
> Bonjour, à Douala vous êtes Gilles-André Vision, et je passais par là.
> Cette page d'un cabinet de Douala est ici.
> Vous regardez tranquillement, quand vous avez le temps.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#18 L'Opticien SARL — Douala — 694 33 65 82**
> Bonjour, à Douala je vois L'Opticien SARL dans l'annuaire des pros.
> J'ai fait la page d'un opticien de Douala.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#19 La Lunetterie Médicale El Shadai — Douala — 696 89 64 11**
> Bonjour, à Douala je vois La Lunetterie Médicale El Shadai dans l'annuaire des pros.
> Une page d'un opticien de Douala tourne aussi.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot : je vous montre le lien ?

**#20 Le Samaritain Optique — Douala — 670 19 74 51**
> Bonjour, Le Samaritain Optique : à Douala, j'ai quelque chose à vous montrer.
> Cette page d'un opticien de Douala est ici.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Dites-moi en un mot : je vous l'envoie ?

**#21 London Vision — Douala — 696 76 81 16**
> Bonjour, à Douala vous êtes London Vision, et je passais par là.
> C'est la page d'un cabinet de Douala, prête.
> Le lien part quand vous voulez, sans condition.
> Un mot : je vous montre le lien ?

**#22 Lux Optique — Douala — 655 04 05 49**
> Bonjour, vous êtes Lux Optique à Douala, si je ne me trompe.
> Voilà la page d'un opticien de Douala, en ligne.
> Vous regardez tranquillement, quand vous avez le temps.
> Répondez par un mot : je vous le transmets ?

**#23 LyfyOptic — Douala — 699 98 06 66**
> Bonjour, LyfyOptic : à Douala, j'ai quelque chose à vous montrer.
> Une page d'un opticien de Douala tourne aussi.
> Je peux vous envoyer le lien, sans rien préparer.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#24 Mel's Optic — Douala — 690 98 85 18**
> Bonjour, à Douala, Mel's Optic — je passais par votre nom ce matin.
> Et la page d'un opticien de Douala existe.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Dites-moi en un mot : je vous l'envoie ?

**#25 Mouscou Optique Médicale — Douala — 696 65 41 64**
> Bonjour, Mouscou Optique Médicale : à Douala, deux minutes de votre temps suffisent.
> Cette page d'un opticien de Douala est ici.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot, un seul : vous voulez voir ?

**#26 OMB Optique — Douala — 699 77 02 34**
> Bonjour, à Douala, OMB Optique — je passais par votre nom ce matin.
> J'ai fait la page d'un opticien de Douala.
> Vous regardez tranquillement, quand vous avez le temps.
> Vous me dites un mot : je vous le partage ?

**#27 Optic Laser Médical — Douala — 677 82 74 34**
> Bonjour, Optic Laser Médical : à Douala, deux minutes de votre temps suffisent.
> C'est la page d'un opticien de Douala, prête.
> Je peux vous envoyer le lien, sans rien préparer.
> Répondez par un mot : je vous le transmets ?

**#28 OpticPlus — Douala — 699 37 91 50**
> Bonjour, à Douala je travaille pour les opticiens de la ville.
> Et la page d'un opticien de Douala existe.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#29 Win Optic Plus — Douala — 699 12 59 06**
> Bonjour, à Douala je vois Win Optic Plus dans l'annuaire des pros.
> Voilà la page d'un opticien de Douala, en ligne.
> Cinq minutes sur votre téléphone, et vous verrez.
> Dites-moi en un mot : je vous l'envoie ?

**#30 Divine Success Comprehensive College (DSCC) — Ngodi — 696023696**
> Bonjour, à Ngodi vous apparaissez sous « Kingdom Family Int'l » sur WhatsApp.
> L'Ordre, lui, vous inscrit « Divine Success Comprehensive College (DSCC) ».
> Aucun reproche : ce n'est pas votre page.
> Dites-moi, en un mot : lequel vos patients utilisent ?

**#31 American School of Douala (ASD) — BP 1909 — 677717083**
> Bonjour, à BP 1909 je travaille pour les opticiens de la ville.
> Une page d'une école de Douala tourne aussi.
> Le lien part quand vous voulez, sans condition.
> Dites-moi en un mot : je vous l'envoie ?

**#32 Blessed Group of Schools (BGS / Blessed Anglo-Saxon) — Simbock — 680139453**
> Bonjour, à Simbock je travaille pour les opticiens de la ville.
> Cette page d'une école de Douala tourne.
> Je vous le transmets, vous comparez avec la vôtre.
> Vous me dites un mot : je vous le partage ?

**#33 COMED — Bonapriso — 699 91 56 52**
> Bonjour, à Bonapriso vous êtes COMED, et je passais par là.
> Une page d'un cabinet de Douala tourne aussi.
> Je vous le transmets, vous comparez avec la vôtre.
> Un mot, un seul : vous voulez voir ?

**#34 Complexe Scolaire et Universitaire Siantou — Mvog-Mbi — 668556755**
> Bonjour, Complexe Scolaire et Universitaire Siantou : à Mvog-Mbi, j'ai quelque chose à vous montrer.
> Cette page d'une école de Douala tourne.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot : je vous montre le lien ?

**#35 COSBINAL – Complexe Scolaire Bilingue NAL — Bonamoussadi — 677786379**
> Bonjour, vous êtes COSBINAL – Complexe Scolaire Bilingue NAL à Bonamoussadi, si je ne me trompe.
> Cette page d'un cabinet de Douala est ici.
> Le lien part quand vous voulez, sans condition.
> Un mot suffit : vous voulez que je vous l'envoie ?


## Jour 3 — mercredi 29/10 · 7 messages, à joindre aux 22 du stock restant

**#36 Isalyd Corporation — Douala — 694 85 87 46**
> Bonjour, à Douala vous êtes Isalyd Corporation, et je passais par là.
> Cette page d'un cabinet de Douala tourne.
> Je vous l'envoie : vous regardez sur votre téléphone.
> Répondez par un mot : je vous le transmets ?

**#37 Le Paradis des Anges (PDA) — Makepe — 677378542**
> Bonjour, vous êtes Le Paradis des Anges (PDA) à Makepe, si je ne me trompe.
> C'est la page d'un cabinet de Douala, prête.
> Je vous le transmets, vous comparez avec la vôtre.
> Dites-moi en un mot : je vous l'envoie ?

**#38 New Horizon International Comprehensive High School (NHICHS) — Cité Sonara — 680738111**
> Bonjour, à Cité Sonara je travaille pour les opticiens de la ville.
> J'ai fait la page d'une école de Douala.
> Cinq minutes sur votre téléphone, et vous verrez.
> Un mot : je vous montre le lien ?

**#39 One Stop Medical Laboratory & Diagnostics — Douala — 691632941**
> Bonjour, à Douala, One Stop Medical Laboratory & Diagnostics — je passais par votre nom ce matin.
> Voilà la page d'un laboratoire de Douala, en ligne.
> Le lien part quand vous voulez, sans condition.
> Dites-moi juste un mot : je l'envoie ce soir ?

**#40 Rainforest International School (RFIS) — SIL — 677937162**
> Bonjour, Rainforest International School (RFIS) : à SIL, j'ai quelque chose à vous montrer.
> Et la page d'une école de Douala existe.
> Vous regardez tranquillement, quand vous avez le temps.
> Un mot, un seul : vous voulez voir ?

**#41 Saint Anne's High School Limbe (SAHISCOL) — New Town — 682122959**
> Bonjour, Saint Anne's High School Limbe (SAHISCOL) : à New Town, deux minutes de votre temps suffisent.
> Une page d'une école de Douala tourne aussi.
> Vous l'ouvrez sur votre téléphone, et vous jugez.
> Un mot suffit : vous voulez que je vous l'envoie ?

**#42 Solidarity Health Foundation (Solidarity Clinic & Laboratory) — Untarred Malingo St — 677615757**
> Bonjour, à Untarred Malingo St je vois Solidarity Health Foundation (Solidarity Clinic & Laboratory) dans l'annuaire des pros.
> Cette page d'un laboratoire de Douala est ici.
> Je peux vous envoyer le lien, sans rien préparer.
> Vous me dites un mot : je vous le partage ?
