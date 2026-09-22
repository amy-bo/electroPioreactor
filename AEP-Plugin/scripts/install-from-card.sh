#!/usr/bin/env bash
# Offline install of the electroPioreactor plugin from a payload staged on the
# microSD card's boot partition by scripts/stage-sd-card.sh.
#
# Run this ON THE PIOREACTOR, as the `pioreactor` user, after first boot:
#
#   bash /boot/firmware/electropioreactor/install.sh
#
# Needs no internet and no LAN. Prefers a real pip install of the payload; falls
# back to Pioreactor's plugins-folder mechanism if pip cannot build offline.
set -euo pipefail

PAYLOAD="${1:-/boot/firmware/electropioreactor}"
SRC="$PAYLOAD/AEP-Plugin"
VENV="${PIO_VENV:-/opt/pioreactor/venv}"
DOT="${DOT_PIOREACTOR:-$HOME/.pioreactor}"
PLUGINS="$DOT/plugins"
YAML_SRC="$SRC/pioreactor_electropioreactor_plugin/ui/contrib/jobs/electropioreactor.yaml"
YAML_DST="$PLUGINS/ui/jobs/20_electropioreactor.yaml"

die() { echo "error: $*" >&2; exit 1; }

[ "$(id -un)" = "pioreactor" ] || die "run this as the pioreactor user, not with sudo (it sudos only for lighttpd)"
[ -d "$SRC" ]        || die "no payload at $SRC - was the card staged with stage-sd-card.sh?"
[ -f "$YAML_SRC" ]   || die "payload is incomplete: $YAML_SRC is missing"
[ -x "$VENV/bin/python" ] || die "no Pioreactor venv at $VENV - is this a Pioreactor image?"

echo "==> Installing the plugin's Python code"
if "$VENV/bin/pip" install --no-deps --no-index --no-build-isolation "$SRC" 2>/tmp/ep-pip.log; then
    MODE=pip
    # A pip install and a plugins-folder copy would both register the job.
    rm -f "$PLUGINS/electropioreactor.py"
    echo "    installed into the venv (pip)"
else
    MODE=folder
    echo "    pip could not build offline (see /tmp/ep-pip.log); using the plugins folder instead"
    mkdir -p "$PLUGINS"
    install -m 644 "$SRC/pioreactor_electropioreactor_plugin/electropioreactor.py" "$PLUGINS/electropioreactor.py"
    echo "    installed to $PLUGINS/electropioreactor.py"
fi

echo "==> Deploying the UI job descriptor"
mkdir -p "$PLUGINS/ui/jobs"
install -m 644 "$YAML_SRC" "$YAML_DST"
chgrp www-data "$YAML_DST" 2>/dev/null || true
echo "    $YAML_DST"

echo "==> Patching config.ini"
if [ -f "$DOT/config.ini" ]; then
    "$VENV/bin/python" "$SRC/scripts/patch-config-ini.py"
else
    echo "    no $DOT/config.ini - this is a worker; the leader will send it its config. Skipping."
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
echo "Done (install mode: $MODE)."
echo "Hard-refresh http://$(hostname).local/ and look for electroPioreactor under Activities."
