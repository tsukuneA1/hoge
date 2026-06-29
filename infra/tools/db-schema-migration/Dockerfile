FROM golang:1.24-bookworm AS builder

WORKDIR /src

COPY apps/backend/sqlc/go.mod apps/backend/sqlc/go.sum ./

RUN go install github.com/sqldef/sqldef/cmd/psqldef

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /go/bin/psqldef /usr/local/bin/psqldef

COPY apps/backend/sqlc/schema.sql /app/schema.sql
COPY infra/tools/db-schema-migration/migrate.sh /app/migrate.sh

RUN chmod +x /app/migrate.sh

ENTRYPOINT ["/app/migrate.sh"]
CMD ["diff"]
