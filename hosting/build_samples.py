# -*- coding: utf-8 -*-
"""Assemble hosting/samples/ from site/ — the PUBLIC agency site + nameless
templates (Nova / Little Oaks / Crestwood). Unlike hosting/previews/, this
bundle is meant to be indexable: it is the public face + the generic preview
links used in cold outreach (never send a named concept to a different lead).

Deploy as its own Vercel project (e.g. amk-web), root dir = hosting/samples.
Shareable preview links afterwards:
  /sample-secondary.html  -> comprehensive / high / bilingual colleges
  /sample-school.html     -> general day schools (Nova)
  /sample-nursery.html    -> nursery/primary (Little Oaks)
"""
import pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "site"
OUT = ROOT / "hosting" / "samples"

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
print("copied", SRC, "->", OUT)
for p in sorted(OUT.rglob("*")):
    if p.is_file():
        print("  ", p.relative_to(OUT))
