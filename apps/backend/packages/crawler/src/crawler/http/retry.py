from __future__ import annotations

from collections.abc import Callable

import httpx
import time

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def is_retryable(response: httpx.Response) -> bool:
    return response.status_code in RETRYABLE_STATUS_CODES


def retry_http_call(
    call: Callable[[], httpx.Response],
    *,
    max_attempts: int = 3,
    base_delay_seconds: float = 1.0,
    max_delay_seconds: float = 8.0,
) -> httpx.Response:
    last_exc: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = call()

            if not is_retryable(response):
                return response

            if attempt == max_attempts:
                return response

        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            last_exc = exc

            if attempt == max_attempts:
                raise
        
        # NOTE: discover jobは単一のbatch jobで動く想定の為jitterはなし。ingest jobは分散するとして2,3個なのでこちらもjitterを付ける必要なしと判断した
        delay = min(max_delay_seconds, 2 ** (attempt - 1) * base_delay_seconds)
        time.sleep(delay)

    if last_exc:
        raise last_exc

    raise RuntimeError("unreachable retry state")
