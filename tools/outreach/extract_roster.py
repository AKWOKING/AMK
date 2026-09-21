import zipfile, re, json, sys

z = zipfile.ZipFile("leads/leads_50.xlsx")
x = z.read("xl/worksheets/sheet2.xml").decode("utf-8", errors="replace")
rows = re.findall(r"<row[^>]*>(.*?)</row>", x, re.S)

def cells(b):
    o = {}
    for m in re.finditer(r'<c[^>]*?(?:t="(\w+)")?[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>', b, re.S):
        col = re.search(r'r="([A-Z]+)\d+"', m.group(0))
        val = m.group(2) or m.group(3) or ""
        if col and val:
            o[col.group(1)] = val.replace("&amp;", "&").replace("&#10;", " ").replace("&gt;", ">").strip()
    return o

hdr = cells(rows[0])
recs = []
for b in rows[1:]:
    c = cells(b)
    if c:
        recs.append({hdr.get(k, k): c.get(k, "") for k in c})
json.dump(recs, open("/tmp/roster.json", "w"), ensure_ascii=False)
print("leads:", len(recs), file=sys.stderr)

want = {3, 4, 6, 7, 8, 9, 10, 14, 16, 19, 20, 21, 22, 24, 25, 26, 28, 29, 30, 33, 18, 36, 38, 27, 17, 23}
for rec in recs:
    raw = str(rec.get("ID", "")).strip()
    if not raw.isdigit():
        continue
    i = int(raw)
    if i not in want:
        continue
    print("[%2d] %-36s | TEL:%s | WA:%s | FB:%s" % (
        i, rec.get("School", "")[:36], rec.get("Phone", "")[:24] or "-",
        rec.get("WhatsApp", "")[:24] or "-", rec.get("Facebook", "")[:30] or "-"))
