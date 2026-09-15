# -*- coding: utf-8 -*-
"""15 Sep PM: King renamed the nameless clinic concept to
Bonabéri Medical Centre (Douala); canonical file is now
site/clinic-bonaberi.html (old sample-clinic.html removed)."""
import openpyxl

wb = openpyxl.load_workbook('leads/leads_50.xlsx')
ws = wb['Leads 50']
hdr = [c.value for c in ws[1]]
C = {h: i + 1 for i, h in enumerate(hdr)}

def upd(lid, **kw):
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, 1).value == lid:
            for k, v in kw.items():
                ws.cell(r, C[k if k in C else k.replace('_', ' ')]).value = v
            return r
    raise KeyError(lid)

def note(lid, text):
    r = upd(lid)
    c = ws.cell(r, C['Notes'])
    c.value = (c.value or '') + ' ' + text

upd(36, **{'Demo made': 'nameless clinic-bonaberi.html (Bonabéri Medical Centre, Douala; Forest palette; was Molyko Medical Centre/sample-clinic.html, renamed by King 15 Sep PM)'})
note(36, '| 15 Sep PM RENAME: live concept is /clinic-bonaberi.html (LIVE, partial hand-rename by King; canonical repo build fully renamed to Douala/BMC, redeploys with amk-site.zip). Solidarity (Buea) warm-yes link uses it with placeholder caption; ask King if he wants a Buea/city-neutral variant + matching mockup-clinic image.')

upd(37, **{'Demo made': 'YES named: site/mitoc.html (built 15 Sep, send after warm yes); LIVE at https://mitoc-concept.vercel.app'})

wb.save('leads/leads_50.xlsx')
print('xlsx patched: 36 rename, 37 demo pointer')
