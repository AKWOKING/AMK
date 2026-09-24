# DM OPTIC — le message d'envoi de l'aperçu (24/09/2026, nuit)

**Pour qui :** M. Domche Noumbi, DM OPTIC, Douala — **656 122 239** (WhatsApp).
**Pourquoi maintenant :** il a répondu « **Ok Envoyé svp...** » à 15:54 ; la promesse du message du lot 4
(§7) était « je vous construis votre page, d'abord : vous l'ouvrez sur votre téléphone, vous décidez
après ». La page est construite (`demos/concept-dmoptic-v1.html`).

**AVANT D'ENVOYER :** le portique de déploiement. Le dossier `hosting/previews/dmoptic/` doit être
**en ligne** (`index.html` **et** `og.jpg`), puis `python3 demos/build_dmoptic.py --url https://<adresse>`
relancé et le dossier redéployé — sinon la vignette du lien est grise et l'adresse peut être fausse.
Une seule règle : **on n'envoie pas une adresse devinée.**

---

## 1 · Le message (à copier tel quel, après la carte du lien)

```
Votre cabinet a maintenant sa page : <ADRESSE>

Elle ne dit que ce qui est vrai aujourd'hui : votre inscription à l'Ordre depuis 2016
(n° 021/2016, arrêté 0382), le titulaire M. Domche Noumbi, votre numéro — et le fait
qu'un patient qui vous cherchait depuis son téléphone ne trouvait rien.

Je n'ai inventé ni adresse, ni horaires, ni photos : ces six informations sont marquées
« à confirmer » sur la page, et elles attendent vos réponses. Envoyez-les moi, elles
s'affichent le jour même.

Ouvrez-la sur votre téléphone, comme le ferait un patient. Dites-moi ce qui manque ou ce
qui est faux : je corrige aujourd'hui.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ce texte est écrit comme ça** (MESSAGES §1) : les six premiers mots — « Votre cabinet a
maintenant sa page » — sont **pour lui** ; le nom et le titre passent à la fin. Aucun prix, aucun délai,
aucune promesse de classement, aucun « site gratuit », et **pas un mot** sur ce que la page ne fait pas
encore.

## 2 · Les six informations qu'on attend de lui (et qu'on ne devinera pas)

| # | Le champ | Pourquoi il change la page |
|---|---|---|
| 1 | **Adresse exacte** + le point de repère (« en face de… », « à côté de… ») | c'est la question n° 1 d'un patient, et elle alimente le bouton d'itinéraire |
| 2 | **Horaires** (jours et heures) | deuxième question, et la première cause d'appel perdu |
| 3 | **3 ou 4 photos du cabinet** | elles remplacent les deux images d'illustration légendées « mise en situation » |
| 4 | **Moyens de paiement** (espèces, MTN MoMo, Orange Money) | évite au patient de venir sans pouvoir payer |
| 5 | **Assurances / mutuelles** prises en charge | décide le patient assuré, et le distingue de la concurrence |
| 6 | **Marques de montures** qu'il aime vendre | donne de la matière à la bande des actes |

## 3 · Ce qu'on veut savoir s'il répond par une question

- **« Combien ça coûte ? »** → la grille est celle de King, jamais improvisée dans la conversation :
  remonter la question à King avant de répondre un chiffre (règle des prix).
- **« Qui a fait ça ? »** → Akwo King / AMK, Douala. La page porte la mention « Aperçu préparé par AMK
  pour DM OPTIC » dans son bandeau de pied de page — elle est assumée.
- **« Pourquoi il n'y a pas mes photos ? »** → parce qu'on n'a pas le droit d'inventer un cabinet ; les
  deux images sont des mises en situation, et ses photos prennent leur place.

## 4 · Après l'envoi

- La réponse se traite **dans l'heure** et s'écrit dans `sales/Activity-Log.md` avec l'heure et le mot
  exact (règle §34.1 : une réponse humaine arrête l'horloge).
- S'il donne les six informations : `python3 demos/build_dmoptic.py --url <adresse>` → redéploiement du
  dossier → on lui renvoie la page complétée. **Un seul redéploiement par étape**, jamais en rafale.
- S'il ne répond pas : **aucune relance-reproche**. Le fil reste ouvert ; il a la page en main.
