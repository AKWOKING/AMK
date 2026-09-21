# -*- coding: utf-8 -*-
"""Assemble hosting/samples/ from site/ — the PUBLIC agency site + the
nameless templates (Nova / Little Oaks / Crestwood / Molyko Medical Centre)
plus named concepts built for a specific lead (e.g. /mitoc.html for Midas
Touch Optic Center; named previews are only sent to that lead).

Deploy rule (King, standing): this bundle goes INSIDE the existing
amk-cm.vercel.app project, never a separate Vercel project. King redeploys
the site/ folder; hosting/samples/ is the snapshot of the same files.
Shareable preview links afterwards:
  /sample-secondary.html  -> comprehensive / high / bilingual colleges
  /sample-school.html     -> general day schools (Nova)
  /sample-nursery.html    -> nursery/primary (Little Oaks)
  /sample-clinic.html     -> clinics & laboratories (Molyko Medical Centre)
  /mitoc.html             -> NAMED preview for Midas Touch Optic Center only
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
