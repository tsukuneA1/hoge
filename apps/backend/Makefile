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
	cd sqlc && sqlc generate

.PHONY: sqlc-fmt
sqlc-fmt:
	cd sqlc && sqlfluff fix query/backend && sqlfluff fix schema.sql