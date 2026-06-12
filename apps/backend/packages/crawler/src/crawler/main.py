from crawler.http.client import WasedaSyllabusClient
from libs.logging import configure_logging
from logging import getLogger

logger = getLogger(__name__)

def main() -> None:
    configure_logging()

    with WasedaSyllabusClient() as client:
        r = client.fetch_search_page(year=2026, page=1, page_size=2000)
        print(r)


if __name__ == "__main__":
    main()
