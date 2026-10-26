/**
 * ─────────────────────────────────────────────────────────────────────────────
 * App — le seul endroit qui touche au DOM
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * Rien n'est écrit en dur dans le HTML : les textes viennent du dictionnaire,
 * les lieux de la configuration, la semaine de la configuration aussi. Changer
 * un jour de consultation = éditer js/config/doctor.js, et rien d'autre.
 */
import { doctorConfig, isKnown, doctorDisplayName, whatsappNumber } from "./config/doctor.js";
import { services, servicesEmptyNotice } from "./config/services.js";
import {
  contactMethods,
  limits,
  whatsappMessage,
  formatDateOnly,
  buildWhatsappUrl,
} from "./config/appointment.js";
import { createTranslator, defaultLang, supportedLangs, langTag } from "./i18n/index.js";
import { buildWeek, hasAnyHours, hoursText, locationDays, locationLabel } from "./lib/schedule.js";
import { validate, errorText } from "./lib/validators.js";

/* ── État : une seule source, et le rendu en découle ───────────────────── */
const STORAGE_KEY = "dr-ophtalmo.lang";

const firstLocationId = doctorConfig.locations[0]?.id || "";

const state = {
  lang: readInitialLang(),
  selectedId: firstLocationId,
  values: {
    fullName: "",
    contactMethod: "whatsapp",
    contact: "",
    locationId: firstLocationId,
    preferredDate: "",
    preferredTime: "",
    note: "",
  },
  errors: {},
  attempted: false,
  result: null,
};

let t = createTranslator(state.lang);

/* ── Petits outils DOM ─────────────────────────────────────────────────── */
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "html") node.innerHTML = value;
    else if (key === "dataset") Object.assign(node.dataset, value);
    else if (key.startsWith("on") && typeof value === "function") {
      node.addEventListener(key.slice(2).toLowerCase(), value);
    } else node.setAttribute(key, value === true ? "" : String(value));
  }
  const list = Array.isArray(children) ? children : [children];
  for (const child of list) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

const clear = (node) => {
  while (node && node.firstChild) node.removeChild(node.firstChild);
  return node;
};

const reducedMotion = () =>
  window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function readInitialLang() {
  const fromUrl = new URLSearchParams(window.location.search).get("lang");
  if (fromUrl && supportedLangs.includes(fromUrl)) return fromUrl;
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored && supportedLangs.includes(stored)) return stored;
  } catch {
    /* navigation privée : on continue sans mémoire */
  }
  return defaultLang;
}

function persistLang() {
  try {
    window.localStorage.setItem(STORAGE_KEY, state.lang);
  } catch {
    /* sans mémoire, la langue reste correcte pour la visite en cours */
  }
}

const selectedLocation = () =>
  doctorConfig.locations.find((location) => location.id === state.selectedId) || doctorConfig.locations[0];

/* ═════════════════════════════════════════════════════════════════════════
   1 · Textes statiques (data-i18n)
   ═════════════════════════════════════════════════════════════════════════ */
function renderStatic() {
  document.documentElement.lang = state.lang;
  document.title = t("meta.title");
  const description = $('meta[name="description"]');
  if (description) description.setAttribute("content", t("meta.description"));

  for (const node of $$("[data-i18n]")) {
    const key = node.dataset.i18n;
    if (key) node.textContent = t(key);
  }
  for (const node of $$("[data-i18n-aria]")) {
    const key = node.dataset.i18nAria;
    if (key) node.setAttribute("aria-label", t(key));
  }

  // Le titre du hero : trois lignes, dictées par le dictionnaire
  const heroTitle = $("[data-hero-title]");
  if (heroTitle) {
    clear(heroTitle);
    for (const line of t("hero.h1")) heroTitle.append(el("span", { text: line }));
  }

  // Les photographies du médecin, remplies depuis la configuration : jamais
  // une image en dur dans le HTML, sinon la légende et l'alt divergent.
  renderImages();

  const heroStatus = $("[data-hero-status]");
  if (heroStatus) heroStatus.textContent = t("hero.statusLine");

  for (const node of $$("[data-i18n-placeholder]")) {
    node.setAttribute("placeholder", t(node.dataset.i18nPlaceholder));
  }

  for (const button of $$("[data-lang]")) {
    button.setAttribute("aria-pressed", String(button.dataset.lang === state.lang));
  }

  const toggle = $("[data-nav-toggle]");
  if (toggle) {
    const open = toggle.getAttribute("aria-expanded") === "true";
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = open ? t("common.closeMenu") : t("common.openMenu");
  }
}

