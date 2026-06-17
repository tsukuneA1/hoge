from libs.infrastructure.db.repositories import crawl_runs, crawl_targets

from crawler.discover.parser import (
    extract_pkeys,
    extract_total_count,
)
from crawler.http.client import WasedaSyllabusClient


def run_discover_job(
    *,
    crawl_runs_repository: crawl_runs.CrawlRunsRepository,
    crawl_targets_repository: crawl_targets.CrawlTargetsRepository,
    client: WasedaSyllabusClient,
    year: int,
    page_size: int,
) -> None:
    run = crawl_runs_repository.start(job_type="discover")

    html = client.fetch_search_page(year=year, page_size=page_size, page=1)

    total_count = extract_total_count(html)

    for page in range(1, (total_count + page_size - 1) // page_size):
        html = client.fetch_search_page(year=year, page_size=page_size, page=page)
        pkeys = extract_pkeys(html)
        for pkey in pkeys:
            crawl_targets_repository.upsert(
                pkey=pkey,
                last_seen_run_id=run.id,
                discovered_year=year,
                source_page=page,
            )
