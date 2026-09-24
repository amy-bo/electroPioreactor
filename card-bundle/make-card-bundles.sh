#!/usr/bin/env bash
# Build the two card bundles: the files dragged onto the bootfs drive of a
# freshly flashed Pioreactor microSD card. Needs internet on this computer.
#
#   electroPioreactor-AEP-card-bundle.zip   AEP0.2: electroPioreactor + precision temperature + XR profile
#   electroPioreactor-MEP-card-bundle.zip   MEP: electroPioreactor only
#   each: pioreactor/plugins/*.whl + README.txt, and local_access_point (hotspot units only)
#
# Usage: bash card-bundle/make-card-bundles.sh      (from the repository root)
# Output: dist/*.zip
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

BUILD=build/card-bundles
DIST=dist
WHEELS=$BUILD/wheels
rm -rf "$BUILD"
mkdir -p "$WHEELS" "$DIST"

python3 -m pip wheel --no-deps --wheel-dir "$WHEELS" ./AEP-Plugin >/dev/null
python3 -m pip wheel --no-deps --wheel-dir "$WHEELS" ./card-bundle >/dev/null
python3 -m pip download --no-deps --only-binary :all: --python-version 3.13 --dest "$WHEELS" pioreactor-precision-temperature-plugin >/dev/null

readme() {
cat <<TXT
$1 plugins, staged for install from the microSD card.

Drag the "pioreactor" folder onto the "bootfs" drive of a freshly flashed
Pioreactor microSD card, eject the card, and boot. The plugins install
themselves on first boot and this folder is cleared from the card.

If a plugin does not appear in the Pioreactor web interface, put the card
back in your computer: a failed install leaves the wheel and a .log file in
pioreactor/plugins/failed/ on this drive.

Full instructions: https://github.com/amy-bo/electroPioreactor/tree/main/AEP-Plugin#installation
TXT
}

bundle() {
    # $1 kit name, then wheel filename patterns
    local kit=$1; shift
    local dir=$BUILD/$kit
    mkdir -p "$dir/pioreactor/plugins"
    for pattern in "$@"; do cp "$WHEELS"/$pattern "$dir/pioreactor/plugins/"; done
    readme "$kit" > "$dir/pioreactor/plugins/README.txt"
    printf 'GB' > "$dir/local_access_point"
    local out=$DIST/electroPioreactor-$kit-card-bundle.zip
    rm -f "$out"
    (cd "$dir" && zip -q -r "../../../$out" pioreactor local_access_point)
    echo "Built $out:"
    unzip -l "$out" | grep -v "^Archive"
}

bundle AEP 'pioreactor_electropioreactor_plugin-*.whl' 'pioreactor_precision_temperature_plugin-*.whl' 'aep02_profile-*.whl'
bundle MEP 'pioreactor_electropioreactor_plugin-*.whl'
