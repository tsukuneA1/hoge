import argparse
from logging import getLogger

import sqlalchemy
from libs.config import DatabaseSettings
from libs.logging import configure_logging

from crawler.discover.service import run_discover_job
from crawler.http.client import WasedaSyllabusClient

logger = getLogger(__name__)


def _get_engine() -> sqlalchemy.Engine:
    settings = DatabaseSettings()
    return sqlalchemy.createEngine(settings.sqlalchemy_database_url)


def main() -> None:
    configure_logging()

    parser = argparse.ArgumentParser(prog="crawler")

    subparsers = parser.add_subparsers(dest="command", required=True)

    discover_parser = subparsers.add_parser("discover")
    discover_parser.add_argument("--year", type=int, required=True)
    discover_parser.add_argument("--page-size", type=int, default=2000)

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("--limit", type=int, default=10)
    ingest_parser.add_argument("--max-attempts", type=int, default=3)

    args = parser.parse_args()

    # Composition Root
    if args.command == "discover":
        with WasedaSyllabusClient() as client:
            run_discover_job(client=client, year=args.year, page_size=args.page_size)
    elif args.command == "ingest":
        print("ingest", args.limit, args.max_attempts)

    # with WasedaSyllabusClient() as client:
    #     r = client.fetch_search_page(year=2026, page=1, page_size=100)
    #     pkeys = extract_pkeys(r)
    #     logger.info(pkeys)
    #     for key in pkeys:
    #         r = client.fetch_detail_page(pKey=key)
    #         course = parse_course_detail(r)
    #         logger.info(course)


if __name__ == "__main__":
    main()
