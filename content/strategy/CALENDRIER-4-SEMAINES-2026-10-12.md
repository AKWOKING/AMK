# CALENDRIER DE CONTENU — 4 semaines · 12/10 → 08/11/2026 · @amkweb.cm

> **Statut : PROPOSITION du 08/10 (soir), à valider par King. Rien n'est publié.** Publication : King seul.
> **Sources :** `research/IG-AUDIT-AMKWEB-2026-10-08.md` (audit + concurrents) · `CONTENT-STRATEGY-V2-2026-10-05.md` · `VIDEO7-REPLAN-2026-10-06.md` · `POSTING-CALENDAR.md` §E/§F · `CONTENT-LESSONS.md` §1, §2, §10.4, §12 · `RULE-CREDENTIAL-CLAIMS.md` · `ANALYTICS-LOG.md`.
> **Les 3 premiers carrousels sont prêts :** `content/carousels/POST-READY.md` (images + légendes + textes alternatifs).

## 1 · Règles qui cadrent ce calendrier (déjà tranchées, non modifiées)

| Règle | Source | Effet ici |
|---|---|---|
| Problème d'abord, travail réel, CTA « seulement parfois » | V2 §2 | Chaque post ouvre sur un problème ou un test que le lecteur peut vérifier lui-même |
| Zéro preuve tant qu'aucun client n'est signé | V2 §2.4 | Aucun chiffre, aucun témoignage, aucun « depuis ». Exemples visuels = pages **fictives étiquetées** |
| Pas de prix public, pas de délai promis | décision 08/10 (7ᵉ message) · `RULE-CREDENTIAL-CLAIMS` | Aucun prix ni « 24 h » / « 3–5 jours » dans les posts |
| Test 30 jours 05/10 → **04/11**, kill rule | V2 §4 | Les créneaux **après le 04/11** sont conditionnels |
| La métrique : DM « APERÇU »/« ESSAI » qualifiés, pas les vues | V2 §4 | Une colonne « Mesure » ; les vues ne sont qu'un diagnostic |
| Une plateforme = 1 publication/jour max, 4 h d'écart minimum ; TikTok **ven 18:00–20:00** tenu constant ; les vidéos sortent sur TikTok d'abord | `POSTING-CALENDAR` §F · `VIDEO7-REPLAN` | Reels Instagram = **réemploi le lendemain (samedi 12:00–14:00)** |
| Vidéos : V7 = mouvement ≤ 0,8 s + voix à 0 s ; V8 ajoute sous-titres, CTA ≤ 20 s, ≤ 25 s, double canal ; gate FFmpeg | `VIDEO7-REPLAN` | Un master qui échoue le gate est tué pour le cycle |
| Aucun nom réel d'opticien, de clinique ou d'école sans écrit | `CONTENT-LESSONS` §11 | Format et agrégats seulement |
| V2 §5 interdit « plus de trois publications par semaine » : le plafond est donc **3/semaine** | V2 §5 | Votre demande de 3/semaine est **au plafond**, pas en dessous |

**Conséquence de production :** V2 prévoyait 2 publications/semaine (« deux tenues battent six promises »). Pour tenir 3 sans augmenter la charge, la 3ᵉ est un **réemploi** (Reel du samedi = la vidéo du vendredi). Les carrousels sont des productions légères (rendu automatique, `tools/content/render_carousels.py`).

**Mot-clé unique :** les carrousels disent **APERÇU**. La vidéo C1 dit « PREVIEW » dans son script. Proposition : **APERÇU partout**, PREVIEW compté comme synonyme dans le décompte.

## 2 · Le calendrier (12 publications)

**Objectif :** V = visibilité · C = confiance · X = conversion. **Heures :** carrousels mar/jeu **19:25** (heure fixe, comparable) · Reels sam **12:00–14:00**.

### Semaine 1 — 12 → 18/10 · « Le problème, vu par la cible »

| # | Date | Format | Cible | Sujet | Accroche (slide 1 ou 3 premières secondes) | Obj. | Mesure | Statut |
|---|---|---|---|---|---|---|---|---|
| 1 | **Mar 13/10** | Carrousel 7 slides | Cliniques, labos, cabinets | Une page Facebook ne répond pas à celui qui pose la question | « « Vous êtes ouverts ? » Votre page Facebook ne répond pas. » | **V** | partages, abonnés (7 j) | ✅ prêt (`c01`) |
| 2 | **Jeu 15/10** | Carrousel 7 slides | Écoles, collèges | Le test sur téléphone : où, quand, comment écrire | « Ouvrez la page de votre école. Comptez jusqu'à 10. » | **C** | enregistrements, partages | ✅ prêt (`c02`) |
| 3 | **Sam 17/10** | Reel (réemploi TikTok ven 16/10) | Opticiens | C1-vidéo « L'annuaire ne suffit pas » | « Vous êtes dans l'annuaire de l'Ordre. » | **X** | DM APERÇU | ⏳ master à produire ; gate FFmpeg ; format de l'annuaire + agrégat « 150+ », aucun nom réel |

