#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the first-batch school prospects CRM (2026-09-09)."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEADERS = [
    "ID", "School", "City", "Language", "Facebook", "Website", "Website status",
    "Last FB post", "FB followers", "Admissions activity", "Phone", "WhatsApp",
    "Decision maker", "Contact channel", "Facilities", "Multiple branches",
    "Lead score", "Priority", "Demo made", "Contacted", "Reply", "Conversation",
    "Offer made", "Deposit", "Sale", "Follow-up date", "Notes",
]

# Data rows (research done 2026-09-09 via web directories, school sites, press)
LEADS = [
 # ---------------- DOUALA (10) ----------------
 ("COMOBIL – Collège Moderne Bilingue Les Lauréats", "Douala (Bonamoussadi)", "FR/EN",
  "facebook.com/100064111147236", "COMOBIL.com", "Expired",
  "Oct 2021 (page); Groupe WAFO page active Aug 2024", "N/V", "Yes (prix/remise des prix, open day — UCAC-ICAM fair Mar 2026)",
  "+237 233 470 608", "N/V (landline)", "Pierre WAFO (promoteur)", "Phone then WhatsApp",
  "Strong (documentation center, multimedia, language + science labs, infirmary)", "Yes (La Maturité, GS WAFO, EPL Fraternité, ENIEG)",
  18, "A",
  "Founded 1999 by decree; complex general/technical/anglo-saxon; COMOBIL.com is PARKED (verified 09/09/26) = golden D/E target; one contact = whole WAFO group."),
 ("Groupe Scolaire Moderne Bilingue WAFO", "Douala (Denver-Bonamoussadi, BP 6081)", "FR/EN",
  "facebook.com/p/Groupe-WAFO-61556258549625", "groupescolairemodernebilinguewafo.com", "Broken",
  "Aug 2024 (remise des prix COMOBIL)", "37", "Partial (events/prix)",
  "+237 233 473 253", "N/V", "Pierre WAFO (promoteur)", "Phone",
  "Average (unverified)", "Yes (5 institutions in group)",
  12, "A",
  "Same promoter as COMOBIL → merge outreach. Website down (fetch failed 09/09/26). Prématernelle→Terminale + teacher training. groupewafo00@gmail.com."),
 ("COSBINAL – Complexe Scolaire Bilingue NAL", "Douala (Bonamoussadi, Kotto Bloc K)", "FR/EN",
  "facebook.com/Complexe.Scolaire.Bilingue.NAL", "cosbinal.online", "Good",
  "Jan 2024 (PTA meeting)", "1,265", "Yes (conditions d'admissions on site, active news Jan 2026)",
  "+237 677 786 379", "Likely same (mobile)", "N/V", "WhatsApp",
  "Average (cycle complet)", "No",
  10, "C",
  "DO NOT SELL BASIC: recent professional site built by local agency Didacweb (competitive intel). Park; upsell candidate (e-learning, multilingual)."),
 ("Le Paradis des Anges (PDA)", "Douala (Makepe, Carrefour SNEC Bloc A)", "FR/EN",
  "Linked from site (URL N/V)", "leparadisdesanges.org", "Good",
  "N/V", "N/V", "Yes ('venez nous voir', 26 years running)",
  "+237 677 378 542 / +237 233 471 924", "677 378 542 (likely)", "N/V", "WhatsApp",
  "Average", "No",
  4, "C",
  "Nursery+primary, laïque, 26 ans, Wix site. paradangesmakepe@gmail.com. Park; possible custom bilingual site upsell."),
 ("American School of Douala (ASD)", "Douala (BP 1909)", "EN",
  "N/V", "asddouala.com", "Good",
  "N/V", "N/V", "Yes (annual admissions, 4-term year)",
  "+237 677 717 083", "N/V", "Head of School (N/V)", "Phone/Email (asd@asddouala.com)",
  "Strong (20m pool, auditorium, IT lab)", "No",
  9, "C",
  "PARK: US Dept of State fact sheet, MSA accredited, founded 1978, pre-K→12. High budget but good existing site; long-term relationship play."),
 ("Divine Success Comprehensive College (DSCC)", "Douala (Ngodi)", "EN",
  "N/V (active TikTok ads instead)", "None found", "None",
  "TikTok active (Jul 2026)", "N/V", "Yes ('inbox us for admissions' TikTok ads)",
  "+237 696 023 696", "Likely same", "N/V", "WhatsApp",
  "N/V", "Yes (1 Douala + 2 Yaoundé per TikTok)",
  8, "B",
  "Anglo-Saxon secondary. Data from TikTok — verify on Maps/FB before outreach. No website found = +2."),
 ("Presbyterian Comprehensive Secondary School Bonamoussadi (PCSS)", "Douala (Bonamoussadi)", "FR (N/V)",
  "facebook.com/p/Presbyterian-Comprehensive-Secondary-School-Bonamoussadi-100066311097097", "None found", "None",
  "N/V (fundraiser event posted)", "1,785", "N/V",
  "N/V", "N/V", "Headmaster (N/V)", "FB/Phone",
  "N/V", "Yes (Presbyterian PCSS network: Buea + Bonamoussadi)",
  9, "B",
  "Active FB page (1,785 likes, school fundraiser). Need phone before outreach — try FB message first."),
 ("École Privée Bilingue Les Génies", "Douala (Akwa)", "FR/EN",
  "N/V", "N/V", "Unknown — verify",
  "N/V", "N/V", "N/V", "N/V", "N/V", "N/V", "Phone",
  "N/V", "No",
  4, "C",
  "Listed in Douala private primary directory (vosreponses). Verify name/contacts on Google Maps before contact."),
 ("Groupe Scolaire La Semence", "Douala (Bonamoussadi, Fin Goudron Bangue, BP 1661)", "FR/EN",
  "N/V", "N/V", "Unknown — verify",
  "N/V", "N/V", "N/V", "N/V", "N/V", "N/V", "Phone",
  "N/V", "No",
  3, "C",
  "Groupe scolaire primaire+maternelle bilingue privé laïc (banabam directory). Verify before contact."),
 ("Institut Polyvalent Fosso", "Douala (Akwa/Bépanda Tonerre, 'safari' route Bonamoussadi)", "FR/EN",
  "N/V", "N/V", "Unknown — verify",
  "N/V", "N/V", "N/V", "N/V", "N/V", "N/V", "Phone",
  "N/V", "No",
  4, "C",
  "Enseignement secondaire général + commercial + section Anglo-Saxon (since 2015). Bilingual angle. Verify before contact."),
 # ---------------- YAOUNDÉ (6) ----------------
 ("Collège Catholique Bilingue La Retraite", "Yaoundé (159 Ave Konrad Adenauer)", "FR/EN",
  "facebook.com/colegedelaretraite", "laretraitecatholicbilingualcollege.org", "Outdated",
  "N/V (site news active to Aug 2026)", "N/V", "Yes (concours entrée 6e/Form 1 May 2026; Semaine des Lauréats Aug 2026)",
  "+237 233 588 654", "N/V", "Abbé Alexandre Messi Mbarga (nouveau Principal, nommé août 2026)", "Phone/FB",
  "Strong (Bât. Mgr Jean Mbarga, 25 PC donnés, e-learning, bibliothèque multimédia)", "No",
  17, "A",
  "FOUNDER-LEVEL HOOK: 'digitalisation' is an official 2026-2027 priority (conseil d'enseignement, 31/08/26). Founded 1950, top BAC results, 98% target. Outdated Joomla site. contact@collegedelaretraite.org."),
 ("Complexe Scolaire et Universitaire Siantou", "Yaoundé (Mvog-Mbi/Coron-Biteng, BP 04)", "FR",
  "facebook.com/INSTITUT SIANTOU (secondaire page: 732 likes)", "siantou-univ.com (+ siantou.net e-service subdomains)", "Good",
  "N/V", "~732 (secondaire page)", "Yes (préinscription en ligne active)",
  "+237 668 556 755", "Likely same", "Wantou Siantou Lucien (fondateur/président)", "PARKED — do not pitch",
  "Strong ('La Tour des Majors' amphi, modern campus)", "Yes (secondary + university + technical campuses)",
  12, "C",
  "CORRECTED 09/09/26 (per King): current site siantou-univ.com is UP and digitally mature — modern WP (2025-26 content), online pre-registration (preinscription.siantou.net), document portal (document.siantou.net), e-learning, WhatsApp widget, 12+ filières BTS→MBA. Old siantou.net homepage down but its subdomains work. PARK per brief (B site); long-term upsell: mobile refresh, results page, e-learning (EN|FR is AMK standard on all builds)."),

 ("Blessed Group of Schools (BGS / Blessed Anglo-Saxon)", "Yaoundé (Simbock + Nomayos, BP 1839)", "FR/EN",
  "Linked from site (N/V) — NOTE: facebook.com/blessedgroupofschools is an Ibadan/Nigeria school, NOT this one", "blessedgroupofschools.com", "Good",
  "N/V", "N/V", "Yes (Admissions open 2026–2027, fees + bank details published)",
  "+237 680 139 453", "Likely same", "Proprietor (N/V)", "WhatsApp",
  "Average (2 campuses, technical workshops)", "Yes (2 campuses: Simbock + Nomayos)",
  12, "C",
  "PARK: modern structured site, MINESEC-authorized, nursery→secondary + technical (auto, civil, electrical, coding). Upsell: mobile refresh, results page, e-learning (EN|FR is standard). blessedanglosaxonhss@yahoo.com."),
 ("Baptist High School (BHS) Awae", "Yaoundé (Awae)", "FR/EN",
  "facebook.com/pages/BAPTIST-HIGH-SCHOOL-AWAE/5687915", "None found", "None",
  "N/V", "N/V", "N/V",
  "+237 677 647 802", "Likely same", "Headmaster (N/V)", "Phone/WhatsApp",
  "Average (boarding)", "Yes (Baptist Convention network incl. BHS Buea)",
  8, "B",
  "Respected Christian boarding school, consistent GCE results (237zoom ranking #8). No website found. Verify FB activity before outreach."),
 ("Rainforest International School (RFIS)", "Yaoundé (SIL, BP 1299)", "EN",
  "N/V", "rfis.org", "Good",
  "N/V", "N/V", "Yes (ongoing, contact form 'Let's talk!')",
  "+237 677 937 162 (2017 dir — verify)", "N/V", "Head (N/V)", "Phone",
  "Average", "No",
  7, "C",
  "PARK: modern WP site, founded 1991, Christian, North-American curriculum, missionary-governed. Long-term relationship play."),
 ("Institut Notre Dame des Apôtres", "Yaoundé", "FR",
  "N/V", "None found", "Unknown — verify",
  "N/V", "N/V", "N/V", "N/V", "N/V", "N/V", "Phone",
  "Average (boarding, girls)", "No",
  5, "C",
  "Private Catholic girls' boarding school (237zoom ranking #7). Verify contacts before contact."),
 # ---------------- BUEA (5) ----------------
 ("St. Joseph's College Sasse (SJC Sasse)", "Buea (Sasse/Small Soppo)", "EN",
  "'SJC – The Republic' (URL N/V); very active on TikTok #saintjosephcollegesasse", "None found", "None",
  "Active 2026 (admissions campaign on TikTok/FB)", "N/V (TikTok active)", "YES — 'Admissions now open' 2026, interview sessions ongoing",
  "+237 677 195 500", "N/A — 677 195 500 NOT on WhatsApp (King verified 09/09)", "Fr. Njanto Jude (Principal)", "TikTok DM + email + call",
  "Strong (historic 1939 campus, boarding, 'cleanest school in Cameroon' claim)", "No",
  16, "A",
  "THE #1 DEMO TARGET. 100% exam success tradition; SOBA alumni network (FCFA 23M scholarships 2025); Catholic all-boys; sajoscol@gmail.com. No website = missing destination for their active attention. DEMO BUILT: sjc-sasse-homepage.html. 2012 'Best School in West Africa' + 2013 'Best School in Cameroon' (Fondation Terre d'accueil) — demo material. WhatsApp 677 195 500 NOT available (King 09/09) → TIKTOK DM @SJC - The Republic + email sajoscol@gmail.com + call. Diocesan education line: +237 334 745 678."),
 ("Presbyterian Comprehensive Secondary School (PCSS) Buea", "Buea (Madam Namondo Alexander)", "FR/EN",
  "N/V", "None found (pcss@yahoo.com)", "None",
  "N/V", "N/V", "N/V (700 pupils, boarding, general + technical)",
  "+237 652 075 229", "N/V", "Headmaster (N/V); staff contact: Kinang Edwin Ngenge, 675 533 321", "Phone",
  "Strong (boarding, 700+ students, 1993)", "Yes (PCSS network: Buea + Bonamoussadi)",
  10, "B",
  "4.1/5 (43 reviews, inovedu); tuition 213k–281k FCFA/yr. Presbyterian co-ed boarding. Quick verification could push to A."),
 ("Frankfils Comprehensive College", "Buea", "EN",
  "N/V", "None found", "None",
  "N/V", "N/V", "N/V", "N/V", "N/V", "Headmaster (N/V)", "Phone",
  "N/V", "No",
  5, "C",
  "GCE centre 11402; 71% O-Level pass rate 2018 (concourscameroon). Verify before contact."),
 ("Salvation Bilingual High School (Molyko-Buea)", "Buea (Molyko)", "FR/EN",
  "N/V", "None found", "None",
  "N/V", "N/V", "N/V", "N/V", "N/V", "Headmaster (N/V)", "Phone",
  "N/V", "No",
  5, "C",
  "GCE centre 11412; accommodation centre for BHS Buea. Verify before contact."),
 ("Marthlo Comprehensive Bilingual College", "Buea", "FR/EN",
  "N/V", "None found", "None",
  "N/V", "N/V", "N/V", "N/V", "N/V", "Headmaster (N/V)", "Phone",
  "N/V", "No",
  5, "C",
  "GCE centre 22037 (technical streams). Verify before contact."),
 # ---------------- LIMBE (5) ----------------
 ("Saint Anne's High School Limbe (SAHISCOL)", "Limbe (New Town)", "EN",
  "facebook.com/p/Saint-Annes-High-School-Limbe-100092337257373", "sahiscol.org", "Broken",
  "2023 (GCE review)", "60", "Yes (admission portal on site — stale: still says 'CLOSED for 2024/2025')",
  "+237 233 322 551 / +237 334 745 678 (diocesan line)", "TRY 334 745 678 on WhatsApp; 682 122 959 is NOT school's (King verified 09/09 — wrong profile)", "Headmistress (N/V) — GIRLS' school", "WhatsApp (new no) + Messenger + landline + email",
  "Average", "No",
  9, "A",
  "GOLDEN D: sahiscol.org returns HTTP 502 (verified 09/09/26) — domain/hosting abandoned. info@sahiscol.org. Use broken-website pitch. Close to us (Limbe). DIOCESAN school (Buea Diocese portfolio: 'Saint Ann Girls College Limbe', New Town) — GIRLS' school, adjust demo wording. sahiscol@gmail.com. Published mobile was stale (someone else's number) = further evidence of abandoned digital presence."),
 ("New Horizon International Comprehensive High School (NHICHS)", "Limbe (Cité Sonara, Bota)", "EN",
  "N/V", "nhiss.org (live) + nhichs.org (PARKED/expired)", "Good / brand domain Expired",
  "N/V", "N/V", "Yes ('Apply Now — No Cost!', technical department launching 2026)",
  "+237 677 754 290 / 680 738 111 / 679 246 223", "TRY 680 738 111 or 679 246 223 on WhatsApp; 677 754 290 NOT on WhatsApp (King verified 09/09)", "Director (mehdi@nhiss.org)", "WhatsApp (other no) + Director email + phone",
  "Average (equipped labs, computer lab, music club)", "No",
  11, "A",
  "Pitch: branded domain nhichs.org expired (parked at Namecheap) + template full of typos + add EN|FR toggle. Founded 2004; 5000+ graduates claimed; GCE grammar+commercial centre; scholarships; info@nhiss.org (updated). inovedu 4.4/5 (40 reviews, 271 likes); tuition 192k–274k FCFA. Director email = mehdi@nhiss.org (direct line to decision maker)."),
 ("College de l'Excellence de Limbe", "Limbe", "FR",
  "N/V", "coel.net (from info@coel.net)", "Broken",
  "N/V", "N/V (221 likes on directory profile)", "N/V", "N/V", "N/V", "N/V", "Email/FB",
  "Average (4.3/5, 25 parent reviews; tuition 173k–265k FCFA)", "No",
  9, "A",
  "GOLDEN D: coel.net returns HTTP 500 (verified 09/09/26). French-medium school — French pitch. Find phone via Google Maps/parents before outreach."),
 ("National Comprehensive High School (NCHS) Limbe", "Limbe (near Atlantic Technical & Commercial)", "EN",
  "Alumni page 'NCHS Limbe Ex-students'; official page N/V", "None found", "None",
  "N/V (alumni page only)", "N/V", "N/V", "N/V", "N/V", "Headmaster (N/V)", "Phone (visit)",
  "Average (500+ students)", "No",
  6, "B",
  "Founded 1972 by parents (non-profit origin); commercial + general sections; strong GCE O/A level results. Verify official FB + phone."),
 ("Presbyterian Girls Secondary School (PGSS) Limbe", "Limbe", "EN",
  "N/V", "None found", "Unknown — verify",
  "N/V", "N/V", "N/V", "N/V", "N/V", "Headmistress (N/V)", "Phone",
  "N/V", "Yes (Presbyterian network)",
  4, "C",
  "Confessional private secondary (ecolesaucameroun directory). Verify before contact."),
]

