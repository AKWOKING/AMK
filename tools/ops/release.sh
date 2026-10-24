#!/usr/bin/env bash
# release.sh — sortir un livrable de l'arbre et le poser dans une Release GitHub.
#
# Un livrable (zip, pdf, docx final) ne sert qu'une fois — le jour où on le remet — et pèse ensuite
# pour toujours dans chaque clone. Une Release garde le fichier, daté, avec son empreinte, sans
# compter dans la taille du dépôt (2 Go par fichier, illimité en nombre).
#
# Ce script ne supprime rien de lui-même : il publie, il VÉRIFIE par un aller-retour réel
# (téléchargement + sha256), puis il affiche les deux commandes exactes pour sortir le fichier de
# l'arbre et l'inscrire au registre. Le geste destructeur reste humain, daté et commité.
#
#   bash tools/ops/release.sh --tag livraison-dmoptic-2026-10-21 \
#        --file dmopticsarl-2026-10-21.zip \
#        --title "Site DM Optic — archive livrée le 21/10" \
#        --notes "182 entrées, 4,8 Mo. Reconstruire : python3 demos/pack_dmoptic.py"
#
# Options :
#   --tag <tag>        obligatoire · minuscules, chiffres, points, tirets
#   --file <chemin>    obligatoire · fichier à publier (suivi par git de préférence)
#   --title <texte>    défaut : le tag
#   --notes <texte>    défaut : « Livrable du <date> — <fichier>, <taille>, sha256 <empreinte> »
#   --target <ref>     défaut : main · le commit sur lequel le tag est créé
#   --dry-run          affiche ce qui serait fait, ne publie rien
#   --allow-untracked  accepte un fichier non suivi par git (par défaut, on refuse : on ne publie
#                      pas ce qu'on ne sait pas reproduire)
#
# Codes retour : 0 publié et vérifié · 1 erreur · 2 rien à faire (déjà publié à l'identique)

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

TAG=""; FILE=""; TITLE=""; NOTES=""; TARGET="main"; DRY=0; ALLOW_UNTRACKED=0

die() { printf '\033[31m⛔ %s\033[0m\n' "$*" >&2; exit 1; }
say() { printf '%s\n' "$*"; }
ok()  { printf '\033[32m✓\033[0m %s\n' "$*"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --tag) TAG="${2:-}"; shift 2 ;;
    --file) FILE="${2:-}"; shift 2 ;;
    --title) TITLE="${2:-}"; shift 2 ;;
    --notes) NOTES="${2:-}"; shift 2 ;;
    --target) TARGET="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --allow-untracked) ALLOW_UNTRACKED=1; shift ;;
    -h|--help) sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "option inconnue : $1" ;;
  esac
done

[ -n "$TAG" ]  || die "--tag obligatoire"
[ -n "$FILE" ] || die "--file obligatoire"
printf '%s' "$TAG" | grep -Eq '^[a-z0-9][a-z0-9._-]*$' || die "tag invalide « $TAG » (minuscules, chiffres, . _ -)"
[ -f "$FILE" ] || die "fichier introuvable : $FILE"
command -v gh >/dev/null || die "gh absent — la Release se publie avec gh"
gh auth status >/dev/null 2>&1 || die "gh non authentifié — gh auth login"

# ── 0 · les deux hôtes de GitHub, et ils ne sont pas les mêmes
# `api.github.com` crée la release ; `uploads.github.com` reçoit le fichier. Le 24/10, dans un
# environnement dont le pare-feu n'autorisait que le premier, `gh` a répondu « EOF » — un message qui
# ne dit rien. On teste l'hôte d'upload AVANT de créer quoi que ce soit : une release à moitié faite
# n'est pas une livraison.
if ! curl -sS -o /dev/null -m 10 https://uploads.github.com/ 2>/dev/null; then
  if ! curl -sS -o /dev/null -m 10 -w '' https://uploads.github.com/ 2>&1 | grep -qi 'http'; then
    die "uploads.github.com injoignable depuis cette machine — la release et son fichier ne peuvent pas être publiés ici. Relancer depuis une machine qui joint cet hôte. (api.github.com répond, ce n'est pas l'authentification.)"
  fi
