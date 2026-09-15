// Shared capture + AMK mockup composition pipeline (puppeteer-core + sparticuz chromium)
const puppeteer = require("puppeteer-core");
const chromium = require("@sparticuz/chromium");
const fs = require("fs");
const path = require("path");

async function launch() {
  const exe = await chromium.executablePath();
  return puppeteer.launch({
    executablePath: exe,
    args: [...chromium.args, "--no-sandbox", "--disable-dev-shm-usage", "--force-color-profile=srgb"],
    headless: chromium.headless,
    defaultViewport: null,
  });
}

// Build @font-face block for Noto Color Emoji with inlined woff2 (subset css)
function emojiFontCSS() {
  const base = "/tmp/shots/node_modules/@fontsource/noto-color-emoji";
  const css = fs.readFileSync(path.join(base, "index.css"), "utf8");
  return css.replace(/url\((?:\.\.\/)?files\/([^)]+)\)/g, (m, f) => {
    const buf = fs.readFileSync(path.join(base, "files", f));
    return `url(data:font/woff2;base64,${buf.toString("base64")})`;
  }).replace(/format\(['"]?woff['"]?\)/g, 'format("woff2")');
}

async function injectEmoji(page) {
  const css = emojiFontCSS();
  await page.evaluateOnNewDocument((fontCSS) => {
    const st = document.createElement("style");
    st.textContent = fontCSS;
    document.documentElement.appendChild(st);
  }, css);
}

async function captureHero(browser, url, name, outdir) {
  fs.mkdirSync(outdir, { recursive: true });
  // DESKTOP hero (laptop screen crop)
  const d = await browser.newPage();
  await d.setViewport({ width: 1280, height: 860, deviceScaleFactor: 1 });
  await injectEmoji(d);
  await d.goto(url, { waitUntil: "networkidle0", timeout: 60000 }).catch(e => console.log("goto warn:", e.message));
  await new Promise(r => setTimeout(r, 1600));
  // screenshot only through end of hero + trust/stats band, excluding sticky demo strip? keep strip off mockups:
  await d.addStyleTag({ content: ".demobar{display:none!important}" });
  const dShot = await d.screenshot({ clip: { x: 0, y: 0, width: 1280, height: 800 } });
  fs.writeFileSync(path.join(outdir, name + "-desktop.png"), dShot);
  await d.close();

  // MOBILE hero
  const m = await browser.newPage();
  await m.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await injectEmoji(m);
  await m.goto(url, { waitUntil: "networkidle0", timeout: 60000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 1600));
  await m.addStyleTag({ content: ".demobar{display:none!important}" });
  const mShot = await m.screenshot({ clip: { x: 0, y: 0, width: 390, height: 844 } });
  fs.writeFileSync(path.join(outdir, name + "-mobile.png"), mShot);
  await m.close();
  return { desktop: dShot.toString("base64"), mobile: mShot.toString("base64") };
}

// Compose AMK house-style laptop+phone mockup
async function composeMockup(browser, cfg, outPath) {
  const OUTFIT = path.join(__dirname, "node_modules", "@fontsource", "outfit", "files");
  const outfitFace = (w) => `@font-face{font-family:'Outfit';font-style:normal;font-weight:${w};font-display:block;src:url('file://${path.join(OUTFIT, `outfit-latin-${w}-normal.woff2`)}') format('woff2');}`;
  const fontCSS = [400, 500, 600, 700, 800].map(outfitFace).join("\n");
  const desktopURL = "file://" + path.join(path.dirname(outPath), cfg.desktopFile);
  const mobileURL = "file://" + path.join(path.dirname(outPath), cfg.mobileFile);
  const S = (id, x, y, size) =>
    `<svg class="spark" style="left:${x}px;top:${y}px;width:${size}px;height:${size}px" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0l2.4 9.6L24 12l-9.6 2.4L12 24l-2.4-9.6L0 12l9.6-2.4z"/></svg>`;

  const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
${fontCSS}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;font-family:Outfit,Arial,sans-serif;overflow:hidden;
  background:radial-gradient(1100px 700px at 82% 8%, ${cfg.glow}, transparent 62%),radial-gradient(900px 700px at 12% 95%, ${cfg.glow2 || cfg.glow}, transparent 60%),linear-gradient(160deg,${cfg.bg1},${cfg.bg2});position:relative}
.spark{position:absolute;color:${cfg.spark};opacity:.9}
.dot{position:absolute;width:11px;height:11px;border-radius:50%;background:${cfg.accent}}
.eyebrow{position:absolute;top:86px;left:112px;font-size:18px;font-weight:700;letter-spacing:.20em;text-transform:uppercase;color:${cfg.accent};display:flex;align-items:center;gap:14px;white-space:nowrap}
.eyebrow::before{content:"";width:13px;height:13px;border-radius:50%;background:${cfg.accent};flex:none}
h1{position:absolute;top:118px;left:110px;font-size:64px;font-weight:800;letter-spacing:-.02em;color:${cfg.title};line-height:1.05;white-space:nowrap}
.tag{position:absolute;top:208px;left:112px;font-size:27px;color:${cfg.tag};font-weight:500;white-space:nowrap}
.chip{position:absolute;top:250px;left:112px;background:${cfg.chipBg};color:${cfg.chipText};font-size:18px;font-weight:700;padding:15px 28px;border-radius:999px;letter-spacing:.01em;white-space:nowrap;z-index:5;box-shadow:0 14px 30px rgba(10,20,30,.18)}
/* laptop */
.laptop{position:absolute;left:276px;top:256px;width:1144px;z-index:2}
.screen{background:linear-gradient(180deg,#1b242e,#0d1319);border-radius:26px;padding:24px;box-shadow:0 60px 120px ${cfg.shadow}}
.screen img{width:100%;height:700px;display:block;border-radius:8px;object-fit:cover;object-position:top center}
.shelf{width:1194px;height:46px;margin:6px 0 0 -25px;background:linear-gradient(180deg,#222c36,#0b1015);border-radius:8px 8px 26px 26px;position:relative}
.shelf::after{content:"";position:absolute;left:50%;top:0;transform:translateX(-50%);width:170px;height:12px;background:#05080b;border-radius:0 0 16px 16px}
/* phone overlapping laptop right edge */
.phone{position:absolute;left:1406px;top:366px;width:297px;height:589px;background:linear-gradient(180deg,#1b242e,#0d1319);border-radius:42px;padding:13px;z-index:4;box-shadow:0 60px 120px ${cfg.shadow}, 0 0 0 2px rgba(255,255,255,.08) inset}
.phone img{width:100%;height:563px;object-fit:cover;object-position:top center;border-radius:30px;display:block}
.island{position:absolute;top:27px;left:50%;transform:translateX(-50%);width:104px;height:28px;background:#05080b;border-radius:999px;z-index:6}
</style></head><body>
${S("s1",1348,100,52)}
${S("s2",1808,212,42)}
${S("s3",158,724,32)}
${S("s4",1748,842,54)}
<div class="dot" style="left:236px;top:838px;opacity:.55"></div>
<div class="eyebrow">${cfg.eyebrow}</div>
<h1>${cfg.title}</h1>
<div class="tag">${cfg.tagline}</div>
<div class="chip">${cfg.chip}</div>
<div class="laptop"><div class="screen"><img src="${desktopURL}"></div><div class="shelf"></div></div>
<div class="phone"><div class="island"></div><img src="${mobileURL}"></div>
</body></html>`;

  const htmlPath = outPath.replace(/\.png$/, ".html");
  fs.writeFileSync(htmlPath, html);
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto("file://" + htmlPath, { waitUntil: "networkidle0", timeout: 60000 });
  await page.evaluate(async () => { await document.fonts.ready; });
  await new Promise(r => setTimeout(r, 700));
  await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  await page.close();
}

module.exports = { launch, captureHero, composeMockup };
