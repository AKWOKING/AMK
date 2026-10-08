# -*- coding: utf-8 -*-
"""bake_default_lang.py — écrit la langue par défaut DANS le HTML statique d'une page bilingue AMK.

    python3 tools/seo/bake_default_lang.py site/index.html fr          # applique
    python3 tools/seo/bake_default_lang.py site/index.html fr --dry    # compte seulement

POURQUOI (08/10/2026, amk-cm). Nos pages bilingues portent chaque texte en deux versions
(`data-en` / `data-fr`) et un petit JS qui réécrit `innerHTML` au clic sur EN|FR. Mais le HTML
SERVI au robot est celui d'avant le JS. Sur `amk-cm`, il était mélangé : `lang="en"`, 207 textes
en anglais, 36 en français (dont le H1), titre et description en français. Google lit la langue du
contenu, pas l'intention : une page à moitié anglaise ne se classe bien ni sur « création site web »
ni sur « website design ». Cet outil rend l'HTML statique cohérent avec la langue choisie ; le JS
reste intact (il remet l'autre langue au clic ou depuis `localStorage`).

CE QU'IL FAIT : pour chaque élément portant `data-en`+`data-fr` dont le contenu actuel est EXACTEMENT
le texte `data-en` (espaces et entités normalisés), remplace ce contenu par `data-fr` (ou
l'inverse pour `en`). Les éléments imbriqués dans un autre élément `data-en` sont ignorés (le JS
les écraserait de toute façon). Les éléments dont le contenu n'est NI l'un NI l'autre (icône SVG,
texte spécial) sont SIGNALÉS, jamais touchés.

CE QU'IL NE FAIT PAS : titre, meta, `lang`, boutons EN|FR, placeholders, alt, JSON-LD → à la main
(voir `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` §3). Aucune réécriture de texte :
il ne choisit que parmi les deux versions déjà écrites.
"""
import re, sys, html
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}


def _norm(x: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(x)).strip()


class _Scan(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.starts = [0]
        for m in re.finditer("\n", text):
            self.starts.append(m.end())
        self.stack = []      # (tag, start_abs, len_starttext, has_data_en, en, fr)
        self.found = []      # (inner_a, inner_b, en, fr, tag)

    def _abs(self):
        line, col = self.getpos()
        return self.starts[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        st = self.get_starttag_text()
        en = re.search(r'\sdata-en="([^"]*)"', st)
        fr = re.search(r'\sdata-fr="([^"]*)"', st)
        self.stack.append((tag, self._abs(), len(st), bool(en and fr),
                           en.group(1) if en else None, fr.group(1) if fr else None))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                t, a, ln, has, en, fr = self.stack[i]
                del self.stack[i:]
                if has and not any(s[3] for s in self.stack):
                    self.found.append((a + ln, self._abs(), en, fr, tag))
                return


def bake(text: str, lang: str):
    """text en LF. Retourne (nouveau_texte, remplacés, déjà_ok, signalés[])."""
    assert lang in ("fr", "en")
    p = _Scan(text)
    p.feed(text)
    p.close()
    done = same = 0
    flagged = []
    for a, b, en, fr, tag in sorted(p.found, reverse=True):
        inner = text[a:b]
        want, other = (fr, en) if lang == "fr" else (en, fr)
        if _norm(inner) == _norm(want):
            same += 1
        elif _norm(inner) == _norm(other):
            text = text[:a] + want + text[b:]
            done += 1
        else:
            flagged.append((tag, _norm(inner)[:70], _norm(en)[:50]))
    return text, done, same, flagged


if __name__ == "__main__":
    path, lang = sys.argv[1], sys.argv[2]
    raw = open(path, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    new, done, same, flagged = bake(t, lang)
    print(f"{path}: {done} texte(s) passés en {lang}, {same} déjà en {lang}, {len(flagged)} signalé(s)")
    for f in flagged:
        print("   SIGNALÉ (non touché) :", f)
    if "--dry" not in sys.argv:
        open(path, "w", encoding="utf-8", newline="").write(new.replace("\n", "\r\n") if crlf else new)
