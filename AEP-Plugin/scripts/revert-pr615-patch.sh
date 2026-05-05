#!/usr/bin/env bash
# Revert the PR #615 hot-patch by restoring the .pre-pr615.bak backup.
# Use this after upgrading to Pioreactor 26.4.5+ where PR #615 ships natively.
set -euo pipefail

PIO_STATIC=$(/opt/pioreactor/venv/bin/python -c "import pioreactor.web, os; print(os.path.join(os.path.dirname(pioreactor.web.__file__), 'static'))")

if [ ! -d "${PIO_STATIC}.pre-pr615.bak" ]; then
  echo "No backup found at ${PIO_STATIC}.pre-pr615.bak; nothing to revert." >&2
  exit 1
fi

echo "Restoring $PIO_STATIC from ${PIO_STATIC}.pre-pr615.bak"
sudo rm -rf "$PIO_STATIC"
sudo mv "${PIO_STATIC}.pre-pr615.bak" "$PIO_STATIC"
sudo systemctl restart lighttpd

echo "Reverted. lighttpd restarted."