/* ═════════════════════════════════════════════════════════════════════════
   2 · Parcours — fiche professionnelle
   ═════════════════════════════════════════════════════════════════════════ */
function renderProfile() {
  const list = $("[data-profile-list]");
  if (!list) return;
  clear(list);

  const profile = doctorConfig.profile;
  const name = doctorDisplayName();
  const rows = [
    ["name", name, "parcours.placeholders.name"],
    ["specialty", doctorConfig.specialty, null],
    ["qualifications", profile.qualifications.join(" · "), "parcours.placeholders.qualifications"],
    ["registration", profile.registration, "parcours.placeholders.registration"],
    ["languages", profile.languages.join(" · "), "parcours.placeholders.languages"],
    ["interests", profile.interests.join(" · "), "parcours.placeholders.interests"],
    ["bio", profile.bio, "parcours.placeholders.bio"],
  ];

  for (const [key, value, placeholderKey] of rows) {
    const dd = el("dd");
    if (isKnown(value)) {
      dd.textContent = value;
    } else if (placeholderKey) {
      dd.append(el("span", { class: "placeholder", text: t(placeholderKey) }));
    } else {
      continue; // ni valeur ni texte d'attente : la ligne n'existe pas
    }
    list.append(
      el("div", { class: "profile-row" }, [el("dt", { text: t(`parcours.labels.${key}`) }), dd]),
    );
  }

  const serviceList = $("[data-service-list]");
  const serviceNote = $("[data-service-note]");
  if (serviceList) {
    clear(serviceList);
    if (services.length === 0) {
      if (serviceNote) serviceNote.textContent = servicesEmptyNotice[state.lang] || servicesEmptyNotice.fr;
    } else {
      if (serviceNote) serviceNote.textContent = "";
      for (const service of services) {
        const item = el("li", {}, [document.createTextNode(service.label[state.lang] || service.label.fr)]);
        const note = service.note && (service.note[state.lang] || service.note.fr);
        if (note) item.append(el("span", { class: "service-note-line", text: note }));
        serviceList.append(item);
      }
    }
  }
}

/* ═════════════════════════════════════════════════════════════════════════
   3 · Consultations — sélecteur, détail, semaine
   ═════════════════════════════════════════════════════════════════════════ */
const chip = (status, light = false) =>
  el("span", {
    class: light ? "chip chip--light" : "chip",
    dataset: { status },
    text: t(`common.${status === "unknown" ? "unknown" : status}`),
    title: t(`consultations.statusHint.${status}`),
  });

function renderPicker() {
  const picker = $("[data-location-picker]");
  if (!picker) return;
  clear(picker);

  for (const location of doctorConfig.locations) {
    const input = el("input", {
      type: "radio",
      name: "location",
      value: location.id,
      checked: location.id === state.selectedId,
      onchange: () => selectLocation(location.id, { scroll: false, fromPicker: true }),
    });
    const days = locationDays(location, t);
    const label = el("label", { class: "picker-option" }, [
      input,
      el("span", { class: "picker-num", text: location.order || "" }),
      el("span", {}, [
        el("span", { class: "picker-name", text: locationLabel(location, t) }),
        el("span", {
          class: "picker-days",
          text: days || t("consultations.notPublished"),
        }),
      ]),
      el("span", {
        class: "picker-status",
        dataset: { status: location.status || "unknown" },
        "aria-hidden": "true",
      }),
    ]);
    picker.append(label);
  }
}

