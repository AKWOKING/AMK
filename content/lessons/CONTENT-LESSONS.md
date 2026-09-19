# AMK — CONTENT LESSONS (living playbook)

**Version v0.9** · 19 Sep 2026 · sources: `content/handover/2026-09-17-content-handover.md` (previous chat, authoritative), King's 17 Sep brief, repo content history, `research/YouTube-Lessons.md` batches 1–3, `research/HyperFrames-Evaluation-2026-09-19.md`.
**Rule:** append dated entries; never silently rewrite. Conflicts get logged and go to King.

---

## 1 · Brand fingerprint (every video, no exceptions)
- Same **cartoon host**, same **selected voice**, same **navy `#1B2055` / teal `#23C4B1` / amber `#FFB020`** palette, same **Montserrat/Poppins** typography, same **educational tone**.
- Vertical **9:16, 1080×1920, 30 fps, SAR 1:1, H.264** — *verify by decoding the output, never assert.*
- **Host introduces → real website footage teaches.** Never a talking head; never an avatar reciting a script over generic art.
- **One message per beat · one question per screen** when narration lists items.
- Every conclusion and every CTA gets **its own clean, high-contrast, mobile-readable frame**.
- **No overlays on the thing being demonstrated** — a caption once covered the good site's WhatsApp buttons; it was fixed and **must not be reintroduced**.

