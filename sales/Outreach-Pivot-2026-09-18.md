# Outreach — pivot du 18 Sep 2026 : maquette d'abord, build après le « oui »

**Décision de King (18 Sep 2026) :** « we have been building a demo site for each prospect
which has been costing us a lot of time for people who don't even reply — it's not worth it. »
→ On **ne construit plus** de démo avant qu'un prospect demande explicitement l'aperçu.
Avant le « oui » : **maquette légère et personnalisée**. Après le « oui » : le build.
Et on **augmente le nombre de messages**, pas le nombre de builds.

---

## 1 · Pourquoi c'est la bonne décision (données, 18/09)

| Donnée | Conséquence pour nous |
|---|---|
| Message froid WhatsApp : **3–5 %** de réponses | Sur 100 messages, 3 à 5 réponses. Construire pour les 95 autres = 95 % du travail perdu. |
| Ultra-personnalisé : **15–20 %** · diffusion générique : **2–8 %** | Le levier n'est pas le volume brut, c'est **la personnalisation**. Une maquette portant le nom, le métier et la couleur du prospect **est** le signal de personnalisation. |
| Listes ≤ 50 cibles : **5,8 %** vs **2,1 %** sur grosses listes | Moins de cibles, mieux choisies. |
| Répondre en **< 90 s** → 50–60 % de réponses, 8–12 % de démos réservées · **> 24 h = mort** | **C'est l'argument décisif :** si on construit après le « oui », il faut pouvoir livrer dans la minute. D'où la banque de maquettes + la banque de démos déjà construites. |
| **55 %** des réponses viennent des relances (1re 30 %, 2e 20 %, 3e 5 %) | Nos relances M+2 / +4 / +7 ne sont pas optionnelles : plus de la moitié du résultat est là. |
| 3 canaux ou plus : **+ 287 %** de réponses | WhatsApp + TikTok/IG + relance téléphonique si le numéro est public. |

**Où va le temps économisé :** dans les **messages**, pas dans les builds. Les messages
coûtent des minutes ; un site coûte des heures. On échange le travail cher contre du travail bon marché.

## 2 · Nouvelle mécanique d'envoi (remplace l'ancienne)

1. **Image d'abord**, texte en légende — un seul message (2 bulles maximum).
2. La légende garde la structure qui marche : **raison d'OUVRIR** + **question-micro** dont la réponse est « oui ». ≤ 5 lignes. Bilingue.
3. Zéro lien dans le message froid (§44 : autorisation d'abord, lien ensuite).
4. Le prospect répond « oui » → **on livre l'aperçu en moins de 90 secondes** (lien live + capture).

Gabarit :

```
[IMAGE : maquette personnalisée 1080×1350]

Bonjour <Nom> — j'ai vu <détail précis et vérifiable de leur page>.
Je suis au Cameroun, je fais les sites des cliniques et des écoles.
J'ai préparé à quoi ressemblerait <son nom> en ligne.
Je vous l'envoie ?
```

## 3 · Ce qui ne change pas

- Fenêtre **09:00–21:00**, jamais après 21:00.
- **3 relances maximum** (M+2 / +4 / +7), jamais de poursuite vers le bas.
- 100 000 FCFA, 50/50, **jamais de rabais**.
- Jamais de prix dans le hero ; le prix se pose à côté de la preuve qu'il achète.
- Jamais de témoignage, de chiffre ou de prix inventé — **loi d'exactitude**.
- Aucun nom réel de clinique ou d'école dans un contenu public sans autorisation écrite.

## 4 · Livrer en moins de 90 secondes : la banque

| Ressource | État |
|---|---|
| Générateur de maquette | `tools/outreach/mockup.py` — **~2 min/prospect** · `tools/outreach/README-MOCKUP.md` |
| Modèle d'accueil à jetons | `site/mockup-hero.html` (mots du prospect uniquement) |
| Démos déjà construites et en ligne | labethanie-concept · jempo-concept · opticien · oracare · skye · yaks · sjc-sasse |
| Bibliothèque de démos | `hosting/previews/demo/` — 5 pages, 0 fuite, audit 0 |

Une réponse « oui » se traite donc en trois gestes : montrer **sa** maquette, ouvrir le lien
d'une démo existante du même métier, puis proposer l'appel de cadrage.

## 5 · Les trois envois du 18/09 tiennent (démos déjà construites)

`sales/Send-Sheet-2026-09-18.md` : 09:00 L'Opticien · 09:15 La Béthanie · 09:30 JEMPO
(09:45 Skye FU1 · 10:00 YAKS FU1). Ces démos sont **déjà bâties et en ligne** : les envoyer
ne coûte plus rien et c'est notre signal le plus fort. **Le pivot s'applique à partir de la
vague suivante.**

## 6 · Prochaine vague (à préparer)

Une maquette par cible, 2 minutes chacune, puis envoi par vagues de 3 à 5 par jour maximum,
toujours dans la fenêtre 09:00–21:00. Cliniques > écoles.
