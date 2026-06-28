SQLC_DIR := sqlc
DB_HOST ?= localhost
DB_PORT ?= 5432
DB_NAME ?= hoge_db
DB_USER ?= postgres
DB_PASSWORD ?= password
GO        ?= go

.PHONY: fmt
fmt:
	uv run ruff format .
	uv run ruff check . --fix

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: typecheck
typecheck:
	uv run mypy

.PHONY: test
test:
	uv run --all-packages pytest

.PHONY: check
check: lint typecheck test

.PHONY: sqlc
sqlc:
	cd $(SQLC_DIR) && $(GO) tool sqlc generate -f sqlc.yaml

.PHONY: dry-migrate
dry-migrate:
	cd $(SQLC_DIR) && PGPASSWORD=$(DB_PASSWORD) $(GO) tool psqldef -h $(DB_HOST) -U $(DB_USER) -p $(DB_PORT) $(DB_NAME) --dry-run --enable-drop < schema.sql

.PHONY: migrate
migrate:
	cd $(SQLC_DIR) && PGPASSWORD=$(DB_PASSWORD) $(GO) tool psqldef -h $(DB_HOST) -U $(DB_USER) -p $(DB_PORT) $(DB_NAME) --enable-drop < schema.sql