## 2 · Content quality (hard rules)
- **Show real webpages**, never rectangles masquerading as sites (King's explicit criticism of earlier videos).
- **Bad examples: believable, not parody** — and **labelled**. MboaCare carries "FICTIONAL CLINIC · Deliberately flawed website demonstration" on every capture.
- **Label fiction as fiction, real as real.** Concept sites are **not** client case studies.
- **Hooks are questions or specifics, never hype.** "10 seconds" is a hook, **not** a measured threshold — never turn it into a statistic.
- Payoff frames stay clean: **HARD TO FIND → EASY TO LEAVE · CURIOUS → CONFIDENT · MAKE CONTACT EASY.**
- **Never invent** testimonials, rankings, conversion stats, client outcomes, or completion claims.
- **Never claim a post, a profile edit, or tracking installation happened unless King says so.** Bio/pinned/link advice is *recommendation only*.

## 3 · Funnel & measurement
- Funnel: **Views → Profile visits → Website clicks → PREVIEW DMs → qualified inquiries → projects.**
- Every video ends with the **DM "PREVIEW" closing beat, separate from the educational payoff**. Latest #4 has it; #1–#3 do **not** — **retrofit only if King asks** (and #1's file isn't in the repo).
- **Track IG and TikTok separately. Never average. Never declare a cross-platform winner.**
- Report **24 h / 72 h / 7 d, per platform, only with King's numbers** — never assume, never round up.
- **Views ≠ unique reach.** A bio tap ≠ a loaded session. A WhatsApp click ≠ an inquiry. **A UTM tag = attribution only if analytics actually collect it.**
- Suggested first reply to a PREVIEW DM: ask for **name of school/clinic, town, current website link**. No automation exists.

## 4 · Sources (a stated decision, never a default)
MboaCare (abstract principle) · our own shipped work · **our concept/preview library** (real prospects, real problems, real fixes) · before/after pairs with permission or clean anonymisation · build footage · verified client stories with consent · the niche itself (schools/clinics in Cameroon). State why the source fits the video.

## 5 · Production discipline
- **Unique filename per stage, never edit in place, preserve every prior deliverable.**
- **FFmpeg via `imageio_ffmpeg.get_ffmpeg_exe()`** — never a hard-coded path (packages moved after env resets).
- **Small sequential compositing passes** — a 7-input full-res graph once exhausted the sandbox.
- **Browser captures at 15 fps → compose at 30 fps**; say so in any technical note.
- **QA every final file:** decode, resolution, fps, SAR/DAR, duration — report what was checked.
- **Inspect frames when images are available. Never claim you can't see.**

## 6 · Technical failure log (do not repeat)
| Failure | Fix that worked |
|---|---|
| Wrong loop variable in output filenames → only last clip kept (was wrongly blamed on cleanup) | inspect code before inventing environmental explanations |
| Input and output both `tmpcap.mp4` | unique paths per step; FFmpeg cannot edit in place |
| Mixed/default frame rates | set input & output rates explicitly, `fps=30`, `-r 30`, `setsar=1`; verify output |
| Multiline Bash filter → array instead of one filter string | Python arg list or one correctly quoted filter string |
| "ExtraBold" variable fonts rendered **Thin** | `set_variation_by_axes([800])` bold / `[500]` regular, with fallback (verified working 17 Sep) |
| Font lacked check/arrow glyphs → missing boxes | draw simple marks with PIL lines/vector |
| Playwright Chromium missing system libs | `python -m playwright install-deps chromium` |
| `imageio_ffmpeg` absent after env change | `pip install imageio-ffmpeg`; resolve path at runtime |

## 7 · Evidence from the series so far (King-reported views)
| Platform | #1 | #2 | #3 |
|---|---:|---:|---:|
| Instagram | 13 | **47** | 41 |
| TikTok | not supplied | 87 | **137** |
- **Actionable, specific education beats generic** (#2/#3 vs #1) — direction, not proof.
- **#2 (list/educational) leads IG; #3 (pain-led) leads TikTok.** Test that split, don't average it.
- **⚠ Qualified by the handover:** earlier confident advice about fixed posting windows, minimum weekly cadence, engagement-weight hierarchies and prescribed hashtag counts is **unverified** — treat as hypotheses, never as facts.
- **Duration discipline:** 40.38 s was once called "inside a 35–40 s brief" — it wasn't. Report exact duration; ask before exceeding a cap.
- #1's **SOCIAL MEDIA → ATTENTION / WEBSITE → TRUST → ACTION** mapping was **not prominent enough** — diagrams that matter need their own clean frame (same lesson as #4's CTA frame).

## 8 · Absorbed from the lesson batches (`research/YouTube-Lessons.md`)
- Copy law [5]: visualize / falsify / nobody-else-can-say-it; 2-second test on frame 1; read aloud.
- Claim → proof [6]: every claim carries its artifact on screen; one quote at a time, never a wall.
- Anti-slop [10]: no scroll-jacking, no content-hiding animation, no moving buttons, no emoji icons — applies to any UI on camera.
- Conversion-first [12]: hierarchy (biggest = most important), solid high-contrast CTAs, never ghost buttons as primary.
- Direction exploration [13]: three directions before visual work; explicit avoid-list.
- Taste is the moat [14]: the decisions differentiate when everyone's feed looks the same.

## 10 · Video-marketing lessons (batch #4, 17 Sep 2026 — `research/YouTube-Lessons.md` [15]–[17])

### 10.1 · From Nate Woodbury ("How To Make A Marketing Video For My Business")
- **Two asset classes, don't mix them:** the *educational short-form series* (reach, mirrored to Shorts) vs the **flagship promo** (60–90 s, unlisted on YouTube, embedded on the site + used in proposals). A promo is not expected to go viral; it converts people who already arrived. → production candidate **V-13**.
- **Outcome-over-features gate:** in every script, features may be a minority of beats — the outcome must carry the majority ("features don't sell; the outcome does").
- **Clarity gate before render (4 questions):** what we do · who we help · which outcome · the emotional journey start→middle→end.
- **Testimonials = soundbites**, 5–10 s, placed under the claim they prove — only with consent (ties to [6]).
- **Polish is our pipeline:** §19 three directions + §13 pre-flight + QA — no external production.

### 10.2 · From Brooklyn Social ("How To Make High Converting Videos For Your Business")
- **3-second hook gate (written):** line 1 is a question or a specific aimed at **one person** (a clinic owner, a school proprietor) — never a self-intro, never "today we're going to talk about".
- **"Why should someone care?"** — required per beat before a script is approved.
- **Zero-fluff pass:** read aloud, delete filler (reinforces copy law [5]).
- **Every video carries one clear CTA** — independent confirmation of the PREVIEW closing-beat mandate.
- **Our "lighting/audio" equivalents:** contrast/legibility checked on a phone-sized canvas; music ducked under narration.
- ❌ Rejected: get-the-team-on-camera (no talking heads — BTS becomes build footage: screens, hands, craft), the 78 % Sprout Social stat (unverifiable here), the algorithm/lighting claim (unverified).

### 10.3 · From Digital Canva Mastery (Canva explainer tutorial)
- **Adopted (micro):** element **pop-in** for labels/numbers, and **match-and-move** when the same element grows/moves between beats — implemented in our own PIL/FFmpeg renderer. **Constraint: never animate the demonstrated UI** (no moving buttons — §3.8 anti-slop); titles/labels only.
- **Three-component pre-flight** formalised in the script header: script → visuals → voice.
- ❌ Rejected: the Canva/ChatGPT/ElevenLabs template stack — it cannot show **real websites** (our hard requirement) and produces the generic look King banned. Our pipeline already does script→visuals→voice with the real pages.

### 10.4 · Depuis `/brag` de latent-spaces (19 Sep 2026) — la lisibilité devient un nombre
**Contexte :** King a envoyé `github.com/latent-spaces/brag` (« can this be useful to us »). Évaluation
complète : `research/HyperFrames-Evaluation-2026-09-19.md`. Le *skill* ne nous convient pas (il lit le
**code** d'un projet, et ses tons — parodie, chaotique, deadpan — saborderaient la crédibilité d'une
clinique). Mais ses **lois créatives** contiennent une règle mesurable et une micro-technique.

1. **ADOPTÉ — porte de lisibilité (loi dure).** « Toute ligne qu'un spectateur doit lire reste assez
   longtemps pour être lue : **label court ~0,8 s une fois posé ; une phrase ~0,3 s par mot.
   *Fast-in, then hold* — jamais *fast-in, then gone*. »**
   → **À vérifier automatiquement** : `compose.py` connaît la durée de chaque carte. Une carte qui reste
   moins longtemps que `0,3 s × nombre de mots` (ou moins de 0,8 s pour un label) = échec, au même titre
   que le portique mouvement §13. **Raison :** notre falaise est à 0:02 (§12) ; un texte qui fuit avant
   d'être lu est un texte qui n'existe pas.
2. **ADOPTÉ — la frame 0 est la vignette.** Choisir la **meilleure** image et la poser en frame 0, pour que
   la vidéo soit belle partout où elle apparaît. **Pourquoi ça compte ici plus qu'ailleurs :** notre canal
   de partage est **WhatsApp**, où la vignette décide du clic. Micro-gain, zéro coût.
3. **ADOPTÉ — le patron de 15–25 s, écrit noir sur blanc :**
   **Hook 2–3 s → Révélation 2–4 s → 2–3 points forts 5–12 s → Chute 2–4 s.**
   Notre V-05 (23,9 s) est déjà dans la cible — on écrit la structure au lieu de la deviner.
4. **REJETÉ — les tons parodiques du skill.** `yc-parody`, `chaotic`, `deadpan`, « fausse levée de fonds » :
   registre incompatible avec un laboratoire ou une école. **Seul `polished` est transposable.**
5. **REJETÉ — générer des visuels par IA pour « avoir de vraies photos ».** Même interdiction que
   le lot [20] : on peut générer une maquette **du site**, jamais une fabrication **de leur réalité**.

**Moteur évalué et installable :** HyperFrames (Apache-2.0) — voir §13 bis ci-dessous pour la piste
« mouvement réel ». `tools/video/install_hyperframes.sh` installé et testé (rendu 1080×1920/30 vérifié).

### 13 ter · HyperFrames — la piste pour sortir du diaporama (19 Sep 2026)
**Constat qui motive :** §13 a chiffré notre faiblesse (6/17 · 8/14 · 9/17 fenêtres figées) et §12 a
localisé la falaise à 0:02. **Le problème n'est pas le message, c'est qu'il ne bouge pas.**
**Ce qui a été testé :** HyperFrames rend du HTML/CSS/JS en vidéo, image par image, en local, sans compte
ni clé, avec **notre Chromium et notre FFmpeg** (`HYPERFRAMES_BROWSER_PATH`, `HYPERFRAMES_FFMPEG_PATH`,
`HYPERFRAMES_FFPROBE_PATH`). MP4 de test = 1080×1920, 30 fps, 300 images, H.264, audité par notre portique.
**Statut : ÉVALUÉ, PAS ADOPTÉ.** `compose.py` reste le chemin de production.
**Condition d'adoption — un essai, une fois :** produire **un** clip réel avec HyperFrames, le passer au
portique §13, et le comparer aux fenêtres figées de #2/#3/#4. **S'il ne bouge pas mieux, on abandonne.**
Aucune migration avant cette preuve.


## 11 · King's decisions (17 Sep 2026) — binding
1. **No real clinic/school name in any content without the owner's written permission.** Default: **anonymise** (blur/rename logos, addresses, unique details); the live *named* concepts (YAKS, Skye, OraCare, MITOC) are unlisted and shared only with their prospect — **no public content may show or link them**.
2. **Voice:** King agrees we **re-audition a voice before video #5** — **FAIT le 17 Sep (nuit)** : la voix des videos precedentes venait de **l'outil de voix de la plateforme d'AMK** (audition -> `voice-00`), pas d'un service externe ; `voice-00` est re-enregistree et narre V-05. Aucun telechargement de modele n'etait necessaire (piste Piper/HuggingFace abandonnee).
3. **#1 master** (`Instagram_vs_Website_v2.mp4`) is **not re-uploaded**; its TikTok status is recorded as **not posted**.
4. **Founding videos (repo, 15 Sep):** King confirms **only one of the four was posted — `clinic-founding-en.mp4` on TikTok**; the other three are unposted assets → integrated in the calendar (§A2).
5. **Strategy + calendar + shortlist: APPROVED.** **Video #4 is approved** — the remaining action is **posting** (King), first slot Tue 23 Sep TikTok / Wed 24 Sep IG, or earlier if King posts it with the outreach push.

## 12 · Lecture des analytics TikTok (17 Sep 2026) — les règles de la falaise à 0:02
**Source :** `content/pipeline/ANALYTICS-LOG.md` (captures TikTok Studio de King, 2 publications : « avant WhatsApp » 156 vues · fondatrice EN 121 vues). Chiffres de King uniquement.

1. **Loi des 2 secondes.** Les deux publications perdent l'essentiel de l'audience à **0:02** (rétention 18 % / 13 %). Sur TikTok, tout ce qui suit la seconde 2 est vu par ~1 spectateur sur 5. **Conséquence : le message entier doit tenir dans les 2 premières secondes, et il doit y avoir un mouvement + une voix dès la frame 1.**
2. **Aucun cadre figé à l'ouverture.** Vérifié : #4 tient une image immobile de 0:00 à 4,78 s (première coupe) ; la fondatrice EN fait une révélation lente. **Gate de production : première coupe ≤ 1,5 s, et le plan 0:00–0:02 contient du mouvement réel** (défilement de page, zoom lent, apparition d'élément — jamais l'UI démontrée elle-même, §3.8).
3. **Narration plutôt que musique seule (corrigé, King 17/09).** `clinic-founding-en.mp4` n'a **aucune piste audio dans le fichier** ; King y a ajouté **un son tendance TikTok à la publication** — la vidéo n'était donc pas muette, mais **sans voix**. Elle est dernière sur tout (3,8 s / 13 % / 1,4 % / 0 abonné) face à la vidéo **narrée** (6,2 s / 18 % / 4,35 % / +1). **Règle : chaque vidéo porte une narration — et le fichier livré doit déjà contenir sa piste audio** (`ffmpeg -i` doit l'afficher) ; un son tendance ajouté à la publication n'est pas un substitut (il ne dit rien et n'est pas réutilisable). Écart confondu par ailleurs → **indice fort, pas preuve**. Les 3 vidéos fondatrices non publiées restent **muettes : ne pas publier** (retirées du calendrier sur décision de King).
4. **Le premier cadre intéresse, la suite non.** Le plus de likes tombe à **0:00** (33 % / 80 %) — le hook visuel fonctionne. Ce n'est pas la promesse qu'il faut changer, c'est **ce qui se passe juste après**.
5. **Longueur : viser 15–22 s.** Avec 4–6 s de lecture moyenne, une vidéo de 29–34 s passe l'essentiel de sa durée devant des gens déjà partis. Test à faire (V-12 de la shortlist, déjà approuvée) : un payoff de 8–10 s.
6. **La falaise n'est pas un problème de diffusion.** Pour Toi = 87,5 % / 90,9 %, **100 % de non-abonnés** : TikTok nous échantillonne. Il arrête parce que la vidéo n'est pas regardée. Ne jamais lire ces vues comme un plafond d'algorithme.
7. **L'audience atteinte n'est pas l'acheteur.** 18–34 ans = 91 % / 86 % ; 35–54 ans = 8 % / 13 %. Le ton « dessin animé + annonce » classe le contenu en divertissement jeunesse. **Le message acheteur (propriétaire de clinique/école) passe aussi par le statut WhatsApp et la page Facebook** — là où ils sont réellement.
8. **Recherche = 0,0 %.** Aucune vue par recherche : légendes et mots-clés doivent porter les termes que l'acheteur taperait (site web clinique Douala, cabinet dentaire Bonamoussadi…).
9. **Rien à envoyer, rien à garder** : 0 enregistrement, 0–1 partage. Pour un contenu B2B, viser au moins une raison de « transmettre » (checklist, avant/après, chiffre vérifiable).
10. **Heure de publication : tenir 18:00–20:00 constant, sans conclure.** Le post de 19:25 bat celui de 12:02 sur toutes les mesures, mais les deux vidéos diffèrent aussi par l'audio et le contenu → **indice, pas preuve**. On garde l'heure fixe sur les 3 prochaines publications pour obtenir une comparaison propre.
**À ne pas faire :** publier un doublon (même script, nouvelle coupe) sur le même compte à quelques jours d'intervalle — vérifier d'abord le registre (`ANALYTICS-LOG.md` §question ouverte).

### 12 bis · Cadence de publication (réponse à King, 17 Sep)
**Règle dure :** jamais plus de **1 publication par plateforme et par jour** ; jamais le même fichier deux fois sur la même plateforme ; jamais deux publications à moins de **4 h** d'intervalle sur la même plateforme.
**Rythme de travail actuel : 3 TikTok + 2 Reels IG + 1 Shorts = 6/semaine au maximum**, à partir de **2 productions par semaine** (notre plafond réel : script + rendu + QA + validation de King + publication par King).
**Condition pour monter à 1/jour :** une vidéo doit d'abord **passer la porte des 2 secondes** — objectif interne : **lecture moyenne ≥ 12 s** ou **visionnage complet ≥ 15 %** (aujourd'hui 3,8–6,2 s et 1,4–4,35 %).
**Pourquoi pas plus maintenant :** la contrainte n'est pas l'offre de vues (TikTok échantillonne déjà ~120–160 vues par publication) mais la rétention ; poster 3× plus avec la même ouverture figée = 3× plus d'échecs, et deux publications rapprochées se partagent le même échantillon.

## 13 · PORTIQUE MOUVEMENT — « un zoom n'est pas du mouvement » (King, 17 Sep, après refus de la v04b)
**Déclencheur :** King a regardé le correctif de l'ouverture de #4 et a répondu : *« the difference isn't really noticeable it's just a zoom in »*. Il a raison. J'ai mesuré l'ensemble du catalogue :

| Fichier | Fenêtres de 2 s figées |
|---|---|
| `Video_04_Real_Website_PREVIEW.mp4` (#4, publié) | **6 / 17** (dont 0-2 s et 2-4 s) |
| `Video_04b_Animated_Opening.mp4` (mon correctif) | **4 / 17** |
| `Video_02_Five_Website_Answers.mp4` (#2, publié · TT 87) | **8 / 14** |
| `Video_03_Part_2.mp4` (#3, publié · TT 137) | **9 / 17** |
| `clinic-founding-en.mp4` (publié) | **5 / 14** |

**Constat : nos vidéos sont des diaporamas.** Le problème n'est ni le texte du hook, ni l'heure de publication : à l'intérieur de chaque beat, **rien ne bouge** — une image fixe avec une voix off. C'est ce qui explique la falaise à 0:02 mieux que n'importe quelle hypothèse de créneau.

**Règles (opposables) :**
1. **Portique obligatoire avant toute livraison vidéo :** `python3 tools/qa/audit_video_motion.py <fichier>` doit renvoyer **OK — mouvement présent dans chaque fenêtre**. Une fenêtre de 2 s sans changement visible = **BLOQUÉ**, on ne livre pas, on ne publie pas.
2. **Mouvement = quelque chose change à l'écran**, pas un recadrage lent. Sont du mouvement : un vrai défilement de page, une capture d'écran réelle, un tap, une coupe franche, une apparition d'élément. **Un push-in sur une carte fixe n'en est pas.**
3. **Interdit : recadrer une carte composée.** Vérifié sur la v04c : un zoom de 1,35× coupe « MAKE CONTACT EASY. » et la ligne du dessous. Nos cartes sont composées plein cadre → **toute coupe doit rester au cadre entier**, sinon le texte est tronqué (défaut éliminatoire).
4. **CORRIGÉ (17 Sep, nuit) — la matière première était accessible.** Je pensais qu'aucun navigateur ne pouvait tourner ici. Faux : `tools/shots/package.json` déclarait déjà **`@sparticuz/chromium`**, un paquet npm qui **embarque un Chromium compilé dans son archive** (aucun CDN à joindre), avec les couches `al2023`/`fonts` en `.tar.br` à extraire. Chaîne reconstruite et vérifiée → `tools/video/` (`install.sh`, `capture.mjs`, `compose.py`, `anonymise.py`). Voir aussi `research/Video-Toolchain-Research.md`.
   **Leçon de méthode :** avant de déclarer une capacité impossible, **lire l'outillage du dépôt** — il contenait la réponse depuis le 14 Sep.
5. **Conséquence de production :** un clip qui passe le portique et utilise de la vraie capture vaut mieux que dix cartes animées. **Bibliothèque de démos publiables :** `hosting/previews/demo/` — 5 concepts (réception polyclinique, maternité, dentaire, optique, clinique) anonymisés en fiction MboaCare, **0 fuite d'identité, audit HTML 0 anomalie**. On ne dépend plus d'une seule page.
6. **Pas de recadrage sur une carte composée** (zoom 1,3× = texte tronqué, vérifié). Le mouvement doit venir de la **capture**, ou d'une animation *dans* la carte (apparition, reflet, barre) — jamais d'un rognage.

## 9 · Changelog
- **v0.9 — 19 Sep 2026 :** évaluation `/brag` + HyperFrames (§10.4 lois créatives adoptées : porte de lisibilité 0,8 s / 0,3 s par mot, frame 0 = vignette, patron 15–25 s ; tons parodiques rejetés) + §13 ter piste moteur HyperFrames (évalué, non adopté, conditionné à un essai au portique). Source : `research/HyperFrames-Evaluation-2026-09-19.md`.
- **v0.8 — 17 Sep 2026 (nuit) :** V-05 produite avec narration (`voice-00` re-auditionnee) ; outil de voix identifie = plateforme AMK ; regle « le texte du hook doit tenir en entier dans sa carte » (un texte tronque a ete corrige) ; capture par plages (`--from-frac`/`--to-frac`), `--settle`, vitesse plafonnee a 420 px/s.
- **v0.7 — 17 Sep 2026 (nuit) :** chaîne vidéo reconstruite (§13 corrigé) — Chromium embarqué dans un paquet npm, capture réelle du défilement, cartes animées, bibliothèque de 5 démos publiables, portique mouvement bloquant ; recherche d'outillage complète dans `research/Video-Toolchain-Research.md`.
- **v0.6 — 17 Sep 2026 (nuit) :** §13 portique mouvement — toutes nos vidéos sont des diaporamas, le zoom n'est pas du mouvement, recadrer une carte coupe le texte, pas de capture possible dans cet environnement.
- **v0.5 — 17 Sep 2026 (nuit) :** corrections de King (narration vs son tendance ; #4 déjà publié ; fondatrices retirées) + §12 bis cadence de publication.
- **v0.4 — 17 Sep 2026 (soir) :** analytics TikTok de King absorbées (§12 — loi des 2 secondes, audio vérifié par décodage, ouverture immobile, audience ≠ acheteur, heure à tenir constante). Source : `content/pipeline/ANALYTICS-LOG.md`.
- **v0.3 — 17 Sep 2026:** batch-4 video-marketing lessons absorbed (§10.1–10.3) + King's binding decisions (§11) + script gates formalised in `content/scripts/README.md`.
- **v0.2 — 17 Sep 2026:** handover absorbed — fingerprint hexes, hard rules, production discipline, full technical failure log, evidence table, qualified earlier advice.
- **v0.1 — 17 Sep 2026:** created from King's brief + repo history + lesson batches.
