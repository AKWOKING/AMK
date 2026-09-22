# FEUILLE D'ENVOI · UNIVERS OPTIQUE (Bépanda, Douala) — mardi 22/09/2026, soir
**Objet : la v3 est prête. Deux fichiers, deux lecteurs. Le créneau se calcule tout seul.**

À King, pas au client. Ce qui est écrit ici ne part pas dans la page.

---

## 1 · Ce qui a changé depuis ce matin (les deux reproches du roi)

| Ce qu'il a dit | Ce qui a été fait |
|---|---|
| « the things written on the site shows like we trying to tell what is and what was before the site… the objectif of the site is so clients find, him his services, increase trust and they book easily » | Le fichier **public** ne parle plus qu'au client : trouver ce qu'on cherche, ce qui se passe à la boutique, quoi apporter, où nous trouver, écrire pour un créneau. Les six constats, le 3,3 sur six avis, le comparatif, les questions à trancher et la liste des photos manquantes **restent** — dans la **note au cabinet**, absente du fichier public. Un contrôle refuse que le vocabulaire du dossier fuie dans la page. |
| « are they dynamique??, do they auto update ? » | **Non, et c'était une vraie faute** : cinq dates tapées à la main. Elles sont parties. Cinq journées sont calculées par la page à l'ouverture, à partir de la grille d'horaires du comptoir : le dimanche n'est jamais proposé, une journée entamée saute s'il reste moins de deux heures, chaque pastille est un lien WhatsApp réel avec le message déjà écrit. Sans JavaScript, le bloc se retire et le vrai chemin (numéro + horaires) reste lisible. **Aucune date n'existe dans aucun fichier** — un contrôle le refuse. |
| (non demandé, trouvé en chemin) | Les boutons WhatsApp portaient le numéro **sans indicatif** (`wa.me/699252874`) : l'API exige le format international, donc l'appel à l'action de la version de ce matin ouvrait « numéro invalide ». Corrigé en `+237` et désormais contrôlé à la construction. |

Le visuel n'a pas bougé : « I love the designs of V2 » est pris au mot — mêmes rendus, mêmes tons
(papier #FBF6EC, encre #1E1A15, rouille #A94C23, pétrole #12303F), Newsreader + Public Sans +
JetBrains Mono, même budget de révélation (3 blocs animés sur 44).

## 2 · Les fichiers — à envoyer, et celui qui ne part pas

| Fichier |_octets_ | sha256 (16 premiers) | Destinataire |
|---|---|---|---|
| `demos/univers-optique-site-v2.html` | **718 514** (702 Ko) | `ec91063bbe80604b` | **le cabinet** — le site seul, tel qu'un client le lit |
| `demos/univers-optique-site-v2-sobre.html` | 66 676 (65 Ko) | `e3d9243bd376fac0` | repli si WhatsApp refuse la pièce jointe (même copie, 0 visuel) |
| `demos/concept-univers-optique-v2.html` | 755 254 (738 Ko) | `b6ef949f2d74496c` | **toi + le cabinet, à ta main** — le site + la note au cabinet. Ne l'envoie que si tu veux qu'ils voient le dossier |
| `demos/concept-univers-optique-v1.html` | 740 056 | — | le dossier v1, **à ne plus envoyer** |

**Ce matin, c'est `concept-univers-optique-v2.html` (734 727 o) qui est parti.** Si le cabinet a déjà ce
fichier en main, n'envoie pas les trois : envoie le site (718 514 o) en disant « la version pour vos
clients, celle d'hier restait notre brouillon » — une ligne, pas une excuse.

**Vérification avant d'envoyer (30 secondes, personne d'autre ne peut la faire)** : ouvre le fichier sur
ton téléphone, touche une pastille de créneau et un « Écrire au comptoir ». Ça doit ouvrir **une
conversation avec Univers Optique** (699 25 28 74) avec le message préécrit. C'est le seul point que ce
bac ne peut pas prouver — il n'a pas de navigateur.

## 3 · Le chemin réel, pas un lien

```
/home/user/AMK/demos/univers-optique-site-v2.html
```

`amk-cm.vercel.app/univers/` répond **404** tant que TU ne déploies pas : n'envoie **aucun lien**, envoie
**le fichier**. La page se peint sans JavaScript ; le JS n'ajoute que l'animation d'apparition, le
basculement FR/EN et les créneaux. **Si l'écran semble vide ou coupé** : téléchargement tronqué —
vérifier les **718 514 octets** et `ec91063bbe…` avant de répondre à la remarque.

## 4 · Message à coller (FR, WhatsApp)

