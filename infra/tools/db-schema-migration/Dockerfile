FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# sqldef install
ARG SQLDEF_VERSION=v3.10.0
RUN wget https://github.com/sqldef/sqldef/releases/download/${SQLDEF_VERSION}/psqldef_linux_amd64.tar.gz \
    && tar -zxvf psqldef_linux_amd64.tar.gz \
    && mv psqldef /usr/local/bin \
    && rm psqldef_linux_amd64.tar.gz

WORKDIR /app

COPY apps/backend/sqlc/schema.sql /app/schema.sql
COPY infra/tools/db-schema-migration/migrate.sh /app/migrate.sh

RUN chmod +x /app/migrate.sh

ENTRYPOINT ["/app/migrate.sh"]
CMD ["diff"]