from libs.infrastructure.db.repositories import crawl_runs, crawl_targets

from crawler.discover.parser import (
    extract_pkeys,
    extract_total_count,
)
from crawler.http.client import WasedaSyllabusClient


def run_discover_job(
    *,
    connection,
    crawl_runs_repository: crawl_runs.CrawlRunsRepository,
    crawl_targets_repository: crawl_targets.CrawlTargetsRepository,
    client: WasedaSyllabusClient,
    year: int,
    page_size: int,
) -> None:
    with connection.begin():
        run = crawl_runs_repository.start(job_type="discover")

    ingested_count = 0
    failed_count = 0
    errors = ""
    try:
        html = client.fetch_search_page(year=year, page_size=page_size, page=1)

        total_count = extract_total_count(html)

        pages = [(1, html)]

        for page in range(2, (total_count + page_size - 1) // page_size + 1):
            html = client.fetch_search_page(year=year, page_size=page_size, page=page)
            pages.append((page, html))

        for page, html in pages:
            try:
                pkeys = extract_pkeys(html)
                with connection.begin():
                    for pkey in pkeys:
                        crawl_targets_repository.upsert(
                            pkey=pkey,
                            last_seen_run_id=run.id,
                            discovered_year=year,
                            source_page=page,
                        )
                ingested_count += len(pkeys)
            except Exception as exc:
                failed_count += 1
                errors.append(str(exc))

        if failed_count == 0:
            status = "succeeded"
        elif ingested_count == 0 and total_count > 0:
            status = "failed"
        else:
            status = "partially_succeeded"

        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status=status,
                discovered_count=total_count,
                ingested_count=ingested_count,
                failed_count=failed_count,
                error_message=errors,
            )
    except Exception as exc:
        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status="failed",
                discovered_count=total_count,
                ingested_count=ingested_count,
                failed_count=failed_count,
                error_message=str(exc),
            )
        raise
