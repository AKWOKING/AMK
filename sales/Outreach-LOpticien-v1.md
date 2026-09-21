# OUTREACH — L'OPTICIEN (Bali, Douala) · 670 27 60 65

**Statut : PRÊT À ENVOYER (17/09 au soir).** Il ne manque que : déployer `hosting/previews/` → `amk-cm.vercel.app/opticien/`, QA téléphone, puis envoi. Concept audité : 0 trouvaille structure/contraste (`tools/qa/audit_html.py`).
Concept : `demos/concept-opticien-v1.html` (générique « Votre Opticien ») · Image : `demos/shots/mockup-opticien-wa.jpg` (165 KB) · Dossier : `clients/l-opticien/` (portes §8b, douleurs, design).

## 0 · Portes §8b (RESEARCH-STANDARD) — 3/3 ✅
A joignabilité : WhatsApp **Business** « L'Opticien », profil + catalogue actifs, vu aujourd'hui · B intention digitale : compte pro tenu, catalogue, horaires renseignés · C acheteur : mono-boutique, SARL → propriétaire.

## 1 · Message 1 — **image d'abord**, puis ce texte (copier-coller)

> Bonjour 👋 Depuis le 1ᵉʳ juillet, les verres ont un prix plafonné au niveau national, et 80 boutiques d'optique clandestines ont été fermées à Douala et Yaoundé. Pour un opticien en règle, c'est le moment où les clients regardent qui est sérieux — et sur Google, votre boutique ne sort pas.
> Je suis Akwo King, développeur web à Douala. J'ai préparé un aperçu : contrôle de la vue sur rendez-vous, choix de la monture selon la forme du visage, devis verres reçu sur WhatsApp avant de se déplacer.
> Je vous l'envoie ? Un simple « oui » suffit — vous regardez une minute sur votre téléphone, sans engagement.
> — Akwo King / AMK – Développement Web & Solutions Digitales

**Pourquoi ça marche :** la 1ʳᵉ ligne (visible dans la notification) est un fait local daté, pas une vente · aucune promesse de prix ou de délai de livraison · la question finale est une micro-question à un mot · « sans engagement » en dernière ligne seulement.

## 2 · Check avant envoi
- [ ] Preview déployée + **QA téléphone** (le sandbox n'a pas de navigateur) — miroir animé, FR/EN, liens WhatsApp, taille sur 3G
- [x] **Numéro réel intégré** : variante `demos/concept-opticien-lopticien.html` construite avec `python3 demos/build_opticien.py --wa 237670276065 --out concept-opticien-lopticien.html` — les 8 liens `wa.me` et le libellé « +237 670 27 60 65 » sont dedans ; le fichier générique garde le placeholder. C'est cette variante que sert `hosting/previews/opticien/`.
- [ ] Image `mockup-opticien-wa.jpg` envoyée **avant** le texte
- [ ] Fenêtre 09–21, pas de relance avant M+2

## 3 · Après « oui » (dans l'heure)
1. Lien + l'image une seconde fois : « Voici : <lien> — c'est un aperçu, pas encore votre site. »
2. Deux questions seulement : « Je mets votre **vraie ligne** et vos **photos** ? » + « Vous préférez être appelé comment ? »
3. Ce qu'on attend de lui : logo, photos boutique/montures, horaires réels, adresse exacte, liste des services, numéro WhatsApp définitif.
4. Ensuite : « Je vous laisse le lien 3 jours, puis je vous dis ce qui serait différent sur votre site à vous. » (pas de prix en message 1 ni 2)

## 4 · Objections probables
| Il dit | Réponse |
|---|---|
| « J'ai déjà Facebook / WhatsApp Business. » | « Vos clients actuels vous trouvent. Ceux qui **cherchent** “opticien Douala” ou “contrôle de la vue Douala” sur Google, non. C'est un autre flux. » |
| « Combien ça coûte ? » | Annoncer 100 000 FCFA, 50 % au départ, 50 % à la livraison — jamais de rabais. |
| « Je n'ai pas le temps. » | « Vous m'envoyez 6 photos et votre adresse, je fais le reste. Vous validez sur votre téléphone. » |
| « Les prix ont changé (ONOC). » | « Justement : votre site peut expliquer le référentiel et donner un **devis écrit** — c'est ce qui vous distingue des clandestins. » |
| « J'ai déjà un site. » | Il n'en a pas (vérifié). Ne jamais l'affirmer de travers : « Je n'en ai pas trouvé. » |

## 5 · Relances (max 3)
- **M+2 (sam 19/09)** : « Un mot : vous voulez que je vous envoie l'aperçu ? »
- **M+4 (lun 21/09)** : le lien renvoyé seul + « Il reste en ligne jusqu'à mardi. »
- **M+7 (jeu 24/09)** : clôture douce : « Je le laisse de côté. Si un jour vous voulez être visible sur Google, écrivez-moi. »

## 6 · À ne jamais dire / écrire
« Vous n'avez pas de site » (dire « je n'en ai pas trouvé ») · un prix de verre inventé · « dépistage gratuit » (c'est l'offre de Golden Eyes) · une marque qu'il ne vend pas · un faux témoignage · un délai de livraison qu'il n'a pas confirmé.
