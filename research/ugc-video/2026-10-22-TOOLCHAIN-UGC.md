# UGC vidéo — recherche d'outillage, 22/10/2026

```
Commande  King : trouver/garder un outil qui produit de l'UGC réaliste, « au moins aussi bon que
          Google Flow », quitte à retourner-ingenierer un dépôt (morluto/rea).
Statut    recherche faite + moteur livré + limites mesurées (voir §6)
Portée    DM Optique d'abord, transposable à tout client
```

---

## 0 · Le verdict, en cinq lignes

1. **Aucun modèle de génération vidéo ne peut tourner dans ce sandbox** : 2 cœurs, **3 Go de RAM**,
   **pas de GPU**, et **HuggingFace est bloqué** (donc aucun poids de modèle). Ce n'est pas une
   préférence, c'est une mesure (§6.1).
2. **`morluto/rea` n'est pas un générateur vidéo.** C'est un serveur MCP de rétro-ingénierie de
   binaires et d'applications, avec un pont d'observation de navigateur. Il ne produit aucune image.
   Le détourner pour piloter Flow supposerait une session Google, un navigateur et une violation des
   conditions d'utilisation — et ne donnerait toujours pas de génération ici (§5).
3. **Google Flow n'a pas d'API publique.** Le modèle derrière, **Veo 3.1**, s'achète à la seconde via
   l'API Gemini (0,05 à 0,40 $/s, 9:16, 4/6/8 s, audio synchronisé). C'est la seule voie « qualité
   Flow » utilisable dans un pipeline (§3).
4. **Ce que je peux produire ici, ce soir, sans clé ni GPU** : de l'**UGC sans visage** de qualité
   broadcast — vraies photos de produit, mouvement, sous-titres incrustés, voix, carton de fin, portique
   de contrôle. C'est un genre qui performe réellement, pas un pis-aller (§2.3).
5. **La pièce qui manque — un humain à l'écran — devient un fichier d'entrée.** Le moteur l'accepte
   dans une scène `clip` : le jour où tu as une clé Veo/HeyGen, ou une séquence filmée au cabinet, elle
   entre dans le même montage sans rien réécrire.

---

## 1 · Ce qu'est un « UGC réaliste », techniquement

Trois couches, et les outils ne couvrent pas les mêmes :

| Couche | Ce que ça veut dire | Qui la fournit |
|---|---|---|
| **Le visage / la performance** | un humain qui parle, bouge, tient le produit | modèles vidéo (Veo, Kling, Hedra, HeyGen) |
| **La voix** | timbre, débit, accent, naturel | TTS (ElevenLabs, Gemini TTS, nos voix) |
| **L'assemblage** | rythme, sous-titres, cartons, produit, CTA, mesure | **personne ne le fait bien pour toi** — c'est 60 % du résultat perçu |

C'est la troisième couche qui fait la différence entre « une vidéo IA » et « une pub qui convertit ».
**C'est celle que je construis ici**, et c'est pour ça qu'un modèle plus fort ne suffit pas.

Ce que dit la recherche sur les performances (2026) :

- Les pubs IA se situent au **54ᵉ centile** de l'efficacité créative, contre **65ᵉ** pour les pubs non-IA
  (Kantar, *State of GenAI in Media and Advertising*, 2026) — un écart de 11 points, pas de 40.
- Sur du trafic froid, UGC humain et avatar IA sont **à 10–15 % l'un de l'autre en CPA** ; sur du
  retargeting, le témoignage humain garde **20–25 %** d'avance en conversion.
- Le **sans-visage** perd un peu au clic (pas de visage qui arrête le pouce) et **gagne au visionnage**
  (pas de motif « visage + sous-titre » que le spectateur a appris à scroller).
- Verdict opérationnel : **IA/UGC sans visage pour tester, humain pour scaler ce qui marche.**

---

## 2 · Le paysage des outils (octobre 2026)

### 2.1 Plateformes hébergées — « acteur IA qui parle »

| Outil | Ce qu'il fait le mieux | Prix d'entrée | Coût / vidéo 30 s | Réserve |
|---|---|---|---|---|
| **HeyGen** (Avatar V) | identité et synchro labiale tenues sur un long script ; 175+ langues | 29 $/mois (24 $ annuel) | ~0,10 à 1,16 $ selon le modèle d'avatar | rendu « présentateur », moins « filmé au téléphone » |
| **Arcads** | 300 à 1 000 « acteurs IA », style direct-response | ~110 $/mois (≈10 vidéos) | ~11 $ | cher au volume, pas d'essai gratuit |
| **Creatify** | URL → pub (produit → script → avatar) | 39 $/mois | ~3,90 $ | réalisme d'acteur en retrait |
| **Hedra** (Character-3) | animer **une seule photo** avec une voix | ~20 $/mois | non publié | parfait pour un mascotte/personnage, moins pour du réaliste |
| **Higgsfield** | plans cinématiques, produit → vidéo | 19–29 $/mois | ~3,19 $ (Seedance) | crédits brûlent vite |
| **Synthesia** | corporate, formation | 18–30 $/mois | — | **interdit les avatars stock en paid social sans accord écrit** |