> Bonjour, la version que vous attendiez est prête — un seul fichier HTML, à ouvrir dans un navigateur
> (téléphone ou ordinateur), rien à installer. Vous y trouverez votre salle de vente, ce qui se passe
> à la boutique pour un client qui arrive avec une ordonnance ou une monture cassée, ce qu'il faut
> apporter, comment vous trouver rue de Bépanda, et un moyen simple de poser un rendez-vous : les
> horaires affichés sont ceux de votre comptoir, et les créneaux proposés se recalculent tout seuls
> chaque jour — rien n'est écrit à l'avance par moi. Le tout existe en français et en anglais.
> J'y ai joint aussi une note interne (notre brouillon) avec les six points que vous êtes seuls à
> pouvoir trancher, et ce que nous n'avons pas pu vérifier : nous ne l'avons pas inventé, nous le
> demandons. Les visuels sont des rendus de concept : vos propres photos les remplaceront.
> Le cadre reste le même que celui que vous avez demandé : 100 000 FCFA, 50 % à la signature, 50 % à
> la livraison, hébergement et nom de domaine non compris.

**Version courte**, si le cabinet n'aime pas les pavés :

> Votre page est prête (fichier HTML ci-joint, à ouvrir dans un navigateur). Elle parle à vos clients :
> ce que vous faites, quoi apporter, où vous trouver, et le rendez-vous — les créneaux se recalculent
> tout seuls, le dimanche n'est jamais proposé. FR et EN dans le même fichier. Note interne jointe : six
> points sont à trancher par vous avant publication. Cadre inchangé : 100 000 FCFA, 50/50.

**EN**, si c'est la version anglaise qui circule :

> Hello, the version you were waiting for is ready — one HTML file, opened in any browser. It shows your
> showroom, what happens in the shop for someone arriving with a prescription or a broken frame, what to
> bring, how to find you on rue de Bépanda, and a simple way to book: the hours shown are your counter's,
> and the slots are recomputed on the day — nothing is pre-written by me. French and English in the same
> file. A short internal note is attached with the six points only you can settle. Terms unchanged:
> 100 000 FCFA, 50 % at signing, 50 % at delivery, hosting and domain not included.

## 5 · À ne pas écrire

- « **absent du web** » — faux : il y a eu un site, mort le 9 janv. 2024.
- « **15 %** » comme une offre — elle existe sans date de fin : c'est **une question**, pas un argument.
- un **témoignage**, une **note en étoiles**, un **avant/après** clinique : nous n'en avons aucun à vérifier.
- un prix nouveau : **100 000 FCFA, 50/50** est la réponse déjà faite à sa question du 21/09 18:08 — à
  **maintenir**, pas à réécrire.
- « **nous avons corrigé nos erreurs** » — rien de tout ça ne se dit au client. Ce qui se dit : la page
  est prête, elle travaille pour vous.

## 6 · Ce qui reste dû, dans l'ordre

1. **Sa réponse** sur la direction (v3) et sur les six points de la note — rien n'est publiable sans ça.
2. **Photos réelles** : les six que la note réclame (façade avec l'enseigne, salle de vente au jour,
   atelier, ordonnance en main, équipe, vérificateur de lunetterie). Tant qu'elles manquent, les rendus
   disent « rendu de concept » — ils ne se font pas passer pour des photos du cabinet.
3. **LE CRISTALLIN** : sa réponse **A / B** (page seule 100 000 · page + page Facebook 50 000) — relance
   prévue le 23/09, et lui renvoyer `demos/concept-le-cristallin-v1.html` (620 492 o), sa copie du
   dimanche étant cassée.
4. **Feuille de leads** : le *Follow-up date* d'Univers passe du 22/09 au **23/09** dès ce
   fichier envoyé — à changer dans `leads/build/crm.py`, bloc `ETAT_21_2209`, **jamais dans
   `leads/CRM.csv`** (c'est une sortie : le 22/09 à 08:31, un `rebuild.sh` a effacé l'état qui n'y
   figurait qu'à la main). Puis `bash leads/build/rebuild.sh`.)
5. **Envoi** : je ne touche à aucun compte — les messages sont prêts ci-dessus, le déclencheur reste à toi.

---

### Contrôle passé sur cette v3 (pour ta garantie, pas pour le client)

92 lignes de contrôle dans le générateur, **0 faute** · **10/10** fautes injectées **refusées** (chaque
faute nommée, fichiers livrés comparés avant/après) · moteur rejoué sur **six instants figés** (mardi
après-midi, après 17h, samedi, dimanche, 28 décembre en bascule d'année, mardi en anglais) : étiquettes,
liens, messages et état du comptoir vérifiés à chaque fois · `audit_html.py` **0 finding** sur les trois
fichiers · `check_inline_js.py` 5 blocs, 0 faute · `diff` démo ↔ aperçu **0 ligne** sur `/univers/`
(le site), `/univers-note/` (le document de travail) et `/univers-v1/`.