function renderDetail() {
  const detail = $("[data-location-detail]");
  if (!detail) return;
  clear(detail);

  const location = selectedLocation();
  if (!location) return;

  const status = location.status || "unknown";
  const days = locationDays(location, t);

  const head = el("div", { class: "detail-head" }, [
    el("div", {}, [
      el("h3", { class: "detail-name", text: location.facility || location.city }),
      location.facility ? el("p", { class: "detail-city", text: location.city }) : null,
    ]),
    chip(status, true),
  ]);

  const rows = [
    ["city", location.city],
    ["facility", location.facility],
    ["address", location.address],
    ["days", days],
    ["hours", hoursText(location.hours, state.lang)],
    ["phone", location.contactPhone],
  ];

  const dl = el("dl", { class: "detail-rows" });
  for (const [key, raw] of rows) {
    const value = isKnown(raw) ? raw : null;
    const dd = el("dd");
    if (value) {
      dd.textContent = value;
    } else if (key === "hours") {
      dd.append(el("span", { class: "placeholder", text: t("consultations.scheduleHoursMissing") }));
    } else if (key === "facility") {
      dd.append(el("span", { class: "placeholder", text: t("consultations.facilityPlaceholder") }));
    } else {
      dd.append(el("span", { class: "placeholder", text: t("consultations.notPublished") }));
    }
    if (key === "facility" && !value) continue; // pas de structure annoncée : la ligne n'aide pas
    dl.append(
      el("div", { class: "detail-row" }, [
        el("dt", { text: t(`consultations.labels.${key}`) }),
        dd,
      ]),
    );
  }

  const actions = el("div", { class: "detail-actions" });
  actions.append(
    el("button", {
      type: "button",
      class: "btn btn--primary",
      text: t("consultations.requestCta"),
      onclick: () => {
        selectLocation(location.id, { scroll: true });
      },
    }),
  );
  if (isKnown(location.mapUrl)) {
    actions.append(
      el("a", {
        class: "btn btn--ghost",
        href: location.mapUrl,
        target: "_blank",
        rel: "noopener",
        text: t("consultations.directions"),
      }),
    );
  }

  const parts = [head, dl, actions];

  if (location.facility) {
    parts.push(el("p", { class: "detail-note", text: t("consultations.facilityNote") }));
  }

  const sourceDetails = el("details", { class: "detail-source" }, [
    el("summary", { text: `${t("consultations.sourceLabel")} · ${t("common.reported")}` }),
    el("p", { text: location.source || t("consultations.scheduleNote") }),
  ]);
  parts.push(sourceDetails);

  for (const part of parts) detail.append(part);
}

function renderSchedule() {
  const container = $("[data-schedule]");
  const noteNode = $("[data-schedule-note]");
  if (!container) return;
  clear(container);

  const week = buildWeek();
  const todayIndex = (new Date().getDay() + 6) % 7; // lundi = 0
  const anythingMissing = !hasAnyHours() || doctorConfig.locations.some((l) => !l.days?.length);

  week.forEach((day, index) => {
    const row = el("div", { class: "schedule-row" + (index === todayIndex ? " is-today" : "") });
    const dayLabel = el("div", { class: "day-name" }, [
      document.createTextNode(t(`weekdays.${day.day}`)),
    ]);
    if (index === todayIndex) {
      dayLabel.append(el("span", { class: "day-today", text: t("common.today") }));
    }
    row.append(dayLabel);

    if (day.entries.length === 0) {
      row.append(el("p", { class: "day-empty", text: t("consultations.scheduleDayEmpty") }));
    } else {
      const first = day.entries[0];
      const placeText = day.entries
        .map((entry) => locationLabel({ facility: entry.facility, city: entry.city, id: entry.locationId }, t))
        .join(" · ");
      row.append(el("p", { class: "day-place", text: placeText }));

      const hours = day.entries.map((entry) => hoursText(entry.hours, state.lang)).filter(isKnown).join(" · ");
      row.append(
        hours
          ? el("p", { class: "day-hours", text: hours })
          : el("p", { class: "day-hours is-missing", text: t("consultations.scheduleHoursMissing") }),
      );

      if (first) {
        row.append(
          el("button", {
            type: "button",
            class: "day-action",
            text: t("consultations.scheduleAction"),
            "aria-label": `${t("consultations.scheduleAction")} — ${placeText}`,
            onclick: () => selectLocation(first.locationId, { scroll: true }),
          }),
        );
      }
    }
    container.append(row);
  });

  if (noteNode) {
    clear(noteNode);
    noteNode.append(
      el("p", {
        text: t("consultations.scheduleAsOf", { date: formatDateOnly(doctorConfig.meta.infoAsOf, state.lang) }),
      }),
    );
    noteNode.append(el("p", { text: t("consultations.scheduleNote") }));
    if (anythingMissing) {
      noteNode.append(
        el("p", { class: "note-alert" }, [
          el("span", { class: "notice-icon", "aria-hidden": "true", text: "!" }),
          el("span", { text: t("consultations.scheduleUnverified") }),
        ]),
      );
    }
  }
}

