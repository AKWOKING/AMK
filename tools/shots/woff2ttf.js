// Minimal WOFF1 -> TTF decoder (WOFF = sfnt with optionally zlib-compressed tables).
const fs = require("fs");
const zlib = require("zlib");
const path = require("path");

function decode(woffBuf) {
  if (woffBuf.toString("ascii", 0, 4) !== "wOFF") throw new Error("not woff");
  const flavor = woffBuf.readUInt32BE(4);
  const numTables = woffBuf.readUInt16BE(12);
  const dir = [];
  let p = 44;
  for (let i = 0; i < numTables; i++) {
    const tag = woffBuf.toString("ascii", p, p + 4);
    const offset = woffBuf.readUInt32BE(p + 4);
    const compLength = woffBuf.readUInt32BE(p + 8);
    const origLength = woffBuf.readUInt32BE(p + 12);
    const origChecksum = woffBuf.readUInt32BE(p + 16);
    p += 20;
    let data = woffBuf.subarray(offset, offset + compLength);
    if (compLength !== origLength) data = zlib.inflateSync(data);
    dir.push({ tag, data, origLength, origChecksum });
  }
  const entrySelector = Math.floor(Math.log2(numTables));
  const searchRange = Math.pow(2, entrySelector) * 16;
  const rangeShift = numTables * 16 - searchRange;
  const header = Buffer.alloc(12);
  header.writeUInt32BE(flavor, 0);
  header.writeUInt16BE(numTables, 4);
  header.writeUInt16BE(searchRange, 6);
  header.writeUInt16BE(entrySelector, 8);
  header.writeUInt16BE(rangeShift, 10);
  const records = Buffer.alloc(16 * numTables);
  let offset = 12 + 16 * numTables;
  const tableBufs = [];
  // sfnt requires tables sorted by tag
  dir.sort((a, b) => (a.tag < b.tag ? -1 : 1));
  dir.forEach((t, i) => {
    records.write(t.tag, i * 16, 4, "ascii");
    records.writeUInt32BE(t.origChecksum, i * 16 + 4);
    records.writeUInt32BE(offset, i * 16 + 8);
    records.writeUInt32BE(t.origLength, i * 16 + 12);
    let data = t.data;
    tableBufs.push(data);
    offset += data.length;
    const pad = (4 - (data.length % 4)) % 4;
    if (pad) tableBufs.push(Buffer.alloc(pad));
    offset += pad;
  });
  return Buffer.concat([header, records, ...tableBufs]);
}

const srcDir = process.argv[2];
const outDir = process.argv[3];
fs.mkdirSync(outDir, { recursive: true });
for (const f of fs.readdirSync(srcDir).filter((x) => x.endsWith(".woff"))) {
  const ttf = decode(fs.readFileSync(path.join(srcDir, f)));
  const out = path.join(outDir, f.replace(/\.woff$/, ".ttf"));
  fs.writeFileSync(out, ttf);
  console.log(out, ttf.length);
}
