#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-diff}"

: "${PGHOST:?PGHOST is required}"
: "${PGPORT:=5432}"
: "${PGDATABASE:?PGDATABASE is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGPASSWORD:?PGPASSWORD is required}"

SCHEMA_FILE="${SCHEMA_FILE:-/app/schema.sql}"

case "$COMMAND" in
  diff)
    psqldef "$PGDATABASE" --file "$SCHEMA_FILE" --dry-run --enable-drop
    ;;
  apply)
    psqldef "$PGDATABASE" --file "$SCHEMA_FILE" --enable-drop
    ;;
  *)
    echo "usage: migrate.sh [diff|apply]" >&2
    exit 1
    ;;
esac