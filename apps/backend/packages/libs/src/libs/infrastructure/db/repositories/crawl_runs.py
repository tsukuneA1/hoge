from libs.infrastructure.db.gen import crawl_runs, models
from sqlalchemy import Connection


class CrawlRunsRepository:
    def __init__(self, connection: Connection):
        self.querier = crawl_runs.Querier(connection)

    def start(self, job_type: models.CrawlJobType) -> models.CrawlRun:
        start_run = self.querier.create_crawl_run(job_type=job_type)
        if start_run is None:
            raise ValueError("db returned None")
        return start_run

    def finish(
        self,
        id: int,
        status: str,
        discovered_count: int,
        ingested_count: int,
        failed_count: int,
        error_message: str | None = None,
    ) -> models.CrawlRun:
        params = crawl_runs.FinishCrawlRunParams(
            id=id,
            status=models.CrawlRunStatus(status),
            discovered_count=discovered_count,
            ingested_count=ingested_count,
            failed_count=failed_count,
            error_message=error_message,
        )
        finish_run = self.querier.finish_crawl_run(params)
        if finish_run is None:
            raise ValueError("db returned None")
        return finish_run
