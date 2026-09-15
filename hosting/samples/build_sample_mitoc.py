# -*- coding: utf-8 -*-
"""Build site/mitoc.html — NAMED concept preview for Midas Touch Optic Center
(MITOC), Molyko-Malingo, Buea. Built before the warm yes at King's request;
send only after MITOC accepts the free preview (Invitation-First rule).

Stage 1 verified facts (Tier A, their own Facebook intro):
- "We refract, prescribe n mount lenses" -> eye exam/refraction, prescription
  lenses, lens mounting are the ONLY claimed services.
- Address: Molyko, opposite the former police station, Malingo (page intro).
- Line: +237 678 90 89 62 (page number; King WA-profile check still pending).
- Facebook-only presence; no website, no Google listing found.
Everything else (prices, hours, reviews, product brands) is labeled DEMO or
omitted. No contact lenses / surgery / brand names invented.

Design Read: local independent optician landing for student-heavy Molyko
walk-in clients, crisp lens-clear premium-retail language (Warby Parker /
MOSCOT references + King's attached template), leaning toward sheet C
Cobalt + Cream (STYLE-TOKENS.md, queued for MITOC).
Dials: VARIANCE 6 · MOTION 4 · DENSITY 4 (school/clinic conversion preset).
Reference override (law §4.4): attached template carries an eyebrow on nearly
every section -> page-wide eyebrows are reference-instructed, exempt from the
1-per-3 eyebrow ration. Logged in delivery notes.
Single file, base64 images, AMK demo routing to 237677789631, ref MIT-XXXX.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent

def b64img(name):
    data = (HERE / "img" / name).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()

IMG = {k: b64img("mit-%s.jpg" % k) for k in
       ("hero", "exam", "wall", "craft", "fit", "flatlay", "f1", "f2", "f3")}

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midas Touch Optic Center, Molyko Buea · Eye Exams, Lenses &amp; Frames (Website Concept by AMK)</title>
<meta name="description" content="A website concept for Midas Touch Optic Center, Molyko-Malingo, Buea: eye tests and refraction, prescription lenses mounted on site, frame gallery, WhatsApp booking, English and French.">
<link rel="canonical" href="https://amk-cm.vercel.app/mitoc.html">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='2' y='2' width='28' height='28' rx='8' fill='%2315539E'/%3E%3Cg fill='none' stroke='%23F7F5EE' stroke-width='2'%3E%3Ccircle cx='10.5' cy='17' r='4.5'/%3E%3Ccircle cx='21.5' cy='17' r='4.5'/%3E%3Cpath d='M15 17h2M6 15l-2-1.5M26 15l2-1.5'/%3E%3C/g%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Optician",
  "name": "Midas Touch Optic Center (concept preview)",
  "url": "https://amk-cm.vercel.app/mitoc.html",
  "telephone": "+237 677 789 631",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Malingo, opposite the former police station, Molyko",
    "addressLocality": "Buea",
    "addressRegion": "South-West",
    "addressCountry": "CM"
  }
}
</script>
<style>
:root{
  --ease-out:cubic-bezier(.23,1,.32,1);
  --ease-in-out:cubic-bezier(.77,0,.175,1);
  --ease-drawer:cubic-bezier(.32,.72,0,1);
  --dur-press:140ms;--dur-pop:170ms;--dur-menu:220ms;--dur-panel:320ms;--dur-reveal:520ms;
  --ink:#10202E; --ink-soft:#46596A; --surface:#F7F5EE; --surface-2:#FFFFFF; --line:#E2E5E1;
  --brand:#15539E; --brand-bright:#0F3F78; --brand-tint:#E2ECF7; --on-brand:#FFFFFF;
  --navy-900:#0C2745; --navy-800:#081E38;
  --accent:#E8A33D; --accent-tint:#FAEFD9;
  --radius:18px; --radius-btn:12px; --radius-input:11px;
  --shadow:0 18px 40px rgba(16,32,46,.13);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
section[id],#book{scroll-margin-top:84px}
body{font-family:'Outfit',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--surface);line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{line-height:1.12;letter-spacing:-.02em;font-weight:800}
a{color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
section{padding:84px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--brand);margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--accent);border-radius:2px}
h2{font-size:clamp(27px,3.4vw,38px);margin-bottom:12px;text-wrap:balance}
.sub{font-size:16.5px;color:var(--ink-soft);max-width:620px}
.center{text-align:center}.center .eyebrow{justify-content:center}.center .sub{margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 26px;border-radius:var(--radius-btn);font-size:15.5px;font-weight:700;text-decoration:none;border:2px solid transparent;cursor:pointer;font-family:inherit;transition:transform var(--dur-press) var(--ease-out),background .2s var(--ease-out),box-shadow .2s var(--ease-out),border-color .2s var(--ease-out),color .2s var(--ease-out);text-align:center;white-space:nowrap}
.btn:active{transform:scale(.97)}
.btn-blue{background:var(--brand);color:#fff;box-shadow:0 10px 24px rgba(21,83,158,.26)}
.btn-blue:hover{background:var(--brand-bright)}
.btn-cream{background:var(--surface);color:var(--navy-900)}
.btn-cream:hover{background:#fff}
.btn-ghost-light{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
.btn-ghost-light:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.btn-outline{background:transparent;color:var(--brand);border-color:rgba(21,83,158,.35)}
.btn-outline:hover{border-color:var(--brand);background:var(--brand-tint)}
/* demo strip */
.demobar{background:var(--accent);color:#3A2A08;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;text-align:center;padding:7px 0}
/* nav */
header{position:sticky;top:0;z-index:60;background:rgba(247,245,238,.86);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:14px;height:70px}
.logo{display:flex;align-items:center;gap:11px;text-decoration:none}
.mark{width:42px;height:42px;border-radius:12px;background:var(--brand);display:flex;align-items:center;justify-content:center;flex:none}
.mark svg{width:24px;height:24px}
.logo .t{font-size:16px;font-weight:800;line-height:1.05;color:var(--navy-900)}
.logo .t small{display:block;font-size:9px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:var(--ink-soft)}
.nav-links{display:flex;gap:24px}
.nav-links a{text-decoration:none;font-size:14.5px;font-weight:600;color:var(--ink-soft);transition:color .2s var(--ease-out)}
.nav-right{display:flex;align-items:center;gap:10px}
.lang{display:flex;border:1.5px solid var(--line);border-radius:999px;overflow:hidden}
.lang button{border:none;background:transparent;font-family:inherit;font-size:12.5px;font-weight:700;padding:6px 12px;cursor:pointer;color:var(--ink-soft);transition:background .2s var(--ease-out),color .2s var(--ease-out)}
.lang button:active{transform:scale(.97)}
.lang button.on{background:var(--brand);color:#fff}
.concept-chip{font-size:11px;font-weight:700;color:var(--ink-soft);border:1px solid var(--line);border-radius:99px;padding:5px 11px;text-decoration:none;white-space:nowrap}
.concept-chip b{color:var(--brand)}
.burger{display:none;width:42px;height:42px;border:1.5px solid var(--line);background:var(--surface-2);border-radius:12px;cursor:pointer;position:relative;flex:none;transition:transform var(--dur-press) var(--ease-out)}
.burger:active{transform:scale(.97)}
.burger span{display:block;position:absolute;left:11px;right:11px;height:2px;background:var(--ink);border-radius:2px;transition:transform var(--dur-menu) var(--ease-out),opacity var(--dur-menu) var(--ease-out)}
.burger span:nth-child(1){top:14px}.burger span:nth-child(2){top:20px}.burger span:nth-child(3){top:26px}
.burger.open span:nth-child(1){top:20px;transform:rotate(45deg)}
.burger span:nth-child(2){opacity:1}
.burger.open span:nth-child(2){opacity:0}
.burger.open span:nth-child(3){top:20px;transform:rotate(-45deg)}
/* drawer */
.drawer{position:fixed;inset:0;z-index:80;background:var(--surface);transform:translateX(100%);visibility:hidden;transition:transform var(--dur-panel) var(--ease-drawer),visibility 0s linear var(--dur-panel);display:flex;flex-direction:column}
.drawer.open{transform:none;visibility:visible;transition:transform var(--dur-panel) var(--ease-drawer)}
.drawer-top{height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--line)}
.drawer nav{display:flex;flex-direction:column;padding:26px 28px;gap:6px;flex:1}
.drawer nav a{font-size:22px;font-weight:700;text-decoration:none;padding:12px 0;border-bottom:1px solid var(--line);opacity:0;transform:translateX(18px);transition:opacity var(--dur-panel) var(--ease-out),transform var(--dur-panel) var(--ease-out)}
.drawer.open nav a{opacity:1;transform:none;transition-delay:calc(var(--i)*60ms + 100ms)}
.drawer .d-foot{padding:20px 28px 30px;display:flex;flex-direction:column;gap:12px}
.drawer .d-foot .btn{width:100%}
/* hero */
.hero{background:linear-gradient(180deg,var(--surface) 0%,#ECEFE8 100%);padding:64px 0 76px;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:54px;align-items:center}
.hero h1{font-size:clamp(36px,4.6vw,54px);font-weight:800;margin-bottom:18px}
.hero h1 em{font-style:normal;color:var(--brand)}
.hero .sub{font-size:17.5px;margin-bottom:30px;max-width:520px}
.hero-ctas{display:flex;gap:13px;flex-wrap:wrap}
.hero-media{position:relative}
.hero-media img{width:100%;aspect-ratio:4/4.6;object-fit:cover;object-position:center 28%;border-radius:22px;box-shadow:0 34px 70px rgba(12,39,69,.28)}
.hero-badge{position:absolute;top:16px;left:16px;background:rgba(255,255,255,.92);color:var(--navy-900);border-radius:999px;padding:8px 15px;font-size:12.5px;font-weight:700;backdrop-filter:blur(6px)}
.hero-float{position:absolute;right:-14px;bottom:28px;background:var(--surface-2);border:1px solid var(--line);border-radius:14px;padding:14px 18px;box-shadow:0 18px 40px rgba(12,39,69,.2);display:flex;align-items:center;gap:12px;max-width:250px}
.hero-float .ic{width:40px;height:40px;border-radius:50%;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;flex:none;font-size:18px}
.hero-float b{display:block;font-size:14px}
.hero-float span{font-size:12px;color:var(--ink-soft)}
/* trust strip */
.trust{background:var(--surface-2);border-block:1px solid var(--line);padding:26px 0}
.trust .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.tchip{display:flex;gap:13px;align-items:flex-start}
.tchip .ic{width:42px;height:42px;border-radius:12px;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;font-size:18px;flex:none}
.tchip b{display:block;font-size:14.5px;line-height:1.25}
.tchip span{display:block;font-size:12.5px;color:var(--ink-soft);margin-top:2px}
/* services bento */
.bento{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:46px}
.cell{background:var(--surface-2);border:1px solid var(--line);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column;transition:transform var(--dur-pop) var(--ease-out),box-shadow var(--dur-pop) var(--ease-out)}
.cell.photo{padding:0;overflow:hidden}
.cell.photo .ph{width:100%;background-size:cover;background-position:center}
.cell.photo.wide{grid-column:span 2}
.cell.photo.wide .ph{height:300px}
.cell.photo.narrow .ph{height:190px}
.cell.photo .pin{padding:22px 26px 24px}
.cell .ico{width:46px;height:46px;border-radius:12px;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:20px}
.cell h3{font-size:17px;margin-bottom:6px}
.cell p{font-size:14px;color:var(--ink-soft)}
.cell .more{margin-top:auto;padding-top:14px;font-size:13.5px;font-weight:700;color:var(--brand);text-decoration:none;align-self:flex-start}
.bg-exam{background-image:url(BG_EXAM)}
.bg-craft{background-image:url(BG_CRAFT)}
/* frames rail */
.frames{background:#EFF1EC}
.rail{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:46px}
.fcard{background:var(--surface-2);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column;transition:transform var(--dur-pop) var(--ease-out),box-shadow var(--dur-pop) var(--ease-out)}
.fcard .ph{width:100%;aspect-ratio:1/1;object-fit:cover;background:var(--surface)}
.fcard.tall .ph{aspect-ratio:1/0.82;object-position:center 30%}
.fcard .pin{padding:20px 20px 22px;display:flex;flex-direction:column;flex:1}
.fcard .style{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--brand);margin-bottom:5px}
.fcard h3{font-size:16.5px;margin-bottom:5px}
.fcard p{font-size:13px;color:var(--ink-soft);flex:1}
.fprice{display:flex;align-items:center;gap:8px;margin:12px 0 14px;flex-wrap:wrap}
.fprice b{font-size:17px;font-weight:800;color:var(--navy-900);font-variant-numeric:tabular-nums}
.dtag{display:inline-block;font-size:9.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;background:var(--accent-tint);color:#8A5E14;border-radius:999px;padding:3px 9px}
.fcard .btn{width:100%;padding:11px 14px;font-size:13.5px}
.ownframe{background:var(--navy-900);color:#fff;border-color:transparent}
.ownframe .style{color:var(--accent)}
.ownframe p{color:#B9C8D8}
.ownframe .fprice b{color:#fff}
.demo-note{text-align:center;font-size:12.5px;color:var(--ink-soft);margin-top:22px}
/* steps split */
.steps-grid{display:grid;grid-template-columns:.95fr 1.05fr;gap:56px;align-items:center}
.steps-media img{width:100%;border-radius:20px;aspect-ratio:4/3;object-fit:cover;box-shadow:0 26px 60px rgba(12,39,69,.22)}
.steps{display:flex;flex-direction:column;gap:20px;margin-top:26px}
.step{display:flex;gap:16px;align-items:flex-start}
.step .n{width:36px;height:36px;border-radius:10px;background:var(--brand);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;font-size:15px}
.step h3{font-size:16.5px;margin-bottom:3px}
.step p{font-size:14.5px;color:var(--ink-soft)}
/* dark find band */
.find{position:relative;color:#fff;overflow:hidden}
.find-bg{position:absolute;inset:0;background-size:cover;background-position:center;background-image:url(BG_WALL)}
.find-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(8,30,56,.95) 0%,rgba(8,30,56,.82) 42%,rgba(8,30,56,.45) 78%)}
.find .wrap{position:relative;padding:110px 24px}
.find .eyebrow{color:var(--accent)}
.find h2{color:#fff;max-width:560px}
.find p{color:#C9D7E5;max-width:520px;font-size:16.5px}
.find .fctas{display:flex;gap:13px;flex-wrap:wrap;margin-top:28px}
.find .fnote{margin-top:18px;font-size:12.5px;color:#9DB4C8}
/* visit / booking */
.visit-grid{display:grid;grid-template-columns:1fr 470px;gap:54px;align-items:start}
.info-blocks{display:flex;flex-direction:column;gap:14px;margin-top:24px}
.ib{background:var(--surface-2);border:1px solid var(--line);border-radius:14px;padding:18px 20px;display:flex;gap:14px;align-items:flex-start}
.ib .ic{font-size:20px;width:42px;height:42px;border-radius:11px;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;flex:none}
.ib h3{font-size:15.5px;margin-bottom:3px}
.ib p{font-size:14px;color:var(--ink-soft)}
.ib a{font-weight:700;color:var(--brand);text-decoration:none}
.form-card{background:var(--surface-2);border:1px solid var(--line);border-radius:20px;padding:32px 28px;box-shadow:var(--shadow);position:sticky;top:92px}
.form-card h3{font-size:21px;margin-bottom:4px}
.fc-sub{font-size:13.5px;color:var(--ink-soft);margin-bottom:18px}
.fld{margin-bottom:12px}
.fld label{display:block;font-size:12.5px;font-weight:700;color:var(--navy-900);margin-bottom:5px}
.fld input,.fld select{width:100%;padding:13px 14px;border:1.5px solid var(--line);border-radius:var(--radius-input);font-size:15px;font-family:inherit;background:var(--surface);color:var(--ink);transition:border-color .2s var(--ease-out),box-shadow .2s var(--ease-out),background .2s var(--ease-out)}
.fld input:focus,.fld select:focus{outline:none;border-color:var(--brand);box-shadow:0 0 0 4px rgba(21,83,158,.12);background:#fff}
.fgrid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.form-card .btn{width:100%;margin-top:4px}
.form-small{font-size:11.5px;color:var(--ink-soft);text-align:center;margin-top:12px;line-height:1.5}
/* faq */
.faq{background:#EFF1EC}
.faq-list{max-width:760px;margin:40px auto 0}
.faq-list details{border-bottom:1px solid var(--line);padding:6px 0}
.faq-list summary{cursor:pointer;list-style:none;font-size:16.5px;font-weight:700;padding:14px 30px 14px 0;position:relative;color:var(--navy-900);transition:transform var(--dur-press) var(--ease-out)}
.faq-list summary:active{transform:scale(.99)}
.faq-list summary::-webkit-details-marker{display:none}
.faq-list summary::after{content:"+";position:absolute;right:4px;top:11px;font-size:24px;font-weight:400;color:var(--brand);transition:transform var(--dur-menu) var(--ease-out)}
.faq-list details[open] summary::after{transform:rotate(45deg)}
.faq-list .ans{font-size:14.5px;color:var(--ink-soft);padding:0 0 18px;max-width:660px}
/* footer */
footer{background:var(--navy-800);color:#AFC1D3;padding:48px 0 24px;font-size:14px}
.amk-bar{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.amk-bar b{color:#fff}
.amk-bar small{display:block;color:#93A9BD;font-size:12.5px;margin-top:3px;max-width:760px}
.f-grid{display:grid;grid-template-columns:1.3fr 1fr 1.2fr;gap:34px;margin-bottom:26px}
.f-grid h5{color:#fff;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
.f-grid a{display:block;text-decoration:none;padding:3px 0}
.f-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:18px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12.5px}
/* mobile cta */
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:70;background:#fff;border-top:1px solid var(--line);padding:10px 12px;gap:9px;box-shadow:0 -8px 24px rgba(16,32,46,.1)}
.mbar a{flex:1}
.mbar a:first-child{flex:0 0 96px}
/* press feedback on every remaining pressable */
.cell .more{transition:transform var(--dur-press) var(--ease-out)}
.cell .more:active{transform:scale(.97)}
.drawer nav a:active{transform:scale(.99)}
.concept-chip:active,.logo:active{transform:scale(.97)}
.concept-chip,.logo{transition:transform var(--dur-press) var(--ease-out)}
/* reveal */
.rv{opacity:0;transform:translateY(22px);transition:opacity var(--dur-reveal) var(--ease-out),transform var(--dur-reveal) var(--ease-out)}
.rv.in{opacity:1;transform:none}
@media (hover:hover) and (pointer:fine){
  .btn-blue:hover{transform:translateY(-2px)}
  .btn-cream:hover{transform:translateY(-2px)}
  .cell:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
  .fcard:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
  .nav-links a:hover{color:var(--navy-900)}
  .fcard .more:hover{text-decoration:underline}
}
@media(max-width:960px){
  .hero-grid,.steps-grid,.visit-grid{grid-template-columns:1fr;gap:40px}
  .bento{grid-template-columns:1fr 1fr}
  .cell.photo.wide{grid-column:span 2}
  .rail{grid-template-columns:1fr 1fr}
  .trust .wrap{grid-template-columns:1fr 1fr;gap:22px}
  .form-card{position:static}
  .f-grid{grid-template-columns:1fr 1fr}
  .hero-float{right:8px}
}
@media(max-width:860px){
  .nav-links,.concept-chip{display:none}
  .burger{display:block}
  .nav-right .btn{display:none}
}
@media(max-width:640px){
  section{padding:60px 0}
  .bento{grid-template-columns:1fr}
  .cell.photo.wide{grid-column:span 1}
  .cell.photo.wide .ph{height:220px}
  .rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin-left:-16px;margin-right:-16px;padding:4px 16px 14px;scrollbar-width:none}
  .rail::-webkit-scrollbar{display:none}
  .fcard{min-width:78vw;scroll-snap-align:start;flex:none}
  .trust .wrap{grid-template-columns:1fr;gap:18px}
  .find .wrap{padding:84px 16px}
  .mbar{display:flex}
  body{padding-bottom:76px}
  .hero{padding:44px 0 56px}
  .hero-ctas .btn{flex:1}
  .wrap{padding:0 16px}
  .nav{height:60px;gap:8px}
  .nav-right{gap:8px}
  .logo{gap:8px;min-width:0}
  .logo .mark{width:30px;height:30px;flex:0 0 30px}
  .logo .t{font-size:13px;line-height:1.1;white-space:nowrap}
  .logo .t small{display:none}
  .lang button{padding:6px 9px;font-size:12px}
  .demobar{font-size:10.5px;letter-spacing:.1em;padding:6px 12px}
  .hero-float{left:10px;right:auto;max-width:230px;bottom:18px;padding:12px 14px}
  .hero-badge{font-size:11.5px;padding:7px 12px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
  .rv{opacity:1;transform:none}
  .drawer nav a{opacity:1;transform:none}
}
</style>
</head>
<body>

<div class="demobar" data-en="Demo concept built for Midas Touch Optic Center: sample prices and photos" data-fr="Démo conçue pour Midas Touch Optic Center : prix et photos d'exemple">Demo concept built for Midas Touch Optic Center: sample prices and photos</div>

<header>
  <div class="wrap nav">
    <a class="logo" href="#top">
      <span class="mark"><svg viewBox="0 0 24 24" fill="none" stroke="#F7F5EE" stroke-width="1.8" stroke-linecap="round"><circle cx="8.5" cy="14" r="4"/><circle cx="15.5" cy="14" r="4"/><path d="M12.5 14h-1M4.5 12.5 2.5 11.5M19.5 12.5l2-1"/></svg></span>
      <span class="t">Midas Touch Optic Center<small data-en="Eye tests · Lenses · Frames" data-fr="Examens de vue · Verres · Montures">Eye tests · Lenses · Frames</small></span>
    </a>
    <nav class="nav-links">
      <a href="#services" data-en="Services" data-fr="Services">Services</a>
      <a href="#frames" data-en="Frames" data-fr="Montures">Frames</a>
      <a href="#find" data-en="Find us" data-fr="Nous trouver">Find us</a>
      <a href="#faq" data-en="Questions" data-fr="Questions">Questions</a>
    </nav>
    <div class="nav-right">
      <span class="lang"><button type="button" id="btn-en" class="on" onclick="setLang('en')">EN</button><button type="button" id="btn-fr" onclick="setLang('fr')">FR</button></span>
      <a class="concept-chip" href="index.html" data-en="Website concept by <b>AMK</b>" data-fr="Site concept par <b>AMK</b>">Website concept by <b>AMK</b></a>
      <a class="btn btn-blue" style="padding:10px 18px;font-size:13.5px" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
      <button type="button" class="burger" id="burger" aria-label="Open menu" aria-expanded="false" onclick="toggleDrawer(true)"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<!-- MOBILE DRAWER -->
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-top">
    <span class="t" style="font-size:15px;font-weight:800;color:var(--navy-900)">Midas Touch Optic Center</span>
    <button type="button" class="burger open" aria-label="Close menu" onclick="toggleDrawer(false)"><span></span><span></span><span></span></button>
  </div>
  <nav>
    <a href="#services" style="--i:0" onclick="toggleDrawer(false)" data-en="Services" data-fr="Services">Services</a>
    <a href="#frames" style="--i:1" onclick="toggleDrawer(false)" data-en="Frames" data-fr="Montures">Frames</a>
    <a href="#find" style="--i:2" onclick="toggleDrawer(false)" data-en="Find us" data-fr="Nous trouver">Find us</a>
    <a href="#faq" style="--i:3" onclick="toggleDrawer(false)" data-en="Questions" data-fr="Questions">Questions</a>
  </nav>
  <div class="d-foot">
    <a class="btn btn-blue" href="#book" onclick="toggleDrawer(false)" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
    <a class="btn btn-outline" href="tel:+237677789631" data-en="📞 Call" data-fr="📞 Appeler">📞 Call</a>
  </div>
</div>

<!-- HERO -->
<div class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Independent optician · Molyko, Buea" data-fr="Opticien indépendant · Molyko, Buéa">Independent optician · Molyko, Buea</span>
      <h1 data-en="Sharp vision, <em>fitted properly</em>" data-fr="Une vue nette, <em>bien ajustée</em>">Sharp vision, <em>fitted properly</em></h1>
      <p class="sub" data-en="Eye test, prescription lenses and frame fitting in Malingo. Book by WhatsApp and leave seeing clearly." data-fr="Examen de vue, verres de prescription et ajustage de montures à Malingo. Réservez sur WhatsApp et repartez avec une vue nette.">Eye test, prescription lenses and frame fitting in Malingo. Book by WhatsApp and leave seeing clearly.</p>
      <div class="hero-ctas">
        <a class="btn btn-blue" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        <a class="btn btn-outline" href="#frames" data-en="Browse frames" data-fr="Voir les montures">Browse frames</a>
      </div>
    </div>
    <div class="hero-media rv" style="transition-delay:.12s">
      <img src="HERO" alt="A young client wearing stylish fitted glasses in the Midas Touch optician shop" loading="eager">
      <span class="hero-badge" data-en="📍 Malingo · opposite the former police station" data-fr="📍 Malingo · face à l'ancien commissariat">📍 Malingo · opposite the former police station</span>
      <div class="hero-float">
        <span class="ic">👓</span>
        <div><b data-en="Tested, prescribed, mounted" data-fr="Examen, prescription, montage">Tested, prescribed, mounted</b><span data-en="The full service in one shop" data-fr="Tout le service dans un seul magasin">The full service in one shop</span></div>
      </div>
    </div>
  </div>
</div>

<!-- TRUST STRIP -->
<div class="trust">
  <div class="wrap">
    <div class="tchip rv"><span class="ic">👁️</span><div><b data-en="One complete service" data-fr="Un service complet">One complete service</b><span data-en="We refract, prescribe and mount your lenses" data-fr="Examen de vue, prescription et montage des verres">We refract, prescribe and mount your lenses</span></div></div>
    <div class="tchip rv" style="transition-delay:.06s"><span class="ic">💬</span><div><b data-en="Book by WhatsApp" data-fr="Réservation WhatsApp">Book by WhatsApp</b><span data-en="Pick a day in one message" data-fr="Choisissez un jour en un message">Pick a day in one message</span></div></div>
    <div class="tchip rv" style="transition-delay:.12s"><span class="ic">🌐</span><div><b data-en="English | French site" data-fr="Site anglais | français">English | French site</b><span data-en="Switch language with one tap" data-fr="Changez de langue en une touche">Switch language with one tap</span></div></div>
    <div class="tchip rv" style="transition-delay:.18s"><span class="ic">📍</span><div><b data-en="Easy to find in Molyko" data-fr="Facile à trouver à Molyko">Easy to find in Molyko</b><span data-en="Opposite the former police station, Malingo" data-fr="Face à l'ancien commissariat, Malingo">Opposite the former police station, Malingo</span></div></div>
  </div>
</div>

<!-- SERVICES BENTO -->
<section id="services">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="What we do" data-fr="Nos services">What we do</span>
      <h2 data-en="From eye test to fitted glasses, in one place" data-fr="De l'examen de vue aux lunettes ajustées, au même endroit">From eye test to fitted glasses, in one place</h2>
      <p class="sub" data-en="The three steps most opticians split across shops and days all happen here, under one roof." data-fr="Les trois étapes que la plupart des opticiens séparent en plusieurs lieux et jours se font ici, sous un même toit.">The three steps most opticians split across shops and days all happen here, under one roof.</p>
    </div>
    <div class="bento">
      <div class="cell rv">
        <div class="ico">👁️</div>
        <h3 data-en="Eye test &amp; refraction" data-fr="Examen de vue et réfraction">Eye test &amp; refraction</h3>
        <p data-en="We measure how clearly each eye sees at distance and near, and write the exact prescription you need." data-fr="Nous mesurons la vision de loin et de près de chaque œil, et écrivons la prescription exacte qu'il vous faut.">We measure how clearly each eye sees at distance and near, and write the exact prescription you need.</p>
        <a class="more" href="#book" data-en="Book an eye exam →" data-fr="Réserver un examen de vue →">Book an eye exam →</a>
      </div>
      <div class="cell photo wide rv" style="transition-delay:.06s">
        <div class="ph bg-exam" role="img" aria-label="Optician performing an eye refraction test"></div>
        <div class="pin">
          <h3 data-en="A careful, unhurried test" data-fr="Un examen soigné, sans précipitation">A careful, unhurried test</h3>
          <p data-en="You say what you see; we adjust lens by lens until the prescription is exact." data-fr="Vous dites ce que vous voyez ; nous ajustons verre par verre jusqu'à la prescription exacte.">You say what you see; we adjust lens by lens until the prescription is exact.</p>
        </div>
      </div>
      <div class="cell rv">
        <div class="ico">🔎</div>
        <h3 data-en="Prescription lenses" data-fr="Verres de prescription">Prescription lenses</h3>
        <p data-en="Lenses cut to your prescription for reading, distance or everyday wear, with advice for your budget." data-fr="Des verres taillés à votre prescription pour la lecture, la loin ou le quotidien, avec des conseils selon votre budget.">Lenses cut to your prescription for reading, distance or everyday wear, with advice for your budget.</p>
      </div>
      <div class="cell rv" style="transition-delay:.06s">
        <div class="ico">👓</div>
        <h3 data-en="Frame styling &amp; fitting" data-fr="Choix et ajustage des montures">Frame styling &amp; fitting</h3>
        <p data-en="Try frames with help, then hinges, nose pads and temples are adjusted until the glasses sit right." data-fr="Essayez les montures avec aide, puis charnières, plaquettes et branches sont ajustées jusqu'à ce que les lunettes tiennent parfaitement.">Try frames with help, then hinges, nose pads and temples are adjusted until the glasses sit right.</p>
      </div>
      <div class="cell photo narrow rv" style="transition-delay:.12s">
        <div class="ph bg-craft" role="img" aria-label="Lenses being mounted into a frame"></div>
        <div class="pin">
          <h3 data-en="Lenses mounted in house" data-fr="Montage des verres sur place">Lenses mounted in house</h3>
          <p data-en="Your lenses are cut and fitted into the frame you choose, including frames you bring yourself." data-fr="Vos verres sont taillés et montés dans la monture de votre choix, y compris une monture que vous apportez.">Your lenses are cut and fitted into the frame you choose, including frames you bring yourself.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FRAMES RAIL -->
<section class="frames" id="frames">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="The collection" data-fr="La collection">The collection</span>
      <h2 data-en="Frames for every face and budget" data-fr="Des montures pour chaque visage et budget">Frames for every face and budget</h2>
      <p class="sub" data-en="A sample of frame styles for this concept. The live gallery is photographed in your shop and shows your real prices in FCFA." data-fr="Aperçu de styles pour ce concept. La galerie finale est photographiée dans votre magasin et affiche vos vrais prix en FCFA.">A sample of frame styles for this concept. The live gallery is photographed in your shop and shows your real prices in FCFA.</p>
    </div>
    <div class="rail">
      <div class="fcard rv">
        <img class="ph" src="F1" alt="Black rectangular frame" loading="lazy">
        <div class="pin">
          <span class="style" data-en="Style 01" data-fr="Style 01">Style 01</span>
          <h3 data-en="Black rectangular" data-fr="Noire rectangulaire">Black rectangular</h3>
          <p data-en="A clean, professional shape that suits most faces." data-fr="Une forme nette et professionnelle qui convient à la plupart des visages.">A clean, professional shape that suits most faces.</p>
          <div class="fprice"><b data-en="From 20 000 FCFA" data-fr="À partir de 20 000 FCFA">From 20 000 FCFA</b><span class="dtag" data-en="Demo" data-fr="Démo">Demo</span></div>
          <a class="btn btn-outline" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        </div>
      </div>
      <div class="fcard rv" style="transition-delay:.06s">
        <img class="ph" src="F2" alt="Round tortoiseshell frame" loading="lazy">
        <div class="pin">
          <span class="style" data-en="Style 02" data-fr="Style 02">Style 02</span>
          <h3 data-en="Round tortoiseshell" data-fr="Ronde écaille">Round tortoiseshell</h3>
          <p data-en="A softer, classic look in warm acetate." data-fr="Un style classique et doux en acétate chaud.">A softer, classic look in warm acetate.</p>
          <div class="fprice"><b data-en="From 20 000 FCFA" data-fr="À partir de 20 000 FCFA">From 20 000 FCFA</b><span class="dtag" data-en="Demo" data-fr="Démo">Demo</span></div>
          <a class="btn btn-outline" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        </div>
      </div>
      <div class="fcard rv" style="transition-delay:.12s">
        <img class="ph" src="F3" alt="Thin gold metal frame" loading="lazy">
        <div class="pin">
          <span class="style" data-en="Style 03" data-fr="Style 03">Style 03</span>
          <h3 data-en="Thin gold metal" data-fr="Métal doré fin">Thin gold metal</h3>
          <p data-en="Lightweight lines for a lighter feel all day." data-fr="Des lignes légères pour un porter plus léger toute la journée.">Lightweight lines for a lighter feel all day.</p>
          <div class="fprice"><b data-en="From 25 000 FCFA" data-fr="À partir de 25 000 FCFA">From 25 000 FCFA</b><span class="dtag" data-en="Demo" data-fr="Démo">Demo</span></div>
          <a class="btn btn-outline" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        </div>
      </div>
      <div class="fcard tall ownframe rv" style="transition-delay:.18s">
        <img class="ph" src="FLAT" alt="A collection of frames laid out" loading="lazy">
        <div class="pin">
          <span class="style" data-en="Own frames welcome" data-fr="Vos montures sont les bienvenues">Own frames welcome</span>
          <h3 data-en="Bring a frame you love" data-fr="Apportez une monture que vous aimez">Bring a frame you love</h3>
          <p data-en="We mount new prescription lenses into suitable frames you already own." data-fr="Nous montons de nouveaux verres de prescription dans les montures adaptées que vous possédez déjà.">We mount new prescription lenses into suitable frames you already own.</p>
          <div class="fprice"><a class="btn btn-cream" style="padding:11px 14px;font-size:13.5px" href="#book" data-en="Ask about new lenses →" data-fr="Demander des verres neufs →">Ask about new lenses →</a></div>
        </div>
      </div>
    </div>
    <p class="demo-note" data-en="(Demo) Sample prices for this concept. Your real frames, lens options and prices replace these at launch." data-fr="(Démo) Prix d'exemple pour ce concept. Vos vraies montures, options de verres et prix les remplacent au lancement.">(Demo) Sample prices for this concept. Your real frames, lens options and prices replace these at launch.</p>
  </div>
</section>

<!-- STEPS -->
<section>
  <div class="wrap steps-grid">
    <div class="steps-media rv"><img src="FIT" alt="An optician fitting new glasses on a client" loading="lazy"></div>
    <div class="rv" style="transition-delay:.1s">
      <span class="eyebrow" data-en="How it works" data-fr="Comment ça marche">How it works</span>
      <h2 data-en="Three steps to glasses that feel right" data-fr="Trois étapes vers des lunettes bien ajustées">Three steps to glasses that feel right</h2>
      <div class="steps">
        <div class="step"><span class="n">1</span><div><h3 data-en="Book your eye exam" data-fr="Réservez votre examen de vue">Book your eye exam</h3><p data-en="Message on WhatsApp and choose a day. No long phone calls, no waiting to be told when to come." data-fr="Écrivez sur WhatsApp et choisissez un jour. Sans longs appels ni attente pour savoir quand revenir.">Message on WhatsApp and choose a day. No long phone calls, no waiting to be told when to come.</p></div></div>
        <div class="step"><span class="n">2</span><div><h3 data-en="Get tested and prescribed" data-fr="Examen et prescription">Get tested and prescribed</h3><p data-en="We refract both eyes and explain the result in plain language, with your prescription written down." data-fr="Nous testons les deux yeux et expliquons le résultat simplement, avec une prescription écrite.">We refract both eyes and explain the result in plain language, with your prescription written down.</p></div></div>
        <div class="step"><span class="n">3</span><div><h3 data-en="Choose frames and get fitted" data-fr="Choisissez et faites ajuster">Choose frames and get fitted</h3><p data-en="Try on frames from the wall, then your lenses are mounted and the fit adjusted before you leave." data-fr="Essayez les montures du mur, puis les verres sont montés et l'ajustage fait avant votre départ.">Try on frames from the wall, then your lenses are mounted and the fit adjusted before you leave.</p></div></div>
      </div>
    </div>
  </div>
</section>

<!-- FIND BAND -->
<section class="find" id="find" style="padding:0">
  <div class="find-bg"></div>
  <div class="wrap">
    <div class="rv">
      <span class="eyebrow" data-en="Find us" data-fr="Nous trouver">Find us</span>
      <h2 data-en="In the heart of Molyko, Malingo" data-fr="Au cœur de Molyko, Malingo">In the heart of Molyko, Malingo</h2>
      <p data-en="Midas Touch Optic Center, opposite the former police station, Malingo, Molyko, Buea. Look for the frames in the window." data-fr="Midas Touch Optic Center, face à l'ancien commissariat, Malingo, Molyko, Buéa. Repérez les montures en vitrine.">Midas Touch Optic Center, opposite the former police station, Malingo, Molyko, Buea. Look for the frames in the window.</p>
      <div class="fctas">
        <a class="btn btn-cream" href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        <a class="btn btn-ghost-light" href="https://wa.me/237677789631" target="_blank" rel="noopener" data-en="Chat on WhatsApp" data-fr="Discuter sur WhatsApp">Chat on WhatsApp</a>
      </div>
      <p class="fnote" data-en="The live Google listing, map and opening hours are connected at launch." data-fr="La fiche Google, la carte et les heures d'ouverture sont connectées au lancement.">The live Google listing, map and opening hours are connected at launch.</p>
    </div>
  </div>
</section>

<!-- VISIT + BOOKING -->
<section id="visit">
  <div class="wrap visit-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Book your visit" data-fr="Réserver votre visite">Book your visit</span>
      <h2 id="book" data-en="Book an eye exam on WhatsApp" data-fr="Réservez un examen de vue sur WhatsApp">Book an eye exam on WhatsApp</h2>
      <p class="sub" data-en="Your request opens WhatsApp already written. Nothing is sent until you press send. We confirm your slot by message. Reference: MIT-XXXX." data-fr="Votre demande ouvre WhatsApp déjà rédigée. Rien n'est envoyé sans vous. Nous confirmons le créneau par message. Référence : MIT-XXXX.">Your request opens WhatsApp already written. Nothing is sent until you press send. We confirm your slot by message. Reference: MIT-XXXX.</p>
      <div class="info-blocks">
        <div class="ib"><span class="ic">📍</span><div><h3 data-en="Where" data-fr="Lieu">Where</h3><p data-en="Malingo, opposite the former police station, Molyko, Buea." data-fr="Malingo, face à l'ancien commissariat, Molyko, Buéa.">Malingo, opposite the former police station, Molyko, Buea.</p></div></div>
        <div class="ib"><span class="ic">💬</span><div><h3 data-en="Call or WhatsApp" data-fr="Appel ou WhatsApp">Call or WhatsApp</h3><p><a href="tel:+237677789631">+237 677 789 631</a> <span data-en="(demo routing to AMK)" data-fr="(acheminement démo vers AMK)">(demo routing to AMK)</span></p></div></div>
        <div class="ib"><span class="ic">👓</span><div><h3 data-en="Bring along" data-fr="À apporter">Bring along</h3><p data-en="Your current glasses or previous prescription, if you have either." data-fr="Vos lunettes actuelles ou votre ancienne prescription, si vous les avez.">Your current glasses or previous prescription, if you have either.</p></div></div>
      </div>
    </div>
    <form class="form-card rv" style="transition-delay:.1s" onsubmit="return book(event)">
      <h3 data-en="Request an eye exam" data-fr="Demander un examen de vue">Request an eye exam</h3>
      <p class="fc-sub" data-en="30 seconds. We confirm your day by WhatsApp." data-fr="30 secondes. Nous confirmons le jour sur WhatsApp.">30 seconds. We confirm your day by WhatsApp.</p>
      <div class="fgrid2">
        <div class="fld"><label for="b-fn" data-en="Your name *" data-fr="Votre nom *">Your name *</label><input id="b-fn" type="text" required></div>
        <div class="fld"><label for="b-ph" data-en="WhatsApp number *" data-fr="Numéro WhatsApp *">WhatsApp number *</label><input id="b-ph" type="tel" required></div>
      </div>
      <div class="fld"><label for="b-sv" data-en="What do you need? *" data-fr="Que vous faut-il ? *">What do you need? *</label>
        <select id="b-sv" required>
          <option data-en="Eye test &amp; prescription" data-fr="Examen de vue et prescription">Eye test &amp; prescription</option>
          <option data-en="Complete glasses (frames + lenses)" data-fr="Lunettes complètes (monture + verres)">Complete glasses (frames + lenses)</option>
          <option data-en="New lenses for my own frame" data-fr="Verres neufs pour ma monture">New lenses for my own frame</option>
          <option data-en="Fitting or adjustment" data-fr="Ajustage">Fitting or adjustment</option>
          <option data-en="Not sure yet" data-fr="Je ne sais pas encore">Not sure yet</option>
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
      <button class="btn btn-blue" type="submit" data-en="Book an eye exam →" data-fr="Réserver un examen de vue →">Book an eye exam →</button>
      <p class="form-small" data-en="Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the shop's own number and logs the booking." data-fr="Ouvre WhatsApp avec votre message rédigé. Acheminement démo vers AMK ; sur le site final, cela arrive au numéro du magasin et enregistre la réservation.">Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the shop's own number and logs the booking.</p>
    </form>
  </div>
</section>

<!-- FAQ -->
<section class="faq" id="faq">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Quick answers" data-fr="Réponses rapides">Quick answers</span>
      <h2 data-en="Good to know before you come" data-fr="À savoir avant de venir">Good to know before you come</h2>
    </div>
    <div class="faq-list rv">
      <details><summary data-en="Do I need an appointment?" data-fr="Faut-il un rendez-vous ?">Do I need an appointment?</summary><div class="ans" data-en="Walk-ins are welcome, but a WhatsApp message books a confirmed slot so you are not kept waiting." data-fr="Les visites sans rendez-vous sont acceptées, mais un message WhatsApp garantit un créneau confirmé et peu d'attente.">Walk-ins are welcome, but a WhatsApp message books a confirmed slot so you are not kept waiting.</div></details>
      <details><summary data-en="What happens during an eye exam?" data-fr="Que se passe-t-il pendant l'examen de vue ?">What happens during an eye exam?</summary><div class="ans" data-en="We test distance and near vision in each eye, compare lenses until the choice is clear, and write your prescription. Bring your current glasses if you wear any." data-fr="Nous testons la vision de loin et de près de chaque œil, comparons les verres jusqu'au choix clair, puis écrivons votre prescription. Apportez vos lunettes actuelles.">We test distance and near vision in each eye, compare lenses until the choice is clear, and write your prescription. Bring your current glasses if you wear any.</div></details>
      <details><summary data-en="Can I bring my own frame?" data-fr="Puis-je apporter ma propre monture ?">Can I bring my own frame?</summary><div class="ans" data-en="Yes. If the frame is in good condition, new prescription lenses can be mounted into it." data-fr="Oui. Si la monture est en bon état, de nouveaux verres de prescription peuvent y être montés.">Yes. If the frame is in good condition, new prescription lenses can be mounted into it.</div></details>
      <details><summary data-en="I already have a prescription. Do I need another test?" data-fr="J'ai déjà une prescription. Faut-il un autre examen ?">I already have a prescription. Do I need another test?</summary><div class="ans" data-en="Bring it. If it is recent and still comfortable, we work from it; if your sight has changed, a short refraction updates it." data-fr="Apportez-la. Si elle est récente et confortable, nous travaillons avec ; si votre vue a changé, un court examen la met à jour.">Bring it. If it is recent and still comfortable, we work from it; if your sight has changed, a short refraction updates it.</div></details>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="wrap">
    <div class="amk-bar">
      <span class="t"><b data-en="This website is a concept by AMK" data-fr="Ce site est un concept d'AMK">This website is a concept by AMK</b> · Web Development &amp; Digital Solutions<small data-en="Bilingual (EN|FR), mobile-fast optic-center template with WhatsApp booking and an online frame gallery. Add your real photos, prices and Google listing, and it is yours in 3 to 5 days." data-fr="Modèle de centre optique bilingue (EN|FR), rapide sur mobile, avec réservation WhatsApp et galerie de montures en ligne. Ajoutez vos photos, prix et fiche Google, et il est à vous en 3 à 5 jours.">Bilingual (EN|FR), mobile-fast optic-center template with WhatsApp booking and an online frame gallery. Add your real photos, prices and Google listing, and it is yours in 3 to 5 days.</small></span>
      <a class="btn btn-cream" style="padding:12px 22px;font-size:14px" href="index.html" data-en="Back to AMK website" data-fr="Retour au site d'AMK">Back to AMK website</a>
    </div>
    <div class="f-grid">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
          <span class="mark" style="width:38px;height:38px;border-radius:11px"><svg viewBox="0 0 24 24" fill="none" stroke="#F7F5EE" stroke-width="1.8" stroke-linecap="round"><circle cx="8.5" cy="14" r="4"/><circle cx="15.5" cy="14" r="4"/><path d="M12.5 14h-1M4.5 12.5 2.5 11.5M19.5 12.5l2-1"/></svg></span>
          <b style="color:#fff;font-size:15.5px">Midas Touch Optic Center</b>
        </div>
        <p data-en="Malingo, opposite the former police station, Molyko, Buea, Cameroon" data-fr="Malingo, face à l'ancien commissariat, Molyko, Buéa, Cameroun">Malingo, opposite the former police station, Molyko, Buea, Cameroon</p>
        <p style="margin-top:6px"><a href="tel:+237677789631">+237 677 789 631</a> <span style="color:#7C91A5" data-en="(demo routing to AMK)" data-fr="(acheminement démo vers AMK)">(demo routing to AMK)</span></p>
        <p style="margin-top:10px;font-size:12.5px;color:#7C91A5" data-en="Concept preview. Replace the demo number, live map and opening hours with the shop's own before launch." data-fr="Aperçu conceptuel. Remplacer le numéro démo, la carte et les heures d'ouverture par ceux du magasin avant lancement.">Concept preview. Replace the demo number, live map and opening hours with the shop's own before launch.</p>
      </div>
      <div>
        <h5 data-en="Quick links" data-fr="Liens rapides">Quick links</h5>
        <a href="#services" data-en="Services" data-fr="Services">Services</a>
        <a href="#frames" data-en="Frames" data-fr="Montures">Frames</a>
        <a href="#book" data-en="Book an eye exam" data-fr="Réserver un examen de vue">Book an eye exam</a>
        <a href="#faq" data-en="Questions" data-fr="Questions">Questions</a>
      </div>
      <div>
        <h5 data-en="Good to know" data-fr="Bon à savoir">Good to know</h5>
        <p style="font-size:13px" data-en="Refraction, prescribing and lens mounting as stated on the shop's own Facebook page. Single fast file that opens on any phone. Prices and photos are clearly marked as samples until the real ones are added." data-fr="Réfraction, prescription et montage de verres selon la page Facebook du magasin. Un seul fichier rapide qui s'ouvre sur tout téléphone. Prix et photos clairement marqués comme exemples en attendant les vrais.">Refraction, prescribing and lens mounting as stated on the shop's own Facebook page. Single fast file that opens on any phone. Prices and photos are clearly marked as samples until the real ones are added.</p>
      </div>
    </div>
    <div class="f-bottom">
      <span data-en="© 2026 Midas Touch Optic Center (concept preview)" data-fr="© 2026 Midas Touch Optic Center (aperçu conceptuel)">© 2026 Midas Touch Optic Center (concept preview)</span>
      <span>Concept by AMK · Web Development &amp; Digital Solutions</span>
    </div>
  </div>
</footer>

<div class="mbar">
  <a class="btn btn-outline" href="tel:+237677789631" data-en="📞 Call" data-fr="📞 Appeler">📞 Call</a>
  <a class="btn btn-blue" href="#book" data-en="Book an eye exam →" data-fr="Réserver un examen de vue →">Book an eye exam →</a>
</div>

<script>
var WA_NUM = "237677789631"; // AMK demo routing; replace with MITOC's 678 90 89 62 at launch
function setLang(l){
  document.documentElement.lang = l;
  document.querySelectorAll("[data-en]").forEach(function(el){ el.innerHTML = (l === "fr") ? el.getAttribute("data-fr") : el.getAttribute("data-en"); });
  document.getElementById("btn-en").classList.toggle("on", l === "en");
  document.getElementById("btn-fr").classList.toggle("on", l === "fr");
  try{ history.replaceState(null, "", l === "fr" ? "?lang=fr" : "mitoc.html"); }catch(e){}
}
function toggleDrawer(open){
  var d = document.getElementById("drawer"), b = document.getElementById("burger");
  d.classList.toggle("open", open);
  b.classList.toggle("open", open);
  d.setAttribute("aria-hidden", String(!open));
  b.setAttribute("aria-expanded", String(open));
  document.body.style.overflow = open ? "hidden" : "";
}
var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target); } }); }, {threshold:.12});
document.querySelectorAll(".rv").forEach(function(el){ io.observe(el); });
function book(e){
  e.preventDefault();
  var fr = document.documentElement.lang === "fr";
  var name = document.getElementById("b-fn").value.trim();
  var phone = document.getElementById("b-ph").value.trim();
  var sv = document.getElementById("b-sv").selectedOptions[0].text;
  var day = document.getElementById("b-day").selectedOptions[0].text;
  var tm = document.getElementById("b-time").selectedOptions[0].text;
  var q = document.getElementById("b-q").value.trim();
  var ref = "MIT-" + Math.floor(1000 + Math.random()*9000);
  var msg = fr
    ? "Bonjour Midas Touch Optic Center ! Je souhaite réserver un examen de vue.\n\nNom : " + name + "\nTéléphone : " + phone + "\nBesoin : " + sv + "\nJour : " + day + "\nHeure : " + tm + (q ? "\nNote : " + q : "") + "\nRéférence : " + ref
    : "Hello Midas Touch Optic Center! I would like to book an eye exam.\n\nName: " + name + "\nPhone: " + phone + "\nNeed: " + sv + "\nDay: " + day + "\nTime: " + tm + (q ? "\nNote: " + q : "") + "\nReference: " + ref;
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
        .replace('src="F1"', 'src="%s"' % IMG["f1"])
        .replace('src="F2"', 'src="%s"' % IMG["f2"])
        .replace('src="F3"', 'src="%s"' % IMG["f3"])
        .replace('src="FLAT"', 'src="%s"' % IMG["flatlay"])
        .replace('src="FIT"', 'src="%s"' % IMG["fit"])
        .replace("url(BG_EXAM)", "url('%s')" % IMG["exam"])
        .replace("url(BG_CRAFT)", "url('%s')" % IMG["craft"])
        .replace("url(BG_WALL)", "url('%s')" % IMG["wall"]))

out = HERE / "mitoc.html"
out.write_text(HTML, encoding="utf-8")
print("wrote", out, round(len(HTML)/1024), "KB")
