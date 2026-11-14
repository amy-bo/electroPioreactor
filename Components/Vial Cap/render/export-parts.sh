#!/usr/bin/env bash
# Export every Vial Cap component to a binary STL (one per material group).
# Usage: ./export-parts.sh [outdir]      (default ./parts)
# Env:   OPENSCAD=/path/to/openscad  to override the binary; JOBS=n for parallelism.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
scad="$here/../Vial Cap render.scad"
out="${1:-./parts}"
components="cap septum cathode anode needles hubs screws washers glass flea thermal_pad pcb pcb_copper pcb_parts led led_die led_legs pd pd_die pd_board beam"

mac_app="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
if [ -n "${OPENSCAD:-}" ]; then
  bin="$OPENSCAD"
elif command -v openscad >/dev/null 2>&1; then
  bin="openscad"
elif [ -x "$mac_app" ]; then
  bin="$mac_app"
else
  echo "error: OpenSCAD not found. Install it, or set OPENSCAD=/path/to/binary" >&2
  exit 1
fi
[ -f "$scad" ] || { echo "error: missing $scad" >&2; exit 1; }

extra=()
if "$bin" --help 2>&1 | grep -q -- '--backend'; then
  extra+=(--backend=manifold)
fi

mkdir -p "$out"
out="$(cd "$out" && pwd)"
jobs="${JOBS:-$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)}"

export bin scad out
export EXTRA="${extra[*]:-}"

export_one() {
  c="$1"
  f="$out/$c.stl"
  rm -f "$f"
  # shellcheck disable=SC2086
  if ! "$bin" $EXTRA -o "$f" --export-format=binstl -D "component=\"$c\"" "$scad" >"$out/$c.log" 2>&1; then
    echo "FAILED: $c (see $out/$c.log)" >&2
    exit 1
  fi
  if [ ! -s "$f" ]; then
    echo "FAILED: $c produced an empty STL (see $out/$c.log)" >&2
    exit 1
  fi
  echo "ok: $c"
}
export -f export_one

echo "Using: $bin ${extra[*]:-} ; $jobs parallel jobs ; output: $out"
# shellcheck disable=SC2086
# shellcheck disable=SC2016
if ! printf '%s\n' $components | xargs -P "$jobs" -I{} bash -c 'export_one "$1"' _ {}; then
  echo "error: one or more exports failed" >&2
  exit 1
fi

# Final check: every component present and non-empty.
for c in $components; do
  [ -s "$out/$c.stl" ] || { echo "error: $c.stl missing or empty" >&2; exit 1; }
done
echo "All $(echo "$components" | wc -w | tr -d ' ') parts exported to $out"
