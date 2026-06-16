from libs.infrastructure.db.gen import crawl_runs, models
from sqlalchemy import Connection


class CrawlRunsRepository:
    def __init__(self, connection: Connection):
        self.querier = crawl_runs.Querier(connection)

    def start(self, job_type: models.CrawlJobType) -> models.CrawlRun | None:
        start_run = self.querier.create_crawl_run(job_type=job_type)
        if start_run is None:
            raise ValueError("db returned None")
        return start_run

    def finish(self, params: crawl_runs.FinishCrawlRunParams) -> models.CrawlRun | None:
        finish_run = self.querier.finish_crawl_run(params)
        if finish_run is None:
            raise ValueError("db returned None")
        return finish_run