### 2.2 Modèles ouverts — ce qu'ils exigent vraiment

| Modèle | Licence | VRAM minimale réelle | Usage |
|---|---|---|---|
| **Wan 2.2 TI2V-5B** | Apache-2.0 (code **et** poids) | 8 Go (GGUF/offload) à 24 Go officiel | texte/image → vidéo 720p |
| **Wan 2.2 S2V-14B** | Apache-2.0 | **80 Go documentés** | image + audio → personnage qui parle |
| **InfiniteTalk** | Apache-2.0 | 6 Go en 480p, 16 Go+ en 720p | photo + audio → tête parlante longue durée |
| **MuseTalk** | MIT (poids commercialisables) | **4 Go** en fp16 | lip-sync temps réel sur vidéo existante |
| **LatentSync 1.5 / 1.6** | Apache-2.0 | 8 Go / 18 Go | lip-sync diffusion, meilleure qualité |
| **EchoMimicV3** | Apache-2.0 | 12 Go | corps entier |

**Ce que ça veut dire** : la voie libre existe, mais elle demande **une machine à GPU** (8 à 24 Go) et le
téléchargement des poids — deux choses que ce sandbox n'a pas.

### 2.3 Le sans-visage — ce qui est réellement faisable ici

Un genre à part entière, documenté comme performant : la persona devient une **esthétique** (mains,
produit, décor, lumière) et non un visage. Trois raisons pour lesquelles c'est le bon point de départ
pour DM Optique :

1. **C'est vrai.** Les photos sont celles du cabinet, le produit est réel, la voix dit des choses
   vérifiables. Aucun risque d'« uncanny valley ».
2. **Ça contourne la dette des visages** (King et le docteur dans deux villes différentes) sans mentir
   au spectateur.
3. **Ça se mesure** : mêmes règles d'attribution (message WhatsApp pré-rempli), mêmes portiques.

---

## 3 · La voie « qualité Flow », chiffrée

Flow = interface web, **aucune API publique**. Le modèle s'achète autrement :

| Modèle (Gemini API) | 720p | 1080p | 1 clip 8 s en 1080p | Notre besoin (8 s + assemblage) |
|---|---|---|---|---|
| Veo 3.1 **Lite** | 0,05 $/s | 0,08 $/s | **0,64 $** | ~0,64 $ |
| Veo 3.1 **Fast** | 0,10 $/s | 0,12 $/s | **0,96 $** | ~0,96 $ |
| Veo 3.1 **Standard** | 0,40 $/s | 0,40 $/s | **3,20 $** | ~3,20 $ |

