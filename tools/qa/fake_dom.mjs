/**
 * fake_dom.mjs — un DOM minuscule, juste assez grand pour rejouer le JavaScript d'une page AMK
 * sans navigateur (il n'y en a pas dans le bac : voir `design/LESSONS.md`).
 *
 * Pourquoi ce fichier existe, et pourquoi il est dans le dépôt et non dans /tmp :
 * ces harnais avaient été écrits dans /tmp le 23/09 au soir, et l'instantané du bac est revenu au point
 * de branchement — les tests avaient disparu, la page non. Un test qu'on ne peut pas relancer n'est pas
 * un test, c'est une anecdote. Il vit maintenant ici, versionné, à côté du portique.
 *
 * Ce qu'il fait, et ce qu'il ne fait PAS :
 *  - il fournit `el()`, `doc()`, un `localStorage` en mémoire et un faux `Date` : de quoi exécuter les
 *    scripts de la page et LIRE CE QU'ILS ÉCRIVENT (textes, attributs, classes) ;
 *  - il ne fait ni mise en page, ni CSS, ni rendu. Il ne remplace pas l'œil de King : il vérifie ce qui
 *    est vérifiable en code (états, messages générés, attributs d'accessibilité).
 *
 * Usage :  node tools/qa/test_unilabo_page.mjs
 */

/** Un élément : attributs, classes, écouteurs, texte — et de quoi déclencher un événement à la main. */
export function el(tag = "div") {
  const attrs = Object.create(null);
  const classes = new Set();
  const listeners = Object.create(null);
  let text = "";
  const node = {
    tagName: tag.toUpperCase(),
    value: "",
    hidden: false,
    innerHTML: "",
    checked: false,
    prevented: false,
    _attrs: attrs,
    _classes: classes,
    setAttribute(k, v) { attrs[k] = String(v); },
    getAttribute(k) { return k in attrs ? attrs[k] : null; },
    removeAttribute(k) { delete attrs[k]; },
    addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
    focus() { node.focused = true; },
    /** déclenche un écouteur avec un événement minimal (preventDefault est observable) */
    fire(type, ev) {
      const e = ev || { preventDefault() { node.prevented = true; } };
      (listeners[type] || []).forEach((fn) => fn(e));
      return node.prevented;
    },
  };
  Object.defineProperty(node, "textContent", { get: () => text, set: (v) => { text = String(v); } });
  Object.defineProperty(node, "className", { get: () => [...classes].join(" ") });
  node.classList = {
    add: (c) => classes.add(c),
    remove: (c) => classes.delete(c),
    contains: (c) => classes.has(c),
    toggle: (c, force) => (force ? classes.add(c) : classes.delete(c)),
  };
  return node;
}

/**
 * Un faux `document`.
 * `registry` fait tout le travail : les clés préfixées `Q:` répondent à `querySelector`,
 * `QA:` à `querySelectorAll` (tableau), et tout le reste à `getElementById`.
 */
export function doc(registry, lang = "fr") {
  const root = el("html");
  root.setAttribute("data-lang", lang);
  return {
    documentElement: root,
    body: el("body"),
    getElementById: (id) => (id in registry ? registry[id] : null),
    querySelector: (sel) => (("Q:" + sel) in registry ? registry["Q:" + sel] : null),
    querySelectorAll: (sel) => registry["QA:" + sel] || [],
    addEventListener() {},
  };
}

export function localStorageStub() {
  const store = Object.create(null);
  return {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
  };
}

/**
 * Une horloge figée, à l'heure de Douala (UTC+1) — c'est ce que la page lit pour dire « ouvert ».
 * `iso` est l'instant réel ; la classe rend le décalage comme le ferait un navigateur réglé sur UTC.
 */
export function fixedClock(iso) {
  const t = Date.parse(iso);
  return class FixedDate extends Date {
    constructor() { super(t); }
    getTime() { return t; }
    getTimezoneOffset() { return 0; }
    getDay() { return new Date(t + 3600000).getUTCDay(); }
    getHours() { return new Date(t + 3600000).getUTCHours(); }
    getMinutes() { return new Date(t + 3600000).getUTCMinutes(); }
  };
}

/** Extrait d'un fichier HTML le contenu d'un `<script>` repéré par un marqueur de son en-tête. */
export function scriptAfter(html, marker) {
  const i = html.indexOf(marker);
  if (i < 0) throw new Error("marqueur introuvable : " + marker);
  const start = html.lastIndexOf("<script>", i);
  const end = html.indexOf("</script>", i);
  if (start < 0 || end < 0) throw new Error("bloc <script> introuvable autour de : " + marker);
  return html.slice(start + "<script>".length, end);
}

/** Lisible par un humain : le message WhatsApp décodé, prêt à être lu mot pour mot. */
export function waMessage(href) {
  const m = /[?&]text=([^&]*)/.exec(href || "");
  return m ? decodeURIComponent(m[1]) : "";
}

export function ok(label, condition, detail = "") {
  console.log(`${condition ? "  ok  " : "  FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!condition) process.exitCode = 1;
  return condition;
}
