# Brag plan — DM OPTIQUE SARL (brouillon de livraison, §1f②)

- **Ton :** `polished` (santé) · **Format :** vertical 1080×1920 · **Durée :** 20 s · **Langue :** FR
- **Matière :** captures RÉELLES du site construit (`hosting/previews/dmoptic/` @ `8cb43bc`),
  pages accueil / catalogue femmes / fiche F01 / examen — aucune donnée inventée, aucune
  fausse statistique, aucun prix (verrous).
- **Couleurs/polices :** celles du site — marine `#0A1220`, crème `#F6EBE0`, Schibsted Grotesk +
  IBM Plex Mono (@font-face locaux).
- **Musique :** nappe générée ffmpeg (libre AMK) ajoutée après rendu — la piste embarquée de brag
  (ende.app) reste interdite (licence non documentée).

| # | Scène | t | Mouvement continu |
|---|---|---|---|
| 1 | HOOK — « Votre opticien est en ligne. » + dmoptiquesarl.com | 0–3,0 s | entrée 0,7 s + zoom lent 1,0→1,07 |
| 2 | LE CABINET — capture accueil réelle (hero + carte) | 3,0–8,0 s | panoramique −16,5 % + zoom 1,05 |
| 3 | CATALOGUE — capture grille femmes réelle | 8,0–13,0 s | panoramique −23 % + zoom 1,05 |
| 4 | EXAMEN — capture page examen réelle | 13,0–16,5 s | panoramique −20 % + zoom 1,05 |
| 5 | OUTRO — DM OPTIQUE SARL · dmoptiquesarl.com · WhatsApp | 16,5–20 s | entrée + zoom lent |

**Portiques dans l'ordre :** `hyperframes check` 0 erreur → `snapshot --at` relu à l'œil →
`render --quality looks` → musique mux ffmpeg → poster frame 0 → `audit_video_motion.py` OK →
lecture téléphone par King (portique final). **Rien n'est envoyé au client sans validation de King.**
