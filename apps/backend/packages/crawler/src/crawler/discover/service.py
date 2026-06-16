from libs.infrastructure.db.repositories import crawl_runs, crawl_targets

from crawler.http.client import WasedaSyllabusClient


def run_discover_job(
    *,
    crawl_runs_repository: crawl_runs.CrawlRunsRepository,
    crawl_targets_repository: crawl_targets.CrawlTargetsRepository,
    client: WasedaSyllabusClient,
    limit: int,
    max_attempts: int,
) -> None:
    run = crawl_runs_repository.start(job_type="discover")

    pkeys = client.fetch_search_page(year=2026, page_size=limit)

    for pkey in pkeys:
        crawl_targets_repository.upsert(
            pkey=pkey,
            last_seen_run_id=run,
            discovered_year=2026,
            source_page="hogehoge.html",
        )
