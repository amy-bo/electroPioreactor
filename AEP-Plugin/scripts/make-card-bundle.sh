#!/usr/bin/env bash
# Build the electroPioreactor card bundle: a zip whose contents are dragged onto
# the bootfs drive of a freshly flashed Pioreactor microSD card.
#
#   electroPioreactor-card-bundle.zip
#   └── pioreactor/
#       └── plugins/
#           ├── pioreactor_electropioreactor_plugin-<version>-py3-none-any.whl
#           └── README.txt
#
# Pioreactor images with boot-partition plugin support install every wheel in
# bootfs/pioreactor/plugins/ on first boot (leader) or when the unit is added
# to a cluster (worker). Dependency wheels can be dropped in the same folder;
# this plugin needs none beyond what the Pioreactor image already ships.
#
# Usage: bash scripts/make-card-bundle.sh            (from AEP-Plugin/)
# Output: dist/electroPioreactor-card-bundle.zip
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

BUILD=build/card-bundle
DIST=dist
rm -rf "$BUILD"
mkdir -p "$BUILD/pioreactor/plugins" "$DIST"

python3 -m pip wheel --no-deps --wheel-dir "$BUILD/pioreactor/plugins" . >/dev/null

WHEEL=$(find "$BUILD/pioreactor/plugins" -name 'pioreactor_electropioreactor_plugin-*.whl' | head -n 1)
[ -n "$WHEEL" ] || { echo "error: wheel was not built" >&2; exit 1; }

cat > "$BUILD/pioreactor/plugins/README.txt" <<'TXT'
electroPioreactor plugin, staged for install from the microSD card.

Drag the "pioreactor" folder (the one containing this file's parent
"plugins" folder) onto the "bootfs" drive of a freshly flashed Pioreactor
microSD card, eject the card, and boot the Pioreactor. The plugin installs
itself on first boot and this folder is cleared from the card.

If the plugin does not appear in the Pioreactor web interface, put the card
back in your PC: a failed install leaves the wheel and a .log file in
pioreactor/plugins/failed/ on this drive.

Full instructions: https://github.com/amy-bo/electroPioreactor/tree/main/AEP-Plugin#installation
TXT

OUT=$DIST/electroPioreactor-card-bundle.zip
rm -f "$OUT"
(cd "$BUILD" && zip -q -r "../../$OUT" pioreactor)
echo "Built $OUT containing $(basename "$WHEEL")"
