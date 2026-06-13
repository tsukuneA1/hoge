from crawler.http.client import WasedaSyllabusClient
from crawler.discover.parser import extract_pkeys
from crawler.ingest.parser import parse_course_detail
from libs.logging import configure_logging

from logging import getLogger

logger = getLogger(__name__)


def main() -> None:
    configure_logging()

    with WasedaSyllabusClient() as client:
        r = client.fetch_search_page(year=2026, page=1, page_size=100)
        pkeys = extract_pkeys(r)
        logger.info(pkeys)
        for key in pkeys:
            r = client.fetch_detail_page(pKey=key)
            course = parse_course_detail(r)
            logger.info(course)


if __name__ == "__main__":
    main()