fi

NAME="$(basename "$FILE")"
SIZE=$(wc -c < "$FILE")
HUMAN=$(du -h "$FILE" | cut -f1)
SHA=$(sha256sum "$FILE" | cut -d' ' -f1)
TODAY=$(date +%F)

# ── 1 · on ne publie que ce qu'on sait reproduire
if git ls-files --error-unmatch "$FILE" >/dev/null 2>&1; then
  TRACKED="suivi par git"
elif [ "$ALLOW_UNTRACKED" -eq 1 ]; then
  TRACKED="NON suivi (accepté par --allow-untracked)"
else
  die "$NAME n'est pas suivi par git — un livrable doit venir d'une source versionnée (ou --allow-untracked en connaissance de cause)"
fi

say ""
say "LIVRABLE   $NAME"
say "  taille   $HUMAN ($SIZE octets)"
say "  sha256   $SHA"
say "  source   $TRACKED"
say "  tag      $TAG  →  $TARGET"

# ── 2 · la release existe-t-elle déjà, et à l'identique ?
EXISTING_SHA=""
if gh release view "$TAG" >/dev/null 2>&1; then
  say "  état     release $TAG déjà présente"
  TMPD=$(mktemp -d)
  if gh release download "$TAG" -p "$NAME" -D "$TMPD" >/dev/null 2>&1; then
    EXISTING_SHA=$(sha256sum "$TMPD/$NAME" | cut -d' ' -f1)
    say "  déjà là  $EXISTING_SHA"
  fi
  rm -rf "$TMPD"
  if [ "$EXISTING_SHA" = "$SHA" ]; then
    ok "rien à faire : $NAME est déjà publié à l'identique"
    exit 2
  fi
  say "  action   remplacement de l'asset (--clobber)"
else
  say "  état     release $TAG à créer"
fi

if [ -z "$TITLE" ]; then TITLE="$TAG"; fi
if [ -z "$NOTES" ]; then
  NOTES="Livrable du $TODAY — $NAME, $HUMAN, sha256 \`$SHA\`."
fi

if [ "$DRY" -eq 1 ]; then
  say ""
  say "── dry-run : aucune écriture sur GitHub"
  exit 0
fi

# ── 3 · publication
if gh release view "$TAG" >/dev/null 2>&1; then
  gh release upload "$TAG" "$FILE" --clobber
else
  gh release create "$TAG" "$FILE" --target "$TARGET" --title "$TITLE" --notes "$NOTES"
fi

# ── 4 · l'aller-retour : on retélécharge ce que GitHub dit avoir reçu
TMPD=$(mktemp -d)
gh release download "$TAG" -p "$NAME" -D "$TMPD" >/dev/null || { rm -rf "$TMPD"; die "asset introuvable au téléchargement — publication à moitié faite"; }
GOT_SIZE=$(wc -c < "$TMPD/$NAME")
GOT_SHA=$(sha256sum "$TMPD/$NAME" | cut -d' ' -f1)
URL=$(gh release view "$TAG" --json url --jq .url)
rm -rf "$TMPD"

[ "$GOT_SIZE" = "$SIZE" ] || die "taille différente après aller-retour ($GOT_SIZE ≠ $SIZE)"
[ "$GOT_SHA" = "$SHA" ]   || die "empreinte différente après aller-retour ($GOT_SHA ≠ $SHA)"
ok "publié et vérifié par aller-retour — $URL"

# ── 5 · ce qu'il reste à faire, à la main
say ""
say "── À FAIRE, dans cet ordre (rien n'a été supprimé)"
say ""
say "   1. inscrire la ligne au registre :  ops/LIVRAISONS.md"
say "      | $TODAY | \`$TAG\` | \`$NAME\` | $HUMAN | \`${SHA:0:12}…\` | $URL |"
say ""
say "   2. sortir le fichier de l'arbre (le fichier reste téléchargeable par la Release) :"
say "      git rm --cached \"$FILE\"        # garde la copie locale"
say ""
say "   3. noter OÙ le refabriquer (build-notes.md du client, ou le script qui le produit)."
say ""
