#!/bin/bash
# AEP0.2 profile: record this unit as a Pioreactor 40ml XR v1.5 so the
# "Update Pioreactor model" dialog never appears. Only touches a unit whose
# model is still unset. A worker's model is set by the leader when it is added.
set -e
PIO=/usr/local/bin/pio
[ -x "$PIO" ] || PIO=/opt/pioreactor/venv/bin/pio
DB=$("$PIO" config get storage database 2>/dev/null) || exit 0
[ -f "$DB" ] || exit 0
sqlite3 "$DB" "UPDATE workers SET model_name='pioreactor_40ml_XR', model_version='1.5' WHERE pioreactor_unit='$(hostname)' AND model_name IS NULL;"
