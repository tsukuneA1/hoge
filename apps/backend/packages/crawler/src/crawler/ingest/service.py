from libs.infrastructure.db.repositories import courses, crawl_runs, crawl_targets

from crawler.http.client import WasedaSyllabusClient
from crawler.ingest.parser import parse_course_detail


def run_ingest_job(
    *,
    connection,
    crawl_runs_repository: crawl_runs.CrawlRunsRepository,
    crawl_targets_repository: crawl_targets.CrawlTargetsRepository,
    courses_repository: courses.CoursesRepository,
    client: WasedaSyllabusClient,
    limit: int,
    max_attempts: int,
) -> None:
    with connection.begin():
        run = crawl_runs_repository.start(job_type="ingest")

    with connection.begin():
        targets = crawl_targets_repository.list_ingest_targets(
            limit=limit, max_attempts=max_attempts, lease_timeout_seconds=5.0
        )

    discovered_count = len(targets)
    ingested_count = 0

    try:
        for target in targets:
            html = client.fetch_detail_page(pKey=target.pkey)
            parsed_course = parse_course_detail(html)

            with connection.begin():
                crawl_targets_repository.mark_succeeded(pkey=target.pkey)
                courses_repository.upsert(*parsed_course)
            ingested_count += 1
        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status='succeeded',
                discovered_count=discovered_count,
                ingested_count=ingested_count,
                failed_count=0,
            )

    except Exception as exc:
        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status='failed',
                discovered_count=discovered_count,
                ingested_count=ingested_count,
                failed_count=discovered_count-ingested_count,
                error_message=str(exc)
            )