- Formats **16:9 ou 9:16**, 24 fps, **4, 6 ou 8 s** ; 1080p et 4K exigent 8 s.
- **Audio synchronisé inclus** dans le tarif « with audio » (l'API Gemini ne vend que cette variante).
- Ordre de grandeur pour un mois de DM Optique (8 posts de 23 s, un clip IA de 8 s chacun) :
  **≈ 5 $ en Lite, 8 $ en Fast, 26 $ en Standard** — hors assemblage, qui est gratuit ici.

**Recommandation** : **Fast en 1080p** pour les tests, **Standard** une fois qu'un script est prouvé.
Lite est tentant mais le mouvement est le premier truc qui trahit l'IA.

---

## 4 · L'architecture retenue

```
storyboard.json  ──►  tools/ugc/ugc.py  ──►  MP4 FINAL  ──►  portique mouvement
                          ▲     ▲
                          │     └── voix (TTS fournie ou générée)
                          └──────── clip IA (Veo / HeyGen / Hedra / InfiniteTalk) — optionnel
```

Le point clé : **le clip IA est une scène parmi d'autres**, pas le produit fini. On assemble toujours
autour : accroche, produit réel, preuve, sortie honnête, carton. C'est ce qui distingue une pub d'un
bout de vidéo générée.

Le moteur est **agnostique du fournisseur** : `tools/ugc/providers.py` décrit Veo (Gemini API), HeyGen,
Hedra et fal (Wan / InfiniteTalk), avec estimation de coût, et échoue **proprement** quand la clé
manque — jamais un faux succès.

---

## 5 · `morluto/rea`, examiné et écarté (avec les raisons)

Ce que le dépôt est, d'après son README et ses skills : **« Reverse Engineer Anything — One MCP for
reverse engineering across binaries, applications, and runtime behavior »**. Outils : analyse de
binaires natifs (pont Hopper/Ghidra), applications Apple/Android/Electron/Flutter, firmware, EVM, et
**observation de navigateur**. Skills : `reverse-engineer-anything`, `rea-tool-design`,
`rea-ci-tests-audit`…

| Idée | Réalité |
|---|---|
| « rea génère des vidéos » | non : il n'y a aucun modèle génératif dans le dépôt |
| « rea pilote Flow pour moi » | il faudrait un navigateur, **une session Google authentifiée**, et ça violerait les CGU de Flow ; le sandbox n'a ni l'un ni l'autre |
| « on inverse le modèle de Flow » | les poids ne sont pas distribués ; l'API est le seul accès, et elle est payante à la seconde |
| « on inverse un outil d'avatar » | même conclusion : soit API, soit poids ouverts (donc GPU) |

**Ce qui reste utile de rea** : rien pour cette tâche. Il est excellent pour comprendre un binaire ou
une app mobile — pas pour produire une vidéo. **Écarté, sans détour.**

---

## 6 · Les limites, mesurées (pas supposées)

### 6.1 Le sandbox

| Contrainte | Mesure |
|---|---|
| CPU | **2 cœurs** |
| RAM | **3 Go** (dont ~1 Go libre) |
| GPU | **aucun** (`/dev/nvidia*` absent) |
| `huggingface.co` | **bloqué** (`SSL_ERROR_SYSCALL`) → **aucun poids de modèle téléchargeable** |
| Réseau autorisé | `github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org` |

Même MuseTalk (4 Go de VRAM) est hors de portée : il n'y a pas de GPU du tout, et ses poids ne sont pas
joignables.

### 6.2 Ce que je peux garantir, et ce que je ne peux pas

| Promesse | État |
|---|---|
| Des vidéos UGC **sans visage**, 1080×1920, voix, sous-titres, portique vert, produites **ici** | ✅ fait, plusieurs fichiers |
| Un **humain IA réaliste** produit **ici** | ❌ impossible sans GPU ou sans clé API — je ne le simulerai pas |
| Le **même montage** avec un clip IA ou une séquence filmée en entrée | ✅ scène `clip`, testée |
| « Aussi bon que Flow » sur la couche visage | ✅ atteignable **via l'API Veo** (0,64 à 3,20 $ le clip) — pas ici |
| « Aussi bon que Flow » sur l'assemblage | ✅ déjà au-dessus : Flow n'assemble pas, ne sous-titre pas, ne mesure pas |

---

## 7 · Décision proposée

1. **Outil de référence : `tools/ugc/`** (ce dépôt) — il assemble, sous-titre, mesure, et accepte
   n'importe quel fournisseur de clips.
2. **Fournisseur de visage, quand tu voudras** : **Veo 3.1 Fast via l'API Gemini** (0,96 $ le clip de
   8 s en 1080p, audio inclus, 9:16 natif). C'est le meilleur rapport qualité/prix pour « qualité Flow ».
3. **Alternative sans carte bancaire** : **HeyGen** (29 $/mois, avatar V) pour un présentateur nommé —
   mais la recherche est claire : le présentateur `` lit « pub corporate », pas « recommandation ».
4. **La meilleure vidéo reste celle qu'on filme.** Une demi-journée au cabinet, une fois par mois, avec
   le docteur ou un agent : coût quasi nul, authenticité maximale, et le moteur l'assemble aussi.

---

## 8 · Sources

- Comparatifs UGC/avatars : heygen.com/blog (scores 2026), adtestbench.com/ai-ugc (coûts réels par
  30 s), pixo.video, rekreate.ai, outliercreator.com, hyperfx.ai.
- Modèles ouverts : github.com/Wan-Video/Wan2.2, therundown.ai/tools/wan2-2 (S2V 80 Go),
  github.com/TMElyralab/MuseTalk (4 Go fp16), latentsync (sync.so), infinitetalk.org, builderai.tools,
  thundercompute.com.
- Veo : ai.google.dev/gemini-api/docs/pricing ; cloud.google.com (tarifs Vertex, 9:16, 24 fps, 4/6/8 s) ;
  useapi.net/docs/api-google-flow-v1 (« Flow n'a pas d'API publique »).
- Performance : Kantar *State of GenAI in Media and Advertising* 2026 (54ᵉ vs 65ᵉ centile),
  ugccopilot.ai (sans-visage : hold rate vs CTR), tok-vibes.com (retargeting +20–25 %),
  tagshop.ai, devilab.eu.
- `morluto/rea` : README + `.agents/skills/` + `docs/` du dépôt, cloné et lu le 22/10.

**Réserves** : les prix des plateformes changent tous les mois et plusieurs pages se contredisent
(Higgsfield, Creatify) ; seuls les tarifs **Gemini API** sont sourcés sur la documentation officielle.
Les scores Kantar sont cités par des tiers, non relus à la source primaire.