### Semaine 2 — 19 → 25/10 · « Voir avant de payer »

| # | Date | Format | Cible | Sujet | Accroche | Obj. | Mesure | Statut |
|---|---|---|---|---|---|---|---|---|
| 4 | **Mar 20/10** | Carrousel 7 slides | Écoles, cliniques, labos | Comment fonctionne l'aperçu, en 4 étapes | « Avant de payer, vous voyez votre page. » | **X** | **DM APERÇU** (la mesure du test) | ✅ prêt (`c03`) |
| 5 | **Jeu 22/10** | Carrousel 7 slides | Cliniques, écoles | Le test « Googlez-vous » : que voit-on en tapant votre nom et votre ville ? | « Tapez le nom de votre clinique et votre ville sur Google. Qu'est-ce qui sort en premier ? » | **V** | partages, vues | ✍️ à rédiger après le résultat de #1–#2 |
| 6 | **Sam 24/10** | Reel (réemploi TikTok ven 23/10) | Cliniques | Vidéo 2 du cycle (V8) : « Votre page Facebook ne prend pas de rendez-vous » | « Votre page Facebook a tout. Il manque une chose : la réponse. » | **X** | DM APERÇU | ⏳ le script V-06 existe ; le master (38,6 s) dépasse la règle V8 (≤ 25 s) : **recut à décider** |

### Semaine 3 — 26 → 01/11 · « Le local »

| # | Date | Format | Cible | Sujet | Accroche | Obj. | Mesure | Statut |
|---|---|---|---|---|---|---|---|---|
| 7 | **Mar 27/10** | Carrousel 7 slides | Écoles, cliniques (Buea et Douala) | Une page dans la langue du visiteur (FR / EN, un bouton visible dès le premier écran) | « Un parent de Buea ouvre votre page. Elle est en français seulement. » (scénario étiqueté) | **V** | partages, abonnés | ✍️ à rédiger |
| 8 | **Jeu 29/10** | Carrousel 7 slides | Cliniques, labos | Les 3 questions qu'un patient se pose avant de venir : horaires, examens proposés, comment prendre rendez-vous | « Avant de venir, il se pose 3 questions. Votre page y répond-elle ? » | **C** | enregistrements | ✍️ à rédiger (sans allégation médicale, `HOUSE-KNOWLEDGE-BASE` §8.6) |
| 9 | **Sam 31/10** | Reel (réemploi TikTok ven 30/10) | Écoles | Vidéo 3 du cycle (V9) : « Un parent cherche votre école » | « Un parent cherche votre école. Que trouve-t-il ? » | **X** | DM APERÇU | ⏳ V-05 FR : **le master n'est pas dans le dépôt** (STATUS seulement) → à reconstruire, puis gate |

### Semaine 4 — 02 → 08/11 · « Preuve, puis décision du 04/11 »

| # | Date | Format | Cible | Sujet | Accroche | Obj. | Mesure | Statut |
|---|---|---|---|---|---|---|---|---|
| 10 | **Mar 03/11** | Carrousel 7 slides | Écoles, cliniques | **A :** première preuve réelle, **si** acompte DM Optique encaissé + proforma tamponnée + accord écrit du client. **B (sinon) :** « Même clinique, deux pages » — l'avant/après fictif MboaCare (`content/studio/before.html` / `after.html`, étiqueté) | A : à écrire avec les faits du client · B : « C'est la même clinique. Laquelle ferait écrire ? » | **C** | enregistrements, DM | ⛔ A bloqué par l'acompte (non encaissé au 08/10) · B possible dès maintenant |
| — | **Mer 04/11** | **Point de décision** (pas une publication) | — | Lecture de la kill rule : DM APERÇU/ESSAI qualifiés depuis le 05/10 | — | — | — | Zéro DM qualifié → on arrête la production vidéo entrante (V2 §4) |
| 11 | **Jeu 05/11** | Carrousel 7 slides | La cible qui a produit le 1er DM | « 3 questions à poser avant de payer un site » (à qui appartient le nom de domaine, en quelle langue, qui change le texte) | « Avant de payer un site, posez ces 3 questions. » | **C** | enregistrements, DM | 🔶 **conditionnel : seulement si le test passe le 04/11** |
| 12 | **Sam 07/11** | Reel (réemploi TikTok ven 06/11) | La cible gagnante | À choisir le 04/11 : reprendre en vidéo le carrousel le plus enregistré | selon le gagnant | **X** | DM APERÇU | 🔶 **conditionnel** (kill rule) |

