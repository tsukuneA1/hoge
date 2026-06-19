import argparse
from logging import getLogger

import sqlalchemy
from libs.config import DatabaseSettings
from libs.infrastructure.db.repositories import courses, crawl_runs, crawl_targets
from libs.logging import configure_logging

from crawler.discover.service import run_discover_job
from crawler.http.client import WasedaSyllabusClient
from crawler.ingest.service import run_ingest_job

logger = getLogger(__name__)


def _get_engine() -> sqlalchemy.Engine:
    settings = DatabaseSettings()
    return sqlalchemy.create_engine(settings.sqlalchemy_database_url)


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(prog="crawler")

    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover")
    discover_parser.add_argument("--year", type=int, required=True)
    discover_parser.add_argument("--page-size", type=int, default=1000)

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("--limit", type=int, default=10)
    ingest_parser.add_argument("--max-attempts", type=int, default=3)

    args = parser.parse_args()

    # Composition Root
    if args.command == "discover":
        engine = _get_engine()

        with engine.connect() as conn:
            crawl_runs_repository = crawl_runs.CrawlRunsRepository(connection=conn)
            crawl_targets_repository = crawl_targets.CrawlTargetsRepository(
                connection=conn
            )

            with WasedaSyllabusClient() as client:
                run_discover_job(
                    connection=conn,
                    crawl_runs_repository=crawl_runs_repository,
                    crawl_targets_repository=crawl_targets_repository,
                    client=client,
                    year=args.year,
                    page_size=args.page_size,
                )
    elif args.command == "ingest":
        engine = _get_engine()

        with engine.connect() as conn:
            crawl_runs_repository = crawl_runs.CrawlRunsRepository(connection=conn)
            crawl_targets_repository = crawl_targets.CrawlTargetsRepository(
                connection=conn
            )
            courses_repository = courses.CoursesRepository(connection=conn)

            with WasedaSyllabusClient() as client:
                run_ingest_job(
                    connection=conn,
                    crawl_runs_repository=crawl_runs_repository,
                    crawl_targets_repository=crawl_targets_repository,
                    courses_repository=courses_repository,
                    client=client,
                    limit=args.limit,
                    max_attempts=args.max_attempts,
                )


if __name__ == "__main__":
    main()
