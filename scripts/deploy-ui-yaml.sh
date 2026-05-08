#!/usr/bin/env bash
# Copy the plugin's UI job descriptor into Pioreactor's plugin scan path.
set -euo pipefail

PLUGIN=$(/opt/pioreactor/venv/bin/python -c "import pioreactor_electropioreactor_plugin, os; print(os.path.dirname(pioreactor_electropioreactor_plugin.__file__))")
TARGET_DIR="$HOME/.pioreactor/plugins/ui/jobs"
TARGET="$TARGET_DIR/20_electropioreactor.yaml"

mkdir -p "$TARGET_DIR"
cp "$PLUGIN/ui/contrib/jobs/electropioreactor.yaml" "$TARGET"
echo "Deployed: $TARGET"
