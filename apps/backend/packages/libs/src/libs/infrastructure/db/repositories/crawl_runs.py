from typing import Optional
from sqlalchemy import Connection

from libs.infrastructure.db.gen import crawl_runs, models


class CrawlRunsRepository:
    def __init__(self, connection: Connection):
        self.conn = connection
        self.querier = crawl_runs.Querier(connection)

    def start(self, job_type: models.CrawlJobType) -> Optional[models.CrawlRun]:
        return self.querier.create_crawl_run(job_type=job_type)

    def finish(self, params: crawl_runs.FinishCrawlRunParams) -> Optional[models.CrawlRun]:
        return self.querier.finish_crawl_run(params)
