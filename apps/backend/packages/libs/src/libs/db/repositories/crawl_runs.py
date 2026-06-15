from sqlalchemy import Connection

from libs.db.gen import crawl_runs, models


class CrawlRunsRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = crawl_runs.Querier(connection)

    def start(self, job_type: models.CrawlJobType) -> models.CrawlRun:
        return self.querier.create_crawl_run(job_type=job_type)

    def finish(
        self,
        *,
        run_id: int,
        status: models.CrawlRunStatus,
        failed_count: int = 0,
        error_message: str | None = None,
    ) -> models.CrawlRun:
        return self.querier.finish_crawl_run(
            id=run_id,
            status=status,
            failed_count=failed_count,
            error_message=error_message,
        )
