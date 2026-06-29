#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-diff}"

: "${PGHOST:?PGHOST is required}"
: "${PGPORT:=5432}"
: "${PGDATABASE:?PGDATABASE is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGPASSWORD:?PGPASSWORD is required}"

case "$COMMAND" in
  diff)
    # dry-run / diff
    ;;
  apply)
    # apply
    ;;
  *)
    echo "usage: migrate.sh [diff|apply]" >&2
    exit 1
    ;;
esac