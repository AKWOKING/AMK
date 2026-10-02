# GABARIT DE TÂCHE — Carrousel (livrable récurrent)

> `ops/` créé le 02/10 (KB §9, pilier 3). Pattern : déclencheur · rôle · entrées · sous-tâches · heures ·
> sortie · exception · succès. Ce gabarit élimine le « qu'est-ce que je dois faire ? ».

**Déclencheur :** semaine de cadence du client (DM OPTIQUE : 1 carrousel/semaine dès semaine 1 pour ce qui
est produisible).

**Rôles :** orchestrateur = production + QA interne · King = approbation finale avant envoi client.

**Entrées requises (rien ne démarre sans) :**
1. Les mots du client (playbook Part H / dossier client / verbatims publics datés).
2. `clients/_uniqueness-registry.md` (ce qui a déjà été fait pour ne pas se répéter).
3. `design/STYLE-TOKENS.md` + `AMK-DESIGN-SKILLS.md` (dials, anti-slop, type, couleur).
4. Le message-variante pré-rempli WhatsApp correspondant (CTA → WhatsApp, jamais vers du vide).

**Sous-tâches :**
1. Une idée = une slide ; hook sur la première (le lecteur décide en 1 s).
2. Copy FR d'abord, EN ensuite si le client est bilingue ; 2–3 phrases max par slide.
3. Dernière slide = CTA WhatsApp avec la chaîne pré-remplie.
4. **Gate R1 :** aucun claim médical / symptôme / soulagement ; aucun concurrent nommé ; aucune remise ;
   aucun témoignage ou classement inventé ; santé : ne jamais nommer une conséquence.
5. QA interne (orchestrateur relit, §Review de `ops/LIFECYCLE.md`) → puis client.

**Heures estimées :** angle+copy 1 h · design 1 h · QA 0,5 h · déclinaison client 0,25 h.

**Spec de sortie :** dimensions/placements selon `design/STYLE-TOKENS.md` · texte complet en légende ·
chaîne WhatsApp pré-remplie par variante livrée avec.

**Exception :** mots du client insuffisants → sources publiques vérifiées et datées (registre, annuaire),
jamais d'invention ; si rien : le carrousel attend (un carrousel faux coûte plus qu'un carrousel tardif).

**Succès :** gate R1 passée · QA interne passée · client n'a rien reçu avant relecture interne.
