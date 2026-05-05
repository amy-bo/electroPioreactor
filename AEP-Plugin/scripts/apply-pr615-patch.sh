#!/usr/bin/env bash
# Apply Pioreactor PR #615 frontend hot-patch from the bundled tarball.
# Required on Pioreactor 26.4.4 and earlier; no-op once 26.4.5+ ships.
set -euo pipefail

PIO_STATIC=$(/opt/pioreactor/venv/bin/python -c "import pioreactor.web, os; print(os.path.join(os.path.dirname(pioreactor.web.__file__), 'static'))")
TARBALL="$(dirname "$(realpath "$0")")/../transitional/pioreactor-static-pr615.tar.gz"

if [ ! -f "$TARBALL" ]; then
  echo "Tarball not found at $TARBALL" >&2
  exit 1
fi

if [ -e "${PIO_STATIC}.pre-pr615.bak" ]; then
  echo "Backup already exists at ${PIO_STATIC}.pre-pr615.bak, leaving it (it preserves the original)."
else
  echo "Backing up $PIO_STATIC -> ${PIO_STATIC}.pre-pr615.bak"
  sudo cp -a "$PIO_STATIC" "${PIO_STATIC}.pre-pr615.bak"
fi

echo "Replacing $PIO_STATIC with PR #615 bundle"
sudo rm -rf "$PIO_STATIC"
sudo tar -xzf "$TARBALL" -C "$(dirname "$PIO_STATIC")"
sudo chown -R pioreactor:pioreactor "$PIO_STATIC"

echo "Done. Run 'sudo systemctl restart lighttpd' after step 6."
