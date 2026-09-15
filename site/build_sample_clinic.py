# -*- coding: utf-8 -*-
"""Build site/sample-clinic.html — nameless clinic template (Molyko Medical Centre).

Design Read: local private clinic & laboratory landing for anxious first-time
patients in a Cameroonian town, warm premium trust language, Forest family
(deep green + bone + amber; rotated away from the OraCare cream/navy reference),
rounded-16, glass nav, WA-first booking, FCFA pricing, EN|FR.
Dials: VARIANCE 6 · MOTION 4 · DENSITY 4 (school/clinic conversion preset).
Single file, base64 images, AMK demo routing to 237677789631.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent

def b64img(name):
    data = (HERE / "img" / name).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()

IMG = {k: b64img(f"mmc-{k}.jpg") for k in ("hero", "consult", "lab", "maternity")}

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Medical Clinic & Laboratory Website Concept · Molyko Medical Centre (Template) | AMK Cameroon</title>
<meta name="description" content="A patient-first private clinic concept by AMK: transparent FCFA pricing, same-day laboratory, maternity scans, WhatsApp booking in English and French. Template for any clinic in Cameroon. Free 24h preview.">
<link rel="canonical" href="https://amk-cm.vercel.app/sample-clinic.html">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='2' y='2' width='28' height='28' rx='8' fill='%23155642'/%3E%3Cpath d='M14 8h4v6h6v4h-6v6h-4v-6H8v-4h6z' fill='%23F6F3EC'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "Molyko Medical Centre (concept)",
  "url": "https://www.your-clinic.cm",
  "telephone": "+237 677 789 631",
  "address": { "@type": "PostalAddress", "addressLocality": "Your Town", "addressCountry": "CM" },
  "medicalSpecialty": ["GeneralPractice", "LaboratoryScience", "Obstetric"]
}
</script>
<style>
:root{
  --ease-out:cubic-bezier(.23,1,.32,1);
  --ease-in-out:cubic-bezier(.77,0,.175,1);
  --ease-drawer:cubic-bezier(.32,.72,0,1);
  --dur-press:140ms;--dur-pop:170ms;--dur-menu:220ms;--dur-panel:320ms;--dur-reveal:520ms;
  --g900:#114333; --g800:#155642; --g700:#1B6B52; --emerald:#0E7A5C; --emerald-b:#12936E;
  --bone:#F6F3EC; --bone-2:#EFE8D9; --card:#FFFFFF;
  --ink:#14201B; --muted:#56655E; --line:rgba(20,32,27,.10);
  --amber:#C9923B; --amber-t:#F7EBD7; --red:#B5342A; --red-t:#FBEAE7;
  --radius:16px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Outfit',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--bone);line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{line-height:1.12;letter-spacing:-.02em;font-weight:800}
a{color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
section{padding:84px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--g700);margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--amber);border-radius:2px}
h2{font-size:clamp(27px,3.4vw,38px);margin-bottom:12px}
.sub{font-size:16.5px;color:var(--muted);max-width:620px}
.center{text-align:center}.center .eyebrow{justify-content:center}.center .sub{margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 26px;border-radius:12px;font-size:15.5px;font-weight:700;text-decoration:none;border:2px solid transparent;cursor:pointer;font-family:inherit;transition:transform var(--dur-press) var(--ease-out),background .2s var(--ease-out),box-shadow .2s var(--ease-out),border-color .2s var(--ease-out);text-align:center;white-space:nowrap}
.btn:active{transform:scale(.97)}
.btn-green{background:var(--emerald);color:#fff;box-shadow:0 10px 24px rgba(14,122,92,.28)}
.btn-green:hover{background:var(--emerald-b)}
.btn-red{background:var(--red);color:#fff;box-shadow:0 10px 24px rgba(181,52,42,.26)}
.btn-red:hover{background:#9E2B22}
.btn-ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.45)}
.btn-ghost:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.btn-outline-d{background:transparent;color:var(--g800);border-color:rgba(21,86,66,.35)}
.btn-outline-d:hover{border-color:var(--emerald);background:var(--amber-t)}
/* demo strip */
.demobar{background:var(--amber);color:#3A2A08;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;text-align:center;padding:7px 0}
/* nav */
header{position:sticky;top:0;z-index:60;background:rgba(246,243,236,.86);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:14px;height:70px}
.logo{display:flex;align-items:center;gap:11px;text-decoration:none}
.mark{width:42px;height:42px;border-radius:12px;background:var(--g800);display:flex;align-items:center;justify-content:center;flex:none}
.mark svg{width:22px;height:22px}
.logo .t{font-size:16.5px;font-weight:800;line-height:1.05;color:var(--g900)}
.logo .t small{display:block;font-size:9.5px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.nav-links{display:flex;gap:24px}
.nav-links a{text-decoration:none;font-size:14.5px;font-weight:600;color:var(--muted)}
.nav-right{display:flex;align-items:center;gap:10px}
.lang{display:flex;border:1.5px solid var(--line);border-radius:999px;overflow:hidden}
.lang button{border:none;background:transparent;font-family:inherit;font-size:12.5px;font-weight:700;padding:6px 12px;cursor:pointer;color:var(--muted)}
.lang button.on{background:var(--g800);color:#fff}
.concept-chip{font-size:11px;font-weight:700;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:5px 11px;text-decoration:none;white-space:nowrap}
.concept-chip b{color:var(--emerald)}
/* hero */
.hero{background:linear-gradient(180deg,var(--bone) 0%,#EFEADF 100%);padding:64px 0 76px;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:54px;align-items:center}
.hero h1{font-size:clamp(36px,4.6vw,54px);font-weight:800;margin-bottom:18px}
.hero h1 em{font-style:normal;color:var(--emerald)}
.hero .sub{font-size:17.5px;margin-bottom:30px;max-width:520px}
.hero-ctas{display:flex;gap:13px;flex-wrap:wrap}
.hero-media{position:relative}
.hero-media img{width:100%;aspect-ratio:4/3.4;object-fit:cover;border-radius:22px;box-shadow:0 34px 70px rgba(17,67,51,.28)}
.hero-float{position:absolute;left:-18px;bottom:26px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;box-shadow:0 18px 40px rgba(17,67,51,.2);display:flex;align-items:center;gap:12px;max-width:250px}
.hero-float .ic{width:40px;height:40px;border-radius:50%;background:var(--red-t);display:flex;align-items:center;justify-content:center;flex:none;font-size:18px}
.hero-float b{display:block;font-size:14px}
.hero-float span{font-size:12px;color:var(--muted)}
.hero-badge{position:absolute;top:16px;right:16px;background:rgba(17,67,51,.92);color:#fff;border-radius:999px;padding:8px 15px;font-size:12.5px;font-weight:700;backdrop-filter:blur(6px)}
/* stats */
.stats{background:var(--g900);color:#fff;padding:34px 0}
.stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center}
.stat-num{font-size:clamp(27px,3.2vw,38px);font-weight:800;font-variant-numeric:tabular-nums}
.stat-num .u{color:var(--amber);font-size:.72em}
.stat .lbl{font-size:12.5px;color:#B9CBC3;margin-top:2px}
.stat .demo{display:block;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:#7E968C;margin-top:5px}
/* services bento */
.bento{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:46px}
.bcell{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column;transition:transform var(--dur-pop) var(--ease-out),box-shadow var(--dur-pop) var(--ease-out)}
.bcell:hover{box-shadow:0 18px 40px rgba(17,67,51,.12)}
.bcell.photo{padding:0;overflow:hidden;grid-row:span 1}
.bcell.photo img{width:100%;height:178px;object-fit:cover}
.bcell.photo .pin{padding:22px 26px 24px}
.bcell .ico{width:46px;height:46px;border-radius:12px;background:var(--amber-t);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:20px}
.bcell h3{font-size:17px;margin-bottom:6px}
.bcell p{font-size:14px;color:var(--muted)}
.bcell .more{margin-top:auto;padding-top:14px;font-size:13.5px;font-weight:700;color:var(--emerald);text-decoration:none}
/* pricing */
.pricing{background:var(--bone-2)}
.price-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:44px}
.pcard{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px 22px;display:flex;flex-direction:column;position:relative}
.pcard.hot{border:2px solid var(--emerald);box-shadow:0 20px 44px rgba(14,122,92,.16)}
.pflag{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--emerald);color:#fff;font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:999px;white-space:nowrap}
.pico{width:48px;height:48px;border-radius:13px;background:#E7F3EE;display:flex;align-items:center;justify-content:center;font-size:21px;margin-bottom:14px}
.pcard h3{font-size:16.5px;min-height:42px;display:flex;align-items:center}
.pcard .desc{font-size:13px;color:var(--muted);min-height:58px;margin:6px 0 14px}
.price{font-size:30px;font-weight:800;color:var(--g900);font-variant-numeric:tabular-nums}
.price small{font-size:12.5px;font-weight:600;color:var(--muted)}
.pmeta{font-size:11.5px;color:var(--muted);margin:4px 0 14px;letter-spacing:.04em}
.pcard ul{list-style:none;margin-bottom:18px}
.pcard li{font-size:13.5px;padding:5px 0 5px 26px;position:relative;color:#33443D}
.pcard li::before{content:"✓";position:absolute;left:2px;color:var(--emerald);font-weight:800}
.pcard .btn{padding:12px 16px;font-size:14px;width:100%}
.demo-note{text-align:center;font-size:12.5px;color:var(--muted);margin-top:22px}
/* expect split */
.expect-grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:56px;align-items:center}
.expect-media img{width:100%;border-radius:20px;aspect-ratio:4/3;object-fit:cover;box-shadow:0 26px 60px rgba(17,67,51,.22)}
.steps{display:flex;flex-direction:column;gap:20px;margin-top:26px}
.step{display:flex;gap:16px;align-items:flex-start}
.step .n{width:36px;height:36px;border-radius:10px;background:var(--g800);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;font-size:15px}
.step h3{font-size:16.5px;margin-bottom:3px}
.step p{font-size:14.5px;color:var(--muted)}
/* facility gallery */
.facility{background:var(--g900);color:#fff}
.facility .eyebrow{color:var(--amber)}
.facility .sub{color:#B9CBC3}
.gallery{display:grid;grid-template-columns:1.25fr 1fr;grid-template-rows:1fr 1fr;gap:16px;margin-top:44px;height:460px}
.gallery .bg{width:100%;height:100%;background-size:cover;background-position:center;border-radius:16px}
.expect-media .bg{width:100%;border-radius:20px;aspect-ratio:4/3;box-shadow:0 26px 60px rgba(17,67,51,.22);background-size:cover;background-position:center}
.bcell.photo .ph{height:178px;background-size:cover;background-position:center}
.bg-consult{background-image:url(BG_CONSULT)}
.bg-lab{background-image:url(BG_LAB)}
.bg-mat{background-image:url(BG_MAT)}
.gallery .g1{grid-row:1/3}
.gcap{position:relative}
.gcap span{position:absolute;left:12px;bottom:12px;background:rgba(17,67,51,.86);color:#fff;font-size:12px;font-weight:600;padding:6px 12px;border-radius:999px;backdrop-filter:blur(4px)}
/* visit / booking */
.visit-grid{display:grid;grid-template-columns:1fr 470px;gap:54px;align-items:start}
.info-blocks{display:flex;flex-direction:column;gap:14px;margin-top:24px}
.ib{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;display:flex;gap:14px;align-items:flex-start}
.ib .ic{font-size:20px;width:42px;height:42px;border-radius:11px;background:var(--amber-t);display:flex;align-items:center;justify-content:center;flex:none}
.ib h3{font-size:15.5px;margin-bottom:3px}
.ib p{font-size:14px;color:var(--muted)}
.ib a{font-weight:700;color:var(--emerald);text-decoration:none}
.form-card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:32px 28px;box-shadow:0 30px 70px rgba(17,67,51,.14);position:sticky;top:92px}
.form-card h3{font-size:21px;margin-bottom:4px}
.fc-sub{font-size:13.5px;color:var(--muted);margin-bottom:18px}
.fld{margin-bottom:12px}
.fld label{display:block;font-size:12.5px;font-weight:700;color:var(--g900);margin-bottom:5px}
.fld input,.fld select{width:100%;padding:13px 14px;border:1.5px solid var(--line);border-radius:11px;font-size:15px;font-family:inherit;background:var(--bone);color:var(--ink)}
.fld input:focus,.fld select:focus{outline:none;border-color:var(--emerald);box-shadow:0 0 0 4px rgba(14,122,92,.12);background:#fff}
.fgrid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.form-card .btn{width:100%;margin-top:4px}
.form-small{font-size:11.5px;color:var(--muted);text-align:center;margin-top:12px;line-height:1.5}
/* faq */
.faq{background:var(--bone-2)}
.faq-list{max-width:760px;margin:40px auto 0}
.faq-list details{border-bottom:1px solid var(--line);padding:6px 0}
.faq-list summary{cursor:pointer;list-style:none;font-size:16.5px;font-weight:700;padding:14px 30px 14px 0;position:relative;color:var(--g900)}
.faq-list summary::-webkit-details-marker{display:none}
.faq-list summary::after{content:"+";position:absolute;right:4px;top:12px;font-size:24px;font-weight:400;color:var(--emerald);transition:transform var(--dur-menu) var(--ease-out)}
.faq-list details[open] summary::after{transform:rotate(45deg)}
.faq-list .ans{font-size:14.5px;color:var(--muted);padding:0 0 18px;max-width:660px}
/* footer */
footer{background:#0C2E23;color:#9CB5AC;padding:48px 0 24px;font-size:14px}
.amk-bar{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.amk-bar b{color:#fff}
.amk-bar small{display:block;color:#8FA89F;font-size:12.5px;margin-top:3px;max-width:760px}
.f-grid{display:grid;grid-template-columns:1.3fr 1fr 1.2fr;gap:34px;margin-bottom:26px}
.f-grid h5{color:#fff;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
.f-grid a{display:block;text-decoration:none;padding:3px 0}
.f-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:18px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12.5px}
/* mobile cta */
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:70;background:#fff;border-top:1px solid var(--line);padding:10px 12px;gap:9px;box-shadow:0 -8px 24px rgba(0,0,0,.08)}
.mbar a{flex:1}
/* reveal */
.rv{opacity:0;transform:translateY(22px);transition:opacity var(--dur-reveal) var(--ease-out),transform var(--dur-reveal) var(--ease-out)}
.rv.in{opacity:1;transform:none}
@media (hover:hover) and (pointer:fine){
  .btn-green:hover{transform:translateY(-2px)}
  .btn-red:hover{transform:translateY(-2px)}
  .bcell:hover{transform:translateY(-5px)}
  .nav-links a:hover{color:var(--g800)}
    }
@media(max-width:960px){
  .hero-grid,.expect-grid,.visit-grid{grid-template-columns:1fr;gap:40px}
  .bento{grid-template-columns:1fr 1fr}
  .price-grid{grid-template-columns:1fr 1fr}
  .stats .wrap{grid-template-columns:1fr 1fr;gap:26px}
  .form-card{position:static}
  .f-grid{grid-template-columns:1fr 1fr}
  .hero-float{left:10px}
}
@media(max-width:640px){
  section{padding:60px 0}
  .nav-links,.concept-chip{display:none}
  .bento{grid-template-columns:1fr}
  .price-grid{grid-template-columns:1fr}
  .gallery{grid-template-columns:1fr;grid-template-rows:none;height:auto}
  .gallery .g1{grid-row:auto}
  .gcap{height:200px}
  .mbar{display:flex}
  body{padding-bottom:76px}
  .hero{padding:44px 0 56px}
  .hero-ctas .btn{flex:1}
  .wrap{padding:0 16px}
  .nav{height:60px;gap:8px}
  .nav-right{gap:8px}
  .logo{gap:8px;min-width:0}
  .logo .mark{width:30px;height:30px;flex:0 0 30px}
  .logo .t{font-size:13.5px;line-height:1.1;white-space:nowrap}
  .logo .t small{display:none}
  .lang button{padding:6px 9px;font-size:12px}
  .nav-right .btn{padding:9px 14px;font-size:12.5px}
  .demobar{font-size:10.5px;letter-spacing:.1em;padding:6px 12px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
  .rv{opacity:1;transform:none}
}
</style>
</head>
<body>

<div class="demobar" data-en="Demo / concept: fictional medical facility" data-fr="Démo / concept — établissement médical fictif">Demo / concept — fictional medical facility</div>

<header>
  <div class="wrap nav">
    <a class="logo" href="#top">
      <span class="mark"><svg viewBox="0 0 24 24" fill="none"><path d="M10.5 4h3v4.5H18v3h-4.5V16h-3v-4.5H6v-3h4.5z" fill="#F6F3EC"/></svg></span>
      <span class="t">Molyko Medical Centre<small data-en="Clinic · Laboratory · Maternity" data-fr="Clinique · Laboratoire · Maternité">Clinic · Laboratory · Maternity</small></span>
    </a>
    <nav class="nav-links">
      <a href="#services" data-en="Services" data-fr="Services">Services</a>
      <a href="#pricing" data-en="Pricing" data-fr="Tarifs">Pricing</a>
      <a href="#visit" data-en="Visit" data-fr="Visite">Visit</a>
      <a href="#faq" data-en="Questions" data-fr="Questions">Questions</a>
    </nav>
    <div class="nav-right">
      <span class="lang"><button id="btn-en" class="on" onclick="setLang('en')">EN</button><button id="btn-fr" onclick="setLang('fr')">FR</button></span>
      <a class="concept-chip" href="index.html" data-en="Website concept by <b>AMK</b>" data-fr="Site concept par <b>AMK</b>">Website concept by <b>AMK</b></a>
      <a class="btn btn-green" style="padding:10px 18px;font-size:13.5px" href="#book" data-en="Book" data-fr="Rendez-vous">Book</a>
    </div>
  </div>
</header>

<!-- HERO -->
<div class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Private clinic & laboratory · Buea, Cameroon" data-fr="Clinique privée & laboratoire · Buéa, Cameroun">Private clinic & laboratory · Buea, Cameroon</span>
      <h1 data-en="Healthcare that answers, <em>day or night</em>" data-fr="Des soins qui répondent, <em>jour et nuit</em>">Healthcare that answers, <em>day or night</em></h1>
      <p class="sub" data-en="See a doctor today, know the price before you are seen, and book by WhatsApp in English or French. Laboratory results the same day, maternity scans on site." data-fr="Consultez un médecin aujourd'hui, connaissez le prix avant la consultation, et prenez rendez-vous sur WhatsApp en anglais ou en français. Résultats de laboratoire le jour même, échographies sur place.">See a doctor today, know the price before you are seen, and book by WhatsApp in English or French. Laboratory results the same day, maternity scans on site.</p>
      <div class="hero-ctas">
        <a class="btn btn-green" href="#book" data-en="📅 Book an appointment" data-fr="📅 Prendre rendez-vous">📅 Book an appointment</a>
        <a class="btn btn-red" href="tel:+237677789631" data-en="📞 Emergency line" data-fr="📞 Ligne d'urgence">📞 Emergency line</a>
      </div>
    </div>
    <div class="hero-media rv" style="transition-delay:.12s">
      <img src="HERO" alt="Molyko Medical Centre reception" loading="eager">
      <span class="hero-badge" data-en="🕒 Open 7 days · emergencies 24/7" data-fr="🕒 Ouvert 7j/7 · urgences 24h/24">🕒 Open 7 days · emergencies 24/7</span>
      <div class="hero-float">
        <span class="ic">💬</span>
        <div><b data-en="WhatsApp booking" data-fr="Rendez-vous WhatsApp">WhatsApp booking</b><span data-en="Reply in minutes, EN or FR" data-fr="Réponse en quelques minutes, EN ou FR">Reply in minutes, EN or FR</span></div>
      </div>
    </div>
  </div>
</div>

<!-- STATS -->
<div class="stats">
  <div class="wrap">
    <div class="stat"><div class="stat-num" data-count="7">0</div><div class="lbl" data-en="Days open every week" data-fr="Jours d'ouverture par semaine">Days open every week</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num" data-count="90" data-suffix="%">0</div><div class="lbl" data-en="Lab results the same day" data-fr="Résultats labo le jour même">Lab results the same day</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num">2</div><div class="lbl" data-en="Languages: English &amp; French" data-fr="Langues : anglais &amp; français">Languages: English &amp; French</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num">5 000<span class="u"> FCFA</span></div><div class="lbl" data-en="General consultation, from" data-fr="Consultation générale, à partir de">General consultation, from</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
  </div>
</div>

<!-- SERVICES BENTO -->
<section id="services">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="What we care for" data-fr="Nos prises en charge">What we care for</span>
      <h2 data-en="One calm place for most of what your family needs" data-fr="Un lieu serein pour la plupart des besoins de votre famille">One calm place for most of what your family needs</h2>
      <p class="sub" data-en="Six services under one roof, so a consultation, a test and a scan do not mean three trips across town." data-fr="Six services sous un même toit : une consultation, un examen et une échographie ne vous font pas traverser la ville trois fois.">Six services under one roof, so a consultation, a test and a scan do not mean three trips across town.</p>
    </div>
    <div class="bento">
      <div class="bcell rv"><div class="ico">🩺</div><h3 data-en="General consultation" data-fr="Consultation générale">General consultation</h3><p data-en="Adult and family medicine. Full examination, a diagnosis you understand and a written treatment plan." data-fr="Médecine générale adulte et familiale. Examen complet, diagnostic expliqué et plan de traitement écrit.">Full examination, a diagnosis you understand and a written treatment plan.</p><a class="more" href="#book" data-en="Book a visit →" data-fr="Prendre rendez-vous →">Book a visit →</a></div>
      <div class="bcell photo rv" style="transition-delay:.06s"><div class="ph bg-mat" role="img" aria-label="Maternity ultrasound scan"></div><div class="pin"><div class="ico">🤰</div><h3 data-en="Maternity &amp; 4D ultrasound" data-fr="Maternité &amp; échographie 4D">Maternity &amp; 4D ultrasound</h3><p data-en="Antenatal visits with a live scan: see your baby, and leave with printed images." data-fr="Consultations prénatales avec échographie en direct : voyez votre bébé et repartez avec les images.">Antenatal visits with a live scan: see your baby, and leave with printed images.</p></div></div>
      <div class="bcell rv" style="transition-delay:.12s"><div class="ico">🧪</div><h3 data-en="Diagnostic laboratory" data-fr="Laboratoire d'analyses">Diagnostic laboratory</h3><p data-en="Blood counts, malaria and typhoid screening, blood sugar, urinalysis and more, same day." data-fr="Numérations sanguines, dépistages paludisme et fièvre typhoïde, glycémie, analyse d'urines et plus, le jour même.">Blood counts, malaria and typhoid screening, blood sugar, urinalysis and more, same day.</p><a class="more" href="#book" data-en="Book a test →" data-fr="Planifier un examen →">Book a test →</a></div>
      <div class="bcell photo rv"><div class="ph bg-lab" role="img" aria-label="Clinic laboratory"></div><div class="pin"><div class="ico">🔬</div><h3 data-en="Modern equipment" data-fr="Équipement moderne">Modern equipment</h3><p data-en="Maintained analyzers and sterile procedures for every patient, every time." data-fr="Analyseurs entretenus et procédures stériles pour chaque patient, à chaque fois.">Maintained analyzers and sterile procedures for every patient, every time.</p></div></div>
      <div class="bcell rv" style="transition-delay:.06s"><div class="ico">👶</div><h3 data-en="Pediatric checkups" data-fr="Consultations pédiatriques">Pediatric checkups</h3><p data-en="Growth checks, vaccination review and unhurried parent questions, in the language you speak at home." data-fr="Suivi de croissance, revue de vaccination et réponses sans précipitation aux questions des parents.">Growth checks, vaccination review and unhurried parent questions, in the language you speak at home.</p><a class="more" href="#book" data-en="Book a child visit →" data-fr="Rendez-vous enfant →">Book a child visit →</a></div>
      <div class="bcell rv" style="transition-delay:.12s"><div class="ico">💊</div><h3 data-en="Pharmacy, insurance &amp; home visits" data-fr="Pharmacie, assurances &amp; visites à domicile">Pharmacy, insurance &amp; home visits</h3><p data-en="Common medicines on site, accepted insurance partners, and home visits for patients who cannot travel." data-fr="Médicaments courants sur place, partenaires d'assurance acceptés, et visites à domicile pour les patients alités.">Common medicines on site, accepted insurance partners, and home visits for patients who cannot travel.</p></div>
    </div>
  </div>
</section>

<!-- PRICING -->
<section class="pricing" id="pricing">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Honest pricing" data-fr="Tarifs honnêtes">Honest pricing</span>
      <h2 data-en="The price you see is the price you pay" data-fr="Le prix affiché est le prix que vous payez">The price you see is the price you pay</h2>
      <p class="sub" data-en="Baseline prices for our most requested services. Pay by cash, MTN Mobile Money, Orange Money or insurance. Replace these cards with your real price list at launch." data-fr="Tarifs de base pour nos services les plus demandés. Paiement en espèces, MTN MoMo, Orange Money ou assurance. Ces cartes sont remplacées par vos vrais tarifs au lancement.">Baseline prices for our most requested services. Pay by cash, MTN Mobile Money, Orange Money or insurance. Replace these cards with your real price list at launch.</p>
    </div>
    <div class="price-grid">
      <div class="pcard rv">
        <div class="pico">🩺</div>
        <h3 data-en="General consultation" data-fr="Consultation générale">General consultation</h3>
        <p class="desc" data-en="Full history, examination, diagnosis and a treatment plan you understand." data-fr="Anamnèse complète, examen, diagnostic et plan de traitement expliqué.">Full history, examination, diagnosis and a treatment plan you understand.</p>
        <div class="price">5 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="~30 MIN · (DEMO)" data-fr="~30 MIN · (DÉMO)">~30 MIN · (DEMO)</div>
        <ul>
          <li data-en="Clinical examination" data-fr="Examen clinique">Clinical examination</li>
          <li data-en="Diagnosis &amp; treatment plan" data-fr="Diagnostic &amp; plan de traitement">Diagnosis &amp; treatment plan</li>
          <li data-en="Referral coordination" data-fr="Coordination des références">Referral coordination</li>
        </ul>
        <a class="btn btn-outline-d" href="#book" data-en="Book this service" data-fr="Réserver ce service">Book this service</a>
      </div>
      <div class="pcard hot rv" style="transition-delay:.06s">
        <div class="pflag" data-en="Most requested" data-fr="Le plus demandé">Most requested</div>
        <div class="pico">🤰</div>
        <h3 data-en="Maternity &amp; 4D ultrasound scan" data-fr="Maternité &amp; échographie 4D">Maternity &amp; 4D ultrasound scan</h3>
        <p class="desc" data-en="Prenatal consultation with a live 4D scan. See your baby before you meet them." data-fr="Consultation prénatale avec échographie 4D en direct. Voyez votre bébé avant de le rencontrer.">Prenatal consultation with a live 4D scan. See your baby before you meet them.</p>
        <div class="price">25 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="~60 MIN · (DEMO)" data-fr="~60 MIN · (DÉMO)">~60 MIN · (DEMO)</div>
        <ul>
          <li data-en="Prenatal consultation" data-fr="Consultation prénatale">Prenatal consultation</li>
          <li data-en="4D scan &amp; printed images" data-fr="Échographie 4D &amp; images imprimées">4D scan &amp; printed images</li>
          <li data-en="Wellbeing assessment" data-fr="Évaluation du bien-être">Wellbeing assessment</li>
        </ul>
        <a class="btn btn-green" href="#book" data-en="Book a scan" data-fr="Réserver une échographie">Book a scan</a>
      </div>
      <div class="pcard rv" style="transition-delay:.12s">
        <div class="pico">🧫</div>
        <h3 data-en="Diagnostic laboratory panel" data-fr="Bilan de laboratoire">Diagnostic laboratory panel</h3>
        <p class="desc" data-en="Same-day blood work: the standard panel our doctors trust for first visits." data-fr="Analyses le jour même : le bilan standard que nos médecins utilisent en première visite.">Same-day blood work: the standard panel our doctors trust for first visits.</p>
        <div class="price">15 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="~20 MIN · (DEMO)" data-fr="~20 MIN · (DÉMO)">~20 MIN · (DEMO)</div>
        <ul>
          <li data-en="Full blood count" data-fr="Numération sanguine complète">Full blood count</li>
          <li data-en="Malaria &amp; typhoid screening" data-fr="Dépistage paludisme &amp; typhoïde">Malaria &amp; typhoid screening</li>
          <li data-en="Blood sugar, lipids, urinalysis" data-fr="Glycémie, lipides, analyse d'urines">Blood sugar, lipids, urinalysis</li>
        </ul>
        <a class="btn btn-outline-d" href="#book" data-en="Book laboratory" data-fr="Réserver au labo">Book laboratory</a>
      </div>
      <div class="pcard rv" style="transition-delay:.18s">
        <div class="pico">👶</div>
        <h3 data-en="Pediatric checkup" data-fr="Consultation pédiatrique">Pediatric checkup</h3>
        <p class="desc" data-en="Growth, development and a parent Q&amp;A, unhurried and in your language." data-fr="Croissance, développement et questions-réponses avec les parents, sans hâte et en votre langue.">Growth, development and a parent Q&amp;A, unhurried and in your language.</p>
        <div class="price">7 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="~40 MIN · (DEMO)" data-fr="~40 MIN · (DÉMO)">~40 MIN · (DEMO)</div>
        <ul>
          <li data-en="Growth &amp; development check" data-fr="Contrôle croissance &amp; développement">Growth &amp; development check</li>
          <li data-en="Vaccination review" data-fr="Revue du carnet de vaccination">Vaccination review</li>
          <li data-en="Nutrition guidance" data-fr="Conseils en nutrition">Nutrition guidance</li>
        </ul>
        <a class="btn btn-outline-d" href="#book" data-en="Book a child visit" data-fr="Rendez-vous enfant">Book a child visit</a>
      </div>
    </div>
    <p class="demo-note" data-en="(DEMO) Sample prices for this concept. Your real services and prices replace these before launch." data-fr="(DÉMO) Tarifs d'exemple pour ce concept. Vos vrais services et tarifs les remplacent avant le lancement.">(DEMO) Sample prices for this concept. Your real services and prices replace these before launch.</p>
  </div>
</section>

<!-- WHAT TO EXPECT -->
<section>
  <div class="wrap expect-grid">
    <div class="expect-media rv"><div class="bg bg-consult" role="img" aria-label="Doctor listening to a patient"></div></div>
    <div class="rv" style="transition-delay:.1s">
      <span class="eyebrow" data-en="Your visit" data-fr="Votre visite">Your visit</span>
      <h2 data-en="Nervous about the visit? That is normal here." data-fr="Anxieux à l'idée de consulter ? C'est normal ici.">Nervous about the visit? That is normal here.</h2>
      <p class="sub" data-en="We removed the things patients dislike most: unknown prices, long waits and unexplained treatment." data-fr="Nous avons supprimé ce que les patients redoutent le plus : tarifs inconnus, longues attentes et traitements inexpliqués.">We removed the things patients dislike most: unknown prices, long waits and unexplained treatment.</p>
      <div class="steps">
        <div class="step"><span class="n">1</span><div><h3 data-en="Book in 30 seconds on WhatsApp" data-fr="Réservez en 30 secondes sur WhatsApp">Book in 30 seconds on WhatsApp</h3><p data-en="Choose a service and a time. We confirm your slot the same day, in English or French." data-fr="Choisissez un service et une heure. Nous confirmons le créneau le jour même, en anglais ou en français.">Choose a service and a time. We confirm your slot the same day, in English or French.</p></div></div>
        <div class="step"><span class="n">2</span><div><h3 data-en="We explain before anything happens" data-fr="On explique avant chaque geste">We explain before anything happens</h3><p data-en="You hear the diagnosis, the options and the price, and you agree before treatment begins." data-fr="Vous entendez le diagnostic, les options et le prix, et vous donnez votre accord avant tout traitement.">You hear the diagnosis, the options and the price, and you agree before treatment begins.</p></div></div>
        <div class="step"><span class="n">3</span><div><h3 data-en="Results and follow-up on WhatsApp" data-fr="Résultats et suivi sur WhatsApp">Results and follow-up on WhatsApp</h3><p data-en="Laboratory results and your next steps arrive in your chat. No second trip just to collect paper." data-fr="Les résultats et les prochaines étapes arrivent dans votre discussion. Pas de second déplacement pour récupérer un papier.">Laboratory results and your next steps arrive in your chat. No second trip just to collect paper.</p></div></div>
      </div>
    </div>
  </div>
</section>

<!-- FACILITY -->
<section class="facility">
  <div class="wrap">
    <div class="rv">
      <span class="eyebrow" data-en="Inside the centre" data-fr="À l'intérieur du centre">Inside the centre</span>
      <h2 data-en="Clean, quiet and easy to find" data-fr="Propre, calme et facile à trouver">Clean, quiet and easy to find</h2>
      <p class="sub" data-en="Reception, consultation rooms, laboratory and ultrasound in one building." data-fr="Accueil, salles de consultation, laboratoire et échographie dans un seul bâtiment.">Reception, consultation rooms, laboratory and ultrasound in one building.</p>
    </div>
    <div class="gallery rv">
      <div class="gcap g1 bg bg-consult"><span data-en="Reception" data-fr="Accueil">Reception</span></div>
      <div class="gcap bg bg-lab"><span data-en="Laboratory" data-fr="Laboratoire">Laboratory</span></div>
      <div class="gcap bg bg-mat"><span data-en="Ultrasound room" data-fr="Salle d'échographie">Ultrasound room</span></div>
    </div>
  </div>
</section>

<!-- VISIT + BOOKING -->
<section id="visit">
  <div class="wrap visit-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Visit us" data-fr="Nous rendre visite">Visit us</span>
      <h2 id="book" data-en="Book in three steps, on WhatsApp" data-fr="Réservez en trois étapes, sur WhatsApp">Book in three steps, on WhatsApp</h2>
      <p class="sub" data-en="No account, no waiting on hold. Your request opens WhatsApp already written; nothing is sent without you. We confirm the same day. Reference: MMC-XXXX." data-fr="Pas de compte, pas d'attente au téléphone. Votre demande ouvre WhatsApp déjà rédigée ; rien n'est envoyé sans vous. Confirmation le jour même. Référence : MMC-XXXX.">No account, no waiting on hold. Your request opens WhatsApp already written; nothing is sent without you. We confirm the same day. Reference: MMC-XXXX.</p>
      <div class="info-blocks">
        <div class="ib"><span class="ic">📍</span><div><h3 data-en="Find us" data-fr="Nous trouver">Find us</h3><p data-en="Main road, Molyko, Buea. Two minutes from the main junction (concept address)." data-fr="Route principale, Molyko, Buéa. À deux minutes du carrefour principal (adresse de démo).">Main road, Molyko, Buea. Two minutes from the main junction (concept address).</p></div></div>
        <div class="ib"><span class="ic">🕒</span><div><h3 data-en="Opening hours" data-fr="Heures d'ouverture">Opening hours</h3><p data-en="Monday to Saturday 7:30 to 19:00 · Sundays and after hours: emergencies by line." data-fr="Lundi au samedi 7h30 à 19h00 · Dimanches et après les heures : urgences par la ligne.">Monday to Saturday 7:30 to 19:00 · Sundays and after hours: emergencies by line.</p></div></div>
        <div class="ib"><span class="ic">📞</span><div><h3 data-en="Call or WhatsApp" data-fr="Appel ou WhatsApp">Call or WhatsApp</h3><p><a href="tel:+237677789631">+237 677 789 631</a> <span data-en="(demo routing to AMK)" data-fr="(acheminement démo vers AMK)">(demo routing to AMK)</span></p></div></div>
      </div>
    </div>
    <form class="form-card rv" style="transition-delay:.1s" onsubmit="return book(event)">
      <h3 data-en="Request an appointment" data-fr="Demander un rendez-vous">Request an appointment</h3>
      <p class="fc-sub" data-en="30 seconds. We confirm on WhatsApp the same day." data-fr="30 secondes. Confirmation WhatsApp le jour même.">30 seconds. We confirm on WhatsApp the same day.</p>
      <div class="fgrid2">
        <div class="fld"><label for="b-fn" data-en="Your name *" data-fr="Votre nom *">Your name *</label><input id="b-fn" type="text" required></div>
        <div class="fld"><label for="b-ph" data-en="WhatsApp number *" data-fr="Numéro WhatsApp *">WhatsApp number *</label><input id="b-ph" type="tel" required></div>
      </div>
      <div class="fld"><label for="b-sv" data-en="Service *" data-fr="Service *">Service *</label>
        <select id="b-sv" required>
          <option data-en="General consultation" data-fr="Consultation générale">General consultation</option>
          <option data-en="Laboratory test" data-fr="Examen de laboratoire">Laboratory test</option>
          <option data-en="Maternity &amp; ultrasound" data-fr="Maternité &amp; échographie">Maternity &amp; ultrasound</option>
          <option data-en="Pediatric visit" data-fr="Consultation pédiatrique">Pediatric visit</option>
          <option data-en="Pharmacy / insurance" data-fr="Pharmacie / assurance">Pharmacy / insurance</option>
          <option data-en="Home visit" data-fr="Visite à domicile">Home visit</option>
          <option data-en="Not sure yet" data-fr="Je ne sais pas encore">Not sure yet</option>
          <option data-en="Emergency (same day)" data-fr="Urgence (le jour même)">Emergency (same day)</option>
        </select>
      </div>
      <div class="fgrid2">
        <div class="fld"><label for="b-day" data-en="Day" data-fr="Jour">Day</label>
          <select id="b-day"><option data-en="Today" data-fr="Aujourd'hui">Today</option><option data-en="Tomorrow" data-fr="Demain">Tomorrow</option><option data-en="This week" data-fr="Cette semaine">This week</option></select>
        </div>
        <div class="fld"><label for="b-time" data-en="Time" data-fr="Heure">Time</label>
          <select id="b-time"><option data-en="Morning" data-fr="Matin">Morning</option><option data-en="Afternoon" data-fr="Après-midi">Afternoon</option><option data-en="Any time" data-fr="Peu importe">Any time</option></select>
        </div>
      </div>
      <div class="fld"><label for="b-q" data-en="Note (optional)" data-fr="Note (facultatif)">Note (optional)</label><input id="b-q" type="text"></div>
      <button class="btn btn-green" type="submit" data-en="Send my request →" data-fr="Envoyer ma demande →">Send my request →</button>
      <p class="form-small" data-en="Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the clinic's own number and logs the booking." data-fr="Ouvre WhatsApp avec votre message rédigé. Acheminement démo vers AMK ; sur votre site en ligne, cela arrive au numéro de la clinique et enregistre la réservation.">Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the clinic's own number and logs the booking.</p>
    </form>
  </div>
</section>

<!-- FAQ -->
<section class="faq" id="faq">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Quick answers" data-fr="Réponses rapides">Quick answers</span>
      <h2 data-en="The questions we hear most" data-fr="Les questions que nous entendons le plus">The questions we hear most</h2>
    </div>
    <div class="faq-list rv">
      <details><summary data-en="Do I need an appointment?" data-fr="Faut-il un rendez-vous ?">Do I need an appointment?</summary><div class="ans" data-en="Walk-ins are welcome, but booking on WhatsApp means a confirmed slot and little or no waiting. Emergencies are seen immediately." data-fr="Les visites sans rendez-vous sont acceptées, mais réserver sur WhatsApp garantit un créneau confirmé et peu d'attente. Les urgences sont prises immédiatement.">Walk-ins are welcome, but booking on WhatsApp means a confirmed slot and little or no waiting. Emergencies are seen immediately.</div></details>
      <details><summary data-en="How do I pay, and do you take insurance?" data-fr="Comment payer, et acceptez-vous les assurances ?">How do I pay, and do you take insurance?</summary><div class="ans" data-en="Cash, MTN Mobile Money and Orange Money at the desk. We work with selected insurance partners; send your insurer's name on WhatsApp before the visit." data-fr="Espèces, MTN MoMo et Orange Money à l'accueil. Nous travaillons avec des partenaires d'assurance sélectionnés ; envoyez le nom de votre assurance sur WhatsApp avant la visite.">Cash, MTN Mobile Money and Orange Money at the desk. We work with selected insurance partners; send your insurer's name on WhatsApp before the visit.</div></details>
      <details><summary data-en="How fast are laboratory results?" data-fr="Quelle est la rapidité des résultats de laboratoire ?">How fast are laboratory results?</summary><div class="ans" data-en="Most routine panels are ready the same day and are sent to you on WhatsApp, with an explanation of what they mean." data-fr="La plupart des bilans de routine sont prêts le jour même et vous sont envoyés sur WhatsApp, avec une explication claire.">Most routine panels are ready the same day and are sent to you on WhatsApp, with an explanation of what they mean.</div></details>
      <details><summary data-en="Do you see patients in French?" data-fr="Recevez-vous les patients en français ?">Do you see patients in French?</summary><div class="ans" data-en="Yes. Reception, doctors and the laboratory work in English and French, and this website switches language with one tap." data-fr="Oui. L'accueil, les médecins et le laboratoire travaillent en anglais et en français, et ce site change de langue en une touche.">Yes. Reception, doctors and the laboratory work in English and French, and this website switches language with one tap.</div></details>
      <details><summary data-en="What counts as an emergency after hours?" data-fr="Qu'est-ce qu'une urgence après les heures ?">What counts as an emergency after hours?</summary><div class="ans" data-en="Severe pain, breathing difficulty, high fever that will not break, heavy bleeding, pregnancy complications. Call the emergency line and we direct you immediately." data-fr="Douleur intense, difficulté à respirer, forte fièvre qui ne baisse pas, saignement abondant, complications de grossesse. Appelez la ligne d'urgence et nous vous orientons immédiatement.">Severe pain, breathing difficulty, high fever that will not break, heavy bleeding, pregnancy complications. Call the emergency line and we direct you immediately.</div></details>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="wrap">
    <div class="amk-bar">
      <span class="t"><b data-en="This website is a concept by AMK" data-fr="Ce site est un concept d'AMK">This website is a concept by AMK</b> — Web Development &amp; Digital Solutions<small data-en="Patient-first, bilingual (EN|FR), mobile-fast clinic template with transparent FCFA pricing and WhatsApp booking. Replace the name, photos, prices and team with your clinic's own, and it is yours in 3 to 5 days." data-fr="Modèle de clinique pensé patient, bilingue (EN|FR), rapide sur mobile, avec tarifs FCFA transparents et réservation WhatsApp. Remplacez nom, photos, tarifs et équipe par ceux de votre clinique, et il est à vous en 3 à 5 jours.">Patient-first, bilingual (EN|FR), mobile-fast clinic template with transparent FCFA pricing and WhatsApp booking. Replace the name, photos, prices and team with your clinic's own, and it is yours in 3 to 5 days.</small></span>
      <a class="btn btn-green" style="padding:12px 22px;font-size:14px" href="index.html" data-en="Back to AMK website" data-fr="Retour au site d'AMK">Back to AMK website</a>
    </div>
    <div class="f-grid">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
          <span class="mark" style="width:38px;height:38px;border-radius:11px"><svg viewBox="0 0 24 24" fill="none"><path d="M10.5 4h3v4.5H18v3h-4.5V16h-3v-4.5H6v-3h4.5z" fill="#F6F3EC"/></svg></span>
          <b style="color:#fff;font-size:15.5px">Molyko Medical Centre</b>
        </div>
        <p data-en="Your street, your town, Cameroon (demo address)" data-fr="Votre rue, votre ville, Cameroun (adresse de démo)">Your street, your town, Cameroon (demo address)</p>
        <p style="margin-top:6px"><a href="tel:+237677789631">+237 677 789 631</a></p>
        <p style="margin-top:10px;font-size:12.5px;color:#7E968C" data-en="Demo facility. Replace with the real Google Maps embed, hours and team before launch." data-fr="Établissement de démo. Remplacer par la vraie carte Google Maps, les heures et l'équipe avant lancement.">Demo facility. Replace with the real Google Maps embed, hours and team before launch.</p>
      </div>
      <div>
        <h5 data-en="Quick links" data-fr="Liens rapides">Quick links</h5>
        <a href="#services" data-en="Services" data-fr="Services">Services</a>
        <a href="#pricing" data-en="Pricing" data-fr="Tarifs">Pricing</a>
        <a href="#visit" data-en="Book a visit" data-fr="Prendre rendez-vous">Book a visit</a>
        <a href="#faq" data-en="Questions" data-fr="Questions">Questions</a>
      </div>
      <div>
        <h5 data-en="Good to know" data-fr="Bon à savoir">Good to know</h5>
        <p style="font-size:13px" data-en="Sterile procedure for every patient · works on any mobile connection · WCAG-minded accessibility · prices and hours clearly published, in English and French." data-fr="Procédure stérile pour chaque patient · fonctionne sur toute connexion mobile · accessibilité inspirée de WCAG · tarifs et heures clairement publiés, en anglais et en français.">Sterile procedure for every patient · works on any mobile connection · WCAG-minded accessibility · prices and hours clearly published, in English and French.</p>
      </div>
    </div>
    <div class="f-bottom">
      <span data-en="© 2026 Molyko Medical Centre (concept)" data-fr="© 2026 Molyko Medical Centre (concept)">© 2026 Molyko Medical Centre (concept)</span>
      <span>Concept by AMK · Web Development &amp; Digital Solutions</span>
    </div>
  </div>
</footer>

<div class="mbar">
  <a class="btn btn-red" href="tel:+237677789631" data-en="Emergency" data-fr="Urgence">Emergency</a>
  <a class="btn btn-green" href="#book" data-en="Book on WhatsApp →" data-fr="Réserver sur WhatsApp →">Book on WhatsApp →</a>
</div>

<script>
var WA_NUM = "237677789631"; // AMK demo routing; replace with the clinic's number at launch
function setLang(l){
  document.documentElement.lang = l;
  document.querySelectorAll("[data-en]").forEach(function(el){ el.innerHTML = (l === "fr") ? el.getAttribute("data-fr") : el.getAttribute("data-en"); });
  document.getElementById("btn-en").classList.toggle("on", l === "en");
  document.getElementById("btn-fr").classList.toggle("on", l === "fr");
  try{ history.replaceState(null, "", l === "fr" ? "?lang=fr" : "sample-clinic.html"); }catch(e){}
}
var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target); } }); }, {threshold:.12});
document.querySelectorAll(".rv").forEach(function(el){ io.observe(el); });
var counted = false;
var cio = new IntersectionObserver(function(es){ es.forEach(function(en){
  if(en.isIntersecting && !counted){
    counted = true;
    document.querySelectorAll(".stat-num[data-count]").forEach(function(el){
      var target = parseInt(el.getAttribute("data-count"), 10), suffix = el.getAttribute("data-suffix") || "", start = null, dur = 1400;
      function tick(now){ if(!start) start = now; var p = Math.min((now-start)/dur,1), e = 1 - Math.pow(1-p,3); el.innerHTML = Math.round(target*e) + suffix; if(p<1) requestAnimationFrame(tick); }
      requestAnimationFrame(tick);
    });
    cio.disconnect();
  }
}); }, {threshold:.4});
var statsEl = document.querySelector(".stats"); if(statsEl) cio.observe(statsEl);
function book(e){
  e.preventDefault();
  var fr = document.documentElement.lang === "fr";
  var name = document.getElementById("b-fn").value.trim();
  var phone = document.getElementById("b-ph").value.trim();
  var sv = document.getElementById("b-sv").selectedOptions[0].text;
  var day = document.getElementById("b-day").selectedOptions[0].text;
  var tm = document.getElementById("b-time").selectedOptions[0].text;
  var q = document.getElementById("b-q").value.trim();
  var ref = "MMC-" + Math.floor(1000 + Math.random()*9000);
  var msg = fr
    ? "Bonjour Molyko Medical Centre ! Je souhaite prendre rendez-vous.\n\nNom : " + name + "\nTéléphone : " + phone + "\nService : " + sv + "\nJour : " + day + "\nHeure : " + tm + (q ? "\nNote : " + q : "") + "\nRéférence : " + ref
    : "Hello Molyko Medical Centre! I would like to book an appointment.\n\nName: " + name + "\nPhone: " + phone + "\nService: " + sv + "\nDay: " + day + "\nTime: " + tm + (q ? "\nNote: " + q : "") + "\nReference: " + ref;
  window.open("https://wa.me/" + WA_NUM + "?text=" + encodeURIComponent(msg), "_blank");
  return false;
}
(function(){ var p = new URLSearchParams(location.search).get("lang"); if(p === "fr" || p === "en"){ setLang(p); } })();
</script>
</body>
</html>
"""

HTML = (HTML
        .replace('src="HERO"', 'src="%s"' % IMG["hero"])
        .replace("url(BG_CONSULT)", "url('%s')" % IMG["consult"])
        .replace("url(BG_LAB)", "url('%s')" % IMG["lab"])
        .replace("url(BG_MAT)", "url('%s')" % IMG["maternity"]))

out = HERE / "sample-clinic.html"
out.write_text(HTML, encoding="utf-8")
print("wrote", out, round(len(HTML)/1024), "KB")