**Équilibre :** visibilité 3 (#1, #5, #7) · confiance 4 (#2, #8, #10, #11) · conversion 5 (#3, #4, #6, #9, #12, dont #12 conditionnel). Les cinq posts de conversion portent la demande d'aperçu comme message principal ; les carrousels de visibilité et de confiance ne la portent qu'en dernière slide (carrousels #1, #2) ou pas du tout (#8, #11), conformément à « CTA seulement parfois » (V2 §2).

## 3 · Ce qui est volontairement dit sur les chiffres

- **Échantillon du test.** V2 demande 8 publications (4 vidéos + 4 carrousels). Ce calendrier atteint 8 publications le **29/10**, mais **3 vidéos distinctes** avant le 04/11 (TikTok ven 16, 23, 30/10 = V7, V8, V9, conformément au replan du 06/10), pas 4. Une 4ᵉ vidéo (ven 06/11) tombe après la décision. **À trancher par King** : accepter 3 vidéos + 7 carrousels, ou compter autrement.
- **Le compte a 6 abonnés** (capture du 08/10). La portée organique vers l'abonné est quasi nulle ; **hypothèse** (non mesurée) : les carrousels servent surtout à ceux qui ouvrent le profil après un message d'AMK, et au partage par WhatsApp (canal des 35–55 ans, règle 6 du replan). **Recommandation :** King envoie chaque carrousel en statut WhatsApp le jour de la publication.
- **Hashtags :** huit par post, du plus local au plus large. Aucun volume n'a été vérifié ; leur effet est une hypothèse (`CONTENT-LESSONS` §7).
- **Lecture des résultats :** 24 h / 72 h / 7 j, par plateforme, chiffres de King seulement, consignés dans `ANALYTICS-LOG.md`. Jamais moyennés entre TikTok et Instagram.

## 4 · Contrôle des affirmations des trois carrousels (`RULE-CREDENTIAL-CLAIMS`)

| Affirmation | Nature | Statut |
|---|---|---|
| « Il appelle la clinique d'à côté » | **Scénario**, étiqueté « SCÉNARIO » sur la slide | ✅ pas une statistique |
| « Ouvrez… comptez jusqu'à 10 » · « 3 sur 3 : gardez-le » | **Test à faire soi-même** ; ne dit pas que les parents partent après 10 s | ✅ |
| « Aperçu gratuit » · « Avant de payer, vous voyez votre page » · « Pas d'obligation de continuer » | **Offre d'AMK** : déjà publique (légende V-06 « gratuit, vous la regardez avant de décider ») ; cohérent avec DM Optique (aperçu, puis acompte) | ⚠️ **King confirme que l'offre tient telle quelle** avant le 13/10 |
| « Nous construisons votre page d'accueil : votre nom, votre ville, vos services » | Processus décrit, sans résultat promis | ✅ |
| Captures MboaCare et Crestwood College | **Pages fictives** avec bandeau « fictif » visible ; la caption le redit ; ni client ni prospect | ✅ |
| Prix · délais · « depuis » · nombre de clients | **Absents** | ✅ |

## 5 · Avant le 13/10 (décisions de King, non prises ici)

1. **Post fondateur** (« 100 000 F », « Only 2 founding clients this month », « live in 3–5 days ») : le retirer ou le garder ? Il contredit la décision « pas de prix public » et date de septembre.
2. **Bio** : « free 24h homepage preview » promet plus que le processus (relecture ≤ 1 h, envoi le jour ouvré si le DM arrive avant 15 h WAT).
3. **Lien Threads** `alex_aiproductlab` : voulu ?
4. **Lien de bio** : il pointe l'accueil ; les pages `creation-site-web-clinique-cameroun` et `-ecole-` ne sont en ligne qu'après le déploiement de vendredi. Un post clinique pourrait pointer vers la page clinique.
5. **Public cible de la bio** : elle dit « schools & clinics » ; l'onde du 12/10 et la vidéo C1 visent les opticiens. Décision du 9ᵉ message : l'accueil reste écoles + cliniques jusqu'à ce que DM Optique soit en ligne et approuvé.
6. **Langue** : les cinq Reels actuels sont en anglais ; ces carrousels sont en **français**, légende française + une ligne anglaise.

## 6 · Production

- **Carrousels** : source unique `content/carousels/carousels.json` → `python3 tools/content/render_carousels.py` (contrôles : glyphes, cadre, contraste ≥ 4,5, ≤ 7 slides). Les carrousels #5, #7, #8, #10 et #11 se rédigent une fois la semaine précédente lue (le 5 dépend des chiffres de #1–#2).
- **Vidéos** : 3 masters à produire ou recouper (C1, V-06 ≤ 25 s, V-05). Aucun n'existe au format V7/V8 aujourd'hui ; le master V-06 existe (38,6 s), le master V-05 est absent du dépôt.
- **Créneau du vendredi 09/10** : v06 (compte client, acompte requis) : hors de ce calendrier.
