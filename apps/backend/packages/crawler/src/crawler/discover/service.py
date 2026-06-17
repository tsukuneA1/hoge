from libs.infrastructure.db.repositories import crawl_runs, crawl_targets

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

    pkeys = client.fetch_search_page(year=year, page_size=page_size)

    for pkey in pkeys:
        crawl_targets_repository.upsert(
            pkey=pkey,
            last_seen_run_id=run,
            discovered_year=year,
            source_page="hogehoge.html",
        )
