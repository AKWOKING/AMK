/**
 * Le dictionnaire est unique, plat par convention (clés « a.b.c »), et c'est
 * lui qui pilote tout : le HTML ne porte que des attributs data-i18n, jamais de
 * texte figé. Changer de langue ne remplace donc rien « à la main ».
 */
import { fr } from "./fr.js";
import { en } from "./en.js";

export const dictionaries = { fr, en };
export const defaultLang = "fr";
export const supportedLangs = Object.keys(dictionaries);

/** Résout « appointment.labels.fullName » dans un dictionnaire. */
export function resolve(dict, path) {
  return path.split(".").reduce((node, key) => (node == null ? undefined : node[key]), dict);
}

/** Remplace {clef} par sa valeur ; laisse le texte tel quel si la clef manque. */
export function interpolate(template, vars = {}) {
  if (typeof template !== "string") return template;
  return template.replace(/\{(\w+)\}/g, (match, key) =>
    Object.prototype.hasOwnProperty.call(vars, key) ? String(vars[key]) : match,
  );
}

/**
 * Fabrique la fonction de traduction. `fallback` : si une clef manque en
 * anglais, on affiche le français plutôt qu'un trou — et on le voit tout de suite.
 */
export function createTranslator(lang) {
  const dict = dictionaries[lang] || dictionaries[defaultLang];
  const t = (path, vars) => {
    const value = resolve(dict, path);
    if (value === undefined) {
      const frValue = resolve(dictionaries[defaultLang], path);
      if (frValue === undefined) {
        if (typeof console !== "undefined") console.warn(`[i18n] clef manquante : ${path}`);
        return path;
      }
      return interpolate(frValue, vars);
    }
    return interpolate(value, vars);
  };
  t.lang = lang;
  t.dict = dict;
  return t;
}

/** Le nom de la langue, pour aria-label et <html lang>. */
export const langTag = (lang) => (lang === "en" ? "en-GB" : "fr-FR");
