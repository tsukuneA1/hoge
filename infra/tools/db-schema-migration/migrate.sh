#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-diff}"

: "${PGHOST:?PGHOST is required}"
: "${PGPORT:=5432}"
: "${PGDATABASE:?PGDATABASE is required}"
: "${PGUSER:?PGUSER is required}"
: "${PGPASSWORD:?PGPASSWORD is required}"

SCHEMA_FILE="${SCHEMA_FILE:-/app/schema.sql}"

common_args=(
  "--host=${PGHOST}"
  "--port=${PGPORT}"
  "--user=${PGUSER}"
  "${PGDATABASE}"
  "--file=${SCHEMA_FILE}"
)

case "$COMMAND" in
  diff)
    psqldef "${common_args[@]}" --dry-run --enable-drop
    ;;
  apply)
    psqldef "${common_args[@]}" --enable-drop
    ;;
  *)
    echo "usage: migrate.sh [diff|apply]" >&2
    exit 1
    ;;
esac