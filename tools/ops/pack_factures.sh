#!/usr/bin/env bash
# pack_factures.sh — refabriquer l'archive de l'outil de factures, et prouver qu'elle est identique.
#
# L'archive `amk-factures-pwa-v2.zip` (88 Ko, l'outil de factures livré) a quitté l'arbre le 24/10
# parce qu'elle se **refait à l'identique** depuis `ops/amk-factures-pwa/`, qui reste versionné. Ce
# script est la preuve : il reconstruit le zip, calcule l'empreinte de contenu et la compare à celle
# inscrite dans `ops/LIVRAISONS.md`.
#
# L'empreinte de contenu n'est pas le sha256 du zip (un zip embarque des dates, donc deux zips du même
# contenu diffèrent) : c'est le sha256 de la liste triée « sha256  nom » des six fichiers. C'est ce qui
# permet de dire « c'est le même livrable » sans dépendre de l'horloge.
#
#   bash tools/ops/pack_factures.sh                 # reconstruit et vérifie
#   bash tools/ops/pack_factures.sh --out /tmp/x.zip
#
# Sortie par défaut : /tmp/amk-factures-pwa-<date>.zip — JAMAIS dans l'arbre (c'est tout l'objet du
# chantier ② : un livrable ne rentre plus dans le dépôt).

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

SRC="ops/amk-factures-pwa"
REGISTRE="ops/LIVRAISONS.md"
FILES=(index.html manifest.json sw.js icon-192.png icon-512.png apple-touch-icon.png)
OUT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "option inconnue : $1" >&2; exit 1 ;;
  esac
done
[ -n "$OUT" ] || OUT="/tmp/amk-factures-pwa-$(date +%F).zip"

[ -d "$SRC" ] || { echo "⛔ source absente : $SRC" >&2; exit 1; }
for f in "${FILES[@]}"; do
  [ -f "$SRC/$f" ] || { echo "⛔ fichier manquant dans la source : $SRC/$f" >&2; exit 1; }
done

DIGEST=$(cd "$SRC" && sha256sum "${FILES[@]}" | sort -k2 | sha256sum | cut -d' ' -f1)
# la ligne du registre qui nomme CE script — pas « la première empreinte du fichier », qui changerait
# de sens dès qu'une livraison s'ajoute au-dessus.
# `grep -o '[0-9a-f]\{64\}'` et pas `tr -dc '0-9a-f'` : ce dernier laissait passer « de » de « digest ».
ATTENDU=$(grep 'pack_factures.sh' "$REGISTRE" 2>/dev/null | grep -o '[0-9a-f]\{64\}' | head -1 || true)

rm -f "$OUT"
( cd "$SRC" && zip -q -X "$OUT" "${FILES[@]}" )

echo ""
echo "ARCHIVE    $OUT"
echo "  taille   $(du -h "$OUT" | cut -f1) ($(wc -c < "$OUT") octets)"
echo "  contenu  ${#FILES[@]} fichiers · digest $DIGEST"
if [ -n "$ATTENDU" ] && [ "$DIGEST" = "$ATTENDU" ]; then
  echo "  verdict  ✓ identique au livrable enregistré dans $REGISTRE"
  exit 0
elif [ -n "$ATTENDU" ]; then
  echo "  verdict  ⛔ DIFFÉRENT du livrable enregistré ($ATTENDU)"
  echo "           soit la source a changé (nouvelle version à livrer), soit un fichier a bougé."
  exit 3
else
  echo "  verdict  ⚠ aucune empreinte enregistrée dans $REGISTRE — rien à comparer"
  exit 0
fi