function selectLocation(id, { scroll = false } = {}) {
  state.selectedId = id;
  state.values.locationId = id;

  const select = $("[data-location-select]");
  if (select) select.value = id;

  for (const input of $$('input[name="location"]')) {
    input.checked = input.value === id;
  }

  renderDetail();

  if (state.attempted) {
    state.errors = validate(state.values, { t });
    renderErrors();
  }

  if (scroll) scrollToId("appointments");
}

/* ═════════════════════════════════════════════════════════════════════════
   4 · Rendez-vous
   ═════════════════════════════════════════════════════════════════════════ */
function renderForm() {
  const select = $("[data-location-select]");
  if (select) {
    const current = state.values.locationId || state.selectedId;
    clear(select);
    select.append(el("option", { value: "", text: t("appointment.placeholders.choose") }));
    for (const location of doctorConfig.locations) {
      select.append(el("option", { value: location.id, text: locationLabel(location, t) }));
    }
    select.value = current;
  }

  const methods = $("[data-contact-methods]");
  if (methods) {
    clear(methods);
    for (const method of contactMethods) {
      methods.append(
        el("label", { class: "radio-option" }, [
          el("input", {
            type: "radio",
            name: "contactMethod",
            value: method,
            checked: state.values.contactMethod === method,
            onchange: () => {
              state.values.contactMethod = method;
              renderContactLabel();
              if (state.attempted) {
                state.errors = validate(state.values, { t });
                renderErrors();
              }
            },
          }),
          document.createTextNode(t(`appointment.methods.${method}`)),
        ]),
      );
    }
  }

  renderContactLabel();

  const placeholders = {
    fullName: t("appointment.placeholders.fullName"),
    contact:
      state.values.contactMethod === "email"
        ? t("appointment.placeholders.contactEmail")
        : t("appointment.placeholders.contactPhone"),
    note: t("appointment.placeholders.note"),
  };
  for (const [field, placeholder] of Object.entries(placeholders)) {
    const input = $(`[data-field="${field}"]`);
    if (input) input.setAttribute("placeholder", placeholder);
  }
  const contactInput = $('[data-field="contact"]');
  if (contactInput) {
    contactInput.type = state.values.contactMethod === "email" ? "email" : "text";
    contactInput.inputMode = state.values.contactMethod === "email" ? "email" : "tel";
    contactInput.autocomplete = state.values.contactMethod === "email" ? "email" : "tel";
  }

  renderErrors();
  renderResult();
}

function renderContactLabel() {
  const label = $("[data-contact-label]");
  if (!label) return;
  const method = state.values.contactMethod;
  label.textContent =
    method === "email" ? t("appointment.labels.contactEmail") : t("appointment.labels.contactPhone");
}

function renderErrors() {
  const summary = $("[data-form-summary]");
  const keys = Object.keys(state.errors);

  for (const node of $$("[data-error]")) {
    const field = node.dataset.error;
    node.textContent = state.errors[field] ? errorText(state.errors[field], t) : "";
  }
  for (const input of $$("[data-field]")) {
    const field = input.dataset.field;
    if (state.errors[field]) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
  }
  if (summary) {
    summary.textContent = keys.length > 0 && state.attempted ? t("appointment.errors.summary") : "";
  }
}

