import asyncio

import httpx

from speed_run import fetch_all, fetch_all_limited, fetch_all_safe, fetch_one


URLS = [f"https://example.com/page/{i}" for i in range(20)]


class TrackingTransport(httpx.AsyncBaseTransport):
    def __init__(self):
        self.running = 0
        self.max_running = 0

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self.running += 1
        self.max_running = max(self.max_running, self.running)
        try:
            await asyncio.sleep(0.05 if "slow" in request.url.path else 0.005)
            return httpx.Response(
                200,
                text=f"<html><body>{request.url}</body></html>",
                request=request,
            )
        finally:
            self.running -= 1


def run_with_client(operation):
    async def run():
        transport = TrackingTransport()
        async with httpx.AsyncClient(transport=transport) as client:
            result = await operation(client)
        return result, transport.max_running

    return asyncio.run(run())


def test_fetch_one():
    url = URLS[0]
    result, _ = run_with_client(lambda client: fetch_one(client, url))
    assert result == (url, len(f"<html><body>{url}</body></html>"))


def test_fetch_all_runs_concurrently_and_preserves_order():
    result, max_running = run_with_client(lambda client: fetch_all(client, URLS))
    assert [url for url, _ in result] == URLS
    assert max_running > 10


def test_fetch_all_limited_respects_limit_and_runs_in_parallel():
    result, max_running = run_with_client(
        lambda client: fetch_all_limited(client, URLS, limit=3)
    )
    assert [url for url, _ in result] == URLS
    assert max_running == 3


def test_fetch_all_safe_times_out_slow_pages():
    urls = URLS[:5] + [
        "https://example.com/slow/1",
        "https://example.com/slow/2",
    ]
    result, _ = run_with_client(
        lambda client: fetch_all_safe(client, urls, timeout=0.02)
    )
    by_url = dict(result)
    assert by_url["https://example.com/slow/1"] is None
    assert by_url["https://example.com/slow/2"] is None
    assert all(by_url[url] for url in URLS[:5])


def test_fetch_all_limited_rejects_nonpositive_limit():
    async def run():
        async with httpx.AsyncClient() as client:
            await fetch_all_limited(client, URLS, limit=0)

    try:
        asyncio.run(run())
    except ValueError as error:
        assert str(error) == "limit must be greater than zero"
    else:
        raise AssertionError("expected ValueError for a nonpositive limit")
