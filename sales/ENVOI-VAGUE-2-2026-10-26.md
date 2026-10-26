# ENVOI — VAGUE 2 · les sept qui ont les trois portes (26/10/2026)

```text
PORTE    python3 tools/qa/audit_outreach.py sales/ENVOI-VAGUE-2-2026-10-26.md --strict
         → 0 bloquant, 0 avertissement (§13 : ≤ 55 mots, une question, dédouanement, action finale)
SOURCE   leads/VERIF-2026-10-27.md §1 — sept cabinets à 3/3, capture du 25/10, titulaire nommé au CRM
CADENCE  les sept partent le 27/10, en tête du palier de 20 (CAMPAGNE-VOLUME §1)
```

## 1 · L'ordre, et ce qui le fixe

L'ordre **n'est pas** la préférence : il va du fait le plus fort au plus faible. Trois cabinets exercent
sous **un autre nom** que celui du tableau de l'Ordre — c'est le fait le plus vérifiable qui existe, et
le seul dont le patient subit la conséquence tous les jours. Les quatre autres ont un profil Business :
la vitrine existe, mais elle est dans WhatsApp, que Google ne lit pas.

| # | Cabinet | Numéro | Le fait, et sa date |
|---|---|---|---|
| ① | Ets Espace Médical (PK11) | 655 04 95 29 | Business « Optic Medical Favour and Joy » ≠ tableau de l'Ordre — 25/10 |
| ② | ASS pour RRPHDD | 675 39 90 23 | Business « AMBASSADOR Vision Sarl » ≠ tableau de l'Ordre — 25/10 |
| ③ | ISEE | 656 97 80 43 | Business « I See Better » ≠ tableau de l'Ordre — 25/10 |
| ④ | Bellevue Optique (Bali) | 694 89 26 96 | Business, adresse Bali Serena Hôtel rue des pavés — 25/10 |
| ⑤ | S.O.S Vision | 699 86 04 63 | Business, trois métiers + horaires + catalogue — 25/10 |
| ⑥ | Free Optic | 679 11 37 60 | Business, « examens de vue, vente de lunettes » — 25/10 |
| ⑦ | Capelli Optique Médicale | 675 26 89 81 | Business, Optometrist · Optician + adresse — 25/10 |

> **Les sept partent le même jour, dans cet ordre, avant les treize du lot volume.** Ce ne sont pas sept
> jours de données, c'est **un** jour à vingt messages. La règle « un message par jour » a été annulée
> le 26/10 : elle avait été écrite pour un numéro qui n'avait jamais rien envoyé.

## 2 · Les sept messages, mot pour mot

**① Ets Espace Médical — PK11 — 655 04 95 29**

> Bonjour, à PK11 votre compte WhatsApp s'appelle « Optic Medical Favour and Joy », et le tableau de l'Ordre vous inscrit « Ets Espace Médical ».
> Ce n'est pas votre travail, c'est le nom : un patient cherche l'un, trouve l'autre, et appelle le numéro d'après.
> Dites-moi en un mot : lequel des deux noms vos clients prononcent ?

**② ASS pour RRPHDD — Douala — 675 39 90 23**

> Bonjour, à Douala vous êtes « AMBASSADOR Vision Sarl » sur WhatsApp, avec vos montures et votre service après-vente ; au tableau de l'Ordre, « ASS pour RRPHDD ».
> Ce n'est pas votre faute, c'est le nom : deux noms font deux recherches, et le patient qui cherche l'un ne voit pas l'autre.
> Dites-moi en un mot : lequel je dois retenir ?

**③ ISEE — Douala — 656 97 80 43**

> Bonjour, à Douala, « ISEE » au tableau de l'Ordre et « I See Better » sur WhatsApp, avec une adresse postale et un email.
> Ce n'est pas votre travail, c'est le nom : qui tape « ISEE Douala » sur Google trouve une ligne d'annuaire, un numéro et rien d'autre.
> Dites-moi en un mot : lequel des deux vos patients utilisent ?

**④ Bellevue Optique — Bali — 694 89 26 96**

> Bonjour, à Bali votre profil WhatsApp Business indique l'adresse Serena Hôtel, rue des pavés, et le métier « opticien ».
> Ce n'est pas votre organisation qui est en cause : une adresse dans WhatsApp, Google ne la lit pas.
> Dites-moi en un mot : un patient peut trouver cette adresse sur Google ce soir ?

**⑤ S.O.S Vision — Douala — 699 86 04 63**

> Bonjour, à Douala votre profil WhatsApp Business déclare trois métiers — opticien, lunetterie, ophtalmologue — avec des horaires et un catalogue.
> Ce n'est pas votre organisation qui est en cause : ces horaires vivent dans WhatsApp, et la recherche les ignore.
> Dites-moi en un mot : un patient peut voir vos horaires en ligne ce soir ?

**⑥ Free Optic — Douala — 679 11 37 60**

> Bonjour, à Douala votre profil WhatsApp Business dit « examens de vue, vente de lunettes » — c'est exactement ce qu'un patient cherche.
> Ce n'est pas votre offre qui manque, c'est l'endroit : ce texte est dans WhatsApp, pas sur une page.
> Dites-moi en un mot : un patient peut lire vos examens de vue en ligne aujourd'hui ?

**⑦ Capelli Optique Médicale — Douala — 675 26 89 81**

> Bonjour, à Douala votre profil WhatsApp Business vous déclare à la fois « Optometrist » et « Optician », avec votre adresse.
> Ce n'est pas votre travail, c'est la vitrine : un patient qui vous cherche sur Google ne lit ni vos deux métiers ni votre adresse.
> Dites-moi en un mot : un patient peut voir les deux en ligne ?

## 3 · Ce que chaque message fait, et ne fait pas

| Il fait | Il ne fait pas |
|---|---|
| il nomme **ce qu'il a vu**, et la date de ce qu'il a vu | il n'affirme **jamais** « vous n'avez pas de site » — nous ne l'avons pas vérifié (§8c) |
| il dédouane une fois, avant la conséquence | il ne reproche rien au travail du cabinet |
| il finit par **une question fermée à un mot**, qui demande une action | il ne propose pas de rendez-vous, ne donne pas de prix, ne joint aucun lien |
| il laisse la sortie ouverte (« un mot ») | il ne promet ni fiche Google validée, ni nombre de patients |

## 4 · La relance

**Une seule, à J+7, et seulement si le message a été lu** (`CLIENT-MESSAGING-RULES` §13, ruling 24/09).
Si les coches restent grises (livré, jamais ouvert) : `parked` au CRM, raison datée, aucune relance — et
on ne rouvre que si le cabinet écrit. Un message froid sans réponse n'est pas un refus, c'est un silence :
il ne justifie ni un second message, ni un appel (ruling 25/10 : pas de repli hors WhatsApp).

## 5 · Ce que King fait, et dans quel ordre

1. Envoyer ① à ⑦ **dans cet ordre**, d'affilée, puis les treize du lot volume.
2. Répondre **dans l'heure** à qui répond : c'est la fenêtre où le prospect est devant son écran.
3. Si la réponse est **oui**, ouvrir `sales/REPONSE-OUI-2026-10-26.md` — la page part dans les 24 h.
4. Cocher le tracker (`CAMPAGNE-VOLUME` §5) le soir, même si la case est vide.
