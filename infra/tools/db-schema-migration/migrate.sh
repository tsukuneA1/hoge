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
    PGPASSWORD=$(DB_PASSWORD) psqldef -h $(DB_HOST) -U $(DB_USER) -p $(DB_PORT) $(DB_NAME) --dry-run --enable-drop < schema.sql
    ;;
  apply)
    PGPASSWORD=$(DB_PASSWORD) psqldef -h $(DB_HOST) -U $(DB_USER) -p $(DB_PORT) $(DB_NAME) --enable-drop < schema.sql
    ;;
  *)
    echo "usage: migrate.sh [diff|apply]" >&2
    exit 1
    ;;
esac