function renderResult() {
  const panel = $("[data-result]");
  if (!panel) return;
  const result = state.result;
  panel.hidden = !result;
  if (!result) return;

  const title = $("[data-result-title]");
  const note = $("[data-result-note]");
  const message = $("[data-result-message]");
  const link = $("[data-result-whatsapp]");

  const hasNumber = Boolean(whatsappNumber());
  if (title) title.textContent = hasNumber ? t("appointment.review") : t("appointment.noNumberTitle");
  if (note) note.textContent = hasNumber ? t("appointment.preparedNote") : t("appointment.noNumberBody");
  if (message) message.textContent = result.message;

  if (link) {
    if (result.url) {
      link.href = result.url;
      link.hidden = false;
      link.target = "_blank";
      link.rel = "noopener";
    } else {
      link.removeAttribute("href");
      link.hidden = true;
    }
  }
}

function collectForm() {
  for (const input of $$("[data-field]")) {
    const field = input.dataset.field;
    if (field === "contactMethod") continue;
    state.values[field] = input.value;
  }
}

function onSubmit(event) {
  event.preventDefault();
  collectForm();
  state.attempted = true;
  state.errors = validate(state.values, { t });
  renderErrors();

  if (Object.keys(state.errors).length > 0) {
    state.result = null;
    renderResult();
    const firstKey = Object.keys(state.errors)[0];
    const target = $(`[data-field="${firstKey}"]`);
    if (target) target.focus();
    return;
  }

  const location = doctorConfig.locations.find((item) => item.id === state.values.locationId);
  const message = whatsappMessage({
    t,
    values: state.values,
    locationLabel: location ? locationLabel(location, t) : "",
    doctorName: doctorDisplayName() || "",
  });

  const number = whatsappNumber();
  state.result = {
    message,
    url: number ? buildWhatsappUrl(number, message) : "",
  };
  renderResult();

  announce(t("appointment.preparedTitle"));
  const panel = $("[data-result]");
  if (panel) panel.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "center" });
}

async function copyMessage() {
  const text = state.result?.message || "";
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    announce(t("appointment.copied"));
  } catch {
    const pre = $("[data-result-message]");
    if (pre) {
      const range = document.createRange();
      range.selectNodeContents(pre);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }
    announce(t("appointment.copyFailed"));
  }
}

function resetForm() {
  state.values = {
    fullName: "",
    contactMethod: "whatsapp",
    contact: "",
    locationId: state.selectedId,
    preferredDate: "",
    preferredTime: "",
    note: "",
  };
  state.errors = {};
  state.attempted = false;
  state.result = null;
  const form = $("[data-form]");
  if (form) form.reset();
  for (const input of $$("[data-field]")) {
    if (input.tagName === "SELECT") input.value = state.selectedId;
    else if (input.type !== "radio" && input.type !== "checkbox") input.value = "";
  }
  renderForm();
  const first = $('[data-field="fullName"]');
  if (first) first.focus();
}

/* ═════════════════════════════════════════════════════════════════════════
   5 · Pied de page, dialogue, données structurées
   ═════════════════════════════════════════════════════════════════════════ */
function renderFooter() {
  const list = $("[data-footer-locations]");
  if (list) {
    clear(list);
    for (const location of doctorConfig.locations) {
      const days = locationDays(location, t);
      list.append(
        el("li", {}, [
          el("a", {
            href: "#consultations",
            text: locationLabel(location, t),
            onclick: (event) => {
              event.preventDefault();
              selectLocation(location.id, { scroll: true });
              history.replaceState(null, "", "#consultations");
            },
          }),
          el("span", { class: "footer-days", text: days || t("consultations.notPublished") }),
        ]),
      );
    }
  }

  const contact = $("[data-footer-contact]");
  if (contact) {
    clear(contact);
    const entries = [];
    const number = whatsappNumber();
    if (number) {
      entries.push(
        el("a", {
          href: buildWhatsappUrl(number, whatsappMessage({ t, values: {}, locationLabel: "", doctorName: "" })),
          target: "_blank",
          rel: "noopener",
          text: `WhatsApp · ${formatPhone(number)}`,
        }),
      );
    }
    if (isKnown(doctorConfig.contact.phone)) {
      entries.push(
        el("a", { href: `tel:${doctorConfig.contact.phone.replace(/\s/g, "")}`, text: doctorConfig.contact.phone }),
      );
    }
    if (isKnown(doctorConfig.contact.email)) {
      entries.push(el("a", { href: `mailto:${doctorConfig.contact.email}`, text: doctorConfig.contact.email }));
    }
    if (entries.length === 0) {
      entries.push(el("p", { class: "footer-missing", text: t("footer.contactMissing") }));
      entries.push(el("p", { class: "footer-missing", text: t("footer.contactMissingNote") }));
    }
    for (const entry of entries) contact.append(entry);
  }

  const rights = $("[data-footer-rights]");
  if (rights) rights.textContent = `${t("footer.rights")} · ${doctorConfig.meta.infoAsOf}`;
}

