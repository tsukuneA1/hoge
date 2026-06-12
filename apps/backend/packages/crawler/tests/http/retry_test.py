import httpx

from crawler.http.retry import retry_http_call


class TestRetryHttpCall:
    def test_returns_response_without_retry_when_status_is_200(self) -> None:
        response = httpx.Response(200)

        call_count = 0

        def fake_call() -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return response

        result = retry_http_call(fake_call)

        assert result is response
        assert call_count == 1

    def test_retries_retryable_status_and_return_success_response(self) -> None:
        retryable_response = httpx.Response(429)
        succeeded_response = httpx.Response(200)

        call_count = 0

        def fake_call() -> httpx.Response:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return retryable_response
            else:
                return succeeded_response
        
        result = retry_http_call(fake_call, base_delay_seconds=0)
        assert result is succeeded_response
        assert call_count == 2

