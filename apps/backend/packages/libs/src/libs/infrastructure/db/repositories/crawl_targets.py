from libs.infrastructure.db.gen import crawl_targets, models
from sqlalchemy import Connection


class CrawlTargetsRepository:
    def __init__(self, connection: Connection):
        self.querier = crawl_targets.Querier(connection)

    def list_ingest_targets(
        self, limit: int, max_attempts: int, lease_timeout_seconds: float
    ) -> list[models.CrawlTarget]:
        return list(
            self.querier.list_ingest_targets(
                max_attempts=max_attempts,
                lease_timeout_seconds=lease_timeout_seconds,
                row_limit=limit,
            )
        )

    def success(self, pkey: str) -> models.CrawlTarget:
        target = self.querier.mark_crawl_target_succeeded(pkey=pkey)
        if target is None:
            return ValueError("db returned None")
        return target

    def fail(self, *, last_error: str | None, pkey: str) -> models.CrawlTarget:
        target = self.querier.mark_crawl_target_failed(pkey=pkey, last_error=last_error)
        if target is None:
            return ValueError("db returned None")
        return target

    def running(self, pkey: str) -> models.CrawlTarget:
        target = self.querier.mark_crawl_target_running(pkey=pkey)
        if target is None:
            return ValueError("db returned None")
        return target

    def upsert(
        self,
        pkey: str,
        last_seen_run_id: int | None,
        discovered_year: int,
        source_page: int,
    ) -> models.CrawlTarget:
        target = self.querier.upsert_crawl_target(
            pkey=pkey,
            last_seen_run_id=last_seen_run_id,
            discovered_year=discovered_year,
            source_page=source_page,
        )
        if target is None:
            return ValueError("db returned None")
        return target
