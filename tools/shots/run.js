// AMK concept mockup pipeline — capture hero shots and compose the house-style
// laptop+phone mockup (1920x1080, matching demos/shots/oracare-mockup.png).
//
// Setup (once): see README.md  — npm i; chromium needs NSS/NSPR libs on minimal Linux.
// Run:   node run.js [secondary|mitoc|clinic|...]
// Output: raw hero shots in out/<name>-{desktop,mobile}.png
//         composed mockup in out/mockup-<name>.png  (copy kept deliverables to demos/shots/)
const { launch, captureHero, composeMockup } = require("./lib");
const path = require("path");

const REPO = path.join(__dirname, "..", "..");
const SITE = "file://" + path.join(REPO, "site") + "/";
const OUT = path.join(__dirname, "out");

const JOBS = [
  {
    file: "sample-secondary.html", name: "secondary",
    cfg: {
      bg1: "#FAF8F2", bg2: "#ECE3CB", glow: "rgba(176,138,62,.22)", glow2: "rgba(15,42,71,.07)",
      accent: "#B08A3E", title: "#0F2A47", tag: "#5A6675", chipBg: "#0F2A47", chipText: "#ffffff",
      spark: "#B08A3E", shadow: "rgba(15,32,55,.28)",
      eyebrow: "Website concept &nbsp;·&nbsp; Bilingual secondary college · Cameroon",
      title: "Crestwood College",
      tagline: "GCE O &amp; A Level · Day &amp; boarding · FCFA fees · WhatsApp admissions",
      chip: "Concept by AMK — your real site, live in 3-5 days",
    },
  },
  {
    file: "mitoc.html", name: "mitoc",
    cfg: {
      bg1: "#F6F8FC", bg2: "#DFE8F4", glow: "rgba(21,83,158,.20)", glow2: "rgba(232,163,61,.10)",
      accent: "#15539E", title: "#0C2745", tag: "#4C5D70", chipBg: "#133E6E", chipText: "#ffffff",
      spark: "#C9923B", shadow: "rgba(12,39,69,.28)",
      eyebrow: "Website concept &nbsp;·&nbsp; Molyko-Malingo, Buea",
      title: "Midas Touch Optic Center",
      tagline: "Eye tests · Frames, computer &amp; swimming glasses · WhatsApp booking",
      chip: "Concept by AMK — your real site, live in 3-5 days",
    },
  },
  {
    file: "clinic-bonaberi.html", name: "clinic",
    cfg: {
      bg1: "#F5F4EC", bg2: "#DFE8DA", glow: "rgba(14,122,92,.20)", glow2: "rgba(201,146,59,.10)",
      accent: "#0E7A5C", title: "#103F31", tag: "#4E6259", chipBg: "#114333", chipText: "#ffffff",
      spark: "#C9923B", shadow: "rgba(17,67,51,.28)",
      eyebrow: "Website concept &nbsp;·&nbsp; Private clinic &amp; laboratory · Douala",
      title: "Bonabéri Medical Centre",
      tagline: "Transparent FCFA prices · Same-day laboratory · WhatsApp appointments",
      chip: "Concept by AMK — your real site, live in 3-5 days",
    },
  },
];

(async () => {
  const only = process.argv[2]; // optional single name
  const browser = await launch();
  for (const j of JOBS) {
    if (only && j.name !== only) continue;
    await captureHero(browser, SITE + j.file, j.name, OUT);
    await composeMockup(browser, {
      ...j.cfg,
      desktopFile: j.name + "-desktop.png",
      mobileFile: j.name + "-mobile.png",
    }, path.join(OUT, "mockup-" + j.name + ".png"));
    console.log("mockup done:", j.name);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
