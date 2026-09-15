# -*- coding: utf-8 -*-
"""Build site/sample-secondary.html — NAMELESS Cameroon secondary-school
concept ("Crestwood College"), replacing the old US-style Crestwood template.

Design Read: Cameroonian private secondary college (Forms 1 to Upper Sixth,
day + boarding) landing for fee-paying parents choosing a school, trustworthy
institutional language with warmth, token sheet D (deep navy + cream + gold
honors accent), rounded-14, glass nav, WA-first admissions, FCFA fees, GCE
O/A Level framing, EN|FR. Dials 6/4/4.
Audit fix vs the old file: no US content (Model UN, Canvas, state fairs),
no dead portal buttons, local GCE/boarding/admissions reality, mobile drawer.
Single file, base64 images, demo routing to AMK 237677789631, ref SCH-XXXX.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent

def b64img(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / "img" / name).read_bytes()).decode()

IMG = {k: b64img("sec-%s.jpg" % k) for k in
       ("hero", "class", "lab", "dorm", "sports", "awards", "campus", "lib")}

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cameroon Secondary School Website Concept · Crestwood College (Template) | AMK</title>
<meta name="description" content="A bilingual private secondary school concept by AMK for Cameroon colleges: GCE Ordinary and Advanced Level programmes, boarding, transparent FCFA fees, admissions by WhatsApp in English and French.">
<link rel="canonical" href="https://amk-cm.vercel.app/sample-secondary.html">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='2' y='2' width='28' height='28' rx='7' fill='%230F2A47'/%3E%3Cpath d='M16 7l9 5-9 5-9-5 9-5zM9 15.5v4c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-4l-7 3.9-7-3.9z' fill='%23B08A3E'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "School",
  "name": "Crestwood College (concept)",
  "url": "https://www.your-college.cm",
  "telephone": "+237 677 789 631",
  "address": { "@type": "PostalAddress", "addressLocality": "Your Town", "addressCountry": "CM" }
}
</script>
<style>
:root{
  --ease-out:cubic-bezier(.23,1,.32,1);
  --ease-in-out:cubic-bezier(.77,0,.175,1);
  --ease-drawer:cubic-bezier(.32,.72,0,1);
  --dur-press:140ms;--dur-pop:170ms;--dur-menu:220ms;--dur-panel:320ms;--dur-reveal:520ms;
  --ink:#1A2033; --ink-soft:#51606F; --surface:#FAFAF7; --surface-2:#FFFFFF; --line:#E6E6E0;
  --navy:#0F2A47; --navy-b:#0A1E34; --brand:#0F2A47; --brand-bright:#0A1E34;
  --brand-tint:#E7EEF5; --on-brand:#FFFFFF;
  --gold:#B08A3E; --gold-tint:#F3EAD7;
  --radius:14px; --radius-lg:18px;
  --shadow:0 16px 36px rgba(15,32,55,.12);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
section[id]{scroll-margin-top:84px}
body{font-family:'Outfit',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:var(--surface);line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{line-height:1.12;letter-spacing:-.02em;font-weight:800}
a{color:inherit}
img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
section{padding:84px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--navy);margin-bottom:14px}
.eyebrow::before{content:"";width:22px;height:2px;background:var(--gold);border-radius:2px}
h2{font-size:clamp(27px,3.4vw,38px);margin-bottom:12px;text-wrap:balance}
.sub{font-size:16.5px;color:var(--ink-soft);max-width:620px}
.center{text-align:center}.center .eyebrow{justify-content:center}.center .sub{margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 26px;border-radius:11px;font-size:15.5px;font-weight:700;text-decoration:none;border:2px solid transparent;cursor:pointer;font-family:inherit;transition:transform var(--dur-press) var(--ease-out),background .2s var(--ease-out),box-shadow .2s var(--ease-out),border-color .2s var(--ease-out);text-align:center;white-space:nowrap}
.btn:active{transform:scale(.97)}
.btn-navy{background:var(--navy);color:#fff;box-shadow:0 10px 24px rgba(15,42,71,.24)}
.btn-navy:hover{background:var(--navy-b)}
.btn-gold{background:var(--gold);color:#fff;box-shadow:0 10px 24px rgba(176,138,62,.28)}
.btn-gold:hover{background:#9A7631}
.btn-cream{background:var(--surface);color:var(--navy)}
.btn-ghost-light{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
.btn-ghost-light:hover{border-color:#fff;background:rgba(255,255,255,.08)}
.btn-outline{background:transparent;color:var(--navy);border-color:rgba(15,42,71,.35)}
.btn-outline:hover{border-color:var(--navy);background:var(--brand-tint)}
.demobar{background:var(--gold);color:#2E2408;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;text-align:center;padding:7px 0}
header{position:sticky;top:0;z-index:60;background:rgba(250,250,247,.88);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:14px;height:70px}
.logo{display:flex;align-items:center;gap:11px;text-decoration:none}
.mark{width:42px;height:42px;border-radius:11px;background:var(--navy);display:flex;align-items:center;justify-content:center;flex:none}
.mark svg{width:23px;height:23px}
.logo .t{font-size:16px;font-weight:800;line-height:1.05;color:var(--navy)}
.logo .t small{display:block;font-size:9px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}
.nav-links{display:flex;gap:24px}
.nav-links a{text-decoration:none;font-size:14.5px;font-weight:600;color:var(--ink-soft);transition:color .2s var(--ease-out)}
.nav-right{display:flex;align-items:center;gap:10px}
.lang{display:flex;border:1.5px solid var(--line);border-radius:999px;overflow:hidden}
.lang button{border:none;background:transparent;font-family:inherit;font-size:12.5px;font-weight:700;padding:6px 12px;cursor:pointer;color:var(--ink-soft);transition:background .2s var(--ease-out)}
.lang button:active{transform:scale(.97)}
.lang button.on{background:var(--navy);color:#fff}
.concept-chip{font-size:11px;font-weight:700;color:var(--ink-soft);border:1px solid var(--line);border-radius:99px;padding:5px 11px;text-decoration:none;white-space:nowrap}
.concept-chip b{color:var(--navy)}
.burger{display:none;width:42px;height:42px;border:1.5px solid var(--line);background:var(--surface-2);border-radius:11px;cursor:pointer;position:relative;flex:none;transition:transform var(--dur-press) var(--ease-out)}
.burger:active{transform:scale(.97)}
.burger span{display:block;position:absolute;left:11px;right:11px;height:2px;background:var(--ink);border-radius:2px;transition:transform var(--dur-menu) var(--ease-out),opacity var(--dur-menu) var(--ease-out)}
.burger span:nth-child(1){top:14px}.burger span:nth-child(2){top:20px}.burger span:nth-child(3){top:26px}
.burger.open span:nth-child(1){top:20px;transform:rotate(45deg)}
.burger.open span:nth-child(2){opacity:0}
.burger.open span:nth-child(3){top:20px;transform:rotate(-45deg)}
.drawer{position:fixed;inset:0;z-index:80;background:var(--surface);transform:translateX(100%);visibility:hidden;transition:transform var(--dur-panel) var(--ease-drawer),visibility 0s linear var(--dur-panel);display:flex;flex-direction:column}
.drawer.open{transform:none;visibility:visible;transition:transform var(--dur-panel) var(--ease-drawer)}
.drawer-top{height:70px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--line)}
.drawer nav{display:flex;flex-direction:column;padding:26px 28px;gap:6px;flex:1}
.drawer nav a{font-size:22px;font-weight:700;text-decoration:none;padding:12px 0;border-bottom:1px solid var(--line);opacity:0;transform:translateX(18px);transition:opacity var(--dur-panel) var(--ease-out),transform var(--dur-panel) var(--ease-out)}
.drawer.open nav a{opacity:1;transform:none;transition-delay:calc(var(--i)*60ms + 100ms)}
.drawer .d-foot{padding:20px 28px 30px;display:flex;flex-direction:column;gap:12px}
.drawer .d-foot .btn{width:100%}
/* hero */
.hero{background:linear-gradient(180deg,var(--surface) 0%,#EFEEDF 100%);padding:64px 0 76px;overflow:hidden}
.hero-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:54px;align-items:center}
.hero h1{font-size:clamp(36px,4.6vw,54px);margin-bottom:18px}
.hero h1 em{font-style:normal;color:var(--navy)}
.hero .sub{font-size:17.5px;margin-bottom:30px;max-width:530px}
.hero-ctas{display:flex;gap:13px;flex-wrap:wrap}
.hero-media{position:relative}
.hero-media img{width:100%;aspect-ratio:4/4.6;object-fit:cover;object-position:center 26%;border-radius:var(--radius-lg);box-shadow:0 34px 70px rgba(10,30,52,.28)}
.hero-badge{position:absolute;top:16px;left:16px;background:rgba(255,255,255,.93);color:var(--navy);border-radius:999px;padding:8px 15px;font-size:12.5px;font-weight:700;backdrop-filter:blur(6px)}
.hero-float{position:absolute;right:-14px;bottom:28px;background:var(--surface-2);border:1px solid var(--line);border-radius:13px;padding:14px 18px;box-shadow:0 18px 40px rgba(10,30,52,.18);display:flex;align-items:center;gap:12px;max-width:258px}
.hero-float .ic{width:40px;height:40px;border-radius:11px;background:var(--gold-tint);display:flex;align-items:center;justify-content:center;flex:none;font-size:18px}
.hero-float b{display:block;font-size:14px}
.hero-float span{font-size:12px;color:var(--ink-soft)}
/* stats */
.stats{background:var(--navy);color:#fff;padding:34px 0}
.stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center}
.stat-num{font-size:clamp(26px,3.1vw,37px);font-weight:800;font-variant-numeric:tabular-nums}
.stat-num .u{color:var(--gold);font-size:.72em}
.stat .lbl{font-size:12.5px;color:#C3CEDB;margin-top:2px}
.stat .demo{display:block;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:#8294A8;margin-top:5px}
/* programmes bento */
.bento{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:46px}
.cell{background:var(--surface-2);border:1px solid var(--line);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column;transition:transform var(--dur-pop) var(--ease-out),box-shadow var(--dur-pop) var(--ease-out)}
.cell.photo{padding:0;overflow:hidden}
.cell.photo .ph{width:100%;background-size:cover;background-position:center}
.cell.photo.wide{grid-column:span 2}
.cell.photo.wide .ph{height:290px}
.cell.photo.narrow .ph{height:190px}
.cell.photo .pin{padding:22px 26px 24px}
.cell .ico{width:46px;height:46px;border-radius:11px;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:20px}
.cell h3{font-size:17px;margin-bottom:6px}
.cell p{font-size:14px;color:var(--ink-soft)}
.cell .more{margin-top:auto;padding-top:14px;font-size:13.5px;font-weight:700;color:var(--navy);text-decoration:none;align-self:flex-start}
.bg-class{background-image:url(BG_CLASS)}
.bg-lab{background-image:url(BG_LAB)}
/* boarding split */
.boarding{background:#EFEEDF}
.bd-grid{display:grid;grid-template-columns:1.02fr .98fr;gap:54px;align-items:center}
.bd-media img{width:100%;border-radius:var(--radius-lg);aspect-ratio:4/3;object-fit:cover;box-shadow:0 26px 60px rgba(10,30,52,.22)}
.bd-list{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px}
.bd-item{background:var(--surface-2);border:1px solid var(--line);border-radius:13px;padding:18px}
.bd-item .ic{font-size:19px}
.bd-item b{display:block;font-size:14.5px;margin:6px 0 3px}
.bd-item span{font-size:13px;color:var(--ink-soft)}
/* life gallery */
.life-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:46px}
.life{border-radius:var(--radius);overflow:hidden;background:var(--surface-2);border:1px solid var(--line)}
.life .ph{height:230px;background-size:cover;background-position:center}
.life figcaption{padding:16px 18px;font-size:13.5px;font-weight:600}
.bg-sports{background-image:url(BG_SPORTS)}
.bg-awards{background-image:url(BG_AWARDS)}
.bg-lib{background-image:url(BG_LIB)}
/* student corner */
.res-links{list-style:none;margin-top:12px;display:flex;flex-direction:column;gap:8px}
.res-links a{font-size:13.5px;font-weight:700;color:var(--navy);text-decoration:none}
.res-links a:hover{text-decoration:underline}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chips span{font-size:12px;font-weight:700;background:var(--brand-tint);color:var(--navy);border-radius:999px;padding:6px 12px}
.cell .small{font-size:12px;color:var(--ink-soft);margin-top:12px}
.flyer-strip{margin-top:24px;background:var(--gold-tint);border:1px solid #E3D3AA;border-radius:var(--radius);padding:24px 28px;text-align:center}
.flyer-strip b{display:block;font-size:17px;color:var(--navy);margin-bottom:6px}
.flyer-strip span{font-size:13.5px;color:#5B4A1F}
/* fees */
.fees{background:var(--surface-2);border-block:1px solid var(--line)}
.fee-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:44px}
.fcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-lg);padding:28px 24px;display:flex;flex-direction:column;position:relative}
.fcard.hot{border:2px solid var(--navy);box-shadow:0 20px 44px rgba(15,42,71,.14)}
.fflag{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--navy);color:#fff;font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:999px;white-space:nowrap}
.fico{width:48px;height:48px;border-radius:12px;background:var(--gold-tint);display:flex;align-items:center;justify-content:center;font-size:21px;margin-bottom:14px}
.fcard h3{font-size:16.5px;min-height:44px;display:flex;align-items:center}
.price{font-size:29px;font-weight:800;color:var(--navy);font-variant-numeric:tabular-nums;margin:8px 0 2px}
.price small{font-size:12.5px;font-weight:600;color:var(--ink-soft)}
.pmeta{font-size:11.5px;color:var(--ink-soft);letter-spacing:.04em;margin-bottom:14px}
.fcard ul{list-style:none;margin-bottom:18px}
.fcard li{font-size:13.5px;padding:5px 0 5px 26px;position:relative;color:#34404F}
.fcard li::before{content:"✓";position:absolute;left:2px;color:var(--gold);font-weight:800}
.fcard .btn{width:100%;padding:12px 16px;font-size:14px}
.demo-note{text-align:center;font-size:12.5px;color:var(--ink-soft);margin-top:22px}
/* admissions band */
.adband{position:relative;color:#fff;overflow:hidden}
.adband-bg{position:absolute;inset:0;background-size:cover;background-position:center 60%;background-image:url(BG_CAMPUS)}
.adband-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,rgba(8,22,40,.95) 0%,rgba(8,22,40,.8) 44%,rgba(8,22,40,.4) 80%)}
.adband .wrap{position:relative;padding:108px 24px}
.adband .eyebrow{color:var(--gold)}
.adband h2{color:#fff;max-width:580px}
.adband p{color:#CDD8E5;max-width:540px;font-size:16.5px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:34px;max-width:820px}
.step{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:13px;padding:20px;backdrop-filter:blur(4px)}
.step .n{width:34px;height:34px;border-radius:10px;background:var(--gold);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:12px;font-size:15px}
.step b{display:block;font-size:15px;margin-bottom:4px}
.step span{font-size:13px;color:#C3CEDB}
.adband .fctas{display:flex;gap:13px;flex-wrap:wrap;margin-top:30px}
/* apply form */
.visit-grid{display:grid;grid-template-columns:1fr 470px;gap:54px;align-items:start}
.info-blocks{display:flex;flex-direction:column;gap:14px;margin-top:24px}
.ib{background:var(--surface-2);border:1px solid var(--line);border-radius:13px;padding:18px 20px;display:flex;gap:14px;align-items:flex-start}
.ib .ic{font-size:20px;width:42px;height:42px;border-radius:11px;background:var(--brand-tint);display:flex;align-items:center;justify-content:center;flex:none}
.ib h3{font-size:15.5px;margin-bottom:3px}
.ib p{font-size:14px;color:var(--ink-soft)}
.ib a{font-weight:700;color:var(--navy);text-decoration:none}
.form-card{background:var(--surface-2);border:1px solid var(--line);border-radius:var(--radius-lg);padding:32px 28px;box-shadow:var(--shadow);position:sticky;top:92px}
.form-card h3{font-size:21px;margin-bottom:4px}
.fc-sub{font-size:13.5px;color:var(--ink-soft);margin-bottom:18px}
.fld{margin-bottom:12px}
.fld label{display:block;font-size:12.5px;font-weight:700;color:var(--navy);margin-bottom:5px}
.fld input,.fld select{width:100%;padding:13px 14px;border:1.5px solid var(--line);border-radius:10px;font-size:15px;font-family:inherit;background:var(--surface);color:var(--ink);transition:border-color .2s var(--ease-out),box-shadow .2s var(--ease-out),background .2s var(--ease-out)}
.fld input:focus,.fld select:focus{outline:none;border-color:var(--navy);box-shadow:0 0 0 4px rgba(15,42,71,.12);background:#fff}
.fgrid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.form-card .btn{width:100%;margin-top:4px}
.form-small{font-size:11.5px;color:var(--ink-soft);text-align:center;margin-top:12px;line-height:1.5}
/* faq */
.faq{background:#EFEEDF}
.faq-list{max-width:760px;margin:40px auto 0}
.faq-list details{border-bottom:1px solid var(--line);padding:6px 0}
.faq-list summary{cursor:pointer;list-style:none;font-size:16.5px;font-weight:700;padding:14px 30px 14px 0;position:relative;color:var(--navy);transition:transform var(--dur-press) var(--ease-out)}
.faq-list summary:active{transform:scale(.99)}
.faq-list summary::-webkit-details-marker{display:none}
.faq-list summary::after{content:"+";position:absolute;right:4px;top:11px;font-size:24px;font-weight:400;color:var(--gold);transition:transform var(--dur-menu) var(--ease-out)}
.faq-list details[open] summary::after{transform:rotate(45deg)}
.faq-list .ans{font-size:14.5px;color:var(--ink-soft);padding:0 0 18px;max-width:660px}
/* footer */
footer{background:var(--navy-b);color:#A9BACC;padding:48px 0 24px;font-size:14px}
.amk-bar{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.amk-bar b{color:#fff}
.amk-bar small{display:block;color:#93A6B9;font-size:12.5px;margin-top:3px;max-width:760px}
.f-grid{display:grid;grid-template-columns:1.3fr 1fr 1.2fr;gap:34px;margin-bottom:26px}
.f-grid h5{color:#fff;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
.f-grid a{display:block;text-decoration:none;padding:3px 0}
.f-bottom{border-top:1px solid rgba(255,255,255,.1);padding-top:18px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:12.5px}
/* proof strip (conversion standard addendum #3) */
.proof{background:var(--surface-2);border-bottom:1px solid var(--line)}
.proof-grid{display:grid;grid-template-columns:290px 1fr;gap:34px;align-items:center;padding:42px 0}
.proof-rate{text-align:center;border-right:1px solid var(--line);padding-right:34px}
.proof-rate .stars{color:var(--gold);font-size:21px;letter-spacing:2px}
.proof-rate .big{font-size:46px;font-weight:800;color:var(--navy);line-height:1.05;margin:2px 0}
.proof-rate .who{font-size:12.5px;color:var(--ink-soft)}
.proof-rate a{display:inline-block;margin-top:8px;font-size:13px;font-weight:700;color:var(--navy);text-decoration:none}
.proof-rate .gce{display:inline-block;margin-top:6px;font-size:12px;color:var(--ink-soft)}
.proof-q{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.proof-q blockquote{background:var(--gold-tint);border:1px solid var(--line);border-radius:14px;padding:16px 17px;font-size:13.5px;color:var(--ink)}
.proof-q b{display:block;margin-top:9px;font-size:12.5px;color:var(--navy)}
.follow{display:flex;flex-wrap:wrap;gap:11px;align-items:center;justify-content:center;margin-top:26px}
.follow .lbl{font-size:13.5px;font-weight:700;color:var(--ink-soft)}
.follow a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 18px;border-radius:999px;border:1.5px solid rgba(15,42,71,.28);text-decoration:none;font-size:13.5px;font-weight:700;color:var(--navy);background:var(--surface-2)}
.follow a:hover{border-color:var(--navy);background:var(--brand-tint)}
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:70;background:#fff;border-top:1px solid var(--line);padding:10px 12px;gap:9px;box-shadow:0 -8px 24px rgba(15,32,55,.1)}
.mbar a{flex:1;min-height:52px;display:flex;align-items:center;justify-content:center}
.mbar a:first-child{flex:0 0 92px}
@media(max-width:860px){.proof-grid{grid-template-columns:1fr;gap:22px;padding:32px 0}.proof-rate{border-right:none;border-bottom:1px solid var(--line);padding:0 0 22px}.proof-q{grid-template-columns:1fr}}
.cell .more{transition:transform var(--dur-press) var(--ease-out)}
.cell .more:active,.concept-chip:active,.logo:active{transform:scale(.97)}
.concept-chip,.logo{transition:transform var(--dur-press) var(--ease-out)}
.drawer nav a:active{transform:scale(.99)}
.rv{opacity:0;transform:translateY(22px);transition:opacity var(--dur-reveal) var(--ease-out),transform var(--dur-reveal) var(--ease-out)}
.rv.in{opacity:1;transform:none}
@media (hover:hover) and (pointer:fine){
  .btn-navy:hover,.btn-gold:hover,.btn-cream:hover{transform:translateY(-2px)}
  .cell:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
  .life{transition:transform var(--dur-pop) var(--ease-out),box-shadow var(--dur-pop) var(--ease-out)}
  .life:hover{transform:translateY(-5px);box-shadow:var(--shadow)}
  .nav-links a:hover{color:var(--navy)}
  .cell .more:hover{text-decoration:underline}
}
@media(max-width:960px){
  .hero-grid,.bd-grid,.visit-grid{grid-template-columns:1fr;gap:40px}
  .bento{grid-template-columns:1fr 1fr}
  .cell.photo.wide{grid-column:span 2}
  .fee-grid{grid-template-columns:1fr 1fr}
  .life-grid{grid-template-columns:1fr}
  .life .ph{height:260px}
  .stats .wrap{grid-template-columns:1fr 1fr;gap:26px}
  .steps{grid-template-columns:1fr;max-width:440px}
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
  .fee-grid{grid-template-columns:1fr}
  .bd-list{grid-template-columns:1fr}
  .stats .wrap{grid-template-columns:1fr 1fr;gap:20px}
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
  .hero-float{left:10px;right:auto;max-width:232px;bottom:18px;padding:12px 14px}
  .hero-badge{font-size:11.5px;padding:7px 12px}
  .adband .wrap{padding:80px 16px}
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

<div class="demobar" data-en="Demo concept: fictional secondary college, sample fees and photos" data-fr="Démo : collège secondaire fictif, frais et photos d'exemple">Demo concept: fictional secondary college, sample fees and photos</div>

<header>
  <div class="wrap nav">
    <a class="logo" href="#top">
      <span class="mark"><svg viewBox="0 0 24 24" fill="none"><path d="M12 4.5 20 9l-8 4.5L4 9l8-4.5zM6.5 11.6v3.2c0 1.2 2.5 2.2 5.5 2.2s5.5-1 5.5-2.2v-3.2L12 15l-5.5-3.4z" fill="#B08A3E"/></svg></span>
      <span class="t">Crestwood College<small data-en="Secondary · Day &amp; Boarding" data-fr="Secondaire · Externat &amp; Internat">Secondary · Day &amp; Boarding</small></span>
    </a>
    <nav class="nav-links">
      <a href="#programmes" data-en="Programmes" data-fr="Programmes">Programmes</a>
      <a href="#boarding" data-en="Boarding" data-fr="Internat">Boarding</a>
      <a href="#corner" data-en="Students" data-fr="Élèves">Students</a>
      <a href="#fees" data-en="Fees" data-fr="Frais">Fees</a>
      <a href="#admissions" data-en="Admissions" data-fr="Admissions">Admissions</a>
      <a href="#faq" data-en="Questions" data-fr="Questions">Questions</a>
    </nav>
    <div class="nav-right">
      <span class="lang"><button type="button" id="btn-en" class="on" onclick="setLang('en')">EN</button><button type="button" id="btn-fr" onclick="setLang('fr')">FR</button></span>
      <a class="concept-chip" href="index.html" data-en="Website concept by <b>AMK</b>" data-fr="Site concept par <b>AMK</b>">Website concept by <b>AMK</b></a>
      <a class="btn btn-navy" style="padding:10px 18px;font-size:13.5px" href="#apply" data-en="Apply" data-fr="Inscription">Apply</a>
      <button type="button" class="burger" id="burger" aria-label="Open menu" aria-expanded="false" onclick="toggleDrawer(true)"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-top">
    <span style="font-size:15px;font-weight:800;color:var(--navy)">Crestwood College</span>
    <button type="button" class="burger open" aria-label="Close menu" onclick="toggleDrawer(false)"><span></span><span></span><span></span></button>
  </div>
  <nav>
    <a href="#programmes" style="--i:0" onclick="toggleDrawer(false)" data-en="Programmes" data-fr="Programmes">Programmes</a>
    <a href="#boarding" style="--i:1" onclick="toggleDrawer(false)" data-en="Boarding" data-fr="Internat">Boarding</a>
    <a href="#corner" style="--i:2" onclick="toggleDrawer(false)" data-en="Students" data-fr="Élèves">Students</a>
    <a href="#fees" style="--i:3" onclick="toggleDrawer(false)" data-en="Fees" data-fr="Frais">Fees</a>
    <a href="#admissions" style="--i:4" onclick="toggleDrawer(false)" data-en="Admissions" data-fr="Admissions">Admissions</a>
    <a href="#faq" style="--i:5" onclick="toggleDrawer(false)" data-en="Questions" data-fr="Questions">Questions</a>
  </nav>
  <div class="d-foot">
    <a class="btn btn-navy" href="#apply" onclick="toggleDrawer(false)" data-en="Start admission" data-fr="Commencer l'inscription">Start admission</a>
    <a class="btn btn-outline" href="https://wa.me/237677789631" target="_blank" rel="noopener" data-en="WhatsApp the office" data-fr="WhatsApp du bureau">WhatsApp the office</a>
  </div>
</div>

<!-- HERO -->
<div class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Private bilingual secondary college · Cameroon" data-fr="Collège secondaire bilingue privé · Cameroun">Private bilingual secondary college · Cameroon</span>
      <h1 data-en="Character and results, <em>from Form One</em>" data-fr="Caractère et résultats, <em>dès la 6e</em>">Character and results, <em>from Form One</em></h1>
      <p class="sub" data-en="GCE Ordinary and Advanced Level programmes, day and boarding, with admissions, fees and results a parent can check on the phone, in English and French." data-fr="Programmes GCE Ordinary et Advanced Level, externat et internat, avec inscriptions, frais et résultats consultables sur téléphone, en anglais et en français.">GCE Ordinary and Advanced Level programmes, day and boarding, with admissions, fees and results a parent can check on the phone, in English and French.</p>
      <div class="hero-ctas">
        <a class="btn btn-navy" href="#apply" data-en="Start admission" data-fr="Commencer l'inscription">Start admission</a>
        <a class="btn btn-outline" href="#fees" data-en="See fees (sample)" data-fr="Voir les frais (exemple)">See fees (sample)</a>
      </div>
    </div>
    <div class="hero-media rv" style="transition-delay:.12s">
      <img src="HERO" alt="Students in uniform on the college campus" loading="eager">
      <span class="hero-badge" data-en="🎓 Forms 1 to Upper Sixth" data-fr="🎓 De la 6e à la Terminale">🎓 Forms 1 to Upper Sixth</span>
      <div class="hero-float">
        <span class="ic">💬</span>
        <div><b data-en="Admissions on WhatsApp" data-fr="Inscriptions sur WhatsApp">Admissions on WhatsApp</b><span data-en="Ask about a place in one message" data-fr="Renseignez-vous en un message">Ask about a place in one message</span></div>
      </div>
    </div>
  </div>
</div>

<!-- STATS -->
<div class="stats">
  <div class="wrap">
    <div class="stat"><div class="stat-num">2</div><div class="lbl" data-en="Languages of study and service" data-fr="Langues d'études et de service">Languages of study and service</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num" data-count="7">0</div><div class="lbl" data-en="Years: Form 1 to Upper Sixth" data-fr="Années : de la 6e à la Terminale">Years: Form 1 to Upper Sixth</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num">GCE<span class="u"> O/A</span></div><div class="lbl" data-en="Ordinary &amp; Advanced Level" data-fr="Ordinary &amp; Advanced Level">Ordinary &amp; Advanced Level</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
    <div class="stat"><div class="stat-num">24<span class="u">/7</span></div><div class="lbl" data-en="Boarding supervision day and night" data-fr="Encadrement internat jour et nuit">Boarding supervision day and night</div><span class="demo" data-en="demo values" data-fr="valeurs de démo">demo values</span></div>
  </div>
</div>

<!-- PROOF (addendum #3: third-party-linked; replace demo values at launch or remove) -->
<section class="proof">
  <div class="wrap proof-grid">
    <div class="proof-rate rv">
      <div class="stars">★★★★★</div>
      <div class="big">4.9</div>
      <div class="who" data-en="Google rating · 58 parent reviews (demo)" data-fr="Note Google · 58 avis de parents (démo)">Google rating · 58 parent reviews (demo)</div>
      <!-- LAUNCH: replace href with the college's real Google Business Profile reviews URL -->
      <a href="#" data-en="Read parent reviews on Google →" data-fr="Lire les avis des parents sur Google →">Read parent reviews on Google →</a>
      <span class="gce"><br><a href="https://www.camgceb.org" target="_blank" rel="noopener" style="font-size:12.5px;font-weight:600" data-en="Official GCE results: camgceb.org" data-fr="Résultats GCE officiels : camgceb.org">Official GCE results: camgceb.org</a></span>
    </div>
    <div class="proof-q">
      <blockquote class="rv" style="transition-delay:.05s" data-en="“I am in Douala for work and I get the boarding update on WhatsApp every week. I know what my child is eating and scoring.”<b>— Boarding parent (demo)</b>" data-fr="« Je suis à Douala pour le travail et je reçois le bulletin de l'internat sur WhatsApp chaque semaine. Je sais ce que mon enfant mange et ses notes. »<b>— Parent d'interne (démo)</b>">“I am in Douala for work and I get the boarding update on WhatsApp every week. I know what my child is eating and scoring.”<b>— Boarding parent (demo)</b></blockquote>
      <blockquote class="rv" style="transition-delay:.1s" data-en="“The fees were exactly what the website said. No hidden levy at the bursary.”<b>— Day parent (demo)</b>" data-fr="« Les frais étaient exactement ceux du site. Aucune cotisation cachée à la comptabilité. »<b>— Parent d'externe (démo)</b>">“The fees were exactly what the website said. No hidden levy at the bursary.”<b>— Day parent (demo)</b></blockquote>
      <blockquote class="rv" style="transition-delay:.15s" data-en="“My sister did the whole admission from abroad by WhatsApp before flying into Douala. That is why we chose them.”<b>— Parent abroad (demo)</b>" data-fr="« Ma sœur a fait toute l'inscription depuis l'étranger par WhatsApp avant de voler vers Douala. C'est pour ça que nous les avons choisis. »<b>— Parent à l'étranger (démo)</b>">“My sister did the whole admission from abroad by WhatsApp before flying into Douala. That is why we chose them.”<b>— Parent abroad (demo)</b></blockquote>
    </div>
  </div>
</section>

<!-- PROGRAMMES -->
<section id="programmes">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Our programmes" data-fr="Nos programmes">Our programmes</span>
      <h2 data-en="One campus, the full secondary journey" data-fr="Un même campus, tout le parcours secondaire">One campus, the full secondary journey</h2>
      <p class="sub" data-en="From the first day of Form One to the GCE papers, every stage is taught on one campus by the same team." data-fr="Du premier jour de 6e aux épreuves du GCE, chaque étape est enseignée sur un même campus par la même équipe.">From the first day of Form One to the GCE papers, every stage is taught on one campus by the same team.</p>
    </div>
    <div class="bento">
      <div class="cell photo wide rv">
        <div class="ph bg-class" role="img" aria-label="Students in a classroom lesson"></div>
        <div class="pin">
          <h3 data-en="Forms 1 to 5 · GCE Ordinary Level" data-fr="Formes 1 à 5 · GCE Ordinary Level">Forms 1 to 5 · GCE Ordinary Level</h3>
          <p data-en="A broad first cycle in English, French, mathematics, sciences and the humanities, leading to the Ordinary Level papers." data-fr="Un premier cycle complet en anglais, français, mathématiques, sciences et lettres, menant aux épreuves de l'Ordinary Level.">A broad first cycle in English, French, mathematics, sciences and the humanities, leading to the Ordinary Level papers.</p>
        </div>
      </div>
      <div class="cell rv" style="transition-delay:.06s">
        <div class="ico">🔬</div>
        <h3 data-en="Science practicals" data-fr="Travaux pratiques scientifiques">Science practicals</h3>
        <p data-en="Physics, chemistry and biology are taught as hands-on practicals, the way the GCE exams test them." data-fr="La physique, la chimie et la biologie s'enseignent en travaux pratiques, tels que les examens GCE les évaluent.">Physics, chemistry and biology are taught as hands-on practicals, the way the GCE exams test them.</p>
      </div>
      <div class="cell rv">
        <div class="ico">📖</div>
        <h3 data-en="Lower &amp; Upper Sixth · A Level" data-fr="Lower &amp; Upper Sixth · A Level">Lower &amp; Upper Sixth · A Level</h3>        <p data-en="Arts and science combinations chosen with a university target, with guided applications and transcripts." data-fr="Des combinaisons littéraires et scientifiques choisies selon l'objectif universitaire, avec dossiers et relevés guidés.">Arts and science combinations chosen with a university target, with guided applications and transcripts.</p>
      </div>
      <div class="cell photo narrow rv" style="transition-delay:.06s">
        <div class="ph bg-lab" role="img" aria-label="Students in the science laboratory"></div>
        <div class="pin">
          <h3 data-en="Bilingual section" data-fr="Section bilingue">Bilingual section</h3>
          <p data-en="English-medium and French-medium streams, so every graduate works comfortably in both official languages." data-fr="Des filières anglophone et francophone, pour que chaque élève travaille à l'aise dans les deux langues officielles.">English-medium and French-medium streams, so every graduate works comfortably in both official languages.</p>
        </div>
      </div>
      <div class="cell rv" style="transition-delay:.12s">
        <div class="ico">🧭</div>
        <h3 data-en="Guidance &amp; discipline" data-fr="Orientation &amp; discipline">Guidance &amp; discipline</h3>
        <p data-en="A named form teacher per class, weekly reports to parents, and career guidance before university choices." data-fr="Un professeur titulaire par classe, des bilans hebdomadaires aux parents et une orientation avant les choix universitaires.">A named form teacher per class, weekly reports to parents, and career guidance before university choices.</p>
        <a class="more" href="#apply" data-en="Ask about a place →" data-fr="Demander une place →">Ask about a place →</a>
      </div>
    </div>
  </div>
</section>

<!-- BOARDING -->
<section class="boarding" id="boarding">
  <div class="wrap bd-grid">
    <div class="bd-media rv"><img src="DORM" alt="A tidy boarding dormitory"></div>
    <div class="rv" style="transition-delay:.1s">
      <span class="eyebrow" data-en="Boarding" data-fr="Internat">Boarding</span>
      <h2 data-en="A safe place for a child whose parents are far away" data-fr="Un lieu sûr pour l'enfant dont les parents sont loin">A safe place for a child whose parents are far away</h2>
      <p class="sub" data-en="Parents out of town see the dormitory, the daily routine and the fee sheet before deciding, not after paying." data-fr="Les parents éloignés voient le dortoir, la routine quotidienne et les frais avant de décider, pas après avoir payé.">Parents out of town see the dormitory, the daily routine and the fee sheet before deciding, not after paying.</p>
      <div class="bd-list">
        <div class="bd-item"><span class="ic">🛏️</span><b data-en="Supervised dormitories" data-fr="Dortoirs encadrés">Supervised dormitories</b><span data-en="Boys' and girls' blocks with resident staff." data-fr="Blocs garçons et filles avec personnel résident.">Boys' and girls' blocks with resident staff.</span></div>
        <div class="bd-item"><span class="ic">🍲</span><b data-en="Three meals a day" data-fr="Trois repas par jour">Three meals a day</b><span data-en="Kitchen and menu shown on the visiting day." data-fr="Cuisine et menu présentés au jour de visite.">Kitchen and menu shown on the visiting day.</span></div>
        <div class="bd-item"><span class="ic">📚</span><b data-en="Evening prep" data-fr="Études du soir">Evening prep</b><span data-en="Supervised study hours every weekday evening." data-fr="Heures d'étude surveillées chaque soir de semaine.">Supervised study hours every weekday evening.</span></div>
        <div class="bd-item"><span class="ic">🩺</span><b data-en="Health &amp; safety" data-fr="Santé &amp; sécurité">Health &amp; safety</b><span data-en="First aid on site, night security, parent updates." data-fr="Premiers soins sur place, sécurité de nuit, nouvelles aux parents.">First aid on site, night security, parent updates.</span></div>
      </div>
    </div>
  </div>
</section>

<!-- LIFE -->
<section>
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="College life" data-fr="Vie au collège">College life</span>
      <h2 data-en="Lessons, laboratories and the sports field" data-fr="Cours, laboratoires et terrain de sport">Lessons, laboratories and the sports field</h2>
    </div>
    <div class="life-grid">
      <figure class="life rv"><div class="ph bg-lib" role="img" aria-label="Students reading in the library"></div><figcaption data-en="Quiet study hours in the college library" data-fr="Heures d'étude silencieuses à la bibliothèque">Quiet study hours in the college library</figcaption></figure>
      <figure class="life rv" style="transition-delay:.06s"><div class="ph bg-sports" role="img" aria-label="Students racing on sports day"></div><figcaption data-en="Inter-house sports on the college field" data-fr="Compétitions sportives inter-maisons sur le terrain">Inter-house sports on the college field</figcaption></figure>
      <figure class="life rv" style="transition-delay:.12s"><div class="ph bg-awards" role="img" aria-label="A student receiving a prize"></div><figcaption data-en="Prize-giving after the GCE results" data-fr="Remise des prix après les résultats du GCE">Prize-giving after the GCE results</figcaption></figure>
    </div>
  </div>
</section>

<!-- STUDENT CORNER -->
<section id="corner">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Student &amp; parent corner" data-fr="Espace élèves &amp; parents">Student &amp; parent corner</span>
      <h2 data-en="A reason to open the site every week — not just once" data-fr="Une raison d'ouvrir le site chaque semaine — pas une seule fois">A reason to open the site every week — not just once</h2>
      <p class="sub" data-en="Results day, downloads, a curated research corner and college news: pupils and parents come back to the site, share it, and give the college something real to print on its flyers." data-fr="Jour des résultats, téléchargements, coin recherche et nouvelles du collège : élèves et parents reviennent sur le site, le partagent, et donnent au collège de quoi imprimer sur ses flyers.">Results day, downloads, a curated research corner and college news: pupils and parents come back to the site, share it, and give the college something real to print on its flyers.</p>
    </div>
    <div class="bento">
      <div class="cell photo wide rv">
        <div class="ph bg-awards" role="img" aria-label="Prize-giving ceremony"></div>
        <div class="pin">
          <h3 data-en="🏆 GCE results &amp; honour roll, published results day" data-fr="🏆 Résultats GCE &amp; palmarès, publiés le jour des résultats">🏆 GCE results &amp; honour roll, published results day</h3>
          <p data-en="Pass rates, prize winners and university destinations go online the day the GCE Board publishes — the page proud parents and old students share at home and abroad. (Example figures only.)" data-fr="Taux de réussite, lauréats et admissions universitaires en ligne le jour de publication du GCE Board — la page que parents et anciens partagent au pays et à l'étranger. (Chiffres d'exemple uniquement.)">Pass rates, prize winners and university destinations go online the day the GCE Board publishes — the page proud parents and old students share at home and abroad. (Example figures only.)</p>
          <a class="more" href="https://camgceb.org" target="_blank" rel="noopener" data-en="Official GCE Board results ↗" data-fr="Résultats officiels du GCE Board ↗">Official GCE Board results ↗</a>
        </div>
      </div>
      <div class="cell rv" style="transition-delay:.06s">
        <div class="ico">📂</div>
        <h3 data-en="Downloads, term by term" data-fr="Téléchargements, trimestre par trimestre">Downloads, term by term</h3>
        <p data-en="Prospectus, school calendar, fee sheet, past-question packs and admission forms, uploaded by the office instead of reprinted every January." data-fr="Prospectus, calendrier scolaire, grille des frais, sujets anciens et dossiers d'inscription, mis en ligne par le bureau au lieu d'être réimprimés chaque janvier.">Prospectus, school calendar, fee sheet, past-question packs and admission forms, uploaded by the office instead of reprinted every January.</p>
        <div class="chips">
          <span data-en="Prospectus (PDF)" data-fr="Prospectus (PDF)">Prospectus (PDF)</span>
          <span data-en="Calendar" data-fr="Calendrier">Calendar</span>
          <span data-en="Fee sheet" data-fr="Grille des frais">Fee sheet</span>
          <span data-en="Past questions" data-fr="Anciens sujets">Past questions</span>
        </div>
        <p class="small" data-en="Slots shown; the college publishes its own files at launch." data-fr="Emplacements affichés ; le collège publie ses propres fichiers au lancement.">Slots shown; the college publishes its own files at launch.</p>
      </div>
      <div class="cell photo narrow rv" style="transition-delay:.06s">
        <div class="ph bg-lib" role="img" aria-label="College library study corner"></div>
        <div class="pin">
          <h3 data-en="📚 Research corner" data-fr="📚 Coin recherche">📚 Research corner</h3>
          <ul class="res-links">
            <li><a href="https://camgceb.org" target="_blank" rel="noopener" data-en="GCE Board · syllabuses &amp; results" data-fr="GCE Board · programmes &amp; résultats">GCE Board · syllabuses &amp; results</a></li>
            <li><a href="https://minesec.gov.cm" target="_blank" rel="noopener" data-en="MINESEC · official news" data-fr="MINESEC · informations officielles">MINESEC · official news</a></li>
            <li><a href="https://www.khanacademy.org" target="_blank" rel="noopener" data-en="Khan Academy · free revision" data-fr="Khan Academy · révision gratuite">Khan Academy · free revision</a></li>
          </ul>
        </div>
      </div>
      <div class="cell photo wide rv" style="grid-column:span 2;transition-delay:.12s">
        <div class="pin" style="padding:26px">
          <h3 data-en="📰 News worth printing on a flyer" data-fr="📰 Des nouvelles à imprimer sur les flyers">📰 News worth printing on a flyer</h3>
          <p data-en="Inter-house sports, science week, debate club wins, visiting-day photos and announcements — posted by the office, shared by parents on WhatsApp, and turned into next term's admissions poster. While the Ministry digitises school cards and fee payments, the college visibly moves with the times instead of watching neighbours catch up." data-fr="Compétitions inter-maisons, semaine des sciences, victoires du club de débat, photos du jour de visite et annonces — publiés par le bureau, partagés par les parents sur WhatsApp, et transformés en affiche d'inscription au trimestre suivant. Pendant que le Ministère numérise cartes et paiements scolaires, le collège avance visiblement avec son époque.">Inter-house sports, science week, debate club wins, visiting-day photos and announcements — posted by the office, shared by parents on WhatsApp, and turned into next term's admissions poster. While the Ministry digitises school cards and fee payments, the college visibly moves with the times instead of watching neighbours catch up.</p>
          <a class="more" href="https://wa.me/237677789631" target="_blank" rel="noopener" data-en="Send the office a news item on WhatsApp →" data-fr="Envoyer une nouvelle au bureau sur WhatsApp →">Send the office a news item on WhatsApp →</a>
        </div>
      </div>
    </div>
    <div class="flyer-strip rv">
      <b data-en="&ldquo;Our GCE results, calendar and admissions are online — open them on any phone.&rdquo;" data-fr="« Nos résultats GCE, notre calendrier et nos inscriptions sont en ligne — consultez-les sur n'importe quel téléphone. »">“Our GCE results, calendar and admissions are online — open them on any phone.”</b>
      <span data-en="A ready-made line for every admissions flyer, prospectus and banner. (Demo concept.)" data-fr="Une phrase prête pour chaque flyer, prospectus et bannière. (Concept de démonstration.)">A ready-made line for every admissions flyer, prospectus and banner. (Demo concept.)</span>
    </div>
  </div>
</section>

<!-- FEES -->
<section class="fees" id="fees">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Fees (sample)" data-fr="Frais (exemple)">Fees (sample)</span>
      <h2 data-en="The full fee, written down before you ask" data-fr="Le montant complet, écrit avant que vous demandiez">The full fee, written down before you ask</h2>
      <p class="sub" data-en="A clear fee sheet removes the conversation parents dislike most. These are sample figures; the college's real fee structure replaces them at launch." data-fr="Une grille claire élimine la conversation que les parents redoutent. Ce sont des montants d'exemple ; les vrais frais du collège les remplacent au lancement.">A clear fee sheet removes the conversation parents dislike most. These are sample figures; the college's real fee structure replaces them at launch.</p>
    </div>
    <div class="fee-grid">
      <div class="fcard rv">
        <div class="fico">📝</div>
        <h3 data-en="Registration (once)" data-fr="Inscription (une fois)">Registration (once)</h3>
        <div class="price" data-en="10 000 <small>FCFA</small>" data-fr="10 000 <small>FCFA</small>">10 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="NEW PUPIL · (DEMO)" data-fr="NOUVEL ÉLÈVE · (DÉMO)">NEW PUPIL · (DEMO)</div>
        <ul>
          <li data-en="Admission form and file" data-fr="Dossier et formulaire d'admission">Admission form and file</li>
          <li data-en="Placement assessment" data-fr="Test de classement">Placement assessment</li>
        </ul>
        <a class="btn btn-outline" href="#apply" data-en="Start admission" data-fr="Commencer l'inscription">Start admission</a>
      </div>
      <div class="fcard hot rv" style="transition-delay:.06s">
        <div class="fflag" data-en="Most families" data-fr="La plupart des familles">Most families</div>
        <div class="fico">🎒</div>
        <h3 data-en="Day student, per term" data-fr="Externe, par trimestre">Day student, per term</h3>
        <div class="price" data-en="90 000 <small>FCFA</small>" data-fr="90 000 <small>FCFA</small>">90 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="3 TERMS PER YEAR · (DEMO)" data-fr="3 TRIMESTRES PAR AN · (DÉMO)">3 TERMS PER YEAR · (DEMO)</div>
        <ul>
          <li data-en="Tuition and reports" data-fr="Cours et bulletins">Tuition and reports</li>
          <li data-en="Library and practicals" data-fr="Bibliothèque et travaux pratiques">Library and practicals</li>
          <li data-en="End-of-term exams" data-fr="Examens de fin de trimestre">Examens de fin de trimestre</li>
        </ul>
        <a class="btn btn-navy" href="#apply" data-en="Ask about a day place" data-fr="Demander une place externe">Ask about a day place</a>
      </div>
      <div class="fcard rv" style="transition-delay:.12s">
        <div class="fico">🛏️</div>
        <h3 data-en="Boarding, per term" data-fr="Interne, par trimestre">Boarding, per term</h3>
        <div class="price" data-en="180 000 <small>FCFA</small>" data-fr="180 000 <small>FCFA</small>">180 000 <small>FCFA</small></div>
        <div class="pmeta" data-en="FEES + BOARD · (DEMO)" data-fr="FRAIS + PENSION · (DÉMO)">FEES + BOARD · (DEMO)</div>
        <ul>
          <li data-en="Everything in the day package" data-fr="Tout le forfait externe">Everything in the day package</li>
          <li data-en="Dormitory and three meals" data-fr="Dortoir et trois repas">Dormitory and three meals</li>
          <li data-en="Supervised evening prep" data-fr="Études du soir surveillées">Supervised evening prep</li>
        </ul>
        <a class="btn btn-outline" href="#apply" data-en="Ask about boarding" data-fr="Demander l'internat">Ask about boarding</a>
      </div>
    </div>
    <p class="demo-note" data-en="(Demo) Sample fees for this concept. Your real amounts, uniform costs and payment schedule replace these before launch. Cash, Mobile Money and bank transfer are all supported." data-fr="(Démo) Frais d'exemple. Vos montants réels, coût des uniformes et calendrier de paiement les remplacent avant le lancement. Espèces, Mobile Money et virement bancaire pris en charge.">(Demo) Sample fees for this concept. Your real amounts, uniform costs and payment schedule replace these before launch. Cash, Mobile Money and bank transfer are all supported.</p>
  </div>
</section>

<!-- ADMISSIONS BAND -->
<section class="adband" id="admissions" style="padding:0">
  <div class="adband-bg"></div>
  <div class="wrap">
    <div class="rv">
      <span class="eyebrow" data-en="Admissions" data-fr="Admissions">Admissions</span>
      <h2 data-en="Three steps to a place" data-fr="Trois étapes pour une place">Three steps to a place</h2>
      <div class="steps">
        <div class="step"><span class="n">1</span><b data-en="Message the office" data-fr="Écrivez au bureau">Message the office</b><span data-en="Send the child's name and the class sought on WhatsApp. No agent, no long forms first." data-fr="Envoyez le nom de l'enfant et la classe souhaitée sur WhatsApp. Sans agent ni longs formulaires.">Send the child's name and the class sought on WhatsApp. No agent, no long forms first.</span></div>
        <div class="step"><span class="n">2</span><b data-en="Visit and assessment" data-fr="Visite et test">Visit and assessment</b><span data-en="Tour the campus and dormitory; the child sits a short placement assessment." data-fr="Visitez le campus et le dortoir ; l'enfant passe un petit test de classement.">Tour the campus and dormitory; the child sits a short placement assessment.</span></div>
        <div class="step"><span class="n">3</span><b data-en="Offer and enrolment" data-fr="Offre et inscription">Offer and enrolment</b><span data-en="Receive the offer letter and fee sheet by WhatsApp, then pay the deposit to confirm the place." data-fr="Recevez l'offre et la grille des frais sur WhatsApp, puis versez l'acompte pour confirmer.">Receive the offer letter and fee sheet by WhatsApp, then pay the deposit to confirm the place.</span></div>
      </div>
      <div class="fctas">
        <a class="btn btn-gold" href="#apply" data-en="Start admission" data-fr="Commencer l'inscription">Start admission</a>
        <a class="btn btn-ghost-light" href="https://wa.me/237677789631" target="_blank" rel="noopener" data-en="Ask a question on WhatsApp" data-fr="Poser une question sur WhatsApp">Ask a question on WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<!-- APPLY -->
<section id="visit">
  <div class="wrap visit-grid">
    <div class="rv">
      <span class="eyebrow" data-en="Visit or apply" data-fr="Visite ou inscription">Visit or apply</span>
      <h2 id="apply" data-en="Request admission on WhatsApp" data-fr="Demander une inscription sur WhatsApp">Request admission on WhatsApp</h2>
      <p class="sub" data-en="Fill this in and the message opens already written for the college office. Nothing is sent until you press send. Reference: SCH-XXXX." data-fr="Remplissez ceci et le message s'ouvre déjà rédigé pour le bureau du collège. Rien n'est envoyé sans vous. Référence : SCH-XXXX.">Fill this in and the message opens already written for the college office. Nothing is sent until you press send. Reference: SCH-XXXX.</p>
      <div class="info-blocks">
        <div class="ib"><span class="ic">📍</span><div><h3 data-en="Find the college" data-fr="Trouver le collège">Find the college</h3><p data-en="Your quarter and nearest landmark, your town, Cameroon (concept address)." data-fr="Votre quartier et point de repère le plus proche, votre ville, Cameroun (adresse de démo).">Your quarter and nearest landmark, your town, Cameroon (concept address).</p></div></div>
        <div class="ib"><span class="ic">🕒</span><div><h3 data-en="Office hours" data-fr="Heures du bureau">Office hours</h3><p data-en="Monday to Friday, 7:30 to 16:30; visiting Saturdays by appointment." data-fr="Lundi au vendredi, 7 h 30 à 16 h 30 ; samedis de visite sur rendez-vous.">Monday to Friday, 7:30 to 16:30; visiting Saturdays by appointment.</p></div></div>
        <div class="ib"><span class="ic">💬</span><div><h3 data-en="Call or WhatsApp" data-fr="Appel ou WhatsApp">Call or WhatsApp</h3><p><a href="tel:+237677789631">+237 677 789 631</a> <span data-en="(demo routing to AMK)" data-fr="(acheminement démo vers AMK)">(demo routing to AMK)</span></p></div></div>
      </div>
    </div>
    <form class="form-card rv" style="transition-delay:.1s" onsubmit="return apply(event)">
      <h3 data-en="Admission request" data-fr="Demande d'inscription">Admission request</h3>
      <p class="fc-sub" data-en="30 seconds. The office replies on WhatsApp." data-fr="30 secondes. Le bureau répond sur WhatsApp.">30 seconds. The office replies on WhatsApp.</p>
      <div class="fgrid2">
        <div class="fld"><label for="b-parent" data-en="Parent name *" data-fr="Nom du parent *">Parent name *</label><input id="b-parent" type="text" required></div>
        <div class="fld"><label for="b-phone" data-en="WhatsApp number *" data-fr="Numéro WhatsApp *">WhatsApp number *</label><input id="b-phone" type="tel" required></div>
      </div>
      <div class="fld"><label for="b-child" data-en="Child's full name *" data-fr="Nom complet de l'enfant *">Child's full name *</label><input id="b-child" type="text" required></div>
      <div class="fgrid2">
        <div class="fld"><label for="b-class" data-en="Class sought *" data-fr="Classe souhaitée *">Class sought *</label>
          <select id="b-class" required>
            <option data-en="Form 1" data-fr="Forme 1 / 6e">Form 1</option>
            <option data-en="Form 2 to 4" data-fr="Forme 2 à 4">Form 2 to 4</option>
            <option data-en="Form 5 (GCE OL)" data-fr="Forme 5 (GCE OL)">Form 5 (GCE OL)</option>
            <option data-en="Lower Sixth" data-fr="Lower Sixth">Lower Sixth</option>
            <option data-en="Upper Sixth (GCE AL)" data-fr="Upper Sixth (GCE AL)">Upper Sixth (GCE AL)</option>
          </select>
        </div>
        <div class="fld"><label for="b-board" data-en="Day or boarding *" data-fr="Externe ou interne *">Day or boarding *</label>
          <select id="b-board" required>
            <option data-en="Day student" data-fr="Externe">Day student</option>
            <option data-en="Boarding" data-fr="Interne">Boarding</option>
            <option data-en="Not sure" data-fr="Indécis">Not sure</option>
          </select>
        </div>
      </div>
      <div class="fld"><label for="b-q" data-en="Note (optional)" data-fr="Note (facultatif)">Note (optional)</label><input id="b-q" type="text"></div>
      <button class="btn btn-navy" type="submit" data-en="Send my admission request →" data-fr="Envoyer ma demande d'inscription →">Send my admission request →</button>
      <p class="form-small" data-en="Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the college office and logs the request." data-fr="Ouvre WhatsApp avec votre message rédigé. Acheminement démo vers AMK ; sur le site final, cela arrive au bureau du collège et enregistre la demande.">Opens WhatsApp with your message written. Demo routing to AMK; on your live site this reaches the college office and logs the request.</p>
    </form>
  </div>
</section>

<!-- FAQ -->
<section class="faq" id="faq">
  <div class="wrap">
    <div class="center rv">
      <span class="eyebrow" data-en="Quick answers" data-fr="Réponses rapides">Quick answers</span>
      <h2 data-en="What parents ask first" data-fr="Ce que les parents demandent d'abord">What parents ask first</h2>
    </div>
    <div class="faq-list rv">
      <details><summary data-en="When do admissions open?" data-fr="Quand les inscriptions ouvrent-elles ?">When do admissions open?</summary><div class="ans" data-en="Admissions run through the long vacation for the new school year, with a few late places in the first week of the first term. Send a WhatsApp message to reserve a placement assessment." data-fr="Les inscriptions se font pendant les grandes vacances pour la nouvelle année, avec quelques places tardives la première semaine du premier trimestre. Envoyez un WhatsApp pour réserver un test de classement.">Admissions run through the long vacation for the new school year, with a few late places in the first week of the first term. Send a WhatsApp message to reserve a placement assessment.</div></details>
      <details><summary data-en="Which exams do students sit?" data-fr="Quels examens les élèves présentent-ils ?">Which exams do students sit?</summary><div class="ans" data-en="Students prepare for the GCE Ordinary Level at the end of Form 5 and the GCE Advanced Level at the end of Upper Sixth, set by the Cameroon GCE Board." data-fr="Les élèves préparent le GCE Ordinary Level à la fin de la Forme 5 et le GCE Advanced Level à la fin de l'Upper Sixth, organisés par le Cameroon GCE Board.">Students prepare for the GCE Ordinary Level at the end of Form 5 and the GCE Advanced Level at the end of Upper Sixth, set by the Cameroon GCE Board.</div></details>
      <details><summary data-en="Can a French-speaking pupil enrol?" data-fr="Un élève francophone peut-il s'inscrire ?">Can a French-speaking pupil enrol?</summary><div class="ans" data-en="Yes. The bilingual section supports French-medium pupils joining the English stream, with extra language support in the first year." data-fr="Oui. La section bilingue accompagne les élèves francophones rejoignant le filière anglophone, avec un soutien linguistique renforcé la première année.">Yes. The bilingual section supports French-medium pupils joining the English stream, with extra language support in the first year.</div></details>
      <details><summary data-en="How do boarding parents follow progress?" data-fr="Comment les parents d'internes suivent-ils les progrès ?">How do boarding parents follow progress?</summary><div class="ans" data-en="Weekly reports and visiting-day news arrive by WhatsApp, and the office answers out-of-town parents directly instead of relying on the child to relay messages." data-fr="Les bilans hebdomadaires et les nouvelles du jour de visite arrivent sur WhatsApp, et le bureau répond directement aux parents éloignés au lieu de faire passer les messages par l'enfant.">Weekly reports and visiting-day news arrive by WhatsApp, and the office answers out-of-town parents directly instead of relying on the child to relay messages.</div></details>
      <details><summary data-en="How are fees paid?" data-fr="Comment les frais sont-ils payés ?">How are fees paid?</summary><div class="ans" data-en="Per term, before the term begins, by cash at the bursary, bank transfer or Mobile Money, with a receipt issued for every payment. The figures on this concept page are samples." data-fr="Par trimestre, avant la rentrée, en espèces à la comptabilité, par virement ou Mobile Money, avec un reçu pour chaque paiement. Les montants de cette page concept sont des exemples.">Per term, before the term begins, by cash at the bursary, bank transfer or Mobile Money, with a receipt issued for every payment. The figures on this concept page are samples.</div></details>
    </div>
  </div>
</section>

<!-- ALTERNATIVE CTA (addendum #3: low-commitment path; replace # with real pages at launch or remove) -->
<section style="padding:54px 0 60px">
  <div class="wrap center rv">
    <h2 style="font-size:clamp(22px,2.6vw,28px)" data-en="Still deciding? Follow admissions here" data-fr="Pas encore décidé ? Suivez les inscriptions ici">Still deciding? Follow admissions here</h2>
    <p class="sub" style="margin:8px auto 0" data-en="Open-day clips, boarding life and admission deadlines as they happen, in English and French." data-fr="Vidéos des journées portes ouvertes, vie à l'internat et dates limites d'inscription en direct, en anglais et en français.">Open-day clips, boarding life and admission deadlines as they happen, in English and French.</p>
    <div class="follow">
      <span class="lbl" data-en="Follow:" data-fr="Suivez :">Follow:</span>
      <!-- LAUNCH: replace each href with the college's real social page; delete any they do not have -->
      <a href="#">🎵 TikTok</a>
      <a href="#">📘 Facebook</a>
      <a href="#">📸 Instagram</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="wrap">
    <div class="amk-bar">
      <span><b data-en="This website is a concept by AMK" data-fr="Ce site est un concept d'AMK">This website is a concept by AMK</b> · Web Development &amp; Digital Solutions<small data-en="Bilingual (EN|FR), mobile-fast college template with GCE programmes, transparent FCFA fees, boarding and WhatsApp admissions. Replace the name, crest, photos, fees and results with your college's own, and it is yours in 3 to 5 days." data-fr="Modèle de collège bilingue (EN|FR), rapide sur mobile, avec programmes GCE, frais FCFA transparents, internat et inscriptions WhatsApp. Remplacez nom, écusson, photos, frais et résultats par ceux de votre collège, et il est à vous en 3 à 5 jours.">Bilingual (EN|FR), mobile-fast college template with GCE programmes, transparent FCFA fees, boarding and WhatsApp admissions. Replace the name, crest, photos, fees and results with your college's own, and it is yours in 3 to 5 days.</small></span>
      <a class="btn btn-cream" style="padding:12px 22px;font-size:14px" href="index.html" data-en="Back to AMK website" data-fr="Retour au site d'AMK">Back to AMK website</a>
    </div>
    <div class="f-grid">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
          <span class="mark" style="width:38px;height:38px;border-radius:10px"><svg viewBox="0 0 24 24" fill="none"><path d="M12 4.5 20 9l-8 4.5L4 9l8-4.5zM6.5 11.6v3.2c0 1.2 2.5 2.2 5.5 2.2s5.5-1 5.5-2.2v-3.2L12 15l-5.5-3.4z" fill="#B08A3E"/></svg></span>
          <b style="color:#fff;font-size:15.5px">Crestwood College</b>
        </div>
        <p data-en="Your quarter, your town, Cameroon (demo address)" data-fr="Votre quartier, votre ville, Cameroun (adresse de démo)">Your quarter, your town, Cameroon (demo address)</p>
        <p style="margin-top:6px"><a href="tel:+237677789631">+237 677 789 631</a> <span style="color:#7E92A7" data-en="(demo routing to AMK)" data-fr="(acheminement démo vers AMK)">(demo routing to AMK)</span></p>
        <p style="margin-top:10px;font-size:12.5px;color:#7E92A7" data-en="Concept college. Replace the map, results lists and office hours with the college's own before launch." data-fr="Collège de démo. Remplacer la carte, les listes de résultats et les heures du bureau par celles du collège avant lancement.">Concept college. Replace the map, results lists and office hours with the college's own before launch.</p>
      </div>
      <div>
        <h5 data-en="Quick links" data-fr="Liens rapides">Quick links</h5>
        <a href="#programmes" data-en="Programmes" data-fr="Programmes">Programmes</a>
        <a href="#boarding" data-en="Boarding" data-fr="Internat">Boarding</a>
        <a href="#fees" data-en="Fees" data-fr="Frais">Fees</a>
        <a href="#apply" data-en="Admissions" data-fr="Inscriptions">Admissions</a>
      </div>
      <div>
        <h5 data-en="Built for Cameroon" data-fr="Conçu pour le Cameroun">Built for Cameroon</h5>
        <p style="font-size:13px" data-en="GCE Ordinary and Advanced Level framing, day and boarding packages, FCFA fee sheets, English and French throughout, and WhatsApp admissions that work on any phone connection." data-fr="Cadrage GCE Ordinary et Advanced Level, forfaits externat et internat, grilles de frais en FCFA, anglais et français partout, et inscriptions WhatsApp qui fonctionnent sur toute connexion téléphonique.">GCE Ordinary and Advanced Level framing, day and boarding packages, FCFA fee sheets, English and French throughout, and WhatsApp admissions that work on any phone connection.</p>
      </div>
    </div>
    <div class="f-bottom">
      <span data-en="© 2026 Crestwood College (concept)" data-fr="© 2026 Crestwood College (concept)">© 2026 Crestwood College (concept)</span>
      <span>Concept by AMK · Web Development &amp; Digital Solutions</span>
    </div>
  </div>
</footer>

<div class="mbar">
  <a class="btn btn-outline" href="tel:+237677789631" data-en="📞 Call" data-fr="📞 Appeler">📞 Call</a>
  <a class="btn btn-navy" href="#apply" data-en="Start admission →" data-fr="Commencer l'inscription →">Start admission →</a>
</div>

<script>
var WA_NUM = "237677789631"; // AMK demo routing; replace with the college's number at launch
function setLang(l){
  document.documentElement.lang = l;
  document.querySelectorAll("[data-en]").forEach(function(el){ el.innerHTML = (l === "fr") ? el.getAttribute("data-fr") : el.getAttribute("data-en"); });
  document.getElementById("btn-en").classList.toggle("on", l === "en");
  document.getElementById("btn-fr").classList.toggle("on", l === "fr");
  try{ history.replaceState(null, "", l === "fr" ? "?lang=fr" : "sample-secondary.html"); }catch(e){}
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
var counted = false;
var cio = new IntersectionObserver(function(es){ es.forEach(function(en){
  if(en.isIntersecting && !counted){
    counted = true;
    document.querySelectorAll(".stat-num[data-count]").forEach(function(el){
      var target = parseInt(el.getAttribute("data-count"), 10), start = null, dur = 1200;
      function tick(now){ if(!start) start = now; var p = Math.min((now-start)/dur,1), e = 1 - Math.pow(1-p,3); el.innerHTML = Math.round(target*e); if(p<1) requestAnimationFrame(tick); }
      requestAnimationFrame(tick);
    });
    cio.disconnect();
  }
}); }, {threshold:.4});
var statsEl = document.querySelector(".stats"); if(statsEl) cio.observe(statsEl);
function apply(e){
  e.preventDefault();
  var fr = document.documentElement.lang === "fr";
  var parent = document.getElementById("b-parent").value.trim();
  var phone = document.getElementById("b-phone").value.trim();
  var child = document.getElementById("b-child").value.trim();
  var cls = document.getElementById("b-class").selectedOptions[0].text;
  var board = document.getElementById("b-board").selectedOptions[0].text;
  var q = document.getElementById("b-q").value.trim();
  var ref = "SCH-" + Math.floor(1000 + Math.random()*9000);
  var msg = fr
    ? "Bonjour au bureau du collège ! Je souhaite une inscription.\n\nParent : " + parent + "\nTéléphone : " + phone + "\nÉlève : " + child + "\nClasse : " + cls + "\nRégime : " + board + (q ? "\nNote : " + q : "") + "\nRéférence : " + ref
    : "Hello college office! I would like to request admission.\n\nParent: " + parent + "\nPhone: " + phone + "\nChild: " + child + "\nClass: " + cls + "\nDay/boarding: " + board + (q ? "\nNote: " + q : "") + "\nReference: " + ref;
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
        .replace('src="DORM"', 'src="%s"' % IMG["dorm"])
        .replace("url(BG_CLASS)", "url('%s')" % IMG["class"])
        .replace("url(BG_LAB)", "url('%s')" % IMG["lab"])
        .replace("url(BG_SPORTS)", "url('%s')" % IMG["sports"])
        .replace("url(BG_AWARDS)", "url('%s')" % IMG["awards"])
        .replace("url(BG_LIB)", "url('%s')" % IMG["lib"])
        .replace("url(BG_CAMPUS)", "url('%s')" % IMG["campus"]))

out = HERE / "sample-secondary.html"
out.write_text(HTML, encoding="utf-8")
print("wrote", out, round(len(HTML)/1024), "KB")
