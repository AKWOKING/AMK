# AMK — ANALYTICS LOG (lectures par publication)

**Règle :** uniquement les chiffres de King, recopiés **verbatim**, plateforme par plateforme, jamais moyennés, jamais arrondis vers le haut. Une donnée absente reste **« non disponible »** — on ne l'estime pas. Chaque lecture indique sa source (capture) et son horodatage.

---

## 2026-09-17 · TikTok — deux lectures (11 captures WhatsApp de King, ~12:48–12:52)
**Source :** écrans **TikTok Studio → Video analysis** envoyés par King le 17/09. Fenêtre d'observation : ~2 j pour la publication A, ~1 j pour la publication B. **Ce ne sont pas des lectures 24 h/72 h/7 j normalisées** — l'âge diffère entre les deux.

### A · « Losing customers — BEFORE WHATSAPP? » · 34.27 s · publiée **mar 15 sep 2026, 19:25**

| Mesure | Valeur (verbatim) |
|---|---|
| Vues · likes · commentaires · partages · enregistrements | **156 · 7 · 1 · 1 · 0** |
| Temps de lecture total | **0 h 18 min 55 s** |
| Durée de lecture moyenne | **6,2 s** |
| Ont regardé la vidéo en entier | **4,35 %** |
| Nouveaux abonnés | **1** |
| Rétention moyenne | **18 %** — « la plupart ont arrêté à **0:02** » |
| Rétention ponctuelle (curseur) | **21 % à 00:06** · **16 % à 00:10** |
| Spectateurs (total) | **65** (dont **74 % nouveaux / 26 % de retour**) |
| Abonnés / non-abonnés | **0 % / 100 %** |
| Sexe | H **58 %** · F **41 %** · autre **1 %** |
| Âge | 18–24 **46 %** · 25–34 **45 %** · 35–44 **7 %** · 45–54 **1 %** · 55+ **1 %** |
| Localisations | Cameroun **99,0 %** · Inde **0,5 %** |
| Sources de trafic | Pour Toi **87,5 %** · Profil perso **9,8 %** · Autre **2,2 %** · Messages directs **0,5 %** · Abonnements **0,0 %** · Son **0,0 %** · Recherche **0,0 %** |
| Moment des likes | le plus de likes à **0:00 (33 %)** |
| Mots des commentaires | *pas encore prêts* |

### B · `clinic-founding-en` « Only 2 founding clients this month » · 29.21 s · publiée **mer 16 sep 2026, 12:02**

| Mesure | Valeur (verbatim) |
|---|---|
| Vues · likes · commentaires · partages · enregistrements | **121 · 4 · 0 · 0 · 0** |
| Temps de lecture total | **0 h 08 min 58 s** |
| Durée de lecture moyenne | **3,8 s** |
| Ont regardé la vidéo en entier | **1,4 %** |
| Nouveaux abonnés | **0** |
| Rétention moyenne | **13 %** — « la plupart ont arrêté à **0:02** » |
| Rétention ponctuelle (curseur) | **1 % à 00:27** |
| Spectateurs (total) | **en cours de calcul** (non disponible) |
| Abonnés / non-abonnés | **0 % / 100 %** |
| Sexe | H **33 %** · F **66 %** · autre **1 %** |
| Âge | 18–24 **53 %** · 25–34 **33 %** · 35–44 **11 %** · 45–54 **2 %** · 55+ **1 %** |
| Localisations | Cameroun **98,6 %** · Émirats **0,7 %** · Belgique **0,7 %** |
| Sources de trafic | Pour Toi **90,9 %** · Profil perso **4,2 %** (reste partiellement visible) |
| Moment des likes | le plus de likes à **0:00 (80 %)** |
| Mots des commentaires | *pas encore prêts* |

### Calculs AMK (arithmétique simple, déclarée — pas des chiffres TikTok)
- A : **156 vues / 65 spectateurs = 2,4 vues par spectateur** (les gens revoient) · taux de like **4,5 %**.
- B : taux de like **3,3 %**.
- Les deux : **4,35 % de 156 ≈ 7 personnes** ont vu les 34 s en entier ; **1,4 % de 121 ≈ 2 personnes** pour la vidéo B. En valeur absolue, la « fin de vidéo » est quasi déserte dans les deux cas.
- ⚠ **Les chiffres de TikTok ne se recoupent pas exactement** : temps total ÷ vues = **7,3 s** pour A et **4,5 s** pour B, contre 6,2 s et 3,8 s annoncés. Écart normal (modes de comptage, relectures) → **à traiter comme directionnel, pas au dixième**.