const formatPhone = (digits) =>
  String(digits).replace(/^(\d{3})(\d{1})(\d{2})(\d{2})(\d{2})(\d{2})$/, "+$1 $2 $3 $4 $5 $6");


/* ═════════════════════════════════════════════════════════════════════════
   1 bis · Photographies du médecin, et actions directes
   ═════════════════════════════════════════════════════════════════════════ */

/**
 * Chaque `img[data-photo]` reçoit sa source, son srcset, ses dimensions et son
 * texte alternatif depuis `doctorConfig.images`. Les légendes suivent : une
 * photographie réelle porte sa provenance, une image d'illustration se déclare.
 */
function renderImages() {
  const images = doctorConfig.images || {};
  for (const img of $$("img[data-photo]")) {
    const cfg = images[img.dataset.photo];
    if (!cfg) continue;
    img.src = cfg.src;
    img.srcset = cfg.srcset || "";
    if (cfg.width) img.width = cfg.width;
    if (cfg.height) img.height = cfg.height;
    img.alt = cfg.alt ? cfg.alt[state.lang] || cfg.alt[defaultLang] : "";
    const caption = img.closest("figure")?.querySelector("[data-photo-caption]");
    if (caption) {
      const text = cfg.caption ? cfg.caption[state.lang] || cfg.caption[defaultLang] : "";
      caption.textContent = text || "";
      caption.hidden = !text;
    }
  }

  // Le portrait du hero garde son propre point d'entrée (compatibilité).
  const portrait = $("[data-portrait]");
  const portraitCfg = doctorConfig.profile.portrait;
  if (portrait && portraitCfg) {
    portrait.srcset = portraitCfg.srcset;
    portrait.alt = portraitCfg.alt[state.lang] || portraitCfg.alt[defaultLang];
  }
  const portraitCaption = $("[data-portrait-caption]");
  if (portraitCaption) {
    const text = portraitCfg?.isRealPhoto
      ? portraitCfg.caption?.[state.lang] || portraitCfg.caption?.[defaultLang] || ""
      : t("hero.portraitCaption");
    portraitCaption.textContent = text;
    portraitCaption.hidden = !text;
  }

  // L'identité affichée sous le titre du hero : « Dr Fogue · Ophtalmologie ».
  const identity = $("[data-hero-identity]");
  if (identity) {
    const name = doctorDisplayName();
    identity.textContent = name ? `${name} · ${doctorConfig.specialty}` : t("hero.identityPending");
    identity.hidden = false;
  }

  // Le bouton WhatsApp du hero : il n'existe que si un numéro est publié.
  const waLink = $("[data-hero-wa]");
  if (waLink) {
    const number = whatsappNumber();
    if (number) {
      waLink.href = buildWhatsappUrl(number, t("wa.direct"));
      waLink.textContent = `${t("hero.whatsappCta")} · ${formatPhone(number)}`;
      waLink.hidden = false;
    } else {
      waLink.hidden = true;
    }
  }
}

