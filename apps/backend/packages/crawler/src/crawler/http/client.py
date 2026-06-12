from __future__ import annotations

import httpx
from crawler.http.retry import retry_http_call

BASE_URL = "https://www.wsl.waseda.jp/syllabus"


def as_multipart_fields(data: dict[str, str]) -> dict[str, tuple[None, str]]:
    """
        大学のAPIは一覧検索をPOST methodのbodyに入っているパラメータで判定している。
        その内検索条件はquery paramater(params)やbody生データ(data)では受け取られずfileアップロードのみ対応している。
        この関数ではmultipart/form-dataのContent Typeで送信できるようdictを受け取ってそれ用のdictに変換している。
    """

    return {key: (None, value) for key, value in data.items()}


class WasedaSyllabusClient:
    def __init__(self, timeout: float = 60.0) -> None:
        self._client = httpx.Client(
            base_url=BASE_URL, follow_redirects=True, timeout=timeout, headers={
                "User-Agent": "syllabus-crawler/0.1"
            }
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
            return self._client.post("/JAA101.php", files=as_multipart_fields(form))

        response = retry_http_call(request)
        response.raise_for_status()
        return response.text

    def fetch_detail_page(self, *, pKey: str) -> str:
        def request() -> httpx.Response:
            return self._client.get(
                "/JAA104.php",
                params={"pKey": pKey, "pLng": "jp"},
            )

        response = retry_http_call(request)
        response.raise_for_status()
        return response.text

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> WasedaSyllabusClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
