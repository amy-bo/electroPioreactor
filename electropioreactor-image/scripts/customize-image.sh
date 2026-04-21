#!/usr/bin/env bash
# Customise a Pioreactor Raspberry Pi OS image to create the electroPioreactor image.
#
# Usage (run as root):
#   ./customize-image.sh <pioreactor-base.img> <output.img> [<plugin-source-dir>]
#
# If <plugin-source-dir> is given, the plugin is pip-installed from that local
# path (bind-mounted into the chroot). Otherwise the plugin is git-cloned from
# $PLUGIN_REPO at $PLUGIN_BRANCH inside the chroot (requires network there).
#
# Requirements:
#   apt install qemu-user-static binfmt-support util-linux mount

set -euo pipefail

BASE_IMG="${1:?Usage: $0 <base.img> <output.img> [plugin-source-dir]}"
OUT_IMG="${2:?Usage: $0 <base.img> <output.img> [plugin-source-dir]}"
PLUGIN_SRC="${3:-}"

PLUGIN_REPO="${PLUGIN_REPO:-https://github.com/amy-bo/electroPioreactor.git}"
PLUGIN_BRANCH="${PLUGIN_BRANCH:-AEP-Plugin}"
PIOREACTOR_HOME="/home/pioreactor/.pioreactor"
PIOREACTOR_VENV="/opt/pioreactor/venv"
CONFIG_SECTION="electropioreactor.config"

echo "==> Copying base image to $OUT_IMG"
cp --reflink=auto "$BASE_IMG" "$OUT_IMG"

# Pioreactor images may need a bit of free space for pip installs; grow by 500 MB.
echo "==> Growing image by 500 MB to leave room for plugin install"
dd if=/dev/zero bs=1M count=500 >> "$OUT_IMG" status=none
LOOP_DEV=$(losetup --find --show --partscan "$OUT_IMG")
# Expand partition 2 and its filesystem (best-effort — skip on failure)
parted -s "$LOOP_DEV" resizepart 2 100% || true
partprobe "$LOOP_DEV" || true
e2fsck -f -y "${LOOP_DEV}p2" || true
resize2fs "${LOOP_DEV}p2" || true

MOUNT_ROOT=$(mktemp -d)
MOUNT_BOOT=$(mktemp -d)
mount "${LOOP_DEV}p2" "$MOUNT_ROOT"
mount "${LOOP_DEV}p1" "$MOUNT_BOOT"
mount --bind /proc    "$MOUNT_ROOT/proc"
mount --bind /sys     "$MOUNT_ROOT/sys"
mount --bind /dev     "$MOUNT_ROOT/dev"
mount --bind /dev/pts "$MOUNT_ROOT/dev/pts"

# Bind-mount the local plugin source into the chroot so pip can install from it.
if [ -n "$PLUGIN_SRC" ]; then
  mkdir -p "$MOUNT_ROOT/tmp/plugin-src"
  mount --bind "$PLUGIN_SRC" "$MOUNT_ROOT/tmp/plugin-src"
fi

cp /usr/bin/qemu-arm-static      "$MOUNT_ROOT/usr/bin/" 2>/dev/null || true
cp /usr/bin/qemu-aarch64-static  "$MOUNT_ROOT/usr/bin/" 2>/dev/null || true

cleanup() {
    set +e
    [ -n "$PLUGIN_SRC" ] && umount -lf "$MOUNT_ROOT/tmp/plugin-src"
    umount -lf "$MOUNT_ROOT/dev/pts"
    umount -lf "$MOUNT_ROOT/dev"
    umount -lf "$MOUNT_ROOT/proc"
    umount -lf "$MOUNT_ROOT/sys"
    umount -lf "$MOUNT_BOOT"
    umount -lf "$MOUNT_ROOT"
    losetup -d "$LOOP_DEV"
    rm -rf "$MOUNT_ROOT" "$MOUNT_BOOT"
}
trap cleanup EXIT

chroot_run() {
    chroot "$MOUNT_ROOT" /bin/bash -c "$*"
}

echo "==> Installing plugin into Pioreactor venv"
if [ -n "$PLUGIN_SRC" ]; then
  chroot_run "
    set -euo pipefail
    ${PIOREACTOR_VENV}/bin/pip install --no-deps /tmp/plugin-src
  "
else
  chroot_run "
    set -euo pipefail
    apt-get update -qq
    apt-get install -y git
    rm -rf /tmp/electropioreactor-plugin
    git clone --depth 1 --branch ${PLUGIN_BRANCH} ${PLUGIN_REPO} /tmp/electropioreactor-plugin
    ${PIOREACTOR_VENV}/bin/pip install --no-deps /tmp/electropioreactor-plugin/AEP-Plugin
    rm -rf /tmp/electropioreactor-plugin
  "
fi

echo "==> Deploying UI YAML"
chroot_run "
  mkdir -p ${PIOREACTOR_HOME}/ui/contrib/jobs
  cp ${PIOREACTOR_VENV}/lib/python3.*/site-packages/pioreactor_electropioreactor_plugin/ui/contrib/jobs/electropioreactor.yaml \
     ${PIOREACTOR_HOME}/ui/contrib/jobs/20_electropioreactor.yaml
  chown pioreactor:pioreactor ${PIOREACTOR_HOME}/ui/contrib/jobs/20_electropioreactor.yaml
"

echo "==> Updating config.ini"
CONFIG_FILE="${MOUNT_ROOT}${PIOREACTOR_HOME}/config.ini"

python3 - <<PYEOF
import configparser
path = "${CONFIG_FILE}"
p = configparser.ConfigParser()
p.read(path)

if not p.has_section("PWM"):
    p.add_section("PWM")
p.set("PWM", "4", "relay")

if not p.has_section("${CONFIG_SECTION}"):
    p.add_section("${CONFIG_SECTION}")
p.set("${CONFIG_SECTION}", "electrolysis_power",      "2.5")
p.set("${CONFIG_SECTION}", "sparge_duration_seconds", "10.0")
p.set("${CONFIG_SECTION}", "sparge_interval_minutes", "60.0")

with open(path, "w") as fh:
    p.write(fh)
print("config.ini updated")
PYEOF

echo "==> Image customisation complete: $OUT_IMG"
