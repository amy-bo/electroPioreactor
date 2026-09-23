#!/usr/bin/env bash
# Refresh site/vendor/*.tgz from a docsandeye checkout (Docs&I is not on npm yet).
#   bash scripts/vendor-docsandeye.sh /path/to/docsandeye
# Builds the four packages there, packs them into site/vendor/, then reinstalls.
set -euo pipefail
SRC="${1:?usage: bash scripts/vendor-docsandeye.sh /path/to/docsandeye}"
SITE="$(cd "$(dirname "$0")/.." && pwd)"
(cd "$SRC" && npm run build >/dev/null)
rm -f "$SITE"/vendor/*.tgz
for p in core themes starlight-docsandeye cli; do
  (cd "$SRC/packages/$p" && npm pack --pack-destination "$SITE/vendor" >/dev/null)
done
ls -1 "$SITE/vendor"
# Same version number, new contents: drop the lockfile so npm does not reinstall the cached old tarballs.
(cd "$SITE" && rm -rf node_modules package-lock.json && npm install --no-audit --no-fund)
