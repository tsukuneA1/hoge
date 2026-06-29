FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# sqldef install
# COPY sqldef or curl release binary

WORKDIR /app

COPY apps/backend/sqlc/schema.sql /app/schema.sql
COPY infra/tools/db-schema-migration/migrate.sh /app/migrate.sh

RUN chmod +x /app/migrate.sh

ENTRYPOINT ["/app/migrate.sh"]
CMD ["diff"]