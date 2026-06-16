from libs.infrastructure.db.gen import crawl_runs, models
from sqlalchemy import Connection


class CrawlRunsRepository:
    def __init__(self, connection: Connection):
        self.querier = crawl_runs.Querier(connection)

    def start(self, job_type: models.CrawlJobType) -> models.CrawlRun | None:
        return self.querier.create_crawl_run(job_type=job_type)

    def finish(self, params: crawl_runs.FinishCrawlRunParams) -> models.CrawlRun | None:
        return self.querier.finish_crawl_run(params)
