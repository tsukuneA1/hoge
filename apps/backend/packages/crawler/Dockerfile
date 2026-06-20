FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

RUN groupadd -g 1000 app && useradd -r -u 1000 -g app -m app && \
    mkdir -p /home/app/.cache/uv && \
    chown -R app:app /app /home/app/.cache
USER app

COPY --chown=app:app pyproject.toml uv.lock ./
COPY --chown=app:app packages/ /app/packages/

RUN --mount=type=cache,target=/home/app/.cache/uv,uid=1000,gid=1000 \
    uv sync --frozen --no-dev --no-editable --package crawler

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 app && useradd -r -u 1000 -g app -m app && \
    chown app:app /app
USER app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["crawler"]
CMD ["--help"]