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
    max_attempts=3,
    base_delay_seconds=1.0,
    max_delay_seconds=8.0,
) -> httpx.Response:
    last_exec: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = call()

            if not is_retryable(response):
                return response

            if attempt == max_attempts:
                return response

        except (httpx.TimeoutException, httpx.NetworkError) as exec:
            last_exec = exec

            if attempt == max_attempts:
                raise

        delay = min(max_delay_seconds, 2 ** (attempt - 1) * base_delay_seconds)
        time.sleep(delay)

    if last_exec:
        raise last_exec

    raise RuntimeError("unreachable retry state")