function renderInfoDialog() {
  const container = $("[data-info-list]");
  if (!container) return;
  clear(container);

  const groups = [
    {
      title: t("footer.questionsTitle"),
      items: (doctorConfig.meta.questions || []).map((question) => [
        question[state.lang] || question.fr,
        false,
        "",
      ]),
    },
    {
      title: t("parcours.labels.name"),
      items: [
        [t("parcours.labels.name"), isKnown(doctorConfig.name), doctorConfig.name],
        [t("parcours.labels.qualifications"), doctorConfig.profile.qualifications.length > 0, ""],
        [t("parcours.labels.registration"), isKnown(doctorConfig.profile.registration), ""],
        [t("parcours.labels.languages"), doctorConfig.profile.languages.length > 0, ""],
        [t("parcours.labels.bio"), isKnown(doctorConfig.profile.bio), ""],
      ],
    },
    {
      title: t("footer.contact"),
      items: [
        [t("footer.contact"), isKnown(doctorConfig.contact.whatsapp), ""],
        [t("appointment.labels.contactEmail"), isKnown(doctorConfig.contact.email), ""],
      ],
    },
    ...doctorConfig.locations.map((location) => ({
      title: locationLabel(location, t),
      items: [
        [t("consultations.labels.facility"), isKnown(location.facility), location.facility],
        [t("consultations.labels.address"), isKnown(location.address), location.address],
        [t("consultations.labels.days"), (location.days || []).length > 0, locationDays(location, t)],
        [t("consultations.labels.hours"), isKnown(hoursText(location.hours, state.lang)), hoursText(location.hours, state.lang)],
        [t("consultations.labels.phone"), isKnown(location.contactPhone), location.contactPhone],
      ],
    })),
  ];

  for (const group of groups) {
    const items = el("ul");
    for (const [label, known, value] of group.items) {
      items.append(
        el("li", { dataset: { known: String(known) }, text: known && value ? `${label} — ${value}` : label }),
      );
    }
    container.append(
      el("div", { class: "info-group" }, [el("h3", { text: group.title }), items]),
    );
  }
}

function renderStructuredData() {
  const previous = $("#doctor-jsonld");
  if (previous) previous.remove();

  const data = {
    "@context": "https://schema.org",
    "@type": "Physician",
    medicalSpecialty: "https://schema.org/Ophthalmologic",
    areaServed: doctorConfig.locations.map((location) => ({
      "@type": "City",
      name: location.city,
    })),
    availableService: services.map((service) => ({
      "@type": "MedicalProcedure",
      name: service.label.fr,
    })),
  };
  const name = doctorDisplayName();
  if (name) data.name = name;
  if (isKnown(doctorConfig.contact.phone)) data.telephone = doctorConfig.contact.phone;
  if (isKnown(doctorConfig.contact.email)) data.email = doctorConfig.contact.email;

  const script = el("script", { type: "application/ld+json", id: "doctor-jsonld" });
  script.textContent = JSON.stringify(data);
  document.head.append(script);
}

/* ═════════════════════════════════════════════════════════════════════════
   6 · Navigation, langue, défilement, apparitions
   ═════════════════════════════════════════════════════════════════════════ */
function announce(message) {
  const live = $("[data-live]");
  if (!live) return;
  live.textContent = "";
  window.setTimeout(() => {
    live.textContent = message;
  }, 40);
}

function scrollToId(id) {
  const target = document.getElementById(id);
  if (!target) return;
  if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
  target.scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "start" });
  target.focus({ preventScroll: true });
  history.replaceState(null, "", `#${id}`);
}

function setLang(lang) {
  if (!supportedLangs.includes(lang) || lang === state.lang) return;
  state.lang = lang;
  t = createTranslator(lang);
  persistLang();

  // Le formulaire garde ses valeurs : on relit le DOM avant de redessiner.
  collectForm();
  renderStatic();
  renderProfile();
  renderPicker();
  renderDetail();
  renderSchedule();
  renderForm();
  renderFooter();
  renderInfoDialog();

  // L'URL suit la langue, sans recharger la page ni perdre la section.
  const url = new URL(window.location.href);
  url.searchParams.set("lang", lang);
  history.replaceState(null, "", url);

  const pressed = $(`[data-lang="${lang}"]`);
  if (pressed) pressed.focus({ preventScroll: true });
}

