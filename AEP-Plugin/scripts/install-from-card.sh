#!/usr/bin/env bash
# Offline install of the electroPioreactor plugin - and any other Pioreactor
# plugin staged alongside it - from a payload written to the microSD card's boot
# partition by scripts/stage-sd-card.sh.
#
# Run this ON THE PIOREACTOR, as the `pioreactor` user, after first boot:
#
#   bash /boot/firmware/electropioreactor/install.sh
#
# Needs no internet and no LAN. Re-running it is safe.
set -euo pipefail

PAYLOAD="${1:-/boot/firmware/electropioreactor}"
SRC="$PAYLOAD/AEP-Plugin"
WHEELS="$PAYLOAD/wheels"
VENV="${PIO_VENV:-/opt/pioreactor/venv}"
DOT="${DOT_PIOREACTOR:-$HOME/.pioreactor}"
PLUGINS="$DOT/plugins"
FORCE_PWM4="${EP_FORCE_PWM4:-}"
YAML_SRC="$SRC/pioreactor_electropioreactor_plugin/ui/contrib/jobs/electropioreactor.yaml"
YAML_DST="$PLUGINS/ui/jobs/20_electropioreactor.yaml"
WARNINGS=()

die() { echo "error: $*" >&2; exit 1; }

[ "$(id -un)" = "pioreactor" ] || die "run this as the pioreactor user, not with sudo (it sudos only for lighttpd)"
[ -d "$SRC" ]        || die "no payload at $SRC - was the card staged with stage-sd-card.sh?"
[ -f "$YAML_SRC" ]   || die "payload is incomplete: $YAML_SRC is missing"
[ -x "$VENV/bin/python" ] || die "no Pioreactor venv at $VENV - is this a Pioreactor image?"

shopt -s nullglob
WHEEL_LIST=("$WHEELS"/*.whl)
shopt -u nullglob

echo "==> Installing plugin code"
MODE=""
if [ ${#WHEEL_LIST[@]} -gt 0 ]; then
    # A wheel needs no build backend, which matters: the image's venv has no
    # setuptools, so building from source on the unit fails.
    if "$VENV/bin/pip" install --no-deps --no-index "${WHEEL_LIST[@]}" >/tmp/ep-pip.log 2>&1; then
        MODE=wheel
        rm -f "$PLUGINS/electropioreactor.py"
        for w in "${WHEEL_LIST[@]}"; do echo "    installed $(basename "$w")"; done
    else
        echo "    staged wheels would not install (see /tmp/ep-pip.log)"
        WARNINGS+=("the staged wheels would not install; see /tmp/ep-pip.log")
    fi
fi
if [ -z "$MODE" ] && "$VENV/bin/pip" install --no-deps --no-index --no-build-isolation "$SRC" >>/tmp/ep-pip.log 2>&1; then
    MODE=pip
    rm -f "$PLUGINS/electropioreactor.py"
    echo "    built and installed from the staged source"
fi
if [ -z "$MODE" ]; then
    MODE=folder
    echo "    pip could not build offline (see /tmp/ep-pip.log); using the plugins folder instead"
    mkdir -p "$PLUGINS"
    install -m 644 "$SRC/pioreactor_electropioreactor_plugin/electropioreactor.py" "$PLUGINS/electropioreactor.py"
    echo "    installed to $PLUGINS/electropioreactor.py"
    if [ ${#WHEEL_LIST[@]} -gt 1 ]; then
        WARNINGS+=("only this plugin was installed - the other staged wheels need a working pip install")
    fi
fi

echo "==> Deploying the UI job descriptor"
mkdir -p "$PLUGINS/ui/jobs"
install -m 644 "$YAML_SRC" "$YAML_DST"
chgrp www-data "$YAML_DST" 2>/dev/null || true
echo "    $YAML_DST"

# Anything else that came in on a wheel brings its own UI descriptors, its own
# config defaults and sometimes a post-install step. `pio plugins install` would
# do this over the network; offline, do it here.
SITE=$("$VENV/bin/python" -c 'import site; print(site.getsitepackages()[0])')
for pkg in "$SITE"/pioreactor_*_plugin; do
    name=$(basename "$pkg")
    [ "$name" = "pioreactor_electropioreactor_plugin" ] && continue
    echo "==> Setting up $name"
    for kind in jobs automations charts; do
        shopt -s nullglob
        for y in "$pkg/ui/contrib/$kind"/*.yaml; do
            mkdir -p "$PLUGINS/ui/$kind"
            install -m 644 "$y" "$PLUGINS/ui/$kind/$(basename "$y")"
            chgrp www-data "$PLUGINS/ui/$kind/$(basename "$y")" 2>/dev/null || true
            echo "    UI $kind: $(basename "$y")"
        done
        shopt -u nullglob
    done
    if [ -f "$pkg/additional_config.ini" ] && [ -f "$DOT/config.ini" ]; then
        "$VENV/bin/python" - "$pkg/additional_config.ini" "$DOT/config.ini" <<'PY'
import sys
from pioreactor.config import ConfigParserMod

src, dst = sys.argv[1], sys.argv[2]
incoming, current = ConfigParserMod(), ConfigParserMod()
incoming.read([src])
current.read([dst])

added = []
for section in incoming.sections():
    if section not in current:
        current.add_section(section)
    for key, value in incoming[section].items():
        if key not in current[section]:
            current[section][key] = value
            added.append(f"{section}.{key}")

if added:
    with open(dst, "w") as fh:
        current.write(fh)
print("    config.ini: added " + (", ".join(added) if added else "nothing new"))
PY
    fi
    if [ -f "$pkg/post_install.sh" ]; then
        PATH="$VENV/bin:$PATH" bash "$pkg/post_install.sh" 2>&1 | sed 's/^/    /' \
            || WARNINGS+=("$name's post_install.sh did not finish cleanly")
    fi
done

echo "==> Patching config.ini"
if [ ! -f "$DOT/config.ini" ]; then
    echo "    no $DOT/config.ini - this is a worker; the leader will send it its config. Skipping."
else
    PATCH_ARGS=()
    [ -n "$FORCE_PWM4" ] && PATCH_ARGS+=(--force)
    if ! "$VENV/bin/python" "$SRC/scripts/patch-config-ini.py" ${PATCH_ARGS+"${PATCH_ARGS[@]}"}; then
        WARNINGS+=("config.ini was NOT patched - see the message above. Re-run with EP_FORCE_PWM4=1 to take PWM 4 anyway.")
    fi
fi

echo "==> Restarting lighttpd"
sudo systemctl restart lighttpd

echo "==> Verifying"
PIO="$VENV/bin/pio"; command -v pio >/dev/null 2>&1 && PIO=pio
DOT_PIOREACTOR="$DOT" "$PIO" plugins list 2>/dev/null | grep -i electro || echo "    (pio plugins list showed nothing - check the UI's Plugins page)"
ls -l "$YAML_DST"
n=$(curl -s http://localhost/unit_api/jobs/descriptors 2>/dev/null | grep -c electropioreactor || true)
echo "    job descriptors served by the UI mentioning electropioreactor: ${n:-0} (expect 1 on a leader, 0 on a worker)"

echo
if [ ${#WARNINGS[@]} -gt 0 ]; then
    echo "Finished with ${#WARNINGS[@]} thing(s) to deal with (install mode: $MODE):"
    for w in "${WARNINGS[@]}"; do echo "  - $w"; done
    exit 1
fi
echo "Done (install mode: $MODE)."
echo "Hard-refresh http://$(hostname).local/ and look for electroPioreactor under Activities."
