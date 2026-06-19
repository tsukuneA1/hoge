from dataclasses import asdict

import sqlalchemy
from libs.infrastructure.db.repositories import courses, crawl_runs, crawl_targets

from crawler.http.client import WasedaSyllabusClient
from crawler.ingest.parser import parse_course_detail


def run_ingest_job(
    *,
    connection: sqlalchemy.Connection,
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
            # NOTE: detail fetch は最悪 timeout10s×retry3 ≒ 30s。安全係数2倍で60s。
            limit=limit, max_attempts=max_attempts, lease_timeout_seconds=60.0
        )

        for target in targets:
            crawl_targets_repository.mark_running(pkey=target.pkey)

    discovered_count = len(targets)
    ingested_count = 0
    failed_count = 0

    try:
        for target in targets:
            try:
                html = client.fetch_detail_page(pKey=target.pkey)
                parsed_course = parse_course_detail(html)

                with connection.begin():
                    courses_repository.upsert(pkey=target.pkey, **asdict(parsed_course))
                    crawl_targets_repository.mark_succeeded(pkey=target.pkey)

                ingested_count += 1

            except Exception as exc:
                failed_count += 1
                with connection.begin():
                    crawl_targets_repository.mark_failed(
                        pkey=target.pkey, last_error=str(exc)
                    )
        if failed_count == 0:
            status = "succeeded"
        elif ingested_count == 0 and discovered_count > 0:
            status = "failed"
        else:
            status = "partially_succeeded"

        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status=status,
                discovered_count=discovered_count,
                ingested_count=ingested_count,
                failed_count=failed_count,
            )

    except Exception as exc:
        with connection.begin():
            crawl_runs_repository.finish(
                id=run.id,
                status="failed",
                discovered_count=discovered_count,
                ingested_count=ingested_count,
                failed_count=discovered_count - ingested_count,
                error_message=str(exc),
            )
        raise
