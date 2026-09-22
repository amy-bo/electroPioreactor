#!/usr/bin/env bash
# Stage an offline electroPioreactor install onto a freshly-imaged microSD card.
#
# Run this ON YOUR MAC, from the repo, with the card still in the card reader
# after Raspberry Pi Imager has finished - before the card goes into the Pi:
#
#   bash AEP-Plugin/scripts/stage-sd-card.sh [BOOT_VOLUME] [COUNTRY_CODE]
#
# BOOT_VOLUME defaults to /Volumes/bootfs (or /Volumes/boot). COUNTRY_CODE is
# the two-letter WiFi country for the Pioreactor's own access point, e.g. GB;
# pass it to create the `local_access_point` file, or drop the file downloaded
# from https://docs.pioreactor.com/user-guide/local-access-point yourself.
#
# Imager ejects the card when it finishes. Pull it out and push it back in -
# the boot partition remounts read-write, and nothing is rewritten.
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
SRC="$REPO_ROOT/AEP-Plugin"
CARD="${1:-}"
COUNTRY="${2:-}"

die() { echo "error: $*" >&2; exit 1; }

if [ -z "$CARD" ]; then
    for candidate in /Volumes/bootfs /Volumes/boot; do
        [ -d "$candidate" ] && CARD="$candidate" && break
    done
fi
[ -n "$CARD" ] || die "no boot partition mounted. Re-insert the card, then pass its path (e.g. /Volumes/bootfs)"
[ -d "$CARD" ] || die "$CARD is not mounted"
[ -f "$CARD/config.txt" ] || die "$CARD has no config.txt - that is not a Raspberry Pi boot partition"
[ -d "$SRC/pioreactor_electropioreactor_plugin" ] || die "no plugin source at $SRC"

DEST="$CARD/electropioreactor"
echo "==> Staging the plugin payload to $DEST"
rm -rf "$DEST"
mkdir -p "$DEST/AEP-Plugin"
cp -R "$SRC/pioreactor_electropioreactor_plugin" "$DEST/AEP-Plugin/"
find "$DEST/AEP-Plugin" -name '__pycache__' -type d -prune -exec rm -rf {} +
find "$DEST/AEP-Plugin" -name '*.pyc' -delete
find "$DEST/AEP-Plugin" -name '.DS_Store' -delete
mkdir -p "$DEST/AEP-Plugin/scripts"
cp "$SRC/scripts/patch-config-ini.py" "$DEST/AEP-Plugin/scripts/"
for f in setup.py MANIFEST.in README.md LICENSE.txt; do
    [ -f "$SRC/$f" ] && cp "$SRC/$f" "$DEST/AEP-Plugin/"
done
cp "$SRC/scripts/install-from-card.sh" "$DEST/install.sh"

echo "==> Checking the local access point file"
if [ -f "$CARD/local_access_point" ]; then
    echo "    present: $CARD/local_access_point ($(cat "$CARD/local_access_point"))"
elif [ -n "$COUNTRY" ]; then
    [[ "$COUNTRY" =~ ^[A-Z][A-Z]$ ]] || die "COUNTRY_CODE must be two capital letters, e.g. GB"
    printf '%s' "$COUNTRY" > "$CARD/local_access_point"
    echo "    created: $CARD/local_access_point ($COUNTRY)"
else
    echo "    MISSING. Without it the Pioreactor will not raise its own WiFi, and with"
    echo "    no LAN you will have no way in. Re-run with a country code:"
    echo "        bash AEP-Plugin/scripts/stage-sd-card.sh $CARD GB"
    echo "    (or download the file from https://docs.pioreactor.com/user-guide/local-access-point)"
fi

echo "==> Flushing writes"
sync

cat <<EOF

Staged. Next:
  1. Eject the card (Finder, or: diskutil eject "$CARD"), put it in the Pi, power up.
  2. Wait for first boot, then join the WiFi network "pioreactor" (password: raspberry).
  3. ssh pioreactor@<hostname>.local
  4. bash /boot/firmware/electropioreactor/install.sh
EOF
