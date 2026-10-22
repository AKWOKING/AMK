# hypit — moteur vidéo SVML pour agents (outil AMK)

**Audit-before-install (règle debout King), 21/10/2026 — verdict : INSTALLÉ (Apache-2.0 modifiée,
flux OUI-potentiel, rendu complet non testé au bac — dit plus bas).** Clone d'audit @ `0d36de9`
(18/10/2026, v0.3.1).

## Le verdict, en quatre cases

| Question | Réponse |
|---|---|
| **(a) C'est quoi** | Un moteur de production vidéo pour agents : on décrit la vidéo en **SVML** (ancrage aux mots, pas aux secondes), et le CLI `hypit` fait `check → plan → pricing → build` ; rendu en Chromium headless ; **modèles génératifs optionnels** (HypiHub ou autre, payants) — un workflow de captions, motion graphics et visuels code-rendus se compile **sans appel de modèle, donc sans coût de service** (lecture directe du README amont). |
| **(b) Licence : Apache-2.0 MODIFIÉE** (lue en entier) — **usage pour nos clients explicitement permis sans licence commerciale** (« using it for your own organization's work, including commercial work and work performed for your clients ») ; interdits sans accord écrit : **multi-tenant** (2ᵉ workspace hors organisation), **revente de l'outil**, **retrait du logo/copyright** des rapports CLI ; les outputs (vidéos, manifests) **nous appartiennent** (§3). |
| **(c) Flux : OUI-potentiel** — installé (`tools/hypit/install.sh`, npm `~/.npm-global`), **testé** : `hypit --version` → 0.3.1, `--help` → CLI complet. **Non testé au bac : le rendu complet** (build = Chromium + charge ; à prouver sur un cas réel). Ne remplace pas Hyperframes (moteur brag en production) ; candidat pour des formats à captions/motion (ex. UGC W1 TikTok) — **décision de King au moment venu**. |
| **(d) Vente : composant du service vidéo existant** (offre « vidéo d'annonce de livraison » + contenus TikTok) ; ne se vend pas seul. Coût réel d'un build à lire AVANT via `hypit pricing` (la licence amont l'impose d'affichage — on en fait notre garde). |

## Règles d'usage AMK (non négociables)

1. **Jamais cloner la vidéo réelle d'un créateur** pour un client : le positionnement amont
   (« clone any viral video ») sert à répliquer une STRUCTURE ; chez AMK, la structure s'inspire,
   le contenu reste à nous — verrous « que du vrai », pas de visages IA (R2), musique générée ou
   licenciée seulement.
2. Chaque build : `hypit check` puis `hypit pricing` d'abord — aucun build sans coût lu.
3. Le logo/copyright amont dans les rapports/manifests CLI **reste en place** (clause 1c licence).
4. Pas de déploiement multi-tenant, jamais de revente de l'outil lui-même.
5. Toute sortie vidéo passe les portiques habitude (`audit_video_motion`, lecture téléphone) avant
   envoi client ; rien n'est publié sans validation de King.

## Installation

```bash
bash tools/hypit/install.sh
```

`npm install -g --prefix ~/.npm-global @hypit/hypit` + preuve `hypit --version`. Épinglé par
version de paquet (0.3.1). Le skill amont (`npx skills add hypit-ai/hypit`) n'est **pas** installé
— le CLI fait foi, pas de double mécanisme (règle 5 TOOL-SCAN).
