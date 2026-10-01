# Protocole — tester nos pages au LECTEUR D'ÉCRAN (5 minutes, à la main)

**Pourquoi ce document existe.** L'audit automatique (`tools/qa/audit_a11y.py`) vérifie ce qui se lit dans
le code : les alts, les étiquettes, les repères, l'ordre des titres. Il ne peut pas dire ce qu'une personne
**entend**. Les sources du lot [28] — le tutoriel NVDA de *Software Testing 101* et l'article de Kortic sur
les formulaires — montrent la même chose par deux chemins : un lecteur d'écran annonce « page blank » sur une
page pleine, ne dit pas à quel groupe appartient une case à cocher, et n'annonce **aucune** erreur quand le
formulaire en contient une. Ces trois pannes-là ne se voient qu'à l'oreille.

**Qui le fait :** King (5 minutes, une fois par page livrée) — ou en séance, devant le client, comme
démonstration. **Quand :** avant de livrer une page, et après toute refonte.

---

## 1 · S'équiper (une fois)

| plateforme | lecteur | où | prix |
|---|---|---|---|
| Windows | **NVDA** | nvaccess.org | gratuit, libre — c'est celui du tutoriel |
| Android (**le téléphone de nos clients**) | **TalkBack** | Paramètres → Accessibilité → TalkBack | préinstallé |
| iPhone | VoiceOver | Réglages → Accessibilité | préinstallé |

**Astuce pour voyants** (du tutoriel NVDA) : dans `Préférences → Vision`, cocher **Visual Highlight**. Trois
couleurs apparaissent alors : **bleu** = ce qui a le focus clavier, **rouge** = le curseur de lecture, **jaune**
= le curseur de revue. On VOIT alors ce que le lecteur d'écran lit — c'est ce qui rend le test possible pour
quelqu'un qui voit.

## 2 · Les huit touches qui comptent (NVDA)

| touche | ce qu'elle fait | ce qu'une panne donne à l'oreille |
|---|---|---|
| **Tab** / **Maj+Tab** | élément interactif suivant / précédent | un élément sauté, ou un bouton annoncé « bouton » sans nom |
| **D** / **Maj+D** | repère suivant / précédent | **« page blank »** : la page a un menu et un pied de page, et rien au milieu |
| **H** / **Maj+H** | titre suivant / précédent | « niveau 3 » juste après « niveau 1 » (un niveau manquant) |
| **K** / **Maj+K** | lien suivant / précédent | un lien annoncé « lien, ici » : on ne sait pas où il mène |
| **F** | champ de formulaire suivant | « champ de saisie, vide » sans le nom du champ |
| **B** | bouton suivant | « bouton » tout court |
| **NVDA+Tab** | où suis-je ? | après avoir fermé une fenêtre, on a perdu le focus |
| **Ctrl** (arrête) / **Maj** (pause) | contrôle de la voix | — |

## 3 · Ce qu'on doit entendre sur NOS pages

### Site AMK — `site/index.html` (269 textes)

1. **Premier Tab** → « *Aller au contenu, lien* » (le lien d'évitement, en première position).
2. **D** → « *contenu principal* » (repère `main`), puis la navigation, l'en-tête, le pied de page.
3. **H** → le titre est annoncé **une fois**, puis 44 titres suivent l'ordre sans sauter de niveau.
4. **K** → chaque lien se comprend **seul** : « *Site web pour école* », pas « *en savoir plus* ».
5. **F** → « *École ou clinique, champ de saisie* » (l'étiquette est attachée au champ).
6. **Le test qui compte** : cliquer « Recevoir mon aperçu » **sans rien écrire** → la voix doit dire
   « *Il manque le nom de votre établissement… vous êtes sur  Nom de l'école ou de la clinique, champ de saisie,
   non valide* ». Si la voix ne dit rien, la correction a été perdue.

### UNI-LABO — `demos/concept-unilabo-v2.html` (385 textes, 25 champs)

1. **D** → contenu principal, navigation, en-tête, pied de page.
2. **F** puis **Tab** → la première case cochée doit être annoncée avec **son groupe** :
   « *1 · Vos analyses, groupe de cases à cocher* », puis « *Biochimie — Glycémie, case à cocher, non cochée,
   1 sur 19* ». **Sans le nom du groupe**, on entend des cases isolées et on ne sait pas ce qu'on coche.
3. **Tab** sur `FR` / `EN` → « *bouton, appuyé* » : l'état de la langue est annoncé, pas seulement colorié.
4. **Le test qui compte** : cocher une analyse, écrire un nom, choisir un moment → le bouton d'envoi doit
   s'annoncer comme **activé** ; laisser un seul élément manquant → la page doit dire **ce qui manque**.

### Les deux pages de langue (école / clinique)

**D** → repère principal ; **K** → les liens sont explicites ; **F** → aucun champ sans nom.

## 4 · Sur téléphone Android (TalkBack) — le test qui parle à nos clients

**Activer :** les deux touches de volume **enfoncées 3 secondes** (ou Paramètres → Accessibilité → TalkBack).

**Gestes :** balayer à **droite** = élément suivant · **gauche** = précédent · **double tap** = activer ·
**deux doigts** = faire défiler · **trois doigts** = aller vite.

**Les trois questions à se poser sur notre page :**

1. **Tout se trouve-t-il au balayage ?** Chaque bouton, chaque case, chaque lien — un élément invisible au
   balayage est un élément perdu. *(C'est ce que le module TalkBack-NVDA du lot [28] rappelle : sur Android,
   on explore élément par élément, avec un son par objet.)*
2. **Le double tap ouvre-t-il WhatsApp ?** C'est le cœur de notre promesse : bouton → WhatsApp pré-rempli.
   Si le double tap ouvre une fenêtre vide, tout l'édifice tombe.
3. **Les étiquettes tiennent-elles à l'oreille ?** « *Nom de l'école* », puis le champ. Pas « *champ de
   saisie* » tout court.

## 5 · Ce qu'on note, et où

| quoi | où |
|---|---|
| une panne trouvée | `sales/Activity-Log.md`, datée, avec la phrase exacte entendue |
| une page validée à l'oreille | la même ligne, un mot suffit : « NVDA : OK, lu en 4 min » |
| en séance client | `clients/<client>/AUDIT-*.md` — et dans le dossier si le client pose la question |

**On n'écrit jamais « certifié accessible ».** On écrit ce qu'on a entendu, sur quelle page, avec quel lecteur
et quelle version. C'est la même règle que pour les mesures : **un chiffre qu'on n'a pas pris soi-même n'entre
pas dans un rapport.**

## 6 · Les limites de ce protocole, écrites noir sur blanc

- **Aucun de nous deux n'est un utilisateur de lecteur d'écran expérimenté.** Nous testons la mécanique, pas
  l'usage réel : un utilisateur aveugle de longue date va plus vite et remarque autre chose.
- **Nous testons avec une page à nous**, jamais avec la vraie page du client (les statuts de compte, la saisie
  d'un vrai rendez-vous, la réception d'un vrai message WhatsApp : cela ne se teste pas en démonstration).
- **Ce protocole ne remplace pas l'audit automatique** : il le complète. L'un trouve les 90 % mécaniques,
  l'autre dit ce que ça donne à l'oreille.
