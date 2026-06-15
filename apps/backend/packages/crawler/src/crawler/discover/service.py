from libs.db.gen.models import CrawlJobType
from libs.db.gen.crawl_runs import Querier as CrawlRunsQuerier

CrawlRunsQuerier.create_crawl_run(job_type=CrawlJobType.DISCOVER)