### Vérifications techniques faites par AMK sur les masters du dépôt (17 Sep, FFmpeg)
| Fichier | Durée conteneur | Piste audio | Ouverture |
|---|---|---|---|
| `content/videos/v04-before-whatsapp/Video_04_Real_Website_PREVIEW.mp4` | **34,20 s** (audio 34,21) | **OUI** | **image totalement figée de 0:00 à ≥2,4 s ; première coupe à 4,78 s** (`timeline.json` : 0 → 4.78 → 9.78 → 16.02 → 21.30 → 26.50 → 30.50) |
| `sales/social/videos/clinic-founding-en.mp4` | **29,20 s** | **NON — aucune piste audio** | carte sombre à 0,2 s → carte allumée à 3,0 s (révélation lente), **silencieuse de bout en bout** |
| `sales/social/videos/{clinic-school}-founding-{en,fr}.mp4` (les 3 non publiées) | 29,20 s | **NON — aucune piste audio** | idem |
| `Video_02_Five_Website_Answers.mp4` (#2) | 29,40 s | OUI | — |
| `Video_03_Part_2.mp4` (#3) | 34,90 s | OUI | — |

**Correspondance TikTok :** `clinic-founding-en` = 29,20 s dans le dépôt → **29,21 s** sur la carte TikTok (écart 0,01 s = arrondi). La publication A affiche **34,27 s** alors que notre master #4 fait **34,20 s** (audio 34,21) → **écart de 0,06–0,07 s : soit un arrondi de ré-encodage, soit une version légèrement différente de la même idée. À confirmer par King** (voir question ouverte ci-dessous).

### Question ouverte (bloque le calendrier)
> **Cette publication A du 15/09 à 19:25 est-elle une version antérieure du concept #4 « avant WhatsApp » ?**
> - **Si oui :** #4 a déjà été publié sur TikTok → la place du **mar 23** ne peut pas reprendre le même script (doublon + risque de déclassement TikTok), et la lecture de rétention ci-dessus s'applique **à #4 lui-même**.
> - **Si non :** ce fichier n'est pas dans le dépôt → merci de dire ce qui a été publié ce soir-là (titre/durée), pour tenir le registre exact.

### Ce que ces chiffres disent (et ne disent pas)
1. **Falaise à 0:02 — le fait central.** Les deux publications perdent l'essentiel de l'audience à **2 secondes** ; rétention 18 % / 13 % ; fin de vidéo ~7 et ~2 personnes. TikTok échantillonne (87,5 % / 90,9 % Pour Toi, **100 % de non-abonnés**) mais ne pousse pas : la vidéo échoue au test d'attention avant sa première coupe.
2. **L'ouverture est immobile — vérifié sur les masters.** #4 : cadre figé jusqu'à 2,4 s minimum (première coupe à 4,78 s). B : révélation lente **et aucune piste audio**. La règle « 3-second hook » (§10.2) est respectée dans le **texte**, pas dans le **mouvement**.
3. **Le premier cadre plaît** : le plus de likes arrive à **0:00** (33 % / 80 %) → la couverture/hook fonctionne ; c'est la **seconde suivante** qui est perdue.
4. **B sans audio.** La vidéo fondatrice EN a été publiée **sans son** ; elle est dernière sur toutes les mesures (3,8 s de lecture moyenne, 1,4 % de visionnage complet, 0 abonné) alors que A, narrée, fait 6,2 s / 4,35 % / +1 abonné. **Hypothèse forte, non encore prouvée** (contenus différents par ailleurs).
5. **L'audience atteinte n'est pas l'acheteur** : 18–34 ans = **91 %** (A) et **86 %** (B) ; 35–54 ans = **8 %** et **13 %**. Le Cameroun à ~99 %. Un propriétaire de clinique qui décide d'un site à 100 000 FCFA est majoritairement hors de cette tranche.
6. **Rien ne circule** : 0 enregistrement sur les deux, 1 partage (A), 0 (B). Aucune valeur « à envoyer à quelqu'un ».
7. **Recherche = 0,0 %** : aucune vue via la recherche TikTok — les légendes/mots-clés ne captent pas d'intention.
8. **Le créneau soir vs midi** : A (19:25) bat B (12:02) sur **toutes** les mesures (vues 156 vs 121, lecture moyenne 6,2 vs 3,8 s, rétention 18 % vs 13 %, visionnage complet 4,35 % vs 1,4 %, temps total 18:55 vs 8:58, +1 abonné vs 0). **Mais** les deux vidéos diffèrent par l'audio, la langue, le contenu et l'ancienneté → **ce n'est pas un test propre de l'heure**. À retenir comme indice, pas comme preuve.

---

### CORRECTIONS & RÉSOLUTION (King, 17 Sep ~22:15 — réponses à mes 3 questions)
1. **La question ouverte est résolue :** la publication A du **15/09 à 19:25 est bien une version modifiée de la vidéo #4** (« post #4 = video #4 = before whatsapp »). → **#4 a donc été publié sur TikTok le 15/09.** Le registre du calendrier est corrigé ; le créneau TikTok du mar 23 est **libéré** (republier le même script = doublon).
2. **Correction de la découverte « vidéo muette » :** `clinic-founding-en.mp4` n'a **aucune piste audio dans le fichier**, mais King a **ajouté un son tendance proposé par TikTok au moment de la publication** → **la vidéo n'a pas été publiée en silence.** Le constat devient : *la vidéo publiée avait un fond musical TikTok, pas de narration.* Comparaison A/B à lire en conséquence : **narration (A : 6,2 s / 18 %) vs son tendance seul (B : 3,8 s / 13 %)** — écart cohérent avec l'hypothèse « la voix retient », mais **toujours confondu** par le contenu, la langue et l'ouverture. Ne pas présenter comme une preuve.
3. **Vidéos fondatrices : King a tranché — on les retire** (voir `POSTING-CALENDAR.md` §A2). Les 4 fichiers restent dans le dépôt comme archives, marqués **ne pas publier**.

**Ce qui reste vrai après correction :** la **falaise à 0:02** sur les deux publications, l'**ouverture figée 4,8 s** de #4 (vérifiée image par image), la **récence** de l'audience (86–91 % en 18–34 ans) et la distribution quasi exclusivement « Pour Toi » auprès de non-abonnés.
