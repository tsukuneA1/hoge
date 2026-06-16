from collections.abc import Iterator
from sqlalchemy import Connection

from libs.infrastructure.db.gen import crawl_targets, models


class CrawlTargetsRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = crawl_targets.Querier(conn=connection)

    def list(self, limit: int, max_attempts: int, lease_timeout: float) -> Iterator[models.CrawlTarget]:
        return self.querier.list_ingest_targets(
            max_attempts=max_attempts,
            lease_timeout_seconds=lease_timeout,
            row_limit=limit,
        )

    def success(self, pkey: str):
        self.querier.mark_crawl_target_succeeded(pkey=pkey)

    def fail(self, *, last_error: str | None, pkey: str):
        self.querier.mark_crawl_target_failed(pkey=pkey, last_error=last_error)

    def upsert(
        self,
        pkey: str,
        last_seen_run_id: int | None,
        discovered_year: int,
        source_page: int,
    ):
        self.querier.upsert_crawl_target(
            pkey=pkey,
            last_seen_run_id=last_seen_run_id,
            discovered_year=discovered_year,
            source_page=source_page,
        )
