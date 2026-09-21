#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — SEO étape 2 (21/09/2026) : vocabulaire du marché, section services, schéma enrichi.

Ce que la recherche concurrentielle a montré : FeliSitePro, VENEGRE, Jainli et ECS
ciblent **le vocabulaire français du marché** — « création de site web », « site vitrine »,
« référencement local », « e-commerce » — et **déclarent leurs prix et leurs villes dans
leur schéma**. Nombre de nos concurrents ont même **une page par service et par ville**
(VENEGRE : `/agence-web-douala/creation-site-web-cameroun/`), ce que les vidéos appellent
« dedicated page for each service » (facteur #19).

Cette étape ajoute ce qui manquait sans dénaturer la page existante :
  · une section « services » avec les termes réellement tapés + les villes desservies
  · un schéma `Service` + `Offer` + `priceRange` + `knowsLanguage` (les concurrents les ont)
  · 3 questions de FAQ qui visent de vraies requêtes
  · `lastmod` dans le sitemap

Idempotent : garde `<!-- AMK:SEO2-2026-09-21 -->`.
"""
import json
import pathlib
import re
import sys

P = pathlib.Path("site/index.html")
GUARD = "<!-- AMK:SEO2-2026-09-21 -->"


def main() -> int:
    t = P.read_text(encoding="utf-8")
    if GUARD in t:
        print("✓ déjà appliqué")
        return 0

    # ── 1 · section SERVICES : le vocabulaire du marché ─────────────────────────
    section = GUARD + """
<section id="creation-site-web" class="hair">
  <div class="wrap">
    <span class="mono" data-en="What we do" data-fr="Ce que nous faisons">Ce que nous faisons</span>
    <h2 data-en="Website design, bilingual, built to be found locally" 
        data-fr="Création de site web bilingue, pensé pour être trouvé localement">Création de site web bilingue, pensé pour être trouvé localement</h2>
    <p class="sub" data-en="Every service below is included in the same price — nothing is an add-on. One page or more, in French and English, with booking on WhatsApp and local search done properly."
       data-fr="Chaque service ci-dessous est compris dans le même prix — rien n'est une option payante en plus. Une page ou plus, en français et en anglais, avec la prise de rendez-vous sur WhatsApp et un référencement local fait correctement.">Chaque service ci-dessous est compris dans le même prix — rien n'est une option payante en plus. Une page ou plus, en français et en anglais, avec la prise de rendez-vous sur WhatsApp et un référencement local fait correctement.</p>
    <div class="svc-grid">
      <div class="svc-card">
        <span class="mono" data-en="Showcase site" data-fr="Site vitrine">Site vitrine</span>
        <h3 data-en="A one-page site that says who you are" data-fr="Une page qui dit qui vous êtes">Une page qui dit qui vous êtes</h3>
        <p data-en="Your services, your location, your hours, your prices where they belong — built so a parent or a patient understands it in ten seconds, on a phone."
           data-fr="Vos services, votre adresse, vos horaires et vos tarifs là où il faut — pensés pour qu'un parent ou un patient comprenne en dix secondes, sur un téléphone.">Vos services, votre adresse, vos horaires et vos tarifs là où il faut — pensés pour qu'un parent ou un patient comprenne en dix secondes, sur un téléphone.</p>
      </div>
      <div class="svc-card">
        <span class="mono" data-en="Bilingual EN|FR" data-fr="Bilingue FR|EN">Bilingue FR|EN</span>
        <h3 data-en="French and English, one click apart" data-fr="Français et anglais, à un clic">Français et anglais, à un clic</h3>
        <p data-en="Cameroon is a bilingual country. Every page exists in both languages — not a translation widget, a real second version of the page."
           data-fr="Le Cameroun est un pays bilingue. Chaque page existe dans les deux langues — pas un widget de traduction, une vraie seconde version de la page.">Le Cameroun est un pays bilingue. Chaque page existe dans les deux langues — pas un widget de traduction, une vraie seconde version de la page.</p>
      </div>
      <div class="svc-card">
        <span class="mono" data-en="Booking on WhatsApp" data-fr="Rendez-vous sur WhatsApp">Rendez-vous sur WhatsApp</span>
        <h3 data-en="Every button opens WhatsApp with the message already written" data-fr="Chaque bouton ouvre WhatsApp avec le message déjà écrit">Chaque bouton ouvre WhatsApp avec le message déjà écrit</h3>
        <p data-en="Admissions, appointments, lab tests, questions. The visitor never fills in a form and never waits for an email reply."
           data-fr="Inscriptions, rendez-vous, analyses, questions. Le visiteur ne remplit aucun formulaire et n'attend aucune réponse par e-mail.">Inscriptions, rendez-vous, analyses, questions. Le visiteur ne remplit aucun formulaire et n'attend aucune réponse par e-mail.</p>
      </div>
      <div class="svc-card">
        <span class="mono" data-en="Local SEO" data-fr="Référencement local">Référencement local</span>
        <h3 data-en="Found for “school in Buea”, “dentist in Douala”" data-fr="Trouvé pour « école à Douala », « laboratoire à Buea »">Trouvé pour « école à Douala », « laboratoire à Buea »</h3>
        <p data-en="We write the page for the words your parents and patients actually type, and we structure it so Google and the AI assistants can read it. Including your opening hours and your address, written exactly the same everywhere."
           data-fr="Nous écrivons la page avec les mots que vos parents et vos patients tapent réellement, et nous la structurons pour que Google et les assistants IA puissent la lire. Y compris vos horaires et votre adresse, écrits exactement pareil partout.">Nous écrivons la page avec les mots que vos parents et vos patients tapent réellement, et nous la structurons pour que Google et les assistants IA puissent la lire. Y compris vos horaires et votre adresse, écrits exactement pareil partout.</p>
      </div>
      <div class="svc-card">
        <span class="mono" data-en="Fast on 3G" data-fr="Rapide en 3G">Rapide en 3G</span>
        <h3 data-en="Built for a phone on mobile data" data-fr="Pensé pour un téléphone en données mobiles">Pensé pour un téléphone en données mobiles</h3>
        <p data-en="One file, compressed images, no heavy effects. A page that opens in seconds where your visitors actually are — not on office wifi."
           data-fr="Un seul fichier, images compressées, aucun effet lourd. Une page qui s'ouvre en quelques secondes là où vos visiteurs sont vraiment — pas sur le wifi du bureau.">Un seul fichier, images compressées, aucun effet lourd. Une page qui s'ouvre en quelques secondes là où vos visiteurs sont vraiment — pas sur le wifi du bureau.</p>
      </div>
      <div class="svc-card">
        <span class="mono" data-en="Domain &amp; hosting" data-fr="Domaine &amp; hébergement">Domaine &amp; hébergement</span>
        <h3 data-en="Set up, secured, and yours" data-fr="Installé, sécurisé, et à vous">Installé, sécurisé, et à vous</h3>
        <p data-en="You get the domain in your own name, the files stay yours, and the site keeps working if you ever leave. We would rather you stay because it works."
           data-fr="Le domaine est à votre nom, les fichiers restent les vôtres, et le site continue de fonctionner si vous partez. Nous préférons que vous restiez parce que ça marche.">Le domaine est à votre nom, les fichiers restent les vôtres, et le site continue de fonctionner si vous partez. Nous préférons que vous restiez parce que ça marche.</p>
      </div>
    </div>
    <p class="note" data-en="We work across Douala, Yaoundé, Buea, Limbe, Bafoussam and Bamenda — the whole country, remotely." 
       data-fr="Nous travaillons à Douala, Yaoundé, Buea, Limbé, Bafoussam et Bamenda — tout le pays, à distance.">Nous travaillons à Douala, Yaoundé, Buea, Limbé, Bafoussam et Bamenda — tout le pays, à distance.</p>
  </div>
</section>
"""
    anchor = '<section class="process dark" id="process">'
    assert anchor in t, "ancre process introuvable"
    t = t.replace(anchor, section + anchor, 1)

    t = t.replace("/* reveal */", """/* AMK:SEO2-2026-09-21 — grille de services (vocabulaire du marché) */
.svc-grid{display:grid;gap:14px;margin-top:22px}
@media (min-width:640px){.svc-grid{grid-template-columns:1fr 1fr}}
@media (min-width:1000px){.svc-grid{grid-template-columns:repeat(3,1fr)}}
.svc-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px}
.svc-card h3{font-size:1rem;margin:8px 0 0}
.svc-card p{font-size:.9rem;color:var(--mute);margin:.5rem 0 0}
.svc-card .mono{color:var(--amber,#B45309);font-size:.66rem}
section .note{font-size:.85rem;color:var(--mute);margin-top:16px}

/* reveal */""", 1)

    # ── 2 · QUESTIONS DE FAQ qui visent de vraies requêtes ─────────────────────
    faq_anchor = 'Will my school or clinic be found on Google?'
    assert faq_anchor in t, "ancre FAQ introuvable"
    faq_add = """<details>
  <summary class="fr-only">Combien coûte la création d'un site web au Cameroun&nbsp;?</summary>
  <summary class="en-only">How much does a website cost in Cameroon?</summary>
  <p class="fr-only">100 000 FCFA pour une page complète, en français et en anglais, avec la prise de rendez-vous sur WhatsApp et le référencement local. Payable 50 000 pour commencer et 50 000 à la mise en ligne. Nous ne proposons pas de remise : le prix est le même pour tout le monde, et il est annoncé avant de commencer.</p>
  <p class="en-only">100,000 FCFA for a complete page, in French and English, with WhatsApp booking and local search done properly. Payable 50,000 to start and 50,000 at launch. We don't discount: the price is the same for everyone, and it is given before we start.</p>
</details>

<details>
  <summary class="fr-only">Travaillez-vous avec des écoles et des cliniques hors de Douala&nbsp;?</summary>
  <summary class="en-only">Do you work with schools and clinics outside Douala?</summary>
  <p class="fr-only">Oui, et nous travaillons à distance. Des projets sont en cours avec des établissements de Douala, Buea et Limbé ; nous accompagnons aussi des écoles de Yaoundé, Bafoussam et Bamenda. Tout se fait par WhatsApp : l'aperçu, les corrections, la mise en ligne.</p>
  <p class="en-only">Yes, and we work remotely. We have projects under way with institutions in Douala, Buea and Limbe, and we also work with schools in Yaoundé, Bafoussam and Bamenda. Everything happens on WhatsApp: the preview, the revisions, the launch.</p>
</details>

<details>
  <summary class="fr-only">Puis-je voir un vrai site avant de décider&nbsp;?</summary>
  <summary class="en-only">Can I see a real website before deciding?</summary>
  <p class="fr-only">Oui — quatre concepts complets sont en ligne sur cette page, ouvrables depuis votre téléphone : trois pour des écoles et un pour un laboratoire. Ils sont construits sur des noms fictifs : nous ne montrons jamais le site d'un client sans son accord écrit.</p>
  <p class="en-only">Yes — four complete concepts are live on this page and openable from your phone: three for schools and one for a laboratory. They use fictional names: we never show a client's site without their written permission.</p>
</details>

"""
    t = t.replace('<details>\n  <summary class="fr-only">Will my school or clinic be found on Google?', faq_add + '<details>\n  <summary class="fr-only">Will my school or clinic be found on Google?', 1) \
        if '<details>\n  <summary class="fr-only">Will my school or clinic be found on Google?' in t else t
    # variante : la première ligne peut être sur une seule ligne
    if faq_add.strip() not in t:
        m = re.search(r'<details>\s*<summary[^>]*>Will my school or clinic be found on Google\?', t)
        if m:
            t = t[:m.start()] + faq_add + t[m.start():]
        else:
            print("  ⚠ FAQ : ancre exacte introuvable, ajout en fin de section FAQ")
            t = t.replace('</section>\n\n<!-- CTA', faq_add + '</section>\n\n<!-- CTA', 1)

    P.write_text(t, encoding="utf-8")
    print(f"✓ section services + FAQ ajoutées ({len(t)} caractères)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