function setupNav() {
  const header = $("[data-header]");
  const toggle = $("[data-nav-toggle]");
  const nav = $("#primary-nav");
  if (!header || !toggle || !nav) return;

  const setOpen = (open) => {
    header.classList.toggle("is-nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    const label = toggle.querySelector(".visually-hidden");
    if (label) label.textContent = open ? t("common.closeMenu") : t("common.openMenu");
  };

  toggle.addEventListener("click", () => {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) setOpen(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && header.classList.contains("is-nav-open")) {
      setOpen(false);
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!header.classList.contains("is-nav-open")) return;
    if (!header.contains(event.target)) setOpen(false);
  });

  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Le lien courant, sans dépendre du survol
  const sections = ["hero", "parcours", "consultations"]
    .map((id) => document.getElementById(id))
    .filter(Boolean);
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const id = entry.target.id;
          for (const link of $$(".nav-list a")) {
            if (link.getAttribute("href") === `#${id}`) link.setAttribute("aria-current", "true");
            else link.removeAttribute("aria-current");
          }
        }
      },
      { rootMargin: "-45% 0px -45% 0px", threshold: 0 },
    );
    for (const section of sections) observer.observe(section);
  }
}

function setupSmoothAnchors() {
  document.addEventListener("click", (event) => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const id = link.getAttribute("href").slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    scrollToId(id);
  });
}

function setupReveal() {
  if (reducedMotion() || !("IntersectionObserver" in window)) return;
  const targets = $$(".section-title, .lede, .parcours-figure, .profile-card, .band-figure, .panel, .location-detail, .appointment-card, .hero-figure");
  targets.forEach((node, index) => {
    node.dataset.reveal = "";
    node.style.setProperty("--reveal-delay", `${Math.min(index % 4, 3) * 70}ms`);
  });
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        }
      }
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.05 },
  );
  targets.forEach((node) => observer.observe(node));
}

function setupForm() {
  const form = $("[data-form]");
  if (!form) return;

  form.addEventListener("input", (event) => {
    const input = event.target.closest("[data-field]");
    if (!input) return;
    collectForm();
    if (state.attempted) {
      state.errors = validate(state.values, { t });
      renderErrors();
    }
  });

  form.addEventListener("change", (event) => {
    const input = event.target.closest("[data-field]");
    if (!input) return;
    collectForm();
    if (state.attempted) {
      state.errors = validate(state.values, { t });
      renderErrors();
    }
    if (input.dataset.field === "locationId") {
      state.selectedId = state.values.locationId;
      for (const radio of $$('input[name="location"]')) radio.checked = radio.value === state.selectedId;
      renderDetail();
    }
  });

  form.addEventListener("submit", onSubmit);

  const reset = $("[data-reset]");
  if (reset) reset.addEventListener("click", resetForm);

  const copy = $("[data-copy]");
  if (copy) copy.addEventListener("click", copyMessage);

  const dateInput = $('[data-field="preferredDate"]');
  if (dateInput) {
    const today = new Date();
    const iso = (date) =>
      `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
    dateInput.min = iso(today);
    const limit = new Date();
    limit.setDate(limit.getDate() + limits.maxLeadDays);
    dateInput.max = iso(limit);
  }

  const noteInput = $('[data-field="note"]');
  if (noteInput) noteInput.maxLength = limits.message;
}

function setupLanguage() {
  for (const button of $$("[data-lang]")) {
    button.addEventListener("click", () => setLang(button.dataset.lang));
  }
}

function setupInfoDialog() {
  const dialog = $("[data-info-dialog]");
  const open = $("[data-open-info]");
  if (!dialog || !open) return;
  open.addEventListener("click", () => {
    renderInfoDialog();
    if (typeof dialog.showModal === "function") dialog.showModal();
  });
}

/* ═════════════════════════════════════════════════════════════════════════
   Démarrage
   ═════════════════════════════════════════════════════════════════════════ */
function init() {
  if (!doctorConfig.locations.some((location) => location.id === state.selectedId)) {
    state.selectedId = "";
  }

  renderStatic();
  renderProfile();
  renderPicker();
  renderDetail();
  renderSchedule();
  renderForm();
  renderFooter();
  renderInfoDialog();
  renderStructuredData();

  setupNav();
  setupSmoothAnchors();
  setupReveal();
  setupForm();
  setupLanguage();
  setupInfoDialog();

  // Un lieu peut être visé directement : #consultations?loc=… ou depuis le pied
  const params = new URLSearchParams(window.location.search);
  const requested = params.get("loc");
  if (requested && doctorConfig.locations.some((location) => location.id === requested)) {
    selectLocation(requested, { scroll: false });
  }

  document.documentElement.dataset.ready = "true";
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init, { once: true });
} else {
  init();
}
