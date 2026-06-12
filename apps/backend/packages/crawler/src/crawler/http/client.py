from __future__ import annotations

import httpx
from crawler.http.retry import retry_http_call

BASE_URL = "https://www.wsl.waseda.jp/syllabus/JAA101.php"


def as_multipart_fields(data: dict[str, str]) -> dict[str, tuple[None, str]]:
    return {key: (None, value) for key, value in data.items()}


class WasedaSyllubasClient:
    def __init__(self, timeout=60.0) -> None:
        self._client = httpx.Client(
            base_url=BASE_URL, follow_redirects=True, timeout=timeout
        )

    def fetch_search_page(self, *, year: int, page: int, page_size: int) -> str:
        form = {
            "ControllerParameters": "JAA103SubCon",
            "nendo": str(year),
            "p_number": str(page_size),
            "p_page": str(page),
            "pLng": "jp",
        }

        def request() -> httpx.Response:
            return self._client(files=as_multipart_fields(form))

        response = retry_http_call(request)
        response.raise_for_status()
        return response.text

    def fetch_detail_page(self, *, pKey: str) -> str:
        def request() -> httpx.Response:
            return self._client(
                params={"pKey": pKey, "pLang": "jp"},
            )

        response = retry_http_call(request)
        response.raise_for_status()
        return response.text

    def close(self) -> None:
        self._client.close()
