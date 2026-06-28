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

SQLC_DIR := sqlc
DB_HOST ?= localhost
DB_PORT ?= 5432
DB_NAME ?= hoge_db
DB_USER ?= postgres
DB_PASSWORD ?= password

.PHONY: sqlc
sqlc:
	cd $(SQLC_DIR) && go run github.com/sqlc-dev/sqlc/cmd/sqlc generate

.PHONY: dry-migrate
dry-migrate:
	cd $(SQLC_DIR) && PGPASSWORD=$(DB_PASSWORD) go run github.com/sqldef/sqldef/cmd/psqldef \
		-h $(DB_HOST) \
		-p $(DB_PORT) \
		-U $(DB_USER) \
		--dry-run \
		$(DB_NAME) \
		< schema.sql

.PHONY: migrate
migrate:
	cd $(SQLC_DIR) && PGPASSWORD=$(DB_PASSWORD) go run github.com/sqldef/sqldef/cmd/psqldef \
		-h $(DB_HOST) \
		-p $(DB_PORT) \
		-U $(DB_USER) \
		$(DB_NAME) \
		< schema.sql