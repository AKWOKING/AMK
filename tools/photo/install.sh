#!/usr/bin/env bash
# AMK photo prep — installe la chaîne locale de détourage/correction photo.
# Idempotent. Deux chemins pour le modèle ONNX (jamais commité, ~88 Mo) :
#   1. npm @imgly/background-removal-node : le modèle ISNet voyage DANS le
#      paquet npm (chunks), donc il passe même l'egress restreint de la sandbox.
#   2. Repli internet normal : `rembg d u2net` (rembg MIT, poids u2net Apache-2.0).
# Usage : bash tools/photo/install.sh [--smoke]
set -euo pipefail

VENV="$HOME/.venv-amk"
MODEL_DIR="$HOME/.rembg/models/manual"
MODEL="$MODEL_DIR/imgly-medium.onnx"
PY="$VENV/bin/python"

echo "== 1/3 Environnement Python ($VENV) =="
[ -x "$PY" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q pillow "rembg[cpu,cli]"
"$PY" -c "import PIL, onnxruntime; print('Pillow', PIL.__version__, '| onnxruntime', onnxruntime.__version__)"

echo "== 2/3 Modèle de détourage =="
if [ -f "$MODEL" ]; then
  echo "Modèle déjà présent : $MODEL"
else
  mkdir -p "$MODEL_DIR"
  if command -v npm >/dev/null 2>&1; then
    TMP="$(mktemp -d)"
    ( cd "$TMP" && npm init -y >/dev/null 2>&1 \
      && npm i --ignore-scripts @imgly/background-removal-node >/dev/null 2>&1 )
    "$PY" - "$TMP/node_modules/@imgly/background-removal-node/dist" "$MODEL" <<'PYEOF'
import hashlib, json, sys
from pathlib import Path
dist, dst = Path(sys.argv[1]), Path(sys.argv[2])
res = json.loads((dist / "resources.json").read_text())
chunks = sorted(res["/models/medium"]["chunks"], key=lambda c: c["offsets"][0])
with dst.open("wb") as f:
    for c in chunks:
        data = (dist / c["hash"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == c["hash"], "hash mismatch"
        f.write(data)
print(f"Modèle reconstruit : {dst} ({dst.stat().st_size/1e6:.1f} Mo)")
PYEOF
    rm -rf "$TMP"
  else
    echo "npm absent — repli rembg (internet normal requis) :"
    "$VENV/bin/rembg" d u2net
  fi
fi

echo "== 3/3 Vérification =="
"$PY" - <<'PYEOF'
import glob
import onnxruntime as ort
paths = glob.glob(f"{__import__('os').path.expanduser('~')}/.rembg/models/manual/*.onnx") \
      + glob.glob(f"{__import__('os').path.expanduser('~')}/.rembg/models/u2net/*.onnx")
assert paths, "aucun modèle"
s = ort.InferenceSession(paths[0], providers=["CPUExecutionProvider"])
i = s.get_inputs()[0]
print("Modèle OK :", paths[0].rsplit("/", 1)[-1], "entrée", i.shape)
PYEOF

if [ "${1:-}" = "--smoke" ]; then
  SMOKE="$(mktemp -d)"
  "$PY" - "$SMOKE" <<'PYEOF'
import sys
from PIL import Image, ImageDraw
img = Image.new("RGB", (600, 450), (210, 205, 195))
d = ImageDraw.Draw(img)
d.rectangle([120, 180, 480, 300], outline=(30, 30, 30), width=14)
d.line([120, 200, 60, 170], fill=(30, 30, 30), width=12)
d.line([480, 200, 540, 170], fill=(30, 30, 30), width=12)
img.save(f"{sys.argv[1]}/smoke-monture.png")
PYEOF
  "$PY" "$(dirname "$0")/prep.py" "$SMOKE/smoke-monture.png" -o "$SMOKE/out" --mode catalogue
  test -f "$SMOKE/out/smoke-monture-catalogue.jpg" && echo "SMOKE OK"
  rm -rf "$SMOKE"
fi
echo "Prêt : $PY tools/photo/prep.py --help"
