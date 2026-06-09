.PHONY: format lint typecheck test check sqlc sqlc-fmt

fmt:
	uv run ruff format .
	uv run ruff check . --fix

lint:
	uv run ruff check .

typecheck:
	uv run mypy

test:
	uv run pytest

check: lint typecheck test

sqlc:
	cd sqlc && sqlc generate

sqlc-fmt:
	cd sqlc && sqlfluff fix query/backend && sqlfluff fix schema.sql