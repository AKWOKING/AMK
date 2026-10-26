# Brag plan — Dr Ophtalmo (brouillon de livraison, §1f②)

- **Ton :** `polished` (santé — les tons `app-store`/`polished` sont les seuls admis) · **Format :** vertical
  1080×1920, 30 fps, H.264 + AAC · **Durée :** 20 s · **Langue :** FR (le site est bilingue, la vidéo parle
  au médecin d'abord, puis à ses patients sur WhatsApp)
- **Matière :** **captures réelles du site construit** (`hosting/previews/dr-ophtalmo/` @ `f177b6c`), prises
  en Chromium à 540 × 960 @2×, défilement lent, lazy-load déclenché : hero, parcours, lieux, semaine,
  formulaire. Aucune maquette, aucune capture d'un autre site, aucune personne générée présentée comme le
  médecin (les images du site portent déjà leurs légendes « image générée »).
- **Couleurs / polices :** celles du site — marine `#07111d`, teal `#76b9b4`, crème `#f6f8fa` ; Newsreader +
  Inter Tight en woff2 **locaux** (aucun appel réseau au rendu).
- **Musique :** nappe générée par ffmpeg (accord C–E–G–A, `aecho`, fondus), ajoutée après rendu. La piste
  embarquée de brag (ende.app) reste **interdite** — licence non documentée (issue #59).

| # | Scène | t | Mouvement continu |
|---|---|---|---|
| 1 | HOOK — « Où consulter ? » puis « Un médecin, quatre lieux. » | 0–3,6 s | entrée + zoom lent, halo radial qui dérive |
| 2 | 01 · LE SITE — capture réelle du hero | 3,6–8,0 s | panoramique vertical + zoom 1,05 |
| 3 | 02 · LA SEMAINE — capture réelle, **« Horaires à confirmer » visible à l'écran** | 8,0–12,4 s | panoramique + grille en dérive |
| 4 | 03 · LES LIEUX — capture réelle des quatre lieux numérotés | 12,4–16,8 s | panoramique + zoom |
| 5 | GÉNÉRIQUE — « Votre vision, ma priorité. » + 4 villes + « Aperçu privé, non publié » | 16,8–20 s | générique animé (y −46, échelle 1,075) + halo |

**Ce que la vidéo ne dit pas :** aucun nom de médecin, aucun horaire précis, aucun numéro, aucun prix,
aucun avis, aucune disponibilité en temps réel, aucune inscription à l'Ordre. Elle ne dit pas non plus
« voici un beau site » : elle dit « voici où l'on consulte cette semaine — et tout ce qui reste à
confirmer est écrit dessus ».

**Portiques, dans l'ordre :** `hyperframes check` **0 issue, 19/19 AA** → `snapshot --at 1.6,5.2,9.6,13.9,18.4`
relu à l'œil → `render --quality looks` → musique mux ffmpeg (`-c:v copy -c:a aac`) → poster extrait à
18,4 s (séparé, **jamais** en `attached_pic`) → `audit_video_motion.py` **OK sur les deux fichiers**
(fenêtre la plus faible 1,93) → **lecture téléphone par King (portique final)**.

**Livrables** (hors dépôt, trop lourds pour Git) :

```text
/home/user/brag-output-dr-ophtalmo/brag.mp4            10,4 Mo  4 Mbps  (lecture, ordinateur)
/home/user/brag-output-dr-ophtalmo/brag-whatsapp.mp4    2,28 Mo  crf 26  (statut WhatsApp)
/home/user/brag-output-dr-ophtalmo/poster.jpg          1080×1920, t = 18,4 s
```

**Rien n'est publié, rien n'est envoyé au médecin sans validation de King** (règle brag AMK).