TOP5 = [
 (1, "St. Joseph's College Sasse", "Buea", 16,
  "No official website at all, while running a loud 2026/2027 admissions campaign (TikTok + FB, interviews ongoing). Their attention has nowhere to land. Mobile number available = easy WhatsApp contact.",
  "Admissions now open 2026/2027; interview sessions; SOBA alumni day (Dec 2025).",
  "Fr. Njanto Jude (Principal); diocese + SOBA alumni board",
  "TIKTOK DM @SJC - The Republic + EMAIL sajoscol@gmail.com (677 195 500 NOT on WhatsApp — King 09/09); call in evening; diocesan line +237 334 745 678",
  "Hello, my name is Akwo King, from AMK – Web Development & Digital Solutions. I came across St. Joseph's College Sasse while researching schools in Buea, and I noticed your 2026/2027 admissions campaign is doing very well on social media — but there isn't a modern official website yet.\n\nI put together a quick homepage concept showing how the school could present its programs, admissions information and important details for parents, with a direct WhatsApp contact.\n\nWould you like me to send you the preview?\n\n— Akwo King\nAMK – Web Development & Digital Solutions",
  "Bonjour, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales. En recherchant des établissements à Buea, je suis tombé sur le St. Joseph's College Sasse et j'ai vu que votre campagne d'admissions 2026/2027 fonctionne très bien sur les réseaux — mais qu'il n'existe pas encore de site officiel moderne.\n\nJ'ai préparé rapidement une idée de page d'accueil : programmes, informations d'admissions et un contact direct via WhatsApp pour les parents.\n\nSouhaitez-vous que je vous envoie l'aperçu ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "YES — BUILT (sjc-sasse-homepage.html)", "STAGE 2 — TikTok DM + email on MON (outreach starts Monday). FU1 M+2, FU2 M+4, FU3 M+7, then archive. No walk-in unless invited."),
 (2, "Saint Anne's High School Limbe (SAHISCOL)", "Limbe (New Town)", 9,
  "sahiscol.org returns HTTP 502 — site broken/abandoned (verified 09/09/26). Admission portal still shows 'CLOSED for 2024/2025' (stale). Mobile number available.",
  "Admission portal (stale); GCE exam cycle.",
  "Headmaster (N/V)",
  "TRY 334 745 678 on WhatsApp; MESSENDER (FB page); landline 233 322 551; info@sahiscol.org / sahiscol@gmail.com",
  "Hello, my name is Akwo King, from AMK – Web Development & Digital Solutions. I came across Saint Anne's High School while researching schools in Limbe, and I noticed that your current website (sahiscol.org) doesn't appear to be accessible at the moment.\n\nI work with schools on modern, mobile-friendly websites, and I thought I'd reach out because this is something I could help you fix. I can also show you a quick concept of how the school's website could look on mobile and desktop.\n\nWould you like me to send it?\n\n— Akwo King\nAMK – Web Development & Digital Solutions",
  "Bonjour, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales. En recherchant des établissements à Limbe, j'ai remarqué que le site du Saint Anne's High School (sahiscol.org) ne semble actuellement pas accessible.\n\nJe travaille avec des établissements sur des sites web modernes et adaptés aux téléphones, et je me suis dit que cela pourrait vous être utile. Je peux vous préparer rapidement un aperçu de ce que pourrait être une version moderne du site, sur téléphone et ordinateur.\n\nSouhaitez-vous que je vous l'envoie ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Optional (broken-site pitch first)", "STAGE 2 — WhatsApp 334 745 678 + Messenger on MON; landline if silent. FU1 M+2, FU2 M+4, FU3 M+7. No walk-in. GIRLS' school — adjust demo wording if built."),
 (3, "New Horizon International Comprehensive High School (NHICHS)", "Limbe (Cité Sonara, Bota)", 11,
  "Branded domain nhichs.org EXPIRED (parked at Namecheap); live site nhiss.org is a generic template full of typos. Parents may not find the school reliably. Mobile number available.",
  "'Apply Now — No Cost!'; technical department launching 2026; scholarships.",
  "Head (N/V)",
  "TRY 680 738 111 / 679 246 223 on WhatsApp; DIRECTOR EMAIL mehdi@nhiss.org; info@nhiss.org",
  "Hello, my name is Akwo King, from AMK – Web Development & Digital Solutions. I came across New Horizon International Comprehensive High School while researching schools in Limbe.\n\nI noticed that your main domain (nhichs.org) is no longer active, and the current site on nhiss.org looks a bit dated, with a few typos — parents searching on their phones may not always find the school easily.\n\nI work with schools on modern, mobile-friendly websites. I'd be happy to show you a quick concept of what a refreshed version could look like, including an English/French option for both parent groups.\n\nWould you like me to send it?\n\n— Akwo King\nAMK – Web Development & Digital Solutions",
  "Bonjour, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales. En recherchant des établissements à Limbe, je suis tombé sur le New Horizon International Comprehensive High School.\n\nJ'ai remarqué que votre domaine principal (nhichs.org) n'est plus actif, et que le site actuel sur nhiss.org est un peu périmé — les parents qui cherchent l'école sur téléphone ne la trouvent pas toujours facilement.\n\nJe travaille avec des établissements sur des sites web modernes et adaptés aux téléphones. Je peux vous montrer rapidement un aperçu de ce que pourrait être une version renovée, avec une option anglais/français pour les deux familles d'élèves.\n\nSouhaitez-vous que je vous l'envoie ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Optional (refresh concept can be built if they bite)", "STAGE 2 — WhatsApp 680 738 111 on MON; if not on WA, email the DIRECTOR (mehdi@nhiss.org) — straight to decision maker. FU1 M+2, FU2 M+4, FU3 M+7."),
 (4, "Collège Catholique Bilingue La Retraite", "Yaoundé (Ave Konrad Adenauer)", 17,
  "Outdated Joomla site for one of Yaoundé's most respected private colleges; content active but look dated. Only a landline (233) — so text-first via the official FB page (Messenger).",
  "Concours d'entrée 6e/Form 1; Semaine des Lauréats 2026; target 98% BAC; 'digitalisation' = OFFICIAL 2026-27 PRIORITY (conseil d'enseignement 31/08/26).",
  "Abbé Alexandre Messi Mbarga (nouveau Principal, août 2026); Archidiocèse de Yaoundé",
  "MESSENDER facebook.com/colegedelaretraite (text-first); call +237 233 588 654 if needed",
  "Bonjour, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales.\n\nJ'ai vu dans la presse que la digitalisation figure parmi les priorités du Collège de la Retraite pour l'année 2026-2027. J'ai remarqué aussi que votre site actuel date un peu — or, les parents cherchent d'abord les établissements sur téléphone.\n\nJ'ai préparé rapidement une idée de page d'accueil moderne, avec les programmes bilingues, les résultats et un contact direct.\n\nSouhaitez-vous que je vous envoie un aperçu ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Bonjour, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales.\n\nJ'ai vu dans la presse que la digitalisation figure parmi les priorités du Collège de la Retraite pour l'année 2026-2027. J'ai remarqué aussi que votre site actuel date un peu — or, les parents cherchent d'abord les établissements sur téléphone.\n\nJ'ai préparé rapidement une idée de page d'accueil moderne, avec les programmes bilingues, les résultats et un contact direct.\n\nSouhaitez-vous que je vous envoie un aperçu ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Optional (site-refresh pitch)", "STAGE 2 — Messenger on MON. FU1 M+2, FU2 M+4, FU3 M+7."),
 (5, "COMOBIL – Les Lauréats + Groupe WAFO", "Douala (Bonamoussadi)", 18,
  "COMOBIL.com PARKED (domain expired, verified 09/09/26); WAFO group site down. ONE promoter (Pierre WAFO) runs 5 institutions. Landline only — try FB page first, then call.",
  "Remise des prix; open-day stands (UCAC-ICAM fair, Mar 2026).",
  "Pierre WAFO (promoteur — also La Maturité, GS WAFO, EPL Fraternité, ENIEG WAFO)",
  "MESSENDER facebook.com/100064111147236 then CALL +237 233 470 608; comobil@yahoo.fr",
  "Monsieur WAFO, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales.\n\nJe cherchais le site du Collège Moderne Bilingue Les Lauréats et COMOBIL.com ne semble plus accessible actuellement. Je travaille avec des établissements sur des sites web modernes et adaptés aux téléphones, et je me suis dit que cela pourrait vous être utile pour tout le groupe.\n\nJe peux vous préparer rapidement un aperçu de ce que pourrait être une version moderne du site, sur téléphone et ordinateur.\n\nSouhaitez-vous que je vous l'envoie ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Monsieur WAFO, je m'appelle Akwo King, je travaille chez AMK – Développement web & Solutions Digitales.\n\nJe cherchais le site du Collège Moderne Bilingue Les Lauréats et COMOBIL.com ne semble plus accessible actuellement. Je travaille avec des établissements sur des sites web modernes et adaptés aux téléphones, et je me suis dit que cela pourrait vous être utile pour tout le groupe.\n\nJe peux vous préparer rapidement un aperçu de ce que pourrait être une version moderne du site, sur téléphone et ordinateur.\n\nSouhaitez-vous que je vous l'envoie ?\n\n— Akwo King\nAMK – Développement web & Solutions Digitales",
  "Optional (broken-site pitch works first)", "STAGE 2 — Messenger on MON, then call THU if no reply. One contact = whole group (5 institutions)."),
 (7, "Complexe Scolaire et Universitaire Siantou", "Yaoundé (Mvog-Mbi)", 12,
  "PARKED (corrected 09/09/26 per King): initial intel was wrong — siantou.net homepage is down, but the group's CURRENT site siantou-univ.com is up and digitally mature: online pre-registration (preinscription.siantou.net), document request portal (document.siantou.net), e-learning, WhatsApp widget, content current to 2025-26, 12+ filières BTS→MBA.",
  "BTS/DUT/university recruitment via online pre-registration; 'l'école des majors' branding.",
  "Wantou Siantou Lucien (fondateur/président)",
  "PARKED — no outreach for a basic website",
  "— DO NOT SEND (site re-evaluated as Good) —",
  "— DO NOT SEND —",
  "N/A", "Long-term upsell only: mobile refresh, results page, e-learning. Keep warm."),
]



wb = openpyxl.Workbook()

# ---------- Sheet 1: Leads 50 ----------
ws = wb.active
ws.title = "Leads 50"
thin = Border(*[Side(style="thin", color="D0D0D0")]*4)
head_fill = PatternFill("solid", fgColor="1F3864")
for c, h in enumerate(HEADERS, 1):
    cell = ws.cell(1, c, h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border = thin

prio_fill = {"A": PatternFill("solid", fgColor="C6EFCE"),
             "B": PatternFill("solid", fgColor="FFEB9C"),
             "C": PatternFill("solid", fgColor="FFC7CE")}
city_fill = {"Douala": PatternFill("solid", fgColor="DDEBF7"),
             "Yaoundé": PatternFill("solid", fgColor="E2EFDA"),
             "Buea": PatternFill("solid", fgColor="FCE4D6"),
             "Limbe": PatternFill("solid", fgColor="EDEDED")}
status_fill = {"Broken": PatternFill("solid", fgColor="FFC7CE"),
               "Expired": PatternFill("solid", fgColor="FFC7CE"),
               "Outdated": PatternFill("solid", fgColor="FFEB9C"),
               "None": PatternFill("solid", fgColor="DDEBF7")}

for i, row in enumerate(LEADS, 1):
    # row tuple: 15 lead fields (school..branches) + score + priority + notes
    vals = [i, *row[:15], row[15], row[16],
            "No", "No", "No", "No", "No", "No", "", "", row[17]]
    assert len(vals) == len(HEADERS), f"row {i} has {len(vals)} cols"
    for c, v in enumerate(vals, 1):
        cell = ws.cell(i + 1, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = thin
    # fills
    city = row[1]
    for prefix in city_fill:
        if city.startswith(prefix):
            ws.cell(i + 1, 3).fill = city_fill[prefix]
            break
    status = row[5]
    for k in status_fill:
        if status.startswith(k):
            ws.cell(i + 1, 7).fill = status_fill[k]
            break
    ws.cell(i + 1, 18).fill = prio_fill[row[16]]
    ws.cell(i + 1, 18).font = Font(bold=True)
    if row[15] >= 12:
        ws.cell(i + 1, 17).font = Font(bold=True, color="C00000")

widths = [5, 38, 22, 9, 34, 30, 15, 22, 12, 26, 22, 18, 30, 14, 24, 14, 9, 9, 9, 10, 8, 12, 10, 9, 8, 13, 60]
for c, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(c)].width = w
ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(LEADS)+1}"

# ---------- Sheet 2: Top 5 Deep Dive ----------
ws2 = wb.create_sheet("Deep Dive – Contact Plan")
h2 = ["Rank", "School", "City", "Score", "Problem (evidence)", "What they're promoting now",
      "Decision maker", "Contact channel", "Opening message (EN)", "Opening message (FR)",
      "Demo", "Next action / date"]
for c, h in enumerate(h2, 1):
    cell = ws2.cell(1, c, h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border = thin
for i, row in enumerate(TOP5, 1):
    for c, v in enumerate(row, 1):
        cell = ws2.cell(i + 1, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = thin
    ws2.cell(i + 1, 1).font = Font(bold=True, size=12)
    ws2.cell(i + 1, 4).font = Font(bold=True, color="C00000")
w2 = [6, 30, 18, 7, 45, 40, 35, 30, 60, 60, 22, 30]
for c, w in enumerate(w2, 1):
    ws2.column_dimensions[get_column_letter(c)].width = w
ws2.freeze_panes = "A2"

# ---------- Sheet 3: Daily Tracker ----------
ws3 = wb.create_sheet("Daily Tracker")
h3 = ["Date", "New prospects", "Messages sent", "Replies", "Positive replies",
      "Demos sent", "Calls/conversations", "Offers", "Deposits", "Sales (FCFA)", "Notes"]
for c, h in enumerate(h3, 1):
    cell = ws3.cell(1, c, h)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border = thin
ws3.cell(2, 1, "2026-09-09")
ws3.cell(2, 2, 25)
ws3.cell(2, 3, 0)
for c in range(4, 11):
    ws3.cell(2, c, 0)
ws3.cell(2, 11, "First batch built: 25 leads (10 Douala / 6 Yaoundé / 5 Buea / 5 Limbe). Top 5 deep-dived. Sasse demo built.")
for r in range(2, 40):
    for c in range(1, 12):
        ws3.cell(r, c).border = thin
w3 = [12, 13, 14, 9, 14, 11, 18, 8, 10, 12, 70]
for c, w in enumerate(w3, 1):
    ws3.column_dimensions[get_column_letter(c)].width = w


# ---------- Sheet 4: Pipeline - 5 Stages ----------
ws4 = wb.create_sheet("Pipeline - 5 Stages")
for c, htxt in enumerate(["Stage", "Name", "Goal", "Entry", "Exit gate", "Key actions", "SLA / cadence", "KPI target (month 1)"], 1):
    cell = ws4.cell(1, c, htxt)
    cell.font = Font(bold=True, color="FFFFFF"); cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True); cell.border = thin
stages = [
 ("1", "PROSPECTING", "Find & capture qualified schools with full intel", "Any school in target city", "In CRM with 0-20 score + channel VERIFIED (WhatsApp opened)", "Maps 13 queries EN+FR, Facebook, directories (inovedu/ecolesaucameroun/237zoom/banabam), GCE centre lists, diocese pages, TikTok", "10 leads/day; score same day", "MQL rate >=40% of captured"),
 ("2", "QUALIFYING (MQL->SQL)", "Message right leads; separate worth-messaging from worth-selling", "Lead in CRM", "MQL: ICP 5/7 + channel verified. SQL: replied + BANT complete (B+A+N+T, T<=8 weeks)", "Personalized first message (problem-specific variant); BANT conversation; log B/A/N/T + evidence in Notes", "Reply <24h; FU1 M+2, FU2 M+4, FU3 M+7 then archive C", "Reply 15-25%; MQL->SQL >=25% of replies"),
 ("3", "DEMO & ENGAGEMENT", "Send custom homepage concept; create conversation", "SQL (or A+ with obvious opportunity)", "They ask price / request changes / set a call", "Build EN|FR homepage <=24h after the 'yes'; show ONLY their stated problem; 3 conversation questions", "Send within 24h of permission; 1 follow-up at 48h", "Demo->conversation >=50%; ->offer request >=30%"),
 ("4", "OFFER & CLOSE", "Convert conversation into signed deal", "Positive conversation, need confirmed", "50% DEPOSIT PAID (MoMo/bank)", "Founding-client offer: 100,000 FCFA, 50/50, 3-5 days; scope pages+WhatsApp+domain/hosting+mobile; EN|FR bilingual = STANDARD on all builds (King decision 09/09); ask for the deposit directly", "Offer within 48h of conversation; close window <=1 week", "Offer->deposit >=50%"),
 ("5", "DELIVERY, PROOF & GROWTH", "Deliver, collect proof, generate next leads", "Deposit paid", "Case study live + >=1 referral -> back to Stage 1", "Build 3-5 days with daily WhatsApp progress; handover checklist; balance 50%; testimonial (video+written); referral ask; upsell menu (EN|FR, results page, e-learning, other campuses, hosting)", "Delivery <=5 days; balance at handover", "On-time 100%; testimonials 100%; >=1 referral/client"),
]
for i, row in enumerate(stages, 2):
    for c, v in enumerate(row, 1):
        cell = ws4.cell(i, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True); cell.border = thin
    ws4.cell(i, 1).font = Font(bold=True, size=11, color="C00000")

ws4.cell(8, 1, "CURRENT PIPELINE (as of 09/09/2026)").font = Font(bold=True, size=12)
for c, htxt in enumerate(["ID", "School", "City", "Score", "Priority", "Stage", "Next action"], 1):
    cell = ws4.cell(9, c, htxt)
    cell.font = Font(bold=True, color="FFFFFF"); cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True); cell.border = thin
pipe = [
 (1, "St. Joseph's College Sasse", "Buea", 16, "A", "2 — outreach MON", "TikTok DM + email; demo READY"),
 (2, "SAHISCOL (Saint Ann Girls College)", "Limbe", 9, "A", "2 — outreach MON", "WhatsApp 334 745 678 + Messenger; broken-site pitch"),
 (3, "NHICHS", "Limbe", 11, "A", "2 — outreach MON", "WhatsApp 680 738 111; else email Director mehdi@nhiss.org"),
 (4, "Collège de la Retraite", "Yaoundé", 17, "A", "2 — outreach MON", "Messenger; digitalization-priority hook"),
 (5, "COMOBIL / Groupe WAFO", "Douala", 18, "A", "2 — outreach MON", "Messenger; broken-domain pitch; 1 contact = 5 schools"),
 (6, "GS WAFO (separate entity)", "Douala", 12, "A", "2 — merged with #5", "Same contact as COMOBIL"),
 (7, "PCSS Buea", "Buea", 10, "B", "2 — backup (week 2)", "Verify headmaster name first"),
 (8, "PCSS Bonamoussadi", "Douala", 9, "B", "2 — backup (week 2)", "FB Messenger; find phone"),
 (9, "Divine Success Comprehensive College", "Douala", 8, "B", "1 — verify", "Verify 3 campuses + real name on Maps, then qualify"),
 (10, "Baptist High School Awae", "Yaoundé", 8, "B", "1 — verify", "Verify FB activity + website absence, then qualify"),
 (11, "NCHS Limbe", "Limbe", 6, "B", "1 — verify", "Find official FB + phone"),
 (12, "Collège de l'Excellence de Limbe", "Limbe", 9, "A", "2 — verify then MON+", "D site (500) confirmed; find phone via Maps/parents, then pitch"),
 (13, "COSBINAL / NAL", "Douala", 10, "C", "PARK", "Good recent site (Didacweb) — upsell list only"),
 (14, "Blessed Group of Schools", "Yaoundé", 12, "C", "PARK", "Good modern site — upsell: bilingual EN|FR, e-learning"),
 (15, "American School of Douala", "Douala", 9, "C", "PARK", "Strong incumbent site — long-term relationship play"),
 (16, "Siantou Group", "Yaoundé", 12, "C", "PARK", "CORRECTED 09/09: siantou-univ.com up + online pre-registration — upsell only"),
 (17, "Le Paradis des Anges", "Douala", 4, "C", "PARK", "Decent Wix site — upsell candidate later"),
 (18, "Rainforest International School", "Yaoundé", 7, "C", "PARK", "Good site — long-term play"),
 (19, "Les Génies (Akwa)", "Douala", 4, "C", "1 — verify", "Verify on Maps before anything"),
 (20, "La Semence (Bonamoussadi)", "Douala", 3, "C", "1 — verify", "Directory only"),
 (21, "Institut Polyvalent Fosso (Akwa)", "Douala", 4, "C", "1 — verify", "Anglo-Saxon section = bilingual angle"),
 (22, "Frankfils Comprehensive College", "Buea", 5, "C", "1 — verify", "GCE 11402; find FB/phone"),
 (23, "Salvation Bilingual HS (Molyko)", "Buea", 5, "C", "1 — verify", "GCE 11412; find FB/phone"),
 (24, "Marthlo Comprehensive Bilingual", "Buea", 5, "C", "1 — verify", "GCE 22037; find FB/phone"),
 (25, "Notre Dame des Apôtres", "Yaoundé", 5, "C", "1 — verify", "Girls' boarding; find contacts"),
 (26, "PGSS Limbe", "Limbe", 4, "C", "1 — verify", "Presbyterian network; find contacts"),
]
for i, row in enumerate(pipe, 10):
    for c, v in enumerate(row, 1):
        cell = ws4.cell(i, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True); cell.border = thin
    if "outreach MON" in str(row[5]):
        ws4.cell(i, 6).fill = PatternFill("solid", fgColor="C6EFCE")
    elif row[5] == "PARK":
        ws4.cell(i, 6).fill = PatternFill("solid", fgColor="FFC7CE")
w4 = [6, 34, 12, 7, 9, 22, 52, 30]
for c, w in enumerate(w4, 1):
    ws4.column_dimensions[get_column_letter(c)].width = w

# ---- Daily Tracker: planned Monday row ----
tr_row = None
for r in range(2, ws3.max_row + 1):
    if str(ws3.cell(r, 1).value) == "2026-09-09":
        tr_row = r
        break
nr = (tr_row or 2) + 1
ws3.cell(nr, 1, "Mon (planned)")
ws3.cell(nr, 2, 0)
ws3.cell(nr, 3, 5)
ws3.cell(nr, 11, "Outreach start: 5 first messages (Sasse, SAHISCOL, NHICHS, La Retraite, COMOBIL) — all STAGE 2 per Sales Process v1.0.")
for c in range(1, 12):
    ws3.cell(nr, c).border = thin

out = "/home/user/agency/leads/leads_50.xlsx"
wb.save(out)
print("saved", out, "rows:", len(LEADS))
